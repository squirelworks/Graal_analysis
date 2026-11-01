# Graal 2.22 generators

Date: 2026-11-01

The `generators` folder in the Graal 2.22 tree holds three writers. Each one
below is a Python 3 reference (standard library only) of the file it writes.
The windows are not reproduced. The original executables were not run.
Static reads of the Linux dungeon binary and the terrain and level-generator
images supplied the file layout, the colour table, and the forest stamp.
Tags: **[doc]** the text in that folder, **[bin]** a static read, **[file]**
a small options or script file from the same folder.

`seihai-core` already parses `GLEVNW01` boards, links and NPCs
(`assets/level.rs`) and a `GRMAP001` `LEVELNAMES` grid (`gmap.rs`). It skips
generator keys (`GENERATED`, `HEIGHTMAP`, and the rest) and does not keep a
text `HEIGHTS` block. These references stay in Graal_analysis.

| Module | Tool in the 2.22 tree | What the reference writes |
| --- | --- | --- |
| `terrain.py` | `TerrainGenerator.exe` (2003-12-16) | Plasma control grid → `GRMAP001` generator form and `GLEVNW01` levels of tile 0 plus a 9×9 `HEIGHTS` block and edge `LINK`s. |
| `dungeon.py` | `dungeongen.exe` and the Linux `dungeongen` (2003-05-23) | `GDUNG001` options, an `X`/`.` layout or a named style, 8×11 blocks, edge links, NPCs, short `GRMAP001`. |
| `levelgen.py` | `GraalLevelGen_nw-gmap.exe` (2003-03-07) | Twelve colours, a 6-pixel grid, forest stamp, `GLEVNW01` and a `LEVELNAMES` gmap. A second run paints over an existing level. |

`nwtext.py` is the shared text writer. Tests build their own grids and pixels.

## Not reimplemented

- **gif2mng.exe**, in the client tree next to `generators/`. The frame rule in `../gif2mng.md` is implemented in `../level-tools-gaps/gif2mng.py` (one frame PNG, more frames MNG, `-b` forces transparent index 2 on the existing palette). The seven slot RGB values are not in that note, so the writer does not invent them.
- **GraalEditor** and **GraalShop**. Editors, not generators. See `../graaleditor.md` and `../graaleditor-vs-205.md`.
- **TextConvert**, **GChar**, and **Graal Character Designer**. Not in this folder. See `../classic-tools/`.
- **GraalLevelGen_graal-txt.exe** (2004-01-18) and **GraalLevelGen_nw-txt.exe** (2001-06-30). File names and `bigmap.txt` are in `../level-tools-gaps/`. This module stays the nw-gmap build, which matches `levelgendoc.html` from the same day. The two txt programs do not write that gmap.
- The nw-gmap image can also write `GR-V1.03` when the output name does not end in `.nw`. **[bin]** This module writes the `.nw` branch only.
- DungeonMaker 0.9's crawlers. The Linux `dungeongen` links that library for the random styles and reads `layouts/rooms*`, `layouts/stats*` and `layouts/constants`. **[bin]** The style functions here draw the shapes named in `docu_dungeongenerator.txt` (maze, onion, spiral, rogue, snake, square spiral). They are not that library. The manual names the styles and the option bits and does not give the crawler steps, so `../level-tools-gaps/` does not add a second generator.
- Water, mountain and sand edge pieces in GraalLevelGen. The image tests neighbour flags and blits small stamps. **[bin]** The March 2003 manual names the colours and not the edge tiles, so this reference still marks those colours with one fill tile. `../level-tools-gaps/` records that limit.

## Terrain

Dialog fields are grid width and height, base, height, chaos, even borders, an islands preset, and a seed. **[doc][bin]** Islands are even borders: the rim of the control grid stays at the base. The gmap keys, in the order the image's literal pool lists them, are `WIDTH`, `HEIGHT`, `GENERATED 1`, `GENSEED`, `GENBASE`, `GENEVENBORDERS`, `GENHEIGHT`, `GENCHAOS`, `LEVHEIGHT`, `LEVCHAOS`, `MAPIMG`, one level name per line, `HEIGHTMAP`, `RANDOMSEEDS`. **[bin]** Level names are the world name, an `A`…`Z`/`AA` column, and a zero-padded row, plus `.nw`. A level is `GLEVNW01`, 64 `BOARD` rows of tile 0 (` 64 0 ` and 128 `A`s), `HEIGHTS` (nine lines of nine numbers), and a `LINK` on each edge that has a neighbour. West arrives at 61, east at 0, north at 61, south at 0; the other axis is `playerx` or `playery`. **[bin]**

The displacement is the usual midpoint split. The random step is the Delphi generator (`seed * 134775813 + 1` in 32 bits). `LEVHEIGHT` and `LEVCHAOS` default to the map height and chaos. The numbers will not match a save from the window.

## Dungeon

`dungeonoptions.txt` starts with `GDUNG001`. **[file]** A `LAYOUTFILE` of `X` (wall) and `.` (path) wins over `LAYOUTSTYLE`. Each cell is 8 tiles wide and 11 tall, then cut into 64×64 levels. **[doc]** Level names are `LEVELSTART`, a column letter, and a 1-based row (`cave_A1.nw`). The gmap is three lines after the signature: `WIDTH`, `HEIGHT`, `GENERATED` plus the bottom-right name. **[bin]**

Place names, for NPCs and for `TILES` blocks of 88 ids:

- `path` — the cell is not `X`.
- `walln` / `walls` / `wallw` / `walle` — exactly one open side, and the wall sits on the opposite side (`walln` has path to the south, the north wall of a room). That matches the torch lines in the shipped options. **[doc][file]**
- `wallnw`, `wallne`, `wallsw`, `wallse` — no open side, and exactly one open diagonal. A rectangular room's northwest corner has its path on the southeast diagonal.
- `wallnw2`, `wallne2`, `wallsw2`, `wallse2` — two adjacent open sides (a 270° notch).
- `walld1` — path to the north and the south. `walld2` — path to the east and the west. Those two names are in the image and in the example `TILES` lines, not in the manual's place list. **[bin][file]**
- `wall` — anything else, including a solid cell.

Without a `TILES` line the reference uses a plain block: path is tile 0, a wall is tile 1 with the open side cleared. The original's default sheet is the cave png, which this does not redraw. **[doc]**

`NPC` lines take `image`, `script`, `blocking`, `underplayer`, `dominant`, `chance`, `place`, `x`, `y`. Chance is 1 to 100, with or without a `%`. `x` and `y` are offsets inside the 8×11 block. A false `blocking` adds `dontblock`; `underplayer` adds `drawunderplayer`. **[bin]** `ADDTESTNPCS` adds one NPC per level whose script is the `addtiledef` / `addtiledef2` / `loadmap` test from the manual. **[doc][bin]**

`LAYOUTSYMMETRY` 1 leaves the grid alone, 2 mirrors across the vertical centre, 3 across the horizontal centre, 4 does both, and 0 picks one of 1–4 from the seed. `DOUBLE 1` draws a maze on half the cells and scales it up; `DOUBLE 0` carves at full size. `LAYOUTORIENTATION` is accepted and stored; the sample file sets it to 1 and the reference does not rotate.

## Level generator

Draw a picture whose width is 64 times the levels across and whose height is 64 times the levels down. Colours, with the match limit of 32 from the image: **[doc][bin]**

| Index | Name | RGB |
| --- | --- | --- |
| 0 | Grass, not drawn | 24, 140, 24 |
| 1 | Forest | 181, 239, 189 |
| 2 | Water | 0, 0, 255 |
| 3 | Mountains | 128, 0, 0 |
| 4 | Flowers | 255, 0, 0 |
| 5 | Sand | 150, 110, 0 |
| 6 | Puddle | 0, 255, 255 |
| 7 | Puddle stone | 0, 179, 179 |
| 8 | Small sand stones | 113, 82, 0 |
| 9 | Big sand stone | 83, 61, 0 |
| 10 | Swamp | 0, 106, 0 |
| 11 | Bushes | 0, 66, 0 |

The grid is `(width + 5) // 6` by `(height + 5) // 6`. Cell `(x, y)` reads the pixel at `(x * 6, y * 6)`. **[bin]** Forest blits this 6×5 stamp at `(x * 6, y * 6 + 1)`, shifted 3 tiles left on odd rows:

```
25 26 27 28 29 30
41 42 43 44 45 46
57 58 59 60 61 62
73 74 75 76 77 78
89 90 91 92 93 94
```

Other matched colours write one fill tile (water 12, mountains 80, flowers 4, sand 5, puddle 6, puddle stone 7, small stones 8, big stone 9, swamp 10, bushes 11). An unknown colour, and grass, write nothing.

Level names are `world_a-01.nw` through `world_z-99.nw` style: a lower-case column, a dash, and a 1-based row of two digits. **[doc]** The gmap is `WIDTH`, `HEIGHT`, and quoted `LEVELNAMES` rows. **[bin]** Edge links use the same 0/61 arrival as the terrain levels. A second run keeps existing `LINK` and `NPC` lines and paints only the new non-grass tiles. **[doc]**
