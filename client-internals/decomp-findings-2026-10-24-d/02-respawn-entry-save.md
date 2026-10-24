# Respawn destination: the level-entry save

The respawn moves the player to the *saved entry point* (level, x, y, direction). This note is about when the client saves it.

## The decision, run after every level entry
Inputs: the name of the level just left (empty at login), the new level's name, and the current gmap's level list (a string list; -1 when a name is not in it or there is no gmap).
1. Level left is empty: save.
2. Compute index(new) * index(old). If it is negative: save. So exactly one of the two is in the list and at an index of 1 or more; an index of 0 gives a product of 0, so the first list entry behaves like "not in the list" (the client's quirk).
3. 2.05 only: otherwise, compare the name groups. Different groups: save. Same group: do not save.
4. 2.17.1, 2.22, 2.31: otherwise do not save (no group test).

Saving stores the new level's name and the player's current x and y, direction as it is.

## The name group (2.05)
Take the level name, drop everything up to the last path delimiter, lower-case it, then take the text up to and including the last `§` (byte 0xA7) or `$`. If there is neither, the group is empty, and two empty groups are equal. The extension stays in the name.

Effect: two plain names such as `a.nw` and `b.nw` are always the same group. The test only separates names that use the delimiters.

## Which builds have the group test
Only the 2.05 builds were read for the test itself. A scan of the build files for the delimiter-set constant finds it in 1.37 to 1.41, 2.00 (all revisions) to 2.05, NewMain 24 and 26 and NewWorld beta 1, and not in 2.1 test 2 and 3, 2.17.1, 2.22, 2.31 and NewWorld beta 2. The constant being present before 2.05 does not show that the save rule is the same there; it was not read. See name-group-constant-by-build.tsv.

## After the respawn
The respawn routine moves the player (same-level shortcut or a level change), then calls the same save routine once more, unconditionally. If the warp completed in the same call, this stores the respawn point itself. If an online level change finishes later, the stored point could be the spot where the player died. Not resolved.

## Open
See 03.
