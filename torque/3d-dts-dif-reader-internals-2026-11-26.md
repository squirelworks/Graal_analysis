# The `.dts` and `.dif` body readers: the structure g3d-replay must match, and the gaps left (for the renderer)

Date: 2026-11-26. Static read of the shape and interior body readers in
`Graal3DEngine.dll` (5.00r7 = 5.12), paired with the renderer rebuild's own
readers in `graal-client-repro` (`common/cpp/graal3dengine/render/read_dts.cpp`,
`read_dif.cpp`). Behaviour only; no addresses, no decompiled text. This sits under
the renderer brief's strand 2 (`graal3d-renderer/CLIENT-CAPABILITY-MAPPING.md`) and
extends the version-gate note ([loader validation](3d-loader-validation-by-build-2026-11-26.md),
T3D-098) from "what is accepted" to "what is read". **[bin]** for the class set and
bounds; the per-field layout is the stock-TGE/Marble-Blast (MIT) format the rebuild
already implements, confirmed applicable by the client's class set.

## Why the rebuild's layout is the client's layout

The 5.12 engine carries the **stock Torque (TGE-era) loader classes** as names and
code: `TSShape`, `TSMesh`, `TSSortedMesh`, `TSSkinMesh`, `TSShapeInstance` for shapes;
`InteriorResource`, `Interior`, `ForceField`, `InteriorSubObject` (and `TexGen`,
`zone`, `surface`) for interiors. So the on-disk format the client reads is the
stock-TGE three-stream `.dts` and version-44 `.dif`, the same format the rebuild's
readers were written from (Torque3D / hx_dif, MIT) and whose **bounds are
bin-confirmed** (`.dts` 17–24, `.dif` resource 44 / interior 0; T3D-098). The rebuild
can therefore stand in for the client's reader; the open question is only *which parts*
of the format the client reads that the rebuild does not yet draw.

## `.dts` (TSShape) body layout

After the version word (low byte = shape version; T3D-098), the file is **one block of
three streams read side by side** — 32-bit, 16-bit and 8-bit — with the block header
giving the 32-bit word count and the 16-bit and 8-bit start offsets, and an
**incrementing guard value checked across all three streams after each section**
(`read_dts.cpp` `Alloc::checkGuard`). Read order:

1. **Sequences**, then the **material list** (a stream-type byte, a count, length-prefixed
   names, then one flags word per material — only the translucent bit matters for drawing).
2. **Header counts**: nodes, objects, decals, sub-shapes, IFL materials; then (v>21)
   node rotations / translations / uniform / aligned / arbitrary scales, else one
   node-state count; then (v>23) ground frames; then object states, decal states,
   triggers, details, meshes, (v<23) skins, names; smallest-visible size/detail.
3. **Tables**: nodes (name, parent, first object/child/sibling), objects (name,
   numMeshes, startMesh, node, …), decals, IFL materials, sub-shape first/count arrays,
   then the **default pose** — one 16-bit quaternion per node (Torque keeps the
   **conjugate**, so the reader negates x/y/z) and one translation per node — then the
   animated rotation/translation/scale pools, object/decal states, triggers, and the
   detail-level records (name, sub-shape, object-detail, size, errors, poly count).
4. **Meshes**, each tagged by type: **standard**, **skin**, **sorted**, **decal**, or
   **null**. A standard mesh is vertices, texture coords, normals (+ encoded normals
   for v>21), primitives (start/count + a material/type word), indices, merge indices;
   a skin mesh adds initial vertices already in shape space plus transforms, weights and
   node indices; a mesh may name an earlier mesh as its parent and share its vertices.
   Primitives carry a 2-bit type in the top bits (triangle **list**, **strip** or **fan**)
   and a no-material flag.
5. For **versions below 23** the skins are a separate list after the names, each detail
   level naming its run of them.

Drawn: the shape in its default pose at its highest positive-size detail level, each
standard mesh placed by its object's node transform, each skin mesh in shape space;
list/strip/fan primitives expanded to triangles; a no-material primitive skipped.

## `.dif` (Interior) body layout

Resource **version 44**, then an optional **preview image** (a PNG, skipped to its
`IEND`), then a detail-level count, then the **first (most detailed) Interior at
version 0**: bounding box and sphere, alarm state, light-state count, then the geometry
lists — **normals**, **planes** (normal index + distance), **points**, point visibility,
**TexGens** (two 4-float planes for u and v), **BSP nodes** and **BSP leaves**, a
material-list version byte and the **material names**, the **winding** (point-index)
list, winding indices, **zones**, zone surfaces, zone portals, **portals**, and finally
the **surfaces**. Several lists use Torque's **flex-width encoding** (entries are 16-bit
when the count's top bit is set and a following parameter byte is non-zero, else 32-bit),
which the reader probes (`read_dif.cpp` `flexList`, and `readSurfaces` tries the
byte-wide then the 16-bit lightmap layout).

A **surface** is a run of the winding list (`windingStart`/`windingCount`), a plane, a
material, a TexGen, plus lightmap fields. Drawn: each surface's winding run as a triangle
strip, textured by its TexGen planes (`u = planeX·p + dX`, `v = planeY·p + dY`); Torque's
marker materials (`null`, `origin`, `trigger`, `forcefield`, `emitter`) are never drawn.

## The gaps left for the renderer (client reads these; the rebuild does not draw them)

| Area | In 5.12 | Rebuild (`graal-client-repro`) today | Fidelity impact |
| --- | --- | --- | --- |
| `.dts` **sorted** meshes | `TSSortedMesh` present | refused ("not read yet") | a shape built only of sorted meshes draws nothing — worth adding, since the class exists in 5.12 |
| `.dts` **decal** meshes | `TSDecalMesh` name not found in 5.12 | refused | likely moot for 5.12 (the class string is absent); confirm before spending effort |
| `.dts` sequences / IFL / ground frames | read | stepped over | only matters for animation and IFL material swaps, not a static pose |
| `.dif` **sub-objects** | `InteriorSubObject` present | not read | sub-object geometry (detached interior pieces) would be missing |
| `.dif` **force fields**, triggers, path, vehicle collision | `ForceField` present; others version-gated | not read | invisible/markup in-game; low render impact |
| `.dif` **portals / zones** geometry | read | lists skipped, only first-detail surfaces drawn | no portal culling, but all surfaces still draw |
| `.dif` **lightmaps** | read (byte or 16-bit layout) | fields skipped | no baked lighting; geometry and textures unaffected |

## For the renderer

The rebuild's `read_dts.cpp` / `read_dif.cpp` already match the client's loader for the
common case (standard + skin shape meshes in the default pose at top detail; first-detail
interior surfaces with TexGen UVs). The one gap worth closing against a real 5.12 asset is
**`.dts` sorted meshes** (the class is in 5.12), and, if interiors with detached pieces
turn up, **`.dif` sub-objects**. Everything else the client reads but the rebuild skips
(sequences, IFL, ground frames, force fields, portals, lightmaps) does not change the
drawn geometry of a static scene. Bounds and version gates are in
[T3D-098](3d-loader-validation-by-build-2026-11-26.md); this note is the body-structure
companion for g3d-replay.
