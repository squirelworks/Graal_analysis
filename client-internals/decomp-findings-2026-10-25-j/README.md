# Z3-V1 (`.zelda`) levels: format checked against 139 real files and three clients

Date: 2026-10-25. Derived facts only: counts, offsets and structure. No level content, names, paths or code addresses.

Material: the old client builds' level folders (1st Graal to 15th Graal, Graal 1.1 and 1.1.9, the 2nd/4th "alpha" folders, and the Java Zelda Online game folder with its source), which hold 663 `Z3-V1` files (139 distinct by content). Each file was decoded twice, with a throwaway Python scanner built on `formats/grv1-decoder/grv1.py` and with Seihai's new strict Rust reader, and the two agreed. The Java Zelda Online source, the 1st Graal client and the 1.39 client were read for the loader rules (derived facts only; no decompile text is kept here). A private player-world archive was counted for comparison.

## Verdict on the existing notes

| Note | Result |
|------|--------|
| Sections: board, links, baddies, signs; no NPC and no chest section | Confirmed. All 139 distinct files end exactly at the end of the signs. |
| 12-bit codes for `Z3-V1.03` / `.04` | Confirmed (all 139 boards give 4096 tiles and the links start on the next byte). |
| Verse line only in `Z3-V1.04` | Confirmed, with detail: see 01. `Z3-V1.03` records have an empty rest-of-line, so every record is 4 bytes (3 + line end), as in the Java source. |
| Baddy terminator `FF FF FF` + line end | Confirmed. |
| Links `dest x y w h newx newy` | Incomplete: `Z3-V1.03` writes decimals and `-1` arrivals (see 02). |
| `Z3-V1.02` | Only the Java client reads it; no real file has it. |
| "Only GR-V1.00 to 1.03 load, `.zelda` Z3-V1 for the offline levels" (1.33 to 1.39) | Incomplete. Every Graal client binary from 1.28b2 to 2.31 carries both `Z3-V1.03` and `Z3-V1.04` magics, and the 1st Graal and 1.39 loaders accept them whatever the file name. |

## Files

- `01-record-shapes.md` board, link, computer and sign records as seen; computer types; `Z3-V1.04` verses.
- `02-links-and-arrivals.md` decimal links, negative arrivals, destination extensions.
- `03-extensions-and-magic.md` which names hold which magic; what the loaders key on.
- `04-loader-rules-compared.md` Java, 1st Graal and 1.39 rules side by side, with the differences that matter.
- `05-old-reader-failures.md` what a `.graal`-style section reader gets wrong on `Z3-V1` (counts).
- `by-build.tsv` per-build counts (18 builds).
- `format-stats.tsv` aggregate counts over the 139 distinct files.

## Open

- Which build tries `.zelda` for a bare level name, and whether a missing `.zelda` link falls back to the `.graal` of the same stem. No binary traced says.
- The 2.0 to 2.31 loaders were checked for the magic strings only, not traced.
- Java sign alphabet versus the shared one for codes 82 to 88 (5 real signs touch 82 or 83; not compared).
- Computer type names beyond the Java source's 0 to 6 (none seen).
- No `Z3-V1.02` sample.
