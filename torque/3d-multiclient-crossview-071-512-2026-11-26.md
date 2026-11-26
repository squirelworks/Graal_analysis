# What one build draws of a player on another build (T3D-071)

Date: 2026-11-26. Lab: real clients under Wine/Mesa in a Linux VM, loopback, against
seihai-gserver main (5cd9c15). Two mixed pairs, each in one world, with an overhead
camera; each client's screen and log recorded. Behaviour only; captures stay in the
lab kit. **[lab]**

This answers the on-screen half of T3D-071 — what a client of one build renders and
logs for a player on another build. It extends [the multi-client coexistence note](3d-multiclient-coexistence-066-072-211-512-2026-11-26.md)
(T3D-066/072, which established that the mixes stay server-clean) with the client-side
draw result.

## Pair 1 — 4.20r6 [proto 24] + 5.12 [proto 24]

Linux 4.20r6 (links as protocol 24) and 5.12 in one world. Both linked, both stayed up
until quit, no drop.

- **Cross-draw: both ways, as the world playershape (a cube).** Once the second client
  links, each screen gains the other player's cube beside its own (the other's
  `G3DPlayer_<acct>`, a GameObject carrying the world playershape). No octahedron and no
  unknown shape — both are protocol 24, so each is ghosted the other as a GameObject.
- **No ghost or class errors** on either client; neither console has a ghost/class/
  unknown-object line, only the normal mission start. The server logs none either.
- The brief 2D stand-ins come and go on the server's schedule with no client errors:
  while the second client was TCP-only, the first got a `G2DPlayer_<acct>` stand-in,
  replaced by `G3DPlayer_<acct>` ~3 s later when it linked; on quit the other briefly
  got a `G2DPlayer_<acct>` at the spawn, gone a fraction of a second later.

## Pair 2 — 4.04r2 [proto 19] + 5.12 [proto 24]

Linux 4.04r2 (protocol 19) and 5.12 in one world. Both linked, no drop; the 4.04r2 sent
thousands of moves over the run.

- **The 5.12 draws the proto-19 player.** Once the 4.04r2 links, the 5.12 gains a second
  cube beside its own — the 19-player's `G3DPlayer_<acct>` as a GameObject with the world
  playershape, exactly as in pair 1. So a proto-24 client renders a proto-19 player with
  no special handling.
- **The 4.04r2's view of the proto-24 player is unobservable on screen.** The server gave
  the 4.04r2 a stock TGE `Player` for the 5.12 (and its own `Player`), and it fetched
  `octahedron.dts` — but the 4.04r2 screen only ever shows the Sky band (the same blind
  spot as T3D-066: protocol 19 has no ground and no visible reference), so the octahedron
  is never in frame and "not drawn" can't be told apart from "out of view". The one odd
  log line is `Could not locate texture: green` — the octahedron's bare material name,
  which the server doesn't carry (the same miss as the 3.153 player-shape probe).
- **No ghost or class errors** on either client.

## Verdict

The cross-view is **asymmetric only in observability, not in correctness**. A proto-24
client (4.20r6 or 5.12) draws a player of either protocol as its GameObject cube with no
errors. A proto-19 client (4.04r2) is server-side given a stock TGE Player for the other
and fetches its shape, but has no on-screen reference to confirm the draw, so its render
of a proto-24 player stays unconfirmed (as in T3D-066). Every pairing links, stays in
sync and raises no ghost/class error; the transient `G2DPlayer`→`G3DPlayer` stand-ins
are normal and client-clean. For a replica: a proto-24 client must ghost any other
player — whatever its protocol — as a GameObject playershape; nothing build-specific is
needed to render a cross-protocol player.

## Summary

| row | verdict |
| --- | --- |
| T3D-071 | 4.20r6[24]+5.12 and 4.04r2[19]+5.12 each link with no drop and no ghost/class errors; a proto-24 client draws the other player (either protocol) as its GameObject playershape cube; the proto-19 client is given a stock TGE Player + fetches octahedron.dts but has no ground reference so its draw of a proto-24 player is unobservable (T3D-066 blind spot), with only a `Could not locate texture: green` miss; cross-view is asymmetric in observability, not correctness |
