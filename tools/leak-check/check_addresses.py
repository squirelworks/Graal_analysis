"""Repo-wide leak check for binary code addresses and disassembler names.

Run from anywhere inside the repo:  python tools/leak-check/check_addresses.py
It scans every tracked text file (PDFs and binary files are skipped) and fails on:

* a 0x hex literal with 5 to 8 digits that is not on the allowlist below,
* a bare 8-digit hex word starting with 00 (``00xxxxxx``) that is not on the allowlist,
* a Ghidra/IDA style name such as FUN_/DAT_/LAB_/PTR_DAT_ followed by hex.

Allowlisted values are constants, sizes, masks and magic numbers, compared by
numeric value, so 0x4A80B38 and 0x04A80B38 are the same entry. Add a value here
only when it is plainly not a code or data address, and say what it is.
Pure Python, so it runs the same on Linux, macOS and Windows. CI runs it through
tools/manual/test_repo_addresses.py in the 3-OS `manual` job.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ALLOWED_HEX = {
    0x04A80B38: 'gen-3/5 cipher LCG seed',
    0x08088405: 'Borland Random LCG multiplier',
    0x400000: 'default PE image base; also a mask bit in torque/wire-by-build.md',
    0xFFFFFFFF: 'all-ones 32-bit mask / static class CRC',
    0xFFFFFFFE: 'all-ones minus one mask',
    0xFFFFFFF: '28-bit mask (DES key halves)',
    0x7FFFFFFF: '31-bit mask',
    0x7FFF0000: 'top of user address space used as a scan limit',
    0x1000000: 'end of the exe-image scan range',
    0xFFFFFF: 'white (RGB)',
    0xFF0000: 'colour value (RGB)',
    0x800000: 'colour value / out-queue cap / mask bit',
    0xFDCC47: 'colour value (RGB)',
    0x37FFFF: 'id 50 raw-data length cap',
    0x3FFFF: 'compressed-output overload limit',
    0x40000: 'out-queue drop limit',
    0x10000: 'action flag bit',
    0x3FC000: 'update mask bits',
    0xFFFF0C: 'DirectInput dwType flags',
    0xEDB88320: 'CRC-32 polynomial',
    0x82D0B188: 'Thinstall package magic',
    0x15A8EA07: 'CRC-32 of a cached file',
    0x51000: 'Thinstall block size (uncompressed)',
    0x18A5B: 'Thinstall block size (compressed)',
    0x1A6400: 'GraalEditor payload size',
    0x20A00: 'hvdi.dll payload size',
    0x1B1000: 'PE SizeOfImage',
}
ALLOWED_BARE = {
    '00000001': 'packet value in a capture',
    '00000004': 'packet value in a capture',
    '00000005': 'packet value in a capture',
    '00040000': 'Torque packet bytes (sequence 0x400)',
    '00010203': 'Torque packet bytes (digest)',
}

HEX_RE = re.compile(r'(?<![0-9A-Za-z_])0[xX]([0-9a-fA-F]{5,8})(?![0-9A-Za-z_])')
BARE_RE = re.compile(r'(?<![0-9A-Za-z_])(00[0-9a-fA-F]{6})(?![0-9A-Za-z_])')
NAME_RE = re.compile(r'\b(?:(?:FUN|DAT|LAB|PTR_DAT|PTR_FUN|thunk_FUN)_[0-9a-fA-F]{4,}|sub_[0-9a-fA-F]{6,8})\b')

SKIP_SUFFIXES = {'.pdf', '.png', '.gif', '.jpg', '.jpeg', '.bmp', '.ico', '.zip', '.gz',
                 '.tar', '.exe', '.dll', '.bin', '.pcap', '.pcapng', '.mng', '.wav', '.mp3'}


def line_errors(line: str) -> list[str]:
    errs = []
    for m in HEX_RE.finditer(line):
        if int(m.group(1), 16) not in ALLOWED_HEX:
            errs.append(f'code address {m.group(0)}')
    for m in BARE_RE.finditer(line):
        if m.group(1).lower() not in ALLOWED_BARE:
            errs.append(f'bare code address {m.group(1)}')
    for m in NAME_RE.finditer(line):
        errs.append(f'disassembler name {m.group(0)}')
    return errs


def tracked_files(root: Path) -> list[Path]:
    try:
        out = subprocess.run(['git', 'ls-files', '-z'], cwd=root, capture_output=True, check=True).stdout
        names = [n for n in out.decode('utf-8', 'surrogateescape').split('\0') if n]
    except (OSError, subprocess.CalledProcessError):
        names = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d != '.git']
            names += [os.path.relpath(os.path.join(dirpath, f), root) for f in filenames]
    return [root / n for n in names]


def scan(root: Path) -> list[str]:
    problems = []
    for path in tracked_files(root):
        if path.suffix.lower() in SKIP_SUFFIXES or not path.is_file():
            continue
        data = path.read_bytes()
        if b'\0' in data[:8192]:
            continue
        text = data.decode('utf-8', 'replace')
        rel = path.relative_to(root).as_posix()
        for no, line in enumerate(text.splitlines(), 1):
            for err in line_errors(line):
                problems.append(f'{rel}:{no}: {err}')
    return problems


def repo_root() -> Path:
    here = Path(__file__).resolve().parent
    try:
        out = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=here,
                             capture_output=True, check=True, text=True).stdout.strip()
        return Path(out)
    except (OSError, subprocess.CalledProcessError):
        return here.parent.parent


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else repo_root()
    problems = scan(root)
    for p in problems:
        print(p)
    if problems:
        print(f'binary address / disassembler name leak: {len(problems)} hit(s)', file=sys.stderr)
        return 1
    print('address leak check: clean')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
