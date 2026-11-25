# The original TerrainGenerator compared with servertools `gen terrain` (2026-11-25)

Lab: every distinct TerrainGenerator build in the archives, run inside a lab
VM with the Hills, Isles and Peaks presets. Each output was compared with
servertools `gen terrain` and fed to servertools `gen 3d`. Behaviour only.
The binaries and outputs stay in the lab share. Board row: T3D-043. **[lab]**

## Builds

There are five distinct builds, dated 2001-08-01, 2001-08-05, 2002-01-08,
2002-01-09 and 2003-12-16. All five write the same gmap for the same input.
The only difference is that the 2003 build leaves out a trailing blank line.

## What the original writes

- **HEIGHTMAP.** One comma-separated height for each level corner, so a map
  of w x h levels has (w+1) x (h+1) values.
- **RANDOMSEEDS.** A block after the heightmap with one seed for each level.
- **Level files.** No build writes a HEIGHTS block into the `.nw` files.
  The 2001 and 2002 builds write tile-0 BOARD rows plus the links between
  levels. The 2003 build writes the links only.

## How servertools `gen terrain` differs

| Field | Original | servertools `gen terrain` |
|---|---|---|
| Heightmap grid | (w+1) x (h+1), one per level corner | (8w+1)², one per tile corner |
| Separator | comma | space |
| RANDOMSEEDS | present, one per level | absent |
| LEVELNAMES | absent | present |
| Level naming | original scheme | `worldA00` style |
| HEIGHTS in each level | none | 9x9 block |
| LEVHEIGHT | scaled | not scaled |

With the same seed, servertools does not reproduce the original map.

## `gen 3d` on original gmaps

servertools `gen 3d` (PR #116) refuses all three original gmaps. It first
fails on the commas. With the commas changed to spaces, it fails on the grid
size, because it expects the (8w+1)² grid. So there were no chunk stamps to
compare. Reading an original gmap would need `gen 3d` to accept the
corner-per-level grid and either interpolate it or take the level HEIGHTS
from somewhere else.

**Update.** servertools PR #118 now reads the original gmaps and interpolates
the corners. With it, the chunks outside the levels match (190 to 207 of 256
per map) and every chunk over the levels differs, as expected for a plane
interpolated from the corners.
