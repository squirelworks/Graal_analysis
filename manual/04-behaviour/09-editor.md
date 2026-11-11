<!-- manual: kind=reference status=draft -->
# 4.9 The built-in editor

This chapter gives what is particular to the editor built into the 2.05 client: how play and editing switch, what entering the editor does to the game, and what it writes. The editor's window, dialogs and objects, and the later standalone GraalEditor, are in → §11.6; the level formats it reads and writes are in → §3.1.

> Status: draft. Read from 2.05 rev 2, with Generate map, Play and Edit flags checked live on 2.05 rev 2.

## 4.9.1 Where the editor lives

Where the level editor lives changed between 2.05 and 2.31. Each row gives a build and its editor [2.05] (client-internals/level-editor-205.md).

| Builds | Editor | Source |
| --- | --- | --- |
| 2.05 | a second mode of the main game window, not a separate program | [2.05] (client-internals/level-editor-205.md) |
| 2.31 | the client has no editor of its own; the start screen's Editor button starts `GraalEditor.exe` from the game folder as a separate process (→ §11.6) | [live] (client-internals/live-checks-editor-offline-sound.md#231-and-graaleditor) |

## 4.9.2 Switching between play and editing (2.05)

Four keys move a 2.05 player between play and editing. Each row gives a key and what it does in game mode [2.05] (client-internals/level-editor-205.md#entering-and-leaving).

| Key | In game mode | Source |
| --- | --- | --- |
| F4 | opens the editor; refused while connected, with a message that the editor cannot be opened online (→ §4.8.1) | [2.05] (client-internals/level-editor-205.md#entering-and-leaving) |
| F5 | the Load level dialog; online it first warns that loading disconnects from the server (→ §4.8.2) | [2.05] (client-internals/level-editor-205.md#entering-and-leaving) |
| P or the Play button | back to game mode on the current level (→ §4.9.4) | [2.05] (client-internals/level-editor-205.md#entering-and-leaving) |
| Close | closes the current level tab, asking to save a modified level | [2.05] (client-internals/level-editor-205.md#entering-and-leaving) |

The rules below give what happens on the way into the editor, how a level on the command line is opened, and which keys a focused field blocks [2.05] (client-internals/level-editor-205.md#entering-and-leaving).

| Rule | Detail | Source |
| --- | --- | --- |
| teardown | entering the editor stops looped sounds (→ §4.7.1), frees the level's NPC and baddy instances, and opens the player's level as a tab re-read from disk, so board changes made while playing are not carried over; the view centres on the player | [2.05] (client-internals/level-editor-205.md#entering-and-leaving) |
| command line | `Graal.exe path\level.graal` skips the login screen, changes into the file's folder, creates a local player at (30, 30.5) and opens the file in the editor | [2.05] (client-internals/level-editor-205.md#entering-and-leaving) |
| editor keys | L, S, P and M (links, signs, play, generate map) are ignored while a combo box in the side panel has focus; the full key list is in → §11.6 | [2.05] (client-internals/level-editor-205.md#editor-keys) |
| NPC with no image | shown with a placeholder picture only in the editor's view (→ §4.6.2.3) | [2.05] (client-internals/sign-panel.md#npcs-with-no-image) |

## 4.9.3 Undo (2.05)

Undo covers board tiles only. The rules below give what is recorded, how deep the stack goes and what an undo restores [2.05] (client-internals/level-editor-205.md#undo).

| Rule | Detail | Source |
| --- | --- | --- |
| scope | board tiles only, hence the button's name, Undo board copy; links, signs, NPCs, baddies and chests are not undoable | [2.05] (client-internals/level-editor-205.md#undo) |
| record | before any board write: the rectangle (x, y, width, height) and the tiles it overwrites | [2.05] (client-internals/level-editor-205.md#undo) |
| stack | one per level tab, at most 128 records; the oldest is dropped when full | [2.05] (client-internals/level-editor-205.md#undo) |
| undo | pops the newest record, writes the old tiles back, re-selects the rectangle (or clears the selection if it was the whole board) and marks the level modified | [2.05] (client-internals/level-editor-205.md#undo) |

## 4.9.4 Play, flags and the map image (2.05)

The rules below cover the editor's Play button, its flag list and how it builds the map image [live][2.05] (client-internals/live-checks-editor-offline-sound.md#play-saves-first).

| Rule | Detail | Source |
| --- | --- | --- |
| Play saves first | Play on a named, modified level writes it to disk ("Level saved") before the Level options dialog asks for the start position; a level with no name must be saved under a name first; 2.22 does the same (→ §11.6) | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#play-saves-first); [2.05] (client-internals/level-editor-205.md#entering-and-leaving) |
| Edit flags | edits the client's in-memory flag list, not anything in the level; the list survives Play and a return to the editor, but is never written to disk or the registry and is gone after a restart | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#edit-flags) |
| Generate map (M) | after a prompt that it may take minutes, walks the level list of the loaded big map (`bigmap.txt` or the list a `setmap` NPC loaded) in list order, row by row | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#generate-map-m) |
| Generate map, each level | read from disk, its NPCs run into a 1024 × 1024 view, shrunk to 56 × 56 px; a missing or unreadable entry is a blank square; links are not followed, so a level not in the list (such as the tutorial house) is skipped | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#generate-map-m) |
| Generate map, output | offered in a save dialog as `graalmap.png` in the level's folder; the 3 × 4 tutorial list gave a 168 × 224 image; the level that was open is restored afterwards | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#generate-map-m) |

## 4.9.5 Saving and opening (2.05)

The editor writes a level by its extension. The rules below give the format chosen, how the board is packed and two edge cases [2.05] (client-internals/level-editor-205.md#saving).

| Rule | Detail | Source |
| --- | --- | --- |
| format by extension | `.nw` is written as `GLEVNW01` text (→ §3.1); any other extension, normally `.graal`, always as `GR-V1.03`; the 2.05 editor cannot write older versions | [2.05] (client-internals/level-editor-205.md#saving) |
| `GR-V1.03` board | the writer emits a single run for two or more equal tiles and a double run when `A B A B` starts at the cursor, otherwise a plain tile (→ §3.1) | [2.05] (client-internals/level-editor-205.md#saving) |
| baddy section | ends with `FF FF FF 0A` on write; the reader does not need it (→ §3.1) | [2.05] (client-internals/level-editor-205.md#saving); [2.05] (client-internals/level-editor-205.md#loader-note-for-formatslevel-binarymd) |
| URL levels | saving a level opened from a URL falls through to Save as | [2.05] (client-internals/level-editor-205.md#saving) |
| opening | accepts `Z3-V1.03`, `Z3-V1.04`, `GR-V1.00` to `GR-V1.03` and `GLEVNW01`; anything else is refused as an unsupported file type | [2.05] (client-internals/level-editor-205.md#saving) |
| chest items | in index order: greenrupee, bluerupee, redrupee, bombs, darts, heart, glove1, bow, bomb, shield, sword, fullheart, superbomb, battleaxe, goldensword, mirrorshield, glove2, lizardshield, lizardsword, goldrupee, fireball, fireblast, nukeshot, joltbomb, spinattack (→ §4.5.4) | [2.05] (client-internals/level-editor-205.md#chests-tchestedit) |
| new chest | defaults to item 1 (bluerupee) and no sign (−1) | [2.05] (client-internals/level-editor-205.md#chests-tchestedit) |
