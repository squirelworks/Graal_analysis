"""Tests for tools/manual/coverage.py. Standard library + pytest."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import coverage  # noqa: E402

HEADER = 'path\tstatus\tsections\tplanned\treason\n'
NOTE = ''.join(f'`term{i:02d}` ' for i in range(10))


def make_repo(tmp_path: Path, manual: str, row: str, explained: str | None = None) -> Path:
    (tmp_path / 'manual').mkdir()
    (tmp_path / 'manual' / '01-x.md').write_text(manual, encoding='utf-8')
    (tmp_path / 'notes').mkdir()
    (tmp_path / 'notes' / 'a.md').write_text(NOTE, encoding='utf-8')
    (tmp_path / 'manual' / 'sources.tsv').write_text(HEADER + row + '\n', encoding='utf-8')
    if explained is not None:
        (tmp_path / 'manual' / 'coverage-explained.tsv').write_text(
            'path\tterm\treason\n' + explained, encoding='utf-8')
    return tmp_path


def test_lists_every_miss_and_part(tmp_path):
    root = make_repo(tmp_path, 'term00 term01', 'notes/a.md\tcited\t4.2; E\t\t')
    [rec] = coverage.run(root)
    assert rec['part'] == 'IV'
    assert rec['terms'] == 10
    assert len(rec['missing']) == 8
    assert rec['unexplained'] == rec['missing']


def test_explained_terms_and_wildcard(tmp_path):
    root = make_repo(tmp_path, '', 'notes/a.md\tcited\t2\t\t',
                     'notes/a.md\tterm00\tbookkeeping\n')
    [rec] = coverage.run(root)
    assert 'term00' in rec['missing'] and 'term00' not in rec['unexplained']
    (root / 'manual' / 'coverage-explained.tsv').write_text(
        'path\tterm\treason\nnotes/a.md\t*\tout of scope\n', encoding='utf-8')
    assert coverage.run(root)[0]['unexplained'] == []


def test_strict_exit(tmp_path, capsys):
    root = make_repo(tmp_path, '', 'notes/a.md\tcited\tE\t\t')
    assert coverage.main(['--root', str(root)]) == 0
    assert coverage.main(['--root', str(root), '--strict']) == 1
    full = ' '.join(f'term{i:02d}' for i in range(10))
    (root / 'manual' / '01-x.md').write_text(full, encoding='utf-8')
    assert coverage.main(['--root', str(root), '--strict']) == 0


def test_excluded_rows_are_not_measured(tmp_path):
    root = make_repo(tmp_path, '', 'notes/a.md\texcluded\t\t\tnot Graal')
    assert coverage.run(root) == []


def test_runs_on_repo():
    assert coverage.run(REPO)
