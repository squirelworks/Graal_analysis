# Level editor: every other build as a delta from 2.22

Date: 2026-10-25. Base: `222-reference.md`. Tags as in `README.md`. "Present" below means the exact class name is in the exe's class table or string table; a class that looks absent may only have been renamed. Builds are named as in `client-internals/drive-clients-inventory.md`.

## 1. The standalone editors (one line each)

- `GraalEditor.exe` 2.3.1.1 (2005): a **Thinstall package** (Thinstall signature as in `tools/graaleditor.md`; a single 17 KB code section in a file of about 1 MB). **Not unpacked in this pass.** Earlier notes (`tools/graaleditor.md`, `tools/graaleditor-vs-205.md`) already describe an unpacked image and are used as they stand.
- `Greaditor.exe` (2001, in the New World beta folders): **UPX-packed** (UPX0/UPX1, high entropy). It looks like a separate New World era editor and is **not unpacked**. `levelformat.txt` in the nwb1 folder documents the text format those betas used.

## 2. Class timeline of the built-in editor

`x` = present in the exe. Columns are the editor dialogs and model classes. Builds that have the same row are merged.

| Builds | Baddy class | NPC class | Level class | Chest dlg | Flags dlg | Person dlg | Char dlg | New NPC dlg | Obj set | Tiledef | Map | Heights | Cache | Tiles-array | Log |
|--------|-------------|-----------|-------------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 1st Graal | TEditorOpponent | none | none | . | . | . | . | . | . | . | . | . | . | . | . |
| 2nd Graal | Opponent | — | none | x | . | x | . | . | . | . | . | . | . | . | . |
| 3rd–15th Graal, 1.1, 1.1.9 | Opponent | Person (most builds) | none | x | x | x | . | . | . | . | . | . | . | . | . |
| 1.28b2, 1.31–1.33, 1.3b | Opponent | NPC | TEditorLevel | x | x | x | x | . | . | . | . | . | . | . | . |
| 1.34–2.04, 1.41 | **Baddy** | NPC | TEditorLevel | x | x | x | x | . | . | . | . | . | . | . | . |
| 2.04 | Baddy | NPC | TEditorLevel | x | x | x | x | . | x | x | . | . | . | . | . |
| 2.05, 2.05 rev1/rev2 | (TComputer) | NPC | TAdventureLevel | x | x | x | x | . | x | x | rev1+ | . | . | . | . |
| New World beta 1 | none | NPC | — | **.** | x | x | x | . | x | x | x | x | . | . | . |
| New World beta 2, 2.1 test 2/3 | none / (TComputer) | NPC | — | beta 2: **.**; test: x | x | . | x | x | . | x | . | beta 2 x | . | . | . |
| 2.17.1, 2.22 | (TComputer) | NPC | TAdventureLevel | x | x | . | x | x | . | x | x | x | x | x | x |
| 2.31 | — | NPC (model only) | — | . | . | . | . | . | . | x | . | x | . | . | x |

Notes on reading the table.

- 2.05 and later keep the `TEditorNPC` name. The baddy list uses `TComputer`, so the `TEditorBaddy` class is absent from the 2.05+ rows. The old level class `TEditorLevel` became `TAdventureLevel`, which the table does not track by name. **[inf]**
- `TEditPerson` / `TPersonAction` (image dialog plus script dialog) were merged into one `TEditNPC` in the 2.1 test builds. `TShowCodes` (the sign special-codes window) went at the same time: the 2.1 change log says the sign codes and add-NPC windows were merged into other windows. **[log]**
- The 2.1 test builds and the New World betas are **forks of the 2.0x line**; both carry the 2.05 text loader, but they differ in which dialogs are present. The New World betas have **no chest or baddy dialog and no chest or baddy class**. That matches the two obfuscated flags in 2.22 that switch chests and baddies off in the writers. **[inf]**
- `TObjectSet` (the *new set* dialog) is absent in 2.1 test, New World beta 2 and 2.17+, while the stamp sets still load in 2.22; the set-creation step moved elsewhere. **[inf]**
- 2.22 and 2.17.1 have the same class list. The 2.21 and 2.22 change logs contain no editor entries. No functional difference between the two editors was found; function shapes and section strings match, but a line-by-line comparison was not done.
- 2.31 has none of the dialogs. The level model classes (links, signs, chests, heights) and the GR-V1.04 reader stay because the game needs them, but the open, save and text readers are gone.

## 3. Formats, per build

| Build | Reads | Editor save | Open filter | Notes |
|-------|-------|-------------|-------------|-------|
| 1st Graal | `Z3-V1` family only | not traced | `*.graal, *.zelda` | **structure-only** (inventory level). |
| 2nd–1.39 | `GR-V1.00`–`GR-V1.03`, `Z3-V1.03/1.04` | `GR-V1.03` always | `*.graal, *.zelda` | Chest position clamped 0–62 on load, NPC position 0–63 (GR-V1.00 path). Baddy section ends at length < 3 or first byte ≥ 0x80. **[1.39]** |
| 2.00 – 2.0 rev2 | same | same | `*.graal, *.zelda` | Same loaders as 1.39 (same clamps). **[2.00]** |
| 2.0 rev3 – 2.04 | same | same | `*.graal` | **`.zelda` dropped from the dialog** at 2.0 rev3. The reader still accepts `Z3-V1`. Clamps remain. **[inf][2.04]** |
| 2.05 – 2.05 rev2 | same **plus `GLEVNW01`** | `.nw` → text, other → `GR-V1.03` | `*.graal` (text files should still open, since the loader reads the magic **[inf]**) | **GLEVNW01 first appears in 2.05.** No `HEIGHTS` in the editor path. The chest clamp is gone. **[2.05]** |
| NW beta 1 | same | `.nw` / `.graal` | `*.nw, *.graal` | Text format documented in the beta's own `levelformat.txt`. |
| NW beta 2, 2.1 test 2/3 | same | same | `*.graal, *.nw` | Dialog order switches to `*.graal` first. |
| 2.17.1 | same | same, plus `HEIGHTS` in text when the overlay is modified | `*.graal, *.nw` | `GR-V1.04` is accepted by the weblevels cache path only. |
| **2.22** | see `222-reference.md` | | `*.graal, *.nw` | Reference. |
| 2.31 client | `GR-V1.00`–`GR-V1.04`, `Z3-V1`; **no `GLEVNW01`** | none (no editor) | — | `GR-V1.04` = `GR-V1.03` plus an optional 9 × 9 `HEIGHTS` block. See `formats/level-binary-client.md`. |
| GraalEditor 2.3.1.1 | `*.graal, *.nw` | text with `HEIGHTS`; GR writer strings present | | **Conflict.** `tools/graaleditor.md` says its `BOARD 0` section is 64 lines of decimal tile indices and not accepted by the client loader. The 2.22 built-in writer produces base64 rows. This was not checked against a GraalEditor-written file in this pass. **[prev]** |

Verification notes.

- The clamp rows are from the loader code shape (a compare against 62.0 for chests and 63.0 for NPCs in the 1.39, 2.00 and 2.04 loaders; the compares are absent in 2.05, 2.17.1 and 2.22). A level with a chest at x = 63 therefore loads at 62 in ≤ 2.04. **[struct]**
- No editor writes `Z3-V1` or `GR-V1.00`–`GR-V1.02` (checked 1.39, 2.05 via the existing note, and 2.22).

## 4. Change-log dated features

From the shipped `newfeatures` files, dated by the heading each entry sits under. Not by the code; the 2.22 column says whether the 2.22 build is after that version (all are, except the 2.3 split).

| Feature | Change-log version | In 2.22 |
|---------|--------------------|---------|
| Draw by dragging with a single tile chosen; M builds a map PNG; status bar shows mouse position and tile; double-click sets the background tile; fields outside the level not selectable; drag a text file to make an NPC; trailing empty sign lines removed; new level uses the chosen background tile | 1.41 and 1.41 rev 1 | yes |
| Flood fill with the right mouse button (Shift: complete objects only; nothing selected: background tile) | 2.00 | yes |
| Object sets in the tile-objects folder, selectable in the editor; `addtiledef`, `addtiledef2`, `removetiledefs` | 2.04 | yes |
| Predefined NPCs (`defnpc*.txt`, `#COMMENTS`, `#EDIT`); sign-code and add-NPC windows merged away; multi-tile selection in the tile panel; F4 on a tutorial level opens a new empty level | 2.1 | yes |
| Multi-level editing when an NPC called `setmap`; scroll by dragging the player or by arrow keys | 2.12 | yes |
| Single levels get scrollbars again; big cursor on maps; Play saves all modified levels; editor control-NPCs (`editnpc*.txt`, mouse variables); M fixed | 2.13 | yes |
| Dragging baddies, NPCs and chests onto a level can be released and then moved; level caching and player position on Play fixed | 2.13 rev 3 | yes |
| Mouse wheel scrolls; arrow-key scrolling on single levels | 2.15 | yes |
| Button showing the selected tile rectangle as text; `showimg` and `putnpc` allowed in editor NPCs; flood-fill, undo and NPC-delete fixes on map levels; M faster | 2.16 | yes |
| M works on gmaps | 2.16 rev 7 | yes |
| Editor and online client become separate exes; the editor writes a copy and renames it so a crash no longer deletes the level; filename cache | **2.3** | **no** |

## 5. Deltas as a checklist (per build, relative to 2.22)

- **2.17.1**: none found.
- **2.05 (all revisions)**: no heights, no level cache, no tiles-array and log windows, no predefined NPCs, separate person-image and script dialogs, `TShowCodes` window for sign codes, open filter `*.graal` only. Save and load otherwise identical to 2.22. New World style map parser present from rev1 but dormant.
- **2.04 – 2.0 rev3**: no `GLEVNW01` reader or writer at all; object sets and tile definitions present from 2.04. Chest position clamp 0–62 on load.
- **2.0 – 2.0 rev2 and 1.3x**: open filter includes `.zelda`; the `Z3-V1` reader is live. Same clamps.
- **1.28b2 – 1.33**: baddy class still named opponent. Character NPC dialog present.
- **Before 1.28b2**: no character dialog, no level class; 2nd Graal adds chests and person dialogs; 3rd Graal adds the flags dialog; 1st Graal has no chest or NPC dialog.
- **New World betas**: no chest and no baddy; heights and map present in beta 1.
- **2.1 test builds**: combined NPC dialog, predefined NPCs, tiledef type, no sign-codes window.
- **2.31 and later client**: no editor; the standalone editor takes over (Thinstall).
