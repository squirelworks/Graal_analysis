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
| 5.12 | kicked: "Received illegal data (2) from game server" | no | no |
| 5.24r3, 5.24r4 | yes | yes | 5.24r4: full set of tests |
| 6.00 beta1, beta2 | yes | yes | login only |
| 5.30r3 | yes (clock set back) | yes | push, lift, throw, sword |
| 5.31r4 | yes (clock set back) | after the warp below | walk |
| 6.00r2, 6.00r4 | yes (clock set back) | no: the window never paints and the client stops pinging after its first downloads | no |
| 6.03r7 | yes | after the warp below | full set of tests |

## Lab setup, and what it took

1. **Server.** GServer-v2 runs as the game server named `Login`, on the port the clients use for the login server (14900). The world folder is the 2.22 file set: levels, `pics1.png`, heads, bodies, swords, shields and ganis.
2. **Tokens.** The stock gs2lib knows `G3D14097` (5.12), `G3D26090` (5.30–6.00r4) and `G3D0311C` (6.03r7), but not `G3D15010` (5.24 and 6.00 beta2) or `G3D03048` (6.00 beta1).
   - For an unknown token the server falls back to older file packets. The 5.24 client then saves files under names like `1.png<PNG data>…` and logs "Couldn't open … for writing". **[wire]**
   - A lab copy of the library with two token strings renamed fixes this. `G3D14097` was renamed to `G3D15010`, and `G3D3007A` to `G3D03048`. **[srv]**
3. **Beta expiry.** 5.30r3, 5.31r4, 6.00r2 and 6.00r4 run only with the clock set back.
   - Setting the clock back only for the start is not enough. When the clock jumps forward again, the client shows "You have been disconnected due to inactivity".
   - The clock has to stay back for the whole session. The server, on the same machine, then also runs in the past, so its respawn timers are useless in those runs. **[wire]**
4. **Gani headers.** The 2.22 ganis have no `GANI0001` first line. 88 world ganis were given one, as the 5.x bundled ganis have it. This made no visible difference by itself (see the next section).
5. **Wine.** No renderer change was needed. Mouse-click the window once so that it takes keys. Hold each key for at least 150 ms: shorter taps are missed.

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

**Tiles in 5.31r4 and 6.03r7.** Before the warp these two draw no tiles at all, only chests and image NPCs. 5.24 and 5.30r3 draw them. After the warp, with a GS2 weapon `-System` given to every player that calls `addtiledef("pics1.png", "", 0)`, both draw the full level. Whether the warp alone is enough was not separated. **[shot]**

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

### Chat text

Chat was set by the server (own props 9 and other-player props 8, prop 12), because neither Tab nor Enter opens a chat bar in these runs. With no server GUI scripts there is no chat bar on screen. **[wire][shot]**

- **Look.** There is **no bubble**. The text is drawn above the head, centred, in a light colour with a blue outline, on one line. A long line is not wrapped: it runs past the edges of the view. **[shot]**
- **Font.** 5.24r4 uses a plain sans font (its config says `font=Arial`). 6.03r7 uses a script-like font (its config says `font=Tempus Sans ITC`, `fontsize=24`). Nicknames under the feet use the same style. **[shot]**
- **Timeout.** The client cleared its own chat **2.97–2.99 s** after the server set it, sending prop 12 as empty. This happened in both builds and every time. **[wire]**

## For Seihai profiles

- A **5.x/6.x profile** draws chat as outlined text above the head, with no bubble, and clears its own chat after about 3 s. The 5.24 font is Arial. The 6.03 font is Tempus Sans ITC.
- The movement timings above (walk 0.5 tile per tick, push at 0.9 s, lift 6 ticks, sword 5 ticks with the cut on swing start) are the same as in 2.05.
- The **only new mannerism on the wire** is the trigger action `pushed,0`, sent once a second while pushing.
- The **server** decides the tile respawn time and bush items. A Seihai-compatible server for these clients needs to:
  - use a game server name that does not start with "login" (or warp there with 178);
  - know the tokens `G3D15010` and `G3D03048`;
  - serve `basepackage.gupd` and `tiledefs<server>.txt`;
  - provide tile definitions. On 5.31 and later this was done with a script calling `addtiledef`.

## Still open

- **5.12**'s kick for "illegal data (2)" through this proxy. The v5 thread reports 5.12 working through its own proxy.
- **6.00r2 and 6.00r4** stop after the first file downloads and never paint under Wine.
- **Typed chat.** A chat bar was not found without server GUI scripts.
- Not tested here:
  - hiding (D while carrying);
  - pots and stones (none in the start level);
  - hurt, swim, grab and pull.
- The tile-definition rule: whether 5.31+ needs `addtiledef` or only the warp.
