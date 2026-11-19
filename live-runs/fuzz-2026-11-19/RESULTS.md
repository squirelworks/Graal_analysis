# Protocol fuzzing, 2026-11-19

Real clients in the Debian lab VM, each in a private network namespace with only a loopback
interface. A lab gserver sits behind the `gen5probe` proxy, which injects server packets. Clients:
6.03r7 (native Linux), plus 4.20r8, 5.24r4, 2.22 and 2.31 under Wine. Packet specs use the probe
syntax (`c:N` GCHAR, `s:N` GSHORT, `i3`/`i5`, `str:` length-prefixed, `t:` raw, `hex:`).
Each test sends a canary after the field under test, so a wrong-width read shows up as a lost
canary. Rows are in `fuzz-results.tsv`, with the same columns as Graal_analysis
`protocol/probe-results.tsv`. Plans are in `plans/`. Raw logs and screenshots stay in the VM.

Lab note: the Wine runs moved to a private copy of the Wine lab tree with its own namespace.
`runwine.sh` kills every lab process in its namespace when it starts, so two threads that
share one tree end each other's runs. That happened twice today, with the GR v1.05 thread. The
2.22/2.31 server list now gets a click retry, because under load the list arrives after the click.
On this VM, `run603.sh`'s black-screen check always fails (no PIL in the system Python), so each
run restarts four times; use `NOBLACK=0`.

## 1. Baddy props 11 and up (PLO_BADDYPROPS, 2)

**Still mode (6.03r7).** The client runs the AI for baddies that `PLO_BADDYPROPS` creates, and it
reports their changes back as `PLI_BADDYPROPS` (C>S 15). That makes C>S 15 an observer that needs
no screenshot. Mode 0–4 and 8: the baddy walks, and its x/y/ani/dir are reported. Mode 5: the ani
counts down 55→0 (dying), then the reports stop. Mode 6: animates in place (ani only). Mode 7:
jumps in place (ani and one y). **Modes 9 and 10: no reports at all.**

**Canary.** The test creates a fresh baddy in mode 10, so it is silent, then sends
`[tested prop][mode 0]`. If mode 0 lands, the client starts reporting that baddy. Controls (mode 0
alone, string prop 10 + mode, 1-byte prop 7 + mode) landed on all three clients.

| Client | Props 11–30, 1 byte (`c:0`) | Props 11–30, string (`str:x`) |
|---|---|---|
| 6.03r7 | canary lost for every prop | canary lost for every prop |
| 4.20r8 | canary lost for every prop | canary lost for every prop |
| 2.22 | canary lost for every prop | canary lost for every prop |

None of the three clients reads a baddy prop above 10. An unknown id ends the parse, and the rest
of that baddy message is dropped, as with NPC props 48–52. No crashes. 4.20r8 reports
ani/dir within 1.6 s but no x/y in that window; 6.03r7 reports x/y as well.

## 2. PLO_SETACTIVELEVEL (156) on 2.22 and 2.31

The test sent 156 with: the current level (`gs1ctl.nw`), a neighbour (`labroom.nw`), the gmap
name (`lab.gmap`), an empty name, and an unknown name (`nosuchlevel.nw`). After each one, a 3x3
`PLO_BOARDMODIFY` (7) at a new spot and a bombs canary followed.

- 2.22 and 2.31 behave the same. No 156 changes the screen. The level NPC's script keeps running,
  and every later board block and bombs prop lands. No client crashed.
- The only reply: **156 with the gmap name makes both clients ask for the gmap file**
  (C>S 34, `PLI_UPDATEFILE` `lab.gmap`). The level names, empty and unknown, get no reply.

## 3. PLO_LOADGANI (195) DEFAULT* lines on 6.03r7 and 4.20r8

Each 195 named a unique file (`DEFAULTHEAD`, `DEFAULTBODY`, `DEFAULTATTR1`–`3`, `DEFAULTSHIELD`,
`DEFAULTSWORD`, `DEFAULTHORSE`, `DEFAULTPARAM1`, a `SPRITE` line, and `DEFAULTHEAD` with no
value). The player was then set to that gani (`idle`, `walk` or `sit`).

- Neither client ever asked for any of the named files.
- The idle shots on 6.03r7 are pixel-identical to the plain idle shot. Walk and sit draw
  normally, with the player's own head and body. 4.20r8 looks the same.
- In this test, DEFAULT* lines in 195 change nothing for the player's own character. Not
  tested: an NPC with `showcharacter` and no head of its own, which is the case where a DEFAULT*
  value would be used.

## 4. NPC prop widths on the Windows clients

The NPC under test is 300, the level's block NPC at (30,27). Before each test it was reset to
x=30, y=27. The test packet held the prop at four widths (`c:0`, `s:300`, `str:x`, `i5`), then
X=35 as the canary. Each shot was compared with x=30 and x=35 reference shots.

| Prop | 4.20r8 | 5.24r4 | (6.03r7, earlier round) |
|---|---|---|---|
| 48–52 | dropped at every width | dropped at every width | dropped |
| 74 CLASS | dropped at every width | dropped at every width | script stops |
| 75 X2 | 2 bytes; 1 byte / i5 sends the NPC out of view | same | 2 bytes |
| 76 Y2 | inconclusive (bad test value) | 2 bytes (`s:864` lands); others out of view | 2 bytes |
| 77 Z2 | 2 bytes (NPC drawn raised at x=35) | 2 bytes (drawn raised) | 2 bytes |
| 78–90 | dropped at every width | dropped at every width | dropped |

"Dropped" means the rest of the NPC message is lost. On the 4.x/5.x clients, 74 does not stop
the NPC: the message is cut short. No crashes. 2.22 / 2.31: pending (paused for VM load).
The other-player props 77–90 on the Windows clients are not done yet.

## 5–8 (not run: VM load)

Sections 4 (2.22/2.31 columns) and 5–8 are planned but did not run on 2026-11-19. I set up a queue
(`plans/fzq.sh`, `plans/queue.txt`) of 11 runs that started one at a time, each only when the
VM's 1-minute load was under 4 and no other thread's `runwine.sh`/`run603.sh` was live. It
waited 110 minutes, from 19:34 to 21:24 VM time, and no slot came up. The load stayed between
9 and 16 on the VM's 2 CPUs. Other threads' probe runs and clients started directly (2.22,
Graal3D, Torque, 4.x/5.x Graal.exe, a gserver LTO build) kept it there. The 2.31 keysweep was
also waiting for its own slot (load under 3) the whole time.

Queued, ready to run as is (`sh fzq.sh` with `DEADLINE` set to a Unix time):

- (a) NPC prop widths 48–52/74–90 on 2.22 and 2.31 (`npcwidth-win3.plan`). NPC 300 is the
  block NPC in `gs1ctl.nw` on the 2.x world too.
- (b) Last byte of PLO_ARROWADD (19), 0x20..0x7e, on 2.22 (`shotbyte222.plan`).
- (c) 4.20r8: 197 descriptors (text, i5, class, empty, name only), then 140 with a Seihai-compiled
  `keylog.gs2` body (no-cache, cache=1, 197 after 140 with the same key, header length −2, empty
  body). The C>S per window is the observer (`gs2deliver420.plan`, c2swin prefix G).
- (d) Key/chat fuzz (`keychat.plan`) on 2.22, 4.20r8, 5.24r4, 6.03r7 (DISP 187), 2.31 and 2.05.
  E#322 on 2.05 (`e322-205.plan`): plain a, Ctrl+A once and three times, Ctrl+S/D, Alt/Shift+A,
  F1–F12, C>S per window.

Not covered by the plans even once they run:
- Keys on the login form: `runwine.sh` fills the form itself.
- E#322 second-client visibility: `runwine.sh` starts one client. If the 2.05 C>S shows a prop
  change on Ctrl+A, the relay to other players still has to be checked with a second client.
