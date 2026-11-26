# The 5.12-class 3D entry route on our gserver is the mission-phases sequence, with GhostAlways nested inside Phase 1 and the 3D GUI attaching at the control object (T3D-022, Linux 4.20r6)

Date: 2026-11-26. Single-client lab on native Linux 4.20r6 (5.12-class, protocol 24, g3d420 route), software GL; a logging weapon traced the login steps and GUI attach. Observation only. Board row: [T3D-022](3d-capability-board.tsv). Complements the third-party capture (the phase-free route seen 2026-11-24, [live-512-third-party-session](live-512-third-party-session-2026-11-24.md)); the lighting phase is [T3D-052](3d-lighting-phase-timing-404r2-420r6-2026-11-26.md); the class-set corroboration is [T3D-026](3d-capability-board.tsv).

## Headline

Our own gserver drives the **mission-phases** entry route (not the phase-free "ghost-always-only" route). The client still reaches every login step because the **GhostAlways events ride inside Phase 1**, not as a standalone phase-free entry. The **3D GUI (`GuiGraal3DCtrl`) attaches at the Initial Control Object**, as the scene renders.

## The entry sequence **[lab]**

A logging weapon observed this order:

1. `Graal has been activated!`
2. `Loading tile definitions for server Login`
3. `Phase 1: Download Ghost Objects` — the **GhostAlways** events ride **inside** Phase 1: `GhostAlwaysStarting` → the ghosts → `GhostAlwaysDone`, after `DataBlocksDone`.
4. `Phase 2: Mission Lighting` → `Mission lighting done` (the fixed two-line handshake of [T3D-052](3d-lighting-phase-timing-404r2-420r6-2026-11-26.md)).
5. `Initial Control Object` — the control object arrives and the **3D GUI (`GuiGraal3DCtrl`) attaches** as the scene renders.

## Phase-free vs phase route

- The **phase-free (ghost-always-only) route** is real — it was captured on a third-party server ([live-512-third-party-session](live-512-third-party-session-2026-11-24.md), where the world arrived as ghost-always events with no mission phases). But **our gserver does not run it**: it always sends `MissionStartPhase1/2/3` with GhostAlways nested in Phase 1. A phase-free variant would need a gserver emit mode we don't enable.
- So GhostAlways exists on our route too, but as a **sub-step of Phase 1**, which is why the client reaches the same login steps either way: the GhostAlways delivery is common to both; only the surrounding phase framing differs.

## Corroboration (T3D-026)

The same run confirms the 4.20r6 client unpacks the shared gserver's GameObject section order `NAME→VELOCITY→SHAPE→SKIN→TRANSFORM→CHAT→ATTR[1..8]→NICKNAME→FLAGS` and registers the same ~28-class proto-24 set as 5.12 ([T3D-081](3d-capability-board.tsv)/[T3D-026](3d-capability-board.tsv)) — one server drives a 4.20r6 and a 5.12 client as the same wire target.

## For a server

3D entry over our route is the **mission-phases** sequence: Phase 1 (ghost objects + GhostAlways), Phase 2 (mission lighting), then the Initial Control Object, at which the 3D GUI attaches. The phase-free route is possible (third-party servers use it) but is a separate gserver emit mode, not the default here.

## Method caveat

Single client, our own loopback gserver, software GL. The step order is the console/log sequence the client prints; the phase-free comparison rests on the earlier third-party capture, not on reconfiguring our gserver to emit phase-free this run.
