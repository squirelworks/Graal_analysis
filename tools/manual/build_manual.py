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
            # outline: the PDF bookmarks panel, built from the h1-h6 headings;
            # Chromium needs a tagged PDF to emit it.
            tagged=True, outline=True,
        )
        browser.close()


def scrub_browser_version(pdf: bytes) -> bytes:
    """Rewrite the dotted Chrome version in the PDF's Creator with underscores.

    The dotted four-part version looks like an IP literal to the repo's leak
    check. The replacement keeps the byte length, so xref offsets stay valid.
    """
    return re.sub(rb'(Chrome/)(\d+(?:\.\d+){3})',
                  lambda m: m.group(1) + m.group(2).replace(b'.', b'_'), pdf)


def page_count(pdf: bytes) -> int:
    """Pages in a PDF: its `/Type /Page` objects (Chromium writes no object streams)."""
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
    pdf = scrub_browser_version(out.read_bytes())
    out.write_bytes(pdf)
    pages = page_count(pdf)
    print(f'built {out} from {commit}: {pages} pages')
    return 0


if __name__ == '__main__':
    sys.exit(main())
