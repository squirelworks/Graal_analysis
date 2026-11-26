# Graal 5.12 replicator update (`DynamicShapeReplicator`, `DynamicGrass`, `DynamicGrassReplicator`)

Date: 2026-11-25. Client: the real 5.12 `Graal3DEngine.dll` (SHA-256 `04f7a133…`), static read.
Tags as in `README.md`: **[bin]** read from that binary for behaviour, **[inf]** inferred,
**[lab]** seen live. Nothing here is decompiled text. Encoding terms as in
[udp-session.md](udp-session.md) §2 and [fxsunlight-512.md](fxsunlight-512.md).

The three classes are ghosted objects. `DynamicGrass` and `DynamicGrassReplicator` derive from
`DynamicShapeReplicator`, which derives from `GameObject`, and all three use the same update
reader. **[bin]** Ground cover is scattered around the object on a grid of 8-unit cells.

## Update layout

The update is a whole `GameObject` update (§8 of [udp-session.md](udp-session.md), all thirteen
section flags), then the replicator's own part **[bin]**:

| # | Field (client property) | Encoding |
|---|---|---|
| 0 | anything follows | flag; 0 ends the update |
| 1 | transform | position 3 × raw 32 floats, then the rotation quaternion's x, y, z (3 × raw 32 floats) and a flag set when w is negative; the same encoding as `WaterBlock` and `fxSunLight` |
| 2 | `seed` | int32 |
| 3 | `shapefiles` | `pstring` |
| 4 | `radius` | int8, in grid cells (the client multiplies by 8 and stores world units) |
| 5 | `mingridobjects` | int8 |
| 6 | `maxgridobjects` | int8 |
| 7 | `boxmin` | 3 × signed int16 (whole numbers) |
| 8 | `boxmax` | 3 × signed int16 (whole numbers) |
| 9 | `shapescalemin` | 3 × raw 32 floats |
| 10 | `shapescalemax` | 3 × raw 32 floats |
| 11 | `shaperotatemin` | 3 × raw 32 floats |
| 12 | `shaperotatemax` | 3 × raw 32 floats |
| 13 | `offsetz` | raw 32 float |
| 14 | `allowonterrain`, `allowoninteriors`, `allowonstatics`, `allowonwater`, `allowwatersurface` | 5 flags, in that order |
| 15 | `allowedterrainslope` | signed int8 |
| 16 | `aligntoterrain` | flag |
| 17 | `terrainalignment` | 3 × raw 32 floats |
| 18 | `surfaceexclusionmode` | flag |
| 19 | `surfacetype` | signed int8 |
| 20 | `hidereplications` | flag |

A **signed intN** is a sign flag (1 = negative) followed by an N−1 bit magnitude, so a signed
int8 holds −127 to 127 and a signed int16 −32767 to 32767. "int32" is read bit by bit and "raw
32" byte-wise at the current bit position; on the wire both are the same 32 bits, LSB first.
**[bin]**

After reading, the client applies the transform and, if the object is already in the world,
regrows its replications. **[bin]**

## What the client does with the values

- `radius` is kept in cells, clamped to 1–64 cells (8 to 512 units). The client allocates a
  (2r+1)² cell grid. **[bin]**
- `mingridobjects` and `maxgridobjects` are clamped to 0–20 per cell. Raising the minimum above
  the maximum raises the maximum, and lowering the maximum below the minimum lowers the
  minimum. **[bin]**
- Setting `radius`, `mingridobjects`, `maxgridobjects`, `shapefiles` or `surfacetype` to a new
  value regrows the cover. **[bin]**
- `shapefiles` is a comma-separated list of shape file names: the client splits it at each `,`
  and keeps each part as one shape name. **[bin]** Whether spaces around a comma are
  trimmed is not read. **[inf]**
- The meanings follow the names: allowed surfaces, a slope limit (degrees **[inf]**), optional
  alignment to the terrain normal, a height offset, and per-object random scale and rotation
  between the min and max vectors. `hidereplications` hides the cover without dropping the
  object. **[inf]**

## Where cover grows

The grid is not centred on the replicator: it follows the client's control object. The
client snaps that object's position to the 8-unit grid and keeps a (2r+1)² block of cells around
it, growing cells that come into range and dropping those that leave. **[bin]** A cell grows
only if:

- `hidereplications` is off and at least one of `allowonterrain`, `allowoninteriors`,
  `allowonstatics` or `allowonwater` is on;
- at least one shape from `shapefiles` is loaded;
- the cell's corner lies inside the box in **world** x and y: `boxmin.x ≤ x < boxmax.x` and
  `boxmin.y ≤ y < boxmax.y`. The box's z values are used later, on each copy's ground height. **[bin]**

Inside a cell the count is random between `mingridobjects` and `maxgridobjects`, from a random
stream seeded by `seed` and the cell, so the same cell always grows the same cover. The stream is
stock Torque's R250 generator (`MRandomR250`), seeded per cell with
`seed + 256·(cy & 255) + (cx & 255)`, where `cx` and `cy` are the cell corner's world x and y
divided by 8 and cut toward zero. The count is `min + r mod (max − min + 1)` from the first
number drawn, or just `min` when the two are equal. **[bin]**

Placing each copy in a cell **[bin]**:

1. **Where in x/y.** `DynamicShapeReplicator` places copies at random: for each copy it draws two
   more numbers r₁, r₂ from the cell's stream and puts the copy at
   `x = cx·8 + (r₁/2³¹ − 0.5)·8`, `y = cy·8 + (r₂/2³¹ − 0.5)·8`, so within ±4 units of the cell
   corner. `DynamicGrass` uses a regular sub-grid instead: with n pieces it takes
   `cols = min(16, ⌊√n⌋)` (at least 1) and `rows = min(16, ⌊n / cols⌋)`, draws `cols × rows` pieces
   (so 5 becomes 4), and puts piece i at `x = cx·8 + ((i mod cols)/cols − 0.5)·8`,
   `y = cy·8 + ((i div cols)/rows − 0.5)·8`.
2. **Ground.** A ray is cast straight down from z = 2000 to z = −2000 through the client's world.
   No hit, or a hit on a surface kind whose allow flag is off (terrain, interiors, statics,
   water), drops the copy.
3. **Height box.** The hit height must satisfy `boxmin.z ≤ z < boxmax.z`.
4. **Slope.** The surface may tilt at most `allowedterrainslope` degrees: the copy is dropped when
   `sin((90 − slope)°)` is greater than the surface normal's z.
5. **Surface type.** When `surfacetype` is 0–31, the copy is also tested against the terrain
   material at that spot, with `surfaceexclusionmode` choosing whether that material is
   required or excluded **[inf]**.
6. Then the copy is created (`DynamicShapeReplicator`), drawing in this order from the same
   stream: a number whose remainder by the shape count picks the shape from `shapefiles`; for a
   shape that is animated, one more number (`r mod 64 + 1`), used for its animation **[inf]**;
   the rotation's z, y and x angles, each uniform between `shaperotatemin` and `shaperotatemax`
   (degrees); then the scale's z, y and x, each uniform between `shapescalemin` and
   `shapescalemax`. A min above its max is swapped first. The copy sits at the ground hit
   plus `offsetz`.
 Each object
is then placed by casting rays onto the allowed surfaces. **[bin]** Each tick the grid is centred on the game connection's **control object** (the player avatar),
read from its transform, not on the camera or the replicator. **[bin]** Live, on flat streamed terrain with a wide box, cover grows around the avatar wherever it spawns:
at (128, −128), at (104, 4) and at (−124, 132), whether the replicator object is next to the avatar, far away at (−300, −300), or hidden 500 units up. **[lab]**
Two things stopped it in earlier runs:

- **The avatar in cell (0, 0).** With the avatar anywhere in the origin cell (−8 < x < 8 and −8 < y < 8, since cells cut toward zero), nothing grows, wherever the replicator is: (4, 4), (7, 7) and (−4, −4) are all bare. One cell out in any direction grows a full patch: (9, 4), (4, 9), (−9, 4) and (20, 20). Moving the avatar from (4, 4) to (40, 4) after spawn makes cover appear around the new spot. A likely reason is that the grid starts out centred on cell (0, 0), so an avatar that starts there never registers a cell change and the grid is never filled **[inf]**. **[lab]**
- **The replicator object on the spot.** (−124, 132) stayed bare while the replicator object sat on it, and grew a full patch once the replicator moved to (104, 4). Why the replicator's own spot blocks cover is still open. **[lab]**

A box of (−1,−1) to (1,1)
allows only the one cell whose corner is at the world origin; a server wanting cover over an area
must send that area as the box, in world units. **[bin]**

Cover grows only in cells inside the **world-coordinate** box (corner x and y). With the
avatar inside the box, the avatar-centred grid holds exactly. In one run (±1024 box, avatar at
(128, −128)), every cube at radius 1 and 2 sat within 0.4 units of the predicted cell
positions, with none outside the predicted cells. With a ±512 box and the avatar at (128, −128),
even the minimal line grows, and count and scale add cover as expected **[lab]**:

| Line, avatar inside the box | Cover (overhead pixels, marker excluded) |
|---|---|
| minimum (radius 1, 1 per cell, scale 1) | about 10k |
| per cell 2 / 5 | about 20k / 47k |
| scale 2 / 5 | about 39k / 206k |

The earlier "lower bound on the parameters" came from a ±100 box, which left the avatar at
(128, −128) outside it. In that case cover doesn't grow around the avatar. It grows just inside
the box corner nearest the avatar, and moves inward by about one cell per radius step
(overhead at z 250, positions ±a few units) **[lab]**:

| Radius, avatar outside a ±100 box | Cover | Where |
|---|---|---|
| 1 | none | — |
| 2 | one clump | about (97, −97) |
| 3 | a few clumps | about (88, −89) |
| 4 | a few clumps | about (81, −80) |

With the avatar outside the box, raising the count or scale at radius 1 still grows nothing.
A follow-up run fits one rule: the clump sits at the cell corner **avatar − 8·(r + 2)** on each
axis, and grows only if that corner is inside the box **[lab]**:

| Avatar, box | Radius 2 | Radius 3 | Radius 4 | Radius 6 |
|---|---|---|---|---|
| (128, −128), ±100 | ~(97, −97) | ~(88, −89) | ~(81, −80) | ~(64, −63) |
| (136, −136), ±100 | none (corner 104 is outside) | ~(93, −93) | ~(84, −84) | — |
| (128, −128), ±90 | none (corner 96 is outside) | ~(83, −84) | — | — |

Measured centres sit about 3–4 units inside the predicted corner, which fits copies scattered
within ±4 units of it. Radius 1 predicts corner 104 for an avatar at 128, which is outside a
±100 box, matching no growth. So the clump is tied to the avatar, not to the box corner: moving
the avatar 8 units out moved it one cell, and radius 2 then grew nothing. Nothing grew nearer the
avatar. Why the client grows this one far cell, rather than the in-range cells, is still open
**[inf]**.

## Live

The real 5.12 client (GDI renderer) accepted this layout for all three classes: each ghost was
created and the client stayed up, for radius 1, 4, 64 and 100 cells, grid counts 0/20 and 25/25,
`allowonterrain` 0 and `hidereplications` 1. Nothing about the replicator was logged. **[lab]**
No copies of the shape were seen in any of these runs, but the ground under the object was about
100 units above the camera, so the copies may have been out of view. A rerun on fresh flat ground (a `TerrainBlock` with no chunks) with the camera 15 units away
also grew nothing visible, with grid counts 5/5 and 20/20 and with no `TerrainBlock`. All these
runs used the box (−1,−1) to (1,1), which allows a single cell, and the flat block had no
heights for the rays to hit; with a wide box over streamed terrain, cover grows. **[lab]**

**Cover grows** on the real 5.12 client (GDI renderer) under these conditions: a
`DynamicShapeReplicator` over streamed hilly terrain, with box (−256,−256) to (256,256), radius 4
cells, 5 objects per cell, `labcube.3ds` at scale 3, slope 90 and all allow flags on. The client
drew a dense carpet of cube copies, each scaled and randomly turned, sitting on the terrain and
following its slopes around the player (about 19% of the frame changed against the same scene
without the replicator). This confirms the layout above, and that the earlier misses came from
the one-cell box and the missing ground. **[lab]** With 20 objects per cell the
covered area grew only a little, since at scale 3 the copies from 5 per cell already nearly
fill the near cells. With `allowonterrain` off and `allowonstatics` on, nothing was placed on
the bare terrain. **[lab]**

Further runs on the same terrain, each changing one value against that base **[lab]**:

| Change | Result |
|---|---|
| same world sent again | pixel-identical cover |
| a second 5.12 client at the same spot | identical cover to the first client |
| `seed` + 1 | a fully different scatter of about the same density |
| `boxmin.x` = 128 | cover only on the side with x ≥ 128 |
| `offsetz` 5 | the copies float 5 units above the ground |
| `shaperotatemax` (0,0,0) | every copy faces the same way, in the same spots |
| `aligntoterrain` on | the copies tilt to the slope |
| `hidereplications` on | all cover gone; only the replicator's own shape remains |
| radius 1 / 8 cells | much less / much more ground covered |
| `shapefiles` `a.3ds,b.3ds` | both shapes appear, picked per copy, at the same positions |
| `DynamicGrass` or `DynamicGrassReplicator` with the same values | the ghost is created and nothing is drawn |

So the cover is the same for every client that gets the same values. The two grass classes take
the same update but do not draw a `.3ds` this way; what they draw is still open. **[lab]** Statically, the grass
classes replace the cell-filling and the grid-count setters (their counts are clamped to 0–100
per cell instead of 0–20) and build their own geometry instead of placing shapes, so they expect textures rather than shape files.

With a texture name (`lp_white.png`) in `shapefiles` and a radius of at least ~8 cells (see the
radius correction below), both grass classes
**draw**: many small flat pieces lying on the ground, over the same area the shapes covered,
denser at 50 per cell than at 5. Under the GDI renderer they showed untextured. A 64×64 RGBA
texture that is almost all transparent drew nothing visible. Both textures were already cached,
and grass never asked the server for its texture. When the server pushes the grass textures
(`graal3dpushgrass`, on by default), the texture arrives over TCP right after the 3D link,
quietly (no server log line); without it only `heights.info` is sent. With this timing grass does not
draw in the very first frame (that frame is untextured), only on a later visit once the texture
is cached. Holding the grass ghosts back by up to 10 s after the rest of the world
(`graal3dgrassdelay`) does not change this, which points at the client building its grass once at
mission load **[inf]**. **[lab]** But when the server pushes the grass texture one channel earlier,
over the TCP link at login rather than at the 3D link, grass **does** draw on the very first visit:
on a fresh cache the texture lands in the client's cache before the 3D mission loads (it is not
listed among the 3D file downloads), and the first frame then shows the full grass field that the
later-push timing left blank. The terrain under the camera is still untextured white on that first
frame; only the grass is added. So pre-loading the texture before mission load lets the one grass
pass at mission load draw it. **[lab]** Under a full OpenGL renderer (Mesa llvmpipe)
the same runs draw a lit white patch with `lp_white.png`, and the nearly transparent texture
draws as soft round glowing spots, so the empty GDI result was the renderer. A ground-level close-up shows the grass pieces are flat-to-tilted quads lying on the ground at per-piece random yaw and tilt (their top faces foreshorten), not upright or camera-facing cards; each is on the order of a metre across at scale 1, and raising the scale enlarges the quad in both width and height. **[lab]** An overhead shot with a 1-unit reference cube as a ruler confirms this: from straight above each piece is a filled rotated square (a diamond), not the thin line a vertical card would show edge-on, so the cards lie flat on the ground. A scale-2 piece measures about 1.8 × 1.55 units across its bounding box; since the square is rotated, its true edge is about that over √2, roughly 1.25 units at scale 2, so near 0.6 units at scale 1. The piece is roughly square (width ≈ height), not a wider-than-tall blade, and larger than earlier guessed. **[lab]** The per-piece orientation is an independent random, not driven by `shaperotatemin`/`shaperotatemax`: a patch with the rotation range pinned to 0 and one with the default 0–360 are essentially identical (about 0.7% of pixels differ, edge noise), with the cards fanned to varied yaw in both. So grass carries its own orientation and ignores the replicator's `shaperotate` range. **[lab]**

**The drawing runs all used a radius of at least ~8 cells; on the radius-4 shape base the grass
classes draw nothing.** A later exhaustive bisection (real 5.12 under Mesa against seihai-gserver
#216/#218, both a `rawobject` replay of the exact create and plain `replicator` lines, the control
object off the origin) settled why every radius-4 grass line here drew 0 px: the 5.12 grass
classes build **no** quads below a radius of about 8 cells, while `DynamicShapeReplicator` scatters
at radius 4. Stepping only the radius was decisive — radius 4 with any count (5 or 10) grew
nothing, while radius 8 with 4, 5 or 20 per cell drew a full patch — and scale, the texture
name/path/content, ghost order, `terrainalignment`, the allow flags, the box z-range, and the
GameObject section set were each ruled out on their own, with the radius the one thing that
mattered. So the grass that drew above was a radius-8 line (the C++ fork's
`replicator DynamicGrass 128 -128 0 8 …`), not the radius-4 shape base. The exact threshold sits
somewhere in 5–8 cells (not narrowed). End to end, a plain
`replicator DynamicGrass 0 0 0 8 10 10 lp_white.png` draws while the same line at radius 4 draws
nothing (tested with the camera 20 and 40 units up, so it is not view-distance culling).
seihai-gserver #218 floors grass lines to 8 cells (shape replicators keep theirs) with a
start-up warning, after which the original radius-4 line draws. **[lab]** (T3D-048.)

On 4.20r8 the replicator ghost is created without a crash or error, but with the camera kept
250 units up (to avoid 4.20r8's terrain crash) no cover was in frame. With the camera pitched down over the
ground around the player (radius 8, scale 10) still nothing grew, against the same view without
the replicator. So 4.20r8 takes the ghost but grows no cover, under GDI and under Mesa alike. **[lab]**
