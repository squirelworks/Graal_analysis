# Which networked object classes each build draws: the game layer is 4.04r2-only (T3D-081)

Date: 2026-11-25. Static read of the registered console classes and class-name strings in the Linux 4.20r6 (5.12-class, protocol 24) and 4.04r2 (protocol 19) engines, plus a read of the lab gserver's ghost types and world-format keywords. Linux 4.20r6 is 3D-equal to Windows 4.20r8 and class-equal to 5.00r7/5.12 ([T3D-004](3d-engines-5007-512-and-403-411-2026-11-25.md), [T3D-003](3d-engines-5007-512-and-403-411-2026-11-25.md)). Board row: [T3D-081](3d-capability-board.tsv). Builds on [T3D-085](3d-particles-512-vs-404r2-2026-11-25.md) (28 vs 117 class tables).

Two layers:
- **[bin]** — is the class a registered console class (so it *can* be ghosted at all)? Definitive.
- **[lab]** — of the registered classes, which can our gserver + world format emit on the g3d420 route, and does the client draw it? Route-limited.

## The game-content classes **[bin]**

| Class | Registered on 4.20r6 (5.12-class)? | Registered on 4.04r2? | Note |
| --- | --- | --- | --- |
| Item | no | yes | 4.04r2-only |
| StaticShape | no | yes | 4.04r2-only |
| TSStatic | no | yes | 4.04r2-only |
| InteriorInstance | no | yes | 4.04r2-only (the `.dif` drawable) |
| Marker | no | yes | 4.04r2-only (also MissionMarker, WayPoint, SpawnSphere) |
| Trigger | no | yes | 4.04r2-only |
| PhysicalZone | no | yes | 4.04r2-only |
| ParticleEmitterNode | no | yes | 4.04r2-only ([T3D-085](3d-particles-512-vs-404r2-2026-11-25.md)) |
| AudioEmitter | no | yes | 4.04r2-only |
| Precipitation | no | yes | 4.04r2-only |
| Lightning | no | yes | 4.04r2-only (its `LightningStrikeEvent` is likewise gone from 5.12) |

**Every one of the eleven is 4.04r2-only** — registered on 4.04r2, and neither registered nor even present as a class-name string on the 5.12-class engine. 4.20r6 registers **28** console classes; 4.04r2 registers **117**; the whole datablock-era game layer is in the 117 and absent from the 28. (`Player` and `WayPoint` appear only as byte substrings inside `G3DPlayer`/`playershape` on 4.20r6 — not registered classes, so not drawable.)

## The scene frame, and what replaced the game layer **[bin]**

| Class | 4.20r6 | 4.04r2 | |
| --- | --- | --- | --- |
| Sun, Sky, Camera, TerrainBlock, WaterBlock | registered | registered | the scene frame both keep |
| **GameObject** | **registered** | not present | the 5.12-era generic drawable that replaced the datablock game classes |
| ShapeBase, GameBase, Player, Item, StaticShape, … | not registered | registered | the datablock game layer, 4.04r2-only |

So the 5.12-class engine's drawable-content model is essentially **one class, `GameObject`** (plus Sky/Sun/Camera/Terrain/Water for the frame). Everything specialised — items, static shapes, interiors, markers, triggers, zones, particles, audio emitters, precipitation, lightning — was collapsed out and is 4.04r2-only.

## Lab layer — what the route can emit **[lab]**

The lab gserver can ghost only **Sun, Sky, GameObject, Camera**, plus **TgePlayer / TgeCamera** (the stock Player/Camera on the protocol-19 path). The world/scene format has keywords only for `sun`, `sky`, `object` (→ GameObject), `camera`, `playershape`, `tgeplayershape`, `tgecontrol`, `skyoptions`, `spawn`, `weapon3d` — no line for any of the eleven classes.

- **None of the eleven can be server-ghosted on this route**, on 5.12 or 4.04r2 — a server-side limit (no code or world syntax to emit them), which on 5.12 coincides with the client not having the classes either.
- The content class the route does emit, **GameObject**, draws correctly ([T3D-090](3d-shape-textures-420r6-2026-11-25.md), [T3D-091](3d-world-limits-420r6-2026-11-25.md)). On 4.04r2 the route's **TgePlayer / TgeCamera** draw. None of these is in the eleven.
- "Draws when emitted" is therefore unobservable for the eleven on this route; the ceiling is the registered-class fact, which is definitive.

## Headline for a shared world ([T3D-109](3d-capability-board.tsv))

**All eleven are 4.04r2-only and do not exist in the 5.12-class engine.** A world placing Items, StaticShapes, TSStatics, InteriorInstances, Markers, Triggers, PhysicalZones, ParticleEmitterNodes, AudioEmitters, Precipitation or Lightning is a **protocol-19 / 4.0x-era world**; a 5.12-class client cannot be sent those objects at all (an unknown-class ghost drops the link, [T3D-085](3d-particles-512-vs-404r2-2026-11-25.md)). For a 5.12-class client, drawable networked content is **GameObject shapes** (plus the Sky/Sun/Camera frame); the old classes' equivalents would have to be rebuilt as GameObjects or driven by the 5.12 script side (e.g. the `TParticleEmitter` system from [T3D-085](3d-particles-512-vs-404r2-2026-11-25.md) for particles).
