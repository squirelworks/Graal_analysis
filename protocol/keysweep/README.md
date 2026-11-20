# Key and mouse sweep on real clients

Date: 2026-11-19/20. Swept: Linux 6.03r7, and Windows 4.20r8, 5.24r4 and 2.31 under Wine. 2.22,
2.17.1, 2.05 rev 2 and 5.12 are being swept on another lab host with the same tool.

Every key and mouse action of `tools/probe/lab/keysweep.keys` was pressed once on a logged-in real
client in the lab world: F1–F12, the number row, letters, punctuation, Space, modifiers alone, the
edit block, arrows, keypad, lock keys, Ctrl+letters, Alt+digits, Shift/Ctrl+arrows, and
left/right/middle/double clicks on the own player, the ground, an NPC and the HUD, plus the wheel.
Last come Escape, Tab, Return, keypad Enter, Alt+Return and Alt+F4. The client was on our own lab
gserver behind the probe proxy, on loopback only. The tool is `tools/probe/lab/keysweep.sh` (see
`tools/probe/README.md`, "Key and mouse sweep").

A key-logging level script reported each key event and the `keydown(0..10)` bits through the
player's chat prop. On 4.x–6.x it is GS2 `onKeyPressed`, compiled by Seihai's own compiler; on 2.x
it is GS1 `keypressed`.

Tables, one per client (`client, key, effect, c2s, script_event, notes`):

| File | Client | Runs |
|---|---|---|
| [`603r7.tsv`](603r7.tsv) | 6.03r7 Linux | with logger + clean (effects from the clean run); keypad 1 … Alt+2 redone |
| [`420r8.tsv`](420r8.tsv) | 4.20r8 Windows | with logger; F6 … O and keypad 1 … Alt+9 redone |
| [`524r4.tsv`](524r4.tsv) | 5.24r4 Windows | with logger; \` … / redone twice |
| [`231.tsv`](231.tsv) | 2.31 Windows | with logger (GS1 `keypressed`); hung stretches pressed again after restarts |

Columns:
- `effect`: any new window (title, size), the screen change (changed pixels and a bounding box in
  game-window pixels, and what it is near), and any disconnect or crash.
- `c2s`: the client→server packets between the key's marks, as `id:NAME{decoded props}`. The
  logger's own chat props are taken out.
- `script_event`: `key(code,char,scan)` for each key event the script saw, and `keydown=N` for the
  bit sum of `keydown(0..10)` when it changed.

## Script key codes

[lab] Every client swept passes Windows virtual-key codes, the Linux 6.03r7 build too:

| Key | code | Key | code |
|---|---|---|---|
| F1–F12 | 112–123 | Escape | 27 |
| Tab | 9 | Return | 13 |
| BackSpace | 8 | Space | 32 |
| A–Z | 65–90 (char is lower case) | 0–9 | 48–57 |
| \` - = | 192 189 187 | [ ] \ | 219 221 220 |
| ; ' , . / | 186 222 188 190 191 | Shift / Ctrl / Alt alone | 160 / 162 / 164 |
| Insert Delete Home End PgUp PgDn | 45 46 36 35 33 34 | Left Up Right Down | 37 38 39 40 |
| Keypad 0–9 | 96–105 (char is the digit) | Keypad + - * / . | 107 109 106 111 110 |
| Pause / Scroll Lock / Caps Lock / Num Lock | 19 / 145 / 20 / 144 | Keypad Enter | 13 |

- 4.x–6.x (`onKeyPressed`):
  - Modifiers are added to the code: Shift +256, Ctrl +512, Alt +1024 (Shift+Left 293, Ctrl+Left
    549, Alt+7 1079, Alt+Return 1037). A combination first reports the modifier alone (Ctrl 162,
    Alt 164).
  - On 4.20r8, 5.24r4 and 6.03r7, Ctrl+letter reports only the Ctrl key (162), not a combined code. The
    letter still drives the game key: Ctrl+A sets the action bit, Ctrl+M the map bit.
  - The third value is the hardware scan code: the X keycode on Linux 6.03r7 (a 38, F1 67), the PC
    set-1 scan code under Windows (a 30, F1 59).
  - Every key reaches the script, including F-keys, Escape and the modifiers alone. A key with no
    game action sends no packet.
- 2.31 (GS1 `keypressed`):
  - `#p(0)` is the same VK code and `#p(1)` the char; `#p(2)` is empty.
  - Ctrl adds 512 (Ctrl+A 577 … Ctrl+Z 602). Ctrl+H, Ctrl+I and Ctrl+M give the ASCII controls 8, 9
    and 13.
  - Arrows, Shift, Alt and Alt+digits raise no `keypressed`. Keypad 0 gives 48/"0".
- `keydown(i)` bits: up 1, left 2, down 4, right 8, D 16, S 32, A 64, M 128; held keypad keys showed
  1024 (`keydown(10)`) on 2.31.

## Mouse clicks (PLI 38)

[lab] On every client swept (2.31, 4.20r8, 5.24r4, 6.03r7), every click sends PLI 38
(TRIGGERACTION) whether or not anything is under the cursor, and nothing shows on screen. The body is:

- three bytes of NPC id, all 0 (`0x20 0x20 0x20`)
- x and y as one GCHAR each: the level position of the point clicked, in half tiles. The value is
  7-bit, so x wraps past 64 tiles: a click 55 tiles across the level arrived as 7.
- the action text `leftmouse`, `rightmouse` or `middlemouse`, with no length byte. A double click
  sends `leftmouse` then `doublemouse` (4.x–6.x); 2.31 sends a further `leftmouse` after that.

The wheel sends nothing. On 2.31 and 4.20r8 a right click on the own player also opens the
"Profile" window and sends PLI 80 with the bare account name.

## Game keys

[lab] 6.03r7 uses the default `game_config.txt` key sets:

- Set 0: arrows, D item, S attack, A action, M map, Tab to chat, Q item list, P pause.
- Set 1: keypad 8/4/2/6 to move, keypad 1 item (fires the bow), keypad 5 attack, keypad 3 action, + map,
  \* item list, keypad 0 pause.
- Set 2: I/J/K/L to move, Space attack.

The Windows builds behave the same.

Movement and actions:
- Walking (arrows, Shift/Ctrl+arrows, I/J/K/L, keypad 2/4/6/8) sends PLI 2 with `gani=walk`, the
  sprite (direction) and props 78/79 (X2/Y2, half-tile steps), and ends with `gani=idle`.
  - 4.x–6.x also send PLI 157 `walk`.
  - 4.x–5.x and 2.x check `walk.gani` and the step sound with PLI 34 (file date) before using them;
    6.03r7 uses PLI 23.
- D fires the bow on 6.03r7: `gani=shoot,wbow1.png`, PLI 9 (ARROWADD), and prop 4 (arrows) goes down
  by one. S and Space swing the sword (`gani=sword`).
- Q (item list), P and keypad 0 (pause) set the status prop 18 paused bit (20 → 21), and 6.03r7 asks
  for `letters.png`. The next key closes the list.

Windows and in-game GUIs:
- 2.31: F1 "Help", F2 "RPG Window for <account>", F5 "Load level", F7 "Playerlist", Alt+0 "Log",
  Alt+1/Alt+2 "Save screenshot". Escape opens a small "Warning" box (quit confirm).
- 4.20r8: F2 "Log", F3 "Options", O "PlayerList Options", F5 an in-game GUI prompt, Alt+2 "Save
  Screenshot".
- 5.24r4: Escape opens an in-game guiblue menu, and Return then quits; Alt+2 "Save As".
- 6.03r7: Alt+2 an in-game "Save As" window; Alt+8 starts a video capture file in the client's
  `videos` folder.

2.31 Ctrl+letter shows the 26 emoticons (`emoticon_afk_stay.mng` … `emoticon_zzz_stay.mng`). It
checks the file with PLI 34 and sends an add record and, about 0.1 s later, a remove record in
PLI 24.

Quits and failures:
- Alt+F4 quits 2.31, 4.20r8 and 5.24r4, but not 6.03r7.
- Alt+Return opens a 1024×768 full-screen window on 4.20r8 and a second game window on 2.31; it
  crashed 5.24r4 under Wine.
- 2.31 F8 dropped the session. Under Wine, 2.31 F1/F2/F5/F10 took the client down after their
  window closed.

## Limits

- Keys were tapped, not held (arrows were held 0.4 s), so actions that need a hold may show nothing.
- 4.20r8: F8 sends an empty chat prop and seems to open a chat input, so F9 … N typed into it and
  show no script events.
- 5.24r4: after J (an alternate left-walk key), K … / showed no script events, likely because the
  player walked off the logger's level.
- Under heavy VM load the Wine 2.x clients stall. The sweep then sees no packets for 15 s, restarts
  the client and presses the last keys again.
- Screen-change counts under ~2000 px spread over the game area are idle animation, not an effect.
  In logged runs the logger's chat bubble also appears near the player; the clean-run table (6.03r7)
  has none.
