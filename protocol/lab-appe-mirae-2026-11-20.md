# Appendix E lab runs on Mirae (2026-11-20)

Date: 2026-11-20. Evidence: **[lab]**. Real Windows clients under Wine in the Mirae Graal Linux RE
Lab VM, each in its own network namespace with loopback only, against gs2emu lab worlds through the
`gen5probe` proxy. Captures and screenshots stay in the lab. Probe rows are appended to
[`probe-results.tsv`](probe-results.tsv).

## Once-per-second hit stamp on 2.05 (E#310)

Build: 2.05 rev 2 (`GNW03081`). Two real clients, a victim and an attacker, on the classic world.
Hurt messages (40) were also injected into the victim's stream.

| Sequence | Result | Runs |
| --- | --- | --- |
| a guild-rejected 40, then a clean 40 from the same attacker in the same frame | no hit | 3/3 one-client, 1/1 two-client |
| the same pair 1.5 s apart | the second 40 hits | 2/2 |
| a guild-rejected real swing, then a clean 40 from that attacker 0.3–0.5 s later, same second | the 40 hits | 3/3 |
| a guild-rejected 40, then a clean real swing 0.3 s later, same second | the swing hits | 4/4 |

- The hurt-message path stores the per-attacker stamp before the guild test.
- The sword judge neither checks that stamp nor stores one. So the stamp belongs to the
  hurt-message path only.
- Two swings 0.5 s apart give one hit, because the victim is still in hurt mode.
- A 2.05 swing reaches the other client as the `sword` gani (prop 10), not as a sword sprite.
  Injected other-player sprites 26 to 42 never hurt the victim (4 variants).
- The lab server strips an unknown "(tag)" from a player's own nickname, so the guild tests
  injected the tag on the victim's side.

## Knockback on 1.39 (E#309)

Build: 1.39 (`GNW07080`), online on the demo world. A hurt message (40) came from an injected
player, on open ground.

| Direction | From | To |
| --- | --- | --- |
| east (3 runs) | x 20 | x 25 |
| south | y 20 | y 25 |
| north | y 40 | y 35 |

The victim reported each step (21, 23, 25). A west push was blocked at once by the map, so it does
not count as open ground. Knockback is five tiles.

## `.nw` and gmaps on 1.41 rev 1 (E#617)

Build: 1.41 rev 1 (`GNW13110`), through a loopback listserver. The lab world's allowed-versions
line has to list `GNW13110`.

- The server sent a `.nw` start level as the level name (6), one full board packet (101, 8193
  bytes) and the modtime (39). The client drew the level and walked in it.
- The server sent no link (1) or height messages for that level, so those stay unobserved.
- With a 2 x 1 `.gmap` as the start level, the server sends 1.41 rev 1 a plain warp (14) to the gmap
  name, then the first cell as an ordinary level (6, 101). There is no gmap warp (49), and the
  client never asks for the `.gmap` file: it plays the cell as a normal level. The seam was not
  walked.

## Single-player start levels on 2.05 (E#319)

Build: 2.05 rev 2, offline (Training), using the F5 level loader, with a fresh client per load.

- Each special name was loaded at (10, 10), next to a byte-identical copy under a control name:
  - `level1.graal` (a 1.21 file);
  - `YoshiClanR2.zelda` and `YoshiClanFields.zelda` (1.19 files).
- Position, facing, HUD (3 hearts, 10 bombs, 5 darts) and level were identical at 1.5, 4.5 and
  10 s. The only differing pixels were animated flower tiles.
- There was no move to (31, 31) and no other state change.
- This is the F5 path. A step that runs only when a new game starts would not show here.

## Sign list end on 2.05 (E#604)

Build: 2.05 rev 2, offline, F5 loader. The 1.21 file `level40.graal` (`GR-V1.03`) had its three
sign slots rewritten as `ONE`, `TWO` and `THREE`.

| File after the board | Signs shown |
| --- | --- |
| three signs, no gap | all 3 |
| an empty line after sign 1 | `ONE` only |
| an empty line, a `HEIGHTS` line, then signs 2 and 3 | `ONE` only |

So 2.05 stops at the first empty line, like 2.31; it does not read to the end of the file. 2.31 was
not run, because it needs its own offline driver.

## Sword against sword on 2.05 (E#324, one sub-check)

Two real 2.05 clients stood 3 tiles apart, facing each other, and swung at the same moment, 4
times.

- No separate spark sprite appeared in frames 80, 160 and 260 ms after the press.
- The victim took half a heart in 3 of 4 tries, and the attacker was never hurt.
- So a true sword-on-sword meeting was not confirmed.

The 1.21 ranged kill and the 2.17.1 archer scene were not run, because 2.17.1 Training has no
sword.

## RC props tail counts (E#420)

Build: RC 2004 (`RemoteControl.exe`, `GSERV024`) against the Seihai GServer-v2 fork lab build,
behind `gen5probe`. Props requests by account name (74) were injected for four offline lab
accounts, and the tail of each 72 reply was decoded.

| Account | First `s` | Second `s` |
| --- | --- | --- |
| 3 flags, no chests | 3, then the flag strings, newest first | 0 |
| no flags, 2 chests | 0 | 2 |
| 3 flags, 1 chest | 3 | 1 |
| nothing | 0 | 0 |

- The first count is flags, the second opened chests.
- Each chest entry is `c` (length + 2), `c` x, `c` y, then the level name.
- The weapon count and names follow, and nothing comes after the weapons.
- This is the lab server's writer; no original 2001–2004 server was run.
- The RC account needs `LOCALRIGHTS`, not `ADMINRIGHTS`, or the server refuses to show player
  props.

## 6.03r7 HUD (E#326)

Build: 6.03r7 Linux (`G3D0511C`) on Mesa software GL.

- Hearts. In the identified-state captures of the 2026-11-13 HUD lab:
  - With 4 full hearts at window width 1024, the slots are at x = 826, 871, 916 and 961. The row
    ends at 1001, so the right margin is 23 px.
  - The 68 px margin is the 3-heart case (826, 871 and 916, ending at 956).
  - The slots stay at W − 198 + 45k at 640, 800, 1024 and 1280 wide.
- Sword. With the server's `sword1.png` replaced by an all-opaque magenta 128 x 96 image, the sword
  slot draws a magenta block of exactly 28 x 28 at (105, 31), and nothing more. The source
  rectangle is 28 px wide, not 34.
- Windows text positions and a Windows run at a current clock were not done; they need the Windows
  guest.

## 6.03r7 chest art and menu (E#327)

Build: 6.03r7 Linux.

- Chest. The same script-free scene, with the world now serving `chest.png` (32 x 32) and
  `chestopen.png`:
  - The client fetches `chest.png` at level entry and draws the closed chest.
  - Walking up opens it (gralats 0 → 1). The client then fetches `chestopen.png` and draws the
    open chest.
  - The missing art was only the two files the lab world lacked.
- Menu:
  - The 6.03r7 image names no GUI skin or window image. Its built-in image names are only sprites,
    state, swords, shields, bombs, bows, baddies, chest and chestopen.
  - The client requests no file when D, Q, Tab or Esc toggles the menu.
  - So the orange box is the default, unskinned GUI drawing, and a skin can only come from a
    server script. A scripted skin was not delivered.

## Upload ids from a game connection (E#9)

Build: 6.03r7 Linux on its game connection to the lab GServer-v2 fork. The file-browser and upload
ids were injected as client-to-server packets: 93 with data, 92, 155 + 93 + 156 (large file), and
96, 97 and 98.

- The server logs each as an unknown player packet. After three, it reports the player as
  sending invalid packets and closes the connection.
- No file is created. The handlers exist only for RC connections, and even there an upload checks
  a protected-file list, not folder rights.
- The 6.03r7 image describes its upload calls as working "only if the scripted RC has currently a
  file browser window open", for "uploading of files (into scripted RC)". So the in-game file
  browser is the scripted-RC staff feature, and on this server a game connection's upload ids go
  nowhere.

## Prop 81 (E#23, not settled)

- None of the 96 player variables that 6.03r7 scripts can read is a category, so a player-list
  script can't read prop 81 directly.
- The image has `openplayerlist` and `togglescriptedplayerlist` events. Opening the built-in list
  from a script needs a compiled bytecode delivery that this round did not build.

## Not run in groups B and C

- E#423: the original 1.3 server and test client are in the lab VM, but there wasn't time.
- E#424: RC2 2.05 under Wine draws text as boxes and never connects.
- E#425: its outlook is a static read.
- E#618: Mirae has no Mac guest that runs the 6.0x Cocoa builds.
