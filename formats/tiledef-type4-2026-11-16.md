# Tiledef type 4 (sheet line), 2.22

Date: 2026-11-16. Tracker: [#619](https://github.com/squirelworks/Graal_analysis/issues/619) (b). Tags: **[file][bin][2.22][doc]**.

Settles what can be measured without a live walk/draw run: how type **4** appears in install `tiledefs` lines, what the 2.22 loader stores, and how that relates to the already-published walk-kind switch. It does **not** yet close the draw/walk consumer path end to end.

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
| Whether type 4 is draw-only (addtiledef2-like), a new walk kind, or both | **open** — needs a consumer trace or offline lab on a type-4 prefix level |

Do not treat type 4 as bed-top collision type 4 (`arrays.dat` / tile-type byte 4). That is a different namespace. **[2.22]**

## Open

- End-to-end draw path for a type-4 prefix (blit at x,y vs full-sheet replace). **[bin][lab]**
- Whether `tiletype()` / wall tests on a type-4 sheet follow kind 0, kind 1/2, or fail closed. **[lab]**
