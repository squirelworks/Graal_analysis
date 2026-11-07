import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('check_addresses', HERE / 'check_addresses.py')
ca = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ca)

# Samples are split so this file never holds a contiguous address.
BAD = [
    '0x' + '4dab' + 'c8',
    '0x' + '0040' + '1a2b',
    '0x' + '1000' + 'a220',
    '00' + '4849' + 'fc',
    'FUN_' + '0040' + '1000',
    'DAT_' + '0053' + 'a610',
]
GOOD = [
    '0x04A80B38', '0x4A80B38', '0x08088405', '0x8088405', '0x400000',
    '0xFFFFFFFF', '0x37FFFF', '0x1000', '0x7F', '`FUN_` names', 'b\'-00000005\'',
    'GNW24011', 'c93e659e2cda36379aaea4706db20b38',
]


def test_bad_samples_fail():
    for s in BAD:
        assert ca.line_errors(f'see {s} here'), s


def test_good_samples_pass():
    for s in GOOD:
        assert not ca.line_errors(f'see {s} here'), s


def test_scan_flags_file(tmp_path):
    (tmp_path / 'note.md').write_text('handler at ' + '0x' + '4db' + '984\n', encoding='utf-8')
    (tmp_path / 'doc.pdf').write_text('0x' + '4db' + '984\n', encoding='utf-8')
    problems = ca.scan(tmp_path)
    assert len(problems) == 1 and problems[0].startswith('note.md:1:')


def test_repo_is_clean():
    assert ca.scan(ca.repo_root()) == []
