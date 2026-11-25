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

- **(a) Reconnect spawn (T3D-076) — correct, not a bug.** A spawns at
  30,-26,1. B's first join lands at 32,-26,1 (the +2 offset, because A still
  held the base point). B then leaves and reconnects while A is still in, and
  lands at 30,-26,1 — the base point, with no offset. The trace (S1 rerun,
  `g3dtrace.tsv`) shows why this is correct, not a missing offset: by the
  time B reconnected, A's server-side object had walked ~4 units off the base
  (A's last relay before the reconnect reads `at=30,-22,1`), so the base
  point was free and `spawnPosition()` handed it to B. A never drew on top of
  B. The offset is only applied to avoid a point within ~1 unit of a linked
  player's *current* object; a vacated base point is reused. Both TCP sides
  are in `onlinestartlocal.nw`.
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
- **ANSWERED — 4.20r8 draws streamed terrain on Mesa, untextured.** Rerun on
  gserver #154 @ ca00d9a6 with `graal3dterrainall = true`, world `g2t` (a
  real TerrainBlock from `world/t3d_png`, 256 chunks), a 5.12 already in the
  world; 4.20r8 under Wine on Mesa llvmpipe (GL vendor Mesa, renderer
  llvmpipe). The server names 4.20r8 "GameObject layer, terrain streamed
  (graal3dterrainall)" and creates the TerrainBlock ghost on it; the client
  asks with no stamps and receives all 256 chunks ("Loading terrain from
  terrain chunks", "Terrain lit", 255 chunk-received lines). It draws the sky
  then a **white** ground plane to the horizon, with the world cube and the
  5.12 player standing on it. The terrain is white because **4.20r8 never
  asks for `heights.info` or any texture — no downloads at all**, unlike
  5.12. No crash across ~4 minutes including a walk. So the near-terrain
  crash seen before was the GDI GL renderer (spawn z 1 on Mesa does not
  crash); on a real GL driver 4.20r8 accepts streamed terrain and draws it
  untextured.
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
  server waiting to be asked, not a client limit.
- **ANSWERED — Mesa draws the pushed terrain textured on the first visit.**
  Real 5.12 under Wine on Mesa llvmpipe (vendor Mesa, renderer llvmpipe),
  cache cleared first; gserver #154 @ ca00d9a6 with `graal3dpushterrain =
  true`, world `g2t`, one `heights.info` in the folders. The server streams
  the TerrainBlock and all 256 chunks; on the first visit, before ghost
  download starts, the client logs `heights.info` done, then `g3d_water.png`,
  `g3d_sand.png`, `g3d_grass.png` and `g3d_rock.png` done (~60 KB each).
  From ~30 s on, the terrain fills the view to the horizon with the **water**
  texture (the first entry in `heights.info`, as expected for this flat low
  terrain); the cubes stand on it; no white ground and no crash in 150 s. So
  the push fixes the first visit and Mesa draws the textures — the earlier
  white was the GDI/no-push case (white on first visit, textures only on the
  second), not a GLSL-driver limit. T3D-044 first-visit draw is settled.

### M3 (Mac 3.153 on Tiger + 5.12)

- 3.153's six sky `.gif` requests are all answered with the PNGs, and it
  gets past the loading screen to the sky view with no crash. So the
  gserver's PNG-for-GIF answer works for 3.153.
- 3.153 gets the 5.12 player as a TGE `Player`; the 5.12 gets
  `G3DPlayer_<account>`.

### M1 (4.04r2 + 5.12)

- The 4.04r2 script `player` x/y now follows the walk (settling at 0, 15.44),
  matching the server's relay.
- 5.12 draws the 4.04r2 player moving but leaves a dotted orange trail in
  the black band between the sky and the ground.

**M1 (c) clean rerun (gserver #154 @ ca00d9a6, no edits during the run),
`graal3dworld.m1c`, skyoptions 1 1 1:** the trail is a 5.12 frame-clearing
smear, not stale ghosts. The 4.04r2 links as protocol 19 at 2,-6,1; each
side gets exactly **one** ghost create for the other; 305 relay lines carry
the 4.04r2 walk to the 5.12 (ending near 2,13.5); on close the server logs
"left: its object goes from 1 other 3D clients" and sends **one** ghost-out
kill to the 5.12. The trail persists ~40 s after the kill, while the
4.04r2's cube itself is gone — so with exactly one create and one kill it
cannot be stale server ghosts. It sits only in the black horizon band where
nothing draws (the sky faces don't cover that band), i.e. 5.12 is not
clearing that part of the frame — a smear, unchanged since 944a5bb2. A
server-side mitigation (not a client fix) would be a world that covers the
horizon band: a larger ground, or a sky whose lower half is filled.

### S2 (two 4.04r2, protocol 19)

Two Windows 4.04r2 clients under Wine (separate hard-linked prefix copies —
a second Wine client can't share the first's prefix; its window fails to
open on the second display), against gserver #154 @ ca00d9a6 on loopback,
world `m3`. Board rows: T3D-066, T3D-074.

- **Server side — full relay, like the 5.12 pair.** Both link as protocol
  19: the first at 30,-26,1 (0 others), the second at 32,-26,1 (1 other, the
  ring offset). Each gets a **`Player`** ghost for the other. Walks relay
  both ways (314 and 312 relay lines). When the first leaves, the second
  gets one ghost-out kill, then the second leaves cleanly.
- **Client side — nothing drawn.** Both windows draw only the sky gradient
  for the whole session. There is no ground (GameObjects are not sent to
  protocol 19), and neither client draws the other's `Player` in view. No
  crashes.

So on 4.04r2 another player arrives as a stock Torque `Player` ghost
server-side (T3D-066: a `Player`, not a Graal GameObject or AIPlayer) and
the walk relays fine, but the 4.04r2 client renders neither the ground nor
the other player in a bare GameObject-less world — there is nothing on
screen to see them by. Two 4.04r2 players therefore have no visible
interaction in this world (T3D-074) despite the clean server-side relay.
