# Where the 3.04 client gets its tile types

Date: 2026-11-12. This is a static read of the Linux 3.04 `graalexe`, UPX-unpacked; its digest matches the one in the v3 findings. The 2.22 `arrays.dat` (11,500 bytes) was compared value by value. Nothing was run. Evidence ID: `T304-TILETYPES-20261112`. Tags as in [README.md](README.md).

## Short answer

3.04 has no `arrays.dat`, and no tile-type file or packet. The tile lists the 2.x clients read from `arrays.dat` are **compiled into the executable** as sorted lists of tile ids, and the walk test searches them directly. **[bin]**

The rule a tile is judged by depends on the sheet type that `tiledefs` picks for the level:
- with the classic `pics1.png` and type 0, it is the lists;
- with type 1 or 2, it is a fixed id-range rule.

The server can change the sheet through `tiledefs`. It does not send tile types. **[bin]**

## The compiled-in lists

Each list is a sorted array of `pics1` tile ids (0–4095). A tile is found in one by binary search. **[bin]**

| List | Count | Used as | Same as in 2.22 `arrays.dat` |
| --- | --- | --- | --- |
| A | 934 | the walkable list (see the walk test) | array 0, identical |
| B | 114 | water (type 11), and also walkable | array 1, **minus ids 1824 and 1825** (2.22 has 116) |
| C | 133 | type 20 | array 2, identical |
| D | 76 | type 12 | array 3, identical |
| E | 40 | type 3 | array 4, identical |
| F | 4 | type 4 (ids 708–711) | array 5, identical |
| G | 4 | type 5 (ids 724–727) | array 6, identical |
| H | 4 facings × 6 slots, −1 = unused | type 21 (ledges), by the player's facing | array 8, identical, padded to 6 per facing |

**[bin]** for the counts and the uses; **[file]** for the comparison with the 2.22 file. A rebuild can therefore take the 3.04 tables from the 2.22 `arrays.dat`, apart from the two water ids.

## The walk test (`onwall` and movement)

1. **Finding the tile id.** A position on the current level reads the board's tile id. On a gmap, the position is first mapped to the level under it. A position off the board, or with no level, uses a stand-in id: **632** on a type-0 sheet, **0** on any other. Id 632 is in neither list, so off-board counts as wall on the classic sheet. **[bin]**
2. **Sheet type 0** (the default `pics1.png`). The tile is walkable **only if its id is in list A or in list B**. Any other id blocks. There is no per-tile type number here: an id absent from both lists is a wall, whatever it looks like. **[bin]**
3. **Sheet types 1 and 2** (for example the offline tutorial's `picso.png`, type 1). There are no lists; the tile is judged by its id. With `row = id / 16` and `col = id % 16`, the tile **blocks** when any of these holds; otherwise it is walkable: **[bin]**
   - `id == 32`;
   - `row` is 26 or 27 and `col ≥ 2`;
   - `row` is in 30–47, 84–95 or 116–127;
   - `row ≥ 128` and `row & 16` is non-zero.
4. **Gmap override.** When the level (or the gmap it belongs to) has a particular flag set, "blocked" means "no level at that position" instead of the tile rule. **[bin]** What sets that flag was not traced.

NPC and object shapes (`setshape2`) are tested before the board. A shape cell whose value is ≥ 20 blocks. **[bin]**

## Type tests

The engine test "is this tile of type N" (water, ledges, the script checks) works as follows. **[bin]**

| N | Sheet type 0 | Sheet types 1, 2 |
| --- | --- | --- |
| 3 | in list E | id 320–383 |
| 4 | in list F | id 384–399 |
| 5 | in list G | id 400–415 |
| 11 (water) | in list B | id 64–287 |
| 12 | in list D | id 192–287 |
| 20 | in list C | id 512–767 |
| 21 (ledge) | in list H for the player's facing | `col ≥ 8` and `row` 30–31 |

If a type test fails, or N is any other number, the engine falls back to the level's objects at that spot. The separate "on water" test is list B on a type-0 sheet and id 64–287 on types 1 and 2. **[bin]**

## How the sheet type is chosen

- **Loading.** `tiles.cpp` loads `tiledefs/tiledefs<name>.txt`, where `<name>` is the current server name or `Offline`. In the package that folder is under `levels/`. It logs `Loading tile definitions for server <name>.` or `… for offline mode.`. **[bin]**
- **Entries.** Each line is `image,levelprefix,type[,x,y]`. **[bin]**
- **Script commands.** The script verbs `addtiledef`, `addtiledef2` and `removetiledefs` add and remove entries at run time. **[bin]**
- **Picking an entry.** On entering a level, the client takes the entry of type 0, 1, 2 or 5 whose level prefix matches the level name. The longest prefix wins. With no match it uses `pics1.png`, type 0. Type 5 sets a flag of its own. **[bin]**
- **What ships.** The 3.04 Linux package ships only `tiledefsOffline.txt`, with one line: `picso.png,offlinetutorial,1,0,0`. So the offline tutorial levels use the type-1 range rule, and every other level uses `pics1.png` with the lists. **[file]**

## What this means for the rebuild

- **The grass-as-wall symptom.** The tables are not missing in 3.04; they are in the executable, and they equal 2.22's. A rebuild that treats 3.04 grass as wall is probably applying a rule other than "walkable iff in list A or list B". **[inf]** Three likely causes:
  - it uses a per-tile type table in place of the two lists;
  - it uses the type-1/2 range rule on a `pics1` level;
  - it reads tile ids from the wrong board, for example from a gmap without the level offset.
- **Checks to make:**
  - the selected sheet type for the level;
  - that board tile ids are looked up in lists A and B from `arrays.dat` arrays 0 and 1;
  - that off-board positions use id 632.
- **Water.** Drop ids 1824 and 1825 from the water list for 3.04 parity. **[file][bin]**

## Not settled

- [ ] What the type-5 flag changes when drawing or walking.
- [ ] Whether a 3.04 game server sends `addtiledef` lines at login; no 3.04-era server capture was checked for them.
