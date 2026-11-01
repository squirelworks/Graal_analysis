# Level-tool gaps

Date: 2026-11-01

What the 2.22 generator reference and the level converter leave open, filled
only where a note or a static read already states the layout. The original
programs were not run. No image from the generators folder is committed.

`tools/generators-222/` and `tools/level-convert/` are on `main`. This folder
does not replace them.

## Z3-V1.02 and GR-V1.04

`formats/grv1-decoder/grv1.py` reads both.

- `Z3-V1.02` is 11-bit codes. Only the 1998 Java Zelda Online games read it.
  The baddy record is the same 3 bytes plus a newline the `.03` reader already
  accepts. No real `.02` file is in the notes; the tests are synthetic.
  **[doc]** `formats/level-binary.md`, `client-internals/precursors-and-fan-builds.md`.
- `GR-V1.04` is `GR-V1.03` (13-bit board, NPCs, chests) plus an optional
  `HEIGHTS` block after the signs: an empty line, `HEIGHTS`, at most nine
  lines of at most nine comma-separated decimals, `HEIGHTSEND`
  (case-insensitive). The same block is kept on any magic. **[2.31]**
  `formats/level-binary-client.md`.

`tools/level-convert` now loads those two magics. Saving `.graal` still
writes `GR-V1.03` and drops `HEIGHTS` with the existing warning. Saving
`.zelda` still writes `Z3-V1.04`. `tools/file-formats/gwebl.py` uses the
same 11-bit width for `Z3-V1.02`.

## graal-txt and nw-txt

Both executables are in the generators folder on Drive. The March 2003
`levelgendoc.html` describes the nw-gmap build (dashed `.nw` names and a
`.gmap`), not these two. `txtlevel.py` is the file-name and container
contract from a static read:

| Build | Level name | Body | Map file |
| --- | --- | --- | --- |
| graal-txt (2004-01-18) | `prefix` + column + `-` + row + `.graal` | `GR-V1.03`, because the name does not end in `.nw` | `bigmap.txt` |
| nw-txt (2001-06-30) | `prefix` + column + row + `.nw` (no dash) | `GLEVNW01`, because `.nw` selects the text writer | `bigmap.txt` |

Column letters are `a` plus the index mod 26. A leading letter is added
only when the map is at least 26 levels wide. The row is 1-based. It gains
one leading zero when the map is at least 10 levels tall, and another when
it is at least 100. `bigmap.txt` is one row per line of `"name","name"`.
**[bin]**

The reference writes those names, an empty-object level body, and the
bigmap. It does not paint the picture. Links are the terminator only.

## DungeonMaker 0.9

`docu_dungeongenerator.txt` names the styles (maze, onion, spiral, rogue,
snake, square spiral), the symmetry values 0–4, `DOUBLE`, and the onion and
spiral option bits. It shows pictures of the results. It does not say how
the crawler walks, where it turns, or how a room is stamped. The `layouts`
folder holds `rooms0`–`rooms9`, `roomsX`, matching `stats*` files and
`constants`. The manual does not describe those bytes.

There is no crawler reference here. `tools/generators-222/dungeon.py`
already draws the shapes the manual names, and it says those shapes are
not the library. **[doc]**

## Water, mountain and sand edges

The March 2003 manual names water, mountains and sand as colours. It does
not name edge tiles. A static read of graal-txt shows colour 2 (water) and
colour 3 (mountains) each mark a 6-pixel cell from its four corners, and a
later pass blits small stamps from neighbour flags. Colour 5 (sand) is
tested in the per-pixel pass. The colour match is the sum of absolute
channel differences, strictly under 32, the same limit as the nw-gmap
reference.

The stamp-to-shore table is a long branch list. Publishing a guess would
invent a layout, so `generators-222/levelgen.py` still paints one fill tile
for those colours, and this folder does not add another painter. **[doc][bin]**

## gif2mng

`gif2mng.py` writes the subset `../gif2mng.md` states, on synthetic frames:

- one frame → PNG
- two or more frames → MNG
- `-b` forces transparent index 2 and does not add a palette entry

The seven body-slot RGB values are not in the note (the draw-time roles are
in `client-internals/body-colours-and-attributes.md`, which is not a file
palette). `-b` therefore leaves the RGB entries as they were. TERM is a
chunk name in the program; its delay fields are not specified, so it is not
written. MHDR ticks and play time are 0. One FRAM of mode 1 precedes the
frames. **[doc][bin]**
