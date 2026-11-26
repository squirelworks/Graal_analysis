# Level warp, per-player objects and replicator first-visit on seihai-gserver #208/#209 (T3D-135, T3D-136, T3D-048)

Date: 2026-11-26. Lab: real 5.12 in a Windows 10 VM, loopback, trace on, against
seihai-gserver PR #208 (ab3cc6d) and PR #209 (da3c1cd → c7ee7e9). These three rows
needed server features our earlier loopback gserver did not have; #208 added them
and #209 fixed what the first runs found, in a tight lab↔server loop. Behaviour
only; no addresses, captures stay in the lab kit. **[lab]**

Builds on [the terrain/water/sun route note](3d-terrain-water-sun-route-420r6-2026-11-26.md)
(why the old route couldn't exercise these) and
[replicators-512.md](replicators-512.md) (the replicator update layout and the
grass-vs-shape static read), which are cited, not repeated.

## T3D-135 — mid-session level warp: works on #209, both routes

A second world is a `config/graal3dworlds/NAME.txt` (same grammar as the main
`graal3dworld.txt`) with its own sky/objects/spawn. Two switch routes were tested:
the weapon3d `triggerserver(..,"g3dworld","cave")` (and `"default"` back), and a
TCP warp through a lab account (`players warp pc:1 cave.nw ...`, with a 2D level
`cave.nw` next to `graal3dworlds/cave.txt`). Both carry the linked 3D client across.

**#208 (ab3cc6d) — the bug.** The switch mostly worked: one UDP link held the
whole run (no relink), the sky swapped both ways (cave's own sky + fog; default's
blue came back), the player landed on the new spawn, and `clientr.g3dworld` read
`cave` then `default`. But the **old world's objects were never removed**: the
server log showed one "created on the client" (MARK only, never BIG) for the
switch *into* cave and none for the return. Diagnosis (confirmed by the server
author): `switch_world` removed a ghost and re-added one under the same key in the
same tick, hitting the "brought back before its delete was acked → whole again"
path, so neither the delete nor the re-create was sent.

**#209 — fixed and verified.** When an object is set under a key whose delete
isn't acked yet, the server now waits for the delete ack and then sends a real
`BIG` create at that index. On #209 every switch creates the new world's objects
on both routes (into cave: Sun, Sky, BIG, MARK; back: Sun, Sky, RED), the player
spawns correctly, `clientr.g3dworld` tracks, the link holds, and the shared
weapon3d is **sent once** (a `client.` counter in `onCreated` read "instance #1"
after three switches — `onCreated` runs once). With terrain drawn in both worlds
there is **no stale geometry**: cave shows BIG + fog sky and no RED; default shows
RED and no BIG.

**Two false alarms, corrected.** The "leftover cube" seen on #208 was partly a
5.12 **frame-clear artifact**: the client does not clear the black, untextured
ground region between frames (the same family as the horizon-band smear in
[T3D-116](multi-client-3d-lab-2026-11-25.md)), so an old draw lingers there even
after its object is gone. With terrain drawn the region is repainted and the
"cube" is gone. The real missing-create bug was underneath it and is the part #209
fixed. The "doubled showtext" was the **same** effect, not a second script: the
overlay text changes every tick and 5.12 draws the new text over the old in that
black area; with static text it reads cleanly. The warp weapon (`weapons/warpw.gs2`)
is a weapon3d file, not a 2D server weapon, and the account holds no weapons.

## T3D-136 — per-player objects: pass on #208

Two real 5.12 instances (named `pc:1` / `pc:2` by the server) on one world with
`objectfor pc:1 SECRET bigred.3ds 2 4 1` next to a shared `object RED`. The server
log shows **pc:1 got the SECRET ghost and pc:2 never did**; SECRET draws in every
pc:1 frame and no pc:2 frame. Each client saw the other's `G3DPlayer`; both links
held to quit.

Per-player **hide/show**: only pc:1's weapon3d sent
`triggerserver(..,"g3dhide","SECRET")` (and `RED`), then `"g3dshow"` 30 s later.
SECRET vanished from pc:1's screen and returned on show; the log shows RED and
SECRET re-created on **pc:1 only** (seq 238). pc:2 got no deletes or creates at any
point. So both per-player scoping (`objectfor`) and per-player hide/show are
client-isolated. (RED is confirmed by log only — it sits behind the player cubes
in this camera.)

## T3D-048 — replicator scatter: shapes scatter, grass wants a texture

World: streamed terrain (`terrain world_terrain 1`, 256 chunks), overhead camera,
`graal3d_pushterrain = true`, one line each class
(`replicator CLASS 0 0 0 4 2 6 SHAPE SEED`).

- **DynamicShapeReplicator** (`redcube.3ds`): scatters a dense carpet of its shape
  over the terrain (~150+ cubes within radius 4 cells). But on **#208** a **cold
  first visit drew no scatter at all** — the ghosts were created, but the cover
  only appeared on a warm second visit, the same "too late this session" pattern
  as textures/fonts. **#209** adds a server-side resend (each replicator's whole
  update at mission-start-end and 5/15/30 s, and after a world switch); on a cold
  first visit the scatter now **appears ~5–6 s after mission start** (matching the
  5 s resend) and stays for the run. So first-visit scatter is a server resend, not
  a client change.
- **DynamicGrass** / **DynamicGrassReplicator**: ghost fine but **draw nothing with
  a `.3ds`** — by design. Statically ([replicators-512.md](replicators-512.md)) the
  grass subclasses replace the cell-fill and grid-count setters (counts clamped
  0–100/cell vs 0–20 for shapes) and build their **own geometry**, expecting a
  **texture** name in `shapefiles`, not a shape. Prior lab confirmed a texture name
  draws (flat ground pieces; untextured under GDI, a lit patch under Mesa). The
  shape `dmk10.3ds` draws fine as a plain object, so the shape isn't the reason. A
  warm-visit confirm of the grass-as-texture path on #209 is the one small open
  follow-up.
- Terrain stayed **white** on 5.12 in the Windows 10 VM (GDI renderer) on cold and
  warm visits alike — the separate texture-apply issue tracked under T3D-044, not a
  replicator matter.

No crash and the link held on every run above.

## Summary

| row | verdict |
| --- | --- |
| T3D-135 level warp | works on #209; both routes; no relink, sky/spawn/`clientr.g3dworld` swap, real BIG creates both ways, no stale geometry (the #208 "stale cube" was a missing-create plus a frame-clear artifact) |
| T3D-136 per-player objects | pass on #208; `objectfor` scopes a ghost to one client, per-player hide/show affects only the calling client |
| T3D-048 replicator scatter | `DynamicShapeReplicator` scatters (cold first-visit works on #209 via the resend; warm always); the two grass classes expect a texture in `shapefiles`, not a shape |
