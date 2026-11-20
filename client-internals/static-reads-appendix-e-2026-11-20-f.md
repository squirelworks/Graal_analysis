# Static reads for Appendix E, sixth batch (2026-11-20)

Date: 2026-11-20. Evidence: **[bin]** (a decompiler read of the real client executables on the
GwenTea2 lab, plus a linear disassembly of the same files; no client run). Only behaviour is given
here. Covers App. E#308 and E#613, and the throw part of E#323.

Builds read: the original Windows 2.22 `Graal2220.exe` (token `GNW03014`; it differs from the
`Graal_222.exe` copy read in earlier batches in 34 bytes, none in the code paths below) and, for
the comparisons marked, 2.05 rev 2 `Graal.exe`.

## The neighbour-table builder and its skip flags (E#308)

On level entry, and again whenever the big map changes, the client rebuilds the player's 3 x 3
neighbour table:

1. It empties all nine names and all nine loaded-level slots, and clears an "any neighbour named"
   flag.
2. It builds the table only when a map is loaded and both of these hold:
   - the `dontconnectlevels` option (`graalconfig.txt`, → §3.9) is off, **or** the loaded map is
     a gmap (`GRMAP001`);
   - the client is not generating a map image (the "Generate map" command, which also forces
     `dontconnectlevels` on for its run and restores it after), **or** the map has a `HEIGHTMAP`
     block.
3. It looks the current level's name up in the map's level list. If found, the column is the
   index modulo the map width and the row is the index divided by the width. Each of the eight
   cells round it that falls inside the map gets its name; cells off the map stay empty.
4. For each non-empty name it records the level object of that name if one is loaded, and sets the
   "any neighbour named" flag.
5. The centre cell always gets the current level's own name and level.

So the flag that skips the table is the player's `dontconnectlevels` option. A gmap ignores it.
2.05 rev 2 has the same builder, guarded by the same option alone (2.05 has no gmap or
map-generation override).

A second routine runs after the builder. It loads each named neighbour that is not loaded yet:
offline, from the level file; online, as an empty level marked "requested", for which it sends
`PLI_ADJACENTLEVEL` (35). Levels that left the 3 x 3 window get their NPCs' and timers' leave
calls; levels that entered get their enter calls.

### Cell coordinates on a gmap

When the player enters a level that is in the loaded gmap's list, the player records the gmap
and copies the level's cell (column and row in the gmap) as its own cell coordinates; on any other
level they are cleared. While that gmap link is set, the link routine works differently:

- It does not use the per-facing probe or the four big-map edge links.
- Each tick it takes the player's raw position. On each axis the cell offset is -1 below 0, +1 at
  64 or more, and 0 otherwise.
- For a diagonal step whose corner neighbour is not loaded, it falls back to the vertical
  neighbour if that is loaded, else to the horizontal one.
- If that neighbour is loaded it switches to it, with x and y shifted by 64 per cell crossed.
  In play mode 2 (a value the client keeps scrambled; what each value means was not traced), when
  the neighbour's name is not in the gmap's list, it instead marks the game for a reload and stays.
- In play mode 2 with no neighbour named at all, the whole link routine returns at once, before
  the ordinary links are tested.

### `PLO_BIGMAP` (171) and the GS1 `setmap` command

- 171 is read as text, image, x and y. 172 (`PLO_MINIMAP`) goes to the minimap twin of the same
  routine. GS1 `setmap` calls the same routine with its four arguments.
- If the text file is present locally: online it is checked for an update with the server, the
  current big-map file name and image name are replaced by the message's, x and y are stored
  times 64, and the big-map loader runs.
- If it is not present: online, the client asks the server for it unless it is already the
  current big-map file. Nothing else changes, so the new grid takes effect only on a later 171,
  or on the file's arrival if its name is already the current one.
- The loader is the same one that loads `bigmap.txt` at start-up and on a reset (both names are
  defaults: `bigmap.txt` and `map.png`). It skips the load when the current map already has that
  name. In play mode 0, with a player in a level, it then re-runs the gmap check, the neighbour builder
  and the neighbour loader.

So 171 installs a grid through exactly the path `bigmap.txt` uses; only the file name differs.

## The 2.22 player roster and private messages (E#613)

### No roster request

- The connection object has one send routine per client-to-server id. In 2.22 they cover ids 1
  to 24, 26 to 30, 32 to 39, 41, 43 to 45, 80 and 81. None asks the server for a player list.
- The roster is the client's own player collection, filled only by `PLO_OTHERPLPROPS` (8). An 8
  for an unknown id creates the player, whatever its level, adds it to the collection and to the
  player-list window, and logs "Added player name (id: n)". A player whose props mark it as gone
  is logged "Removed player" and freed.
- When the collection grows past 8 players while the server's `PLO_SIGNATURE` (25) value is 0,
  the client shows "Server error: There are too many players online." and quits. Any other
  signature value lifts the cap.
- 55, 56 and 82 have no handler in the original 2.22 either; they take the default exit.

### What a received PM (37) does

- The sender id is two base-128 digits. A sender that is not in the collection is dropped; 37
  never creates a player.
- A body that starts with `"` is split at the first `",`. The quoted part is kept as the
  message's prefix (`"Mass message:"` and `"Guild message:"` are the two the client ranks; see
  below) and the rest is the text.
- A body equal to `"Your messages are ignored."` only marks the sender as ignoring us and redraws
  their player-list row.
- If we ignore the sender, the client answers at once with a PM to that one sender whose text is
  `"Your messages are ignored."`, and keeps nothing.
- Otherwise the text is written to the PM log (`pms\messages_<account>.txt`, unless
  `dontsavepms` is on), appended to the sender's pending text (lines joined by a line break), the
  prefix is kept, the arrival time is stamped, and the sender's row in the player list is redrawn.
  No window opens at arrival.
- Clicking players on the board picks one to open. The order is: an ordinary pending PM first,
  then a guild message, then a mass message, then a player with a second kind of pending entry. A
  player with a pending PM opens its message window.

### Not covered

- The look of the pending-message marker on the board and in the list, and the window's layout.
  One lab run with two players would show both.
- The virtual send behind type 28 is the ordinary send routine of the connection; its framing is
  that of every other PLI and was not re-read here.

## The 2.22 throw (E#323)

### Sending

- The throw creates a flying object (below), clears the carried flag, the carried NPC and the
  carried bomb, and sets the carry sprite back to -1.
- Online it then sends UDP id 18 (throw carried) with an empty body to the peers. It also sends
  `PLI_THROWCARRIED` (11), empty, over TCP whenever a TCP copy is needed: UDP is off, the client
  has no UDP port, or some player in the level has none. With UDP working and nobody else in the
  level, only the UDP message goes out.
- This is the only sender of TCP 11 in 2.22. The routine that sends x times 2 plus 32 and y times 2
  plus 32 when a laid bomb is picked up, grabbed or removed by a script sends UDP id 11 (bomb del)
  and, as its TCP copy, `PLI_BOMBDEL` (5).

### Flight

- Start: x = player x + 0.5; the drawn y = player y - 1.375; the shadow y = player y + 1. It flies
  in the player's facing for 9 ticks.
- Each tick it moves by a fixed step per facing, in tiles:

  | Facing | x | drawn y | shadow y |
  | --- | ---: | ---: | ---: |
  | up | 0 | -0.8 | -1.0 |
  | left | -1.0 | +0.2 | 0 |
  | down | 0 | +1.2 | +1.0 |
  | right | +1.0 | +0.2 | 0 |

  So it travels 1 tile per tick along the throw and sinks 0.2 tile per tick towards its shadow.
  The same 12-number table is in 2.05 rev 2.
- Past a level edge (x at or below -1 going left, y at or below -1 going up, 63 or more going right
  or down) it moves into the loaded neighbour on that side, shifted by 64, and keeps flying. A
  thrown NPC does not cross.

### What it hits

Each tick it tests the point (x + 1, shadow y + 1), in this order, and stops at the first hit:

1. A wall at that point.
2. An NPC there. For a thrown object the NPC's "pelted with" text is set to `bush`, `sign`,
   `vase`, `stone` or `blackstone` by the carry sprite (261, 267, 265, 263, 239), or `npc` for a
   thrown NPC, and the NPC gets `waspelt` if it has that event.
3. Each baddy of the level, hit with power 3, or 1 for a bush, a thrown NPC or a bomb.
4. The local player, when it is the thrower's level, the player can be hurt, the object is not
   the player's own, and |x - (player x + 0.5)| < 2 and |shadow y - (player y + 1)| < 2. The
   damage is one heart, or half a heart when the player has exactly one heart left; knockback is
   one tile along the throw. Online, the owner rules of §4.3 apply.

### Landing

It lands at the first hit or when the 9 ticks run out:

- On water: a splash (break effect 5, `water.wav`).
- Otherwise: a break effect at (x, shadow y) with `crush.wav`. The kind is 0 for a bush (leaves),
  3 for a sign, and 2 for everything else.
- A carried bomb is put back down where it lands instead (drawn y + 0.75), keeps its owner, and is
  sent as `PLI_BOMBADD` (4); no break effect.
- A thrown NPC is put down at the landing point (with its image offset taken into account) and
  gets `wasthrown`; it breaks only on water.
- The landing never changes the board.

### What a cut or lift drops

The 2.22 cut and lift routines do not call the random generator and do not add an item. As in
2.05, every drop from a bush or pot is the server's (→ §4.5.5). The client's own item-add path is
used only by chests, scripts, laying an item down and the server's `PLO_ITEMADD` (22).

### Not covered

- The live distance: the code gives 9 tiles along the throw before the timer runs out, while the
  2.05 live note measured about 6 tiles. A frame-by-frame lab throw on 2.22 in open ground would
  settle which is seen.
- The other open parts of E#323: the carrying pose, the chest and sign probe points, the glove
  value the server sends, snapping after a step, and the swim and carry speed factors.
