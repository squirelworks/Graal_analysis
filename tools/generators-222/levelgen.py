"""GraalLevelGen as shipped in the 2.22 `levelgenerator` folder.

The March 2003 `nw-gmap` build (the HTML in that folder is the same day)
writes `GLEVNW01` levels and a `GRMAP001` with a LEVELNAMES list. A name
that does not end in `.nw` takes the older GR-V1.03 branch instead; this
module writes the `.nw` branch.

Pixels match one of the twelve documented colours when the sum of absolute
channel differences is under 32. The picture is sampled on a 6-pixel grid,
`(pixels + 5) // 6`. Grass is not drawn. Forest places the 6×5 stamp from
the tool's object table. The other colours place one reference fill tile:
the original then draws neighbour edge pieces, and those pieces are not
reproduced here.

A second run reads levels that already exist and paints new tiles over
them. Grass does not erase what is already there. `seihai-core` parses the
same BOARD, LINK and LEVELNAMES text.
"""

import math

from nwtext import edge_links, level_text, levelnames_gmap, parse_board

# Binary order of the colour table, not the order in the HTML.
COLOURS = (
    ('grass', (24, 140, 24)),
    ('forest', (181, 239, 189)),
    ('water', (0, 0, 255)),
    ('mountains', (128, 0, 0)),
    ('flowers', (255, 0, 0)),
    ('sand', (150, 110, 0)),
    ('puddle', (0, 255, 255)),
    ('puddle_stone', (0, 179, 179)),
    ('small_stones', (113, 82, 0)),
    ('big_stone', (83, 61, 0)),
    ('swamp', (0, 106, 0)),
    ('bushes', (0, 66, 0)),
)

# 6×5 forest stamp, row-major, from the nw-gmap object table.
FOREST_STAMP = (
    (25, 26, 27, 28, 29, 30),
    (41, 42, 43, 44, 45, 46),
    (57, 58, 59, 60, 61, 62),
    (73, 74, 75, 76, 77, 78),
    (89, 90, 91, 92, 93, 94),
)

# One tile per colour so a cell is visible. Not the original edge pieces.
FILL = {
    2: 12,
    3: 80,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: 11,
}

MATCH_LIMIT = 32


def match_colour(rgb):
    """Return a colour index, or None when nothing is within the limit."""
    best = None
    best_distance = MATCH_LIMIT
    for index, (_name, colour) in enumerate(COLOURS):
        distance = abs(rgb[0] - colour[0]) + abs(rgb[1] - colour[1]) + abs(rgb[2] - colour[2])
        if distance < best_distance:
            best = index
            best_distance = distance
    return best


def grid_size(width, height):
    return (width + 5) // 6, (height + 5) // 6


def level_name(world, x, y):
    return '%s_%s-%02d.nw' % (world, _column(x), y + 1)


def _column(index):
    name = ''
    n = index
    while True:
        name = chr(ord('a') + (n % 26)) + name
        n = n // 26 - 1
        if n < 0:
            return name


def generate(world, pixels, width, height, existing=None):
    """`pixels` is row-major RGB tuples. `existing` maps a filename to text.

    Returns `{filename: text}` including `world.gmap`.
    """
    if width < 1 or height < 1:
        raise ValueError('image size must be at least 1 pixel')
    if len(pixels) != width * height:
        raise ValueError('pixel count does not match the image size')
    existing = existing or {}
    levels_x = int(math.ceil(width / 64.0))
    levels_y = int(math.ceil(height / 64.0))
    names = [level_name(world, x, y) for y in range(levels_y) for x in range(levels_x)]
    tiles = {}
    kept_tail = {}
    for name in names:
        if name in existing:
            tiles[name] = parse_board(existing[name])
            kept_tail[name] = _tail(existing[name])
        else:
            tiles[name] = [0] * (64 * 64)
            kept_tail[name] = None
    cells_x, cells_y = grid_size(width, height)
    for cy in range(cells_y):
        for cx in range(cells_x):
            px, py = cx * 6, cy * 6
            if px >= width or py >= height:
                continue
            kind = match_colour(pixels[py * width + px])
            if kind is None or kind == 0:
                continue
            if kind == 1:
                origin_x = cx * 6 + (-3 if cy % 2 else 0)
                origin_y = cy * 6 + 1
                _blit(tiles, names, levels_x, levels_y, origin_x, origin_y, FOREST_STAMP)
            else:
                _put(tiles, names, levels_x, levels_y, px, py, FILL[kind])
    files = {}
    for y in range(levels_y):
        for x in range(levels_x):
            name = names[y * levels_x + x]
            if kept_tail[name] is None:
                extra = ()
                links = edge_links(names, levels_x, levels_y, x, y)
                npcs = ()
            else:
                extra = ()
                links = kept_tail[name]['links']
                npcs = kept_tail[name]['npcs']
            files[name] = level_text(tiles[name], links=links, npcs=npcs, extra=extra)
    files['%s.gmap' % world] = levelnames_gmap(levels_x, levels_y, names)
    return files


def _blit(tiles, names, levels_x, levels_y, origin_x, origin_y, stamp):
    for row, line in enumerate(stamp):
        for col, tile in enumerate(line):
            if tile < 0:
                continue
            _put(tiles, names, levels_x, levels_y, origin_x + col, origin_y + row, tile)


def _put(tiles, names, levels_x, levels_y, x, y, tile):
    if x < 0 or y < 0:
        return
    level_x, level_y = x // 64, y // 64
    if level_x >= levels_x or level_y >= levels_y:
        return
    local = (y % 64) * 64 + (x % 64)
    tiles[names[level_y * levels_x + level_x]][local] = tile


def _tail(text):
    links = []
    npcs = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('LINK '):
            links.append(line)
        elif line.startswith('NPC '):
            block = [line]
            i += 1
            while i < len(lines):
                block.append(lines[i])
                if lines[i].strip() == 'NPCEND':
                    break
                i += 1
            npcs.append('\n'.join(block))
        i += 1
    return {'links': links, 'npcs': npcs}
