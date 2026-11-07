"""Dungeon generator shipped in Graal 2.22 (`dungeongen`).

Reads a GDUNG001 options file. A layout is either a hand-drawn `X` / `.`
grid or one of the styles named in the 2003 manual (maze, onion, spiral,
rogue, snake, squarespiral). Each cell is an 8×11 tile block. Blocks are
sliced into 64×64 levels with edge links, optional NPCs, and a short
GRMAP001 whose GENERATED name is the bottom-right level.

The style layouts are clean-room maps of those shapes. They are not a
replay of DungeonMaker 0.9, which the Linux build links in for the random
styles. The original executables were not run.
"""

import math

from nwtext import (
    column_name,
    dungeon_gmap,
    edge_links,
    level_text,
    npc_block,
)

BLOCK_W = 8
BLOCK_H = 11
PLACES = (
    'wall', 'path',
    'walln', 'walle', 'walls', 'wallw',
    'wallne', 'wallnw', 'wallse', 'wallsw',
    'wallne2', 'wallnw2', 'wallse2', 'wallsw2',
    'walld1', 'walld2',
)


class DelphiRandom:
    def __init__(self, seed):
        self.seed = int(seed) & 0xFFFFFFFF

    def unit(self):
        self.seed = (self.seed * 0x08088405 + 1) & 0xFFFFFFFF
        return self.seed / 4294967296.0

    def below(self, limit):
        if limit <= 0:
            raise ValueError('limit must be positive')
        return int(self.unit() * limit)


def parse_options(text):
    """Return a dict. NPC rules and TILES blocks keep their file order."""
    lines = [line.strip() for line in text.replace('\r\n', '\n').replace('\r', '\n').split('\n')]
    body = [line for line in lines if line and not line.startswith('#')]
    if not body or body[0] != 'GDUNG001':
        raise ValueError('dungeon options must start with GDUNG001')
    opts = {
        'levelstart': 'level_',
        'gmap': 'dungeon',
        'walltiles': '',
        'groundtiles': '',
        'layoutwidth': 8,
        'layoutheight': 8,
        'layoutstyle': 'maze',
        'double': 1,
        'layoutoption': 0,
        'layoutsymmetry': 1,
        'layoutorientation': 1,
        'randomseed': 1,
        'addtestnpcs': False,
        'layoutfile': None,
        'npcs': [],
        'tiles': {},
    }
    for line in body[1:]:
        if line == 'ADDTESTNPCS':
            opts['addtestnpcs'] = True
            continue
        if line.startswith('NPC '):
            opts['npcs'].append(_npc_rule(line[4:]))
            continue
        if line.startswith('TILES '):
            name, ids = _tiles_line(line[6:])
            opts['tiles'][name] = ids
            continue
        key, _, value = line.partition(' ')
        key = key.upper()
        if key in ('LEVELSTART', 'GMAP', 'WALLTILES', 'GROUNDTILES', 'LAYOUTFILE'):
            field = {
                'LEVELSTART': 'levelstart',
                'GMAP': 'gmap',
                'WALLTILES': 'walltiles',
                'GROUNDTILES': 'groundtiles',
                'LAYOUTFILE': 'layoutfile',
            }[key]
            opts[field] = value
        elif key == 'LAYOUTSTYLE':
            opts['layoutstyle'] = value.lower()
        elif key in ('LAYOUTWIDTH', 'LAYOUTHEIGHT', 'DOUBLE', 'LAYOUTOPTION',
                     'LAYOUTSYMMETRY', 'LAYOUTORIENTATION', 'RANDOMSEED'):
            field = {
                'LAYOUTWIDTH': 'layoutwidth',
                'LAYOUTHEIGHT': 'layoutheight',
                'DOUBLE': 'double',
                'LAYOUTOPTION': 'layoutoption',
                'LAYOUTSYMMETRY': 'layoutsymmetry',
                'LAYOUTORIENTATION': 'layoutorientation',
                'RANDOMSEED': 'randomseed',
            }[key]
            opts[field] = int(value)
    return opts


def _npc_rule(body):
    rule = {
        'image': '-',
        'script': '',
        'blocking': True,
        'underplayer': False,
        'dominant': False,
        'chance': 1.0,
        'place': 'path',
        'x': 0.0,
        'y': 0.0,
    }
    for part in body.split(','):
        name, _, value = part.strip().partition('=')
        name = name.strip().lower()
        value = value.strip()
        if name == 'image':
            rule['image'] = value or '-'
        elif name == 'script':
            rule['script'] = value
        elif name == 'blocking':
            rule['blocking'] = value.lower() == 'true'
        elif name == 'underplayer':
            rule['underplayer'] = value.lower() == 'true'
        elif name == 'dominant':
            rule['dominant'] = value.lower() == 'true'
        elif name == 'chance':
            # `30%` and a bare `30` are both 30 percent. The manual's range is 1 to 100.
            rule['chance'] = float(value.rstrip('%')) / 100.0
        elif name == 'place':
            rule['place'] = value.lower()
        elif name == 'x':
            rule['x'] = float(value)
        elif name == 'y':
            rule['y'] = float(value)
    return rule


def _tiles_line(body):
    name, _, rest = body.partition('=')
    ids = []
    for piece in rest.split(','):
        piece = piece.strip()
        if not piece:
            continue
        ids.append(int(piece, 0))
    if len(ids) != BLOCK_W * BLOCK_H:
        raise ValueError('TILES %s needs %d ids' % (name, BLOCK_W * BLOCK_H))
    return name.strip().lower(), ids


def load_layout(text):
    rows = [line.rstrip('\r') for line in text.splitlines() if line.strip()]
    if not rows:
        raise ValueError('layout file is empty')
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError('layout rows must be the same length')
    return [list(row) for row in rows]


def classify(grid):
    """Place name for every cell. See the module note for the facing rule."""
    height = len(grid)
    width = len(grid[0])
    out = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(_place(grid, x, y))
        out.append(row)
    return out


def _is_path(grid, x, y):
    if y < 0 or x < 0 or y >= len(grid) or x >= len(grid[0]):
        return False
    return grid[y][x] != 'X'


def _place(grid, x, y):
    if grid[y][x] != 'X':
        return 'path'
    north = _is_path(grid, x, y - 1)
    south = _is_path(grid, x, y + 1)
    west = _is_path(grid, x - 1, y)
    east = _is_path(grid, x + 1, y)
    # The name is the side of the room the wall sits on.
    # One open side: the wall sits on the far side of that path.
    if north and not south and not west and not east:
        return 'walls'
    if south and not north and not west and not east:
        return 'walln'
    if west and not east and not north and not south:
        return 'walle'
    if east and not west and not north and not south:
        return 'wallw'
    # Two adjacent open sides: a 270° notch. The name is the open corner.
    if south and east and not north and not west:
        return 'wallse2'
    if south and west and not north and not east:
        return 'wallsw2'
    if north and east and not south and not west:
        return 'wallne2'
    if north and west and not south and not east:
        return 'wallnw2'
    if north and south and not east and not west:
        return 'walld1'
    if east and west and not north and not south:
        return 'walld2'
    # No open side, one open diagonal: the 90° corner of a rectangular room.
    # The corner is named for the wall, opposite the path.
    if not (north or south or west or east):
        ne = _is_path(grid, x + 1, y - 1)
        nw = _is_path(grid, x - 1, y - 1)
        se = _is_path(grid, x + 1, y + 1)
        sw = _is_path(grid, x - 1, y + 1)
        if se and not (ne or nw or sw):
            return 'wallnw'
        if sw and not (ne or nw or se):
            return 'wallne'
        if ne and not (nw or se or sw):
            return 'wallsw'
        if nw and not (ne or se or sw):
            return 'wallse'
    return 'wall'


def default_stamp(place):
    """8×11 block used when the options file has no TILES line for `place`."""
    tiles = [0] * (BLOCK_W * BLOCK_H)
    if place == 'path':
        return tiles
    for i in range(len(tiles)):
        tiles[i] = 1
    def clear(x, y):
        if 0 <= x < BLOCK_W and 0 <= y < BLOCK_H:
            tiles[y * BLOCK_W + x] = 0
    opening = {
        'walln': 's', 'walls': 'n', 'walle': 'w', 'wallw': 'e',
        'wallnw': 'se', 'wallne': 'sw', 'wallsw': 'ne', 'wallse': 'nw',
        'wallse2': 'se', 'wallsw2': 'sw', 'wallne2': 'ne', 'wallnw2': 'nw',
    }.get(place, '')
    if 'n' in opening:
        for x in range(BLOCK_W):
            clear(x, 0)
            clear(x, 1)
    if 's' in opening:
        for x in range(BLOCK_W):
            clear(x, BLOCK_H - 1)
            clear(x, BLOCK_H - 2)
    if 'w' in opening:
        for y in range(BLOCK_H):
            clear(0, y)
            clear(1, y)
    if 'e' in opening:
        for y in range(BLOCK_H):
            clear(BLOCK_W - 1, y)
            clear(BLOCK_W - 2, y)
    return tiles


def stamp_for(place, tilesets):
    if place in tilesets:
        return tilesets[place]
    return default_stamp(place)


def paint(grid, tilesets):
    """Tile ids for the whole dungeon, row-major, before the level cut."""
    places = classify(grid)
    height = len(grid)
    width = len(grid[0])
    pixel_w = width * BLOCK_W
    pixel_h = height * BLOCK_H
    board = [0] * (pixel_w * pixel_h)
    for y in range(height):
        for x in range(width):
            block = stamp_for(places[y][x], tilesets)
            origin_x = x * BLOCK_W
            origin_y = y * BLOCK_H
            for by in range(BLOCK_H):
                for bx in range(BLOCK_W):
                    board[(origin_y + by) * pixel_w + (origin_x + bx)] = block[by * BLOCK_W + bx]
    return board, pixel_w, pixel_h, places


def generate(options_text, layouts=None, scripts=None):
    """`layouts` and `scripts` map filenames to text. Nothing is read from disk."""
    opts = parse_options(options_text)
    layouts = layouts or {}
    scripts = scripts or {}
    if opts['layoutfile']:
        if opts['layoutfile'] not in layouts:
            raise ValueError('layout file %s was not provided' % opts['layoutfile'])
        grid = load_layout(layouts[opts['layoutfile']])
    else:
        grid = styled_layout(
            opts['layoutstyle'], opts['layoutwidth'], opts['layoutheight'],
            opts['layoutoption'], opts['double'], opts['layoutsymmetry'],
            opts['randomseed'],
        )
    board, pixel_w, pixel_h, places = paint(grid, opts['tiles'])
    levels_x = int(math.ceil(pixel_w / 64.0))
    levels_y = int(math.ceil(pixel_h / 64.0))
    names = [
        '%s%s%d.nw' % (opts['levelstart'], column_name(x), y + 1)
        for y in range(levels_y) for x in range(levels_x)
    ]
    npcs_by_level = _place_npcs(opts, places, scripts, levels_x, levels_y)
    files = {}
    for y in range(levels_y):
        for x in range(levels_x):
            tiles = _slice_level(board, pixel_w, pixel_h, x, y)
            text = level_text(
                tiles,
                links=edge_links(names, levels_x, levels_y, x, y),
                npcs=npcs_by_level.get((x, y), []),
            )
            files[names[y * levels_x + x]] = text
    files['%s.gmap' % opts['gmap']] = dungeon_gmap(
        levels_x, levels_y, names[-1],
    )
    return files


def _slice_level(board, pixel_w, pixel_h, level_x, level_y):
    tiles = [0] * (64 * 64)
    for y in range(64):
        src_y = level_y * 64 + y
        if src_y >= pixel_h:
            break
        for x in range(64):
            src_x = level_x * 64 + x
            if src_x >= pixel_w:
                break
            tiles[y * 64 + x] = board[src_y * pixel_w + src_x]
    return tiles


def _place_npcs(opts, places, scripts, levels_x, levels_y):
    rng = DelphiRandom(opts['randomseed'])
    found = {}
    dominant = set()
    height = len(places)
    width = len(places[0])
    for rule in opts['npcs']:
        for y in range(height):
            for x in range(width):
                if places[y][x] != rule['place']:
                    continue
                if rule['dominant'] and (x, y) in dominant:
                    continue
                if rng.unit() >= rule['chance']:
                    continue
                if rule['dominant']:
                    dominant.add((x, y))
                px = x * BLOCK_W + rule['x']
                py = y * BLOCK_H + rule['y']
                level_x = int(px) // 64
                level_y = int(py) // 64
                if level_x >= levels_x or level_y >= levels_y:
                    continue
                script = _npc_script(rule, scripts.get(rule['script'], ''))
                block = npc_block(rule['image'], px - level_x * 64, py - level_y * 64, script)
                found.setdefault((level_x, level_y), []).append(block)
    if opts['addtestnpcs']:
        script = _test_script(opts)
        for y in range(levels_y):
            for x in range(levels_x):
                found.setdefault((x, y), []).append(npc_block('-', 32, 32, script))
    return found


def _npc_script(rule, body):
    lines = []
    flags = []
    if not rule['blocking']:
        flags.append('  dontblock;')
    if rule['underplayer']:
        flags.append('  drawunderplayer;')
    if flags:
        lines.append('if (created) {')
        lines.extend(flags)
        lines.append('}')
    if body:
        lines.append(body.strip('\n'))
    return '\n'.join(lines)


def _test_script(opts):
    return '\n'.join([
        'if (playerenters) {',
        '//#CLIENTSIDE',
        '  addtiledef tiles_inside.png,%s,1;' % opts['levelstart'],
        '  addtiledef2 %s,%s,1024,224;' % (opts['walltiles'], opts['levelstart']),
        '  addtiledef2 %s,%s,1216,0;' % (opts['groundtiles'], opts['levelstart']),
        '  loadmap %s;' % opts['gmap'],
        '}',
    ])


def styled_layout(style, width, height, option, double, symmetry, seed):
    if width < 1 or height < 1:
        raise ValueError('layout size must be at least 1')
    rng = DelphiRandom(seed)
    style = style.lower()
    if style == 'maze':
        grid = _maze(width, height, rng, full=(option == 1), double=double)
    elif style == 'onion':
        grid = _onion(width, height, option, rng)
    elif style == 'snake':
        grid = _snake(width, height)
    elif style == 'squarespiral':
        grid = _square_spiral(width, height)
    elif style == 'spiral':
        grid = _round_spiral(width, height, option)
    elif style == 'rogue':
        grid = _rogue(width, height, rng, option)
    else:
        raise ValueError('unknown layout style %s' % style)
    mode = symmetry
    if mode == 0:
        mode = 1 + rng.below(4)
    return _symmetry(grid, mode)


def _maze(width, height, rng, full, double):
    """Carve passages. DOUBLE 1 draws the maze on half the cells, then scales up."""
    if double:
        coarse_w = max(3, width // 2)
        coarse_h = max(3, height // 2)
        coarse = _carve_maze(coarse_w, coarse_h, rng, full)
        grid = [['X'] * width for _ in range(height)]
        for y in range(coarse_h):
            for x in range(coarse_w):
                for dy in range(2):
                    for dx in range(2):
                        yy, xx = y * 2 + dy, x * 2 + dx
                        if yy < height and xx < width:
                            grid[yy][xx] = coarse[y][x]
        return grid
    return _carve_maze(width, height, rng, full)


def _carve_maze(width, height, rng, full):
    grid = [['X'] * width for _ in range(height)]
    if width < 3 or height < 3:
        for y in range(height):
            for x in range(width):
                grid[y][x] = '.'
        return grid
    start_x = 1 if width > 2 else 0
    start_y = 1 if height > 2 else 0
    grid[start_y][start_x] = '.'
    stack = [(start_x, start_y)]
    while stack:
        x, y = stack[-1]
        ways = []
        for dx, dy in ((0, -2), (2, 0), (0, 2), (-2, 0)):
            nx, ny = x + dx, y + dy
            if 0 < nx < width - (0 if full else 1) and 0 < ny < height - (0 if full else 1) and grid[ny][nx] == 'X':
                if 0 <= nx < width and 0 <= ny < height:
                    ways.append((dx, dy))
        if not ways:
            stack.pop()
            continue
        dx, dy = ways[rng.below(len(ways))]
        grid[y + dy // 2][x + dx // 2] = '.'
        grid[y + dy][x + dx] = '.'
        stack.append((x + dx, y + dy))
    if full:
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if grid[y][x] == 'X' and rng.unit() < 0.15:
                    grid[y][x] = '.'
    return grid


def _onion(width, height, option, rng):
    if option == 0:
        option = 1
    grid = [['.'] * width for _ in range(height)]
    if option & 16:
        inset = 1
    else:
        inset = 0
    layer = 0
    while inset < width // 2 and inset < height // 2:
        for x in range(inset, width - inset):
            grid[inset][x] = 'X'
            grid[height - 1 - inset][x] = 'X'
        for y in range(inset, height - inset):
            grid[y][inset] = 'X'
            grid[y][width - 1 - inset] = 'X'
        door_x = width // 2
        door_y = height // 2
        if option & 8:
            door_x = width - 1 - inset
            door_y = height - 1 - inset
        elif option & 4:
            door_y = height - 1 - inset
        if 0 <= door_y < height and 0 <= door_x < width:
            grid[door_y][min(width - 1 - inset, max(inset, door_x))] = '.'
        step = 2
        if option & 32:
            step = 2 + rng.below(2)
        inset += step
        layer += 1
        if layer > max(width, height):
            break
    return grid


def _snake(width, height):
    grid = [['X'] * width for _ in range(height)]
    band = 0
    y = 1
    while y < height - 1:
        for x in range(1, width - 1):
            grid[y][x] = '.'
        if y + 2 < height - 1:
            door = 1 if band % 2 == 0 else width - 2
            grid[y + 1][door] = '.'
        y += 2
        band += 1
    return grid


def _square_spiral(width, height):
    grid = [['X'] * width for _ in range(height)]
    left, right, top, bottom = 1, width - 2, 1, height - 2
    while left <= right and top <= bottom:
        for x in range(left, right + 1):
            grid[top][x] = '.'
        for y in range(top + 1, bottom + 1):
            grid[y][right] = '.'
        if top < bottom:
            for x in range(right - 1, left - 1, -1):
                grid[bottom][x] = '.'
        if left < right:
            for y in range(bottom - 1, top, -1):
                grid[y][left] = '.'
        left += 2
        right -= 2
        top += 2
        bottom -= 2
    return grid


def _round_spiral(width, height, option):
    grid = [['X'] * width for _ in range(height)]
    cx = (width - 1) / 2.0
    cy = (height - 1) / 2.0
    turns = 3 if option & 2 else 2
    steps = max(width, height) * turns * 4
    for i in range(steps):
        angle = i / float(max(steps, 1)) * turns * 2.0 * math.pi
        radius = 0.5 + (i / float(max(steps, 1))) * min(cx, cy)
        if option & 4:
            x = int(round(cx + math.cos(angle) * radius * (width / float(height or 1))))
        else:
            x = int(round(cx + math.cos(angle) * radius))
        y = int(round(cy + math.sin(angle) * radius))
        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = '.'
    return grid


def _rogue(width, height, rng, option):
    grid = [['X'] * width for _ in range(height)]
    rooms = []
    count = 3 if width >= 8 and height >= 8 else 1
    for _ in range(count * 4):
        if len(rooms) >= count:
            break
        if option & 2:
            rw = rh = 3 + rng.below(3)
        else:
            rw = 3 + rng.below(max(1, width // 3))
            rh = 3 + rng.below(max(1, height // 3))
        if rw >= width or rh >= height:
            continue
        rx = rng.below(width - rw)
        ry = rng.below(height - rh)
        if any(_rooms_touch(rx, ry, rw, rh, other) for other in rooms):
            continue
        rooms.append((rx, ry, rw, rh))
        for y in range(ry, ry + rh):
            for x in range(rx, rx + rw):
                if option & 2:
                    dx = x - (rx + rw / 2.0)
                    dy = y - (ry + rh / 2.0)
                    if dx * dx + dy * dy > (min(rw, rh) / 2.0) ** 2:
                        continue
                grid[y][x] = '.'
    for i in range(len(rooms) - 1):
        x0 = rooms[i][0] + rooms[i][2] // 2
        y0 = rooms[i][1] + rooms[i][3] // 2
        x1 = rooms[i + 1][0] + rooms[i + 1][2] // 2
        y1 = rooms[i + 1][1] + rooms[i + 1][3] // 2
        _corridor(grid, x0, y0, x1, y1)
    if not rooms:
        grid[height // 2][width // 2] = '.'
    return grid


def _rooms_touch(x, y, w, h, other):
    ox, oy, ow, oh = other
    return not (x + w + 1 < ox or ox + ow + 1 < x or y + h + 1 < oy or oy + oh + 1 < y)


def _corridor(grid, x0, y0, x1, y1):
    x, y = x0, y0
    while x != x1:
        grid[y][x] = '.'
        x += 1 if x1 > x else -1
    while y != y1:
        grid[y][x] = '.'
        y += 1 if y1 > y else -1
    grid[y][x] = '.'


def _symmetry(grid, mode):
    if mode not in (1, 2, 3, 4):
        raise ValueError('symmetry must be 0..4')
    height = len(grid)
    width = len(grid[0])
    if mode in (2, 4):
        for y in range(height):
            for x in range(width // 2):
                grid[y][width - 1 - x] = grid[y][x]
    if mode in (3, 4):
        for y in range(height // 2):
            grid[height - 1 - y] = list(grid[y])
    return grid
