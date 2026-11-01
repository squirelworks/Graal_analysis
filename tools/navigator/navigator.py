#!/usr/bin/env python3
"""Local browser for the markdown notes in this repository.

The index is built when the process starts. Search runs in the browser.
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


def article_html(rel: str, body: str) -> str:
    safe = html.escape(rel, quote=True)
    return (
        f'<article id="doc" data-path="{safe}">'
        f'<p class="note-path">{html.escape(rel)}</p>'
        f'{body}'
        f'</article>'
    )


PLACEHOLDER = (
    '<article id="doc">'
    '<h1>Notes navigator</h1>'
    '<p>Choose a note on the left. The filter compares the title and the path '
    'in this browser. Nothing is sent away for search.</p>'
    '</article>'
)

APP_SCRIPT = """
(function () {
  var input = document.getElementById("search");
  var items = Array.prototype.slice.call(document.querySelectorAll(".note-item"));
  var blocks = Array.prototype.slice.call(document.querySelectorAll(".folder-block"));
  var count = document.getElementById("count");

  // Same rule as note_matches(): empty query matches all; otherwise a
  // case-insensitive substring of the title or the path. No server search.
  function noteMatches(title, path, query) {
    var q = String(query || "").trim().toLowerCase();
    if (!q) {
      return true;
    }
    title = String(title || "").toLowerCase();
    path = String(path || "").toLowerCase();
    return title.indexOf(q) !== -1 || path.indexOf(q) !== -1;
  }

  function applyFilter() {
    var query = input.value;
    var shown = 0;
    items.forEach(function (item) {
      var ok = noteMatches(item.getAttribute("data-title"), item.getAttribute("data-path"), query);
      item.hidden = !ok;
      if (ok) {
        shown += 1;
      }
    });
    blocks.forEach(function (block) {
      block.hidden = !block.querySelector(".note-item:not([hidden])");
    });
    count.textContent = shown + " of " + items.length;
  }

  input.addEventListener("input", applyFilter);
  applyFilter();

  function mark(path) {
    Array.prototype.forEach.call(document.querySelectorAll("a[data-note]"), function (link) {
      link.classList.toggle("current", link.getAttribute("data-note") === path);
    });
  }

  function showNote(path, hash, push) {
    var fragment = "/note?path=" + encodeURIComponent(path) + "&fragment=1";
    fetch(fragment).then(function (res) {
      if (!res.ok) {
        throw new Error(String(res.status));
      }
      return res.text();
    }).then(function (page) {
      var main = document.getElementById("doc-holder");
      main.innerHTML = page;
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
      if (main && main.scrollTo) {
        main.scrollTo(0, 0);
      }
    }).catch(function () {
      window.location.assign("/note?path=" + encodeURIComponent(path) + (hash || ""));
    });
  }

  document.body.addEventListener("click", function (event) {
    var link = event.target.closest("a[data-note]");
    if (!link) {
      return;
    }
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
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
  --paper: #f6f3ec;
  --side: #24302c;
  --side-ink: #f4f0e6;
  --muted: #5e675f;
  --line: #d9d2c5;
  --accent: #0f5c6b;
  --code: #efe8dc;
}
* { box-sizing: border-box; }
html, body { margin: 0; height: 100%; }
body {
  color: var(--ink);
  background: var(--paper);
  font: 18px/1.55 Palatino, "Palatino Linotype", "Iowan Old Style", Georgia, serif;
}
.app { display: flex; min-height: 100%; }
aside {
  width: 22rem;
  flex: none;
  background: var(--side);
  color: var(--side-ink);
  padding: 1.1rem 0.9rem 2rem;
  height: 100vh;
  overflow: auto;
  font-family: "Segoe UI", sans-serif;
}
.mark {
  margin: 0;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-size: 0.72rem;
  color: #b7c7bf;
}
aside h1 {
  margin: 0.15rem 0 0.35rem;
  font: 600 1.45rem/1.2 "Segoe UI", sans-serif;
}
.local { margin: 0 0 0.9rem; color: #c5d2cb; font-size: 0.86rem; }
.search-label { display: block; font-size: 0.78rem; margin-bottom: 0.25rem; color: #d5e0da; }
#search {
  width: 100%;
  padding: 0.45rem 0.55rem;
  border: 0;
  border-radius: 0.25rem;
  font: 0.95rem/1.3 "Segoe UI", sans-serif;
  color: var(--ink);
  background: #f7f4ee;
}
#count { margin: 0.55rem 0 0; color: #b7c4be; font-size: 0.78rem; }
.folder {
  margin: 1rem 0 0.3rem;
  font-size: 0.72rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #9fb0a8;
  font-weight: 600;
}
.folder-block ul { list-style: none; margin: 0; padding: 0; }
.note-item { margin: 0 0 0.15rem; }
.note-item a {
  display: block;
  color: inherit;
  text-decoration: none;
  padding: 0.28rem 0.4rem;
  border-radius: 0.2rem;
  font-size: 0.92rem;
}
.note-item a:hover, .note-item a.current { background: #345049; }
.path { display: block; color: #9aada5; font-size: 0.72rem; font-weight: 400; }
main {
  flex: 1;
  height: 100vh;
  overflow: auto;
  padding: 1.8rem 2.2rem 4rem;
}
main article { max-width: 46rem; }
.note-path {
  font-family: "Segoe UI", sans-serif;
  color: var(--muted);
  font-size: 0.85rem;
  margin-top: 0;
}
main h1, main h2, main h3, main h4 { line-height: 1.25; font-family: "Segoe UI", sans-serif; }
main a { color: var(--accent); }
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
.note-item[hidden], .folder-block[hidden] { display: none; }
@media (max-width: 860px) {
  .app { display: block; }
  aside, main { width: auto; height: auto; position: relative; }
}
"""


def _sidebar(index: list[dict], current: str | None) -> str:
    groups: list[tuple[str, list[dict]]] = []
    for entry in index:
        if not groups or groups[-1][0] != entry['folder']:
            groups.append((entry['folder'], []))
        groups[-1][1].append(entry)
    chunks = []
    for folder, entries in groups:
        items = []
        for entry in entries:
            title = html.escape(entry['title'])
            title_attr = html.escape(entry['title'], quote=True)
            path = html.escape(entry['path'])
            path_attr = html.escape(entry['path'], quote=True)
            href = html.escape(note_href(entry['path']), quote=True)
            current_class = ' class="current"' if entry['path'] == current else ''
            items.append(
                f'<li class="note-item" data-title="{title_attr}" data-path="{path_attr}">'
                f'<a href="{href}" data-note="{path_attr}"{current_class}>{title}'
                f'<span class="path">{path}</span></a></li>'
            )
        folder_html = html.escape(folder)
        chunks.append(
            f'<section class="folder-block" data-folder="{html.escape(folder, quote=True)}">'
            f'<h2 class="folder">{folder_html}</h2><ul>{"".join(items)}</ul></section>'
        )
    return ''.join(chunks)


def _page_csp(nonce: str) -> str:
    return (
        "default-src 'none'; "
        "style-src 'unsafe-inline'; "
        f"script-src 'nonce-{nonce}'; "
        "img-src 'self'; "
        "connect-src 'self'; "
        "base-uri 'none'; "
        "form-action 'none'; "
        "frame-ancestors 'none'"
    )


def render_page(index: list[dict], article: str, current: str | None) -> tuple[str, str]:
    nonce = secrets.token_urlsafe(16)
    if current:
        title_text = next((entry['title'] for entry in index if entry['path'] == current), current)
        title = html.escape(title_text) + ' — Notes navigator'
        autofocus = ''
    else:
        title = 'Notes navigator'
        autofocus = ' autofocus'
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
<div class="app">
<aside>
<p class="mark">Graal analysis</p>
<h1>Notes</h1>
<p class="local">Local only. This page does not phone home.</p>
<label class="search-label" for="search">Filter by title or path</label>
<input id="search" type="search" autocomplete="off" spellcheck="false" placeholder="title or path"{autofocus}>
<p id="count"></p>
<nav id="list">{_sidebar(index, current)}</nav>
</aside>
<main id="doc-holder">{article}</main>
</div>
<script nonce="{nonce}">{APP_SCRIPT}</script>
</body>
</html>
"""
    return page, _page_csp(nonce)


def render_note_article(repo: Path, raw: str) -> tuple[str, str]:
    rel, text = read_note(repo, raw)
    body = render_markdown(text, rel, repo)
    return rel, article_html(rel, body)


class NotesServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = False

    def __init__(self, server_address, repo: Path, index: list[dict]):
        self.repo = Path(repo)
        self.index = index
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
        if route in ('/', '/index.html'):
            page, csp = render_page(index, PLACEHOLDER, None)
            self._send(200, page, 'text/html; charset=utf-8', csp, write_body)
            return
        if route == '/note':
            raw_values = query.get('path') or ['']
            raw = raw_values[0]
            fragment = (query.get('fragment') or [''])[0] == '1'
            try:
                rel, article = render_note_article(repo, raw)
            except OutsideRepo:
                self._send(403, 'refused\n', 'text/plain; charset=utf-8', PLAIN_CSP, write_body)
                return
            except NoteNotFound:
                self._send(404, 'not found\n', 'text/plain; charset=utf-8', PLAIN_CSP, write_body)
                return
            if fragment:
                self._send(200, article, 'text/html; charset=utf-8', FRAGMENT_CSP, write_body)
                return
            page, csp = render_page(index, article, rel)
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
    return NotesServer((bind, port), root, index)


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
