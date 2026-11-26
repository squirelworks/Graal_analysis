#!/usr/bin/env python3
"""Generate the conformance suite's own 3D content (no game content).

Every file the generated worlds name is made here from nothing: plain cubes in
.3ds, solid-colour PNG and GIF textures, and marker files. So the suite needs
no client asset and nothing generated is ever committed.

    python3 tools/conformance/gen_content.py OUTDIR

Files (all under OUTDIR):

    conf_red.3ds       unit cube, one material "conf_red" with a red diffuse colour
    conf_nomat.3ds     the same cube with no material (5.12 and 4.20r6 draw none of it)
    conf_red_v2.3ds    the red cube's material in pink, swapped in as conf_red.3ds (T3D-155)
    conf_tex.3ds       the cube with UVs and a material whose texture is conf_tex.png
    conf_tex.png       256x256 solid green
    conf_sky0..5.png   sky faces, each its own solid colour (SKY_COLOURS)
    conf_sky0..5.gif   the same as GIF (3.153 asks for sky textures as .gif)
    conf_overlay.png   64x64 solid magenta, for GS2 showimg over the 3D view
    conf_marker.cs     a TorqueScript marker, which no read build should request
    conf_marker.ter    a .ter marker, likewise
    conf_ground.png    256x256 solid tan: the flat terrain's one material
    conf_water.png     64x64 solid deep blue: a water surface texture
    heights.info       the terrain material list (conf_ground.png)
    conf_grass.png     256x256 solid white: a grass texture
    heights_grass.info heights.info with conf_grass.png as a second material, so that
                       graal3d_pushterrain pushes the grass texture too (served as heights.info)
    conf_huge.png      a 64x64 white PNG whose header claims 100000 x 100000 (T3D-146)
    conf_huge.3ds      the cube with UVs and a material whose texture is conf_huge.png
    conf_ter/heights<x>-<y>.dat   a flat 256 x 256 streamed terrain at height 0, 256 chunks
                       (torque/terrain-512.md: one zlib stream of the chunk bit stream each)

Derived files (from a held content pack, made by `derive`): a copy of a
.dts or .dif with its version word set, for the version-bound cases.

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
TAN = (200, 160, 90)
WATER = (20, 40, 160)
WHITE = (255, 255, 255)
PINK = (255, 150, 200)
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


# ------------------------------------------------------------------ terrain

class BitWriter:
    """Torque bit stream: least significant bit first within each byte."""

    def __init__(self):
        self.bits: list[int] = []

    def write(self, value: int, n: int):
        for i in range(n):
            self.bits.append((value >> i) & 1)

    def bytes(self) -> bytes:
        out = bytearray((len(self.bits) + 7) // 8)
        for i, b in enumerate(self.bits):
            out[i // 8] |= b << (i % 8)
        return bytes(out)


def flat_chunk(height: int = 0, material: int = 0) -> bytes:
    """One streamed terrain chunk (torque/terrain-512.md "Chunk data"), flat:
    mode 0 (leave holes), h0, 256 zero deltas, one material. `height` is in
    wire units (8 a world unit). Returned zlib-compressed, as the
    heights<x>-<y>.dat cache file and the chunk event carry it."""
    w = BitWriter()
    w.write(0, 8)                 # mode
    w.write(height & 0xFFFF, 16)  # h0
    for _ in range(256):
        w.write(0, 8)             # deltas
    w.write(1, 6)                 # N = 1 material
    w.write(material, 5)
    return zlib.compress(w.bytes(), 9)


def flat_terrain(folder: str = "conf_ter") -> dict[str, bytes]:
    chunk = flat_chunk()
    return {f"{folder}/heights{x}-{y}.dat": chunk for x in range(16) for y in range(16)}


# ------------------------------------------------------------------ derived

def set_version(data: bytes, version: int, name: str) -> bytes:
    """A copy of a .dts or .dif with its version word set. A .dts starts with
    a 16-bit version (the exporter version in the next 16 bits, kept); a
    .dif starts with a 32-bit version."""
    if name.lower().endswith(".dts"):
        return struct.pack("<H", version) + data[2:]
    if name.lower().endswith(".dif"):
        return struct.pack("<I", version) + data[4:]
    raise ValueError(f"{name}: only .dts and .dif have a version word here")


# ------------------------------------------------------------------ all

def huge_png(width: int = 100000, height: int = 100000) -> bytes:
    """A small white PNG whose IHDR claims width x height (CRC kept valid):
    seihai-gserver-v2 refuses any PNG over 8192 a side at start-up, and one
    claiming 30000 x 30000 crashed a real 5.12."""
    data = bytearray(png(64, 64, WHITE))
    struct.pack_into(">II", data, 16, width, height)
    struct.pack_into(">I", data, 29, zlib.crc32(bytes(data[12:29])))
    return bytes(data)


def grass_rawobject(name: str, x: float, y: float, z: float, radius: int, lo: int, hi: int,
                    texture: str, seed: int = 1, box=(-1024, -1024, 1024, 1024), scale: float = 3) -> str:
    """A `rawobject DynamicGrass ...` world line carrying the same update as
    seihai-gserver's `replicator DynamicGrass` line (src/graal3d/ground.rs,
    Replicator::write) but with the radius as given: the server's own line
    raises a grass radius below 8 to 8 (#218), a raw object does not. Checked
    bit for bit against Replicator::write at seihai-gserver 6c42a37."""
    f = ["f1", "f0", f"str:{name}", "f0", "f0", "f0",                  # name; no scale, shape, skin
         "f1", f"f32:{x:g}", f"f32:{y:g}", f"f32:{z:g}", "f32:0", "f32:0", "f32:1", "f32:0",  # transform
         "f0", "f0", "f0", "f0", "f0", "f0", "f0", "f0",               # sections 6 to 13 clear
         "f1", f"f32:{x:g}", f"f32:{y:g}", f"f32:{z:g}", "f32:0", "f32:0", "f32:0", "f0",  # position, quat
         f"u32:{seed}", "f0", f"str:{texture}", f"u8:{radius}", f"u8:{lo}", f"u8:{hi}"]
    x0, y0, x1, y1 = box
    for v in (x0, y0, -32767, x1, y1, 32767):                         # signed int16s
        f += ["f1" if v < 0 else "f0", f"i15:{abs(v)}"]
    f += [f"f32:{scale:g}"] * 6 + ["f32:0"] * 5 + ["f32:360", "f32:0"]  # scale, rotation, offset z
    f += ["f1", "f0", "f0", "f0", "f0",                                # terrain only
          "f0", "i7:90", "f0", "f32:1", "f32:1", "f32:1", "f0", "f0", "i7:0", "f0"]
    return "rawobject DynamicGrass " + " ".join(f)


def files() -> dict[str, bytes]:
    out = {
        "conf_red.3ds": cube_3ds("conf_red", RED),
        "conf_nomat.3ds": cube_3ds(None),
        # The red cube's replacement for the cache cases: same material name,
        # pink, swapped in under the name conf_red.3ds between sessions.
        "conf_red_v2.3ds": cube_3ds("conf_red", PINK),
        "conf_tex.3ds": cube_3ds("conf_texmat", (255, 255, 255), texture="conf_tex.png"),
        "conf_tex.png": png(256, 256, GREEN),
        "conf_overlay.png": png(64, 64, MAGENTA),
        "conf_marker.cs": b'echo("CONFORMANCE-MARKER-CS");\n',
        "conf_marker.ter": b"CONFORMANCE-MARKER-TER\n",
        "conf_ground.png": png(256, 256, TAN),
        "conf_water.png": png(64, 64, WATER),
        "heights.info": b"conf_ground.png\n",
        "conf_grass.png": png(256, 256, WHITE),
        "heights_grass.info": b"conf_ground.png\nconf_grass.png\n",
        "conf_huge.png": huge_png(),
        "conf_huge.3ds": cube_3ds("conf_hugemat", WHITE, texture="conf_huge.png"),
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
