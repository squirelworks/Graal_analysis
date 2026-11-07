<!-- manual: kind=reference status=draft -->
# 4.6 HUD, sign panel, chat text and options

This chapter covers what the client draws over the game view: the status display, the sign panel, chat text and nicknames over players, and the item list window, plus what the in-game options change while playing. The file formats behind them are in → §3.6 (sign text), §3.9 (config) and §3.10 (sheets).

> Status: draft. The HUD, sign panel and item list are read from 2.05 rev 2; chat text is read from every Delphi build and checked live on 2.05 rev 2. The player list window is in → §4.10.

## 4.6.1 The status display

### 4.6.1.1 Sheet

| Rule | Detail | Source |
| --- | --- | --- |
| sheet | every build from 1.41 on ships a 224 × 145 `state.png` | [file] (client-internals/status-display.md#sheets) |
| 2.22 against 2.05 | the 2.22 sheet matches the 2.05 rev 2 and 2.1 test 3 sheets pixel for pixel except one 27 × 14 patch at (190, 60), which the status routine does not use | [file] (client-internals/status-display.md#sheets) |
| buttons | 1.41's sheet has three blank buttons at x 158, 180 and 202; the 2.0-era NewMain sheets have one, at x 202, which the routine draws in all three slots | [file] (client-internals/status-display.md#sheets) |

### 4.6.1.2 Layout (2.05 rev 2)

Positions are from the top-left of the game view; the routine's base point is (15, 15). Each part is drawn only when its `showstats` bit is set:

| Part | `showstats` bit | Sheet rect (x, y, w, h) | Screen position | Source |
| --- | --- | --- | --- | --- |
| rupee, bomb and arrow icons | 0x02 | (80, 33, 120, 16), one strip | (274, 30) | [2.05] (client-internals/status-display.md#layout) |
| rupee count | 0x04 | digit d at (14d, 81, 14, 16) | 1 to 7 digits, no leading zeros, 12 px apart, centred on x 280, y 48 | [2.05] (client-internals/status-display.md#layout) |
| bomb count | 0x08 | same digits | two digits at x 326 and 338, y 48 | [2.05] (client-internals/status-display.md#layout) |
| arrow count | 0x10 | same digits | two digits at x 374 and 386, y 48 | [2.05] (client-internals/status-display.md#layout) |
| hearts | 0x20 | big (40·half, 0, 40, 44); small (80 + 31·half, 0, 31, 33) | → §4.6.1.3 | [2.05] (client-internals/status-display.md#layout) |
| buttons | 0x01 | (202, 0, 22, 33) | x 15, 80 and 145, y 30 | [2.05] (client-internals/status-display.md#layout) |
| key names | 0x01 | text | on each button, 26 pt Helvetica, white with a black copy at +1, +1; smaller for longer key names; the item-list key drawn small at (147, 27) | [2.05] (client-internals/status-display.md#layout) |
| glove icon | 0x01 | sprite 145 for power 2, sprite 325 on top for power 3 | (40, 29); the power printed at (60, 31) when 2 or more | [2.05] (client-internals/status-display.md#layout) |
| sword icon | 0x01 | sprite 17, from the player's sword image | (105, 31); the sword power printed at (125, 31) | [2.05] (client-internals/status-display.md#layout) |
| selected weapon | 0x01 | the weapon's whole image | x 170, centred on y 45 | [2.05] (client-internals/status-display.md#layout) |
| alignment bar | 0x40 | frame (0, 97, 130, 22); fill (0, 119, AP, 10) | (15, 65); fill at +22, +6 | [2.05] (client-internals/status-display.md#layout) |
| magic bar | 0x80 | frame (0, 49, 130, 22); fill (0, 71, MP, 10) | (15, 90); only with weapons on and MP above 0 | [2.05] (client-internals/status-display.md#layout) |

| Rule | Detail | Source |
| --- | --- | --- |
| other bits | 0x100 and 0x200 belong to the player icons and the stacked weapon image list, drawn by the same routine but not part of the status display | [2.05] (client-internals/status-display.md#layout) |
| sprite rects | sprites 17, 145 and 325 come from `arrays.dat` array 24 (→ §3.5): 17 is (94, 36, 28, 28) of the sword image; 145 is (28, 212, 28, 32) and 325 is (0, 212, 28, 32) of `sprites.png` | [file] (client-internals/status-display.md#layout) |
| weapons flag | with weapons off only the first button, its key name and the alignment bar are drawn; the same flag gates the S and D keys | [2.05] (client-internals/status-display.md#layout) |

### 4.6.1.3 Hearts

| Rule | Detail | Source |
| --- | --- | --- |
| which | one heart per container while power remains; empty containers are not drawn; heart *i* is full when power − 1 ≥ *i* and half when *i* < power | [2.05] (client-internals/status-display.md#hearts) |
| big hearts | while power is 4 hearts or less; from (W − 198, 24), 45 px apart, W the view width | [2.05] (client-internals/status-display.md#hearts) |
| small hearts | above 4 hearts, 35 px apart; new rows start at hearts 5, 11, 16, 22 and 27; row *k* + 1 is 20(*k* + 1) px lower and shifted round(17.5(*k* + 1)) − 35 px sideways; the block moves 10 px down while power is below 6 | [2.05] (client-internals/status-display.md#hearts) |

### 4.6.1.4 The selected weapon

| Rule | Detail | Source |
| --- | --- | --- |
| one list | server weapons (`PLO_NPCWEAPONADD`) and built-in weapons (`PLO_DEFAULTWEAPON`) share one list in arrival order; a built-in weapon is skipped when the list already has its name (→ §2.5) | [2.05] (client-internals/status-display.md#the-selected-weapon-205-rev-2) |
| adding | every add selects the new last entry | [2.05] (client-internals/status-display.md#the-selected-weapon-205-rev-2) |
| selecting index *i* | the first entry from *i* on, wrapping round, whose name is not empty and does not start with `-`; if every entry is hidden, *i* stays selected | [2.05] (client-internals/status-display.md#the-selected-weapon-205-rev-2) |
| deleting | the selection keeps its index if it still exists, otherwise it moves to the new last entry | [2.05] (client-internals/status-display.md#the-selected-weapon-205-rev-2) |
| built-in weapons | of the 25-entry item table, only ids 7 bow, 8 bomb, 12 superbomb, 20 fireball, 21 fireblast, 22 nukeshot and 23 joltbomb are weapons; the name is the item name with a capital first letter | [2.05] (client-internals/status-display.md#built-in-weapons) |
| images | `wbowi1` to `wbowi4` and `wbomb1` to `wbomb3` (`.gif` in 2.05); 2.22 asked for the same names as `.png` | [2.05][lab][2.22] (client-internals/status-display.md#built-in-weapons) |

### 4.6.1.5 Not measured

| Item | State | Source |
| --- | --- | --- |
| 2.22 and 2.31 status routines | unmeasured; their sheets and a 2.22 screenshot match 2.05 | [cap] (client-internals/status-display.md#not-read) |
| builds before 2.05, including 1.41's three button cells | unmeasured | [doc] (client-internals/status-display.md#not-read) |
| font, colour and anchor of the glove and sword power text | unmeasured | [doc] (client-internals/status-display.md#not-read) |

## 4.6.2 The sign panel (2.05)

### 4.6.2.1 Drawing

| Rule | Detail | Source |
| --- | --- | --- |
| sheet | `letters.png`, 256 × 224, 16 glyphs a row, each 16 × 32; glyph `g` at (g mod 16 × 16, g div 16 × 32); loaded once at start; the glyph order is the sign alphabet of → §3.6 | [2.05] (client-internals/sign-panel.md#the-sheet) |
| advances | each glyph has its own advance, twice the client's half-width table (I 6 px, space 8, most letters 12) | [2.05] (client-internals/sign-panel.md#the-sheet) |
| frame glyphs | 96 to 99 corners (top-left, top-right, bottom-left, bottom-right), 100 and 101 top and bottom edge, 102 and 103 left and right edge | [2.05] (client-internals/sign-panel.md#the-sheet) |
| button glyphs | 91 to 94 the A, B, X and Y buttons; 77 to 80 up, down, left, right; 71 to 75, 87, 88 and 67 the other button pictures | [2.05] (client-internals/sign-panel.md#the-sheet) |
| fill colours | the pixels at (254, 223) and (255, 223) are the outer fill and, 8 px further in, the inner fill; a fill in the sheet's transparent colour is skipped; cream and cream on the 2.22 sheet, inner white on 1.39 | [2.05][file] (client-internals/sign-panel.md#the-sheet) |
| size | 24 cells wide and 9 tall (16 px cells), centred across the view | [2.05] (client-internals/sign-panel.md#the-panel) |
| vertical place | 640-wide view: y 256, or y 128 when the player is more than 14 tiles down the view; 800: 18 tiles, y 320 or 160; 1024: 22 tiles, y 448 or 192; which two values are compared is inferred | [2.05][inf] (client-internals/sign-panel.md#the-panel) |
| frame order | top and bottom edges every 16 px, sides every 32 px, corners over them, then the two fills from (x + 16, y + 24) | [2.05] (client-internals/sign-panel.md#the-panel) |
| text | three lines a page from (x + 16, y + 16), 32 px apart; the text is split at newlines | [2.05] (client-internals/sign-panel.md#the-panel) |
| `#` codes | `#A #B #X #Y #u #d #l #r #h #x #y #z #4 #.` draw button pictures; `#` and any other letter draws glyph 86 and moves 16 px; `#i` and a character shows an image from the level's list | [2.05] (client-internals/sign-panel.md#the-panel) |
| other characters | a character outside the glyph order is drawn in the system font, in the colour at (253, 223) | [2.05] (client-internals/sign-panel.md#the-panel) |
| check | not compared against a screenshot of a real client | [doc] (client-internals/sign-panel.md#confirmed-inferred-not-tested) |

### 4.6.2.2 Keys while reading

| Rule | Detail | Source |
| --- | --- | --- |
| own state | reading is its own input state: the player does not walk, swing, lift or use an item; switch-to-chat still works, and while the chat bar has focus the sign keys are skipped | [2.05] (client-internals/sign-panel.md#keys-while-reading) |
| map key | ends reading at once | [2.05] (client-internals/sign-panel.md#keys-while-reading) |
| up | turns back three lines, unless on the first page | [2.05] (client-internals/sign-panel.md#keys-while-reading) |
| other game keys | left, down, right, D, S, A, item list and pause turn to the next three lines; when the page on show is not full, reading ends instead, so a sign of exactly three lines shows an empty second page before it closes | [2.05] (client-internals/sign-panel.md#keys-while-reading) |
| edge | a key counts only when no game key was down on the tick before; a held key does not repeat (→ §4.1.2.1) | [2.05] (client-internals/sign-panel.md#keys-while-reading) |
| side effects | `nextpage.wav` on each page turn (→ §4.7.3); `playerendsreading` runs when reading ends | [2.05][live] (client-internals/sign-panel.md#keys-while-reading); [live] (client-internals/live-checks-editor-offline-sound.md#sound-205) |

### 4.6.2.3 NPCs with no image

| Rule | Detail | Source |
| --- | --- | --- |
| in game | an NPC with no image draws nothing of its own, only its text if any | [2.05] (client-internals/sign-panel.md#npcs-with-no-image) |
| gani and character NPCs | drawn from the gani, or the way players are drawn | [2.05] (client-internals/sign-panel.md#npcs-with-no-image) |
| placeholder | the placeholder picture appears only in the level editor's view (→ §4.9) | [2.05] (client-internals/sign-panel.md#npcs-with-no-image) |

## 4.6.3 Chat text and nicknames

The chat line is player prop 12 (→ §2.6.2); the chat and PM messages are in → §2.8.

### 4.6.3.1 Font

| Builds | Face | Height (px, cell) | Shadow | Source |
| --- | --- | --- | --- | --- |
| 1st Graal, 4th, 9th, 15th, 1.1.9, 1.21 | `Dialog` | 28 | always blue | [bin] (client-internals/chat-text.md#font-per-build) |
| 1.31, 1.38 | `Dialog` | 28 | contrast rule | [bin] (client-internals/chat-text.md#font-per-build) |
| 1.39, 1.41 | `Helvetica` | 24 | contrast rule | [bin] (client-internals/chat-text.md#font-per-build) |
| NewMain 1.42, 2.00 to 2.05 rev 2, 2.17, 2.22, 2.31 | `Tempus Sans ITC`, installed from the client folder | 24 | contrast rule | [bin] (client-internals/chat-text.md#font-per-build) |

| Rule | Detail | Source |
| --- | --- | --- |
| drawing | straight onto the game view with the Windows canvas, bold, no bubble and no box | [bin][live][2.05] (client-internals/chat-text.md) |
| config | from 1.31 on, `font=` and `fontsize=` replace the defaults (→ §3.9.3) | [bin] (client-internals/chat-text.md#font-per-build) |
| height | the value is the cell height in pixels, not a point size; for Tempus Sans ITC a 24 px cell is an em of about 18.4 px, which the live capture matches | [bin][live][2.05] (client-internals/chat-text.md#font-per-build) |
| missing faces | `Dialog` does not exist on Windows and is mapped to a sans serif, normally Arial; `Helvetica` maps to Arial; neither was checked on real Windows | [inf] (client-internals/chat-text.md#font-per-build) |
| bold | Tempus Sans ITC has only a regular face, so Windows emboldens it: each glyph smeared one pixel right, each advance one pixel wider | [inf] (client-internals/chat-text.md#font-per-build) |

### 4.6.3.2 Colour and position

| Rule | Detail | Source |
| --- | --- | --- |
| colour | chat is white | [bin] (client-internals/chat-text.md#colour-and-shadow) |
| passes | shadow at (+1, +1), then text at (0, 0) | [bin] (client-internals/chat-text.md#colour-and-shadow) |
| shadow, 1.21 and earlier | always RGB (0, 0, 255) | [bin] (client-internals/chat-text.md#colour-and-shadow) |
| shadow, 1.31 on | red and green 0 if the text's red or green is above 0xE0, otherwise 0xFF; blue equals the text's blue; the same routine draws nicknames and number pop-ups | [bin] (client-internals/chat-text.md#colour-and-shadow) |
| x | centred on the player's x + 1.5 tiles | [bin] (client-internals/chat-text.md#position) |
| y | the top of the text cell at the player's y − 1 tile, or y − 2 while carrying (the carry part read, not checked live) | [bin][live][2.05] (client-internals/chat-text.md#position) |
| clip | to the level view rectangle | [bin] (client-internals/chat-text.md#position) |

### 4.6.3.3 Wrapping

| Builds | Rule | Source |
| --- | --- | --- |
| 1.21 and earlier | one centred line, clipped, no wrapping | [bin] (client-internals/chat-text.md#wrapping-131-and-later) |
| 1.31 and later | text wider than the view (640 px in 2.05) is split at spaces; a word that does not fit starts the next line, and a word too long for a line stands alone, unbroken | [bin] (client-internals/chat-text.md#wrapping-131-and-later) |
| 1.31 and later | lines stack upward so the last line sits on the anchor; each line is centred on its own, then pushed left to fit the right edge and right to start at 0 or more | [bin] (client-internals/chat-text.md#wrapping-131-and-later) |
| 6.x | wraps only text of 11 or more characters, breaking after any of ` .,;+-?!` | [doc] (client-internals/chat-text.md#wrapping-131-and-later) |

### 4.6.3.4 How long chat stays (2.05 rev 2)

| Rule | Detail | Source |
| --- | --- | --- |
| own line | stays while the player stands still (over 7 minutes seen); the first direction key starts a 60-tick (3 s) countdown, after which the line goes and the client sends an empty chat prop | [live][2.05] (client-internals/chat-text.md#how-long-it-stays-live-205-rev-2-2026-10-30) |
| another player's line | shows for at least 3 s from arrival and until that player's empty chat arrives; an empty line only waits out what is left of the 3 s, it does not start a fresh 3 s; with no empty line the text stays | [live][2.05] (client-internals/chat-text.md#how-long-it-stays-live-205-rev-2-2026-10-30) |
| length | a line longer than 256 characters is cut to 253 characters plus `...` when sent; the receiver draws what arrives | [bin] (client-internals/chat-text.md#length) |
| `showap` | a chat of exactly `showap` shows the player's AP instead of the text | [2.05] (client-internals/chat-text.md#special-texts-205) |
| other uses of the slot | while a per-player counter runs it shows two numbers joined by `/`; in some sprite states it shows an item image or a carried number; the chat is then not drawn; these branches were read but not named | [2.05] (client-internals/chat-text.md#special-texts-205) |

### 4.6.3.5 Nicknames (1.31 to 2.31)

| Rule | Detail | Source |
| --- | --- | --- |
| position | drawn by the chat routine, centred on x + 1.5 tiles, the top of the text cell at y + 2.5 tiles | [bin][live][2.05] (client-internals/chat-text.md#nickname-131-to-231) |
| other players | always shown | [bin] (client-internals/chat-text.md#nickname-131-to-231) |
| own name | shown for 60 ticks (3 s) after setup (so at login), after an AP change, and after typing exactly `showname`, which is not sent | [bin][live][2.05] (client-internals/chat-text.md#nickname-131-to-231) |
| length | cut to `nicknamelimit` (default 50) only when `limitnicknames` is on (off by default) | [2.05] (client-internals/chat-text.md#nickname-131-to-231) |
| colour | follows AP (prop 32, → §2.6.2); 1.21 has no AP colours; the same ramp is in every build from 1.31 to 2.31 | [bin] (client-internals/chat-text.md#nickname-131-to-231) |

The AP colour ramp, each step `floor(n × k / d)` with a 0.0001 bias:

| AP | Colour (R, G, B) | Source |
| --- | --- | --- |
| 0 | (64, 0, 0) | [bin] (client-internals/chat-text.md#nickname-131-to-231) |
| 1 to 26 | (128 + (ap − 1)·127/25, 64 − (ap − 1)·64/25, same as G), dark red to red | [bin] (client-internals/chat-text.md#nickname-131-to-231) |
| 27 to 49 | (255, (ap − 26)·255/24, same as G), red to pale pink | [bin] (client-internals/chat-text.md#nickname-131-to-231) |
| 50 to 55 | white | [bin] (client-internals/chat-text.md#nickname-131-to-231) |
| 56 to 60 | (255 − (ap − 55)·127/5, 255, same as R), white to light green | [bin] (client-internals/chat-text.md#nickname-131-to-231) |
| 61 to 70 | (128 − (ap − 61)·128/10, 255, 128 + (ap − 61)·127/10), light green to cyan | [bin] (client-internals/chat-text.md#nickname-131-to-231) |
| 71 to 99 | (0, 255 − (ap − 70)·255/29, 255), cyan to blue | [bin] (client-internals/chat-text.md#nickname-131-to-231) |
| 100 | (224, 196, 0), gold | [bin] (client-internals/chat-text.md#nickname-131-to-231) |
| live check | AP 0, 20, 40, 58, 65, 85 and 100 drew exactly (64,0,0), (224,16,16), (255,148,148), (179,255,179), (77,255,178), (0,124,255) and (224,196,0); AP 50, the value before any AP is sent, was white | [live][2.05] (client-internals/chat-text.md#nickname-131-to-231) |

## 4.6.4 The item list (2.05)

| Rule | Detail | Source |
| --- | --- | --- |
| key | the `itemlist` action (index 9; default Q) opens and closes the list; it opens from the normal state only when a player flag allows it, flag not identified | [2.05] (client-internals/decomp-findings-2026-10-28/02-item-list.md) |
| content | the player's built-in and NPC weapons; a `/` in a weapon name makes a folder, and the current level's folders come first as 32 × 32 cells; names starting with `-` are skipped when selecting | [2.05] (client-internals/decomp-findings-2026-10-28/02-item-list.md) |
| window | framed, from (16, 80) to 16 px from the right and bottom edges; cells from (48, 112) to 48 px from the right and 64 px from the bottom | [2.05] (client-internals/decomp-findings-2026-10-28/02-item-list.md) |
| cells | max(image width, label width) + 10 wide, image height + label height + 15 tall, packed in the first free place left to right then down; image centred 5 px from the top, label centred below; a weapon with no image gets a 32 × 32 placeholder; the selected cell is filled RGB(255, 212, 128); font size 16; scroll arrows when cells are cut off | [2.05] (client-internals/decomp-findings-2026-10-28/02-item-list.md) |
| arrows | stretch the selected cell to the edge in that direction and take the overlapping cell with the closest near edge; moving selects the weapon at once and sends nothing | [2.05] (client-internals/decomp-findings-2026-10-28/02-item-list.md) |
| other keys | item key or Enter opens a folder, the attack key goes up a folder, other game keys and Esc close the list, a click selects a cell | [2.05] (client-internals/decomp-findings-2026-10-28/02-item-list.md) |
| Delete | removes the selected weapon; online it sends `PLI_NPCWEAPONDEL` (29) with the name, or `PLI_NPCDEL` (22) with the NPC id for an NPC that is not a weapon (→ §2.4) | [2.05] (client-internals/decomp-findings-2026-10-28/02-item-list.md) |

## 4.6.5 Options at run time (2.05)

The file, its keys and its parse rules are in → §3.9; this table gives what each option does while playing.

| Options | Effect | Source |
| --- | --- | --- |
| `musicon`, `soundfxon`, `reversestereo`, `usewinamp` | sound and music (→ §4.7) | [2.05] (client-internals/feature-specs/09-options.md#what-the-options-change-at-run-time) |
| `noudp`, `fixedport`, `fixedudpport` | the UDP channel (→ §2.9) | [2.05] (client-internals/feature-specs/09-options.md#what-the-options-change-at-run-time) |
| `nomassmessages`, `notoalls`, `nohtmlinpms`, `nohtmlimages`, `sortplayersbyname`, `dontloadlistheads` | the player list and messages (→ §4.10) | [2.05] (client-internals/feature-specs/09-options.md#what-the-options-change-at-run-time) |
| `dontconnectlevels` | stops loading the neighbour levels of a gmap ahead of time | [2.05] (client-internals/feature-specs/09-options.md#what-the-options-change-at-run-time) |
| `limitnicknames`, `nicknamelimit` | cut drawn nicknames (→ §4.6.3.5) | [2.05] (client-internals/feature-specs/09-options.md#what-the-options-change-at-run-time) |
| network | none of the options is sent to the server | [2.05] (client-internals/feature-specs/09-options.md#what-it-is) |
| dialogs | More Options, Player List Options and the Controls frame; closing either dialog rewrites the whole file | [2.05] (client-internals/feature-specs/09-options.md#what-it-is) |
| later builds | 2.17 and later add volume keys and an Audio/Microphone tab (→ §3.10.4) | [2.17][2.22] (client-internals/feature-specs/09-options.md#keys-file-order-default) |
