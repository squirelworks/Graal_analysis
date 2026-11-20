# 2.x link probe offsets, `PLO_BIGMAP`, and gmap entry save (gap #34)

Date: 2026-11-16. Research-gaps / research-list rank **#34** (focus 2.220). E#308 / E#314.

**Question:** What are the per-facing link probe offsets, the flag that skips the neighbour table, how `PLO_BIGMAP` (171) interacts with offline bigmap, and how gmap entry save behaves on death/crossing?

**Answer so far:**

| Piece | Status | Evidence |
|---|---|---|
| Edge-link fire rules and ±64 seam arrivals (W/E/N/S) | **Settled for 2.05** | `client-internals/decomp-findings-2026-10-28/03-edge-links.md` **[bin]** |
| Neighbour 3×3 filled from big-map text grid on level entry | **Settled for 2.05** | same **[bin]** |
| Per-facing **probe offsets** (player + offset before rectangle tests) | **Settled for 2.05 and 2.22** (2026-11-19): up (+1.5, +1.0), left (+0.5, +2.0), down (+1.5, +3.0), right (+2.5, +2.0); the table is identical in both | [`link-probe-offsets-205-222-2026-11-19.md`](link-probe-offsets-205-222-2026-11-19.md) **[bin]** |
| Flag that **skips** the neighbour-table fill | **Open** (unidentified) | E#308 **[bin]** |
| Whether 2.22 uses `PLO_BIGMAP` (171) the same way 2.05 uses offline `bigmap.txt` | **Open** | E#308 — 2.22/2.31 not read there **[bin]** |
| Walking past the edge before the link fires when neighbour is loaded | **Read** (2026-11-19): with the neighbour loaded only the probe threshold applies; no crossing run yet | [`link-probe-offsets-205-222-2026-11-19.md`](link-probe-offsets-205-222-2026-11-19.md) **[bin]** |
| Gmap entry / death save (E#314) | **Open** | needs S+L on 2.22 |

Tags: **[bin][doc]**. No new binary session in this pass. Focus 2.220 still needs its own S of the probe table.

## What a 2.22 lab should confirm

1. S: probe offset table and neighbour-skip flag in 2.22 (and whether 171 installs the same grid as `maps/bigmap.txt`).
2. L: crossing each edge on a 2×2 gmap with neighbour loaded vs not; death on each side of a seam (E#314).
3. Fold with neighbour-framing / gmap re-send labs where the same fixture applies.

## Still open

| Item | Status |
|---|---|
| Numeric probe offsets per facing on 2.22 | **Settled** (2026-11-19, same table as 2.05) |
| Neighbour-table skip flag identity | **Open** S |
| `PLO_BIGMAP` vs offline bigmap on 2.22 | **Open** S then L |
| Entry-point save across gmap death/crossing (E#314) | **Open** L |
