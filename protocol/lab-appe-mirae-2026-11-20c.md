# Appendix E lab runs on Mirae, batch 3 (2026-11-20)

Date: 2026-11-20. Evidence: **[lab]**. Real clients under Wine in the Mirae Graal Linux RE Lab VM,
each in its own network namespace with loopback only. The servers are the original GServer 1.3
(1999) and the gs2emu lab worlds. A logging relay or the `gen5probe` proxy sits between client and
server. No public service was contacted. Captures and screenshots stay in the lab. Probe rows are
appended to [`probe-results.tsv`](probe-results.tsv). The earlier batches are
[`lab-appe-mirae-2026-11-20.md`](lab-appe-mirae-2026-11-20.md) and
[`lab-appe-mirae-2026-11-20b.md`](lab-appe-mirae-2026-11-20b.md).

## Level change and other-level props on GServer 1.3 (E#423)

Builds: original GServer 1.3 and the 1.3 test client (`GSERV014`), three clients (A, B, C). The
server and clients are unchanged. 1.3 frames are a 2-byte length plus zlib with no cipher, so a
plain relay logged both directions. The start level `onlinestartlocal.graal` holds a link to
`house2.graal` at (31, 26), 2 × 1, with arrival (24.5, 35). `house2.graal` was a copy of a stock
house level placed in the server folder. B walked north into the link.

**The level change**
- The first time, B sent `PLI_LEVELWARP` (0) with x 24.5, y 35 and `house2.graal`. The server
  answered with 100, the board, the links (1), the modification time (39) and 10.
- With the level cached (a second run), B sent `PLI_LEVELWARPMOD` (30) with the cached time,
  position and name. The server sent an empty id 0 in place of the board, then 10.
- A, left behind, got two id 8 messages about B:
  - prop 50 = 0 (B left the level);
  - prop 20 `house2.graal` with props 15 and 16 (24.5, 35).
  No nickname or head was sent.
- B got id 8 prop 50 = 0 for A.

**Changes made while B was in the other level** (each sent as B's own `PLI_PLAYERPROPS`)

| B sent | What A received |
| --- | --- |
| nickname (prop 0) | id 8 prop 0 with the new nickname, at once |
| head (prop 11) | id 8 prop 11 with one GCHAR, the head number. The text sent after the number was not passed on, so 1.3 reads prop 11 as a one-byte head number |
| colours (13), sword (8), chat (12) | nothing |

**C logging in while B is away and A is in the start level**
- About B, C got one id 8 holding: nickname, head (one GCHAR), x, y, level name, prop 30 and the UDP
  port (31). It held no hearts, sword, shield or colours.
- About A, C got the full set: hearts, sword, shield, colours, sprite, alignment and the rest.
- After C's first `PLI_PLAYERPROPS`:
  - A (same level) got C's nickname, head, colours and UDP port;
  - B (other level) got only C's nickname and head.

The nickname and head go to every player online, in every level. Colours and the UDP port go only
to the level. A level change tells the other players the new level and position.

**Prop limits.** A sent values over the limits. The server echoed some to A and announced some to
the level.

| A sent | Echo to A (id 9) | What C saw later |
| --- | --- | --- |
| max hearts 30 | 20 | |
| current power 60 (half hearts) | 40 | 40 |
| arrows 150 | 99 | |
| bombs 150 | 99 | |
| sword 9 | none | image form: 30 + 9 with an empty image name. Sword 9 was kept |
| shield 9 | none | image form: 10 + 3 with an empty image name. Shield became 3 |
| alignment 150 | none | 100 |
| glove 9, bomb power 9, gralats (3 bytes, each 127) | none | not in the level messages, so not seen |

## Combat checks on 1.21 (E#324): tried, not settled

Build: 1.21, One Player, offline. The start level was replaced with a corridor. An archer (type 3)
was penned behind a row of bushes: bush tiles block walking, and thrown objects fly over them.
Spare bushes lay behind the player.

- When the archer's arrows had a clear line to the player, the player died within about 2 s, and
  1.21 restarted the level. The bush row stopped the arrows.
- A thrown bush that reached the archer put it in its hurt state (its `hurt` text showed). Two such
  hits were seen. There was no kill in four lift-and-throw cycles. A lift missed, the next action
  key lifted the wall bush instead, the archer came through, and the player died.
- Lifting a bush in 1.21 left a drawn item on the emptied spot: a green gralat once, hearts at
  other spots. The item stayed on the ground. So 1.21 does draw ground drops, at least from bushes.
- A penned hare (type 5) did not react to a thrown bush. It stayed in its sleeping start state.
- Not run: the 2.17.1 archer scene, and a sword against a sword or a baddy's shield.

## Walking speed on 2.05 (E#302)

Build: 2.05 rev 2, online on a gs1classic copy with a lab start level. Speeds come from the
client's own position props, sent every 0.1 s, over a 1.5 s key hold. The run used glove 3.

| State | Speed (tiles per 0.1 s) |
| --- | --- |
| on foot, right and left | 1.0 |
| carrying a bush, sign, pot, light stone or black stone | 1.0 each |
| sword key held after a swing | 1.0 |
| shield power 0, 1 or 2 | 1.0 |
| **shield power 3** (2 runs) | **1.2** (steps alternate 1.0 and 1.5) |
| sword power 4, glove 1 | 1.0 |
| **riding** (horse added with id 17, walked onto) | **0.8** (steps alternate 0.5 and 1.0), with shield 1 or 3 |

- Riding uses factor 0.8, not the black stone. Carrying does not slow the walk for any object kind.
- Shield power 3 gives the 1.2 state.
- Factor 0.4 was not found in these states.

## Walking into a rock on 2.22 (E#304)

Build: 2.22 (`GNW03014`), online. A single 2 × 2 rock (tile 2055) stood at (30, 20)–(32, 22). The
player was placed at each x below with y 26 or 26.5, and walked up for 1.2 s. The body spans
x + 0.5 to x + 2.5.

| Start x | Overlap with the rock | What happened (wire values) |
| --- | --- | --- |
| 28 | 0.5, left edge | stops at y 21.0, x slides to 27.5, then walks on past |
| 28.5 | 1.0, left | stops at y 21.0, x 28.0 then 27.5 (0.1 s and 0.35 s after the stop), walks on |
| 29, 29.5 | 1.5 and 2.0 | stops at y 21.0, no slide |
| 30.5 | 1.0, right | stops at y 21.0, x 31.0 then 31.5, walks on |
| 31 | 0.5, right | stops at y 21.0, x 31.5, walks on |
| 31.5 | none | walks past |

- From y 26 the steps were 25.5 … 21.5, then 21.0. From y 26.5 they were 26.0 … 21.0. Both
  alignments stop flush at 21.0.
- Every x and y on the wire was a half-tile value. The slide passed through 28.0 between 28.5 and
  27.5.
- The client sends at most one position every 0.1 s, and the slide's step size is unknown. So these
  values do not separate truncation from rounding.

## Bush tiles placed as a stamp (E#100)

The ids 2, 3, 18 and 19 were placed as a 2 × 2 bush at (30, 20), with a rock control at (40, 20).
The player walked up into each from y 26 and 26.5. This was run on 2.22 and on 2.05 rev 2, each
with the world's stock `pics1.png`.

On both builds the bush stopped the player at y 21.0, exactly like the rock: three bush approaches
and two rock approaches per build. A stamped bush blocks.

## GS1 condition truth on 1.39 (E#200)

Build: 1.39 (`GNW07080`), online. Level NPCs set one global flag per true condition. The client
sends each flag as `PLI_FLAGSET` (18), so the proxy log records them. Each NPC sets a final flag
to show it finished.

| Condition | 1.39 |
| --- | --- |
| `(1+0)`, `(0.5+0)`, `(-0.5)`, `(0-1)` | **false** |
| bare `1`, bare `0.5`, `(0+0)`, `false` | false |
| `created`, `true` | true |
| `!(0+0)`, `!0` | true |
| `(1+0)&&(1+0)`, `(0+0)\|\|(1+0)`, `1 && 0 \|\| 1` | false |
| `playerx==playerx`, `this.a==1` (after setting 1), `strequals(#a,#a)` | true |
| `playerx!=playerx` | false |
| `1==1`, `1!=0`, `1<2`, `2>1`, `1=1`, `(1+0)==1`, `0==0` | true |
| `1==1.00001`, `0.1+0.2==0.3`, `this.a==1.00001` | true (compared with a tolerance) |
| `(1/0)`, `(0/0)`, `(-1/0)` | false |
| `(1/0)==(1/0)`, `(0/0)==(0/0)` | true |
| `(1/0)>1000000` | false |

- 1.39 differs from 2.05 to 2.31 in one way. A computed value standing alone, such as `(1+0)`, is
  false. `!` of a computed zero is true, and comparisons work.
- 1.39 does not fold constant comparisons the way 2.05 does. It compares with a tolerance.
- Division by zero gives a finite value: `(1/0)>1000000` is false and `(0/0)==(0/0)` is true.
  This fits a result of 0.

**Loops**
- `while (1)` ran 0 times, and so did `while ((1+0))`.
- `while (1==1)` ran until the client's loop limit (10,000 or more passes). The script then went on.
- `while (this.c<3)` ran 3 times.

**Malformed conditions**
- `if (1+)` and `if ()` count as false, and the script goes on.
- `if (abc def)` and `if ((1+0) set …` stop the script there: no later flag in that NPC was set.

## GS1 argument conversion on 2.05 (E#201)

Build: 2.05 rev 2, online. Level NPC scripts ran on `playerenters`.

**`puthorse` (stored letters `MRR`).** The client sends each horse as `PLI_HORSEADD` (7).

| Argument written as | Sent as |
| --- | --- |
| `ride.png` | `ride.png` |
| `#s(hs)` (holds `ride.png`) | `ride.png`, so the code is expanded |
| `"ride.png"` | `"ride.png"` with the quotes kept; no horse is drawn |
| `ride png` | `ride png`, with the space kept |
| x as `14+14` | 28 |
| x as `#s(nx)` (holds `26`) | 0 |
| x as `"30"` | 0 |

So the first argument is free text with message codes expanded. The numeric slots evaluate
expressions, and a string there becomes 0.

**`toinventory` (stored `S`).** Each form (`Lab Bare`, `#s(wn)`, `"Lab Quoted"`) sent its argument
as a `PLI_FLAGSET` (18) flag name, as written: the code was not expanded and the quotes were kept.
No weapon message was sent. A `toweapons` control sent `PLI_WEAPONADD` (33) with the NPC's id.

**`replaceani` (stored `MM`).** Bare `sit`, `#s(an)`, `"push"`, `dead hurt`, `sit,lift` and `idle`
were each applied 1 to 3 s before the player went idle. None changed the idle gani on the wire
(still `idle`) or on screen. So this setup could not observe conversion for `replaceani`.

**`showimg` (stored `RMRR`).** The images were placed at y 12, outside the view, so they were not
checked.

## Item draw order on 1.39 (E#317)

Build: 1.39, online. An injected other player stood at (30, 30), facing down. Items (id 22) were
injected around its body.

- A heart at (30.5, 31) and a green gralat at (31.5, 32) drew **over** the player.
- A heart at (30.5, 29.5), a green gralat at (31.5, 30) and a blue gralat at (31, 29) drew
  **behind** it.
- So 1.39 draws items and players in y order: an item covers a player only when its y is larger
  than the player's. The unit of the item sprite size was not read.

## Expiry dates of 6.00r2 and 6.00r4 (E#14)

Builds: 6.00r2 and 6.00r4, from their installer archives. Each archive holds one protected
`GraalSetup.exe`, which is the client itself and was run as `Graal.exe`. The method was the same as
for 5.30r3 and 5.31r4: libfaketime under Wine with the date at 12:00. A day passes when the client
dials the login host within 30 s.

| Build | Exe date in the archive | Last day it runs | First day it stops |
| --- | --- | --- | --- |
| 6.00r2 | 2011-06-13 | 2011-08-26 | 2011-08-27 |
| 6.00r4 | 2011-06-27 | 2011-09-08 | 2011-09-09 |

- A stopped build writes only its beta banner to the console, opens no connection and exits. This
  is the same as 5.30r3 and 5.31r4.
- 6.00r2 stops 75 days after its exe date, and 6.00r4 after 74 days. That is close to 5.31r4's 75
  days after its link date.
- A fresh 6.00r4 folder can take more than 30 s on its first start. One probe on a known good day
  timed out that way; a longer run of the same day dialled.

## `.mis` and `.dso` beside the 4.04r2 client (E#502, E#503)

Build: 4.04r2 (`Graal4.exe`) with its 3D plug-in, through the 3D lab login to the lab 3D server. It
went through mission phases 1 to 3 and took its control object. Wine's file trace was on.

- **`.mis`.** Marker missions were placed at four spots: `lab3d.mis` and `mission.mis` in the client
  folder, `levels3d/lab3d.mis` and `levels3d/missions/lab3d.mis`. Each starts with an `echo` line
  and defines a `MissionGroup`. They show up only in the client's folder scan (directory listing
  entries). None was opened. No marker reached the client's console. The mission was built from the
  network, as before.
- **`.dso`.** `main.cs`, `main.cs.dso`, `lab3d.mis.dso`, `levels3d/main.cs.dso` and
  `levels3d/lab3d.mis.dso` were placed. The `.cs` held an `echo`, and each `.dso` had a compiled
  script header and a marker. The result was the same: listed in the folder scan, never opened, no
  console output.
- So in a normal 3D session, 4.04r2 opens no `.mis`, `.cs` or `.dso` file beside it. A reader linked
  in but never called cannot be ruled out this way.

## Graal 2002 v22 login (E#15)

Build: Graal 2002 v22 (`GNW31101`). The stack was the lab listserver and a gs1classic copy behind
`gen5probe`, with a relay in front of the list port.

**The list exchange**
- The client sends list name `graal2002` and its account.
- The lab listserver answers with one row of 8 fields: name, language, description, empty URL,
  version, players, host (field 6) and port (field 7). That is already the shape ver10 accepts. A
  welcome line follows.

**Why the earlier Connect did nothing.** Without a Wine virtual desktop, a stale "Getting server
list" box stayed mapped over the list. With a virtual desktop (1024 × 768), the list was clean, and
selecting the row and pressing Connect opened the game connection at once. So the earlier failure
was the Wine display, not the list reply.

**Login capture**
- Login frame: type 0, generation 3 (one iterator byte per message), key 36, token `GNW31101`, then
  the account and password. The lab server logged the build as 2.1.
- The client's first messages: 37 (language, `English`) and 39 (10 bytes).
- The server sent 25, 168, 190, 194, 179, 41, 82, 47, 180, 9, 34 (`Bomb`, `Bow`), 43, 33 (two
  weapons), then 14, 6, 100, 101 (board), 39, 10, 156 and 3.
- The client then:
  - sent file checks (34) for its sword, shield, head, body and weapon images;
  - sent its first `PLI_PLAYERPROPS` (2, 35 bytes: nickname, head, colours and the rest), then 24
    with one byte about every 5.2 s;
  - ran the level's clientside GS1 NPC (an NPC prop counter every second) and the GS1 weapon
    (`gs1 timer ok` chat).
- The server sent 42 every 5 s.
- It stayed connected for the 30 s watched. Not done: send-site reads and the default-route
  fixtures.

## Frame timing of the early builds (E#300)

Builds: 4th Graal alpha, 5th Graal and 5th Graal alpha, unchanged, under Wine, One Player. Wine's
DirectDraw trace was on, with timestamps. After Start, each frame ends with one front-buffer Blt
and one vertical-blank wait. Timed over about 11 to 12 s in game:

| Build | Front-buffer Blts | Rate | Median gap | 10th to 90th percentile |
| --- | --- | --- | --- | --- |
| 4th Graal alpha | 220 in 10.8 s | 20.3 a second | 50.0 ms | 48 to 52 ms |
| 5th Graal | 241 in 12.3 s | 19.6 a second | 50.0 ms | 45 to 57 ms |
| 5th Graal alpha | 241 in 11.9 s | 20.2 a second | 50.0 ms | 48 to 52 ms |

- The frames follow the declared 50 ms interval in elapsed time, about 20 a second, on all three
  builds.
- The busy idle loop seen earlier is the DelphiX timer polling. It draws only when 50 ms have passed.
- Under Xvfb the in-game picture redraws only in part, but the draw calls run at full rate.

## Special start-level names entered by a link on 2.05 (E#319)

Build: 2.05 rev 2, offline (Training, then the F5 loader into a lab level). The lab level holds one
link into the target, with arrival (10, 10). The player walked into it. Each target ran with a
fresh client:
- `level1.graal` and `ctlone.graal` (a byte-identical copy);
- `YoshiClanR2.zelda` and `ctlr2.zelda`;
- `YoshiClanFields.zelda` and `ctlfields.zelda`.

- Every pair arrived at (10, 10), with the same facing, HUD and level, and no move to (31, 31).
- Screenshots of each pair differ only in animated tiles and the player's animation frame.
- Together with the F5 loads of the first batch, neither the F5 path nor the link path shows a
  special step. If one exists, it is on the new-game path only.

## Latin-1 text on 5.00r7 (E#213)

Build: unchanged 5.00r7, online, Wine's default Western code page. The player's own chat (prop 12)
and nickname (prop 0) were set by `PLO_PLAYERPROPS` to the text "Français éüñ" in Latin-1 bytes
(ç as byte 231).

- Both drew as "Français éüñ" above and below the player.
- A second chat with more `ç` letters drew them too.
- This uses the chat and nickname drawing, not `showtext` or a sign. 6.x was not checked.

## 4.04r2 offline scene on Windows (E#610, E#611): not run

These need the Windows guest, and driving it needs a direct request from the owner, so they were
left for that.

## Mac 6.004 and 6.015 frame (E#618): not run

Neither Mac guest has working OpenGL.
- On Mirae: the PowerPC Tiger (10.4.5) guest under QEMU has no OpenGL. The Mac 4.x and 5.x clients
  needed a render shim there, and drew a black captured display without it.
- The Lion guest on GwenTea2 also lacks OpenGL (see the 2026-11-16 note).

What the builds need:
- Both builds are universal (PowerPC 7400, i386 and x86_64), and their `Info.plist` names no
  minimum system.
- The PowerPC slice links OpenGL, AppKit, Foundation, OpenAL, AudioToolbox and AudioUnit. A 10.4.5
  system may not have OpenAL; this was not checked in the guest.
