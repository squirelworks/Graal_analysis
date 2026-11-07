# Respawn destination: the level-entry save

The respawn moves the player to the *saved entry point* (level, x, y, direction). This note is about when the client saves it.

## The decision, run after every level entry
Inputs: the name of the level just left (empty at login), the new level's name, and the current gmap's level list (a string list; -1 when a name is not in it or there is no gmap).
1. Level left is empty: save.
2. Compute index(new) * index(old). If it is negative: save. So exactly one of the two is in the list and at an index of 1 or more; an index of 0 gives a product of 0, so the first list entry behaves like "not in the list" (the client's quirk).
3. 2.00 to 2.05: otherwise, compare the name groups. Different groups: save. Same group: do not save.
4. 2.17.1, 2.22, 2.31: otherwise do not save (no group test).

Saving stores the new level's name and the player's current x and y, direction as it is.

## The name group (2.00 to 2.05)
Take the level name, drop everything up to the last path delimiter, lower-case it, then take the text up to and including the last `§` (byte 0xA7) or `$`. If there is neither, the group is empty, and two empty groups are equal. The extension stays in the name.

Effect: two plain names such as `a.nw` and `b.nw` are always the same group. The test only separates names that use the delimiters.

## Which builds have the group test
Read in the code, step by step, for all eleven 2.00 to 2.04 builds: 2.00 and its revisions 1 to 3, 2.01 and rev1, 2.02, rev1 and rev2, 2.03, 2.04. Each has the same decision as 2.05 rev2, in the same order: the empty-name test, the product of the two list indices, then the name-group test, then the save. The name-group routine is the same instruction for instruction in all eleven builds and in 2.05 rev2. (Confirmed, from the machine code.)

One difference: 2.05 returns -1 for both indices when there is no current gmap. In 2.00 to 2.04 the list is taken straight from the client's state with no such test. Whether that list is simply empty when there is no gmap, which would give the same -1, was not traced. (Inferred, not tested.)

2.17.1, 2.22 and 2.31 have no group test. The 2.1 test builds 2 and 3 do not contain the delimiter-set constant, so they are expected to have none; their code was not read. A scan of the build files for that constant finds it in 1.37 to 1.41, 2.00 to 2.05, NewMain 24 and 26 and NewWorld beta 1. Builds before 2.00 were not read. See name-group-constant-by-build.tsv.

## After the respawn
The respawn routine moves the player (same-level shortcut or a level change), then calls the same save routine once more, unconditionally. If the warp completed in the same call, this stores the respawn point itself. If an online level change finishes later, the stored point could be the spot where the player died. Not resolved.

## Open
See 03.
