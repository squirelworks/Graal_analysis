# Which gmap readers take `HEIGHTS`: by engine component

Date: 2026-11-19. Evidence: **[bin]** (a read-only look at the gmap section tokens of installed
client components on the lab host B, with no client run). Closes App. E#606.

## Question

Windows 4.04r2 and four Mac PowerPC builds read both the coarse `HEIGHTMAP` and named per-level
`HEIGHTS` blocks inside a gmap ([gmap-heights-404r2.md](gmap-heights-404r2.md),
[gmap-heights-mac-ppc.md](gmap-heights-mac-ppc.md)). The open question was whether every 4.x
and later gmap reader does.

## Method

For each installed build, the gmap text parser of each engine component was found by the section
tokens it compares against (`LEVELNAMES`, `LEVELNAMESEND`, `WIDTH`, `HEIGHTMAP`, `HEIGHTS`,
`HEIGHTSEND`). Any other tokens next to them in the same parser were noted. Component files were
compared by size and digest across builds.

## Result

| Component | Builds | `LEVELNAMES` | `HEIGHTMAP` | `HEIGHTS` … `HEIGHTSEND` | Other gmap tokens |
| --- | --- | --- | --- | --- | --- |
| Linux 2D engine library (`libgraalengine.so`) | 4.04r2, 4.11, 4.20r6, 4.20r8, 5.00r7, 5.12; one identical file in all six | yes | no | no | none |
| Linux 3D client binary (`graal`) | 4.20r6 | yes | yes | yes | none |
| Windows engine DLLs (`GraalEngine.dll`, `Graal3DEngine.dll`) | 4.20r8, 5.00r7 | yes | yes | yes | none |
| Merged client binary | 6.03r7 | yes | yes | yes | `NOAUTOMAPPING`, `MINIMAPIMG` |

## What this settles

- A gmap can carry per-level `HEIGHTS` blocks, but only the 3D-capable engine components read
  them, along with the merged 6.x client. The plain Linux 2D engine of 4.04r2 to 5.12 has no
  `HEIGHTMAP` or `HEIGHTS` section at all and reads only the level-name grid.
- So support depends on the component, not on the version. The earlier guess that "every 4.x and
  later gmap reader accepts both forms" is false.
- The Windows 4.04r2 and Mac PowerPC readers that take both forms fit this pattern, because they
  are 3D-capable components.
- `NOAUTOMAPPING` and `MINIMAPIMG` appear first in the 6.03r7 parser and in none of the 4.x or 5.x
  components checked.

## Limits

- This is a token-level read: it shows whether a component's parser has a section, not how each
  reader stores the values. Each reader was not disassembled line by line.
- The rendering of `HEIGHTS`, server support and the salvage author's intent stay as open as
  [gmap-heights-404r2.md](gmap-heights-404r2.md#correction-and-limits) leaves them.
