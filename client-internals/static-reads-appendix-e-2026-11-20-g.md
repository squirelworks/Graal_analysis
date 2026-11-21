# Static reads for Appendix E, seventh batch (2026-11-20)

Date: 2026-11-20. Evidence: **[bin]** (a decompiler read of the real client executables on the
lab host A, plus a linear disassembly of the same files; no client run) and **[file]** (the
`arrays.dat` shipped with 1.39). Only behaviour is given here. Covers App. E#305 and E#317.

Builds read: the original Windows 2.22 `Graal2220.exe` (token `GNW03014`), and Windows 1.39
`Graal.exe` (the copy in the 1.39 archive and the one in the 1.x comparison set are the same file).

## The 2.22 gani frame fields (E#305)

The player object keeps its current gani in three fields: the gani itself, the **frame index**, and
a **tick count within the current frame**.

- Setting a gani: if the gani or its parameters change, both the frame index and the tick count
  go back to 0. A name with a `[n]` suffix starts at frame n instead (0 if n is out of range). Setting
  the gani the player already has changes nothing, so a gani set again every tick keeps running.
- Each tick: the tick count goes up by 1. Any sound of the frame whose tick equals the count is
  played. When the count reaches the frame's own length in ticks, the frame index goes up by 1 and
  the count goes back to 0. Past the last frame the gani loops or stops, as the gani says.
- In the earlier memory trace of 2.22 (`live-runs/2gta-222-2026-10-30`), the field logged as "walk
  frame" is the frame index. The field logged as "push frame", which cycled 0 to 3 each tick, is the
  tick count within the frame. It cycles through four values because each `push` frame lasts
  4 ticks. That is what the stock `push.gani` gives (five frames, each `WAIT 3`).

### The push threshold in the same routine

- The blocked-step counter is a general state counter of the player. While walking, if it has
  reached 38 it is set back to 18.
- Each tick while walking with the counter at 18 or more, the client sets the `push` gani. Because
  setting the same gani again changes nothing, the pose runs on from where it was.
- Five frames of 4 ticks make 20 ticks. That is the same length as the 18-to-38 counter cycle, so
  the pose loops in step with the counter.

So the trace is consistent with 2.05: `push` frames last 4 ticks, and the pose begins once 18
blocked ticks have been counted.

## The 1.39 item box and its unit (E#317)

### The pickup test, again

The 1.39 pickup routine was read again with the decompiler. It works in eighths of a tile, with
every position rounded down:

- The item box's left edge is (item x + 1) × 8 − w / 2, so the box is centred on x + 1. Its top
  edge is item y × 8 + 1, one eighth of a tile below the item's y. It is w eighths wide and
  h eighths tall.
- The player box is 16 × 16 eighths, starting at (player x + 0.5) × 8 and (player y + 1) × 8.
- The overlap is strict on all four sides. An item whose busy flag is set is skipped (what sets
  that flag was not traced).

### Where w and h come from

- w and h are two 6-bit fields of the item's sprite record. The record also holds the sprite's
  place in the item image.
- The sprite records are array 24 of `arrays.dat` (→ §3.5). A built-in 25-entry table maps each
  item to its record.
- The same record is read by the sprite drawer, which doubles w and h to get pixels. The item
  drawer divides them by 8 to get tiles. So **w and h are in eighths of a tile (2 pixels)**, the same
  unit as the pickup test.

### The boxes in tiles

These sizes come from the 1.39 `arrays.dat`, divided by 8:

| Item | Width | Height |
| --- | ---: | ---: |
| green, blue, red and gold rupee | 1 | 2 |
| bombs | 1.75 | 2 |
| darts | 1 | 2 |
| heart | 1 | 1 |
| glove 1, glove 2 | 1.75 | 2 |
| bow | 0.875 | 2 |
| bomb, super bomb | 2 | 2 |
| shield, mirror shield, lizard shield | 1 | 1.25 |
| sword, golden sword | 1 | 2.125 |
| full heart | 1.625 | 1.625 |
| battle axe | 1 | 1.875 |
| lizard sword | 0.625 | 2 |
| fireball | 0.875 | 0.875 |
| fireblast | 1.875 | 0.625 |
| nuke shot | 1 | 1.25 |
| jolt bomb | 0.75 | 1.875 |
| spin attack | 2 | 1.875 |

So a heart is taken when the player's body box overlaps the one-tile square from x + 0.5 to
x + 1.5 and from y + 1/8 to y + 1 1/8. A rupee's box is the same width and two tiles tall.

The 2.22 file gives the same sizes. The 1.21 file differs for darts (2.125 tall) and for the bomb
and super bomb (1.75 tall). Other builds take the sizes from their own `arrays.dat`.

### Draw order

The 1.39 lab run had already measured the draw order (`protocol/lab-appe-hostb-2026-11-20c.md`):
items and players are drawn in y order. That run is the evidence for the draw order. The drawer
was not read again here.

## Not covered

- What the 2.22 tick does after the last frame of a gani that neither loops nor continues. It was
  not needed for `push`.
- Which 1.39 pickups go to the server and which are counted locally, beyond the earlier note.
