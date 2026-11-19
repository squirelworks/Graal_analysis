# Tile id to `pics1.png` position: a render test

Date: 2026-11-19. Evidence: **[test]** (a render of real level files with a real tile sheet, in the
cloud, no client run). Closes App. E#102.

## Question

Two formulas for where tile id `t` sits on `pics1.png` were on record:

| Claim | Column | Row |
| --- | --- | --- |
| A (`formats/tiletypes.txt`, before this note) | `t % 128` | `t / 128` |
| B (`client-internals/client-assets.md`, and the Windows 4.04r2 tile draw) | `(t % 16) + (t / 512) * 16` | `(t / 16) % 32` |

Claim B is eight side-by-side blocks of 512 ids, each 16 columns by 32 rows. Pixel position is
`(column * 16, row * 16)` in both.

## Method

- Inputs: the `pics1.png` and the two shipped level files (`start1.graal`, `house1.graal`, both
  `GR-V1.03`) of one 1.41-era installed folder held by the owner. The sheet in that folder is
  1856 x 512 pixels, palette mode.
- Each 64 x 64 board was decoded with [`grv1-decoder/grv1.py`](grv1-decoder/grv1.py), then drawn
  twice, once with each formula, by pasting the 16 x 16 cell of each tile into a 1024 x 1024 image.
- The images were compared by eye, and the number of ids whose cell falls outside the sheet was
  counted.

## Result

| Level | Highest id | Cells off the sheet, A | Cells off the sheet, B | Picture, A | Picture, B |
| --- | ---: | ---: | ---: | --- | --- |
| `start1.graal` | 2135 | 2660 of 4096 | 0 | noise: unrelated tile fragments in place of every wall and floor | a coherent cave: rock walls, a grass room, a floor corridor, a door and two torches |
| `house1.graal` | 1899 | 3736 of 4096 | 0 | noise | a coherent interior |

Claim B draws both levels as levels. Claim A puts most cells off the sheet and draws the rest from
the wrong places. So Claim B is the layout, and the static read of the 4.04r2 draw path (which
computes Claim B before any tiledef remapping) agrees. **[test][bin]**

Claim A was a guess that the sheet is a plain 128-column grid. `formats/tiletypes.txt` is
corrected in the same change.

## Limits

- One sheet and two levels from one build. The 4.04r2 static read covers the later client; the
  manual already followed Claim B for every build (→ §3.5).
- Rendered images stay with the owner; only these counts are published.
