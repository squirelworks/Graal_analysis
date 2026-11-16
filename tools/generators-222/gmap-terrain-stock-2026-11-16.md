# Gmap terrain generator: stock LCG and height roles

Date: 2026-11-16. Tags: **[bin]** for stock `TerrainGenerator.exe`; **[file]** for gmap keys already published; **[inf]** where byte-identical window replay is unproven.

Leads-only. No third-party code. Extends [`tools/generators-222/README.md`](../tools/generators-222/README.md) and the gmap key tables in the manual.

## Stock tool present

The 2.22-with-editors archive includes stock **`TerrainGenerator.exe`**. This pass is not blocked on a missing binary. **[file]**

## Random source — Delphi LCG

Stock `TerrainGenerator.exe` contains the classic Delphi LCG multiplier **134775813** in the image (two LE dwords). That matches:

- the published GA Python reference (`tools/generators-222/terrain.py`): `seed = seed * 134775813 + 1`, unit in `[0,1)` then signed displacement
- the usual Delphi `Random` step

So the stock window is on the **same PRNG family**, not a different generator. Offsets are omitted here. **[bin]**

## What the gmap carries (already published keys)

Terrain maps carry `GENSEED`, `GENBASE`, `GENEVENBORDERS`, `GENHEIGHT`, `GENCHAOS`, `LEVHEIGHT`, `LEVCHAOS`, `HEIGHTMAP`…`HEIGHTMAPEND`, and `RANDOMSEEDS`…`RANDOMSEEDSEND`, plus level names / `MAPIMG`. **[bin][file]**

Roles that matter for a faithful **reader**:

| Input | Role |
| --- | --- |
| `HEIGHTMAP` | Coarse **(WIDTH+1)×(HEIGHT+1)** corner/control heights |
| `GENSEED` | Shared seed for **border** continuity |
| `RANDOMSEEDS` | One uint seed **per level cell** for interior detail |
| `GEN*` / `LEV*` height & chaos | Amplitude and decay on recursive midpoint steps |
| Per-level `HEIGHTS` 9×9 | Coarse / override layer the stock tool also writes |

A third-party runtime path reconstructs a **65×65** vertex field per level from those borders + per-level seeds (tile step 64), then may soften optional 9×9 overrides into that grid. Our GA `terrain.py` is a **writer-side** plasma reference that emits 9×9 `HEIGHTS` and derived seeds — explicitly **not** claimed byte-identical to the Delphi window. Treat writer vs reader roles separately. **[bin][inf]**

## Seihai / notes impact

- Parse GEN* / HEIGHTMAP / RANDOMSEEDS when fidelity needs generated maps.
- Either keep 9×9 as today or implement the 65×65 border+quadrant fill with the Delphi LCG above.
- Do **not** treat GA `terrain.py` plasma as a drop-in of a load-time reconstruct path.

## Still open

- Byte-identical save compare: stock window vs our writer on a fixed seed. **[lab]**
- Exact `GENEVENBORDERS` / `GENBASE` interaction on stock border fill. **[bin]/[lab]**
