# Extensions say nothing; the magic does

Distinct files (by content) in the old builds, by magic and extension:

| Magic | `.zelda` | `.graal` | `.editor` | other |
|-------|---------:|---------:|----------:|------:|
| `Z3-V1.03` | 84 | 0 | 1 | 0 |
| `Z3-V1.04` | 23 | 31 | 0 | 0 |
| `GR-V1.00` to `GR-V1.03` | 694 | 1271 | 9 | 111 (assorted suffixes) |

- The `.zelda` extension is not a format marker: 694 of 801 distinct `.zelda`-named files are `GR-V1.00` to `GR-V1.03`. 2nd Graal to 15th Graal ship 68 to 368 such files per build (`by-build.tsv`, column `gr_magic_in_.zelda`).
- 1st Graal's 16 levels are all `Z3-V1.04` under `.graal` names.
- The Java Zelda Online game folder holds 51 `Z3-V1.03` files, all `.zelda`, and no `Z3-V1.04`.
- The player-world archive (`.graal` and `.nw` names) holds no `.zelda` file and no `Z3-V1` file.
- Every client binary tested (1st Graal, 1.28b2 to 1.41, 2.0 to 2.31, the two NewWorld betas) carries both `Z3-V1.03` and `Z3-V1.04` as magic strings; none carries a third `Z3-V1` revision. The 1st Graal and 1.39 loaders were read: they compare the 8 magic bytes only. 2.0 to 2.31 were not traced beyond the strings.
