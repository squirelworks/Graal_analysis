# The 6.03r7 built-in HUD, measured from the screen (Linux and Windows)

Date: 2026-11-12 to 2026-11-13. Black-box lab only: nothing was disassembled. The real Linux 6.03r7
x64 client (token `G3D0511C`) ran headless in a Debian lab VM (software GL, no window manager, so
the X window is exactly the client area), in a network namespace that reaches only the loopback
address. The real Windows 6.03r7 (the packed installer build, token `G3D0311C`) ran in a Windows 10
lab VM with its clock held at a date in 2012. Servers: stock GServer-v2 as a login server that
serverwarps (PLO 178) to a second GServer-v2 world, and the Seihai listserver. The world level is
plain grass with no NPCs, and the server has no GS2 weapons or GUI scripts, so everything drawn is
the client's own HUD. A decrypting proxy logged both directions. The account was the built-in
`guest`, edited per run (`heartlimit` raised to 20). **[lab][shot][cap]**

Every box is client-area pixels as x, y, w, h with (0, 0) top left, measured on 1:1 captures by
exact pixel matching against the files the client was sent. Screenshots, logs and scripts are
owner-held. For the 2.05 rev 2 status display see [status-display.md](status-display.md) and manual
§4.6.1; for the 5.x HUD under GS1 scripts see [gs1-on-5x-hud-and-flags.md](gs1-on-5x-hud-and-flags.md).

## Window

| Item | Value | Tag |
| --- | --- | --- |
| First window | 1024 × 768 client area (`game_config` `windowmode=1024x768` on Windows). Mapped while still on the login server, which draws its level with **no HUD** | [shot] |
| HUD visible | only after the warp to the world server; the window title becomes the world server's name | [shot] |
| Windows frame | outer window 1040 × 807 (left, right and bottom 8, title 31), class `Graal Windowed Window Class`, title `Graal` before the warp | [shot] |
| Resize | the view **does not scale**: tiles stay 16 px and the HUD keeps its pixel size; a bigger window shows more level. The camera keeps the player centred, clamped to the level; a window larger than the 64 × 64-tile level shows it centred with black around it | [shot] |
| Sizes accepted | 640 × 480, 800 × 600, 1024 × 768, 1280 × 1024 (Windows clamps the last to the desktop height) | [shot] |

## Layout at 1024 × 768

All HUD art comes from the server's `state.png`, except the glove (`sprites.png`) and the sword
(`swordN.png`). A server with a different `state.png` changes the look, not the layout. **[shot]**

| Element | state.png source | Screen | Notes |
| --- | --- | --- | --- |
| A, S, D tabs | (202, 0, 22, 30), the same sprite three times, not mirrored | (15, 30), (80, 30), (145, 30); pitch 65 | Linux draws no letters on them; Windows draws "A", "S", "D" as font text (below) |
| A slot: glove | `sprites.png` (28, 212, 28, 32) red at power 2; (0, 212, 28, 32) yellow at power 3 | (40, 29) = A tab + (25, −1) | nothing at glove power 1 |
| S slot: sword | sub-rect of `swordN.png` from (94, 36), 28 high, 28–34 wide | screen = source + (11, −5), so (105, 31) | the same translation for sword 1 to 4 |
| D slot | — | about (170, 30) | empty in every run (no weapon selected) |
| Shield | — | not drawn | |
| AP frame | (0, 97, 130, 22) | (15, 65) | |
| AP fill | (0, 119, AP, 10) | (37, 71) = frame + (22, 6) | **1 px per AP point**; one fixed 100-px gradient strip clipped to AP, so the colour shows the level; empty interior is see-through |
| MP frame | (0, 49, 130, 22) | (15, 90) | **drawn only when MP > 0** |
| MP fill | (0, 71, MP, 10) | (37, 96) | 1 px per MP point |
| Gralat, bomb, arrow icons | icon strip | (274, 30), (330, 31), (379, 30) | |
| Digits | 14 × 16 cell at (14·d, 81), d = 0–9 | top y 48 | fixed 12-px advance, so cells overlap by 2 px |

**Counters.** Gralats are centred: the first digit is at x = 280 − 6·n for n digits, then +12 per
digit (one digit at 274, "1234" at 256–292). Gralats are drawn with no padding ("0", "1234",
"99999"); bombs and arrows always as **two zero-padded digits**, bombs at x 326 and 338, arrows at
374 and 386, so 100 arrows shows as "10". **[shot]**

The counters are anchored top-left like the tabs and bars: they keep their x at every window size.
Only the hearts are anchored top-right. Nothing is anchored to the centre or bottom. **[shot]**

## Hearts

The wire carries hearts in half-heart units (PLO 9 prop 2 = HP × 2), so a quarter heart cannot be
shown. **Only current hearts are drawn**: empty containers never are, and max hearts changes
neither the size nor the position of the block. **[cap][shot]**

| Sprite | state.png |
| --- | --- |
| full-size full heart | (0, 0, 40, 44) |
| full-size half heart | (40, 0, 30, 44) |
| small full heart | (80, 0, 31, 33) |
| small half heart | (111, 0, 24, 33) |

The small hearts are separate sprites drawn 1:1, not scaled. A half heart is drawn at its slot's own
top-left. **[shot]**

| HP | Layout |
| --- | --- |
| up to 4 | full size, one row: slots at x = W − 198 + 45k, y 24 (826, 871, 916, 961 at W = 1024) |
| 5 and up | small, staggered rows, horizontal pitch 35, row pitch 20; row 1: 5 slots at x = W − 198 + 35k, y 24; row 2: 6 slots half a pitch further left, y 44; row 3: 5 slots, y 64; row 4: 4 slots, y 84. Filled row by row, so 20 hearts make a hexagon (5 + 6 + 5 + 4) |
| 5 and 5.5 only | the whole small block sits 10 px lower (rows at y 34 and 54); from 6 it is back at 24 |

The right margin is 68 px for the full-size row at every window width, and the rightmost small
heart (row 2, slot 6) ends 10 px from the edge. **[shot]**

## Windows against Linux

Pixel diffs of the same states at 640 × 480, 800 × 600 and 1024 × 768: tiles, player, hearts,
icons, counters and bars are identical with no shift. **The only systematic difference is text.**
Windows draws font glyphs that the Linux run (no fonts installed or served) leaves out: the letters
"A", "S" and "D" on the tabs (white fill, red and black edge), a small glyph above "D", and the
sword power "1" to the right of the sword (white with blue). **[shot]**

On Windows the stock OpenGL path was the software GDI renderer ("Maximum texture size: 1024"); a
Mesa `opengl32.dll` placed next to the executable was not loaded. A Wine memory dump of the
6.03r7 executable crashed at start on real Windows; the packed original ran. **[lab]**

## Files and packets

HUD values arrive once at world login in PLO 9 (PLAYERPROPS): 1 max hearts, 2 HP in half hearts,
3 gralats (GINT3), 4 arrows, 5 bombs, 6 glove power, 8 sword, 9 shield, 25/26/32 AP counter, MP
and AP. The world server sends PLO 42 (new world time) every 5 s. **[cap]**

**AP regeneration shows in the bar.** About 66–68 s into a session the lab server raised AP from 50
to 51, and every later frame has one more fill column (x 87). Two captures of the same size can
differ by that column only because one was taken after the tick. **[cap][shot]**

Files the client asked for (C→S 23, WANTFILE) in every run **[cap]**:

| Stage | Requested |
| --- | --- |
| login server | `basepackage.gupd` (twice), `minimap.txt`, `arial.ttf`, `guigames_arcmessage2.png`, `idle.gani`, `pics1.png`, `wbowi1.png`, `wbomb1.png` |
| world server | `basepackage.gupd` (twice), `arial.ttf`, `sprites.png`, `body.png`, `head0.png`, `shield1.png`, `tempsitcbd.ttf`, `tempsitc.ttf`, `arialbd.ttf`, `state.png`, then the account's `swordN.png` / `shieldN.png` |

- **No text without fonts.** When the server does not have the four `.ttf` files the client draws
  no text at all: no chat, no NPC messages, no tab letters. The HUD digits are `state.png` glyphs
  and are drawn either way. The client's default font is Tempus Sans ITC, size 24. The same holds
  for 5.24r4. **[cap][shot]**
- **`pics1.png` must be in the cache before the warp.** When the login server's PLO 178 arrives in
  the middle of the `pics1.png` download, the download is dropped and the world is drawn black with
  no tiles; the client does not ask for it again. Seeding the cache avoids it. Both the Linux and the
  Windows 6.03r7 do this. **[cap][shot]**
- Keys Tab, Q, M and F2 opened nothing with no server GUI scripts; on 6.x those windows are server
  scripts. **[shot]**

## Open

- The exact right edge of the sword sub-rect (28 to 34 px; no source pixels pin it).
- The Windows text positions at other window sizes, and whether Windows 6.03r7 runs at a 2026 clock.
