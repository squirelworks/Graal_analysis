"""GRMAP001 read and write, and a directory of level files.

The file form follows formats/gmap.md (the keys a server reader uses):
signature, WIDTH, HEIGHT, LEVELNAMES quoted CSV, MAPIMG, MINIMAPIMG,
NOAUTOMAPPING, LOADFULLMAP, LOADATSTART. Generator-only lines are kept
and written back; they are not turned into cells. gmap.md says GENERATED
is not used to rebuild names.

A directory becomes a gmap from grid.txt (this tool's index, not a client
file) or, if that is absent, from GraalLevelGen names
`prefix_<column>-<row>.ext` (tools/classic-tools/graal-level-gen.md).
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

from errors import ConvertError, Truncated

GRID_NAME = 'grid.txt'
_MAX_SIDE = 512
_LEVEL_EXT = {'.nw', '.graal', '.zelda'}
# prefix_a-01.nw — column letter, 1-based row. graal-level-gen.md.
_LEVELGEN = re.compile(
    r'^.+_([A-Za-z])-([0-9]+)\.(nw|graal|zelda)$',
    re.IGNORECASE,
)
_BLOCKS = ('HEIGHTMAP', 'RANDOMSEEDS')


@dataclass
class Gmap:
    width: int
    height: int
    names: list
    mapimg: str | None = None
    minimap: str | None = None
    no_auto_mapping: bool = False
    load_full_map: bool = False
    load_at_start: list = field(default_factory=list)
    extra: list = field(default_factory=list)

    def cell(self, x, y):
        if not 0 <= y < self.height or not 0 <= x < self.width:
            return ''
        return self.names[y][x]


def loads(data, warnings=None):
    """Parse GRMAP001 text. `data` is bytes or str."""
    if warnings is None:
        warnings = []
    if isinstance(data, (bytes, bytearray)):
        if len(data) < len(b'GRMAP001'):
            raise Truncated('gmap is shorter than the GRMAP001 signature')
        text = bytes(data).decode('latin-1')
    else:
        text = data
        if len(text.encode('latin-1')) < len('GRMAP001'):
            raise Truncated('gmap is shorter than the GRMAP001 signature')
    lines = text.splitlines()
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    if idx >= len(lines):
        raise Truncated('gmap is empty')
    if lines[idx].strip() != 'GRMAP001':
        raise ConvertError('not a GRMAP001 gmap')
    idx += 1
    width = height = None
    rows = []
    saw_names = False
    gmap = Gmap(0, 0, [])
    while idx < len(lines):
        raw = lines[idx]
        idx += 1
        stripped = raw.strip()
        if not stripped:
            continue
        parts = stripped.split()
        key = parts[0]
        if key == 'WIDTH' and len(parts) >= 2:
            width = _side(parts[1], 'WIDTH')
        elif key == 'HEIGHT' and len(parts) >= 2:
            height = _side(parts[1], 'HEIGHT')
        elif key == 'MAPIMG' and len(parts) >= 2:
            gmap.mapimg = parts[1]
        elif key == 'MINIMAPIMG' and len(parts) >= 2:
            gmap.minimap = parts[1]
        elif key == 'NOAUTOMAPPING':
            gmap.no_auto_mapping = True
        elif key == 'LOADFULLMAP':
            gmap.load_full_map = True
        elif key == 'LEVELNAMES':
            saw_names = True
            rows, idx = _csv_block(lines, idx, 'LEVELNAMESEND')
        elif key == 'LOADATSTART':
            body, idx = _csv_block(lines, idx, 'LOADATSTARTEND')
            for row in body:
                gmap.load_at_start.extend(n for n in row if n)
        elif key in _BLOCKS:
            gmap.extra.append(stripped)
            gmap.extra, idx = _raw_block(lines, idx, key + 'END', gmap.extra)
        else:
            gmap.extra.append(stripped)
    if width is None:
        width = max((len(row) for row in rows), default=0)
    if height is None:
        height = len(rows)
    if width < 1 or height < 1:
        raise ConvertError('gmap has no grid size')
    if width > _MAX_SIDE or height > _MAX_SIDE:
        raise ConvertError(
            f'gmap grid is larger than {_MAX_SIDE} on a side, which this tool refuses'
        )
    if not saw_names:
        warnings.append(
            'no LEVELNAMES block; cell names were left empty '
            '(GENERATED is not expanded, formats/gmap.md)'
        )
    names = [['' for _ in range(width)] for _ in range(height)]
    dropped = False
    for y, row in enumerate(rows):
        if y >= height:
            dropped = True
            break
        for x, name in enumerate(row):
            if x >= width:
                dropped = True
                break
            names[y][x] = name
    if dropped:
        warnings.append('LEVELNAMES had cells outside WIDTH and HEIGHT; those were dropped')
    gmap.width = width
    gmap.height = height
    gmap.names = names
    return gmap


def dumps(gmap):
    """Canonical GRMAP001 text. Extra lines follow the reader keys."""
    lines = [
        'GRMAP001',
        f'WIDTH {gmap.width}',
        f'HEIGHT {gmap.height}',
        'LEVELNAMES',
    ]
    for row in gmap.names:
        lines.append(','.join(_quote(name) for name in row))
    lines.append('LEVELNAMESEND')
    if gmap.mapimg:
        lines.append(f'MAPIMG {gmap.mapimg}')
    if gmap.minimap:
        lines.append(f'MINIMAPIMG {gmap.minimap}')
    if gmap.no_auto_mapping:
        lines.append('NOAUTOMAPPING')
    if gmap.load_full_map:
        lines.append('LOADFULLMAP')
    if gmap.load_at_start:
        lines.append('LOADATSTART')
        lines.extend(_quote(name) for name in gmap.load_at_start)
        lines.append('LOADATSTARTEND')
    lines.extend(gmap.extra)
    try:
        return ('\n'.join(lines) + '\n').encode('latin-1')
    except UnicodeEncodeError as exc:
        raise ConvertError('gmap text is not latin-1') from exc


def dumps_grid(gmap):
    """grid.txt body. Occupied cells only; WIDTH and HEIGHT keep the holes."""
    lines = [
        '# cell x, cell y, level file name',
        '# written by tools/level-convert; not a Graal client format',
        f'WIDTH {gmap.width}',
        f'HEIGHT {gmap.height}',
    ]
    for y, row in enumerate(gmap.names):
        for x, name in enumerate(row):
            if name:
                lines.append(f'{x} {y} {name}')
    return '\n'.join(lines) + '\n'


def load_directory(path, warnings=None):
    """Build a gmap from a directory of level files. Does not read subfolders."""
    if warnings is None:
        warnings = []
    path = Path(path)
    if not path.is_dir():
        raise ConvertError(f'not a directory: {path}')
    grid = path / GRID_NAME
    if grid.is_file():
        placed = _placements_from_grid(grid)
    else:
        placed = _placements_from_names(path)
    return _gmap_from_placements(path, placed, warnings)


def _placements_from_grid(grid):
    text = grid.read_bytes().decode('latin-1')
    width = height = None
    placed = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        if parts[0] == 'WIDTH' and len(parts) >= 2:
            width = _side(parts[1], 'WIDTH')
            continue
        if parts[0] == 'HEIGHT' and len(parts) >= 2:
            height = _side(parts[1], 'HEIGHT')
            continue
        if len(parts) != 3:
            raise ConvertError(f'{GRID_NAME}:{lineno} is not "x y filename"')
        x, y = _cell(parts[0], 'x'), _cell(parts[1], 'y')
        name = parts[2]
        _check_name(name)
        placed.append((x, y, name))
    return _finish_placements(placed, width, height)


def _cell(token, label):
    if not re.fullmatch(r'\d+', token):
        raise ConvertError(f'{label} is not a whole number')
    value = int(token, 10)
    if value > _MAX_SIDE:
        raise ConvertError(f'{label} is larger than {_MAX_SIDE}')
    return value


def _placements_from_names(path):
    levels = [p.name for p in path.iterdir() if p.is_file() and p.suffix.lower() in _LEVEL_EXT]
    if not levels:
        raise ConvertError(
            f'{path} has no level files and no {GRID_NAME}. '
            'A .gmap is built from a directory, not from one level renamed.'
        )
    placed = []
    odd = []
    for name in sorted(levels):
        match = _LEVELGEN.match(name)
        if not match:
            odd.append(name)
            continue
        col = match.group(1).lower()
        row = int(match.group(2), 10)
        if row < 1:
            raise ConvertError(f'{name} has a row below 1; GraalLevelGen rows are 1-based')
        placed.append((ord(col) - ord('a'), row - 1, name))
    if odd:
        raise ConvertError(
            'no grid.txt, and these level files are not GraalLevelGen names '
            '(prefix_a-01.nw): ' + ', '.join(odd)
        )
    return _finish_placements(placed, None, None)


def _finish_placements(placed, width, height):
    if not placed and (width is None or height is None):
        raise ConvertError('the directory grid has no level files')
    seen = {}
    max_x = max_y = 0
    for x, y, name in placed:
        if (x, y) in seen:
            raise ConvertError(f'two levels in cell {x},{y}: {seen[(x, y)]} and {name}')
        seen[(x, y)] = name
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    if width is None:
        width = max_x + 1
    if height is None:
        height = max_y + 1
    if width < 1 or height < 1 or width > _MAX_SIDE or height > _MAX_SIDE:
        raise ConvertError(f'grid must be between 1 and {_MAX_SIDE} on a side')
    for x, y, name in placed:
        if x >= width or y >= height:
            raise ConvertError(f'{name} is outside WIDTH {width} HEIGHT {height}')
    return width, height, placed


def _gmap_from_placements(path, placed, warnings):
    import levelio

    width, height, cells = placed
    names = [['' for _ in range(width)] for _ in range(height)]
    for x, y, name in cells:
        level_path = path / name
        if not level_path.is_file():
            raise ConvertError(f'file does not exist: {name}')
        if level_path.suffix.lower() not in _LEVEL_EXT:
            raise ConvertError(f'{name} is not a .nw, .graal or .zelda level')
        # A truncated level fails the build. The gmap stores the name only.
        levelio.load_path(level_path, warnings)
        names[y][x] = name
    return Gmap(width, height, names)


def _check_name(name):
    if name in ('', '.', '..') or '/' in name or '\\' in name:
        raise ConvertError(f'level name {name!r} is not a file in the directory')


def _side(token, label):
    if not re.fullmatch(r'\d+', token):
        raise ConvertError(f'{label} is not a whole number')
    value = int(token, 10)
    if value < 1:
        raise ConvertError(f'{label} must be at least 1')
    return value


def _quote(name):
    return '"' + name.replace('"', '""') + '"'


def _split_csv(line):
    fields = []
    cur = []
    in_quote = False
    i = 0
    while i < len(line):
        ch = line[i]
        if in_quote:
            if ch == '"':
                if i + 1 < len(line) and line[i + 1] == '"':
                    cur.append('"')
                    i += 2
                    continue
                in_quote = False
            else:
                cur.append(ch)
        elif ch == '"':
            in_quote = True
        elif ch == ',':
            fields.append(''.join(cur).strip())
            cur = []
        else:
            cur.append(ch)
        i += 1
    if in_quote:
        raise Truncated('LEVELNAMES quote is not closed')
    tail = ''.join(cur).strip()
    if line.rstrip().endswith(',') and tail == '':
        return fields
    fields.append(tail)
    return fields


def _csv_block(lines, idx, end):
    rows = []
    closed = False
    while idx < len(lines):
        row = lines[idx]
        idx += 1
        if row.strip() == end:
            closed = True
            break
        if row.strip():
            rows.append(_split_csv(row))
    if not closed:
        raise Truncated(f'{end} missing')
    return rows, idx


def _raw_block(lines, idx, end, extra):
    closed = False
    while idx < len(lines):
        row = lines[idx]
        idx += 1
        extra.append(row.strip())
        if row.strip() == end:
            closed = True
            break
    if not closed:
        raise Truncated(f'{end} missing')
    return extra, idx
