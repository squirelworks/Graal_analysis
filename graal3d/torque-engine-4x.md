# Graal 4.x 3D engine (Graal3DEngine.dll)

Date: 2026-10-30

The Windows Graal 4.04r2 client includes a 3D plug-in, `Graal3DEngine.dll` (linked 3 March 2006). It is a cut-down Torque Game Engine (TGE) with Graal changes. This note covers how the 2D client hands over to it, its network protocol to a 3D server, and the files it reads. Static reads only; nothing here has been checked on the wire.

This is not the 2000 standalone Graal3D (TCP 14901, `GR3DV002`); see `protocol.md` in this folder for that one.

Evidence tags as in `protocol/v4x-clients.md`: **[bin]** read from the binary, **[inf]** inferred, **[file]** from the shipped data.

## Overview

- The DLL exports three functions: `loadGraal3DEngine(char *cmdline)`, `runGraal3DEngine()` (one frame) and `endGraal3DEngine()`. It imports 623 symbols from `GraalEngine.dll`. **[bin]**
- The launcher (`Graal4.exe`) loads the DLL **on demand**, the first time the player picks a 3D server. It calls `loadGraal3DEngine("")` and, from then on, `runGraal3DEngine` once per frame. **[bin]**
- Once loaded, the DLL takes over **all** drawing for the engine: it registers the engine's text, bitmap, tile and panel callbacks, then re-initialises the engine. The 2D game then draws through Torque's GUI canvas. **[bin]**
- A 3D session uses **two connections to the same host**:
  - the normal Graal TCP game connection on the listed port;
  - a Torque UDP connection on **port + 1**.

  Both are opened together. **[bin]**
- The Torque console and TorqueScript are gone. Every engine object is exposed to Graal's GS2 script objects instead. There is no TorqueScript compiler, and `.dso` files are never requested. **[bin]**

## Hand-off from 2D

### Server list entry

A server whose list name starts with `"3 "` is a 3D server. The engine strips the two-character prefix for display. **[bin]**

### Connecting

When the player connects to a server by name:

1. If the name starts with `"3 "` and the engine is not in 3D mode yet, it calls the launcher's "start Graal3D" callback with (name, host, port).
   - The launcher loads `GRAAL3DENGINE.DLL`, which removes that callback.
   - The launcher then reconnects with the same three values. **[bin]** That the reconnect call is `connectToGraalServer` is **[inf]**.
   - If the DLL is missing, the launcher has the text "You need to download Graal3D at … for playing this server!" **[bin][inf]**
2. With the DLL loaded:
   - The engine sets its 3D-mode flag (`isGraal3DMode()` returns it).
   - It calls the DLL's `connectTo3DServer(host, port + 1, localUdpPort)`.
   - It opens the Graal TCP connection to `host:port` exactly as for a 2D server: login id 5, then id 37 (see `protocol/v4x-clients.md`). **[bin]**
3. `localUdpPort` is the `fixedudpport` option (default 14899) when the `fixedport` option is on. Otherwise it is 0, meaning any free port. **[bin]**

### State the DLL receives

The DLL pulls the login data from the engine through `getGraalLoginInfo()`. That function returns account name, nickname and password: the same values the launcher stores in the registry (`accountname`, `nickname`, `password`). **[bin]** No session key or cookie is passed. **[bin]**

### Callbacks the DLL gives the engine

| Callback | What it does in the DLL |
|---|---|
| connectTo3DServer(host, port, localPort) | Creates the client `MissionGroup`. Opens the UDP port. Creates a `GameConnection` named `ServerConnection` and connects to `host:port`. |
| removeGraal3DConnection(reason) | Disconnects the Torque connection. |
| sendGraal3DScriptEvent(name, params) | Queues a Graal event line for the 3D server (see "Graal events"). |
| sendGraal3DScriptEvents() | Flushes the queue. |
| sendGraal3DServerText(a, b, c, d) | Sends one text message over the big-data channel. No caller was found in the engine. |
| removeGraal3DDatablocks(), removeGraal3DMissionGroup() | Clean up on a level or server change. |
| getDatablockProperties(obj, list) | Lists datablock fields for GS2 scripts. |
| setGraalWindowLocked, getAllowCursorOff, getGraalPlayerScriptObject | Mouse lock and the script object for the local player. |

**[bin]**

When the Torque connection times out ("The 3D server connection has timed out"), the DLL reports it with `setGraal3DConnectionError`. The engine then also drops the TCP session. **[bin]**

## Torque connection

Except where marked, everything below is stock TGE 1.x. Every field is a BitStream bit field, written least-significant bit first. `u8`/`u32` are 8/32-bit fields; `intN` is an N-bit field; `flag` is one bit; `str` is TGE's Huffman-coded string (the character-frequency table is identical to TGE's). **[bin]**

### Out-of-band handshake

| Packet | Type | Layout |
|---|---|---|
| Connect challenge request | 26 (0x1A) | u8 type, u32 connectSequence |
| Connect challenge response | 30 | u8 type, u32 sequence, 4 × u32 address digest |
| Connect request | 32 | u8 type, u32 sequence, 4 × u32 digest, str `GameConnection`, then the request fields below |
| Connect accept | 36 | u8 type, u32 sequence, **class table**, u32 protocol version |
| Connect reject / disconnect | 34 / 38 | as in TGE |

**[bin]** The address digest is TGE's MD5 over the client address, the sequence and a random server key. **[bin][inf]**

**Connect request fields:**

| Field | Value sent by this client |
|---|---|
| u32 net class group | 0 (game) **[inf]** |
| u32 class CRC | A per-build value. The stock code rejects a mismatch with `CHR_INVALID`, so a custom server should skip this check. |
| str game name | `Graal3D` |
| u32 current protocol | **19** |
| u32 minimum protocol | **19** |
| str join password | The player's **Graal password, in clear text** |
| u32 argc | 2 |
| str argv[0], argv[1] | Account name, nickname |

**[bin]**

- Rejection reasons the code knows: `CHR_GAME`, `CHR_PROTOCOL_LESS`, `CHR_PROTOCOL_GREATER`, `CHR_PROTOCOL`, `CHR_INVALID`, `CR_INVALID_ARGS` (more than 16 arguments). **[bin]**
- The accept must carry protocol version 19 exactly. 5.00r7 uses 24 instead (`protocol/v5x-clients.md`). **[bin]**

**Class table (Graal change).**

```
for each class:  flag 1, int12 type, int12 classId, str className
end:             flag 0
```

The server lists its own networked classes this way, inside connect accept. The type is 0 (object), 1 (datablock) or 2 (event). The client matches each name against its own classes and keeps a map in both directions. From then on, every class id on the wire is **12 bits, in the server's numbering**. A class the client doesn't know maps to "unknown" and is skipped. So a server can pick its own ids, as long as it sends the names. **[bin]**

### Packet header and rates

- Header (stock TGE): flag 1, int1 (sequence parity), int9 packet sequence, int9 highest ack, int2 type (0 data, 1 ping, 2 ack), int3 ack byte count, then the ack mask. **[bin]**
- Then: flag (rate changed) → int10 update delay, int10 packet size; flag (max rate changed) → two int10s. **[bin]**
- Rate preferences:

| Pref | Default | Allowed range |
|---|---|---|
| `pref::Net::PacketRateToServer` | 32 | 8–32 |
| `pref::Net::PacketRateToClient` | 32 | 1–32 |
| `pref::Net::PacketSize` | 800 | 100–450 |

  The update delay is 1024 / rate ms. So in practice the client runs at 32 packets/s, 450 bytes each. **[bin]**

### Length prefixes (Graal change)

Every event, every ghost update and every datablock is sent as `int14 bitLength` + payload. The reader always jumps to the end of the payload, so an unknown or newer class can be skipped. **[bin]**

### Server → client data packet

1. int32 last move ack.
2. flag → { flag → float7 damage flash; flag → float7 white-out }.
3. flag (control object). Then either:
   - flag (dirty) → u32 **server time**, int12 control-object ghost, the control object's packet data;
   - or 3 × F32 compression point.
4. flag (camera) → int12 camera ghost, flag → camera packet data.
5. flag → int8 field of view.
6. Events, then ghosts.

**[bin]** The u32 server time is a Graal addition. **[bin]**

### Client → server data packet

1. flag (first person). **[inf]**
2. 3 × F32 position of the control object, then flag → int12 its ghost index.
3. flag (client sends its own state) → the control object's packet data. Otherwise: int32 first move index, int5 move count (up to 30), the moves.
4. flag → int8 field of view.
5. Events, then ghosts.

**[bin]** While the player controls an object, the client sends that object's state instead of moves, so position is client-reported, as in 2D Graal. **[inf]**

### Events

- Unguaranteed events: flag 1, int12 class id, sized payload, … flag 0.
- Guaranteed-ordered events: flag 1, flag (next in sequence) else int7 sequence, int12 class id, sized payload, … flag 0.

**[bin]**

| Event | Direction | Note |
|---|---|---|
| SimDataBlockEvent | server → client | int12 (id − 3), int12 class id, int12 index, int13 total, sized datablock data (TGE uses 10-bit ids) |
| GhostAlwaysObjectEvent, NetStringEvent, ConnectionMessageEvent, PathManagerEvent, SimpleMessageEvent | either | Stock TGE |
| RemoteCommandEvent | either | int5 argc, tagged-string arguments. The client acts only on `MissionStartPhase1/2/3` (see below). |
| Sim2DAudioEvent, Sim3DAudioEvent, LightningStrikeEvent | server → client | Stock TGE |
| BigDataStartEvent, BigDataChunkEvent | either | Graal text channel (below) |
| TerrainChunkEvent | either | Graal terrain streaming (below) |
| TerrainRequestUpdatesEvent | client → server | 256 × u32 (one per terrain chunk) |
| RequestReloadEvent | client → server | Asks the server to resend an object |

**[bin]**

### Ghosts (Graal changes)

1. flag (ghost data follows).
2. int4 **index width** (the number of bits of the highest index, sent as is; TGE sends width − 3).
3. For each ghost: flag 1, index, flag (delete). If not deleted: int12 class id (**sent on every update, not only the first**), sized update data.
4. flag 0 at the end.

**[bin]** New objects go into the client's `MissionGroup`. If the engine is still downloading files over TCP, they wait until the download is done. **[bin]**

Networked object classes, all stock TGE unless marked:

- **Shapes and players:** AIPlayer, Player, ShapeBase, StaticShape, Item, TSStatic, Shape3ds (Graal, 3DS models), Projectile, Debris, Splash.
- **Vehicles:** FlyingVehicle, HoverVehicle, WheeledVehicle, VehicleBlocker.
- **Cameras:** Camera, PathCamera, AdvancedCamera.
- **World:** InteriorInstance, PathedInterior, TerrainBlock, WaterBlock, Sky, Sun, Precipitation, Lightning.
- **Mission and markers:** GameBase, Marker, MissionArea, MissionMarker, SpawnSphere, WayPoint, Trigger, PhysicalZone, ScopeAlwaysShape, SimpleNetObject.
- **Effects:** AudioEmitter, ParticleEmitterNode, FractalTree, fxFoliageReplicator, fxGrassReplicator, fxShapeReplicator, fxShapeReplicatedStatic, fxLight, fxSunLight, volumeLight, twSurfaceReference.
- **Graal-only replicators:** DynamicGrass, DynamicGrassReplicator, DynamicShapeReplicator.

Datablock classes (stock TGE):

- **Shapes:** ShapeBaseData, ShapeBaseImageData, StaticShapeData, ItemData, PlayerData, TSShapeConstructor.
- **Cameras:** CameraData, PathCameraData, AdvancedCameraData.
- **Vehicles:** FlyingVehicleData, HoverVehicleData, WheeledVehicleData, WheeledVehicleSpring, WheeledVehicleTire.
- **Projectiles and effects:** ProjectileData, DebrisData, ExplosionData, SplashData, ParticleData, ParticleEmitterData, ParticleEmitterNodeData, PrecipitationData, LightningData, DecalData, fxLightData.
- **Audio:** AudioProfile, AudioDescription, AudioEnvironment, AudioSampleEnvironment.
- **Other:** GameBaseData, SimDataBlock, MissionMarkerData, PathedInteriorData, TriggerData.

**[bin]**

`ShapeBase` carries a Graal `chat` string: the text above a player's head, with `e_emoticon` handling. It is drawn by `GuiShapeNameHud` with a `chatprofile`. **[bin]** How the client's own chat reaches the 3D server was not found in the Torque code. It probably goes over the TCP connection as in 2D. **[inf]**

### Mission start

The server drives the start with `commandToClient`. The client handles these steps in native code:

| Server sends | Client does | Client answers |
|---|---|---|
| `MissionStartPhase1` | Script event `onGraal3DLoginStep(1)` | `commandToServer('MissionStartPhase1Ack')` |
| `MissionStartPhase2` | `onGraal3DLoginStep(2)` | `MissionStartPhase2Ack` |
| `MissionStartPhase3` | Starts scene lighting, `onGraal3DLoginStep(3)`. When lighting is done: `$missionRunning = 1`, `onGraal3DLoginStep(4)`. | `MissionStartPhase3Ack` (after lighting) |
| First control object (in a data packet) | Switches the screen to the `GUIContainer3D` GUI, `onGraal3DLoginStep(5)` | – |

**[bin]** Unlike the TGE example scripts, the acks carry **no sequence number**, only the command tag. Every other `commandToClient` name is ignored. **[bin]**

### Graal events and text (big-data channel)

Graal-specific data runs over two Graal events. **[bin]**

| Event | Layout |
|---|---|
| BigDataStartEvent | int16 transfer id, str `s1`, str `s2`, str `s3`, int24 total length, int3 compression (0 none, 1 zlib, 2 bzip2) |
| BigDataChunkEvent | int16 transfer id, int8 length (up to 191), the bytes |

The sender compresses with bzip2 over 4,095 bytes and with zlib over 49 bytes. It sends the start event and then up to 16 chunks per call. **[bin]**

**Server → client** (the only direction this DLL handles; its server-side handler is empty). When `s1` (a weapon name) is set, the data goes to that weapon as `onReceiveText(s2, s3, params)`. Otherwise `s2` selects the action:

| `s2` | Effect |
|---|---|
| `set` / `unset` | Set or clear the player flag in the data |
| `events` | One line per event: `s <flag>` sets a flag; `t <target>,<kind>,<action>,<params>` triggers `action<action>` on a weapon or GUI (`weapon`, `gui`) or an NPC (`npc`). Kind `rc` is RC chat (`onRCChat`); kind `torque` is ignored. |
| `addweapon` | Add weapon `s3`; the data holds a 5-byte Graal integer (a time stamp **[inf]**) |
| `weaponscript` | Script for weapon `s3` |
| `deleteweapon` | Remove weapon `s3` |
| `addnpc` | Script for the client-side object named `s3` |
| `setmaterials` | Terrain material list |
| `rpg` | `onRPGMessage(data)` |

**[bin]** So the 3D server, not the TCP gserver, delivers the client's GS2 weapons and flags in 3D mode. **[bin][inf]**

**Client → server.** The 2D engine's game events are queued as lines and sent as one message with `s1 = ""`, `s2 = "events"`, `s3 = ""`:

| Line | Comes from |
|---|---|
| `w <weapon>` | getweapon |
| `s <name>=<value>` | client-variable and flag sets |
| `t weapon,<name>,<params>` | serverside triggeraction from a weapon |

**[bin]**

### Terrain streaming (Graal)

- `TerrainChunkEvent` carries: int4 chunk x, int4 chunk y, u32 stamp **[inf]**, int10 length, then a zlib-compressed 16 × 16 piece of heights and materials. 16 × 16 chunks make a 256 × 256 terrain. **[bin]**
- The client tells the server what it already has with `TerrainRequestUpdatesEvent` (256 × u32). It caches terrain under `levels3d/terrain/`. **[bin][inf]**
- `.ter` files are never requested over TCP. **[bin]**

## The TCP gserver connection in 3D mode

The Graal TCP connection stays up for the whole session. **[bin]**

| Traffic | In 3D mode |
|---|---|
| S→C 0 `LEVELBOARD`, 14 `PLAYERWARP`, 28 `FLAGSET`, 31 `FLAGDEL`, 49 `PLAYERWARP2`, 101 `BOARDPACKET` | Ignored. The level, warps and flags come from the 3D server. **[bin]** |
| Level requests at startup, getweapon, client-variable and flag sets, serverside triggers | Rerouted to the 3D server (see above). **[bin]** |
| Chat, PMs, the player list, file transfer, RC | Not touched by the 3D-mode switch, so presumably still TCP. **[inf]** |
| Missing 3D resources (shapes, interiors, textures, sounds) | Fetched with the engine's normal TCP file download, by lower-case file name (everything except `.dso`, `.cs` and `.ter`). **[bin]** |

## Files

| Kind | Notes |
|---|---|
| `.dts` shapes | TGE format, version 24 or older. Sequence import is supported. **[bin]** |
| `.dif` interiors | TGE format: resource version 44, interior version 0. **[bin]** |
| `.ter` terrain | TGE format, version 3 or older. Normally streamed, not downloaded. **[bin]** |
| `.md3` | Quake 3 models, version 15 (`_lower`, `_upper`, `_head` parts plus skins and an animation config). Graal addition. **[bin]** |
| `.3ds` | 3D Studio models (`Shape3ds`). Graal addition. **[bin]** |
| `.gft`, `.dml` | TGE font and material-list files. **[bin]** |
| Images | `.png`, `.jpg`, `.jp2`, `.jng`, `.mng`, `.gif`, `.bmp`, `.bm8`, `.tga`, `.dds`. **[bin]** |
| `.zip`, `.gpake` | Archives the resource manager opens. **[bin]** |
| `.mis` | Not used. The mission arrives over the network. **[bin][inf]** |
| `.dso`, `.cs` | Not used as TorqueScript; never downloaded. **[bin]** |
| `levels3d/gui/*.png` | Shipped GUI skins: `default*` and `guiblue_*` controls, player-list and PM-bubble images, `defaultnamehud.png`, `default3darrow.png`, the title screen. **[file]** |
| `levels3d/help/*.hfl` | Help pages (About, Links, Key shortcuts). **[file]** |
| `languages3D/language*.cs` | Nine languages, each a list of `$language::Name = "text";` lines. Neither binary names these files, so they are probably loaded by server GUI scripts. **[file][inf]** |

## Torque version

The DLL matches open TGE 1.x in:

- the out-of-band packet numbers and layouts;
- the packet header;
- the Huffman string table;
- the rate limits;
- the DTS, DIF and TER versions;
- its class list.

It has none of TGE 1.4's new lighting system. So it comes from the same TGE 1.2/1.3 line as the 3.x client. **[bin][inf]**

Open TGE source (1.3 to 1.5) is a good base for the formats and the low-level net layer. A compatible client or server must add the Graal changes:

- the class table in connect accept, with 12-bit class ids;
- 14-bit length prefixes on events, ghosts and datablocks;
- a class id on every ghost update, and the raw index width;
- 12-bit datablock ids;
- the server time and client state in the game packets;
- the acks without a sequence number;
- the big-data and terrain events;
- GS2 in place of TorqueScript.

## Not done

- Exact `Player` and `ShapeBase` update layouts (Graal adds at least `chat` and a name colour).
- How the 3D server authenticates the player. The client sends the plain password in the connect request, and the TCP session is open at the same time.
- ~~How the per-build class CRC is computed.~~ It is not computed: the table at `0x101ba8b4` is static `{0xFFFFFFFF, 0, 0, 0}` and is only read (`torque/wire-by-build.md`).
- When the launcher shows "You need to download Graal3D".
- A capture from a real 2006 3D server, to check all of the above.
