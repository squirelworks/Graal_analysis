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
