# Client frame-rate scaling with ghosts and triangles (T3D-113, Linux 4.20r6, software GL)

Date: 2026-11-25. Loopback lab of the Linux 4.20r6 client (5.12-class, protocol 24) against our own 3D lab server, under **Xvfb + software GL (Mesa llvmpipe, no GPU)** (runs `fps420-*`; no movement input). Linux 4.20r6 is 3D-equal to Windows 4.20r8 ([T3D-004](3d-engines-5007-512-and-403-411-2026-11-25.md)). Board row: [T3D-113](3d-capability-board.tsv). Builds on [T3D-091](3d-world-limits-420r6-2026-11-25.md) (1000 GameObjects drew, no crash).

## Read the numbers as relative, not absolute **[lab]**

All FPS below come from a **software rasteriser (Mesa llvmpipe, no GPU)**, so they are a CPU-rendering **floor** — a real client on a GPU would be far higher. Use the **shape of the curve** and the **relative ordering**, not the raw numbers. FPS was measured with a 32-bit `LD_PRELOAD` shim wrapping the GL buffer-swap (one swap = one frame), reporting the median of the steady last-15 s samples; each run changed one variable, ~42 s.

## Axis 1 — ghost count (each ghost a 12-triangle cube)

"Total ghosts" includes the 4 fixed ghosts (Sun, Sky, player control object, Camera) on top of the N world objects.

| N world objects | total ghosts | FPS (sw GL) | steady range |
| --- | --- | --- | --- |
| 1 | 5 | 295 | 280–302 |
| 10 | 14 | 262 | 254–269 |
| 50 | 54 | 176 | 159–182 |
| 100 | 104 | 146 | 141–150 |
| 500 | 504 | 53 | 51–54 |
| 1000 | 1004 | 28 | 26–30 |

- **Flat at the low end, then a smooth decline — no knee or cliff.** 1→10 objects barely moves; the per-ghost cost only bites past ~50. At the high end it is roughly **inverse-linear** (≈2× ghosts → ≈½ FPS).
- **Never unusable** across the sweep — even 1000 objects held 28 FPS and kept drawing. 1000 is where it turns sluggish on this software floor.

## Axis 2 — triangles per shape (10 shapes held constant)

Each of 10 shapes was a grid mesh of the stated triangle count (total scene triangles ≈ 10 × per-shape, plus a few from sky/player).

| triangles / shape | ~total scene triangles | FPS (sw GL) | steady range |
| --- | --- | --- | --- |
| 98 | ~1.4 k | 227 | 205–241 |
| 968 | ~9.7 k | 131 | 128–133 |
| 9 800 | ~98 k | 18 | 16–20 |
| 49 928 | ~500 k | 6 | 5.6–6.3 |

- **A steady, steep decline** — each ~10× in triangles costs roughly half to two-thirds of the FPS. Crosses the **<10 FPS "unusable" line between ~100 k and ~500 k total triangles**.
- The client **kept drawing even at ~500 k triangles** (reached the control object) — no stop, no crash — just very slow on software GL.

## Triangles dominate over ghost count

On this software rasteriser, raw triangle budget hurts far more than object count: **1000 cubes (≈12 k triangles) = 28 FPS**, but **10 shapes of ~98 k triangles = 18 FPS**. The per-triangle vertex/fill work (what llvmpipe does on the CPU) is the real limiter, not the number of ghosts. A GPU shifts both limits up by orders of magnitude, but the *ordering* (triangles cost more than object count) is a real property.

## Axis 3 — terrain, and the 4.04r2 contrast

- **Terrain: not testable on this route** — the gserver emits no terrain (TerrainBlock/TerrainChunkEvent are never sent, [T3D-108](3d-recovery-420r6-2026-11-25.md)/[T3D-109](3d-shared-world-subset-2026-11-25.md)), so terrain-chunk scaling couldn't be exercised. **[route limit]**
- **4.04r2: not run.** The ghost-count axis is protocol-24/GameObject-specific: a protocol-19 client is not sent GameObjects at all ([T3D-109](3d-shared-world-subset-2026-11-25.md)) — on this route it only ever has its own single Player — so there's nothing to sweep. A meaningful 4.04r2 sweep would need a server that ghosts many stock Players/StaticShapes to it. So this is 4.20r6 only.

## For a server

- The client degrades **gracefully** with scene size — a smooth decline, no cliff or crash, even at 1000 objects or ~500 k triangles. There's no hard ghost/triangle ceiling to design around on the client side; it just gets slower.
- **Triangle budget is the dominant cost**, well ahead of object count. For a shared world, capping per-shape mesh density matters more than capping the number of shapes.
- All figures here are a software-GL floor; treat them as relative scaling, not as what a real-GPU client achieves.
