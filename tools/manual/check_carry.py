#!/usr/bin/env python3
"""Check that every note the manual cites is carried, or says why not.

Standard library only.

    python tools/manual/check_carry.py           # fail on uncarried notes
    python tools/manual/check_carry.py --report  # also list the lowest carries

Two rules, both applied to `manual/sources.tsv` rows with status `cited`
and an empty `reason` column:

1. Planned sections. Every section in the `planned` column must be among
   the sections that cite the note (`sections`). A planned `5.2` is met by
   a citing `5` or `5.2.1`, and a planned `4` by any `4.x`.
2. Term carry. For a Markdown note, the distinctive terms (message names,
   hex constants, format magics, short inline-code spans that are not file
   names) are looked up in the manual text. When a note has at least
   MIN_TERMS such terms and fewer than CARRY_FLOOR of them appear in the
   manual, the note is not carried.

A note that fails either rule needs a `reason` that says where its facts
went or why the manual leaves them out. The rules are in
`manual/00-conventions.md` (section 0.11).
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

CARRY_FLOOR = 0.3
MIN_TERMS = 8

IDENT_RE = re.compile(
    r'\b(?:PLI|PLO|NPCPROP|PLPROP|BDPROP|PLTYPE|SVO|SVI|NCO|NCI|RCO|RCI|PLFLAG|NPCBUFFER)_[A-Z0-9_]+\b')
HEX_RE = re.compile(r'\b0x[0-9A-Fa-f]{2,8}\b')
MAGIC_RE = re.compile(
    r'\b(?:GLEVNW01|GRMAP001|GANI\d{4}|GOBJSET\d\d|GR-V1\.\d\d|Z3-V1\.\d\d|GWEBL\d{3}'
    r'|NCL\d+|GNP\d+|GSERV\d+|NW2[0-9A-Z]+|G3D[0-9A-Z]+)\b')
CODE_RE = re.compile(r'`([^`\n]{3,40})`')
# A code span that names a file, an archive or a path is bookkeeping, not a fact.
FILE_LIKE_RE = re.compile(r'(?:[/\\]|\.\*$|\.[A-Za-z][A-Za-z0-9]{0,4}$|^\.)')
FRAGMENT_RE = re.compile(r'^[\s,;:.)(|+\-]|[,;(|]\s*$|…')


def section_list(cell: str) -> list[str]:
    return [s.strip() for s in cell.split(';') if s.strip()]


def planned_met(planned: str, sections: list[str]) -> bool:
    return any(s == planned or s.startswith(planned + '.') or planned.startswith(s + '.')
               for s in sections)


def note_terms(text: str) -> set[str]:
    terms = set(IDENT_RE.findall(text)) | {h.lower() for h in HEX_RE.findall(text)}
    terms |= set(MAGIC_RE.findall(text))
    for span in CODE_RE.findall(text):
        span = span.strip()
        if HEX_RE.fullmatch(span):
            continue
        if len(span) < 3 or FILE_LIKE_RE.search(span) or FRAGMENT_RE.search(span):
            continue
        if ' ' in span and len(span) > 25:
            continue
        terms.add(span)
    return terms


def manual_text(root: Path) -> str:
    parts = [p.read_text(encoding='utf-8', errors='replace')
             for p in sorted((root / 'manual').rglob('*.md'))]
    return '\n'.join(parts).lower()


def load_rows(root: Path) -> list[dict[str, str]]:
    with open(root / 'manual' / 'sources.tsv', encoding='utf-8', newline='') as fh:
        return [dict(r) for r in csv.DictReader(fh, delimiter='\t')]


def term_carry(root: Path, rel: str, mtext: str) -> tuple[int, float, list[str]] | None:
    path = root / rel
    if path.suffix != '.md' or not path.is_file():
        return None
    terms = note_terms(path.read_text(encoding='utf-8', errors='replace'))
    if not terms:
        return None
    missing = sorted(t for t in terms if t.lower() not in mtext)
    return len(terms), 1 - len(missing) / len(terms), missing


def run(root: Path) -> tuple[list[str], list[tuple[float, str, int]]]:
    errors: list[str] = []
    carries: list[tuple[float, str, int]] = []
    mtext = manual_text(root)
    for row in load_rows(root):
        if row.get('status') != 'cited' or (row.get('reason') or '').strip():
            continue
        rel = row['path']
        sections = section_list(row.get('sections') or '')
        unmet = [p for p in section_list(row.get('planned') or '') if not planned_met(p, sections)]
        if unmet:
            errors.append(f'{rel}: planned for {", ".join(unmet)} but cited only in '
                          f'{", ".join(sections) or "nothing"}; cite it there or record a reason')
        tc = term_carry(root, rel, mtext)
        if tc is None:
            continue
        n, carry, missing = tc
        carries.append((carry, rel, n))
        if n >= MIN_TERMS and carry < CARRY_FLOOR:
            errors.append(f'{rel}: {carry:.0%} of {n} distinctive terms carried '
                          f'(floor {CARRY_FLOOR:.0%}); missing e.g. {", ".join(missing[:6])}; '
                          f'carry them or record a reason')
    return errors, carries


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument('--report', action='store_true', help='list the 20 lowest carries')
    args = ap.parse_args(argv)
    errors, carries = run(args.root)
    if args.report:
        for carry, rel, n in sorted(carries)[:20]:
            print(f'{carry:5.0%} {n:4d}  {rel}')
    for e in errors:
        print(f'error: {e}')
    if errors:
        print(f'carry check failed: {len(errors)} note(s)')
        return 1
    print(f'carry check ok ({len(carries)} notes measured)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
