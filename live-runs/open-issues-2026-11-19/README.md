# Open-issue lab run, 2026-11-19

Lab run for #443 (drop control, 1.21, sword spark, 6.x timer), #245 (login default checks),
#619 (tiledef type 4) and #398 (the action list on Linux 6.03r7 and on real Windows 4.20r8
to 6.03r7). Every run was offline, in the Debian lab VM and the Windows 10 lab VM, on lab
servers at the loopback address and lab ports. Raw logs and
screenshots are kept privately; this page has the derived results. **[lab]**

## Setup

| Item | Value |
| --- | --- |
| Clients | 1.21, 1.39 (`GNW07080`), 2.05 rev 2, 2.22 (`GNW03014`) under Wine + Xvfb; Linux 6.03r7 (two copies for the harness) |
| Servers | GServer-v2 lab build (file checks, harness world); seihai-gserver behind the probe proxy (`tools/probe/`) for 6.03r7 |
| Script compiler | seihai-core `main` c56c322, for the 6.03r7 GS2 timer (neither lab server build sends GS2 bytecode to 6.03r7) |
| Input | X11 key events into the focused client |
| Logs | Wine shim logs capped at 60 MB |

1.21 needed head, sword, shield and baddy images copied in from 1.28b2 before it would play.

## 1. #443: item drops when a baddy dies

The 1.21 to 1.41 clients roll 0–99 when a baddy dies and drop an item on a low roll; an
archer (type 3) drops darts below 75, so about three archer kills in four drop something
(→ [combat-baddy-tile-by-version.md](../../client-internals/combat-baddy-tile-by-version.md)).
Archers make the control sharp: a roll like that would show within a few kills.

Scene: a rock corridor in GR-V1.03 format (2.05r2 offline loads `BADDY` records only from
GR-V1.03 levels), archers and gray soldiers, killed one at a time with the sword. Each death
was watched for about 3 s, with the gralat, dart and heart counters read before and after.

| Build | Archer kills | Soldier kills | Drops | Notes |
| --- | ---: | ---: | --- | --- |
| 1.39 (positive control, same levels) | 12 | — | 9 of 12 | 8 × darts (+5 each), 1 × green gralat; fits the 75 % archer roll |
| 2.05 rev 2 | 17 | 8 | **none** | no item drawn; gralats, darts and hearts never changed |
| 1.21 | 12 | — | see below | +1 gralat in the frame of death, every kill |

- **2.05 rev 2 has no client-side drop roll offline.** With a 75 % roll, 17 archer kills with
  no drop would happen about once in 10^10 tries. This matches the static reading that the
  roll is gone from 2.0 on, where the server drops items. **[lab][bin]**
- **1.21:** each of the 12 archer kills gave exactly one gralat, in the frame the baddy died,
  and no darts or hearts. That does not look like the 0–99 roll, which would give darts most
  of the time. The drop spot is the baddy's top-left corner, which overlapped the player at
  every sword kill, so this run could not tell a dropped green gralat that was picked up at
  once from a direct kill reward. **Open.**
- 2.17.1 was not run.

## 2. #443: the sword spark

1.39, three sword swings into a rock wall, screenshots at about 28 a second. The swing shows
from about 25 ms to 240 ms after the key goes down. No separate spark sprite could be told
apart from the swing in these frames. 2.22's Training level starts without a sword, so 2.22
was not tried. **Not identified.**

## 3. #443: the 6.03r7 timer, repeated

GS1 is not available to 6.x, so the GS2 form was used: `setTimer(T)` with `onTimeout`,
compiled with seihai-core and injected through the probe proxy. Periods over 10 s:

| `setTimer` | Period |
| --- | --- |
| 0.01, 0.03, 0.05 | 50 ms |
| 0.07, 0.1 | 100 ms |
| 0.12, 0.15 | 150 ms |
| 0.2 | 200 ms |

The timer **rounds up** to whole 50 ms steps, and values under 0.05 fire every step. This is
an independent repeat of the earlier 6.03r7 timer lab
([gs2-vm-quirks-by-version.md](../../client-internals/gs2-vm-quirks-by-version.md#linux-603r7-timer-lab),
[update-cadence-3x-6x.md](../../client-internals/update-cadence-3x-6x.md#603r7-gs2-timer-ceils-to-50-ms))
and agrees with it. It is the opposite of the GS1 floor on 1.33 to 5.00r7. **[lab]**

## 4. #245: 2.22 login default checks, with a server that answers

GServer-v2 answered each check, so the client went on past its first frame.

| Data folder | Files checked | Packet | Count |
| --- | --- | --- | ---: |
| full | every default file | 34 (modification time + name) | 13 |
| near-empty (start-up files only) | every default file | 23 (name only) | 17 |

- **At most four file packets go in one frame.** The first four share a frame with the
  first flags and props line. Each further batch of up to four goes out after the server has
  answered the batch before it. **[lab]**
- With nothing but the exe, 2.22 stops at start-up because `pics1.png` is missing, so
  "near-empty" means the root start-up files only (as in the 2026-11-14 run).

Why the two counts differ (13 against 17) was not worked out in this run. The per-file
lists are kept with the private logs.

## 5. #619: tiledef type 4

The test level, an overlay image and the `tiledefsOffline` lines were built. Under the VM's
load, 2.22 stopped repainting after the F5 load, so where the type-4 tiles draw and how they
walk was not measured.

A second try at low load did not get further. 2.22's F5 loader also freezes under Wine on
its own tutorial level, so the freeze is not caused by the test level. In 2.31, Training opens
the level editor, and Play there does read `tiledefsOffline`: a type-0 line blacks out the
whole board. The 256 × 512 test overlay never drew, so where type-4 tiles land and how they
walk is still **not measured**. Next: a full-size 2048 × 512 overlay, or a run outside Wine.

## 6. #398: the action list on Linux 6.03r7

Two Linux 6.03r7 clients on the harness fixture world (both chests, a wall, the three block
tiles, bushes, water, a chat-warp NPC and a level link). Pass / attempts; a pass means the
actor sent it and the observer saw it. The observer saw every gani the actor sent.

| Action | 6.03r7 Linux |
| --- | --- |
| walk | 4/4 |
| sword | 1/1 |
| spin chest | 1/1 |
| glove chest | 0/1 |
| spin (double-tap S) | 1/3 |
| wall push | 1/1 |
| wall grab-and-pull | 1/1 |
| block push | 3/3 |
| block pull | 5/5 |
| bush lift | 3/3 |
| throw | 3/3 (sends id 11) |
| hide (lift, then D) | 3/8 (2/2 with lift then D) |
| swim | 1/1 |
| chat | 0/1: Tab opens no chat line on 6.03r7 |
| level link | 1/1 |

- An injected player warp to the **same** level freezes 6.03r7's input. The run moved the
  player with props 15 and 16 (X and Y) instead. **[lab]**
- Prop 81 (`PLAYERLISTCATEGORY`): not run. 6.03r7 has no key that opens a player list here;
  on 6.x the list is a script window, which the lab server does not provide.

## 7. #398: the action list on real Windows 4.20r8 to 6.03r7

Real, unchanged Windows clients in the Windows 10 lab VM, each with the guest clock at its
build's era (as in [real-win10-2026-11-18](../real-win10-2026-11-18/README.md)), logged in
through the Login lobby of a lab server in the Debian VM, on lab ports only. The logging proxy
kept `LISTPROCESSES` (182) out of the burst, since it crashes Windows 6.03r7 and that server
build predates the seihai-gserver#158 fix, and sent the two packets that close the
"Connecting…" box. The player was placed with props 15/16. Keys went in as VirtualBox scan
codes after one click inside the game window; without that click no key reached any build.
There was no observer client: a pass here means the server received the action from the player.

| Action | 4.20r8 | 5.00r7 | 5.12 | 5.24r4 | 6.03r7 |
| --- | --- | --- | --- | --- | --- |
| walk | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| sword | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| spin chest | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| glove chest | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 |
| spin (double-tap S) | 0/3 ‡ | 0/3 ‡ | 0/3 ‡ | 0/3 ‡ | 0/3 ‡ |
| wall push | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| wall grab-and-pull | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| block push | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 |
| block pull | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| bush lift | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| throw | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| hide | 3/8 | 3/8 | 3/8 | 3/8 | 3/8 |
| swim | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| chat | 1/1 | 0/1 | 0/1 | 0/1 | 0/1 |
| level link | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |

‡ Not a client result: each VirtualBox key event takes about 0.1 s, too slow for the double tap.

- **Hide:** lifting the bush and then pressing D hides, 2/2 on every build. Pressing A again,
  or S, never hides.
- **Block push on 6.03r7:** the two pushes on the push/pull stone did not register.
- **Glove chest:** 0/1 on every Windows build and on Linux 6.03r7. The client never sends the
  open-chest packet, so the fixture's glove chest itself is suspect.
- **Chat:** 5.x and 6.x show no chat line unless the server sends a chat script. 4.20r8 does
  without one.

## 8. #619: tiledef type 4 on 2.22

A later round ran 2.22 under Wine with a virtual desktop and the GDI renderer. The earlier
"freeze" was Wine leaving the hidden Load dialog's window over the game when no window
manager runs. With that, F5 loads the test level. Two things blocked §5: the overlay was a
24-bit PNG, which 2.22 ignores without a message, and the window problem.

- Type 4 pastes an 8-bit palette image into the tile sheet at **pixel** (x, y): (256, 0) lands
  at sheet column 16, (256, 64) at column 16 and row 4, and (264, 0) splits image columns across
  sheet column 17.
- Walking follows the board's tile codes; a rock row blocks the same with the stock sheet,
  under a type-4 overlay, and with type 0.

Write-up: [formats/tiledef-type4-2026-11-16.md](../../formats/tiledef-type4-2026-11-16.md#live-result-2026-11-19).
**[lab]**

## Still open after this run

Tracked in #652:

- 1.21: dropped gralat or direct reward (a sword kill one tile further away did not reach the archer; a ranged kill needs 1.21's item keys).
- 2.17.1 drop check, and the sword spark on 2.22 (the Training player has no sword; a way to give the offline player one is needed).
- The sword spark.
- Spin on the Windows builds (needs a faster input path), and the fixture's glove chest.
- Prop 81's effect on the player list.
