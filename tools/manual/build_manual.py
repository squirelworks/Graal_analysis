#!/usr/bin/env python3
"""Build the Graal Technical Reference Manual as one PDF.

From the repository root, on Linux, macOS or Windows:

    python tools/manual/build_manual.py
    python tools/manual/build_manual.py --out some/dir/trm.pdf
    python tools/manual/build_manual.py --version 0.0.3

Steps: join the chapter files in manual order (dropping the
`<!-- manual: ... -->` marker lines), turn them into one HTML page with
pandoc, then print that page to an A4 PDF with Chromium. The default output
is `manual/pdf/graal-trm.pdf`, or `manual/pdf/graal-trm-<version>.pdf` with
`--version`. Build it into the repo only when the owner
asks for a build (issue #191, work-plan item 15).

Needs:
  - pandoc on PATH, or the `pypandoc_binary` package (its bundled pandoc);
  - the `playwright` package and its Chromium
    (`pip install playwright` then `python -m playwright install chromium`).
  - the `pypdf` package, which writes the bookmarks (the PDF outline). Without
    it the PDF is still built, with a warning and no bookmarks.
    `--chromium PATH` or the PLAYWRIGHT_CHROMIUM_EXECUTABLE variable points it
    at a Chromium that is already installed.

All paths go through pathlib and the work folder comes from tempfile, so
nothing depends on a Unix layout.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TITLE = 'Graal Technical Reference Manual'
MARKER = '<!-- manual:'

# Chapter order. A string is a single file; a tuple is a folder whose `.md`
# files are taken in name order.
ORDER = (
    '00-conventions.md',
    '01-builds.md',
    ('02-protocol',),
    ('03-formats',),
    ('04-behaviour',),
    '05-servers.md',
    '06-listserver.md',
    '07-rc-nc.md',
    ('08-scripting',),
    '09-graal3d.md',
    '10-torque.md',
    '11-tools.md',
)

CSS = """\
body{font-family:"DejaVu Sans","Helvetica Neue",Arial,sans-serif;font-size:9pt;line-height:1.35;max-width:none;margin:0}
h1{page-break-before:always;font-size:18pt;border-bottom:2px solid #333}
h2{font-size:13pt;margin-top:1.4em} h3{font-size:11pt} h4{font-size:10pt}
table{border-collapse:collapse;width:100%;margin:.5em 0;font-size:8pt;page-break-inside:auto}
th,td{border:1px solid #999;padding:2px 4px;vertical-align:top;word-break:break-word}
th{background:#eee} tr{page-break-inside:avoid}
code{font-family:"DejaVu Sans Mono",Consolas,Menlo,monospace;font-size:8pt;background:#f4f4f4}
pre{background:#f4f4f4;padding:4px;font-size:8pt;white-space:pre-wrap}
#TOC{page-break-after:always} #TOC ul{list-style:none;padding-left:1em}
"""

FOOTER = (
    '<div style="font-size:7pt;width:100%;text-align:center">'
    '<span class="pageNumber"></span> / <span class="totalPages"></span></div>'
)


def chapter_files(manual: Path) -> list[Path]:
    """The chapter files in manual order, then the appendices."""
    files: list[Path] = []
    for entry in ORDER:
        if isinstance(entry, tuple):
            files.extend(sorted((manual / entry[0]).glob('*.md')))
        else:
            files.append(manual / entry)
    files.extend(sorted(manual.glob('app-*.md')))
    missing = [str(f) for f in files if not f.is_file()]
    if missing:
        raise SystemExit('missing chapter files: ' + ', '.join(missing))
    return files


def join_chapters(files: list[Path]) -> str:
    """One Markdown text, marker lines dropped, chapters split by blank lines."""
    parts = []
    for path in files:
        lines = path.read_text(encoding='utf-8').splitlines()
        parts.append('\n'.join(l for l in lines if not l.startswith(MARKER)))
    return '\n\n\n'.join(parts) + '\n'


def find_pandoc() -> str:
    found = shutil.which('pandoc')
    if found:
        return found
    try:
        import pypandoc  # type: ignore[import-not-found]

        return pypandoc.get_pandoc_path()
    except (ImportError, OSError):
        raise SystemExit('pandoc not found: install pandoc or `pip install pypandoc_binary`')


def commit_of(root: Path) -> str:
    try:
        out = subprocess.run(
            ['git', '-C', str(root), 'rev-parse', '--short', 'HEAD'],
            capture_output=True, text=True, check=True,
        )
        return out.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return 'unknown'


def build_html(markdown: str, work: Path, commit: str, pandoc: str,
               version: str | None = None) -> Path:
    src = work / 'all.md'
    src.write_text(markdown, encoding='utf-8')
    head = work / 'head.html'
    head.write_text('<style>\n' + CSS + '</style>\n', encoding='utf-8')
    html = work / 'trm.html'
    subprocess.run(
        [
            pandoc, str(src), '-f', 'gfm', '-t', 'html5', '-s',
            '--toc', '--toc-depth=2',
            '--metadata', f'title={TITLE}',
            '--metadata', 'subtitle=' + (f'version {version}, ' if version else '') + f'build of {commit}',
            '-H', str(head), '-o', str(html),
        ],
        check=True,
    )
    return html


def print_pdf(html: Path, out: Path, chromium: str | None) -> None:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore[import-not-found]
    except ImportError:
        raise SystemExit('playwright not found: `pip install playwright` then '
                         '`python -m playwright install chromium`')
    launch = {'executable_path': chromium} if chromium else {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(**launch)
        page = browser.new_page()
        page.goto(html.resolve().as_uri())
        page.pdf(
            path=str(out), format='A4',
            margin={'top': '14mm', 'bottom': '14mm', 'left': '12mm', 'right': '12mm'},
            display_header_footer=True, header_template='<span></span>',
            footer_template=FOOTER,
        )
        browser.close()


class _Headings(HTMLParser):
    """Collect (level, id, text) for every h1 and h2 that carries an id."""

    def __init__(self) -> None:
        super().__init__()
        self.found: list[tuple[int, str, str]] = []
        self._cur: tuple[int, str] | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in ('h1', 'h2') and dict(attrs).get('id'):
            self._cur = (int(tag[1]), dict(attrs)['id'])
            self._text = []

    def handle_data(self, data):
        if self._cur:
            self._text.append(data)

    def handle_endtag(self, tag):
        if self._cur and tag == f'h{self._cur[0]}':
            text = ' '.join(''.join(self._text).split())
            self.found.append((self._cur[0], self._cur[1], text))
            self._cur = None


def outline_entries(html: str) -> list[tuple[int, str, str]]:
    """(depth, id, title) for the bookmarks, nested Part > chapter > section.

    A Part and its chapters are both h1 (`# 2 Wire protocol`, `# 2.1 Framing`);
    a chapter whose number starts with the open Part's number goes one level
    under it. Sections (h2) go one level under the h1 before them. The title
    block's own heading, the pandoc contents list and the Part indexes'
    `Chapters` lists are skipped.
    """
    parser = _Headings()
    parser.feed(html)
    out: list[tuple[int, str, str]] = []
    part = None
    h1_depth = 0
    for level, ident, text in parser.found:
        if ident in ('TOC', 'title-block-header') or (level == 2 and text == 'Chapters'):
            continue
        number = text.split(' ', 1)[0]
        if level == 1:
            if part and '.' in number and number.split('.')[0] == part:
                h1_depth = 1
            else:
                part = number if re.fullmatch(r'[0-9A-Z]+', number) else None
                h1_depth = 0
            out.append((h1_depth, ident, text))
        else:
            out.append((h1_depth + 1, ident, text))
    return out


def add_outline(pdf_path: Path, html: str) -> int:
    """Write the bookmarks into the PDF from the h1/h2 named destinations.

    Chromium makes a named destination for each heading the contents list
    links to (pandoc `--toc-depth=2`). Returns the number of bookmarks, or
    -1 when pypdf is not installed.
    """
    try:
        from pypdf import PdfReader, PdfWriter  # type: ignore[import-not-found]
        from pypdf.generic import Fit  # type: ignore[import-not-found]
    except ImportError:
        print('warning: pypdf not found, so the PDF has no bookmarks (`pip install pypdf`)',
              file=sys.stderr)
        return -1
    reader = PdfReader(str(pdf_path))
    dests = reader.named_destinations
    writer = PdfWriter(clone_from=reader)
    parents: list = []
    count = 0
    for depth, ident, title in outline_entries(html):
        dest = dests.get('/' + ident) or dests.get(ident)
        if dest is None:
            continue
        page = reader.get_destination_page_number(dest)
        parent = parents[depth - 1] if 0 < depth <= len(parents) else None
        item = writer.add_outline_item(title, page, parent=parent,
                                       fit=Fit.xyz(top=dest.top))
        del parents[depth:]
        parents.append(item)
        count += 1
    writer.page_mode = '/UseOutlines'
    with open(pdf_path, 'wb') as fh:
        writer.write(fh)
    return count


def scrub_browser_version(pdf: bytes) -> bytes:
    """Rewrite the dotted Chrome version in the PDF's Creator with underscores.

    The dotted four-part version looks like an IP literal to the repo's leak
    check. The replacement keeps the byte length, so xref offsets stay valid.
    """
    return re.sub(rb'(Chrome/)(\d+(?:\.\d+){3})',
                  lambda m: m.group(1) + m.group(2).replace(b'.', b'_'), pdf)


def page_count(pdf: bytes) -> int:
    """Pages in a PDF: its `/Type /Page` objects (neither Chromium nor pypdf's
    default writer uses object streams)."""
    return len(re.findall(rb'/Type\s*/Page(?![a-zA-Z])', pdf))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--root', type=Path, default=ROOT, help='repository root')
    ap.add_argument('--version', help='edition label, such as 0.0.3: shown on the title page and '
                    'used in the default file name')
    ap.add_argument('--out', type=Path,
                    help='PDF path (default manual/pdf/graal-trm[-VERSION].pdf)')
    ap.add_argument('--html', type=Path, help='also keep the HTML page here')
    ap.add_argument('--chromium', default=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE'),
                    help='Chromium executable to use instead of the Playwright download')
    args = ap.parse_args(argv)

    root = args.root.resolve()
    name = f'graal-trm-{args.version}.pdf' if args.version else 'graal-trm.pdf'
    out = (args.out or root / 'manual' / 'pdf' / name).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    commit = commit_of(root)
    markdown = join_chapters(chapter_files(root / 'manual'))
    pandoc = find_pandoc()
    with tempfile.TemporaryDirectory(prefix='graal-trm-') as tmp:
        html = build_html(markdown, Path(tmp), commit, pandoc, args.version)
        if args.html:
            shutil.copyfile(html, args.html)
        print_pdf(html, out, args.chromium)
        marks = add_outline(out, html.read_text(encoding='utf-8'))
    pdf = scrub_browser_version(out.read_bytes())
    out.write_bytes(pdf)
    pages = page_count(pdf)
    print(f'built {out} from {commit}: {pages} pages'
          + (f', {marks} bookmarks' if marks >= 0 else ', no bookmarks'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
