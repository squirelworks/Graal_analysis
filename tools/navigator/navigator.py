#!/usr/bin/env python3
"""Local map of the markdown notes in this repository.

The home page is an architecture diagram, the link web of one area, and a
version map. Search filters by title or path. The note reader stays.

The server listens on the loopback address only and does not phone home:
no telemetry, no analytics, and no outbound request.

Standard library only.
"""

from __future__ import annotations

import argparse
import html
import os
import re
import secrets
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# Bind address (the loopback address), without a dotted literal.
# Same construction as tools/lab-servers/listserver.py.
LOOPBACK = '%d.%d.%d.%d' % (127, 0, 0, 1)
DEFAULT_PORT = 8765

MD_SUFFIXES = {'.md', '.markdown'}
SKIP_DIRS = {'.git', '__pycache__', '.pytest_cache'}
FOLDER_ORDER = (
    'root',
    'protocol',
    'formats',
    'client-internals',
    'graal3d',
    'tools',
    'archive',
    'npc-library',
    'version-profiles',
)

HEADING_RE = re.compile(r'^(#{1,6})\s+(.+?)\s*#*\s*$')
SETEXT_RE = re.compile(r'^(=+|-+)\s*$')
HR_RE = re.compile(r'^(\*[ \t]*){3,}$|^(-[ \t]*){3,}$|^(_[ \t]*){3,}$')
LIST_RE = re.compile(r'^( *)([-*+]|\d{1,9}[.)])\s+(.*)$')
SEP_CELL_RE = re.compile(r':?-{3,}:?')
LANG_RE = re.compile(r'[A-Za-z0-9_+.#-]{1,32}')

PLAIN_CSP = "default-src 'none'; script-src 'none'; style-src 'none'; img-src 'none'"
FRAGMENT_CSP = (
    "default-src 'none'; script-src 'none'; style-src 'unsafe-inline'; "
    "img-src 'none'; connect-src 'none'; base-uri 'none'; form-action 'none'"
)


class OutsideRepo(Exception):
    """The requested path is not a file inside the repository."""


class NoteNotFound(Exception):
    """The path is inside the repository but is not a markdown note."""


def default_repo() -> Path:
    return Path(__file__).resolve().parents[2]


def is_loopback_host(host: str) -> bool:
    if not isinstance(host, str):
        return False
    name = host.strip()
    return name.lower() == 'localhost' or name == LOOPBACK


def note_matches(entry: dict, query: str) -> bool:
    """Case-insensitive substring of the title or the path.

    An empty query matches every note. The browser uses the same rule.
    There is no server-side search.
    """
    needle = (query or '').strip().lower()
    if not needle:
        return True
    return needle in entry['title'].lower() or needle in entry['path'].lower()


def filter_notes(entries: list[dict], query: str) -> list[dict]:
    return [entry for entry in entries if note_matches(entry, query)]


def _folder_key(folder: str) -> tuple:
    try:
        rank = FOLDER_ORDER.index(folder)
    except ValueError:
        rank = len(FOLDER_ORDER)
    return (rank, folder.lower())


def _inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _plain_text(raw: str) -> str:
    text = raw.strip()
    text = re.sub(r'`([^`]*)`', r'\1', text)
    text = re.sub(r'!\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    text = re.sub(r'(?<![A-Za-z0-9])\*([^*]+)\*(?![A-Za-z0-9])', r'\1', text)
    return re.sub(r'\s+', ' ', text).strip()


def first_heading(text: str) -> str | None:
    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    in_fence = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence or not stripped:
            continue
        heading = HEADING_RE.match(stripped)
        if heading:
            title = _plain_text(heading.group(2))
            return title or None
        if index + 1 < len(lines) and SETEXT_RE.match(lines[index + 1].strip()):
            if not stripped.startswith(('#', '>', '-', '*', '+')) and not LIST_RE.match(line):
                title = _plain_text(stripped)
                if title:
                    return title
    return None


def build_index(repo: Path) -> list[dict]:
    """Walk markdown files and skip `.git` (and bytecode caches)."""
    root = Path(repo).resolve()
    entries = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(name for name in dirnames if name not in SKIP_DIRS)
        for name in sorted(filenames):
            if Path(name).suffix.lower() not in MD_SUFFIXES:
                continue
            path = Path(dirpath) / name
            lexical = path.relative_to(root)
            if any(part in SKIP_DIRS for part in lexical.parts):
                continue
            if not _inside(root, path):
                continue
            text = path.read_text(encoding='utf-8-sig', errors='replace')
            title = first_heading(text) or path.name
            folder = lexical.parts[0] if len(lexical.parts) > 1 else 'root'
            entries.append({
                'path': lexical.as_posix(),
                'title': title,
                'folder': folder,
            })
    entries.sort(key=lambda entry: (_folder_key(entry['folder']), entry['path'].lower()))
    return entries


# Areas of the corpus. `folders` are real top-level directories (or `root`).
# A lab note inside another folder is classified by `is_lab_path` first.
AREAS = (
    {
        'id': 'clients',
        'name': 'Client versions',
        'blurb': 'Client behaviour notes',
        'folders': ('client-internals', 'version-profiles'),
    },
    {
        'id': 'protocol',
        'name': 'Protocol',
        'blurb': 'Packet and login notes',
        'folders': ('protocol', 'server-notes'),
    },
    {
        'id': 'formats',
        'name': 'Formats',
        'blurb': 'Level, gani and map files',
        'folders': ('formats',),
    },
    {
        'id': 'npc',
        'name': 'NPC scripts',
        'blurb': 'GS1 and Ash notes',
        'folders': ('npc-library', 'ash'),
    },
    {
        'id': 'graal3d',
        'name': 'Graal3D',
        'blurb': 'Separate 3D client',
        'folders': ('graal3d',),
    },
    {
        'id': 'torque',
        'name': 'Torque',
        'blurb': 'Engine and TorqueScript',
        'folders': ('torque',),
    },
    {
        'id': 'tools',
        'name': 'Tools',
        'blurb': 'Editors and generators',
        'folders': ('tools', 'recovered-drive-tools', 'recovered-hacks'),
    },
    {
        'id': 'labs',
        'name': 'Labs',
        'blurb': 'Loopback lab runs',
        'folders': ('live-runs',),
    },
    {
        'id': 'archives',
        'name': 'Archives',
        'blurb': 'Retired notes and assets',
        'folders': ('archive', 'archival'),
    },
    {
        'id': 'indexes',
        'name': 'Corpus index',
        'blurb': 'Contents, rules and tasks',
        'folders': ('docs', 'root'),
    },
)

# Diagram geometry. The nine areas above, minus the corpus index, which is a
# strip of real notes rather than a tenth product area.
_BOX_W = 200
_BOX_H = 74
_DIAGRAM_BOXES = {
    'formats': (20, 18),
    'clients': (290, 18),
    'protocol': (560, 18),
    'npc': (830, 18),
    'archives': (20, 148),
    'tools': (290, 148),
    'graal3d': (560, 148),
    'torque': (830, 148),
    'labs': (290, 278),
}
_DIAGRAM_EDGES = (
    ('formats', 'clients', 'levels'),
    ('clients', 'protocol', 'packets'),
    ('protocol', 'npc', 'NC'),
    ('formats', 'archives', 'held'),
    ('clients', 'tools', 'editors'),
    ('tools', 'labs', 'runs'),
    ('protocol', 'graal3d', 'own wire'),
    ('graal3d', 'torque', 'plug-in'),
)
_DIAGRAM_W = 1050
_DIAGRAM_H = 372

# Eras named in this corpus, left to right. A path is linked only when that
# note is in the index. These are not invented dates or picture sizes.
VERSION_ERAS = (
    ('1998 and 1.x', (
        'client-internals/zelda-online-1998.md',
        'protocol/relay-1998.md',
        'protocol/gserv-1999.md',
        'client-internals/versions-133-139.md',
        'version-profiles/matrix/rules-1st-graal.md',
        'version-profiles/matrix/rules-139.md',
    )),
    ('2.x', (
        'client-internals/cross-version-timeline.md',
        'client-internals/client-architecture-205.md',
        'version-profiles/2.22-2.31.md',
        'protocol/client-versions.md',
    )),
    ('3.x', (
        'protocol/v3x-clients.md',
        'version-profiles/3.04-3.153.md',
    )),
    ('4.x', (
        'protocol/v4x-clients.md',
        'client-internals/live-behaviour-404.md',
    )),
    ('5.x', (
        'protocol/v5x-clients.md',
        'version-profiles/lab-v5-2026-10-30.md',
    )),
    ('6.x', (
        'protocol/v6x-clients.md',
    )),
    ('Graal3D', (
        'graal3d/README.md',
        'graal3d/protocol.md',
    )),
)
MATRIX_NOTE = 'version-profiles/matrix/README.md'
INDEX_NOTES = (
    'README.md',
    'docs/NEXT.md',
    'AGENTS.md',
    'CONSOLIDATED.md',
)

WEB_CAP = 48
SEARCH_CAP = 24
_SECTION_RE = re.compile(r'^[A-Za-z0-9._+-]{1,80}$')

_AREA_BY_ID = {area['id']: area for area in AREAS}
_FOLDER_AREA = {}
for _area in AREAS:
    for _folder in _area['folders']:
        _FOLDER_AREA[_folder] = _area['id']


def is_lab_path(path: str) -> bool:
    """Lab runs and the lab desk, wherever the note was filed."""
    parts = path.split('/')
    name = parts[-1].lower()
    if parts[0] == 'live-runs':
        return True
    if any(part in ('lab-servers', 'respawn-lab', 'relay-bridge') for part in parts):
        return True
    if name == 'lab-setup.md':
        return True
    if name.startswith(('lab-', 'live-')):
        return True
    if any(part.startswith(('lab-', 'live-')) for part in parts[:-1]):
        return True
    return False


def area_for(path: str) -> dict:
    if is_lab_path(path):
        return _AREA_BY_ID['labs']
    folder = path.split('/')[0] if '/' in path else 'root'
    return _AREA_BY_ID[_FOLDER_AREA.get(folder, 'indexes')]


def valid_section(section: str) -> bool:
    return bool(section) and bool(_SECTION_RE.fullmatch(section)) and section not in SKIP_DIRS


def clean_query(query: str) -> str:
    return (query or '').replace('\x00', '').strip()[:200]


def version_columns(source) -> list[tuple[str, list[dict]]]:
    """Era columns. A note is included only when it is in the index."""
    index = source if isinstance(source, list) else build_index(source)
    by_path = {entry['path']: entry for entry in index}
    columns = []
    for label, paths in VERSION_ERAS:
        found = [by_path[path] for path in paths if path in by_path]
        columns.append((label, found))
    return columns


def _mask_unlinked_lines(text: str):
    """Yield source lines outside fenced code, with inline code blanked."""
    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    fence = False
    for line in lines:
        if line.startswith('```'):
            fence = not fence
            continue
        if fence:
            continue
        chars = list(line)
        index = 0
        while index < len(chars):
            if chars[index] != '`':
                index += 1
                continue
            opener = re.match(r'`+', line[index:])
            if not opener:
                break
            ticks = opener.group(0)
            close = line.find(ticks, index + len(ticks))
            if close == -1:
                for cursor in range(index, len(chars)):
                    chars[cursor] = ' '
                break
            for cursor in range(index, close + len(ticks)):
                chars[cursor] = ' '
            index = close + len(ticks)
        yield ''.join(chars)


def outgoing_links(text: str, note_path: str, repo: Path) -> list[str]:
    """Relative markdown links in `text` that resolve to a note in `repo`."""
    found = []
    seen = set()
    for line in _mask_unlinked_lines(text):
        index = 0
        while index < len(line):
            if line[index] != '[':
                index += 1
                continue
            link = _match_link(line, index, image=False)
            if not link:
                index += 1
                continue
            rel = _note_target(repo, note_path, link[1])
            if rel and rel != note_path and rel not in seen:
                seen.add(rel)
                found.append(rel)
            index = link[2]
    return found


def build_edges(repo: Path, index: list[dict] | None = None) -> list[tuple[str, str]]:
    """Directed edges from relative markdown links between notes."""
    root = Path(repo).resolve()
    if index is None:
        index = build_index(root)
    edges = []
    seen = set()
    for entry in index:
        try:
            rel, text = read_note(root, entry['path'])
        except (OutsideRepo, NoteNotFound, OSError):
            continue
        for target in outgoing_links(text, rel, root):
            key = (rel, target)
            if key in seen:
                continue
            seen.add(key)
            edges.append(key)
    edges.sort()
    return edges


def _degree(notes: list[dict], edges: list[tuple[str, str]]) -> dict:
    paths = {entry['path'] for entry in notes}
    degree = {path: 0 for path in paths}
    for src, dst in edges:
        if src in degree:
            degree[src] += 1
        if dst in degree:
            degree[dst] += 1
    return degree


def area_sections(index: list[dict], area_id: str) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    for entry in index:
        if area_for(entry['path'])['id'] != area_id:
            continue
        parts = entry['path'].split('/')
        if len(parts) < 3:
            continue
        counts[parts[1]] = counts.get(parts[1], 0) + 1
    return sorted(counts.items())


def select_web(index, edges, area_id, section, query):
    """Notes to draw for one area.

    A small area is drawn whole. A large area draws the notes that actually
    link to each other, not every file in the folder.
    """
    pool = [entry for entry in index if area_for(entry['path'])['id'] == area_id]
    if section:
        pool = [entry for entry in pool if section in entry['path'].split('/')[:-1]]
    total = len(pool)
    if query:
        matched = filter_notes(pool, query)
        return matched[:SEARCH_CAP], len(matched), 'search'
    if len(pool) <= WEB_CAP:
        return pool, total, 'cluster'
    paths = {entry['path'] for entry in pool}
    linked_paths = set()
    for src, dst in edges:
        if src in paths and dst in paths:
            linked_paths.add(src)
            linked_paths.add(dst)
    if not linked_paths:
        return [], total, 'narrow'
    chosen = [entry for entry in pool if entry['path'] in linked_paths]
    degree = _degree(chosen, edges)
    chosen.sort(key=lambda entry: (-degree[entry['path']], entry['path'].lower()))
    return chosen[:WEB_CAP], total, 'web'


def _safe_parts(raw: str) -> list[str]:
    if raw is None or not isinstance(raw, str):
        raise OutsideRepo('empty')
    if len(raw) > 1024 or '\x00' in raw or '\n' in raw or '\r' in raw:
        raise OutsideRepo(raw)
    text = raw.replace('\\', '/').strip()
    if not text:
        raise NoteNotFound(raw)
    lowered = text.lower()
    if text.startswith(('/', '~')) or re.match(r'^[A-Za-z]:', text):
        raise OutsideRepo(raw)
    if lowered.startswith((
        'javascript:', 'data:', 'vbscript:', 'file:',
        'http://', 'https://', 'ftp://', 'mailto:',
    )):
        raise OutsideRepo(raw)
    parts: list[str] = []
    for part in text.split('/'):
        if part in ('', '.'):
            continue
        if part == '..':
            if not parts:
                raise OutsideRepo(raw)
            parts.pop()
            continue
        parts.append(part)
    if not parts:
        raise NoteNotFound(raw)
    if any(part in SKIP_DIRS for part in parts):
        raise OutsideRepo(raw)
    return parts


def locate_note(repo: Path, raw: str) -> Path:
    """Return a markdown file inside repo, or raise before reading outside."""
    root = Path(repo).resolve()
    parts = _safe_parts(raw)
    candidate = root.joinpath(*parts)
    resolved = candidate.resolve()
    if not _inside(root, resolved):
        raise OutsideRepo(raw)
    rel_parts = resolved.relative_to(root).parts
    if any(part in SKIP_DIRS for part in rel_parts):
        raise OutsideRepo(raw)
    if not resolved.is_file() or resolved.suffix.lower() not in MD_SUFFIXES:
        raise NoteNotFound(raw)
    return resolved


def read_note(repo: Path, raw: str) -> tuple[str, str]:
    root = Path(repo).resolve()
    path = locate_note(root, raw)
    rel = path.resolve().relative_to(root).as_posix()
    return rel, path.read_text(encoding='utf-8-sig', errors='replace')


def note_href(rel: str) -> str:
    return '/note?path=' + urllib.parse.quote(rel, safe='/')


def _slugify(text: str) -> str:
    slug = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return slug or 'section'


def _unique_slug(text: str, used: dict) -> str:
    base = _slugify(text)
    count = used.get(base, 0) + 1
    used[base] = count
    if count == 1:
        return base
    return f'{base}-{count}'


def _unwrap_dest(dest: str) -> str:
    dest = dest.strip()
    if dest.startswith('<') and dest.endswith('>') and len(dest) >= 2:
        return dest[1:-1].strip()
    return dest


def _note_target(repo: Path, note_path: str, dest: str) -> str | None:
    dest = _unwrap_dest(dest)
    if not dest or dest.startswith('#') or '://' in dest or dest.startswith('//'):
        return None
    lowered = dest.lower()
    if lowered.startswith(('javascript:', 'data:', 'mailto:', 'file:', 'vbscript:')):
        return None
    path_part, _hash, _anchor = dest.partition('#')
    if not path_part:
        return None
    path_part = urllib.parse.unquote(path_part.replace('\\', '/'))
    if path_part.startswith('/'):
        raw = path_part.lstrip('/')
    else:
        parent = str(Path(note_path).parent)
        raw = path_part if parent in ('', '.') else parent + '/' + path_part
    try:
        located = locate_note(repo, raw)
    except (OutsideRepo, NoteNotFound):
        return None
    return located.resolve().relative_to(Path(repo).resolve()).as_posix()


def _is_em_open(text: str, index: int) -> bool:
    marker = text[index]
    if index > 0 and text[index - 1].isalnum():
        return False
    if index + 1 >= len(text) or text[index + 1].isspace() or text[index + 1] == marker:
        return False
    return True


def _find_em_close(text: str, index: int, marker: str) -> int:
    cursor = index + 1
    while cursor < len(text):
        if text[cursor] == marker:
            if text.startswith(marker + marker, cursor):
                cursor += 2
                continue
            if cursor > index + 1 and not (cursor + 1 < len(text) and text[cursor + 1].isalnum()):
                return cursor
        cursor += 1
    return -1


def _match_link(text: str, index: int, image: bool = False):
    """Return (label, destination, end) or None. Destinations may contain parentheses."""
    if image:
        if not text.startswith('![', index):
            return None
        label_at = index + 2
    else:
        if text[index] != '[':
            return None
        label_at = index + 1
    close_label = text.find(']', label_at)
    if close_label == -1 or text[label_at:close_label].find('\n') != -1:
        return None
    if close_label + 1 >= len(text) or text[close_label + 1] != '(':
        return None
    label = text[label_at:close_label]
    if not image and not label:
        return None
    cursor = close_label + 2
    if cursor < len(text) and text[cursor] == '<':
        end = text.find('>', cursor + 1)
        if end == -1 or '\n' in text[cursor:end]:
            return None
        dest = text[cursor:end + 1]
        cursor = end + 1
    else:
        depth = 0
        start = cursor
        while cursor < len(text):
            char = text[cursor]
            if char == '\\' and cursor + 1 < len(text):
                cursor += 2
                continue
            if char in ' \t\n':
                break
            if char == '(':
                depth += 1
            elif char == ')':
                if depth == 0:
                    break
                depth -= 1
            cursor += 1
        if cursor == start:
            return None
        dest = text[start:cursor]
    while cursor < len(text) and text[cursor] == ' ':
        cursor += 1
    if cursor < len(text) and text[cursor] == '"':
        end_quote = text.find('"', cursor + 1)
        if end_quote == -1:
            return None
        cursor = end_quote + 1
        while cursor < len(text) and text[cursor] == ' ':
            cursor += 1
    if cursor >= len(text) or text[cursor] != ')':
        return None
    return label, dest, cursor + 1


def _inline(text: str, note_path: str, repo: Path, slugs: dict) -> str:
    out: list[str] = []
    index = 0
    length = len(text)
    while index < length:
        if text[index] == '`':
            opener = re.match(r'`+', text[index:])
            ticks = opener.group(0)
            close = text.find(ticks, index + len(ticks))
            if close == -1:
                out.append(html.escape(text[index:]))
                break
            out.append('<code>' + html.escape(text[index + len(ticks):close]) + '</code>')
            index = close + len(ticks)
            continue
        if text.startswith('![', index):
            image = _match_link(text, index, image=True)
            if image:
                # Alt text only. No <img>, so the page does not fetch the target.
                label, dest, end = image
                shown = html.escape(label)
                target = _unwrap_dest(dest)
                if target and not target.lower().startswith(('javascript:', 'data:', 'vbscript:')):
                    extra = html.escape(target)
                    shown = f'{shown} ({extra})' if shown else extra
                out.append(shown)
                index = end
                continue
        if text[index] == '[':
            link = _match_link(text, index, image=False)
            if link:
                out.append(_link(link[0], link[1], note_path, repo, slugs))
                index = link[2]
                continue
        if text.startswith('**', index) or text.startswith('__', index):
            marker = text[index:index + 2]
            close = text.find(marker, index + 2)
            if close != -1:
                inner = _inline(text[index + 2:close], note_path, repo, slugs)
                out.append('<strong>' + inner + '</strong>')
                index = close + 2
                continue
        if text[index] in '*_' and _is_em_open(text, index):
            close = _find_em_close(text, index, text[index])
            if close != -1:
                inner = _inline(text[index + 1:close], note_path, repo, slugs)
                out.append('<em>' + inner + '</em>')
                index = close + 1
                continue
        out.append(html.escape(text[index]))
        index += 1
    return ''.join(out)


def _link(label: str, dest: str, note_path: str, repo: Path, slugs: dict) -> str:
    inner = _inline(label, note_path, repo, slugs)
    target = _unwrap_dest(dest)
    if target.startswith('#'):
        anchor = _slugify(urllib.parse.unquote(target[1:]))
        return f'<a href="#{html.escape(anchor, quote=True)}">{inner}</a>'
    _path, _sep, anchor = target.partition('#')
    rel = _note_target(repo, note_path, target)
    if rel:
        href = note_href(rel)
        if anchor:
            href += '#' + _slugify(urllib.parse.unquote(anchor))
        return (
            f'<a href="{html.escape(href, quote=True)}" '
            f'data-note="{html.escape(rel, quote=True)}">{inner}</a>'
        )
    lowered = target.lower()
    if lowered.startswith(('javascript:', 'data:', 'vbscript:')):
        return inner
    if target:
        return inner + ' (' + html.escape(target) + ')'
    return inner


def _code_block(code: str, lang: str) -> str:
    klass = ''
    if LANG_RE.fullmatch(lang or ''):
        klass = f' class="language-{lang}"'
    return f'<pre><code{klass}>{html.escape(code)}</code></pre>'


def _heading(level: int, raw: str, note_path: str, repo: Path, slugs: dict) -> str:
    level = min(max(level, 1), 6)
    slug = html.escape(_unique_slug(_plain_text(raw), slugs), quote=True)
    body = _inline(raw.strip(), note_path, repo, slugs)
    return f'<h{level} id="{slug}">{body}</h{level}>'


def _list_marker(line: str):
    match = LIST_RE.match(line)
    if not match:
        return None
    indent = len(match.group(1))
    marker = match.group(2)
    kind = 'ol' if marker[0].isdigit() else 'ul'
    return indent, kind, match.group(3)


def _split_cells(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith('|'):
        stripped = stripped[1:]
    if stripped.endswith('|'):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split('|')]


def _is_separator_row(line: str) -> bool:
    cells = _split_cells(line)
    return bool(cells) and all(SEP_CELL_RE.fullmatch(cell) for cell in cells)


def _is_table_start(line: str, nxt: str | None) -> bool:
    return nxt is not None and '|' in line and _is_separator_row(nxt)


def _starts_new_block(lines: list[str], index: int) -> bool:
    line = lines[index]
    stripped = line.strip()
    if not stripped:
        return False
    if line.startswith('```') or stripped.startswith('>'):
        return True
    if HEADING_RE.match(stripped) or HR_RE.match(stripped) or _list_marker(line):
        return True
    nxt = lines[index + 1] if index + 1 < len(lines) else None
    if _is_table_start(line, nxt):
        return True
    if nxt is not None and SETEXT_RE.match(nxt.strip()) and not stripped.startswith('#'):
        return True
    return False


def _render_list(lines, index, note_path, repo, slugs):
    first = _list_marker(lines[index])
    indent, kind, _rest = first
    items = []
    total = len(lines)
    while index < total:
        if not lines[index].strip():
            cursor = index + 1
            while cursor < total and not lines[cursor].strip():
                cursor += 1
            nxt = _list_marker(lines[cursor]) if cursor < total else None
            if nxt and nxt[0] == indent and nxt[1] == kind:
                index = cursor
            else:
                break
        info = _list_marker(lines[index])
        if info is None or info[0] != indent or info[1] != kind:
            break
        _indent, _kind, rest = info
        index += 1
        extras = []
        while index < total and lines[index].strip():
            info2 = _list_marker(lines[index])
            if info2 and info2[0] == indent and info2[1] == kind:
                break
            if info2 and info2[0] > indent:
                child, index = _render_list(lines, index, note_path, repo, slugs)
                extras.append(child)
                continue
            if lines[index].startswith(' ') and not (info2 and info2[0] <= indent):
                extras.append(_inline(lines[index].strip(), note_path, repo, slugs))
                index += 1
                continue
            break
        item = _inline(rest, note_path, repo, slugs)
        for extra in extras:
            if extra.startswith('<ul') or extra.startswith('<ol'):
                item += extra
            else:
                item += ' ' + extra
        items.append('<li>' + item + '</li>')
    return f'<{kind}>{"".join(items)}</{kind}>', index


def _render_table(lines, index, note_path, repo, slugs):
    header = _split_cells(lines[index])
    separators = _split_cells(lines[index + 1])
    aligns = []
    for cell in separators:
        left = cell.startswith(':')
        right = cell.endswith(':')
        if left and right:
            aligns.append('center')
        elif right:
            aligns.append('right')
        elif left:
            aligns.append('left')
        else:
            aligns.append('')
    index += 2
    rows = []
    total = len(lines)
    while index < total and lines[index].strip() and '|' in lines[index]:
        if _starts_new_block(lines, index) and _is_table_start(
            lines[index], lines[index + 1] if index + 1 < total else None
        ):
            break
        rows.append(_split_cells(lines[index]))
        index += 1

    def cell(tag: str, text: str, align: str) -> str:
        style = f' style="text-align:{align}"' if align else ''
        return f'<{tag}{style}>{_inline(text, note_path, repo, slugs)}</{tag}>'

    width = max([len(header), *[len(row) for row in rows]] or [0])
    head = ''.join(
        cell('th', header[col] if col < len(header) else '', aligns[col] if col < len(aligns) else '')
        for col in range(width)
    )
    body = []
    for row in rows:
        body.append('<tr>' + ''.join(
            cell('td', row[col] if col < len(row) else '', aligns[col] if col < len(aligns) else '')
            for col in range(width)
        ) + '</tr>')
    return '<table><thead><tr>' + head + '</tr></thead><tbody>' + ''.join(body) + '</tbody></table>', index


def _render_blocks(text: str, note_path: str, repo: Path, slugs: dict) -> str:
    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    parts: list[str] = []
    index = 0
    total = len(lines)
    while index < total:
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith('```'):
            lang = line[3:].strip().split()[0] if line[3:].strip() else ''
            index += 1
            buf = []
            while index < total and not lines[index].startswith('```'):
                buf.append(lines[index])
                index += 1
            if index < total and lines[index].startswith('```'):
                index += 1
            parts.append(_code_block('\n'.join(buf), lang))
            continue
        stripped = line.strip()
        heading = HEADING_RE.match(stripped)
        if heading:
            level = len(heading.group(1))
            parts.append(_heading(level, heading.group(2), note_path, repo, slugs))
            index += 1
            continue
        nxt = lines[index + 1] if index + 1 < total else None
        if (
            nxt is not None
            and SETEXT_RE.match(nxt.strip())
            and stripped
            and not stripped.startswith(('#', '>'))
            and not _list_marker(line)
        ):
            level = 1 if nxt.strip().startswith('=') else 2
            parts.append(_heading(level, stripped, note_path, repo, slugs))
            index += 2
            continue
        if HR_RE.match(stripped):
            parts.append('<hr>')
            index += 1
            continue
        if stripped.startswith('>'):
            chunk = []
            while index < total and lines[index].lstrip().startswith('>'):
                chunk.append(re.sub(r'^\s*>\s?', '', lines[index]))
                index += 1
            inner = _render_blocks('\n'.join(chunk), note_path, repo, slugs)
            parts.append('<blockquote>' + inner + '</blockquote>')
            continue
        if _list_marker(line):
            block, index = _render_list(lines, index, note_path, repo, slugs)
            parts.append(block)
            continue
        if _is_table_start(line, nxt):
            block, index = _render_table(lines, index, note_path, repo, slugs)
            parts.append(block)
            continue
        buf = [stripped]
        index += 1
        while index < total and lines[index].strip() and not _starts_new_block(lines, index):
            buf.append(lines[index].strip())
            index += 1
        parts.append('<p>' + _inline(' '.join(buf), note_path, repo, slugs) + '</p>')
    return '\n'.join(parts)


def render_markdown(text: str, note_path: str, repo: Path) -> str:
    """Render a note to HTML. Raw HTML from the note is escaped, never executed."""
    return _render_blocks(text, note_path, Path(repo).resolve(), {})


def article_html(rel: str, body: str, strip: str = '') -> str:
    safe = html.escape(rel, quote=True)
    return (
        f'<article id="doc" data-path="{safe}">'
        f'<p class="note-path">{html.escape(rel)}</p>'
        f'{strip}'
        f'{body}'
        f'</article>'
    )


def link_strip_html(path: str, edges: list[tuple[str, str]], index: list[dict]) -> str:
    """Notes this page links to, and notes that link here."""
    by_path = {entry['path']: entry for entry in index}
    outgoing = sorted(dst for src, dst in edges if src == path)
    incoming = sorted(src for src, dst in edges if dst == path)

    def items(paths: list[str]) -> str:
        if not paths:
            return '<li class="none">none</li>'
        rows = []
        for rel in paths:
            entry = by_path.get(rel)
            title = entry['title'] if entry else rel
            href = html.escape(note_href(rel), quote=True)
            attr = html.escape(rel, quote=True)
            rows.append(
                f'<li><a href="{href}" data-note="{attr}">{html.escape(title)}</a></li>'
            )
        return ''.join(rows)

    return (
        '<nav class="link-strip" aria-label="Linked notes">'
        f'<p class="strip-label">Links to</p><ul>{items(outgoing)}</ul>'
        f'<p class="strip-label">Linked from</p><ul>{items(incoming)}</ul>'
        '</nav>'
    )


APP_SCRIPT = """
(function () {
  var input = document.getElementById("search");
  var count = document.getElementById("count");

  // Same rule as note_matches(): empty query matches all; otherwise a
  // case-insensitive substring of the title or the path. No remote search.
  function noteMatches(title, path, query) {
    var q = String(query || "").trim().toLowerCase();
    if (!q) {
      return true;
    }
    title = String(title || "").toLowerCase();
    path = String(path || "").toLowerCase();
    return title.indexOf(q) !== -1 || path.indexOf(q) !== -1;
  }

  function nodeByPath(path) {
    var nodes = document.querySelectorAll(".web-node");
    var i;
    for (i = 0; i < nodes.length; i++) {
      if (nodes[i].getAttribute("data-path") === path) {
        return nodes[i];
      }
    }
    return null;
  }

  function applyFilter() {
    if (!input) {
      return;
    }
    var nodes = document.querySelectorAll(".web-node");
    if (!nodes.length) {
      return;
    }
    var query = input.value;
    if (!String(query || "").trim()) {
      var j;
      for (j = 0; j < nodes.length; j++) {
        nodes[j].style.display = "";
      }
      var idle = document.querySelectorAll(".web-edge");
      for (j = 0; j < idle.length; j++) {
        idle[j].style.display = "";
      }
      if (count) {
        count.textContent = "";
      }
      return;
    }
    var shown = 0;
    var i;
    for (i = 0; i < nodes.length; i++) {
      var node = nodes[i];
      var ok = noteMatches(node.getAttribute("data-title"), node.getAttribute("data-path"), query);
      node.style.display = ok ? "" : "none";
      if (ok) {
        shown += 1;
      }
    }
    var edges = document.querySelectorAll(".web-edge");
    for (i = 0; i < edges.length; i++) {
      var edge = edges[i];
      var from = nodeByPath(edge.getAttribute("data-from"));
      var to = nodeByPath(edge.getAttribute("data-to"));
      var visible = from && to && from.style.display !== "none" && to.style.display !== "none";
      edge.style.display = visible ? "" : "none";
    }
    if (count) {
      count.textContent = shown + " of " + nodes.length;
    }
  }

  if (input) {
    input.addEventListener("input", applyFilter);
    applyFilter();
  }

  function mark(path) {
    Array.prototype.forEach.call(document.querySelectorAll("a[data-note]"), function (link) {
      link.classList.toggle("current", link.getAttribute("data-note") === path);
    });
  }

  function showNote(path, hash, push) {
    var holder = document.getElementById("doc-holder");
    if (!holder) {
      window.location.assign("/note?path=" + encodeURIComponent(path) + (hash || ""));
      return;
    }
    var fragment = "/note?path=" + encodeURIComponent(path) + "&fragment=1";
    fetch(fragment).then(function (res) {
      if (!res.ok) {
        throw new Error(String(res.status));
      }
      return res.text();
    }).then(function (page) {
      holder.innerHTML = page;
      var next = "/note?path=" + encodeURIComponent(path) + (hash || "");
      if (push) {
        history.pushState({path: path}, "", next);
      }
      mark(path);
      if (hash) {
        var target = document.getElementById(hash.slice(1));
        if (target && target.scrollIntoView) {
          target.scrollIntoView();
          return;
        }
      }
      if (holder.scrollTo) {
        holder.scrollTo(0, 0);
      }
    }).catch(function () {
      window.location.assign("/note?path=" + encodeURIComponent(path) + (hash || ""));
    });
  }

  document.body.addEventListener("click", function (event) {
    var link = event.target.closest ? event.target.closest("a[data-note]") : null;
    if (!link) {
      return;
    }
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
      return;
    }
    if (!document.getElementById("doc-holder")) {
      return;
    }
    event.preventDefault();
    showNote(link.getAttribute("data-note"), link.hash || "", true);
  });

  window.addEventListener("popstate", function () {
    window.location.reload();
  });
})();
"""

PAGE_STYLE = """
:root {
  --ink: #1c1915;
  --paper: #f3eee4;
  --card: #fffdf8;
  --muted: #5e675f;
  --line: #d9d2c5;
  --accent: #0f5c6b;
  --code: #efe8dc;
}
* { box-sizing: border-box; }
html, body { margin: 0; }
body {
  color: var(--ink);
  background: var(--paper);
  font: 17px/1.5 Palatino, "Palatino Linotype", "Iowan Old Style", Georgia, serif;
}
a { color: var(--accent); }
.banner {
  display: flex;
  justify-content: space-between;
  gap: 1.2rem;
  align-items: flex-end;
}
.mark {
  margin: 0;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font: 600 0.72rem/1.2 "Segoe UI", sans-serif;
  color: var(--muted);
}
.banner h1, .note-app h1.site {
  margin: 0.1rem 0 0;
  font: 600 1.55rem/1.1 "Segoe UI", sans-serif;
}
.local { margin: 0.2rem 0 0; color: var(--muted); font: 0.82rem/1.3 "Segoe UI", sans-serif; }
.search { margin: 0; min-width: 16rem; flex: 0 1 22rem; }
.search-label { display: block; font: 0.75rem/1.2 "Segoe UI", sans-serif; margin-bottom: 0.2rem; color: var(--muted); }
#search {
  width: 100%;
  padding: 0.4rem 0.55rem;
  border: 1px solid var(--line);
  border-radius: 0.25rem;
  font: 0.95rem/1.3 "Segoe UI", sans-serif;
  color: var(--ink);
  background: #fff;
}
.home {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-areas:
    "banner"
    "index"
    "arch"
    "versions"
    "web";
  gap: 0.55rem;
  padding: 0.7rem 0.85rem 1.2rem;
}
.banner { grid-area: banner; }
.index-strip { grid-area: index; margin: 0; font: 0.85rem/1.4 "Segoe UI", sans-serif; }
.index-strip span { color: var(--muted); margin-right: 0.4rem; }
.index-strip a { margin-right: 0.7rem; }
.architecture { grid-area: arch; }
.versions { grid-area: versions; }
.web-panel { grid-area: web; }
.panel {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 0.45rem;
  padding: 0.5rem 0.65rem 0.65rem;
}
.panel h2 { margin: 0 0 0.15rem; font: 600 0.95rem/1.2 "Segoe UI", sans-serif; }
.caption, .web-note { margin: 0 0 0.4rem; color: var(--muted); font-size: 0.82rem; }
#count { margin: 0.25rem 0 0; color: var(--muted); font: 0.75rem/1.2 "Segoe UI", sans-serif; }
.arch, .web { width: 100%; height: auto; display: block; }
.arch rect, .web rect { fill: #fffdf8; stroke: #0f5c6b; stroke-width: 1.6; }
.arch a.is-on rect { fill: #d7eef0; stroke-width: 2.6; }
.arch line, .web-edge { stroke: #8aa39c; stroke-width: 1.5; }
.arch text.name { font: 600 15px "Segoe UI", sans-serif; fill: #1c1915; }
.arch text.blurb { font: 11px "Segoe UI", sans-serif; fill: #4d5b55; }
.arch text.edge-label {
  font: 11px "Segoe UI", sans-serif;
  fill: #24564f;
  paint-order: stroke;
  stroke: #fffdf8;
  stroke-width: 5px;
}
.web text { font: 12px "Segoe UI", sans-serif; fill: #1c1915; }
.web text.web-path { font: 10px "Segoe UI", sans-serif; fill: #5e675f; }
.arch a, .web a { text-decoration: none; }
.version-map { display: flex; gap: 0.35rem; align-items: flex-start; }
.era { flex: 1 1 0; min-width: 0; border-top: 3px solid #0f5c6b; padding-top: 0.3rem; }
.era h3 {
  margin: 0 0 0.35rem;
  font: 600 0.82rem/1.2 "Segoe UI", sans-serif;
  white-space: nowrap;
}
.era a {
  display: block;
  font: 0.72rem/1.35 "Segoe UI", sans-serif;
  margin: 0.12rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.matrix { margin: 0 0 0.4rem; font-size: 0.82rem; }
.sections { display: flex; flex-wrap: wrap; gap: 0.3rem; margin: 0.2rem 0 0.55rem; }
.sections a {
  display: inline-block;
  text-decoration: none;
  color: var(--ink);
  background: #f3efe6;
  border: 1px solid var(--line);
  border-radius: 0.3rem;
  padding: 0.12rem 0.4rem;
  font: 0.72rem/1.3 "Segoe UI", sans-serif;
}
.sections a.is-on { background: #d5eef0; }
.sections span { color: var(--muted); margin-left: 0.25rem; }
.match-row { display: flex; flex-wrap: wrap; gap: 0.45rem; }
a.match {
  width: 16rem;
  text-decoration: none;
  color: inherit;
  background: #fffdf8;
  border: 1px solid #0f5c6b;
  border-radius: 0.4rem;
  padding: 0.35rem 0.5rem;
}
.match-title { display: block; font: 600 0.86rem/1.3 "Segoe UI", sans-serif; }
.match-path { display: block; color: var(--muted); font: 0.72rem/1.3 "Segoe UI", sans-serif; word-break: break-all; }
.note-app { padding: 0.7rem 0.9rem 2.4rem; }
.note-app main { max-width: 46rem; margin-top: 0.8rem; }
.crumb { margin: 0.25rem 0 0; font: 0.85rem/1.3 "Segoe UI", sans-serif; }
.note-path {
  font-family: "Segoe UI", sans-serif;
  color: var(--muted);
  font-size: 0.85rem;
  margin-top: 0;
}
main h1, main h2, main h3, main h4 { line-height: 1.25; font-family: "Segoe UI", sans-serif; }
main pre {
  overflow: auto;
  background: var(--code);
  padding: 0.75rem 0.9rem;
  border-radius: 0.2rem;
}
main code { font-family: ui-monospace, "Cascadia Code", "Source Code Pro", monospace; font-size: 0.88em; }
main table { border-collapse: collapse; width: 100%; font-size: 0.92rem; }
main th, main td { border: 1px solid var(--line); padding: 0.28rem 0.45rem; vertical-align: top; }
main blockquote {
  margin-left: 0;
  padding-left: 0.9rem;
  border-left: 3px solid var(--line);
  color: #3d453f;
}
.link-strip {
  margin-top: 1.5rem;
  padding-top: 0.7rem;
  border-top: 1px solid var(--line);
  font-family: "Segoe UI", sans-serif;
  font-size: 0.92rem;
}
.strip-label {
  margin: 0.55rem 0 0.15rem;
  font-size: 0.72rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--muted);
}
.link-strip ul { list-style: none; margin: 0; padding: 0; }
.link-strip li { margin: 0.12rem 0; }
a.current { font-weight: 600; }
@media (max-width: 980px) {
  .banner { display: block; }
  .search { margin-top: 0.6rem; }
  .era h3, .era a { white-space: normal; }
}
"""


def _page_csp(nonce: str) -> str:
    return (
        "default-src 'none'; "
        "style-src 'unsafe-inline'; "
        f"script-src 'nonce-{nonce}'; "
        "img-src 'self'; "
        "connect-src 'self'; "
        "base-uri 'none'; "
        "form-action 'self'; "
        "frame-ancestors 'none'"
    )


def _document(title: str, body: str) -> tuple[str, str]:
    nonce = secrets.token_urlsafe(16)
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer">
<meta name="robots" content="noindex">
<title>{title}</title>
<style>{PAGE_STYLE}</style>
</head>
<body>
{body}
<script nonce="{nonce}">{APP_SCRIPT}</script>
</body>
</html>
"""
    return page, _page_csp(nonce)


def _era_node_label(path: str) -> str:
    """The note's own file name, short enough to sit on the era map."""
    name = path.rsplit('/', 1)[-1]
    if name.lower().endswith('.md'):
        name = name[:-3]
    elif name.lower().endswith('.markdown'):
        name = name[:-9]
    return name


def _short(text: str, limit: int) -> str:
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) <= limit:
        return text
    return text[:limit - 1].rstrip() + '...'


def _area_href(area_id: str, section: str | None = None, query: str = '') -> str:
    params = [('area', area_id)]
    if section:
        params.append(('section', section))
    if query:
        params.append(('q', query))
    return '/?' + urllib.parse.urlencode(params)


def _box_center(area_id: str) -> tuple[float, float]:
    x, y = _DIAGRAM_BOXES[area_id]
    return x + _BOX_W / 2, y + _BOX_H / 2


def _architecture_svg(focus: str | None) -> str:
    lines = []
    labels = []
    for src, dst, label in _DIAGRAM_EDGES:
        x1, y1 = _box_center(src)
        x2, y2 = _box_center(dst)
        lines.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}"></line>')
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        if abs(x2 - x1) >= abs(y2 - y1):
            my -= 8
        else:
            mx += 36
        labels.append(
            f'<text class="edge-label" x="{mx:.0f}" y="{my:.0f}" text-anchor="middle">'
            f'{html.escape(label)}</text>'
        )
    boxes = []
    for area in AREAS:
        area_id = area['id']
        if area_id not in _DIAGRAM_BOXES:
            continue
        x, y = _DIAGRAM_BOXES[area_id]
        href = html.escape(_area_href(area_id), quote=True)
        current = ' is-on' if area_id == focus else ''
        aria = ' aria-current="true"' if area_id == focus else ''
        name = html.escape(area['name'])
        blurb = html.escape(area['blurb'])
        cx = x + _BOX_W / 2
        boxes.append(
            f'<a class="area-box{current}" href="{href}" data-area="{area_id}"{aria}>'
            f'<rect x="{x}" y="{y}" width="{_BOX_W}" height="{_BOX_H}" rx="10"></rect>'
            f'<text class="name" x="{cx:.0f}" y="{y + 32}" text-anchor="middle">{name}</text>'
            f'<text class="blurb" x="{cx:.0f}" y="{y + 52}" text-anchor="middle">{blurb}</text>'
            f'</a>'
        )
    label = html.escape(
        'Architecture of the notes: client versions, protocol, formats, '
        'NPC scripts, Graal3D, Torque, tools, labs and archives.',
        quote=True,
    )
    return (
        f'<svg class="arch" viewBox="0 0 {_DIAGRAM_W} {_DIAGRAM_H}" role="img" aria-label="{label}">'
        + ''.join(lines) + ''.join(labels) + ''.join(boxes)
        + '</svg>'
    )


def _version_html(index: list[dict]) -> str:
    by_path = {entry['path']: entry for entry in index}
    columns = []
    for era, entries in version_columns(index):
        links = []
        for entry in entries:
            href = html.escape(note_href(entry['path']), quote=True)
            rel = html.escape(entry['path'], quote=True)
            node = html.escape(_era_node_label(entry['path']))
            title = html.escape(entry['title'], quote=True)
            links.append(f'<a href="{href}" data-note="{rel}" title="{title}">{node}</a>')
        columns.append(
            f'<section class="era"><h3>{html.escape(era)}</h3>{"".join(links)}</section>'
        )
    matrix = ''
    entry = by_path.get(MATRIX_NOTE)
    if entry:
        href = html.escape(note_href(entry['path']), quote=True)
        rel = html.escape(entry['path'], quote=True)
        title = html.escape(entry['title'])
        matrix = f'<p class="matrix"><a href="{href}" data-note="{rel}">{title}</a></p>'
    return matrix + f'<div class="version-map">{"".join(columns)}</div>'


def _index_strip(index: list[dict]) -> str:
    by_path = {entry['path']: entry for entry in index}
    links = []
    for path in INDEX_NOTES:
        entry = by_path.get(path)
        if not entry:
            continue
        href = html.escape(note_href(path), quote=True)
        rel = html.escape(path, quote=True)
        title = html.escape(entry['title'])
        links.append(f'<a href="{href}" data-note="{rel}">{title}</a>')
    if not links:
        return ''
    return '<p class="index-strip"><span>Corpus index</span> ' + ' '.join(links) + '</p>'


def _sections_html(index: list[dict], area_id: str, current: str | None) -> str:
    items = []
    for name, count in area_sections(index, area_id):
        href = html.escape(_area_href(area_id, name), quote=True)
        cls = ' class="is-on"' if name == current else ''
        items.append(
            f'<a{cls} href="{href}">{html.escape(name)}<span>{count}</span></a>'
        )
    if not items and not current:
        return ''
    whole = ''
    if current:
        href = html.escape(_area_href(area_id), quote=True)
        whole = f'<a href="{href}">Whole area</a>'
    return f'<nav class="sections" aria-label="Sections">{whole}{"".join(items)}</nav>'


def _match_nodes(notes: list[dict]) -> str:
    items = []
    for entry in notes:
        href = html.escape(note_href(entry['path']), quote=True)
        rel = html.escape(entry['path'], quote=True)
        title_attr = html.escape(entry['title'], quote=True)
        title = html.escape(entry['title'])
        path = html.escape(entry['path'])
        items.append(
            f'<a class="web-node match" href="{href}" data-note="{rel}" '
            f'data-path="{rel}" data-title="{title_attr}">'
            f'<span class="match-title">{title}</span>'
            f'<span class="match-path">{path}</span></a>'
        )
    return '<div class="match-row">' + ''.join(items) + '</div>'


def _web_svg(notes: list[dict], edges: list[tuple[str, str]]) -> str:
    if not notes:
        return ''
    count = len(notes)
    cols = 4 if count > 8 else (3 if count > 3 else count)
    cols = max(cols, 1)
    box_w, box_h = 188, 58
    gap_x, gap_y = 28, 26
    margin = 12
    placed = []
    for i, note in enumerate(notes):
        col = i % cols
        row = i // cols
        x = margin + col * (box_w + gap_x)
        y = margin + row * (box_h + gap_y)
        placed.append((note, x, y))
    rows = (count + cols - 1) // cols
    width = margin * 2 + cols * box_w + (cols - 1) * gap_x
    height = margin * 2 + rows * box_h + (rows - 1) * gap_y
    pos = {note['path']: (x, y) for note, x, y in placed}
    lines = []
    for src, dst in edges:
        if src not in pos or dst not in pos:
            continue
        x1 = pos[src][0] + box_w / 2
        y1 = pos[src][1] + box_h / 2
        x2 = pos[dst][0] + box_w / 2
        y2 = pos[dst][1] + box_h / 2
        src_attr = html.escape(src, quote=True)
        dst_attr = html.escape(dst, quote=True)
        lines.append(
            f'<line class="web-edge" x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
            f'data-from="{src_attr}" data-to="{dst_attr}"></line>'
        )
    nodes = []
    for note, x, y in placed:
        rel = html.escape(note['path'], quote=True)
        title_attr = html.escape(note['title'], quote=True)
        href = html.escape(note_href(note['path']), quote=True)
        cx = x + box_w / 2
        title = html.escape(_short(note['title'], 28))
        path = html.escape(_short(note['path'], 32))
        nodes.append(
            f'<a class="web-node" href="{href}" data-note="{rel}" data-path="{rel}" '
            f'data-title="{title_attr}">'
            f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="8"></rect>'
            f'<text x="{cx:.0f}" y="{y + 24}" text-anchor="middle">{title}</text>'
            f'<text class="web-path" x="{cx:.0f}" y="{y + 42}" text-anchor="middle">{path}</text>'
            f'</a>'
        )
    return (
        f'<svg class="web" viewBox="0 0 {width} {height}" role="group" aria-label="Linked notes">'
        + ''.join(lines) + ''.join(nodes)
        + '</svg>'
    )


def _web_region(index, edges, area_id, section, query):
    if query and not area_id:
        matched = filter_notes(index, query)
        shown = matched[:SEARCH_CAP]
        if not matched:
            return '', f'<p class="web-note">No note matches {html.escape(query)}.</p>'
        extra = ''
        if len(matched) > len(shown):
            extra = f' Showing {len(shown)} of {len(matched)}.'
        note = (
            f'<p class="web-note">Matches for {html.escape(query)}.{extra} '
            '<a href="/">Clear</a></p>'
        )
        return _match_nodes(shown), note
    if not area_id:
        return '', (
            '<p class="web-note">Choose an area. The web draws the notes in that '
            'cluster that link to each other, not every file in the repository. '
            'Search still filters by title or path.</p>'
        )
    area = _AREA_BY_ID[area_id]
    name = html.escape(area['name'])
    notes, total, mode = select_web(index, edges, area_id, section, query)
    sections = '' if query else _sections_html(index, area_id, section)
    if mode == 'search':
        extra = ''
        if total > len(notes):
            extra = f' Showing {len(notes)} of {total}.'
        note = f'<p class="web-note">{name}: matches for {html.escape(query)}.{extra}</p>'
        body = _match_nodes(notes) if notes else ''
        return sections + body, note
    if mode == 'narrow':
        note = (
            f'<p class="web-note">{name} has {total} notes. Open a section or '
            'search. They are not listed all at once.</p>'
        )
        return sections, note
    if mode == 'web' and len(notes) < total:
        note = (
            f'<p class="web-note">{name}: {len(notes)} linked notes of {total}. '
            'Open a section or search for the rest.</p>'
        )
    else:
        note = f'<p class="web-note">{name}: {len(notes)} notes in this cluster.</p>'
    return sections + _web_svg(notes, edges), note


def render_home(index, edges, area, section, query) -> tuple[str, str]:
    """Home page: architecture, one area's link web, and the version map."""
    area_id = area if area in _AREA_BY_ID else None
    if section and not (area_id and valid_section(section)):
        section = None
    query = clean_query(query)
    web_html, web_note = _web_region(index, edges, area_id, section, query)
    value = html.escape(query, quote=True)
    article = f"""
<div class="home">
<header class="banner">
<div>
<p class="mark">Graal analysis</p>
<h1>Notes</h1>
<p class="local">Local only. This page does not phone home.</p>
</div>
<form class="search" action="/" method="get">
<label class="search-label" for="search">Filter by title or path</label>
<input id="search" name="q" type="search" autocomplete="off" spellcheck="false" placeholder="title or path" value="{value}" autofocus>
</form>
</header>
{_index_strip(index)}
<section class="panel architecture" id="architecture">
<h2>Architecture</h2>
<p class="caption">Open an area to see that cluster. Lines join clients to protocol, formats and NPC scripts; Graal3D to the protocol and to Torque; tools to the labs; archives to the formats.</p>
{_architecture_svg(area_id)}
</section>
<section class="panel versions" id="versions">
<h2>Versions</h2>
<p class="caption">Left to right, the eras named in these notes. A name is a link only when that note is in the repository.</p>
{_version_html(index)}
</section>
<section class="panel web-panel" id="web">
<h2>Link web</h2>
{web_note}
<p id="count"></p>
{web_html}
</section>
</div>
"""
    return _document('Notes navigator', article)


def render_note_page(index, rel, article) -> tuple[str, str]:
    title_text = next((entry['title'] for entry in index if entry['path'] == rel), rel)
    area = area_for(rel)
    area_name = html.escape(area['name'])
    href = html.escape(_area_href(area['id']), quote=True)
    body = f"""
<div class="note-app">
<header class="banner">
<div>
<p class="mark">Graal analysis</p>
<h1 class="site">Notes</h1>
<p class="crumb"><a href="/">Map</a> · <a href="{href}">{area_name}</a></p>
<p class="local">Local only. This page does not phone home.</p>
</div>
<form class="search" action="/" method="get">
<label class="search-label" for="search">Filter by title or path</label>
<input id="search" name="q" type="search" autocomplete="off" spellcheck="false" placeholder="title or path">
</form>
</header>
<main id="doc-holder">{article}</main>
</div>
"""
    title = html.escape(title_text) + ' — Notes navigator'
    return _document(title, body)


def render_note_article(repo: Path, raw: str, edges=None, index=None) -> tuple[str, str]:
    rel, text = read_note(repo, raw)
    body = render_markdown(text, rel, repo)
    strip = ''
    if edges is not None and index is not None:
        strip = link_strip_html(rel, edges, index)
    return rel, article_html(rel, body, strip)


class NotesServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = False

    def __init__(self, server_address, repo: Path, index: list[dict], edges: list[tuple[str, str]]):
        self.repo = Path(repo)
        self.index = index
        self.edges = edges
        super().__init__(server_address, NotesHandler)


class NotesHandler(BaseHTTPRequestHandler):
    server: NotesServer

    def log_message(self, fmt, *args):
        return

    def do_GET(self):
        self._respond(write_body=True)

    def do_HEAD(self):
        self._respond(write_body=False)

    def do_POST(self):
        self._plain(405, 'method not allowed\n')

    def do_PUT(self):
        self._plain(405, 'method not allowed\n')

    def do_DELETE(self):
        self._plain(405, 'method not allowed\n')

    def _plain(self, status: int, body: str):
        self._send(status, body, 'text/plain; charset=utf-8', PLAIN_CSP, write_body=True)

    def _send(self, status: int, body: str, content_type: str, csp: str, write_body: bool):
        data = body.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', csp)
        self.send_header('Referrer-Policy', 'no-referrer')
        self.end_headers()
        if write_body and self.command != 'HEAD':
            self.wfile.write(data)

    def _respond(self, write_body: bool):
        parsed = urllib.parse.urlparse(self.path)
        route = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        repo = self.server.repo
        index = self.server.index
        edges = self.server.edges

        def one(key: str) -> str:
            values = query.get(key) or ['']
            return values[0] if values else ''

        if route in ('/', '/index.html'):
            area = one('area')
            if area not in _AREA_BY_ID:
                area = None
            section = one('section')
            if not valid_section(section):
                section = None
            page, csp = render_home(index, edges, area, section, clean_query(one('q')))
            self._send(200, page, 'text/html; charset=utf-8', csp, write_body)
            return
        if route == '/note':
            raw = one('path')
            fragment = one('fragment') == '1'
            try:
                rel, article = render_note_article(repo, raw, edges, index)
            except OutsideRepo:
                self._send(403, 'refused\n', 'text/plain; charset=utf-8', PLAIN_CSP, write_body)
                return
            except NoteNotFound:
                self._send(404, 'not found\n', 'text/plain; charset=utf-8', PLAIN_CSP, write_body)
                return
            if fragment:
                self._send(200, article, 'text/html; charset=utf-8', FRAGMENT_CSP, write_body)
                return
            page, csp = render_note_page(index, rel, article)
            self._send(200, page, 'text/html; charset=utf-8', csp, write_body)
            return
        self._send(404, 'not found\n', 'text/plain; charset=utf-8', PLAIN_CSP, write_body)


def make_server(repo: Path, host: str | None = None, port: int = DEFAULT_PORT) -> NotesServer:
    bind = LOOPBACK if host is None else host
    if not is_loopback_host(bind):
        raise ValueError('notes navigator listens on the loopback address only')
    if not isinstance(port, int) or not (0 <= port <= 65535):
        raise ValueError('port must be between 0 and 65535')
    root = Path(repo).resolve()
    if not root.is_dir():
        raise FileNotFoundError(root)
    index = build_index(root)
    edges = build_edges(root, index)
    return NotesServer((bind, port), root, index, edges)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description='Browse Graal analysis notes on the loopback address.'
    )
    parser.add_argument(
        '--host',
        default=LOOPBACK,
        help='bind address (the loopback address only; any other host is refused)',
    )
    parser.add_argument(
        '--port',
        type=int,
        default=DEFAULT_PORT,
        help='TCP port (default 8765, not a lab server port)',
    )
    parser.add_argument(
        '--repo',
        type=Path,
        default=None,
        help='repository root (defaults to this checkout)',
    )
    args = parser.parse_args(argv)
    if not is_loopback_host(args.host):
        print('The notes navigator listens on the loopback address only.', file=sys.stderr)
        return 2
    if not (1 <= args.port <= 65535):
        print('Port must be between 1 and 65535.', file=sys.stderr)
        return 2
    repo = args.repo if args.repo is not None else default_repo()
    try:
        server = make_server(repo, args.host, args.port)
    except (ValueError, FileNotFoundError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f'Notes navigator on the loopback address, port {args.port}.', flush=True)
    print('Local only. It does not phone home.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
    finally:
        server.server_close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
