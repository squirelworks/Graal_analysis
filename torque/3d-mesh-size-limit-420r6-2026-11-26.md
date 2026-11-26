# 5.12-class mesh limits: the .3ds 16-bit cap (~65k faces/chunk) then a per-shape draw ceiling (~265k–400k verts); never a crash (T3D-124, Linux 4.20r6)

Date: 2026-11-26. Single-client renderer lab on native Linux 4.20r6 (5.12-class, protocol 24, g3d420 route), software GL (llvmpipe); the client is a 32-bit (ELF i386) process. Observation only. Board row: [T3D-124](3d-capability-board.tsv). Companion to [T3D-118](3d-texture-size-limit-420r6-2026-11-26.md) (texture ceiling) and [T3D-113](3d-frame-rate-scaling-420r6-2026-11-25.md) (frame-rate scaling); extends [T3D-032](3d-capability-board.tsv) (the u16-cap mesh).

## Headline

Mesh size is bounded by **two draw limits, never a memory crash**: (1) the `.3ds` **format cap** — 16-bit vertex/face counts per chunk, so the **face count caps first at ~65535 faces (~33k verts)**; and (2) a **per-shape total-geometry draw ceiling** — a multi-chunk shape draws to ~265k verts / ~524k faces and **silently stops by ~397k verts / ~786k faces**. Both failures are **silent** (the whole shape just doesn't draw); the client never crashes, even at ~2.1M verts in a 101 MB `.3ds`. Gentler than the texture path ([T3D-118](3d-texture-size-limit-420r6-2026-11-26.md)), which *crashes* on an oversized texture.

## Setup

One GameObject whose `.3ds` is a UV sphere (a coloured ball) at controlled vertex/face counts, served over the file protocol; multi-mesh tests stack several chunks at one spot. A `.3ds` mesh chunk's vertex- and face-count fields are 16-bit and face indices are 16-bit, so one chunk cannot encode >65535 verts or >65535 faces.

## Size → outcome **[lab]**

| mesh | verts | faces | outcome | client |
| --- | --- | --- | --- | --- |
| single sphere | ~1k–16k | ~2k–33k | draws | alive |
| single sphere (at face cap) | ~33k | **65 522** | draws | alive |
| single sphere (faces over 16-bit) | ~40k | 80 000 (wraps) | **does NOT draw** (silent) | alive |
| 2 chunks, total > 65 535 verts | 66 248 | 131 044 | draws | alive |
| 8 chunks | ~265k | ~524k | draws | alive |
| 12 small chunks | ~99k | ~194k | draws | alive |
| 12 large chunks | ~397k | ~786k | **does NOT draw** (silent) | alive |
| 16 chunks | ~530k | ~1.05M | does NOT draw | alive |
| 32 chunks (50 MB) | ~1.06M | ~2.10M | does NOT draw | alive |
| 64 chunks (101 MB) | ~2.12M | ~4.19M | does NOT draw | **alive — no crash** |

## The limits (which bites first)

1. **`.3ds` FORMAT cap — 16-bit counts, per chunk (~65535 verts / 65535 faces).** A closed mesh has ~2× faces, so the **face count caps first** at ~65535 faces ≈ ~33k verts. A single chunk draws right to the cap (65 522 faces drew); past it the 16-bit field wraps → malformed → the shape **silently draws nothing** (no partial, no error, no crash).
2. **Per-mesh CLIENT limit below the format cap — none.** A single mesh draws to the format cap; no stricter client ceiling.
3. **Per-SHAPE total-geometry DRAW limit — this bites for big shapes.** A shape can exceed 65535 total verts via multiple chunks (66k drew), but only up to a point: it draws to **~265k verts / ~524k faces** and silently stops by **~397k verts / ~786k faces**. The cutoff is on **total geometry, not chunk count** — 12 small chunks (~99k) draw, 12 large (~397k) don't — so splitting a huge mesh across chunks does **not** get past it. Above it the whole shape vanishes; client stays up.
4. **Total-triangle MEMORY/crash ceiling — not reached.** No crash even at ~2.1M verts / 4.2M faces in a 101 MB `.3ds`; the client loads it, stays alive/activated, just doesn't draw. Mesh data is far lighter per element (millions of verts ≈ tens of MB, vs ~1 GB+ for a 16384² texture), so the **draw cutoff (~265k–400k verts) bites long before any memory crash** — the opposite of the texture case ([T3D-118](3d-texture-size-limit-420r6-2026-11-26.md)).

## Failure mode

**Silent — the whole shape stops drawing, never a crash, never a partial.** Both paths (a chunk past the 16-bit cap; a shape past ~265k–400k verts) make the GameObject render nothing (plain sky), no error, client stays up. Gentler than the texture path.

## FPS note

Not separately instrumented this run (cross-ref [T3D-113](3d-frame-rate-scaling-420r6-2026-11-25.md)). The heavy drawing cases (up to ~265k verts under software llvmpipe) rendered and the client stayed responsive across the capture window; software-GL FPS surely drops at high poly but was not fatal.

## For a server

Keep each `.3ds` mesh chunk under **~65k faces (~33k verts)** (the hard format cap), and each GameObject shape under **a few hundred thousand verts total** (~265k safe; by ~400k it silently stops drawing). Splitting one giant mesh into chunks does **not** raise the per-shape ceiling. Over-large meshes fail quietly (don't draw) rather than crashing — but they won't appear, so stay well under these limits.
