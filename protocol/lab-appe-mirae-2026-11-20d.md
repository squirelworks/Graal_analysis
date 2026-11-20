# Appendix E lab runs on Mirae, batch 4 (2026-11-20)

Date: 2026-11-20. Evidence: **[lab]**, with one short **[bin]** read for E#302. Real clients ran
under Wine in the Mirae Graal Linux RE Lab VM, each in its own network namespace with loopback
only, or (E#506) in the Mac OS X Tiger guest under QEMU with user-mode networking. The servers
are the gs2emu lab worlds behind the `gen5probe` proxy, and for E#506 the Seihai gserver with
its Graal3D mode on. No public service was contacted. Captures and screenshots stay in the lab.
The earlier batches are [`lab-appe-mirae-2026-11-20.md`](lab-appe-mirae-2026-11-20.md),
[`lab-appe-mirae-2026-11-20b.md`](lab-appe-mirae-2026-11-20b.md) and
[`lab-appe-mirae-2026-11-20c.md`](lab-appe-mirae-2026-11-20c.md). Probe rows are appended to
[`probe-results.tsv`](probe-results.tsv).

## Protocol 19 on the Mac 3.153 (E#506)

Build: Mac PowerPC 3.153 (the 3.15r2 disk image, token `G3D28015`), unchanged, run under the
same render shim as before (it only drops two attributes from the OpenGL pixel-format request so
QEMU's software renderer is used). Guest: Tiger 10.4 under QEMU, throwaway overlay. Server: the
Seihai gserver (Graal3D on, UDP on the TCP port + 1) and seihai-listserver 0.1.1, both in the
Debian VM, reached only through VirtualBox forwards on the host's loopback. World: no `sky` line,
no `tgeplayershape`, so the client gets a plain Sky and a `Camera`.

**First run: no 3D link.** The client logged in over TCP, entered the 2D start level and never
sent a UDP datagram (a logging relay on the UDP port saw none in two runs). Its server list
showed the server on the **Hosted** tab as "3 Lab 3D".

- The gserver lists itself as `3 Lab 3D` by name. seihai-listserver puts the HQ-level tag in
  front of every name in the client list, and a gserver that never sends an HQ level is level 1,
  tagged `H `. So the client got `H 3 Lab 3D`, stripped `H `, filed it as Hosted, and treated it
  as a 2D server.
- GServer-v2, in the 2026-11-14 run that did link, registered the plain name `Lab 3D` with HQ
  level 4, which the listserver tags `3 `.

**Second run: camera path complete.** A small lab stand-in registered the same address and port
with seihai-listserver as `Lab 3D`, HQ level 4 (the gserver's own listing was switched off). The
list then showed the server on the **Graal 3D** tab, and Connect opened both links at once:

- UDP challenge before the TCP login (the server held it until the login was done), then
  "Connection established", phase 1 (datablocks), phase 2 (ghosts: `Camera` and `Sky`),
  phase 3 ("Mission lighting done") and "*** Initial Control Object".
- The server logged the control object (ghost 1, the Camera) as delivered.
- **No crash.** The 2026-11-14 run (GServer-v2, before the seven-entry Sky rule) crashed on the
  first frame after the control object. This time the client kept running and kept the link:
  61 moves received over about 2.5 minutes, pings both ways.
- Quitting sent a Torque disconnect; the server logged "client disconnected", then the TCP leave.
- The client logged "Could not locate texture: g3d_sky" and "cloakTexture", both harmless.
- The window showed the sky colour above the horizon and left the loading picture below it. An
  arrow key held for 1.5 s changed nothing on screen. As on the 4.20r6 Tiger run, the software
  renderer under QEMU does not draw the scene below the horizon, so the view itself is not
  checked.

So the protocol-19 order works on the real 3.153 for the camera path, as it does on 4.04r2.
Separately, a Seihai 3D server listed through seihai-listserver needs HQ level 4 (or the
listserver must leave a `3 ` name untagged): a 3.153 picks 3D from the list tag, and `H 3 …` is
not 3D to it.

## Walking speed factor 0.4 on 2.05 (E#302)

Build: 2.05 rev 2, online, lab level, speeds from the client's own position props (every 0.1 s)
over a 1.5 s key hold. All tiles came from the stock tile-type table.

**Tiles: all 1.0.** Swamp (type 6), lava swamp (7), near water (8), deep water (11, the swim gani)
and chair (3) all walked at 1.0 tile per 0.1 s, right and left. Swamp showed its splash under the
feet. The chair played `sit` while moving.

**Where 0.4 comes from [bin].** The 2.05 walk picks its factor in this order: riding (0.8, plus
small steps up the longer the ride lasts), hidden (0.2), then **0.4 when the player's current
gani is the `sleep` gani** (by its default name, or whatever gani `replaceani` has put in the
sleep slot), then 1.2 for shield power 3 or more, else 1.0.

**Lab check** (`replaceani` needs the NPC-server flag on 2.05, see E#201, so the proxy sent
PLO 44 first):

| State | Gani on the wire | Speed (tiles per 0.1 s) |
| --- | --- | --- |
| `replaceani walk,sleep` (two runs) | `sleep` | **0.4** (x 10.5 → 16.5 in 1.5 s, steps 0.5 every 0.1 to 0.15 s) |
| `replaceani sleep,lift` then `replaceani walk,lift` | `lift` | **0.4** |
| `replaceani walk,sit` (sleep slot back to `sleep`) | `sit` | 1.0 |
| `replaceani walk,walk` | `walk` | 1.0 |
| `replaceani walk,hurt` | `hurt` | 1.0 |
| `setani sleep,` then walk | `walk` from the first step | 1.0 |
| hurt by GS1 `hurt 1`, key held | `hurt` | knocked back 2.5 tiles, then no movement for about 1 s although the key was held, then 1.0 |
| server-set gani `hurt` or `sit`, then walk | `walk` | 1.0 |
| `freezeplayer 1`, key held | none until free | 1.0 after |

So factor 0.4 is walking while the gani is the sleep gani. In ordinary play the walk step puts the
walk gani on first, so it is reached only through `replaceani` on the walk or sleep slot.

## Shot types 0 and 1 on 2.22 (E#312)

Build: 2.22 (`GNW03014`), two clients online: a victim and a visible second player as the shooter
(id 4). Each shot was sent to the victim as `PLO_ARROWADD` (19): shooter id, x 30.5, y 25, flags,
power 1, last byte. The victim stood at (30, 30) facing up with shield 0, 3 hearts, reset before
each shot. Flags = direction 2 (down) plus the bit under test.

| Level | Shot | Owner | Result |
| --- | --- | --- | --- |
| no `noplayerkilling` | type 0 (byte 33) | none (id 0) | **hit**, half a heart (power 6 → 5), `hurt` |
| no `noplayerkilling` | type 1 (byte 34) | none | **hit**, one heart (6 → 4) |
| no `noplayerkilling` | type 0 | shooter id 4, flags + 8 | hit, half a heart |
| no `noplayerkilling` | type 1 | shooter id 4, flags + 8 | hit, one heart |
| no `noplayerkilling` | type 0 | id 4, no extra flag; or flags + 16, + 32, + 64 | hit, half a heart each |
| no `noplayerkilling` | type 1 | id 4, flags + 4 | hit, one heart |
| no `noplayerkilling` | type 2 (byte 35) | none | hit, half a heart |
| `noplayerkilling` (level NPC runs it on `playerenters`; the HUD shows its mark) | all of the above (10 shots) | as above | **no hit**, no hearts lost, no `hurt` |

- Types 0 and 1 hurt a receiving client directly, at half a heart and one heart, as the static
  read says. The owner link made no difference here: linked, unlinked and unknown-flag shots all
  hit. So on this setup the owner field the static read compares was equal in every case (most
  likely 0 on both players); its identity is still not known.
- A `noplayerkilling` level stopped every shot, with or without an owner.
- Why the 2026-11-20 GwenTea2 sweep saw no hits is not settled by this run; its shot placement
  and level were not repeated here.
- An injected `PLO_PLAYERWARP` (14) to the other level left the 2.22 client on "loading" (no board
  follows it), so the `noplayerkilling` half was rerun with that level as the start level.

## `move` timing on 2.05 (E#206)

Build: 2.05 rev 2, online. A level NPC (`block.png`) started each move when the player was placed
in a trigger band, set the player's chat at the start, and on `movementfinished` (option 8) set
the chat again. Times are the proxy's arrival times of the two chat props (both pass the same send
path, so the offset cancels).

| Move | Asked | Took | Note |
| --- | --- | --- | --- |
| `move 10,0,2,8` | 2.00 s | 2.03 s | |
| `move 10,0,0.5,8` | 0.50 s | 0.57 s | |
| `move 16,0,1.6,8` | 1.60 s | 1.65 s | |
| `move 10,0,0.12,8` | 0.12 s | 0.15 s | three steps of 50 ms (the biased floor gives 2, then 1, then done) |
| `move 10,0,4,8` | 4.00 s | 4.60 s | the VM was loaded at the time |
| `move 10,0,2,8`, client stopped (SIGSTOP) for 1.0 s mid-move | 2.00 s | **3.01 s** | no catch-up |
| `move 10,0,2,8`, client stopped for 2.0 s mid-move | 2.00 s | **4.23 s** | no catch-up |

- Every move ended at the right x (20 + 10, or 36 for the 16-tile move).
- No move finished early. A move takes its steps at 50 ms each, a little longer when the client
  runs slow, and a stall adds its full length: the consumer advances once per 50 ms step and does
  not catch up.

## `replaceani` and `showimg` on 2.05 (E#201)

Build: 2.05 rev 2, online. The proxy sent PLO 44 (the NPC-server announcement) first; without it
2.05 skips `replaceani` online (batch 3 saw no change). A level NPC ran each form when the player
was placed in its band, then the player walked left and right.

**`replaceani` (stored `MM`)**

| Written as | Walk gani on the wire | On screen while walking |
| --- | --- | --- |
| `replaceani walk,sit` | `sit` | the sitting body, moving |
| `replaceani walk,#s(an)` (holds `lift`) | `#s(an)` | nothing (no such gani) |
| `replaceani walk,"push"` | `"push"` with the quotes | nothing |
| `replaceani walk,dead hurt` | `dead hurt` | nothing |
| `replaceani walk,sit,lift` | unchanged (`dead hurt` from before) | the whole line did nothing, and the chat set after it on the same line was not sent either |
| `replaceani walk,walk` | `walk` | normal walk |
| `replaceani walk,hurt` | `hurt` | the hurt body, moving |
| `replaceani idle,sleep` | `sleep` when standing | the sleeping body |

So both `replaceani` arguments are taken as raw text: message codes are not expanded, quotes and
spaces are kept. A third argument stops the command and the rest of that line.

**`showimg` (stored `RMRR`)**, images placed in view relative to the player:

| Written as | Result |
| --- | --- |
| `showimg 1,block.png,playerx+3,playery` | drawn 3 tiles right of the player |
| `showimg 2,#s(im),playerx+6,playery` (holds `block.png`) | drawn 6 tiles right: the code was expanded |
| `showimg 3,"block.png",playerx+9,playery` | nothing drawn (quotes kept, no such file) |
| `showimg 4,block.png,#s(nx),playery-4` (holds `30`) | nothing in view at x 30; consistent with x = 0, which is outside the view |
| `showimg 5,@Lab text,playerx-6,playery-3` | the text "Lab text" drawn there |
| `showimg 6,bl ock.png,…` | nothing drawn |
| `showimg 7,block.png,"34",playery+4` | nothing in view at x 34; consistent with x = 0 |

So `showimg` converts like `puthorse`: the image slot is free text with codes expanded and quotes
kept, and the numeric slots evaluate expressions, with a string giving 0.

## Latin-1 byte 231 in `showtext` and a sign on 5.00r7 (E#213)

Build: unchanged 5.00r7 under Wine's Western code page, online on a gs2emu world. The level held
the text "Français éüñ ça" as Latin-1 bytes (ç as byte 231) written straight into the level file.

| Source | What the server sent | What 5.00r7 drew |
| --- | --- | --- |
| GS2 level NPC, `showtext(…, "GS2 Français éüñ ça")` | the Latin-1 bytes | **"GS2 Français éüñ ça"** |
| GS2 level NPC, `"GS2 C" @ char(231) @ "a"` | (built on the client) | **"GS2 Cça"** |
| GS1 level NPC, `showtext` (through the server's GS1-to-GS2 translator) | each non-ASCII byte replaced by the three-byte UTF-8 replacement character | "Franï¿½ais ï¿½ï¿½ï¿½ ï¿½a" |
| GS1 `showimg` with `@` text (same translator) | the same replacement | "Img Franï¿½ais …" |
| level sign | encoded as `#K(-25)`, `#K(-23)`, `#K(-4)`, `#K(-15)`: the server's sign encoder reads the bytes as signed | not seen: the walk-and-read keys did not reach the game window in this setup |

- 5.00r7 draws byte 231 as `ç` (and 233, 252, 241 as `é`, `ü`, `ñ`) in `showtext`, as it did in
  chat and nicknames. Together with batch 3 this settles the Western-code-page case for 5.00r7.
- The two broken forms come from the lab server, not the client: its GS1 translator replaces bytes
  that are not UTF-8, and its sign encoder writes negative `#K` codes for bytes over 127.

## Combat checks on 2.17.1 and 2.05 (E#324)

**2.17.1 archer scene: tried, no kill.** Build: 2.17.1 Training (offline), Wine virtual desktop
(without one, the F5 level dialog stays drawn over the game). Levels in `.nw` form: a rock corridor
with one archer (type 3) at its top, and an NPC that runs `setsword sword1.png,1` on entry (the
Training player has no sword). The sword appeared and swung. In 12 levels with 16 swings each, the
archer never died and never showed its hurt state; its arrows hurt the player, and after a death
the client went back to the Training start level. So no drop could be checked. This fits the
static gate that from 2.17.1 a sword does not hit in Kingdoms or New World mode, if Training runs
in one of those modes; that was not checked.

**2.05 sword against a shielded soldier.** Build: 2.05 rev 2 Training, same corridor in GR-V1.03
form with one gray soldier (type 0, shield and sword). Ten swings per level, four screenshots
during each swing (about 25 ms apart), four levels.

- All four soldiers were killed by the sword. Gralats, bombs and arrows did not change, and no item
  was drawn: no drop, as in the earlier 2.05 runs.
- The soldier showed `attack` and `hurt`. While both swung at close range, an orange arc was drawn
  over the soldier for several frames. No separate small spark sprite could be told apart from the
  two swings in these frames.

Still open: a 2.17.1 kill (bombs or arrows, or a non-Training offline mode) and a clean sword-on-
sword frame.

## Windows 4.04r2 offline scene on Win10 (E#610, E#611): partly run

Build: Windows 4.04r2 (`Graal4.exe`, file version 4.0.4.2, packed), unchanged, from a stock install
folder copied to a fresh work folder. Guest: the Win10 "Graal RE Lab" VM with **no network
adapter**, so the run was offline by construction. Run on the interactive desktop, driven by
keyboard scancodes and a small click helper inside the guest, with screenshots.

**Start-up on the Win10 desktop**
- As in earlier runs, the client stopped at start with an access violation inside a window
  callback, reported as a fatal user-callback exception. Its console log had already reached
  "Created DirectDraw object", "Initialized Direct3D7" and "Graal has been activated!".
- With the guest's `DisableUserModeCallbackFilter` compatibility setting on (the setting that lets
  an old program's own handlers see exceptions raised inside window callbacks), the client opened
  its login window on the desktop: nickname and account fields, Start, Options, Become a Member
  and **Offline Test**.

**E#610: offline play**
- In the first session, Offline Test opened the offline tutorial level: drawn tiles, palms, a
  cauldron, the path, and the player standing on grass. The console added "FMod Sounds: using
  default sound driver" and the tutorial tile definition file was written
  (`picso.png,offlinetutorial,1,0,0`).
- **Before and after a move:** the player in the grass below the cauldron; after Right held 1.5 s
  the player had walked right to the beach edge and the view had scrolled with it (sea in view).
- A following Down hold ended the session: the window closed, with no error report.
- Four later starts reached the login window each time, then closed within 5 s of Offline Test,
  again with no error report. Restoring the original config file and deleting the file-name cache
  did not change that. With the callback filter off, errors inside callbacks no longer produce a
  crash report, so these silent exits are probably the same fault the filter used to turn into a
  crash.
- So 4.04r2 does play offline on Win10 (a drawn level and controlled movement were captured once),
  but not reliably in this guest.

**E#611: not reached.** No bush or other liftable object was reached before the session ended, so
no lift, carry or throw was captured.

**Guest state afterwards.** The compatibility setting was removed again, the click helper stopped,
and the guest shut down. The work folder `e610` is left in the guest.
