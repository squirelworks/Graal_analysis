"""Synthetic frames and boards. No generator executable and no Drive image."""

import struct
import sys
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'formats' / 'grv1-decoder'))

import gif2mng  # noqa: E402
import grv1  # noqa: E402
import txtlevel  # noqa: E402


def test_graal_txt_and_nw_txt_names():
    assert txtlevel.level_name('world_', 0, 0, 2, 1, 'graal') == 'world_a-1.graal'
    assert txtlevel.level_name('world_', 1, 0, 2, 1, 'graal') == 'world_b-1.graal'
    assert txtlevel.level_name('world_', 0, 0, 2, 10, 'graal') == 'world_a-01.graal'
    assert txtlevel.level_name('world_', 0, 4, 2, 100, 'graal') == 'world_a-005.graal'
    assert txtlevel.level_name('world_', 0, 0, 26, 1, 'graal') == 'world_aa-1.graal'
    assert txtlevel.level_name('world_', 26, 0, 27, 1, 'graal') == 'world_ba-1.graal'
    assert txtlevel.level_name('world_', 0, 0, 2, 1, 'nw') == 'world_a1.nw'
    assert txtlevel.level_name('world_', 0, 0, 2, 10, 'nw') == 'world_a01.nw'


def test_bigmap_and_level_bodies():
    files = txtlevel.write_world('cave_', 2, 1, 'graal', {(1, 0): [7] * 4096})
    assert files['bigmap.txt'] == b'"cave_a-1.graal","cave_b-1.graal"\n'
    empty = grv1.load(files['cave_a-1.graal'])
    assert empty['magic'] == 'GR-V1.03'
    assert empty['board'] == [0] * 4096
    assert empty['links'] == [] and empty['npcs'] == []
    painted = grv1.load(files['cave_b-1.graal'])
    assert painted['board'] == [7] * 4096

    nw = txtlevel.write_world('cave_', 1, 1, 'nw', {(0, 0): [1] + [0] * 4095})
    text = nw['cave_a1.nw'].decode('ascii')
    assert text.startswith('GLEVNW01\nBOARD 0 0 64 0 AB')
    assert 'LINK ' not in text
    assert nw['bigmap.txt'] == b'"cave_a1.nw"\n'


def _chunks(blob, signature):
    assert blob.startswith(signature)
    pos = len(signature)
    found = []
    while pos < len(blob):
        length = struct.unpack_from('>I', blob, pos)[0]
        tag = blob[pos + 4:pos + 8]
        data = blob[pos + 8:pos + 8 + length]
        crc = struct.unpack_from('>I', blob, pos + 8 + length)[0]
        assert zlib.crc32(tag + data) & 0xFFFFFFFF == crc
        found.append((tag, data))
        pos += 12 + length
    return found


def _png_pixels(blob):
    chunks = _chunks(blob, gif2mng.PNG_SIG)
    tags = [tag for tag, _ in chunks]
    assert tags[0] == b'IHDR' and b'IEND' in tags and tags.count(b'PLTE') == 1
    width, height, depth, colour, comp, filt, inter = struct.unpack(
        '>IIBBBBB', chunks[0][1])
    assert (depth, colour, comp, filt, inter) == (8, 3, 0, 0, 0)
    raw = zlib.decompress(b''.join(data for tag, data in chunks if tag == b'IDAT'))
    pixels = []
    stride = width + 1
    for y in range(height):
        row = raw[y * stride:(y + 1) * stride]
        assert row[0] == 0
        pixels.extend(row[1:])
    palette = chunks[tags.index(b'PLTE')][1]
    trns = next((data for tag, data in chunks if tag == b'tRNS'), None)
    return width, height, palette, trns, pixels


def test_one_frame_is_png_and_many_are_mng():
    palette = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12)]
    frame = {'width': 2, 'height': 2, 'palette': palette, 'pixels': [0, 1, 2, 3]}
    png = gif2mng.convert([frame])
    width, height, stored, trns, pixels = _png_pixels(png)
    assert (width, height, pixels) == (2, 2, [0, 1, 2, 3])
    assert stored == b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c'
    assert trns is None

    mng = gif2mng.convert([frame, dict(frame, pixels=[3, 2, 1, 0])])
    chunks = _chunks(mng, gif2mng.MNG_SIG)
    tags = [tag for tag, _ in chunks]
    assert tags[0] == b'MHDR'
    assert b'FRAM' in tags and b'TERM' not in tags and tags[-1] == b'MEND'
    assert tags.count(b'IHDR') == 2
    assert tags.count(b'PLTE') == 2
    assert tags.count(b'IEND') == 2
    mhdr = chunks[0][1]
    assert struct.unpack('>IIIIIII', mhdr)[:3] == (2, 2, 0)


def test_body_slots_force_index_2_and_keep_the_palette():
    palette = [(9, 9, 9), (8, 8, 8), (7, 7, 7), (6, 6, 6)]
    frame = {
        'width': 1,
        'height': 1,
        'palette': palette,
        'pixels': [2],
        'transparent': 0,
    }
    png = gif2mng.convert([frame], body_slots=True)
    _, _, stored, trns, pixels = _png_pixels(png)
    assert pixels == [2]
    assert stored == b'\x09\x09\x09\x08\x08\x08\x07\x07\x07\x06\x06\x06'
    assert trns == b'\xff\xff\x00'
    try:
        gif2mng.convert([{
            'width': 1, 'height': 1, 'palette': [(0, 0, 0)], 'pixels': [0],
        }], body_slots=True)
    except ValueError as exc:
        assert 'at least 3' in str(exc)
    else:
        raise AssertionError('short palette')
