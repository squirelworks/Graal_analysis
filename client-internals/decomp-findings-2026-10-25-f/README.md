# Real GR-V1.03 levels: what two supplied files and a 3113-level archive show

Date: 2026-10-25. Derived facts only: counts, offsets and structure. No level content, names or paths.

Material: two single `GR-V1.03` levels, and an old private player-world archive with 3141 files named `.graal` (27 empty, 1 text `GLEVNW01` level under a `.graal` name, 3113 binary `GR-V1.03`, 2812 distinct by CRC-32). Every binary level was decoded with the rules in `formats/level-binary.md` and `formats/level-binary-client.md`, using a second implementation (Seihai's reader), and checked against `formats/grv1-decoder/grv1.py`.

## Verdict on the existing notes

| Note | Result |
|------|--------|
| 13-bit codes for `GR-V1.03` | Confirmed. 1998 of 3113 boards use a tile id of 2048 or more; 12 bits cannot carry them. |
| Board rules (flag bit, low-byte count, `0x100` double, runs up to 64) | Confirmed. All 3113 boards give exactly 4096 tiles; the next section starts on the next byte. 2091 files use double runs, 1809 a run of 64, none a longer one. |
| Section order and terminators | Confirmed (see 01). |
| Baddy section ends at first byte >= 0x80 | Confirmed; `grv1.py`'s extra "or x = 0" is wrong (see 03). |
| Sign alphabet, one table, `byte - 32` | Consistent; 2381 signs decode, 498 use `#K(n)` escapes (see 04). |
| GR-V1.04 `HEIGHTS` block | No file has one; nothing to confirm. |
| Link arrival "number or `playerx`/`playery`" | Incomplete (see 02). |

## Files

- `01-section-shapes.md` section layout as seen, the no-sign-section ending, coordinate units.
- `02-link-arrival-expressions.md` arrivals written as `playerY+N`.
- `03-baddy-terminator.md` x = 0 baddies and the `grv1.py` rule.
- `04-sign-and-chest-details.md` sign escapes, chest sign index -1, out-of-range positions.
- `corpus-stats.tsv` aggregate counts.
