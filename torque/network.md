# Torque networking in the Graal 3.x–5.12 clients

Date: 2026-10-30. Tags as in `README.md`.

## How a client gets to a 3D server

The server list marks a 3D server by a `"3 "` prefix on its name (the "Graal 3D" tab; see `protocol/v3x-clients.md` for the other prefixes). Choosing one runs the same routine in 3.153 (Mac, `0x39f148`), 4.04r2 (`GraalEngine.dll` `0x100be000`) and 5.12 (`Graal3DEngine.dll` `0x10199310`): **[bin]**

1. Strip the two-character prefix.
2. If the name had `"3 "`: remember **UDP port = listed port + 1**, set the "3D mode" flag, and start the Torque side.
   - 3.153: creates a `SimGroup` named `MissionGroup`, then `exec("main3D.cs")`. That script creates `GameConnection(ServerConnection)` and calls `connect()`; the engine supplies the stored address.
   - 4.04r2 and 5.12: first ask the launcher (`graal_setStartGraal3D` callback; a non-zero answer cancels), then call the launcher's `graal_setConnectTo3DServer` callback with host, port + 1 and the UDP option. In 4.04r2 that loads the separate `Graal3DEngine.dll`.
3. In **both** cases (2D or 3D) open the normal Graal TCP connection to host:listed port and log in as usual.

So a Graal3D server is two servers on one host: a Graal gserver on TCP *P* and a Torque server on UDP *P* + 1. The client's own UDP port is random unless `$pref::Graal::fixedport` is set, in which case it is `fixedudpport` (default 14899). **[bin][file]**

Seen live **[run]**: the real 5.12 client under Wine, told to join `"3 Seihai Test"` at `127.0.0.1:14800` (by calling its exported `connectToGraalServer(name, host, int port)` from an injected DLL, because no login server was available to list a 3D server). In the same millisecond it sent the Torque connect challenge to UDP 14801 and opened TCP 14800. The TCP side carried the ordinary 5.x login frame (`G3D14097`, account `guest`, then ids 37 and 23), the same bytes it sends to a 2D server.

## Torque packet framing

Stock TGE 1.x `NetInterface`. The first bit of a datagram picks the kind: **[bin]**

- bit 0 = 1: a data packet for an established `NetConnection` (Torque's notify protocol: sequence numbers, acks, then events, ghost updates and moves in a `BitStream`).
- bit 0 = 0: an "info" packet, byte-aligned. The first byte is the type:

| Type | Name | Direction | Body |
|---|---|---|---|
| `0x1A` | ConnectChallengeRequest | C→S | U32 connect sequence |
| `0x1C` | ConnectChallengeReject | S→C | (not handled by the Graal clients) |
| `0x1E` | ConnectChallengeResponse | S→C | U32 connect sequence, 4 × U32 address digest |
| `0x20` | ConnectRequest | C→S | U32 sequence, 4 × U32 digest, string class name (`GameConnection`), then the class's `writeConnectRequest` (below) |
| `0x22` | ConnectReject | S→C | U32 sequence, string reason |
| `0x24` | ConnectAccept | S→C | U32 sequence, then `writeConnectAccept` (U32 protocol version) |
| `0x26` | Disconnect | both | U32 sequence, string reason |

Types below `0x17` go to the master-server/LAN query handler. All integers are little-endian. Strings are Torque `writeString` (length byte + bytes, max 255).

Live capture **[run]** (5.12, Wine, `torque/tools/tq.py` answering):

```
C->S 1a 00040000                      challenge request, sequence 0x400
S->C 1e 00040000 00010203 04050607 08090a0b 0c0d0e0f   our challenge response
```

The 5.12 client did not go on to send `0x20` under Wine: starting the 3D view failed with "DirectX couldn't…" and a null-pointer fault, which stops its game loop. The connect request below is therefore read from the code, not captured.

## The connect request by version

`NetConnection::writeConnectRequest` first writes the **net class group** (U32, 0 = game) and the **class CRC** for that group (U32). Then `GameConnection::writeConnectRequest` writes: **[bin]**

| Field | 3.04 Linux | 4.04r2 | 5.12 |
|---|---|---|---|
| game string | `Torque Game Engine Demo` | `Graal3D` | `Graal3D` |
| U32 current protocol | 9 | 19 | 24 |
| U32 minimum protocol | 9 | 19 | 24 |
| string join password | server password pref | the account password, plain text | the account password, plain text |
| U32 argc (≤ 16), then argc strings | script args | 2: account, nickname | 2: account, nickname (field layout unchanged from 4.04r2) |

The 4.04r2 column comes from the v4 thread (`protocol/v4x-clients.md`); the 5.12 one is from `Graal3DEngine.dll` `0x1004e950` (write) and `0x1004ea00` (server-side read). 5.12's server-side read rejects with:

- game string not `Graal3D` → `CHR_GAME` ("Only official Graal clients are allowed to connect.")
- client current < 24 → `CHR_PROTOCOL_LESS` ("Please update your Graal, the server is requiring a new Graal version!")
- client minimum > 24 → `CHR_PROTOCOL_GREATER` ("The server runs an older version of Graal, contact the admins to update it.")
- argc > 16 → `CR_INVALID_ARGS`

The accept is one U32, the server's protocol. The 5.12 client accepts **exactly 24** (`0x1004e900`), 4.04r2 exactly 19, 3.04 exactly 9; anything else gives `CHR_PROTOCOL`.

**Class CRC.** Stock Torque compares the group and CRC and rejects a mismatch with `CHR_INVALID`. In 5.12 the CRC table at `0x1037754c` is static data `{0xFFFFFFFF, 0, 0, 0}` and nothing writes to it; reading it from the running client gave the same values. So a server that answers 5.12 sends group 0 and CRC `0xFFFFFFFF`. **[bin][run]** (3.04 and 4.04r2 read the same way from a static table; their values were not checked.)

**Encryption.** None beyond Torque's own framing. The join password travels in clear. **[bin]**

## After the connection is accepted

Mission download follows Torque's `MissionStartPhaseN` / `MissionStartPhaseNAck` remote commands (`commandToServer` / `clientCmd…`): **[bin][file]**

| Build | Phases |
|---|---|
| 3.153, 4.04r2 (stock TGE) | 1 "Download Datablocks & Targets", 2 "Download Ghost Objects", 3 "Mission Lighting" |
| 5.12 | 1 "Download Ghost Objects", 2 "Mission Lighting" (no datablocks exist any more) |

In 3.153 these are script functions (decompiled in the project folder, `dec3153/scripts_missionDownload.cs`): phase 1 acks with `commandToServer('MissionStartPhase1Ack', %seq)`, phase 3 calls `lightScene("sceneLightingComplete")` and acks phase 3 when lighting finishes. The loading screen is a snowball rolling across `LoadingGui` (`missionDownload2.cs`). In 5.12 the same steps are native and raise the GS2 event `onGraal3DLoginStep`.

Other Torque events and objects the Graal clients register (5.12, from RTTI): `NetStringEvent`, `RemoteCommandEvent`, `ConnectionMessageEvent`, `GhostAlwaysObjectEvent`, `RequestReloadEvent`, `TerrainChunkEvent` and `TerrainRequestUpdatesEvent` (terrain is streamed, see `engine-and-formats.md`), and Graal's own `BigDataStartEvent` / `BigDataChunkEvent`, which carry Graal text and scripts over the Torque connection (described from 4.04r2 in `protocol/v4x-clients.md`). **[bin]**

## For a Seihai 3D server

The minimum to get a real 5.12 client past the handshake: answer `0x1A` with `0x1E` (echo the sequence, any digest the server can later check), accept a `0x20` whose class group is 0, CRC `0xFFFFFFFF`, game string `Graal3D`, protocol 24/24, and reply `0x24` with protocol 24. From there it is Torque's notify protocol and ghosting, which open TGE 1.x source documents. Use 19 for 4.04r2 clients. Keep the Graal TCP server on the port below.

To repeat the live run: `wine-3d-lab/` in the project folder has `run3d.sh` (starts the listeners and the 5.12 client, then injects `conn.c` to join a fake 3D server) and `crc.c` (reads the CRC table from the running client).
