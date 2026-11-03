#!/usr/bin/env python3
"""Check the Graal Technical Reference Manual under `manual/`.

Standard library only; runs on Linux, macOS and Windows.

    python tools/manual/check_manual.py            # normal check
    python tools/manual/check_manual.py --final    # also fail on `pending` rows

The rules are described in `manual/00-conventions.md` (section 0.11).
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

NOTE_SUFFIXES = {'.md', '.tsv', '.toml', '.txt'}
SKIP_DIRS = {'.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'venv'}
SOURCES_HEADER = ['path', 'status', 'sections', 'planned', 'reason']
STATUSES = {'pending', 'cited', 'excluded'}
KINDS = {'reference', 'front', 'index'}
FILE_STATUSES = {'stub', 'draft', 'complete'}

HEADER_RE = re.compile(r'^<!--\s*manual:\s*kind=(\w+)\s+status=(\w+)\s*-->\s*$')
EVIDENCE_TAGS = (
    'bin', 'file', 'doc', 'srv', 'src', 'lab', 'live', 'cap', 'wire', 'run',
    'shot', 'test', 'inf', 'GE', 'checked',
)
# A build tag: [2.05], [1.39], [4.20r8], [5.12], [6.03r7], [2.05rev2] ...
_TAG = r'\[(?:' + '|'.join(EVIDENCE_TAGS) + r'|\d+\.\d+[0-9A-Za-z.\-]*)\]'
TAG_RE = re.compile(_TAG)
# One or more tags, optional spaces, then a parenthesised source list.
CITE_RE = re.compile(r'((?:' + _TAG + r')+)\s*\(([^()]+)\)')
HEADING_RE = re.compile(r'^(#{1,6})\s+(.*\S)\s*$')
NUM_HEADING_RE = re.compile(r'^(?:Appendix\s+)?((?:\d+|[A-G])(?:\.\d+)*)[.\s]')
ENTRY_HEADING_RE = re.compile(r'^([A-G]#\d+)\b')
SECTION_REF_RE = re.compile(r'§\s?(\d+(?:\.\d+)*)')
APP_REF_RE = re.compile(r'App\.\s?([A-G])(?:#(\d+))?')
XREF_ONLY_RE = re.compile(r'→\s*(?:§|App\.)')
INLINE_CODE_RE = re.compile(r'`[^`]*`')
TABLE_SEP_RE = re.compile(r'^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$')

LEAK_PATTERNS = (
    (re.compile(r'\b(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}'), 'disassembler name'),
    (re.compile(r'\b0x00[4-6][0-9a-fA-F]{5}\b'), 'code address'),
    (re.compile(r'(?<![0-9A-Za-z])00[4-6][0-9a-fA-F]{5}(?![0-9A-Za-z])'), 'bare code address'),
    (re.compile(r'graalonline\.com|graal\.in\b|graalreborn\.(?:com|net)', re.I), 'official hostname'),
    (re.compile(r'\blocalhost\b', re.I), 'loopback literal'),
)
IPV4_RE = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
VERSION_LIKE_RE = re.compile(r'^[0-9]\.[0-9]+\.[0-9]+\.[0-9]+$')

# Source tables for the id completeness check.
PACKET_IDS_NOTE = 'protocol/packet-ids.md'
PROPS_NOTE = 'protocol/player-props.md'
MESSAGE_NAME_RE = re.compile(r'`((?:PLI|PLO)_[A-Z0-9_]+)`')
PROP_SECTIONS = {'PLPROP': 'PLPROP', 'NPCPROP': 'NPCPROP', 'BDPROP': 'BDPROP'}


@dataclass
class ManualFile:
    path: Path
    rel: str
    kind: str = ''
    status: str = ''
    number: str = ''
    lines: list[str] = field(default_factory=list)


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)

    def add(self, where: str, message: str) -> None:
        self.errors.append(f'{where}: {message}')


def _posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def walk_notes(root: Path) -> list[str]:
    """Every note in the repository (outside `manual/`), as POSIX paths."""
    notes = []
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if rel.parts and rel.parts[0] == 'manual':
            continue
        if path.is_file() and path.suffix.lower() in NOTE_SUFFIXES:
            notes.append(rel.as_posix())
    return notes


def load_manual(root: Path, report: Report) -> list[ManualFile]:
    manual = root / 'manual'
    files = []
    for path in sorted(manual.rglob('*.md')):
        rel = _posix(path, root)
        if 'pdf' in path.relative_to(manual).parts:
            continue
        text = path.read_text(encoding='utf-8')
        lines = text.splitlines()
        mf = ManualFile(path=path, rel=rel, lines=lines)
        if rel == 'manual/README.md':
            mf.kind, mf.status = 'front', 'complete'
        else:
            match = HEADER_RE.match(lines[0]) if lines else None
            if not match:
                report.add(f'{rel}:1', 'missing `<!-- manual: kind=K status=S -->` header')
            else:
                mf.kind, mf.status = match.group(1), match.group(2)
                if mf.kind not in KINDS:
                    report.add(f'{rel}:1', f'unknown kind {mf.kind!r}')
                if mf.status not in FILE_STATUSES:
                    report.add(f'{rel}:1', f'unknown status {mf.status!r}')
        for line in lines:
            heading = HEADING_RE.match(line)
            if heading and len(heading.group(1)) == 1:
                num = NUM_HEADING_RE.match(heading.group(2))
                if num:
                    mf.number = num.group(1)
                break
        files.append(mf)
    return files


def collect_anchors(files: list[ManualFile]) -> tuple[set[str], set[str]]:
    sections: set[str] = set()
    entries: set[str] = set()
    for mf in files:
        in_code = False
        for line in mf.lines:
            if line.startswith('```'):
                in_code = not in_code
                continue
            if in_code:
                continue
            heading = HEADING_RE.match(line)
            if not heading:
                continue
            title = heading.group(2)
            entry = ENTRY_HEADING_RE.match(title)
            if entry:
                entries.add(entry.group(1))
                continue
            num = NUM_HEADING_RE.match(title)
            if num:
                sections.add(num.group(1))
    return sections, entries


def iter_body(mf: ManualFile):
    """Yield (line_no, line, kind) for lines outside code blocks and comments.

    kind is one of: heading, blank, quote, table-head, table-sep, table-row,
    item, text.
    """
    in_code = False
    in_comment = False
    prev_table = False
    for no, line in enumerate(mf.lines, 1):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            prev_table = False
            continue
        if in_code:
            continue
        if in_comment:
            if '-->' in stripped:
                in_comment = False
            continue
        if stripped.startswith('<!--'):
            if '-->' not in stripped:
                in_comment = True
            continue
        if not stripped:
            prev_table = False
            yield no, line, 'blank'
        elif HEADING_RE.match(stripped):
            prev_table = False
            yield no, line, 'heading'
        elif stripped.startswith('>'):
            prev_table = False
            yield no, line, 'quote'
        elif stripped.startswith('|'):
            if TABLE_SEP_RE.match(stripped):
                yield no, line, 'table-sep'
            elif not prev_table:
                yield no, line, 'table-head'
            else:
                yield no, line, 'table-row'
            prev_table = True
        elif re.match(r'^([-*+]|\d+\.)\s', stripped):
            prev_table = False
            yield no, line, 'item'
        else:
            prev_table = False
            yield no, line, 'text'


def split_sources(group: str) -> list[str]:
    out = []
    for part in group.split(';'):
        part = part.strip().strip('`').strip()
        if not part:
            continue
        out.append(part.split('#', 1)[0].strip())
    return out


def check_files(root: Path, files: list[ManualFile], report: Report) -> dict[str, set[str]]:
    """Run per-line rules. Returns {note path: {manual numbers citing it}}."""
    sections, entries = collect_anchors(files)
    app_letters = {mf.number for mf in files if mf.number and mf.number.isalpha()}
    cited_by: dict[str, set[str]] = {}
    for mf in files:
        for no, line, kind in iter_body(mf):
            where = f'{mf.rel}:{no}'
            check_leaks(line, where, report)
            if kind == 'blank':
                continue
            prose = INLINE_CODE_RE.sub('', line)
            for ref in SECTION_REF_RE.findall(prose):
                if ref not in sections:
                    report.add(where, f'cross-reference §{ref} does not resolve to a heading')
            for letter, entry in APP_REF_RE.findall(prose):
                if letter not in app_letters:
                    report.add(where, f'App. {letter} does not exist')
                elif entry and f'{letter}#{entry}' not in entries:
                    report.add(where, f'App. {letter}#{entry} does not resolve to an entry heading')
            cites = CITE_RE.findall(line)
            for _tags, group in cites:
                for src in split_sources(group):
                    if '/' not in src and not src.endswith(('.md', '.tsv', '.toml', '.txt')):
                        report.add(where, f'source {src!r} is not a repository path')
                        continue
                    target = root / PurePosixPath(src.rstrip('/'))
                    if not target.exists():
                        report.add(where, f'cited path {src} does not exist')
                        continue
                    if mf.number:
                        cited_by.setdefault(src.rstrip('/'), set()).add(mf.number)
            if kind in ('heading', 'table-sep', 'table-head'):
                continue
            is_xref = bool(XREF_ONLY_RE.search(line))
            if mf.status == 'stub' or mf.kind == 'index':
                if kind == 'quote' or is_xref:
                    continue
                if mf.status == 'stub':
                    report.add(where, 'stub file has content; only headings, cross-references and `>` notes are allowed')
                else:
                    report.add(where, 'index file has content; only headings and cross-references are allowed')
                continue
            if mf.kind == 'reference' and kind in ('table-row', 'item', 'text', 'quote'):
                if kind == 'quote':
                    report.add(where, 'quotes are only allowed in stub files')
                    continue
                if not cites and not is_xref:
                    report.add(where, 'factual line has no `[tag] (path)` source')
    return cited_by


def check_leaks(line: str, where: str, report: Report) -> None:
    for pattern, label in LEAK_PATTERNS:
        if pattern.search(line):
            report.add(where, f'leak: {label}')
    for match in IPV4_RE.finditer(line):
        if not VERSION_LIKE_RE.match(match.group(0)):
            report.add(where, 'leak: dotted IP literal')


def load_sources(root: Path, report: Report) -> list[dict[str, str]]:
    path = root / 'manual' / 'sources.tsv'
    if not path.exists():
        report.add('manual/sources.tsv', 'missing')
        return []
    rows = []
    lines = path.read_text(encoding='utf-8').splitlines()
    if not lines or lines[0].split('\t') != SOURCES_HEADER:
        report.add('manual/sources.tsv:1', 'header must be ' + '\\t'.join(SOURCES_HEADER))
        return []
    for no, line in enumerate(lines[1:], 2):
        if not line.strip():
            continue
        cells = line.split('\t')
        if len(cells) != len(SOURCES_HEADER):
            report.add(f'manual/sources.tsv:{no}', f'expected {len(SOURCES_HEADER)} columns, got {len(cells)}')
            continue
        row = dict(zip(SOURCES_HEADER, cells))
        row['_line'] = str(no)
        rows.append(row)
    return rows


def _section_list(cell: str) -> list[str]:
    return [part.strip() for part in cell.split(';') if part.strip()]


def check_sources(root: Path, rows: list[dict[str, str]], cited_by: dict[str, set[str]],
                  sections: set[str], final: bool, report: Report) -> None:
    notes = set(walk_notes(root))
    seen: dict[str, str] = {}
    for row in rows:
        where = f'manual/sources.tsv:{row["_line"]}'
        path = row['path']
        if path in seen:
            report.add(where, f'duplicate row for {path} (first at line {seen[path]})')
        seen[path] = row['_line']
        if path not in notes:
            report.add(where, f'{path} is not a note in the repository')
        status = row['status']
        if status not in STATUSES:
            report.add(where, f'unknown status {status!r}')
            continue
        listed = _section_list(row['sections'])
        for sec in listed:
            if sec not in sections:
                report.add(where, f'section {sec} does not exist in the manual')
        if status == 'excluded' and not row['reason'].strip():
            report.add(where, 'excluded row needs a reason')
        if status == 'cited' and not listed:
            report.add(where, 'cited row needs the sections that cite it')
        if status == 'pending' and final:
            report.add(where, f'{path} is still pending')
        citing = cited_by.get(path, set())
        missing = sorted(citing - set(listed))
        if missing:
            report.add(where, f'{path} is cited by {", ".join(missing)} but not listed in its sections column')
    for note in sorted(notes - set(seen)):
        report.add('manual/sources.tsv', f'note {note} has no row')
    for path in sorted(cited_by):
        if path not in seen and (root / path).is_file():
            report.add('manual/sources.tsv', f'cited file {path} has no row')


def _table_rows(text: str):
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith('|') and not TABLE_SEP_RE.match(stripped):
            yield [cell.strip() for cell in stripped.strip('|').split('|')]


def required_message_names(root: Path) -> set[str]:
    path = root / PACKET_IDS_NOTE
    if not path.exists():
        return set()
    return set(MESSAGE_NAME_RE.findall(path.read_text(encoding='utf-8')))


def required_props(root: Path) -> set[tuple[str, str]]:
    """(kind, id) pairs from the PLPROP/NPCPROP/BDPROP tables of the props note."""
    path = root / PROPS_NOTE
    if not path.exists():
        return set()
    out: set[tuple[str, str]] = set()
    current = None
    for line in path.read_text(encoding='utf-8').splitlines():
        heading = HEADING_RE.match(line.strip())
        if heading:
            level = len(heading.group(1))
            title = heading.group(2)
            if level <= 2:
                current = next((kind for key, kind in PROP_SECTIONS.items()
                                if title.startswith(key)), None)
            continue
        if current is None or not line.strip().startswith('|') or TABLE_SEP_RE.match(line.strip()):
            continue
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        for i, cell in enumerate(cells):
            # An id cell is a bare integer followed by a name cell.
            if cell.isdigit() and i + 1 < len(cells) and cells[i + 1]:
                out.add((current, cell))
    return out


def check_indexes(root: Path, files: list[ManualFile], report: Report) -> None:
    by_number = {mf.number: mf for mf in files if mf.number}
    app_a = by_number.get('A')
    if app_a and app_a.status != 'stub':
        text = '\n'.join(app_a.lines)
        for name in sorted(required_message_names(root)):
            if not re.search(r'\b' + re.escape(name) + r'\b', text):
                report.add(app_a.rel, f'{name} from {PACKET_IDS_NOTE} is missing')
    app_b = by_number.get('B')
    if app_b and app_b.status != 'stub':
        present = set()
        for cells in _table_rows('\n'.join(app_b.lines)):
            if len(cells) >= 2:
                present.add((cells[0].strip('`'), cells[1]))
        for kind, pid in sorted(required_props(root)):
            if (kind, pid) not in present:
                report.add(app_b.rel, f'{kind} {pid} from {PROPS_NOTE} is missing (rows start `| {kind} | {pid} |`)')


def run(root: Path, final: bool = False) -> Report:
    report = Report()
    root = Path(root).resolve()
    if not (root / 'manual').is_dir():
        report.add('manual', 'missing directory')
        return report
    files = load_manual(root, report)
    sections, _entries = collect_anchors(files)
    cited_by = check_files(root, files, report)
    rows = load_sources(root, report)
    check_sources(root, rows, cited_by, sections, final, report)
    check_indexes(root, files, report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', default=Path(__file__).resolve().parents[2], type=Path,
                        help='repository root (default: this checkout)')
    parser.add_argument('--final', action='store_true',
                        help='also fail on rows still marked pending')
    args = parser.parse_args(argv)
    report = run(args.root, final=args.final)
    for error in report.errors:
        print(error)
    if report.errors:
        print(f'{len(report.errors)} problem(s)', file=sys.stderr)
        return 1
    print('manual check ok')
    return 0


if __name__ == '__main__':
    sys.exit(main())
