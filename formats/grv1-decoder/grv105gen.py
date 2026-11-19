#!/usr/bin/env python3
"""Write GR-V1.05 test levels (multi-layer binary .graal) for loopback labs.

Usage:
  grv105gen.py OUTDIR [--prefix fz105] [--base LEVEL.graal] [--tile N]

Writes the level set below into OUTDIR, plus OUTDIR/MANIFEST.tsv. Every level
links back to the first one (PREFIX-hub.graal) so a client can walk between them.

Layout written (formats/gr-v105-500r7.md): `GR-V1.05`, GCHAR layer count, one
13-bit board per layer (byte-aligned, no pad after the count), then the usual
GR-V1.03 body (links, baddies, NPCs, chests, signs) and an optional HEIGHTS block.
Upper-layer cells that are not painted are 4095, as the stock 5.00r7 writer leaves them.

--base copies layer 0 (and nothing else) from an existing GR-V1.0x level so the
ground looks like the lab world. Without it layer 0 is all tile 0.

Original code. The set is for our own lab servers only.
"""
import os, sys

EMPTY = 4095            # on-disk empty upper-layer cell (gr-v105-empty-tiles-2026-11-16.md)
FLAG = 1 << 12          # 13-bit RLE control flag


def pack(codes, width=13):
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


def literal_codes(board):
    return list(board)


def rle_codes(board):
    """Single runs (count <= 255) and double runs for two-tile alternations."""
    codes, i, n = [], 0, len(board)
    while i < n:
        t = board[i]
        j = i
        while j < n and board[j] == t and j - i < 255:
            j += 1
        run = j - i
        if run >= 3:
            codes += [FLAG | run, t]
            i = j
            continue
        # double run: a b a b ...
        if i + 3 < n and board[i + 1] != t:
            a, b = t, board[i + 1]
            k = i
            while k + 1 < n and board[k] == a and board[k + 1] == b and (k - i) // 2 < 255:
                k += 2
            pairs = (k - i) // 2
            if pairs >= 2:
                codes += [FLAG | 0x100 | pairs, a, b]
                i = k
                continue
        codes.append(t)
        i += 1
    return codes


def gchar(n):
    return bytes([(n + 32) & 0xff])


def body(links=(), signs=(), heights=None, npcs=()):
    out = bytearray()
    for l in links:
        out += l.encode('latin1') + b'\n'
    out += b'#\n'                     # links end
    out += b'\xff\xff\xff\n'          # baddies end
    for x, y, img, script in npcs:
        out += gchar(x) + gchar(y) + img.encode('latin1') + b'#' + script.replace('\n', '\xa7').encode('latin1') + b'\n'
    out += b'#\n'                     # npcs end
    out += b'#\n'                     # chests end
    for x, y, text in signs:
        out += gchar(x) + gchar(y) + text + b'\n'
    if heights is not None:
        out += b'\nHEIGHTS\n'
        for row in heights:
            out += ','.join(str(v) for v in row).encode() + b'\n'
        out += b'HEIGHTSEND\n'
    return bytes(out)


def level(layers, count=None, rle=False, links=(), heights=None, npcs=(), count_byte=None,
          truncate_layer=None, truncate_at=None, magic=b'GR-V1.05'):
    out = bytearray(magic)
    if magic == b'GR-V1.05':
        if count_byte is not None:
            out.append(count_byte)
        else:
            out += gchar(len(layers) if count is None else count)
    for i, b in enumerate(layers):
        data = pack(rle_codes(b) if rle else literal_codes(b))
        if truncate_layer == i:
            out += data[:truncate_at]
            return bytes(out)
        out += data
    out += body(links=links, heights=heights, npcs=npcs)
    return bytes(out)


def blank():
    return [EMPTY] * 4096


def paint(board, x0, y0, w, h, tile):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            board[y * 64 + x] = tile if not callable(tile) else tile(x, y)
    return board


def load_base(path):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import grv1
    return list(grv1.load(open(path, 'rb').read())['board'])


def build_set(prefix, base, tile):
    hub = prefix + '-hub.graal'
    back = ['%s 0 63 64 1 30 30' % hub]   # bottom edge back to the hub

    def L(*boards):
        return [list(base)] + [list(b) for b in boards]

    patch = paint(blank(), 28, 28, 8, 8, tile)                 # 8x8 block next to the arrival point
    second = paint(blank(), 20, 28, 4, 4, tile + 1)
    checker = paint(blank(), 36, 28, 8, 8, lambda x, y: tile if (x + y) % 2 else EMPTY)
    one4095 = paint(list(patch), 30, 30, 1, 1, EMPTY)          # explicit 4095 inside the patch

    names = ['2', '3', '8', '1', '0', 'rle', 'checker', 'explicit4095', 'heights', 'many-short',
             'count255', 'trunc', 'base4095', 'npc', 'v104']
    hub_links = []
    for i, n in enumerate(names):
        hub_links.append('%s-%s.graal %d 0 2 1 30 32' % (prefix, n, 2 + i * 4))   # top edge doors
    cases = [
        (hub, level(L(), links=hub_links), 'GR-V1.05 hub, one layer, doors along the top edge'),
        ('2', level(L(patch), links=back), '2 layers: 8x8 patch of TILE on layer 1 at (28,28)'),
        ('3', level(L(patch, second), links=back), '3 layers: patch on 1, 4x4 TILE+1 on layer 2 at (20,28)'),
        ('8', level(L(*([blank()] * 6 + [patch])), links=back), '8 layers: only layer 7 painted'),
        ('1', level(L(), links=back), 'count 1: GR-V1.05 with a single board'),
        ('0', level(L(patch), count=0, links=back), 'count byte 0x20 (0 layers) but two boards follow'),
        ('rle', level(L(patch, second), rle=True, links=back), '3 layers, RLE-coded boards (single and double runs)'),
        ('checker', level(L(checker), rle=True, links=back), 'layer 1 checkerboard TILE / 4095 (double runs)'),
        ('explicit4095', level(L(one4095), links=back), 'layer 1 patch with one explicit 4095 cell at (30,30)'),
        ('heights', level(L(patch), links=back, heights=[[1, 2, 3], [4, 5, 6]]), '2 layers + HEIGHTS block after signs'),
        ('many-short', level(L(patch), count=200, links=back), 'count 200 but only two boards in the file'),
        ('count255', level(L(patch), count_byte=0xff, links=back), 'raw count byte 0xff (GCHAR 223) with two boards'),
        ('trunc', level(L(patch), truncate_layer=1, truncate_at=1000), 'layer 1 board cut after 1000 bytes, no body'),
        ('base4095', level([paint(list(base), 28, 28, 8, 8, EMPTY), patch], links=back), 'layer 0 has 4095 cells under the layer-1 patch'),
        ('npc', level(L(patch), links=back, npcs=[(30, 26, '', 'if (created) {\n  setplayerprop #c,layers ok;\n}\n')]), '2 layers + one NPC (body still in step after the boards)'),
        ('v104', level([list(base)], links=back, heights=[[1, 2], [3, 4]], magic=b'GR-V1.04'), 'control: GR-V1.04 with HEIGHTS (lab server reads heights only for 1.05)'),
    ]
    out = []
    for name, data, note in cases:
        fn = name if name.endswith('.graal') else '%s-%s.graal' % (prefix, name)
        out.append((fn, data, note))
    return out


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith('-'):
        sys.exit(__doc__)
    outdir = a[0]
    prefix = a[a.index('--prefix') + 1] if '--prefix' in a else 'fz105'
    tile = int(a[a.index('--tile') + 1], 0) if '--tile' in a else 0x2a0
    base = load_base(a[a.index('--base') + 1]) if '--base' in a else [0] * 4096
    os.makedirs(outdir, exist_ok=True)
    rows = ['file\tbytes\tcase']
    for fn, data, note in build_set(prefix, base, tile):
        open(os.path.join(outdir, fn), 'wb').write(data)
        rows.append('%s\t%d\t%s' % (fn, len(data), note.replace('TILE', str(tile))))
    open(os.path.join(outdir, 'MANIFEST.tsv'), 'w').write('\n'.join(rows) + '\n')
    print('\n'.join(rows))


if __name__ == '__main__':
    main()
