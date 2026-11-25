# The 5.12 DLL: stock-TGE content is removed or dead, the drawable frame + Graal additions are live (T3D-103)

Date: 2026-11-25. Static synthesis (5.12-class represented by 4.20r6, 4.04r2 as the pre-split protocol-19 baseline); conceptual/subsystem level only, from a host-side marker-string comparison of the two Linux binaries. Board row: [T3D-103](3d-capability-board.tsv). Builds on [T3D-081](3d-object-classes-by-build-2026-11-25.md) (networked class sets), [T3D-084](3d-sound-paths-2026-11-25.md)/[T3D-085](3d-particles-512-vs-404r2-2026-11-25.md) (audio/particles), [T3D-088](3d-gs2-functions-by-build-2026-11-25.md)/[T3D-109](3d-shared-world-subset-2026-11-25.md) (control + common subset), [T3D-092](3d-lightscene-cache-2026-11-25.md) (lighting).

## Headline

"Dead stock-TGE code" on 5.12 is **not one thing** — three fates must be told apart:

1. **Removed outright** — the engine was recompiled without it (no class registration, no name marker). This is *not* dead code; it is simply gone.
2. **Present but unreachable** — the code is still compiled in, but the networked class that would drive it was cut, so nothing reaches it. This is the only literal "dead code in the DLL."
3. **Present and reachable, not exercised here** — live-capable; our lab server just never drives it.

Most of stock TGE's content path is category 1 or 2 on 5.12; the drawable frame plus the Graal additions are live.

## 1. Dead / removed stock-TGE **[bin]**

**Removed outright (gone from the engine, not dead code).** The stock Torque datablock-content classes — the item / static-shape / mesh-static / interior-instance / marker / trigger / physical-zone / particle-emitter-node / audio-emitter / precipitation / lightning family (the eleven, [T3D-081](3d-object-classes-by-build-2026-11-25.md)) — are absent from 5.12: their class registrations and name markers are gone, not merely unreferenced (confirmed against 4.04r2, where all are present). Likewise the stock datablock-audio event classes (the 2D/3D audio-event + emitter/description/profile/environment set, [T3D-084](3d-sound-paths-2026-11-25.md)) and the stock TGE control/AI classes (advanced-camera, path-camera, AI-player, shape-image-data, plus the third-person/FOV camera script functions, [T3D-088](3d-gs2-functions-by-build-2026-11-25.md)) — all on 4.04r2, all absent on 5.12. These were cut when the networked class set was trimmed from the ~117 of the protocol-19 era to the ~28 of protocol-24. So for most of "stock TGE content," 5.12 carries **no dead code at all** — it isn't in the binary.

**Present but unreachable (the genuine dead code).** The interior (`.dif`) renderer is the clear case: on 5.12 the interior-*instance* content class is gone, yet interior-renderer **support fragments still linger** (interior-resource / interior-sub-object / the scene-lighting interior-proxy machinery). Nothing can instantiate a networked interior on 5.12, so this interior-render code is **never reached** — present-but-dead. Alongside it, the scene-lighting interior-bake branch is present ([T3D-092](3d-lightscene-cache-2026-11-25.md)) but, with no interior class to light, that branch is dead on 5.12 for interior content; the mission-lighting bake collapses to a near-empty handshake for the Sun/Sky/GameObject scenes 5.12 actually uses (live Sun lighting replaces the bake).

## 2. Live Graal additions **[bin]**

Present **and** run on 5.12 (and, where noted, on 4.04r2 too):

- **The GS2 bytecode VM and its scripting classes** — the Graal var base, the script particle emitter (`TParticleEmitter`), the drawable/player script objects, and `play`/`play2`/`play3d`/`playlooped2` ([T3D-018](3d-client-events-420r6-2026-11-25.md)/[T3D-084](3d-sound-paths-2026-11-25.md)/[T3D-085](3d-particles-512-vs-404r2-2026-11-25.md)/[T3D-088](3d-gs2-functions-by-build-2026-11-25.md)). This is 5.12's content path: particles and positional 3D sound are done here, not via the removed Torque datablock classes.
- **The GameObject networked class + the protocol-24 two-phase ghost path** — the trimmed, datablock-free ghost flow that carries the 3D scene ([T3D-109](3d-shared-world-subset-2026-11-25.md)).
- **The Graal file/update protocol** — the client-driven file-request/update exchange that fetches shapes, textures, sounds, fonts on demand (fires in every lab: [T3D-084](3d-sound-paths-2026-11-25.md)/[T3D-058](3d-gui-overlay-420r6-2026-11-25.md)).
- **The Graal GUI** — the 3D-viewport control `GuiGraal3DCtrl` (an ordinary GUI control), the `GuiShapeNameHud`, and `showimg`/`showtext` overlays over the 3D view ([T3D-056](3d-player-identity-420r6-2026-11-25.md)/[T3D-058](3d-gui-overlay-420r6-2026-11-25.md)).
- **The FMOD audio backend** — present and initialising on both builds; what the live `play2`/`play3d` calls drive. (The stock datablock-audio *event* classes are removed; the low-level mixer is retained and live.)
- **The lobby/login flow** — the gen-5 login and lobby warp into the 3D server.

**Present and reachable, but not stock-dead and not exercised on our route:** `TerrainBlock` and `WaterBlock` are still registered on 5.12 and gain new GS2 terrain-query functions ([T3D-088](3d-gs2-functions-by-build-2026-11-25.md)) — live-capable, just never sent by our lab server; and scene-lighting's `lightScene` entry and its terrain-proxy path are present and reachable ([T3D-092](3d-lightscene-cache-2026-11-25.md)). These are the retained-and-live remnant of the old TGE renderer, distinct from the interior branch that died with its class.

## 3. The boundary rule

**A stock-TGE subsystem survives on 5.12 exactly as far as a *drawable-frame* renderer, and dies at the *networked content class* line.** The drawable frame — sky, sun, camera, terrain, water, the GameObject shape — plus the GS2 script VM, the Graal file/update protocol and the lobby/login flow is live. Everything that in stock Torque arrives as a *datablock-backed networked content object* (items, static/mesh shapes, interiors, particle-emitter nodes, audio emitters, precipitation, lightning, the stock player/camera/AI control objects) is cut from the 5.12 networked class set — **mostly removed outright, with only the interior renderer left behind as true dead code** because its support fragments outlived its class. Content stock TGE would deliver as datablocks is re-expressed on 5.12 through the GS2 script channel (script particles, `play2`/`play3d` sound).

## For a server

Drive a 5.12 client through the live set: GameObject shapes + sky/sun/camera (and terrain/water if you add emit support), the GS2 script channel for particles/sound/GUI, and the Graal file protocol for assets. The stock-TGE datablock-content path (the eleven classes, the datablock-audio events, the stock control objects) is unavailable — on 5.12 it is removed or dead, not reachable.
