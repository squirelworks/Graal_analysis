# LevelFiller (2001)

LevelFiller ("LF") by Bruges was the NewWorld team's theme filler: it scatters
tile objects ("fillers": flowers, bushes, trees, rocks) over `GLEVNW01`
levels so a plain grass level looks hand-made, and it can append NPCs to many
levels at once. It shipped with a small level viewer and with LFThemeMaker,
which generates themes of random terrain patches.

Date: 2026-11-14. Static teardown only; nothing was run.

## What we hold

| File | Size | Date | State |
|---|---|---|---|
| `Levelfill.exe` v0.7 (two copies, same hash) | 681,984 | 2001-07-04 | Damaged: the first 604,160 bytes are zero. Only the resource tail (form text) survives. |
| `Levelfill.exe` v0.6 (a backup the DClient updater kept) | 689,664 | 2001-06-29 | Intact Delphi PE. The teardown below is of this build. |
| `levelviewer.exe` ("Level Viewer - v0.2") | 434,176 | 2001-06-29 | Intact Delphi PE. |
| `LFThemeMaker-Patches.exe` | 77,824 | 2001-06-29 | Intact VB6 PE. |
| `Readme.txt` (v0.7) and the v0.6 copy, `Levelfill.Commands.rtf` | | 2001-07-04 | The author's docs. |
| Themes `*.nwt`, patch recipes `*.tm`, preset objects `Levelfill.dat`, demo levels | | 2001 to 2003 | Text. |

v0.7 added `for`, `while` and `round` to the object language, rewrote the
interpreter and raised the object limit to 1,024. v0.6 has everything else
below. A Rust port should follow the v0.7 documentation for the language and
the v0.6 code for placement, which v0.7's notes say did not change.

## Files

### Theme (`.nwt`)

INI-like text, CRLF or LF.

```
[theme]
name=<display name>
author=<name>

[rules]
repbase=<tile>          ; optional: the level's background tile to fill over
base=<tile>             ; the background a preview level is made of
<object>=<quantity>[|<replace tile>]
;comment lines start with ';'

[objects]
<object>                ; "<name>" on its own line opens an object
.author=<name>          ; optional dotted properties
.top=100%,<object>      ; border objects (see Borders)
.left=… .bttm=… .rght=…
<tile rows>             ; two Graal tile characters per cell, a space pair = transparent
```

- Tiles are the two-character base64 codes of `BOARD` lines (`AA` is tile 0).
- A rule with no `|tile` uses the theme's `base` as the tile it may replace.
- A name followed by `*` (`<Complex Flowers>*`) marks a complex object: the
  body is script text, not tile rows. When saved, `<` and `>` inside script
  are escaped as `#l` and `#g`.
- Rules are tried in file order. Objects higher in the list are placed first
  and can use up the space (the editor's own hint says so).
- Names are case sensitive and may not contain `(`, `)`, `<`, `>`. A theme
  holds at most 200 objects in v0.6, 1,024 in v0.7.

`Levelfill.dat` is the same `[objects]` body with 90 preset objects (Vangel's
set) that the theme editor offers.

### Quantity

| Form | Meaning |
|---|---|
| `n` | Try `n` placements. Must be an integer. |
| `p%` | A share of the level: `Round(width × height × p / 100)` cells. Each placement attempt subtracts the object's own area (w × h) instead of 1. `p` may be fractional. |
| `r(a,b)` | A random integer from `a` to `b`, then as above. `r(a,b)%` is allowed. |
| `c(p%,n)` | Roll `n` times with a `p`% chance each; the count of hits. |

The number is how many the program tries, not a guarantee: a placement that
finds no room is dropped.

### Level I/O

LF reads a `GLEVNW01` file, takes the 64 `BOARD` rows into a 64 × 64 grid of
two-character cells, and keeps every other line (links, signs, NPCs, chests)
as an opaque tail. On save it writes `GLEVNW01`, then 64 lines
`BOARD 0 <y> 64 0 <128 characters>`, then the tail unchanged. v0.5 fixed a bug
that added extra `GLEVNW01` lines.

### INI

`LEVELFILL.ini` `[config]`: `edgessetting`, `autosave`, `autodebug`,
`picsfile` (the `pics*nw.png` tileset the editor draws with) and `deftheme`.
In plug-in mode the file is `levelfill.<app>.ini`.

## Placement

For each rule, in order:

1. Evaluate the quantity (above) to a remaining amount.
2. While the amount is above 0: pick `row = Random(H')` then
   `col = Random(W')`, where `W'`, `H'` are the level size, less the object's
   size when "keep inside the level" is ticked. Delphi's `Random` (the
   `RandSeed × 0x08088405 + 1` generator).
3. A position fits when every cell of the object's bounding box, transparent
   cells included, currently holds the replace tile. Cells outside the level
   read the neighbouring level when "fill across levels" is on and that level
   was loaded; otherwise the fit fails.
4. Up to three positions are tried per placement. On a fit the object's
   non-blank cells are written (into the neighbour level for overhang). A
   complex object is evaluated first and placed as the object it builds or
   returns.
5. Subtract 1 (or the area, for `%`) whether or not a fit was found.

Neighbours: "fill across levels" keeps five neighbour grids next to the
current level (the four sides and one corner) and reads and writes overhang
into them. Which corner, and how the batch is laid out as a map, was not
pinned down.

### Borders

An object with `.top=`, `.left=`, `.bttm=`, `.rght=` (`percent,object`) gets
border objects after all placements of that rule, so touching copies form one
patch and only its outer edges get a border, each with the given chance. This
is from the author's readme, who called it "a dubious feature"; the border
code itself was not traced.

## Object language (complex objects)

Statements end in `;`. Line breaks are spaces. `//` and `/* */` comments.

| Form | Effect |
|---|---|
| `setsize(w,h);` | The object's size. Required before `add`. |
| `setworkarea(x,y,w,h);`, `unsetworkarea;` | Restrict `add` to a sub-rectangle. |
| `add(obj,n);` | `n` copies of a plain object or tile (`*AA`) at random spots in the area. |
| `add(obj,x,y);` | One copy at that spot. |
| `return(obj);` | Use another object or tile instead of this one. |
| `r(a,b)`, `c(p%,n)`, `round(x)` | Random, chance count, rounding. |
| `if (cond) {…}`, `while (cond) {…}`, `for (v=a,b[,step]) {…}` | v0.7 adds `while`, `for`, `round`. |
| `v=expr` | Variables. Operators `+ - * / ^`, `=`/`==`, `not`, `and`, `or`. `/` is integer division. |
| `debug(v);`, `debug(*);`, `msg('text'&10'more');` | Message boxes; a port can print them. |

Errors the checker raises: "Parameter is not a percentage.", "Unterminated
String.", an object over the limit.

## Command line (plug-in mode)

| Switch | Effect |
|---|---|
| `/n:<app>` | Plug-in mode: title shows the host, loads `levelfill.<app>.ini`, hides level selection, forces autosave, "Exit" becomes "Done". |
| `/l:"a.nw[,b.nw…]"` | The levels to fill. |
| `/o:"caption"` | Text shown instead of the level list. |
| `/t:"theme.nwt"` | Fix the theme. |
| `/silent` | No window: apply, save, exit. Needs `/t` and `/l`. |
| `/log:"file"` | Write a log of the actions. |

Greaditor called LF this way on a temporary copy of the open level.

## LFThemeMaker (`.tm` → `.nwt`)

A VB6 generator for "X on Y" patch themes (dirt on grass, deep water on
water). A `.tm` recipe:

```
[Tiles]   Tile00..Tile15 = 16 tiles, one per corner mask
[Objects] WidthMin/Max, HeightMin/Max (3..32), DensityMin/Max (%), BaseObjectName, Method2
[Theme]   #ofObjects, QtyPerObject (e.g. c(5%,1)), Description, Filename, Overwrite
```

Each generated object is a random blob of "inside" corners in a grid of the
chosen size and density. Every cell takes `Tile[mask]`, where the mask is the
four corners around the cell: top-left 1, top-right 2, bottom-right 4,
bottom-left 8. Mask 0 is written as blank (transparent). This was checked on
the shipped `default.nwt` against `LightGrass_on_Grass.tm`: `g1` (mask 4) opens
a patch at its top-left, `go` (mask 3) is a bottom edge, `g0` (15) is inside.
The rule for every object is `QtyPerObject|<Tile00>`.

## For a port

`seihai-servertools level fill` in lat-core: read `.nwt`, evaluate quantities
and the object language, place with the rules above, write `GLEVNW01` with the
tail preserved, and a `theme make` that turns a `.tm` into a `.nwt`. Use a
seeded generator (`--seed`) for tests; reproducing Delphi's exact sequence is
only needed to match a captured output, and we have none.

Open: the v0.7 interpreter's own code is lost with its exe, so `for`/`while`
semantics come from the manual only. The border pass was read at the level of
"which edges", not tile by tile.
