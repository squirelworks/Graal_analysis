# Static reads for Appendix E, fifth batch (2026-11-20)

Date: 2026-11-20. Evidence: **[bin]** (a disassembler read of the real client executables on the
Mirae lab, with no client run). Only behaviour is given here. Covers App. E#323 in part.

Build read: the real Windows 2.22 `Graal_222.exe`.

## What 2.22 sends as id 11 (E#323)

- The body of client-to-server id 11 is two bytes: the object's x times 2 plus 32, and its y times
  2 plus 32. There is no object kind and no direction.
- 11 is sent only when a carried object already lying in the level leaves the level's list of
  landed objects. There are exactly three senders:
  1. The player picks it up through a probe point inside the object's box, from x-1 to x+3 and
     y-1 to y+3. The player's carry state becomes 3 and the carried image is taken from the object.
  2. The player grabs it through a second probe pass, over the box x to x+2 and y to y+2. The
     object is kept as the player's grabbed object and its lying flag is cleared.
  3. A script removes it by index.
- None of the three runs at the moment of the throw.
- So on 2.22, 11 announces "the landed object at (x, y) is gone". It is not a throw message. That
  differs from 5.00r7, where a lab throw recorded 11 being sent when throwing (→ §2.4.2).

## Not covered by this read

- The throw itself: flight, landing, and what is dropped on a cut or lift.
- E#308's neighbour-table builder. All that was seen is that each tick the client updates its 3x3
  neighbour levels in a loop, and that one player flag changes how each cell's coordinates are set.
- E#613.
