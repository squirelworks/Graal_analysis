#!/usr/bin/env python3
"""Generate the conformance suite's own 3D content (no game content).

Every file the generated worlds name is made here from nothing: plain cubes in
.3ds, solid-colour PNG and GIF textures, and marker files. So the suite needs
no client asset and nothing generated is ever committed.

    python3 tools/conformance/gen_content.py OUTDIR

Files (all under OUTDIR):

    conf_red.3ds       unit cube, one material "conf_red" with a red diffuse colour
    conf_nomat.3ds     the same cube with no material (5.12 and 4.20r6 draw none of it)
    conf_tex.3ds       the cube with UVs and a material whose texture is conf_tex.png
    conf_tex.png       256x256 solid green
    conf_sky0..5.png   sky faces, each its own solid colour (SKY_COLOURS)
    conf_sky0..5.gif   the same as GIF (3.153 asks for sky textures as .gif)
    conf_overlay.png   64x64 solid magenta, for GS2 showimg over the 3D view
    conf_marker.cs     a TorqueScript marker, which no read build should request
    conf_marker.ter    a .ter marker, likewise

Python 3 standard library only.
"""

from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path

RED = (220, 0, 0)
GREEN = (0, 200, 0)
MAGENTA = (255, 0, 255)
# Sky faces in the order the world's sky line names them (face 0 to 5).
SKY_COLOURS = [
    (255, 128, 0),    # 0 orange
    (0, 160, 255),    # 1 sky blue
    (255, 255, 0),    # 2 yellow
    (0, 255, 160),    # 3 mint
    (160, 0, 255),    # 4 violet (up)
    (90, 60, 30),     # 5 brown (down)
]


# ------------------------------------------------------------------ images

def png(width: int, height: int, rgb: tuple[int, int, int]) -> bytes:
    """A solid-colour 24-bit PNG."""
    row = b"\0" + bytes(rgb) * width
    raw = row * height

    def chunk(kind: bytes, body: bytes) -> bytes:
        return (struct.pack(">I", len(body)) + kind + body
                + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def gif(width: int, height: int, rgb: tuple[int, int, int]) -> bytes:
    """A solid-colour GIF87a. The LZW stream sends a clear code before every
    pixel code, so the code size never grows (valid, if not small)."""
    min_code = 2
    clear, end = 1 << min_code, (1 << min_code) + 1
    width_bits = min_code + 1
    codes = []
    for _ in range(width * height):
        codes += [clear, 0]
    codes.append(end)
    bits = 0
    nbits = 0
    data = bytearray()
    for c in codes:
        bits |= c << nbits
        nbits += width_bits
        while nbits >= 8:
            data.append(bits & 0xFF)
            bits >>= 8
            nbits -= 8
    if nbits:
        data.append(bits & 0xFF)
    blocks = bytearray()
    for i in range(0, len(data), 255):
        part = data[i:i + 255]
        blocks += bytes([len(part)]) + part
    blocks += b"\0"
    palette = bytes(rgb) + b"\0\0\0" + b"\0\0\0" * 2  # 4 entries (2 bits)
    head = b"GIF87a" + struct.pack("<HHBBB", width, height, 0x81, 0, 0)
    image = b"," + struct.pack("<HHHHB", 0, 0, width, height, 0)
    return head + palette + image + bytes([min_code]) + bytes(blocks) + b";"


# ------------------------------------------------------------------ .3ds

def _chunk(cid: int, body: bytes) -> bytes:
    return struct.pack("<HI", cid, len(body) + 6) + body


# A unit cube centred on the origin: 8 corners, 12 triangles.
_V = [(-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
      (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5)]
_F = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4),
      (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7)]
_UV = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0), (1, 0), (1, 1), (0, 1)]


def cube_3ds(material: str | None = None, colour=RED, texture: str | None = None) -> bytes:
    """A .3ds unit cube, optionally with one material (diffuse colour and,
    with `texture`, a texture map and UVs) applied to every face."""
    editor = b""
    if material:
        mat = _chunk(0xA000, material.encode() + b"\0")
        mat += _chunk(0xA020, _chunk(0x0011, bytes(colour)))
        if texture:
            mat += _chunk(0xA200, _chunk(0xA300, texture.encode() + b"\0"))
        editor += _chunk(0xAFFF, mat)
    mesh = _chunk(0x4110, struct.pack("<H", len(_V))
                  + b"".join(struct.pack("<3f", *v) for v in _V))
    if texture:
        mesh += _chunk(0x4140, struct.pack("<H", len(_UV))
                       + b"".join(struct.pack("<2f", *uv) for uv in _UV))
    faces = struct.pack("<H", len(_F)) + b"".join(struct.pack("<4H", a, b, c, 7) for a, b, c in _F)
    if material:
        faces += _chunk(0x4130, material.encode() + b"\0" + struct.pack("<H", len(_F))
                        + b"".join(struct.pack("<H", i) for i in range(len(_F))))
    mesh += _chunk(0x4120, faces)
    editor += _chunk(0x3D3E, struct.pack("<I", 3))
    editor += _chunk(0x4000, b"conf_cube\0" + _chunk(0x4100, mesh))
    return _chunk(0x4D4D, _chunk(0x0002, struct.pack("<I", 3)) + _chunk(0x3D3D, editor))


def chunk_ids(data: bytes, start: int = 0, end: int | None = None) -> list[int]:
    """Every chunk id in a .3ds, depth first (for tests)."""
    end = len(data) if end is None else end
    out = []
    i = start
    containers = {0x4D4D, 0x3D3D, 0xAFFF, 0x4000, 0x4100, 0xA020, 0xA200, 0x4120}
    while i + 6 <= end:
        cid, length = struct.unpack_from("<HI", data, i)
        if length < 6 or i + length > end:
            raise ValueError(f"bad chunk {cid:04x} at {i}")
        out.append(cid)
        if cid in containers:
            body = i + 6
            if cid == 0x4000:
                body = data.index(b"\0", body) + 1
            elif cid == 0x4120:  # the face list: a count, the faces, then sub-chunks
                body += 2 + 8 * struct.unpack_from("<H", data, body)[0]
            out += chunk_ids(data, body, i + length)
        i += length
    if i != end:
        raise ValueError("trailing bytes")
    return out


# ------------------------------------------------------------------ all

def files() -> dict[str, bytes]:
    out = {
        "conf_red.3ds": cube_3ds("conf_red", RED),
        "conf_nomat.3ds": cube_3ds(None),
        "conf_tex.3ds": cube_3ds("conf_texmat", (255, 255, 255), texture="conf_tex.png"),
        "conf_tex.png": png(256, 256, GREEN),
        "conf_overlay.png": png(64, 64, MAGENTA),
        "conf_marker.cs": b'echo("CONFORMANCE-MARKER-CS");\n',
        "conf_marker.ter": b"CONFORMANCE-MARKER-TER\n",
    }
    for i, c in enumerate(SKY_COLOURS):
        out[f"conf_sky{i}.png"] = png(64, 64, c)
        out[f"conf_sky{i}.gif"] = gif(16, 16, c)
    return out


def write(outdir: Path) -> list[Path]:
    outdir.mkdir(parents=True, exist_ok=True)
    written = []
    for name, data in files().items():
        p = outdir / name
        p.write_bytes(data)
        written.append(p)
    return written


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    for p in write(Path(argv[0])):
        print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
