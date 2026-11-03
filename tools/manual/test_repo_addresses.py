"""Runs the repo-wide address leak check (tools/leak-check/) inside the 3-OS
`manual` CI job, which already runs `pytest tools/manual` on Linux, macOS and Windows."""
import importlib.util
from pathlib import Path

CHECKER = Path(__file__).resolve().parents[1] / 'leak-check' / 'check_addresses.py'
spec = importlib.util.spec_from_file_location('check_addresses', CHECKER)
ca = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ca)


def test_repo_has_no_code_addresses():
    problems = ca.scan(ca.repo_root())
    assert problems == [], '\n'.join(problems)


def test_checker_catches_an_address():
    assert ca.line_errors('handler at ' + '0x' + '4dab' + 'c8')
    assert not ca.line_errors('seed 0x04A80B38, multiplier 0x08088405')
