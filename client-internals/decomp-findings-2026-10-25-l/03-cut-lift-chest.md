# Sword cut, lift, and chests

Date: 2026-10-25. From the 2.05 client (derived).

## Matching a 2 x 2 object

Take the tile under the probe point. For each table entry in order, for each
of its four tiles equal to that tile, the object's top-left is the point
minus that tile's column and row. The four board tiles there must equal the
entry's four, all on the board. First full match wins.

## Sword cut

At the start of a sword swing, at the A-key probe point: match against the
cut table (all entries, no glove). On a match the four tiles are replaced by
the entry's "left" tiles (array 10) through the routine that also writes board
changes the server relays, then a routine that takes the entry index spawns
debris or items (not read).

## Lift (A key)

First action of the A key (checked before pulling a block). Glove power `g` allows the first `g + 2` lift entries:
a bare hand the first two (bush, 512 block), power 1 adds the 684 block,
power 2 the rock and the 990 block. A match replaces the four tiles with the
entry's "left" tiles (array 12) and the player carries an object. The throw,
its flight and landing, and the carrying pose were not read.

## Chests

The open actions below are what the Seihai client does after its reading of the
2.05 client; only the lift and cut probes were read in detail.

* By board tile: if the tile at the A-key probe is one of the closed chest
  tiles (1800/1801 bottom row), it is replaced by the open chest 2 x 2 and
  PLI_OPENCHEST is sent.
* By record: a `PLO_LEVELCHEST` record at the probe, not yet opened: it is set opened, the item is spawned, PLI_OPENCHEST is sent, and
  the sign the record names is shown.
* A chest record has **no draw code**. A chest looks like its board tiles
  and nothing else. The record adds the open action and a 2 x 2 solid
  footprint (opened or not).
* Record bytes (each plus 32): opened flag, x, y, and, only if not opened,
  item index and sign index. The item index names an entry of the client's
  built-in chest item list (the list was not read here).

## A-key order

Lift is tried first, then grab (pull a block). Where reading a sign and opening a chest sit in that order was not read.

## Sword while carrying

See `../decomp-findings-2026-10-28/01-sword-while-carrying.md`: with an
object carried, the sword key throws it instead of swinging.
