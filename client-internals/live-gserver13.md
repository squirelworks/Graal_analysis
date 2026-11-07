# The real 1.3 server and client, live under Wine (2026-10-30)

The 1999 `GServer13.exe` and the 1.3 test client `Graal13.exe` (both from the `graal13b` archive) were run together under Wine, inside a loopback-only network namespace. The traffic was captured with tcpdump. This is the first time an original server and its own client were played together in the lab. Tags: **[live]** seen in the running programs, **[cap]** read from the capture.

The raw capture, the decoded message list, screenshots, the run notes and the tools are in the project files under `graal-decompile/live-trace/early/`. This note has no addresses and no decompiler text.

## Server settings and the default account **[live]**

GServer13 opens a start dialog before it listens:

| setting | default |
|---|---|
| port | 14804 |
| respawn time (bushes etc.) | 10 s |
| horse lifetime | 10 s |
| alignment increment time | 1200 s |
| baddies respawn time | 60 s |

These values are saved to `serverconfig.txt` as `serverport`, `respawntime`, `horselifetime`, `apincrementtime` and `baddyrespawntime`.

A new account from Edit accounts starts with these values:

* level `onlinestartlocal.graal` at x 30.5, y 30
* AP 50, MP 0
* 3 hearts of 3
* 0 rupees, 10 bombs, 5 arrows
* glove 1, bomb 1, bow 1
* sword 1 `sword1.gif`, shield 1 `shield1.gif`
* head `head0.gif`, colors orange, white, blue, red, black
* weapons enabled, no spin attack

The rights levels are no rights, Graalian Police, Trusted Admin and Administrator. The 1.3 zip does not ship `onlinestartlocal.graal`. It was copied from the 15th Graal build, which uses the same `GR-V1.03` level format.

## Login **[cap]**

* **Client's first frame.** u16 big-endian length + zlib of id 0 + `GSERV014` + length-prefixed account + length-prefixed password + `\n`. Lengths are chr(n + 32).
* **Wrong account.** The server sends id 16 with the text "An account with the name and password you typed in doesn't exist.", and the client offers Reconnect or Play offline.
* **Good login, server order.**
  1. 9: player props.
  2. 14: warp, with x, y and the level name.
  3. 100: raw-data size, 8194.
  4. A **separate** zlib frame holding 101 (board) + 8192 bytes. In 2.05 the size message and the board share one frame.
  5. 6: level name.
  6. 1: level links.
  7. 5: signs.
  8. 39: level modification time.
  9. 3: NPC props, one message per NPC, carrying the whole script.
  10. 10.
* **Client's next messages.** It asks for each NPC image with 23, sets flags from the NPC scripts with 18, and adds horses with 7 (from `puthorse`). The server answers 30 (file not sent) for images it lacks. It deletes each horse with 18 about 9.5 to 9.8 s later, which matches the 10 s horse lifetime on a 1 s server tick.
* **Server sweeps.** The horse deletes and the bush regrows all landed on the same fractional second, so the server checks its timers once a second.

## In play **[live] [cap]**

* **Walking.** While a key is held, the client sends one id 2 (player props) message every 100 ms, carrying X (prop 15) and SPRITE (17). Speed is 0.5 tile per 50 ms tick, the same as 2.05.
* **Chat.** Sent as id 2 prop 12. It is drawn as plain white text with a blue outline above the head, with **no bubble** (`shots/chat13.png`).
* **Cutting a bush.**
  * The client sends id 1 (board modify) with x, y, w = 2, h = 2 and the four leftover tiles.
  * The server does not echo the change back to the cutter.
  * The server regrows the bush with id 7 and the original tiles 2 3 / 18 19.
  * Two cuts regrew after 7.6 s and 9.2 s. Both fit the 6 to 12 s formula in `board-respawn.md`.
  * A bush cut also dropped rupees, which were rolled on the client, as that note describes.

## Wine notes for 1.x clients

* **Keyboard.** The 1.3 client gives DirectInput a keyboard data format that lists one object, with a 256-byte buffer. Windows filled the whole buffer. Wine fills only the listed objects, so the arrow keys never reach the game. Keys do reach DirectInput, and chat and Alt shortcuts work, so the player just stands still.
  * Patching the exe on disk trips the client's own checksum ("The Graal execution file is corrupted").
  * `tools/kbfix.py` in the project files instead rewrites the format in memory to a full 256-key table right after start, before the client sets it. Walking then works.
  * Other Delphi builds that use the same DirectX header probably need the same fix at their own address.
* **Display.** Run a window manager (openbox) on the Xvfb display. Set Wine's Direct3D renderer to `gdi`. With the GL renderer, each DirectDraw blit was very slow.
* **Settings.** Edit `graalconfig.txt` (`gamemode=One Player Online`, `serveraddr=<loopback>`) rather than typing into the server combo box, which mangled the text.

## Which builds start under Wine **[live]**

Each archive was unpacked and its client started offline for 15 s (`survey-all-builds.txt` in the project files).

* **Opens its window:** every build from the 1st to 15th Graal builds (including the 4th, 5th and 9th alphas), 1.1, 1.1.9, 1.28b2, 1.3 test, 1.31 to 1.39, 1.41.1, 2.0 (all revs), 2.01, 2.03, 2.04, 2.05 (all revs), 2.1 test 2 and 3, NewMain 24 and 26, NewWorld beta 1 and 2, and Graal 3D.
* **Exits at once:** 2.02, all three revisions.
* **NewMain 24:** opens a "File not found" box.
* **No client exe in the archive:** 1.21 and Zelda Online 2.
