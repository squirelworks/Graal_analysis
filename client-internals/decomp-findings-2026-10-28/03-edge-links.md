# Edge links and the big map

Date: 2026-10-28. From the 2.05 client (derived). 2.22 and 2.31 not read.
Not checked against a running client.

## The level's neighbours

When a level is entered, the client fills a 3 x 3 table of level names
around it from the big map: the text grid of quoted level names that the
map screen uses (`maps/bigmap.txt` style, one row per line). It finds the
current level's name in the grid and copies the eight names around it;
cells off the grid stay empty. This happens only while a big map is
loaded, and is skipped under one global flag (not identified; it may be
the gmap or editor state). For each non-empty neighbour name the client
also looks up a loaded level object of that name; that slot stays empty
when the level is not loaded.

So the big map is not only a picture for the client: it decides which
levels are "next to" the current one.

## Following a link

Each tick the client takes a probe point: the player's position plus a
per-facing offset. Then for each link of the level, in order:

1. **West edge link**: the link's x is 0, its width is 1, and its
   destination is the west neighbour's name (exact text compare). It fires
   when the probe x is 0 or less while facing left, or the player x is
   below -2.5, or, when the west neighbour level is **not** loaded, when the
   probe is inside the link's rectangle. Arrival: **x = player x + 64**, y
   unchanged. The link's own new-x/new-y are not used.
2. **East edge link**: x 63, width 1, destination = east neighbour. Fires
   when the probe x is 64 or more while facing right, or the player x is
   above 63.5, or (east neighbour not loaded) the probe is in the
   rectangle. Arrival: **x = player x - 64**, y unchanged.
3. **North edge link**: y 0, height 1, destination = north neighbour.
   Probe y 0 or less facing up, or player y below -3.0, or (not loaded) in
   the rectangle. Arrival: **y = player y + 64**, x unchanged.
4. **South edge link**: y 63, height 1, destination = south neighbour.
   Probe y 64 or more facing down, or player y above 63.0, or (not loaded)
   in the rectangle. Arrival: **y = player y - 64**, x unchanged.
5. **Any other link** (including an edge link whose destination is not the
   neighbour on that side): it fires when the probe is in the rectangle,
   except that a probe within 1 tile of an edge (x or y at most 1, or at
   least 63) only counts while the player faces out across that edge. The arrival coordinates are the
   link's new-x and new-y, evaluated as expressions (`playerx` /
   `playery` give the player's current coordinate).

The first link that fires is taken; offline the client loads the level,
online it asks the server.

So an edge link between two levels that sit side by side on the big map
keeps the player's exact offset across the seam (east off x 63.6 arrives at
x -0.4), whatever the link's new-x says. Without a big map, or for a level
that is not the big-map neighbour, the link's own coordinates are used, and
`playerx` on an east-edge link then arrives on the east edge of the
destination.

## Link records (for reference)

* A link line has the destination, x, y, width, height, and optionally
  new-x and new-y. A missing new-x or new-y, or one that is `-1`, means
  `playerx` / `playery`.
* The level editor's default for a new link on an edge: on the east edge
  (x 63) new-x is `0`; on the south edge (y 63) new-y is `0`; on the west
  edge (x 0, width 1) new-x is `61`; on the north edge (y 0, height 1)
  new-y is `61`. The other coordinate stays `playerx` / `playery`.

## Open

* The probe offsets per facing were not read.
* The flag that turns the neighbour table off was not identified.
* Which big map a 2.05 client uses offline, and whether 2.22 does the same
  with the `PLO_BIGMAP` (171) map, is not read.
* How walking behaves past the edge when the neighbour level is loaded
  (the player x can go below 0 or above 63.5 before the link fires), and
  whether the neighbour's tiles are tested there, is not read.
