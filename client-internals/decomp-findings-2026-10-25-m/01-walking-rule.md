# The walking rule, whole

Date: 2026-10-25. Source: the walking routine of the 2.05, 2.17.1, 2.22 and
2.31 clients (derived; the four agree on every table and constant below).

## One key, one step

The routine is given the key's direction, 0 up, 1 left, 2 down, 3 right, and
runs the step for that direction. With several keys held the steps run in the
order up, left, down, right, each at the position the earlier ones left. The first thing
it does is set the player's facing to that direction. A step is half a tile
times a speed factor (1.0 on foot); the step vectors are (0, -0.5), (-0.5, 0),
(0, 0.5), (0.5, 0). Positions are doubles, in tiles.

## The probe points

Six points per facing, as offsets from the sprite's top-left, read at the
position the step would reach (table as in `../decomp-findings-2026-10-25-l/
01-walking-body-box.md`):

| facing | the six points |
|---|---|
| up | y + 1.0; x + 0.525, 1.475, 1.525, 2.475, 2.525, 0.475 |
| left | x + 0.5; y + 1.025, 1.975, 2.025, 2.975, 3.025, 0.975 |
| down | y + 3.0; x + 0.525, 1.475, 1.525, 2.475, 2.525, 0.475 |
| right | x + 2.5; y + 1.025, 1.975, 2.025, 2.975, 3.025, 0.975 |

Numbered 0 to 5 in that order. Each point goes through the same blocked test,
which returns blocked or free.

**Point to tile.** A coordinate becomes a tile as `floor(v + 0.0001)`. A point
exactly on a tile line reads the tile that starts there; a value a hair under a
whole number (rounding) reads the tile above it. A tile outside 0..63 is not
read from this level: it is the neighbour in a gmap, or a fixed tile outside a
gmap.

**What blocks a point.** In this order: a list of objects with two flags and a
body box like the player's (only when a client option is on); the level's NPCs
that have a blocking shape or image; a list of 1.5 x 2 boxes with an enabled
flag (x + 0.25 to x + 1.75, y to y + 2); the chests (each record x, y to x + 2,
y + 2, edges included, opened or not); then the tile, which blocks unless its
id is in one of the two passable lists of `arrays.dat` (arrays 0 and 1). The
first list and the 1.5 x 2 list were not identified.

## Decision

Points 0 to 3 are the step test. If all four are free the step is kept
(and the position is set to the stepped one). If any is blocked it is refused.

## On a refused step

In this order:

1. **Corner nudge.** If point 0 is blocked and points 2, 3 and 4 are free:
   add 0.1 across the edge (+x for up and down, +y for left and right). Else if
   points 0 and 1 are free, point 3 is blocked and point 5 is free: add -0.1.
   The nudge table is the same in all four clients:
   up and down `(+0.1, 0)` and `(-0.1, 0)`, left and right `(0, +0.1)` and
   `(0, -0.1)`. It is added to the stepped position.
2. **Take the step back** (subtract the step vector times the speed factor).
   The nudge stays.
3. **Flush snap, along the facing only**, if the fraction of the coordinate is
   above zero (the fraction is 0 for a value just under a whole number):
   up `y = floor(y)`; left `x = floor(x + 0.5) - 0.5`; down `y = floor(y + 1)`;
   right `x = floor(x + 1.5) - 0.5`. The body's edge ends on a tile line.
   There is no wall test on the snapped position.

When the player is standing on a platform object or has a parent, the snaps are
relative to the parent's position; without one the offset is 0.

## After every step

Accepted or refused: `y` snaps to `floor(y + 0.0625)` if the fraction of y is
under 0.0625 or over 0.9375. The same for x on `x + 0.5`: if its fraction is
out of that band, `x = floor(x + 0.5 + 0.0625) - 0.5`. Then the position is
stored. (A refused step still stores the position: that is how the nudge and
the flush snap move the player.)

## What this means for stopping positions

* Moving left or up, the probe is inside the body box; a body ends with its
  edge on the wall's tile line without any snap.
* Moving right or down, the probe is the tile line one tile beyond the body. The
  step that would put the body's right or bottom edge on a wall's tile line is
  refused (its probe reads the wall tile), and the flush snap then moves the
  body that half tile. Without the snap the body would stop half a tile short.
* A 2-wide body fits a 2-tile gap and not a 1-tile gap.
* Pressing against the end of a wall slides the body round it at 0.1 tile per
  tick: ten ticks to clear one tile.

## Not read

See `open-questions.tsv`.
