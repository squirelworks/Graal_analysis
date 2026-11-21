# Keyboard fuzz and other-player prop widths, 2026-11-20

**What this round adds.** It closes the two parts of the
[2026-11-19 fuzz round](../fuzz-2026-11-19/README.md) that were still open: keyboard and chat
input, and the widths of other-player props on the Windows clients. The other queued items (the shot
byte, 4.20r8 GS2 delivery, the 2.22/2.31 NPC widths and the 2.05 key emote) had already run in
the [lab host A Appendix E lab](../../protocol/lab-appe-hosta-2026-11-20.md).

- **Other-player props (`PLO_OTHERPLPROPS`, 8):** 74 and 75 are strings and 76 is five bytes on all four
  builds. 77 and everything from 83 up end the message. From 2.31 on, 78–80 are the two-byte X2/Y2/Z2. The
  Y2 test values (79) put the player off screen. 81 is one byte on 4.20r8 and 5.24r4, and 82 is a string on 5.24r4 only.
- **Key codes (2.x `keypressed`):** the code is the upper-case ASCII value. Shift adds 256 and Ctrl adds 512.
  Keys with no code (such as `(` and `)`) report −1.
- **Ctrl+letter on 2.05 and 2.22:** every letter A to Z is a local emoticon. Each one sends a single
  file check (34), once per session, and nothing that reaches other players.
- **Modal windows stop all traffic.** Escape opens a quit box on 2.x, and Space then confirms it. An F-key
  opens Options on 4.20r8. While either is open, the client sends nothing at all.
- **Chat text goes out raw.** `#` codes are not expanded by the client, and Latin-1 bytes are not escaped.
- No client crashed. The only exits were the quit box being confirmed.

Evidence: lab **[lab]**. Rows are in `fuzz-results.tsv`, which has the columns of
[`probe-results.tsv`](../../protocol/probe-results.tsv), and they are appended there too.

## Lab

The lab is the lab host A Debian lab VM, on loopback only. The clients run under Wine 10, behind a gs2emu
lab gserver and the `gen5probe` proxy (`tools/probe`). Each run uses one client, and runs go one at a time
on an idle VM (1-minute load under 3, with no other thread's probe run live). Captures and screenshots
stay in the lab.

- **2.x** runs log in to a copy of the "GS1 Control" world. Its start level holds a key-logger NPC:
  `keypressed` sets the chat to `K<code>_<char>_`, and a 0.1 s timer reports the `keydown(0..10)`
  bitmask as `D<n>`. So C>S prop 12 shows what the client's script engine sees for each key.
- **4.20r8 and 5.24r4** start on a plain lab level. For these, the observer is the C>S traffic that
  each input causes.
- Input comes from `xdotool` into the client window (`plans/kx2.sh`). Plans: `plans/keychat2.plan`
  (keys) and `plans/otherpl-win.plan` (widths). `plans/kan.py` lists the C>S traffic per mark, and
  `plans/opcls.py` finds the fake player in each width shot.
- `xdotool type` under Xvfb drops some characters of fast-typed text (`fzhello1` sometimes reached
  2.x as `f`, `l`, Return). Single keys and key combos arrive intact.

## 1. Other-player prop widths (PLO_OTHERPLPROPS, 8)

Each test makes a fresh fake player with its own id. It has a nickname, an account, the current level,
gani `idle`, and a position of (26, 26). The test packet is `[tested prop][value][X = 36]`. If the
player then stands at x = 36, the client read the tested prop at that width. The shot is then
compared with a shot of the level with no fake player. Afterwards the player is moved to another
level so it leaves the screen. The values sent are `c:0`, `s:300`, `str:x` and `i5:2080768`.

| Prop | 2.22 | 2.31 | 4.20r8 | 5.24r4 | (6.03r7, earlier) |
|---|---|---|---|---|---|
| controls (canary only; 12 chat; 2 power) | lands | lands | lands | lands | lands |
| 74 | string (`c:0`, `str:x` land) | string | string | string | — |
| 75 | string | string | string | string | — |
| 76 | 5 bytes (only `i5` lands) | 5 bytes | 5 bytes | 5 bytes | — |
| 77 | ends the message | ends | ends | ends | ends |
| 78 (X2) | ends | 2 bytes (`s`, `str` land; `c`, `i5` hide the player) | 2 bytes | 2 bytes | 2 bytes |
| 79 | ends | Y2: every value moves the player off screen | same | same | — |
| 80 (Z2) | ends | 2 bytes | 2 bytes | 2 bytes | — |
| 81 | ends | ends | 1 byte (`s` hides the player) | 1 byte (`s` hides) | 1 byte |
| 82 | ends | ends | ends | string (`c:0`, `str:x` land) | string |
| 83–90 | end the message | end | end | end | 83 and 90 end |

"Ends" means the canary is not applied: the id has no case, and the rest of that message is dropped.
"Vanishes" means the fake player is not drawn anywhere on screen after the test packet. For 79 that
happens at every width. 79 is Y2, the two-byte own-player Y
([probe targets](../../protocol/probe-targets-2026-11-18.md)), and the X canary cannot bring a player
back once Y2 has put it off screen. `s:300` and `str:x` are both two bytes, so they fit that width; a
Y canary would be needed to confirm it. The width pattern grows build by build:
2.22 knows only 74–76 here, 2.31 adds 78–80, 4.20r8 adds 81, and 5.24r4 adds 82, which matches 6.03r7.

## 2. Keyboard and chat input

The plan ran on 2.05, 2.22, 2.31, 4.20r8 and 5.24r4. It covered the Tab chat line, plain typing,
300-character lines with and without Tab, a line of `#` codes, Latin-1 bytes, Ctrl+A/C/V with the
chat open, 200 rapid `a` presses, 50 rapid Spaces, Right held across an injected warp, Ctrl+Alt,
Ctrl+Shift and Alt+Shift combos, `/` commands, Ctrl+A to Ctrl+Z, about 70 single keys (letters,
digits, punctuation, editing keys, the keypad, Pause, Print and the lock keys), Alt/Ctrl/Shift+Return
and Tab, the F-keys, `/reconnect`, and Escape last.

### What the 2.x script engine sees (key-logger level)

| Input | `keypressed` code / `keydown` |
|---|---|
| letter keys | upper-case ASCII: f = 70, l = 76, a = 65, e = 69, p = 80 |
| Shift+key | +256: L = 332, M = 333, K = 331, # (Shift+3) = 307 |
| Ctrl+key | +512: Ctrl+C = 579, Ctrl+V = 598 |
| Return, Space | 13, 32 |
| `(` `)` and some punctuation | −1 |
| held Right / s / a / M | `keydown(3)`, `keydown(5)` (and the sword starts), `keydown(6)`, `keydown(7)` |

Each press of M fires `keypressed` and toggles `keydown(7)`. During the 300-character run of
capital L, the player also walked right in half-tile steps. The cause is not settled. 2.22 and 2.31
report the same codes.

### Ctrl+letter emoticons (2.05 and 2.22)

Every Ctrl+letter draws an emoticon locally. The client sends one file check (34) for the image the
first time each one is used in a session, and sends nothing after that:

a `afk_stay`, b `brb_stay`, c `conf`, d `dgrin`, e `eyes`, f `frown`, g `grr`, h `heart`, i `idea`,
j `jpm_stay`, k `kitty`, l `lol`, m `maybe`, n `ncool`, o `ohh`, p `ptongue`, q `qphone_stay`, r `rofl`,
s `smile`, t `tears`, u `umad`, v `vsorry`, w `wink`, x `xx`, y `yummy`, z `zzz_stay`
(file names `emoticon_<name>`, `.png`, or `.mng` for the animated ones).

Ctrl+Alt+letter and Ctrl+Shift+letter trigger the same emoticons. As in E#322, there is no
`PLI_SHOWIMG` and no prop, so other players never see them. 2.31 was in chat-entry mode from that
point on, and 4.20r8 and 5.24r4 sent nothing for any Ctrl+letter.

### Modal windows stop the client's traffic

- **2.05 and 2.22:** Escape opens a "Do you really want to quit Graal?" box. While it is open, the client sends
  nothing: 200 `a` presses produced no packets. The next Space presses OK, and the client exits (the
  proxy sees a connection reset). That is how two runs ended early. It is not a crash.
- **4.20r8:** one of F2, F3, F4, F9 or F10 opens the modal Options window. From then on the client
  sends nothing, including its periodic id 24, until the window closes. The injected warp was queued but
  never acted on.
- **5.24r4:** Escape opens a GUI window, and the client fetches `guiblue_window.png` and
  `guiblue_button.png` for it. The client keeps running.

### Chat text

- **2.31:** a chat line of `#c#n#v(playerrupees)#s(x)…` goes out literally as prop 12, so the
  client expands no codes. A line of `fz` plus six Latin-1 bytes goes out raw (`e4 f6 fc ff a7
  b0`), with no escaping.
- **4.20r8:** Tab opens the chat bar, and the first use fetches `defaulttextedit.png`. Lines go out as prop
  12, and `#` codes are sent literally there too. After the `#` code line, the bar kept focus, and later
  keys made no game traffic.
- **2.22 and 2.05:** Tab does not open a chat line on the control world, and letters go to the game (and
  to the key logger).

### Other input effects

- **Alt+Return** (display-mode toggle) makes 4.20r8 re-check `pics1.png` and `head0.png`, and 5.24r4
  re-check `pics1.png`.
- **5.24r4:** `a` starts the `grab` gani and Space the `sword` gani. Walking into a wall starts `push`.
  The first use of each gani sends C>S 157 with the gani name, next to the 34 check for its `.gani`. 4.20r8 does
  the same for `walk`.
- The `/` commands (`/help`, `/sethead`, `/setbody`, `/setnick`, `/toall`, `/showkills`, `/reconnect`)
  produced no C>S traffic at all on 2.05, 2.22, 4.20r8 or 5.24r4 in this setup. That includes the key logger's
  reports on 2.x, so the input probably did not reach the game there. Treat this as untested, not as
  "ignored".

## Not covered

- 6.03r7 was left out, because it does not draw under the VM's virtual display.
- Keys on the login form: `runwine.sh` fills the form itself.
- 2.31 after its chat line opened: the rest of its key sweep went into the chat line, so its
  Ctrl+letter and single-key results are missing.
- Which F-key opens Options on 4.20r8: they were sent as one group.
