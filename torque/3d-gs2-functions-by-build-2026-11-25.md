# 3D GS2 and console functions across builds: core shared, camera dropped at 24, spatial queries added (T3D-088)

Date: 2026-11-25. Comparison of the `-listscriptfunctions` GS2/console-function dumps for 4.04r2 (protocol 19), 4.20r8, 5.00r7 and 5.12 (all protocol 24); the 4.04r2 dump was generated this session from the native Linux client. Linux 4.20r6 is 3D-equal to 4.20r8 ([T3D-004](3d-engines-5007-512-and-403-411-2026-11-25.md)). Board row: [T3D-088](3d-capability-board.tsv). Builds on [T3D-081](3d-object-classes-by-build-2026-11-25.md)/[T3D-085](3d-particles-512-vs-404r2-2026-11-25.md) (networked classes) and [T3D-092](3d-lightscene-cache-2026-11-25.md).

**4.04r2 has the same GS2 console** (TGraalVar classes, `-listscriptfunctions`) as the 5.x family — it is not GS1-only, so this is a like-for-like GS2 comparison. A function's presence in a dump means it is **exposed**, not that it runs on the lab route; live confirmations are noted below.

## Per-family table **[bin]**

`Y` = present in that build's dump.

| family / function | 4.04r2 (19) | 4.20r8 (24) | 5.00r7 (24) | 5.12 (24) | note |
| --- | --- | --- | --- | --- | --- |
| **object create / scene** | | | | | |
| `TDrawableObject` (+`TBaddy`, `TLevelObject`) | Y | Y | Y | Y | the GS2 drawable-object model — same on all |
| `addcontrol(obj)`, `attachplayertoobj`, `setshapename` | Y | Y | Y | Y | same |
| `attachmovie(…)` | – | – | Y | Y | new in 5.00r7/5.12 (Flash-clip attach) |
| **getz / terrain** | | | | | |
| `getz(float,float) → float` | Y | Y | Y | Y | terrain-height query — same on all |
| `onwater`, `onwater2` | Y | Y | Y | Y | same |
| `castray(start,end,types)` | – | Y | Y | Y | new in 24 (3D ray pick) |
| `get3dobjectsbybox`, `get3dobjectsbyradius` | – | Y | Y | Y | new in 24 (spatial object query) |
| `getterraintexture`, `getterraintextureindex`, `gettileset(type)` | – | Y | Y | Y | new in 24 (terrain-texture query) |
| `setterrainrendermode`, `updateterrain`, a `TerrainEditor` GUI | Y | – | – | – | 4.04r2-only (TGE editor-side terrain) |
| **camera** | | | | | |
| `Camera` class parent | `ShapeBase` | `GameObject` | `GameObject` | `GameObject` | class model shifted (datablock → GameObject) |
| `cameramode` | Y (integer) | Y (string) | Y (string) | Y (string) | kept, type changed |
| `getcamerafov()` / `setcamerafov(float)` | Y | – | – | – | 4.04r2-only (FOV control dropped) |
| `AdvancedCamera` + `setthirdpersonmode/offset/panmode/targetmode`, `getcameraposition`, `PathCamera` | Y | – | – | – | 4.04r2-only (whole third-person/advanced camera family dropped) |
| `$camera::movementspeed` | Y | – | – | – | 4.04r2-only |
| `camera` (read-only object handle) | – | Y | Y | Y | new in 24 (the 3D control's camera handle) |
| **sky / lighting** | | | | | |
| `setfogcolors`, `setskybandcolors`, `setskybandsizes`, `setsuncolors`, `setfog`, `fog` | Y | Y | Y | Y | same on all |
| `Sky (SceneObject)` + `realfog`, `stormfog`, `stormfogshow` | Y | Y | Y | Y | same |
| `skysolidcolor`, `useskytextures` (Sky props) | – | Y | Y | Y | new in 24 (the 5.12 Sky layout) |
| `lightscene()` | Y | Y | Y | Y | same on all ([T3D-092](3d-lightscene-cache-2026-11-25.md)) |
| `fxSunLight`, `Sun` | Y | Y | Y | Y | same |
| **particles** | | | | | |
| `TParticleEmitter` (+`TParticle`, `TParticleModifier`), `emit()`, `particleeffectsenabled` | Y | Y | Y | Y | the GS2 particle scripting API is on all builds |
| **position getters** | | | | | |
| `getz`, `getposition` | Y | Y | Y | Y | same on all |

## Shared / 4.04r2-only / new-in-24

- **Shared by all (incl. 4.20r8):** the GS2 drawable-object model, `getz`/terrain-height and `onwater`, the sky/sun/fog set functions and `lightscene`, the TParticleEmitter particle scripting API, and position getters. The core 3D GS2 surface is **largely the same across the protocol-19/24 boundary**.
- **4.04r2-only (dropped at 24):** the rich camera API — `AdvancedCamera` + third-person functions, `getcamerafov`/`setcamerafov`, `PathCamera`, `$camera::movementspeed`. Camera on 4.04r2 is a `ShapeBase` datablock; on 24 it collapses to a `GameObject` with just `cameramode`. Also 4.04r2's editor-side terrain functions (`setterrainrendermode`, `updateterrain`, `TerrainEditor`).
- **New in protocol 24:** the 3D spatial-query functions — `castray`, `get3dobjectsbybox`, `get3dobjectsbyradius`, `getterraintexture`/`getterraintextureindex`, `gettileset(type)` — plus the Sky texture props and the `camera` object handle. `attachmovie` is new in 5.00r7/5.12 over 4.20r8.

## Important nuance (ties to T3D-085)

`TParticleEmitter` is a **GS2 scripting class present on all builds, 4.04r2 included** — not to be confused with the networked Torque `ParticleEmitterNode` datablock class, which is 4.04r2-only ([T3D-081](3d-object-classes-by-build-2026-11-25.md)/[T3D-085](3d-particles-512-vs-404r2-2026-11-25.md)). The particle *scripting API* is shared; only the particle *datablock content* the server ghosts is 4.04r2-era. The same split applies to camera: GS2 `cameramode` survives on all, but the datablock `AdvancedCamera`/third-person functions are 4.04r2-only.

## Presence vs works

Presence in a dump proves a function is **exposed**, not that it runs on this route. Prior 4.20r6 labs confirm live: sky renders ([T3D-077](3d-texture-formats-420r6-2026-11-25.md)/[T3D-109](3d-shared-world-subset-2026-11-25.md)), lighting/`lightScene`/Sun drive shading ([T3D-092](3d-lightscene-cache-2026-11-25.md)/[T3D-111](3d-state-authority-420r6-2026-11-25.md)), camera positions via the `camera` world line ([T3D-109](3d-shared-world-subset-2026-11-25.md)), the GameObject/drawable path draws ([T3D-090](3d-shape-textures-420r6-2026-11-25.md)/[T3D-091](3d-world-limits-420r6-2026-11-25.md)). The `getz`/terrain and 3D-query functions (`castray`, `get3dobjectsby*`) could **not** be live-confirmed on this route (no terrain, no second 3D object set) — present in the dumps only.

## For a server

- A clientside GS2 script targeting a 5.12-class client should use the protocol-24 surface: `cameramode` (string), the `camera` handle, `castray`/`get3dobjectsby*` for picking, and the drawable-object model; it must **not** rely on the 4.04r2 camera API (`setcamerafov`, `AdvancedCamera`, third-person functions), which is gone.
- The sky/sun/fog set functions, `getz`, `lightscene` and the TParticleEmitter API are safe to use across all builds.
