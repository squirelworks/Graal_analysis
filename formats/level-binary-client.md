# GR-V levels as the client reads them (2.05, 2.31) and GR-V1.04

Date: 2026-10-21

Companion to `level-binary.md`, which is built from server source. This file is from the clients themselves: the 2.05 rev 2 GR-V reader and writer, and the 2.31 reader and writer. The board rules were confirmed by decoding 144 real cached levels and 13 embedded tutorial levels and re-encoding every board byte for byte. Tags: **[2.05]** · **[2.31]** · **[test]** · **[inf]** inferred.

## Corrections to `level-binary.md`

1. **Code width.** The client uses **13 bits for `GR-V1.02` and `GR-V1.03`** (and `GR-V1.04` in 2.31). `GR-V1.00`, **`GR-V1.01`** and both `Z3-V1.*` use 12 bits. `level-binary.md` puts GR-V1.01 in the 13-bit group. **[2.05]** **[2.31]**
2. **Double runs.** The 2.05 writer does emit double runs. That closes the open question. **[2.05]** **[test]**
3. **Sign terminator.** 2.05 reads signs to end of file. 2.31 stops at the first empty line, because a `HEIGHTS` block can follow. **[2.05]** **[2.31]**

## Board writer (2.05)

Walks the 4096 tiles in order and picks, at each position:

| Case | Codes emitted |
|------|---------------|
| Next tile equals this one | `0x1000 \| n`, then the tile. `n` counts up to 63 equal tiles. |
| Tiles `i, i+1` equal `i+2, i+3` (pattern AB AB) | `0x1100 \| n`, then A, then B. `n` counts up to 63 pairs. |
| Otherwise | the tile (`& 0xFFF`) |

Codes are packed 13 bits each, least significant bit first, and the last partial byte is flushed. **[2.05]** `write_board` in `tools/file-formats/gwebl.py` follows these rules and reproduces every board in the test set exactly. **[test]**

## Section rules in the client reader (2.05)

| Section | Read for |
|---------|----------|
| Links, `#`-terminated | all versions |
| Baddies, records until one whose first byte is ≥ 0x80 (the `FF FF FF` terminator) | all versions |
| NPCs, `#`-terminated | GR-V1.00 and later |
| Chests, `#`-terminated | GR-V1.01 and later |
| Signs | everything left |

A baddy record is read up to a `\n` that comes after at least 3 bytes, so the 3 binary bytes may contain `0x0A`. **[2.05]**

## Sign text in files

`sign-text.md` describes a separate "file alphabet" (`char + 89`, with `v*eUWf` + a high byte as a space). That's not what the client does. Signs in `.graal` files use **the same alphabet as signs on the wire**: `byte - 32` indexes the table

```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!?-.,#>()#####"####':/~&### <####;\n
```

and `#` entries are escape codes (`#A #B #X #Y #u #d #l #r #h #x #y #z #4 #.`). **[2.05]** The token `v*eUWf` + `0x80` decodes to `#K(13)` followed by a newline. It is the explicit line-break marker, not a space. **[test]** `sign_text` in `gwebl.py` implements this.

Signs at (0,0) are common in the test levels. They hold dialogue text, so they are probably messages that NPC scripts show by index rather than signs placed on the map. **[inf]**

## GR-V1.04 (2.31)

GR-V1.04 is **GR-V1.03 plus an optional height map**. **[2.31]**

- The writer emits `GR-V1.04` only when the level has a height map, and `GR-V1.03` otherwise.
- After the signs it writes an empty line, then:

```
HEIGHTS
h00,h01,…,h08
…                       9 lines of 9 comma-separated decimals
h80,h81,…,h88
HEIGHTSEND
```

- The reader accepts this block after the signs whatever the magic says. `HEIGHTSEND` is matched case-insensitively, and at most 9 rows of 9 values are kept.
- The 9×9 grid is the same `HEIGHTS` overlay that `GLEVNW01` carries (`glevnw01.txt`) and that TerrainGenerator writes (`tools/generators.md`). A 9×9 grid fits the corners of an 8×8 grid of 8×8-tile cells on a 64×64 level. **[inf]**
- Board coding is unchanged: 13 bits, same run codes.

In 2.31, GR-V parsing appears only in the web-level cache code. That's the one place the client both writes and reads GR-V1.04. **[2.31]**

## Embedded tutorial levels (2.05)

The 2.05 exe carries the offline tutorial as 13 `RCDATA` resources, all plain GR-V1.03: **[2.05]**

| Resource | Level name |
|----------|-----------|
| `TUTORIALA1`…`A4` | `tutorial_a-1.graal` … `tutorial_a-4.graal` |
| `TUTORIALB1`, `B2`, `B3`, `B4` | `tutorial_b-1.graal` … `tutorial_b-4.graal` |
| `TUTORIALB2H` | `tutorial_b-2_house.graal` |
| `TUTORIALC1`…`C4` | `tutorial_c-1.graal` … `tutorial_c-4.graal` |

When the client is **not connected** and the requested level's name starts with `tutorial`, it opens the matching resource instead of a file on disk. Otherwise levels come from disk. **[2.05]** The levels form a 3×4 grid joined by edge links. The house in B2, the B4 level and the B2 level hold all the NPCs, chests and signs. **[test]**

`tools/file-formats/extract_tutorials.py Graal.exe OUTDIR --json` writes the 13 `.graal` files and a parsed JSON for each.
