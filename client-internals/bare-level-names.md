# Bare level names and the `.zelda` extension

Which client tries `.zelda` for a level name with no extension, and whether a missing `.zelda` falls back to the `.graal` of the same stem. The answer is that none does, in any client read.

Read in 26 Windows client builds: 1st Graal to 15th Graal (with the 4th, 5th and 9th alphas), 1.1, 1.1.9, 1.21, 1.28 beta 2, 1.3 beta, 1.31, 1.32, and 2.05.

## Findings

- **No client adds `.zelda`.** No build carries `.zelda` as a bare extension string. Its only `.zelda` strings are full built-in level names, such as `level1.zelda`, `cave2.zelda`, `mod26.zelda` and `house12.zelda`. Those are compared against the current level's name or used as fixed warp targets, and are present in 1st Graal to 9th Graal.
- **The one extension rule adds `.graal`, and only in the editor.** Every build has the same rule in the level editor's open and save buttons, and in 1.3 and later also the snapshot save: when the chosen file name has no extension, `.graal` is added.
- **No fallback.** No build has code that swaps one extension for the other. A link or warp to `name.zelda` loads `name.zelda` as written; a missing file is just missing.
- **Contents still decide the format.** The loader decides the format from the file's magic, not its extension (`decomp-findings-2026-10-25-j/03-extensions-and-magic.md`), so a `.graal` name holding a `Z3-V1` level still loads.

## For a reimplementation

- Keep a level name exactly as the link, warp or server wrote it.
- Add `.graal` only when the editor saves a name typed without one.
- Pick the reader from the magic.

## Confirmed, inferred, not tested

- Confirmed from the programs: there is no bare `.zelda` string, the editor adds `.graal`, and no extension-swap code exists.
- Inferred: that the level loader uses the name unchanged. That follows from there being no other extension string near the load path; the loader's file-open call was not traced to its end.
- Not tested: the Java Zelda Online client, and builds between 1.32 and 2.05 other than those listed.
