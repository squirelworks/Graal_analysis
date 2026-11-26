# 3D resource loaders: the exact version checks and what `.ft` is (T3D-098, T3D-029, T3D-030, T3D-036)

Date: 2026-11-26. Static read of the resource loaders in the Windows
`Graal3DEngine.dll` for 4.04r2 (protocol 19), 4.20r8 and 5.00r7 (= "5.12",
[T3D-005](3d-engines-5007-512-and-403-411-2026-11-25.md)). Nothing was run.
Behaviour only; no addresses or decompiled text. Board rows:
[T3D-098, T3D-029, T3D-030, T3D-036](3d-capability-board.tsv). **[bin]**

This completes the "other per-loader checks open" part of
[T3D-098](3d-engine-static-reads-2026-11-25.md) and pins, statically, the bounds
the live labs saw ([T3D-029](live-512-shapes-2026-11-25.md),
[T3D-030/087](3d-dif-interiors-512-2026-11-25.md)). Knowing the bound before a
feed makes a reject informative rather than a crash (the renderer brief's
strand 2, `graal3d-renderer/CLIENT-CAPABILITY-MAPPING.md`).

## `.dts` (TSShape) — version gate, exact bounds

The shape reader takes the first 32-bit word of the file. The **low byte** is the
shape version; the **high word** is the exporter version (kept for sequence-import
checks). Then two bounds:

| Build | accepts version | too-new reject | too-old reject |
| --- | --- | --- | --- |
| 4.04r2 | **v ≤ 24** (no lower floor) | — | "can currently only load version 24 and before" |
| 4.20r8 | **17 ≤ v ≤ 24** | "version %i … not supported anymore" (v < 17) | "can currently only load version 24 and before" (v > 24) |
| 5.00r7 / 5.12 | **17 ≤ v ≤ 24** | same | same |

So 4.20r8, 5.00r7 and 5.12 are identical at the shape loader (max 24, min 17),
and the 24-era **added the lower floor**: 4.04r2 will read a shape older than 17,
the protocol-24 clients reject it. The bound is checked on the **version word
only**; the body is trusted, which is why a mislabelled v17–24 body hangs or
draws nothing on a live client ([T3D-029](live-512-shapes-2026-11-25.md)) — the
loader never validates the body against the version it believed. This is the
static root of that live finding.

`.dsq` sequence import has its own version reject ("sequence version not supported
anymore"), present on 4.20r8 and 5.00r7 / 5.12, absent on 4.04r2.

## `.dif` (Interior) — version must be 44

`InteriorResource::read` takes a 4-byte version and **rejects unless it is exactly
44** (0x2c); `Interior::read` and `ForceField::read` are likewise version-gated
(the interior sub-objects and force fields each check their own version, logging
"incompatible file version found"). This is the static side of the live result
that only a v44 `.dif` draws and v43/v45 are rejected
([T3D-030/087](3d-dif-interiors-512-2026-11-25.md)). The value 44 is constant
across every build read.

## `.3ds` — no version gate; collision-hull and colour parsing

The `.3ds` reader has **no version check** (the 3DS chunk format carries none). It
walks the stock 3DS chunks and, beyond the mesh, reads per-object collision hulls
and a `3dscolor r g b` material colour. It warns (logged, non-fatal) when a
collision hull is "not closed" or "not convex" and continues. So a `.3ds` is
accepted on its structure alone, with hull quality only a warning — unlike `.dts`
and `.dif`, there is no version a server can get wrong.

## `GameShapeFT` — what `.ft` is (T3D-036)

`GameShapeFT` is **not a mesh format**. It is a 3D text shape drawn with
FreeType (`freetype6.dll`) and the GL font path (`wglUseFontOutlinesA`,
`wglUseFontBitmapsA`), using the `defaultfont` / `defaultfontsize` prefs and a
`.ttf` font, rendered through `drawText`. There is no `.ft` file format and no
mesh loader for it; a `GameShapeFT` is a font-backed label. This explains the
live T3D-036 result directly: the `.ft` GameObject downloaded its file and
texture but **never drew as a shape** across flags and `defaultLevels`
([live-512-shapes](live-512-shapes-2026-11-25.md)) — there is no shape geometry to
draw, only GL text, which that lab's fixed world camera and object placement
never showed. A server that wants visible 3D text drives it as a font label, not
as a mesh.

## Terrain

The terrain loader requires textures to be **256×256×24** ("Terrain texture of bad
format (must be 256x256x24)"), on all three builds. The in-memory height query
(`getz` in 3D mode) samples a **256×256** grid of height pairs and, when the
block's wrap flag is clear, rejects an x or y outside 0..255; with wrap set it
folds the index. (The streamed terrain *chunk* format is
[T3D-097](3d-engine-dll-interface-and-events-2026-11-26.md): block x/y as `int4`,
compressed bytes with an `int10` length.)

## Summary for the renderer and the server

| Loader | Gate | Accept | Note |
| --- | --- | --- | --- |
| `.dts` | shape version (low byte of word 0) | 17–24 (24-era); ≤24 (4.04r2) | body not validated against version |
| `.dsq` | sequence version | 24-era only rejects old | absent on 4.04r2 |
| `.dif` | interior version | exactly 44 | sub-objects + force fields version-gated too |
| `.3ds` | none | any well-formed 3DS | hull non-closed/non-convex → warning only |
| `GameShapeFT` | — | a `.ttf` via FreeType | a GL text label, not a mesh |
| terrain texture | format | 256×256×24 only | |
| terrain heights | index | 0..255 (wrap folds) | 256×256 grid |

Feed a 5.12 client `.dts` in 17–24 and `.dif` at 44; serve terrain textures only at
256×256×24; and treat `GameShapeFT` as font text, not geometry. The loader bounds
are identical on 4.20r8 and 5.00r7 / 5.12, one more confirmation that 4.20r8
stands in for 5.12 on the 3D side
([T3D-104](3d-engine-dll-interface-and-events-2026-11-26.md)).
