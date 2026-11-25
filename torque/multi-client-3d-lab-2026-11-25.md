# Multiple clients in one 3D world: first lab pairs (2026-11-25)

Lab: real clients in separate VMs against our own gserver, one pair at a
time, with per-VM packet captures, a step log and screenshots. Behaviour
only; the captures stay in the lab share. Board rows: T3D-065, T3D-068,
T3D-070, T3D-073, T3D-076, T3D-110, T3D-115, T3D-116. **[lab][cap]**

These are first runs on an early build. The gserver 3D thread is still
changing how other players are relayed, so read these as the state on
2026-11-25, not as settled behaviour.

## H1: a 2D client and a 3D client in one level

5.24r3 as a 2D client and 5.12 as a 3D client, both on our gserver.

- The 2D client's `players` count is 2, so it knows the 3D player is there,
  but that entry is empty and never draws. The 3D player's walk never
  reaches the 2D side.
- The 3D client never sees the 2D player at all (`players` is 0, no ghost).
- 2D chat does reach the 3D client, as `onRemotePlayerChats`, over TCP, at
  join and again at rejoin. 3D chat and flags never reach the 2D client.
- Neither side gets a leave event.

So on this build a 2D and a 3D client can sit in the same level and exchange
chat one way (2D to 3D), but neither draws the other, and nothing cleans up
on leave.

## S1: two 3D clients in one world

Two 5.12 clients on the PR #154 build with the trace on.

- On join, the server creates a `G3DPlayer_<other>` object on both clients
  within the same second.
- The relay carries chat but not `g3dpos` moves, so each trace keeps the
  other player at the spawn position.
- Both players spawn on the same point. Client B saw A's cube stacked on its
  own during A's actions; A never visibly showed B.
- `players` stays 0 and no per-player events fire.
- On leave, no ghost delete is logged; on reconnect, the ghost is created
  again under the same index.

So two 3D players are created on each other's clients, but with the same
spawn point, no position relay and no delete on leave, another player is
close to invisible. These are the next things for the gserver to fix.

## What this answers

- **2D and 3D together (T3D-115, T3D-116):** yes, they share a level and 2D
  chat crosses to 3D, but no player is drawn across the 2D/3D line and no
  flags cross.
- **Other 3D players (T3D-065, T3D-070):** created as `G3DPlayer_<account>`
  GameObjects, relayed with chat; movement and leave are not yet relayed.
- **Leave and reconnect (T3D-076):** no delete is sent on leave; the ghost
  returns on reconnect.

## Re-run on the fixed gserver (PR #154 at 944a5bb2)

After the gserver fixes, the same pairs were re-run with the trace on.

### S1 (two 5.12), confirmed

- Spawns are now 2 units apart (on a first visit).
- `g3dpos` moves relay and stick; a "tcp position" line appears for each
  step.
- Both clients draw the other player's cube moving through the walk.
- On leave the trace shows "left: its object goes from 1 other 3D clients"
  and the other client drops the cube.
- A client still logging in briefly shows as a `G2DPlayer`.
- **Still off:** on reconnect, B spawned on A's point (first-visit spawns
  are correct).

### H1 (5.24r3 2D + 5.12 3D)

- The 3D client now shows the 2D player as `G2DPlayer`: shown, moved, with
  its chat, and gone on leave. The 3D walk reaches the TCP side as tcp
  positions.
- **Still open on the 2D side:** its `players` list never contains the 3D
  player (count is 2, but only itself is listed), and it draws no sprite
  because this world has no head or body images. Whether 3D chat shows on
  the 2D client is not settled (its console was overwritten on reconnect).

### gserver PR #154 at ca00d9a6 — checks (a), (b), (d)

Clients: 5.12 (3D) plus 5.12 / 5.24r3 (2D), each in its own lab Windows 10
VM clone; server on loopback.

- **(a) Reconnect spawn (T3D-076).** A spawns at 30,-26,1. B's first join
  lands at 32,-26,1 (the +2 offset). B then leaves and reconnects while A is
  still in, and lands at 30,-26,1 — on A's point, *without* the +2 offset.
  So the spawn offset is applied on a first join but not on a reconnect.
  Whether a reconnect should also get the offset is a gserver design call
  (left to the gserver thread), not a client fact.
- **(b) 2D sees a 3D player (T3D-115, T3D-073) — PASS.** With stock
  head/body/sword/shield ganis in the world, the 5.24r3 2D client gets the
  3D player's full look in one players-props packet, then position updates
  as the 3D player walks, plus its chat ("hello from 3D"). B's 2D screen
  shows two complete player sprites from the first join shot on, and the 3D
  one moves. (Before the fix the 3D player was invisible on the 2D screen.)
  **One gap:** the 2D client's own GS2 `players` list still counts only
  itself — the 3D player shows as a sprite but is absent from the scripted
  list.
- **(d) Shadowed heights.info (T3D-044) — PASS.** With a second
  `heights.info` left in another world folder, the server logs an error at
  start-up that names the file clients will receive and says to remove or
  rename the other. With a single `heights.info`: visit 1 streams
  `heights.info` and all 256 terrain chunks; visit 2 streams 0 chunks (the
  cache is current). The ground still draws **white** on the GDI GL
  renderer, so whether the terrain draws textured is a renderer question —
  the Mesa draw check is still pending (item 4 of the queue).

### Return visit to a 1-object world

Two visits, no stall in phase 1, the world drew both times. The
MissionStartPhase1Ack fix holds.

### 4.20r8 terrain (T3D-117)

4.20r8 under Wine on Mesa llvmpipe, with a 5.12, on a TerrainBlock world:

- The server marks 4.20r8 "terrain none" and sends it no TerrainBlock.
- 4.20r8 runs with no crash and draws the ground and three cubes, including
  the 5.12 player. So the earlier 4.20r8 crash was the VM's basic Windows
  OpenGL, not the client: on a real GL driver it runs. **Caveat:** in this
  run the server sent 4.20r8 no TerrainBlock ("terrain none"), so this shows
  only that 4.20r8 starts and draws on Mesa, not that it draws *streamed
  terrain*. A Mesa run that does send 4.20r8 a TerrainBlock is still needed
  to answer T3D-117.
- 5.12 draws the streamed terrain white on this run. The terrain thread then
  found the cause: a first visit (empty cache) fetches only `heights.info`
  and draws white; 5.12 fetches the textures only on the next visit. Clearing
  `levels3d/heights` before each run keeps it on a perpetual first visit,
  which is why it looked like it never fetched textures.
- **Push on first visit (GDI run, server pushes once per account).** With
  the server pushing the terrain file set up front (rather than waiting for
  the client to ask on a second visit), a real 5.12 under GDI gets
  `heights.info` *and* all four terrain textures on the first visit, before
  the terrain loads, and logs no "Missing terrain texture". So the textures
  are available to the client on the first visit when the server pushes them
  — the earlier "textures only on the second visit" was a consequence of the
  server waiting to be asked, not a client limit. **Still open:** whether
  5.12 *draws* those first-visit textures (vs. still drawing white) on a GLSL
  driver — the GDI run confirms arrival, not the rendered result. A Mesa run
  with the cache cleared and the server pushing is needed to settle the draw.

### M3 (Mac 3.153 on Tiger + 5.12)

- 3.153's six sky `.gif` requests are all answered with the PNGs, and it
  gets past the loading screen to the sky view with no crash. So the
  gserver's PNG-for-GIF answer works for 3.153.
- 3.153 gets the 5.12 player as a TGE `Player`; the 5.12 gets
  `G3DPlayer_<account>`.

### M1 (4.04r2 + 5.12)

- The 4.04r2 script `player` x/y now follows the walk (settling at 0, 15.44),
  matching the server's relay.
- 5.12 draws the 4.04r2 player moving but leaves a trail of copies in the
  band between the sky and the ground. A redraw or ghost-clear gap, still
  open.
