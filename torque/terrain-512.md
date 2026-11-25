# Graal 5.12 streamed terrain: TerrainBlock, chunk events and the heights cache

Date: 2026-11-25. Client: the real 5.12 `Graal3DEngine.dll` (SHA-256 `04f7a133…`, 2007-10-19).
Tags as in `README.md`: **[bin]** read from that binary for behaviour, **[lab]** seen with the real
client against the Seihai gserver in a lab VM, **[inf]** inferred.

This closes the open item in [udp-session.md](udp-session.md) ("`TerrainBlock` … layouts are
unread") for terrain, and replaces the guesses in `graal3d/torque-engine-4x.md` § Terrain streaming
and [5007-g3d.md](5007-g3d.md) § Terrain chunks. Nothing here is decompiled text; it is the wire and
file behaviour a clean-room server or client needs.

Graal's terrain is a stock TGE 1.x-sized grid, 256 × 256 squares, but it never comes from a `.ter`
file in 5.12. The server ghosts a `TerrainBlock` that carries only settings, and then streams the
heights, materials and holes as 256 chunks of 16 × 16 squares in `TerrainChunkEvent`s. The client
keeps every chunk it receives in a per-server cache and tells the server which chunks it already
has. **[bin]**

All fields are Torque bit-stream fields as in [udp-session.md](udp-session.md) §2: integers
low bit first, `pstring` as there, and "raw" values copied through the stream's byte-write at the
current bit position (a raw 32-bit value is the same bits as an `int32`).

## 1. The `TerrainBlock` ghost

Object class `TerrainBlock` (protocol 24 class table, [udp-session.md](udp-session.md) §3). Every
update is one guarded block **[bin]**:

| # | Field | Width | Client use |
|---|---|---|---|
| 1 | init | flag | 0: nothing more follows, nothing changes |
| 2 | object name | `pstring` | assigned as the object's name (use `Terrain`) |
| 3 | value | raw 32 | stored, then reset to 1 when the block is added; a server may send 0 |
| 4 | text | `pstring` | read and dropped (the stock writer sends an empty string) |
| 5 | text | `pstring` | read and dropped (empty) |
| 6 | value | raw 32 | dropped (the stock writer sends 1.0 as a float) |
| 7 | value | raw 32 | dropped (the stock writer sends 0.01 as a float) |
| 8 | value | raw 32 | dropped (the stock writer sends the integer 8) |
| 9 | square size | raw 32, integer | metres per square; use 8 |
| 10 | repeat | raw 8 | non-zero: the terrain repeats (tiles) beyond its edges |

That is 1 bit with init 0, and 1 + 2 × 8-bit-or-more strings + 168 bits with init 1. The ghost
update carries its own `int14` bit length (§8), so a wrong guess costs nothing.

**When the block is added** (its first update) the client **[bin]**:

1. becomes the client's current terrain if it has none yet (a later block named `Terrain` replaces it);
2. places the terrain's corner at (−128 × square size, −128 × square size, 0), so the 256 × 256
   grid is centred on the origin;
3. logs `Loading terrain from terrain chunks.`;
4. loads the material list from `heights.info` in the cache folder (§4). If that file is not in
   the cache it asks for `heights.info` with the normal Graal file request over TCP; an empty answer
   leaves the material list as it was;
5. loads each cached chunk file `heights<x>-<y>.dat`, x and y 0–15, that exists (§4);
6. sends one `TerrainRequestUpdatesEvent` (§3) with the stamp of every chunk.

## 2. `TerrainChunkEvent` (server → client)

Event class `TerrainChunkEvent` (§3 table). Payload **[bin]**:

```
int4    chunk x (0–15)
int4    chunk y (0–15)
raw 32  stamp (the sender's stamp for this chunk; the receiver ignores it)
int10   n, the compressed length in bytes (0–1023)
n bytes zlib stream (RFC 1950, with the 2-byte header) holding the chunk data below
```

On receipt, if n > 0 and the client has a current terrain, it logs
`received terrain chunk (x, y): len n`, inflates the bytes, applies the chunk to the terrain,
re-encodes the chunk, stores the new stamp and writes the cache file, then rebuilds that 16 × 16
area. A chunk that arrives before the `TerrainBlock` is added is dropped, so send chunks only
after the block's create is acknowledged. **[bin]** The stock writer of these events lives in the
same DLL (the server half of the engine, logging `sending terrain chunk`).

### Chunk data (inflated)

```
int8      mode: 2 = hole flags follow at the end; 1 = clear all holes in this chunk; 0 = leave holes
int16     h0, the height of square (0, 0) of the chunk
256 raw bytes   signed deltas d[y][x], row by row (y outer, x inner)
int6      N, the number of materials used in this chunk (0–63; only ids 0–31 make sense)
N × int5  material ids (indices into the heights.info list)
if N > 1: for each square, rows then columns:
            flag  blend
            intW  primary: an index into the N ids
            if blend: intW secondary index, int4 a
if mode 2: 256 flags, rows then columns: 1 = hole
```

`W` is the number of bits for N choices: N rounded up to a power of two, then its base-2
logarithm (N = 2 → 1 bit, 3 or 4 → 2, 5 to 8 → 3). With N of 0 or 1 every square takes the first
id. **[bin]**

**Heights.** The client keeps a 16-bit height per square and stores each decoded value shifted
up 2 bits. In stock TGE 1.x a stored height of 32 is 1 m, so one wire unit is 1/8 m **[inf]**.
Decoding, with all arithmetic 16-bit for heights and 8-bit signed for deltas, and "/2" truncating
toward zero **[bin]**:

```
h[0][0] = h0
row 0:      h[0][x] = h[0][x-1] + d[0][x]                       (x = 1..15; d[0][0] unused)
column 0:   h[y][0] = h[y-1][0] + d[y][0]                       (y = 1..15)
other:      d[y][x] = d[y][x] + (d[y-1][x] + d[y][x-1]) / 2      (already-decoded neighbours)
            h[y][x] = (h[y-1][x] + h[y][x-1]) / 2 + d[y][x]
```

The writer does the inverse: first-pass deltas against the same predictors (row 0 against the
left neighbour, column 0 against the square above, the rest against the mean of both), each
clamped to −127…127, then a second pass from the last row and column back to (1, 1) that
replaces each first-pass delta with itself minus the mean of its upper and left first-pass deltas,
clamped again. Large steps are therefore lossy: a writer must clamp, and a reader must decode
exactly as above. **[bin]**

**Materials.** The decoded square writes the primary material id into the material map. For the
32 alpha maps, the primary's alpha becomes a × 16, the secondary's 255 − a × 16, every other
material's 0; without blend the primary's alpha is 255. The writer chooses the primary as the
material with the largest alpha and sends that alpha divided by 16. **[bin]**

**Holes** are bit 3 (value 8) of the square's flag byte, as in stock TGE (`Material::Empty`).
**[bin][inf]**

## 3. `TerrainRequestUpdatesEvent` (client → server)

Event class `TerrainRequestUpdatesEvent`. Payload: 256 raw 32-bit stamps, index y × 16 + x
(8192 bits). Stamp 0 means the client has no data for that chunk. The client sends it once, when
the `TerrainBlock` is added, after loading its cache. **[bin]** A server should answer by sending a
`TerrainChunkEvent` for every chunk whose stamp differs from its own.

**Stamp** = Torque's `calculateCRC` over the inflated chunk bytes: the standard CRC-32 table
(polynomial 0xEDB88320), starting value 0xFFFFFFFF, **no** final inversion. In zlib terms,
`crc32(data) XOR 0xFFFFFFFF`. The client computes it itself after applying each chunk and after
loading each cache file. **[bin]**

## 4. The cache folder

Path: the user folder, then `levels3d/heights/<server>/`, where `<server>` is the current Graal
server name, escaped for use as a folder name. **[bin]**

| File | Content |
|---|---|
| `heights.info` | the material list: up to 32 texture names, comma-separated, in material-id order. Fetched once over TCP when missing, then kept. **[bin]** |
| `heights<x>-<y>.dat` | one per chunk, x and y in decimal without padding (`heights0-0.dat` … `heights15-15.dat`): the zlib-compressed chunk data of §2, exactly as the client re-encoded it. **[bin]** |

A cached chunk is loaded with the same decoder as a received one, so a server can pre-seed a
client by shipping these files (or a lab can plant them). The client rewrites a chunk file every
time it receives that chunk. **[bin]**

**Material textures.** Each name in `heights.info` is loaded as a texture through the normal
resource path. It must be 256 × 256 and 24-bit; anything else logs
`Terrain texture of bad format (must be 256x256x24): <name>` and falls back to `default`, and a
missing one logs `Missing terrain texture: <name>`. **[bin]** A server can also change the list
during play with the `setmaterials` BigData text message ([udp-session.md](udp-session.md) §7).
**[bin]**

## 5. `WaterBlock` (read beside the terrain)

Object class `WaterBlock`. Unlike `TerrainBlock`, only the name is guarded; every update carries
the whole block **[bin]**:

| # | Field | Width |
|---|---|---|
| 1 | name follows | flag → `pstring` object name |
| 2 | transform | position 3 × `f32`, then rotation as a quaternion: x, y, z as 3 × `f32` and a flag "w is negative" (w = √(1 − x² − y² − z²)). This is Torque's compact matrix read, not the axis-angle of the `GameObject` update. |
| 3 | scale | 3 × `f32` (the water's extent in metres). The client only takes it when x and y are both at least 1024. |
| 4 | textures | 5 × `pstring`: surface, specular mask, environment map over, environment map under, shore |
| 5 | submerge textures | 2 × `pstring`, loaded as the under-water overlay textures |
| 6 | liquid type | raw 32, integer (stock TGE: 0 water, 1 ocean, 2 river, 3 stagnant, 4 lava, 5 hot lava, 6 crusty lava, 7 quicksand **[inf]**) |
| 7 | physics and look | 5 × raw 32 floats: density, viscosity, wave magnitude, surface opacity, environment-map intensity |
| 8 | two switches | 2 × raw 8 (non-zero = on): remove wet edges, use depth mask |
| 9 | shading | 12 × raw 32 floats: surface and shore tessellation, surface parallax, flow angle, flow rate, distortion grid scale, distortion magnitude, distortion time, shore depth, minimum alpha, maximum alpha, depth gradient |
| 10 | specular colour | 4 × `int8` R, G, B, A (0–255, divided by 255) |
| 11 | specular power | raw 32 float |
| 12 | ignore terrain | raw 8 (non-zero = on) |

The field names come from the class's own property names in the same binary, in the order the
stock TGE 1.x writer used; the meaning of each float is stock Torque's **[inf]**. Nothing in the
update is a file name the client downloads by itself; textures go through the normal resource
path **[inf]**.

## 6. For a server

1. Ghost one `TerrainBlock`: init 1, name `Terrain`, 0, two empty strings, 1.0, 0.01, 8, square
   size 8, repeat 0 or 1.
2. Serve `heights.info` (and the textures it names) as ordinary level files.
3. When the client's `TerrainRequestUpdatesEvent` arrives, send a `TerrainChunkEvent` for each chunk
   whose stamp differs. Most chunks compress to well under the 1023-byte limit; a flat chunk is a
   few dozen bytes.

A reference encoder and decoder that follows this note (kept with the owner's lab material, not in
this repo) produced 256 chunks of rolling hills at about 150 compressed bytes each.

## 7. Script access: `Terraformer.setTerrain`

The 5.12 DLL keeps a cut-down `Terraformer` (`loadGrayscale` / `loadGreyscale`, `saveGreyscale`,
`setTerrain`). `setTerrain(register)` returns false and does nothing unless a streamed
`TerrainBlock` is the client's current terrain. Otherwise it copies the 256 × 256 register into
that terrain's heights with the rows flipped (register row 255 becomes terrain row 0),
rebuilds the grid, relights it with a fixed light (direction 0.5, 0.5, −0.5; ambient 0.35;
colour 0.8) and returns true. No chunk file is written and no stamp changes on that path, so it
changes the live view only. **[bin]**

Research board rows (`torque/3d-capability-board.tsv`): T3D-040 (`TerrainBlock`, chunks, cache),
T3D-044 (terrain texture rules), T3D-045 (`WaterBlock`).

## Lab results

_Pending: the live run against the Seihai gserver's raw-object harness on 2026-11-25._
