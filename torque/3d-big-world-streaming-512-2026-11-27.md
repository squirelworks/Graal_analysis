# 5.12 big worlds: whole-world at join, and how an Enigma-scale world can still work (T3D-166)

Date: 2026-11-27. Lab: the real Windows **5.12** client (`G3D14097`, `Graal.exe` SHA-256
`ece87e57…`) under Wine 10 with Mesa llvmpipe in the headless Debian lab VM on GwenTea2, one
private loopback network namespace, one Wine prefix per client, against **seihai-gserver PR #223
head `126f946`** built from a local lab-only branch (`lab/bigworld-1127`, patch described below;
not pushed). Worlds, terrain and shapes were generated for these runs. Derived numbers only;
captures, logs and screenshots stay in the owner-held lab kit. Tags as in `README.md`. **[lab]**

Question from the owner: on a bigger world, does the client take the whole world, or request
updates as it moves through it? And can a world the size of a large 2D playerworld be made to
work in 3D?

## Short answer

- **Terrain: whole world at join, never on demand.** When the `TerrainBlock` is added the
  client sends one `TerrainRequestUpdatesEvent` with all 256 chunk stamps
  ([terrain-512.md](terrain-512.md) §3) and the server answers with every chunk that differs.
  Walking afterwards asks for nothing.
- **Objects: whole world at join, decided by the server.** Our server ghosts every object to
  every client after Mission Phase 2. The client never asks for scoping, but it accepts ghosts
  being created and deleted at any time.
- **Where it breaks:** the 4096-slot ghost table, join time at our server's packet rate, world
  switches that resend all terrain, and lighting that happens only at Phase 2. Memory is not the
  limit.
- **It can work.** One world with a **sliding terrain window** (repeat on, chunks overwritten as
  the player moves, then a Phase 2 relight) plus **distance-scoped objects** (about 1100 units)
  covered a 20 000-object world while walking with no visible pop-in, using under 1500 ghost slots.

(2D playerworlds are the opposite: the client fetches levels on demand, the 3×3 gmap
neighbourhood around the player; see
[../protocol/gmap-adjacent-level-target.md](../protocol/gmap-adjacent-level-target.md).)

## 1. Terrain size sweep

One client, `TerrainBlock` square size 2, 8 and 32 (the grid spans ±256, ±1024, ±4096). Join
time is from 3D link up to the client's Mission Phase 2 acknowledgement.

| Terrain | Cache | Chunks sent | Chunk payload (zlib) | UDP s→c in join | Link → Phase 2 |
|---|---|---|---|---|---|
| hilly, any square size | cold | 256 | ~46 KB | ~51 KB | 8.3–8.6 s |
| flat, any square size | cold | 256 | ~4.3 KB | — | ~1.4 s |
| either | warm (all stamps match) | 0 | 0 | — | ~0.5 s |

- **Square size changes nothing on the wire:** the same 256 chunks, the same bytes and the
  same time at sizes 2, 8 and 32. A "bigger" terrain is the same grid stretched.
- Join time is set by our server's send rate (§4), not by the client.
- Client RSS about 185 MB after join, independent of terrain and object count.

## 2. Walking across the world

Square size 32 hilly terrain; the server stepped the avatar diagonally from (−4000, −4000) to
(+4000, +4000) and past the edge, about once a second for 3 minutes, with repeat 0 and 1.

- **No `TerrainChunkEvent`, no `TerrainRequestUpdatesEvent` and no ghost create or delete** in
  either direction during the walk.
- Traffic was only position updates, about **85 B/s**.
- Client RSS grew about 60 MB over the walk (render-side, not network data); server RSS stayed
  at or under 21 MB.

## 3. Object count

Size-32 terrain, small cubes spread uniformly over ±4000 (plus a run with a few heavier shapes).

| Objects | Result |
|---|---|
| 0 – 4000 | all ghosted after Phase 2 at about **130 ghosts/s**, about **52 bytes per ghost**; 4000 objects took **31 s** and **209 KB** |
| ≥ 4094 | the objects fill the 4096-slot table before the player's own object, its `Camera` and the `TerrainBlock` are ghosted; those are refused and the view is **black for the whole session** |

Nothing was ghosted in or out while walking (no scoping exists in the server; run 5).

Three clients on the size-32 world with 2000 objects: about **155 KB per client to join**, then
**110–137 B/s per client** while walking.

## 4. Join time is our server's send rate

The server sends one ~400-byte packet every 50 ms, about 8 KB/s. With the lab patch's 10 ms
interval the client kept up with no loss:

| Content | 50 ms (shipping) | 10 ms (lab) |
|---|---|---|
| hilly terrain, cold | 8.3–8.6 s | 2.05 s |
| 4000 objects | 31 s | 8.7 s |

## 5. World switches and lighting

- **The terrain cache is per server name, not per world** ([terrain-512.md](terrain-512.md) §4).
  Switching between two worlds with different terrain resends **all 256 chunks every time**
  (45–51 KB, about 7 s), three switches out of three.
- **5.12 lights terrain only at Mission Phase 2**
  ([terrain-512.md](terrain-512.md), T3D-162). Neither a world switch nor a chunk received
  mid-session is relit until the server sends Phase 2 again.

## 6. Prototypes for a large world

Lab patch (local only): distance scoping of GameObjects with a radius and hysteresis;
mid-session `TerrainChunkEvent`s for a sliding window; an extra MissionStartPhase2 after a window
update; a configurable packet interval. Described here as behaviour; not proposed as-is.

### A. Distance-scoped objects

20 164 objects; ghost an object when it comes within R of the player, delete it past R + 200.

| R | Peak ghost slots | Join | While walking |
|---|---|---|---|
| 1100 | 1417 | 3–5 s | ~40 creates + ~40 deletes per second, ~2.5 KB/s |
| 1500 | 2533 | 3–5 s | similar |

- Creates landed within 0.5 s of entering the radius; **nothing popped in visibly**, because the
  client's own draw horizon is about 1000 units
  ([3d-scoping-interiors-limits-512-2026-11-26.md](3d-scoping-interiors-limits-512-2026-11-26.md)).
- R = 1100 drew exactly the same objects as R = 1500, so 1100 is enough at the default
  `visibledistance3D`. A world that raises that preference (max 2400) needs a larger R.

### B. Sliding terrain window

Repeat on, square size 8 (window 2048 units) and 4 (1024). The server maps world chunk (X, Y)
onto grid chunk (X mod 16, Y mod 16) and, as the player crosses a chunk boundary, overwrites the
chunks now entering range.

- **5.12 applies and redraws mid-session chunks straight away, with no stall and no seams**
  between new and old chunks; with repeat on the wrapped grid appears correctly around the player.
- Cost: **31 chunks (about 3.8 KB) per diagonal chunk crossing**, about **0.85 KB/s** while walking.
- New chunks keep the old lighting until the server sends **MissionStartPhase2 again**; that
  relit them in about 0.04 s, **pixel-identical** to a static control world.
- Square size 8 is the useful setting: its 2048-unit window keeps the swapped edge about
  1000 units away, outside the draw horizon. Size 4 halves the margin.

### C. Linked regions

The map split into separate `graal3dworlds`, switched at a boundary with a matching spawn. Each
crossing resends all 256 chunks (about 37 KB, 6.2 s), shows about **6 s of stale cached terrain**
and keeps the old lighting. **Good only for places reached by a warp** (houses, caves, dungeons),
not for a seamless overworld.

## For a server: an Enigma-scale 3D world

Viable combination, all measured above:

1. **One world**, terrain at square size 8, **sliding window** with repeat on, chunks swapped as
   the player moves, and a **Phase 2 relight** after each swap.
2. **Objects scoped at about 1100 units** with ~200 hysteresis (raise with `visibledistance3D`).
   This keeps a 20 000-object world at about 1400 ghost slots.
3. **Ghost order:** always ghost the player, its `Camera` and the `TerrainBlock` first, and keep
   their slots reserved, so no world can black out the view.
4. **Faster send rate** than one packet per 50 ms; 10 ms worked with no loss.
5. **Linked worlds** only for warped interiors; expect a full terrain resend per switch until the
   cache key includes the world.

Open: per-chunk relight cost on a slower client; behaviour on a real WAN; many clients walking
at once with scoping on; whether the extra Phase 2 has side effects in client scripts
(not checked in these runs).
