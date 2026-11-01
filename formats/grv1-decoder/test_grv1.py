"""Synthetic boards. The 11-bit and HEIGHTS cases have no sample file in the notes."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import grv1  # noqa: E402


def pack(codes, width):
    buf = nbits = 0
    out = bytearray()
    mask = (1 << width) - 1
    for code in codes:
        buf |= (code & mask) << nbits
        nbits += width
        while nbits >= 8:
            out.append(buf & 0xff)
            buf >>= 8
            nbits -= 8
    if nbits:
        out.append(buf & 0xff)
    return bytes(out)


def literals(tile, width):
    return pack([tile] * 4096, width)


def test_twelve_and_thirteen_bit_widths_are_unchanged():
    assert grv1.code_width(b'GR-V1.00') == 12
    assert grv1.code_width(b'GR-V1.03') == 13
    assert grv1.code_width(b'Z3-V1.03') == 12
    assert grv1.code_width(b'Z3-V1.04') == 12
    zelda = b'Z3-V1.04' + literals(2000, 12) + b'#\n\xff\xff\xff\n'
    loaded = grv1.load(zelda)
    assert loaded['board'] == [2000] * 4096
    assert 'heights' not in loaded
    graal = b'GR-V1.03' + literals(3000, 13) + b'#\n\xff\xff\xff\n#\n#\n'
    loaded = grv1.load(graal)
    assert loaded['board'] == [3000] * 4096
    assert loaded['chests'] == []


def test_ci_smoke_shape_still_reads():
    width, flag = 12, 1 << 11
    codes = []
    remaining = 4096
    while remaining:
        count = min(255, remaining)
        codes.append(flag | count)
        codes.append(0)
        remaining -= count
    loaded = grv1.load(b'GR-V1.00' + pack(codes, width) + b'#\n\x80#\n')
    assert loaded['magic'] == 'GR-V1.00'
    assert loaded['board'] == [0] * 4096


def test_z3_v102_is_eleven_bits():
    assert grv1.code_width(b'Z3-V1.02') == 11
    body = b'Z3-V1.02' + literals(1000, 11) + b'#\n' + bytes([4, 5, 1]) + b'\n\xff\xff\xff\n'
    loaded = grv1.load(body)
    assert loaded['board'] == [1000] * 4096
    assert loaded['baddies'] == [{'x': 4, 'y': 5, 'type': 1, 'verses': ['']}]
    assert loaded['npcs'] == [] and loaded['chests'] == []
    assert 'heights' not in loaded


def test_gr_v104_keeps_chests_and_heights():
    rows = ['1.5,2,3'] + [','.join(['0'] * 9)] * 8
    body = (
        b'GR-V1.04' + literals(3000, 13)
        + b'#\n\xff\xff\xff\n#\n'
        + bytes([32 + 1, 32 + 2, 32 + 3, 32 + 4]) + b'\n'
        + b'#\n\nHEIGHTS\n'
        + ('\n'.join(rows) + '\n').encode('ascii')
        + b'HEIGHTSEND\n'
    )
    loaded = grv1.load(body)
    assert loaded['board'][0] == 3000
    assert loaded['chests'] == [{'x': 1, 'y': 2, 'item': 3, 'sign': 4}]
    assert loaded['heights'][0] == [1.5, 2.0, 3.0]
    assert len(loaded['heights']) == 9
    assert all(len(row) == 9 for row in loaded['heights'][1:])


def test_heightsend_is_case_insensitive_and_caps_the_grid():
    wide = ','.join(str(i) for i in range(12))
    lines = [wide] * 10
    body = b'GR-V1.03' + literals(1, 13) + b'#\n\xff\xff\xff\n#\n#\n\nHEIGHTS\n'
    body += ('\n'.join(lines) + '\n').encode('ascii') + b'heightsend\n'
    loaded = grv1.load(body)
    assert len(loaded['heights']) == 9
    assert loaded['heights'][0] == [float(i) for i in range(9)]
