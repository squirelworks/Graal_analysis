# Lab 2026-11-12: a real 5.12 client's Torque UDP session, decoded

Date: 2026-11-12. Tags as in `README.md`; everything here is **[lab]** unless marked.

The first full trace of the Torque side of a real Graal 5.12 session. It is decoded packet by
packet against [udp-session.md](udp-session.md). All 319 UDP datagrams decode with that note's
layouts. No event's length disagrees with its payload, and every packet ends with fewer than
8 padding bits.

## Setup

- **Client:** the real Graal 5.12 (packed launcher plus `Graal3DEngine.dll`) in the Windows 10
  lab VM. A local lobby on a second loopback address answered its gen-5 login with a server warp
  to `3 Lab 3D` on the loopback address, TCP 14830.
- **Server:** `seihai-gserver-v2` at `ea8fb69` (the Windows CI build, PR #54 line),
  `graal3d = true`, UDP 14831.
  - **World:** a `Ground` and a `Cube` (`.3ds`), Sun, Sky (six textures as a comma list), a per-client `Camera`.
  - **Weapon:** a `-Move3D` weapon sent as GS2 bytecode.
- **Capture:** the UDP payloads were taken inside the client process, at the socket send and
  receive calls, with millisecond times. The payload bytes are exact.
  - TCP was logged only as lengths and the ids of the decoded incoming packets.
  - There is no pcap.
  - The account password in the connect request was masked before the dump left the lab machine.
- **What was done:** login, idle in the 3D view for about 90 s, then the client was closed.
  - The planned walk and chat did not reach the game. A dialog had the keyboard focus.
  - This is an idle session. A rerun with walking and chat is queued.
- **Files:** the decoded results and the hex dump of every datagram are kept with the owner's
  lab material (lab 12), not in this repo.

## Timeline

Times are seconds from the challenge request.

| t | Dir | Bytes | What |
|---|---|---|---|
| 0.000 | C→S | 5 | `0x1A` challenge request, connect sequence 0 |
| 0.076 | S→C | 21 | `0x1E` challenge response |
| 0.076 | C→S | 76 | `0x20` connect request: `GameConnection`, group 0, CRC `0xFFFFFFFF`, `Graal3D`, 24/24, password (masked), argc 2: `guest`, then the nickname; 0 bits left |
| 0.076 | TCP | | the client opens the game TCP connection in the same millisecond |
| 0.34–0.79 | TCP S→C | | the server's login burst |
| 0.883 | S→C | 276 | `0x24` accept: 10 object and 9 event classes, protocol 24 (the table in `udp-session.md` §3, sequence 0) |
| 1.111 | C→S | 19 | data seq 1: max rate 32 ms / 450 bytes; first person, position 0 |
| 1.216 | S→C | 385 | data seq 1: `MissionStartPhase1` (tag 0), `addweapon -Move3D`, the start of `weaponscript -Move3D` (1544 bytes, mode 0); ghosts: width 3, creates 0 `Ground` and 1 `Cube` |
| 1.216 | C→S | 5 | **ack** packet (type 2) for server seq 1 |
| 1.350 | C→S | 69 | data seq 2: `MissionStartPhase1Ack` as a **plain string**, then an `events` text `w -Move3D` |
| 1.350 | S→C | 378, 332 | seq 2 and 3: script chunks; ghosts 2 `Sun`, 3 `Sky`, 4 `G3DPlayer_<account>` (shape, transform, nickname, flags 0x10), 5 `G3DCamera_<account>` |
| 1.56–2.61 | S→C | 206 ×3, 205, 249 | seq 4 to 8: the rest of the script; the camera section names ghost 5 from seq 4 on; seq 8 ends with `MissionStartPhase2` (tag 1) |
| 2.768 | C→S | 69 | data seq 3: `MissionStartPhase2Ack` (plain string), `events` `w -Move3D` |
| 3.370 | S→C | 138 | data seq 9: **control object** (server time, ghost 4, empty update), camera 5; the `Sky` (ghost 3) whole again |
| 3.642 | C→S | 60 | data seq 4: position (0, −6, 1), ghost 4, and the client's **own update** for it: shape `labcube.3ds`, transform position (0, −6, 1) with axis (1, 0, 0) and angle 0, flags 0x10 |
| 4.478 | | | client console: "Connecting to the game server..." |
| 4.9 → end | | | steady state (below) |
| 92.9 | | | the lab runner closed the client's windows; a dialog kept it running |
| 108.566 | C→S | 53 | the last datagram |
| 121.6 | | | client process killed; **no `0x26` disconnect** was sent |

## What the trace settles

- **Commands from the client are plain strings, in the guaranteed list.** Both mission acks
  went as `RemoteCommandEvent` argument code 1 (a `pstring`), not as tags. Every client event in
  the session was guaranteed-ordered. No unguaranteed event appeared in either direction.
- **The prefix flag is on every string, both ways.** All strings decode with the per-packet
  `pstring` flag. All flags seen were 0.
- **The client acks every server data packet at once with an ack packet** (type 2, 5 bytes,
  one mask byte). 124 of the client's 191 data-link packets were such acks. No pings were sent
  in this run: the server's packets kept arriving.
- **Data-packet rate when idle:** the client sent a data packet every 1.7 s on average (0.5 to
  3.5 s). The server sent one about every 0.9 s.
- **Only the client's first data packet changes the rate** (the max-rate pair 32 ms / 450
  bytes). The server never sent a rate field.
- **Padding bits are not always zero.** The client's first data packet ends in `a0`: its last
  three bits are padding and two of them are set. A reader must stop at the last field, not
  check the padding.
- **Connect sequence 0 is valid.** This run used 0, the 2026-10-30 run `0x400`.
- **The control-object echo.** In the first packet after it took the control object, the client
  sent that object's update with sections 3 (shape), 5 (transform) and 13 (flags). The
  transform's rotation came back as axis (1, 0, 0), angle 0, although the server had sent axis
  (0, 0, 1), angle 0. The client seems to normalise a zero rotation to that axis **[inf]**. Every later packet
  carried the 13-bit empty update and the position (0, −6, 1).
- **Steady client packets** are 53 bytes (game section plus a two-event `events` text
  `w -Move3D`) or 21 bytes (game section only), alternating. Only the header, the event
  sequence numbers and the BigData transfer id change. The client sent `w -Move3D` 47 times, about
  every 2.3 s, for the whole session. It looks like the weapon's own script asks for itself
  again **[inf]**. A server must treat a repeated `w` for a weapon the player has as harmless.
- **Steady server packets** are 6 or 7 bytes: the control flag A without B, the camera
  (ghost 5), no field of view, no events, no ghosts.
- **Ghost index width.** Width 3 for ghosts 0 to 5, width 2 for a packet whose highest index was
  3. It is the bit count of the highest index *in that packet*, as `udp-session.md` §8 says.
- **TCP during play.** The client sent nothing on TCP after 1.35 s. The server's TCP packets
  kept arriving every few seconds.
- **Disconnect.** When the client is killed, nothing is sent on UDP. The server notices the TCP
  close and drops the 3D link with it.

## Not covered

- Walking and chat (the queued rerun): what sections 5 and 9 of the client's own update look
  like while it moves and talks.
- The 4.04r2 and 3.x clients (protocol 19 and 9): skipped this run.
- TCP payload bytes.
