# Torque on the wire, build by build (3.04 to 5.12)

Date: 2026-10-30. Tags as in `README.md`. Everything here is a static read of the client binaries (the 3.04 Linux and 3.153 Mac decompiles, the 4.04r2 and 5.12 `Graal3DEngine.dll`, the 4.20r6 Mac client). Nothing new was run. Addresses are for orientation; the decompiles stay in the project folder.

This note fills the gaps the other Torque notes left open: the 3.153 and 4.20r6 columns, the class CRC in 4.04r2, the 5.12 game packets, and the 5.12 `GameObject` update. The 4.04r2 plug-in itself is described in full in `graal3d/torque-engine-4x.md`; this note only compares against it.

## Which builds are Torque

| Build | Torque? | 3D side | Read from |
|---|---|---|---|
| 1998 to 2.31 (Delphi) | no | none (Graal3D 2000 is a separate DirectX program) | `version-profiles/matrix/` |
| 3.04 Linux (Jan 2004) | yes, the whole client | stock TGE networking, no 3D scripts shipped | `lin304.c` |
| 3.153 Mac (Feb 2005) | yes, the whole client | Graal-changed TGE, TGE game layer (Player, datablocks) | `mac315.c`, `mac.rtti` |
| 4.04r2 Win (Mar 2006) | 2D engine on Torque base classes; 3D in `Graal3DEngine.dll` | same family as 3.153 | `g3d404.c` |
| 4.20r6 Mac (Sep 2006) | yes, one binary | Graal's own `GameObject` layer, no datablocks | `mac420.c` |
| 4.20r8 Win (Jan 2007) | 2D engine on Torque base classes | the upload has no `Graal3DEngine.dll`, so not readable | `eng420.c` |
| 5.12 Win (Oct 2007) | one engine DLL for 2D and 3D | `GameObject` layer | `g3de512.c` |
| 5.24r3 and later | no (only the `GuiGraal3DCtrl` name is left) | none | `torque/engine-and-formats.md` |

**[bin]**

## The handshake per build

| | 3.04 | 3.153 | 4.04r2 | 4.20r6 | 5.12 |
|---|---|---|---|---|---|
| Game string | `Torque Game Engine Demo` | `Graal3D` | `Graal3D` | `Graal3D` | `Graal3D` |
| Protocol (current = minimum, accept must match exactly) | 9 | **19** | 19 | **21** | 24 |
| Class table in the accept | no (stock) | **yes, 3 types** | yes, 3 types | **yes, 2 types** | yes, 2 types |
| Class ids on the wire | stock (bit size from the class count) | 12 bits | 12 bits | 12 bits | 12 bits |
| Class CRC in the connect request | stock table (value not read) | not read | **`0xFFFFFFFF`** | not read | `0xFFFFFFFF` |
| Server side of the connect request | stock script `onConnectRequest` | stock script `onConnectRequest` | native | native | native |

**[bin]**

- **3.153 is not "the same family as 3.04"** on the wire, as `README.md` had it. Its `GameConnection::writeConnectRequest` (`0x122b18`) writes `Graal3D` and 19 twice, and its accept reader (`0x122a74`) wants exactly 19. Its connect-accept writers (in `0x260058` and `0x260544`) call the class-table writer (`0x2c954`, three types: object, datablock, event) and its accept handler (`0x260608`) reads the table (`0x2ca48`) before `readConnectAccept`, exactly as 4.04r2 does. Its class-id map (`0x2cbfc` / `0x2cc60`) has the same "identity until a table has been read" rule. **[bin]**
- **3.04 has no Graal changes** in Torque's net layer. Its accept handler (`0x81f9090`) reads the sequence and goes straight to `readConnectAccept`, which only checks for protocol 9 (`0x810db60`). It has none of the Graal net classes (no `BigData…`, no `TerrainChunkEvent`). **[bin]**
- **4.04r2's class CRC** is a static `.data` table at `0x101ba8b4` holding `{0xFFFFFFFF, 0, 0, 0}`. The only two references to it are the reads in `NetConnection::writeConnectRequest` (`0x1012c260`) and `readConnectRequest` (`0x1012c2b0`), so nothing ever computes a CRC. This answers the "how the per-build class CRC is computed" item in `graal3d/torque-engine-4x.md`: it is not; group 0 always sends `0xFFFFFFFF`, as in 5.12. **[bin]**
- **4.20r6 Mac** writes `Graal3D` and 21 (`0x15`), wants exactly 21 in the accept, and its class-id map takes type < 2, like 5.12. **[bin]**
- The port: 3.153's `main3D.cs` path, 4.04r2 and 5.12 all connect to **listed port + 1** (`network.md`). The 28000 in `protocol/v3x-clients.md` is only the default that Torque's address parser fills in when a string has no port. **[bin]**

So the line is: stock TGE in 3.04; Graal's net-layer changes (class table, 12-bit class ids, 14-bit length prefixes, BigData and terrain events) already in 3.153; the TGE game layer and datablocks dropped between 4.04r2 (Feb 2006 token) and 4.20r6 (Jul 2006 token); protocol 19 → 21 → 24.

## The networked class sets

A Seihai server sends these names in the accept. Read from the static class registrations (name, group mask, type, event direction), and cross-checked against the `ConcreteClassRep<…>` RTTI list where there is one: in 5.12 and 4.04r2 the two lists match one for one. **[bin]**

| Type | 4.20r6 Mac | 5.12 |
|---|---|---|
| object (0) | `Camera`, `DynamicGrass`, `DynamicGrassReplicator`, `DynamicShapeReplicator`, `GameObject`, `SimpleNetObject`, `Sky`, `Sun`, `TerrainBlock`, `WaterBlock`, `fxSunLight`, `twSurfaceReference` | the same, without `SimpleNetObject` and `twSurfaceReference` (10) |
| event (1) | `BigDataChunkEvent`, `BigDataStartEvent`, `ConnectionMessageEvent`, `GhostAlwaysObjectEvent`, `NetStringEvent`, `RemoteCommandEvent`, `RequestReloadEvent` (client → server), `SimpleMessageEvent`, `TerrainChunkEvent`, `TerrainRequestUpdatesEvent` (client → server) | the same, without `SimpleMessageEvent` (9) |

Every other class registers with group mask 0 (not networked). The `GameShape…` classes (DTS, DIF, 3DS, FT) are not net classes: they ride inside a `GameObject` update (below). **[bin]**

4.04r2 has 117 class registrations, 98 of them networked: 49 objects, 34 datablocks and 15 events (the full list is in `graal3d/torque-engine-4x.md`; `Item`, `Sky`, `Sun` and `Path` are registered by string address, so a plain string search misses them). 3.153's RTTI has the same TGE game, datablock and Graal event classes (including `BigDataStartEvent`, `BigDataChunkEvent`, `TerrainChunkEvent`, `TerrainRequestUpdatesEvent`, `DynamicGrass…`); of 4.04r2's net and datablock classes only `AudioProfile` is missing from it. **[bin]**

## 5.12 game packets (the `GameObject` era)

These are the client's own `GameConnection::readPacket` (`0x1004f080`) and `writePacket` (`0x1004f360`). They differ from 4.04r2's (`graal3d/torque-engine-4x.md`) in three ways: no move ack, no damage flash or white-out, and no moves at all. 4.20r6's reader (`0x74d90`) has the same shape as 5.12's. **[bin]**

**Server → client**, after the stock packet header and rate fields:

1. flag (control object) → flag (update follows) → u32 **server time** (ms; the client keeps it as its synchronised clock, likely what `timevar3` reads **[inf]**), int12 ghost index of the control object (must resolve to a `GameObject`), the object's packet data (its vtable `+0xfc`). A first control object starts login step 5.
2. flag (camera) → int12 ghost index (a `Camera`), flag → the camera's packet data. No camera flag clears the camera. An unknown ghost logs "Received unknown camera object."
3. flag → int8 field of view.
4. Then stock `NetConnection` data: events, then ghosts.

**Client → server:**

1. flag: set when a float in the connection (`+0x45c`) is 0.0. What it holds was not traced. **[inf]**
2. 3 × F32: the control object's position (the translation column of its transform, or zeros without one), then flag → int12 ghost index of the control object, or of the object it is mounted on.
3. flag (the client controls that object) → the object's packet data (vtable `+0xf8`). There is no "else moves" branch any more.
4. flag → int8 field of view, clamped to 1–179.
5. Then events and ghosts.

So in 5.12 the client always reports its own position, and no Torque `Move` structure is ever sent. **[bin]**

**Events and ghosts** are as in 4.04r2: every event and every ghost update carries an int14 bit length, ghost updates carry a class id on every update, and the ghost index width is a raw int4. In 5.12 the class id reader is `0x1000e0b0` (12 bits, then the server-to-local map), the length wrappers are `0x100984b0` / `0x10098510` (events) and `0x1009c0f0` / `0x1009c160` (ghosts), and new ghosts are added to `MissionGroup` (`0x10099780`). **[bin]**

**Login steps** (`onGraal3DLoginStep`, the value starts at −1): 2 phase 1 "Download Ghost Objects", 3 phase 2 "Mission Lighting", 4 lighting done, 5 the first control object, 6 the TCP file downloads have finished and the `GraalControl3D` GUI is attached. 4.04r2 numbers them 1 to 5 over three phases. **[bin]**

## The 5.12 `GameObject` update

`GameObject::packUpdate` (`0x100511a0`) and `unpackUpdate` (`0x10051640`) agree on thirteen flag-guarded sections. The mask bits are the server's dirty bits; on the wire each section is just a flag. Field names are only given where the code makes them clear; the rest are marked. **[bin]**

| # | Dirty bits | Payload after the flag |
|---|---|---|
| 1 | `0x1` | string, the object's name (empty for `unknown_object`) |
| 2 | `0x2` or `0x200` | 3 × 32 bits (velocity **[inf]**) |
| 3 | `0x8` | string (a setting of the movement object) |
| 4 | `0x10` | string (also passed to the movement object) |
| 5 | `0x20` | transform: position, rotation, then 32 bits (the packing of the first two was not traced) |
| 6 | `0x80` | string that creates or replaces the shape object (`shape` **[inf]**) |
| 7 | `0x40`, and a shape object exists | the shape object's own data |
| 8 | any of `0xF00`, and a movement object exists | int14 bit length, then the movement object's data |
| 9 | `0x1000` | string, the chat text (the reader handles `e:emoticon`) |
| 10 | always 0 from this DLL | (the reader takes a string and loads it as a script or image; what the real server sent here is unknown) |
| 11 | any of `0x3FC000` | the attribute list |
| 12 | `0x400000` | string, then 4 bytes of colour (RGBA, 0–255) (nickname and `nickcolor` **[inf]**) |
| 13 | `0x800000` | int16 of booleans: bits `0x01`, `0x04`, `0x08`, `0x10`, `0x20`, `0x40` are used |

The GS2 properties on `GameObject` are `alpha`, `attachedtoobject`, `attr`, `attrobjects`, `chat`, `collision`, `iseditorobject`, `liquidheight`, `liquidtype`, `movetype`, `nickcolor`, `nickname`, `scaledshapebox`, `shadow`, `shape`, `shapebox`, `showterrain`, `skin`, `solid`, `velocity` and `watercoverage`, so the unnamed strings and booleans are among these. Tying each section to its property needs the GS2 property dispatcher, which was not read. **[bin][inf]**

## For a Seihai Torque side

Pick the profile by protocol: 9 (3.04, stock TGE 1.x, no class table), 19 (3.153 and 4.04r2: class table with datablocks, TGE game classes, moves), 21 (4.20r6) and 24 (5.12): `GameObject` model, two-type class table, client-reported position. 21 and 24 share the packet shapes read above; the class sets differ by three names. The open items for a server are the `GameObject` property map, the rotation packing in section 5, and the movement and shape sub-object payloads.
