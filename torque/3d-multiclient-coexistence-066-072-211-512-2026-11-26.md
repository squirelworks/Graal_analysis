# Multi-client 3D coexistence: two 4.04r2, a 19+24+24 mix, and the level-leader fix (T3D-066, T3D-072, T3D-069 follow-up)

Date: 2026-11-26. Lab: real clients in a Linux lab VM (Xvfb, software GL),
loopback, trace on, against seihai-gserver (#209 bbf165d, and #211 61bb575 for the
level-leader re-check). The 3D clients reach the server through user-mode
networking; the 5.12 runs under Wine in that VM, and a Windows 10 VM 5.12 is used
where a real GDI path matters. Behaviour only; no addresses; captures stay in the
lab kit. **[lab]**

Builds on [the stable-2D-client cross-view note](3d-2d3d-crossview-flags-movetype-512-2026-11-26.md)
(T3D-069/133/054) and the earlier M1 two-client reads
([multi-client-3d-lab](multi-client-3d-lab-2026-11-25.md)).

## T3D-066 — two native Linux 4.04r2 [protocol 19]

Two real 4.04r2 clients (`labone`, `labtwo`), both linking as "protocol 19,
3.153, 4.04r2", full stock mission start ("Initial Control Object", "Graal3D has
been activated!"), each given a Player control object (the second spawned at
(2,0,1) on the spawn ring, trace "1 other 3D players").

- **Link: PASS.** Both linked and ran the whole start sequence.
- **Cross-ghosting (server side): PASS.** Each client got the other as a stock
  TGE `Player` ghost (labone: ghosts 2 and 3; labtwo: 1 and 2). While labtwo was
  still only on TCP, labone was shown a `G2DPlayer_labtwo` stand-in, removed
  ("2D player gone") 50 ms after labtwo's 3D link — no duplicate left. On quit:
  "object deleted on 1 other clients".
- **Stability: PASS.** Moves flowed throughout — labone 3711, labtwo 2856 moves
  in ~2 min, steady "N moves received" counts, no drop and no desync; both links
  closed only on quit.
- **Draw state: INCONCLUSIVE.** Each 4.04r2 draws only its sky/fog band — protocol
  19 gets no GameObjects or terrain in this world, so there is no ground. The
  other's octahedron `Player` was not seen on screen even after labtwo walked into
  labone's forward view, and the trace does not log protocol-19 positions, so where
  labtwo ended up can't be confirmed. Settling it needs a world with a
  protocol-19-visible reference (a TGE-ground interior or object) and a fixed
  overhead camera.

So proto-19 multi-client is **server-clean** (ghosting, moves, teardown all
correct); the open part is purely the on-screen confirmation, blocked by the
no-ground / no-position-log limits of proto 19 in this world. This matches and
extends the prior M1 read (relayed cleanly server-side but drew nothing).

## T3D-072 — mixed protocols on one server (19 + 24 + 24)

Three clients on #209 at once: Linux 4.04r2 [19], Linux 4.20r6 (G3D22126, links
as 24), and 5.12 under Wine [24], joined ~25 s apart. **There is no protocol-21
client on this host** — the only proto-21 (Mac 4.20r6 PPC) is on a separate
machine — so the full 19/21/24 mix still needs that host; this run is the
19+24+24 subset.

- **Link: PASS** for all three. labone "protocol 19, 3.153, 4.04r2"; labtwo
  "4.20 Linux client: protocol 24" (linked as "4.20r8, 5.x"); 5.12 (guest → pc:1)
  "5.12 client: protocol 24", reaching Phase 2 / "Mission lighting done" and
  downloading `redcube.3ds`.
- **Seeing each other (server side): PASS.** The two proto-24 clients each got
  Sun, Sky, RED, the other's `G3DPlayer`, and their own Camera; labtwo got
  `G3DPlayer_pc:1` when the 5.12 joined. The proto-19 client got both 24 players
  as stock TGE `Player` ghosts. On quits: "pc:1 object deleted on 2 other
  clients", "labone … deleted on 1 other clients".
- **Sync and stability: PASS.** labone streamed 4693 moves with no gaps; labtwo
  answered pings at 1 ms to the end and its link was still up when the server was
  stopped; no unread-packet, desync or warning lines; the 5.12 sent **0 moves**
  (normal — 5.12 never sends its own 3D movement). Every close was a quit.
- **Screens (partial):** the 4.20r6 draws sky, fog and a red cube steadily; the
  4.04r2 draws only its sky band (as T3D-066); the 5.12-under-Wine run took no
  screenshots (scrot on its Xvfb failed), so its draw state is unchecked (console
  shows mission start finished). Visually confirming each client's view of the
  others needs a world with a protocol-19-visible reference and fixed cameras.

So a 19 + 24 + 24 mix **coexists cleanly on one server** — all three link, the
server ghosts each to the others at the right protocol (24s as `G3DPlayer`, to
the 19 as TGE `Player`), and nothing desyncs or drops. The remaining gaps are the
proto-21 leg (needs the Mac host) and the on-screen cross-view.

## T3D-069 follow-up — the level-leader timeout was a server gap, fixed in #211

The [cross-view note](3d-2d3d-crossview-flags-movetype-512-2026-11-26.md) recorded
a gotcha: with a 5.12 3D player in a GS1 level, the 2.22's level-NPC **timeouts did
not run**, because old Graal runs level timeouts only on the **level leader**,
which there was the 3D player. The gserver author traced this to the server not
telling a 2D player it had become leader; **seihai-gserver #211 (61bb575)** fixes
it — a 2D player in the level now gets `PLO_ISLEADER` when the leader links 3D,
when a 2D player enters a level a 3D player leads, and on any hand-off.

Re-verified on #211 with a real 5.12 (Windows 10 VM) + real 2.22 (Wine) in the
same level; the level NPC is timeout-only (bumps the 2.22 player's chat "tick N"
once a second, so the count rises only if 2.22 timeouts run):

- **(a) 5.12 links 3D first (15 s), 2.22 joins (41 s): PASS** — 2.22 timeouts run
  from the start, tick 3 → 16 → 29 → 42 → 54.
- **(b) 2.22 in the level first (24 s), 5.12 logs in + links 3D (65 s): PASS** —
  tick 3 → 26 → 48 → 71 → 93, counting straight through the 5.12 link with no
  stall at the hand-off.

Behaviourally the 2.22 is treated as level leader in both orders now; before #211,
with the 5.12 in the level, the timeouts never ran. Nothing crashed or dropped,
and the 2.22 also showed the 3D player's chat in both runs. So the T3D-069
"level-leader timeout" line changes from a mixed-level **gotcha** to a server gap
that is **fixed in #211**. **[lab]**

## Summary

| row | verdict |
| --- | --- |
| T3D-066 | two 4.04r2 [19]: link + server-side cross-ghosting + stability all PASS; on-screen draw inconclusive (proto 19 has no ground/position log — needs a visible reference + overhead camera) |
| T3D-072 | 19 + 24 + 24 coexist cleanly on one server (link, protocol-correct ghosting, sync all PASS; 5.12 sends 0 moves = normal); open: the proto-21 leg (Mac host) and on-screen cross-view |
| T3D-069 follow-up | the mixed-level level-NPC-timeout gotcha was a server gap; seihai-gserver #211 sends `PLO_ISLEADER` to a 2D player, and the 2.22's timeouts now run with a 5.12 in the level in both join orders |
