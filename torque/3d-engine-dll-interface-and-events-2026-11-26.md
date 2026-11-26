# The 3D engine DLL whole: client interface, net-event table, error paths, input (T3D-094, T3D-097, T3D-099, T3D-102, T3D-104, T3D-002)

Date: 2026-11-26. Static reads of the Windows `Graal3DEngine.dll` for 4.04r2
(protocol 19), 4.20r8 and 5.00r7 (both protocol 24), plus the matching
`GraalEngine.dll`. Nothing was run. The 5.00r7 DLL is the one shipped as "5.12"
(byte-identical copy, [T3D-005](3d-engines-5007-512-and-403-411-2026-11-25.md)),
so "5.12" below means this DLL. Behaviour only; no addresses, no decompiled text.
Board rows: [T3D-094, T3D-097, T3D-099, T3D-102, T3D-104, T3D-002](3d-capability-board.tsv).
**[bin]**

Builds on [the engine static reads](3d-engine-static-reads-2026-11-25.md)
(exports and callbacks), [the networked class sets](3d-object-classes-by-build-2026-11-25.md),
[wire-by-build](wire-by-build.md) and [network.md](../protocol/network.md)
(the connect-accept class table), which are cited, not repeated.

## T3D-094: the full client ↔ engine interface

**The four entry points.** The 2D client (`GraalEngine.dll` + the Delphi
launcher) drives the 3D engine through a tiny exported surface and one callback
table:

- 4.04r2 and 4.11 export `loadGraal3DEngine`, `runGraal3DEngine`,
  `endGraal3DEngine`. 4.20r8 and 5.00r7 add `resizeGraal3DWindow` and
  `toggleGraal3DFullScreen` (five exports). 5.12 links the engine into the exe,
  so it exports none, but the same five entry shapes are present inside it.
- `loadGraal3DEngine(cmdline, hostTable)` **stores the host-callback table
  pointer** it is handed, parses the command line, then calls
  `graal_engineInitialize`. `runGraal3DEngine`, `endGraal3DEngine`,
  `resizeGraal3DWindow` and `toggleGraal3DFullScreen` are thin forwarders that
  call back through that stored table (its first four slots). So the exe owns the
  frame loop and window; the DLL is ticked by it and never spins its own thread
  ([T3D-101](3d-engine-static-reads-2026-11-25.md): no threads, no DirectInput).

**The host callbacks the engine calls back into.** The engine imports a block of
`graal_set*` setters from `GraalEngine.dll`; the exe registers each host
function through them at start-up, exactly as the 4.20r8 DLL did, except in 5.x
the names are imported rather than re-exported. Counts of `graal_set*` the
engine imports: **4.04r2 77, 4.11 80, 4.20r8 76, 5.00r7 / 5.12 78**. The 5.x set
is the drawing/text/tile/panel/clipboard/2D-matrix host surface plus the three
3D-specific ones (`graal_setCreateGraal3DGameObject`,
`graal_setGetGraal3DTerrainHeight`, `graal_setSendGraal3DScriptEvent(s)`) first
seen in 4.11.

**Changes across the protocol-24 builds (settles the T3D-094 "4 added / 2
dropped" note precisely):**

- 4.04r2 → 4.11 (the GameObject switch): drops six stock-TGE host calls
  (`DrawTriangleStrip`, `GetDatablockProperties`, `GetGraalRotationActivated`,
  `RemoveGraal3DDatablocks`, `ResetGraalRotation`, `SetGraalRotationAngle`) and
  adds nine (`CreateGraal3DGameObject`, `GetGraal3DTerrainHeight`,
  `IsOpenGLEnvironment`, the 2D-matrix pair `Push/PopGraal2DMatrix` and
  `IsGraal2DMatrixActivated`, `DeleteGraal3DLightInfo`, `DrawLine2`,
  `DrawPolygonEx`). This is the datablock-rotation host surface giving way to the
  GameObject + 2D-matrix overlay surface.
- 4.11 → 4.20r8: drops six (`GetEmoticonFilename`, `GetFilesForPattern`,
  `GetGraalApplicationActive`, `GetLevelFile`, `IsImageFile`,
  `SetEncodedPackageKey`), adds two (`FreeGraalTexture`, `GetGraal2DMatrix`).
- 4.20r8 → 5.00r7 / 5.12: drops two (`DrawGraphicsStretched`,
  `MakeGraalScreenshot`), adds four (`ForceTextureTransparency`,
  `GetGraalScreenCapture`, `PushColorMatrix`, `PopColorMatrix`). The screenshot
  host call becomes a screen-capture one and a colour-matrix pair appears.

**No version negotiation.** The exe loads the DLL by name and resolves the entry
points; there is no version field exchanged between the exe and the DLL, on any
of these builds.

## T3D-097: the complete net class and event table, per build

**How class ids are assigned (recap, [network.md](../protocol/network.md)).** The
ids are **not fixed**: the connect-accept carries a class-name table (`flag,
int12 type, int12 server id, string name` repeated, then the `u32` protocol), the
server chooses every id, and the client maps server id ↔ local id by name. On the
wire after that, every event and every ghost update carries the server's `int12`
class id and an `int14` bit-length wrapper; an id the client cannot map is read as
unknown and skipped by that length. The CRC table is static `{0xFFFFFFFF,0,0,0}`
with no writer. So the "table" below is the set of classes the client **can**
map, not a fixed numbering.

**Registered console classes.** 4.04r2 registers **117** (the full datablock
game layer); 4.20r8 and 5.00r7 / 5.12 each register the **same 28**: SimObject,
SimSet, SimGroup, MaterialPropertyMap, NetObject, NetConnection, GameConnection,
SceneObject, GameObject, Camera, TerrainBlock, WaterBlock, Sky, Sun,
MirrorSubObject, DynamicGrass, DynamicGrassReplicator, DynamicShapeReplicator,
fxSunLight, and the nine networked events below. **The 4.20r8 set is
byte-for-byte the 5.00r7 / 5.12 set** — this closes the T3D-002 / T3D-104
"static class diff queued" item: Windows 4.20r8's engine is protocol 24 with the
same 28 classes and the same event layouts as 5.12 (the 4.20r8 *lab* crash after
a TerrainBlock, [T3D-079](3d-capability-board.tsv), is therefore a runtime fault,
not a different class set).

**The networked events (the classes with a class-rep, so server-assignable an
id), with direction and the fields each reads off the wire.** `int N` = an
N-bit field; `string` = a Huffman string; `raw32` = a plain 4-byte read.
Direction is from the class-rep flag: **S→C** (the client unpacks it) or **C→S**
(the client only ever packs it). Identical on 4.20r8 and 5.00r7 / 5.12 (checked
field by field):

| Event | Dir | Fields read |
| --- | --- | --- |
| `BigDataStartEvent` | S→C | `int16` id, 3× `string`, `int24` size, `int3` type |
| `BigDataChunkEvent` | S→C | `int16` id, `int8` chunk length, raw bytes of that length |
| `ConnectionMessageEvent` | S→C | `raw32`, `int3`, `int11` |
| `NetStringEvent` | S→C | `int5` id, `string`; inserts the string into the tagged-string table at that id |
| `RemoteCommandEvent` | S→C | `int5` argc, then argc × a `int2`-tagged arg (0 empty, 1 string, 2 `int5`+tagged-string, 3 number) |
| `GhostAlwaysObjectEvent` | S→C | `int12` ghost index, then resolve-or-create the ghost |
| `TerrainChunkEvent` | S→C | `int4` block x, `int4` block y, `raw32`, `int10` length, raw compressed bytes; decompresses into the TerrainBlock at (x·16, y·16) |
| `RequestReloadEvent` | **C→S** | `string` object name → looked up as a GS2 var and sent as its net id |
| `TerrainRequestUpdatesEvent` | **C→S** | `raw32` |

So the client's own outbound 3D events are just two: **ask the server to reload
an object**, and **ask for terrain updates**. Everything visual (BigData world
text, ghost-always objects, terrain chunks, net strings, remote commands) is
server→client. `RemoteCommandEvent`'s `int5` argc is why an under-length RC event
runs a garbled command ([T3D-097 lab](3d-fuzz-net-tier1-2026-11-25.md)): the
count is trusted and each arg is pulled by its own type tag.

**The event base classes that are *not* networked content** (present on all
three, no server id): `NetEvent`, `SimEvent`, `NetDelayEvent`,
`SceneLightingProcessEvent`. The abstract `NetEvent` unpack slot is a CRT abort
stub — it must never be reached, i.e. every concrete event overrides it.

**Event classes 4.04r2 has and 5.12 does not** (gone with the datablock layer):
`SimDataBlockEvent`, `Sim2DAudioEvent`, `Sim3DAudioEvent`, `LightningStrikeEvent`,
`AudioEmitterLoopEvent`, `ObjectDeleteEvent`, `PathManagerEvent`,
`SimConsoleEvent`, `SimpleMessageEvent`. (The first four confirm
[T3D-081](3d-object-classes-by-build-2026-11-25.md)/[T3D-084](3d-sound-paths-2026-11-25.md);
`SimpleMessageEvent` is the one 4.11 kept and 4.20r6 dropped, [wire-by-build](wire-by-build.md).)

## T3D-099: error and crash paths

The engine routes messages through one console sink at three levels — **log**,
**warning**, **error** — all written to `console.log` in the client folder
([T3D-100](3d-engine-static-reads-2026-11-25.md)). The level is a severity tag
only; none of log/warning/error by itself ends the session. In the 5.12 DLL the
sink has ~82 log, ~38 warning and ~28 error call sites. The error strings that
matter for a server or a fuzz run, by what they do:

**Logged and the item dropped, link survives:**

- `Invalid event received (unknown event type)` / `(event could not be created)`
  / `(wrong direction)` — a warning; the event is skipped and the connection is
  flagged but not torn down.
- `Invalid packet.` — records a connection-error string (via the same path as
  `setGraal3DConnectionError` / `Connection error: %s`) and drops the packet.
- The format rejects that refuse content without harm:
  `Error: attempt to load a version %i dts-shape which is not supported anymore`
  and `…can currently only load version %i and before` (DTS bounds),
  `Sequence import failed: sequence version not supported anymore`,
  `Interior::read: incompatible file version found`,
  `InteriorResource::read: incompatible file version found`,
  `ForceField::read: incompatible file version found`,
  `Terrain texture of bad format (must be 256x256x24): %s`,
  `Error: bad shape file.`, `Unable to load interior: %s`,
  `Received unknown camera object.`, `Bad key in subObject stream!`
  All are logged errors; the renderer skips the asset. (This is the static side of
  the live "mislabelled DTS body hangs/crashes" finding, [T3D-029](live-512-shapes-2026-11-25.md):
  the *version word* is bounds-checked and rejected here, the *body* is not.)

**Fatal (the only paths that stop the client):**

- Network init failure shows a `Network Error` message box
  (`Unable to initialize the network... aborting.`, `Unable to initialize UDP -
  error %d`) and aborts. This is the one message box in the 3D set.
- A pure-virtual / unexpected-state call ends through the CRT abort stub
  (`runtime error`, `__amsg_exit`), as the abstract-event unpack slot shows.
- Video-mode failure (`Unable to create default Video mode: 640x480 16 bit
  window mode`, `Display Change Failed`) stops start-up before the session.

Everything else — bad assets, unknown classes, invalid events, oversized or
malformed content — is logged and skipped, which is why most fuzz content is
non-fatal ([T3D-038/097](3d-fuzz-net-tier1-2026-11-25.md)) while a few runtime
faults (mislabelled DTS body, oversized texture) crash in code with no error line.

## T3D-102: input and move packing

The 3D engine does **not** pack protocol-24 moves. Input reaches it as named
client **action** strings (the `moveMap2D` binds, [T3D-057](3d-engine-static-reads-2026-11-25.md)),
and one handler maps each name to a small **direction index + pressed flag** and
hands that to the client:

- Movement names → an index and the "key down?" flag, then a call to the client's
  `graalkeypressed(index, pressed)` (imported from `GraalEngine.dll`). Indices
  seen: forward/up 0, left 1, back/down 2, right 3, and 4/5/6/9/10 for the extra
  2D-style binds; `moveup2d`/`moveleft2d`/`movedown2d`/`moveright2d` map to 0–3
  with the 2D flag set.
- Mouse look names (`yaw`, `pitch`) accumulate into the client's `mouseyaw` /
  `mousepitch` float globals (also imported), scaled by the imported
  `mouseSensitivity`; mouse lock is the client's `mouseLock`/`mouseUnlock`.
- A batch of names are pure client-UI actions the engine forwards and returns
  (`togglefullscreen`, `toggleconsole`, `bringupoptions`, `showplayerlist`,
  `showloadlevel`, `showserverlist`, `contexthelp`, `domicro`, `escapefromgame`,
  `alttrigger`, `mousefire`, …), not moves.

So the actual move **packet** is assembled and written by `GraalEngine.dll`
(which owns `graalkeypressed`, `mouseyaw`, `mousepitch` and the
`GameConnection` move list); the 3D DLL only translates names to the engine's
move/look inputs. This closes the T3D-102 "protocol-24 move packing open" item:
the packing is not in the 3D engine at all.

## T3D-104: how 4.20r8, 5.00r7 and 5.12 differ

Same three reads, diffed. For the 3D wire they are the **same program**:

- **Net classes and events:** identical 28-class / 9-networked-event set, with
  byte-identical event field layouts (above). Protocol 24, same reject texts.
- **Host interface:** 5.00r7 / 5.12 add four host callbacks over 4.20r8 and drop
  two (the screenshot→screen-capture + colour-matrix change, §T3D-094).
- **Packaging / exports:** 4.20r8 ships the DLL with ~206 exports (the 76
  `graal_set*` re-exports plus the FreeType font API); 5.00r7 ships it with five
  exports and imports the callbacks instead; 5.12 links it in (no exports). All
  three import FreeType (`freetype6.dll`) for `.gft` fonts.
- **Loaders / bounds:** 4.20r8 and 5.00r7 / 5.12 both carry the DTS upper-bound
  reject (`…not supported anymore`) and the `.dsq` sequence-version reject;
  **4.04r2 has neither** — it only has the lower "version %i and before" line, so
  the 24-era added the "too old" DTS/DSQ rejects. Terrain textures must be
  256×256×24 on all three.

No functional 3D difference was found between 4.20r8 and 5.00r7 / 5.12 beyond the
four-for-two host-callback swap and the packaging; 5.12's extras over 5.00r7 are
the non-3D video/FFmpeg/FreeType items already recorded in
[T3D-005](3d-engines-5007-512-and-403-411-2026-11-25.md).

## For a server

- The id a server assigns in the connect-accept table is free; after that it must
  use its own ids for ghosts and events. A client only ever sends
  `RequestReloadEvent` and `TerrainRequestUpdatesEvent` back.
- To drive terrain, send `TerrainChunkEvent`s (block x/y as `int4`, so a 16×16
  block grid, `int10` compressed length); to drive world text / ghost-always
  content, `BigDataStartEvent` + `BigDataChunkEvent` (`int16` ids, `int24` size).
- Malformed assets and unknown classes are logged and skipped; only network-init,
  video-init and genuine code faults are fatal. A correct version word with a
  wrong body is the dangerous case — it passes the version check and can crash in
  the reader.
- 4.20r8 Windows is interchangeable with 5.00r7 / 5.12 for the 3D wire.
