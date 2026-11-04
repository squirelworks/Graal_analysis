#!/usr/bin/env python3
"""Write GANI files that draw a 2.22 built-in baddy the way the client does,
from the arrays.dat of your own Graal install.

Nothing from arrays.dat is stored in this repository: the sprite lists and
sprite rectangles are read from the file you pass in, when you run this.

    gen_ganis.py ARRAYS_DAT OUT_DIR [--image baddygray.png] [--prefix baddy]

What the client draws (client-internals/baddies-222.md, "Drawing"):

  array 20  32 entries, index ani * 4 + dir; each entry is a list of
            sprites, each packed as sprite << 16 | (dx & 255) << 8 | (dy & 255),
            dx and dy signed, in eighths of a tile from the baddy's x, y
  array 22  5 entries: the puff of smoke when a baddy dies
  array 24  the sprite rectangles: x = v >> 23, y = ((v >> 12) & 1023) * 2,
            w = ((v >> 6) & 63) * 2, h = (v & 63) * 2
  sheets    sprites 48-63, 104-106 and 117-130 come from the baddy's own
            image, 111-114 from wbow1.png, every other one from sprites.png
  head      sprites 48-51 are the head; the client draws 48 + head instead,
            so the head can face another way than the body

GANI pixels are 2 per eighth of a tile (16 pixels a tile).

Files written (4 directions each, the body direction is the NPC's dir):

  <prefix>-walk.gani     ani 0 and 1, 200 ms each, looped (walk and hunt)
  <prefix>-stand.gani    ani 0 (the pauses: sight, after a hit)
  <prefix>-look1.gani    ani 0 with the head turned one way (dir + 1)
  <prefix>-look3.gani    ani 0 with the head turned the other way (dir + 3)
  <prefix>-hurt.gani     ani 0 blinking every 50 ms (body, then shadow only)
  <prefix>-aim.gani      ani 2 (bow drawn) for the archer types 3 and 9
  <prefix>-die.gani      the body for 1.1 s, then the puff, 1.5 s in all
  <prefix>-gone.gani     nothing drawn (dead, waiting to respawn)
"""
from __future__ import annotations

import argparse
import os
import struct


def read_arrays(path):
    data = open(path, 'rb').read()
    pos = 0

    def one():
        nonlocal pos
        (head,) = struct.unpack_from('>I', data, pos)
        pos += 4
        kind, count = head >> 16, head & 0xFFFF
        if kind == 0:
            vals = list(struct.unpack_from('>%di' % count, data, pos))
            pos += 4 * count
            return vals
        return [one() for _ in range(count)]

    arrays = [one() for _ in range(25)]
    return arrays


def unpack(v):
    v &= 0xFFFFFFFF
    s, dx, dy = v >> 16, (v >> 8) & 255, v & 255
    return s, dx - 256 if dx > 127 else dx, dy - 256 if dy > 127 else dy


def rect(a24, s):
    v = a24[s] & 0xFFFFFFFF
    return v >> 23, ((v >> 12) & 1023) * 2, ((v >> 6) & 63) * 2, (v & 63) * 2


def sheet(s, image):
    if 48 <= s <= 63 or 104 <= s <= 106 or 117 <= s <= 130:
        return image
    if 111 <= s <= 114:
        return 'wbow1.png'
    return 'SPRITES'


class Gani:
    def __init__(self, a24, image):
        self.a24, self.image = a24, image
        self.used = set()
        self.steps = []

    def row(self, entries, head=None, drop=()):
        parts = []
        for v in entries:
            s, dx, dy = unpack(v)
            if 48 <= s <= 51 and head is not None:
                s = 48 + head
            if s in drop:
                continue
            self.used.add(s)
            parts.append(f'{s:4d} {dx * 2:4d} {dy * 2:4d}')
        return ', '.join(parts) if parts else '   0  -64  -64'

    def write(self, path, loop=True, setbackto=None):
        out = ['GANI0001']
        for s in sorted(self.used | {0}):
            x, y, w, h = rect(self.a24, s)
            out.append(f'SPRITE {s:4d} {sheet(s, self.image):>14} {x:4d} {y:4d} {w:4d} {h:4d} baddy sprite {s}')
        out.append('')
        if loop:
            out.append('LOOP')
        if setbackto:
            out.append(f'SETBACKTO {setbackto}')
        out += ['', 'ANI']
        for rows, wait in self.steps:
            out += rows
            if wait:
                out.append(f'WAIT {wait}')
            out.append('')
        out.append('ANIEND')
        with open(path, 'w', newline='\r\n') as f:
            f.write('\n'.join(out) + '\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('arrays_dat')
    ap.add_argument('out_dir')
    ap.add_argument('--image', default='baddygray.png')
    ap.add_argument('--prefix', default='baddy')
    a = ap.parse_args()
    arrays = read_arrays(a.arrays_dat)
    a20, a22, a24 = arrays[20], arrays[22], arrays[24]
    os.makedirs(a.out_dir, exist_ok=True)

    def gani():
        return Gani(a24, a.image)

    def frame(g, ani, headturn=None, drop=()):
        return [g.row(a20[ani * 4 + d], None if headturn is None else (d + headturn) & 3, drop)
                for d in range(4)]

    jobs = []
    g = gani(); g.steps = [(frame(g, 0), 3), (frame(g, 1), 3)]; jobs.append(('walk', g, True))
    g = gani(); g.steps = [(frame(g, 0), 0)]; jobs.append(('stand', g, False))
    for k in (1, 3):
        g = gani(); g.steps = [(frame(g, 0, k), 0)]; jobs.append((f'look{k}', g, False))
    g = gani(); g.steps = [(frame(g, 0), 0), (frame(g, 0, None, set(range(1, 107))), 0)]
    jobs.append(('hurt', g, True))
    g = gani(); g.steps = [(frame(g, 2), 0)]; jobs.append(('aim', g, False))
    # dying: 14 steps of 100 ms; the body while the counter is above 3, the
    # puff (array 22, entry 4 - counter div 2) while the counter is below 10
    g = gani()
    for c in range(14, -1, -1):
        rows = []
        for d in range(4):
            body = a20[d] if c > 3 else []
            puff = a22[4 - c // 2] if c < 10 else []
            rows.append(g.row(list(body) + list(puff)))
        g.steps.append((rows, 1))
    jobs.append(('die', g, False))
    # gone: one empty step, so the NPC stays but draws nothing
    g = gani(); g.steps = [(['   0  -64  -64'] * 4, 0)]; jobs.append(('gone', g, False))
    for name, g, loop in jobs:
        path = os.path.join(a.out_dir, f'{a.prefix}-{name}.gani')
        g.write(path, loop)
        print('wrote', path)


if __name__ == '__main__':
    main()
