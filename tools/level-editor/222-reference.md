# The 2.22 built-in level editor

Date: 2026-10-25. Primary reference. The 2.22 client carries the same editor as 2.17.1 (checked: same class list, same loader and writer shapes). Other builds are deltas in `version-deltas.md`. Tags are explained in `README.md`.

Table of contents: 1 Entering and leaving · 2 Window and tool modes · 3 Level model · 4 Loading and saving · 5 Tiles and the sheet · 6 Selection, paste, undo, fill · 7 Stamps · 8 Links · 9 Signs · 10 Chests · 11 Baddies · 12 NPCs · 13 Keys · 14 Tabs, maps and multi-level editing · 15 Other dialogs · 16 Open

## 1. Entering and leaving

The editor is the `TAdventure` main form in a second mode of the game screen. The same exe plays and edits. **[2.22]**

- **F4** opens the editor; it is refused online ("You cannot open the editor in the online mode."). The tutorial levels live inside the exe, so F4 from a tutorial level opens a new empty level instead of failing. **[prev][log]**
- **F5** opens the Load level dialog. **[prev]**
- **P / Play** returns to the game on the current level. Since 2.13 *Play* saves every modified level first. **[prev][log]**
- A level path as the first command-line argument skips the login screen and opens that file in the editor. **[prev]**
- **F10** toggles the window border style (bordered / borderless). **[2.22]**
- **Esc** shows a warning box before leaving. **[2.22]**
- Dropping a text file onto the window creates an NPC from the script (1.41 feature, handler still present in 2.22). **[log]** The handler body is **[struct]**.

## 2. Window and tool modes

- **Board view**: a DirectDraw surface showing 64 × 64 tiles at 16 px, with horizontal and vertical scroll bars. Mouse wheel scrolls vertically; arrow keys scroll, also on single levels (2.15). **[prev][log]**
- **Toolbar**, in order: New, Open, Save, Save as, Undo board copy, Cut, Copy, Paste, Delete, Turn selection into a warp field, Edit links, Edit signs, a button that shows the current tile rectangle as text (added 2.16), Close, Play. **[2.22 for handlers present; labels prev]**
- **Tab bar**: one tab per open level. Close asks about unsaved changes. **[2.22]**
- **Side panel** has two radio modes plus a combo, giving these *palette modes*. **[prev]**
  1. Predefined object (stamp) from a GOBJSET01 set.
  2. Tile palette from the sheet.
  3. Baddies, NPCs and chests.
  4. Predefined NPCs (the `defnpc*.txt` scripts; change log v2.1, class present in the 2.1 test builds). A string grid edits the `#EDIT` parameters of the chosen script. **[log]**
- **Check boxes**: show blocking tiles, show foreground tiles, show terrain tiles. They are overlays computed from the 4096-byte type table, not stored. **[prev]**
- **Status bar**: mouse tile position and the tile under it (1.41). **[log]**
- Editor control-NPCs (since 2.13): a file `editnpc<Name>.txt` placed in the NPC folder scripts editor actions, with `mousex`, `mousey`, `mousescreenx`, `mousescreeny` and `mousebuttons` (left 1, middle 2, right 4) available only in editor mode. Only changing tiles is supported. **[log]**
- **M** builds a map image of the level or gmap (saved as PNG, not 8-bit). On gmaps it works since 2.16 rev 7. **[log][prev]**

Mouse handling (select, move, drag-drop, double-click by object kind) is a state machine over obfuscated fields. Only the outline is known: **[struct]**

- Left drag on empty board selects a tile rectangle, clipped to the level (fields outside the level cannot be selected; 1.41).
- With a tile chosen, left drag paints; pasting a floating block follows the mouse and a click outside drops it.
- Dropping a baddy, NPC or chest from the palette can be released and then moved with the mouse, like in the old days (2.13 rev 3 fix). **[log]**
- Right button on a placed baddy, NPC or chest clones it. **[prev]**
- Right button elsewhere is flood fill (see section 6). **[log]**
- Double-click on an object opens its dialog; double-click on a tile makes it the background tile. **[prev][log]**

## 3. Level model

`TAdventureLevel` owns these lists. **[2.22]**

| List | Element | Notes |
|------|---------|-------|
| board | 64 × 64 tile ids (16-bit) | index = y × 64 + x |
| links | `TEditorLink` | destination, x, y, w, h, new x text, new y text |
| signs | `TEditorSign` | x, y (tiles), message text |
| chests | `TEditorChest` | x, y, item, sign index |
| NPCs | `TEditorNPC` | image name or none, x, y (fractional tiles), script |
| baddies | `TComputer` | x, y, type, three verse strings |
| stamps | `TEditorObject` | only in the object set, not in the level |
| heights | `TLevelHeights` | 9 × 9 floats, optional, edited only in builds with the height tools |

The editor also keeps a cache of recently loaded levels (`TEditorLevelCache`, 2.17 and later) so that the link walker and the gmap code can open neighbours without a reload. **[2.22][prev]**

## 4. Loading and saving

### Open

The open dialog filter is `Graal levels (*.graal, *.nw)`. Several files may be chosen and each opens in its own tab. **[2.22]**

The loader reads the first eight bytes and branches. **[2.22]**

| Magic | Reader |
|-------|--------|
| `GLEVNW01` | text reader (below) |
| `GR-V1.00`, `GR-V1.01`, `GR-V1.02`, `GR-V1.03` | binary reader; 13-bit board codes for 1.02 and 1.03, 12-bit for 1.00 and 1.01 |
| `Z3-V1.03`, `Z3-V1.04` | the old `.zelda` layout, 12-bit codes (accepted on open) |
| `GR-V1.04` | read only by the weblevels cache path in 2.22, not by the editor open path |
| anything else | rejected (the string table has "Unsupported file type!") |

Section order and per-version content of the binary files are in `formats/level-binary.md` and `formats/level-binary-client.md`. The 2.22 reader keeps the same rules as 2.05: a baddy record is at least three bytes and the section ends at the first record shorter than three bytes **or whose first byte is 0x80 or more** (there is no x = 0 test). **[2.22]** This is the same shape in 1.39, 2.00, 2.05 and 2.17.1.

### The GLEVNW01 text reader **[2.22]**

Lines are read until the end of the file. Block sections (`SIGN`, `NPC`, `BADDY`, `HEIGHTS`) swallow lines until their terminator; everything else is a one-line record split on spaces.

- **`BOARD x y w layer data`**
  - `x` and `y` must be 0–63, `w` ≥ 1, `x + w` ≤ 64.
  - The *layer* field (fourth) is **not read**. A row with a non-zero layer is still written onto the one board.
  - `data` needs at least `2 × w` characters. Each tile is two characters of the 64-letter base64 alphabet, high character first, so a tile id is 12-bit (0–4095).
  - A character outside the alphabet ends that row silently; tiles already placed from the row stay. Invalid rows are skipped; no error is raised.
  - Rows may come in any order and may be partial. The board is zero-filled first.
- **`LINK dest x y w h newx newy`**: at least five tokens (dest and four numbers). Missing `newx` / `newy` become `playerx` / `playery`. An empty value is also replaced with `playerx` / `playery`. The text is stored as given; arrival text such as `playery+10` is kept verbatim. **[2.22]** The same parse is in 2.05.
- **`SIGN x y`** then message lines until `SIGNEND`. The lines are joined with newlines and decoded through the sign alphabet (see `formats/sign-text.md`).
- **`CHEST x y item signindex`**
- **`NPC image x y`** then script lines until `NPCEND`. Image `-` means no image. x and y are decimal floats.
- **`BADDY x y type`** then exactly three verse lines, then `BADDYEND`. Position is clamped to 0–63; the type is bounded to 0–9. Extra lines before `BADDYEND` are ignored.
- **`HEIGHTS`** then up to nine lines until `HEIGHTSEND`. Each line is a comma list of up to nine decimals; line *i* is row *i* of a 9 × 9 grid. The block is read only when the level already has a height overlay. **[2.22]**

### Save **[2.22]**

- **Save** (button and Ctrl+S) is a *save-all*: it first commits any floating paste, then walks every level in the editor's level list and saves each one that is marked modified, plus the current one. Levels without a file name are skipped. For each level it **deletes the old file and writes the new one in place**, using the writer picked by the extension, then clears the modified flag. If the map object is modified it is saved too. The status bar shows "N Level(s) saved" (and " + <map name>" when the map was written). **[2.22]**
- **Save as** asks for a name. Saving a level opened from a URL falls through to Save as. **[prev]**
- The **file extension picks the format**. `.nw` (case-insensitive) writes text; **any other extension writes `GR-V1.03`**. The editor never writes `Z3-V1`, `GR-V1.00`–`GR-V1.02` or `GR-V1.04` levels. **[2.22]** (The cache writer, which is not the editor save, writes `GWEBL001` and `GR-V1.03`/`GR-V1.04` for weblevels files.)

**Text writer.** `GLEVNW01`, then 64 rows `BOARD 0 y 64 0 <128 characters>`, then `HEIGHTS` + lines + `HEIGHTSEND` **only when the level has a height overlay marked modified**, then `LINK …`, `SIGN x y` + text + `SIGNEND`, `CHEST x y item sign`, `BADDY x y type` + three verses + `BADDYEND`, `NPC image x y` + script + `NPCEND`. **[2.22]** (2.05 writes the same without `HEIGHTS`.)

**Binary writer (`GR-V1.03`).** Header, board (13-bit run-length codes, including double runs `ABAB…`), links as text lines ending with a `#` line, baddies as three raw bytes (x, y, type, not +32) plus `verse1\verse2\verse3` and a newline, then `FF FF FF 0A`, then NPC records `x+32, y+32, image#script`, then a `#` line, chests as four GCHARs and a newline each, a `#` line, then signs as two GCHARs plus sign-alphabet text. Baddy types 4–6 write empty verses (`\\`). **[2.22]** Details of the run encoder match the 2.05 note.

**Chests and baddies can be skipped.** In both writers, chests and baddies are written only when two session-mode flags are both clear. If either is set the editor writes just the section terminators. The same flags gate the corresponding part of the loaders. The flags are stored in an obfuscated form with a tamper check, so their meaning is **[struct]**. The New World betas have no chest or baddy editor at all, so the flags are most plausibly a *chests and baddies enabled* switch for a New World style mode **[inf]**.

### Safety

2.22 deletes the old file and then writes the new one in place, so a crash between the two loses the level. The 2.3 change log says this was fixed there: the new level is written to a copy and renamed over the old one. **[2.22][log]**

## 5. Tiles and the sheet

- Level tile ids are 0–4095. The sheet `pics1.png` is 2048 × 512, 16-px tiles, 128 columns × 32 rows. **[2.22]**
- **Id → sheet position** (correcting `client-internals/client-assets.md`):

```
col = (id % 16) + (id / 512) * 16
row = (id / 16) % 32
source = (col * 16, row * 16, 16, 16)
```

  The sheet is laid out as eight blocks of 512 ids; each block is 16 columns by 32 rows, filled row by row, and the blocks sit side by side. Ids 0–511 are the left 256 px, 512–1023 the next 256 px, and so on. The earlier note used `col = id % 128`, `row = id / 128`, which is wrong. Seihai's renderer already uses the formula above.
- A *tile definition* (`tiledefs/…`, `addtiledef`) swaps the sheet for levels whose name starts with a prefix. Line format: `image,prefix,type,x,y`. Type 0 is the old order; type 1 is the new order (documented in the 2.1 change log). The sample file in the 2.22 install lists about 17 prefixed overrides (all `type` 4 for the extra sheets with x offsets such as 1344, 1536 or 1728) plus the default row `pics1.png,,0,0,0`. The meaning of type 4 and of the x/y values is **not traced**. **[inf]** They look like a tile-column offset into the replacement sheet. See `formats/tile-walk.md` for how types affect walking.
- *Tile palette*: click picks one tile, drag from the upper-left to the lower-right picks a block (2.1 change log); the block pastes as a floating selection. Double-click a palette tile or a board tile to make it the *background tile* shown in a preview box (1.41). New levels start filled with the chosen background tile (1.41 fix). **[log][prev]**
- Tile *type* (blocking, water, etc.) is not stored in the level. It comes from the 4096-byte type table (`formats/tiletypes.txt`).

## 6. Selection, paste, undo, fill

- **Selection** is a rectangle on the 64 × 64 board. Copy and Cut lift the rectangle into a floating block; Paste follows the mouse. Dropping writes tiles to the board. **[prev]**
- **Undo** covers board tiles only. Before each board write the editor stores the rectangle and the old tile values. The stack is per tab and holds at most **128** records. Undo restores the rectangle and re-selects it, and marks the level modified. Changes to links, signs, NPCs, baddies and chests are not undoable. **[2.22]**
- **Draw mode**: with a single tile selected, left-drag paints tiles until release (1.41). **[log]**
- **Flood fill** (change log v2.00): paste a tile or stamp, then press the right mouse button on the board to fill the area with it. Shift + right button fills only complete objects. With nothing selected, the right button fills with the background tile. **[log]** The handler is **[struct]**. (Right button over a baddy, NPC or chest clones the object instead.)
- **Turn selection into a warp field**: creates a new link covering the selection and opens the link dialog. The link defaults are **[2.22]**:
  - x, y = top-left tile of the selection, w, h = selection size; the destination is left for the dialog;
  - new x = `playerx`, new y = `playery`;
  - then one edge rule is applied, the first that matches: if the selection starts in column 63, new x = `0`; else if it starts in row 63, new y = `0`; else if it starts in column 0 and is one tile wide, new x = `61`; else if it starts in row 0 and is one tile high, new y = `61`.
  
  So a link on the east edge arrives at the left side of the next level, and a one-tile-wide link on the west edge arrives at x = 61, while the other coordinate follows the player. `playerx` / `playery` stand for "keep the player's own coordinate".
- **Selection to text** button: shows the current tile rectangle as text for use in editor NPCs (the `editnpc*.txt` scripts). Another button builds a tile-index line and a script array from the selection (`TTilesArrayFrame`). **[log][prev]**

## 7. Stamps (predefined objects)

- Sets come from `objects<set>.txt` in the tile-objects folder. The plain `objects.txt` is *Standard*. Format: `GOBJSET01` (`formats/gobjset01.md`). Five sets ship with the client (Standard, House Inside, Castle, Snow, Volcano; 288 named objects). **[prev]**
- *Add the selection to the objects* names the current rectangle and inserts it after the selected stamp; *Save objects* rewrites the set file. The name dialog is `TObjectName`. Its OK handler body is **[struct]**; the behaviour is the 2.05 one. **[prev]**
- Placing a stamp writes tile ids only (no layer, no type, no link). Collision is decided by the tile-type table.
- Object sets were added in 2.04 (change log v2.04; the `TObjectSet` class is first in the 2.04 exe). **[log]**

## 8. Links

- **Edit links** (key L) opens the link list: Linkfile, X, Y, W, H, New X, New Y. Buttons: Edit, Delete, Load. *Load* opens the destination in a new tab. **[prev][2.22]**
- **Link dialog** (`TLinkOptions`). Fields: file name or URL, x, y, w, h, new x, new y. OK validates the fields; on failure the dialog shows "Wrong values! Type in a filename…" and stays open. On success the link is added to the level list if it is not already in it, the list is refreshed, and the level is marked modified. **[2.22]**
- New x and new y may be a number or an expression: "you can use math operations and variables like playerx/y". The editor stores the text unchanged. Whether the engine evaluates an offset such as `playery+10` when the link fires was not traced. **[inf]** In a 3113-level archive, 21 arrivals have that form (`client-internals/decomp-findings-2026-10-25-f/02-link-arrival-expressions.md`).
- Link arrival text in the binary writer is the text line `dest x y w h newx newy`.
- Link destinations may be a file name or a URL. A destination that is neither `.graal` nor `.nw` is accepted as typed. **[prev]**

## 9. Signs

- **Edit signs** (key S): a list with X and Y fields, New, Delete. A sign at (0, 0) is not drawn on the board. Such a sign is used by index: a chest shows sign *n* when opened, and the GS1 `say n` command shows sign *n*. **[prev]**
- The special-codes list (`TShowCodes`) was merged into the sign dialog (change log v2.1); the class is gone from the 2.1 test builds on. **[log]**
- Text is stored in the sign alphabet with `#K(n)` escapes (see `formats/sign-text.md`). Empty trailing lines are removed automatically (1.41). **[log]** The encoder in the binary writer follows the alphabet in `formats/sign-text.md`.

## 10. Chests

- Dialog `TChestEdit`: item (index), a sign index, Sign button, Delete, Close. **[2.22]**
- Item list, in index order (unchanged from 2.05, checked against the 2.22 string table): `greenrupee, bluerupee, redrupee, bombs, darts, heart, glove1, bow, bomb, shield, sword, fullheart, superbomb, battleaxe, goldensword, mirrorshield, glove2, lizardshield, lizardsword, goldrupee, fireball, fireblast, nukeshot, joltbomb, spinattack`. A new chest defaults to item 1 and sign -1. **[2.22][prev]**
- The **Sign button** opens the sign editor for the chest's sign index. **[2.22]**

## 11. Baddies

- Dialog `TEditBaddy`: type selector, three verse fields (attack, when hurt, when it hurts the player), Delete, Close. **[2.22]**
- Ten types: Gray Soldier, Blue Soldier, Red Soldier, Shooting Soldier, Swamp Soldier, Frog, Spider, Golden Warrior, Lizardon, Dragon. **[prev]**
- Choosing type 4, 5 or 6 (Swamp Soldier, Frog, Spider) disables the verse fields. The writer saves empty verses for those types. **[2.22]**
- A new baddy starts with "Stop!" and "Ouch!". **[prev]**
- Loaders in builds up to 2.04 clamped baddy and chest positions; see `version-deltas.md`.

## 12. NPCs

- One dialog, `TEditNPC`: image, script, Test (syntax check), Style, Find, and the usual edit menu. **[2.22]**
- The script editor understands the editor markers `//#EDIT name value` and `//#COMMENTS text` used by predefined NPCs. **[log]** Predefined NPCs are `defnpc*.txt` files; when one is dropped on the level every occurrence of the named variable is replaced by the entered value. **[log]**
- *Character NPC* (`TEditCharacter`): a form that generates a walking-character script. Fields as in the 2.05 note. **[prev]**
- Edit flags (`TEditFlags`): the offline flag list; it is not saved in the level. **[prev]**
- NPC x and y are fractional tiles; the binary format stores them as two bytes (+32), so only whole and half tiles survive a binary save. **[inf]**

## 13. Keys

Delphi shift-state bits: 1 = Shift, 2 = Alt, 4 = Ctrl. **[2.22]**

| Key | Action |
|-----|--------|
| Ctrl+N | New |
| Ctrl+O | Open |
| Ctrl+S | Save (save-all, see section 4) |
| Ctrl+Z, Alt+Backspace | Undo board copy |
| Ctrl+X, Shift+Del | Cut |
| Ctrl+C, Ctrl+Ins | Copy |
| Ctrl+V, Shift+Ins | Paste |
| Del | Delete the selection |
| L | Edit links |
| S | Edit signs |
| P | Play |
| M | Generate map image |
| **Ctrl+Q** | Batch re-save for gmaps: for each level name in the loaded map's level list the editor reads the file and writes it again with the writer for its extension. **[struct]** Seen in 2.17.1 and 2.22. Not found in the 2.05 export (the handler may simply be missing there). |
| **F10** | Toggle window border style |
| Esc | Warning box before leaving the editor |

L, S, P and M are ignored while a combo box in the side panel has focus. Ctrl+Enter and a few Ctrl+letter chords are game-mode shortcuts handled by the same form.

## 14. Tabs, maps and multi-level editing

- Each tab keeps its own scroll position, selection, floating paste, undo stack and object lists. New tabs are titled `(new)`. **[prev]**
- Multi-level editing (v2.12): when an NPC calls `setmap`, the editor shows the neighbouring levels together. Drawing follows NPC y order. You scroll by dragging the player or by arrow keys; on maps a big cursor replaces the player (2.13). **[log]**
- Editing a level on a map marks near levels modified when you delete their NPCs; undo works across a level change (v2.16 fixes). **[log]**
- `TGraalMap` holds the gmap model and the generated-map seeds; `TEditorLevelCache` holds recent levels. **[prev]**

## 15. Other dialogs

`TLoadLevel` (open by name, with a browse button that clears the file dialog's options before running it), `TLogFrame` (log window, present since 2.17.1), `TShowImg` (present since 2.17.1; role not traced), `TEditVariable`, and the tile-array window. **[2.22]**

## 16. Open

- The mouse state machine and the exact drag/drop rules.
- Meaning of the two session-mode flags that gate chests and baddies.
- Whether the Ctrl+Q batch re-save converts formats or only normalises files (it reads with the magic-based loader and writes by extension, so a `.graal` file in any readable version comes out as `GR-V1.03`).
- Where "Unsupported file type!" is raised in 2.22. The string is in the 2.22 and 2.31 string tables, but no caller appears in the exported code.
- Three handlers that the second decompiler pass could not recover (no function found).
- How the type and offset fields of tile definitions are used.
- Whether arrival offsets are evaluated at warp time.
