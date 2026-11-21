# Static reads for Appendix E, third batch (2026-11-20)

Date: 2026-11-20. Evidence: **[bin]** (a disassembler read of the real client executables on the
lab host B, with no client run). Only behaviour is given here. Covers App. E#303, E#317 and E#603.

Builds read: 2.05 rev 2 `Graal.exe` and 1.39.

## The two lists in the 2.05 blocked-point test (E#303)

The blocked-point test tries, in order, the first list, the level's NPCs, the second list, the
chests and then the tile.

**The second list (1.5 × 2 boxes with an enabled flag) holds the level's bombs.**

- Only two places add to it.
- The first creates a bomb object, sets its position, type and power, sets the enabled flag, adds it
  and plays `put.wav`. That is placing a bomb.
- The second takes the object the player is carrying, sets its level and its position (the
  carrier's, 0.75 tile lower), sets the enabled flag and adds it. Online, it also sends the bomb to
  the server. That is putting down a carried bomb.
- So a bomb lying in the level blocks walking over x + 0.25 to x + 1.75, y to y + 2.

**The first list (player-sized boxes with two flags) is the level's list of players.**

- It is the list that the level-change code moves a player object out of and into.
- Its test box is x + 0.5 to x + 2.5, y + 1 to y + 3, a player's body. A player with either of two
  state flags set is skipped.
- The test runs only when three things hold: a global "test players too" flag is set, the client is
  online, and a level condition is false.
- That flag is not a user option. A few movement routines set it just around their own probe calls,
  and the ordinary walking step clears it after its probes. So normal walking does not collide with
  other players. Only those few routines do, and which moves they are was not traced.

## The 1.39 pickup test (E#317)

- 1.39 tests a pickup as an overlap of two boxes, measured in eighths of a tile and rounded to whole
  eighths.
- The player's box is 2 × 2 tiles, from x + 0.5 to x + 2.5 and from y + 1 to y + 3. That is the same
  body box the 2.05 walking test uses.
- The item's box is centred across x + 1 and starts one eighth of a tile below y. Its width and height
  come from the item sprite's stored size. Whether that size is in eighths of a tile or in sprite
  pixels was not confirmed, so the item box's size in tiles is still open. (Settled later: eighths of
  a tile; see [static-reads-appendix-e-2026-11-20-g.md](static-reads-appendix-e-2026-11-20-g.md#the-139-item-box-and-its-unit-e317).)
- The overlap is strict on all four sides. When it holds, the client looks the item kind up in its 25-entry table; online
  it sends `PLI_ITEMTAKE` (32) with the position and the item. The offline branch was not followed.
- The draw order of items against players was not read.

## Whole tiles and fractions in 2.05 binary level records (E#603)

The 2.05 rev 2 reader of the `GR-V1.0x` binary levels types each record field as follows.

| Record | Field | How 2.05 reads it |
| --- | --- | --- |
| link | x, y, width, height | text, parsed as a decimal number and then rounded to a whole tile (half up: 43.5 becomes 44) |
| link | arrival x, arrival y | kept as text expressions; a missing value means `playerx` or `playery` |
| baddy | x, y | raw bytes, whole tiles (no 32 offset) |
| NPC | x, y | byte − 32, whole tiles |
| chest | x, y | byte − 32, whole tiles |
| sign | x, y | byte − 32, whole tiles |

- So in 2.05 every stored position is a whole tile. The one exception is a link's arrival, which stays
  an expression and so can be fractional when it is evaluated.
- A fractional link box such as `43.5` loads, but it is rounded.
- The Windows 4.04r2 reader keeps link boxes as floating point, so the two builds differ on exactly
  that field.
