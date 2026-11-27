# Interiors in the same world: doors without a world switch on a real 5.12 (2026-11-27)

Date: 2026-11-27. Lab: the real Windows **5.12** under Wine 10 with Mesa llvmpipe and Xvfb in a
headless Debian lab VM, one private loopback network namespace, against **seihai-gserver
`4dee422`** (branch `claude/project-thread-mk0uvs`, `portal` lines) serving a world made by
**seihai-pw3d `28ff6cc`** (same branch name in seihai-servertools) from a sample 2D playerworld
(a start level with a door link into a one-room interior). Derived results only; captures,
traces and screenshots stay in the owner-held lab kit. **[lab]**

Question from the owner: can the 2D-to-3D converter also build house interiors and other inner
levels, follow the links so a door takes the player in and back out, and not draw the house from
outside?

## Why not a world switch per door

A `g3dworld` switch on a 5.12 resends the whole terrain (the chunk cache is per server name), needs
a second `MissionStartPhase2` to light it, and a switch to a world with no terrain, water or Sun
stalled the client ([3d-worldswitch-terrain-lighting-512-2026-11-26.md](3d-worldswitch-terrain-lighting-512-2026-11-26.md),
[3d-big-world-streaming-512-2026-11-27.md](3d-big-world-streaming-512-2026-11-27.md) §5).

## The layout

- The start level and each gmap are **hubs**. Every other level a hub's links reach, through other
  interiors (a house's cellar), is placed **in the hub's own world**, in rows starting 1536 units
  south of it and 1536 apart.
- 1536 is past the 5.12's draw cut (an object whose centre is over about 1000 to 1050 units from
  the camera is not drawn, T3D-075) and past the server's default scope radius plus hysteresis
  (1100 + 200).
- The walker weapon keeps each level's walk grid in its own coordinates plus where it stands in
  the world. A door into the same world is a move of `player.position`; `g3dworld` goes only when
  the server world changes.
- Each door gets a world-file line `portal <x> <y> <z> <radius> <to x> <to y> <to z>`. With
  `graal3d_scope` on, a player within the radius also has the objects round the far side in scope.

## Results

The arrow keys did not reach `keydown2` under Wine and Xvfb in this VM (Escape and mouse clicks
did), so the lab copy of the walker followed a fixed route: to the door, 10 s inside, out through
the exit, 10 s outside. The rest of the walker was as generated. Each run was done twice, with a
screenshot every 0.5 s and every 0.12 s; both agree.

| | A: scope on, portals | B: scope on, no portals | C: scope off |
|---|---|---|---|
| `g3dworld` at a door | none | none | none |
| Position after entering | the link's landing tile plus the interior's place, exactly | same | same |
| Position after leaving | the exit link's landing tile, next to the door | same | same |
| Room comes into scope | 0.9 s before the door (portal radius) | 0.02 to 0.15 s after the door | at join |
| Land comes back | never left scope (the landing tile is inside the exit portal's radius) | 0.15 s after the exit | always there |
| Sky-only frames, in / out | 0 / 0 | one frame each, under 0.23 s | 0 / 0 |
| Land drawn while inside | no | no | no |
| Room drawn from outside | no | no | no |
| Link held, no freeze, no GS2 errors | yes | yes | yes |

- The shapes were already in the client's cache; on a first visit run B's gap also holds the
  file download. Run A's prefetch covers that too.
- **Conclusion:** on a stock 5.12, interiors placed in the same world 1536 units out, with portal
  prefetch under scoping, give doors with no stall, no terrain resend, no relight and no empty
  frame, and nothing of the outside is drawn inside or the other way round. **[lab]**

## What the stock path cannot do

- **Sky and light are the outdoor ones** inside: the same Sky and Sun ghosts serve the whole world.
  The room is lit as if outdoors and the sky box shows round it. Swapping Sky or Sun ghosts while
  the player is inside has not been tried (a world with neither stalled the client at a switch).
- Interiors must be far apart (1536), because the only culling is the client's distance cut.
- A TCP warp straight into an interior's level still switches to that level's own world.

## The seihai3d path: indoor spaces (proposed bit for the next extension version)

For our own client on the opt-in `seihai3d` extension ([seihai3d-ext-v1.md](seihai3d-ext-v1.md)),
proposed as a new bit `spaces` in the next version (a released bit never changes meaning):

- After the reply, and again after each world switch, the server sends one
  `seihai3dSpace <id> <x0> <y0> <z0> <x1> <y1> <z1> <sky|-> <sun on|off> <ambient r g b>` per
  interior box and one `seihai3dPortal <x> <y> <z> <radius> <space id>` per door. Space 0 is the
  outdoors.
- The client finds the space holding the camera each frame. Crossing a portal switches the sky
  (or none), the Sun and the ambient light in that frame, with no server round trip, and the client
  draws only the objects of the current space and of the spaces its portals open onto.
- With the client culling by space, the server can pack interiors closer than 1536 and scope by
  space: the current space, plus the far side of any portal the player stands at.
- With `world_terrain_cache` and `chunk_relight` (v1 bits 2 and 3), a world switch for interiors
  authored as separate worlds also stops resending terrain and stops needing a phase 2.
- **Fallback:** a 5.12, or our client without the bit, gets the stock layout above. The world file
  is the same; the server sends the space and portal commands only when the bit is agreed.

## Summary

| Row | Finding |
|---|---|
| Interiors (pw3d) | On a real 5.12, a 2D interior placed in its overworld's 3D world 1536 units out is entered and left by a client-side move with no `g3dworld`, no terrain resend and no relight. Positions land exactly on the link targets. Nothing outside is drawn inside and the room is not drawn from outside. Scoped without portals, each crossing shows one sky-only frame (under 0.23 s); with `portal` prefetch, none. Limit: outdoor sky and light inside. **[lab]** |
