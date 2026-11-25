# Graal 5.12 replicator update (`DynamicShapeReplicator`, `DynamicGrass`, `DynamicGrassReplicator`)

Date: 2026-11-25. Client: the real 5.12 `Graal3DEngine.dll` (SHA-256 `04f7a133…`), static read.
Tags as in `README.md`: **[bin]** read from that binary for behaviour, **[inf]** inferred,
**[lab]** seen live (none yet). Nothing here is decompiled text. Encoding terms as in
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
- `shapefiles` is kept as one string; how a list of several shapes is separated is not read
  yet. **[inf]**
- The meanings follow the names: allowed surfaces, a slope limit (degrees **[inf]**), optional
  alignment to the terrain normal, a height offset, and per-object random scale and rotation
  between the min and max vectors. `hidereplications` hides the cover without dropping the
  object. **[inf]**

Open: a live ghost of a `DynamicShapeReplicator` beside the terrain world, varying radius, grid
counts and the allow flags.
