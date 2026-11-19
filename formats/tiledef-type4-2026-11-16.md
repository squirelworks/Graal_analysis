# Tiledef type 4 (sheet line), 2.22

Date: 2026-11-16. Tracker: [#619](https://github.com/squirelworks/Graal_analysis/issues/619) (b). Tags: **[file][bin][2.22][doc]**.

Settles what can be measured without a live walk/draw run: how type **4** appears in install `tiledefs` lines, what the 2.22 loader stores, and how that relates to the already-published walk-kind switch. The draw and walk consumer was measured on a live 2.22 on 2026-11-19 ([below](#live-result-2026-11-19)).

## Line shape

Install and script forms agree on:

```text
image,prefix,type[,x,y]
```

The 2.22 file loader keeps a row when it has at least image, prefix and a numeric type. When more than four comma fields are present it also stores **x** then **y** as integers. **[bin]**

Vendor text for `addtiledef` only names type **0** (old Graal) and **1** (new order, “description later”). The separate command `addtiledef2` takes image, prefix, **x**, **y** and pastes a partial image onto the base sheet. **[doc]** (`newfeatures2001.txt` in the 2.22 tree)

## Walk kinds already known (not type 4)

The 2.05 tile-type tests (carried for 2.22 lists) pick a rule from the **tileset kind**:

| Kind | Rule |
| --- | --- |
| 0 | `arrays.dat` allow-lists |
| 1 or 2 | fixed id-range “new kind” grid |
| 5 | no board rule; NPC shapes only |

**Type 4 is not in that switch.** A sheet line with type 4 is therefore not explained by the published walk table alone. **[2.22]** (`client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md`)

## What install files actually use

The 2.22 adventure tiledefs file keeps the default row `pics1.png,,0,0,0` and about seventeen prefixed overrides. Every override is **type 4**, with **x** in `{1344, 1536, 1728}` and **y** in `{0, 80}` (examples: `alienpics.png` @ 1728,0; `intreepics1.png` @ 1344,0; `zcpics1.png` @ 1536,80). Offline uses type **1** only (`picso.png,offlinetutorial,1,0,0`). **[file]**

`pics1.png` on the measured 2.22 tree is **2048×512**. Those x values are whole 16-pixel columns (84 / 96 / 108). **[file]** (`formats/tile-types-pics1-packing-2026-11-16.md`)

## Reading for implementers

| Fact | Status |
| --- | --- |
| Parser stores type and optional x,y | measured **[bin]** |
| Type 0 / 1 meanings in vendor `addtiledef` text | measured **[doc]** |
| Type 4 absent from walk-kind switch 0 / 1\|2 / 5 | measured **[2.22]** |
| Type 4 install rows carry large x (pixel) offsets | measured **[file]** |
| Type 4 is draw-only: it pastes the image into the tile sheet at pixel (x, y); walking follows the board's tile codes | measured **[lab]** (2026-11-19) |

Do not treat type 4 as bed-top collision type 4 (`arrays.dat` / tile-type byte 4). That is a different namespace. **[2.22]**

## Live result (2026-11-19)

Real 2.22 offline under Wine (virtual desktop, GDI renderer), F5 on a test level with
`tiledefsOffline` lines and a 2048 × 512 overlay image. Screenshots are kept privately.
**[lab]** ([run](../live-runs/open-issues-2026-11-19/README.md#8-619-tiledef-type-4-on-222))

- **The image has to be an 8-bit palette PNG.** A 24-bit PNG is ignored without a message:
  a type-4 line then changes nothing, and a type-0 line draws every tile black.
- **Type 0 and type 1** take the whole tile sheet from the image, each tile at its own sheet
  position.
- **Type 4 pastes the image into the tile sheet at pixel offset (x, y).** The stock sheet stays
  wherever the image does not reach.

  | Line offset | Where the image's first column lands |
  | --- | --- |
  | (256, 0) | sheet column 16, row 0 |
  | (512, 0) | sheet column 32, row 0 |
  | (256, 64) | sheet column 16, row 4 |
  | (264, 0) | column 16 stays stock; column 17 shows the right half of image column 0 and the left half of image column 1 |

  So x and y are **pixels**, not tile columns. The install rows only happen to use multiples
  of 16. A tile that straddles the image's left edge keeps its stock picture.
- **Walking follows the board's tile code, not the picture.** A row of rock tiles blocked the
  player at the same place with the stock sheet, with a type-4 overlay drawn over it, and with
  type 0. Grass stayed walkable in all three. Water was not tested on its own.

So type 4 behaves like the vendor `addtiledef2` (paste a partial image onto the base sheet)
and is not a walk kind.

## Open

- [x] ~~End-to-end draw path for a type-4 prefix (blit at x,y vs full-sheet replace).~~ Blit at pixel (x, y) over the stock sheet ([live result](#live-result-2026-11-19)). **[lab]**
- [x] ~~Whether `tiletype()` / wall tests on a type-4 sheet follow kind 0, kind 1/2, or fail closed.~~ The board's tile codes decide; the pasted picture does not ([live result](#live-result-2026-11-19)). **[lab]**
- [ ] Water and other walk kinds under a type-4 overlay, and type-4 lines on builds other than 2.22.
