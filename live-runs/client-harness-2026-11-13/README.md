# Client test harness: per-build action results, 2026-11-13

Lab run for #398, with the #399 Mac items and one #245 point. The harness drives a real
client, decodes its wire through a logging relay, and checks each action from a second
player (the observer) logged in to the same level. Every run below is offline, on lab
servers at the loopback address and lab ports. **[lab]**

## Setup

| Item | Value |
| --- | --- |
| Clients | 1.39 (`GNW07080`), 1.41r1 (`GNW13110`), 2.22 (`GNW03014`), 2.31 (`GNW28015`), under Wine + Xvfb in a Linux lab VM; Mac 4.04r2, 4.20r6 and 5.12 in a Mac OS X 10.4 PowerPC qemu guest |
| Server | seihai-gserver-v2, the 2026-11-11 harness build. The later commit `a1859bab` never runs the fixture's serverside chat-warp NPC, so it was not used (reported to the server thread) |
| Fixture | one start level with both chests, a wall, the three block **tiles** (push, pull, push/pull; no NPC), bushes, water, a chat-warp NPC and a level link |
| Input | X11 key events. Under Wine they reach the client's DirectInput device, which the Windows key hook did not |
| One driver | each lab desktop has a lock file; a run takes it before it sends input |

The lab VM ran at load 12–27 for the whole session, so short key presses were sometimes
dropped. Read a low count as "not seen in this run", not as "the build cannot do it".

## Action table

Pass / attempts. A pass means the actor sent it and the observer saw it.

| Action | 1.39 | 1.41r1 | 2.22 run b | 2.22 run c | 2.31 run e | 2.31 run b |
| --- | --- | --- | --- | --- | --- | --- |
| walk | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 0/4 \* |
| sword | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 \* |
| spin chest | 0/1 | 0/1 | 0/1 † | 0/1 † | 0/1 | 1/1 |
| glove chest | 0/1 | 0/1 | 0/1 † | 0/1 † | 0/1 | 0/1 |
| spin (double-tap S) | 0/3 | 0/3 | 0/3 | 3/3 | 0/3 | 3/3 |
| wall push | 0/3 | 2/3 | 0/3 | 0/3 | 2/3 | 0/3 |
| wall grab-and-pull | 0/3 | 3/3 | 2/3 | 3/3 | 1/3 | 1/3 |
| block push | 0/3 | 2/3 | 2/3 | 0/3 | 1/3 | 2/3 |
| block pull | 0/3 | 0/3 | 3/3 | 2/3 | 0/3 | 0/3 |
| bush lift | 0/3 | 0/3 | 3/3 | 3/3 | 0/3 | 1/3 |
| throw | 0/3 | 0/3 | 3/3 | 3/3 | 0/3 | 0/3 |
| hide (lift, then D) | n/a | n/a | 2/2 | 1/2 | 0/2 | 1/2 |
| swim | n/a | n/a | 3/3 | 1/3 | 1/3 | 1/3 |
| chat | 1/1 | 1/1 | 0/1 | 1/1 | 1/1 | 1/1 |
| level link | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0/1 |

\* The first steps of that run were sent while the client was still loading.
† The account had already opened that chest in an earlier run.
n/a: 1.x sends no swim or hidden sprite on the wire.

## Findings

- **Spin on 2.x.** Double-tap S spins, and so does tap-then-hold S; holding S alone does not.
  2.22: double-tap 3/3, tap-then-hold 3/3, hold 0/3. 2.31: 3/3, 3/3, 1/3. This matches
  2.05 rev 2 (a second press during the swing), so 2.22 does not differ from 3.04.
- **Walking on 2.22.** Passes 4/4 in two runs once input reaches DirectInput.
- **1.41r1 online.** It goes online through a listserver server list, not through
  `serveraddr=`; the lab listserver has to stay silent for about 500 ms after the list. This
  is why earlier runs saw 1.41r1 "go offline". Its client-to-server stream inserts one junk
  byte per message (encryption generation 3).
- **No spin on 1.x.** 1.39 given STATUS bit 0x20: no spin from a second S press, 0/6.
  1.41r1 given bits 0x20 and 0x40: no spin from a second press or a hold, 0/9.
- **1.41r1 push and pull poses.** Push is 3 frames (sprite steps 11–13, repeating). Pull is
  `grab` for 1 frame (step 14), then 3 frames (steps 15–17, repeating). Ticks per frame were
  not measurable on the loaded VM (wire spacing about 0.10–0.12 s).
- **1.41r1 swim.** Not on the wire: the client sends the idle sprite while swimming.

Not measured in this run: 2.22 blink ticks after a hit; 5.x/6.x hurt lock-out, pull and
swim frames; which bushes a spin cuts and whether it hits players or NPCs. The Windows 4.x to
6.x builds (4.20r8, 5.00r7, 5.12, 6.03r7, 6.113) were not run: their lab desktop was in use
for the whole session.

## Mac PowerPC items (#399)

- **4.20r6 machine field.** Once the emulated network card is marked built-in through an Open
  Firmware boot command, field 2 of the login's comma list is filled. It is the MD5 of the
  6 raw hardware-address bytes (not of their hex text).
- **Flag sends.** Mac 4.04r2 and 4.20r6 send id 18 (`PLI_FLAGSET`) only for `client.` flags.
  A plain flag and a non-`client.` string flag set by a probe weapon on `created` and on a
  timer are never sent. 5.12 runs no clientside GS1 on this server (it wants GS2 bytecode),
  so it has no answer here. 3.153 was not installed in the guest and was not run.
- **5.12 black level.** The Mac 5.12 bundle has no `pics1.png`, so the client asks for it.
  The server refuses with "file send failed" and logs "File too large for client version":
  the Mac tokens are not in seihai-gs2lib's version table, an unknown token is ranked oldest,
  and files over 64 KB are refused to the oldest clients. A tileset under 64 KB is sent and
  the HUD starts drawing, though the world stayed black with the cropped test tileset. The
  fix is to add the Mac tokens to the table and serve the stock tileset; a rebuilt server
  has not been run on the guest yet.
- **Saved password and level caches.** The saved password uses the same DES cipher and string
  format as Windows, with a per-machine key built from the 6 hardware-address bytes and a
  `:pass` key name. The `.code` level caches are `GWEBL001`, with a big-endian unpadded length
  header and the low byte of the generator per block. (The password itself is not recorded.)

## Login default checks (#245)

- 2.22 with a full data folder sends its default files as id 23 (want, when the file is
  missing) or id 34 (update check with a modification time). They go out batched with the
  first props in one zlib frame, followed by two more frames: the sword, shield, body, bomb
  and bow icons, then `head25` and `steps.wav`.
- An empty 2.22 folder, or one without its assets, stops at start-up with "File not found"
  before any network traffic. The empty-folder side of the comparison needs a folder that
  keeps only the start-up images; that run is still to do.

## Next

- Run 4.20r8, 5.00r7, 5.12, 6.03r7 and 6.113 on the Windows lab desktop.
- Rerun 5.12 Mac against a server with the Mac tokens in its version table.
- Find what changed in seihai-gserver-v2 between the 2026-11-11 build and `a1859bab` for
  serverside chat events.
- The #245 near-empty folder run, and the manual cells listed above as not measured.
