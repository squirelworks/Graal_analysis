"""File names and level containers for the two text level generators.

Static read of GraalLevelGen_graal-txt (2004-01-18) and
GraalLevelGen_nw-txt (2001-06-30). The programs were not run.
The March 2003 HTML (nw-gmap: dashed .nw names and a gmap) is a
different build; see tools/generators-222/.

graal-txt joins prefix, column, "-", row, ".graal".
nw-txt joins prefix, column, row, ".nw" (no dash).
A second column letter is written only when the map is at least 26
levels wide. The row is 1-based and gains a leading zero when the map
is at least 10 levels tall, then another when it is at least 100.
Both write bigmap.txt as one quoted comma-separated row per line.

graal-txt names do not end in .nw, so the shared saver writes GR-V1.03.
nw-txt names end in .nw, and that extension takes the GLEVNW01 writer.
Links, NPCs and the image painter are not part of this container.
"""

BOARD = 64
TILES = BOARD * BOARD
_B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'


def level_name(prefix, x, y, width, height, kind):
    if kind not in ('graal', 'nw'):
        raise ValueError('kind must be graal or nw')
    if width < 1 or height < 1:
        raise ValueError('map size must be at least 1')
    if not 0 <= x < width or not 0 <= y < height:
        raise ValueError('level is outside the map')
    column = _column(x, width)
    row = _row(y, height)
    if kind == 'graal':
        return '%s%s-%s.graal' % (prefix, column, row)
    return '%s%s%s.nw' % (prefix, column, row)


def bigmap_text(names, width):
    if width < 1 or len(names) % width:
        raise ValueError('names do not fill complete rows')
    lines = []
    for start in range(0, len(names), width):
        row = names[start:start + width]
        lines.append(','.join('"%s"' % name for name in row))
    return '\n'.join(lines) + '\n'


def write_world(prefix, width, height, kind, boards=None):
    """Return {filename: bytes or text} including bigmap.txt.

    `boards` maps (x, y) to 4096 tile ids. A missing board is tile 0.
    This does not paint water, mountain or sand edge stamps.
    """
    boards = boards or {}
    names = []
    files = {}
    for y in range(height):
        for x in range(width):
            name = level_name(prefix, x, y, width, height, kind)
            names.append(name)
            tiles = boards.get((x, y), [0] * TILES)
            if len(tiles) != TILES:
                raise ValueError('board is not 64 by 64')
            if kind == 'graal':
                files[name] = graal_level(tiles)
            else:
                files[name] = nw_level(tiles).encode('ascii')
    files['bigmap.txt'] = bigmap_text(names, width).encode('ascii')
    return files


def graal_level(tiles):
    out = bytearray(b'GR-V1.03')
    out += _encode_board_13(tiles)
    out += b'#\n\xff\xff\xff\n#\n#\n'
    return bytes(out)


def nw_level(tiles):
    if len(tiles) != TILES:
        raise ValueError('board is not 64 by 64')
    lines = ['GLEVNW01']
    for y in range(BOARD):
        row = tiles[y * BOARD:(y + 1) * BOARD]
        lines.append('BOARD 0 %d 64 0 %s' % (y, _b64_row(row)))
    return '\n'.join(lines) + '\n'


def _column(x, width):
    low = chr(ord('a') + (x % 26))
    if width < 26:
        return low
    high = chr(ord('a') + ((x // 26) % 26))
    return high + low


def _row(y, height):
    text = str(y + 1)
    if height >= 10 and len(text) < 2:
        text = '0' + text
    if height >= 100 and len(text) < 3:
        text = '0' + text
    return text


def _encode_board_13(tiles):
    if len(tiles) != TILES:
        raise ValueError('board is not 64 by 64')
    codes = []
    i = 0
    while i < TILES:
        tile = tiles[i]
        if i + 1 < TILES and tiles[i + 1] == tile:
            count = 1
            while count < 64 and i + count < TILES and tiles[i + count] == tile:
                count += 1
            codes.append(0x1000 | count)
            codes.append(tile & 0xFFF)
            i += count
            continue
        if (i + 3 < TILES and tiles[i + 2] == tile
                and tiles[i + 1] == tiles[i + 3]):
            other = tiles[i + 1]
            count = 2
            i += 4
            while (count < 64 and i + 1 < TILES
                   and tiles[i] == tile and tiles[i + 1] == other):
                count += 1
                i += 2
            codes.extend((0x1100 | count, tile & 0xFFF, other & 0xFFF))
            continue
        codes.append(tile & 0xFFF)
        i += 1
    return _pack(codes, 13)


def _pack(codes, width):
    buf = nbits = 0
    out = bytearray()
    mask = (1 << width) - 1
    for code in codes:
        buf |= (code & mask) << nbits
        nbits += width
        while nbits >= 8:
            out.append(buf & 0xFF)
            buf >>= 8
            nbits -= 8
    if nbits:
        out.append(buf & 0xFF)
    return bytes(out)


def _b64_row(tiles):
    chars = []
    for tile in tiles:
        if not 0 <= tile <= 4095:
            raise ValueError('tile id is outside 0..4095')
        chars.append(_B64[tile >> 6])
        chars.append(_B64[tile & 63])
    return ''.join(chars)
