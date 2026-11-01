#!/usr/bin/env python3
"""Decoder for the Graal client's web-level cache (weblevels/<host>/<level>-<port>.code, "GWEBL001").

usage: gwebl.py FILE.code [--level NAME] [--raw OUT.bin] [--json]
The level name (used to seed the key stream) defaults to the part of the file
name before the last "-<port>.code".
"""
import os, re, struct, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from graaldes import GraalDES

SEED_BASE = 0x04A80B38

class DelphiRandom:
    def __init__(self, seed): self.seed = seed & 0xFFFFFFFF
    def random(self, n):
        self.seed = (self.seed * 0x08088405 + 1) & 0xFFFFFFFF
        return (self.seed * n) >> 32

def seed_for(level):
    s = SEED_BASE
    for b in level.lower().encode('latin1'):
        s = (s * b) & 0xFFFFFFFF
    return s

def decrypt_file(data, level):
    (n,) = struct.unpack_from('<i', data, 0)
    if n + 4 > len(data) or n < 8 or (n % 8):
        raise ValueError('bad length header')
    rnd = DelphiRandom(seed_for(level))
    out = bytearray(); csum = bytearray(8); pos = 4
    while len(out) < n - 8:
        key = bytes(rnd.random(256) for _ in range(8))
        blk = GraalDES(key).decrypt(data[pos:pos+8]); pos += 8
        out += blk
        for i in range(8): csum[i] = (csum[i] + blk[i]) & 0xFF
    if bytes(csum) != data[pos:pos+8]:
        raise ValueError('checksum mismatch (wrong level name?)')
    return bytes(out)

def encrypt_stream(plain, level):
    plain = bytearray(plain)
    while len(plain) % 8: plain.append(10)
    rnd = DelphiRandom(seed_for(level))
    out = bytearray(struct.pack('<i', len(plain) + 8)); csum = bytearray(8)
    for p in range(0, len(plain), 8):
        blk = bytes(plain[p:p+8])
        for i in range(8): csum[i] = (csum[i] + blk[i]) & 0xFF
        key = bytes(rnd.random(256) for _ in range(8))
        out += GraalDES(key).encrypt(blk)
    return bytes(out + csum)

# ---- GR-V level body -------------------------------------------------------

def read_board(buf, pos, bits):
    """Decode the 64x64 tile board. Returns (tiles[4096], new_pos)."""
    tiles = []; acc = 0; nacc = 0
    count = 1; double = False; first = -1
    top = 1 << (bits - 1); mask = (1 << bits) - 1
    while len(tiles) < 4096:
        while nacc < bits:
            acc |= buf[pos] << nacc; pos += 1; nacc += 8
        code = acc & mask; acc >>= bits; nacc -= bits
        if code & top:
            double = bool(code & 0x100); count = code & 0xFF
            continue
        if count == 1:
            tiles.append(code)
        elif not double:
            tiles.extend([code] * count); count = 1
        elif first < 0:
            first = code
        else:
            tiles.extend([first, code] * count); first = -1; double = False; count = 1
    return tiles[:4096], pos

def write_board(tiles):
    """Encode like the client does (13-bit codes, GR-V1.02 and later)."""
    codes = []; i = 0
    while i < 4096:
        t = tiles[i]
        if i < 4093 and tiles[i+1] == t:
            n = 2; i += 2
            while n < 64 and i < 4096 and tiles[i] == t: n += 1; i += 1
            codes += [0x1000 | n, t & 0xFFF]
        elif i < 4093 and tiles[i+2] == t and tiles[i+1] == tiles[i+3]:
            t2 = tiles[i+1]; n = 2; i += 4
            while n < 64 and i < 4095 and tiles[i] == t and tiles[i+1] == t2: n += 1; i += 2
            codes += [0x1100 | n, t & 0xFFF, t2 & 0xFFF]
        else:
            codes.append(t & 0xFFF); i += 1
    out = bytearray(); acc = 0; nacc = 0
    for c in codes:
        acc |= (c & 0x1FFF) << nacc; nacc += 13
        while nacc >= 8: out.append(acc & 0xFF); acc >>= 8; nacc -= 8
    if nacc: out.append(acc & 0xFF)
    return bytes(out)

SIGN_CHARS = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!?-.,#>()#####\"####':/~&### <####;\n")

# Codes that decode to "#<letter>" (button/key symbols); the value is how many input bytes the symbol uses.
SIGN_SYMBOLS = {91: ('A', 1), 92: ('B', 1), 93: ('X', 1), 94: ('Y', 1), 77: ('u', 1), 78: ('d', 1),
                79: ('l', 1), 80: ('r', 1), 74: ('h', 2), 71: ('x', 1), 72: ('y', 1), 73: ('z', 1),
                87: ('4', 2), 67: ('.', 1)}

def sign_text(enc):
    """Decode sign text the way the client's level reader does."""
    s = ''; i = 0
    while i < len(enc):
        k = enc[i] - 32
        c = SIGN_CHARS[k] if 0 <= k < len(SIGN_CHARS) else '?'
        if c == '#':
            if k in SIGN_SYMBOLS:
                letter, n = SIGN_SYMBOLS[k]
                s += '#' + letter; i += n - 1
            else:
                s += '#'
        else:
            s += c
        i += 1
    return s

def parse_grv(buf, pos=0, keep_sections=True):
    ver = buf[pos:pos+8].decode('latin1'); pos += 8
    if ver == 'Z3-V1.02':
        bits = 11
    elif ver in ('GR-V1.02', 'GR-V1.03', 'GR-V1.04'):
        bits = 13
    else:
        bits = 12
    tiles, pos = read_board(buf, pos, bits)
    lines_at = pos
    def line():
        nonlocal pos
        e = buf.find(b'\n', pos)
        if e < 0: e = len(buf)
        l = buf[pos:e]; pos = e + 1
        return l
    lv = {'version': ver, 'tiles': tiles, 'links': [], 'baddies': [], 'npcs': [], 'chests': [], 'signs': []}
    while pos < len(buf):
        l = line()
        if l in (b'#', b''): break
        lv['links'].append(l.decode('latin1'))
    # baddies: binary records x,y,type then verses, terminated by a record starting 0xFF
    while pos < len(buf):
        e = pos
        while True:
            e = buf.find(b'\n', e)
            if e < 0: e = len(buf); break
            if e - pos > 2: break
            e += 1
        rec = buf[pos:e]; pos = e + 1
        if len(rec) < 3 or rec[0] >= 0x80: break
        lv['baddies'].append({'x': rec[0], 'y': rec[1], 'type': rec[2], 'verses': rec[3:].decode('latin1').split('\\')})
    if ver != 'Z3-V1.03' and ver != 'Z3-V1.04':
        while pos < len(buf):
            l = line()
            if l in (b'#', b''): break
            lv['npcs'].append({'x': l[0]-32, 'y': l[1]-32, 'image_and_script': l[2:].decode('latin1')})
    if ver in ('GR-V1.01', 'GR-V1.02', 'GR-V1.03', 'GR-V1.04'):
        while pos < len(buf):
            l = line()
            if l in (b'#', b''): break
            lv['chests'].append({'x': l[0]-32, 'y': l[1]-32, 'item': l[2]-32, 'signindex': l[3]-32})
    # Signs run to EOF in 2.05. 2.31 stops at an empty line and may follow with a HEIGHTS block.
    while pos < len(buf):
        l = line()
        if l == b'HEIGHTS':
            rows = []
            while pos < len(buf):
                l = line()
                if l.upper() == b'HEIGHTSEND': break
                if len(rows) < 9:
                    rows.append([float(v) for v in l.decode('latin1').split(',')[:9] if v.strip()])
            lv['heights'] = rows
            continue
        if len(l) < 2: continue
        lv['signs'].append({'x': l[0]-32, 'y': l[1]-32, 'text': sign_text(l[2:])})
    return lv

def parse_cache(plain):
    if plain[:8] != b'GWEBL001':
        raise ValueError('not GWEBL001')
    p = 8
    n = plain[p] - 32; host = plain[p+1:p+1+n].decode('latin1'); p += 1 + n
    sig = (plain[p] - 32) * 128 + (plain[p+1] - 32); p += 2
    modtime = plain[p:p+5]; p += 5
    n = plain[p] - 32; level = plain[p+1:p+1+n].decode('latin1'); p += 1 + n
    mt = 0
    for b in modtime: mt = (mt << 7) | (b - 32)
    hdr = {'host': host, 'signature': sig, 'modtime_raw': modtime.decode('latin1'), 'modtime': mt, 'level': level}
    return hdr, parse_grv(plain, p)

def level_from_filename(path):
    b = os.path.basename(path)
    m = re.match(r'(.*?)(-\d+)?\.code$', b)
    return m.group(1) if m else b

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('file'); ap.add_argument('--level'); ap.add_argument('--raw'); ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    data = open(a.file, 'rb').read()
    plain = decrypt_file(data, a.level or level_from_filename(a.file))
    if a.raw: open(a.raw, 'wb').write(plain)
    hdr, lv = parse_cache(plain)
    if a.json:
        print(json.dumps({'header': hdr, 'level': lv}, indent=1))
    else:
        print(hdr)
        print('version', lv['version'], 'links', len(lv['links']), 'signs', len(lv['signs']))
        for l in lv['links']: print('  link', l)
        for s in lv['signs']: print('  sign', s['x'], s['y'], repr(s['text'][:60]))
