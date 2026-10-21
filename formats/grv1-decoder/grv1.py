#!/usr/bin/env python3
"""Decode GR-V1.0x / Z3-V1.0x binary levels (.graal / .zelda).

Usage: grv1.py LEVEL [--board] [--json]

Original implementation from the format notes in formats/level-binary.md
and the 2.05 client loader behaviour described in
client-internals/v205-tutorial-levels.md.
"""
import json, sys

ALPHABET = ('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
            '!?-.,#>()#####"####\':/~&### <####;\n')
GLYPHS = {91: '#A', 92: '#B', 93: '#X', 94: '#Y', 77: '#u', 78: '#d',
          79: '#l', 80: '#r', 71: '#x', 72: '#y', 73: '#z', 67: '#.'}
GLYPHS2 = {(74, 75): '#h', (87, 88): '#4'}


def code_width(magic):
    # The 2.05 client reads 13-bit codes only for GR-V1.02 and GR-V1.03.
    return 13 if magic in (b'GR-V1.02', b'GR-V1.03') else 12


class Reader:
    def __init__(self, data):
        self.d, self.p = data, 0

    def byte(self):
        if self.p >= len(self.d):
            return None
        b = self.d[self.p]
        self.p += 1
        return b

    def line(self):
        if self.p >= len(self.d):
            return None
        e = self.d.find(b'\n', self.p)
        e = len(self.d) if e < 0 else e
        s = self.d[self.p:e]
        self.p = e + 1
        return s


def read_board(r, width):
    board, buf, nbits = [], 0, 0
    count, double, first = 1, False, None
    flag = 1 << (width - 1)
    while len(board) < 4096:
        while nbits < width:
            b = r.byte()
            if b is None:
                raise ValueError('board ended early')
            buf |= b << nbits
            nbits += 8
        code = buf & ((1 << width) - 1)
        buf >>= width
        nbits -= width
        if code & flag:
            count = code & 0xFF
            double = bool(code & 0x100)
            continue
        if count == 1:
            board.append(code)
        elif not double:
            board.extend([code] * count)
            count = 1
        elif first is None:
            first = code
        else:
            board.extend([first, code] * count)
            first, count, double = None, 1, False
    return board[:4096]


def decode_sign(payload):
    codes = [b - 32 for b in payload]
    out, i = [], 0
    while i < len(codes):
        c = codes[i]
        if i + 1 < len(codes) and (c, codes[i + 1]) in GLYPHS2:
            out.append(GLYPHS2[(c, codes[i + 1])])
            i += 2
            continue
        if c in GLYPHS:
            out.append(GLYPHS[c])
        elif 0 <= c < len(ALPHABET):
            out.append(ALPHABET[c])
        i += 1
    return ''.join(out).replace('#K(13)', '')


def load(data):
    magic = data[:8]
    if not (magic.startswith(b'GR-V1.0') or magic.startswith(b'Z3-V1.0')):
        raise ValueError('not a GR-V1 / Z3-V1 level: %r' % magic)
    r = Reader(data)
    r.p = 8
    lv = {'magic': magic.decode(), 'links': [], 'baddies': [], 'npcs': [],
          'chests': [], 'signs': []}
    lv['board'] = read_board(r, code_width(magic))
    while True:                                   # links
        s = r.line()
        if not s or s == b'#':
            break
        t = s.decode('latin1').split(' ')
        lv['links'].append({'level': ' '.join(t[:-6]),
                            'x': t[-6], 'y': t[-5], 'w': t[-4], 'h': t[-3],
                            'newx': t[-2], 'newy': t[-1]})
    while True:                                   # baddies
        rec = bytearray()
        while True:
            b = r.byte()
            if b is None or (b == 10 and len(rec) > 2):
                break
            rec.append(b)
        if len(rec) < 3 or rec[0] == 0 or rec[0] >= 0x80:
            break
        verses = rec[3:].decode('latin1').split('\\')
        lv['baddies'].append({'x': rec[0], 'y': rec[1], 'type': rec[2],
                              'verses': verses})
    if magic.startswith(b'GR-'):
        while True:                               # npcs
            s = r.line()
            if not s or s == b'#':
                break
            img, _, script = s[2:].partition(b'#')
            lv['npcs'].append({'x': s[0] - 32, 'y': s[1] - 32,
                               'image': img.decode('latin1'),
                               'script': script.replace(b'\xa7', b'\n').decode('latin1')})
    if magic in (b'GR-V1.01', b'GR-V1.02', b'GR-V1.03'):
        while True:                               # chests
            s = r.line()
            if not s or s == b'#':
                break
            lv['chests'].append({'x': s[0] - 32, 'y': s[1] - 32,
                                 'item': s[2] - 32, 'sign': s[3] - 32})
    while True:                                   # signs
        s = r.line()
        if not s:
            break
        lv['signs'].append({'x': s[0] - 32, 'y': s[1] - 32,
                            'text': decode_sign(s[2:])})
    return lv


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    lv = load(open(sys.argv[1], 'rb').read())
    if '--json' in sys.argv:
        if '--board' not in sys.argv:
            lv.pop('board')
        print(json.dumps(lv, indent=1))
        return
    print('%s  links=%d baddies=%d npcs=%d chests=%d signs=%d' % (
        lv['magic'], len(lv['links']), len(lv['baddies']), len(lv['npcs']),
        len(lv['chests']), len(lv['signs'])))
    for k in ('links', 'baddies', 'chests'):
        for e in lv[k]:
            print(' ', k[:-1] if k != 'baddies' else 'baddy', e)
    for n in lv['npcs']:
        print('  npc', n['x'], n['y'], n['image'] or '(no image)',
              repr(n['script'][:200]))
    for s in lv['signs']:
        print('  sign', s['x'], s['y'], repr(s['text']))
    if '--board' in sys.argv:
        b = lv['board']
        for y in range(64):
            print(' '.join('%4d' % t for t in b[y * 64:y * 64 + 64]))


if __name__ == '__main__':
    main()
