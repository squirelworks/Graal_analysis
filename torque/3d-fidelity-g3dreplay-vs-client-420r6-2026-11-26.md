# g3d-replay vs the real 5.12-class client: a schematic box/grid positional view, not a pixel-faithful renderer — matches on none of the five fidelity features (T3D-105, Linux 4.20r6)

Date: 2026-11-26. Single-client fidelity lab on native Linux 4.20r6 (5.12-class, protocol 24, g3d420 route), software GL; the same scene on the real client (rendered live) and on g3d-replay (read from source). Observation only. Board row: [T3D-105](3d-capability-board.tsv). g3d-replay is the Frankenstein / graal3dengine stand-in view ([T3D-122](3d-frankenstein-6037-vs-600-2026-11-26.md)); real-client look per [live-512-lighting-and-sky](live-512-lighting-and-sky-2026-11-25.md) and [live-512-own-server-textures](live-512-own-server-textures-2026-11-25.md).

## Headline

**g3d-replay is a schematic positional debug view — a box per GameObject, a ground grid, and a flat fog-colour sky — not a faithful renderer.** It matches the real 4.20r6 client on **none** of the five fidelity features (camera FOV/near-far, fog curve, lighting, texture filtering/mips, alpha sorting). The only correspondences are coarse: each GameObject sits roughly at its world position, and the Sky's fog colour is reused as a flat sky tint.

## Scene (same input to both) **[lab]**

A textured `.3ds` cube, a near and a far plain shape (to probe fog by distance), a Sky with a visible-distance + fog colour, and a full Sun. The **real 4.20r6 client was rendered live and screenshotted**. **g3d-replay was read at source** (`view3d.cpp` of the graal3dengine stand-in): no Linux g3d-replay binary exists (only Windows artifacts, and the Windows VM is out of scope), and its source fully determines its output — the build's own notes call it a stand-in that reads the 3D world but does not draw it yet ([T3D-122](3d-frankenstein-6037-vs-600-2026-11-26.md)).

- **Real client:** textured cube with the texture **applied + filtered** (crisp quadrants, mip-smoothed), **per-face directional lighting** (bright front, shaded sides, white specular on top), real mesh geometry, a sky gradient, distance **fog** (the client uses `EXT_fog_coord`), and depth-sorted shapes.
- **g3d-replay (from source):** sky = a flat two-colour split (top = the Sky fog colour, bottom = ground), a 2-unit **ground grid**, **each GameObject as a plain box** (the player's own box yellow), a simple perspective with `near=0.1`. No meshes, textures, lighting, distance fog, or alpha.

## Per-feature match / differ

| feature | real 4.20r6 | g3d-replay (stand-in) | match? |
| --- | --- | --- | --- |
| camera FOV & near/far | GL perspective, true screen size/position | own perspective (`near=0.1`), a box at each GameObject; positions roughly track, FOV/near-far not calibrated | **differ** (positions approximate) |
| fog curve | real distance fog (`EXT_fog_coord`), tints distant shapes | no distance fog — only paints the sky top with the flat fog *colour* | **differ** |
| lighting (built-in + Sun) | directional Sun + ambient per-face shading + specular | flat, unlit boxes | **differ** |
| texture filtering & mips | `.3ds` texture linear-filtered + mipmapped | no textures (boxes only) | **differ** |
| alpha sorting / transparency | depth-sorted; opaque occlude, transparent alpha-blend in order | opaque boxes, no alpha/sort | **differ** |

## Verdict

g3d-replay is a **positional/topology sanity view** (are the right GameObjects in roughly the right places?), not a pixel-fidelity renderer. Everything that makes the real frame look right — mesh geometry, filtered/mipmapped textures, per-face lighting + specular, distance fog, alpha/transparency — is **absent from g3d-replay by design**, until the real Torque renderer replaces the stand-in ([T3D-122](3d-frankenstein-6037-vs-600-2026-11-26.md)).

## For a server

Don't treat g3d-replay as a visual reference for the real client: it is a positional/topology sanity view, not a pixel-fidelity renderer. For look and feel (lighting, fog, textures, transparency) use the real 4.20r6 client; any "does it match" on those features reads **differ** until the stand-in is replaced by the real renderer.

## Method caveat

The real client was rendered live and screenshotted; g3d-replay's output was derived from its source (`view3d.cpp`) because no Linux g3d-replay binary is present and the Windows build can't run in scope here. The source firmly determines the per-feature verdicts (box-per-GameObject, ground grid, flat fog-colour sky, no textures/lighting/fog/alpha); a side-by-side g3d-replay screenshot at the matched pose would be that documented box/grid/flat-sky stand-in.
