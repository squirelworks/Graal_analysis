# Key and mouse sweep on real clients

Date: 2026-11-19. Status: **in progress**. Linux 6.03r7 and Windows 4.20r8 (under Wine) are swept;
5.24r4, 2.31, 2.22, 2.17.1, 2.05 rev 2 and 5.12 have only had a five-key login trial so far.

Every key and mouse action of `tools/probe/lab/keysweep.keys` (F1–F12, Escape, the number row,
letters, punctuation, Return, Space, modifiers alone, the edit block, arrows, keypad, lock keys,
Ctrl+letters, Alt+digits, Alt+Return, Shift/Ctrl+arrows, left/right/middle/double clicks on the
own player, the ground, an NPC and the HUD, the wheel, Alt+F4) was pressed once on a logged-in real
client in the lab world. The client was on our own lab gserver behind the probe proxy, on loopback
only. The tool is `tools/probe/lab/keysweep.sh` (see `tools/probe/README.md`, "Key and mouse sweep").
A key-logging level script reported each key event and the `keydown(0..10)` bits through the
player's chat prop. On 4.x–6.x it is GS2 `onKeyPressed`, compiled by Seihai's own compiler; on 2.x
it is GS1 `keypressed`.

Tables, one per client (`client, key, effect, c2s, script_event, notes`):

| File | Client | Runs |
|---|---|---|
| [`603r7.tsv`](603r7.tsv) | 6.03r7 Linux | with logger + clean (effects from the clean run) |
| [`420r8.tsv`](420r8.tsv) | 4.20r8 Windows | with logger |
| [`524r4.tsv`](524r4.tsv) | 5.24r4 Windows | with logger; \` … / were typed into the Escape menu (redo pending) |
| [`231.tsv`](231.tsv) | 2.31 Windows | with logger (GS1 keypressed NPC); several restarts, hung stretches re-pressed |

Columns: `effect` gives any new window (title, size), the screen change (changed pixels and
bounding box in game-window pixels, and what it is near), and any disconnect or crash. `c2s` lists
the client→server packets between the key's marks, as `id:NAME{decoded props}`; the logger's own
chat props are taken out. `script_event` is `key(code,char,scan)` for each key event the script
saw, and `keydown=N` for the bit sum of `keydown(0..10)` when it changed.

## Script key codes (onKeyPressed, 4.20r8 and 6.03r7)

[lab] Both clients pass Windows virtual-key codes, the Linux 6.03r7 build too:

| Key | code | Key | code |
|---|---|---|---|
| F1–F12 | 112–123 | Escape | 27 |
| Tab | 9 | Return | 13 |
| BackSpace | 8 | Space | 32 |
| A–Z | 65–90 (char is lower case) | 0–9 | 48–57 |
| \` - = | 192 189 187 | [ ] \ | 219 221 220 |
| ; ' , . / | 186 222 188 190 191 | Shift / Ctrl / Alt alone | 160 / 162 / 164 |
| Insert Delete Home End PgUp PgDn | 45 46 36 35 33 34 | Left Up Right Down | 37 38 39 40 |
| Keypad 0 | 96 | | |

- Modifiers are added to the code: Shift +256, Ctrl +512, Alt +1024 (Shift+Left 293, Ctrl+Left 549,
  Alt+7 1079, Alt+Return 1037). A combination first reports the modifier alone (Ctrl 162, Alt 164).
- The third value is the hardware scan code: the X keycode on Linux 6.03r7 (a 38, F1 67), the PC
  set-1 scan code on Windows 4.20r8 (a 30, F1 59).
- Every key reaches the script, including F-keys, Escape and the modifiers alone. A key with no game
  action sends no packet.
- `keydown(i)`: arrows set bits 0–3 (up 1, left 2, down 4, right 8). S (attack) sets 32, which is
  `keydown(5)`.

## Mouse clicks (PLI 38)

[lab] On 4.20r8 and 6.03r7 every click sends PLI 38 (TRIGGERACTION) whether or not anything is under
the cursor, and nothing shows on screen. The body is:

- three bytes of NPC id, all 0 (`0x20 0x20 0x20`)
- x and y as one GCHAR each: level position in half tiles of the point clicked. The value is 7-bit,
  so x wraps past 64 tiles: a click 55 tiles across the level arrived as 7.
- the action text `leftmouse`, `rightmouse` or `middlemouse`. A double click sends `leftmouse`
  and then `doublemouse`.

The wheel sends nothing. On 4.20r8 a right click on the own player also opens the Profile window and
sends PLI 80 (`p` + account name).

## Game keys

[lab] 6.03r7 uses the default `game_config.txt` key sets:

- Set 0: arrows, D item, S attack, A action, M map, Tab to chat, Q item list, P pause.
- Set 1: keypad 8/4/2/6 to move, keypad 1 item, keypad 5 attack, keypad 3 action, + map,
  \* item list, keypad 0 pause.
- Set 2: I/J/K/L to move, Space attack.

Seen on 6.03r7:
- Walking (arrows, Shift/Ctrl+arrows, J/K taps) sends PLI 2 with `gani=walk`, the sprite (dir) and
  props 78/79 (X2/Y2, half-tile steps). It also sends PLI 157 `walk`, asks for `steps.wav`, and ends
  with `gani=idle`.
- D fires the bow: `gani=shoot,wbow1.png`, PLI 9 (ARROWADD), and prop 4 (arrows) goes down by one.
- Q (item list), P and keypad 0 (pause) set the status prop 18 paused bit (20 → 21) and ask for
  `letters.png`. The next key closes the list.
- Alt+2 opens an in-game "Save As" GUI window. Alt+8 changes the top of the screen and a video file
  starts growing in the client's `videos` folder.
- F1–F12, Escape, Return, Tab, Ctrl+letters, the wheel and Alt+F4 show nothing and send nothing.
  Alt+F4 does not quit 6.03r7.

Seen on 4.20r8:
- F2 opens the "Log" window, F3 "Options" and O "PlayerList Options". F5 opens an in-game GUI
  prompt, and Alt+2 a "Save Screenshot" window.
- P and Q pause (status 21). Space is attack (`gani=sword`). Walking is as on 6.03r7.
- Alt+Return switches to a 1024×768 full-screen window. Alt+F4 quits the client.

## Limits and redo

- Keys were tapped, not held (arrows were held 0.4 s), so actions that need a hold may show nothing.
- 6.03r7 keypad 1 … Alt+2 were pressed while the client was paused (keypad 0 is the second pause
  key): to be redone.
- 4.20r8 F6 … O were typed into the F5 prompt, and keypad 1 … Alt+9 ran with keys stuck down after
  the lock-key block (walk gani and a status flip on every key): to be redone. The sweep now releases
  every modifier, arrow and keypad key after each step.
- Without the logger, screen changes near the player are real effects. In logged runs a chat
  bubble also appears there, so use the clean-run tables where they exist.
