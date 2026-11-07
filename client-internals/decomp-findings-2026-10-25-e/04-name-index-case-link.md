# File-name index, case fold, and the packet 40 link

Static read of the 2.05 rev 2 and 2.22 clients. No capture and no client was run. **[bin]**

## Case fold

File names are folded with the plain A–Z fold: each byte from `A` to `Z` is turned into `a` to `z`, and every other byte is left as it is. Accented letters are not folded, so they do not match across case.

The file-name index stores that folded base name (the part after the last `\` or `:`). A lookup folds the same way and then compares the bytes exactly. The runtime also has a locale compare, used by ordinary sorted string lists; the file-name index does not use it.

The same A–Z fold is applied before the folder tests (`head`, `body`, `sword`, `shield`, `hat` plus a digit, the `.code` skip, and the `pms` / `profiles` / `weblevels` skip below). **[bin]**

## Which copy is used

Folder names do not decide the winner. The same base name in two folders is decided as follows.

Both builds, before the index: if a file of that name exists in the current directory, that file is used.

- 2.22 sets the current directory to the game folder at startup, so a copy in the game folder itself beats either subfolder.
- 2.05 rev 2 sets the current directory to the game folder's `levels` directory, so a copy placed directly in `levels` beats `levels/bodies` and `levels/webgifs`. Opening a world can point the current directory at that world instead.

**2.22.** At startup the client walks the game folder and fills a name-to-path index.

- In each directory the files are recorded in the order the directory listing returns them, and only then are subdirectories entered, in that same order.
- A directory whose parent is the game folder and whose folded name is `pms`, `profiles` or `weblevels` is not entered. A file whose folded extension is `.code` is not recorded.
- The key is the folded base name. The stored path is kept with the last-write time from the directory listing. A later time replaces the path. An equal or earlier time leaves the path already stored, which is the one the walk met first.

**2.05 rev 2.** A full-folder indexer with the same skip rules is in the program (it would keep the first name and ignore a later duplicate), but no call site in this image references it. What runs is the lookup:

1. The name as a file in the current directory, as above.
2. Else a path remembered from an earlier lookup, if that file is still there.
3. Else a depth-first search, first of an extra root recorded when a world file is opened, then of the game folder. In a directory, a file of the wanted name is taken before any subdirectory is entered. Subdirectories are tried in directory-listing order, and the search stops at the first hit. The same three folders and `.code` files are skipped. The hit is remembered for the next lookup.

So for two different bytes under the same name, 2.22 draws the newer file, and 2.05 rev 2 draws the first file the search meets. **[bin]**

## Packet 40 link

Packet 40 (and the same test on the longer hit form) is dropped unless one integer on the attacker's record equals the same integer on the victim. A new player is created with that integer 0, so two ordinary players pass.

The horse is a different slot. Setting or clearing the horse image does not write the integer. A player who only has a horse still carries 0 and still matches another ordinary player. **[bin]**

In 2.22 the integer is the layer/parent link:

- It stays 0 until a `layer` property is applied. The value is then the layer number minus one. If that character has a parent, the parent's link is added as well.
- A spawned follower copies the source's link, or one more than the source's link. That is the follower's own link, not the player's. The player's link is unchanged by the spawn.

2.05 rev 2 has the same equality test and the same zero at creation, and its horse image is likewise a different slot. It has no `layer` property string. **[bin]**
