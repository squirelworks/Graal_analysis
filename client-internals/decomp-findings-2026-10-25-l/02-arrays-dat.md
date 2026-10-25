# arrays.dat: layout and meaning

Date: 2026-10-25. From the client's loader and its uses (derived).

## Layout

A run of arrays to the end of the file (the 2.22 file: 11,500 bytes, 25
arrays). Each array starts with a big-endian `u32` header:

* low 16 bits: the count `n`;
* high 16 bits: 0 = `n` big-endian `u32` ints follow; non-zero = `n` nested
  arrays follow, each with its own header.

The 2.22 file parses completely this way with no bytes left over. Counts of
the 25 arrays: 934, 116, 133, 76, 40, 4, 4, 79, 4, 2, 2, 5, 5, 4, 2, 2, 2, 124,
8, 6, 32, 4, 5, 4, 356.

## Arrays (index = position in the file)

| index | what | shape |
|---|---|---|
| 0 | passable tile ids (`nowall`); any other tile is a wall | flat |
| 1 | liquid tile ids (water and lava) | flat |
| 3 | lava tile ids (liquids that are lava) | flat |
| 9 | cuttable 2 x 2 objects | nested: type -> column -> row |
| 10 | the 2 x 2 tiles a cut leaves | same shape, same order |
| 11 | liftable 2 x 2 objects | nested |
| 12 | the 2 x 2 tiles a lift leaves | nested |
| 13 | closed chest tiles (1784 1785 1800 1801) | flat |
| 14 | open chest tiles (829 845 / 830 846) | nested |

Others (2, 4 to 8, 15 to 24) are not read here; several hold per-tile lookups
the client uses for drawing and sounds.

Objects are indexed `[column][row]`. The 2.22 tables: 2 cut types (the bush
`2 3 / 18 19` and `420 421 / 436 437`, leaving `677 678 / 693 694` and
`679 680 / 695 696`), and 5 lift types (the bush, a 512 block, a 684 block,
the rock `34 35 / 50 51`, a 990 block) leaving `677 678 / 693 694`,
`1802 1803 / 1818 1819`, `1770 1771 / 1786 1787`, and `1834 1835 / 1850 1851`
twice.

Note: reading only the first four arrays as flat int lists (as a first
loader did) is right for 0 to 3 and ignores everything else; arrays 9 to 12
need the nested reading.
