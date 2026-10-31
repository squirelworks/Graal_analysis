# Graal 5.x and 6.x Windows clients on a lab server

Date: 2026-10-30. The unpacked builds from `v5v6-windows-unpacked.md` were run under Wine against a local GServer-v2 (OpenGraal GS2Emu), with a proxy in between that decodes both directions and can add server packets. This page covers what the server has to send for these clients to play, what the clients send back, and how they behave in play.

Tags:

- **[wire]** seen in the decoded traffic.
- **[shot]** seen in a screenshot.
- **[srv]** behaviour of the lab server, not of an original Graal server.
- **[inf]** inferred.

Timings come from the client's own messages. A moving client sends its position every 50 ms, so they are good to about one 50 ms tick.

The lab tools, the key scripts, the proxy logs and the screenshots are in the project folder under `graal-decompile/unpacked-installers/lab-v5v6/`.

## What was run

| Build | Logged in | Level drawn | Played |
|---|---|---|---|
| 5.12 | yes, through the proxy (see "5.12's cipher step count") | yes, after the warp | walk |
| 5.24r3, 5.24r4 | yes | yes | 5.24r4: full set of tests, plus pots, stones and hiding |
| 6.00 beta1, beta2 | yes | yes | login only |
| 5.30r3 | yes (clock set back) | yes | push, lift, throw, sword |
| 5.31r4 | yes (clock set back) | after the warp below | walk |
| 6.00r2, 6.00r4 | yes (clock set back) | under Wine no: freezes after the first image. **On Windows 11 yes** (see "6.00r2 and 6.00r4 on real Windows") | on Windows: walk, hurt |
| 6.03r7 | yes | after the warp below | full set of tests, plus black stone and hiding |

## Lab setup, and what it took

1. **Server.** GServer-v2 runs as the game server named `Login`, on the port the clients use for the login server (14900). The world folder is the 2.22 file set: levels, `pics1.png`, heads, bodies, swords, shields and ganis.
2. **Tokens.** The stock gs2lib knows `G3D14097` (5.12), `G3D26090` (5.30–6.00r4) and `G3D0311C` (6.03r7), but not `G3D15010` (5.24 and 6.00 beta2) or `G3D03048` (6.00 beta1).
   - For an unknown token the server falls back to older file packets. The 5.24 client then saves files under names like `1.png<PNG data>…` and logs "Couldn't open … for writing". **[wire]**
   - A lab copy of the library with two token strings renamed fixes this. `G3D14097` was renamed to `G3D15010`, and `G3D3007A` to `G3D03048`. **[srv]**
   - The v5 lab renamed `G3D26090` instead (`version-profiles/lab-v5-2026-10-30.md`). Which slot does not matter for files as long as it is at or above 2.14. The rule and the byte walk of the bad name are in `file-transfer.md`.
3. **Beta expiry.** 5.30r3, 5.31r4, 6.00r2 and 6.00r4 run only with the clock set back.
   - Setting the clock back only for the start is not enough. When the clock jumps forward again, the client shows "You have been disconnected due to inactivity".
   - The clock has to stay back for the whole session. The server, on the same machine, then also runs in the past, so its respawn timers are useless in those runs. **[wire]**
4. **Gani headers.** The 2.22 ganis have no `GANI0001` first line. 88 world ganis were given one, as the 5.x bundled ganis have it. This made no visible difference by itself (see the next section).
5. **Wine.** No renderer change was needed. Mouse-click the window once so that it takes keys. Hold each key for at least 150 ms: shorter taps are missed.

## 5.12's cipher step count

Connected straight to GServer-v2, 5.12 logs "Received illegal data (2) from game server" and is dropped. The message means a frame decoded to nothing. **[wire]**

The cause is in 5.12's frame decoder (`Graal3DEngine.dll`, read from the decompile):

- For zlib frames (type 4) and bz2 frames (type 6), it steps the gen-5 iterator **len / 4 times, rounded down**. That is still capped at 4.
- For uncompressed frames (type 2) it rounds up, as every later build does in both cases.

So any compressed frame shorter than 16 bytes whose length is not a multiple of 4 leaves 5.12 one iterator step behind the server. From then on every frame is garbage. 5.12 encodes the same way when sending, and it sends even short bodies compressed (`v5v6-windows-unpacked.md`), so the server side goes wrong too. **[bin][wire]**

- **The proxy's fix.** For the 5.12 token, decode the client with round-down stepping and re-encode for the server with the normal rule. Towards the client, send everything zlib-compressed with round-down stepping.
- With that, 5.12 logs in, warps and plays, with no illegal-data errors. It also shows its own "Players: 1 online" window and the spaced-out window title. **[wire][shot]**
- An original 5.12-era server must have stepped the same way as 5.12. A server for a 5.12 profile has to as well.

## The "Login" server mode

The first thing every build does is load "tile definitions for server Login". While the current server's name is `Login`, these clients:

- draw no characters: not the own player, not other players, not gani NPCs;
- draw no HUD;
- never request `sprites.png`, heads or bodies.

The level, chests and image NPCs are drawn, and the player walks and sends positions. A D3D9 trace of 5.24r4 shows a constant 144 draw calls per frame, with nothing added when another player is sent. So this is the client choosing not to draw characters, not a rendering fault. **[wire][shot]**

The v5 thread found the cause in the binary. The draw-layer mask is cut down while the server name starts with "login". This is the login lobby mode: the real login server is not meant to be played on.

- **Fix.** After the login burst, send **S→C 178** (server warp) `0,Lab Server,127.0.0.1,14900`.
- The client drops the connection, logs in again under the new name, and then draws the player, the HUD (A/S/D boxes, hearts, rupees, bombs, arrows, the AP bar), other players and their nicknames. **[wire][shot]**
- The lab does this with the proxy. GServer-v2 only sends 178 when its listserver answers a server-info query.
- Confirmed on 5.24r4, 5.31r4 and 6.03r7. 5.12 and 5.00r7 were confirmed by the v5 thread.

**Tiles in 5.31r4 and 6.03r7.** Before the warp these two draw no tiles at all, only chests and image NPCs. 5.24 and 5.30r3 draw them. After the warp, with a GS2 weapon `-System` given to every player that calls `addtiledef("pics1.png", "", 0)`, both draw the full level. **The warp alone is enough:** with the `-System` weapon removed from the server and the account, 5.31r4 still drew the full level after the warp, and its log shows no script running. Before the warp it drew only chests and image NPCs, as before. **[shot]**

After the warp the clients also ask for `tiledefs<server name>.txt` (here `tiledefslab%032server.txt`, with the space written as `%032`). The lab server did not have the file. **[wire]**

## The session on the wire

The same flow is seen in every build that logs in. The server side is GServer-v2's, so this shows what these clients accept, not what an original Graal server sent. **[wire]**

**Server, first burst after the login frame:**

- 25 (signature)
- 168
- 9 (own props)
- 194 (clear weapons)
- 34 Bomb, 34 Bow
- 43
- 33 (weapon `-gr_movement`; the GS1 script is sent empty to these clients)
- 190
- 14 (warp to `onlinestartlocal.nw`, x 30, y 30.5)
- 6 (level name)
- 100 + 101 (board)
- 39 (mod time)
- 0 (empty)
- 4 × chests
- 174
- 10
- 42 (world time, every few seconds after)
- 156 (active level)
- 3 (level NPCs)
- 179 (start message)
- 41 (server HTML message)
- 82
- 47 (staff guilds)
- 180 (status list)
- 182 (window list request)

**Client:**

- 37 `English` (language).
- File requests:
  - **23** (plain);
  - **34** (with the cached file's time; the server answers 45 "not modified");
  - **47** (with time, for `basepackage.gupd`).
- The server answers each with a file (100 size + 102 data), or 30 "not found", or 45.
- **44**, the window list, as the answer to 182: `Select File,Lab Server,Default IME,Default IME`.
- **2**, own props: nickname, colours, language, `win`, then the position.
- **157** with a gani name, each time the client needs a gani it has not checked yet. The server answers with 195 (the gani's attributes, e.g. `SETBACKTO`).
- **158** with a weapon name (`-System`), to fetch a GS2 weapon. The server answers 140 / 197 (bytecode and its hash).
- **24**, keep-alive, every 5.1 s.
- **38** (trigger action) with `leftmouse` when the window is clicked.

**Files a played session fetches.** The Themida builds bundle nothing, so they ask for all of these. The MoleBox builds bundle only GUI images, so they ask for them too.

- After the warp: `sprites.png`, `body.png`, `head0.png`, `shield1.png`, `state.png`, `sword1.png`, `wbowi1.png`, `wbomb1.png`, `pics1.png`, the ganis as they are used, and the step and action sounds.
- A bold font: `arialbd.ttf` in 5.24, `tempsitcbd.ttf` in 6.03r7.
- `basepackage.gupd`, which a minimal `GRPKG001` file with only `NAME`, `VERSION`, `PLATFORM` and `MODE` satisfies.

## Play: what the client does

Tested on 5.24r4 and 6.03r7, with push, lift, throw and sword also on 5.30r3. The three builds agree on every point below. The 2.05 column is from `client-internals/player-mannerisms-live.md`.

| Action | 5.24r4 / 5.30r3 / 6.03r7 | 2.05 rev 2 |
|---|---|---|
| walk | x2/y2 sent every 50 ms, **8 pixels (0.5 tile) per tick** straight | 0.5 tile per tick |
| run into a bush/wall | `walk` keeps going, **`push` 0.85–0.90 s** after the walk started | push on the 18th blocked tick (0.9 s) |
| while pushing | the client sends **38 `pushed,0`** about 0.55 s after `push` starts, then every **1.0 s** | – |
| lift (A at a bush) | `lift` and the board change in the same tick as the key; **`carrystill` 0.30 s later** | `lift` 6 ticks, then `carrystill` |
| carrying | the bush is drawn over the head; the head is hidden behind it. Walking plays `carry`. | the same |
| throw (A while carrying) | **11** (throw) and `idle` in the same tick; carry sprite back to −1 | `idle` in the same tick |
| sword (S) | `sword` and the bush cut (**1**, board change) in the **same tick as the swing starts**; `idle` 0.25 s later (5 ticks) | cut on the first swing frame, 5 ticks |

These are all **[wire]**, plus **[shot]** for carrying.

### What the bush messages look like

- **Lift and sword cut.** The client sends **1**, a board change: x 30, y 16, 2 × 2, the four tiles 677, 678, 693, 694. The server echoes it as **7** to the level. **[wire]**
- The client sends nothing for items dropped from the bush. With `bushitems = true`, the item drop is the server's. **[wire][srv]**
- **Carry sprite.** Prop 19 goes to 1 for the bush while it is carried, then back to −1 when it is thrown. **[wire]**
- **Respawn.** The server puts the bush back by sending **7** with the tiles 2, 3, 18, 19, **14.6 to 14.7 s** after the lift or cut. This is GServer's `respawntime = 15`, a server setting. These clients have no respawn timer of their own for tiles. How long an original Graal 5.x/6.x server waited is not known from this lab. **[wire][srv]**

### Pots, stones and hiding

The level had a pot, a light stone and a black stone put in the player's path. The account had glove power 3 (`GLOVEP 3`). Tested on 5.24r4; the black stone and bush hiding were repeated on 6.03r7 with the same results. **[wire][shot]**

| Object | Lift (C→S 1) leaves tiles | Carry sprite (prop 19) | D (hide) | Server reply |
|---|---|---|---|---|
| bush | 677, 678, 693, 694 (stump) | 1 | hides | – |
| pot | 1770, 1771, 1786, 1787 (the empty base) | 5 | **nothing** | S→C 22: item 5 (a heart) at the pot |
| light stone | 1834, 1835, 1850, 1851 (a hole) | 3 | hides | – |
| black stone | 1834… (the same hole) | byte 0xE9 | hides | – |

- **Hiding** (D while carrying a bush, light stone or black stone):
  - The pose becomes `hiddenstill`, and prop 18 (status) goes from 20 to **22**, which sets the hidden bit 0x02.
  - Only the carried object is drawn, where the player stands. Body, head and shadow are gone. **[shot]**
  - Walking hidden plays `hidden` and moves **1.5 px per tick** (y2 steps of 2 and 1 px, alternating). That is about 0.1 tile per tick, as in 2.05.
- **Leaving the hiding place.** D again, or A, goes back to `carrystill`, and status goes back to 20. S while hidden throws (C→S 11).
- **Carrying.** The pot or stone is drawn over the head, as with the bush.
- **Throwing a pot.** The heart dropped by the server stays on the pot base.
- All of this matches the 2.05 rules in `client-internals/carry-hide-and-glove.md`. The 4.04r2 lab (v4 thread) got the same carry sprites and tiles.

### Grab, pull, hurt and swim

Tested on 5.24r4 and 6.03r7, and the two builds agree. For the grab test the account had glove power 1, so a black stone could not be lifted. **[wire][shot]**

| Action | What the client does |
|---|---|
| grab (A against a stone it cannot lift) | `grab` in the next tick (0.04–0.05 s) |
| pull (Left held with A held, facing the stone) | `pull` in the next tick. The player does not move, and the stone stays put. Dust puffs are drawn at the feet. |
| while pulling | the client sends **38 `pulled,1`** 0.85 s after `pull` starts |
| hurt (an explosion, S→C 36, at the player) | `hurt` and the hearts in the same tick (3 → 2.5 for power 2). The player is pushed back **5 tiles in 5 ticks** (1 tile per tick, twice walking speed) and blinks. `idle` comes **1.54–1.55 s** after the hit. |
| swim (walk into deep water, tile 322) | `swim` in the same tick as the first water step. Swimming moves at walking speed (0.5 tile per tick). Only the head is drawn, with a ripple, and sideways strokes throw splashes. Stepping out goes back to `walk`. |

- 5.24r4 drew the explosion as a large flame cross. In 6.03r7 the 0.15 s screenshot showed no flame. Both left a crater and scorched the stone. **[shot]**
- A hurt packet sent directly (S→C 40) changed nothing in 5.24r4, whether the attacker id was 0 or a player that had been added. Only the explosion hurt the player. **[wire]**
- `pulled,1` is the second trigger action, after `pushed,0`. **[wire]**

### Chat text

Chat was set by the server (own props 9 and other-player props 8, prop 12), because these clients have no chat bar of their own. Tab, Enter and F3 open nothing, and typing in play just presses the game keys (S swings the sword). Escape opens a "Do you really want to quit Graal?" dialog. On these versions the chat bar is a server-side GUI script. **[wire][shot]**

- **Look.** There is **no bubble**. The text is drawn above the head, centred, in a light colour with a blue outline, on one line. A long line is not wrapped: it runs past the edges of the view. **[shot]**
- **Font.** 5.24r4 uses a plain sans font (its config says `font=Arial`). 6.03r7 uses a script-like font (its config says `font=Tempus Sans ITC`, `fontsize=24`). Nicknames under the feet use the same style. **[shot]**
- **Timeout.** The client cleared its own chat **2.97–2.99 s** after the server set it, sending prop 12 as empty. This happened in both builds and every time. **[wire]**

## 6.00r2 and 6.00r4 on real Windows

Under Wine, 6.00r2 and 6.00r4 freeze on a blue window right after they write the level cache and receive the first image. On 2026-10-30 both builds were run on a real Windows PC instead (personal machine; OS build and GPU details redacted). **[shot]**

**Future runs:** loopback-only labs (the loopback address / a second loopback address, in a container, VM or CI). Do not use Squirrel's own machines again.

- **Setup:**
  - a real Windows 11 PC with DirectX 9 hardware (machine identity redacted);
  - the original Themida-packed `GraalSetup.exe` from each installer archive, renamed `Graal.exe`;
  - the date faked for the game process only with NirSoft RunAsDate (2011-06-14 for r2, 2011-06-28 for r4);
  - a hosts line pointing `<login-host>*` at a GServer-v2 beta4 on the same LAN (`<lan-host>`; historical — future runs use loopback).
- **No freeze.** Both builds write the level cache, receive the first image and keep running. They download every file and draw the full level, the player, baddies and the HUD. Arrow keys walk the player, and a baddy's hit takes the hearts from 3 to 2.5. **The freeze is a Wine problem**, not something in the client or the server.
- **On today's date** the packed builds write the "This is a beta release" text to `game_console.log` and exit after about 1 s, before any window opens.
- **The memory dumps don't run on Windows.** The unpacked `Graal.exe` files from `v5v6-windows-unpacked.md` crash at once on Windows (entry point 0, import table full of Wine addresses). They are for reading in Ghidra only.
- **What the server had to do:**
  - serve every file, since these builds bundle nothing: `basepackage.gupd`, `pics1.png`, the sprites, heads, bodies, swords and shields, the ganis and the sounds;
  - send the 178 warp after login. Without it the screen stays black apart from chat text. After it, the window title changes to the new server name and the client requests the images.
- **A server crash to know about.** GServer-v2 beta4 crashed (SIGSEGV) on every 6.00 login while it registered the GS1 weapon `-gr_movement` (the flaghack movement weapon). It took the GS2 bytecode branch for a weapon that has no bytecode. With that weapon removed, logins worked. **[srv]**

What the Wine runs found about the freeze, kept for reference:

- The last thing the game does is write the level cache (`weblevels/…/onlinestartlocal.nw-14900.code`) and receive the first image.
- It then stops reading the socket and never paints.
- The folder scan before login finishes ("Done.").
- Switching to OpenGL (`useopengl=1`, `-opengl`), turning wined3d CSMT off and using RGBA PNGs make no difference.
- The "This is a beta release" text is on the frozen main thread's stack, and nothing in the dumped 6.00r2/r4 code refers to it. So the expiry check runs inside Themida's own code, and it seems to run again after login. **[inf]**
- It is not the file dates. Setting every server file and the client's own files to June 2011 (with the clock set back) still freezes. **[cap]**
- Themida stops winedbg from attaching.

## For Seihai profiles

- A **5.x/6.x profile** draws chat as outlined text above the head, with no bubble, and clears its own chat after about 3 s. The 5.24 font is Arial. The 6.03 font is Tempus Sans ITC.
- The movement timings above (walk 0.5 tile per tick, push at 0.9 s, lift 6 ticks, sword 5 ticks with the cut on swing start) are the same as in 2.05.
- The **only new mannerisms on the wire** are the trigger actions `pushed,0`, sent once a second while pushing, and `pulled,1`, sent 0.85 s into a pull.
- Grab and pull start in the next tick, hurt pushes the player 5 tiles in 0.25 s and lasts about 1.55 s, and swimming is as fast as walking.
- There is no built-in chat bar. A profile for these versions needs a chat input of its own, the way the original servers supplied one.
- The **server** decides the tile respawn time and bush items. A Seihai-compatible server for these clients needs to:
  - use a game server name that does not start with "login" (or warp there with 178);
  - know the tokens `G3D15010` and `G3D03048`;
  - serve `basepackage.gupd` and `tiledefs<server>.txt`;
  - provide tile definitions. On 5.31 and later the warp off the "Login" server name was enough; an `addtiledef` script is not needed.

## Still open

- How a server-side chat bar script sends typed chat. That needs a GS2 GUI script like the original servers had.
- Why S→C 40 (hurt by a player) did nothing.
