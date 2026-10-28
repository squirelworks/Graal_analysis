# Tile type tests (2.05 rev 2)

Date: 2026-10-28. From the client's per-type test, its wall test, the
`arrays.dat` loader and the script expression handler (derived).

## Which rule applies

Each level picks its tileset from the tile definitions (`addtiledef`).
The type of the chosen definition decides how tile types are answered:

- **0, the default** (`pics1.png`): from the `arrays.dat` lists.
- **1 and 2, the new kind**: from the tile id alone, by a fixed rule.
- **5**: no board rule. Only NPC shapes have types.

An NPC shape that the player stands on (`setshape2` with tile types)
answers first, for every tileset.

## The default tileset

No 4096-entry type table is built. Each question asks one list, and
looking up a tile is a binary search of a sorted list:

| question | list |
|---|---|
| wall | not in array 0 (passable) and not in array 1 (liquid) |
| 3 chair | array 4 |
| 4 bed top | array 5 |
| 5 bed bottom | array 6 |
| 11 water | array 1 |
| 12 lava | array 3 |
| 20 throw-through | array 2 |
| 21 jumping stone | array 8: four lists, one picked by the object's direction |

Any other type number is answered only by NPC shapes, so a board tile is
never type 0, 2 or 6 to 10 in this tileset.

Array 7 is not a type list. A tile's position in it (0–11, 12–19, 20–62,
63 and up) gives one of four ground classes, the same four that shape types
6 to 9 give. The horse uses the class to pick the sprite drawn under it.

Off the board, the tile reads as id 632. The wall test checks bounds first
and calls off-board a wall. The type tests skip the bounds check and look
up 632, which is in no list in the 2.22 file.

Consequences:

- **Lava passes the water test.** The liquid list holds lava too, so
  `onwater` and the swim test are both true on lava. A separate lava test
  counts ticks on lava. When the count passes 100, the client calls what
  looks like the hurt routine, and the count resets. Reading that call as
  the hurt routine is **inferred**.
- **The lava test in detail.** Once per player tick the client tests one
  point, the player's position plus (1.5, 2), against the lava list
  (array 3) only. On lava a counter goes up. On the 101st tick in a row it
  calls the hurt routine with -0.5 (half a heart) and a flag that skips the
  usual "can be hurt" checks, then sets the counter to 0. A tick off lava
  sets it to 0. Which of the two offsets belongs to x was read from the
  order of two property reads, so (1.5, 2) rather than (2, 1.5) is
  **inferred**. The tick length was not read here.
- **A tile can be in several lists.** In the 2.22 file, 6 of the 133
  throw-through tiles are passable, and 9 of the 76 lava tiles are not in
  the liquid list. All 9 are in the passable list, so they are walked on,
  not swum in, and the lava test still burns on them. (An earlier version
  of this note called them walls.)
- **Deep water is in no list.** A level made for testing (2026-10-28) uses
  a dark water tile for deep water. In the 2.22 file that tile is in none of
  arrays 0 to 3, so the wall test calls it a wall: deep water blocks.
  Shallow water in the same level is in the passable list only, so it is
  walked on.
- A thrown object is stopped by a tile that is not type 20 and that the
  wall test calls a wall.

## Tilesets of the new kind

With `row = id / 16` and `col = id % 16`, a tile is a **wall** if any of
these holds:

- id 32
- row 26 or 27 and col 2 or more
- row 30 to 47, 84 to 95, or 116 to 127
- row 128 or more and `(row / 16)` odd

A wall tile is 20 if its id is 512 to 767, 21 if it is in row 30 or 31 with
col 8 or more, and 22 otherwise.

A tile that is not a wall is checked in this order, and the first match
wins:

1. 288–319 gives 2
2. 320–383 gives 3
3. 384–399 gives 4
4. 400–415 gives 5
5. 64–287 gives 11
6. 192–287 gives 12. This step can never be reached, because step 5 has
   already taken those ids.
7. row 26 or 27 with col 0 or 1, or 768–799, gives 6
8. 800–831 gives 7
9. 832–911 gives 8
10. 912–943 gives 9
11. 944–991 gives 10
12. anything else gives 0

## Script functions

- `tiletype(x, y)` returns -1 unless the level's tileset is of type 1, 2
  or 5. For type 5 it always returns 1. Otherwise it applies the rule
  above (an NPC shape's type wins when it is above 1). On the default
  tileset, scripts therefore always get -1.
- `onwall(x, y)` is the wall test.
- `onwater(x, y)` is the type 11 test, true on lava as well.

The 2.00 to 2.04 builds all carry the three names. Their code was not
compared.
