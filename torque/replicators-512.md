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
is then placed by casting rays onto the allowed surfaces. **[bin]** Cover only fills around the control object's own spot: on one flat streamed terrain the same line
grew a full carpet at the control object's (128, −128) but nothing at (4, 4), with every other
field held. It is not a terrain gap (terrain draws at both spots) and does not mirror across the
grid: a control at (−124, 132) is as dead as (4, 4), and only the player's spawn position
(128, −128) has ever grown cover, on both the Peaks and the flat terrain. This matches the binary: each tick the grid is centred on the game connection's **control
object** (the player avatar), read from its transform, not on the camera or the replicator, so
cover grows where the avatar actually is, which in these tests was always the spawn (128, −128).
**[bin][lab]** So a box of (−1,−1) to (1,1)
allows only the one cell whose corner is at the world origin; a server wanting cover over an area
must send that area as the box, in world units. **[bin]**

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

With a texture name (`lp_white.png`) in `shapefiles` and the same update, both grass classes
**draw**: many small flat pieces lying on the ground, over the same area the shapes covered,
denser at 50 per cell than at 5. Under the GDI renderer they showed untextured. A 64×64 RGBA
texture that is almost all transparent drew nothing visible. Both textures were already cached,
and grass never asked the server for its texture. When the server pushes the grass textures
(`graal3dpushgrass`, on by default), the texture arrives over TCP right after the 3D link,
quietly (no server log line); without it only `heights.info` is sent. Either way grass does not
draw in the very first frame (that frame is untextured), only on a later visit once the texture
is cached. Holding the grass ghosts back by up to 10 s after the rest of the world
(`graal3dgrassdelay`) does not change this, which points at the client building its grass once at
mission load **[inf]**. **[lab]** Under a full OpenGL renderer (Mesa llvmpipe)
the same runs draw a lit white patch with `lp_white.png`, and the nearly transparent texture
draws as soft round glowing spots, so the empty GDI result was the renderer. A ground-level close-up shows the grass pieces are flat-to-tilted quads lying on the ground at per-piece random yaw and tilt (their top faces foreshorten), not upright or camera-facing cards; each is on the order of a metre across at scale 1, and raising the scale enlarges the quad in both width and height. **[lab]**

On 4.20r8 the replicator ghost is created without a crash or error, but with the camera kept
250 units up (to avoid 4.20r8's terrain crash) no cover was in frame. With the camera pitched down over the
ground around the player (radius 8, scale 10) still nothing grew, against the same view without
the replicator. So 4.20r8 takes the ghost but grows no cover, under GDI and under Mesa alike. **[lab]**
