"""Write the gif2mng frame rule from tools/gif2mng.md.

One indexed frame becomes a PNG. Two or more become an MNG.
`-b` keeps that one palette and forces transparent index 2.
The note does not list the seven body-slot RGB values, so this
writer does not recolour entries and does not add a second palette.

The program's chunk names are MHDR, FRAM, TERM, IHDR, PLTE, tRNS,
IDAT, IEND and MEND. TERM's delay fields are not in the note, so
they are not written. Frame timing is not in the note either:
MHDR ticks and play time are 0, and one FRAM byte of mode 1
("leave framing unchanged") precedes the frames.
"""

import struct
import zlib

PNG_SIG = b'\x89PNG\r\n\x1a\n'
MNG_SIG = b'\x8aMNG\r\n\x1a\n'


def convert(frames, body_slots=False):
    """`frames` are dicts: width, height, palette [(r,g,b)...], pixels [index...].

    Optional `transparent` is a palette index. With body_slots it is index 2.
    """
    if not frames:
        raise ValueError('no frames')
    prepared = [_prepare(frame, body_slots) for frame in frames]
    if len(prepared) == 1:
        return png_bytes(prepared[0])
    width, height = prepared[0]['width'], prepared[0]['height']
    for frame in prepared[1:]:
        if frame['width'] != width or frame['height'] != height:
            raise ValueError('frames differ in size; the note does not say how')
    return mng_bytes(prepared)


def png_bytes(frame):
    chunks = [_ihdr(frame), _plte(frame)]
    trns = _trns(frame)
    if trns is not None:
        chunks.append(trns)
    chunks.append(_idat(frame))
    chunks.append(_chunk(b'IEND', b''))
    return PNG_SIG + b''.join(chunks)


def mng_bytes(frames):
    first = frames[0]
    mhdr = struct.pack(
        '>IIIIIII',
        first['width'],
        first['height'],
        0,
        1,
        len(frames),
        0,
        0,
    )
    parts = [MNG_SIG, _chunk(b'MHDR', mhdr), _chunk(b'FRAM', b'\x01')]
    for frame in frames:
        parts.append(png_bytes(frame)[len(PNG_SIG):])
    parts.append(_chunk(b'MEND', b''))
    return b''.join(parts)


def _prepare(frame, body_slots):
    width = frame['width']
    height = frame['height']
    palette = [tuple(colour) for colour in frame['palette']]
    pixels = list(frame['pixels'])
    if width < 1 or height < 1:
        raise ValueError('frame size must be at least 1')
    if len(pixels) != width * height:
        raise ValueError('pixel count does not match the frame size')
    if not palette or len(palette) > 256:
        raise ValueError('palette must hold 1 to 256 colours')
    for colour in palette:
        if len(colour) != 3 or any(not 0 <= channel <= 255 for channel in colour):
            raise ValueError('palette entry is not an RGB triple')
    if any(not 0 <= pixel < len(palette) for pixel in pixels):
        raise ValueError('pixel index is outside the palette')
    transparent = frame.get('transparent')
    if body_slots:
        if len(palette) < 3:
            raise ValueError('index 2 needs a palette of at least 3; none is added')
        transparent = 2
    if transparent is not None and not 0 <= transparent < len(palette):
        raise ValueError('transparent index is outside the palette')
    return {
        'width': width,
        'height': height,
        'palette': palette,
        'pixels': pixels,
        'transparent': transparent,
    }


def _ihdr(frame):
    data = struct.pack('>IIBBBBB', frame['width'], frame['height'], 8, 3, 0, 0, 0)
    return _chunk(b'IHDR', data)


def _plte(frame):
    data = b''.join(bytes(colour) for colour in frame['palette'])
    return _chunk(b'PLTE', data)


def _trns(frame):
    index = frame['transparent']
    if index is None:
        return None
    alphas = bytearray([255]) * (index + 1)
    alphas[index] = 0
    return _chunk(b'tRNS', bytes(alphas))


def _idat(frame):
    width = frame['width']
    rows = []
    pixels = frame['pixels']
    for y in range(frame['height']):
        rows.append(b'\x00' + bytes(pixels[y * width:(y + 1) * width]))
    return _chunk(b'IDAT', zlib.compress(b''.join(rows)))


def _chunk(tag, data):
    crc = zlib.crc32(tag + data) & 0xFFFFFFFF
    return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', crc)
