# Loader rules compared

Three readers were compared for the points where a re-implementation can go wrong. "Delphi clients" means 1st Graal and 1.39, which agree on every row unless stated.

| Point | Java Zelda Online | Delphi clients | Real files |
|-------|-------------------|----------------|------------|
| Code width | 11 bits for `Z3-V1.02`, 12 for `.03` | 12 for `Z3-V1.03/.04` | 12 (no `.02`) |
| Control code | top bit set, low byte count, `0x100` double | same | same, 4096 tiles in all |
| Double flag | stays set until a double run completes | not separated | the `GR-V1` reader clears it at the next control code; no file shows a difference (0 of 663) |
| Link numbers | six doubles | six floats | decimals present |
| Negative arrival | "constant" flag from `< 0` | same | 151 links |
| Computer record | 4 fixed bytes read as x, y, type, line end (`Z3-V1.03` form) | 1.39: bytes are added until a line end after 3 or more bytes; a first byte below 0x80 starts a record. 1st Graal reads by line (inferred from its shape) | all `.03` records have an empty rest |
| `0x0A` as x or y | harmless (fixed bytes) | harmless in the 1.39 loader (it keeps adding bytes until the line is longer than 2); 1st Graal would end the section | 2 records (not run in 1st Graal) |
| Verses | none | split at backslashes, three strings (`.04`) | `.04` only |
| Signs | `x+32`, `y+32` | same, text `byte - 32` through the shared alphabet | consistent |
| Sign list end | empty line or end of file | empty line | both occur |

Consequences for a re-implementation:

- Read the three computer bytes first, then the line; do not look for the line end before taking x, y, type.
- Parse link numbers as floating point and treat a negative arrival as "keep the player's coordinate".
- Do not dispatch on the extension.
- The double flag rule and the sign-end rule do not matter for any real file; follow the clients.
