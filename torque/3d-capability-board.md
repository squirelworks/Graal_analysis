# Torque-era 3D client capability board (3.x to 5.12)

Date: 2026-11-25. One claimable table of what we still need to know about the 3D side of the
Torque-era clients: the `Graal3DEngine` script surface, what the client does by itself, and the
Torque engine inside it. The table is [`3d-capability-board.tsv`](3d-capability-board.tsv).
The February 2000 DirectX Graal3D is a different program and is not on this board
(see [`graal3d/README.md`](../graal3d/README.md)).

The client is the only ground truth. A third-party server that a client accepts is one example of
what the client will take, never a specification. Lab rows run in lab VMs against our own server
(seihai-gserver-v2 in 3D mode) or a server started on the loopback address; fuzz rows feed content
to the client from our own server only.

## Columns

| Column | Meaning |
|---|---|
| `id` | `T3D-nnn`, stable. New questions are appended; ids are never reused. |
| `area` | Inventory and lineage, Torque files and scripts, script surface (GS2), session and network, content formats, terrain/water/sky, rendering, player and camera, GUI and 2D/3D hand-over, effects and sound. |
| `question` | One question, answerable by a read or a run. |
| `why_it_matters` | What a server, a renderer or the manual gains from the answer. |
| `how_to_test` | The cheapest test that settles it. |
| `method` | `static` (read the binary), `lab` (live client in a VM), `fuzz` (malformed content from our server), `probe` (a GS2 weapon or script that exercises the feature), or a combination. |
| `builds` | `304L` Linux 3.04, `3153M` Mac 3.153, `404W` Windows 4.04r2, `420r6` Linux/Mac 4.20r6, `420r8W`, `500r7W`, `512W`, `512M`; `L`/`M`/`W` = Linux/Mac/Windows. |
| `owner` | `this board` (the capability research), or the lab that already covers it: `renderer lab` (texture naming, sky, shapes, GameObject fields, other table classes), `terrain lab` (TerrainBlock, chunks, WaterBlock), `gserver 3D lab` (our server's routes and lab worlds). Rows owned by another lab are listed so they are not done twice. |
| `status` | `open`, `in progress`, `assigned`, `partial: …`, `answered: …` with the note that settles it. |

## How the board is worked

1. Static first. A read bounds a lab run, so a reject in the lab is informative rather than a crash.
2. Then one live run that varies one thing.
3. Then fuzz, from our own server, to find the edges.
4. Every result becomes a behaviour-only note here (no decompiled text, addresses, captures or
   client files) and the row's status links to it. A result raises the next question, which is
   appended as a new row.

## Results so far

- [Conformance suite](conformance/README.md): each answer as a repeatable lab case (a world, a GS2
  probe, the expected result per build), with a VM runner and a derived results table (2026-11-26).

- [Closing plan for the partly answered rows](3d-partial-rows-closing-plan-2026-11-26.md): the
  remaining gap, closing method and batch for each of the 39 partly answered rows (2026-11-26).

- [Script and terrain tools by build](script-and-terrain-tools-by-build.md): 3.153 still carries the
  TorqueScript compiler and Torque's full terrain generator; 4.04r2 and 5.12 drop the compiler and
  keep only a four-function `Terraformer` and the stock `TerrainEditor`, both registered as script
  objects (T3D-006, T3D-007, T3D-008, T3D-019, T3D-041).
- [A real 5.12 on a third-party 3D server](live-512-third-party-session-2026-11-24.md): a session with
  no mission phases, a `Camera` as the control object, and textures stored without an extension
  (T3D-022, T3D-023, T3D-033).
- [The GS2 3D objects](gs2-3d-objects-404r2-512.md): the classes a script can create. 4.04r2's plug-in
  registers 86, including the whole Torque game layer and its datablocks (`Player`, `PlayerData`,
  vehicles, particles, `Projectile`); 5.12 registers 22 3D ones (`GameObject`, `Sky`, `Sun`,
  `TerrainBlock`, `WaterBlock`, the replicators, the editors). The 5.12 property and function names
  per class are listed (T3D-014, T3D-016, T3D-019, T3D-020, T3D-050).
- [Entering a 3D server and the UDP ports](3d-server-entry-and-udp-port.md): a list name starting
  with `3 ` starts the 3D hand-over; the 3D UDP port is always the listed port + 1; only the client's
  own UDP port can be set (`fixedport`, `fixedudpport` 14899, `noudp`) (T3D-028, T3D-059).
- [Several 3D clients in one world: questions and lab design](3d-multi-client-lab-design.md): how
  each build shows other players, which channel carries them, what passes between clients, and mixed-build
  worlds; pair-by-pair lab plan (T3D-065 to T3D-076).
- [5.12 on our own 3D server: textures and client updates](live-512-own-server-textures-2026-11-25.md):
  texture naming and folders, which image formats draw, what the client sends for a Camera or GameObject
  control object, sky face order (T3D-023, T3D-032, T3D-033, T3D-046).
- [3D formats, renderer, camera and sound by build](3d-formats-renderer-camera-by-build.md): MD3,
  IFL, DML, `TSShapeConstructor`, `PathCamera` and `AdvancedCamera` are 4.04r2 only; 5.12 keeps DTS,
  DIF, 3DS and lists `.dsq`; the `.cs` in 5.12's file list is the GS2 file-access gate (T3D-013,
  T3D-031, T3D-034, T3D-035, T3D-051, T3D-055, T3D-062).
- [5.12 GS2 3D probe on our own server](live-512-gs2-3d-probe-2026-11-25.md): script-made objects do
  not draw, the sky and fog functions change nothing, loadGreyscale crashes without a TerrainBlock,
  and switchToOpenGL alone draws nothing (T3D-016, T3D-021, T3D-050, T3D-063, T3D-064).
- [The original TerrainGenerator compared with servertools](terraingenerator-original-vs-servertools-2026-11-25.md)
  (T3D-043).
- [The 3D engine DLL whole: client interface, net-event table, error paths, input](3d-engine-dll-interface-and-events-2026-11-26.md):
  the four export entry points and the host-callback table the exe hands in (with the exact `graal_set*`
  add/drop list per build); the 28-class / 9-networked-event table with per-event wire fields and
  server-assigned ids (`RequestReload` and `TerrainRequestUpdates` the only client→server events); the
  one `console.log` sink and which paths are fatal; input mapped to the client's `graalkeypressed` and
  mouse-look (the move packet is written by `GraalEngine.dll`, not the 3D DLL); and Windows 4.20r8 is
  byte-identical to 5.00r7/5.12 for the 3D wire (T3D-094, T3D-097, T3D-099, T3D-102, T3D-104, T3D-002).
- [The 5.12 GS2 3D scripting surface, typed](gs2-3d-typed-surface-512-2026-11-26.md):
  every 5.12 GS2 3D class, property and function with its argument and return types, read from the
  `TGraalVar` registration tables — 35 classes, 418 members (`GameObject` = 23 typed properties + 26 typed
  methods), the type codes, the 4.04r2 comparison (the stock camera/vehicle/control API is 4.04r2-only) and
  the global functions (`castRay`/`get3Dobjects`/`getz`/sky setters) with arity; the exact call shapes for a
  5.12 lab probe (T3D-096, and new rows T3D-121/T3D-122).

## Second batch (T3D-077 to T3D-092, 2026-11-25)

Added from the day's findings: texture and heightmap image limits per build, the 4.20r8 terrain
crash, protocol 21 against 24, which object classes each build draws, control-object variants,
ghost visibility between players, 3D sound and particles, the rest of the sky, `.dif` interiors and
collision, the 3D script functions on 4.04r2 and 5.00r7, what 3.153 accepts, shape packaging and
caching, out-of-range worlds, and mission lighting.

## The 3D DLL itself (T3D-093 to T3D-104, 2026-11-25)

Questions that cover the 3D engine DLL as a whole, build by build: its exports and imports and
how the client loads it; the interface between the 2D client and the 3D side in 5.12; which Torque
version it is built from; the full console registry; the NetEvent and ghost class tables with
their fields; the resource loaders and their checks; error paths and logs; the files it reads and
writes; its threads and frame loop; input; dead code against Graal additions; and the 4.20r8 and
5.00r7 differences from 5.12.

## Third batch (T3D-105 to T3D-114, 2026-11-25)

How close our renderer is to each client; what a level author can place and which files win (disk
or server); recovery from partial or bad data; the content subset that 4.04r2, 4.20r8 and 5.12
all draw; flags, weapons and NPCs across 2D and 3D; which state lives on the server and which on
the client; whether a server-sent name can make a client write outside its folders; frame rate
against content size; and a ranked fuzz target list per build. Overlapping questions already on
the board are not repeated: mixed-build worlds (T3D-072), 2D views of 3D players (T3D-073), ghost
scoping (T3D-075, T3D-083) and hard limits (T3D-037, T3D-091).
