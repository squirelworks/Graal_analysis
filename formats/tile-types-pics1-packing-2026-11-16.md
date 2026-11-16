# Tile types and `pics1` id packing (stock vs a flat 4096 file)

Date: 2026-11-16. Tags: **[file]** for measured sheets; **[bin]** for engine strings; **[inf]** where draw-on-miss behaviour is unproven.

Leads-only against a third-party claim that clients load a flat `tiletypes0.dat` of 4096 type bytes.

## `pics1` geometry (closed for measured focus sheets)

| Build / tree | Sheet | Size |
| --- | --- | --- |
| 2.22 | `pics1.png` | **2048×512** |
| 4.20r8 | `pics1.png` | **2048×512** |
| 5.00r7 | `pics1.png` | **2048×512** |
| 5.00r7 | `picso.png` (offline / type-1 sheet) | **1024×512** |

Packing for a 16×16 tile cell on that atlas family:

- strip width 256 px → 16 columns × 16 px
- strip height 512 px → 32 rows × 16 px
- **512** ids per strip; eight strips on 2048×512 → ids **0–4095**

`col = (t % 16) + (t // 512) * 16`, `row = (t // 16) % 32`, source `(col·16, row·16, 16, 16)`. **[file]**

## Where “types” live on stock clients

| Build / path | What holds walk / type data | Flat 4096-byte `tiletypes0.dat`? |
| --- | --- | --- |
| **2.22** | `arrays.dat` id allow-lists + `levels/tiledefs/tiledefs*.txt` | **No** in tree |
| **3.04** | Lists compiled into the executable | **No** |
| **4.20r8 / 5.00r7 engines** | `tiledefs` / `addtiledef` / `pics1.png` strings; **no** `tiletypes0` / `arrays.dat` literals | **No** flat type file in engine strings |
| **5.00r7 data** | `tiledefs*.txt` rows `image,prefix,type[,x,y]` | Sheet selection, not 4096 types |

A **4096×1-byte** table does appear in some **server** headers and in third-party tooling, but **stock focus clients do not load `tiletypes0.dat`**. Classic walkability is id allow-lists (2.x) plus sheet-type / tiledefs rules (3.x–5.x). **[bin][file]**

## Ids 2048–4095 on a smaller sheet

On `picso.png` **1024×512** (four strips), the same packing only addresses ids **0–2047**. Id **2048** would start at source x **1024** — outside that sheet. Whether the engine clamps, wraps, skips, or samples off-sheet is still open. **[file][inf]**

## Still open

- Live / static draw behaviour for high ids on type-1/2 sheets. **[bin]/[lab]**
- Per-build clamp of the type byte table if any client path ever loads one (none found on focus builds). **[bin]**
