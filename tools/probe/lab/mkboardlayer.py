#!/usr/bin/env python3
"""Write boardlayer.plan: probes of PLO_BOARDLAYER (107) and layered PLO_BOARDMODIFY (7).

  mkboardlayer.py [--x 26] [--y 26] [--tile 0x2a0] > boardlayer.plan

Our lab gserver sends each extra GR-V1.05 / .nw layer as PLO_RAWDATA (100) + 107 with
raw bytes `layer 0 0 64 64` and 4096 little-endian shorts. Each step here sends one
variant at a small rectangle near (X, Y), then the bomb canary as its own packet, and
takes a shot. Bombs are reset to 1 before each step; the canary sets 99.
Variants marked 'wrap' go behind a PLO_RAWDATA length in the same frame (needed when
the body can hold 0x0a).
"""
import sys

a = sys.argv[1:]
X = int(a[a.index('--x') + 1], 0) if '--x' in a else 26
Y = int(a[a.index('--y') + 1], 0) if '--y' in a else 26
T = int(a[a.index('--tile') + 1], 0) if '--tile' in a else 0x2a0


def le(t, n):
    return ('%02x%02x' % (t & 0xff, (t >> 8) & 0xff)) * n


def be(t, n):
    return ('%02x%02x' % ((t >> 8) & 0xff, t & 0xff)) * n


def gs(t, n):
    return ('%02x%02x' % (((t >> 7) & 0x7f) + 32, (t & 0x7f) + 32)) * n


def raw_hdr(layer, x, y, w, h):
    return '%02x%02x%02x%02x%02x' % (layer & 0xff, x & 0xff, y & 0xff, w & 0xff, h & 0xff)


def gc_hdr(layer, x, y, w, h):
    return ''.join('%02x' % ((v + 32) & 0xff) for v in (layer, x, y, w, h))


def p107(hexbody, wrap=True):
    body = bytes.fromhex(hexbody)
    pkt = '107 hex:' + hexbody
    if not wrap:
        return pkt
    n = 1 + len(body) + 1                      # id byte + body + newline
    return '100 i3:%d | %s' % (n, pkt)


steps = []


def step(name, inject, note):
    steps.append((name, inject, note))


n = 64
step('raw-le', p107(raw_hdr(1, X, Y, 8, 8) + le(T, n)), 'server form: raw header, LE tiles, layer 1')
step('raw-le-nowrap', p107(raw_hdr(1, X + 10, Y, 8, 8) + le(T, n), wrap=False), 'same, no RAWDATA wrapper')
step('gchar-hdr', p107(gc_hdr(1, X, Y + 10, 8, 8) + le(T, n)), 'GCHAR header, LE tiles')
step('raw-be', p107(raw_hdr(1, X + 10, Y + 10, 8, 8) + be(T, n)), 'raw header, big-endian tiles')
step('raw-gshort', p107(raw_hdr(1, X - 10, Y, 8, 8) + gs(T, n)), 'raw header, GSHORT tiles')
step('erase-4095', p107(raw_hdr(1, X, Y, 4, 4) + le(4095, 16)), '4095 over part of the raw-le patch')
step('erase-ffff', p107(raw_hdr(1, X + 4, Y, 4, 4) + le(0xffff, 16)), '0xFFFF over the rest of its top half')
step('layer0', p107(raw_hdr(0, X, Y - 10, 8, 8) + le(T, n)), 'layer 0 through 107')
for L in (2, 3, 10, 63, 64, 127, 200, 255):
    step('layer%d' % L, p107(raw_hdr(L, X + (L % 5) * 2, Y - 10, 2, 2) + le(T + 1, 4)), 'layer %d, 2x2' % L)
for t in (4094, 4096, 8191, 0x7fff, 0x8000):
    step('tile%d' % t, p107(raw_hdr(1, X - 6, Y + 10, 2, 2) + le(t, 4)), 'tile value %d' % t)
step('clip-x60w8', p107(raw_hdr(1, 60, Y, 8, 2) + le(T, 16)), 'x 60 + w 8 runs past the edge')
step('w0', p107(raw_hdr(1, X, Y, 0, 8)), 'width 0, no tiles')
step('w65', p107(raw_hdr(1, 0, Y + 4, 65, 1) + le(T, 65)), 'width 65')
step('x64', p107(raw_hdr(1, 64, Y, 1, 1) + le(T, 1)), 'x 64')
step('short-body', p107(raw_hdr(1, X, Y + 20, 8, 8) + le(T, 10)), '8x8 header, 10 tiles')
step('long-body', p107(raw_hdr(1, X, Y + 20, 2, 2) + le(T, 100)), '2x2 header, 100 tiles')
step('full-64', p107(raw_hdr(1, 0, 0, 64, 64) + ''.join(
    le(T if (X <= i % 64 < X + 8 and Y + 12 <= i // 64 < Y + 20) else 4095, 1) for i in range(4096))),
    'full 64x64 layer 1, as the server sends it (resets layer 1)')
step('bm7-layer1', '7 c:%d c:%d c:%d c:2 c:2 hex:%s' % (65, X + 12, Y - 4, gs(T + 2, 4)),
     'PLO_BOARDMODIFY with GCHAR(layer+64) marker, GSHORT tiles (lab server form)')
step('bm7-layer0', '7 c:%d c:%d c:2 c:2 hex:%s' % (X + 15, Y - 4, gs(T + 2, 4)), 'PLO_BOARDMODIFY layer 0 control')

print('# PLO_BOARDLAYER (107) and layered PLO_BOARDMODIFY (7). Written by mkboardlayer.py')
print('# rect near (%d,%d), tile %d. Bombs reset to 1 before each step; canary 99 after it.' % (X, Y, T))
print('waitsession 240')
print('wait s2c 9 90')
print('sleep 12')
print('s2c 9 c:5 c:1')
print('sleep 1.5')
print('shot ref-01')
print('s2c 9 c:5 c:99')
print('sleep 1.5')
print('shot ref-99')
for name, inject, note in steps:
    print('mark %s: %s' % (name, note))
    print('s2c 9 c:5 c:1')
    print('sleep 0.6')
    print('s2c ' + inject)
    print('s2c 9 c:5 c:99')
    print('sleep 1.5')
    print('shot %s' % name)
print('sleep 2')
print('shot end')
