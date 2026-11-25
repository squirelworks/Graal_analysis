# lightScene and lightmap caching: retained in 5.12, but its interior content is gone (T3D-092)

Date: 2026-11-25. Lab of a lit mission on native Linux 4.20r6 (5.12-class, protocol 24, g3d420 route) and native Linux 4.04r2 (protocol 19, g3d404 route), plus a read of the `SceneLighting` strings and GS2 dumps in each engine. Linux 4.20r6 is 3D-equal to Windows 4.20r8 ([T3D-004](3d-engines-5007-512-and-403-411-2026-11-25.md)). Board row: [T3D-092](3d-capability-board.tsv). Follows [T3D-111](3d-state-authority-420r6-2026-11-25.md) (Sun ghost drives lighting; no sun → near-black shape) and [T3D-081](3d-object-classes-by-build-2026-11-25.md) (InteriorInstance is 4.04r2-only).

Builds run live: 4.20r6 (24) and 4.04r2 (19). Relied on prior note: 5.00r7 / true 5.12 — class- and GS2-equal to 4.20r6 (same `lightScene` entries), so same behaviour.

## Disk cache after a lit mission **[lab]**

A full lit mission (Sun + Sky + a shape, through Mission Lighting and ~15 s beyond) into a fresh client user folder, then a diff:

| Build | Mission phases | Lighting artifact on disk? | What was written |
| --- | --- | --- | --- |
| 4.20r6 | 2-phase (Download Ghost Objects → Mission Lighting, "Mission lighting done") | none | only downloaded assets + bookkeeping: the shapes (`.3ds` under `levels3d/images/` and `…/global/`), six sky faces (`levels3d/images/sky/`), `basepackage.gupd` (`updatepackages/`), `console.log`, a small `.registry`. (A `.cache/mesa_…` tree is the host GL driver's shader cache, not a Graal file.) |
| 4.04r2 | 3-phase (Download Datablocks → Download Ghost Objects → Mission Lighting, "Mission lighting done") | none | the shape (`.dts` under `levels3d/shapes/`), six sky faces, `basepackage.gupd`, `console.log`, `.registry`. |

**Neither build wrote any lighting file** — no lightmap, no baked-mission cache, nothing new after the lighting phase. Both lit missions completed with zero lighting output on disk.

**Why:** the lightmap-cache machinery *exists* in both engines (below), but it bakes only for **interiors and terrain**, and this route serves neither (InteriorInstance is 4.04r2-only and gone from 5.12, [T3D-081](3d-object-classes-by-build-2026-11-25.md); the server sends no terrain). With nothing bakeable, the lighting phase has nothing to compute to disk. "No file written" is the correct result **for a Sun + Sky + shape scene**, not evidence the engine can never write a lightmap.

## What lightScene is, per build **[bin]**

Both 4.20r6 (5.12-class) and 4.04r2 carry the **same `SceneLighting` subsystem** — it was **not** stripped from 5.12:

- `lightScene()` is a GS2 console function (returns a boolean), present in the 4.20r8/5.00r7/5.12 GS2 dumps and both binaries.
- a `$SceneLighting::lightingProgress` value and a `SceneLightingProcessEvent` (runs incrementally over frames).
- the lighter works through InteriorProxy, TerrainProxy and an ObjectProxy — it bakes lighting for **interiors and terrain**, not arbitrary shapes.
- lightmap persistence: both binaries carry "Loaded lightmap for … from file", "Failed to load lightmap of …, will regenerate it", and a lightmap filename pattern `<name>_<n>_lm_<n>.png` — a baked lightmap saved as a PNG per object/interior and reloaded next time.
- 4.04r2 additionally surfaces terrain-lighting prefs (allow-lexel-splits, generate-level) and a max-hardware-lights pref; 4.20r6's core SceneLighting is the same minus some of those surfacing in the scan.

| | 4.04r2 (protocol 19) | 5.12 / 4.20r6 (protocol 24) |
| --- | --- | --- |
| `lightScene` / SceneLighting present? | yes | yes — retained |
| what it bakes | interior + terrain lightmaps (TGE mission lighting) | same subsystem, but InteriorInstance is gone ([T3D-081](3d-object-classes-by-build-2026-11-25.md)), so only terrain could be lit — and terrain isn't networked on this route |
| lightmap caching | writes/loads `*_lm_*.png` per interior/object | same code path present |
| lighting of a plain shape | lit by the scene's directional/sun light, not a baked lightmap | the Sun ghost's directional light, applied live per frame ([T3D-111](3d-state-authority-420r6-2026-11-25.md)) — no bake |
| the "Mission Lighting" phase on this route | lighter over a scene with no interior/terrain → completes instantly, nothing baked | near-empty phase → completes instantly, nothing baked |

The headline difference is **content, not code**: 4.04r2 worlds actually contain interiors/terrain for `lightScene` to bake and cache as `*_lm_*.png`; a 5.12-class world is GameObject shapes + Sun/Sky, lit **live** by the Sun's directional light with nothing to bake. The `lightScene` machinery survives in 5.12 (and would still bake terrain if terrain were present), but the interior content it was built for can't be networked to a 5.12 client.

## For a server

- Don't expect a 5.12-class client to bake or cache lighting for GameObject shapes — they're lit live by the Sun ghost ([T3D-111](3d-state-authority-420r6-2026-11-25.md)); the Mission-Lighting phase is effectively a no-op handshake for a Sun/Sky/GameObject world.
- The `lightScene` → `*_lm_*.png` bake-and-cache path is an interior/terrain feature, and on 5.12 the interior half of that content is gone; it was the live lighting path for 4.04r2-era interior/terrain worlds.
