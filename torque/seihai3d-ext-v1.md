# The `seihai3d` extension, version 1: an opt-in layer on the protocol-24 3D link

Date: 2026-11-27. Status: **design, wire contract implemented and unit-tested** in seihai-core
`protocol::three_d_ext` (`EXT_VERSION = 1`). No server or client speaks it on the wire yet. Our own
protocol, not a finding about any Graal build. Plan and roadmap:
[3d-next-client-server-plan-2026-11-27.md](3d-next-client-server-plan-2026-11-27.md).

## Why it is opt-in

A real 4.20r8, 5.00r7 or 5.12 client cannot be taught anything: an unknown ghost class drops its
link ([T3D-099](3d-capability-board.tsv), [recovery note](3d-recovery-420r6-2026-11-25.md)) and its
limits are fixed in its engine DLL. So a server must never send a real client anything new, and the
only safe signal is one a real client never sends. A real 5.12's connect request carries exactly
two arguments, the account and the nickname ([udp-session.md](udp-session.md) §3 **[cap]**).

## Handshake

1. **Hello (client → server).** Our client sends the stock connect request (`GameConnection`,
   `Graal3D`, protocol 24 and 24, the password) with a **third argument**:

   ```
   seihai3d/<version>/<caps>
   ```

   `<version>` in decimal (1 to 65535), `<caps>` as up to eight hex digits (written as eight).
   Fields after the caps, `/…`, are reserved for later versions and skipped by a v1 reader. Only
   argument 3 and later are read, so an account or nickname that looks like a hello is not one.
2. **Reply (server → client).** A server that speaks the extension queues one guaranteed
   `RemoteCommandEvent`, command `seihai3d`, arguments `<version>` and `<caps>`, **before**
   `MissionStartPhase1`. The version is the lower of the two sides'; the caps are the client's,
   the server's, and those that version defines, intersected. An empty caps reply is valid: it says
   the server speaks the extension with nothing enabled.
3. **Class table.** A class an agreed bit needs is appended to the connect accept's class table
   after the stock classes, so the stock ids never move. v1 adds none: every v1 bit rides on
   `RemoteCommandEvent`s or changes a field width after the reply.
4. **Fallback.** Guaranteed events arrive in order, so our client that sees `MissionStartPhase1`
   without the reply is on a server without the extension and runs as a plain 5.12 with no caps.
   A reply after that is ignored. A server that sees no hello, or one it cannot read, serves the
   stock protocol and sends nothing of the extension. A bit the server claims and the client did
   not ask for is dropped by the client.

Nothing else changes: the TCP login token stays the host build's (our client keeps a stock token,
so any server lets it in), the Torque protocol stays 24, and the server keeps choosing the client's
capability row by token and protocol.

## Capability bits (v1)

| Bit | Name | Meaning once agreed | Replaces, for our client |
|---|---|---|---|
| 0 | `frame_stats` | Client sends `seihai3dStats <fps> <frame ms p95> <ghosts> <draw ms>` about every 5 s | Lab-only frame-rate shims |
| 1 | `chat_3d` | Server sends `seihai3dChat <account> <text>`; client shows a chat line and bubbles in the 3D view | No chat in the 5.12 3D view |
| 2 | `world_terrain_cache` | Server sends `seihai3dWorld <name>` before a world's terrain; the client keys its chunk cache by server and world, and its `TerrainRequestUpdatesEvent` stamps then let the server send only differing chunks | Full 256-chunk resend per world switch |
| 3 | `chunk_relight` | Client relights each terrain chunk as it arrives | The extra `MissionStartPhase2` after a sliding-window swap |
| 4 | `view_distance` | Client sends `seihai3dView <units>` (may exceed 2400); server sizes its object scope radius from it | Fixed ~1100 radius |
| 5 | `fast_pacing` | Client keeps up with one server packet per 10 ms | 50 ms pacing |
| 6 | `wide_ghosts` | Ghost indices are 14 bits (16 384 slots) from the first data packet after the reply | 4096-slot table |
| 7 | `world_chunks` | Terrain chunk events carry world chunk coordinates (signed 16-bit) instead of grid 0 to 15 | One wrapped 16 by 16 grid |

Bits 0 to 5 are stage 2 of the roadmap; 6 and 7 are stage 3 and change field widths, so they get
their own conformance cases before a server enables them.

## Rules for later versions

- A released bit's meaning never changes. A new capability is a new bit and a version bump
  (`Caps::known(version)` lists which bits a version defines).
- Unknown bits and newer versions are ignored, not refused, so a newer client links to an older
  server at the older version and the other way round.
- Each server-side bit has a server switch, and the whole extension one (`graal3d_ext`), so an
  operator can serve everyone the stock protocol.

## Checks before a server enables it

- A real 5.12 (and 4.20r8) against an extension-enabled server: same session as against the same
  server with the extension off (conformance case, capture compare).
- Our client against a server without the extension: falls back at `MissionStartPhase1`, draws as
  before.
- Open **[inf]**: whether a third-party protocol-24 server accepts the third argument. Our client
  keeps an option to send no hello.
