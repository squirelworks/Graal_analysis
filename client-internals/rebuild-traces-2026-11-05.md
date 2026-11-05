# What the graal-delphi v0.0.4 rebuilds traced from the real clients (2026-11-05)

The graal-delphi rebuilds were compared side by side with the real clients
for v0.0.4: under Wine (screenshots, `WINEDEBUG=+font` call logs, window
dumps), on Windows 10 captures, and by reading each build's own forms and
resources out of its `Graal.exe`. This note collects the facts that came
out of that work and that were not yet written down here. It leaves out
what the rebuilds chose for themselves (fallback fonts, built-in art,
retry timers) and anything a rebuild only guessed.

Each item names the graal-delphi pull request it came from
(`squirelworks/graal-delphi#n`). Tags as elsewhere: **[bin]** read from the
exe (forms, resources, strings, handlers), **[lab]** seen on the real
client under Wine, **[cap]** measured from a capture of the real client.

## Status display text, 2.0x and 2.1x (Wine font trace)

Extends `status-display.md` (key names, and the "Not read" item on the
glove and sword power text) and `chat-text.md`.

The real `Graal-NewMain26.exe` and `Graal-NW.exe` were run under Wine with
`WINEDEBUG=+font`, which logs every `CreateFontIndirect` and `ExtTextOut`.
**[lab]** (graal-delphi#138; the 2.0x folders got the same rule in their
v0.0.4 notes)

| What | Builds | Font asked for | Drawn |
|---|---|---|---|
| A, S, D key letters | 2.1 test 2, 2.1 test 3, 2.17.1, NewMain 24, NewMain 26; 2.0 to 2.05 rev 2 | `Helvetica`, cell 26, bold (Wine maps it to Arial) | black at +1, +1, then white, with the text origin at (16, 32), (81, 32) and (146, 32): one pixel right and two down from each button's corner (15, 30), (80, 30), (145, 30) |
| Q (key 9) over the D button | same | `Helvetica`, cell 10, bold | at (146, 27) |
| Sword power number, names under characters | same | `Tempus Sans ITC`, cell 24, bold: the `graalconfig.txt` font | white over a blue shadow, as the chat text; the exe adds the install's `tempsitc.ttf` with `AddFontResourceA` before asking for it |
| A, S, D key letters | NewWorld betas (nwb1pre, nwb1, nwb2) | face name `b`, cell 24, weight 400 (no such face, so the mapper gives Arial) | white, **no shadow**, three pixels into each tag; the tags are 60 px apart |

Notes:

- The glove power is printed by the same routine as the sword power, so it
  takes the same font. The rebuilds draw it that way; only the sword power
  was seen in the trace. **[lab][inf]**
- The 2.05 static read in `status-display.md` puts the small key-9 name at
  (147, 27). The trace logs (146, 27). The one-pixel difference was not
  rechecked against the routine.
- Without `tempsitc.ttf` in the install (the NewWorld installs ship none),
  Windows falls back to Arial for the names. **[lab]**

## NewWorld beta status bar

Extends `newworld-betas.md` (which records the 150/150 Training HUD). The
positions were matched pixel for pixel against the real NewWorld screen,
using `state.png`'s own parts. **[cap]** (graal-delphi#138)

- Power is drawn as `POWER/MAX` (`150/150` offline) in `state.png`'s
  digits, right-aligned to end at x 540, on y 39.
- The bear sits at (532, 24).
- The gralat orb is at (274, 30), with its count.
- There are no hearts and no bomb or arrow counters.
- Still not placed: the clock, the sword picture and number.

## 1.3x and 1.4x game view

From the Windows 10 side by side of 1.3test to 1.41r1. (graal-delphi#137)

- **NPC messages and names** look like white Arial Bold with a blue shadow.
  On the Windows 10 capture the line "If you have problems, then just press
  F1 and click on 'More" is 556 px wide, which fits an em of about 20 px.
  Messages wrap at the view's width, each line centred over the NPC and
  kept inside the view; an NPC outside the view shows no message. **[cap]**
  - *Open:* `chat-text.md` gives these builds `Dialog` 28 (1.31, 1.38) and
    `Helvetica` 24 (1.39, 1.41) as cell heights, which would make that line
    wider (an em of about 25 px or 21.5 px in Arial). Either the NPC message
    uses another size than the chat text, or Windows 10 maps `Dialog`
    differently. The capture's build and font call were not traced.
- **Start table.** One Player's start is read from a table in the exe (level
  and x, y for players one to four). **[bin]**
  - 1.3test and 1.31: `house1.graal` at 21.5, 28 (the bed).
  - 1.32 and later: `start1.graal` at 21.5, 28. The position is set before
    the level loads, so `start1.graal`'s `playerenters` script then moves
    the player to 13.5, 37.5 (under Stefan). **[bin][cap]**
- **Game window.** A Delphi form owned by the hidden application window,
  style `$16CF0000` (sizable, minimise and maximise boxes), read on
  Windows 10. The 1.x programs set no `Application.Title`, so the taskbar
  shows the exe name (1.3test shows "Graal13"). Alt+Enter switches to
  640 × 480 full screen and back. **[cap]**
- **Minimap.** Shown only on a level of the map's grid; the start cave and
  the houses show none. **[cap]**
- **Start dialog scroll bars (1.3test to 1.39).** The form's scroll range
  counts the details panel at its full design height, so on Windows 10 the
  real dialog shows both scroll bars. **[cap][bin]**

## 1998 betas, 1.1, 1.1.9, 1.21 and 1.28 beta 2

(graal-delphi#124, #128, #129)

### Status display

The early builds draw the status display from their own `state.gif` and the
digit sprites of the body sheet (`link.gif` or `sprites.gif`, sprite-table
entries 268 to 277: 0 to 8 in a row, 9 above the 7). Each build's layout was
measured by template-matching its sheets against the real client's first
game frame (640 × 448 view), and every piece lands on the real one to the
pixel. **[cap]**

The per-build table is `beta-hud-layouts.tsv`. In short:

- **1st and 2nd Graal** write the rupee count as three padded digits
  (`000`) from `link.gif`, 16 px apart, from x 230.
- **3rd Graal to 6th Graal** use 14-px-high digits at row 1472, 12 px apart,
  centred on x 250. 5th Graal alpha and 6th Graal take the heart from
  another place on the sheet (228, 33).
- **7th Graal to 1.1** use the redrawn `state.gif`: a 60 × 60 piece at
  (67, 15), the 31 × 30 piece at (146, 30), the three counter icons, and
  16-px digits at row 1454.
- **1.21 and 1.28 beta 2** have the A, S and D buttons at x 15, 80 and 145,
  the sword picture (`sword1.gif`, 28 × 28) at (105, 31), and the counts
  centred on x 280, as the 2.05 layout does.
- Hearts are 45 px apart from (422, 24), or (442, 24) in 1.21 and 1.28b2.
- **Start counts.** A new game shows 10 bombs, 5 arrows and 3 hearts. The
  rupees are 0 in most builds, 300 in 4th Graal alpha to 6th Graal, and 100
  in 7th to 9th Graal. **[cap]**

### Start level and spot

- 1st to 13th Graal: `house1.graal`, in the middle of the room at 28.5, 30,
  measured from the real first frame. **[cap]**
- 6th Graal: `level13.graal` at 16.5, 35, matched against its capture.
  **[cap]**
- 14th Graal on (and 1.1, 1.1.9, 1.21, 1.28b2): 21.5, 28 (the bed), from the
  start table in the exe. **[bin]**

### Windows

- **Start dialog owner.** From the real exes' live windows: 1st to 5th
  Graal are owned by the application window, 3rd to 5th also stay on top,
  and from 5th Graal alpha on the dialog has no owner. **[lab]**
- **Character list heads.** Each entry's head is drawn from `heads.gif`,
  shrunk to half size: the AND of each 2 × 2 block up to 13th Graal, the
  `COLORONCOLOR` stretch mode in 14th and 15th Graal. The lists hold each
  build's own names in its own order (4 in 3rd Graal, up to 19 in 9th to
  15th Graal). All 18 beta dialogs and the 1.1, 1.1.9, 1.21 and 1.28b2
  dialogs match the rebuilds pixel for pixel under Wine. **[bin][lab]**
- **Game window.** `TAdventure`, owned by the hidden application window,
  with a 640 × 448 client; 1.21 and 1.28b2 add the 24-pixel chat field.
  Styles `$16CE0000` / `$50110`, and `$50100` on 1st Graal, checked against
  the real window's dump under Wine. **[lab]**
- **Alt+Enter.** Most builds switch to a 640 × 480 full screen as a topmost
  popup. 2nd to 5th Graal show "Display mode cannot be changed
  (640x480 16bit)" instead. **[lab]**
- **1.21's real exe** was recovered from its InstallShield 3 package
  (PKWARE DCL); its MD5 matches `build-catalogue.md`'s. **[bin]**

## 2.0x launchers (2.0 to 2.05 rev 2)

Read from each build's forms and compared under Wine with the real 2.0 and
2.05 rev 2. (graal-delphi#121)

- **Start window.** `TConnectFrame`: a 476 × 330 dialog titled
  "Graal 2001", with only the close button, over `SCREENIMG1`. Training,
  Options and Start are drawn from `BUTTON1`; their captions are 12 pt
  bold, with the accelerator letter in red. **[bin][lab]**
- **Server list.** Start opens `TServerListFrame` as its own 577 × 416
  window over `SCREENIMG2`, captioned with the site's name and
  "Server List", and titled "… (loading...)" until the servers are in. "Getting server list ..." shows
  in the `TShortMessage` box while the listserver answers. The account and
  password are typed on the list, under the servers. The list is first asked
  for with id 0 alone. Server names lose a `P ` prefix; other prefixes stay.
  **[bin][lab]**
- **Server-list form, per build.** Four versions of the form: 2.0 to
  2.01 rev 1 (with a RichEdit description box and two server icons), 2.02
  to 2.02 rev 2, 2.05 rev 1 on its own, and 2.03, 2.04, 2.05 and 2.05 rev 2.
  The image list is in the old Delphi layout in 2.0 and in the `IL` layout
  from 2.02. **[bin]**
- **Forms.** 45 forms in 2.0 to 2.03; 46 in 2.04 and the three 2.05 builds.
  **[bin]**
- **`TUTORIALB4`** is 10122 bytes in 2.0, 2.0 rev 1 and 2.0 rev 2, and 10275
  bytes from 2.0 rev 3 on. **[bin]**
- **Language file.** A `language<Name>.txt` next to the program renames the
  start window's controls by component name (`StartScreen-<Name>=`).
  **[bin][lab]**
- **Pictures.** The exe lists its whole install tree and opens a picture by
  its exact name wherever it is (`head0.gif`, `sword1.gif`, `wbomb1.gif`,
  `body.png`); a `.png` is not taken for a `.gif`. Traced under Wine. **[lab]**
- **Windows.** The taskbar entry is the hidden "Graal" application window;
  the start window and the server list have no title-bar icon; the game
  window (640 × 480, "Graal") can be resized, minimised and maximised.
  **[lab]**

## 2.1x launchers (2.1 tests, 2.17.1, NewMain 24/26, NewWorld betas)

(graal-delphi#126, #138)

- Each build opens on its own start window and server list from its own
  forms, sized to the form, with only the close button. **[bin][lab]**
- NewMain 24 and 26: the character box fills from `headsconfig.txt` and
  opens on `graalconfig.txt`'s `head=`. **[bin][lab]**
- 2.17.1: Training opens `maps/offlinetutorial.gmap` in cell b-2, below the
  cauldron. Alt+Enter goes to `graalconfig.txt`'s `fullscreenmode`
  (1024 × 768 as installed) and back; holding Shift on Start or Training,
  or `startinfullscreen`, starts in full screen. **[lab]**

## 2.22

Read from `Graal_222.exe` and checked against the lab's test6 and test7
frames of the real client. (graal-delphi#131, #136)

- **`changeimgvis`.** Accepts 0 to 20. 0 to 2 become layers −1 to 1; 3 and
  up become layers 9 and up. A layer under 9 counts from the NPC's own
  layer. Layer 9 is light, the same as `drawaslight`: the exe's own script
  export writes layer 9 as `drawaslight;`. So the tutorial lamps'
  `changeimgvis 0,3` is what makes their glow a light. This agrees with the
  2.05 reading in `npc-library/gs1-command-reference-205.md` (3 = light,
  4 = screen) and gives the full mapping. **[bin]**
- **Draw list.** Shown pictures and NPCs share one draw list, sorted by
  layer, then by bottom y, then by x (the exe's compare function). NPCs on
  the same layer sort by y, then x, then list order. Light therefore comes
  after everything else. **[bin][cap]**
- **Game tick.** A multimedia timer with an interval of 50 ms and a
  resolution of 10, whose `OnTimer` is the game step. **[bin]** How far a
  gani movie advances per tick is not traced.
- **Ground of new-world levels.** Tile 0 is picked from the four corner
  heights: seven bands (0, 3, 4, 5, 25, 55, 65); when all four corners reach
  a band, a tile from that band's full patch, which is a flower, mushroom or
  stone decoration when the fraction of the corners' sum × 1000 is under 63;
  when only some corners reach it, a transition tile picked by a corner
  mask. Every tile is lit per pixel by the slope down the screen, a
  darkening of 0 to 63 that is 32 on flat ground. Ground under 0 is water
  that darkens with depth, has a set blue level and foams at the shore.
  Level tiles go through the same lighting. **[bin]**
- **Gani movie text.** `fontsize` is in points at 96 dpi (14 gives an 18 px
  em), and the gani's own `bold` flag is used. "Touch to get information" is
  195 px wide, its baseline 4 px above the arrow. **[bin][cap]**
- **Sign letters.** The 96-entry half-width table and the `#` codes
  (`ABXYudlrhxyz4.`, two glyphs for `#h` and `#4`) are the same as 2.05's
  (`sign-panel.md`). An unknown code draws glyph 86 and the letter is then
  drawn as text. **[bin]**
- **Caption.** The Training game window is titled `G r a a l`, the caption
  string in the exe. **[bin]**

## 2.31 (and 2.3, which has no surviving exe)

Compared under Wine and on Windows with `Graal_231.exe`. Extends
`version-profiles/2.22-2.31.md`. (graal-delphi#118, #141)

- **Start window.** Its own 577 × 416 window titled "GraalOnline" (set in
  code), with only a close button. Training is the wide button at the top.
  **[bin][lab]**
- **Editor and Training** start `GraalEditor.exe` (Training with `-play`)
  from the Graal folder; without it, an Error box says
  "GraalEditor.exe has not been found in the Graal folder!". **[bin][lab]**
- **Account and password** start empty; the account box has the focus with
  its text selected. **[lab]**
- **Show More and Donations** are hidden in `TServerListFrame`'s form. The
  client shows Show More when the listserver sends a site page (id 3,
  `SITEURL`) and Donations when it sends an upgrade page (id 5, `UPGURL`).
  Each opens its page through the "Open URL" box, which asks before opening
  the browser. Get an account! and Go use the same box. The Version box
  shows the start of the version string, cut at the right. **[bin][lab]**
- **Dialog font.** Every form has `MS Sans Serif` at `Font.Height` −14.
  **[bin]**
- **Game window.** 640 × 480, titled `G r a a l` with random space padding
  offline, or "Graal: <server>" online. The white chat line runs along the
  bottom and the play area is the 456 pixels above it. Esc asks "Do you
  really want to quit Graal?". **[bin][lab]**
- **Full screen.** Alt+Enter and "Start in fullscreen" switch to
  `fullscreenmode` (1024 × 768 by default). The rebuild shows more of the
  level there, on the assumption that 2.31 does what 2.22's engine does; the
  real 2.31's full-screen view was not captured. **[inf]**

## Graal3D (February 2000)

Extends `graal3d/README.md`. (graal-delphi#120)

- **Start window.** `TConnectFrame`'s start picture is a 433 × 321 JPEG in
  the exe (the wood board, "Graal 3d" and the field names). The window,
  "Graal 3D", is the size of the picture. The five fields are dark red
  (the form's `Color` 64) with white text, Server IP is a drop-down, and
  there is one Start button and no Offline or Quit button. **[bin][lab]**
- **Game window.** `TAdventure`, "Graal 3D", 640 × 480. The start window
  closes while the game runs and comes back after it. **[lab]**
- **Icon.** `MAINICON` is the torch. **[bin]**

## 4.04r2

Extends `client-internals/live-behaviour-404.md` and
`protocol/v4x-clients.md`. (graal-delphi#123)

- **No separate launcher.** `Graal4.exe` opens its 640 × 480 game window and
  the engine draws the start screen inside it from the install's
  `levels3d/gui` pictures: `graalv4screen.jpg` (the house), `graalv4title.png`,
  `defaulttextedit.png`, `defaultscroll.png`, `defaultradio.png` and
  `defaultcheck.png`. It holds the Nickname panel; the Play as / Account
  name / Password panel with the Member radio button and Save password;
  Start; and Become a Member, Options and Offline Test along the bottom.
  Placement and colours were measured under Wine. **[lab]**
- **Caption.** "G r a a l" with eight spaces placed at random around it.
  **[lab]**
- Become a Member opens the sign-up page named in `license.graal`; Offline
  Test plays the offline tutorial. **[lab]**

## The 1998 betas' player drawing (9th Graal, unfinished)

Read from 9th Graal's `Graal.exe` for the next rebuild version. Only 9th
Graal was read, and nothing here was checked against a capture yet. **[bin]**

- **`arrays.dat`** (9th Graal: 21 arrays, read in order at start-up):
  - Array 13 holds the poses: a nested array of 4 × N entries, indexed by
    group × 4 + direction. Each part is one int, `sprite << 16 | dx << 8 | dy`;
    dx and dy are signed bytes in eighths of a tile (2 px) from the player's
    x, y.
  - Array 14 is an extra pose table, used for state 3 after frame 30.
  - Array 17 holds overlay frames, indexed by direction.
  - Array 20 (the last) holds the sprite rectangles. For one int v, in
    pixels: x = 2·(v >> 24), y = 2·((v >> 12) & 4095), w = 2·((v >> 6) & 63),
    h = 2·(v & 63).
- **Frame to pose group.** A table in the exe maps the animation frame to a
  pose group. It starts 0, 4, 5, 4, 3, 2, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13,
  11, 12, 14, 15, 16, 17, 23, 18, 19, 20, 19, 18, 21, 22, 21, 18, 24, 25, 26,
  27, 136, 137, 138. So frame 0 is idle (group 0) and frames 1 to 8 are the
  walk cycle.
- **Sheet by sprite number.** 8192 and up: `heads.gif`, with sprite − 8192
  as the rectangle and the source x moved by head number × 32. 4096 to 8191:
  the picture of a carried object. Anything else: the body sheet, recoloured
  with the player's five colours.
- **Equipment.**
  - Sprites 1 to 4 are the shield, drawn only with shield power ≥ 1 and
    nothing carried. Power 2 moves the source by (128, 600), power 3 by
    (128, 696).
  - Sprites 5 to 21 are the sword. Power 2 moves the source by (128, 600),
    power 3 by (128, 792), power 4 by (128, 696).
  - Sprites 107 to 114 are the glove. Glove power 2, 3 and 4 move the source
    x by 32, 64 and 96.
- **Still open:** how the five colours are applied (the routine that builds
  the recoloured body sheet), and the same tables in the other betas.
