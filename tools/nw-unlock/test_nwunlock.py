"""Self-test for nwunlock.py on a synthetic PE (no client binary needed).

Run: python3 test_nwunlock.py
Builds a tiny PE whose code section holds the three byte patterns the tool looks for, patches it,
and checks the new section, the two redirects and that a second patch is refused.
"""
import os
import struct
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nwunlock as n  # noqa: E402

BASE = 0x400000
CODE_RVA, DATA_RVA = 0x1000, 0x2000


def build_pe() -> bytes:
    data = bytearray(0x200)
    slots = DATA_RVA + 0x10
    struct.pack_into('<6i', data, 0x10, 5, 6, 4, 3, 1, 0)
    coltab = slots + 0x18
    data[0x28:0x28 + 60] = bytes(range(60))
    shield_str = DATA_RVA + 0x80
    data[0x80:0x87] = b'SHIELD\x00'
    form_ptr, colbuf = BASE + DATA_RVA + 0x100, BASE + DATA_RVA + 0x140

    code = bytearray(b'\xc3' * 0x40)  # getter stub at the start (ret)
    getter = BASE + CODE_RVA

    def rel(at, dst):
        return struct.pack('<i', dst - (BASE + CODE_RVA + at + 4))

    g = len(code)  # COLORS gate
    code += b'\xa1' + struct.pack('<I', form_ptr) + b'\x8b\x00\xe8' + rel(g + 8, getter)
    code += bytes.fromhex('84 c0 74 07 b8 08 00 00 00 eb 05 b8 05 00 00 00')
    code += bytes.fromhex('c7 45 f4 05 00 00 00') + b'\xb8' + struct.pack('<I', colbuf)
    code += b'\xba' + struct.pack('<I', BASE + slots)
    code += bytes.fromhex('8b 0a 8d 0c 49 8b 18 8d 1c 5b 8d bc 0e 3d 03 00 00 66 8b 8b')
    code += struct.pack('<I', BASE + coltab) + bytes.fromhex('66 89 0f 8a 8b')
    code += struct.pack('<I', BASE + coltab + 2)
    code += bytes.fromhex('88 4f 02 83 c2 04 83 c0 04 ff 4d f4 75 d1 8b c6 c3')
    code += b'\xba' + struct.pack('<I', BASE + shield_str) + b'\xe8' + rel(len(code) + 6, getter)
    code += b'\x0f\x85' + struct.pack('<i', 0x20)
    code += bytes.fromhex('8b c3 e8 00 00 00 00 85 c0 0f 84 00 00 00 00 8b c3 e8 00 00 00 00 83 78 24 26')
    code += b'\xc3' * (0x200 - len(code))

    hdr = bytearray(0x400)
    hdr[:2] = b'MZ'
    struct.pack_into('<I', hdr, 0x3C, 0x80)
    hdr[0x80:0x84] = b'PE\x00\x00'
    struct.pack_into('<HHIIIHH', hdr, 0x84, 0x14C, 2, 0, 0, 0, 0xE0, 0x10F)
    opt = 0x98
    struct.pack_into('<H', hdr, opt, 0x10B)
    struct.pack_into('<III', hdr, opt + 28, BASE, 0x1000, 0x200)
    struct.pack_into('<II', hdr, opt + 56, 0x3000, 0x400)
    st = opt + 0xE0
    struct.pack_into('<8sIIIIIIHHI', hdr, st, b'CODE', len(code), CODE_RVA, 0x200, 0x400, 0, 0, 0, 0, n.SCN_TEXT)
    struct.pack_into('<8sIIIIIIHHI', hdr, st + 40, b'DATA', len(data), DATA_RVA, 0x200, 0x600, 0, 0, 0, 0, (1 << 6) | n.SCN_READ | (1 << 31))
    return bytes(hdr + code + data)


def main():
    raw = build_pe()
    pe = n.PE(raw)
    a = n.find_anchors(pe)
    assert a['colour_gates'] == 1 and a['paloff'] == 0x33d, a
    with tempfile.TemporaryDirectory() as d:
        src, out = os.path.join(d, 'in.exe'), os.path.join(d, 'out.exe')
        open(src, 'wb').write(raw)
        n.main(['patch', src, out])
        p = n.PE(open(out, 'rb').read())
        assert p.nsec == 3 and p.sections[-1][0] == n.NEW_SECTION
        new_va = BASE + p.sections[-1][1]
        for site in (a['rc_site'], a['sh_site']):
            o = p.va_to_off(site)
            assert p.data[o] == 0xE9, hex(site)
            dst = site + 5 + struct.unpack_from('<i', p.data, o + 1)[0]
            assert new_va <= dst < new_va + p.sections[-1][2]
        try:
            n.main(['patch', out, os.path.join(d, 'again.exe')])
        except SystemExit as e:
            assert e.code, 'second patch must fail'
        else:
            raise AssertionError('second patch must fail')
    print('ok')


if __name__ == '__main__':
    main()
