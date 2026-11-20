<!-- manual: kind=reference status=draft -->
# 3.5 Tile types and arrays.dat

A board stores tile ids; what a tile does is looked up in separate tables. This chapter gives the tile type values, the tile sheet geometry, the `arrays.dat` table file and the signed `arrays2.dat` with its `.sig` files. How movement uses these values is in → §4.2.

> Status: draft. Only part of the 25 `arrays.dat` tables is traced to a gameplay use; the signature key encoding is not pinned down (→ §3.5.5).

## 3.5.1 Tile sheet geometry

A tile id is a position on a sheet and nothing more. The rules below give the sheet's size and the formula from id to picture. The sheet is laid out in blocks, so the formula is not a plain row and column [src] (formats/tiletypes.txt).

| Rule | Detail | Source |
| --- | --- | --- |
| id | a board stores a tile id 0 to 4095; the client does not inspect the tileset image for collision | [src] (formats/tiletypes.txt) |
| sheet | `pics1.png` is 2048×512, palette, 128 by 32 tiles of 16 px | [file] (formats/tiletypes.txt) |
| id to picture | `col = (id % 16) + (id // 512) * 16`, `row = (id // 16) % 32`, source rectangle `(col*16, row*16, 16, 16)`: the sheet is eight side-by-side blocks of 512 ids, each 16 columns by 32 rows, filled row by row; an earlier rule `col = id % 128`, `row = id / 128` draws noise and is wrong (settled below) | [file] (client-internals/client-assets.md#tile-sheets) |

**Settled question, formerly E#102: tile id to pixel position on pics1.** Which formula maps a tile id to its place on `pics1.png` had two answers on record; a render test settled it [test] (formats/pics1-tile-layout-render-2026-11-19.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A (false) | `col = id % 128`, `row = id / 128` | [file] (formats/tiletypes.txt) |
| Claim B (holds) | `col = (id % 16) + (id // 512) * 16`, `row = (id // 16) % 32`: eight side-by-side blocks of 512 ids, each 16 columns by 32 rows; the Windows 4.04r2 draw path computes it | [file] (client-internals/client-assets.md#tile-sheets); [bin] (client-internals/windows-404r2-500r7-static-2026-11-09.md#404r2-tile-sheet-layout) |
| Settled | Two real `GR-V1.03` levels drawn with a real sheet: Claim B gives coherent rooms with every cell on the sheet; Claim A puts 2660 and 3736 of 4096 cells off the sheet and draws noise. `formats/tiletypes.txt` is corrected | [test] (formats/pics1-tile-layout-render-2026-11-19.md) |
| Verdict | Verified | [test] (formats/pics1-tile-layout-render-2026-11-19.md) |

## 3.5.2 Tile type values

The official tile type names, as documented for `setshape2` in the 2001 feature notes [doc] (formats/tiletypes.txt):

| Type | Official name | Source |
| --- | --- | --- |
| 0 | nonblocking | [doc] (formats/tiletypes.txt) |
| 2 | hurting underground | [doc] (formats/tiletypes.txt) |
| 3 | chair | [doc] (formats/tiletypes.txt) |
| 4 | bed, upper side | [doc] (formats/tiletypes.txt) |
| 5 | bed, lower side | [doc] (formats/tiletypes.txt) |
| 6 | swamp | [doc] (formats/tiletypes.txt) |
| 7 | lava swamp | [doc] (formats/tiletypes.txt) |
| 8 | near water | [doc] (formats/tiletypes.txt) |
| 9 | near lava | [doc] (formats/tiletypes.txt) |
| 11 | water | [doc] (formats/tiletypes.txt) |
| 12 | lava | [doc] (formats/tiletypes.txt) |
| 20 | throw-through (fences) | [doc] (formats/tiletypes.txt) |
| 21 | jumping stone | [doc] (formats/tiletypes.txt) |
| 22 | blocking tile | [doc] (formats/tiletypes.txt) |

**Settled question, formerly E#614: tiledef type 4 consumer.** What a type-4 tiledef line does was open: such lines are common in 2.22 install tiledefs, but the walk-kind switch names only 0, 1|2 and 5. A live 2.22 run settled it [lab] (formats/tiledef-type4-2026-11-16.md#live-result-2026-11-19).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A (holds) | Install type-4 rows store pixel x offsets (and sometimes y) beside a replacement image and a level prefix; the 2.22 adventure file keeps the default row `pics1.png,,0,0,0` and about seventeen type-4 overrides with x in 1344, 1536 or 1728 (16-pixel columns 84, 96, 108 of the 2048 × 512 sheet) and y 0 or 80 | [file][bin] (formats/tiledef-type4-2026-11-16.md) |
| Claim B (holds) | Walk kinds for tilesets are 0, 1\|2 and 5; type 4 is not among them | [2.22] (client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md) |
| Settled | Draw only: type 4 pastes its image into the tile sheet at pixel (x, y) and leaves the stock sheet elsewhere; walking follows the board's tile codes, so a rock row blocks the same with or without the overlay. The image must be an 8-bit palette PNG; a 24-bit one is ignored without a message, which is why the earlier tries saw nothing | [lab] (formats/tiledef-type4-2026-11-16.md#live-result-2026-11-19) |
| Left over | Water under an overlay, and type-4 lines on builds other than 2.22 | [inf] (formats/tiledef-type4-2026-11-16.md#open) |

### 3.5.2.1 A 4096-byte type table

A 4096-byte table copied from the standard tileset, one type byte per id, is kept in an outside client's source and written as `tiledefs.txt`: decimal, row-major, 128 values per line (the width of `pics1.png`) [src] (formats/tiletypes.txt). Its counts:

| Value | Count | Official meaning | Source |
| --- | ---: | --- | --- |
| 0 | 823 | nonblocking | [src] (formats/tiletypes.txt) |
| 3 | 40 | chair | [src] (formats/tiletypes.txt) |
| 4 | 4 | bed, upper | [src] (formats/tiletypes.txt) |
| 5 | 4 | bed, lower | [src] (formats/tiletypes.txt) |
| 6 | 12 | swamp | [src] (formats/tiletypes.txt) |
| 7 | 8 | lava swamp | [src] (formats/tiletypes.txt) |
| 8 | 30 | near water | [src] (formats/tiletypes.txt) |
| 11 | 47 | water | [src] (formats/tiletypes.txt) |
| 12 | 67 | lava | [src] (formats/tiletypes.txt) |
| 20 | 129 | throw-through fence | [src] (formats/tiletypes.txt) |
| 21 | 18 | jumping stone | [src] (formats/tiletypes.txt) |
| 22 | 2914 | blocking | [src] (formats/tiletypes.txt) |

The rules below add what the counts leave out: the types missing from the table, how its first row reads, and how that outside client tests a tile. It is not the official client's method, which follows in §3.5.2.2 [src] (formats/tiletypes.txt).

| Rule | Detail | Source |
| --- | --- | --- |
| absent types | types 2 and 9 are in the official list but do not appear in this table | [src] (formats/tiletypes.txt) |
| first row | the first data line, ids 0 to 127, starts `0,0,20,20,…`: the top-left two tiles walk and the next two are walls | [src] (formats/tiletypes.txt) |
| that client's tests | wall if the type byte is ≥ 20 or the foot is outside the 64×64 board; water if it is 11; walkable otherwise | [src] (formats/tiletypes.txt) |

### 3.5.2.2 Sheet types and the type-0 allow lists (official client)

The official client decides walkability differently for each kind of sheet. The rules below come from live tests: how sheets are listed and chosen, and the two allow lists that decide a type-0 tile [live] (formats/tile-walk.md#sheet-loading).

| Rule | Detail | Source |
| --- | --- | --- |
| tile definition list | each entry is `image,prefix,type` with optional `x,y` offsets; the default is `pics1.png` of type 0, stock selection `pics1.png,,0` | [live] (formats/tile-walk.md#sheet-loading); [bin] (formats/tiletypes.txt) |
| sheet order | type 0 is the old Graal tile order (`pics1`), type 1 the new order; `addtiledef2` paints a rectangle on top of the base sheet; the offline tree holds `picso.png,offlinetutorial,1,0,0` | [file] (client-internals/client-assets.md#tiledef) |
| sheet choice | a level may reference several sheets; the active one is selected when the level is entered | [live] (formats/tile-walk.md#sheet-loading) |
| type-0 sheet | a tile walks only if its 12-bit id is in one of two internal allow lists (the "nowall" lists); an id in neither blocks | [live] (formats/tile-walk.md#collision-rules); [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| allow lists | built when the sheet loads; not stored in `tiledefs.txt`, which names only the sheet, prefix and type; they are arrays 0 and 1 of `arrays.dat` (→ §3.5.3) | [live] (formats/tile-walk.md#type-0-allow-lists); [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| type 1 and 2 sheets | consult a fixed 0/1 body-block grid; one extraction counted 1725 blocked and 2371 walkable cells | [live] (formats/tile-walk.md#collision-rules); [bin] (formats/tiletypes.txt) |
| type-0 mask | `retired → §3.5.3.1` | [live] (formats/tile-walk.md#type-0-allow-lists) |
| `setshape2` | blocks the body when the shape-tile type is greater than 19 | [bin] (formats/tiletypes.txt) |
| throw | throw handling does not stop on type `0x14` (20) | [bin] (formats/tiletypes.txt); [live] (formats/tile-walk.md#collision-rules) |
| water | type 11 does not block; it changes the displayed tile and may set a swimming flag | [live] (formats/tile-walk.md#collision-rules) |

The Bush-value membership correction is recorded in → §3.5.3.1; runtime collision is settled below (stamped bushes block) [file] (formats/arrays-membership-2026-11-09.md#what-the-counts-settle).

**Settled question, formerly E#100: Collision of the Bush stamp tiles.** Whether a bush placed with the editor's Bush stamp blocks the player was open, because the inspected arrays are not the collision path. A lab walk settled it [lab] (protocol/lab-appe-mirae-2026-11-20c.md#bush-tiles-placed-as-a-stamp-e100).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | Tile ids 2, 3, 18 and 19 placed as a 2 × 2 bush stop a player walking up into them at the same point as a rock, from both half-tile alignments, on 2.22 and on 2.05 rev 2 with the stock `pics1.png` | [lab] (protocol/lab-appe-mirae-2026-11-20c.md#bush-tiles-placed-as-a-stamp-e100) |
| Verdict | Verified on 2.22 and 2.05 rev 2: a stamped bush blocks like a bush drawn into the board | [lab] (protocol/lab-appe-mirae-2026-11-20c.md#bush-tiles-placed-as-a-stamp-e100) |

## 3.5.3 arrays.dat

`arrays.dat` is a tree of integer arrays with a small header on each. The rules below give the encoding needed to walk it [2.05] (formats/arrays-and-signatures.md#arraysdat).

| Rule | Detail | Source |
| --- | --- | --- |
| integers | big-endian 32-bit | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| array header | `header = (kind << 16) \| count` | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| kind 0 | `count` int32 values follow | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| kind 1 | `count` nested arrays follow, each with its own header | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| order | the client reads exactly 25 arrays in a fixed order into 25 globals at startup | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| missing file | the client quits with "File not found"; the file is not signed or checked | [2.05] (formats/arrays-and-signatures.md#summary) |
| 2.22 file | 11500 bytes; parses to exactly 25 arrays with nothing left over | [test] (formats/arrays-and-signatures.md#arraysdat) |
| tile ids | all tile ids in the tables index the 4096-tile `pics1` sheet | [2.05] (formats/arrays-and-signatures.md#arraysdat) |

The table lists the top-level arrays of the 2.05 file in order, with each one's size and what it is known to hold. Rows that say "use not traced" are arrays whose reader has not been found [2.05] (formats/arrays-and-signatures.md#arraysdat).

| # | Shape | Content | Source |
| --- | --- | --- | --- |
| 0 | 934 ints, max 4089 | tile ids; with array 1, the legacy walkability test: in the old tile mode a tile blocks unless it is in array 0 or array 1 | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| 1 | 116 ints | tile ids, second list for that test | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| 2 | 133 ints | tile ids; use not traced | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| 3 | 76 ints | tile ids; use not traced | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| 4 | 40 ints | tile ids; use not traced | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| 5, 6 | 4 ints each | single 2×2 tile blocks (708–711, 724–727); use not traced | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| 7 | 79 ints | tile ids; the legacy tile-type lookup maps a tile's position in this list to 4 classes (positions 0–11, 12–19, 20–62, 63+); the newer tile-type path returns types 6 to 9 for the same classes | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| 8 | 4 lists, one per facing | ledge tiles (type 21): a ledge jump needs the tile to be in the list for the player's facing | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| 9 to 12 | small nested lists of 2×2 tile groups | level-object code: cut and lift | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| 13 | 4 ints | one 2×2 tile block, used with array 14 | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| 14, 15 | small nested lists of 2×2 tile groups | level-object code | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| 16 | 2 × 2×2 blocks | stone blocks: entry 0 pushable, entry 1 pullable | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| 17 | 124 × 4 | packed records used by the horse object | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| 18 | nested | use not traced | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| 19 | nested | used by the leap object | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| 20, 22, 23 | nested | used by the baddy AI object | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| 21 | 4 × 4 | packed values; use not traced in detail | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| 24 | 356 ints, packed | used by the item, bomb and extras objects | [2.05] (formats/arrays-and-signatures.md#arraysdat) |

Meanings read from the uses in the 2.22 client [bin] (client-internals/decomp-findings-2026-10-25-l/02-arrays-dat.md#arrays-index--position-in-the-file):

| # | Content (2.22) | Source |
| --- | --- | --- |
| 0 | passable tile ids; any other tile is a wall (→ §3.5.3.1) | [bin] (client-internals/decomp-findings-2026-10-25-l/02-arrays-dat.md#arrays-index--position-in-the-file) |
| 1 | liquid tile ids, water and lava | [bin] (client-internals/decomp-findings-2026-10-25-l/02-arrays-dat.md#arrays-index--position-in-the-file) |
| 3 | the liquid tiles that are lava | [bin] (client-internals/decomp-findings-2026-10-25-l/02-arrays-dat.md#arrays-index--position-in-the-file) |
| 9, 10 | cuttable 2×2 objects and the tiles a cut leaves, indexed type, column, row: the bush `2 3 / 18 19` and `420 421 / 436 437` | [bin] (client-internals/decomp-findings-2026-10-25-l/02-arrays-dat.md#arrays-index--position-in-the-file) |
| 11, 12 | liftable 2×2 objects and the tiles a lift leaves: five types, among them the bush and the rock `34 35 / 50 51` | [bin] (client-internals/decomp-findings-2026-10-25-l/02-arrays-dat.md#arrays-index--position-in-the-file) |
| 13 | closed chest tiles 1784, 1785, 1800, 1801 | [bin] (client-internals/decomp-findings-2026-10-25-l/02-arrays-dat.md#arrays-index--position-in-the-file) |
| 14 | open chest tiles 829, 845 / 830, 846 | [bin] (client-internals/decomp-findings-2026-10-25-l/02-arrays-dat.md#arrays-index--position-in-the-file) |

A loader that reads only the first four arrays as flat lists is right for 0 to 3 and misses the nested arrays 9 to 12 [bin] (client-internals/decomp-findings-2026-10-25-l/02-arrays-dat.md#arrays-index--position-in-the-file).

### 3.5.3.1 Bounded packaged-file membership

One packaged `arrays.dat` was read exactly to settle which tile ids are in its first two lists. Each rule records part of that reading and how far it reaches [file] (formats/arrays-membership-2026-11-09.md#structure-and-exact-input).

| Rule | Detail | Source |
| --- | --- | --- |
| identity | 11,500-byte input, researcher-supplied SHA-256 b65905ad1e1d1e48d2b7841525c749272426e5160d187f05e8d6b37946296927; appears in 2.22-labelled and 2.3-labelled packages and a loose copy; release identity and runtime loading are unverified | [file] (formats/arrays-membership-2026-11-09.md#structure-and-exact-input) |
| structure | 25 top-level arrays, no trailing bytes; list 0/list 1 mean the first two structural positions, not runtime categories | [file] (formats/arrays-membership-2026-11-09.md#structure-and-exact-input) |
| first lists | 934 and 116 internally unique values; 15 shared; union 1,035 values within 0–4095; list 1 contributes 101 values absent from list 0 | [file] (formats/arrays-membership-2026-11-09.md#structure-and-exact-input) |
| Bush values | 2, 3, 18 and 19 are absent from both lists, also in all 25 successfully parsed distinct inputs; file membership does not establish runtime collision | [file] (formats/arrays-membership-2026-11-09.md#structure-and-exact-input) |
| collection validation | 53 occurrences, 26 hashes; 25 parse completely and reproduce original bytes on re-encoding; an unsupported 39ster-labelled representation is excluded; other inputs have different shapes and counts | [file] (formats/arrays-membership-2026-11-09.md#structure-and-exact-input) |
| remaining scope | no consuming path or runtime movement was checked; earlier consumer evidence retains its original build scope; the earlier mask count is retired (→ §3.5.3.1) (stamped-bush collision is settled in §3.5.2.2); the 2.05 old-mode walk test checks list 0 and then list 1, and no other (→ §3.5.3.1) | [file] (formats/arrays-membership-2026-11-09.md#what-the-counts-settle); [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#arraysdat-lists-in-the-old-mode-walk-test-e608-205) |

**Settled question, formerly E#608: how many `arrays.dat` lists make a tile passable.** How many `arrays.dat` lists decide whether a tile is walkable was open between a summary and a code read; a static read of the consumer settled it for 2.05 [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#arraysdat-lists-in-the-old-mode-walk-test-e608-205).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: the first array supplies passable tiles and all others are walls. B: the old-mode 2.05 path checks arrays 0 and 1 | [doc] (CONSOLIDATED.md#tiles); [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| Settled | The loader reads 25 lists; the old-mode passability test checks list 0 and, on a miss, list 1, and no other | [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#arraysdat-lists-in-the-old-mode-walk-test-e608-205) |
| Verdict | Verified by static read: Claim B holds; Claim A dropped list 1 | [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#arraysdat-lists-in-the-old-mode-walk-test-e608-205) |

**Settled question, formerly E#101: Size of the type-0 allow lists.** Whether an earlier mask count of walkable tiles describes the `arrays.dat` lists was open, because no one had traced the count to its producer. A search of every held folder and archive settled it [file] (client-internals/static-reads-appendix-e-2026-11-20-l.md#the-earlier-type-0-mask-export-e101).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: one exported type-0 mask counted 3,195 non-blocking and 682 blocking tiles. B: the exact `arrays.dat` lists give a union of 1,035 | [live] (formats/tile-walk.md#type-0-allow-lists); [file] (formats/arrays-membership-2026-11-09.md#structure-and-exact-input) |
| Settled | No export or script behind Claim A exists in any held folder or archive; the sentence entered the notes on 2026-10-14 with no data file. Its counts match neither the `arrays.dat` lists, nor the GServer-v2 fork's `Type0` and `Type1` tables, nor the pixels of the 2.22 `pics1.png`; 3,195 + 682 is 219 short of 4,096 | [file] (client-internals/static-reads-appendix-e-2026-11-20-l.md#the-earlier-type-0-mask-export-e101) |
| Verdict | Claim A is retired; Claim B's 1,035 stands. Side finding: 1,035 is also the number of `Type0` ids below 20 in the fork's table (counts only, membership unchecked) | [file] (client-internals/static-reads-appendix-e-2026-11-20-l.md#the-earlier-type-0-mask-export-e101) |

## 3.5.4 arrays2.dat

2.05 does not reference `arrays2.dat`, `graal.sig` or `arrays2.sig` and has no signature check [2.05] (formats/arrays-and-signatures.md#summary). In 2.17, 2.22 and 2.31 the file is plain text with CRLF lines, numbered from 0; 2.22 needs at least 5 lines [2.22] (formats/arrays-and-signatures.md#arrays2dat).

| Line | Use | Source |
| --- | --- | --- |
| 0 | main listserver host | [2.22] (formats/arrays-and-signatures.md#arrays2dat) |
| 1 | listserver port | [2.22] (formats/arrays-and-signatures.md#arrays2dat) |
| 2 | web host, joined into a URL template | [inf] (formats/arrays-and-signatures.md#arrays2dat) |
| 3 | registration page URL | [2.22] (formats/arrays-and-signatures.md#arrays2dat) |
| 4 | translation service URL | [2.22] (formats/arrays-and-signatures.md#arrays2dat) |
| 5, 6 | fallback listserver hosts, optional | [2.22] (formats/arrays-and-signatures.md#arrays2dat) |

A fan-server copy of the file points line 0 at its own `<listserver-host>` with port 14922 and lists two other list hosts as fallbacks [test] (formats/arrays-and-signatures.md#arrays2dat). The 2.05 list host is hidden in the executable instead (→ §6).

## 3.5.5 graal.sig and arrays2.sig

Two 128-byte signature files guard the executable and `arrays2.dat`. The rules below give what is known of the key, the order of checks and the algorithm, and which parts are judged from names alone [test] (formats/arrays-and-signatures.md#the-signatures).

| Rule | Detail | Source |
| --- | --- | --- |
| size | both files are 128 bytes, the size of an RSA-1024 signature | [test] (formats/arrays-and-signatures.md#the-signatures) |
| key | built at startup from an obfuscated hex string assembled one character at a time; each decoded byte is `not(b) - 10`. In 2.22 the 1,024 characters decode (hex, byte order reversed, then `not(b) - 10`) to 512 hex characters, a 2,047-bit modulus, which would want 256-byte signatures | [2.22] (formats/arrays-and-signatures.md#the-signatures), [bin] (client-internals/static-reads-appendix-e-2026-11-20-k.md#the-key) |
| order | `graal.sig` is verified against the client's own executable file, then `arrays2.sig` against `arrays2.dat` | [2.22] (formats/arrays-and-signatures.md#the-signatures) |
| algorithm | key at least 89 bits; signature exactly (bits + 7) / 8 bytes; m = s^e mod n compared with `01 FF … FF 00` and the 20-byte SHA-1 of the data, (bits − 1) / 8 bytes, with no DigestInfo; no signature has been seen to verify | [bin] (client-internals/static-reads-appendix-e-2026-11-20-k.md#the-verify-routine-a) |
| failure | the client shows "The Graal execution file is corrupted. Please check for viruses or other programs that manipulate…" and exits | [2.22] (formats/arrays-and-signatures.md#the-signatures) |
| builds | 2.17, 2.22 and 2.31 embed the same two key strings and the same error text | [2.17][2.22][2.31] (formats/arrays-and-signatures.md#the-signatures) |
| open | the only held `.sig` files are the Reborn package's 128-byte files, which the 2,047-bit key would reject on size; where the exponent is set and what the second key string does are not read | [test] (formats/arrays-and-signatures.md#the-signatures), [bin] (client-internals/static-reads-appendix-e-2026-11-20-k.md#not-covered) |
| fan-server 2.22 | that executable has the four guards of the verify routine rewritten so verification always passes; the 2.17 and 2.31 executables do not | [2.22][2.17][2.31] (formats/arrays-and-signatures.md#the-graal-reborn-222-exe-has-the-check-disabled) |
| consequence | an unpatched 2.17, 2.22 or 2.31 client refuses an edited `arrays2.dat` or executable; editing `arrays2.dat` alone fails the signature | [inf] (formats/arrays-and-signatures.md#the-graal-reborn-222-exe-has-the-check-disabled) |

### 3.5.5.1 A separate four-guard variant comparison

Two retained Windows inputs reporting 2.2.2.0 differ at four branch conditions in one RSA-verification routine. In input A, the conditions guard minimum key size, supplied signature size, a verification helper's result and a final comparison. Input B replaces each condition with an unconditional branch to the same destination, skipping the associated error path. This is a static code comparison, not measured signature acceptance [bin] (formats/windows-222-verifier-variants.md#what-the-four-edits-change).

The earlier community-control patch and this A-to-B result are the same four edits: the control is B with four labels renamed [bin] (client-internals/static-reads-appendix-e-2026-11-20-k.md#how-the-three-inputs-relate).

**Settled question, formerly E#103: What the four 2.22 verifier guards mean.** Whether the four unconditional guards change which files a client accepts, and how the variant relates to the community control, was open. A read of input A and a byte comparison of all three inputs settled it [bin] (client-internals/static-reads-appendix-e-2026-11-20-k.md#what-this-settles).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | A against the control differs in 34 bytes in eight ranges: the four guards, and the labels `Graal Gold`, `Classic`, `Hosted` and `Graal2002` renamed `Gold`, `Silver`, `Bronze` and `Graal Reborn`. B is A with the guards alone patched; the control is B with the renames. The earlier "three branches" was four | [bin] (client-internals/static-reads-appendix-e-2026-11-20-k.md#how-the-three-inputs-relate) |
| Settled | The verify routine is reached at start-up, for `graal.sig` against the executable and then `arrays2.sig` against `arrays2.dat`; a failure ends in the "corrupted" message | [bin] (client-internals/static-reads-appendix-e-2026-11-20-k.md#where-the-check-runs) |
| Settled | The routine checks key size, signature size, then compares s^e mod n with `01 FF … 00` and the SHA-1 of the data, without DigestInfo. Its helper always succeeds, so the third guard never fires even unpatched. With all four guards jumped, every file and signature passes | [bin] (client-internals/static-reads-appendix-e-2026-11-20-k.md#the-verify-routine-a) |
| Verdict | Verified by read: A is the unpatched build and B is a patched build that accepts unsigned files, the best guess. No PM or GS1 conclusion follows | [bin][inf] (client-internals/static-reads-appendix-e-2026-11-20-k.md#what-this-settles) |
| Left over | Where the exponent is set, the second key string, and whether an official release carried 256-byte signatures; no unpatched signature is held | [inf] (client-internals/static-reads-appendix-e-2026-11-20-k.md#not-covered) |

The check as a client integrity behaviour is in → §4.10.
