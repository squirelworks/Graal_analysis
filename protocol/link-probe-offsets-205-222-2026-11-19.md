# 2.05 and 2.22 edge-link probe offsets

Date: 2026-11-19. Evidence: **[bin]** (a disassembler read of the real 2.05 rev 2 `Graal.exe`
(2.0.5.2) and the Windows 2.22 client, on the lab host B; no client run). Answers the main part
of App. E#308 and the probe-offset row of [link-probe-bigmap-status.md](link-probe-bigmap-status.md).

## Method

The edge-link probe routine in 2.05 was found through its edge constant (63.5), and the probe
point was traced back to a per-facing offset table. The same table was then searched for in the
2.22 executable as a whole constant block.

## Probe offsets

Before the edge tests, the client adds a per-facing offset to the player's position. Values are in
tiles.

| Facing | Index | x offset | y offset |
| --- | ---: | ---: | ---: |
| up | 0 | +1.5 | +1.0 |
| left | 1 | +0.5 | +2.0 |
| down | 2 | +1.5 | +3.0 |
| right | 3 | +2.5 | +2.0 |

- In 2.22, the 64-byte constant block that holds the table is byte-for-byte the same as in 2.05,
  and it occurs once in each executable. So 2.22 keeps 2.05's offsets.
- The edge tests in the routine match the documented 2.05 rules
  ([03-edge-links.md](../client-internals/decomp-findings-2026-10-28/03-edge-links.md)):
  - West fires at probe x ≤ 0 or player x < −2.5, and east at probe x ≥ 64 or player x > 63.5.
  - North fires at probe y ≤ 0 or player y < −3.0, and south at probe y ≥ 64 or player y > 63.0.
  - Arrival is ±64 on the axis crossed.

## Walking past the edge with the neighbour loaded

A per-edge "neighbour not loaded" flag guards the rectangle test. When the neighbour is loaded,
only the probe threshold and hard-limit test applies, so the player can walk past the edge (x below
0, x above 63.5 and so on) until the threshold fires. This is a code read; no crossing was run.

## Still open

- ~~The global flag that skips building the 3 x 3 neighbour table.~~ Settled 2026-11-20: the
  `dontconnectlevels` option ([sixth batch](../client-internals/static-reads-appendix-e-2026-11-20-f.md#the-neighbour-table-builder-and-its-skip-flags-e308)).
- ~~Whether `PLO_BIGMAP` (171) on 2.22 installs the same grid as `maps/bigmap.txt`.~~ Settled
  2026-11-20: it does, through the same loader ([sixth batch](../client-internals/static-reads-appendix-e-2026-11-20-f.md#plo_bigmap-171-and-the-gs1-setmap-command)).
- A lab crossing on 2.22 with a big map installed by 171.
