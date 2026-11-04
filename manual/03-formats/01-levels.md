<!-- manual: kind=reference status=draft -->
# 3.1 Levels: Z3-V1, GR-V1, GLEVNW01

A Graal level is one 64×64 board of tiles plus its links, baddies, NPCs, chests and signs. Three file families carry it: the binary Z3-V1 (`.zelda`) and GR-V1 (`.graal`) formats, and the text GLEVNW01 (`.nw`) format. The wire form of a board is in → §2.

> Status: draft. The 2.05 GR-V reader and writer and the 2.31 reader are measured; the 2.05 loader's Z3-V1 path and every build after 2.31 are not.

## 3.1.0 Format selection

| Item | Rule | Source |
| --- | --- | --- |
| magics in the 2.05 string table | `Z3-V1.03`, `Z3-V1.04`, `GR-V1.00` to `GR-V1.03`, `GLEVNW01`; each set appears three times, one copy next to the GWEBL001 cache code (→ §3.8) | [2.05] (formats/level-binary.md) |
| server loader | picks the loader from the extension `.nw`, `.graal` or `.zelda`; for an unknown extension, from the 8-byte magic | [srv] (formats/glevnw01.txt) |
| server magic fallback | `GLEVNW01` → text loader; `GR-V1.01`, `GR-V1.02`, `GR-V1.03` → binary Graal loader; `Z3-V1.03`, `Z3-V1.04` → Zelda loader | [srv] (formats/glevnw01.txt) |
| real files | a reader must decide by the magic, not the extension: `.zelda` names hold GR-V1 files and `.graal` names hold `Z3-V1.04` files | [test] (formats/level-binary.md#z3-v1-differences) ; [test] (client-internals/decomp-findings-2026-10-25-j/03-extensions-and-magic.md) |
| `.zelda` names | 694 of 801 distinct `.zelda`-named files in the old builds are `GR-V1.00` to `GR-V1.03`; 1st Graal's 16 levels are all `Z3-V1.04` under `.graal` names | [test] (client-internals/decomp-findings-2026-10-25-j/03-extensions-and-magic.md); [test] (client-internals/decomp-findings-2026-10-25-j/by-build.tsv) |
| client magics | every client tested, 1st Graal to 2.31 and the NewWorld betas, carries `Z3-V1.03` and `Z3-V1.04` and no third `Z3-V1` revision; the 1st Graal and 1.39 loaders compare the 8 magic bytes only | [bin] (client-internals/decomp-findings-2026-10-25-j/03-extensions-and-magic.md) |
| 2.05 writer | always writes `GR-V1.03` for a level that is not saved as `.nw` | [2.05] (formats/level-binary.md#open) |
| 2.31 writer | writes `GR-V1.04` only when the level has a height map, `GR-V1.03` otherwise | [2.31] (formats/level-binary-client.md#gr-v104-231) |

| Rule | Detail | Source |
| --- | --- | --- |
| bare names | no client adds `.zelda` to a level name without an extension, and none swaps `.zelda` for `.graal` when a file is missing; a link or warp loads the name as written | [bin] (client-internals/bare-level-names.md#findings) |
| editor | the editor's open and save buttons (and from 1.3 the snapshot save) add `.graal` to a name typed without an extension | [bin] (client-internals/bare-level-names.md#findings) |
| built-in names | 1st to 9th Graal compare the current level with fixed names such as `level1.zelda` and `cave2.zelda` or warp to them | [bin] (client-internals/bare-level-names.md#findings) |
| scope | read in 26 Windows builds, 1st Graal to 1.32 and 2.05; that the loader uses the name unchanged is inferred | [bin][inf] (client-internals/bare-level-names.md#confirmed-inferred-not-tested) |

Which builds accept which magics is in the build catalogue (→ §1.1).

## 3.1.1 Z3-V1 (.zelda)

Z3-V1 is the Zelda Online level family. Its board coding is that of GR-V1 (→ §3.1.2.1); only the code width and the sections differ.

### 3.1.1.1 Layout

| Order | Section | Shape | Source |
| --- | --- | --- | --- |
| 1 | magic | `char[8]`: `Z3-V1.02`, `Z3-V1.03` or `Z3-V1.04` | [srv] (formats/level-binary.md#layout) |
| 2 | board | bit stream until 4096 tiles are produced (→ §3.1.2.1) | [srv] (formats/level-binary.md#layout) |
| 3 | links | text lines until `#` or an empty line (→ §3.1.2.3) | [srv] (formats/level-binary.md#layout) |
| 4 | baddies | binary records until `FF FF FF` (→ §3.1.1.2) | [srv] (formats/level-binary.md#layout) |
| 5 | signs | text until an empty line or end of file (→ §3.1.2.6) | [srv] (formats/level-binary.md#layout) |

Z3-V1 has **no NPC section and no chest section** [srv] (formats/level-binary.md#z3-v1-differences).

### 3.1.1.2 Revisions

| Magic | Code width | Baddy record | Readers | Source |
| --- | --- | --- | --- | --- |
| `Z3-V1.02` | 11 bits | 4 bytes, last byte always `\n` | only the 1998 Java Zelda Online games; no real file is in the notes | [srv][test] (formats/level-binary.md#z3-v1-differences); [src] (formats/grv1-decoder/README.md) |
| `Z3-V1.03` | 12 bits | 4 bytes: `x y type` then an empty line rest; no verse line | Zelda Online, Delphi and later clients, server | [srv][test] (formats/level-binary.md#z3-v1-differences) |
| `Z3-V1.04` | 12 bits | `x y type` then the verse line (→ §3.1.2.4) | Delphi and later clients, server | [srv][test] (formats/level-binary.md#z3-v1-differences) |

| Rule | Detail | Source |
| --- | --- | --- |
| link numbers | `Z3-V1.03` links are written with decimals (`31.0 42.0 2.0 1.0 43.5 41.0`), so the numbers are floating point | [test] (formats/level-binary.md#z3-v1-differences) |
| negative arrival | a negative `newx` or `newy` means "keep the player's own coordinate" | [test] (formats/level-binary.md#z3-v1-differences) |
| baddy bytes | the three raw bytes `x y type` are taken before the line end is looked for, because `0x0A` can be an `x` or a `y` | [test] (formats/level-binary.md#z3-v1-differences) |
| baddy types | values 0 to 6 occur; Zelda Online's names for them are green, blue and red soldier, shot soldier, swamp soldier, jumping hare, octopus | [test] (formats/level-binary.md#z3-v1-differences) |
| link destinations | no destination name contains a space; `Z3-V1.03` links name `.zelda` or `.editor` files, `Z3-V1.04` links `.graal`, `.zelda` or `.editor` | [test] (client-internals/decomp-findings-2026-10-25-j/02-links-and-arrivals.md#destination-extensions) |
| verses | every `Z3-V1.04` record carries the verse line, most with all three verses empty; no `Z3-V1.03` record has one | [test] (client-internals/decomp-findings-2026-10-25-j/01-record-shapes.md#computers-baddies) |
| a GR-V1 reader on Z3-V1 | integer link parsing drops 124 decimal links, a computer line end left in the stream shifts every later record, and a negative arrival is taken as a literal coordinate | [test] (client-internals/decomp-findings-2026-10-25-j/05-old-reader-failures.md) |
| sample | the rules were checked against 139 distinct real files | [test] (formats/level-binary.md#z3-v1-differences) ; [test] (client-internals/decomp-findings-2026-10-25-j/format-stats.tsv); [test] (client-internals/decomp-findings-2026-10-25-j/04-loader-rules-compared.md) |

## 3.1.2 GR-V1 (.graal)

### 3.1.2.0 Layout

| Order | Section | Shape | Revisions | Source |
| --- | --- | --- | --- | --- |
| 1 | magic | `char[8]`: `GR-V1.00` to `GR-V1.04` | all | [srv] (formats/level-binary.md#layout); [2.31] (formats/level-binary-client.md#gr-v104-231) |
| 2 | board | bit stream until 4096 tiles are produced (→ §3.1.2.1) | all | [srv][2.05] (formats/level-binary.md#board-bit-stream) |
| 3 | links | text lines until `#` or an empty line | all | [srv][2.05] (formats/level-binary-client.md#section-rules-in-the-client-reader-205) |
| 4 | baddies | 3-byte records, each followed by a verse line, until `FF FF FF` | all | [srv][2.05] (formats/level-binary-client.md#section-rules-in-the-client-reader-205) |
| 5 | NPCs | text lines until `#` or an empty line | `GR-V1.00` and later | [srv][2.05] (formats/level-binary-client.md#section-rules-in-the-client-reader-205) |
| 6 | chests | text lines until `#` | `GR-V1.01` and later | [srv][2.05] (formats/level-binary-client.md#section-rules-in-the-client-reader-205) |
| 7 | signs | everything left (2.05); up to the first empty line (2.31) | all | [2.05][2.31] (formats/level-binary-client.md#agreement-with-level-binarymd) |
| 8 | heights | empty line, then a `HEIGHTS` block (→ §3.1.2.7) | `GR-V1.04`; accepted after any magic by 2.31 | [2.31] (formats/level-binary-client.md#gr-v104-231) |

The board is a packed bit stream with run-length codes, not a 64×64 array of 2-byte tiles; only `.nw` text and the wire board form store one 16-bit value per tile [srv] (formats/level-binary.md#correction).

### 3.1.2.1 Board bit stream

| Rule | Detail | Source |
| --- | --- | --- |
| bit order | bytes are appended to a little-endian bit buffer; each code is the bottom `width` bits | [srv] (formats/level-binary.md#board-bit-stream) |
| flag bit | the top bit of the code: `0x800` at 12 bits, `0x1000` at 13 bits | [srv] (formats/level-binary.md#board-bit-stream) |
| flag clear | the code is a tile id | [srv] (formats/level-binary.md#board-bit-stream) |
| flag set | a control code: `count = code & 0xFF`; if `code & 0x100` is set the next run is a double run | [srv] (formats/level-binary.md#board-bit-stream) |
| default count | `count = 1`: the next tile is written once | [srv] (formats/level-binary.md#board-bit-stream) |
| single run | the next tile is written `count` times, then `count` resets to 1 | [srv] (formats/level-binary.md#board-bit-stream) |
| double run | two tiles A and B are read and `A B` is written `count` times (`{double 4} 5 6` → `5 6 5 6 5 6 5 6`), then the count resets | [srv] (formats/level-binary.md#board-bit-stream) |
| fill order | tiles fill `board[x + 64*y]` row by row, layer 0 only, until 4096 tiles are produced | [srv] (formats/level-binary.md#board-bit-stream) |
| double flag | the Java Zelda Online reader keeps the double flag until a double run completes, the GR-V1 reader clears it at the next control code; no real file shows a difference (0 of 663) | [test] (client-internals/decomp-findings-2026-10-25-j/04-loader-rules-compared.md) |
| tile range | a 12-bit file cannot address tiles ≥ 2048, because the flag takes the top bit; that is why 1.02 widened the code to 13 bits for the 4096-tile `pics1` | [inf] (formats/level-binary.md#board-bit-stream) |

Code width per magic:

| Magic | Width | Source |
| --- | --- | --- |
| `Z3-V1.02` | 11 | [srv] (formats/level-binary.md#board-bit-stream) |
| `Z3-V1.03`, `Z3-V1.04` | 12 | [srv][2.05] (formats/level-binary.md#board-bit-stream) |
| `GR-V1.00`, `GR-V1.01` | 12 | [srv][2.05] (formats/level-binary.md#board-bit-stream) |
| `GR-V1.02`, `GR-V1.03` | 13; the 2.05 loader compares the magic against 1.02 and 1.03 to pick it | [srv][2.05] (formats/level-binary.md#board-bit-stream) |
| `GR-V1.04` | 13 | [2.31] (formats/level-binary-client.md#agreement-with-level-binarymd) |

### 3.1.2.2 Board writer (2.05)

The 2.05 writer walks the 4096 tiles in order and picks one case at each position [2.05] (formats/level-binary-client.md#board-writer-205):

| Case | Codes emitted | Source |
| --- | --- | --- |
| the next tile equals this one | `0x1000 \| n`, then the tile; `n` counts 2 to 64 equal tiles | [2.05] (formats/level-binary-client.md#board-writer-205); [2.05] (formats/level-binary.md#open) |
| tiles `i, i+1` equal `i+2, i+3` (pattern AB AB) | `0x1100 \| n`, then A, then B; `n` counts up to 64 pairs | [2.05] (formats/level-binary-client.md#board-writer-205) |
| otherwise | the tile, `& 0xFFF` | [2.05] (formats/level-binary-client.md#board-writer-205) |
| packing | 13 bits per code, least significant bit first; the last partial byte is flushed | [2.05] (formats/level-binary-client.md#board-writer-205) |
| check | `write_board` in `tools/file-formats/gwebl.py` follows these rules and re-encodes 144 cached levels and 13 tutorial levels byte for byte | [test] (formats/level-binary-client.md) |
| full runs | single runs of exactly 64 occur in the embedded tutorial levels | [2.05] (formats/level-binary.md#open) |

### 3.1.2.3 Links

| Rule | Detail | Source |
| --- | --- | --- |
| line | `dest x y w h newx newy` | [srv] (formats/level-binary.md#records) |
| spaces | the level name may contain spaces; the tokens before the last six are rejoined into `dest` | [srv] (formats/level-binary.md#records) |
| missing level | a link to a level that does not exist is dropped | [srv] (formats/level-binary.md#records) |
| arrival | `newx` and `newy` may be `playerx` or `playery`, optionally followed by a signed number (`playery+10`) | [srv] (formats/level-binary.md#records) |
| terminator | a line `#` or an empty line | [srv][2.05] (formats/level-binary.md#layout) |
| negative arrival | 805 of 5381 distinct GR-V1 links in the old builds have a negative arrival; that 2.x reads it as "keep the player's coordinate", as Z3-V1 does, is inferred | [test][inf] (client-internals/decomp-findings-2026-10-25-j/02-links-and-arrivals.md#negative-arrivals) |

How the client resolves an arrival expression is in → §4.

### 3.1.2.4 Baddies

| Rule | Detail | Source |
| --- | --- | --- |
| record | `i8 x, i8 y, i8 type`, then a `\n`-terminated verse line | [srv] (formats/level-binary.md#records) |
| verse line | three verses separated by `\`: sight, hurt, attack | [srv] (formats/level-binary.md#records) |
| line end | the client reads up to a `\n` that comes after at least 3 bytes, so the binary bytes may contain `0x0A` | [2.05] (formats/level-binary-client.md#section-rules-in-the-client-reader-205) |
| terminator | `FF FF FF` followed by an empty line; the client stops at a record whose first byte is ≥ `0x80` | [srv] (formats/level-binary.md#records); [2.05] (formats/level-binary-client.md#section-rules-in-the-client-reader-205) |
| x of 0 | a valid baddy; real levels have them; a reader that stops at x = 0 loses them and reads the rest of the baddy bytes as NPC lines | [test] (formats/grv1-decoder/README.md); [test] (client-internals/decomp-findings-2026-10-25-f/03-baddy-terminator.md) |
| corpus | 902 baddies in 99 of 3113 levels; types 0 to 9 all occur | [test] (client-internals/decomp-findings-2026-10-25-f/03-baddy-terminator.md); [test] (client-internals/decomp-findings-2026-10-25-f/corpus-stats.tsv) |
| short record | the reference decoder also ends the section at a record shorter than 3 bytes | [test] (formats/grv1-decoder/README.md) |

### 3.1.2.5 NPCs and chests

| Record | Shape | Source |
| --- | --- | --- |
| NPC | `GCHAR x, GCHAR y, image#script`; the script uses `0xA7` for a newline; an empty image is a script-only NPC | [srv] (formats/level-binary.md#records) |
| chest | `GCHAR x, GCHAR y, GCHAR item, GCHAR signindex` | [srv] (formats/level-binary.md#records) |

Coordinates in these records are whole tiles (GCHAR), not half-tiles [srv] (formats/level-binary.md#records). NPC bytes are single bytes and can lie outside 0 to 63, as 165 NPCs in the corpus do. A level with no chests still ends the section with a bare `#`. Chest items 0 to 11, 16, 17, 19 and 24 occur, plus one 78, outside the 25-name table; 343 of 375 chests have sign index −1, which is "no sign" [test] (client-internals/decomp-findings-2026-10-25-f/01-section-shapes.md); [test] (client-internals/decomp-findings-2026-10-25-f/04-sign-and-chest-details.md). The chest item index table is in → §8.

### 3.1.2.6 Signs

| Rule | Detail | Source |
| --- | --- | --- |
| record | `GCHAR x, GCHAR y`, then text in the sign alphabet | [srv] (formats/level-binary.md#records) |
| alphabet | the same as signs on the wire: `byte - 32` indexes the sign table (→ §3.6) | [2.05] (formats/level-binary-client.md#sign-text-in-files) |
| line break | the token `v*eUWf` + `0x80` decodes to `#K(13)` and a newline; it is the explicit line-break marker, not a space | [test] (formats/level-binary-client.md#sign-text-in-files) |
| end | 2.05 reads signs to end of file; 2.31 stops at the first empty line, because a `HEIGHTS` block can follow | [2.05][2.31] (formats/level-binary-client.md#agreement-with-level-binarymd) |
| signs at (0,0) | common in real levels and hold dialogue text, so they are probably messages that NPC scripts show by index rather than signs on the map | [inf] (formats/level-binary-client.md#sign-text-in-files) ; [test] (client-internals/decomp-findings-2026-10-25-f/04-sign-and-chest-details.md) |
| no signs | a level with no signs ends after the chest `#`, with no empty line; in 3113 files nothing follows the signs | [test] (client-internals/decomp-findings-2026-10-25-f/01-section-shapes.md) |

### 3.1.2.7 GR-V1.04 height block

GR-V1.04 is GR-V1.03 plus an optional height map [2.31] (formats/level-binary-client.md#gr-v104-231).

```
<empty line>
HEIGHTS
h00,h01,…,h08
…                       9 lines of 9 comma-separated decimals
h80,h81,…,h88
HEIGHTSEND
```

| Rule | Detail | Source |
| --- | --- | --- |
| position | after the signs and one empty line | [2.31] (formats/level-binary-client.md#gr-v104-231) |
| reader | accepts the block after the signs whatever the magic says; matches `HEIGHTSEND` case-insensitively; keeps at most 9 rows of 9 values | [2.31] (formats/level-binary-client.md#gr-v104-231) |
| board | unchanged: 13 bits, the same run codes | [2.31] (formats/level-binary-client.md#gr-v104-231) |
| same overlay | the 9×9 grid is the `HEIGHTS` overlay that GLEVNW01 carries and TerrainGenerator writes (→ §3.1.3.5) | [2.31] (formats/level-binary-client.md#gr-v104-231) |
| meaning | a 9×9 grid fits the corners of an 8×8 grid of 8×8-tile cells on a 64×64 level | [inf] (formats/level-binary-client.md#gr-v104-231) |
| where | in 2.31, GR-V parsing appears only in the web-level cache code, the one place that client both writes and reads GR-V1.04 (→ §3.8) | [2.31] (formats/level-binary-client.md#gr-v104-231) |

### 3.1.2.8 Embedded tutorial levels (2.05)

The 2.05 executable carries the offline tutorial as 13 `RCDATA` resources, all plain `GR-V1.03` [2.05] (formats/level-binary-client.md#embedded-tutorial-levels-205):

| Resource | Level name | Source |
| --- | --- | --- |
| `TUTORIALA1` to `TUTORIALA4` | `tutorial_a-1.graal` to `tutorial_a-4.graal` | [2.05] (formats/level-binary-client.md#embedded-tutorial-levels-205) |
| `TUTORIALB1` to `TUTORIALB4` | `tutorial_b-1.graal` to `tutorial_b-4.graal` | [2.05] (formats/level-binary-client.md#embedded-tutorial-levels-205) |
| `TUTORIALB2H` | `tutorial_b-2_house.graal` | [2.05] (formats/level-binary-client.md#embedded-tutorial-levels-205) |
| `TUTORIALC1` to `TUTORIALC4` | `tutorial_c-1.graal` to `tutorial_c-4.graal` | [2.05] (formats/level-binary-client.md#embedded-tutorial-levels-205) |

| Rule | Detail | Source |
| --- | --- | --- |
| selection | when the client is not connected and the requested level name starts with `tutorial`, it opens the matching resource instead of a file on disk | [2.05] (formats/level-binary-client.md#embedded-tutorial-levels-205) |
| grid | the levels form a 3×4 grid joined by edge links; the B2 house, B4 and B2 hold all the NPCs, chests and signs | [test] (formats/level-binary-client.md#embedded-tutorial-levels-205) |
| 2.22 | 2.22 embeds 9 tutorial levels; all parse with the expected link grid, chest items and sign text | [test] (formats/grv1-decoder/README.md) |
| extraction | `tools/file-formats/extract_tutorials.py Graal.exe OUTDIR --json` writes the 13 `.graal` files and a parsed JSON for each | [src] (formats/level-binary-client.md#embedded-tutorial-levels-205) |

### 3.1.2.9 Reference decoder

`formats/grv1-decoder/grv1.py` decodes `GR-V1.00` to `GR-V1.04` and `Z3-V1.02` to `Z3-V1.04` with the rules above; NPC scripts have `0xA7` turned into newlines, and `#K(13)` is dropped from sign text [src] (formats/grv1-decoder/README.md).

## 3.1.3 GLEVNW01 (.nw)

### 3.1.3.1 File

| Rule | Detail | Source |
| --- | --- | --- |
| form | line-oriented text; the first line is the signature `GLEVNW01` | [srv] (formats/glevnw01.txt) |
| editing | official notes say to edit it in an editor that does not wrap lines | [doc] (formats/glevnw01.txt) |
| transfer | servers send the same payload as for a binary `.graal`; only the on-disk form is larger | [srv] (formats/glevnw01.txt) |

### 3.1.3.2 BOARD

```
BOARD x y width layerindex tilesdata
```

| Rule | Detail | Source |
| --- | --- | --- |
| meaning | one horizontal run of `width` tiles on the background, starting at `(x, y)` | [srv] (formats/glevnw01.txt) |
| tilesdata | `width*2` characters; each tile is a 12-bit index into the tile list (`pics1.png`), two base64 characters, high 6 bits first | [srv] (formats/glevnw01.txt) |
| alphabet | `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/`; `tile = index(left) << 6 \| index(right)` | [srv] (formats/glevnw01.txt) |
| examples | `AA` is tile 0, `AB` tile 1, `//` tile 4095 | [srv] (formats/glevnw01.txt) |
| trailing `=` | the client alphabet in the server's level code appends a `=`, which is not part of the 64-character alphabet | [srv] (formats/glevnw01.txt) |
| rejection | a line is ignored unless it has 6 tokens, the run stays inside x 0 to 63, and `tilesdata` has at least `width*2` characters | [srv] (formats/glevnw01.txt) |
| storage | the tile goes to `levelTiles[x + y*64]`; `layerindex` is parsed and not used | [srv] (formats/glevnw01.txt) |

### 3.1.3.3 Other records

| Record | Shape | Rules | Source |
| --- | --- | --- | --- |
| link | `LINK dest x y width height newx newy` | `dest`, `newx` and `newy` must not contain spaces | [srv] (formats/glevnw01.txt) |
| sign | `SIGN x y`, text lines, `SIGNEND` | the body may be empty | [srv] (formats/glevnw01.txt) |
| NPC | `NPC image x y`, script lines, `NPCEND` | `-` if the NPC has no image; x and y may be floating point | [srv] (formats/glevnw01.txt) |
| baddy | `BADDY x y type`, verse lines, `BADDYEND` | type is a name or 0 to 9; verses may be shortened, but `BADDYEND` is required | [srv] (formats/glevnw01.txt) |
| chest | `CHEST x y item signindex` | item is a name or 0 to 24, resolved by the server's item table; an unknown item drops the chest | [srv] (formats/glevnw01.txt) |

### 3.1.3.4 GSERVL01

| Rule | Detail | Source |
| --- | --- | --- |
| magic | `GSERVL01`, a second text-level signature known to the 3.x clients | [bin] (protocol/v3x-clients.md#file-formats) |
| parser | read by the same parser as GLEVNW01 | [bin] (protocol/v3x-clients.md#file-formats) |
| keywords | `BOARD`, `LINK`, `CHEST`, `SIGN`, `NPC`…`NPCEND`, `BADDY`…`BADDYEND`, `HEIGHTS`…`HEIGHTSEND`, and `REPLACENPCS`…`REPLACENPCSEND`, which the client skips | [bin] (protocol/v3x-clients.md#file-formats) |
| later builds | 4.x lists it among the magics it knows, as in 3.x | [bin] (protocol/v4x-clients.md) |

### 3.1.3.5 Other writers of the same keywords

Three tools write level text, and only two of them produce what the loader accepts [GE] (formats/glevnw01.txt):

| Writer | Output | Source |
| --- | --- | --- |
| GraalEditor | opens `*.graal` and `*.nw` with one filter and treats both as text; does not require the signature; `BOARD 0` is the tile layer as 64 lines of 64 decimal tile indices, not a base64 run; heights are a separate overlay, not a second `BOARD`; keywords `LINK`, `SIGN`, `CHEST`, `NPC`, `BADDY`, `LEVELNAMES` with fields in the order the dialogs collect them | [GE] (formats/glevnw01.txt) |
| GraalEditor compatibility | the decimal `BOARD 0` text is not what the loader accepts; it must be rewritten as GLEVNW01 base64 runs before it loads, and a client `.nw` is not a decimal grid | [GE] (formats/glevnw01.txt) |
| TerrainGenerator | GLEVNW01 with 64 rows of tile 0 (each row `64 <y>` and 128 `A`), a `HEIGHTS` block of nine lines of nine numbers closed by `HEIGHTSEND`, then a `LINK` on each edge that has a neighbour; no NPC section | [bin] (formats/glevnw01.txt) |
| DungeonGenerator | GLEVNW01 with base64 `BOARD` runs for 64 by 64 tiles, edge `LINK` lines and `NPC` blocks; stamp id 0 is replaced by a 4 by 4 ground fill before the board is stored, and stamp id 1 is a hole and is not written | [bin] (formats/glevnw01.txt) |

The tools themselves are in → §11.
