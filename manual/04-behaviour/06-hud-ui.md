<!-- manual: kind=reference status=draft -->
# 4.6 HUD, sign panel, chat text and options

This chapter covers what the client draws over the game view: the status display, the sign panel, chat text and nicknames over players, and the item list window, plus what the in-game options change while playing, the windows on the function keys, and the server message window. The file formats behind them are in → §3.6 (sign text), §3.9 (config) and §3.10 (sheets).

> Status: draft. The HUD, sign panel and item list are read from 2.05 rev 2; chat text is read from every Delphi build and checked live on 2.05 rev 2. The player list window is in → §4.10.

## 4.6.1 The status display

### 4.6.1.1 Sheet

The status display is drawn from one sheet. The rules below give its size and how it changed between builds [file] (client-internals/status-display.md#sheets).

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

The table above gives the layout. These rules add the parts drawn by the same routine, the sprite rectangles it uses and the weapons flag [2.05] (client-internals/status-display.md#layout).

| Rule | Detail | Source |
| --- | --- | --- |
| other bits | 0x100 and 0x200 belong to the player icons and the stacked weapon image list, drawn by the same routine but not part of the status display | [2.05] (client-internals/status-display.md#layout) |
| sprite rects | sprites 17, 145 and 325 come from `arrays.dat` array 24 (→ §3.5): 17 is (94, 36, 28, 28) of the sword image; 145 is (28, 212, 28, 32) and 325 is (0, 212, 28, 32) of `sprites.png` | [file] (client-internals/status-display.md#layout) |
| weapons flag | with weapons off only the first button, its key name and the alignment bar are drawn; the same flag gates the S and D keys | [2.05] (client-internals/status-display.md#layout) |

### 4.6.1.3 Hearts

Hearts are drawn big or small depending on how many the player has. The rules below give which hearts are shown and where each row goes [2.05] (client-internals/status-display.md#hearts).

| Rule | Detail | Source |
| --- | --- | --- |
| which | one heart per container while power remains; empty containers are not drawn; heart *i* is full when power − 1 ≥ *i* and half when *i* < power | [2.05] (client-internals/status-display.md#hearts) |
| big hearts | while power is 4 hearts or less; from (W − 198, 24), 45 px apart, W the view width | [2.05] (client-internals/status-display.md#hearts) |
| small hearts | above 4 hearts, 35 px apart; new rows start at hearts 5, 11, 16, 22 and 27; row *k* + 1 is 20(*k* + 1) px lower and shifted round(17.5(*k* + 1)) − 35 px sideways; the block moves 10 px down while power is below 6 | [2.05] (client-internals/status-display.md#hearts) |

### 4.6.1.4 The selected weapon

One list holds every weapon. The rules below give how entries are added, selected and deleted [2.05] (client-internals/status-display.md#the-selected-weapon-205-rev-2).

| Rule | Detail | Source |
| --- | --- | --- |
| one list | server weapons (`PLO_NPCWEAPONADD`) and built-in weapons (`PLO_DEFAULTWEAPON`) share one list in arrival order; a built-in weapon is skipped when the list already has its name (→ §2.5) | [2.05] (client-internals/status-display.md#the-selected-weapon-205-rev-2) |
| adding | every add selects the new last entry | [2.05] (client-internals/status-display.md#the-selected-weapon-205-rev-2) |
| selecting index *i* | the first entry from *i* on, wrapping round, whose name is not empty and does not start with `-`; if every entry is hidden, *i* stays selected | [2.05] (client-internals/status-display.md#the-selected-weapon-205-rev-2) |
| deleting | the selection keeps its index if it still exists, otherwise it moves to the new last entry | [2.05] (client-internals/status-display.md#the-selected-weapon-205-rev-2) |
| built-in weapons | of the 25-entry item table, only ids 7 bow, 8 bomb, 12 superbomb, 20 fireball, 21 fireblast, 22 nukeshot and 23 joltbomb are weapons; the name is the item name with a capital first letter | [2.05] (client-internals/status-display.md#built-in-weapons) |
| images | `wbowi1` to `wbowi4` and `wbomb1` to `wbomb3` (`.gif` in 2.05); 2.22 asked for the same names as `.png` | [2.05][lab][2.22] (client-internals/status-display.md#built-in-weapons) |

### 4.6.1.5 Not measured

Some of the status display has not been read. The table lists what is still unmeasured, so a reader does not take the 2.05 layout as proven for other builds [cap] (client-internals/status-display.md#not-read).

| Item | State | Source |
| --- | --- | --- |
| 2.22 and 2.31 status routines | unmeasured; their sheets and a 2.22 screenshot match 2.05 | [cap] (client-internals/status-display.md#not-read) |
| the 1998 betas to 1.28 beta 2 | measured from captures since: → §4.6.1.6 | [cap] (client-internals/beta-hud-layouts.tsv) |
| 1.3x and 1.41, including 1.41's three button cells | unmeasured | [doc] (client-internals/status-display.md#not-read) |
| font of the key letters and the sword power text, 2.0x and 2.1x | traced under Wine since: → §4.6.1.7 | [lab] (client-internals/rebuild-traces-2026-11-05.md#status-display-text-20x-and-21x-wine-font-trace) |
| glove power text | not seen in a trace; the same routine prints it as the sword power, so it is taken to use the same font | [lab][inf] (client-internals/rebuild-traces-2026-11-05.md#status-display-text-20x-and-21x-wine-font-trace) |

### 4.6.1.6 The status display before 2.0 (1998 betas to 1.28 beta 2)

The early builds draw the status display from their own `state.gif` and the digit sprites of the body sheet (`link.gif` or `sprites.gif`). Each build's layout was measured by matching its sheets against the real client's first game frame, a 640 × 448 view, and every piece lands on the real frame to the pixel. The per-build table is the source; the rows below group the builds that share a layout [cap] (client-internals/beta-hud-layouts.tsv); [cap] (client-internals/rebuild-traces-2026-11-05.md#1998-betas-11-119-121-and-128-beta-2).

| Builds | Rupee count | Other parts | Source |
| --- | --- | --- | --- |
| 1st and 2nd Graal | three padded digits (`000`) from `link.gif`, 14 px high, 16 px apart, from x 230 | bomb count at x 294, arrows at x 342, all on y 48; full heart from (348, 0) | [cap] (client-internals/beta-hud-layouts.tsv) |
| 3rd Graal to 6th Graal | 14 px digits from sheet row 1472, 12 px apart, centred on x 250 | bombs at x 296, arrows at x 344; 5th Graal alpha and 6th Graal take the full heart from (228, 33) instead of (348, 33); 5th Graal moves the digits to `sprites.gif` | [cap] (client-internals/beta-hud-layouts.tsv) |
| 7th Graal to 15th Graal, 1.1, 1.1.9 | 16 px digits from row 1454, centred on x 250 | the redrawn `state.gif`: a 60 × 60 piece at (67, 15), a 31 × 30 piece at (146, 30) and the three counter icons | [cap] (client-internals/beta-hud-layouts.tsv) |
| 1.21, 1.28 beta 2 | 16 px digits from row 896, centred on x 280 | the A, S and D buttons at x 15, 80 and 145, and the sword picture (`sword1.gif`, 28 × 28) at (105, 31): the layout 2.05 keeps | [cap] (client-internals/beta-hud-layouts.tsv) |

The rules below add what every early build shares: where the hearts go and what a new game starts with [cap] (client-internals/rebuild-traces-2026-11-05.md#1998-betas-11-119-121-and-128-beta-2).

| Rule | Detail | Source |
| --- | --- | --- |
| hearts | 45 px apart from (422, 24), or from (442, 24) in 1.21 and 1.28 beta 2 | [cap] (client-internals/beta-hud-layouts.tsv) |
| start counts | 10 bombs, 5 arrows and 3 hearts; the rupees are 0 in most builds, 300 in 4th Graal alpha to 6th Graal, and 100 in 7th to 9th Graal | [cap] (client-internals/rebuild-traces-2026-11-05.md#1998-betas-11-119-121-and-128-beta-2) |
| gap | 1.3x to 1.41 were not measured this way, so the 2.05 layout is not assumed for them (→ §4.6.1.5) | [doc] (client-internals/status-display.md#not-read) |

### 4.6.1.7 Key letters and power text, 2.0x and 2.1x

The real NewMain 26 and NewWorld clients were run under Wine with a log of every font creation and text call. The table gives the font each build asks for and how the text is drawn; Wine maps the faces it lacks to Arial [lab] (client-internals/rebuild-traces-2026-11-05.md#status-display-text-20x-and-21x-wine-font-trace).

| What | Builds | Font asked for | Drawn | Source |
| --- | --- | --- | --- | --- |
| A, S, D key letters | 2.0 to 2.05 rev 2, 2.1 test 2 and 3, 2.17.1, NewMain 24 and 26 | `Helvetica`, cell 26, bold | black at +1, +1, then white, with the text origin one pixel right and two down from each button's corner: (16, 32), (81, 32), (146, 32) | [lab] (client-internals/rebuild-traces-2026-11-05.md#status-display-text-20x-and-21x-wine-font-trace) |
| item-list key over the D button | same | `Helvetica`, cell 10, bold | at (146, 27); the 2.05 static read gives (147, 27), and the routine was not rechecked | [lab] (client-internals/rebuild-traces-2026-11-05.md#status-display-text-20x-and-21x-wine-font-trace) |
| sword power, names under characters | same | `Tempus Sans ITC`, cell 24, bold, the `graalconfig.txt` font | white over a blue shadow, as chat (→ §4.6.3); the exe installs the bundled `tempsitc.ttf` before asking for it, and without it Windows falls back to Arial | [lab] (client-internals/rebuild-traces-2026-11-05.md#status-display-text-20x-and-21x-wine-font-trace) |
| A, S, D key letters | NewWorld betas | a face named `b`, cell 24, regular weight, which no system has, so Arial | white, no shadow, three pixels into each tag; the tags are 60 px apart | [lab] (client-internals/rebuild-traces-2026-11-05.md#status-display-text-20x-and-21x-wine-font-trace) |

The NewWorld betas draw a different status bar, matched pixel for pixel against a real NewWorld screen. Power shows as `POWER/MAX` (`150/150` offline) in `state.png`'s digits, right-aligned to end at x 540 on y 39; the bear sits at (532, 24) and the gralat orb at (274, 30) with its count. There are no hearts and no bomb or arrow counters. The clock and the sword picture are not placed yet [cap] (client-internals/rebuild-traces-2026-11-05.md#newworld-beta-status-bar).

## 4.6.2 The sign panel (2.05)

### 4.6.2.1 Drawing

Sign text is drawn from a bitmap font. The rules below give the sheet, the glyph advances and the glyphs that draw frames and buttons [2.05] (client-internals/sign-panel.md#the-sheet).

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

While a sign is open the keys do different things. The rules below give each key's effect [2.05] (client-internals/sign-panel.md#keys-while-reading).

| Rule | Detail | Source |
| --- | --- | --- |
| own state | reading is its own input state: the player does not walk, swing, lift or use an item; switch-to-chat still works, and while the chat bar has focus the sign keys are skipped | [2.05] (client-internals/sign-panel.md#keys-while-reading) |
| map key | ends reading at once | [2.05] (client-internals/sign-panel.md#keys-while-reading) |
| up | turns back three lines, unless on the first page | [2.05] (client-internals/sign-panel.md#keys-while-reading) |
| other game keys | left, down, right, D, S, A, item list and pause turn to the next three lines; when the page on show is not full, reading ends instead, so a sign of exactly three lines shows an empty second page before it closes | [2.05] (client-internals/sign-panel.md#keys-while-reading) |
| edge | a key counts only when no game key was down on the tick before; a held key does not repeat (→ §4.1.2.1) | [2.05] (client-internals/sign-panel.md#keys-while-reading) |
| side effects | `nextpage.wav` on each page turn (→ §4.7.3); `playerendsreading` runs when reading ends | [2.05][live] (client-internals/sign-panel.md#keys-while-reading); [live] (client-internals/live-checks-editor-offline-sound.md#sound-205) |

### 4.6.2.3 NPCs with no image

An NPC with no image draws nothing in play. The rules below say what is drawn instead in each case [2.05] (client-internals/sign-panel.md#npcs-with-no-image).

| Rule | Detail | Source |
| --- | --- | --- |
| in game | an NPC with no image draws nothing of its own, only its text if any | [2.05] (client-internals/sign-panel.md#npcs-with-no-image) |
| gani and character NPCs | drawn from the gani, or the way players are drawn | [2.05] (client-internals/sign-panel.md#npcs-with-no-image) |
| placeholder | the placeholder picture appears only in the level editor's view (→ §4.9) | [2.05] (client-internals/sign-panel.md#npcs-with-no-image) |

## 4.6.3 Chat text and nicknames

The chat line is player prop 12 (→ §2.6.2); the chat and PM messages are in → §2.8.

### 4.6.3.1 Font

The chat font changed three times. Each row gives a group of builds, the face, the cell height and the shadow rule [bin] (client-internals/chat-text.md#font-per-build).

| Builds | Face | Height (px, cell) | Shadow | Source |
| --- | --- | --- | --- | --- |
| 1st Graal, 4th, 9th, 15th, 1.1.9, 1.21 | `Dialog` | 28 | always blue | [bin] (client-internals/chat-text.md#font-per-build) |
| 1.31, 1.38 | `Dialog` | 28 | contrast rule | [bin] (client-internals/chat-text.md#font-per-build) |
| 1.39, 1.41 | `Helvetica` | 24 | contrast rule | [bin] (client-internals/chat-text.md#font-per-build) |
| NewMain 1.42, 2.00 to 2.05 rev 2, 2.17, 2.22, 2.31 | `Tempus Sans ITC`, installed from the client folder | 24 | contrast rule | [bin] (client-internals/chat-text.md#font-per-build) |

The rules below say how the chat text is drawn, how the config overrides the font, what the height value means and what replaces a missing face [bin][live][2.05] (client-internals/chat-text.md).

| Rule | Detail | Source |
| --- | --- | --- |
| drawing | straight onto the game view with the Windows canvas, bold, no bubble and no box | [bin][live][2.05] (client-internals/chat-text.md) |
| config | from 1.31 on, `font=` and `fontsize=` replace the defaults (→ §3.9.3) | [bin] (client-internals/chat-text.md#font-per-build) |
| height | the value is the cell height in pixels, not a point size; for Tempus Sans ITC a 24 px cell is an em of about 18.4 px, which the live capture matches | [bin][live][2.05] (client-internals/chat-text.md#font-per-build) |
| missing faces | `Dialog` does not exist on Windows and is mapped to a sans serif, normally Arial; `Helvetica` maps to Arial; neither was checked on real Windows | [inf] (client-internals/chat-text.md#font-per-build) |
| bold | Tempus Sans ITC has only a regular face, so Windows emboldens it: each glyph smeared one pixel right, each advance one pixel wider | [inf] (client-internals/chat-text.md#font-per-build) |
| NPC messages, 1.3x and 1.4x | on Windows 10 they look like white Arial Bold with a blue shadow, wrap at the view's width with each line centred over the NPC, and are not shown for an NPC outside the view; one 556 px line fits an em of about 20 px, narrower than the `Dialog` 28 or `Helvetica` 24 cells above would give, so either NPC messages use another size or Windows 10 maps the faces differently; the capture's font call was not traced | [cap] (client-internals/rebuild-traces-2026-11-05.md#13x-and-14x-game-view) |

### 4.6.3.2 Colour and position

Chat is white with a shadow. The rules below give the two drawing passes and how the shadow colour changed at 1.31 [bin] (client-internals/chat-text.md#colour-and-shadow).

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

Long chat lines wrap from 1.31 on. Each row gives a group of builds and its wrapping rule [bin] (client-internals/chat-text.md#wrapping-131-and-later).

| Builds | Rule | Source |
| --- | --- | --- |
| 1.21 and earlier | one centred line, clipped, no wrapping | [bin] (client-internals/chat-text.md#wrapping-131-and-later) |
| 1.31 and later | text wider than the view (640 px in 2.05) is split at spaces; a word that does not fit starts the next line, and a word too long for a line stands alone, unbroken | [bin] (client-internals/chat-text.md#wrapping-131-and-later) |
| 1.31 and later | lines stack upward so the last line sits on the anchor; each line is centred on its own, then pushed left to fit the right edge and right to start at 0 or more | [bin] (client-internals/chat-text.md#wrapping-131-and-later) |
| 6.x | wraps only text of 11 or more characters, breaking after any of ` .,;+-?!` | [doc] (client-internals/chat-text.md#wrapping-131-and-later) |

### 4.6.3.4 How long chat stays (2.05 rev 2)

The rules below give how long a chat line stays on screen in 2.05 rev 2, the length limit, and the special texts that show something else [live][2.05] (client-internals/chat-text.md#how-long-it-stays-live-205-rev-2-2026-10-30).

| Rule | Detail | Source |
| --- | --- | --- |
| own line | stays while the player stands still (over 7 minutes seen); the first direction key starts a 60-tick (3 s) countdown, after which the line goes and the client sends an empty chat prop | [live][2.05] (client-internals/chat-text.md#how-long-it-stays-live-205-rev-2-2026-10-30) |
| another player's line | shows for at least 3 s from arrival and until that player's empty chat arrives; an empty line only waits out what is left of the 3 s, it does not start a fresh 3 s; with no empty line the text stays | [live][2.05] (client-internals/chat-text.md#how-long-it-stays-live-205-rev-2-2026-10-30) |
| length | a line longer than 256 characters is cut to 253 characters plus `...` when sent; the receiver draws what arrives | [bin] (client-internals/chat-text.md#length) |
| `showap` | a chat of exactly `showap` shows the player's AP instead of the text | [2.05] (client-internals/chat-text.md#special-texts-205) |
| other uses of the slot | while a per-player counter runs it shows two numbers joined by `/`; in some sprite states it shows an item image or a carried number; the chat is then not drawn; these branches were read but not named | [2.05] (client-internals/chat-text.md#special-texts-205) |

### 4.6.3.5 Nicknames (1.31 to 2.31)

Nicknames are drawn by the chat routine. The rules below give where, when the player's own name shows, and how it is cut [bin][live][2.05] (client-internals/chat-text.md#nickname-131-to-231).

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

The item list is a window of weapon cells. The rules below give the key that opens it, what it holds and how the cells are laid out [2.05] (client-internals/decomp-findings-2026-10-28/02-item-list.md).

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

## 4.6.6 Function-key windows

Every Windows client opens its side windows from the function keys, but the set changed several times between 1998 and 2.31. The table gives, for each family of builds, what each key opens. F11 and F12 do nothing in any build, F9 works only in the NewWorld betas, and Esc and Alt+Enter (fullscreen) are in every build [bin] (client-internals/gui-windows-fkeys.md#the-key-handler-by-family).

| Builds | F1 | F2, F3 | F4, F5 | F6 to F10 | Source |
| --- | --- | --- | --- | --- | --- |
| 1st to 5th Graal | Options: save games and level editing | load and save a game | editor, Load level | none; Esc quits with no prompt | [bin] (client-internals/gui-windows-fkeys.md#1st-to-5th-graal-1998) |
| 6th Graal to 1.1.9 | Options; 15th Graal adds More options and Controls | as before | as before; 1.1.9 ignores them while the editor or reconnect window is open | F6 to F10 repeat F1 to F5; 9th Graal adds the quit prompt on Esc | [bin] (client-internals/gui-windows-fkeys.md#6th-graal-to-119) |
| 1.28 beta 2 to 1.39 | Options | load a game; save offline only | online, F4 refuses and F5 asks first | F6 debugger (from 1.32 offline or loopback server only), F7 player list | [bin][lab] (client-internals/gui-windows-fkeys.md#128-beta-2-to-139) |
| 1.41 rev1 | Help | as before | as before | F8 server list arrives | [bin] (client-internals/gui-windows-fkeys.md#141-rev1) |
| NewMain, 2.0 to 2.05 rev2 | Help: the F4 to F8 windows, General options, Controls | nothing; save games are gone | as before | F6, F7, F8 as before; F10 toggles the window border from 2.02 | [bin] (client-internals/gui-windows-fkeys.md#newmain-24-and-26-20-to-205-rev2) |
| 2.1 test2 and test3 | redesigned Help with a "Game windows" group | nothing | as before | as 2.05 | [bin] (client-internals/gui-windows-fkeys.md#21-test2-and-test3) |
| NewWorld beta 1 and 2 | as 2.02 | nothing | as before | as 2.02; F9 moves the game clock on one hour, offline only | [bin] (client-internals/gui-windows-fkeys.md#newworld-beta-1-and-2) |
| 2.17, 2.22, 2.31 | Options/Help; 2.31 hides Edit level and Debugger | F2 shows the RPG window from 179; F3 nothing | F4 editor (not 2.31), F5 Load level filled with the current position | F6 debugger (not 2.31), F7 player list, F8 server list while online, F10 border | [bin][cap] (client-internals/gui-windows-fkeys.md#217-222-and-231) |

1.39 was run online against the lab server. Each key behaved as the static read says, with one exception: F6 closed the client [lab] (client-internals/gui-windows-fkeys.md#128-beta-2-to-139).

| Key (1.39, online) | Seen | Source |
| --- | --- | --- |
| F1 | "Options" window with Load game, Save game, Edit level, Load level, More options, Controls, Close | [lab] (client-internals/gui-windows-fkeys.md#128-beta-2-to-139) |
| F2, F3 | a "Load save game" file dialog; a refusal to save online | [lab] (client-internals/gui-windows-fkeys.md#128-beta-2-to-139) |
| F4, F5 | the online-editor refusal; an OK/Cancel warning that loading a level disconnects | [lab] (client-internals/gui-windows-fkeys.md#128-beta-2-to-139) |
| F6 | with a loopback server the client closed within a second, three times out of three; not explained | [lab] (client-internals/gui-windows-fkeys.md#128-beta-2-to-139) |
| F7 | the "Playerlist" window | [lab] (client-internals/gui-windows-fkeys.md#128-beta-2-to-139) |
| F8 to F12 | nothing | [lab] (client-internals/gui-windows-fkeys.md#128-beta-2-to-139) |

What the F-keys and the other keys do on 2.17.1 to 6.03r7 when logged in is in → §4.12.

F8 opens the server list window, whose account and password default to `guest`. If the client has no list connection, F8 opens one on port 14921 and shows a short "Connecting to server ..." window while it waits [bin] (client-internals/gui-windows-fkeys.md#the-server-list-window-f8-141-to-205).

## 4.6.7 The server message window

The server message (`PLO_STARTMESSAGE`, 41, → §4.10.6) has its own window. The client stores each message in a file in the game folder and shows the window only when the text differs from the stored copy, so a player sees a message once per change. There is no key or menu to open it again [bin][lab] (client-internals/gui-windows-fkeys.md#the-server-message-window).

| Builds | Form | What it does with 41 | Source |
| --- | --- | --- | --- |
| 1.32, 1.33 | `TRTFMessage` | loads the text as rich text and always shows it; HTML shows as raw text | [bin] (client-internals/gui-windows-fkeys.md#132-to-139-trtfmessage) |
| 1.39 | `TRTFMessage` | skips the window if the text equals `servermessage.rtf`, otherwise saves it there and shows it; RTF is drawn, HTML shows as raw text; Save offers RTF and TXT | [bin][lab] (client-internals/gui-windows-fkeys.md#132-to-139-trtfmessage) |
| 1.41 rev1 to 2.31 | `TServerMessage` | text starting `{\rtf1` goes to a rich-edit box and `servermessage.rtf`; anything else is HTML, written to `servermessage.html` and drawn by an embedded web browser; an unchanged file means no window | [bin] (client-internals/gui-windows-fkeys.md#141-rev1-to-231-tservermessage) |

In the HTML case the window has five browser buttons. Links load inside the window, and the caption follows the page title [bin] (client-internals/gui-windows-fkeys.md#141-rev1-to-231-tservermessage).

| Button | Action | Source |
| --- | --- | --- |
| 1, 2 | Back and Forward, enabled as the browser's history allows | [bin] (client-internals/gui-windows-fkeys.md#141-rev1-to-231-tservermessage) |
| 3 | Stop, enabled while a page loads | [bin] (client-internals/gui-windows-fkeys.md#141-rev1-to-231-tservermessage) |
| 4 | Refresh | [bin] (client-internals/gui-windows-fkeys.md#141-rev1-to-231-tservermessage) |
| 5 | go to a stored address | [bin] (client-internals/gui-windows-fkeys.md#141-rev1-to-231-tservermessage) |
| Close, Esc | hide the window; the caption and Close text come from the language file keys `RTFMessage` and `RTFMessage-CloseButton` | [bin] (client-internals/gui-windows-fkeys.md#141-rev1-to-231-tservermessage) |

The same form doubles as the private-message History window, opened from the player list (→ §4.10.5). It lists the conversation with that player, with the player's own lines in purple and the other player's in red [bin] (client-internals/gui-windows-fkeys.md#the-same-form-as-the-pm-history-window-205-21-tests).

## 4.6.8 The no-PK indicator and GS1 ammunition on 5.x

On 5.12 and 5.24r4, a level whose GS1 script turns on no-player-killing mode makes the HUD draw a small red crossed icon to the right of the HP/AP bar; a GS1 event guard that sets arrows and bombs shows 99/99. Both appear only when the level's GS1 is compiled with its GS1 meaning kept; 4.20r8 shows neither [lab][shot] (client-internals/gs1-on-5x-hud-and-flags.md#the-hud-difference-on-5x).

| Item | Rule | Source |
| --- | --- | --- |
| red "x" | the no-PK indicator, turned on by a bare zero-argument GS1 command in the `created` guard | [lab] (client-internals/gs1-on-5x-hud-and-flags.md#the-hud-difference-on-5x) |
| 99/99 | a GS1 `if (<event>)` guard that sets `player` ammunition on entry | [lab] (client-internals/gs1-on-5x-hud-and-flags.md#the-hud-difference-on-5x) |
| flags on 5.x | sent unprefixed in `PLO_FLAGSET` before NPC bytecode; `player.<flag>` and the bare name read them; `player.flags` does not list them | [cap][lab] (client-internals/gs1-on-5x-hud-and-flags.md#flags-and-built-ins-on-512-and-524r4) |
| built-ins on 5.x | `player.hearts`, `player.fullhearts`, `player.weapons.size()` and bare `selectedweapon` work; `player.weaponscount`, `player.selectedweapon`, bare `weaponscount` and bare `playerhp` are empty | [lab] (client-internals/gs1-on-5x-hud-and-flags.md#flags-and-built-ins-on-512-and-524r4) |
| 5.12 black level | a stale `FILENAMECACHE.txt` with `cachefilenames=true` hides the client's own tileset; deleting it fixes the view | [lab][shot] (client-internals/gs1-on-5x-hud-and-flags.md#512-draws-a-black-level-a-stale-file-name-cache) |

## 4.6.9 Built-in HUD measured on Linux and Windows 6.03r7

The published black-box study used Linux x64 (`G3D0511C`) and the packed Windows build (`G3D0311C`), a plain world without NPCs or server GUI/weapon scripts, and login-to-world warps through the lab servers. Windows ran with a 2012 clock. These are reported screen/capture measurements, not a new execution or a static implementation read. Coordinates below are client-area pixels, with the origin at the top left; boxes are x, y, width, height. [lab][shot][cap] (client-internals/hud-603r7-black-box.md)

### Window and fixed layout

The first client area was 1024 × 768 (`game_config` option `windowmode=1024x768` on Windows); the login level had no HUD, which appeared after the world warp. The Windows outer frame was 1040 × 807, with 8-pixel sides/bottom and a 31-pixel title area. Tested sizes were 640 × 480, 800 × 600, 1024 × 768 and 1280 × 1024, the last clamped to desktop height on Windows. Resizing did not scale the 16-pixel tiles or HUD: more level became visible, the camera stayed player-centred subject to level bounds, and a view larger than the level centred it with black around it. [shot] (client-internals/hud-603r7-black-box.md#window)

At 1024 × 768, the art comes from `state.png` except the glove (`sprites.png`) and sword (`swordN.png`). Changing the state sheet changes the art, not these measured positions. [shot] (client-internals/hud-603r7-black-box.md#layout-at-1024--768)

| Element | Source box | Screen position/rule | Source |
| --- | --- | --- | --- |
| A/S/D tabs | (202, 0, 22, 30), same sprite without mirroring | (15, 30), (80, 30), (145, 30), pitch 65 | [shot] (client-internals/hud-603r7-black-box.md#layout-at-1024--768) |
| Glove | red power 2: (28, 212, 28, 32); yellow power 3: (0, 212, 28, 32) | (40, 29); power 1 draws nothing | [shot] (client-internals/hud-603r7-black-box.md#layout-at-1024--768) |
| Sword | begins (94, 36), height 28, width unresolved at 28–34 | source translated by (11, −5), giving (105, 31), for swords 1–4 | [shot] (client-internals/hud-603r7-black-box.md#layout-at-1024--768) |
| D slot and shield | D around (170, 30) | D empty with no selected weapon; shield not drawn | [shot] (client-internals/hud-603r7-black-box.md#layout-at-1024--768) |
| AP frame/fill | (0, 97, 130, 22); (0, 119, AP, 10) | frame (15, 65), fill (37, 71); fixed 100-pixel gradient clipped to AP, one pixel per point, transparent empty interior | [shot] (client-internals/hud-603r7-black-box.md#layout-at-1024--768) |
| MP frame/fill | (0, 49, 130, 22); (0, 71, MP, 10) | frame (15, 90), fill (37, 96), one pixel per point; frame drawn only when MP > 0 | [shot] (client-internals/hud-603r7-black-box.md#layout-at-1024--768) |
| Gralat/bomb/arrow icons | icon strip | (274, 30), (330, 31), (379, 30) | [shot] (client-internals/hud-603r7-black-box.md#layout-at-1024--768) |
| Counter digits | (14·d, 81, 14, 16), d = 0–9 | y 48, advance 12; gralats begin x = 280 − 6·n for n digits without padding; bombs x 326/338 and arrows x 374/386 use two zero-padded digits, so 100 arrows shows as 10 | [shot] (client-internals/hud-603r7-black-box.md#layout-at-1024--768) |

Tabs, bars and counters retain their top-left positions across window sizes. Hearts alone anchor to the top right. Only current hearts are drawn; maximum hearts changes neither block size nor position. The captured property uses half-heart units, without a quarter-heart value. [shot][cap] (client-internals/hud-603r7-black-box.md#hearts)

| Heart detail | Measured rule | Source |
| --- | --- | --- |
| Sheet boxes | full (0, 0, 40, 44), half (40, 0, 30, 44), small full (80, 0, 31, 33), small half (111, 0, 24, 33); small sprites are drawn 1:1, and half hearts begin at the slot's top left | [shot] (client-internals/hud-603r7-black-box.md#hearts) |
| Up to four hearts | one full-size row, x = W − 198 + 45k, y 24, at every window size measured; four hearts leave a 23 px right margin, and the source's 68 px is the three-heart case (→ App. E#326) | [shot] (client-internals/hud-603r7-black-box.md#hearts); [lab] (protocol/lab-appe-mirae-2026-11-20.md#603r7-hud-e326) |
| Five and above | small rows of 5, 6, 5, 4 slots, pitch 35 horizontally and 20 vertically; first row x = W − 198 + 35k, y 24, second row half a pitch left; 20 hearts fill the four-row hexagon, whose rightmost small heart ends 10 pixels from the edge | [shot] (client-internals/hud-603r7-black-box.md#hearts) |
| Five or 5.5 hearts | whole small block 10 pixels lower; from six hearts it returns to y 24 | [shot] (client-internals/hud-603r7-black-box.md#hearts) |

### Platform text, files and observed transitions

At matched sizes 640 × 480, 800 × 600 and 1024 × 768, the measured Linux/Windows tiles, player and HUD art aligned. The systematic difference was text: Windows drew A/S/D letters, a glyph above D and the sword-power number; the fontless Linux run omitted them. With the four requested font files unavailable, chat, NPC text and tab letters disappeared, while sheet-based counter digits remained. The study identifies Tempus Sans ITC size 24 as the default and reports the same missing-font behavior on 5.24r4. This is scoped to those runs, not an unconditional platform rule. [shot][cap] (client-internals/hud-603r7-black-box.md#windows-against-linux); (client-internals/hud-603r7-black-box.md#files-and-packets)

At world login, PLO 9 supplied maximum/current hearts, gralats, ammunition, glove/sword/shield and AP/MP fields; PLO 42 arrived every five seconds in this server setup. At about 66–68 seconds the server raised AP 50 to 51, visibly adding one fill column. That is a captured server change, not a client regeneration timer. WANTFILE 23 requests included the base package, tileset and animation on login, then body/equipment/state art and fonts on the world server; the source retains the complete request list. [cap][shot] (client-internals/hud-603r7-black-box.md#files-and-packets)

If PLO 178 interrupted the `pics1.png` download, both clients dropped it, showed a black world and did not request it again; pre-seeding the cache avoided the failure in these runs. Tab, Q, M and F2 opened nothing with this script-free server. The Windows software GDI renderer ran the packed original; a neighbouring Mesa library was not loaded, and a separately dumped executable failed at startup. These observations do not establish behavior with arbitrary renderers, clocks or server GUI scripts. Sword width, other-size Windows text positions and a current-clock Windows check remain open (→ App. E#326). [lab][shot][cap] (client-internals/hud-603r7-black-box.md#windows-against-linux); (client-internals/hud-603r7-black-box.md#files-and-packets); (client-internals/hud-603r7-black-box.md#open)

## 4.6.10 Draw order, layers and ground on 2.22

The rebuild work read 2.22's drawing code and checked it against the lab's frames of the real client. The rules below give how shown pictures and NPCs are layered, how the new-world ground is drawn, and the text sizes found on the way [bin][cap] (client-internals/rebuild-traces-2026-11-05.md#222).

| Rule | Detail | Source |
| --- | --- | --- |
| `changeimgvis` | accepts 0 to 20; 0 to 2 become layers −1 to 1, and 3 and up become layers 9 and up; a layer under 9 counts from the NPC's own layer. Layer 9 is light, the same as `drawaslight`, and the exe's own script export writes layer 9 as `drawaslight;`. This agrees with the 2.05 reading (→ §8.2) and gives the full mapping | [bin] (client-internals/rebuild-traces-2026-11-05.md#222) |
| draw list | shown pictures and NPCs share one list, sorted by layer, then by bottom y, then by x; NPCs on one layer sort by y, then x, then list order. Light therefore comes after everything else | [bin][cap] (client-internals/rebuild-traces-2026-11-05.md#222) |
| new-world ground | tile 0 is picked from the four corner heights, in seven bands (0, 3, 4, 5, 25, 55, 65). When all four corners reach a band, a tile from that band's full patch is used, a flower, mushroom or stone when the fraction of the corners' sum × 1000 is under 63; when only some do, a transition tile is chosen by a corner mask | [bin] (client-internals/rebuild-traces-2026-11-05.md#222) |
| ground light | every tile, level tiles included, is lit per pixel by the slope down the screen, a darkening of 0 to 63 that is 32 on flat ground; ground below 0 is water that darkens with depth, has a set blue level and foams at the shore | [bin] (client-internals/rebuild-traces-2026-11-05.md#222) |
| gani text | `fontsize` is in points at 96 dpi (14 gives an 18 px em), and the gani's `bold` flag is used; "Touch to get information" is 195 px wide, its baseline 4 px above the arrow | [bin][cap] (client-internals/rebuild-traces-2026-11-05.md#222) |
| sign letters | the half-width table and the `#` codes are 2.05's (→ §4.6.2); an unknown code draws glyph 86 and the letter is then drawn as text | [bin] (client-internals/rebuild-traces-2026-11-05.md#222) |
| tick | 50 ms, from the idle handler (→ §4.1.2). This read reported a multimedia timer with resolution 10; that is the DelphiX timer component created in code, whose 10 is its maximum lag count, and 2.22 imports no multimedia-timer functions (→ §4.6.10, settled). How far a gani advances per tick was not traced | [bin] (client-internals/rebuild-traces-2026-11-05.md#222); [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#what-drives-the-222-tick-e328) |

**Settled question, formerly E#328: What drives 2.22's tick.** Whether 2.22's game step runs from a 50 ms multimedia timer or from the idle handler behind a 50 ms gate was open; a static read of the timer's creation settled it [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#what-drives-the-222-tick-e328).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | Claim A: a multimedia timer of 50 ms, resolution 10. Claim B: no form timer, the idle handler behind a 50 ms gate. A 2026-11-19 read found no multimedia-timer import | [bin] (client-internals/rebuild-traces-2026-11-05.md#222); [bin] (version-profiles/matrix/builds-static-survey.tsv); [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#tick-source-e328-222) |
| Settled | 2.22 creates the DelphiX timer component in code, with interval 50 ms and maximum lag 10, bound to the game step. The component runs from the application's idle event: when 50 ms have passed by `timeGetTime` it resets its start to the current time and calls the step once, so late steps are not made up. 2.05 rev 2 creates it the same way | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#what-drives-the-222-tick-e328) |
| Verdict | Claim B is the mechanism; Claim A's "resolution 10" is the component's lag count, not a multimedia timer | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#what-drives-the-222-tick-e328) |
| Left over | Nothing for the tick; the tick is 50 ms either way, so no duration in the manual changes | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#what-drives-the-222-tick-e328) |
