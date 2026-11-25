# A real 5.12 in a third-party 3D world (lab, 2026-11-24)

Date: 2026-11-25 (run 2026-11-24). A genuine Windows 5.12 client (`G3D14097`) in the Win10 lab VM
on lab host B joined a third-party Torque-route 3D server (SharpServer 0.0.40, an independently
written server, not an original one) through a local stand-in login that warped it there. It was a
normal-play capture only: nothing was fuzzed or sent to that server beyond what the client sent by
itself. The capture was then replayed offline through our own link code and renderer. Host, ports,
the capture and the world's files stay owner-held. Board rows: T3D-022, T3D-023, T3D-033
([board](3d-capability-board.md)). Tags: **[cap]** read from the capture, **[lab]** seen on screen,
**[inf]** inference.

The server is not a specification. This note records only what the **client** accepted and did.

## What the client accepted

- **No mission phases.** The server sent no `MissionStartPhase` commands and listed no
  `RemoteCommandEvent` in its class table. The client still linked, built the world, took its control
  object and drew the scene. **[cap][lab]**
- **The world as ghost-always events.** Every object arrived as a `GhostAlwaysObjectEvent`: an int12
  ghost index, a flag, an int12 class id, the int14 bit length and the object's update. All eight
  payloads end exactly on their stated length. **[cap]**
- **A `Camera` as the control object.** The control object was a `Camera` ghost, not a
  `GameObject`; the client accepted it and the view followed it. Its update is the `Camera`'s own
  (the `GameObject` section flags plus mode and follow flags), not a `GameObject` update.
  **[cap][lab]**
- **Connect sequence 0.** The connect sequence in the challenge exchange was 0. **[cap]**
- **No terrain.** No `TerrainBlock`, no `TerrainChunkEvent`; the hills were part of a mesh. No
  `.dts` or `.dif` either: every shape was `.3ds`. **[cap]**
- About 9,100 UDP datagrams in about 380 seconds of play. **[cap]**

## The objects, in order

`Sun`, a world `GameObject` (a `.3ds` at the origin), a `Camera`, `Sky`, three `GameObject` lanterns,
a `GameObject` character, then the control object. **[cap]**

| Object | Values the client received |
|---|---|
| `Sun` | direction (0, 0.707, −0.707), colour 0.7, ambient 0.3 |
| `Camera` | position about (−3, 4, 2.8), rotation about the z axis, angle about 2.44 rad, field of view 60 |
| `Sky` | five named face textures, visible distance 0, a fog colour |
| every `GameObject` | update section 2 always (1, 1, 1) |

**[cap]** Section 2 is (1, 1, 1) on every object, including ones that never move, so it reads as a
scale, not the velocity the static read guessed ([`wire-by-build.md`](wire-by-build.md)). **[inf]**
A controlled test on our own server settles it.

## Files the client fetched

The client fetched 92 files over the Graal TCP connection and stored all of them in
`levels3d\images`: three `.3ds` shapes and 89 PNG images. **[cap][lab]**

- The `.3ds` files kept their extension.
- All 89 images were stored **without** an extension, although materials and the sky named them
  with `.png`. The client's own TCP file requests settle who drops it: the client strips `.png` from
  a material's texture name and requests the bare name, then saves the file bare in
  `levels3d\images`. Shapes keep their extension (the `.3ds` files are requested with it). A mesh's
  textures are requested only after that mesh has arrived (T3D-033, renderer lab read of the same
  capture). **[cap]**

## Replay

Replayed through our own link and renderer, the ghosts decode with the layouts above, and the
rendered frame matches the client's camera and landmarks within a few pixels. The rebuild still
differs in lighting (the client is brighter and more saturated), filtering (the client filters
textures) and water (missing in the rebuild). **[cap][lab]**

## Open

- [ ] T3D-023: what the client sends back each packet while a `Camera` is its control object.
- [x] ~~T3D-033: who drops the image extension.~~ The client does (above).
- [ ] T3D-022: login steps with no mission phases, compared on our server's two routes.
