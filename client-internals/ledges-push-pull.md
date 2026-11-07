# Ledge jumps, pushing and pulling (2.05)

Date: 2026-10-28. Read from the 2.05 rev 2 client; tile lists from the 2.22 install's `arrays.dat`. **[2.05]** unless tagged. No addresses, routine names or decompiler text. Units are tiles; a tick is the 50 ms game tick, and a walk step is one arrow key in one tick. Test level: `new3.nw` (Seihai `client/tests/fixtures/levels/new3.nw`).

## Summary

1. Running into a wall shows the `push` gani once the player has been stopped for 18 steps in a row (0.9 s).
2. Running into a ledge jumps the player off after the same 18 steps, with `jump.wav`: 8 ticks along a fixed curve. No gani changes in the air (the walk gani stays); keys are not read.
3. Running into a stone block pushes it one tile on the 29th blocked step, then every 20 steps. The player follows one tile; `stonemove.wav`.
4. A on a wall (nothing to lift) grabs it (`grab` gani) and holds while A is held. The arrow away from the wall plays `pull`. Every 18 ticks the client tries a pull. A pullable block comes one tile and the player steps back (`lift.wav`, or `lift2.wav` by a player flag not traced). Anything else, including a wall or a rock too heavy for the glove, does not move: the pull gani keeps playing and the `pulled` trigger still fires every 18 ticks. Letting go of the arrow returns to holding; letting go of A ends the grab.
5. Every push and pull try fires a trigger action (`pushed` / `pulled`) at a point in front, which NPCs there see as `actionpushed` / `actionpulled`; online it also goes to the server (PLI_TRIGGERACTION, 38) and to UDP peers (id 26).

## Player modes involved

| mode | meaning |
|---|---|
| 0 | normal |
| 1 | pushing (last step refused) |
| 2 | ledge jump (8 ticks) |
| 4 | lifting (5 ticks, then carrying) |
| 5 | grab / pull |

The blocked-step count and the grab's pull cycle share one per-player counter.

## The ledge test

The client counts blocked steps. A step counts when it is refused and no corner nudge was applied; a free step or a nudge sets the count back to 0, and so does the first refused step after a free one.

* At count 18 the ledge test runs. At 38 the count goes back to 18, so it runs again every 20 steps.
* Test point, from the player's position, by facing (up, left, down, right): `(1.5, 0.5)`, `(0, 2)`, `(1.5, 3.5)`, `(3, 2)`. The tile there must be a ledge tile **for that facing**. In the usual tile mode those are the four lists of `arrays.dat` array 8 (2.05 calls the class tile type 21, "jumping stone"):

| facing | ledge tiles (2.22 `arrays.dat`) |
|---|---|
| up | 190, 191, 4045, 4046 |
| left | 212, 228, 563, 579, 4028, 4044 |
| down | 185, 186, 4061, 4062 |
| right | 273, 289, 4031, 4047 |

* Landing point, from `(x + 1.5, y + 2)`: `(0, -5)`, `(-6.5, 3)`, `(0, 7)`, `(6.5, 3)`. It must pass the ordinary walking test (not a wall, not a chest). If it does not, the player just keeps pushing.
* The jump starts from the position after the refused step. Per tick `i = 0..7` (the first in the same tick as the start):

| facing | position |
|---|---|
| up | `y0 - [1.5, 2.7, 3.8, 4.5, 5.0, 5.2, 5.2, 5.0][i]` |
| down | `y0 + [-0.2, 0.2, 0.5, 1.5, 2.8, 4.0, 5.4, 7.0][i]` |
| left / right | `x0 -/+ [1, 2, 3, 3.8, 4.5, 5.2, 5.8, 6.5][i]`, `y0 + [-0.2, -0.5, 0, 0.5, 1.1, 1.7, 2.3, 3.0][i]` |

* `sounds/jump.wav` plays at `(x + 1.5, y + 2)` when it starts. Keys are not read until it lands.

In `new3.nw` (decoded with the 2.22 lists): the up ledges are the cliff edge at y = 14 and 15 (x 18 to 46); the left ledges are the two slanted cliff sides, x 14 to 16 and x 48 to 56, between y = 27 and 50. There are no down or right ledges. The push block is at 34,19, the pull block at 31,24, and 42,26 to 43,28 holds a mix of push and pull pieces that neither moves cleanly.

## Pushing

At count 28 (checked before the step is counted, so on the 29th blocked step), and every 20 after, the client tries a push:

1. It fires the trigger action `pushed` at the test point above, with the facing as its parameter. NPCs there get `actionpushed`. Online the 2.05 client also sends it to the server and to its peers.
2. It reads the tile under that point. If it is one of the four tiles of the pushable block (`arrays.dat` array 16, entry 0: 1764, 1765 / 1780, 1781), that tile's place in the block gives the block's top-left. Only that one tile is compared, as in 2.05.
3. The two cells the block moves into must not be a wall, a chest, water, a chair or the lower half of a bed. From the block's top-left: up `(0,-1) (1,-1)`, left `(-1,0) (-1,1)`, down `(0,2) (1,2)`, right `(2,0) (2,1)`.
4. The block moves one tile. Each of its old cells first takes the tile two cells ahead, then the block is written one cell ahead. So the row the block leaves gets the floor that was in front of it.
5. The 2.05 client sends the 4 x 4 area around the old spot as a board modify, moves the player one tile in the facing, and plays `sounds/stonemove.wav`.

### Pushed and pulled NPCs

When no block is found, the same routine looks for an NPC at the probe point.

* **Lookup.** The level's NPC hit test at the point. A character NPC is hit in `x + 0.5 .. x + 2.5`, `y + 1 .. y + 3`; a `setshape2` NPC by its shape's tile types; a GANI NPC by its animation; any other by its image box `[x, x + w/16) x [y, y + h/16)`, where a transparent pixel is a miss for plain image NPCs. The NPC needs `canbepushed` (GS1 command 44, cleared by 45). **[2.05]**
* **Edge.** The NPC is left out of its own test while every point along the edge it moves into is checked, one per tile from its left or top, `t` while `t < x + w` (or `y + h`): up `(t, y - 1)`, left `(x - 1, t)`, down `(t, y + h)`, right `(x + w, t)`. Sizes are in pixels / 16; character and GANI NPCs count as 48 x 48. Each point goes through the client's blocked-point test: other players (online only), blocking NPCs, two level object lists (most likely dropped objects and chests), and wall tiles. Water does not stop an NPC. **[2.05]**
* **Move.** The NPC moves exactly one tile, the player one tile the same way, then `waspushed` fires on the NPC. `actionpushed` has already fired. The routine reports success, so the same sound as for a block plays. A character NPC that crosses a water edge gets the splash and switches between `swim` and `idle`. **[2.05]**
* **Server.** Nothing is sent for the NPC move: the NPC's x and y setters only store the value. The `pushed` trigger action is the only message. **[2.05]**
* 2.22 is the same, but its NPC lookup also searches the neighbouring map parts on a gmap. **[2.22]**

### The trigger action on the wire

The `pushed` / `pulled` try goes to the server as `PLI_TRIGGERACTION` (38): GINT 0 (three spaces, no NPC), `GCHAR x*2`, `GCHAR y*2`, then the action name, and `,` plus the parameter when there is one, the direction as a decimal string (`pushed,0`). 2.05 also sends it to UDP peers (id 26). **[2.05]**

## Grabbing and pulling

* **Order on A**: throw what is carried; lift; grab.
* **Grab test** at `(1.5, 0.9)`, `(0, 2)`, `(1.5, 3.1)`, `(3, 2)` by facing: a wall tile there, or an NPC that blocks. Nothing is grabbed when another player stands there.
* The grab lasts while A is held. Arrow keys do not move the player or turn them.
* **The pull cycle.** Holding the arrow away from the wall sets a counter to 2 and starts the pull pose. Each tick the counter goes 2, 3, ... 19, then back to 2 (18 ticks). Whenever the arrow is held at 19 the client tries a pull. Letting go of any arrow puts the counter back to 1 (just holding).
* **A pull try** fires `pulled` one tile out from the body (`(1.5, 0)`, `(-0.5, 2)`, `(1.5, 4)`, `(3.5, 2)`), with the opposite of the facing as its parameter, then reads the tile at the grab point. If it is a tile of the pullable block (array 16, entry 1: 1998, 1999 / 2014, 2015), the two cells behind the player must be free (from the block's top-left: up `(0,4) (1,4)`, left `(4,0) (4,1)`, down `(0,-3) (1,-3)`, right `(-3,0) (-3,1)`). NPCs with `canbepulled` are moved the same way and get `waspulled`. Then the block moves one tile towards the player (each old cell first takes the tile two cells behind), the player steps back one tile, and `lift.wav` plays (or `lift2.wav`, by a player flag that was not traced).
* **Pulled NPCs.** With no pullable block at the grab point, an NPC there with `canbepulled` (command 46, cleared by 47) is pulled the same way as a pushed one. First the two cells behind the player must be free, from the whole-tile grab cell: up `(0,3) (1,3)`, left `(3,0) (3,1)`, down `(0,-3) (1,-3)`, right `(-3,0) (-3,1)`. Then the edge facing the player is checked: up `(t, y + h)`, left `(x + w, t)`, down `(t, y - 1)`, right `(x - 1, t)`. The NPC and the player move one tile back and `waspulled` fires. Nothing goes to the server for the NPC. **[2.05]**
* **The futile pull.** On anything else (a wall, a rock too heavy for the glove, a push block, the mixed block pieces at 42,26 in `new3.nw`) nothing moves. The `pulled` trigger still fires every 18 ticks, and the pull pose keeps playing.

## Sprites on the wire

From the animation step table (`decomp-findings-2026-10-24/sprite-step-table.tsv`): `push` is steps 14 + frame (S 11, 12, 13, 11, 12), `grab` step 19 (S 14), `pull` steps 20 + frame (S 15, 16, 17). The jump sends no sprite of its own.

## arrays.dat

* **Array 8** holds four lists, one per facing (up, left, down, right): the ledge tiles. This is what tile type 21 ("jumping stone") means in the usual tile mode: the test asks whether the tile is in the list for the player's current facing. In the alternative tile mode (a tiledefs sheet of type 1 or 2) type 21 is instead the tiles in rows 30 and 31, columns 8 to 15, of the 16-column sheet.
* **Array 16** holds two 2 x 2 blocks, `[column][row]`: entry 0 the pushable block (1764, 1780 / 1765, 1781), entry 1 the pullable block (1998, 2014 / 1999, 2015). **[2.22]**

## 2.22 and 2.31

Both behave as 2.05 for everything above: the same counts, probe points, flight curve, block tiles, triggers and pull cycle (the number tables are identical in all three). The differences:

* **Grab on NPCs.** 2.05 grabs a blocking NPC only when a per-NPC flag is clear (most likely the character-shape flag). 2.22 and 2.31 grab any NPC that blocks there, and the lookup also checks the neighbouring map parts. The player and wall checks are unchanged. **[2.22] [2.31]**
* **Stop gates.** Walking, the ledge test, the A key and other gameplay code do nothing while either of two server-set flags is on. Server packets 176 and 177 set them; most likely these are the full-stop packets. **[2.22] [2.31]**
* **Sounds and custom ganis.** `jump.wav`, `stonemove.wav`, the pull sound and footsteps play only while the current gani is one of the built-in names (idle, walk, ..., push, grab, pull). The jump, push and pull still happen with a custom gani; it is expected to bring its own sounds. The sound names are also given bare (`jump.wav`) instead of under `sounds/`. **[2.22] [2.31]**
* **No jump gani** in either version: the flight sets none, so the walk or push gani stays. **[2.22] [2.31]**
* A further flag on the server connection also stops gani changes, footsteps and the A key; what it means was not found. **[2.22]**

## Open

* ~~What is drawn right after A is let go while `pull` is playing.~~ Seen live (2026-10-30, `player-mannerisms-live.md`): `pull` keeps looping until the next key moves the player.
* Releasing A or the arrow mid-pull in 2.22 / 2.31 was not checked step by step.
