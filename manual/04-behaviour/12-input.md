<!-- manual: kind=reference status=draft -->
# 4.12 Input: keys and mouse

This chapter says what each key and mouse action does on a logged-in client: the code a script sees, the bits of `keydown`, what a click sends, the default game keys, and the windows and failures a key opens. Keys that open side windows on the Delphi clients are tabulated by build family in → §4.6.6, key emotes in → §4.10.3, laying items with S held in → §4.5.2.2, and the Graal3D number-pad controls in → §9.6.1. The bindings saved in `graalconfig.txt` are in → §3.9.

> Status: draft. Every key and mouse action of one fixed list was pressed once on 2.05 rev 2, 2.17.1, 2.22, 2.31, 4.20r8, 5.12, 5.24r4 and Linux 6.03r7, logged in to a lab server on loopback. Keys were tapped, not held, so actions that need a hold may show nothing.

## 4.12.1 The sweep

The rules below give what was pressed, how each key's effect was recorded, and the limits of the record [lab] (protocol/keysweep/README.md).

| Rule | Detail | Source |
| --- | --- | --- |
| clients | Linux 6.03r7 natively; Windows 4.20r8, 5.24r4, 5.12, 2.31, 2.22, 2.17.1 and 2.05 rev 2 under Wine | [lab] (protocol/keysweep/README.md) |
| keys | F1 to F12, the number row, letters, punctuation, Space, each modifier alone, the edit block, arrows, keypad, the lock keys, Ctrl+letters, Alt+digits, Shift and Ctrl with the arrows, then Escape, Tab, Return, keypad Enter, Alt+Return and Alt+F4 last | [lab] (protocol/keysweep/README.md) |
| mouse | left, right, middle and double clicks on the own player, the ground, an NPC and the HUD, and the wheel | [lab] (protocol/keysweep/README.md) |
| what was recorded per key | any new window (title and size), the changed pixels on screen and where, any disconnect or crash, the client-to-server messages between the key's marks, and every key event a logging level script saw | [lab] (protocol/keysweep/README.md#key-and-mouse-sweep-on-real-clients) |
| the logging script | GS2 `onKeyPressed` on 4.x to 6.x, GS1 `keypressed` on 2.x; it reported through the player's chat prop, which is left out of the message record | [lab] (protocol/keysweep/README.md) |
| per-client tables | one table per client, with the key, its effect, the messages it sent, the script events and notes | [lab] (protocol/keysweep/README.md) |
| weak loggers | the 5.12 and 2.05 rev 2 loggers saw few events (12 on 5.12, almost none on 2.05 rev 2), so their script columns are mostly empty; their message and window columns are complete | [lab] (protocol/keysweep/README.md#limits) |
| idle noise | fewer than about 2000 changed pixels spread over the game area is idle animation, not an effect | [lab] (protocol/keysweep/README.md#limits) |

## 4.12.2 Key codes a script sees

Every client swept passes Windows virtual-key codes to scripts, the Linux 6.03r7 build included. The table gives the code for each key [lab] (protocol/keysweep/README.md#script-key-codes).

| Key | Code | Source |
| --- | --- | --- |
| F1 to F12 | 112 to 123 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| A to Z | 65 to 90; the character is lower case | [lab] (protocol/keysweep/README.md#script-key-codes) |
| 0 to 9 | 48 to 57 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| Escape, Tab, Return, BackSpace, Space | 27, 9, 13, 8, 32 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| `` ` `` `-` `=` | 192, 189, 187 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| `[` `]` `\` | 219, 221, 220 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| `;` `'` `,` `.` `/` | 186, 222, 188, 190, 191 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| Shift, Ctrl, Alt alone | 160, 162, 164 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| Insert, Delete, Home, End, PgUp, PgDn | 45, 46, 36, 35, 33, 34 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| Left, Up, Right, Down | 37, 38, 39, 40 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| keypad 0 to 9 | 96 to 105; the character is the digit | [lab] (protocol/keysweep/README.md#script-key-codes) |
| keypad `+` `-` `*` `/` `.` | 107, 109, 106, 111, 110 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| keypad Enter | 13 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| Pause, Scroll Lock, Caps Lock, Num Lock | 19, 145, 20, 144 | [lab] (protocol/keysweep/README.md#script-key-codes) |

How each script interface reports a key differs by generation. The rules below give the GS2 event on 4.x to 6.x and the GS1 event on 2.x [lab] (protocol/keysweep/README.md#script-key-codes).

| Rule | Builds | Detail | Source |
| --- | --- | --- | --- |
| modifiers in the code | 4.x to 6.x (`onKeyPressed`) | Shift adds 256, Ctrl 512 and Alt 1024 (Shift+Left 293, Ctrl+Left 549, Alt+7 1079, Alt+Return 1037); a combination first reports the modifier alone (Ctrl 162, Alt 164) | [lab] (protocol/keysweep/README.md#script-key-codes) |
| Ctrl+letter | 4.20r8, 5.24r4, 6.03r7 | reports only the Ctrl key (162), not a combined code; the letter still drives the game key, so Ctrl+A sets the action bit and Ctrl+M the map bit | [lab] (protocol/keysweep/README.md#script-key-codes) |
| third value | 4.x to 6.x | the hardware scan code: the X keycode on Linux 6.03r7 (a 38, F1 67), the PC set-1 scan code under Windows (a 30, F1 59) | [lab] (protocol/keysweep/README.md#script-key-codes) |
| which keys reach the script | 4.x to 6.x | every key, F-keys, Escape and the modifiers alone included; a key with no game action sends no message | [lab] (protocol/keysweep/README.md#script-key-codes) |
| `keypressed` parameters | 2.17.1, 2.22, 2.31 | `#p(0)` is the same virtual-key code, `#p(1)` the character, `#p(2)` empty | [lab] (protocol/keysweep/README.md#script-key-codes) |
| Ctrl in GS1 | 2.17.1, 2.22, 2.31 | Ctrl adds 512 (Ctrl+A 577 to Ctrl+Z 602), except Ctrl+H, Ctrl+I, Ctrl+M and Ctrl+S, which give the ASCII controls 8, 9, 13 and 19; Ctrl+T, Ctrl+J and Ctrl+U give 145, 228 and 556 on all three builds; 2.31 logged Ctrl+S only as `keydown` bits | [lab] (protocol/keysweep/README.md#script-key-codes) |
| 2.05 rev 2 | 2.05 rev 2 | arrows, Shift, Alt and Alt+digits raise no `keypressed`; keypad 0 gives 48 and "0"; the rest of its script codes are unmeasured | [lab] (protocol/keysweep/README.md#script-key-codes) |

## 4.12.3 `keydown` bits

`keydown(i)` reads the game keys, not raw key codes. The logger reported the bit sum of `keydown(0)` to `keydown(10)`, and the table gives the bit each game key sets [lab] (protocol/keysweep/README.md#script-key-codes).

| `keydown` index | Game key | Bit | Source |
| --- | --- | --- | --- |
| 0 | up | 1 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| 1 | left | 2 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| 2 | down | 4 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| 3 | right | 8 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| 4 | D (item) | 16 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| 5 | S (attack) | 32 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| 6 | A (action) | 64 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| 7 | M (map) | 128 | [lab] (protocol/keysweep/README.md#script-key-codes) |
| 10 | held keypad keys on 2.31 | 1024 | [lab] (protocol/keysweep/README.md#script-key-codes) |

The server-side GS1 documentation that pyReborn follows gives the same order for 0 to 7 and names 8 chat (Tab) and 9 inventory (Q); the sweep did not see bits 8 and 9 [srv] (client-internals/pyreborn-study/README.md#client-side-script-behaviour-hints-to-check). pyReborn also lets scripts read keys while the player is frozen and has a `keydown2(code, edge)` form; neither was checked in a client [srv][inf] (client-internals/pyreborn-study/README.md#client-side-script-behaviour-hints-to-check).

## 4.12.4 Mouse clicks

On every client swept except 2.05 rev 2, every click sends `PLI_TRIGGERACTION` (38) whether or not anything is under the cursor, and nothing shows on screen. The rules below give its body and the other mouse results [lab] (protocol/keysweep/README.md#mouse-clicks-pli-38).

| Rule | Builds | Detail | Source |
| --- | --- | --- | --- |
| builds that send 38 | 2.17.1, 2.22, 2.31, 4.20r8, 5.12, 5.24r4, 6.03r7 | one 38 per click | [lab] (protocol/keysweep/README.md#mouse-clicks-pli-38) |
| NPC id | as above | three bytes, all 0 (`0x20 0x20 0x20`) | [lab] (protocol/keysweep/README.md#mouse-clicks-pli-38) |
| position | as above | x, then y, one `GCHAR` each: the level position clicked, in half tiles; the value is 7-bit, so x wraps past 64 tiles (a click 55 tiles across arrived as 7) | [lab] (protocol/keysweep/README.md#mouse-clicks-pli-38) |
| action | as above | the text `leftmouse`, `rightmouse` or `middlemouse`, with no length byte (→ §2.4) | [lab] (protocol/keysweep/README.md#mouse-clicks-pli-38) |
| double click | 4.x to 6.x | `leftmouse`, then `doublemouse` | [lab] (protocol/keysweep/README.md#mouse-clicks-pli-38) |
| double click | 2.17.1, 2.22, 2.31 | `leftmouse`, `doublemouse`, then a further `leftmouse` | [lab] (protocol/keysweep/README.md#mouse-clicks-pli-38) |
| 2.05 rev 2 | 2.05 rev 2 | no 38 for any click | [lab] (protocol/keysweep/README.md#mouse-clicks-pli-38) |
| wheel | all | sends nothing | [lab] (protocol/keysweep/README.md#mouse-clicks-pli-38) |
| right click on the own player | 2.05 rev 2, 2.17.1, 2.22, 2.31, 4.20r8, 5.12 | opens the "Profile" window and sends `PLI_PROFILEGET` (80) with the bare account name, before the 38 | [lab] (protocol/keysweep/README.md#mouse-clicks-pli-38) |
| right click on the own player | 5.24r4, 6.03r7 | no 80 | [lab] (protocol/keysweep/README.md#mouse-clicks-pli-38) |

## 4.12.5 Game keys

6.03r7 uses the default key sets of `game_config.txt`, and the Windows builds behave the same. The table gives each set [lab] (protocol/keysweep/README.md#game-keys).

| Set | Move | Item | Attack | Action | Map | Other | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | arrows | D | S | A | M | Tab to chat, Q item list, P pause | [lab] (protocol/keysweep/README.md#game-keys) |
| 1 | keypad 8, 4, 2, 6 | keypad 1 (fires the bow) | keypad 5 | keypad 3 | keypad `+` | keypad `*` item list, keypad 0 pause | [lab] (protocol/keysweep/README.md#game-keys) |
| 2 | I, J, K, L | n/a | Space | n/a | n/a | n/a | [lab] (protocol/keysweep/README.md#game-keys) |

The rules below give what the movement and action keys send [lab] (protocol/keysweep/README.md#game-keys).

| Rule | Builds | Detail | Source |
| --- | --- | --- | --- |
| walking | all swept | arrows, Shift or Ctrl with the arrows, I/J/K/L and keypad 2/4/6/8 send `PLI_PLAYERPROPS` (2) with `gani=walk`, the sprite (direction) and props 78 and 79 (X2 and Y2, in half-tile steps), and end with `gani=idle` | [lab] (protocol/keysweep/README.md#game-keys) |
| walk event | 4.x to 6.x | also send 157 `walk` | [lab] (protocol/keysweep/README.md#game-keys) |
| file check before walking | 2.x, 4.x, 5.x | check `walk.gani` and the step sound with `PLI_UPDATEFILE` (34) before using them | [lab] (protocol/keysweep/README.md#game-keys) |
| file check before walking | 6.03r7 | uses `PLI_WANTFILE` (23) instead | [lab] (protocol/keysweep/README.md#game-keys) |
| D | 6.03r7 | fires the bow: `gani=shoot,wbow1.png`, `PLI_ARROWADD` (9), and prop 4 (arrows) goes down by one | [lab] (protocol/keysweep/README.md#game-keys) |
| S and Space | all swept | swing the sword (`gani=sword`; the timings are in → §4.3.2) | [lab] (protocol/keysweep/README.md#game-keys) |
| Q, P, keypad 0 | all swept | open the item list or pause: the paused bit of status prop 18 is set (20 → 21), and 6.03r7 asks for `letters.png`; the next key closes the list | [lab] (protocol/keysweep/README.md#game-keys) |

## 4.12.6 Windows, emoticons and quits

The F-keys of the Delphi clients are tabulated by family in → §4.6.6. The table below adds what the sweep saw on the later builds and on 2.31 online [lab] (protocol/keysweep/README.md#game-keys).

| Build | Keys and what they open | Source |
| --- | --- | --- |
| 2.31 | F1 "Help", F2 "RPG Window for <account>", F5 "Load level", F7 "Playerlist", Alt+0 "Log", Alt+1 and Alt+2 "Save screenshot"; Escape opens a small "Warning" box that asks before quitting | [lab] (protocol/keysweep/README.md#game-keys) |
| 4.20r8 | F2 "Log", F3 "Options", O "PlayerList Options", F5 an in-game GUI prompt, Alt+2 "Save Screenshot"; F8 sends an empty chat prop and seems to open a chat input | [lab] (protocol/keysweep/README.md#game-keys); [lab] (protocol/keysweep/README.md#limits) |
| 5.24r4 | Escape opens an in-game menu in the blue GUI skin, and Return then quits; Alt+2 "Save As" | [lab] (protocol/keysweep/README.md#game-keys) |
| 6.03r7 | Alt+2 an in-game "Save As" window; Alt+8 starts a video capture file in the client's `videos` folder | [lab] (protocol/keysweep/README.md#game-keys) |

Ctrl and a letter shows an emoticon on some builds. The rules below extend the 2.05 rev 2 key emote of → §4.10.3 to the later builds [lab] (protocol/keysweep/README.md#game-keys).

| Rule | Builds | Detail | Source |
| --- | --- | --- | --- |
| emoticons | 2.17.1, 2.22, 2.31 | Ctrl+letter shows one of the 26 emoticons (`emoticon_afk_stay.mng` to `emoticon_zzz_stay.mng`); the client checks the file with `PLI_UPDATEFILE` (34), then sends in `PLI_SHOWIMGPLAYER` (24) an add record (image 0, the file name, x and y two tiles right of and five above the player) and, about 0.1 s later, a remove record | [lab] (protocol/keysweep/README.md#game-keys) |
| emoticons | 2.05 rev 2 | checks the same files with 34 but sends no 24 | [lab] (protocol/keysweep/README.md#game-keys) |
| emoticons | 5.12 | none shown | [lab] (protocol/keysweep/README.md#game-keys) |

The rules below give the keys that quit, change the window or ended the session [lab] (protocol/keysweep/README.md#game-keys).

| Key | Builds | Result | Source |
| --- | --- | --- | --- |
| Alt+F4 | 2.31, 4.20r8, 5.24r4 | quits | [lab] (protocol/keysweep/README.md#game-keys) |
| Alt+F4 | 6.03r7 | does not quit | [lab] (protocol/keysweep/README.md#game-keys) |
| Alt+Return | 4.20r8 | opens a 1024 × 768 full-screen window | [lab] (protocol/keysweep/README.md#game-keys) |
| Alt+Return | 2.31 | opens a second game window | [lab] (protocol/keysweep/README.md#game-keys) |
| Alt+Return | 5.24r4 | crashed the client under Wine | [lab] (protocol/keysweep/README.md#game-keys) |
| F8 | 2.31 | dropped the session | [lab] (protocol/keysweep/README.md#game-keys) |
| F1, F2, F5, F10 | 2.31 | under Wine, took the client down after their window closed | [lab] (protocol/keysweep/README.md#game-keys) |

## 4.12.7 What the sweep left open

The points below were not measured, so their cells stay `unmeasured` [lab] (protocol/keysweep/README.md#limits).

| Point | Why | Source |
| --- | --- | --- |
| held keys | keys were tapped (arrows held 0.4 s), so actions that need a hold were not seen | [lab] (protocol/keysweep/README.md#limits) |
| 4.20r8 F9 to N | F8 opened a chat input and the keys after it were typed into it | [lab] (protocol/keysweep/README.md#limits) |
| 5.24r4 K to `/` | after J (an alternate left-walk key) the player likely walked off the logger's level | [lab] (protocol/keysweep/README.md#limits) |
| 2.05 rev 2 and 5.12 script codes | their loggers saw too few events | [lab] (protocol/keysweep/README.md#limits) |
| keys on the login form, and how others see a 2.05 key emote | not covered by the sweep; the key and chat fuzz plans that would add them were queued but not run | [lab] (live-runs/fuzz-2026-11-19/README.md#58-not-run-vm-load) |
