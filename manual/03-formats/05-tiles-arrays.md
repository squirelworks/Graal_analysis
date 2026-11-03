<!-- manual: kind=reference status=draft -->
# 3.5 Tile types and arrays.dat

A board stores tile ids; what a tile does is looked up in separate tables. This chapter gives the tile type values, the tile sheet geometry, the `arrays.dat` table file and the signed `arrays2.dat` with its `.sig` files. How movement uses these values is in → §4.2.

> Status: draft. Only part of the 25 `arrays.dat` tables is traced to a gameplay use; the signature key encoding is not pinned down (→ §3.5.5).

## 3.5.1 Tile sheet geometry

| Rule | Detail | Source |
| --- | --- | --- |
| id | a board stores a tile id 0 to 4095; the client does not inspect the tileset image for collision | [src] (formats/tiletypes.txt) |
| sheet | `pics1.png` is 2048×512, palette, 128 by 32 tiles of 16 px | [file] (formats/tiletypes.txt) |
| id to picture | `col = id % 128`, `row = id / 128`, pixel `(col * 16, row * 16)` | [file] (formats/tiletypes.txt) |

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

| Rule | Detail | Source |
| --- | --- | --- |
| absent types | types 2 and 9 are in the official list but do not appear in this table | [src] (formats/tiletypes.txt) |
| first row | the first data line, ids 0 to 127, starts `0,0,20,20,…`: the top-left two tiles walk and the next two are walls | [src] (formats/tiletypes.txt) |
| that client's tests | wall if the type byte is ≥ 20 or the foot is outside the 64×64 board; water if it is 11; walkable otherwise | [src] (formats/tiletypes.txt) |

### 3.5.2.2 Sheet types and the type-0 allow lists (official client)

| Rule | Detail | Source |
| --- | --- | --- |
| tile definition list | each entry is `image,prefix,type` with optional `x,y` offsets; the default is `pics1.png` of type 0, stock selection `pics1.png,,0` | [live] (formats/tile-walk.md#sheet-loading); [bin] (formats/tiletypes.txt) |
| sheet choice | a level may reference several sheets; the active one is selected when the level is entered | [live] (formats/tile-walk.md#sheet-loading) |
| type-0 sheet | a tile walks only if its 12-bit id is in one of two internal allow lists (the "nowall" lists); an id in neither blocks | [live] (formats/tile-walk.md#collision-rules); [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| allow lists | built when the sheet loads; not stored in `tiledefs.txt`, which names only the sheet, prefix and type; they are arrays 0 and 1 of `arrays.dat` (→ §3.5.3) | [live] (formats/tile-walk.md#type-0-allow-lists); [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| type 1 and 2 sheets | consult a fixed 0/1 body-block grid; one extraction counted 1725 blocked and 2371 walkable cells | [live] (formats/tile-walk.md#collision-rules); [bin] (formats/tiletypes.txt) |
| type-0 mask | `disputed → App. E#101` | [live] (formats/tile-walk.md#type-0-allow-lists) |
| `setshape2` | blocks the body when the shape-tile type is greater than 19 | [bin] (formats/tiletypes.txt) |
| throw | throw handling does not stop on type `0x14` (20) | [bin] (formats/tiletypes.txt); [live] (formats/tile-walk.md#collision-rules) |
| water | type 11 does not block; it changes the displayed tile and may set a swimming flag | [live] (formats/tile-walk.md#collision-rules) |

The 2×2 Bush stamp ids 2, 3, 18 and 19 are walls in the 4096-byte table and walkable through the type-0 allow lists `disputed → App. E#100`.

## 3.5.3 arrays.dat

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

| Rule | Detail | Source |
| --- | --- | --- |
| size | both files are 128 bytes, the size of an RSA-1024 signature | [test] (formats/arrays-and-signatures.md#the-signatures) |
| key | built at startup from an obfuscated hex string assembled one character at a time; each decoded byte is `not(b) - 10` | [2.22] (formats/arrays-and-signatures.md#the-signatures) |
| order | `graal.sig` is verified against the client's own executable file, then `arrays2.sig` against `arrays2.dat` | [2.22] (formats/arrays-and-signatures.md#the-signatures) |
| algorithm | an RSA component configured with a SHA-1 signing digest and a PKCS#1 scheme, judged from the component's class and property names; no signature has been verified | [inf] (formats/arrays-and-signatures.md#the-signatures) |
| failure | the client shows "The Graal execution file is corrupted. Please check for viruses or other programs that manipulate…" and exits | [2.22] (formats/arrays-and-signatures.md#the-signatures) |
| builds | 2.17, 2.22 and 2.31 embed the same two key strings and the same error text | [2.17][2.22][2.31] (formats/arrays-and-signatures.md#the-signatures) |
| open | checking the shipped signatures against the decoded key with exponents 3, 17 and 65537 did not reproduce PKCS#1 padding; the key encoding is not pinned down | [test] (formats/arrays-and-signatures.md#the-signatures) |
| fan-server 2.22 | that executable has the three branches that raise the verify error rewritten so verification always passes; the 2.17 and 2.31 executables do not | [2.22][2.17][2.31] (formats/arrays-and-signatures.md#the-graal-reborn-222-exe-has-the-check-disabled) |
| consequence | an unpatched 2.17, 2.22 or 2.31 client refuses an edited `arrays2.dat` or executable; editing `arrays2.dat` alone fails the signature | [inf] (formats/arrays-and-signatures.md#the-graal-reborn-222-exe-has-the-check-disabled) |

The check as a client integrity behaviour is in → §4.10.
