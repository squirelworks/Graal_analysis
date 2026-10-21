# 2.04 → 2.05 → 2.05 rev2: function-level diff

Date: 2026-10-21

This compares the three builds closest to the decompile target. All three were run through the same Ghidra pipeline:
import with the Borland Delphi compiler spec, apply RTTI-recovered class and method names, recover the switch tables,
then export per-function features. The functions were then matched across builds.
This note is cleaned: it has no addresses and no decompiler output. Builds are identified by MD5 in `build-catalogue.md`.

## How the matching works

Each function is reduced to an address-free instruction stream (mnemonics and operands, with in-image addresses replaced by a placeholder).
The matcher then runs these passes in order:

1. Unique RTTI names (`Class.Method`, `Class.virt_N`, `Class.dyn_N`). Virtual-slot names are skipped for classes whose VMT shifted (see below).
2. Unique exact streams of 6 or more instructions.
3. Unique sets of referenced string literals.
4. Unique sets of large immediates.
5. Propagation through ordered callee lists and single unmatched callers, repeated until stable.

A matched pair is **identical** if the streams are equal and **changed** otherwise. Unmatched functions are counted as only-old or only-new.
Small look-alike helpers (many 15-instruction VCL thunks, for example) can fail to pair, so the only-old and only-new counts are an upper bound on real churn.

| Pair | Functions (old / new) | Identical | Changed | Only old | Only new |
|---|---|---|---|---|---|
| 2.05 rev1 → rev2 | 6522 / 6529 | 6345 | 94 | 83 | 90 |
| 2.04 → 2.05 rev2 | 6471 / 6529 | 5799 | 558 | 114 | 172 |

## 2.05 rev1 → rev2

**The game code barely moves.** About 20 game functions differ. Class layouts are identical (same instance sizes, same VMT lengths) and the GS1 command table is the same.
What changed matches the rev2 changelog:

- **Player counting** (changelog: "the script variable playerscount is fixed"). Four helpers count players in the current level and its gmap neighbourhood.
  In rev1 they read the level's player list through the caller's object for one test and through the global level for the other. rev2 reads both through the same object.
- **Tutorial / map start-up.** rev1 created a map object while setting up the tutorial map files. rev2 leaves that slot empty at start-up.
  When a gmap is active, rev2 runs an extra step after the map object is created.
- **Level reset.** One level-reset path no longer sets a flag that depended on game mode 5. A per-level loop takes its bound from a field on the main form instead of a hard-coded 632.
  These may belong to the changelog's "switching to other servers" fix, but that link is not proven.
- **NPC script text.** Of the three helpers that translate the `§` line marker into CR/LF, one was dropped and the other two were reworked.
- **Small changes** in the server-message window, the server-list form constructor, the main form constructor and the mouse-move handler (a few instructions each).

**The library code was rebuilt.** The VCL and RTL units in rev2 (Forms, ComCtrls, Controls, docking, ImgList and others) differ from rev1 in instruction shape.
rev1's library code, by contrast, matches 2.04's. So rev2 was linked against a rebuilt or updated VCL, not just recompiled game units.
For carrying names, this means RTTI-named VCL methods still match by name, but unnamed library helpers between rev1 and rev2 need the shape or callee passes.

## 2.04 → 2.05

This is where the NewWorld code lands in the mainline.

**New classes:** `TGraalMap` (gmap support) and `TADP` (see the anti-debug section below). **Removed classes:** `TEditorBaddy` and `TEditorLevel`.

**The level-object VMT shifted by one slot.** `TDrawableObject` gained a virtual method (2 → 3 user slots).
Every descendant's virtual numbering therefore moves by one from 2.04 to 2.05:
`TDrawableSurface`, `TSurfaceOwner`, `TLevelObject`, `TServerPlayer` → `TPlayer` / `TEditorNPC`, `TComputer`, `TDisplayedNPCImg`, `TEditorChest`, and the ten level-object classes (horse, bomb, ball, carry, extra, flying, leap, explosion…).
So 2.04 `X.virt_N` corresponds to 2.05 `X.virt_(N+1)`.
Any name or type carried between 2.0–2.04 and 2.05 by slot number has to apply this offset.

**Instance-size changes:** `TAdventureLevel` grows from 96 to 184 bytes (gmap and `.nw` state), `TAdventureCommand` from 68 to 76, and `TServerPlayer` / `TPlayer` / `TEditorNPC` each shrink by 4.

**`.nw` support (GLEVNW01) is new code.** The text-level reader parses `BOARD`, `LINK`, `BADDY` … `BADDYEND` and `CHEST` sections and decodes tiles with the standard base64 alphabet. It sits next to the binary `GR-V1.00`–`1.03` reader, which stays.
A matching writer emits `GLEVNW01`, then one `BOARD 0 <y> 64 0 <tiles>` line per row (the `BOARD x y width layer tiles` form in `formats/glevnw01.txt`). A new chest-line parser carries the error "Wrong chest data!".
Three other existing functions gained a GLEVNW01 magic check: one in the level class, one in the player/script class, and one in the main form unit.
`.nw` is added to the level open dialog.

**gmap support is new code.** It covers the `TGraalMap` class, a loader that builds the map image (`map.png`) and is reachable from the GS1 executor, and a `bigmap.txt` / `minimap.txt` setup routine reachable from the reconnect window.
A main-form routine that set up `bigmap.txt`, `minimap.txt` and `map.png` in 2.04 no longer references them.

**GS1 commands new in 2.05:** `loadmap`, `setz`, `updateterrain`, `setbacktile2`, and a `setbacktile` form that takes an argument.
All 163 command records in the 2.05 table are present in rev1 and rev2.

**Smaller additions:**
- PMs are written to `pms\messages_<name>.txt`.
- `drawaslight` appears in the drawing code.
- The script editor gains a 400-instruction routine that handles `/* */` comments and tabs. It is reached from a new button handler, matching the changelog's "new button in the script editor".
- A new level-editor routine, reached from a toolbar button, handles `playerx` / `playery` with values clamped to 0–61.
- 2.04's routine that installed `tempsitc.ttf` into the Windows fonts folder is gone from 2.05, and so is the `Courier New` default in the main form constructor.

## Anti-debug component (ADP), new in 2.05

2.05 links a third-party Delphi component `TADP`. The main form constructor starts it, and the form's DFM sets all four switches:
`Kill_Debugers = True`, `Stop_Execution = True`, `Anti_Procdump = True` and `Kill_Monitors = True`.
It uses the Toolhelp32 process, module and heap walkers. It looks for loader and monitor tools by name (the binary contains `FPLOADER.EXE` and `FROGSI`, likely a fragment of a FrogsICE-style name) and stops execution when it finds one.
The component appears in 2.05, 2.05 rev1, 2.05 rev2, the 2.1 test builds and both NewWorld betas. It is absent from every build up to 2.04.
This matters for live work on 2.05 and later under a debugger or monitor.

## What to reuse

- **2.05 rev1 is close enough to share names with rev2** wherever the RTTI or shape match holds. Only the ~20 functions above, plus library helpers, need re-checking.
- **About 90% of 2.04's functions are identical in 2.05.** It is the cleanest reference for what the NewWorld merge added: TGraalMap, GLEVNW01, the VMT slot, the new GS1 commands and ADP.
