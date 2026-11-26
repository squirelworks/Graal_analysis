# 3D at scale and under edits: ghost capacity, asset lifecycle, and the world-file parser (T3D-147/154/155)

Date: 2026-11-26. Lab: a real 5.12 in a Windows 10 VM (3D mode) against seihai-gserver main
(5cd9c15) on the loopback, with the T3D-164 synthetic client used to read the ghost section
where helpful. Behaviour only; lab tooling and captures stay in the lab kit, off every PR.
**[lab]**

Three rows on how the server and a real client behave at scale and when the world changes
under them.

## T3D-147 — ghost capacity: no cap to 4000, the limit is delivery time and its order

A world with N GameObjects in a grid ahead of the spawn, a fresh real 5.12 per step, at
N = 50, 100, 200, 500, 1000, 2000, 4000 (plus Sun, Sky, the avatar and Camera):

- **No cap and no failure up to 4000.** The 5.12 took every create (e.g. 4005/4005 at
  N = 4000), drew the whole grid, stayed up with no console errors, and lost nothing. The
  server ghosted the whole set with no cap, warning or "create lost".
- **The limit is delivery time.** The server sends about 7 creates per packet at ~20 packets/s
  (~140 creates/s), so the time to a full world is ≈ N/140 s: the player's Camera and control
  object arrive at server packet ~9 (~0.5 s) at N = 50 but not until packet ~572 (~28.6 s) at
  N = 4000.
- **The ghost index width grows past 16 ghosts, and the 5.12 handles it.** The per-packet
  4-bit field carries the index *width in bits*, which rose from 6 bits at 55 ghosts to 12 bits
  at 4005; the client took every width with no trouble (confirming the open question in
  [T3D-159](3d-replica-wire-157-160-165-512-2026-11-26.md)).
- Server load stayed small: lifetime-average CPU peaked at 1.7 % and RSS at 21 MB (7 MB at
  N = 50).

**Ordering gap.** The joining client's own Camera and control object are ghosted **last**,
after every world object. A 5.12 draws nothing until it has its Camera, so on a big world the
player stares at a **black screen for the whole delivery** — ~7 s at 1000 objects, ~14 s at
2000, ~28 s at 4000 — before anything appears (at N = 4000 the screen is black at +30 s, fully
drawn by +71 s). Ghosting the joining client's Camera and own avatar/control object **first**,
then the world (nearest-first if feasible), would bring the view up at once and let it fill in.

## T3D-155 — asset lifecycle: 3D assets are pull-only, stale until relink

A world with sky textures, a `redcube.3ds` object and streamed terrain. Once the 5.12 had
fetched and was drawing them, the server's files were changed in place mid-session (sky PNGs
recoloured, the `.3ds` given a new material, terrain chunks near the spawn reshaped), with no
relink:

- **No new file or terrain request after the change** — not even after a scripted world switch
  (cave and back) that re-ghosted the default world's Sky, cube and TerrainBlock. The 5.12 kept
  its stale copies and its screen was unchanged across the swap and the round trip.
- **The server pushed nothing** on the change: no invalidation, no re-send, no log line. Assets
  are pull-only.
- On a **fresh relink**, the client's freshness checks pick up every change: all textures and
  the shape are re-sent, and the terrain request re-sends **exactly the changed chunks** via its
  stamp comparison.

So the 5.12 only asks for a file when it first needs it in a session; a world switch re-ghosts
objects but does not re-check files it already holds. **For live editing to propagate without a
relink (g3dedit, gserver PR #217), the server must push it** — re-send the changed file over
TCP and re-ghost the objects, or send terrain chunk events for terrain (that path exists).
Relying on the client to re-ask will not work.

## T3D-154 — the world-file parser: defensive, with two authoring sharp edges

Malformed `graal3dworld.txt` entries, one class per run:

- **The parser is line-based and defensive.** Each bad line is logged
  (`graal3dworld.txt line N: <line> (not understood)`) and skipped, the server starts, and the
  rest of the world is served — no crash on any malformation (too-few or non-numeric
  coordinates, bare/truncated/unknown keywords, bad `spawn`/`sky`/`movetype`/`terrain`/`water`
  lines, `replicator` with an unknown class or a huge radius, an empty `objectfor` account
  list, or a binary-garbage line).
- **The world-file parser refuses non-finite and out-of-range coordinates** (`1e40`, `nan`,
  `inf`) — the *opposite* of the client game-section path in
  [T3D-146](3d-robustness-142-146-512-2026-11-26.md), which accepts them. That contrast
  reinforces that the sanitising fix belongs on the game-section side too.

Three malformations the parser accepts, and the client's response:

- **Missing shape** (`object M1 nosuchshape.3ds …`): the server warns at start-up, still ghosts
  M1, and answers the file request "not sent"; the 5.12 logs "File download: … not found",
  draws nothing for M1, and keeps going. The rest of the world draws and the link holds.
- **Duplicate object name** (`object RED` twice): accepted silently and ghosted as two
  GameObjects both named RED, and the 5.12 draws both. Fine visually, but ambiguous for any
  script that looks objects up by name — an optional start-up warning would help authors.
- **weapon3d with a missing script file**: the server logs "cannot read … (os error 2)" at
  link time and sends no weapon; the client is unaffected.

### A rollback corollary (mtime-based freshness)

Because the client's cache freshness is decided by **file mtime**, rolling a server asset
*back* to an older file never reaches a client holding a newer cached copy: the server answers
"file: not sent" and the stale copy wins until the cache is cleared. (Seen directly: a client
still carrying T3D-155's recoloured cache kept it while the server served the original,
older-dated files again.) For g3dedit and especially rollbacks, the server should compare
content (CRC/hash) or bump the modified time it reports whenever a file is replaced, rather
than trust file mtimes.

## Verdict

At scale and under edits the gserver and a real 5.12 are robust and predictable. There is no
ghost cap short of 4000, the index width widens cleanly past 16, and the world-file parser
rejects every malformation without crashing. The behaviours that matter for the live-editing
work are three, all with local fixes: the joining client's Camera/control object are delivered
**last**, so a big world shows a long black screen before the view appears (T3D-147); 3D assets
are **pull-only** and stale until relink, so live edits must be server-pushed (T3D-155); and
cache freshness is **mtime-based**, so rollbacks don't propagate and duplicate object names are
accepted silently (T3D-154). All three are flagged to the gserver work.

## Summary

| row | verdict |
| --- | --- |
| T3D-147 | No ghost cap or failure up to 4000 GameObjects on a real 5.12; the limit is delivery time (~7 creates/packet, ~140/s, full world ≈ N/140 s); the 4-bit ghost-index field carries the index width in bits and widens 6→12 bits past 4005 with no trouble; server load negligible (CPU ≤1.7 %, RSS 21 MB). Gap: the joining client's Camera + control object are ghosted last, so a big world shows a black screen for the whole delivery (~28 s at 4000) — fix by ghosting the client's own Camera/avatar first. **[lab]** |
| T3D-155 | 3D assets (textures, shapes, terrain) are pull-only: a change made in place mid-session triggers no client refetch, even across a world switch, and the server pushes no invalidation — the stale copy is kept until the next relink, at which point freshness checks re-fetch changed files and the terrain request re-sends only the changed chunks. Live editing must be server-pushed (re-send + re-ghost, or terrain chunk events). **[lab]** |
| T3D-154 | The `graal3dworld.txt` parser is line-based and defensive — each bad line is logged "(not understood)" and skipped, the rest of the world served, no crash on any malformation, and non-finite/out-of-range coords are refused (unlike the T3D-146 game-section path); a missing shape still ghosts but draws nothing, a missing weapon script is skipped, and a duplicate object name is accepted silently (both drawn — ambiguous for name lookup). Corollary: cache freshness is mtime-based, so an asset rolled back to an older file never reaches a client holding a newer cached copy — compare content or bump the reported mtime on replace. **[lab]** |
