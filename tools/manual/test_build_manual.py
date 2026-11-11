"""Tests for tools/manual/build_manual.py. Standard library + pytest.

The PDF step itself runs in CI (the manual-pdf job); these tests cover the
parts that need no browser.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import build_manual  # noqa: E402


def test_chapter_order_covers_every_manual_file():
    manual = REPO / 'manual'
    files = build_manual.chapter_files(manual)
    rel = [f.relative_to(manual).as_posix() for f in files]
    assert rel[0] == '00-conventions.md'
    assert rel[-1] == 'app-g-tags.md'
    assert len(rel) == len(set(rel))
    every = {p.relative_to(manual).as_posix() for p in manual.rglob('*.md')} - {'README.md'}
    assert set(rel) == every


def test_chapter_order_is_by_part():
    rel = [f.relative_to(REPO / 'manual').as_posix()
           for f in build_manual.chapter_files(REPO / 'manual')]
    firsts = []
    for name in rel:
        key = name.split('/')[0][:2]
        if not firsts or firsts[-1] != key:
            firsts.append(key)
    assert firsts[:12] == [f'{n:02d}' for n in range(12)]
    assert all(k == 'ap' for k in firsts[12:])


def test_missing_chapter_fails(tmp_path):
    (tmp_path / '00-conventions.md').write_text('# 0\n', encoding='utf-8')
    with pytest.raises(SystemExit):
        build_manual.chapter_files(tmp_path)


def test_join_drops_marker_lines(tmp_path):
    a = tmp_path / 'a.md'
    b = tmp_path / 'b.md'
    a.write_text('<!-- manual: part=I -->\n# A\ntext\n', encoding='utf-8')
    b.write_text('# B\n<!-- manual: x -->\n', encoding='utf-8')
    out = build_manual.join_chapters([a, b])
    assert '<!-- manual:' not in out
    assert out.index('# A') < out.index('# B')
    assert '\n\n# B' in out


def test_page_count():
    pdf = (b'%PDF-1.4\n1 0 obj << /Type /Pages /Kids [2 0 R 3 0 R] /Count 2 >>\n'
           b'2 0 obj << /Type /Page /Parent 1 0 R >>\n'
           b'3 0 obj <</Type/Page/Parent 1 0 R>>\n')
    assert build_manual.page_count(pdf) == 2


@pytest.mark.skipif(shutil.which('pandoc') is None, reason='pandoc not installed')
def test_html_build(tmp_path):
    md = '<!-- manual: x -->\n# Part\n\n## Section\n\n| a | b |\n| --- | --- |\n| 1 | 2 |\n'
    html = build_manual.build_html(md, tmp_path, 'abc1234', build_manual.find_pandoc())
    text = html.read_text(encoding='utf-8')
    assert build_manual.TITLE in text
    assert 'build of abc1234' in text
    assert '<table' in text and 'id="TOC"' in text


@pytest.mark.skipif(shutil.which('pandoc') is None, reason='pandoc not installed')
def test_html_build_with_version(tmp_path):
    html = build_manual.build_html('# Part\n', tmp_path, 'abc1234', build_manual.find_pandoc(), '0.0.3')
    assert 'version 0.0.3, build of abc1234' in html.read_text(encoding='utf-8')


def test_scrub_browser_version_keeps_length():
    version = '.'.join(['153', '0', '0', '0']).encode()
    pdf = b'/Creator (Mozilla/5.0 HeadlessChrome/' + version + b' Safari/537.36)'
    out = build_manual.scrub_browser_version(pdf)
    assert len(out) == len(pdf)
    assert b'HeadlessChrome/153_0_0_0 ' in out
    assert b'Safari/537.36' in out


def test_outline_nests_part_chapter_section():
    html = (
        '<h1 id="2-wire">2 Wire protocol</h1>'
        '<h2 id="20-reading">2.0 Reading this Part</h2>'
        '<h2 id="chapters">Chapters</h2>'
        '<h1 id="21-framing">2.1 Framing <em>and</em> encodings</h1>'
        '<h2 id="211-ints">2.1.1 Integer encodings</h2>'
        '<h1 id="10-torque">10 Torque-era 3D</h1>'
        '<h2 id="101-lineage">10.1 Engine lineage</h2>'
        '<h1 id="app-a">Appendix A. Message index</h1>'
        '<h2 id="a1">A.1 Client to server</h2>'
        '<h3 id="deep">2.1.1.1 Too deep</h3>'
    )
    assert build_manual.outline_entries(html) == [
        (0, '2-wire', '2 Wire protocol'),
        (1, '20-reading', '2.0 Reading this Part'),
        (1, '21-framing', '2.1 Framing and encodings'),
        (2, '211-ints', '2.1.1 Integer encodings'),
        (0, '10-torque', '10 Torque-era 3D'),
        (1, '101-lineage', '10.1 Engine lineage'),
        (0, 'app-a', 'Appendix A. Message index'),
        (1, 'a1', 'A.1 Client to server'),
    ]


def test_sources_become_footnotes_and_bibliography():
    bib = build_manual.Bibliography()
    md = (
        'Text [bin] (a/x.md#y); [2.05] (b/y.md) and more [inf] (a/x.md).\n'
        '\n'
        '| Id | Rule | Source |\n'
        '| --- | --- | --- |\n'
        '| 1 | a `[bin]` rule [inf] | [bin] (a/x.md); [cap] (c/z.md#q) |\n'
        '| 2 | open | disputed → App. E#1 |\n'
    )
    out = build_manual.move_sources(md, bib)
    lines = out.split('\n')
    fn = '<sup class="fn"><a href="#src-{}">{}</a>'
    assert lines[0].startswith('Text' + fn.format(1, 1) + ',<a href="#src-2">2</a></sup> and more')
    assert lines[2] == '| Id | Rule |'
    assert lines[4].startswith('| 1 | a `[bin]` rule' + fn.format(1, 1))
    assert 'src-3' in lines[4]
    assert lines[5].startswith('| 2 | open (disputed → App. E#1) |')
    assert list(bib.number) == ['a/x.md', 'b/y.md', 'c/z.md']
    assert '<p id="src-3">3. <a href="https://github.com/squirelworks/Graal_analysis/blob/main/c/z.md">' in bib.chapter()


def test_a_source_column_of_names_is_kept():
    bib = build_manual.Bibliography()
    md = ('| Source | Hearts | Source |\n| --- | --- | --- |\n'
          '| lava | 1 | [2.05] (a/x.md) |\n| arrow | 0.5 | [2.05] (a/x.md) |\n')
    out = build_manual.move_sources(md, bib).split('\n')
    assert out[0] == '| Source | Hearts |'
    assert out[2].startswith('| lava | 1<sup class="fn">')


def test_wide_tables_get_named_landscape_pages():
    import build_manual as bm
    assert '@page wide{size:A4 landscape' in build_manual.CSS
    assert '@page wider{size:A3 landscape' in build_manual.CSS
    assert '.page-wide{page:wide}' in build_manual.CSS
    # pandoc's template clips a too-wide table (display:block; overflow-x:auto)
    assert 'table{display:table;overflow:visible' in build_manual.CSS
    assert [name for name, _ in bm.PAGE_WIDTHS] == ['', 'page-wide', 'page-wider']


def test_a3_pages_become_inserts():
    assert build_manual.A3_MIN_WIDTH > 842  # wider than A4 landscape
    assert '.page-wider img' in build_manual.CSS
    html = build_manual.PLACEHOLDER.format(pages='<div class="p">x</div>')
    assert '@page{size:A4;margin:0}' in html and '<div class="p">x</div>' in html
    assert callable(build_manual.write_print_set)
