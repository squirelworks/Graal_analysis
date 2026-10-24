# How the editor relates to the format notes

Date: 2026-10-25. Cross-reference between the editor's loaders and writers (2.22, with deltas) and the existing format notes. Tags as in `README.md`.

## `formats/level-binary.md` and `level-binary-client.md`

| Topic | Editor behaviour (2.22) | Relation |
|-------|-------------------------|----------|
| Code width | 13-bit for `GR-V1.02`/`1.03`, 12-bit for `GR-V1.00`/`1.01` and `Z3-V1.*` | Confirms the rule. Same in 1.39, 2.00, 2.05, 2.17.1. |
| Board run-length | The writer emits single runs and double runs (`ABAB…`, up to 64 pairs) | Confirms that stock writers emit double runs. |
| Section order | links, baddies, NPCs, chests, signs, each with its terminator | Confirms. The 2.22 writer appends a newline after each chest record. |
| Baddy section end | Ends at a record shorter than three bytes or a first byte ≥ 0x80. There is no x = 0 test. | Matches batch f; **`client-internals/level-editor-205.md` said otherwise and is corrected in this PR.** |
| Baddy record | Raw bytes (x, y, type, **not +32**), then `verse1\verse2\verse3`. Types 4–6 write empty verses (`\\`). | Confirms. |
| NPC record | `x+32, y+32, image#script` + newline | Confirms. NPC x, y in the text format are floats; only whole and half tiles survive the binary save. |
| Chest record | Four bytes `x+32, y+32, item+32, sign+32` | Confirms; sign index −1 is stored as byte 31. |
| `GR-V1.04` | Cache writer writes it when heights exist; the editor open path does not accept it | Matches `level-binary.md` (GR-V1.04 = V1.03 plus optional 9 × 9 `HEIGHTS`, 2.31). |
| Save format | `.nw` → text, anything else → `GR-V1.03` | New. No editor writes `GR-V1.00`–`1.02`, `Z3-V1.*` or `GR-V1.04`. |

## `formats/glevnw01.txt`

The text reader's rules are in `222-reference.md` section 4. New items for that file's notes:

- The `BOARD` layer field is ignored by the 2.22 reader. 2.05 also ignores it.
- `BOARD` rows are placed by (x, y, w); out-of-range or short rows are skipped silently, invalid base64 characters end a row.
- `HEIGHTS` is a 9 × 9 grid: up to nine lines of up to nine comma-separated decimals.
- `LINK` needs five tokens; a missing or empty new x or new y becomes `playerx` / `playery`.
- Tile ids from text are 12-bit (two base64 characters).

## Batch f (`decomp-findings-2026-10-25-f`, PR #39)

| Batch f finding | What the 2.22 editor adds |
|-----------------|--------------------------|
| Link arrival fields hold numbers, `playerx`/`playery`, and `playerx`/`playery` plus a signed offset | The editor stores arrival text verbatim (no parsing); its own *warp field* tool writes `playerx` / `playery` by default and the literal numbers `0` or `61` at the level edges (rules in `222-reference.md` section 6). Offsets such as `playery+10` are hand-typed text. Whether the engine evaluates them was not traced (open point from batch f stays open). |
| Baddy section ends only at a first byte ≥ 0x80; x = 0 is valid | Matches the code in five builds (1.39, 2.00, 2.05, 2.17.1, 2.22): the test is on the first byte's sign, with a length check; no x test. |
| Sign alphabet and `#K(n)` escapes | The editor's sign dialog edits plain text; the binary writer maps it through the sign alphabet. The special-codes window of old builds listed the escapes (`#h`, `#A`, …). |
| Sign at (0, 0) and chest sign index −1 | Same in the editor: a (0, 0) sign is not drawn, and a new chest has sign −1. |
| No file carries a `HEIGHTS` block | The text writer emits `HEIGHTS` only when the height overlay is marked modified; the binary writer never emits it. A level never touched by height tools has none. |

## GR-V1 notes (`formats/grv1-decoder`, `formats/seihai-boards.md`)

- A Seihai reader/writer for the editor must write by extension: `.nw` text, any other name `GR-V1.03`.
- The board's tile id range is 0–4095; the 12-bit text format cannot carry ids ≥ 4096, and binary levels from player worlds use ids ≥ 2048 in 64 % of boards (batch f). The tile → sheet mapping in `222-reference.md` section 5 covers the full range.

## Correction made in this PR

`client-internals/client-assets.md` gave the tile mapping as `col = t % 128`, `row = t // 128`. The correct mapping is `col = (t % 16) + (t / 512) * 16`, `row = (t / 16) % 32`, the same as Seihai's renderer already uses.
