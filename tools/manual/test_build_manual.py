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
