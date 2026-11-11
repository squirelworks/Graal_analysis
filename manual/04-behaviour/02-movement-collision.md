<!-- manual: kind=reference status=draft -->
# 4.2 Movement and collision

This chapter gives the walking step, the wall test, what blocks a point, the blocked-step counter and the actions that hang off it (push pose, ledge jump, pushing blocks and NPCs), grab and pull, water and lava, link following, and the gates that stop movement. Tile type values and the `arrays.dat` lists are defined in → §3.5; this chapter only says how movement uses them. Units are tiles and 50 ms ticks (→ §4.1.1). Facings are 0 up, 1 left, 2 down, 3 right.

> Status: draft. The rule is read in full for 2.05, 2.17.1, 2.22 and 2.31; the exact 1st Graal geometry is now read statically, while 1.39 still lacks its numeric tables; 3.x and 4.x are not in the notes. Open points are App. E#302 to E#309.

## 4.2.1 The step

| Rule | Detail | Source |
| --- | --- | --- |
| one key, one step | each arrow key held is one step per tick; with several held, the steps run in the order up, left, down, right, each from the position the previous one left; a diagonal is two steps | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#one-key-one-step) |
| facing | the step first sets the player's facing to its direction | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#one-key-one-step) |
| step vector | (0, -0.5), (-0.5, 0), (0, 0.5), (0.5, 0) by facing, times a speed factor | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#one-key-one-step) |
| positions | doubles, in tiles | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#one-key-one-step) |
| first tick | the first tick after the key goes down already moves the player | [live][2.05] (client-internals/player-mannerisms-live.md#walking-idle-and-running-in-place-live) |
| release | letting go switches to `idle` frame 0 in the next tick; there is no slow-down and no finishing step | [live][2.05] (client-internals/player-mannerisms-live.md#walking-idle-and-running-in-place-live) |
| walk animation | `walk` advances one frame per tick, 8 frames, 8-tick cycle | [live][2.05] (client-internals/player-mannerisms-live.md#summary-table-205-rev-2) |

### 4.2.1.1 Speed factors

| Factor | When | Builds | Source |
| --- | --- | --- | --- |
| 1.0 | on foot, carrying or not (carrying does not slow the walk) | 2.05 | [2.05] (client-internals/decomp-findings-2026-10-25-l/01-walking-body-box.md#step); [live][2.05] (client-internals/player-mannerisms-live.md#lifting-carrying-hiding-and-throwing-live) |
| 1.2 | a high speed state | 2.05 | [2.05] (client-internals/decomp-findings-2026-10-25-l/01-walking-body-box.md#step) |
| 0.2 | hidden under a carried object: 0.1 tile per tick | 1.39, 1.41, 2.05, 2.22 | [live][1.39][1.41][2.05] (client-internals/player-mannerisms-live.md#cross-version-table); [1.39] (version-profiles/matrix/rules-139.md#wall--walk-test-bin-lab) |
| about 0.2 | hidden: 1.5 px per tick, steps of 2 and 1 px alternating | 5.x, 6.x | [wire] (protocol/v5v6-lab-play.md) |
| 0.4, 0.8 | exist in the walking code; not tied to states (→ App. E#302) | 2.05 to 2.31 | [bin] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |
| swimming | the same 0.5 tile per tick as walking | 1.39, 1.41, 2.05, 2.22, 5.x, 6.x | [live] (client-internals/player-mannerisms-live.md#cross-version-table); [wire] (protocol/v5v6-lab-play.md) |

### 4.2.1.2 Walking speed by build

| Build | Step per tick | Speed | Source |
| --- | --- | --- | --- |
| 1st Graal | 0.5 | 10 tiles/s | [live] (version-profiles/matrix/live-runs-2026-10-30.md#walking-speed) |
| 1.0 (10th) | 0.5 | 10 tiles/s | [live] (version-profiles/matrix/live-runs-2026-10-30.md#walking-speed) |
| 1.1 (15th) | 0.5 | 10 tiles/s | [live] (version-profiles/matrix/live-runs-2026-10-30.md#walking-speed) |
| 1.32 | 0.5 | 10 tiles/s | [live] (version-profiles/matrix/live-runs-2026-10-30.md#walking-speed) |
| 1.39 | 0.5 | 10 tiles/s | [live][1.39] (client-internals/player-mannerisms-live.md#cross-version-table) |
| 1.41 rev1 | 0.5; a second copy of y moves in 0.25 steps (the view or the drawn position) | 10 tiles/s | [live] (version-profiles/matrix/live-runs-2026-10-30.md#walking-speed) |
| 2.00 | unmeasured | unmeasured | [live] (version-profiles/matrix/live-runs-2026-10-30.md#walking-speed) |
| 2.05 rev2 | 0.5 | 10 tiles/s | [live] (version-profiles/matrix/live-runs-2026-10-30.md#walking-speed) |
| 2.17.1, 2.31 | 0.5 (read from the walking routine) | 10 tiles/s | [2.17.1][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md) |
| 2.22 | 0.5 (live and from the walking routine) | 10 tiles/s | [live][2.22] (live-runs/2gta-222-2026-10-30/README.md) |
| 1.3 test (GServer13) | 0.5 | 10 tiles/s | [live] (client-internals/live-gserver13.md) |
| 5.24r4, 5.30r3, 6.03r7 | 8 px (0.5) per tick | 10 tiles/s | [wire] (protocol/v5v6-lab-play.md) |

## 4.2.2 The wall test

### 4.2.2.1 Probe points (2.05 to 2.31)

Six points per facing, offsets from the sprite's top-left, read at the position the step would reach. They are numbered 0 to 5 in the order given:

| Facing | Fixed coordinate | The six points along the edge | Source |
| --- | --- | --- | --- |
| up | y + 1.0 | x + 0.525, 1.475, 1.525, 2.475, 2.525, 0.475 | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#the-probe-points) |
| left | x + 0.5 | y + 1.025, 1.975, 2.025, 2.975, 3.025, 0.975 | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#the-probe-points) |
| down | y + 3.0 | x + 0.525, 1.475, 1.525, 2.475, 2.525, 0.475 | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#the-probe-points) |
| right | x + 2.5 | y + 1.025, 1.975, 2.025, 2.975, 3.025, 0.975 | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#the-probe-points) |

| Rule | Detail | Source |
| --- | --- | --- |
| body box | the points lie on the leading edge of a two-tile square, x + 0.5 to x + 2.5, y + 1 to y + 3 | [2.05] (client-internals/decomp-findings-2026-10-25-l/01-walking-body-box.md#six-probe-points-per-facing) |
| point to tile | `floor(v + 0.0001)`: a point on a tile line reads the tile that starts there; a value a hair under a whole number reads the tile above | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#the-probe-points) |
| off the board | a tile outside 0 to 63 is the neighbour level's on a gmap, or a fixed tile outside a gmap | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#the-probe-points) |
| off the board, default tileset | the wall test checks bounds first and calls off-board a wall; the type tests skip the bounds check and read id 632, which is in no list of the 2.22 `arrays.dat` | [2.05] (client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md#the-default-tileset) |

### 4.2.2.2 The same test in earlier builds

| Build | Rule | Source |
| --- | --- | --- |
| 1st Graal | exact-input static step/probe/nudge and stepped-axis snapping rules are in → §4.2.2.3; cadence and exceptional gates remain unmeasured | [bin] (client-internals/first-graal-movement-2026-11-09.md) |
| 1.1 (15th) | after bumping furniture x carried a 0.025 offset (26.925) while walking, which fits a nudge rule of the 2.05 kind; not read | [live][inf] (version-profiles/matrix/live-runs-2026-10-30.md#walking-speed) |
| 1.39 | six probe offsets per facing step; the numeric tables are unread (→ App. E#307) | [1.39] (version-profiles/matrix/rules-139.md#wall--walk-test-bin-lab) |
| 1.39 | walking into a character NPC's side nudged the player along it at 0.125 tile per tick, and `playertouchsme` did not fire on that contact | [live][1.39] (client-internals/player-mannerisms-live.md#notes-per-build) |
| 2.05, 2.17.1, 2.22, 2.31 | as §4.2.2.1 to §4.2.4; the four agree on every table and constant | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md) |

### 4.2.2.3 Exact 1st Graal geometry

| Rule | Detail | Source |
| --- | --- | --- |
| input scope | exact Windows x86 executable identified in the source note; no 1.39 or later-build equivalence is established | [bin] (client-internals/first-graal-movement-2026-11-09.md#input-and-evidence-boundary) |
| position | separate little-endian doubles for world X/Y; integer parts select cells of a 64×64 board, supporting tile units | [bin] (client-internals/first-graal-movement-2026-11-09.md#coordinates-and-candidate-step) |
| camera | ordinary 640-pixel-wide viewport: x + 1.5 − 20 horizontally, y + 2 − 14 vertically, clamped to the board; screen displacement is not world displacement | [bin] (client-internals/first-graal-movement-2026-11-09.md#coordinates-and-candidate-step) |
| initial position | new-game/restart stores (24.5, 30) via the coordinate setters; second local player adds 12 to X | [bin] (client-internals/first-graal-movement-2026-11-09.md#coordinates-and-candidate-step) |

Offsets below are ordered probes 0–5 from the candidate after adding the facing step; true means blocked [bin] (client-internals/first-graal-movement-2026-11-09.md#ordered-probes).

| Facing | Candidate delta | Ordered offsets | Source |
| --- | --- | --- | --- |
| up | (0, −0.5) | (0.6, 1.05), (1.4, 1.05), (1.6, 1.05), (2.4, 1.05), (2.525, 1.05), (0.475, 1.05) | [bin] (client-internals/first-graal-movement-2026-11-09.md#ordered-probes) |
| left | (−0.5, 0) | (0.55, 1.1), (0.55, 1.9), (0.55, 2.1), (0.55, 2.9), (0.55, 3.025), (0.55, 0.975) | [bin] (client-internals/first-graal-movement-2026-11-09.md#ordered-probes) |
| down | (0, +0.5) | (0.6, 2.95), (1.4, 2.95), (1.6, 2.95), (2.4, 2.95), (2.525, 2.95), (0.475, 2.95) | [bin] (client-internals/first-graal-movement-2026-11-09.md#ordered-probes) |
| right | (+0.5, 0) | (2.45, 1.1), (2.45, 1.9), (2.45, 2.1), (2.45, 2.9), (2.45, 3.025), (2.45, 0.975) | [bin] (client-internals/first-graal-movement-2026-11-09.md#ordered-probes) |

| Rule | Detail | Source |
| --- | --- | --- |
| nudge axis/size | up/down: ±0.125 X; left/right: ±0.125 Y | [bin] (client-internals/first-graal-movement-2026-11-09.md#refusal-and-sideways-movement) |
| positive nudge | probe 0 blocked and probes 2, 3, 4 clear | [bin] (client-internals/first-graal-movement-2026-11-09.md#refusal-and-sideways-movement) |
| negative nudge | otherwise, probes 0 and 1 clear, probe 3 blocked and probe 5 clear; no new six-probe collection follows either nudge | [bin] (client-internals/first-graal-movement-2026-11-09.md#refusal-and-sideways-movement) |
| refusal | any of probes 0–3 blocked selects pushing and undoes the original facing delta; sideways nudge remains and clears the push count, otherwise the count increments | [bin] (client-internals/first-graal-movement-2026-11-09.md#refusal-and-sideways-movement) |
| snapping convention | for nonnegative coordinates, trunc is truncation toward zero; the helpers explicitly select it; all snaps affect the stepped axis | [bin] (client-internals/first-graal-movement-2026-11-09.md#refusal-and-sideways-movement) |
| up/down snap | when Y has a positive fractional part: up sets Y to trunc(Y); down sets Y to trunc(Y + 1) | [bin] (client-internals/first-graal-movement-2026-11-09.md#refusal-and-sideways-movement) |
| left/right snap | when X + 0.5 has a positive fractional part: left sets X to trunc(X + 0.5) − 0.5; right sets X to trunc(X + 1.5) − 0.5 | [bin] (client-internals/first-graal-movement-2026-11-09.md#refusal-and-sideways-movement) |
| counters | count ≥ 38 becomes 18; at 18 a passing ledge predicate selects an eight-tick hop; a count-28 helper can suppress position commits, with full semantics untraced | [bin] (client-internals/first-graal-movement-2026-11-09.md#refusal-and-sideways-movement) |
| limits | static constants/branches only; no new runtime cadence, all-state-gate or complete object-list validation; 1.39 tables remain open → App. E#307 | [bin] (client-internals/first-graal-movement-2026-11-09.md#verification-and-limits) |

## 4.2.3 What blocks a point

Tested in this order; the first hit blocks:

| # | Test | Source |
| --- | --- | --- |
| 1 | a list of objects with two flags and a player-sized body box, checked only when a client option is on (unidentified → App. E#303) | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#the-probe-points) |
| 2 | the level's NPCs that have a blocking shape or image | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#the-probe-points) |
| 3 | a list of 1.5 × 2 boxes with an enabled flag, x + 0.25 to x + 1.75, y to y + 2 (unidentified → App. E#303) | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#the-probe-points) |
| 4 | chests: each covers x to x + 2, y to y + 2, edges included, opened or not | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#the-probe-points) |
| 5 | the tile, which blocks unless it is in the passable list or the liquid list of `arrays.dat` (arrays 0 and 1, → §3.5.3) | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#the-probe-points) |

### 4.2.3.1 How the tile is answered, by tileset

| Tileset type | Wall | Source |
| --- | --- | --- |
| 0 (default, `pics1.png`) | not in array 0 and not in array 1; looked up by binary search of each sorted list, with no 4096-entry table built | [2.05] (client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md#the-default-tileset) |
| 1, 2 (new kind) | a fixed rule on the tile id: id 32; rows 26 and 27 with column 2 or more; rows 30 to 47, 84 to 95, 116 to 127; row 128 or more with `row / 16` odd (row = id / 16, column = id % 16) | [2.05] (client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md#tilesets-of-the-new-kind) |
| 5 | no board rule; only NPC shapes have types | [2.05] (client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md#which-rule-applies) |
| any | a `setshape2` NPC shape the player stands on answers first | [2.05] (client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md#which-rule-applies) |

Consequences on the default tileset:

| Rule | Detail | Source |
| --- | --- | --- |
| lava is liquid | the liquid list holds lava too, so lava is walkable and the swim test is true on it | [2.05] (client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md#the-default-tileset) |
| deep water | a tile in none of arrays 0 to 3 is a wall: the dark deep-water tile 3644 blocks, and `push` comes on the 18th refused step | [2.05] (client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md#the-default-tileset); [live][2.05] (client-internals/live-trace-205.md#water-and-lava-live-new4nw) |
| shallow water | a tile only in the passable list is walked on, not swum in | [2.05] (client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md#the-default-tileset) |
| several lists | a tile can be in several lists; in the 2.22 file 6 of the 133 throw-through tiles are passable, and the 9 lava tiles that are not liquid are all passable, so they are walked on and still burn | [file][2.05] (client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md#the-default-tileset) |
| thrown objects | a thrown object stops on a tile that is not type 20 and that the wall test calls a wall | [2.05] (client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md#the-default-tileset) |
| scripts | `onwall(x, y)` is this wall test; `onwater(x, y)` is the type 11 test, true on lava; on the classic board that test is the id range 64 ≤ id < 288, matching the type 11 step of the rule above [2.05][bin] (npc-library/gs1-move-205r2.md#options-and-collision); `tiletype(x, y)` returns -1 on the default tileset, 1 on type 5, and the fixed rule on types 1 and 2 (an NPC shape's type wins when above 1); 2.00 to 2.04 carry the same three names, their code not compared | [2.05] (client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md#script-functions) |

## 4.2.4 Refused steps, nudges and snaps

| Step | Rule | Source |
| --- | --- | --- |
| decision | points 0 to 3 decide: all four free keeps the step, any blocked refuses it | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#decision) |
| 1. corner nudge | if point 0 is blocked and points 2, 3 and 4 are free, add +0.1 across the edge (+x for up and down, +y for left and right); else if points 0 and 1 are free, point 3 is blocked and point 5 is free, add -0.1; the nudge is added to the stepped position | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#on-a-refused-step) |
| 2. take the step back | subtract the step vector times the speed factor; the nudge stays | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#on-a-refused-step) |
| 3. flush snap | along the facing only, when the coordinate has a fraction above 0: up `y = floor(y)`; left `x = floor(x + 0.5) - 0.5`; down `y = floor(y + 1)`; right `x = floor(x + 1.5) - 0.5`; there is no wall test on the snapped position | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#on-a-refused-step) |
| parent | on a platform object or with a parent, the snaps are relative to the parent's position | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#on-a-refused-step) |
| after every step | accepted or refused, `y` snaps to `floor(y + 0.0625)` if its fraction is under 0.0625 or over 0.9375, and x the same on `x + 0.5` (`x = floor(x + 0.5 + 0.0625) - 0.5`); then the position is stored, so a refused step still moves the player by the nudge and the snaps | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#after-every-step) |
| state | a refused step puts the player in the pushing mode (mode 1) | [2.05] (client-internals/decomp-findings-2026-10-25-l/01-walking-body-box.md#rule); [2.05] (client-internals/ledges-push-pull.md#player-modes-involved) |

Consequences of the rule:

| Rule | Detail | Source |
| --- | --- | --- |
| left and up | the probe is inside the body box, so the body stops with its edge on the wall's tile line without a snap | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#what-this-means-for-stopping-positions) |
| right and down | the probe is the tile line one tile beyond the body; the step that would put the body's edge on a wall's line is refused, and the flush snap moves the body that half-tile | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#what-this-means-for-stopping-positions) |
| gaps | a two-wide body fits a two-tile gap and not a one-tile gap | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#what-this-means-for-stopping-positions) |
| corners | pressing against the end of a wall slides the body round it at 0.1 tile per tick, ten ticks per tile | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#what-this-means-for-stopping-positions) |
| sliding along a wall | holding Down into a wall and adding Right walks right at full speed with `walk`; the push pose ends in that tick | [live][2.05] (client-internals/player-mannerisms-live.md#walking-idle-and-running-in-place-live) |
| live confirmation | the stopping positions are read from the binary and not walked on a live 2.22 (→ App. E#304) | [bin] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |

## 4.2.5 The blocked-step counter and the push pose

| Rule | Detail | Source |
| --- | --- | --- |
| counting | a step counts when it is refused and no corner nudge was applied; a free step or a nudge sets the count to 0, and so does the first refused step after a free one | [2.05] (client-internals/ledges-push-pull.md#the-ledge-test) |
| shared counter | the blocked-step count and the grab's pull cycle share one per-player counter | [2.05] (client-internals/ledges-push-pull.md#player-modes-involved) |
| running in place | a refused step still advances the walk frame; the gani stays `walk` until the push pose or a jump takes over | [live][2.05] (client-internals/live-trace-205.md#ledge-jump-and-running-in-place-live-new3nw) |
| push pose | `push` replaces `walk` on the 18th blocked tick (0.9 s); at 38 the count goes back to 18 and the gani restarts at frame 0 | [live][2.05] (client-internals/player-mannerisms-live.md#walking-idle-and-running-in-place-live) |
| push frames | 5 frames × 4 ticks = the 20-tick wrap, so the pose loops seamlessly | [live][2.05] (client-internals/player-mannerisms-live.md#walking-idle-and-running-in-place-live) |
| sliding resets | after a slide the count goes on from 1, so the full 18 ticks pass again before `push`; pressing into the wall again after letting go starts at 1 | [live][2.05] (client-internals/player-mannerisms-live.md#walking-idle-and-running-in-place-live) |
| on the wire | `push` is sprite steps 14 + frame (SPRITE 11, 12, 13, 11, 12) | [2.05] (client-internals/ledges-push-pull.md#sprites-on-the-wire) |

By build:

| Build | Push at | Wrap | Push frame length | Source |
| --- | --- | --- | --- | --- |
| 1st Graal | count 18 (the ledge test); push frames while the count is above 17 and not carrying | above 37 back to 18 | unmeasured | [bin] (version-profiles/matrix/rules-1st-graal.md#wall-and-walk-test-bin) |
| 1.39 | 18 | 38 to 18 | about 2 ticks (video) | [live][1.39] (client-internals/player-mannerisms-live.md#cross-version-table); [1.39] (version-profiles/matrix/rules-139.md#wall--walk-test-bin-lab) |
| 1.41 | 18 | 38 to 18 | 4 ticks (`push.gani`) | [live][1.41] (client-internals/player-mannerisms-live.md#cross-version-table) |
| 2.05 rev 2 | 18 | 38 to 18 | 4 ticks | [live][2.05] (client-internals/player-mannerisms-live.md#cross-version-table) |
| 2.22 | the tick after 18 blocked ticks | 37 back to 18 | 5 × 4 ticks, looping; a lab read of the frame field showed it cycling 0 to 3 each tick (→ App. E#305) | [live][2.22] (client-internals/player-mannerisms-live.md#cross-version-table); [live] (live-runs/2gta-222-2026-10-30/README.md) |
| 5.24r4, 5.30r3, 6.03r7 | 0.85 to 0.90 s after the walk started | unmeasured | unmeasured | [wire] (protocol/v5v6-lab-play.md) |

## 4.2.6 Ledge jumps

| Rule | Detail | Source |
| --- | --- | --- |
| when | the ledge test runs at blocked count 18, and again every 20 steps (the wrap) | [2.05] (client-internals/ledges-push-pull.md#the-ledge-test) |
| test point | from the player's position by facing up, left, down, right: (1.5, 0.5), (0, 2), (1.5, 3.5), (3, 2) | [2.05] (client-internals/ledges-push-pull.md#the-ledge-test) |
| ledge tile | the tile there must be a ledge tile for that facing: array 8 of `arrays.dat` on the default tileset (→ §3.5.3), or rows 30 and 31, columns 8 to 15, on a tileset of type 1 or 2 | [2.05] (client-internals/ledges-push-pull.md#arraysdat) |
| landing | from (x + 1.5, y + 2): (0, -5), (-6.5, 3), (0, 7), (6.5, 3); the landing point must pass the walking test (not a wall, not a chest), or the player just keeps pushing | [2.05] (client-internals/ledges-push-pull.md#the-ledge-test) |
| sound | `jump.wav` at (x + 1.5, y + 2) when the jump starts | [2.05] (client-internals/ledges-push-pull.md#the-ledge-test) |
| flight | 8 ticks from the position after the refused step, the first in the same tick as the start; keys are not read until landing; the blocked-step counter counts down 7 to 0 as the jump timer | [2.05] (client-internals/ledges-push-pull.md#the-ledge-test); [live][2.05] (client-internals/live-trace-205.md#ledge-jump-and-running-in-place-live-new3nw) |
| gani | none of its own: the walk (or push) gani stays; no sprite of its own on the wire | [live][2.05] (client-internals/live-trace-205.md#ledge-jump-and-running-in-place-live-new3nw); [2.05] (client-internals/ledges-push-pull.md#sprites-on-the-wire) |
| mode | mode 2 for the 8 ticks | [2.05] (client-internals/ledges-push-pull.md#player-modes-involved) |

The flight, per tick `i` = 0 to 7:

| Facing | Position | Source |
| --- | --- | --- |
| up | `y0 - [1.5, 2.7, 3.8, 4.5, 5.0, 5.2, 5.2, 5.0][i]`; live from y0 = 14: 12.5, 11.3, 10.2, 9.5, 9.0, 8.8, 8.8, 9.0 | [2.05] (client-internals/ledges-push-pull.md#the-ledge-test); [live][2.05] (client-internals/live-trace-205.md#ledge-jump-and-running-in-place-live-new3nw) |
| down | `y0 + [-0.2, 0.2, 0.5, 1.5, 2.8, 4.0, 5.4, 7.0][i]` | [2.05] (client-internals/ledges-push-pull.md#the-ledge-test) |
| left, right | `x0 -/+ [1, 2, 3, 3.8, 4.5, 5.2, 5.8, 6.5][i]`, `y0 + [-0.2, -0.5, 0, 0.5, 1.1, 1.7, 2.3, 3.0][i]` | [2.05] (client-internals/ledges-push-pull.md#the-ledge-test) |

| Build | Difference | Source |
| --- | --- | --- |
| 1st Graal | at count 18 a passing ledge test sets the hop mode and the counter to 8; the hop follows a facing table for 8 ticks | [bin] (version-profiles/matrix/rules-1st-graal.md#wall-and-walk-test-bin) |
| 2.22, 2.31 | the same counts, probe points, flight curve and tables as 2.05; `jump.wav` plays only while the current gani is a built-in name (→ §4.2.12) | [2.22][2.31] (client-internals/ledges-push-pull.md#222-and-231) |

## 4.2.7 Pushing blocks and NPCs

| Rule | Detail | Source |
| --- | --- | --- |
| when | at count 28 (checked before the step is counted, so on the 29th blocked step), and every 20 after | [2.05] (client-internals/ledges-push-pull.md#pushing) |
| trigger | the try first fires the trigger action `pushed` at the ledge test point, with the facing as its parameter (→ §4.2.9) | [2.05] (client-internals/ledges-push-pull.md#pushing) |
| block | the tile under that point is compared with the four tiles of the pushable block (array 16, entry 0, → §3.5.3); only that one tile is compared, and its place in the block gives the block's top-left | [2.05] (client-internals/ledges-push-pull.md#pushing) |
| target cells | from the block's top-left: up (0, -1) (1, -1); left (-1, 0) (-1, 1); down (0, 2) (1, 2); right (2, 0) (2, 1); none may be a wall, a chest, water, a chair or the lower half of a bed | [2.05] (client-internals/ledges-push-pull.md#pushing) |
| move | each old cell first takes the tile two cells ahead, then the block is written one cell ahead, so the row the block leaves gets the floor that was in front of it | [2.05] (client-internals/ledges-push-pull.md#pushing) |
| after | online, the 4 × 4 area round the old spot goes to the server as a board modify; the player moves one tile in the facing; `stonemove.wav` plays | [2.05] (client-internals/ledges-push-pull.md#pushing) |

### 4.2.7.1 Pushed NPCs

| Rule | Detail | Source |
| --- | --- | --- |
| lookup | with no block found, the level's NPC hit test at the point: a character NPC in x + 0.5 to x + 2.5, y + 1 to y + 3; a `setshape2` NPC by its shape's tile types; a gani NPC by its animation; any other by its image box `[x, x + w/16) × [y, y + h/16)`, where a transparent pixel is a miss for plain image NPCs | [2.05] (client-internals/ledges-push-pull.md#pushed-and-pulled-npcs) |
| permission | the NPC needs `canbepushed` (GS1 command 44, cleared by 45, → §8.2) | [2.05] (client-internals/ledges-push-pull.md#pushed-and-pulled-npcs) |
| edge test | with the NPC left out of its own test, every point along the edge it moves into is checked, one per tile, `t` while `t < x + w` (or `y + h`): up (t, y - 1), left (x - 1, t), down (t, y + h), right (x + w, t); sizes in pixels / 16, character and gani NPCs count as 48 × 48 | [2.05] (client-internals/ledges-push-pull.md#pushed-and-pulled-npcs) |
| blocked-point test for NPCs | other players (online only), blocking NPCs, two level object lists, and wall tiles; water does not stop an NPC | [2.05] (client-internals/ledges-push-pull.md#pushed-and-pulled-npcs) |
| move | the NPC moves one tile, the player one tile the same way, `waspushed` fires on the NPC (`actionpushed` has already fired), and the block sound plays | [2.05] (client-internals/ledges-push-pull.md#pushed-and-pulled-npcs) |
| water | a character NPC that crosses a water edge gets the splash and switches between `swim` and `idle` | [2.05] (client-internals/ledges-push-pull.md#pushed-and-pulled-npcs) |
| server | nothing is sent for the NPC move; the `pushed` trigger action is the only message | [2.05] (client-internals/ledges-push-pull.md#pushed-and-pulled-npcs) |
| 2.22 | the NPC lookup also searches the neighbouring map parts on a gmap | [2.22] (client-internals/ledges-push-pull.md#pushed-and-pulled-npcs) |

## 4.2.8 Grab and pull

| Rule | Detail | Source |
| --- | --- | --- |
| A key order | throw what is carried; else lift (→ §4.5); else grab | [2.05] (client-internals/ledges-push-pull.md#grabbing-and-pulling) |
| grab test | by facing (1.5, 0.9), (0, 2), (1.5, 3.1), (3, 2): a wall tile, or an NPC that blocks; nothing is grabbed when another player stands there | [2.05] (client-internals/ledges-push-pull.md#grabbing-and-pulling) |
| grab on NPCs | 2.05 grabs a blocking NPC only when a per-NPC flag (most likely the character-shape flag) is clear; 2.22 and 2.31 grab any blocking NPC, and search the neighbouring map parts | [2.05][2.22][2.31][inf] (client-internals/ledges-push-pull.md#222-and-231) |
| holding | the grab lasts while A is held; arrows do not move or turn the player; mode 5 | [2.05] (client-internals/ledges-push-pull.md#grabbing-and-pulling) |
| pull cycle | the arrow away from the wall sets the counter to 2 and starts `pull`; the counter runs 2 to 19 and back to 2 (18 ticks); a pull is tried whenever the arrow is held at 19; letting go of any arrow sets the counter to 1 | [2.05] (client-internals/ledges-push-pull.md#grabbing-and-pulling) |
| pull try | fires `pulled` one tile out from the body, (1.5, 0), (-0.5, 2), (1.5, 4), (3.5, 2) by facing, with the opposite facing as parameter, then reads the tile at the grab point | [2.05] (client-internals/ledges-push-pull.md#grabbing-and-pulling) |
| pullable block | array 16, entry 1 (→ §3.5.3); the two cells behind the player must be free, from the block's top-left: up (0, 4) (1, 4); left (4, 0) (4, 1); down (0, -3) (1, -3); right (-3, 0) (-3, 1); the block moves one tile towards the player (each old cell first takes the tile two cells behind), the player steps back one tile, and `lift.wav` plays, or `lift2.wav` by a player flag (→ App. E#306) | [2.05] (client-internals/ledges-push-pull.md#grabbing-and-pulling) |
| pulled NPCs | with no pullable block, an NPC with `canbepulled` (command 46, cleared by 47) is pulled: the two cells behind the player must be free from the whole-tile grab cell (up (0, 3) (1, 3); left (3, 0) (3, 1); down (0, -3) (1, -3); right (-3, 0) (-3, 1)), then the edge facing the player is checked (up (t, y + h), left (x + w, t), down (t, y - 1), right (x - 1, t)); NPC and player move one tile back and `waspulled` fires; nothing goes to the server | [2.05] (client-internals/ledges-push-pull.md#grabbing-and-pulling) |
| futile pull | on anything else (a wall, a rock too heavy for the glove, a push block) nothing moves; `pulled` still fires every 18 ticks and `pull` keeps playing | [2.05] (client-internals/ledges-push-pull.md#grabbing-and-pulling) |
| on the wire | `grab` is sprite step 19 (SPRITE 14); `pull` steps 20 + frame (SPRITE 15, 16, 17) | [2.05] (client-internals/ledges-push-pull.md#sprites-on-the-wire) |

Pose timing by build:

| Build | Pull frames | Arrow released during a pull | A released after a pull | Source |
| --- | --- | --- | --- | --- |
| 1.41 | unmeasured | back to `grab` | `grab` stays until the next action | [live][1.41] (client-internals/player-mannerisms-live.md#cross-version-table) |
| 2.05 rev 2 | 3 frames × 2 ticks | counter to 1; the pose stays `pull`, animating | `pull` loops until the next key moves the player | [live][2.05] (client-internals/player-mannerisms-live.md#grab-and-pull-live) |
| 2.22 | 3 × 2 (`pull.gani`) | stays `pull`, looping | as 2.05 | [live][2.22] (client-internals/player-mannerisms-live.md#cross-version-table) |
| 5.x, 6.x | unmeasured | unmeasured | unmeasured; `grab` and `pull` start in the next tick, the stone stays put, dust is drawn at the feet | [wire][shot] (protocol/v5v6-lab-play.md) |

## 4.2.9 The push and pull trigger actions

| Rule | Detail | Source |
| --- | --- | --- |
| local | NPCs at the point see `actionpushed` or `actionpulled` | [2.05] (client-internals/ledges-push-pull.md#summary) |
| server | `PLI_TRIGGERACTION` (38, → §2.4): GINT 0 (no NPC), `GCHAR x*2`, `GCHAR y*2`, the action name, then `,` and the parameter as a decimal string when there is one (`pushed,0`) | [2.05] (client-internals/ledges-push-pull.md#the-trigger-action-on-the-wire) |
| peers | 2.05 also sends it to UDP peers as UDP id 26 (→ §2.9) | [2.05] (client-internals/ledges-push-pull.md#the-trigger-action-on-the-wire) |
| cadence, 2.05 | one try on the 29th blocked step, then every 20 steps (push); every 18 ticks (pull) | [2.05] (client-internals/ledges-push-pull.md#pushing); [2.05] (client-internals/ledges-push-pull.md#grabbing-and-pulling) |
| cadence, 5.x and 6.x | `pushed,0` about 0.55 s after `push` starts, then every 1.0 s; `pulled,1` 0.85 s into a pull | [wire] (protocol/v5v6-lab-play.md) |

## 4.2.10 Water and lava

| Rule | Detail | Source |
| --- | --- | --- |
| check | every tick, except while the sword swings, while riding, and when the player is not under local control | [2.05] (client-internals/water-and-ganis.md#water) |
| entry point | the switch to `swim` happens on the tick the point (x + 1.5, y + 2) is on a liquid tile; leaving happens when it is off, and `walk` comes back at frame 0 | [live][2.05] (client-internals/player-mannerisms-live.md#swimming-live) |
| entering | when not already swimming: a splash (break effect 5) at the player's position; two more splashes when the player was not walking (a warp or a knock); then swim mode with `swim`, or `lava` when the tile type is 12 | [2.05] (client-internals/water-and-ganis.md#water) |
| leaving | one splash, then back to standing | [2.05] (client-internals/water-and-ganis.md#water) |
| splash sound | `water.wav` at (x + 1, y + 1) from the effect's anchor; every other break effect plays `crush.wav` | [2.05] (client-internals/water-and-ganis.md#break-effect-sounds) |
| swim mode | mode 10: set on a type 11 tile; cannot be hurt; the sword needs no horse | [2.05] (client-internals/decomp-findings-2026-10-24/player-modes.tsv) |
| status bit | while crossing water 1.28 beta 2 sets STATUS bit 0x04 and sends prop 18 | [cap] (client-internals/live-trace-early.md#gserver-128-with-128-beta-2-gserv013) |

Swimming by build:

| Build | Standing still in water | Swim frames | Source |
| --- | --- | --- | --- |
| 1.39 | only the head and a water ring are drawn; the ring keeps alternating, the head stays still | n/a (no ganis) | [live][1.39] (client-internals/player-mannerisms-live.md#notes-per-build) |
| 1.41 | `swim` frame resets to 0 and freezes | unmeasured | [live][1.41] (client-internals/player-mannerisms-live.md#cross-version-table) |
| 2.05 rev 2 | keeps animating; does not reset when the player turns | 8 frames × 2 ticks (16-tick stroke) | [live][2.05] (client-internals/player-mannerisms-live.md#swimming-live) |
| 2.22 | keeps animating; the frame resets to 0 at the stop, then runs on | 8 × 2 | [live][2.22] (client-internals/player-mannerisms-live.md#cross-version-table) |
| 5.x, 6.x | unmeasured; `swim` from the first water step, only the head with a ripple, sideways strokes throw splashes | unmeasured | [wire][shot] (protocol/v5v6-lab-play.md) |

### 4.2.10.1 Lava burn

| Rule | Detail | Source |
| --- | --- | --- |
| test | once per player tick, one point, the position plus (1.5, 2), against the lava list (array 3) only; the order of the two offsets is inferred | [2.05][inf] (client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md#the-default-tileset) |
| counter | on lava a counter runs 0 to 100 and wraps to 0 on the next tick: one burn every 101 ticks; a tick off lava sets it to 0 | [live][2.05] (client-internals/live-trace-205.md#water-and-lava-live-new4nw); [2.05] (client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md#the-default-tileset) |
| burn | half a heart through the hurt routine, with a flag that skips the usual "can be hurt" checks (→ §4.3); reading that call as the hurt routine is inferred | [2.05][inf] (client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md#the-default-tileset) |
| tiles | the bright-red lava tile 2882 is swum in (`lava` gani) and burns; the dark-red lava floor 2958 is walked on and burns | [live][2.05] (client-internals/live-trace-205.md#water-and-lava-live-new4nw) |

## 4.2.11 Following links

| Rule | Detail | Source |
| --- | --- | --- |
| neighbours | on entering a level while a big map is loaded, the client fills a 3 × 3 table of level names round it from the big map's text grid (→ §3.2.5); cells off the grid stay empty; the step is skipped under an unidentified flag (→ App. E#308) | [2.05] (client-internals/decomp-findings-2026-10-28/03-edge-links.md#the-levels-neighbours) |
| probe | each tick, the player's position plus a per-facing offset (offsets unread → App. E#308) | [2.05] (client-internals/decomp-findings-2026-10-28/03-edge-links.md#following-a-link) |
| order | each link of the level in order; the first that fires is taken; offline the client loads the level, online it asks the server | [2.05] (client-internals/decomp-findings-2026-10-28/03-edge-links.md#following-a-link) |

| Link | Fires when | Arrival | Source |
| --- | --- | --- | --- |
| west edge: x 0, width 1, destination = west neighbour | probe x ≤ 0 facing left, or player x < -2.5, or (neighbour not loaded) probe in the rectangle | x = player x + 64, y unchanged | [2.05] (client-internals/decomp-findings-2026-10-28/03-edge-links.md#following-a-link) |
| east edge: x 63, width 1, destination = east neighbour | probe x ≥ 64 facing right, or player x > 63.5, or (not loaded) probe in the rectangle | x = player x - 64 | [2.05] (client-internals/decomp-findings-2026-10-28/03-edge-links.md#following-a-link) |
| north edge: y 0, height 1, destination = north neighbour | probe y ≤ 0 facing up, or player y < -3.0, or (not loaded) probe in the rectangle | y = player y + 64 | [2.05] (client-internals/decomp-findings-2026-10-28/03-edge-links.md#following-a-link) |
| south edge: y 63, height 1, destination = south neighbour | probe y ≥ 64 facing down, or player y > 63.0, or (not loaded) probe in the rectangle | y = player y - 64 | [2.05] (client-internals/decomp-findings-2026-10-28/03-edge-links.md#following-a-link) |
| any other link | probe in the rectangle; a probe within 1 tile of an edge (x or y ≤ 1 or ≥ 63) counts only while the player faces out across that edge | the link's new-x and new-y, evaluated as expressions; a missing or `-1` value means `playerx` / `playery` | [2.05] (client-internals/decomp-findings-2026-10-28/03-edge-links.md#following-a-link) |

| Rule | Detail | Source |
| --- | --- | --- |
| seam | an edge link between big-map neighbours keeps the player's exact offset across the seam (east off x 63.6 arrives at x -0.4), whatever its new-x says | [2.05] (client-internals/decomp-findings-2026-10-28/03-edge-links.md#following-a-link) |
| no big map | without a big map, or for a level that is not the neighbour, the link's own coordinates apply, and `playerx` on an east-edge link arrives on the east edge of the destination | [2.05] (client-internals/decomp-findings-2026-10-28/03-edge-links.md#following-a-link) |
| editor defaults | a new edge link gets new-x `0` on the east edge, new-y `0` on the south edge, new-x `61` on the west edge and new-y `61` on the north edge; the other coordinate stays `playerx` / `playery` | [2.05] (client-internals/decomp-findings-2026-10-28/03-edge-links.md#link-records-for-reference) |
| level-entry messages | what the client sends on each level entry is in → §2.4 | [2.31] (client-internals/decomp-findings-2026-10-24-b/03-periodic-ids-2.31.md#pli-46-on-every-level-entry-gchar-1) |

## 4.2.12 Gates that stop movement (2.22, 2.31)

| Rule | Detail | Source |
| --- | --- | --- |
| stop gates | walking, the ledge test, the A key and other gameplay code do nothing while either of two server-set flags is on; server messages 176 and 177 set them (→ §2.5.8); reading them as the full-stop messages is an inference | [2.22][2.31][inf] (client-internals/ledges-push-pull.md#222-and-231) |
| connection flag | a further flag on the server connection also stops gani changes, footsteps and the A key; its meaning was not found | [2.22] (client-internals/ledges-push-pull.md#222-and-231) |
| built-in gani gate | `jump.wav`, `stonemove.wav`, the pull sound and footsteps play only while the current gani is a built-in name (→ §4.10); the jump, push and pull still happen under a custom gani; sound names are bare (`jump.wav`) instead of under `sounds/` | [2.22][2.31] (client-internals/ledges-push-pull.md#222-and-231) |
| 2.05 | none of these gates | [2.05] (client-internals/ledges-push-pull.md#222-and-231) |
