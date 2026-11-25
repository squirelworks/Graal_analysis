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
| 1 | init | flag | 0: nothing more follows. A create with init 0 is still added and still loads and streams the terrain, with no name and a zero square size **[lab]** |
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
   grid is centred on the origin. Chunk (cx, cy), square (sx, sy) starts at
   x = −128·sq + (cx·16 + sx)·sq, y = −128·sq + (cy·16 + sy)·sq, so chunk (0, 0) is the −x, −y
   corner and chunk rows grow toward +y. **[lab]** (`getdropz` sampled at square sizes 8 and 2);
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
area. A chunk that arrives before the `TerrainBlock` is added is logged but not stored, so send
chunks only after the block's create is acknowledged. **[bin][lab]** An event with n = 0 is
ignored. A corrupt or truncated zlib stream is not rejected: the chunk is applied as all zeros
(height 0, material 0) and that flat chunk is saved to the cache. **[lab]** The stock writer of these events lives in the
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
up 2 bits. One world unit is 8 wire units: a flat chunk sent at 3200 reports `getdropz` 400, at square size 8 and at 2 alike **[lab]** (stock TGE 1.x also keeps 32 stored units per metre).
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

### Edge cases seen live

All with the real 5.12 client; it stayed up through every case. **[lab]**

- The event's stamp is ignored: a chunk sent with a made-up stamp is saved with the client's
  own stamp, and that is what the next request reports.
- Any mode other than 2 (3, 127, 255 tested) behaves like "no hole flags": heights apply and the
  chunk is saved as mode 2 with no holes.
- A plain stream cut short reads the missing fields as zero: cut after the deltas gives the
  heights with material list `[0]`; cut after the material ids gives a flat chunk at `h0`.
- Bytes after the end of the chunk data are ignored; the saved chunk is the canonical one.
- A zlib stream cut at n = 1023 bytes (short of its end) is accepted without an error: whatever
  inflated is applied and the rest is zero.
- The same chunk twice in a row: the second wins.
- Heights are not clamped. All deltas +127 climb steadily (800 to 2705 in one chunk); all −127
  wrap below 0 to the top of the 16-bit range. `h0` = 65535 is kept as 16383, because the stored
  value is shifted up 2 bits into 16 bits, so only 14 bits of `h0` survive; later sums can still
  pass 16383.
- 256 chunk events in one burst were all saved (256 of 256, several runs).

## 3. `TerrainRequestUpdatesEvent` (client → server)

Event class `TerrainRequestUpdatesEvent`. Payload: 256 raw 32-bit stamps, index y × 16 + x
(8192 bits). Stamp 0 means the client has no data for that chunk. The client sends it once, when
the `TerrainBlock` is added, after loading its cache. **[bin]** A server should answer by sending a
`TerrainChunkEvent` for every chunk whose stamp differs from its own.

**Canonical re-encoding.** The client never keeps the bytes it was sent. After applying a chunk
it encodes it again with its own writer and saves that: mode is always 2, the material list holds
only the ids actually used in the chunk, sorted ascending (the per-square indices are remapped),
and a blend is stored with the larger-alpha material as primary (a received primary 0, secondary 1,
alpha 7 is saved as primary 1, secondary 0, alpha 8). The file is that stream compressed with
zlib's default level. **[bin][lab]**

**Stamp** = Torque's `calculateCRC` over the client's re-encoded chunk bytes (above), not the
bytes the server sent: the standard CRC-32 table
(polynomial 0xEDB88320), starting value 0xFFFFFFFF, **no** final inversion. In zlib terms,
`crc32(data) XOR 0xFFFFFFFF`. The client computes it itself after applying each chunk and after
loading each cache file. **[bin]**

## 4. The cache folder

Path: the user folder, then `levels3d/heights/<server>/`, where `<server>` is the current Graal
server name escaped for use as a folder name: a space becomes `%032` (a percent sign and the character's code as three decimal digits), so the lab server `Lab 3D` is cached in `levels3d/heights/Lab%0323D/`. **[bin][lab]**

| File | Content |
|---|---|
| `heights.info` | the material list: up to 32 texture names, **one per line**, in material-id order. A comma does not separate names: `grass,rock` on one line is one texture called `grass,rock`. Fetched once over TCP when missing, then kept. **[bin]** |
| `heights<x>-<y>.dat` | one per chunk, x and y in decimal without padding (`heights0-0.dat` … `heights15-15.dat`): the zlib-compressed chunk data of §2, exactly as the client re-encoded it. **[bin][lab]** |

A cached chunk is loaded with the same decoder as a received one, so a server can pre-seed a
client by shipping these files (or a lab can plant them). The client rewrites a chunk file every
time it receives that chunk. **[bin]**

**Material textures.** Each name in `heights.info` is requested by its bare name with the normal
Graal file request and cached as `levels3d/images/<name>`. **[lab]** Without a server push the timing is one visit late: on the first visit
the client fetches only `heights.info` (saved under `levels3d/images/`) and requests no texture;
on the second visit it logs `Missing terrain texture: <name>` for each and then downloads them,
saving each under exactly the listed name (a bare `grass` is saved with no extension, `grass.png`
as `grass.png`; the bare names were each downloaded twice). The 4.20 Linux lab found extensionless
cached textures fail to load on later visits, so list names with their extension. **[lab]** When the server pushes the terrain files (`graal3dpushterrain`), the first visit fetches `heights.info` and every texture before the ghosts arrive and draws the terrain textured at once (real 5.12 under Mesa, T3D-044); the white first visit was the no-push case, not a renderer limit. **[lab]** It must be 256 × 256 and 24-bit; anything else logs
`Terrain texture of bad format (must be 256x256x24): <name>` and falls back to `default`, and a
missing one logs `Missing terrain texture: <name>`. **[bin]** A server can also change the list
during play with the `setmaterials` BigData text message ([udp-session.md](udp-session.md) §7).
**[bin]** That message is **not** split at newlines: a text of `rock`, newline, `grass` was logged
as `setting terrain materials to` the whole text and then reported missing as a single name.
The `setmaterials` list is **comma**-separated: `t_a,t_b` set two materials and fetched both textures. So `heights.info` (one per line) and `setmaterials` (commas) use different separators. **[lab]**

The client persists a `setmaterials` list: it writes `heights.info` in the cache folder as 32
lines with CRLF endings, one per material slot, blank for unused slots, with control characters
stripped from each name (so a name holding a newline becomes the two halves joined). It loads
that file on the next connect. The `heights.info` fetched over TCP is cached separately under
`levels3d/images/`. **[lab]**

## 5. `WaterBlock` (read beside the terrain)

Object class `WaterBlock`. Unlike `TerrainBlock`, only the name is guarded; every update carries
the whole block **[bin]**:

| # | Field | Width |
|---|---|---|
| 1 | name follows | flag → `pstring` object name |
| 2 | transform | position 3 × `f32`, then rotation as a quaternion: x, y, z as 3 × `f32` and a flag "w is negative" (w = √(1 − x² − y² − z²)). This is Torque's compact matrix read, not the axis-angle of the `GameObject` update. |
| 3 | scale | 3 × `f32` (the water's extent in metres). The static read suggested the client only takes it from 1024 up; live, a 512 × 256 block covers exactly 512 × 256 (see below). |
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

Live on 5.12 (a block at z 20 with z scale 20, wave magnitude 0.3) **[lab]**:

- The water surface is at position z + scale z (40 here), not at position z. `liquidheight`
  reads that height with about ±0.15 of wave motion; `watercoverage` is 1 below it, a small
  fraction just above it, and `liquidtype` reads `Water`.
- Footprint (a 2-D `watercoverage` grid, no terrain): a block at (0, 0, 0) with scale
  512 × 256 covers exactly x 0…512, y 0…256. The block runs from its position to position +
  scale (a corner, not the centre), stops at its scale, and a 512 scale is taken. Turned 90°
  about z it covers x 0…256, y −512…0: it turns about its position. (An earlier reading over
  terrain that seemed to run past the scale was stale.)
- Waves (a 5 × 5 grid over a 256 × 256 block at magnitude 1, read one tick after each probe
  move, 12 passes): every point is a clean sine with the same period, and the whole field fits
  (r.m.s. error 0.005)

  `liquidheight = surface + 0.25 · m · (sin(ω·t + k·x + φ) + sin(ω·t + k·y + φ))`

  with m the wave magnitude, x and y in world units, k = 0.050 per unit (wavelength 2π/k ≈
  125.7 units) and ω ≈ 0.983 rad/s (period about 6.39 s). A finer line of 33 points 8 units apart
  fixed k (r.m.s. error 0.0004, each term 0.250 · m). Two equal waves, one along x and one along
  y, crests travelling toward −x and −y: on the diagonal x = y a point swings ±0.5 · m, elsewhere
  less. The waves follow world position, not the block's own corner (the same block moved by
  (1000, 1000) shifts phase as the formula predicts). **[lab]** (fit)
  Note for probes: read `liquidheight` one tick after moving the object; read in the same tick
  it returns the previous point's value.
- A 32 × 16 × 2 block at (0, 16, 0) covers exactly x 0…32, y 16…32 with its surface at 2, with
  or without terrain and whatever `ignoreTerrain`; `ignoreTerrain` changed only a thin band where
  the water meets the ground.
- `liquidheight` keeps its last value after an object leaves the water.
- `ignoreTerrain` 0 and 1 draw visibly differently over terrain.

## 6. For a server

1. Ghost one `TerrainBlock`: init 1, name `Terrain`, 0, two empty strings, 1.0, 0.01, 8, square
   size 8, repeat 0 or 1.
2. Serve `heights.info` (one texture name per line) and the textures it names as ordinary level files.
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

Live: a GS2 weapon can create the object (`new Terraformer(...)` gives object type `Terraformer`).
`setTerrain` returned 0 with no `TerrainBlock` and 1 with one; the chunk files were byte-identical
before and after, and the stamps on the next connect were unchanged. `loadGreyscale` resolves its
file name through the client's own file system and asks the server for that file over TCP when it
is not cached; it returns 0 until the file has arrived. **[lab]**

`loadGreyscale(register, file)` reads the image as at least three bytes per pixel and turns each
pixel into a 0–1 value with luminance weights (0.299 R, 0.587 G, 0.114 B, over 256). It walks the
register's 256 × 256 squares and reads the image bottom row first, so together with `setTerrain`'s
own flip, image row r lands on terrain row r. It does not check the image's depth or size.
**[bin]** In the lab, with a `TerrainBlock` present, 32-bit RGBA PNGs of 64 × 64 and 128 × 128
load (`loadGreyscale` and `setTerrain` both return 1). A 256 × 256 RGBA image returned 1 in one
run but crashed on the second `loadGreyscale` call in another; 512 × 512 and 256 × 128 RGBA
crashed the same way. A 256 × 256 RGBA image also crashed on the first call once the file was
cached, with and without a `TerrainBlock`, so the block is not the factor. A 24-bit RGB PNG
(256 × 256 and 128 × 128) and an 8-bit greyscale PNG (colour type 0) crash at once. So the safe
use is a small (64 or 128 square) RGBA image; nothing at 256 or above is reliable. **[lab]**

The client does not clamp a script-moved `GameObject` to the terrain: its z stays at the value
set (60 in the lab) while `getdropz(x, y, 500)` reports the ground below. Every `getdropz` value
over the planted terrain was a multiple of 1/8, which fits one wire height unit being 1/8 m.
`player.getdropz()` returned 0. **[lab]**

Research board rows (`torque/3d-capability-board.tsv`): T3D-040 (`TerrainBlock`, chunks, cache),
T3D-044 (terrain texture rules), T3D-045 (`WaterBlock`).

## 8. Older builds: the `.ter` file path

4.04r2 and 3.153 still carry stock Torque's file path beside the chunk path. In 4.04r2, adding a
`TerrainBlock` takes the file path only when the object's `terrainFile` property names a `.ter`
resource that loads (the resource filter serves `.ter` from `levels3d/terrain/`). The client then
logs `Loaded terrain from terrain file.` and does not ask for chunks. With no file name, or a file
that does not load, it falls back to `Loading terrain from terrain chunks.` and the chunk path of
§1. **[bin]**

The network update never sets `terrainFile`: only the property setter does. So a ghosted
`TerrainBlock` always streams chunks, and the `.ter` path is reachable only from a script that
creates a `TerrainBlock` locally and sets `terrainFile` before adding it **[bin][inf]**. In 5.12
the property name survives, but adding a block no longer branches on it: 5.12 only streams.
**[bin]** Board row T3D-041.

Live on 4.04r2, a script's `new TerrainBlock(...)` returns a `TerrainBlock` and `terrainFile`
reads back as set, but the client logs neither the file line nor the chunk line, with or without
`terrainFile`: a script-made block never loads terrain, only a ghosted one does (chunk path). So
the `.ter` branch was not reached live. **[lab]**

## Lab results

Run 2026-11-25: the real 5.12 client in the Windows 10 lab VM, joined to the Seihai gserver
(seihai-gserver-v2 PR #150, commit `05a4fcdf`, `graal3d = true`, raw-object harness) on the
loopback address. The test set was 256 chunks of rolling hills with two materials. Captures and
logs are kept with the owner's lab material. **[lab]**

| Check | Result |
|---|---|
| `TerrainBlock` with the §1 layout: log line, cache folder created, `heights.info` requested over TCP, request event with 256 zero stamps | pass |
| 256 chunk events: one cache file per chunk, terrain drawn | pass |
| Reconnect: the 256 stamps in the request equal the expected stamps | pass, 256 of 256 |
| Planted `heights.info` and chunk files before the first connect: loaded, stamps non-zero in the first request | pass, 256 of 256 |
| Chunk mode 0 and 1; mode 2 with holes | accepted; holes kept |
| N = 0 materials | accepted; squares take material 0 |
| Chunk with n = 0 | ignored |
| Corrupt or truncated zlib | chunk zeroed and saved |
| Chunk before the `TerrainBlock` | logged, not stored |
| `TerrainBlock` with init 0 | still loads chunks |
| Chunk with 3 and 5 materials, ids out of order, an unused id; chunks at x or y = 15 | accepted; saved with the used ids only, ascending |
| `TerrainBlock` named `Foo`; square size 0, 1, 32; repeat 1 | accepted, chunks saved, no log difference (the lab VM draws terrain untextured, so the visual effect is not settled) |
| `heights.info` naming a 128 × 128 RGB and a 256 × 256 RGBA texture | no `bad format` or `Missing` log, no crash (not settled whether the texture was used) |
| `WaterBlock` with the §5 layout (with terrain) | ghost created, the surface texture fetched over TCP, a large surface drawn |
| `WaterBlock` liquid type 0 to 7 (eight blocks) | all created, no error |
| `WaterBlock` scale 512 alone | nothing seen in that view; the later coverage grid shows a 512 scale is taken |
| `WaterBlock` scale 1024 and 4096 | created |
| `WaterBlock` opacity 0 and 1; empty and missing surface texture | accepted (one run of opacity 1 and one of the missing texture lost the TCP link during phase 1; the same bytes worked on the next login, so this reads as transient, not layout) |
| Four `GameObject`s with flags 0x10 and 0x30 (show terrain) at heights 0 and 200, beside terrain and water | all created, no error (visual effect not readable in the lab VM) |
| Native terrain from the Seihai gserver (`terrain` world line, a 256-chunk generated world) | first connect: 256 chunks sent, 256 cache files written, hills drawn; reconnect: the client's stamps matched all 256, so the server sent none |

| `Terraformer.loadGreyscale` with a 256 × 256 32-bit RGBA PNG | returns 1, no crash |
| `Terraformer.loadGreyscale` with a 24-bit RGB PNG (256 × 256, 128 × 128) or an 8-bit grey PNG | client crashes (access violation in the 3D engine) |
| Chunk edge cases (wrong stamp, modes 3/127/255, cut streams, trailing bytes, truncated zlib, duplicate chunk, ±127 deltas, `h0` 65535) | all accepted; results in §2 "Edge cases seen live" |
| `setmaterials` then reconnect | list saved to the cache `heights.info` (32 CRLF lines) and reloaded |
| 4.20r8 with the same `TerrainBlock` and chunk bytes | logs `Loading terrain from terrain chunks.`, requests with 256 zero stamps, saves the first chunks byte for byte as 5.12 does (same stamps), then crashes on a null call. Both crashing runs also had `GameObject`s at ground level (z near 0) and a low spawn; the same `TerrainBlock` with no objects and a high spawn ran 110 s without a crash, with or without textures, init 0, repeat 0 or 1. A `WaterBlock` alone is fine. Narrowed further: with only the `TerrainBlock`, the crash comes whenever the camera starts close to the terrain (about 60 units up), and never with the camera 200 units up, with or without objects. So it is in the near-range terrain draw. Height sweep (camera height above the local ground): on a hilly block (square size 2) it crashed at 2–80 units about 1 s after login, at 120 after 1.9 s and at 150 after 3.6 s, and did not crash at 180, 200 or 250. On a flat block with no chunks (square size 8) it crashed at 120 and did not at 180 or 210. So the threshold lies between 150 and 180 units in both worlds, and the higher the camera, the later the crash, which fits the terrain entering the view or detail range shortly after login. **[lab]** The lab VM's OpenGL is the bare Windows software 1.1 driver, so a missing GL extension that 4.20r8 calls without checking is likely **[inf]**; not yet tried on a full OpenGL driver. |
| 5.00r7 | not run: its licence points the login at a fixed LAN address the isolated VM cannot answer; its terrain strings match 5.12 (static) |
| Flat chunk (0, 0) at 3200 beside chunk (1, 0) at 0, `getdropz` every quarter square, square size 8 and 2 | 400 then 0: 8 wire units per world unit; terrain spans −128·sq…+128·sq on both axes; no seam (the last square of a chunk blends linearly into the next chunk's first vertex) |
| `getdropz` at the far edge | the last square before +128·sq blends toward the opposite edge's first vertex (wraps); at or beyond +128·sq and below −128·sq it returns 0 (repeat 0: nothing tiles) |
| `loadGreyscale` RGBA 64, 128 / 256 / 512, 256 × 128 (with terrain) | 1 / 1 in one run, crash in another / crash / crash |
| 4.04r2 script-made `TerrainBlock`, with and without `terrainFile` | created, but neither the file nor the chunk path runs |
| Peaks world from the Seihai gserver: five trees, `getdropz` at each tree | every tree's z within 0.06 of the ground: server placement and the client's terrain agree |
| `heights.info` with bare names vs `.png` names, two visits each | visit 1: only `heights.info` fetched; visit 2: `Missing terrain texture` per name, then each downloaded and saved under the listed name |
| Malformed `WaterBlock`: update cut after the textures; NaN position; +Inf or 1e9 scale; liquid type 8, 255, 2³¹−1; 200-character texture names; zero quaternion | all accepted, client stays up (long names are requested and answered not found) |
| Malformed `TerrainBlock`: square size −8; NaN in the ignored floats; 250-character name; two blocks named `Terrain` | accepted, client stays up |
| `TerrainBlock` square size 2³¹−1 | **client dies** right after `Terrain lit` (4.20r8 too) |
| The malformed `WaterBlock` and `TerrainBlock` rows above on 4.20r8 (camera high) | same as 5.12: all survived |
| A `.3ds` cut to half its length | **client dies** while loading it, no dialog |
| A `.dts` of random bytes / a `.dif` of zeros | logs `attempt to load a version … dts-shape, can currently only load version 24 and before` / nothing; no crash |
| Texture numbering: one chunk with columns 0–7 id 0 and 8–15 id 2, `heights.info` water, sand, grass | the saved chunk decodes to ids [0, 2] with every row id 0 in columns 0–7 and id 2 in columns 8–15: id N is line N + 1 of `heights.info`, same row order as the heights; on the second visit every listed texture is fetched, used or not |
| Mode 2 chunk with squares 6–9 × 6–9 as holes, `getdropz` every 0.5 | an exact cut-out: ground reads 0 for exactly those squares, with no slope at the edge |
| Two `TerrainBlock`s named `Terrain` (square size 8, then 2), then 256 chunks | both send a request (two events); one cache folder; the chunks land on the second block only (ground within ±256, nothing out to ±1024) |
| Script moves a `GameObject` over terrain; `getdropz` sampled | no clamping (z stays as set); `getdropz` values are multiples of 1/8 |

No chunk or ghost case crashed the client; only the `loadGreyscale` cases above did. Corrections this run made to the static read: `heights.info` is
one name per line; the folder-name escape; the canonical re-encoding before the stamp.
