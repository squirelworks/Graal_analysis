# Protocol 19 (3.153, 4.04r2): what a server must send, past the handshake

Date: 2026-11-13. Tags as in `README.md`. Static read of the 4.04r2 `Graal3DEngine.dll` (its readers for each layout below) and of 3.153's decompiled mission scripts. No real 3.153 or 4.04r2 client has been run past the handshake yet. This note fills in §10 of [udp-session.md](udp-session.md) for a **server**. It uses the smallest control object these clients take, a stock `Camera`, so it needs nothing from the still unread `Player` layout.

The Seihai GPL lab server implements this (`seihai-gserver-v2` PR #78, `graal3d = true`). **[srv]**

## 1. What is the same as protocol 24

These are unchanged from [udp-session.md](udp-session.md) §2 to §5 and §8. **[bin]**

- The handshake, data-packet header and 10-bit rate fields.
- The per-packet string buffer. `pstring` is in force here too: `GameConnection::readPacket` and `writePacket` give the stream a 256-byte buffer, as in 5.12.
- The two event lists, each event with `int12` class id and `int14` bit length.
- The ghost section: `int4` index width sent as is, then a class id and `int14` length on every update.

The class table in the accept has three types: object 0, datablock 1, event 2. **[bin]**

## 2. Server → client game section

```
u32      last move ack        (the index after the last move the server took)
flag     → { flag → int7 damage flash ; flag → int7 white-out }
flag A   control object
  flag B   dirty → u32 server time, int12 control ghost, the object's packet data
           else  → 3 × f32 compression point
flag     camera → int12 ghost (must be a ShapeBase ghost; else "Received unknown camera object"
                  and the rest of the packet is dropped), flag → camera packet data
         (flag clear: no camera object; the control object is the view)
flag     → int8 field of view
```

The control ghost is looked up as a `ShapeBase`. The first control object a 4.04r2 client gets raises login step 5. **[bin]**

The client drops moves from its queue up to the move ack. **[bin]**

## 3. Client → server game section

```
flag     first person (set when the camera distance is 0)
3 × f32  control object position (zeros before there is one)
flag     → int12 control ghost
flag     the control object sends its own state → its packet data
         else → u32 first move index, int5 count (≤ 30), the moves
flag     → int8 field of view
```

The state branch is taken only for a control object that carries the vehicle type bit. A `Camera` or `Player` client sends moves. **[bin]**

**One move:**

```
flag → int16 yaw ; flag → int16 pitch ; flag → int16 roll   (each sent only when non-zero)
int6 x ; int6 y ; int6 z                                    (16 = no movement)
11 flags: free look, then ten trigger flags
```

A move with no rotation is 32 bits. **[bin]**

## 4. Connection messages: TGE 1.x numbering

`ConnectionMessageEvent` is `u32` sequence, `int3` message, `int11` ghost count. The 4.04r2 client uses TGE 1.x's numbering, with five NetConnection messages, so GameConnection's datablock pair is at 5 and 6. Torque3D adds a sixth NetConnection message and numbers the pair 6 and 7. **[bin]**

| # | Name | Direction | Client behaviour |
|---|---|---|---|
| 0 | GhostAlwaysDone | S→C | Queues a marker behind the ghost-always objects it is still adding, then answers 1 with the same sequence |
| 1 | ReadyForNormalGhosts | C→S | |
| 2 | EndGhosting | S→C | Deletes every ghost |
| 3 | GhostAlwaysStarting | S→C | GS2 event `onGhostAlwaysStarted(count)` |
| 4 | SendNextDownloadRequest | – | |
| 5 | DataBlocksDone | S→C | Queues a marker behind the datablocks it is still loading; when it reaches it, answers 6 with the same sequence |
| 6 | DataBlocksDownloadDone | C→S | |

Messages 0, 2, 3 and 4 are refused with "Invalid packet" (a disconnect) while the client has no ghost table. The ghost section is ignored in that state too. **[bin]**

## 5. Mission start

| Server sends | 4.04r2 (native) | 3.153 (TorqueScript) |
|---|---|---|
| `MissionStartPhase1` (seq, mission name) | Logs "Phase 1: Download Datablocks", `onGraal3DLoginStep(1)`, acks at once: bare `MissionStartPhase1Ack` | `clientCmdMissionStartPhase1(%seq, %missionName, %musicTrack)`: `commandToServer('MissionStartPhase1Ack', %seq)` |
| datablocks, then message 5 | Loads each one (`onDataBlockObjectReceived(index)`), then answers 6 | the same native code |
| `MissionStartPhase2` (seq, mission name) | "Phase 2: Download Ghost Objects", step 2, bare ack at once | `clientCmdMissionStartPhase2(%seq, %missionName)`: ack with `%seq` |
| `MissionStartPhase3` (seq, mission name) | "Phase 3: Mission Lighting", starts lighting, step 3. When lighting is done: `$missionRunning = 1`, step 4, bare `MissionStartPhase3Ack` | `clientCmdMissionStartPhase3(%seq, %missionName)`: `lightScene`, then on completion `commandToServer('MissionStartPhase3Ack', $MSeq)` |
| first control object | step 5 | – |

The 4.04r2 sources are **[bin]**; the 3.153 column is **[file]**. 4.04r2 ignores every other `commandToClient` name. **[bin]**

A workable server order is the one stock TGE servers use:

1. Phase 1.
2. On its ack: the datablocks, then message 5.
3. On message 6: phase 2, message 3, and the ghosts.
4. When phase 2 is acked and the ghosts are in: message 0, then phase 3.
5. On phase 3's ack: the control object.

Send no ghost before message 6. A ghost naming a datablock the client has not loaded fails its update, and the client drops the connection with "Invalid packet". **[bin][srv]**

## 6. SimDataBlockEvent

```
int12  datablock id − 3
int12  datablock class id (server numbering, type 1)
int12  index        (passed to onDataBlockObjectReceived)
int13  total
int14  bit length, then the datablock's own data
```

If a datablock with that id already exists, the client unpacks into it. Otherwise it creates one of the class, unpacks it, and queues it to be preloaded in order. A preload failure gives "Invalid packet". **[bin]**

## 7. CameraData (= ShapeBaseData, nothing of its own)

Each "flag →" field is read only when its flag is 1. **[bin]**

| # | Field |
|---|---|
| 1 | `pstring` (SimDataBlock: the object name) |
| 2 | `pstring`, `pstring` (GameBaseData) |
| 3 | flag → `u32` (shape CRC) |
| 4 | `pstring` shape file. Empty: no shape is loaded, and preload succeeds |
| 5 | 9 × (flag → `f32`): mass, drag, density, max energy, then the camera distance and field-of-view limits **[inf]** for the names. Clear flags keep the defaults |
| 6 | `pstring` (a second file name; preload loads it when not empty) |
| 7 | flag |
| 8 | flag → `int12` (debris datablock id − 3) |
| 9 | 3 × flag |
| 10 | flag → `int12` (explosion datablock id − 3) |
| 11 | flag → `int12` (underwater explosion datablock id − 3) |
| 12 | flag |
| 13 | up to 8 × { flag 1, mount data } ended by flag 0. The mount data is not read here: send flag 0 |
| 14 | 2 × flag |
| 15 | `u32` |
| 16 | flag |
| 17 | `f32` count N (read as a float). Then for each of N: flag → a sequence reference |
| 18 | flag. Only when it is set and N > 0: N × 6 `f32` |

The smallest CameraData is: name, two empty strings, flag 0, empty shape, nine 0 flags, empty string, five 0 flags, 0, 0, 0, 0, 0, 0, `u32` 0, 0, `f32` 0.0, 0. That is 137 bits with empty names and the string prefix flags on. **[bin][srv]**

## 8. Camera ghost update

```
GameBase:   flag → pstring object name
            flag → 3 × f32 position
            flag → int12 datablock id − 3        (the create must carry it)
ShapeBase:  flag  main section; 0 ends ShapeBase's part   (its contents are not read yet)
Camera:     flag  "controlled by this client": 1 ends the update
            flag → 3 × f32 position, f32 rot.x, f32 rot.z
```

The Camera's type mask has the camera bit only, not the vehicle bit. Its default mode is fly (2). **[bin]**

## 9. Camera packet data (control object, both directions)

```
f32 energy, f32 recharge rate       (ShapeBase; GameBase adds nothing)
3 × f32 position, f32 rot.x, f32 rot.z
int3 mode                           (0 stationary, 1 free rotate, 2 fly, 3 orbit object, 4 orbit point)
modes 3 and 4: 3 × f32 orbit distances (min, max, current)
mode 3: flag, int12 orbited ghost
mode 4: a compressed point
```

**[bin]**

## Open

- [ ] A real 4.04r2 and 3.153 run against this order (the GPL lab server, PR #78).
- [ ] `ShapeBase`'s main update section and `Player`'s update, packet data and `PlayerData` (Graal adds at least `chat` and a name colour), so other players can be shown and a `Player` can be the control object. Started: `PlayerData` is ShapeBaseData, then flag, flag → `pstring`, 19 × `f32`, `int7`, 17 × `f32`, 19 × (flag → `int12` datablock id − 3), 3 × `f32`, flag → `int12`, 2 × `f32`, flag → `int12`, `f32`, 2 × (flag → `int12`), 3 × (flag → `int12`), 9 × `f32` **[bin]**. Tying each float to a field name and value, and the `Player` update's bit widths, are still to do. A `Player` also needs a real shape (a TGE `.dts` with the player sequences) for the client to animate, and none is in the archives.
- [ ] 3.153's Camera, CameraData and move layouts. They are assumed to match 4.04r2 (same Torque line, same net classes); not checked against the Mac binary.
