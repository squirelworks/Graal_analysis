# Open-issue lab run: #442, #443, #254, #245, #398 and #243 stage 0, 2026-11-14

One lab session on six open issues. Every run was offline (no network at all) or on lab
servers at the loopback address and lab ports, inside a loopback-only network namespace.
Several items are partial; each section says what was and was not run. **[lab]**

Run, log and fixture names below are the private lab names (`runs/…`, `run/proxy-….log`,
`gani/…`); the logs, screenshots and frame dumps are owner-held and not in this repo.

## Summary

- **#442:** a bare number in a loop condition is **false** in every build (1.33, 1.41r1,
  2.05r2, 2.17.1, 2.22, 2.31): `while(1)` runs 0 times (1.33 too, via an `if`-test readout).
  `1==1` in a loop is false in 1.41r1 and 2.05r2. **`##`** in 2.05r2 and 2.17.1 is a one-pass
  escape for `#`; in 1.33 it gives nothing. **`#F #S #D #I`** arrive in 2.17.1 (`#F` level
  file, `#S` selected weapon, `#D` empty, `#I` zero-based list pick); **`#R`** from 2.22
  (picks an argument); **`#P6–#P9`** work from 2.17.1 (empty in 2.05r2); **`#C6/#C7`** are
  empty everywhere. In 1.33, `#v()` can't read `this.` variables.
- **#443:** GS1 `timeout` **rounds down** to whole 50 ms steps in 1.33, 1.39, 1.41r1, 2.05r2,
  2.17.1, 2.22, 2.31 and 5.00r7 (online). Under 0.05 it never fires. 1.33 floors a float, so
  0.15 is 2 steps there. 6.03r7 is not testable on this server (no GS1 for 6.x). Walk GANI on
  2.22/2.31: 8 frames, **one per game step**, 8 px per step. Sword spark not identified;
  2.05 drop control and the 2-player sword edge not run; 1.21 runs and loads a baddy scene,
  but the item roll was not seen.
- **#254:** 6.03r7 with 108 sub 1 = 0/1/5/30/300: **no change** in ping answers (19/19,
  value echoed), keepalive (5.1 s), or connection over 10 min.
- **#245:** 2.22 starts with 9 files (exe, 3 DLLs, `arrays.dat`, `arrays2.dat/.sig`,
  `graal.sig`, `pics1.png`). File checks go out in its second frame with the first props
  line: near-empty = id 23 for `idle.gani` + 3 player-list icons; full = id 34 for 4 other
  icons + id 23 for 2 files. This server answered none, so later checks never came; a rerun
  on a server that answers is needed for the full set.
- **#398:** partial. 5.00r7 actor with a Linux 6.03r7 observer: walk 4/4 and sword 3/3
  relayed; the place-dependent actions failed (blind positioning). 4.20r8, 5.12, 6.03r7
  (Windows) and 6.113 not run.
- **#243:** stage-0 run done (none existed): 3.04 Linux sandboxed, log mode 6;
  `console.log`, `prefs.cs`, `config.cs` kept privately (no hosts in them; one local path
  to cut). The server list showed one tab only.

Related notes: [GS1 per client build](../../npc-library/gs1-per-build-2026-11-13.md),
[update cadence of the 3.x, 4.x and 6.x clients](../../client-internals/update-cadence-3x-6x.md),
[combat, baddy and lava rules](../../client-internals/combat-baddy-tile-by-version.md),
[client test harness, 2026-11-13](../client-harness-2026-11-13/README.md).

---

## 1. #442 GS1 per version

### Setup (all of item 1)

- Harness: the offline GS1 harness from the 2026-11-13 GS1-per-version lab. Each run is the
  unchanged original exe under Wine 10.0 in bubblewrap (`--unshare-all`: no network at all,
  private PID/IPC), Xvfb 1024x768 inside the sandbox. The exe hash is checked before and
  after; every run listed reported a clean supervisor exit, cleanup complete and the exe
  unchanged.
- Fixtures: owned synthetic GLEVNW01 levels on a plain-grass board (`lab_ga_while.nw`,
  `lab_ga_hash.nw`, `lab_ga_pop.nw`, and per-case splits). Each probe is one NPC that shows
  `LABEL:value` with `message`.
- Entry routes (same as the 11-13 lab): 2.17.1 / 2.22 = level as a command-line argument,
  then editor Play; 2.31 = editor Open dialog, then Play; 2.05r2 = Training, then F5 Load
  level (2.31 package as donor, 2.05r2 files on top); 1.41r1 = Single player, then F5 Load
  level.
- Client builds: 1.33, 1.41r1, 2.05r2, 2.17.1, 2.22 and 2.31 Windows clients. No server:
  these are offline runs, so there is no server commit or token.

### 1a. Is a bare number true in a loop condition?

Each case: `this.n=0; <loop head>{this.n=this.n+1; if(this.n>=3){break;}} message Wn:#v(this.n);`
(W4 has no break; it is the control). Reading: `3` = the body ran (condition true), `0` =
it never ran (condition false).

| label | loop head | 1.41r1 | 2.05r2 | 2.17.1 | 2.22 | 2.31 |
|---|---|---|---|---|---|---|
| W1 | `while(1)` | 0 | 0 | 0 | 0 | 0 |
| W2 | `while(0.5)` | 0 | 0 | 0 | 0 | 0 |
| W3 | `while((1+0))` | 3 | 3 | 3 | 3 | 3 |
| W4 | `while(this.n<3)` (control, no break) | 3 | 3 | 3 | 3 | 3 |
| W5 | `while(true)` | 3 | 3 | 3 | 3 | 3 |
| W6 | `while(0)` | 0 | 0 | 0 | 0 | 0 |
| W7 | `while((0+0))` | 0 | 0 | 0 | 0 | 0 |
| W8 | `while(1==1)` | **0** | **0** | 3 | 3 | 3 |
| W9 | `for(this.k=0;1;this.k=this.k+1)` | 0 | 0 | 0 | 0 | 0 |
| WA | `for(this.k=0;this.k<3;...)` (control) | 3 | 3 | 3 | 3 | 3 |

**Answer: no.** In every build tested (1.33 below too), a bare number in a `while` or `for`
condition is false, exactly as in `if` (it goes through the flag-name path). `while(1)` and
`for(;1;)` run 0 times; wrap it, `while((1+0))`, or use `while(true)`. `true` is true in
every build. `1==1` in a loop is false in 1.41r1 and 2.05r2 (the constant-folding defect)
and true from 2.17.1.

2.05r2: the full ten-NPC level hangs the client while loading (the Load level dialog never
closes, in `205r2-while`), so each risky case ran in its own level with an `alive`
companion NPC (`205r2-wsafe` = W4/W6/W7/WA, `205r2-w{W2,W3,W5,W8,W9}-b`). All of those load
and show the values above, W1 included (`205r2-wW1-b`). So the hang comes from the level as
a whole, not from any one loop head. (An earlier `205r2-wW1` run was cut off by a lab reset
before it loaded the level; ignore it.)

Runs: `runs/{141r1,2171,222,231}-while` (2.17.1 reading from `2171-while2`: in
`2171-while` the Game-windows help box covered two columns).

### 1b. `##` in the 2.17.1 engine (and 1.33)

2.17.1, level `lab_ga_hash.nw`, run `2171-hash`. Each NPC shows `message Hn:[text];`.

| label | text | 2.17.1 shows |
|---|---|---|
| H1 | `A##B` | `A#B` |
| H2 | `A###B` | `A##B` |
| H3 | `A####B` | `A##B` |
| H4 | `A##v(1)B` | `A#v(1)B` |
| H5 | `A###v(1)B` | `A#1B` |
| H6 | `A##` | `A#` |
| H7 | `##` | `#` |
| H8 | `A##K(65)B` | `A#K(65)B` |
| H9 | `A#v(1)##B` | `A1#B` |
| HS | `setstring this.s,A##B;` then `#s(this.s)` | `A#B` |
| HT | `setstring this.s,A#B;` then `#s(this.s)` | `A#B` |
| HC | `setplayerprop #c,HC:[A##B];` | not readable (chat hidden under another label) |

**Answer:** in 2.17.1, `##` is an escape for one literal `#`, scanned left to right in one
pass: `####` gives `##`, and the `#` it produces does not start a new code (`##v(1)` gives
`#v(1)`). `###v(1)` is `#` + `#v(1)`, so it gives `#1`. An unknown code after a single `#`
stays as written (`#B` stays `#B`, so `A###B` gives `A##B`). `setstring` stores the text
after the same pass (HS).

2.05r2 gives the same results for H1–H8 (runs `205r2-sh0`, `205r2-sh1`: levels of four
probes each, since its loader hangs on the full 12-probe level, `205r2-hash`,
`205r2-hash-b`). The level with H9/HS/HT/HC also hung; one probe per level they load and
give the 2.17.1 results: H9 `A1#B`, HS `A#B`, HT `A#B` (runs `205r2-sH9`, `-sHS`, `-sHT`;
HC's chat was not on screen in `205r2-sHC`). So **2.05r2 already has the 2.17.1 `##`
rule.**

**1.33 is different** (run `133-msg3`, level `lab_ga133_msg.graal`, GR-V1.03 binary scene):

| text | 1.33 shows |
|---|---|
| `A##B` | `AB` (`##` gives nothing) |
| `A#?B` | `A?B` |
| `#v(0.5)` / `#v(2+3)` | `0.5` / `5` |
| `#e(1,2,ABCD)` | `e(1,2,ABCD)` (no `#e` in 1.33: the `#` is dropped and the rest stays) |
| `#K(65)` | `K(65)` (no `#K` in 1.33) |
| `A#bB` / `A#mB` | `AbB` / `AmB` (unknown letter: `#` dropped, letter kept) |
| `A#aB` | `Agu…B` (a name; the end is hidden under the next label) |
| `A#LB` | `Alab_ga133_msg.graalB` (`#L` = level file name) |
| `A#cB` | `AB` (`#c` = player chat, empty) |
| `A#1B` | `Asword1.gifB` (`#1` = sword image) |

So in 1.33 an unknown code drops only the `#`, and `##` is a code that gives an empty
string, not an escape.

1.33 lab notes: the F5 dialog is "Level options" and resolves a bare name against
`levels\`, so the scenes are loaded by full path. 1.33 shows no NPC when its image is a
truecolour PNG (it reads 16/256-colour PNGs only), so the 1.33 scenes use the GIF marker.
The first two 1.33 runs (`133-msg`, `133-msg2`) had the PNG marker and loaded nothing
visible; ignore them.

### 1c. `#F #S #D #I #R #P6–#P9 #C6–#C7` in a populated context

Level `lab_ga_pop.nw` (1.33: `lab_ga133_pop.graal`). Setup NPCs on `created`:
`setplayerprop #P6..#P9` = six/seven/eight/nine, `#C6`=blue, `#C7`=red, `#P1`=one,
`#n`=LabNick; `setstring lab,xx,yy,zz`; `setstring this.l,aa,bb,cc` (in the reading NPC's
own scope it is unset, see I2); `toweapons LabWand` (it shows in the D slot); a
`showcharacter` NPC with `setcharprop #P6/#C6/#n/#P1`. Each probe NPC re-shows
`message L:[codes];` every second (`if(created||timeout)…timeout=1`), so the screenshot is
from a running script after setup. Runs: `133-pop`, `141r1-pop`, `205r2-pop`, `2171-pop`,
`222-pop`, `231-pop`. Offline, single player (so `#a`/`#n` are the offline defaults).

| probe | text | 1.33 | 1.41r1 | 2.05r2 | 2.17.1 | 2.22 | 2.31 |
|---|---|---|---|---|---|---|---|
| F | `#F` | `F` | `F` | `F` | `lab_ga_pop.nw` | `lab_ga_pop.nw` | `lab_ga_pop.nw` |
| S | `#S` | `S` | `S` | `S` | `LabWand` | `LabWand` | `LabWand` |
| D | `#D` | `D` | `D` | `D` | empty | empty | empty |
| I1 | `#I(lab,1)` | `I(lab,1)` | `I(lab,1)` | `I(lab,1)` | `yy` | `yy` | `yy` |
| I2 | `#I(this.l,1)` | — | `I(this.l,1)` | `I(this.l,1)` | `bb` | empty | empty |
| R1 | `#R(lab)` | `R(lab)` | `R(lab)` | `R(lab)` | `#R(lab)` (kept as written) | `lab` | `lab` |
| R2 | `#R(x,y,z)` | — | `R(x,y,z)` | `R(x,y,z)` | `#R(x,y,z)` (kept) | `x` | `x` |
| P6 | `#P6\|#P7\|#P8\|#P9` | `P6\|P7\|P8\|P9` | `P6\|P7\|P8\|P9` | `\|\|\|` (all empty) | `six\|seven\|eight\|nine` | same | same |
| PI | `#P6(0)\|#P9(0)` | — | `P6(0)\|P9(0)` | `\|` | `six\|nine` | `six\|nine` | `six\|nine` |
| C6 | `#C6\|#C7` | `\|` | `\|` | `\|` | `\|` | `\|` | `\|` |
| CI | `#C6(0)\|#C7(0)` | — | `\|` | `\|` | `\|` | `\|` | `\|` |
| PX | `#P(1)\|#P(0,1)` | — | `P(1)\|P(0,1)` | `1)\|0,1)` | `one\|` | `one\|` | `one\|` |
| P1 | `#P1\|#P5` | `P1\|P5` | `P1\|P5` | `one\|` | `one\|` | `one\|` | `one\|` |
| W | `#w\|#W` | `LabWand\|W` | `LabWand\|W` | `LabWand\|` | `LabWand\|` | `LabWand\|` | `LabWand\|` |
| N | `#n\|#a` | `\|guest` | `\|guest` | `\|` | `\|` | `\|` | `\|` |
| C0 | `#C0\|#C5` | `orange\|black` | `orange\|black` | `orange\|black` | `orange\|` | `orange\|` | `orange\|` |
| HH | `A##B` | `AB` | | | | | |

Readings:
- `#F #S #I` arrive in 2.17.1. `#F` is the level file name and `#S` is the selected
  weapon's name (same as `#w`). `#D` exists from 2.17.1 and is empty here.
- `#I(list,i)` is a zero-based pick from a string list from 2.17.1. With a `this.` list,
  2.17.1 returns the item (`bb`); 2.22 and 2.31 return nothing.
- `#R` is not in 2.17.1 (it stays as written, `#` included, the 2.17 rule for unknown
  codes). From 2.22 it picks one argument (`x` of `x,y,z` in this one sample; `lab` for one
  argument).
- `#P6–#P9` hold values from 2.17.1, and `#P6(0)` (an index argument) reads the same value.
  In 2.05r2 they exist but read empty even after `setplayerprop`, while `#P1` works; 2.05r2
  also takes `#P(` as a code (PX shows `1)|0,1)`).
- `#C6` and `#C7` are empty in every build, even after `setplayerprop #C6,blue`. `#C5` is
  `black` in 1.x and 2.05r2 and empty from 2.17.1.
- `#n` stays empty in every build after `setplayerprop #n,LabNick` offline. `#a` is `guest`
  in 1.33 and 1.41r1 and empty from 2.05r2.
- Unknown codes: 1.33, 1.41r1 and 2.05r2 drop the `#` and keep the text; 2.17.1 and later
  keep `#` and text.

### 1d. 1.33 loops (`.graal` scene)

1.33 has no `break`, so its loops end on their own condition. Runs: `133-truth`,
`133-truthb`, `133-while`, `133-w{1,2,3,5}`.

| case | 1.33 |
|---|---|
| `if(0.5)`, `if(1)`, `if((0.5+0))`, `if((0+0))` | false, false, **false**, false |
| `if(created)`, `if(1==1)`, `if(1<2)`, `if((1+0)==1)`, `if(playerx==playerx)`, `if(this.a==1)` | true |
| `if(playerx!=playerx)` | false |
| `if(true)` | **false** (`true` is just an unset flag in 1.33) |
| `#v(1==1)` | `0` (a comparison has no value inside `#v`) |
| `while(1)`, `while(0.5)`, `while((1+0))`, `while(true)` (each alone, no break) | **0**: the body never ran and the client did not hang |
| `while(0)`, `while((0+0))` | 0 |
| `while(this.n<3)` and `for(this.k=0;this.k<3;…)` (controls) | **0** as well |

Those zeros are a readout artefact: **in 1.33 `#v()` can't read `this.` variables**
(`this.n=5; message #v(this.n)` shows `0`, run `133-loopctl`). Read back with `if` tests
and a built-in variable instead (run `133-loopctl2`, level `lab_ga133_loopctl2.graal`):

| case | 1.33 |
|---|---|
| `this.n=5;` then `if(this.n==5)` | five (assignment works) |
| `while(this.n<3){this.n=this.n+1;}` | three |
| `for(this.k=0;this.k<3;this.k=this.k+1){this.n=this.n+1;}` | three |
| `playerrupees=0; while(playerrupees<3){playerrupees=playerrupees+1;}` then `#v(playerrupees)` | 3 |
| `playerrupees=7;` then `#v(playerrupees)` | 7 |
| `while(this.n<3&&1){…}` | **zero** (the body never ran) |
| `while(this.n<3&&0.5){…}` | zero |
| `while(this.n<3&&true){…}` | zero |

**Answer for 1.33: no** as well. Loops work in 1.33, but a bare number in a condition is
false (`&&1` never lets the body run), and `while(1)` alone neither runs nor hangs. `true`
is not a keyword in 1.33 (it is an unset flag).

---

## 2. #443 Gameplay rules: timing and live checks

### 2a. GS1 `timeout` sweep, offline engines

Level `lab_ga_timeout.nw` (1.x: `lab_ga1x_timeout.graal`). Eleven NPCs, each one
`if(created){this.n=0;timeout=T;} if(timeout){this.n=this.n+1; message Ti:#v(this.n); timeout=T;}`,
with T = 0.01, 0.02, 0.05, 0.07, 0.08, 0.1, 0.12, 0.13, 0.15, 0.5, 1 (T0…T10). Two
screenshots, taken about 10–14 s apart (the harness timestamps each one); "fires" is the
count difference between them. The game step under Wine in this lab is slower than 50 ms
(15–18 steps/s), so the reading is the ratio between rows, not the absolute rate: it shows
how many game steps each timeout takes.

Rounding rule, for T between whole steps: round **down** makes 0.07 and 0.08 one step and
0.12 and 0.13 two steps; **nearest** makes 0.08 two steps and 0.13 three steps; **up** makes
0.07 two steps and 0.12 three steps.

| T | steps if rounded down | 1.39 (Δt 10.54 s) | 1.41r1 (Δt 11.95 s) | 2.22 (Δt 10.59 s) | 2.17.1 (Δt 11.12 s) | 2.31 (Δt 15.14 s) |
|---|---|---|---|---|---|---|
| 0.01 | 0 | never fires | never fires | never fires | never fires | never fires |
| 0.02 | 0 | never fires | never fires | never fires | never fires | never fires |
| 0.05 | 1 | 162 | 187 | 194 | 192 | 215 |
| 0.07 | 1 | 162 | 187 | 194 | 192 | 215 |
| 0.08 | 1 | 162 | 187 | 194 | 192 | 215 |
| 0.1 | 2 | 81 | 93 | 97 | 96 | 107 |
| 0.12 | 2 | 81 | 93 | 97 | 96 | 107 |
| 0.13 | 2 | 81 | 93 | 97 | 96 | 107 |
| 0.15 | 3 | 54 | 62 | 65 | 64 | 72 |
| 0.5 | 10 | 16 | 19 | 20 | 19 | 21 |
| 1 | 20 | 8 | 9 | 10 | 10 | 10 |

**1.39, 1.41r1, 2.17.1, 2.22 and 2.31 all round down:** a timeout lasts `floor(T / 0.05)`
game steps, and 0 steps (T < 0.05) means the timer never fires. This is the same rule as
3.x/4.x in the cadence lab (#37), so Seihai's round-up to one step is wrong for these
engines. Runs: `139-timeout`, `141r1-timeout`, `2171-timeout`, `222-timeout`,
`231-timeout-b` (the first 2.31 run, `231-timeout`, never opened the level: the editor Open
dialog did not come up in time).

**2.05r2:** its Load level dialog sometimes never returns (the game stops; seen with the
full 11-timer level twice, with Enter instead of a click too, and once with a two-NPC level
that loads fine elsewhere), so it was measured with small levels, each next to a 0.1
reference timer (runs `205r2-stB`, `-st05`, `-st08`, `-st02`, `-st15`):
- 0.05: 111 fires vs 55 for the 0.1 reference (one step); 0.08: 104 vs 52 (**one step**).
- 0.1 / 0.12 / 0.13 in one level: 42/42/42, then 96/96/96 (all two steps).
- 0.15: 33 vs 50 (three steps). 0.02: never fires.
- 0.07's level hung on load (`205r2-st07`); 0.08 already settles the rule.

So **2.05r2 rounds down too.**

**1.33** (`.graal` scenes): `#v()` can't read `this.` variables there, so each 1.33 scene
has three NPCs that count in the built-in `playerrupees`, `playerdarts` and `playerbombs`,
all started together on `created`, and the reading is their ratio.
- `133-tA` (0.05 / 0.07 / 0.08): 38/38/38, then 86/86/86 2.7 s later: all **one step**.
- `133-tB` (0.1 / 0.12 / 0.13): 49/49/49 (one snapshot; the second capture overwrote it):
  all the same, so 0.13 is not 3 steps.
- `133-tC` (0.05 / 0.15 / 0.02): 62/31/–, then 114/57/–: 0.02 never fires, and **0.15 is
  2 steps in 1.33** (half the 0.05 rate), not 3. So 1.33 also rounds down, but on a
  floating-point value: 0.15/0.05 comes out as 2.999…, which floors to 2. The 1.39 to 2.31
  runs above give 0.15 exactly 3 steps.
- The full eleven-NPC 1.33 run (`133-timeout`) shows every timer from 0.05 up firing and
  0.01/0.02 silent, but its counts read 0 (the `#v` limit).

**5.00r7 (online).** Windows 5.00r7 (unpacked CRC-patch build, full root folder, token
`G3D22067`) under Wine 10, through the lab lobby (14900, warp) → decrypting proxy (14803) →
GServer-v2 beta4 lab build (`365bbd2` + lab patches), all in one loopback-only namespace.
Nine clientside GS1 weapons on the guest account each count in a global variable on
`timeout` (`if(playerenters){gtN=0;timeout=T;} if(timeout){gtN=gtN+1;timeout=T;}`), and a
tenth sends `setplayerprop #c,R<gt0>_…_<gt8>` once a second, so the proxy log has the
counters with timestamps (`proxy-49996.log`). 5.00r7 holds a full 20 steps/s here.

| T | 0.01 | 0.02 | 0.05 | 0.07 | 0.08 | 0.1 | 0.12 | 0.13 | 0.15 |
|---|---|---|---|---|---|---|---|---|---|
| count after 20 reports (~20 s) | 0 | 0 | 399 | 399 | 399 | 199 | 199 | 199 | 133 |
| count after 32 reports | 0 | 0 | 639 | 639 | 639 | 319 | 319 | 319 | 213 |
| per second | 0 | 0 | 20.0 | 20.0 | 20.0 | 10.0 | 10.0 | 10.0 | 6.67 |

**5.00r7 rounds down as well** (1, 1, 1, 2, 2, 2, 3 steps; under one step never fires).

**6.03r7: not testable here.** The lab gserver sends no GS1 to clients newer than 5.007
(6.x gets GS2 bytecode, and this server has no GS2 compiler), and a GS1 weapon on a 6.x
account crashes it (cadence lab). So the 6.x row stays open; it needs a server that can
compile GS2.

**Summary of 2a:** every engine measured (1.33, 1.39, 1.41r1, 2.05r2, 2.17.1, 2.22, 2.31,
5.00r7) rounds a GS1 timeout **down** to whole 50 ms steps, and a timeout under 0.05 never
fires. 1.33 alone does the division in floating point, so 0.15 gives 2 steps there.

### 2b. Walk GANI frame timing at run time (2.22, 2.31)

- Clients: 2.22 and 2.31 from a private copy of the Reborn 2.22.0 folder, offline (editor,
  then Play) on a plain grass level `lab_ga_plain.nw`, under Wine on an Xvfb display, no
  network.
- Method: hold the arrow key with XTest and grab a 630×180 strip around the player every
  ~18 ms. The player is the box of non-green pixels; each new sprite shape is a new GANI
  frame. Walked left 3 s first, then measured 4 s walking right (2.31 left as well). Logs:
  `gani/r222-right`, `gani/r231-right`, `gani/r231-left` (frames.json plus one PNG per
  shape; private).
- `walk.gani` (2.22 folder): 8 frames, no `WAIT`, `LOOP` + `CONTINUOUS`.

| run | frame changes | median frame time | mean frame time | 8-frame cycles (ms) | mean cycle |
|---|---|---|---|---|---|
| 2.22 right | 68 in 3.98 s | 52.6 ms | 59.3 ms | 523, 454, 395, 532, 393, 444, 470 | 459 ms |
| 2.31 right | 63 in 3.91 s | 56.5 ms | 63.1 ms | 405, 507, 543, 377, 931, 476 | 540 ms |
| 2.31 left | 50 in 3.96 s | 65.5 ms | 80.9 ms | 1199, 491, 634, 518 | 710 ms |

- Shapes cycle through the 8 frames in file order, mirrored as in the file (the
  right-facing shapes go a b c d e d c b), **one frame per game step**, and while the camera
  is not following the box moves **8 px per frame change**. So the walk frame and the 8-px
  move step together.
- The game step under Wine in this lab is ~17–18 steps/s (the timeout runs above agree), so
  one frame lasts ~55 ms here, and a cycle ~0.45 s. At the native 20 steps/s that is 50 ms
  per frame and 0.4 s per cycle, which is the value read from the file before.
- The long cycles (931 ms, 1199 ms) and the skipped shapes in the 2.31 left run are Wine
  render stalls (no change for 100–170 ms, then the next shape), not GANI timing.

### 2c. Combat live checks (partial)

All offline, single player, under Wine on an Xvfb display, no network. Frames are private
(`gani/…`).

- **Sword-clash spark: not identified.** 2.22, level `lab_ga_baddy2.nw` (plain grass, gray
  soldiers type 0 ×2 and a blue soldier type 1 to the right, plus an NPC that refills hearts
  every 0.5 s). The player faced the soldiers and swung every 0.25 s for 15 s while a
  200×130 box around them was grabbed every ~8 ms (1795 grabs, 293 distinct images,
  `gani/clash222b`). A search for colours seen in at most 8 frames found only one red, in
  pairs of frames ~2.3 s apart (it matches hits on the soldiers), and no transient sprite by
  eye where the swords crossed. So the five-tick spark was not caught; this method can't
  tell whether no clash happened or the spark uses colours that are on screen anyway. A
  first try (`gani/clash222`) had the player facing the wrong way and dying at 2.6 s. A
  wall of stones (`lab_ga_spark.nw`) gives no spark either (`gani/spark222`), which agrees
  with the static read that the spark is for sword meets baddy sword only.
- **No item drop on 2.22 offline (not the 2.05 control):** both gray soldiers died in the
  run above and nothing appeared where they fell, and the rupee count stayed 0. This is
  2.22 offline, not 2.05; the 2.05 control was not run.
- **1.21:** runs under Wine; One Player starts; F5 opens a Load level dialog ("Level
  specification", file name resolved against `levels\`); a GR-V1.03 scene
  (`lab_ga121_baddy.graal`, board from its `level1.graal`, baddies types 0, 0, 1, 2 written
  as raw `x y type` records) loads and its baddies spawn, patrol and come for the player;
  the sword swings (S) and hits. Two gray soldiers disappeared during 14 s of swinging, but
  off the screenshots, so **the 1.x item roll was not seen**; with a 70 % chance of no item
  per gray soldier, two kills would not settle it anyway.
- **Inclusive 2-tile sideways sword edge with two players: not run.** It needs two clients
  online in one level with exact placement; time went to the items below instead.

---

## 3. #254 S→C 108 sub 1 on 6.03r7

- **Client:** Linux 6.03r7 (token `G3D0511C`), native, HOME in the lab copy, window black
  under Xvfb (known), so read from the wire only.
- **Server:** GServer-v2 beta4 lab build (`365bbd2` + the lab patches, a private copy of the
  cadence-lab pack). The GS1 `-timer` weapon was taken off the guest account first (GS1
  weapons crash beta4 for 6.x clients). Lobby on 14900 warps to the decrypting proxy on
  14803 → gserver 14802, all inside one loopback-only network namespace. The client logs in
  by itself as `guest` from its saved settings.
- **Injection:** the proxy re-encodes S→C, so `108` lines (`c sub`, `s value`) are added to
  the live stream. The 6.03r7 answers (C→S 162) have to be dropped at the proxy: beta4
  counts 162 as an unknown packet and kicks the client for "sending invalid packets" after
  the third (first try, `proxy-37452.log`: kicked at the third ping answer; the client then
  logged in again by itself). With `DROP_CS=162` the proxy re-encodes C→S without them.
- **Script** (phases in `p254-phases.log`, packets in `proxy-60544.log`): baseline of four
  sub-0 pings 5 s apart, then for each sub-1 value 0, 1, 5, 30, 300: send sub 1, 60 s with
  nothing else, three sub-0 pings 5 s apart, 10 s wait. Then 100 s more with nothing.

| phase | sub-0 pings | 162 answers | other C→S | longest C→S gap | disconnect |
|---|---|---|---|---|---|
| baseline (no sub 1) | 4 | 4 | id 24 ×8 | 5.1 s | no |
| sub1 = 0 | 3 | 3 | id 24 ×17 | 5.1 s | no |
| sub1 = 1 | 3 | 3 | id 24 ×17 | 5.1 s | no |
| sub1 = 5 | 3 | 3 | id 24 ×16 | 5.1 s | no |
| sub1 = 30 | 3 | 3 | id 24 ×17 | 5.1 s | no |
| sub1 = 300 | 3 | 3 | id 24 ×17 | 5.1 s | no |
| 100 s after | 0 | 0 | id 24 ×19 | 5.1 s | no |

(One extra sub-0 ping per phase counts in the next phase's window: 19 pings, 19 answers in
all.)

- Every sub-0 ping was answered within 0–5 ms with the same value echoed, before and after
  every sub-1 value.
- The client never sent 162 on its own (no ping from the client side), whatever sub 1 said.
- Its only other traffic, C→S 24 every 5.10 s (min 5.09, max 5.11 over 120 sends), did not
  change.
- No timeout or disconnect in 10 minutes, even with sub1 = 1 or 5 and 60 s without a ping.

**Answer:** on 6.03r7, the sub-1 value has no visible effect on pinging, keepalive timing or
disconnects over 60 s windows. If it is a timeout, it isn't enforced by the client within
60 s at 1 or 5 (in seconds or in units of 5 s), so it is either unused (as the static read
found) or something longer than this test, or it's read by a code path this lab didn't
trigger.

---

## 4. #245 2.22 login default checks with a near-empty data folder

- **Client:** 2.22 Windows build from the Reborn 2.22.0 folder (token `GNW03014`) under
  Wine 10, in this lab's loopback-only namespace. Logged in through the lab listserver
  (14922, server list) to the decrypting proxy (14803) → GServer-v2 beta4 lab build
  (`365bbd2` + lab patches; the lab copy set to `generation = newmain` and `GNW03014` added
  to `newmain`, since it was set up for 4.x–6.x). Account `lab245`, new.
- **What a near-empty folder needs** (found by adding one file per "not found" message):

| step | missing → message |
|---|---|
| exe only | Wine can't load it: `bass.dll` and `hvdi.dll` are imports (`basswma.dll` added with them) |
| + 3 DLLs | "The file arrays2.sig has not been found in the Graal folder!" |
| + `arrays2.sig` | "…arrays2.dat…" |
| + `arrays2.dat` | "The Graal execution file is corrupted…" (that's the missing `graal.sig`) |
| + `graal.sig` | **login screen shows** (its images are inside the exe) |
| Start Online | "…arrays.dat…" |
| + `arrays.dat` | "…pics1.png…" |
| + `pics1.png` | server list, then into the game |

  So the "start-up images only" folder is: the exe, `bass.dll`, `basswma.dll`, `hvdi.dll`,
  `arrays.dat`, `arrays2.dat`, `arrays2.sig`, `graal.sig`, `pics1.png` (the client writes
  `graalconfig.txt`, `servermessage.html` and `weblevels\` itself).

- **File checks on the wire.** Run `proxy-52550.log` (near-empty) and, through the same
  server and account straight after, `proxy-36202.log` (full folder). The proxy now logs
  every C→S frame boundary. All file checks went out **in the client's second C→S frame,
  together with its first player-props line (id 2)**, one zlib frame (type 4), 0.3 s after
  login:

| folder | frame 2 contents (besides the props line) |
|---|---|
| near-empty | id 23 `idle.gani`, id 23 `plisticononline.png`, id 23 `plisticonaway.png`, id 23 `plisticondnd.png` |
| full | id 34 `plisticoneating.png`, id 34 `plisticonhiding.png`, id 34 `plisticonno pms.png`, id 34 `plisticonrping.png` (each with a 5-byte modification time first), id 23 `steps.wav`, id 23 `lab_u7_time.gani` |

  - id 23 (want) is for a file the client doesn't have; id 34 (update check) carries the
    local file's modification time.
  - The player-list icons it checks follow the status list the server sends (S→C 180:
    Online, Away, DND, Eating, Hiding, No PMs, RPing, …). With a full folder,
    Online/Away/DND were not asked for at all; with a near-empty one only those three were
    asked for.
  - **This server answered none of these requests** (no S→C 102 file and no 30 "send
    failed" in either run), and neither client sent any further file check in the minutes
    after: no `sword1.png`, `shield1.png`, `head0.png`, `body.png`, bomb or bow icons,
    although S→C 9 named them. The near-empty client never drew the player. So the client
    seems to wait for answers before asking for more, and this server is not a fair test of
    "the full set": the 2026-11-13 run, whose server did answer, saw two more frames (sword,
    shield, body, bomb and bow icons, then `head25` and `steps.wav`). The set above is what
    goes out before any answer.
- What to do next for the full set: rerun against a server that answers id 23/34
  (seihai-gserver or the 11-13 harness server).

---

## 5. #398 action list on 4.20r8–6.113 (partial: 5.00r7 only)

- **Setup:** GServer-v2 beta4 lab build (`365bbd2` + lab patches) in this lab's
  loopback-only namespace, generation `modern`; the lobby on 14900 warps to the decrypting
  proxy (14803) → gserver (14802). Fixture `lab398.nw` (start level): plain grass, three
  bushes to the west, a stone wall at x=36, a `spinattack` chest at (29,36) and a `glove2`
  chest at (33,36), a link on the west edge to `testworld.nw`.
- **Observer:** Linux 6.03r7 (`G3D0511C`, native, window black under Xvfb), account
  `guest`, standing at the start point; judged from its decoded S→C stream
  (`proxy-40046.log`). **Actor:** Windows 5.00r7 (`G3D22067`) under Wine 10, also `guest`
  (beta4 takes two `guest` logins at once). Inputs are X11 key events (step times in
  `act398-500.log`), packets in `proxy-55166.log`; a per-step summary script reads them.
- **Lab gotchas:** the 5.x/6.x clients show "You have been disconnected from the game
  server" when the lobby closes its socket; pressing its Ok quits the client, so leave it
  (keys still reach the game). With the lobby's 10 s hold the warp sometimes never
  connected; it now holds 60 s.

| action (5.00r7) | actor sent | observer saw | result |
|---|---|---|---|
| walk (R, L, D, U, 0.5 s each) | props with `walk`/`idle`, 13–22 props lines per step | the same lines relayed as S→C 8 | **4/4** |
| sword (S ×3) | `sword` gani, plus C→S 157 | `sword` in S→C 8 | **3/3** |
| spin chest, glove chest | no chest packet: the blind walk did not end next to a chest | — | 0/1, 0/1 (not reached) |
| spin (double-tap S ×3) | `sword` only (no spin item, chest not opened) | `sword` | 0/3 (no item) |
| wall push | `walk` only in that window; `push` appeared later, during the level-link walk, against something else | `push` relayed then | not at the wall (position off) |
| wall grab-and-pull, bush lift, throw | no `grab`/`pull`/`lift`/`carry` | — | 0 (position off) |
| chat | typed text went to the game as keys, no chat prop | — | 0 (chat bar not focused) |
| level link | the walk west ended pushing against something; no level change | — | 0 |

- **What this shows:** on 5.00r7 the observer receives the actor's movement and sword gani
  through the beta4 relay unchanged (the same count and content as sent). Everything that
  depends on standing in a set place failed, because the blind key timing under Wine
  (17–20 steps/s, plus a camera that didn't follow the actor in the screenshot) put the
  actor elsewhere.
- **Not run:** 4.20r8, 5.12, 6.03r7 (Windows) and 6.113 as actors. The next step is
  closed-loop movement: read the actor's x/y from its own C→S props in the proxy log and
  steer until it stands at each fixture spot, then fire the action. With that, the same
  script serves all five builds.

---

## 6. #243 Linux 3.04 stage-0 capture

- **Pre-check:** no stage-0 capture existed. The Torque rebuild's `console.log` files are
  rebuild outputs; the stage-3 input capture has `console.log` + `config.cs`, no `prefs.cs`
  and no menu walk; the macOS Torque lab has no console log. So it was run.
- **Client:** Linux 3.04 `graalexe` from the archive's fixed Linux 3.04 release (the same
  bytes as the cadence-lab copy), a fresh copy, HOME inside the lab folder. `main.cs`
  already sets log mode 6 when no `-log` is given, so it ran unchanged.
- **Sandbox:** first session in `bwrap --unshare-net` (no network at all); the second
  inside this lab's loopback-only namespace so the server list could reach the lab
  listserver (14922) and nothing else. (`--unshare-pid` makes this UPX-packed exe exit 127
  at once, so no PID namespace.) Xvfb 1024×768; the client opens its default 800×600
  window. Mesa llvmpipe.
- **Walk (session 2):** login screen → Options: Graphics, Audio, Controls, General tabs →
  OK → Get an account (no visible effect: it opens a URL) → F2 console open/close →
  nickname `labnick`, account `lab304`, a dummy password → Start → server list → F2,
  `quit` → clean exit.
- **Kept (private):** `console.log` (66 lines, session 2, log mode 6, written to the
  client's per-user `graalexe` folder), `prefs.cs` (104 lines) and `config.cs` (18 lines,
  the key map) written on exit to its `graaldata/client/` folder (it also writes
  `config.cs.dso`), and the session-1 console log (killed, so no prefs). Screenshots of the
  walk stay private.
- **Redaction:** no host names or addresses appear in any of the three files (the lab
  listserver is reached by name through a host shim and isn't logged). `prefs.cs` holds the
  lab account and nick only; the password is not saved. `console.log` has one local path
  (`applicationdir:`), which has to be cut before anything from it goes into a repo.
- **Notes for stage 1:** the console log shows the engine init, the eight missing
  `glVertexBuffer` functions, the OpenGL extension lists, and
  `Con::execute - 0 has no namespace: onDNSResolved` / `onConnected` when the server list
  connects. The typing helper sent `quit()` without its parentheses; the console logged
  "Syntax error in input. ==>quit" and the client then exited normally and wrote its prefs.
- **Not covered:** the server list showed one tab ("Hosted"), because the lab listserver
  has one server in one category; the four-tab view needs a list with servers in four
  categories. No in-game screens (Tutorial was not opened).
