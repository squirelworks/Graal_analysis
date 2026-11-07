# 2dadventureclient, behaviour by behaviour

Source: `xtjoeytx/2dadventureclient` at `78040b7` (2020-02-29), read-only.
Files: `server/src/TGameWindow.cpp`, `TClient.cpp`, `TAnimation.cpp`,
`TImage.cpp`, `TLevel.cpp`, `TPlayer*.cpp`, `bin/data/`. Tags as in
`README.md`.

## What it is

The tree is GServer-v2 (the 2020 code, with the V8 NPC server) renamed
`TServer` to `TClient`, plus an SDL/guichan window. At start it loads the
local account `localplayer`, makes a `TPlayer` for it with no socket, marks it
local and adds it to the server's own player list **[2dac]**. It still opens
the listen socket, so other clients can join it. There is **no client-side
network code**: no login builder, no codec, no `PLO_*` handlers. Every
"client" behaviour is the server's own object model drawn to a window.

Consequence: it has not been run against real servers as a client, and it
cannot tell us anything about the wire from the client's side. What it can
show is how GServer-v2 reacts to a client that writes props, which is already
covered in `server-notes/`.

## Walking and collision

| point | reference **[2dac]** | real clients | verdict |
|---|---|---|---|
| step size | `16 * 0.30` px per axis, truncated to 4 px because the step is an `int` | half a tile (8 px), 1.0 on foot, 1.2 fast (`decomp-findings-2026-10-25-l/01-walking-body-box.md`) **[2.05]** | invented |
| cadence | one step per drawn frame, frame capped at 60 fps, so about 240 px/s (15 tiles/s) and slower if the frame rate drops | one step per 50 ms, 10 tiles/s (Seihai `walk-pace.md`) **[cap]** | invented |
| keys | up, left, down, right all summed into one move; facing is the last held key in that order (right wins) | each key is its own tested step, in the order up, left, down, right **[2.05]** | invented |
| wall test | one point, `(pixelX + move + 32) / 16`, `(pixelY + move + 44) / 16`, so tile (x + 2, y + 2.75) | six points on the leading edge of the box x+0.5..2.5, y+1..3; first four must be free; 0.1-tile corner nudge; snap within 0.0625 **[2.05]** | invented; already recorded in `archival/foot-test-sdl.md` |
| wall rule | `tiletypes[id] >= 20`, off-board is wall | per-tileset rule; default tileset uses `arrays.dat` lists (`decomp-findings-2026-10-28-b/01-tile-type-tests.md`) **[2.05]** | GServer's table, not the client's rule |
| water, lava, chairs, beds | `isOnWater` exists, never called by walking | swim, lava burn, sit **[2.05]** | missing |
| chests, NPCs, other blockers | not tested | chest 2 x 2 and blocking sprites block **[2.05]** | missing |
| refused step | nothing happens | position put back, "pushing" state starts **[2.05]** | missing |

Nothing here is worth adopting. Seihai's body box is the better reference.

## Position on the wire

The local player writes props 78/79 (`PLPROP_X2`/`Y2`, pixels, low bit =
negative) and then sprite and gani props **[2dac]**. Those are the 2.3+
precise props (`protocol/player-props.md`). 2.05 and 2.22 send half-tile
props 15/16 **[2.05][cap]**. The server then derives the half-tile value as
`x2 / 16` for older viewers **[srv]**. Keep Seihai's per-version choice.

## `gr.x` / `gr.y`

Not a client feature: see `README.md`. The local account here carries
`WEAPON -gr_movement` like the stock server's default account **[2dac][srv]**.

## Levels, links and gmaps

| point | reference **[2dac]** | real clients | verdict |
|---|---|---|---|
| level formats | the server's loader (GLEVNW01, GR-V1, Z3-V1, gmap) | same set by version (`build-catalogue.md`) | nothing new; see `formats/` |
| links | never tested for the local player, so doors do nothing | the client tests links on its own walk **[2.05]** | missing |
| gmap | draws every level of the map at its grid offset | crosses levels by walking (Seihai `gmap_cross` lab runs) **[cap]** | drawing only; walking stops at the level edge because off-board is a wall |
| camera | centred on the player's level-local pixel position, clamped to the map size | follows the player across the map | the camera ignores the gmap offset, so it is wrong outside the first level |

## Drawing

| point | reference **[2dac]** | real clients | verdict |
|---|---|---|---|
| tile id to sheet | `col = (id / 512) * 16 + id % 16`, `row = (id % 512) / 16` | the same (`client-assets.md`) | **matches** |
| tileset | hard-coded `zold_tiles_dusty_01.png` | `pics1` or the level's `addtiledef` | invented for their own world |
| chests | 2 x 2 tiles from sheet cells (56, 15) closed and (29, 19) open; open if the local player's chest list has it | those cells are ids 1784 and 829, the closed and opened chest ids in the 2.22 `arrays.dat` (Seihai `chest-drawing.md`) | **matches** |
| draw order | players and NPCs together, sorted by pixel y | height layers: `drawunderplayer`, default, players, `drawoverplayer`, `drawaslight` (Seihai `npc-draw-order.md`) **[2.05]** | invented; y-sort would break NPCs that rely on `drawoverplayer` |
| image files | only `.png` gets a texture; a `.gif` is registered and draws nothing | the classic packages ship `.gif` sheets (1.21 has `letters.gif`, `sprites.gif`, `pics1.gif`); later builds take `.png` too | limitation |
| names and chat | nickname centred at (x + 24, y + 44), chat at (x + 24, y − 34), TTF font, black 1-px shadow | chat drawn by the name routine, stacked up from the head, no balloon (Seihai `chat-log.md`) **[2.05]** | font and offsets are invented; not checked against the real offsets |
| HUD | an FPS counter and a test window | `state` sheet HUD (`status-display.md`) | missing |

## GANI playback

| point | reference **[2dac]** | real clients | verdict |
|---|---|---|---|
| step timer | one timer per loaded `.gani`, shared by every object using it, advanced by `3 * frame time` against `0.05` | each object steps on its own; the wait counter starts at 1 and `WAIT` adds to it (`formats/gani.txt`) | invented |
| `WAIT`, `PLAYSOUND` | skipped | hold and sound cue | missing |
| `LOOP`, `CONTINUOUS`, `SETBACKTO` | parsed, not used | used | missing |
| `ATTR1`, `PARAM` | `ATTR1` draws nothing | attribute sprites (`body-colours-and-attributes.md`) | missing |
| body colours | none | palette per slot **[2.05]** | missing |
| `shadow` sprites | drawn at 2/3 alpha | not checked | unknown |
| placement rows | split on spaces, read as triples with `atoi` (works for `a b c, d e f` only because `atoi("c,")` stops at the comma) | comma-separated placements | accident, don't copy |

Seihai's `walk-gani.md` already steps one frame per walk step and lists the
real `WAIT` timing as open. The reference does not close that gap.

## Chat and commands

Typing in the bottom field sets the chat prop on the local player **[2dac]**.
The server's chat commands then run with the local player treated as admin:
`warpto` and `.ul` skip the rights checks when the player is local **[2dac]**.
That is a convenience of the fork, not a real-client behaviour.

## Bottom line

The fork shows GServer-v2 from the inside, which `server-notes/` already
covers from the full GServer source. As a client it is an early prototype:
every client behaviour it has is simpler than what the 2.05 and 2.22 notes
record, and several (y-sorted drawing, shared GANI timers, 15 tiles/s walking)
would visibly break the feel if copied. Its two correct details (the tile
sheet mapping and the chest cells) Seihai already has.
