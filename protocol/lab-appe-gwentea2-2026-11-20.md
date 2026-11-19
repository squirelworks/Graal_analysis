# Appendix E lab runs on GwenTea2 (2026-11-20)

Date: 2026-11-19/20. Evidence: **[lab]**. Real clients in the GwenTea2 Debian lab VM, on loopback
only: Wine 10, a gs2emu lab gserver and the `gen5probe` injecting proxy. One probe ran at a time
on an idle VM. Captures and screenshots stay in the lab. Probe rows are appended to
[`probe-results.tsv`](probe-results.tsv).

## Key emote on 2.05 (E#322)

Client: 2.05 rev 2 (`Graal.exe`, token `GNW03081`). Plan: `e322-205.plan`, run `fz-e322-205-g`.

| Input | Client to server |
| --- | --- |
| Ctrl+A | one `PLI_UPDATEFILE`-style file check (34) for `emoticon_afk_stay.mng`, once per session; three more presses send nothing |
| Ctrl+S, Ctrl+D | only their own file checks, `emoticon_smile.png` and `emoticon_dgrin.png` |
| plain a, Alt+A, Shift+A, F1–F12 | nothing |

Ctrl+A draws the AFK thought bubble locally. The client sends no `PLI_SHOWIMG` (24) and no
props, so the server has nothing to relay to other players. A second client was not run, because
nothing relayable leaves the first.

## GS2 class path on 4.20r8 (E#202 leftover)

Client: 4.20r8 (`G3D20126`) under Wine. Plan: `gs2deliver420.plan`, run `fz-gd420-g`. The body is
a Seihai-compiled `keylog.gs2` whose `onCreated` timer chats `D0` within 0.1 s if it runs.

- Ten frames were sent:
  - 197 as text, i5 weapon, i5 class, empty, and name only;
  - 140 with a weapon body with no cache, with `cache=1`, after a 197 with the same key, with
    the header length short by 2, and with an empty body.
- No case ran the script. After any 197 the client sent no request at all, and it stayed alive
  throughout.
- So 4.20r8 does not honour the 6.x class path (a 197 descriptor, then the body in 140) as sent
  here. NPC bytecode in 131 behind 100 still runs on 4.20r8
  ([script-fuzz-2026-11-19.md](script-fuzz-2026-11-19.md)).

## Shot last byte on 2.22 (E#312)

Client: 2.22 (`GNW03014`). Plan: `shotbyte222.plan`, sweeping the last byte from 0x20 to 0x7e,
with owners 3 and 999.

- On open ground, with nothing in the path, every byte from 0x20 to 0x7e flies through the player.
  No hearts are lost and no props are sent.
- Bytes 0x23 and up burst in a bomb-style blast only when the shot hits something (a block NPC or a
  wall). The client fetches `bomb.wav` once. 0x20 fetches `arrow.wav`.
- So the earlier lab's "0x23 and up hurt" is not reproduced with an unknown or absent shooter. A
  run with a real other player as the shooter, as in that lab, is queued.

## NPC prop widths on 2.22 and 2.31

`PLO_NPCPROPS` ids 48–52 and 74–90 were each sent as `c:0`, `s:300`, `str:x` and `i5`, followed
by an X canary on NPC 300.

- 2.22: in all 88 cases the canary is not applied, so each of these ids ends the message.
- 2.31: the same, with these exceptions:
  - 75 and 76 read two bytes. The canary lands after `s:` and after a one-character string; `c`
    and `i5` misread and the NPC vanishes.
  - 77: the canary never lands. `c` and `i5` show no change, `s` makes the NPC vanish, and a
    string moves it off its row.

## v7 Worlds 614 at the date boundary (E#615)

A Windows 10 VM with no network adapter, and the guest clock set before each standalone start.

| Guest date | Runs | Result |
| --- | --- | --- |
| 2024-10-12 | 2 | start-up and environment init, failed connector attempts (no network), then OpenGL initialised; window stays up |
| 2024-10-13 | 2 (12:00 and 00:30) | start-up and environment init only; OpenGL never initialises; window stays up, black |

Neither date quits within 2–4 minutes, and no quit line or reason text reaches the player log. So
past the boundary the gate shows up, standalone, as start-up stalling before graphics init. It does
not show as `QuitInstant` or a reason string. Whether a quit would follow with a server present is
not known.

## Arrows and fireballs at a wall on 2.05 (E#313)

Client: 2.05 rev 2. Shots were fired down at a wall row and shot 8 frames apart by 0.1 s.

- Type 0 (arrow, 0x21) and type 1 (fireball, 0x22) cross the wall row and keep going.
- Types 2 to 4 (0x23 to 0x25) burst on the wall.
- In the open column, none of them hurt the player either.

## Walking into a wall on 2.22 (E#304)

Walking up into a wall row at y = 25, from y = 30 and 30.5 and from x = 30 and 30.5, the player
always stops at y = 25.0 (wire half-tile 50), and then the push gani starts. Every y on the wire
was a whole half-tile value. No position between half tiles was seen, so truncation against
rounding is still untested.

## Link arrival offsets on 2.22 (E#601)

A link with arrival `playerx playery+10`, entered walking up at y ≈ 20, sent the player to
(30, 30). A control link with a plain `30 40` arrival sent the player to (30, 40). So the client
evaluates the offset.

## Walking speed on 2.05 (E#302)

On foot the player moves 1 tile per 0.1 s. In deep water (the swim gani) the speed is the same,
so swimming uses factor 1.0, not 0.4 or 0.8. Riding, shield and carrying were not tested.

## Start-up file checks on 2.22 (E#25)

- A near-empty folder (root files and languages only) requests 18 files with id 23.
- A full folder update-checks 13 files with id 34.
- `idle.gani`, `plisticononline.png`, `plisticonaway.png`, `plisticondnd.png` and `head0.png` are
  requested when missing but never update-checked when present. `block.png` is a level file and
  appears in both runs.

## Gmap entry on 2.22 (E#314, E#13)

- Entered from a plain level by a link, a 2 x 2 gmap drew its neighbour cells correctly, with no
  overwrite. 2.22 sends modtime 0 in `PLI_LEVELWARP`-time level requests (35).
- After death (power 0, then a key), the respawn request went to the gmap entry point, not the
  start level. So entering a gmap from outside saves the point.
- Death on each side of a seam is queued.
- The first 2.17.1 run was invalid: a shared cache and identical level times made the server
  answer every 35 with an empty board. 2.17.1 sent the current level's modtime for every
  neighbour. It is queued again with distinct times.

## GS1 condition truth on 2.05, 2.17.1, 2.22 and 2.31 (E#200)

The same scene ran on all four builds.

| Condition | Result on all four |
| --- | --- |
| `(1+0)`, `(0.5+0)`, `(-0.5)`, `(0-1)`, `created` | true |
| bare `1`, bare `0.5`, `(0+0)` | false |
| `true`; `false` | true; false |
| `!(0+0)`, `!0`, `(1+0)&&(1+0)`, `(0+0)\|\|(1+0)` | true |
| `playerx==playerx`, `this.a==1` (after setting 1), `strequals(#a,#a)` | true |
| `playerx!=playerx` | false |

- 2.05 only: every comparison of two constants folds to false (`1==1`, `1!=0`, `1<2`, `2>1`,
  `1=1`, `(1+0)==1`, `1==1.00001`, `0.1+0.2==0.3`).
- 2.17.1, 2.22 and 2.31 evaluate those comparisons, and compare with a tolerance (`1==1.00001` and
  `0.1+0.2==0.3` are true).
- Loops: `while(1)` runs 0 times everywhere. `while(1==1)` runs 0 times on 2.05 and normally
  from 2.17.1. `while((1+0))` runs on all four.

## GS1 member writes (E#204)

Same four builds.

- `npcs[k].x = 44` and `npcs[k].y = 24` read back and move the NPC on screen.
- `players[0].x = 33` moves the player (`playerx` then reads 33).
- A write to `npcs[99].x` reads back 0.
- `npcs[k].zz`, `players[0].zz` and `arrows[0].dy` read 0, and so does `players[0].power`.
- `npcscount` is 3 and `playerscount` 1.
- The only build difference: `npcs[k].dir = 1` reads back 2 on 2.05 (the write does not stick)
  and 1 on 2.17.1, 2.22 and 2.31.

## GS2 top-level pass (E#212)

4.20r8 and 5.12 ran Seihai-compiled bytecode delivered in 131 behind 100.

- A script with a top level: `onCreated` sees the top-level counter at 1, and each later
  `onTimeout` sees it one higher. So the top level runs again before every event.
- Its function-only twin, with a leading jump to the end, never runs a top level.
- The "handler at instruction 0" fixture was not built, and 6.03r7 was not run.

## `format` and `indexof` (E#210)

4.20r8 and 5.12 gave identical results.

- `%d` floors: 3.7 → 3, −3.7 → −4, 2.5 → 2.
- `%d` of `"abc"` → −1, and `%i` of 3.7 → 3.
- `%x` of 255 → `ff`, and `"%3d|"` of 5 → `"  5|"`.
- Position and index lookups are case-sensitive: `"abcB".pos("B")` = 3 and `.pos("b")` = 1;
  `{"a","B","c"}.index("b")` = −1 and `.index("B")` = 1.
- Particles were not tested.

## Latin-1 text (E#213)

On 4.20r8 under Wine (Western default code page), `showtext` of `"Fran" + char(231) + "ais " +
char(233, 252, 241)` drew "Français éüñ". The string length is 12 and byte 231 survives. 5.00r7
and a 6.x build were not checked on screen.

## 4.04r2 3D connect request (E#501)

The client's UDP connect request (74 bytes) was decoded from a native Linux 4.04r2 (`G3D19026`)
Graal3D lab capture of 2026-11-19. It carries net class group 0 and class CRC `0xFFFFFFFF`, the
static table value, with nothing computed. Windows 4.04r2 page-faults under Wine at the 3D start,
so this is the Linux build of the same version.

## Early frame driver (E#300, partial)

4th Graal alpha, 5th Graal and 5th Graal alpha were run under Wine.

- At run time the frame driver is an idle busy loop of `PeekMessage`, `timeGetTime` and
  `QueryPerformanceCounter`, at about 10,000 polls a second. This is the DelphiX idle-timer
  pattern, so an idle handler is installed at run time.
- Two ordinary window timers run as well, at 1000 ms and 500 ms.
- After Start the game goes full-screen DirectDraw, which draws nothing under the virtual display,
  so the 50 ms cadence itself was not measured.

## Not run this round

- E#310: needs two 2.05 clients, and the harness starts one.
- E#319 and E#604: need the offline editor-and-play path, driven by GUI clicks.
- E#201 and E#203: their outlook is a static read, not a lab run.
- E#23 and E#9: need a 6.x script window, and 6.x does not draw in this VM.
