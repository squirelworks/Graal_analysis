"""Read and write one level: Z3-V1, GR-V1, GLEVNW01.

Binary files are read by formats/grv1-decoder/grv1.py. The GR-V1.03 board is
written by tools/file-formats/gwebl.py write_board (the 13-bit encoder the
notes checked against the client). Z3-V1 uses the same run rules with the
12-bit flag from formats/level-binary.md. GLEVNW01 follows formats/glevnw01.txt
and the 2.05 / 2.22 text writer in client-internals/level-editor-205.md and
tools/level-editor/222-reference.md.

.zelda output is Z3-V1.04 (verse line, no NPC section, no chest section).
.graal output is GR-V1.03. .nw output is GLEVNW01.
"""

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from errors import ConvertError, Truncated

BOARD = 64
TILES = BOARD * BOARD
B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
# 2.05 editor list, client-internals/level-editor-205.md. Indexes 0..24.
CHEST_ITEMS = (
    'greenrupee', 'bluerupee', 'redrupee', 'bombs', 'darts', 'heart',
    'glove1', 'bow', 'bomb', 'shield', 'sword', 'fullheart', 'superbomb',
    'battleaxe', 'goldensword', 'mirrorshield', 'glove2', 'lizardshield',
    'lizardsword', 'goldrupee', 'fireball', 'fireblast', 'nukeshot',
    'joltbomb', 'spinattack',
)
GRAAL_MAGICS = {b'GR-V1.00', b'GR-V1.01', b'GR-V1.02', b'GR-V1.03', b'GR-V1.04'}
ZELDA_MAGICS = {b'Z3-V1.02', b'Z3-V1.03', b'Z3-V1.04'}
_ESCAPE = re.compile(r'#K\((\d{1,3})\)')
_INT = re.compile(r'[+-]?\d+')
_grv1_mod = None
_gwebl_mod = None
_sign_cache = None


def _repo_root():
    return Path(__file__).resolve().parents[2]


def _grv1():
    global _grv1_mod
    if _grv1_mod is None:
        folder = str(_repo_root() / 'formats' / 'grv1-decoder')
        if folder not in sys.path:
            sys.path.insert(0, folder)
        import grv1
        _grv1_mod = grv1
    return _grv1_mod


def _gwebl():
    global _gwebl_mod
    if _gwebl_mod is None:
        folder = str(_repo_root() / 'tools' / 'file-formats')
        if folder not in sys.path:
            sys.path.insert(0, folder)
        import gwebl
        _gwebl_mod = gwebl
    return _gwebl_mod


@dataclass
class Link:
    dest: str
    x: str
    y: str
    w: str
    h: str
    newx: str
    newy: str


@dataclass
class Baddy:
    x: str
    y: str
    type_text: str
    verses: list


@dataclass
class Npc:
    image: str
    x: str
    y: str
    script: str


@dataclass
class Chest:
    x: str
    y: str
    item: str
    sign: str


@dataclass
class Sign:
    x: str
    y: str
    text: str


@dataclass
class Level:
    board: list
    links: list = field(default_factory=list)
    baddies: list = field(default_factory=list)
    npcs: list = field(default_factory=list)
    chests: list = field(default_factory=list)
    signs: list = field(default_factory=list)
    heights: list | None = None

    def __post_init__(self):
        if len(self.board) != TILES:
            raise ConvertError('board is not 64 by 64')


def read_file(path):
    path = Path(path)
    if not path.is_file():
        raise ConvertError(f'file does not exist: {path}')
    data = path.read_bytes()
    if not data:
        raise Truncated(f'{path.name} is empty')
    return data


def load_path(path, warnings=None):
    """Load one level. The suffix picks the reader; a binary magic overrides .graal vs .zelda."""
    if warnings is None:
        warnings = []
    path = Path(path)
    ext = path.suffix.lower()
    data = read_file(path)
    if ext == '.nw':
        return loads_nw(data, warnings)
    if ext in ('.graal', '.zelda'):
        level = loads_binary(data)
        magic = data[:8]
        if ext == '.zelda' and magic.startswith(b'GR-'):
            warnings.append(
                f'{path.name} is named .zelda but its magic is {magic.decode("latin-1")}; '
                'the magic decides, so any NPC and chest sections are read'
            )
        elif ext == '.graal' and magic.startswith(b'Z3-'):
            warnings.append(
                f'{path.name} is named .graal but its magic is {magic.decode("latin-1")}; '
                'the magic decides, so it has no NPC or chest section'
            )
        return level
    raise ConvertError(f'{path.name} is not a .zelda, .graal or .nw level')


def loads_binary(data):
    if len(data) < 8:
        raise Truncated('file shorter than an 8-byte magic')
    magic = bytes(data[:8])
    if magic not in GRAAL_MAGICS and magic not in ZELDA_MAGICS:
        raise ConvertError('not a GR-V1.00-04 or Z3-V1.02/03/04 level')
    try:
        raw = _grv1().load(bytes(data))
    except ValueError as exc:
        raise Truncated(str(exc)) from exc
    except IndexError as exc:
        raise Truncated('binary level ended inside a record') from exc
    board = list(raw['board'])
    if len(board) != TILES:
        raise Truncated('board is not 64 by 64')
    links = [
        Link(item['level'], item['x'], item['y'], item['w'], item['h'], item['newx'], item['newy'])
        for item in raw['links']
    ]
    baddies = [
        Baddy(str(item['x']), str(item['y']), str(item['type']), _clean_verses(item['verses']))
        for item in raw['baddies']
    ]
    npcs = [
        Npc(item['image'], str(item['x']), str(item['y']), item['script'])
        for item in raw['npcs']
    ]
    chests = []
    for item in raw['chests']:
        index = item['item']
        if isinstance(index, int) and 0 <= index < len(CHEST_ITEMS):
            name = CHEST_ITEMS[index]
        else:
            name = str(index)
        chests.append(Chest(str(item['x']), str(item['y']), name, str(item['sign'])))
    signs = [
        Sign(str(item['x']), str(item['y']), expand_sign_text(item['text']))
        for item in raw['signs']
    ]
    return Level(board, links, baddies, npcs, chests, signs, _heights_from_grv(raw.get('heights')))


def loads_nw(data, warnings=None):
    if warnings is None:
        warnings = []
    if isinstance(data, str):
        text = data
        raw = text.encode('latin-1')
    else:
        raw = bytes(data)
        text = raw.decode('latin-1')
    if len(raw) < len(b'GLEVNW01'):
        raise Truncated('nw file shorter than the GLEVNW01 signature')
    lines = text.splitlines()
    if not lines or lines[0].strip() != 'GLEVNW01':
        raise ConvertError('not a GLEVNW01 level')
    board = [0] * TILES
    links, baddies, npcs, chests, signs = [], [], [], [], []
    heights = None
    layer_warned = False
    i = 1
    while i < len(lines):
        line = lines[i]
        i += 1
        stripped = line.strip()
        if not stripped:
            continue
        parts = stripped.split()
        key = parts[0]
        if key == 'BOARD':
            _paint_board(board, parts, warnings)
            if len(parts) >= 5 and parts[4] != '0' and not layer_warned:
                warnings.append(
                    'BOARD layer is not stored; lines were painted on the single 64 by 64 board'
                )
                layer_warned = True
        elif key == 'LINK':
            link = _parse_nw_link(parts, warnings)
            if link is not None:
                links.append(link)
        elif key == 'SIGN':
            body, i = _block(lines, i, 'SIGNEND')
            if len(parts) < 3:
                warnings.append('SIGN line has no position and was skipped')
                continue
            signs.append(Sign(parts[1], parts[2], '\n'.join(body)))
        elif key == 'NPC':
            body, i = _block(lines, i, 'NPCEND')
            if len(parts) < 4:
                warnings.append('NPC line is short and was skipped')
                continue
            image = '' if parts[1] == '-' else parts[1]
            npcs.append(Npc(image, parts[2], parts[3], '\n'.join(body)))
        elif key == 'BADDY':
            body, i = _block(lines, i, 'BADDYEND')
            if len(parts) < 4:
                warnings.append('BADDY line is short and was skipped')
                continue
            if len(body) > 3:
                warnings.append(
                    f'baddy at {parts[1]},{parts[2]} keeps three verses; '
                    f'{len(body) - 3} extra line(s) were dropped'
                )
                body = body[:3]
            baddies.append(Baddy(parts[1], parts[2], parts[3], _clean_verses(body)))
        elif key == 'CHEST':
            if len(parts) < 5:
                warnings.append('CHEST line is short and was skipped')
                continue
            chests.append(Chest(parts[1], parts[2], _chest_name(parts[3]), parts[4]))
        elif key == 'HEIGHTS':
            heights, i = _heights(lines, i, warnings)
        else:
            warnings.append(f'unknown GLEVNW01 line {key!r} was skipped')
    return Level(board, links, baddies, npcs, chests, signs, heights)


def dumps_level(level, kind, warnings=None):
    """Serialize `level` as zelda, graal, or nw. Dropped fields are named in `warnings`."""
    if warnings is None:
        warnings = []
    if kind == 'nw':
        return _dumps_nw(level, warnings)
    if kind == 'graal':
        return _dumps_binary(level, zelda=False, warnings=warnings)
    if kind == 'zelda':
        return _dumps_binary(level, zelda=True, warnings=warnings)
    raise ConvertError(f'unknown level kind {kind}')


def encode_board(tiles, bits):
    """Pack 4096 tile ids. 13-bit output is gwebl.write_board. 12-bit is the same walk."""
    tiles = list(tiles)
    if len(tiles) != TILES:
        raise ConvertError('board is not 64 by 64')
    for tile in tiles:
        if not isinstance(tile, int) or isinstance(tile, bool) or not 0 <= tile <= 4095:
            raise ConvertError('tile id is outside 0..4095')
    if bits == 13:
        return _gwebl().write_board(tiles)
    if bits != 12:
        raise ConvertError('code width must be 12 or 13')
    return _pack(_rle([tile & 0x7FF for tile in tiles], 12), 12)


def rle_codes(tiles, bits):
    """Run codes for tests. Production GR-V1.03 bytes come from gwebl.write_board."""
    return _rle(list(tiles), bits)


def expand_sign_text(text):
    """Turn `#K(n)` into the character sign-text.md describes. grv1 already drops `#K(13)`."""
    def repl(match):
        value = int(match.group(1))
        if value == 13:
            return ''
        if value > 255:
            return match.group(0)
        return chr(value)
    return _ESCAPE.sub(repl, text)


def encode_sign_text(text):
    """Inverse of grv1.decode_sign plus the `#K(n)` escape, for one sign body."""
    char_code, glyphs = _sign_tables()
    codes = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == '\r':
            i += 1
            continue
        if ch == '\n':
            _emit_escape(codes, char_code, 13)
            codes.append(char_code['\n'])
            i += 1
            continue
        if ch == '#':
            name = text[i:i + 2]
            if name in glyphs:
                codes.extend(glyphs[name])
                i += 2
                continue
            codes.append(char_code['#'])
            i += 1
            continue
        if ch in char_code:
            codes.append(char_code[ch])
            i += 1
            continue
        value = ord(ch)
        if value > 255:
            raise ConvertError('sign text has a character outside latin-1')
        _emit_escape(codes, char_code, value)
        i += 1
    return bytes(code + 32 for code in codes)


def _dumps_nw(level, warnings):
    lines = ['GLEVNW01']
    for y in range(BOARD):
        row = level.board[y * BOARD:(y + 1) * BOARD]
        lines.append(f'BOARD 0 {y} 64 0 {_b64_row(row)}')
    if level.heights is not None:
        lines.append('HEIGHTS')
        for row in level.heights:
            lines.append(','.join(row))
        lines.append('HEIGHTSEND')
    for link in level.links:
        written = _format_nw_link(link, warnings)
        if written is not None:
            lines.append(written)
    for sign in level.signs:
        lines.append(f'SIGN {sign.x} {sign.y}')
        if sign.text:
            lines.extend(sign.text.split('\n'))
        lines.append('SIGNEND')
    for chest in level.chests:
        lines.append(f'CHEST {chest.x} {chest.y} {chest.item} {chest.sign}')
    for baddy in level.baddies:
        lines.append(f'BADDY {baddy.x} {baddy.y} {baddy.type_text}')
        verses = (list(baddy.verses) + ['', '', ''])[:3]
        lines.extend(verses)
        lines.append('BADDYEND')
    for npc in level.npcs:
        image = npc.image or '-'
        lines.append(f'NPC {image} {npc.x} {npc.y}')
        if npc.script:
            lines.extend(npc.script.split('\n'))
        lines.append('NPCEND')
    try:
        return ('\n'.join(lines) + '\n').encode('latin-1')
    except UnicodeEncodeError as exc:
        raise ConvertError('level text is not latin-1') from exc


def _dumps_binary(level, zelda, warnings):
    high = sum(1 for tile in level.board if tile > 2047)
    if zelda:
        out = bytearray(b'Z3-V1.04')
        out += encode_board(level.board, 12)
        if high:
            warnings.append(
                f'{high} tile(s) are above 2047; Z3-V1 codes are 12-bit and '
                'those tiles were stored as the low 11 bits'
            )
        if level.npcs:
            warnings.append(
                f'.zelda (Z3-V1) has no NPC section; '
                f'{_count(len(level.npcs), "NPC")} not written'
            )
        if level.chests:
            warnings.append(
                f'.zelda (Z3-V1) has no chest section; '
                f'{_count(len(level.chests), "chest")} not written'
            )
    else:
        out = bytearray(b'GR-V1.03')
        out += encode_board(level.board, 13)
    if level.heights is not None:
        who = 'Z3-V1' if zelda else 'GR-V1.03'
        warnings.append(
            f'{who} has no HEIGHTS block (GR-V1.04 would, and this tool does not write it); '
            'the overlay was not written'
        )
    for link in level.links:
        raw = _format_bin_link(link, warnings)
        if raw is not None:
            out += raw
    out += b'#\n'
    for baddy in level.baddies:
        raw = _format_baddy(baddy, warnings)
        if raw is not None:
            out += raw
    out += b'\xff\xff\xff\n'
    if not zelda:
        out += _format_npcs(level.npcs, warnings)
        out += _format_chests(level.chests, warnings)
    for sign in level.signs:
        raw = _format_sign(sign, warnings)
        if raw is not None:
            out += raw
    return bytes(out)


def _format_nw_link(link, warnings):
    if any(ch.isspace() for ch in link.dest):
        warnings.append(
            f'link destination {link.dest!r} contains spaces; GLEVNW01 keeps one '
            'token, so the link was not written'
        )
        return None
    fields = [link.dest, link.x, link.y, link.w, link.h, link.newx, link.newy]
    if any(field == '' or any(ch.isspace() for ch in field) for field in fields):
        warnings.append(f'link to {link.dest!r} has an empty field and was not written')
        return None
    return 'LINK ' + ' '.join(fields)


def _format_bin_link(link, warnings):
    tail = [link.x, link.y, link.w, link.h, link.newx, link.newy]
    if link.dest == '' or any(ch in link.dest for ch in '\r\n'):
        warnings.append('a link with a broken destination was not written')
        return None
    if any(field == '' or any(ch.isspace() for ch in field) for field in tail):
        warnings.append(f'link to {link.dest!r} has an empty field and was not written')
        return None
    try:
        return (link.dest + ' ' + ' '.join(tail)).encode('latin-1') + b'\n'
    except UnicodeEncodeError:
        warnings.append(f'link to {link.dest!r} is not latin-1 and was not written')
        return None


def _format_baddy(baddy, warnings):
    x = _fit_int(baddy.x, 0, 127, warnings, 'baddy x')
    y = _fit_int(baddy.y, 0, 255, warnings, 'baddy y')
    kind = _fit_int(baddy.type_text, 0, 255, warnings, 'baddy type')
    if x is None or y is None or kind is None:
        return None
    verses = (list(baddy.verses) + ['', '', ''])[:3]
    if any('\\' in verse or '\n' in verse or '\r' in verse for verse in verses):
        warnings.append(
            f'baddy at {baddy.x},{baddy.y} has a verse separator in the text and was not written'
        )
        return None
    try:
        body = '\\'.join(verses).encode('latin-1')
    except UnicodeEncodeError:
        warnings.append(f'baddy at {baddy.x},{baddy.y} is not latin-1 and was not written')
        return None
    return bytes((x, y, kind)) + body + b'\n'


def _format_npcs(npcs, warnings):
    out = bytearray()
    for npc in npcs:
        x = _fit_int(npc.x, -32, 223, warnings, 'NPC x')
        y = _fit_int(npc.y, -32, 223, warnings, 'NPC y')
        if x is None or y is None:
            continue
        image = '' if npc.image == '-' else npc.image
        if any(ch.isspace() for ch in image) or '#' in image:
            warnings.append(f'NPC image {image!r} cannot be stored in GR-V1 and was not written')
            continue
        if '\xa7' in npc.script:
            warnings.append(
                'an NPC script contains the binary newline byte; it will be read back as a line break'
            )
        try:
            body = npc.script.replace('\n', '\xa7').encode('latin-1')
            image_b = image.encode('latin-1')
        except UnicodeEncodeError:
            warnings.append('an NPC is not latin-1 and was not written')
            continue
        out += bytes((x + 32, y + 32)) + image_b + b'#' + body + b'\n'
    out += b'#\n'
    return bytes(out)


def _format_chests(chests, warnings):
    out = bytearray()
    for chest in chests:
        x = _fit_int(chest.x, -32, 223, warnings, 'chest x')
        y = _fit_int(chest.y, -32, 223, warnings, 'chest y')
        sign = _fit_int(chest.sign, -32, 223, warnings, 'chest sign')
        item = _chest_index(chest.item, warnings)
        if None in (x, y, sign, item):
            continue
        out += bytes((x + 32, y + 32, item + 32, sign + 32)) + b'\n'
    out += b'#\n'
    return bytes(out)


def _format_sign(sign, warnings):
    x = _fit_int(sign.x, -32, 223, warnings, 'sign x')
    y = _fit_int(sign.y, -32, 223, warnings, 'sign y')
    if x is None or y is None:
        return None
    try:
        payload = encode_sign_text(sign.text)
    except ConvertError as exc:
        warnings.append(f'sign at {sign.x},{sign.y} was not written ({exc})')
        return None
    return bytes((x + 32, y + 32)) + payload + b'\n'


def _chest_name(token):
    if token in CHEST_ITEMS:
        return token
    if _INT.fullmatch(token):
        value = int(token, 10)
        if 0 <= value < len(CHEST_ITEMS):
            return CHEST_ITEMS[value]
    return token


def _chest_index(item, warnings):
    if item in CHEST_ITEMS:
        return CHEST_ITEMS.index(item)
    if _INT.fullmatch(item.strip()):
        value = int(item, 10)
        if 0 <= value <= 223:
            return value
    warnings.append(f'chest item {item!r} is not a known name or index and was not written')
    return None


def _fit_int(token, lo, hi, warnings, label):
    text = token.strip()
    try:
        if _INT.fullmatch(text):
            value = int(text, 10)
            fraction = False
        else:
            number = float(text)
            value = int(number)
            fraction = True
    except (ValueError, OverflowError):
        warnings.append(f'{label} {token!r} is not a number and was not written')
        return None
    if fraction and value != float(text):
        warnings.append(f'{label} {token} is not a whole tile; the binary field stores {value}')
    elif fraction and text != str(value):
        warnings.append(f'{label} {token} was stored as {value}')
    if not lo <= value <= hi:
        warnings.append(f'{label} {value} does not fit this field and was not written')
        return None
    return value


def _paint_board(board, parts, warnings):
    # BOARD x y width layer tiles. Ignored unless it is a full in-range run.
    if len(parts) != 6:
        warnings.append('BOARD line ignored (it does not have 6 tokens)')
        return
    try:
        x, y, width = int(parts[1]), int(parts[2]), int(parts[3])
    except ValueError:
        warnings.append('BOARD line ignored (x, y or width is not an integer)')
        return
    data = parts[5]
    if not (0 <= x <= 63 and 0 <= y <= 63 and width >= 1 and x + width <= 64):
        warnings.append('BOARD line ignored (it does not stay inside the 64 by 64 board)')
        return
    if len(data) < width * 2:
        warnings.append('BOARD line ignored (the tile text is shorter than the width)')
        return
    for offset in range(width):
        pair = data[offset * 2:offset * 2 + 2]
        hi = B64.find(pair[0])
        lo = B64.find(pair[1])
        if hi < 0 or lo < 0:
            break
        board[y * BOARD + x + offset] = (hi << 6) | lo


def _parse_nw_link(parts, warnings):
    # 2.22: at least dest and four numbers. Missing arrivals become playerx/playery.
    if len(parts) < 6:
        warnings.append('LINK line is short and was skipped')
        return None
    dest, x, y, w, h = parts[1:6]
    newx = parts[6] if len(parts) >= 7 and parts[6] else 'playerx'
    newy = parts[7] if len(parts) >= 8 and parts[7] else 'playery'
    if len(parts) > 8:
        warnings.append(
            f'LINK destination {dest!r} was kept as one token; extra tokens were not part of the name'
        )
    return Link(dest, x, y, w, h, newx, newy)


def _block(lines, i, end):
    body = []
    while i < len(lines):
        if lines[i].strip() == end:
            return body, i + 1
        body.append(lines[i])
        i += 1
    raise Truncated(f'{end} missing')


def _height_token(value):
    number = float(value)
    if number == int(number) and abs(number) < 1e15:
        return str(int(number))
    return format(number, '.12g')


def _heights_from_grv(rows):
    """Same 9×9 string grid the text loader keeps. Short rows are filled with 0."""
    if rows is None:
        return None
    out = []
    for row in rows[:9]:
        cells = [_height_token(value) for value in row[:9]]
        while len(cells) < 9:
            cells.append('0')
        out.append(cells)
    while len(out) < 9:
        out.append(['0'] * 9)
    return out


def _heights(lines, i, warnings):
    rows = []
    closed = False
    while i < len(lines):
        if lines[i].strip() == 'HEIGHTSEND':
            closed = True
            i += 1
            break
        text = lines[i].strip()
        i += 1
        if not text:
            continue
        nums = [part.strip() for part in text.split(',') if part.strip()]
        if len(nums) > 9:
            warnings.append('a HEIGHTS row had more than 9 values; the rest were dropped')
            nums = nums[:9]
        while len(nums) < 9:
            nums.append('0')
        if len(rows) < 9:
            rows.append(nums)
        else:
            warnings.append('HEIGHTS had more than 9 rows; the rest were dropped')
    if not closed:
        raise Truncated('HEIGHTSEND missing')
    if len(rows) < 9:
        warnings.append('HEIGHTS had fewer than 9 rows; the rest were filled with 0')
        while len(rows) < 9:
            rows.append(['0'] * 9)
    return rows, i


def _b64_row(tiles):
    out = []
    for tile in tiles:
        if not 0 <= tile <= 4095:
            raise ConvertError('tile id is outside 0..4095')
        out.append(B64[tile >> 6])
        out.append(B64[tile & 63])
    return ''.join(out)


def _rle(tiles, bits):
    """Same cases as gwebl.write_board: single run, double run, or one tile."""
    flag = 1 << (bits - 1)
    mask = flag - 1
    codes = []
    i = 0
    limit = len(tiles)
    while i < limit:
        tile = tiles[i]
        if i < limit - 3 and tiles[i + 1] == tile:
            count = 2
            i += 2
            while count < 64 and i < limit and tiles[i] == tile:
                count += 1
                i += 1
            codes.append(flag | count)
            codes.append(tile & mask)
        elif (
            i < limit - 3
            and tiles[i + 2] == tile
            and tiles[i + 1] == tiles[i + 3]
        ):
            other = tiles[i + 1]
            count = 2
            i += 4
            while count < 64 and i < limit - 1 and tiles[i] == tile and tiles[i + 1] == other:
                count += 1
                i += 2
            codes.append(flag | 0x100 | count)
            codes.append(tile & mask)
            codes.append(other & mask)
        else:
            codes.append(tile & mask)
            i += 1
    return codes


def _pack(codes, bits):
    out = bytearray()
    acc = 0
    nacc = 0
    mask = (1 << bits) - 1
    for code in codes:
        acc |= (code & mask) << nacc
        nacc += bits
        while nacc >= 8:
            out.append(acc & 0xFF)
            acc >>= 8
            nacc -= 8
    if nacc:
        out.append(acc & 0xFF)
    return bytes(out)


def _sign_tables():
    global _sign_cache
    if _sign_cache is None:
        mod = _grv1()
        char_code = {}
        for index, ch in enumerate(mod.ALPHABET):
            if ch == '#':
                continue
            char_code.setdefault(ch, index)
        char_code['#'] = 86
        glyphs = {name: (code,) for code, name in mod.GLYPHS.items()}
        for pair, name in mod.GLYPHS2.items():
            glyphs[name] = tuple(pair)
        _sign_cache = (char_code, glyphs)
    return _sign_cache


def _emit_escape(codes, char_code, value):
    codes.append(char_code['#'])
    codes.append(char_code['K'])
    codes.append(char_code['('])
    for digit in str(value):
        codes.append(char_code[digit])
    codes.append(char_code[')'])


def _clean_verses(verses):
    """Drop the empty padding the writer adds so three blank lines are no verses."""
    cleaned = list(verses)
    while cleaned and cleaned[-1] == '':
        cleaned.pop()
    return cleaned


def _count(n, word):
    if n == 1:
        return f'1 {word} was'
    return f'{n} {word}s were'
