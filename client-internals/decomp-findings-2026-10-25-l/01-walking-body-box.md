# Walking: the wall test is a box, not a point

Date: 2026-10-25. Source: the 2.05 client's walking routine (derived).

The older note (`../foot-test.md`) measured a single-point test in an SDL
reimplementation and said the official client "used a different body-block
mask". This is that mask.

## Step

* Each arrow key is a separate step, handled in the order up, left, down,
  right. A diagonal is two steps, each tested against the position the
  previous one left.
* A step is half a tile times a speed factor: 1.0 on foot, 1.2 with a high
  speed state. Other factors (swimming, carrying) exist; their values were not
  read here. The step vectors per facing are (0, -0.5), (-0.5, 0), (0, 0.5),
  (0.5, 0).

## Six probe points per facing

Offsets from the sprite's top-left, evaluated at the position the step would
reach:

| facing | the points |
|---|---|
| up | y + 1.0; x + 0.525, 1.475, 1.525, 2.475, 2.525, 0.475 |
| left | x + 0.5; y + 1.025, 1.975, 2.025, 2.975, 3.025, 0.975 |
| down | y + 3.0; x + 0.525, 1.475, 1.525, 2.475, 2.525, 0.475 |
| right | x + 2.5; y + 1.025, 1.975, 2.025, 2.975, 3.025, 0.975 |

That is a box x + 0.5 .. x + 2.5, y + 1 .. y + 3 (two tiles square), with the
points on its leading edge. Points are truncated to a tile.

## Rule

* The step is kept when the **first four** points are free.
* Otherwise the position is put back and the player is put in the "pushing"
  state (the push/pull block action starts from that state).
* On a refused step, a 0.1-tile nudge along the edge may apply so a corner does
  not catch. With points numbered 1..6: if point 1 is blocked and 3, 4, 5 are
  free, move +0.1 across the edge (right for up/down, down for left/right);
  if 1 and 2 are free, 4 is blocked and 6 is free, move -0.1.
* After the step the fractional part of the position is snapped to a tile
  edge when it lies within 0.0625 of it (not read in detail).

## What a point tests

Blocked if any of: a chest record covers it (2 x 2, edges included, opened or
not); a solid object sprite or another blocking sprite is there; the tile is
neither in the passable list (`arrays.dat` array 0) nor in the liquid list
(array 1). Lava is a liquid and walkable.

## Other probes (same routine family)

* A-key probe, lift, and sword cut: one tile beyond the middle of the leading
  edge: up (x + 1.5, y), left (x - 0.5, y + 2), down (x + 1.5, y + 4),
  right (x + 3.5, y + 2).
* A separate probe set is used by the push/pull block action; not read here.
