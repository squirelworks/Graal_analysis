# Seihai level editor: tracking note

Date: 2026-10-25. Written for the Graal_analysis repository as a hand-off checklist. **It is not an implementation plan, and the Seihai client remains the main priority.** It can be copied into Seihai's `documentation/` as it stands.

## Design intent (from the owner)

A future Seihai level editor is **version-selectable and profile-driven**, like the client and its version chain. The **2.22 editor comes first**; other versions are deltas applied as profiles. No implementation is started.

Suggested profile fields (names are placeholders): `formats_read`, `formats_write_by_extension`, `has_chests`, `has_baddies`, `has_heights`, `has_predefined_npcs`, `has_level_cache`, `tiledef_support`, `open_filters`, `load_clamps`, `dialogs`.

## Part 1. The 2.22 feature list, in implementation order

Each item names the section of `222-reference.md` that holds the rules.

1. **Level model and the tile sheet.** 64 × 64 board of 16-bit ids, links, signs, chests, NPCs, baddies. Tile id → sheet: `col = (id % 16) + (id / 512) * 16`, `row = (id / 16) % 32`. (§3, §5)
2. **Read and write GLEVNW01 text.** `BOARD x y w layer data` with the exact skip rules, `LINK`, `SIGN`, `CHEST`, `NPC`, `BADDY`, `HEIGHTS` (9 × 9). Round-trip test against real levels. (§4)
3. **Read `GR-V1.00`–`1.03` and `Z3-V1.03/1.04`; write `GR-V1.03`.** Pick by extension. Reuse Seihai's existing binary reader. (§4; `formats-crossref.md`)
4. **Board view.** Scroll, 16-px tiles, tile overlays (blocking, foreground, terrain) from the type table, status bar. (§2, §5)
5. **Selection, copy, cut, paste, delete, floating paste.** (§6)
6. **Undo of board writes**, per tab, 128 records, rectangle snapshots. (§6)
7. **Tile palette.** Single tile, block pick, background tile, draw mode, flood fill with the right button. (§5, §6)
8. **Stamps.** Load `GOBJSET01` sets; place; add selection to the set; save the set. (§7)
9. **Link tools.** Link list and dialog; *turn selection into a warp field* with the `playerx`/`playery` defaults and the edge rules; open the destination in a new tab. (§6, §8)
10. **Sign tools.** List, x/y, text in the sign alphabet; (0, 0) signs. (§9)
11. **Chest tool.** Item list (25 items), sign index, Sign button. (§10)
12. **Baddy tool.** Ten types, three verses, types 4–6 without verses. (§11)
13. **NPC tool.** Image, script text with Test and Find; clone with the right button; predefined NPCs (`defnpc*.txt`, `#EDIT`, `#COMMENTS`). (§12)
14. **Tabs, Save (save-all), Save as, Close with prompt, New.** Write to a temporary file and rename, **not** delete-then-write like 2.22. (§4, §14)
15. **Keys.** The table in §13, including `F10`; `Ctrl+Q` batch re-save is optional.
16. **Maps.** Multi-level view, level cache, gmap map generation (`M`). (§14)
17. **Tile definitions.** `tiledefs` lines, type 0 and 1; type 4 after the semantics are traced. (§5)
18. **Play.** Needs the client. Out of scope for the editor itself.
19. **Editor control-NPCs.** `editnpc*.txt` with mouse variables. (§2) Late, depends on the script engine.

## Part 2. Per-version deltas (as profile switches)

| Profile | Switch changes relative to 2.22 |
|---------|----------------------------------|
| 2.17.1 | none found |
| 2.05 (rev 1/2) | no heights; no level cache; no tiles-array/log windows; no predefined NPCs; open filter `*.graal` only; person image and script are separate dialogs; text save has no `HEIGHTS` |
| 2.04 | as 2.05 and **no text format at all** (read or write); chest load clamp 0–62, NPC 0–63; object sets and tile defs present |
| 2.00 – 2.0 rev3 | as 2.04 without object sets and tile defs (object sets arrive in 2.04); rev 0–2 also open `*.zelda` |
| 1.34 – 1.41 | as 2.00; the baddy class is named baddy; draw mode and map key arrive in 1.41 |
| 1.28b2 – 1.33 | baddy class named opponent |
| 2nd – 1.1 | no level class; character dialog absent before 1.28b2; flags dialog from 3rd Graal; 1st Graal has no chests or NPC dialog |
| New World betas | **no chests, no baddies**; heights and map present in beta 1; text format described by the beta's own format file |
| 2.1 test builds | merged NPC dialog; predefined NPCs; no sign-codes window |
| 2.31 / GraalEditor 2.3.1.1 | editor is a separate program; writes text with `HEIGHTS`; the board section is claimed to be decimal in an older note (unchecked) |

## Open items to settle before any build

- Mouse state machine (drag, drop, double-click by kind): structure only.
- The meaning of the two chest/baddy mode flags.
- Tile definition `type` 4 and its x/y values.
- Whether arrival offsets are evaluated at warp time.
- `GraalEditor.exe` board format (decimal vs base64) against a real file.
