"""Unpack an InstallShield 3 data archive (`_SETUP.1`, `DATA.Z`) without running the installer.

    python -I is3x.py list    <archive>          -> one line per file: group, name, size, stored date
    python -I is3x.py extract <archive> <outdir> -> writes <outdir>/<group>/<name>, prints the same lines + "OK"/"SIZE-MISMATCH"

The archive starts with the magic 13 5D 65 8C. Its header gives the file count (u16 at 12), the directory table
offset (u32 at 41) and the group count (u16 at 49). The table holds the groups (u16 file count, u16 entry size,
u16 name length, name) and then the files (u16 at +1 unused here, u32 size at +3, u32 packed size at +7, u32 data
offset at +11, DOS date at +15, DOS time at +17, u32 attributes at +19, u16 entry size at +23, name length at +29,
name at +30). Every file is one PKWARE Data Compression Library ("implode") stream.

The decoder below is a Python port of the `blast` algorithm (Mark Adler's zlib contrib/blast, zlib licence).
Standard library only. It reads the archive and writes files; it never executes anything.
"""
from __future__ import annotations

import os
import struct
import sys

MAXBITS = 13


class Huffman:
    def __init__(self, rep: list[int]):
        lengths: list[int] = []
        for b in rep:  # run-length coded: high nibble = repeat-1, low nibble = code length
            lengths += [b & 15] * ((b >> 4) + 1)
        self.count = [0] * (MAXBITS + 1)
        for n in lengths:
            self.count[n] += 1
        offs = [0] * (MAXBITS + 2)
        for n in range(1, MAXBITS + 1):
            offs[n + 1] = offs[n] + self.count[n]
        self.symbol = [0] * len(lengths)
        for sym, n in enumerate(lengths):
            if n:
                self.symbol[offs[n]] = sym
                offs[n] += 1


LIT = Huffman([11, 124, 8, 7, 28, 7, 188, 13, 76, 4, 10, 8, 12, 10, 12, 10, 8, 23, 8, 9, 7, 6, 7, 8, 7, 6, 55, 8, 23,
               24, 12, 11, 7, 9, 11, 12, 6, 7, 22, 5, 7, 24, 6, 11, 9, 6, 7, 22, 7, 11, 38, 7, 9, 8, 25, 11, 8, 11, 9,
               12, 8, 12, 5, 38, 5, 38, 5, 11, 7, 5, 6, 21, 6, 10, 53, 8, 7, 24, 10, 27, 44, 253, 253, 253, 252, 252,
               252, 13, 12, 45, 12, 45, 12, 61, 12, 45, 44, 173])
LEN = Huffman([2, 35, 36, 53, 38, 23])
DIST = Huffman([2, 20, 53, 230, 247, 151, 248])
LEN_BASE = [3, 2, 4, 5, 6, 7, 8, 9, 10, 12, 16, 24, 40, 72, 136, 264]
LEN_EXTRA = [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8]


def blast(src: bytes) -> bytes:
    pos = bitbuf = bitcnt = 0
    out = bytearray()

    def bits(n: int) -> int:
        nonlocal pos, bitbuf, bitcnt
        while bitcnt < n:
            bitbuf |= src[pos] << bitcnt
            pos += 1
            bitcnt += 8
        v = bitbuf & ((1 << n) - 1)
        bitbuf >>= n
        bitcnt -= n
        return v

    def decode(h: Huffman) -> int:
        code = first = index = 0
        for n in range(1, MAXBITS + 1):
            code |= bits(1) ^ 1  # codes are stored bit-inverted
            c = h.count[n]
            if code < first + c:
                return h.symbol[index + code - first]
            index += c
            first = (first + c) << 1
            code <<= 1
        raise ValueError('bad Huffman code')

    coded_literals, dict_bits = bits(8), bits(8)
    if coded_literals > 1 or not 4 <= dict_bits <= 6:
        raise ValueError('not a PKWARE DCL stream')
    while True:
        if bits(1):
            sym = decode(LEN)
            length = LEN_BASE[sym] + bits(LEN_EXTRA[sym])
            if length == 519:  # end of stream
                return bytes(out)
            low = 2 if length == 2 else dict_bits
            dist = (decode(DIST) << low) + bits(low) + 1
            if dist > len(out):
                raise ValueError('distance too far back')
            for _ in range(length):
                out.append(out[-dist])
        else:
            out.append(decode(LIT) if coded_literals else bits(8))


def entries(d: bytes):
    if d[:4] != b'\x13\x5d\x65\x8c':
        raise ValueError('not an InstallShield 3 archive')
    files_total, = struct.unpack_from('<H', d, 12)
    table, = struct.unpack_from('<I', d, 41)
    groups_total, = struct.unpack_from('<H', d, 49)
    p = table
    groups = []
    for _ in range(groups_total):
        n, size, name_len = struct.unpack_from('<HHH', d, p)
        groups.append((d[p + 6:p + 6 + name_len].decode('latin-1'), n))
        p += size
    out = []
    for group, n in groups:
        for _ in range(n):
            size, packed, offset, date, time, _attr, entry_size = struct.unpack_from('<IIIHHIH', d, p + 3)
            name = d[p + 30:p + 30 + d[p + 29]].decode('latin-1')
            stamp = (f'{(date >> 9) + 1980:04}-{(date >> 5) & 15:02}-{date & 31:02} '
                     f'{time >> 11:02}:{(time >> 5) & 63:02}:{(time & 31) * 2:02}')
            out.append((group, name, size, packed, offset, stamp))
            p += entry_size
    if len(out) != files_total:
        raise ValueError(f'directory lists {len(out)} files, header says {files_total}')
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[0] not in ('list', 'extract') or (argv[0] == 'extract' and len(argv) < 3):
        print(__doc__, file=sys.stderr)
        return 2
    d = open(argv[1], 'rb').read()
    bad = 0
    for group, name, size, packed, offset, stamp in entries(d):
        line = f'{group}\t{name}\t{size}\t{stamp}'
        if argv[0] == 'extract':
            data = blast(d[offset:offset + packed])
            ok = len(data) == size
            bad += not ok
            safe = os.path.basename(name.replace('\\', '/'))
            folder = os.path.join(argv[2], os.path.basename(group))
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, safe), 'wb') as f:
                f.write(data)
            line += '\tOK' if ok else '\tSIZE-MISMATCH'
        print(line)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
