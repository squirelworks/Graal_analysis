# Level conversion chain

One converter for the level generations, in this order:

`.zelda` (Z3-V1) → `.graal` (GR-V1) → `.nw` (GLEVNW01) → `.gmap` (a grid of
level files) → a future `.seihai` package.

TextConvert (`../classic-tools/text-convert.md`) walks a folder and writes
GLEVNW01 from GR-V1. It does not read Z3-V1, it does not write a gmap, and it
has no package step. This tool is that chain, both directions, as far as each
format can carry the data.

```
python3 tools/level-convert/convert.py <src> <dst>
```

The suffix chooses the format. Exit status is 1 when the file is truncated
and 2 for any other refusal. Warnings go to stderr and the file is still
written when the loss is only a field the target cannot store.

Binary levels are read with `formats/grv1-decoder/grv1.py`. A `.graal` board
is written with `tools/file-formats/gwebl.py` `write_board` (13-bit GR-V1.03).
Nothing here is a second board decoder. Tests are synthetic. No client
program is run.

## What is lossless

| Path | What survives |
| --- | --- |
| `.graal` ↔ `.nw` | 64×64 board (tile ids 0–4095), links (destination, box, `playerx` / `playery` / `playery+10` kept as written), signs, baddies with a numeric type, NPCs, chests whose item is one of the 25 names in `client-internals/level-editor-205.md`. |
| `.zelda` ↔ `.graal` ↔ `.nw` | The same board and links when every tile is 0–2047, plus signs and numeric baddies. A real Z3-V1 file has no NPC section and no chest section, so those lists stay empty. They are not invented. |
| `.nw` → `.seihai` → `.nw` | The GLEVNW01 bytes. |
| `.gmap` → `.seihai` → `.gmap` | The GRMAP001 bytes. |
| directory → `.gmap` → directory | Width, height, and each level's file name and cell. The gmap does not contain the level bytes. |

`.zelda` output is `Z3-V1.04` (the verse line is how baddy text is stored).
`.graal` output is `GR-V1.03`, which is what the 2.05 and 2.22 editors write
for a non-`.nw` file.

## What is lossy

- **NPCs and chests into `.zelda`.** Z3-V1 has no NPC section and no chest
  section. The tool says so and writes neither. A file named `.zelda` whose
  magic is actually `GR-V1` is read by the magic (`formats/level-binary.md`);
  saving it as `.zelda` then drops those sections.
- **Tiles above 2047 into `.zelda`.** Z3-V1 codes are 12-bit. Those tiles are
  stored as the low 11 bits, and a warning names the count. `.graal` and
  `.nw` keep ids 0–4095.
- **HEIGHTS.** A 9×9 overlay is read and written on `.nw`. `GR-V1.03` and
  Z3-V1 have no HEIGHTS block. `GR-V1.04` would, and `grv1.py` does not read
  that magic (it would take the board as 12-bit), so this tool refuses a
  `GR-V1.04` file instead of guessing.
- **NPC coordinates that are not whole tiles.** `.nw` keeps `10.5`. GR-V1
  stores a byte (`x+32`), so the fraction is cut off.
- **Link destinations with spaces.** GR-V1 keeps them (every token before the
  last six). GLEVNW01 keeps one token and the link is not written.
- **Baddy type names.** The notes give the display names and say the script
  names run from `graysoldier` to `dragon`, not the ten tokens. A numeric
  type 0–9 round-trips. A name is kept on `.nw` and is not given a made-up
  byte on `.graal` or `.zelda`.
- **`#K(13)` typed as sign text.** `grv1.py` drops that escape. A newline is
  stored as the editor does (`#K(13)` plus the newline code) and comes back
  as a newline.

## A gmap is a directory

`formats/gmap.md` is the reader: `GRMAP001`, `WIDTH`, `HEIGHT`, `LEVELNAMES`
as quoted CSV, then `MAPIMG`, `MINIMAPIMG`, `NOAUTOMAPPING`, `LOADFULLMAP`,
`LOADATSTART`. Generator lines (`GENERATED`, `HEIGHTMAP`, …) are kept and
are not turned into cells. `GENERATED` is not expanded.

Build one from a directory. Either `grid.txt` (this tool's index, not a
client file):

```
WIDTH 2
HEIGHT 2
0 0 west.nw
1 0 east.nw
0 1 south.nw
```

or GraalLevelGen names `prefix_a-01.nw` (`tools/classic-tools/graal-level-gen.md`),
column letter then a 1-based row. Holes are empty cells. Reading a `.gmap`
writes `grid.txt` only. It does not create the level files, because the map
does not hold them.

The converter refuses a grid above 512 on a side. That is this tool's own
guard, not a client limit.

## The package

`SEIHAI-FORMAT.md`. **[inf]** A 2.22 client does not read it.
