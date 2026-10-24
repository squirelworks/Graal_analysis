# Record shapes seen in the real files

Counts are over the 139 distinct files (85 `Z3-V1.03`, 54 `Z3-V1.04`); see `format-stats.tsv`.

## Layout

```text
char[8]  magic      Z3-V1.03 | Z3-V1.04
bits     board      4096 tiles, 12-bit codes, run rules of GR-V1.00 (formats/level-binary.md)
text     links      `dest x y w h newx newy` lines, then a line holding `#`
binary   computers  x y type (3 raw bytes) + rest of line; ends at a first byte >= 0x80
text     signs      `x+32 y+32 text` lines until an empty line or the end of the file
```

All 139 files end with a line end. Sizes run 443 to 5369 bytes (median 1919).

## Computers ("baddies")

- Zelda Online calls them computers. A record is `x`, `y`, `type`, then the rest of the line and a line end. `x` and `y` are raw tile bytes (not the +32 of signs); no coordinate is 64 or more.
- `Z3-V1.03`: the rest of the line is empty in all 124 records, so a record is 4 bytes.
- `Z3-V1.04`: the rest of the line holds three verses separated by backslashes (sight, hurt, attack). 45 of the 45 records carry the verse form, 40 of them with all three verses empty (two backslashes only).
- Types are 0 to 6 in every file. Counts over all records: type 0 29, 1 29, 2 30, 3 23, 4 33, 5 5, 6 20. The Java source names them: green soldier, blue soldier, red soldier, shot soldier, swamp soldier, jumping hare, octopus. Later builds' names for the numbers are not known.
- Two records (both `Z3-V1.03`) have `0x0A` as x or y. They are data, not a line end: a reader that finds the line end before taking three bytes ends the section there.
- The section ends at `FF FF FF` and a line end (the first byte is the test: any value of 0x80 or more). 42 files have computers, 97 have none and go straight to the terminator.

## Signs

- 120 signs in 63 files. `x+32`, `y+32`, then text in the shared packed alphabet (`formats/sign-text.md`). No empty sign text.
- 86 signs contain a byte of 0x80 or more where a line break goes (as in `GR-V1`).
- 5 signs contain alphabet code 82 or 83; the Java source reads codes 82 to 88 differently (see README, open items).
- The sign list ends at an empty line or at the end of the file; every real file ends at a line end after the last sign.
