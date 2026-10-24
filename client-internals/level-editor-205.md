# Built-in level editor (client 2.05 rev 2)

Date: 2026-10-21

Derived from the 2.05 rev 2 binary: class names (RTTI), form resources (DFM), string tables, and the behaviour of the editor handlers. Names only, no code. Tags: **[2.05]** read from the binary · **[inf]** inferred.

This note covers 2.05. The primary editor reference is now `tools/level-editor/222-reference.md` (2.22), with the other builds as deltas in `tools/level-editor/version-deltas.md`.

In 2.05 the editor is not a separate program. It lives in the main window (`TAdventure`) and is a second mode of the game screen. GraalEditor.exe split off later; see `tools/graaleditor-vs-205.md`.

## Entering and leaving

| Key | Game mode | Notes |
|-----|-----------|-------|
| F4 | open the editor | Refused when connected: "You cannot open the editor in the online mode." **[2.05]** |
| F5 | Load level dialog (`TLoadLevel`) | Asks first when online: loading a level disconnects you. |
| P / Play button | back to game mode on the current level | "Please save the level under a new name before playing!" if the level is unsaved or unnamed. |
| Close button | close the current level tab | Asks "Save changes to …" when modified. |

Entering the editor tears down the game state for the current level: looped sounds stop, NPC and baddy instances are freed, and the level the player stood on is opened as a tab (re-read from disk, so unsaved runtime board changes are not carried over). The scroll position centres on the player. **[2.05]**

Starting the client with a level file as the first command-line argument (`Graal.exe path\level.graal`) skips the login screen. The client changes into the file's folder, creates a local player at (30, 30.5), and opens the file in the editor. **[2.05]**

## Window layout

- **Board view**: the DirectDraw surface shows the 64×64 level at 16 px per tile, with scroll bars.
- **Toolbar**: New, Open, Save, Save as, *Undo board copy*, Cut, Copy, Paste, Delete, *Turn selection into a warp field*, Edit links, Edit signs, Edit flags, Close, Play.
- **Tab bar**: one tab per open level. Each tab keeps its own scroll position, selection, floating paste, undo stack, and object lists. New levels are titled `(new)`.
- **Side panel**, with three radio modes:
  1. *Select predefined object*: stamps from GOBJSET01 sets (see below).
  2. *Select tile*: the tileset palette (`pics1.png`). Click to pick, drag to pick a block. Double-click a tile to make it the background tile shown in the preview box.
  3. *Baddies, Npcs, Chests*: a palette of placeable objects.
- Checkboxes: *Show blocking tiles*, *Show foreground tiles*, *Show terrain tiles* (overlays computed from the tile-type table, not stored in the level).
- Status bar: tile coordinates, tile index, and the object under the cursor (`tile`, `npc`, `chest`).

## Editor keys

The editor uses Delphi shift states. Ctrl is the main modifier.

| Key | Action |
|-----|--------|
| Ctrl+N | New level |
| Ctrl+O | Open |
| Ctrl+S | Save |
| Ctrl+Z, Alt+Backspace | Undo board copy |
| Ctrl+X, Shift+Del | Cut |
| Ctrl+C, Ctrl+Ins | Copy |
| Ctrl+V, Shift+Ins | Paste |
| Del | Delete selection |
| L | Edit links |
| S | Edit signs |
| P | Play |
| M | Generate a map image (`graalmap.png`, "Generating the map may take some minutes. Proceed?") |

L, S, P and M are ignored while a combo box in the side panel has focus.

## Tile editing model

- **Selection.** Dragging on the board selects a tile rectangle. The selection is clipped to the 64×64 board.
- **Floating paste.** Copy or Paste lifts the selected tiles into a floating block that follows the mouse. Clicking outside it drops it. Dropping writes the tiles onto the board. Moving a selection works the same way: it is lifted, dragged, and dropped.
- **Right mouse button** on a placed baddy, NPC, or chest makes a copy of it ("Right Mousebutton-> copy …").
- **Warp field.** *Turn selection into a warp field* creates a link whose rectangle is the selection and opens the link dialog.

### Undo

Undo covers **board tiles only**, which is why the button says *Undo board copy*.

- Before any write to the board, the editor stores an undo record: the rectangle (x, y, width, height) plus the tile values it is about to overwrite.
- Records are kept per level tab in a stack of at most **128**. The oldest record is dropped when the stack is full.
- Undo pops the newest record, writes the old tiles back, re-selects that rectangle (or clears the selection if it was the whole board), and marks the level modified.
- Adding, moving, or deleting links, signs, NPCs, baddies, and chests is **not** undoable.

## Object types

The editor's level document (`TAdventureLevel`) keeps separate lists, one per kind.

| Kind | Class | Placed with | Dialog (double-click) |
|------|-------|-------------|-----------------------|
| Link | `TEditorLink` | warp-field button, or the link list | `TLinkList` → `TLinkOptions` |
| Sign | `TEditorSign` | sign list "New" | `TEditSigns` |
| Chest | `TEditorChest` | object palette | `TChestEdit` |
| NPC | `TEditorNPC` | object palette | `TEditPerson` → `TPersonAction` |
| Character NPC | `TEditorNPC` with a generated script | object palette | `TEditCharacter` |
| Baddy | `TComputer` | object palette | `TEditBaddy` |
| Stamp | `TEditorObject` | "Add the selection to the objects" | `TObjectName`, `TObjectSet` |

### Links (`TLinkList`, `TLinkOptions`)

A list with columns Linkfile, X, Y, W, H, New X, New Y, and buttons Edit, Delete, Load. *Load* opens the destination level in a new tab. The link dialog accepts a file name or URL, and the new position may be an expression: "you can use math. operations and variables like playerx/y". The tutorial levels use `playerx` and `playery` this way.

### Signs (`TEditSigns`, `TShowCodes`)

A list of signs with X and Y fields, New, and Delete. *Show special codes* lists the glyph escapes (`#h` head, `#A`, `#B`, …). A sign at (0, 0) is not drawn on the board. Such a sign is used by index: a chest shows sign *n* when opened, and the GS1 `say n` command shows sign *n*. The embedded tutorial uses both.

### Chests (`TChestEdit`)

The chest holds an item and a sign index (-1 = no sign). The 2.05 item list, in index order:

`greenrupee, bluerupee, redrupee, bombs, darts, heart, glove1, bow, bomb, shield, sword, fullheart, superbomb, battleaxe, goldensword, mirrorshield, glove2, lizardshield, lizardsword, goldrupee, fireball, fireblast, nukeshot, joltbomb, spinattack`

A new chest defaults to item 1 (bluerupee) and sign -1.

### Baddies (`TEditBaddy`)

There are 10 types: Gray Soldier, Blue Soldier, Red Soldier, Shooting Soldier, Swamp Soldier, Frog, Spider, Golden Warrior, Lizardon, Dragon. The script names are `graysoldier` … `dragon`, and the sprites are `baddy*.gif`. Each baddy has three verses: *attack*, *when hurt*, and *when it hurts the player*. A new baddy starts with "Stop!" and "Ouch!". Types 4–6 (Swamp Soldier, Frog, Spider) do not talk, and the writer saves empty verses for them.

### NPCs (`TEditPerson`, `TPersonAction`)

An NPC has a GIF image (or none) and a GS1 script. The script editor has *Test* (syntax check, with the error shown in a status line) and *Style*, plus the usual Undo/Cut/Copy/Paste menu. Runtime flags set by scripts while testing appear in *Edit flags* (`TEditFlags`). That dialog edits the offline flag list, not anything stored in the level.

### Character NPCs (`TEditCharacter`)

A form generates a script that sets up a walking character. The fields are character, shield, nickname, horse, direction, walk mode (None/Random/Left-Right/Up-Down/Rectangle), speed, attack mode (None/Sword), hunt speed, sword power, attack verse, power, roaming box X1–X2/Y1–Y2, respawn time, and the flags *can be carried*, *sword hurts*, *bomb/arrow/stone hurts*, and *attack other npcs too*. The output starts with `// Graal v1.4 NPC by Stefan Knorr` and `showcharacter;` / `setcharprop` lines. After that the NPC is an ordinary NPC: double-clicking it opens the normal NPC editor. **[2.05]** Several tutorial NPCs were made this way.

### Stamps (predefined objects)

Object sets are read from every `objects*.txt` file listed in the file-name cache. The set name is the part between `objects` and `.txt`, and plain `objects.txt` is the *Standard* set. Each file is `GOBJSET01` (see `formats/gobjset01.md`). *Add the selection to the objects* names the current selection (`TObjectName`) and inserts it after the selected stamp. *New* (`TObjectSet`) creates `objects<setname>.txt`. *Save objects* rewrites the set file.

## Saving

The file extension picks the format. **[2.05]**

- **`.nw`**: GLEVNW01 text. It writes `GLEVNW01`, then 64 `BOARD 0 y 64 0 <base64 tiles>` rows, then `LINK …`, `SIGN x y` … `SIGNEND`, `CHEST …`, `BADDY x y type` + three verse lines + `BADDYEND`, and `NPC image x y` … `NPCEND` (image `-` when there is none).
- **Anything else** (normally `.graal`): always `GR-V1.03`. The 2.05 editor cannot write older GR versions.

GR-V1.03 writer details, which complement `formats/level-binary.md`:

- The board is written with 13-bit codes. The encoder emits a single run (`count` ≤ 64) for two or more equal tiles, and a **double run** (`ABAB…`, ≤ 64 pairs) when the pattern `A B A B` starts at the cursor. Otherwise it emits a plain tile. So 2.05 does write double runs, which answers one of the open questions in that file.
- Baddy records are `x, y, type` as raw bytes (not +32), then `verse1\verse2\verse3\n`. The section ends with `FF FF FF 0A`.
- NPC records are `x+32, y+32, image#script\n`. Chest records are four GCHARs. Sign records are two GCHARs plus sign-alphabet text.
- Saving a level that was opened from a URL (`http://…`) falls through to *Save as*.

Opening accepts `Z3-V1.03`, `Z3-V1.04`, `GR-V1.00`–`GR-V1.03`, and `GLEVNW01`. Anything else gives "Unsupported file type!".

## Loader note for formats/level-binary.md

The 2.05 loader picks the code width by magic: **13 bits only for `GR-V1.02` and `GR-V1.03`, 12 bits for `GR-V1.00`, `GR-V1.01`, and `Z3-V1.*`.** The section order also depends on the magic: NPCs from `GR-V1.00` on, and chests from `GR-V1.01` on. The baddy section ends at the first record shorter than three bytes or whose first byte is ≥ 0x80. It does not need a literal `FF FF FF`. An x byte of 0 is a valid baddy, not a terminator (corrected 2026-10-25; the loader has no x = 0 test in 1.39, 2.00, 2.05, 2.17.1 or 2.22; see `decomp-findings-2026-10-25-f/03-baddy-terminator.md`). **[2.05]**

## Open

- How *Generate map* walks the neighbouring levels has not been traced.
- Whether the *Edit flags* list is saved anywhere offline.
