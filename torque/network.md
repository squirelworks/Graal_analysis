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
| `0x24` | ConnectAccept | S→C | U32 sequence, then (5.12) a class-name table, then `writeConnectAccept` (U32 protocol version) |
| `0x26` | Disconnect | both | U32 sequence, string reason |

Types below `0x17` go to the master-server/LAN query handler. All integers are little-endian.

Strings inside info packets are Torque `writeString`: one flag bit (1 = Huffman coded with Torque's fixed character-frequency tree, 0 = raw), a U8 length, then the codes or bytes. Info packets are a plain bit stream after the type byte, so fields after the first string are no longer byte-aligned. `torque/tools/tbits.py` reads and writes this format, including the Huffman tree. **[bin][run]**

### The full handshake, live

Seen live **[run]** from the real 5.12 client under Wine, answered by `torque/tools/tq.py`. Timestamps are relative to the challenge request. The 3-second gap before the connect request is the injector's own wait before it starts running frames:

```
+0.000 C->S 1a 00040000                                   challenge request, sequence 0x400
+0.000 S->C 1e 00040000 00010203 04050607 08090a0b 0c0d0e0f   challenge response (our digest)
+3.009 C->S 20 00040000 00010203 ... 0c0d0e0f 1d6213fd ...   connect request, 71 bytes (decoded below)
+3.009 S->C 24 00040000 00 30000000                       connect accept: seq, empty class table, protocol 24
+3.043 C->S 05 00 00 04 41 b8 00 ...                      first data packet (seq 1)
         ... one 17-byte data packet a second, and a 4-byte ping about every 4.6 s ...
+18.02 C->S 26 00040000 00 00                             disconnect, sequence 0x400, empty reason
```

The client's own console (captured by hooking its `Con::printf` at `0x1000a220`) logs the same steps: `Sending Connect challenge Request`, `Got Connect challenge Response`, `Sending Connect Request`, `Connection established 19`, and at the end `Issuing Disconnect packet.` / `You have been disconnected from the game server.`

The connect request decodes to exactly:

| Field | Value |
|---|---|
| type, sequence, digest | `0x20`, `0x400`, our 16 digest bytes echoed back |
| class name | `GameConnection` (Huffman string) |
| net class group, class CRC | 0, `0xFFFFFFFF` |
| game string | `Graal3D` |
| current / minimum protocol | 24 / 24 |
| join password | `7Y3bdzjf`, the plain built-in guest password (see `protocol/v5v6-windows-unpacked.md`), so for a real account it is the account password in clear |
| argc, argv | 2: `guest` (the account), then an empty string (the nickname, unset here) |

No bits are left over, so the field list above is complete.

**Why the client disconnected.** The disconnect came the moment our lab TCP listener (which never answers the Graal login) closed the TCP side. The client then reports `You have been disconnected from the game server.` and drops the Torque connection with `0x26`. So the 3D connection only lives as long as the Graal TCP connection. **[run]**

**How the live run got this far.** Under Wine the 5.12 launcher faults when it re-initialises DirectDraw on switching to 3D (`Error when loading and initializing DirectDraw: Access violation …` in `game_console.log`), and stops calling the engine's per-frame export `runGraal3DEngine`. The challenge request goes out from inside `connectToGraalServer`, but nothing processes the reply. The injector in `torque/tools/conn.c` calls `connectToGraalServer`, then calls `runGraal3DEngine` every 15 ms itself, which runs Torque's network processing and gets the client through the rest of the handshake. **[run]**

## The connect request by version

`NetConnection::writeConnectRequest` first writes the **net class group** (U32, 0 = game) and the **class CRC** for that group (U32). Then `GameConnection::writeConnectRequest` writes: **[bin]**

| Field | 3.04 Linux | 3.153 Mac | 4.04r2 | 4.20r6 Mac | 5.12 |
|---|---|---|---|---|---|
| game string | `Torque Game Engine Demo` | `Graal3D` | `Graal3D` | `Graal3D` | `Graal3D` |
| U32 current protocol | 9 | 19 | 19 | 21 | 24 |
| U32 minimum protocol | 9 | 19 | 19 | 21 | 24 |
| string join password | server password pref | a string the engine sets (`main3D.cs` sets none; not traced) | the account password, plain text | not traced | the account password, plain text |
| U32 argc (≤ 16), then argc strings | script args | engine-set args (not traced) | 2: account, nickname | not traced | 2: account, nickname (field layout unchanged from 4.04r2) |

The 3.153 column is from `0x122b18` (write) and `0x122c54` (server-side read, which ends in the stock script callback `onConnectRequest`); 4.20r6 from `mac420.c` (`wire-by-build.md`). The 4.04r2 column comes from the v4 thread (`protocol/v4x-clients.md`); the 5.12 one is from `Graal3DEngine.dll` `0x1004e950` (write) and `0x1004ea00` (server-side read). 5.12's server-side read rejects with:

- game string not `Graal3D` → `CHR_GAME` ("Only official Graal clients are allowed to connect.")
- client current < 24 → `CHR_PROTOCOL_LESS` ("Please update your Graal, the server is requiring a new Graal version!")
- client minimum > 24 → `CHR_PROTOCOL_GREATER` ("The server runs an older version of Graal, contact the admins to update it.")
- argc > 16 → `CR_INVALID_ARGS`

**The accept.** In stock TGE the accept body is one U32, the server's protocol. 5.12 inserts a **class-name table** in front of it, read by `0x1000ac20` before `readConnectAccept` (`0x1004e900`) runs: **[bin][run]**

```
repeat while readFlag() == 1:
    U12  class type    (must be < 2: 0 = net object, 1 = net event [inf])
    U12  server class id   (0..255)
    string class name  (Huffman string, e.g. "NetStringEvent")
U32  protocol          (must be exactly 24)
```

For each entry the client looks up its own class of that name, type and group, and records server id to local id (`0x103ae410`) and back (`0x103b0410`), 256 slots per group and type. Ghost and event class ids on the wire are then the **server's** ids. This replaces stock Torque's fixed class numbering, and it is why the class CRC no longer matters. An accept with an empty table (a single 0 bit) plus protocol 24 is enough to reach "Connection established", as in the live run above. An accept without the table bit (stock layout) is read one bit off, gives protocol 12, and is silently rejected. **[run]**

The 5.12 client accepts **exactly 24**, 4.20r6 exactly 21, 4.04r2 and 3.153 exactly 19, 3.04 exactly 9; anything else gives `CHR_PROTOCOL`. 3.153 and 4.04r2 also have the class table, with three types (object, datablock, event); 4.20r6 has two, like 5.12; 3.04 has none (see `wire-by-build.md`).

**Class CRC.** Stock Torque compares the group and CRC and rejects a mismatch with `CHR_INVALID`. In 5.12 the CRC table at `0x1037754c` is static data `{0xFFFFFFFF, 0, 0, 0}` and nothing writes to it; reading it from the running client and the live connect request both gave group 0 and CRC `0xFFFFFFFF`. The class table in the accept (below) takes the CRC's place. **[bin][run]** 4.04r2's table at `0x101ba8b4` is the same static `{0xFFFFFFFF, 0, 0, 0}` with no writer (`wire-by-build.md`). (3.04, 3.153 and 4.20r6 read from a static table too; their values were not checked.)

**Encryption.** None beyond Torque's own framing. The join password travels in clear. **[bin]**

## After the connection is accepted

Data packets use stock Torque `ConnectionProtocol` headers: flag 1, connect-sequence bit, 9-bit sequence, 9-bit highest ack, 2-bit type (0 data, 1 ping, 2 ack), 3-bit ack byte count, then the ack mask. The live client's first data packet (sequence 1) carries the "max rate" flag with two 12-bit values, which read as 2080 and 368 with the stock field order. Every data packet after that is 17 bytes with no events. A ping follows whenever nothing has been acknowledged for about 4.6 s. **[run]**


Mission download follows Torque's `MissionStartPhaseN` / `MissionStartPhaseNAck` remote commands (`commandToServer` / `clientCmd…`): **[bin][file]**

| Build | Phases |
|---|---|
| 3.153, 4.04r2 (stock TGE) | 1 "Download Datablocks & Targets", 2 "Download Ghost Objects", 3 "Mission Lighting" |
| 5.12 | 1 "Download Ghost Objects", 2 "Mission Lighting" (no datablocks exist any more) |

In 3.153 these are script functions (decompiled in the project folder, `dec3153/scripts_missionDownload.cs`): phase 1 acks with `commandToServer('MissionStartPhase1Ack', %seq)`, phase 3 calls `lightScene("sceneLightingComplete")` and acks phase 3 when lighting finishes. The loading screen is a snowball rolling across `LoadingGui` (`missionDownload2.cs`). In 5.12 the same steps are native and raise the GS2 event `onGraal3DLoginStep`.

Other Torque events and objects the Graal clients register (5.12, from RTTI): `NetStringEvent`, `RemoteCommandEvent`, `ConnectionMessageEvent`, `GhostAlwaysObjectEvent`, `RequestReloadEvent`, `TerrainChunkEvent` and `TerrainRequestUpdatesEvent` (terrain is streamed, see `engine-and-formats.md`), and Graal's own `BigDataStartEvent` / `BigDataChunkEvent`, which carry Graal text and scripts over the Torque connection (described from 4.04r2 in `protocol/v4x-clients.md`). **[bin]**

## For a Seihai 3D server

The minimum to get a real 5.12 client connected, tested live: answer `0x1A` with `0x1E` (echo the sequence, any digest the server can later check). Accept a `0x20` whose class group is 0, CRC `0xFFFFFFFF`, game string `Graal3D` and protocol 24/24. Check the join password against the account. Reply `0x24` with the sequence, the class table (every net object and event class the server will send, by name), a 0 bit, and protocol 24. Keep the Graal TCP connection on the port below alive, or the client drops the 3D one too. From there it is Torque's notify protocol, events and ghosting, which TGE 1.x and Torque3D source document. Use protocol 19 for 4.04r2 clients.

To repeat the live run: `wine-3d-lab/` in the project folder has `run3d.sh` (starts the listeners and the 5.12 client, then injects a DLL built from `conn.c` to join a fake 3D server and drive the engine's frames), `crc.c` (reads the CRC table from the running client), and the captures (`capture-512/`, `capture-512-full/`). Run it as `DLL=conn4 TQARGS=accept run3d.sh <name>`.
