# The mission-lighting phase is a fixed handshake, not a per-object bake — it doesn't scale with lit-object count on 4.04r2 or 4.20r6 (T3D-052, Linux lab)

Date: 2026-11-26. Single-client lab on native Linux, 4.20r6 (5.12-class, protocol 24, g3d420 route) and 4.04r2 (protocol 19, g3d404 route), software GL; console-phase comparison at two object counts. Observation only. Board row: [T3D-052](3d-capability-board.tsv). Completes the partial (static + lighting look) in [live-512-lighting-and-sky](live-512-lighting-and-sky-2026-11-25.md); confirms the near-empty handshake of [T3D-092](3d-capability-board.tsv) (lightScene caching).

## Headline

**The mission-lighting phase does not scale with object count on either build.** It is a fixed, fast handshake, not a per-object light bake: the console phase structure is **identical for 2 and 50 lit shapes** on both 4.04r2 and 4.20r6.

## Method **[lab]**

Compared the mission-phase console sequence for **2** vs **50** lit `.3ds` shapes on each build. Precise sub-second timing could not be instrumented (a timestamping wrapper broke the client's connection), but the **phase structure is identical across object counts**, which settles the scaling question regardless of exact milliseconds.

## Result

- **4.20r6 (proto 24): two phases** — Phase 1 `Download Ghost Objects`, Phase 2 `Mission Lighting`. `Phase 2: Mission Lighting` → `Mission lighting done` are **adjacent console lines** — essentially instantaneous, **no bake**, **identical for 2 and 50 objects**. Confirms [T3D-092](3d-capability-board.tsv): a near-empty handshake with live Sun lighting, not a cached lightmap bake.
- **4.04r2 (proto 19): three phases** — Phase 1 `Download Datablocks` (the datablock era, absent on proto-24), Phase 2 `Download Ghost Objects`, Phase 3 `Mission Lighting`. The lighting phase runs a **fixed** TGE sequence (client "Replication Startup" + foliage/grass replicator startup) then `done` — **identical for 2 and 50 objects**, so no per-object scaling and no lightmap bake (there are no interiors/terrain to bake — [T3D-092](3d-capability-board.tsv)).

**Net:** both builds' lighting phase is a fixed, fast handshake that doesn't grow with lit-object count. 4.04r2's is slightly heavier (the proto-19 datablock phase plus TGE replication/foliage init); 4.20r6's is a bare two-line handshake.

## For a server

Adding more lit objects does **not** lengthen the mission-lighting phase on either build — object count is not a lighting cost. The proto-19 (4.04r2) client additionally runs a datablock-download phase and a fixed TGE replication/foliage startup that the proto-24 (5.12-class) client skips. Neither bakes lightmaps for GameObject shapes; shape lighting is the fixed live-light model of [live-512-lighting-and-sky](live-512-lighting-and-sky-2026-11-25.md).

## Method caveat

Scaling is established from the invariant phase structure (2 vs 50 objects), not from instrumented sub-second timings, which the client's connection wouldn't tolerate. A lightmap bake would still bind on **interior/terrain** content, which this scene (GameObject shapes + Sky only) does not include — so "no bake" is specifically about GameObject shape lighting, consistent with [T3D-092](3d-capability-board.tsv).
