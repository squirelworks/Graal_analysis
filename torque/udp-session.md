# The Torque UDP session, start to first ghost (for a client)

Date: 2026-11-12. Tags as in `README.md`, plus **[lab]** for what a real client did against
the Seihai test gserver (`seihai-gserver-v2`, `graal3d = true`) in the November 2026 labs, and
**[doc]** for behaviour taken from the open Torque2D / Torque3D net layer (MIT; see the licence
section of `README.md`, TGE 1.x source is not used).

This note puts the 3D side of a Graal 3.153 to 5.12 session in the order a **client** meets it:
how the UDP link starts after the TCP login, how packets are framed and numbered, and what the
first events, ghosts and control-object messages look like. It is written so a clean-room client
(Ato) can be built from it. It collects and corrects what `network.md`, `wire-by-build.md`,
`open-source-lineage.md` and `graal3d/torque-engine-4x.md` say, and adds what the 5.12 labs on
the Seihai gserver showed. No decompiler output and no binary addresses are reproduced.

Protocol 24 (5.00r7, 5.12) is the line that has been run end to end with a real client: login,
mission start, ghosts, control object, camera, sun, sky, login step 6 and a drawn 3D view
**[lab]**. Protocol 21 (4.20r6) shares its packet shapes **[bin]**. Protocol 19 (3.153, 4.04r2)
has been read but never run past the handshake; it is the stock TGE game layer and is covered
at the end. A real 5.12 client's whole UDP session is decoded in
[lab-2026-11-12-udp-trace.md](lab-2026-11-12-udp-trace.md); every datagram fits this note.

## 1. Two connections, one session

A 3D server is a server whose list name starts with `3 ` (the client strips the two
characters for display). Picking one, or being warped to one by `PLO_SERVERWARP` with a name
that starts with `3 `, makes the client open **two** links to the same host in the same
moment **[bin][run]**:

| Link | Port | What travels |
|---|---|---|
| Graal TCP | the listed port *P* | the ordinary login frame for that build, chat, PMs, player list, file downloads, RC |
| Torque UDP | *P* + 1 | handshake, mission start, ghosts (the 3D world), control object, flags, weapons and serverside triggers (as text, see §7) |

- The client's own UDP port is random unless the build's fixed-port option is on (4.x and
  5.x: `fixedudpport`, default 14899). **[bin][file]**
- The 3D decision is made on the **name only**: no packet flag or login type says "3D".
  **[bin]** (5.12: the 3D path also builds the 3D GUI from GS2 built into the client before
  connecting; the server does not have to send any GUI.)
- The TCP login is byte-for-byte the one the build sends to a 2D server. **[run]**
- While in 3D mode the client ignores TCP level boards, warps and flag packets; the level,
  warps and flags come over UDP. **[bin]**

### Ordering and matching

1. The challenge request leaves before, or in the same millisecond as, the TCP connect.
   **[run]** A client must not wait for the TCP login to finish before starting the Torque
   handshake.
2. The server ties the UDP link to a TCP session by the **account name** (the first argument
   of the connect request, §3) and the **source IP address**. A 5.x guest sends `guest` here,
   not the server-assigned guest name. **[lab]**
3. The Seihai gserver does not answer the connect request until that account's TCP login is
   done; the client simply repeats the request. **[lab]** A client should keep repeating it.
4. If no accept comes, the 5.12 client gives up after about 15 seconds with "The connection to
   the Graal3D server couldn't be established." **[lab]**
5. The two links live and die together: when the TCP side closes, the client sends a
   disconnect (`0x26`) on UDP and reports "You have been disconnected from the game server."
   **[run]** When the UDP side times out, the client reports "The 3D server connection has timed
   out" and drops TCP too. **[bin]**

### What a 5.12 client needs on TCP for the 3D view to show

- Every TCP file request the 3D world causes (shapes, textures, `basepackage.gupd`) must be
  answered, with the file or with `PLO_FILESENDFAILED`. Login step 6 waits for all of them.
  **[lab]**
- The client's "Connecting..." window only closes on `PLO_SERVERLISTCONNECTED`. Without it the
  3D view stays covered by a blue panel even at step 6. **[lab]**

## 2. Bit stream conventions

Everything on UDP is a Torque bit stream. **[bin][doc][run]**

- Bits are packed **least significant bit first** within each byte, bytes in order.
- `intN` is an N-bit unsigned field, low bit first. `u8`/`u32` are 8/32-bit fields; on a byte
  boundary a `u32` is little-endian bytes.
- `flag` is one bit.
- `f32` is the raw 32 IEEE-754 bits as a `u32`.
- `string` (out-of-band packets): `flag` (1 = Huffman coded, 0 = raw), `u8` length, then the
  Huffman codes or the raw bytes. The Huffman tree is built from Torque's fixed character
  frequency table (identical in every Graal build). `tools/tbits.py` reads and writes it.
- `pstring` (strings **inside data packets**, protocol 24): one extra `flag` first. 1 means
  "reuse a prefix of the previous string in this packet": an `int8` count of characters taken
  from the previous string, then a `string` with the rest. 0 means a plain `string` follows.
  The previous-string buffer starts empty at the start of each packet and is replaced by every
  string read. **[lab]** (This corrects `open-source-lineage.md`, which expected plain strings
  for 5.12: a real 5.12 client read the server's mission commands, sky texture list, shapes and
  nicknames with the flag present, and its own strings carry it too.) A writer may always send 0.
  For protocol 19 the same per-packet buffer is expected (stock behaviour) but not lab-checked.

## 3. Out-of-band handshake

An out-of-band ("info") packet has its first bit 0, so its first byte is even. It is byte-
aligned up to its first string. **[bin][run]**

| Type | Name | Direction | Body after the type byte |
|---|---|---|---|
| `0x1A` | challenge request | C→S | `u32` connect sequence |
| `0x1C` | challenge reject | S→C | (not handled by the Graal clients) |
| `0x1E` | challenge response | S→C | `u32` sequence, 4 × `u32` address digest |
| `0x20` | connect request | C→S | `u32` sequence, 4 × `u32` digest (echoed), `string` class name `GameConnection`, then the fields below |
| `0x22` | connect reject | S→C | `u32` sequence, `string` reason |
| `0x24` | connect accept | S→C | `u32` sequence, class table, `u32` protocol |
| `0x26` | disconnect | both | `u32` sequence, `string` reason |

**The connect sequence** is chosen by the client (`0x400` in the 5.12 lab run) and repeated in
every out-of-band packet of the link. Its **lowest bit** is the "connect sequence bit" in every
data packet header (§4), which is how both sides drop stray packets from an older link.
**[run][doc]**

**Connect request fields** after the class name **[bin][run]**:

| Field | 3.04 | 3.153, 4.04r2 | 4.20r6 | 5.00r7, 5.12 |
|---|---|---|---|---|
| `u32` net class group | 0 | 0 | 0 | 0 |
| `u32` class CRC | stock | `0xFFFFFFFF` (4.04r2) | not read | `0xFFFFFFFF` |
| `string` game | `Torque Game Engine Demo` | `Graal3D` | `Graal3D` | `Graal3D` |
| `u32` current protocol | 9 | 19 | 21 | 24 |
| `u32` minimum protocol | 9 | 19 | 21 | 24 |
| `string` join password | server password pref | 4.04r2: the account password in clear | not traced | the account password in clear |
| `u32` argc (≤ 16), then argc `string`s | script args | 4.04r2: 2, account then nickname | not traced | 2, account then nickname (may be empty) |

The 5.12 request seen live was 71 bytes and decoded with no bits left over. **[run]**

**Connect accept.** Graal inserts a class-name table before the stock protocol field
**[bin][run]**:

```
repeat:  flag 1, int12 class type, int12 server class id, string class name
end:     flag 0
u32      protocol   (the client accepts only its own number exactly)
```

- Class types: protocol 19 numbers them object 0, datablock 1, event 2; protocols 21 and 24
  object 0, event 1 (no datablocks). **[bin]**
- The **server** chooses the ids. From then on every class id on the wire (events, ghosts) is
  `int12` in the server's numbering, and the client maps it to its own class by name. A name the
  client does not know maps to "unknown" and its payloads are skipped by length. **[bin]**
- An empty table (one 0 bit) plus the protocol is enough for "Connection established".
  **[run]** A table that names every class the server will send is what the Seihai gserver uses
  in all labs. **[lab]**
- The stock accept (no table bit) is read one bit off by these clients and silently rejected.
  **[run]**
- 5.12's reject texts: game string wrong → "Only official Graal clients are allowed to
  connect."; client too old → "Please update your Graal, the server is requiring a new Graal
  version!"; client too new → "The server runs an older version of Graal, contact the admins
  to update it." **[bin]**

Class names for protocol 24 (server ids are free; this is the set and the order the Seihai
gserver sends) **[bin][lab]**:

- objects (type 0): `Camera`, `DynamicGrass`, `DynamicGrassReplicator`,
  `DynamicShapeReplicator`, `GameObject`, `Sky`, `Sun`, `TerrainBlock`, `WaterBlock`,
  `fxSunLight`
- events (type 1): `BigDataChunkEvent`, `BigDataStartEvent`, `ConnectionMessageEvent`,
  `GhostAlwaysObjectEvent`, `NetStringEvent`, `RemoteCommandEvent`, `RequestReloadEvent`,
  `TerrainChunkEvent`, `TerrainRequestUpdatesEvent`

4.20r6 adds `SimpleNetObject`, `twSurfaceReference` and `SimpleMessageEvent`.

### The 5.12 handshake as captured

From the 2026-10-30 run (sequence `0x400`, the test server's digest `00 01 … 0f`) **[run]**:

```
C->S 1a 00 04 00 00                                       challenge request, seq 0x400
S->C 1e 00 04 00 00  00 01 02 03 … 0e 0f                  challenge response
C->S 20 00 04 00 00  00 01 02 03 … 0e 0f  …(71 bytes)     connect request
S->C 24 00 04 00 00  30 00 00 00 00                       accept: empty table, protocol 24
C->S 05 00 00 04 41 b8 00 …(19 bytes)                     first data packet, seq 1
```

How the 10-byte accept reads: the type byte, the `u32` sequence (bits 8–39), the table's end
flag 0 at bit 40, then the `u32` protocol 24 at bits 41–72. 24 shifted up one bit is 48 = `0x30`,
so byte 5 is `30`, and the protocol's top bit spills into a tenth byte, which is 0. (Earlier
copies of this capture in `network.md` grouped the bytes as `00 30 00 00 00`; that grouping was
a transcription slip. `24 00 04 00 00 30 00 00 00 00` is the accept the real client took, and the
one the Seihai gserver's handshake test checks.) **[run]**

### Test vectors (hex, one line each)

Connect request from the real 5.12 client, 71 bytes, sequence `0x400`, the test server's digest
`00 01 … 0f`, the built-in guest password, account `guest`, empty nickname; it decodes with no
bits left over **[run]**:

```
2000040000000102030405060708090a0b0c0d0e0f1d6213fd6a4af4185809000000e0ffffffff41ac650e47670c0000000c00008008d1e976dc8548169b000000c082de7f0300
```

Connect accept with an empty table **[run]**:

```
24000400003000000000
```

Connect accept with the full protocol-24 table in the order listed above (objects as type 0 with
ids 0–9, events as type 1 with ids 0–8), sequence `0x400`, 276 bytes. Built with
`tools/tbits.py`, which encodes strings the same way the Seihai gserver does (Huffman whenever
it is shorter than the raw bytes); it decodes back to 19 entries and protocol 24 with 5 padding
bits **[srv]**:

```
24000400000100001aac96e82d0340006470ae5022c6b196ad05000168e15ca1448c632d5bebfa7a304e500b0003d0c2b94289184fe7acbfebebc138
412d00104085d844bfe26ef1180240011c984e2a01c0000e4c3d058003c8b07eb3648a188a270100012a3838e12d62289e048004a8b039997a92e77e
860100002322b8774ec8d5664f93b8f404032000464470ef9c90534883b8f4040340005aaca6448f81955cdf5af61f979e60000c408bd8591b748e22
2b6dc5dde231c4a527180004d0c1ed610ac6d4c7a52718000550a2eb91c2afa6082585b8f40403c0004a747d64f3dfa0eb8766884b4f30000e60c4fa
cd9269b5d9d3242e3dc10040801aeb374ba6ae8f6cfe1bc8b10e09dfe2d213c000000000
```

The two first client data packets **[run]**: `0500000441b800000000000000000000000000` (seq 1, 19
bytes) and `0900000800000000000000000000000000` (seq 2, 17 bytes).

## 4. Data packets: header, numbering, acks

A data-link packet has its first bit 1. **[bin][doc][run]**

```
flag     1
int1     connect sequence bit  (lowest bit of the connect sequence)
int9     packet sequence       (this packet's number, mod 512)
int9     highest ack           (the highest sequence received from the other side, mod 512)
int2     type                  0 data, 1 ping, 2 ack
int3     ack byte count        0..4
int(8 × count)  ack mask       bit 0 = the "highest ack" packet itself, bit i = highest ack − i
```

Then, **in data packets only** (type 0), the rate fields **[run][lab]**:

```
flag  current rate changed → int10 update delay (ms), int10 packet size (bytes)
flag  max rate changed     → int10 update delay (ms), int10 packet size (bytes)
```

The fields are **10 bits wide**. The real 5.12 client's first data packet carries the second
pair as 32 ms and 450 bytes, which is 1024 / 32 packets a second at the 450-byte cap. (`network.md`
read them as two 12-bit values, 2080 and 368; with 10-bit fields the same bits give 32 and 450,
and the rest of the packet then parses exactly.) Ping and ack packets end after the ack mask.

**Numbering rules** (as the real 5.12 client and the Seihai server keep them; stock
Torque **[doc]**, matched by **[lab]**):

- Each side numbers its **data** packets 1, 2, 3, … The first data packet of a link is 1.
  Ping and ack packets reuse the last data sequence; they do not consume a number.
- The receiver widens the 9-bit field against its last received sequence (add 512 when it
  wrapped). A packet more than 31 ahead of the last received one is dropped; a packet that
  does not advance the sequence is a duplicate and is dropped after its acks are read.
- **Acks.** On receipt, shift the receive mask left by (new sequence − last sequence) and set
  bit 0 if the packet was a data packet. Every outgoing header carries the last received
  sequence as "highest ack" and that mask, with `ack byte count` = enough bytes to cover the
  packets since the other side last acknowledged our acks (`min(4, (last received − last
  acked-ack + 7) / 8)`).
- When a header's "highest ack" moves forward, each of our packets from the previous highest
  ack + 1 up to it is either **delivered** (its bit set) or **lost**. That notification is the
  only delivery signal: guaranteed events and ghost updates from a lost packet are sent again.
- Keep at most 30 unacknowledged data packets in flight; when the window is full, send only
  acks.
- A **ping** (type 1) asks for an immediate **ack** (type 2). The 5.12 client sends a 4-byte
  ping when it has had nothing acknowledged for about 4.6 s. **[run]**
- With nothing to say, the 5.12 client still sends a data packet every second or two (17 bytes
  before it has a control object; 21 bytes after). **[run][lab]** The Seihai server times a link
  out after 30 s of silence. **[lab]**
- The 5.12 client answers **every** data packet from the server at once with a 5-byte ack packet
  (type 2), and sends no pings while the server's packets keep coming. **[lab]**
- Padding bits after the last field are not always zero (the client's first data packet in lab
  12 ends in `a0`). Stop reading at the last field. **[lab]**

The two captured client data packets, decoded **[run]**:

| Bytes | Header | Rest |
|---|---|---|
| `05 00 00 04 41 b8 00 …` (19) | seq 1, ack 0, data, no ack bytes | rate flag 0; max rate flag 1 → 32 ms, 450 bytes; then the game section (§6) |
| `09 00 00 08 00 …` (17) | seq 2, ack 0, data | both rate flags 0; game section |

## 5. Events

After the game section (§6) each data packet carries two event lists, then the ghost section.
**[bin][lab]**

```
unguaranteed:   { flag 1, int12 class id, int14 bit length, payload } … flag 0
guaranteed:     { flag 1, flag "next in order" (else int7 sequence), int12 class id,
                  int14 bit length, payload } … flag 0
```

- Every payload is preceded by its **bit length** (Graal's change), so the reader always skips
  to the end, and an unknown class costs nothing.
- Guaranteed events are numbered 0, 1, 2, … per direction. The "next in order" flag means
  previous + 1 within this packet; otherwise the low 7 bits are given. The receiver widens the
  7-bit value against the next expected number and delivers strictly in order, holding back
  any that arrive early. **[doc][lab]**
- An event is done when the packet that carried it is notified delivered; a lost packet's
  events go out again, in order, in a later packet. Keep at most 126 events past the oldest
  unacknowledged one. **[doc][lab]**
- The Seihai server sends only guaranteed events, and the 5.12 client took them. The client
  also sends every event of its own as guaranteed-ordered; no unguaranteed event was seen either
  way in the lab 12 trace. **[lab]** A reader should still accept both lists.

Event payloads, with `pstring` strings (§2):

| Event | Payload |
|---|---|
| `NetStringEvent` | `int5` string id, `pstring` text. Defines an entry in the sender's 32-entry tag table. |
| `RemoteCommandEvent` | `int5` argc, then each argument: `int2` code. 0 empty; 1 `pstring`; 2 tag, `int5` string id; 3 integer: `flag` negative, then `flag` → `int7`, else `flag` → `int15`, else `int31`. Argument 0 is the command name. |
| `BigDataStartEvent` | `int16` transfer id, `pstring` s1 (weapon), `pstring` s2 (type), `pstring` s3 (option), `int24` total length, `int3` compression (0 none, 1 zlib, 2 bzip2) |
| `BigDataChunkEvent` | `int16` transfer id, `int8` length (≤ 191), the bytes |
| `ConnectionMessageEvent` | `u32` sequence, `int3` message, `int11` ghost count (stock ghost-mode messages) |

**Tagged command names.** `commandToClient` sends the command name as a tag: first a
`NetStringEvent` that defines the string, then the `RemoteCommandEvent` whose argument 0 is
code 2 with that id. **[lab]** The 5.12 client answers with the name as a **plain string** (code
1), not a tag ([lab 12](lab-2026-11-12-udp-trace.md)); a reader should accept either.

## 6. Game sections (protocols 21 and 24)

Between the rate fields and the events, each data packet has a game section. It differs by
direction. **[bin][lab]**

**Server → client:**

```
flag A   control object section present
  flag B   control object follows (only if A)
    u32    server time (ms; the client's synchronised clock)
    int12  ghost index of the control object (must already be a GameObject ghost)
    ...    the object's packet data: a GameObject update (§8) with no length prefix
flag     camera →  int12 ghost index (a Camera ghost), flag → camera packet data
flag     field of view → int8
```

- A or B clear: the control object stays as it was.
- Name the control object only after its ghost **create has been acknowledged**, and only
  after the last mission phase is acknowledged (§7): `MissionStartPhase2` puts the 5.12 client's
  login step back to 3, and step 5 is only set by the first control object it receives. A
  control object that arrives earlier, even in the same packet as phase 2, leaves the client
  stuck at step 4. **[lab]**
- The packet data may carry no sections at all (all thirteen flags 0); the ghost carries the
  state. **[lab]**
- The camera index must also be an acknowledged `Camera` ghost: an index the client cannot
  resolve logs "Received unknown camera object" and the rest of that packet is lost. No camera
  flag clears the camera. Login steps 5 and 6 do not need a camera. **[bin][lab]**

**Client → server:**

```
flag     first person
f32 × 3  position of the control object (zeros before there is one)
flag     → int12 ghost index of the control object (or of what it is mounted on)
flag     the client controls that object → its packet data: a GameObject update (§8)
flag     field of view → int8 (1–179)
```

There are **no moves** in protocols 21 and 24: the client reports its own position in every
packet, and its own object's changes (transform, chat, shape) as an update. **[bin][lab]**
Before step 5 the captured packets carry first person = 1, a zero position and no object.
**[run]** In the first packet after it takes the control object, the 5.12 client sends the
object's shape, transform and flags back. It returns a zero rotation as axis (1, 0, 0), angle 0.
After that it sends the position, the ghost index and an empty 13-bit update while nothing
changes. **[lab]**

## 7. Mission start and the login steps (protocol 24)

The server drives the start with tagged commands; the 5.12 client answers each in native code
and raises the GS2 event `onGraal3DLoginStep` **[bin][lab]**:

| Server sends | Client shows / logs | Client answers | Login step |
|---|---|---|---|
| (link established) | "Connection established" | – | – |
| `MissionStartPhase1` | "Phase 1: Download Ghost Objects" | `MissionStartPhase1Ack` | 2 |
| `MissionStartPhase2` | "Phase 2: Mission Lighting", then "Mission lighting done" | `MissionStartPhase2Ack` | 3, then 4 |
| first control object (§6) | switches to the 3D GUI | – | 5 |
| (all TCP file requests answered, §1) | 3D view attached | – | 6 |

- The Seihai server sends `MissionStartPhase1` in its first data packet after the client's
  first data packet arrives. **[lab]**
- The acks carry no sequence number (the 3.153 TorqueScript version adds one, see §10). Any
  other `commandToClient` name is ignored by the 5.12 client. **[bin]**
- Ghosts may be sent from the start: the 5.12 client created ghosts without any
  `ConnectionMessageEvent` ghost-mode exchange. **[lab]**

**Graal text over BigData.** After the mission starts, the server sends flags, weapons and
scripts as text messages (start event, then chunks of up to 191 bytes, sent uncompressed is
fine). s2 selects the action: `set` / `unset` (one flag), `events` (lines `s <flag>`, and
`t <target>,<kind>,<action>,<params>`), `addweapon` / `weaponscript` / `deleteweapon` (s3 the
weapon name), `addnpc`, `setmaterials`, `rpg`; a non-empty s1 sends the text to that weapon's
`onReceiveText`. The client sends one `events` message (s1 and s3 empty) with lines
`w <weapon>` (getweapon), `s <name>=<value>` (flag or client-variable set) and
`t weapon,<name>,<params>` (serverside trigger). **[bin][lab]** (The labs confirmed the server
→ client `events` and weapon scripts arrive; the client compiled and ran a GS2 weapon sent as
bytecode.)

## 8. Ghosts and the GameObject update (protocols 21 and 24)

**Ghost section**, after the events **[bin][lab]**:

```
flag     ghost data follows (else nothing more)
int4     index width W: the number of bits of the highest index in this packet (sent as is, ≥ 1)
repeat:  flag 1, intW ghost index, flag deleted
           if not deleted: int12 class id, int14 bit length, update payload
end:     flag 0
```

- The class id comes with **every** update, not only the create. The first update of an index
  is the create and must carry the whole state; new objects go into the client's `MissionGroup`.
- Delivery is per packet notification (§4): a lost create is sent whole again, a lost update's
  sections are sent again, a lost delete is repeated. Free an index only after its delete is
  acknowledged. The client's table holds 4096 ghosts.
- The Seihai server keeps each packet under 400 bytes and orders deletes, then creates, then
  updates. **[lab]**

**GameObject update** (section order as the lab-tested server writes and reads it; this
supersedes the order in `wire-by-build.md`, which had sections 3, 6, 7 and 8 shifted)
**[bin][lab]**:

| # | Present when | Payload |
|---|---|---|
| 1 | name | `pstring` object name (`G3DPlayer_<account>` for players in the Seihai server) |
| 2 | velocity | 3 × `f32` |
| 3 | shape | `pstring` file name (`.dts`, `.dif`, `.3ds`, `.ft`); the client fetches a missing file over TCP |
| 4 | skin | `pstring` |
| 5 | transform | position 3 × `f32`, rotation axis 3 × `f32`, angle `f32` (radians) |
| 6 | movetype | `pstring`: `interpolate`, `list` or `rigid` create a movement object |
| 7 | movement data | only while a movement object exists: `list` = { flag 1, 8 × 32 bits } … flag 0; `interpolate` / `rigid` = 3 × 32 + 4 × 8 + 6 × 9 + 1 bits |
| 8 | shape data | `int14` bit length, then the shape object's own data (animation threads) |
| 9 | chat | `pstring` (handles `e:emoticon`) |
| 10 | script classes | `pstring` (never sent by the 5.x client) |
| 11 | attributes | 8 × { `flag` → `pstring` } for `attr[1]` to `attr[8]` |
| 12 | nickname | `pstring`, then 4 × `int8` colour (R, G, B, A) |
| 13 | flags | `int16`: 0x04 editor object, 0x08 solid, 0x10 shadow, 0x20 show terrain, 0x40 collision (0x01 also used) |

Each section is one `flag` followed, when set, by its payload. **All thirteen flags are always
on the wire**, section 7's included: the reader always reads section 7's flag, and reads the
movement data only when that flag is 1 **and** the object has a movement object (a movetype of
`interpolate`, `list` or `rigid`, from this update's section 6 or an earlier one). A server that
never sends a movetype always writes section 7's flag as 0. An update with all thirteen flags 0
(13 bits) is valid: it is the control object's packet data in §6. **[bin][lab]**

**Camera** = a GameObject update, then `flag` → `int1` camera mode, then `flag` → `flag` →
`int12` followed-object ghost. The Seihai server sends both flags 0; the client's scripts set
the mode and position. **[bin][lab]**

**Sun** = `flag` init, then only if it is 1: `pstring` name, direction 3 × `f32`, colour
4 × `f32`, ambient 4 × `f32`. An update with the flag 0 carries nothing more. The Seihai server
only ever sends the whole Sun (flag 1), on create and on change. **[bin][lab]** (The real client
shaded the world with it.)

**Sky.** The reader's full shape; every part after the name is guarded **[bin][srv]**:

```
flag init            → pstring name
flag material list   → f32 visible distance, pstring comma-separated texture list
                       (front, right, back, left, top, bottom)
if init:
  f32 × 3            fog colour
  u32 N              fog volumes
  int8, int8         two bools (whole 8-bit fields, 0 or 1)
  f32 × 3            solid colour
  int8               a third bool (8 bits)
  flag               (read and ignored)
  N × { f32 × 6, int8 }   the fog volumes
  3 × { pstring cloud texture, f32 height, f32 speed }
  f32 × 3            wind velocity
  u32                (unnamed)
  flag storm fog     → 5 × u32
flag → int8          (mask 0x20)
flag → int8          (mask 0x40)
flag                 (bare flag; the writer repeats the init state here)
flag → 2 × u32       (mask 0x2)
flag → 3 × u32       (mask 0x4)
flag → 4 × u32       (mask 0x8)
flag → 3 × u32       (mask 0x10)
```

So a later Sky update is the same reader with init 0: only the guarded parts that are set
follow. The Seihai server always sends the Sky whole (init 1, material list 1, N = 0, no storm,
trailing flags 0, 0, 1, 0, 0, 0, 0). The client asks for each texture over TCP **without** an
extension and loads them only when it unpacks the Sky, so a server sends the Sky again after the
downloads. **[bin][lab]** (The real 5.12 drew the sky box.) A Sky ghost update, like every ghost
update, also has its `int14` length, so a reader that does not decode Sky can skip it.

### Test vectors for §6 and §8

Written by the Seihai gserver's own encoder (`seihai-gserver-v2` PR #54 head, the build the real
5.12 client drew its world from in labs 7 to 10), so the bytes are the server's, not a real
server's. Strings carry the `pstring` prefix flag (0). **[srv][lab]**

Payloads (the bits after a ghost entry's `int14` length; the byte strings are padded with zero
bits at the end):

`GameObject` create, 471 bits: name `G3DPlayer_lab`, shape `labcube.3ds`, position (0, 0, 1), axis (0, 0, 1), angle 0, nickname `lab` with colour (255, 255, 255, 255), flags 0x48 (solid, collision):

```
6d887574de1b5979938ddce9c2c81df6bb2f1d431300000000000000000000f00700000000000000000000f00700000000e8c0c8ddffffff7f2400
```

Empty `GameObject` update (the control object's packet data), 13 bits: `0000`

`Sun`, 379 bits: name `Sun`, direction (0.57735, 0.57735, −0.57735), colour (0.8, 0.8, 0.8, 1), ambient (0.3, 0.3, 0.35, 1):

```
1d987ab2699ef8b1699ef8b1699ef86d6666fa696666fa696666fa010000fcd1ccccf4d1ccccf4999999f5010000fc01
```

`Sky`, 956 bits: name `Sky`, distance 500, textures `sky_fr,sky_rt,sky_bk,sky_lf,sky_up,sky_dn`, fog (0.5, 0.6, 0.8), bools 1 0, solid colour (0.4, 0.6, 0.9), bool 0, no clouds, no wind:

```
1d984e2a0100f4874c69938a6cb368b749456610ed36a9c8769368b7494536b668b74945e6eb68b7494516080000e0473333e3a79999e90700000020
00a09999d9473333e3c7ccccec0700000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000
```

A whole server session, as the server sends it, against a client that answers each mission phase
and acks every packet (the client's first packet is the real one from §3; the later client
packets are synthetic). Ghost 0 is the Sun, ghost 1 the player's `GameObject` (the create above),
which becomes the control object:

- seq 1: acks client seq 1; events `NetStringEvent` (tag 0 = `MissionStartPhase1`) and `RemoteCommandEvent` (tag 0); ghost section, width 1: creates ghost 0 (`Sun`) and ghost 1 (`GameObject`) (142 bytes):

  ```
  05084002080108000d004ab8b835569a421aeccdd95ebc001880203062007b4107a69e6c9a277e6c9a277e6c9a277e9b99997e9a99997e9a99997e00
  00007f3433337d3433337d6666667d0000007f4600d7411b621d9df74656de642377ba307287fdee4bc7d00400000000000000000000fc0100000000
  000000000000fc01000000003a3072f7ffffff1f0900
  ```

- seq 2: after the client's `MissionStartPhase1Ack`; events: tag 1 = `MissionStartPhase2`, then the command (28 bytes):

  ```
  09104006080908400d084ab8b835569a421aeccdd97eff0260008201
  ```

- seq 3: after `MissionStartPhase2Ack`: the control object section (flag 1, flag 1, `u32` server time, `int12` ghost 1, the 13-bit empty update); no events, no ghosts (13 bytes):

  ```
  0d18400e989300002000000000
  ```

- seq 4: keep-alive data packet (acks only) (6 bytes):

  ```
  1120401e0800
  ```

- seq 5: keep-alive data packet (acks only) (6 bytes):

  ```
  1528403e0800
  ```

## 9. A minimal protocol-24 client, step by step

What a client must do to reach a drawn world against a server that behaves like the Seihai
gserver (and like the real 5.12 expects):

1. Detect the `3 ` name. Open TCP *P* and UDP to *P* + 1 at once.
2. Send `0x1A` with a fresh connect sequence; resend it until `0x1E` comes back.
3. Send `0x20` echoing the digest: `GameConnection`, group 0, CRC `0xFFFFFFFF`, `Graal3D`,
   24, 24, the password, argc 2, account, nickname. Resend until `0x24` (or `0x22`) comes back;
   give up after about 15 s.
4. Read the class table into a server-id → class map; check the protocol is 24.
5. Start numbering data packets at 1. Send one at once (the real client puts its max-rate pair
   in it), then at least one a second, and a ping when nothing has been acked for a few
   seconds; answer every ping with an ack.
6. Read each server data packet in order: header → rate flags → game section → unguaranteed
   events → guaranteed events → ghosts. Use the length prefixes to skip anything unknown.
7. On `MissionStartPhase1` reply `MissionStartPhase1Ack`; on `MissionStartPhase2` light the
   scene and reply `MissionStartPhase2Ack`.
8. Create, update and delete ghosts as the ghost section says. The first control object starts
   the 3D view; from then on put its position (and its changed sections) in every packet you
   send.
9. Keep the TCP session alive; when it ends, send `0x26` and close the UDP side.

## 10. Protocol 19 (3.153, 4.04r2): what differs

Static reads only; the handshake is the one above with 19 and three class types. Nothing past
the handshake has been run. **[bin]**

- **Game layer.** The stock TGE layer: datablocks (`SimDataBlockEvent` with `int12` id − 3,
  class id, index, `int13` total, sized data), `Player` / `ShapeBase` / `Item` / … ghosts, and
  **moves**. Datablock ids are 12 bits (TGE used 10).
- **Server → client game section:** `int32` last move ack; `flag` → { `flag` → damage flash;
  `flag` → white-out }; `flag` control → either `flag` dirty → `u32` server time, `int12`
  control ghost, its packet data, or 3 × `f32` compression point; `flag` camera → `int12`, `flag`
  → camera data; `flag` → `int8` field of view. (`graal3d/torque-engine-4x.md`)
- **Client → server game section:** `flag` first person; 3 × `f32` control-object position,
  `flag` → `int12` its ghost; `flag` "client sends its own state" → the object's packet data,
  **else** `int32` first move index, `int5` move count (≤ 30), the moves; `flag` → `int8` field
  of view.
- **Mission start:** three phases, `MissionStartPhase1` "Download Datablocks & Targets",
  `2` "Download Ghost Objects", `3` "Mission Lighting". In 3.153 these are TorqueScript
  (`main3D.cs` and the mission-download scripts) and the acks carry the phase sequence number
  as a second argument; 4.04r2 handles them natively without it.
- **3.153** runs `main3D.cs`, which creates `ServerConnection` and connects; its join password
  and connect arguments are set by the engine and were not traced.
- Class sets: see `graal3d/torque-engine-4x.md` (4.04r2: 49 object, 34 datablock and 15 event
  classes).

**Protocol 9 (3.04 Linux)** is stock TGE 1.x networking with no Graal changes (no class table,
stock class-id widths, no length prefixes) and ships no 3D scripts. No 3D server for it is known.

## Open

- [x] ~~A full real-client trace through login step 6, decoded packet by packet.~~ Idle session
  done: [lab-2026-11-12-udp-trace.md](lab-2026-11-12-udp-trace.md). All 319 datagrams decode
  with this note.
- [ ] The same with walking and chat (rerun queued).
- [ ] Protocol 19 past the handshake: the per-packet string buffer, the move layout and the
  datablock phase against a real 3.153 or 4.04r2 client.
- [ ] What the 5.12 client sends in sections 5, 9 and 3 of its own update while walking and
  chatting (the 5.x client only moves when a GS2 script moves it; lab 11 is testing that).
- [ ] `TerrainBlock`, `WaterBlock` and the replicators are not sent by any server we have;
  their layouts are unread.
