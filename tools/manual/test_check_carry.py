"""Tests for tools/manual/check_carry.py. Standard library + pytest."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import check_carry  # noqa: E402

HEADER = 'path\tstatus\tsections\tplanned\treason\n'
NOTE = ''.join(f'`term{i:02d}` ' for i in range(10))


def make_repo(tmp_path: Path, manual: str, row: str, note: str = NOTE) -> Path:
    (tmp_path / 'manual').mkdir()
    (tmp_path / 'manual' / '01-x.md').write_text(manual, encoding='utf-8')
    (tmp_path / 'notes').mkdir()
    (tmp_path / 'notes' / 'a.md').write_text(note, encoding='utf-8')
    (tmp_path / 'manual' / 'sources.tsv').write_text(HEADER + row + '\n', encoding='utf-8')
    return tmp_path


def test_carried_note_passes(tmp_path):
    root = make_repo(tmp_path, ' '.join(f'term{i:02d}' for i in range(10)),
                     'notes/a.md\tcited\t1\t1\t')
    assert check_carry.run(root)[0] == []


def test_low_term_carry_fails_without_reason(tmp_path):
    root = make_repo(tmp_path, 'term00 term01', 'notes/a.md\tcited\t1\t1\t')
    errs = check_carry.run(root)[0]
    assert len(errs) == 1 and '20% of 10' in errs[0]


def test_reason_excuses_low_carry(tmp_path):
    root = make_repo(tmp_path, 'term00', 'notes/a.md\tcited\t1\t1\tcode names only')
    assert check_carry.run(root)[0] == []


def test_few_terms_are_not_judged(tmp_path):
    root = make_repo(tmp_path, '', 'notes/a.md\tcited\t1\t1\t', note='`alpha` `beta`')
    assert check_carry.run(root)[0] == []


def test_unmet_planned_section_fails(tmp_path):
    root = make_repo(tmp_path, ' '.join(f'term{i:02d}' for i in range(10)),
                     'notes/a.md\tcited\t2.3\t4; 2\t')
    errs = check_carry.run(root)[0]
    assert len(errs) == 1 and 'planned for 4' in errs[0]


def test_planned_section_granularity():
    assert check_carry.planned_met('5.2', ['5'])
    assert check_carry.planned_met('4', ['4.11'])
    assert not check_carry.planned_met('4', ['3.1'])
    assert not check_carry.planned_met('2.6', ['2.1'])


def test_file_names_are_not_terms():
    terms = check_carry.note_terms('`exports.txt` `a/b` `functions.*` `PLO_FOO` `0x1F` `rate`')
    assert terms == {'PLO_FOO', '0x1f', 'rate'}


def test_repository_passes():
    errs, _ = check_carry.run(REPO)
    assert errs == [], '\n'.join(errs)
