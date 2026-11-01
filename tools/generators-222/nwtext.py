"""GLEVNW01 and GRMAP001 text shared by the 2.22 generators.

`seihai-core` (`assets/level.rs`, `gmap.rs`) already reads BOARD, LINK, NPC
and the LEVELNAMES grid. It skips generator keys such as GENERATED and
HEIGHTMAP, and it does not keep a text HEIGHTS block. This writer stays in
Graal_analysis.
"""

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

LEVEL_W = 64
LEVEL_H = 64


def column_name(index):
    """0 → A, 25 → Z, 26 → AA."""
    if index < 0:
        raise ValueError('column index must be >= 0')
    name = ''
    n = index
    while True:
        name = chr(ord('A') + (n % 26)) + name
        n = n // 26 - 1
        if n < 0:
            return name


def b64_pair(tile):
    tile = int(tile)
    if tile < 0 or tile > 4095:
        raise ValueError('tile id out of range')
    return ALPHABET[tile >> 6] + ALPHABET[tile & 63]


def encode_row(tiles):
    if len(tiles) != LEVEL_W:
        raise ValueError('a board row is 64 tiles')
    return ''.join(b64_pair(tile) for tile in tiles)


def board_lines(tiles):
    """64 `BOARD 0 y 64 0` rows. `tiles` is 4096 ids, row-major."""
    if len(tiles) != LEVEL_W * LEVEL_H:
        raise ValueError('a level board is 64 by 64')
    lines = []
    for y in range(LEVEL_H):
        row = tiles[y * LEVEL_W:(y + 1) * LEVEL_W]
        lines.append('BOARD 0 %d 64 0 %s' % (y, encode_row(row)))
    return lines


def parse_board(text):
    """Read BOARD rows back into 4096 tile ids. Missing rows stay 0."""
    tiles = [0] * (LEVEL_W * LEVEL_H)
    for line in text.splitlines():
        parts = line.strip().split(' ')
        if len(parts) < 6 or parts[0] != 'BOARD':
            continue
        y = int(parts[2])
        width = int(parts[3])
        data = parts[5]
        if y < 0 or y >= LEVEL_H or width != LEVEL_W:
            continue
        for x in range(min(width, len(data) // 2)):
            pair = data[x * 2:x * 2 + 2]
            tiles[y * LEVEL_W + x] = (ALPHABET.index(pair[0]) << 6) | ALPHABET.index(pair[1])
    return tiles


def edge_links(names, width, height, x, y):
    """One link on each side that has a neighbour.

    West arrives at x 61, east at x 0, north at y 61, south at y 0.
    The other axis stays `playerx` or `playery`.
    """
    links = []
    if x > 0:
        links.append('LINK %s 0 0 1 64 61 playery' % names[y * width + (x - 1)])
    if x + 1 < width:
        links.append('LINK %s 63 0 1 64 0 playery' % names[y * width + (x + 1)])
    if y > 0:
        links.append('LINK %s 0 0 64 1 playerx 61' % names[(y - 1) * width + x])
    if y + 1 < height:
        links.append('LINK %s 0 63 64 1 playerx 0' % names[(y + 1) * width + x])
    return links


def npc_block(image, x, y, script):
    body = script.strip('\n')
    lines = ['NPC %s %s %s' % (image or '-', _num(x), _num(y))]
    if body:
        lines.append(body)
    lines.append('NPCEND')
    return '\n'.join(lines)


def level_text(tiles, links=(), npcs=(), extra=()):
    parts = ['GLEVNW01']
    parts.extend(board_lines(tiles))
    parts.extend(extra)
    parts.extend(links)
    parts.extend(npcs)
    return '\n'.join(parts) + '\n'


def levelnames_gmap(width, height, names):
    """GraalLevelGen's GRMAP001: WIDTH, HEIGHT, quoted LEVELNAMES rows."""
    if len(names) != width * height:
        raise ValueError('name count does not match the grid')
    lines = ['GRMAP001', 'WIDTH %d' % width, 'HEIGHT %d' % height, 'LEVELNAMES']
    for y in range(height):
        row = names[y * width:(y + 1) * width]
        lines.append(','.join('"%s"' % name for name in row) + ',')
    lines.append('LEVELNAMESEND')
    return '\n'.join(lines) + '\n'


def dungeon_gmap(width, height, generated):
    """Short dungeon map. GENERATED is the bottom-right level name."""
    return '\n'.join([
        'GRMAP001',
        'WIDTH %d' % width,
        'HEIGHT %d' % height,
        'GENERATED %s' % generated,
    ]) + '\n'


def terrain_gmap(world, width, height, seed, base, even_borders, amplitude,
                 chaos, lev_amplitude, lev_chaos, heightmap_rows, level_seeds):
    """Terrain generator form. Level names are one per line, row-major."""
    lines = [
        'GRMAP001',
        'WIDTH %d' % width,
        'HEIGHT %d' % height,
        'GENERATED 1',
        'GENSEED %d' % seed,
        'GENBASE %s' % _num(base),
        'GENEVENBORDERS %d' % (1 if even_borders else 0),
        'GENHEIGHT %s' % _num(amplitude),
        'GENCHAOS %s' % _num(chaos),
        'LEVHEIGHT %s' % _num(lev_amplitude),
        'LEVCHAOS %s' % _num(lev_chaos),
        'MAPIMG %s.png' % world,
    ]
    for y in range(height):
        for x in range(width):
            lines.append('%s%s%02d.nw' % (world, column_name(x), y))
    lines.append('HEIGHTMAP')
    lines.extend(heightmap_rows)
    lines.append('HEIGHTMAPEND')
    lines.append('RANDOMSEEDS')
    lines.extend(str(value) for value in level_seeds)
    lines.append('RANDOMSEEDSEND')
    return '\n'.join(lines) + '\n'


def heights_block(grid):
    """Nine lines of nine whole numbers, between HEIGHTS and HEIGHTSEND."""
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        raise ValueError('HEIGHTS is 9 by 9')
    lines = ['HEIGHTS']
    for row in grid:
        lines.append(' '.join(str(int(value)) for value in row))
    lines.append('HEIGHTSEND')
    return lines


def _num(value):
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)
