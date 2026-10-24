# What a GR-V1 section reader gets wrong on Z3-V1

A section reader written for `GR-V1.03` (integer links, three-byte baddy records, an NPC and a chest section where `Z3-V1` has none) was replayed over the 139 distinct files. Counts:

| Fault | Effect | Count |
|-------|--------|-------|
| Link numbers parsed as integers | decimal links dropped | 124 links in 47 `Z3-V1.03` files |
| Computer line end left in the stream | next record starts one byte late; the type byte of the record and the line end shift | all 31 `Z3-V1.03` files that have computers (one file: 14 computers reported, 10 present) |
| Negative arrival read as a literal coordinate | arrival at -1 | 151 links (also 805 `GR-V1` links) |
| `.zelda` extension treated as a promise | `GR-V1` files read as `Z3-V1` | 694 distinct files under `.zelda` names are `GR-V1` |

After switching to a strict reader every one of the 663 copies parses to exactly the end of the file with no leftover bytes and no anomaly.
