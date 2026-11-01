"""Synthetic levels only. No client programs, no network, no copyrighted boards."""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import convert  # noqa: E402
import gmapio  # noqa: E402
import levelio  # noqa: E402
import package  # noqa: E402
from errors import Truncated  # noqa: E402

CONVERT = Path(__file__).resolve().parent / 'convert.py'
ROOT = Path(__file__).resolve().parents[2]


def run(src, dst):
    return subprocess.run(
        [sys.executable, str(CONVERT), str(src), str(dst)],
        capture_output=True,
        text=True,
        check=False,
    )


def board_with(*pairs):
    board = [0] * levelio.TILES
    for index, tile in pairs:
        board[index] = tile
    for x in range(64):
        board[x] = 1
    for index in range(100, 150):
        board[index] = 9
    for index in range(200, 216, 2):
        board[index] = 3
        board[index + 1] = 4
    board[64 * 10 + 5] = 42
    board[64 * 63 + 63] = 2047
    return board


def links():
    return [
        levelio.Link('next.nw', '63', '0', '1', '64', '0', 'playery'),
        levelio.Link('cave.zelda', '10', '10', '2.0', '1.0', 'playerx', 'playery+10'),
        levelio.Link('house.graal', '31.0', '42.0', '2.0', '1.0', '43.5', '41.0'),
    ]


def base_level():
    return levelio.Level(
        board_with(),
        links(),
        [levelio.Baddy('4', '8', '1', ['Stop!', 'Ouch!', 'Hey!'])],
        [],
        [],
        [levelio.Sign('2', '3', 'Hello\nWorld #A')],
        None,
    )


def rich_level():
    level = base_level()
    level.board[400] = 4095
    level.npcs = [
        levelio.Npc('', '6', '7', 'if (playerenters) {\n  say 0;\n}'),
        levelio.Npc('hero.gif', '8', '9', '// wave'),
    ]
    level.chests = [
        levelio.Chest('12', '14', 'greenrupee', '-1'),
        levelio.Chest('15', '16', 'fullheart', '0'),
    ]
    return level


def same_core(left, right):
    assert left.board == right.board
    assert [(L.dest, L.x, L.y, L.w, L.h, L.newx, L.newy) for L in left.links] == [
        (L.dest, L.x, L.y, L.w, L.h, L.newx, L.newy) for L in right.links
    ]
    assert [(b.x, b.y, b.type_text, b.verses) for b in left.baddies] == [
        (b.x, b.y, b.type_text, b.verses) for b in right.baddies
    ]
    assert [(s.x, s.y, s.text) for s in left.signs] == [
        (s.x, s.y, s.text) for s in right.signs
    ]


def test_sign_text_round_trip_uses_grv1():
    grv1 = levelio._grv1()
    for text in ('Hello', 'Hello\nWorld', '#A #.', '#h#4', 'Say "hi";', ' ', '\u00e9'):
        payload = levelio.encode_sign_text(text)
        got = levelio.expand_sign_text(grv1.decode_sign(payload))
        assert got == text


def test_graal_board_writer_is_gwebl():
    tiles = board_with()
    tiles[400] = 4095
    gwebl = levelio._gwebl()
    assert levelio.encode_board(tiles, 13) == gwebl.write_board(tiles)
    assert levelio._pack(levelio.rle_codes(tiles, 13), 13) == gwebl.write_board(tiles)


def test_twelve_bit_board_round_trip_and_gr_v1_00():
    tiles = board_with()
    data = b'GR-V1.00' + levelio.encode_board(tiles, 12) + b'#\n\xff\xff\xff\n'
    loaded = levelio.loads_binary(data)
    assert loaded.board == tiles
    assert loaded.npcs == []
    assert loaded.chests == []


def test_zelda_graal_nw_round_trip_keeps_board_and_links():
    level = base_level()
    warnings = []
    zelda = levelio.dumps_level(level, 'zelda', warnings)
    assert warnings == []
    assert zelda.startswith(b'Z3-V1.04')
    assert b'if (playerenters)' not in zelda
    current = levelio.loads_binary(zelda)
    same_core(current, level)
    assert current.npcs == [] and current.chests == []
    for kind in ('graal', 'nw', 'graal', 'zelda'):
        blob = levelio.dumps_level(current, kind, [])
        current = levelio.loads_nw(blob, []) if kind == 'nw' else levelio.loads_binary(blob)
    same_core(current, level)


def test_graal_nw_keeps_npcs_chests_and_signs():
    level = rich_level()
    warnings = []
    graal = levelio.dumps_level(level, 'graal', warnings)
    assert warnings == []
    assert graal.startswith(b'GR-V1.03')
    again = levelio.loads_binary(graal)
    same_core(again, level)
    assert [(n.image, n.x, n.y, n.script) for n in again.npcs] == [
        (n.image, n.x, n.y, n.script) for n in level.npcs
    ]
    assert [(c.x, c.y, c.item, c.sign) for c in again.chests] == [
        (c.x, c.y, c.item, c.sign) for c in level.chests
    ]
    nw = levelio.dumps_level(again, 'nw', [])
    text = nw.decode('latin-1')
    assert text.startswith('GLEVNW01\n')
    assert 'NPC - 6 7\n' in text
    assert 'NPC hero.gif 8 9\n' in text
    assert 'CHEST 12 14 greenrupee -1\n' in text
    back = levelio.loads_binary(levelio.dumps_level(levelio.loads_nw(nw, []), 'graal', []))
    same_core(back, level)
    assert back.npcs[1].script == '// wave'
    assert back.chests[0].item == 'greenrupee'
    assert back.chests[0].sign == '-1'


def test_zelda_says_it_has_no_npc_or_chest_section():
    level = base_level()
    rich = rich_level()
    level.npcs = rich.npcs
    level.chests = rich.chests
    warnings = []
    blob = levelio.dumps_level(level, 'zelda', warnings)
    assert any('no NPC section' in w for w in warnings)
    assert any('no chest section' in w for w in warnings)
    loaded = levelio.loads_binary(blob)
    assert loaded.npcs == [] and loaded.chests == []
    assert b'hero.gif' not in blob
    assert b'if (playerenters)' not in blob
    same_core(loaded, base_level())


def test_high_tiles_do_not_fit_in_zelda():
    level = base_level()
    level.board[500] = 3000
    warnings = []
    blob = levelio.dumps_level(level, 'zelda', warnings)
    assert any('12-bit' in w for w in warnings)
    loaded = levelio.loads_binary(blob)
    assert loaded.board[500] == (3000 & 0x7FF)
    assert loaded.board[64 * 10 + 5] == 42
    nw_warnings = []
    nw = levelio.loads_nw(levelio.dumps_level(level, 'nw', nw_warnings), [])
    assert nw_warnings == []
    assert nw.board[500] == 3000


def test_heights_stay_on_nw_and_are_named_when_dropped():
    level = base_level()
    level.heights = [['0'] * 9 for _ in range(9)]
    level.heights[0][0] = '3'
    level.heights[8][8] = '1.5'
    warnings = []
    nw = levelio.dumps_level(level, 'nw', warnings)
    assert warnings == []
    loaded = levelio.loads_nw(nw, [])
    assert loaded.heights == level.heights
    warnings = []
    levelio.dumps_level(loaded, 'graal', warnings)
    assert any('HEIGHTS' in w for w in warnings)


def test_fractional_npc_is_kept_in_nw_and_cut_for_graal():
    level = base_level()
    level.npcs = [levelio.Npc('a.gif', '10.5', '4', 'x')]
    assert levelio.loads_nw(levelio.dumps_level(level, 'nw', []), []).npcs[0].x == '10.5'
    warnings = []
    graal = levelio.dumps_level(level, 'graal', warnings)
    assert any('10.5' in w for w in warnings)
    assert levelio.loads_binary(graal).npcs[0].x == '10'


def test_spaced_link_destination_is_not_written_to_nw():
    level = base_level()
    level.links.append(levelio.Link('my town.nw', '0', '0', '1', '1', '1', '1'))
    warnings = []
    graal = levelio.dumps_level(level, 'graal', warnings)
    assert warnings == []
    assert levelio.loads_binary(graal).links[-1].dest == 'my town.nw'
    warnings = []
    nw = levelio.dumps_level(level, 'nw', warnings)
    assert any('spaces' in w for w in warnings)
    assert all(link.dest != 'my town.nw' for link in levelio.loads_nw(nw, []).links)
    assert len(levelio.loads_nw(nw, []).links) == 3


def test_named_baddy_type_is_not_invented_as_a_byte():
    level = base_level()
    level.baddies = [levelio.Baddy('1', '2', 'graysoldier', ['Hi'])]
    warnings = []
    levelio.dumps_level(level, 'graal', warnings)
    assert any('baddy type' in w for w in warnings)
    text = levelio.dumps_level(level, 'nw', []).decode('latin-1')
    assert 'BADDY 1 2 graysoldier\n' in text


def test_magic_wins_over_a_misleading_suffix(tmp_path):
    level = rich_level()
    path = tmp_path / 'misnamed.zelda'
    path.write_bytes(levelio.dumps_level(level, 'graal', []))
    warnings = []
    loaded = levelio.load_path(path, warnings)
    assert loaded.npcs and any('magic' in w for w in warnings)


def test_gmap_round_trip_from_grid(tmp_path):
    folder = tmp_path / 'levels'
    folder.mkdir()
    level = base_level()
    for name in ('west.nw', 'east.nw', 'south.nw'):
        (folder / name).write_bytes(levelio.dumps_level(level, 'nw', []))
    (folder / 'grid.txt').write_text(
        'WIDTH 2\nHEIGHT 2\n0 0 west.nw\n1 0 east.nw\n0 1 south.nw\n',
        encoding='latin-1',
    )
    gmap_path = tmp_path / 'world.gmap'
    warnings = convert.convert(folder, gmap_path)
    assert warnings == []
    gmap = gmapio.loads(gmap_path.read_bytes())
    assert (gmap.width, gmap.height) == (2, 2)
    assert gmap.names == [['west.nw', 'east.nw'], ['south.nw', '']]
    back = tmp_path / 'back'
    assert run(gmap_path, back).returncode == 0
    grid_text = (back / 'grid.txt').read_text(encoding='latin-1')
    assert '0 0 west.nw' in grid_text
    assert '1 1' not in grid_text
    for name in ('west.nw', 'east.nw', 'south.nw'):
        (back / name).write_bytes((folder / name).read_bytes())
    again = gmapio.load_directory(back, [])
    assert again.names == gmap.names


def test_gmap_from_levelgen_names_and_package(tmp_path):
    folder = tmp_path / 'world'
    folder.mkdir()
    blob = levelio.dumps_level(base_level(), 'nw', [])
    (folder / 'lab_a-01.nw').write_bytes(blob)
    (folder / 'lab_b-01.nw').write_bytes(blob)
    (folder / 'lab_a-02.nw').write_bytes(blob)
    gmap_path = tmp_path / 'lab.gmap'
    assert convert.convert(folder, gmap_path) == []
    gmap = gmapio.loads(gmap_path.read_bytes())
    assert gmap.names == [['lab_a-01.nw', 'lab_b-01.nw'], ['lab_a-02.nw', '']]
    packed = tmp_path / 'lab.seihai'
    assert run(gmap_path, packed).returncode == 0
    kind, payload = package.loads(packed.read_bytes())
    assert kind == 'gmap' and payload == gmap_path.read_bytes()
    out = tmp_path / 'unpacked.gmap'
    assert run(packed, out).returncode == 0
    assert out.read_bytes() == gmap_path.read_bytes()


def test_seihai_level_package_is_the_nw_bytes(tmp_path):
    level = rich_level()
    nw = tmp_path / 'room.nw'
    nw.write_bytes(levelio.dumps_level(level, 'nw', []))
    packed = tmp_path / 'room.seihai'
    assert convert.convert(nw, packed) == []
    kind, payload = package.loads(packed.read_bytes())
    assert kind == 'nw' and payload == nw.read_bytes()
    back = tmp_path / 'back.nw'
    assert run(packed, back).returncode == 0
    assert back.read_bytes() == nw.read_bytes()
    graal = tmp_path / 'back.graal'
    assert run(packed, graal).returncode == 0
    same_core(levelio.loads_binary(graal.read_bytes()), level)


def test_reader_keys_survive_a_gmap_rewrite(tmp_path):
    text = (
        'GRMAP001\n'
        'WIDTH 1\n'
        'HEIGHT 1\n'
        'GENERATED 1\n'
        'LEVELNAMES\n'
        '"only.nw"\n'
        'LEVELNAMESEND\n'
        'MAPIMG overview.png\n'
        'NOAUTOMAPPING\n'
    )
    src = tmp_path / 'in.gmap'
    src.write_bytes(text.encode('latin-1'))
    dst = tmp_path / 'out.gmap'
    assert convert.convert(src, dst) == []
    body = dst.read_text(encoding='latin-1')
    assert 'GENERATED 1' in body
    assert 'MAPIMG overview.png' in body
    assert 'NOAUTOMAPPING' in body
    loaded = gmapio.loads(dst.read_bytes())
    assert loaded.names == [['only.nw']]
    assert loaded.mapimg == 'overview.png'
    assert loaded.no_auto_mapping is True


def test_cli_says_zelda_has_no_npc_section(tmp_path):
    src = tmp_path / 'room.graal'
    src.write_bytes(levelio.dumps_level(rich_level(), 'graal', []))
    result = run(src, tmp_path / 'room.zelda')
    assert result.returncode == 0
    assert 'no NPC section' in result.stderr
    assert 'no chest section' in result.stderr
    loaded = levelio.loads_binary((tmp_path / 'room.zelda').read_bytes())
    assert loaded.npcs == [] and loaded.chests == []


def test_refuses_magics_the_decoder_does_not_read():
    from errors import ConvertError
    for magic, needle in ((b'GR-V1.04', 'GR-V1.04'), (b'Z3-V1.02', '11-bit')):
        try:
            levelio.loads_binary(magic + b'\x00' * 4)
        except ConvertError as exc:
            assert needle in str(exc)
        else:
            raise AssertionError(magic)


def test_gmap_is_not_one_level_renamed(tmp_path):
    nw = tmp_path / 'room.nw'
    nw.write_bytes(levelio.dumps_level(base_level(), 'nw', []))
    result = run(nw, tmp_path / 'room.gmap')
    assert result.returncode == 2
    assert 'directory' in result.stderr
    assert 'not one level renamed' in result.stderr


def test_truncated_files_exit_nonzero(tmp_path):
    short = tmp_path / 'short.graal'
    short.write_bytes(b'GR-V1.03' + b'\x00\x01')
    result = run(short, tmp_path / 'out.nw')
    assert result.returncode == 1
    assert result.stderr.startswith('truncated:')

    cut = tmp_path / 'cut.nw'
    cut.write_bytes(b'GLEVNW01\nSIGN 1 2\nHello\n')
    result = run(cut, tmp_path / 'out.graal')
    assert result.returncode == 1

    gmap = tmp_path / 'cut.gmap'
    gmap.write_bytes(b'GRMAP001\nWIDTH 1\nHEIGHT 1\nLEVELNAMES\n"a.nw"\n')
    result = run(gmap, tmp_path / 'copy.gmap')
    assert result.returncode == 1

    packed = tmp_path / 'cut.seihai'
    packed.write_bytes(b'SEIHAI01\nkind nw\nbytes 40\nGLEVNW01\n')
    result = run(packed, tmp_path / 'out2.nw')
    assert result.returncode == 1

    empty = tmp_path / 'empty.zelda'
    empty.write_bytes(b'')
    assert run(empty, tmp_path / 'out3.nw').returncode == 1


def test_unclosed_heights_is_truncated():
    try:
        levelio.loads_nw(b'GLEVNW01\nHEIGHTS\n0,0,0,0,0,0,0,0,0\n')
    except Truncated as exc:
        assert 'HEIGHTSEND' in str(exc)
    else:
        raise AssertionError('expected Truncated')


def test_cli_chain_from_zelda_through_seihai(tmp_path):
    """The order the owner asked for: zelda, graal, nw, a gmap, a seihai package."""
    level = base_level()
    zelda = tmp_path / 'room.zelda'
    zelda.write_bytes(levelio.dumps_level(level, 'zelda', []))
    graal = tmp_path / 'room.graal'
    nw = tmp_path / 'lab_a-01.nw'
    assert run(zelda, graal).returncode == 0
    assert run(graal, nw).returncode == 0
    same_core(levelio.loads_nw(nw.read_bytes(), []), level)
    other = tmp_path / 'lab_b-01.nw'
    other.write_bytes(nw.read_bytes())
    gmap = tmp_path / 'lab.gmap'
    assert run(tmp_path, gmap).returncode == 2  # tmp_path also holds graal/zelda files that are not levelgen names
    world = tmp_path / 'world'
    world.mkdir()
    nw.replace(world / 'lab_a-01.nw')
    other.replace(world / 'lab_b-01.nw')
    assert run(world, gmap).returncode == 0
    loaded = gmapio.loads(gmap.read_bytes())
    assert loaded.names[0] == ['lab_a-01.nw', 'lab_b-01.nw']
    packed = tmp_path / 'lab.seihai'
    assert run(gmap, packed).returncode == 0
    assert package.loads(packed.read_bytes())[0] == 'gmap'
    note = (ROOT / 'tools' / 'level-convert' / 'SEIHAI-FORMAT.md').read_text(encoding='utf-8')
    assert 'SEIHAI01' in note and '[inf]' in note
