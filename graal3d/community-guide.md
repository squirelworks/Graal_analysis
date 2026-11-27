# Graal 3D: the community guide

What Graal's Torque-era 3D client can do, how to build worlds for it, how to script it, and how
to write a server for it.

Last updated 2026-11-27. This guide covers the 3D mode of the 3.153 to 5.12 clients, which runs on
the Torque Game Engine, and the community "Frankenstein" 6.037 client that carries the same 3D
engine. The February 2000 DirectX "Graal3D" is a different program; see [README.md](README.md).

Most of what follows was checked on a real 5.12 client in a lab, against servers we wrote
ourselves, on a closed network. Where something rests only on a read of the client program, or
on one build, the text says so. Nothing here comes from a public Graal server.

For this week's news, downloads and the gserver-v2 add-on package, read the separate status
update (`release-3d/graal3d-status-2026-11-27.md` in the project's shared folder). This guide is
the long reference and does not repeat the release notes.

## Contents

1. [What the 3D mode is](#1-what-the-3d-mode-is)
2. [What you can build today](#2-what-you-can-build-today)
3. [Which clients have it](#3-which-clients-have-it)
4. [Quick start: serve a 3D world](#4-quick-start-serve-a-3d-world)
5. [Building worlds](#5-building-worlds)
6. [World tools and in-game editing](#6-world-tools-and-in-game-editing)
7. [Client scripting](#7-client-scripting)
8. [Writing your own server](#8-writing-your-own-server)
9. [Frankenstein 6.037 and what comes next](#9-frankenstein-6037-and-what-comes-next)
10. [Limits at a glance](#10-limits-at-a-glance)
11. [Troubleshooting](#11-troubleshooting)
12. [Glossary](#12-glossary)
13. [Where the facts come from](#13-where-the-facts-come-from)

---

## 1. What the 3D mode is

From version 3 to 5.12, the Graal client had a second game inside it: a 3D world built on the
Torque Game Engine 1.x. A server marked as a 3D server sends the player into it. There, Graal
draws:

- a sky box with fog;
- a sun that lights the scene;
- a streamed heightfield terrain with blended textures;
- water;
- ground cover (scattered rocks, grass);
- shapes in `.dts`, `.3ds` and `.dif` form;
- every other player as a shape with a name tag.

The 2D game does not vanish. The client stays logged in to the normal Graal server over TCP the
whole time. It keeps its account, flags and weapons there, and it downloads every 3D file over
that link. Beside it, it opens a second link over UDP to the same host. On that link it plays a
Torque "mission": the server ghosts objects to it and the client reports where its player is.

Three things about the 5.x client shape everything else in this guide:

1. **The server sends the world.** Nothing comes from a local mission file. The client draws
   only what it is ghosted.
2. **The client owns its own position.** The 5.x client sends no Torque "moves". It reports its
   player's position in every packet, and a client script does the walking.
3. **GS2 is the scripting language.** There is no TorqueScript on 4.04r2 and later. A server
   sends GS2 weapons (`weapon3d`), and they run in the 3D session.

## 2. What you can build today

Everything in this table works on a real 5.12 against seihai-gserver, the Seihai project's own
Rust server.

| You want | How | Where in this guide |
|---|---|---|
| A world of placed shapes with a sky and a sun | the world file: `object`, `sky`, `sun` | [5.2](#52-the-world-file) |
| Rolling terrain with grass, sand and rock | `terrain`, built with `seihai-servertools gen terrain --3d --stream` | [5.8](#58-terrain) |
| Seas and lakes | `water` | [5.9](#59-water) |
| Grass and scattered rocks | `replicator` | [5.10](#510-ground-cover) |
| Several players who see each other move and chat | built in; every player is a `GameObject` | [5.11](#511-players-and-multiplayer) |
| 2D and 3D players in the same level | built in; a 2D player shows in 3D as `G2DPlayer_<account>` | [5.11](#511-players-and-multiplayer) |
| A world of 20,000 objects | distance scoping, `graal3d_scope` | [5.13](#513-big-worlds-scoping-and-regions) |
| An 8,192-unit overworld with no seams | `regions`: a grid of region folders | [5.13](#513-big-worlds-scoping-and-regions) |
| Houses you walk into | interiors in the same world, joined by `portal` lines | [5.14](#514-interiors-and-doors) |
| Separate worlds with warps between them | `config/graal3dworlds/<name>.txt` and level warps | [5.12](#512-several-worlds-and-warps) |
| Objects only some players see | `objectfor`, `g3dhide` and `g3dshow` | [5.12](#512-several-worlds-and-warps) |
| Your 2D playerworld in 3D | `seihai-pw3d` | [6.2](#62-seihai-pw3d-a-2d-playerworld-in-3d) |
| Staff who place and move objects in game | `graal3d_edit = staff` and the `g3dedit` triggers | [6.5](#65-editing-in-game-g3dedit) |
| Custom walking, cameras and HUDs | `weapon3d` GS2 scripts | [7](#7-client-scripting) |
| Your own server | the wire protocol, and a runnable example | [8](#8-writing-your-own-server) |

What the client cannot do, whatever the server sends:

- It has no collision of its own. Players walk through walls unless a script stops them.
- Scripts cannot reach other objects: `findobject` returns NULL for world objects and other
  players.
- An object a script creates (`new GameObject(...)`) is not drawn. Only ghosts are drawn.
- There is no chat line or 2D HUD in the 3D view. Any HUD is script-drawn (see [7.7](#77-a-hud-text-and-chat)).
- It draws nothing more than 1,000 units from the camera by default, and at most 2,400.
- It holds at most 4,096 ghosts.

The full list, with numbers, is in [section 10](#10-limits-at-a-glance).

## 3. Which clients have it

| Client | Torque protocol | World model | State |
|---|---|---|---|
| 3.04 (Linux) | 9 | stock Torque, no 3D scripts | no 3D server for it is known |
| 3.153 (Mac PPC) | 19 | stock Torque: datablocks, `Player` | runs the mission phases with a Sky; little content tested |
| 4.04r2 (Windows) | 19 | stock Torque, GS2 instead of TorqueScript | walks a Torque `Player` with a `.dts` |
| 4.20r6 (Mac) | 21 | Graal's `GameObject` | as 24, with a quirk in the Sky |
| 4.20 Linux, 4.20r8 (Windows) | 24 | `GameObject` | full sessions; 4.20r8 needs a full OpenGL driver near terrain |
| 5.00r7, 5.12 (Windows, Mac) | 24 | `GameObject` | the best-known build; this guide is written for it |
| 5.24r3 and later, 6.x | none | no Torque | 2D only |
| Frankenstein 6.037 (community) | 24 | the 5.12 world, rebuilt | see [section 9](#9-frankenstein-6037-and-what-comes-next) |

There are two eras:

| | Torque era (3.153, 4.04r2) | GameObject era (4.20 onward) |
|---|---|---|
| Protocol | 19 | 21 and 24 |
| World objects | stock Torque `Player`, `Camera`, `Sky`, datablocks | Graal's `GameObject` with a shape, `Sun`, `Sky`, `Camera` |
| Mission start | three phases, with datablocks | two phases |
| Player input | Torque moves, sent to the server | the client reports its own position |
| Terrain | stock Torque terrain (no server path known) | streamed terrain chunks |

Unless a line says otherwise, the rest of this guide is about protocol 24 and the 5.12.
[Section 8.14](#814-protocols-19-and-21) lists what differs on the other two.

## 4. Quick start: serve a 3D world

Two servers can host the 3D side today:

- **seihai-gserver** is the Seihai project's own Graal server, written in Rust (MIT or Apache).
  New 3D work lands here first, and it has every feature in this guide.
- **seihai-gserver-v2** is the Seihai fork of GServer-v2, written in C++ (GPL-3.0). It has the 3D
  side as an add-on. Its pull request #184 also lets it load the 3D side as a separate module.
  It lacks regions, `portal`, the `TilesControl` fix, `g3dedit`, several worlds and per-player
  objects for now.

### 4.1 On seihai-gserver

In `config/server.txt`:

```text
graal3d = true
# graal3d_port = 14901         the clients use the listed TCP port + 1; leave unset
# graal3d_pushterrain = true   push terrain textures at login (see 5.8)
# graal3d_scope = auto         for worlds with more than 2,000 objects (see 5.13)
# graal3d_edit = staff         in-game editing for staff (see 6.5)
# graal3d_sendms = 50          least ms between two packets to one client (10 to 1000)
# graal3d_shapecheck = skip    leave out shapes that crash clients (or warn, or off)
```

Then write `config/graal3dworld.txt`:

```text
sun 0.57735 0.57735 -0.57735 0.8 0.8 0.8 1 0.3 0.3 0.35 1
sky sky_fr,sky_rt,sky_bk,sky_lf,sky_up,sky_dn 1000 0.6 0.7 0.9
skyoptions 1 1 0 0.4 0.6 0.9
playershape player.3ds
spawn 12 -12 1
camera 0 -6 3
object house house.dts 30 10 0
object tree1 tree.3ds 20 -5 0 0 0 1 0.6
```

Put the shapes and textures (`player.3ds`, `house.dts`, `tree.3ds`, `sky_fr.png` and so on) in
the server's file folders, as you would any download.

With `graal3d` on, the server:

- registers at HQ level 4, so the listserver tags its name with `3 `;
- answers every file request a 3D client makes, with the file or with a refusal;
- sends `PLO_SERVERLISTCONNECTED`, which closes the client's "Connecting..." window;
- holds each UDP link until the same account (or a guest) from the same address has logged in
  over TCP.

A 5.12 enters 3D through a warp to a server whose name starts with `3 `. On a lab server with no
listserver, name the server `3 My Lab` yourself.

### 4.2 On seihai-gserver-v2

The options go in `config/serveroptions.txt`, and they are spelled without underscores:

```text
graal3d = true
# graal3dport = 0         0 or unset: the server port + 1
# graal3dscope = off      or on, or auto
# graal3dsendms = 50
# graal3dshapecheck = skip
# graal3dpushterrain = false
# graal3dmodule = auto    with PR #184: auto, a path, or off
```

Set `hq_level = 4` in `config/adminconfig.txt` so that the server is listed as a 3D server. The
world file is the same `config/graal3dworld.txt`. An `object` line there may carry a scale
after the angle: `object <name> <shape> x y z ax ay az angle sx sy sz`.

With PR #184, the server can be built with no 3D code (`-DGRAAL3D=OFF -DGRAAL3D_MODULE=ON`). It
then loads `libseihai-graal3d.so` (`seihai-graal3d.dll` on Windows, `.dylib` on macOS) from the
server folder, its `addons/` folder, or beside the program. Before it loads the module, it
checks the add-on API version (1), the standard library and platform, and how gs2lib numbers
client versions. If any of them differ, it says why and runs without 3D. The module has its own
version (0.1.0) and its own `graal3d-v*` tags. The built-in add-on is still the default.

### 4.3 Your first world without writing anything

`seihai-servertools` can make a complete server folder with a 3D terrain world:

```text
seihai-servertools gen terrain myworld --world isle --size 4x4 --3d --stream --playerworld
seihai-gserver --world myworld
```

That writes the 2D levels and gmap, a `.3ds` ground and its trees and rocks, a streamed terrain
with its `heights.info` and textures, `config/graal3dworld.txt`, and a `config/server.txt` with
3D on and the terrain pushed at login. See [section 6](#6-world-tools-and-in-game-editing) for
the other tools.

### 4.4 What a player sees

1. The client logs in over TCP as usual. A 5.12 always logs in as a guest.
2. It is warped to the `3 ` server. It opens TCP on the listed port and UDP on the port + 1 at
   the same time.
3. The UDP link comes up. The console logs "Phase 1: Download Ghost Objects", then "Phase 2:
   Mission Lighting", then "Initial Control Object".
4. Once every file it asked for has been answered, the 3D view appears. A weapon sees this as
   `onGraal3DLoginStep` with steps 2 to 6.

If it stops anywhere along the way, see [section 11](#11-troubleshooting).

---

## 5. Building worlds

### 5.1 Units, axes and turns

- **Axes:** Torque's, with z up. +y is north, +x is east.
- **Units:** one unit is one 2D tile. A 3D point (x, y) is tile (x, −y), so the 2D map's
  south-going y is the 3D world's −y. The server keeps a 3D player's TCP position in step with
  this, so 2D scripts see where the player is.
- **A shape's origin** sits exactly on the point you give it.
- **Order:** the shape is scaled along its own axes, then turned once about an axis, then moved.
- **Turns are an axis and an angle in radians.** The clients turn the opposite way from the
  right-hand rule:
  - a positive angle about +z turns clockwise seen from above, so +y swings toward +x;
  - a positive angle about +x tilts a camera down.
  For a shape that should face east, use `0 0 1 1.5708`.
- Script `rotation` reads back as an axis and an angle in **degrees**. `eulerrotation` only
  reflects what a script wrote.
- Positions are limited to 100,000 units from the origin on seihai-gserver.

### 5.2 The world file

`config/graal3dworld.txt` holds one entry per line; `#` starts a comment. The server prints any
line it does not understand at start-up.

| Line | What it does |
|---|---|
| `object <name> <shape> x y z [ax ay az angle]` | a shape in the world. The name must be unique in the world. |
| `objectfor <accounts> <name> <shape> x y z [...]` | the same, sent only to the listed accounts (comma separated) |
| `sun dx dy dz  r g b a  ar ag ab aa` | the light direction (pointing down for daylight), its colour and the ambient colour, 0 to 1 |
| `sky <textures> [<distance> [<fog r g b>]]` | six sky-box faces, comma separated, the visible distance and the fog colour |
| `skyoptions <b1> <b2> <b3> <r g b>` | the sky's three switches and its solid colour (see [5.5](#55-sky-fog-and-draw-distance)) |
| `playershape <shape>` | every player's own shape |
| `spawn x y z` | where players start |
| `camera x y z [ax ay az angle]` | each player's camera, as an **offset from the spawn** (default `0 -5 2`, facing the spawn) |
| `movetype interpolate\|rigid\|list` | sends server moves of a player as movement data, so a 5.12 glides there |
| `weapon3d <name> [<file>]` | a GS2 weapon sent to every 3D client (the file is relative to the world folder; without one, the server weapon of that name) |
| `terrain <folder> [<square size>] [repeat] [<W>x<H>]` | a streamed terrain (see [5.8](#58-terrain)) |
| `regions <folder> <cols>x<rows> [<chunks>] [<square size>]` | a terrain and objects made of region folders (see [5.13](#513-big-worlds-scoping-and-regions)) |
| `water x y z  sx sy sz [<surface texture> [<liquid type>]]` | a box of water; its surface is at z + sz |
| `replicator <class> x y z <radius> <min> <max> <shapes> [<seed> [x0 y0 x1 y1]] [scale=...]` | ground cover (see [5.10](#510-ground-cover)) |
| `portal x y z <radius> tx ty tz` | a door to a far part of the same world (see [5.14](#514-interiors-and-doors)) |
| `tgecontrol player\|camera`, `tgeplayershape <file.dts>` | protocol 19 only (3.153, 4.04r2) |

A small complete world:

```text
# A walled garden at 40,-40
sun 0.4 0.6 -0.7 1 0.95 0.85 1 0.35 0.35 0.4 1
sky sky_fr,sky_rt,sky_bk,sky_lf,sky_up,sky_dn 900 0.7 0.75 0.85
skyoptions 1 1 0 0.5 0.6 0.8
terrain world/garden 8
water -1024 -1024 -19.5 2048 2048 20 water_surface 0
replicator DynamicGrass 0 0 0 6 20 40 g3d_blades.png
playershape player.3ds
spawn 40 -40 31
camera 0 -6 3
weapon3d TilesControl weapons/tilescontrol.gs2
weapon3d Walker weapons/walker.gs2
object gate gate.dts 40 -30 30
object well well.3ds 44 -44 30 0 0 1 0.785
```

### 5.3 Shapes

| Format | Draws on 5.12 | Rules |
|---|---|---|
| `.dts` (Torque shape) | yes | **version 24 only.** 5.12 rejects other versions; a version 17 file froze the Linux 4.20 client. |
| `.3ds` (3D Studio) | yes | **must hold at least one material**; a mesh with none loads without an error and draws nothing. Each mesh is limited to 65,535 vertices. |
| `.dif` (Torque interior) | loads | version 44 (`InteriorResource` 44, `Interior` 0) |
| `.ft` (`GameShapeFT`) | stored under `trees` | format not settled |
| `.md3`, `.dsq`, `.ifl`, `.dml`, `.gft` | no | 4.04r2-era or unused on 5.12 |

How big a shape may be:

- About 100,000 triangles (1.6 MB) in one shape drew fine.
- 131,070 vertices across two meshes drew fine. There is no per-shape vertex limit beyond the
  per-mesh `.3ds` cap.
- A 16.8 MB, one-million-triangle shape stalled the 5.12 for good. Keep shape files well under
  2 MB.

The clients trust their files. A `.3ds` that is cut short, has a chunk that runs past its parent,
or has a face that points past its mesh has crashed a 5.12. So have a `.dts` with a huge size
word and a cut `.dts`. seihai-gserver checks every shape the world file names at start-up and,
with `graal3d_shapecheck = skip` (the default), leaves bad ones out and refuses them when a
client asks.

### 5.4 Textures

How a 5.12 asks for textures:

- It drops the image extension from material and sky names, lower-cases them, and asks for the
  bare name: `C6CYN.PNG` is requested as `c6cyn`. A server must find the file by its stem.
  seihai-gserver tries `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tga` and `.dds`, in that order.
- Shape names keep their extension.
- It asks for a mesh's textures only after the mesh has arrived, and it never asks again after a
  "not found".
- It saves a name with an underscore in a subfolder named after the part before the first
  underscore (`gnsky_fr` goes in `images/gnsky/`).
- 3.153 asks for Sky textures as `.gif`; a `.png` of the same stem answers it.

What draws:

| Draws | Draws plain white |
|---|---|
| 8-bit PNG (RGB, RGBA, paletted, grey, interlaced) | 16-bit PNG |
| JPEG (baseline and progressive) | BMP, TGA, DDS |
| GIF | a missing texture |

- Alpha 0 is cut out and anything else is opaque. There is no alpha blending, only cut-outs.
- GIF transparency draws white.
- Keep images at 1,024 pixels a side or less. A PNG claiming 30,000 × 30,000 pixels crashed a
  5.12.
- Terrain textures should be 256 × 256, 24-bit.

(The Linux 4.20r6 accepted BMP and TGA in one lab when the file was on disk under that extension.
Do not rely on it.)

### 5.5 Sky, fog and draw distance

The `sky` line names six faces, then the visible distance and the fog colour. The faces do not
follow "front is +y": a camera looking along +y sees the **third** texture, flipped.

`skyoptions` sets three switches and the solid colour:

| Switch | Effect |
|---|---|
| 1 | draw the sky textures (off: the solid colour, though the faces still download) |
| 2 | draw the bottom face (off: black below the horizon, which leaves trails as the camera moves) |
| 3 | no visible effect found |

Use `skyoptions 1 1 0 <colour>` for a normal textured sky.

- **Field of view:** 90° across, about 73.7° up and down at 4:3. One sky face fills the whole
  view across, so a face about as wide as the window looks sharp.
- **Draw distance:** the client's own `visibledistance3D` in `game_config.txt`, 1,000 by
  default, at most 2,400. The fog distance is always 0.85 times it. The server never learns a
  player's setting, so keep anything important within 1,000 units of where the camera will be.
- **Clouds:** cloud textures in the Sky download but have never drawn in a lab. Treat clouds as
  not working.
- A world with no Sky at all clears to flat dark red on the Linux 4.20, and 3.153 needs one.
  Always send a Sky.

### 5.6 The sun and lighting

The `sun` line gives a direction and two colours. The client lights the mission once, at
**Mission Lighting** (phase 2 of the mission start), from the terrain, water and sun it holds at
that moment. That has consequences:

- A terrain that arrives after phase 2 draws without slope shading. seihai-gserver holds phase 2
  until the terrain, water, Sun and every terrain chunk the client asked for are in (at most 15 s
  after phase 1).
- After a world switch that brings a new terrain, water or Sun, the server sends phase 2 again,
  and a 5.12 relights.
- After a terrain window slide (large terrains), the server sends phase 2 again once the new
  chunks are acked. "Terrain lit" takes 0.03 to 0.04 s.

GS2's sky and lighting functions (`setSunColors`, `setFogColors`, `setSkyBandColors`,
`lightScene` and the rest) changed nothing visible on a 5.12 when the server sends a Sun and a
Sky. Set the look from the world file.

### 5.7 The camera

A 5.x client draws its 3D view only through a `Camera` ghost. With just its own player the view
stays black. seihai-gserver gives each client its own camera, `G3DCamera_<account>`:

- at the spawn plus the `camera` offset (`0 -5 2` by default), facing the spawn unless the line
  gives a turn;
- created before the world's objects, so the view comes up first and the objects fill in;
- named in every packet once the client has it.

The client owns the camera after that. A weapon moves it (see [7.3](#73-moving-the-camera)).
The server cannot steer it, with one exception: when the server moves a player (a `g3dpos`
trigger, a door, a staff move), it moves the camera to the same offset from the new spot,
because a 5.12 never moves its own camera on a server move. The default camera for `spawn 0 0 1`
is the same as `camera 0 -5 2 1 0 0 0.38`.

`startinfullscreen` in `game_config.txt` gave a 640 × 480 full screen that stayed at
"Connecting...". Play 3D in a window.

### 5.8 Terrain

The 4.20r6, 4.20r8 and 5.x clients draw one streamed heightfield: a grid of 256 × 256 squares,
centred on the origin, sent as 16 × 16 chunks of 16 × 16 squares.

```text
terrain world/island 8          # 8 units a square: the terrain spans -1024 to 1024
terrain world/island 8 repeat   # tiled past its edges
```

The folder holds `heights<x>-<y>.dat` for x and y from 0 to 15 (no zero padding). Each file is
one chunk as a zlib stream of at most 1,023 bytes, the same file the client keeps in its cache.
A missing chunk is left out. The square size may be 1 to 64. Use 8; a huge one killed a 5.12,
and at 4 the frame rate halved.

**Make the chunks with a tool.** `seihai-servertools gen terrain ... --stream` writes chunks in
the client's own encoding. That matters: the client stamps its own re-encoding of each chunk,
and a server re-sends every chunk whose stamp differs. A chunk in any other form is downloaded
again on every visit. [Section 8.10](#810-terrain-streaming) has the encoding.

**Textures.** Put `heights.info` (one texture name a line, in material order) and its textures
in the file folders. Name them with their extension (`g3d_grass.png`); the Linux 4.20 saved bare
names without one and then could not load them. Make them 256 × 256, 24-bit. A name may not
contain a space or a comma. All worlds share one `heights.info`, since the client asks for it by
its bare name.

**The first visit draws white.** By default a 5.12 fetches only `heights.info` on its first
visit, and the textures on its second. `graal3d_pushterrain = true` sends `heights.info` and its
textures over TCP right after the link comes up, once per account, so the first visit is
textured.

**The ground near the camera (`TilesControl`).** Within 150 units of the camera, a 4.20r8 or 5.x
draws a second tile layer over the terrain. It asks a client object named `TilesControl` for it:
`getTilesForSpot("x,y")` must return four texture names, one per quarter square. With no such
object, it paints every near square in the **first** `heights.info` texture. Below about 75
units that layer covers the terrain completely, and it fades out by 150. So a world whose first
texture is water looks all water up close.

The fix is a `weapon3d` named `TilesControl` that returns names that do not exist. The client
asks for the missing name once a session, and the blended terrain then shows right up to the
camera:

```gs2
//#CLIENTSIDE
function getTilesForSpot(xy) {
  return {"notile","notile","notile","notile"};
}
```

seihai-gserver sends a built-in one with every terrain (`g3dnotile`). A world's own `weapon3d
TilesControl` replaces it, for example to lay real tiles on chosen squares. The four names map
to the quarters as index = qx + 2·qy: [0] is the low-x low-y quarter, [1] is +x, [2] is +y and
[3] is both.

**Large terrains.** A client holds one 16 × 16-chunk grid. A bigger terrain slides that grid
round the player:

```text
terrain world/continent 8 repeat 48x48
```

- The size is in chunks, each side even, 16 to 256. `repeat` is required.
- The folder holds `heights<X>-<Y>.dat` for the whole size, centred on the origin as before.
- Each grid slot holds the world chunk that falls in it among the 16 round the player's chunk (8
  behind and 7 ahead). When the player crosses into another chunk, the 16 new chunks (31 at a
  diagonal) go out mid-session, and phase 2 goes again once they are acked.
- In the lab, a 48 × 48 terrain at size 8 cost about 3.8 KB a diagonal crossing, with no stall.
  At size 8 the window is 2,048 units across, which keeps about 900 units of fresh terrain
  ahead: about the draw distance.
- Past the edge, the edge region repeats. Put a border of sea or flat chunks round the terrain.

**One terrain a world.** With two `TerrainBlock`s, a 5.12 lays chunks only on the last one. A
later `terrain` line replaces the first.

### 5.9 Water

```text
water -1024 -1024 -19.5 2048 2048 20 water_surface 0
```

This is a `WaterBlock` from that corner, unrotated, of that size. Its surface is at z plus the
z size (0.5 here), not at z. The liquid types are stock Torque's: 0 water, 1 ocean, 2 river,
3 stagnant, 4 lava, and so on.

### 5.10 Ground cover

```text
replicator DynamicShapeReplicator 0 0 0 4 1 3 rock.dts,stone.3ds
replicator DynamicGrass 0 0 0 8 20 40 g3d_blades.png
```

- Cover grows on a grid of 8-unit cells **round the player's own object**, not round the
  replicator's point. The radius is in cells (1 to 64); min and max are objects a cell.
- `DynamicShapeReplicator` scatters shapes (up to 20 a cell).
- `DynamicGrass` and `DynamicGrassReplicator` build flat grass pieces from a **texture** and draw
  nothing for a shape name (up to 100 a cell). A mostly transparent texture draws next to
  nothing.
- `scale=<n>` or `scale=<min>,<max>` sizes the copies. Grass defaults to 3, since a grass quad at
  1 is only about 0.6 units.
- An optional box `x0 y0 x1 y1` limits where cells may lie.
- Cover is placed by casting rays, so it needs real ground under it: terrain or solid objects.

**The origin cell.** A 5.12 grows no cover at all while the player stands in the world's origin
cell, with x and y both between −8 and 8. Keep the spawn at least 8 units from `0 0` in x or y.
seihai-gserver warns at start-up about a world with cover whose spawn is there.

A 5.12 grows cover only from the shapes and ground it holds when it reads the replicator. On a
first visit those arrive later, so seihai-gserver sends each replicator again at the end of the
mission start, and 5, 15 and 30 seconds after it.

### 5.11 Players and multiplayer

- Every 3D player is a `GameObject` named `G3DPlayer_<account>` with the world's `playershape`,
  its nickname and its chat. Each sees the others move and talk. Shape, chat, nickname and
  attribute changes are relayed; another client downloads a changed shape on demand.
- The first player stands on the `spawn`. Later ones take the first free point of a ring 2 units
  out, then 4, and so on.
- A 2D player in a 3D player's level is shown in 3D as `G2DPlayer_<account>`, at its tile
  position, with its nickname and chat. A 2D client draws a 3D player as a normal sprite.
- A 2D player's chat reaches a 3D script through `onRemotePlayerChats`. Private messages cross
  in neither direction.
- Players and shapes overlap freely: there is no collision on the client. Mounting and attaching
  cannot be driven from a client script.
- A 5.12 in 3D runs no GS1 level NPCs, so a 2D player in the level leads it, not the 3D one.
- The client's position is trusted. A server that cares about cheating must check moves itself.

### 5.12 Several worlds and warps

`config/graal3dworld.txt` is the default world. Each `config/graal3dworlds/<name>.txt` is
another world, in the same format.

- A 3D player is in the world named after its 2D level (`cave.nw` is world `cave`), else in the
  default one. A TCP warp (a link, a serverside `setlevel2`) takes the 3D client with it.
- A script can also ask: `triggerserver("gui", <weapon>, "g3dworld", "cave")`, or `"default"`.
- The switch needs no new link. The old world's ghosts are deleted and the new world's sent; the
  player and camera move to the new spawn. New `weapon3d` lines are sent, and phase 2 goes again
  when the new world brings a terrain, water or Sun.
- **Give every 3D world a Sun.** A switch into a world with no terrain, water or Sun leaves a
  5.12 frozen on a sky-only frame.
- Each player sees only the players in its own world. The client gets `clientr.g3dworld`.

`objectfor one,two door door.3ds 2 2 0` is an object sent only to the accounts `one` and `two`. A
script can hide any world object from its own player, and bring it back:
`triggerserver("gui", <weapon>, "g3dhide", "door")` and `"g3dshow"`.

### 5.13 Big worlds: scoping and regions

A GameObject-era client holds 4,096 ghosts. Without scoping, every object is sent at join, at
about 130 to 140 creates a second, so 4,000 objects take about 30 seconds and most are too far
away to be drawn.

**Distance scoping** sends only what is near:

```text
graal3d_scope = auto           # off, on (every world) or auto
graal3d_scopeauto = 2000       # auto: only worlds with more objects than this
graal3d_scoperadius = 1100     # world units
graal3d_scopehysteresis = 200  # world units
```

- An object is ghosted while it is within the radius of the player, and deleted past the radius
  plus the hysteresis. Scopes are checked 5 times a second.
- Only `object` and `objectfor` lines are scoped. The Sun, Sky, terrain, water, cover and players
  always go.
- At most 3,584 world objects are in one client's scope (the table less 512 for players and the
  rest). In a denser spot the nearest win.
- The server ghosts the terrain, the player's own object and its camera first, then the Sun, Sky,
  water and cover, then the other players, and world objects last. Before this order, a world of
  4,094 objects filled the table before the camera, and the view stayed black.
- Lab numbers: 20,164 objects on a 56-unit grid joined in about 3 s with a radius of 1,100, and
  peaked at about 1,400 ghosts while walking at about 70 units a second.

**Regions** build a big overworld from a grid of smaller pieces, the way a 2D playerworld is a
gmap of levels:

```text
regions world/enigma 8x8          # 8 x 8 regions of 8 chunks (1,024 units) each
regions world/enigma 4x4 16       # 4 x 4 regions of 16 chunks (2,048 units)
```

- The folder holds one subfolder a region, `<i>-<j>` (i east, j north). Each may hold its own
  `heights<x>-<y>.dat` and a `region.txt` of `object`, `objectfor`, `water` and `replicator`
  lines in the region's own coordinates, from its south-west corner.
- `heights.info` and the terrain textures go in the regions folder itself. A missing region is
  flat and empty.
- The server stitches the regions into one large terrain and one list of objects. Nothing
  switches at a region edge: the terrain window slides and scoping brings objects in.
- The client gets `clientr.g3dregion` (`<i>-<j>`) whenever it changes.

A real 5.12 walked an 8 × 8-region demo world of 18,055 objects with six towns:

| | Result |
|---|---|
| Join next to a town (1,952 objects in scope) | phase 2 acked in 2.4 s at `graal3d_sendms = 10` (about 7 s at 50); every object in by 5.5 s (20 s at 50) |
| A region edge | an ordinary window slide, relit 0.1 to 0.3 s later; no seam, stall or pop-in |
| Ghost table | peak 2,075 of 4,096; a 3,500-house stress town held at 3,584 |
| Frame rate (software rendering) | 32 to 41 FPS in the open, 18 to 20 in a 1,440-house town, 11 to 12 in the stress town |
| Memory | at most 621 MB committed of the 2 GB a 5.12 can address |

So the limit is the frame rate in dense places, not memory or the ghost table. A town too dense
for one spot is better as its own world behind a warp.

`graal3d_sendms = 10` worked with no loss on loopback, but it has not been tried over a real
network. The default stays 50 (packets of at most 400 bytes, about 8 KB/s).

### 5.14 Interiors and doors

A world switch at every door is slow: it resends the terrain and needs a second phase 2. So put
houses and caves **in the same world**, far enough away that they are never drawn from outside
(1,536 units is what `seihai-pw3d` uses), and join them with portals:

```text
portal 120 -64 0 2  1700 -1600 0
```

While a player is within 2 units of the door at `120 -64 0`, the objects round `1700 -1600 0` are
in scope too. They are ghosted while the player still stands at the door, too far away to be
drawn, so the room is there the moment the player is moved through. The land outside comes back
the same way on the way out. A walker weapon does the move. Without scoping, portals change
nothing (every interior is sent at join, but still not drawn).

An interior in the same world shares the world's Sky and Sun.

### 5.15 Changing files while players are on

- A 5.12 asks for a file only the first time it needs it in a session. A changed file reaches a
  player only after they link again. Terrain chunks are re-sent by stamp, so only changed
  chunks go.
- The client judges its cached copy by the file's time. To roll a file back to an older copy,
  save it again so that it gets a new modification time.
- `g3dedit` changes object lines only, and those reach linked clients at once.

### 5.16 The start-up check

seihai-gserver looks up every shape and texture the world file names at start-up and logs the
missing ones. It then checks each for the faults that crashed or blanked a real client: `.3ds`
materials, chunk bounds and face indices; `.dts` version and section bounds; PNG sizes and bit
depths; terrain texture sizes; `heights.info` names with spaces or commas; a second `terrain`
line; and ground cover with a spawn in the origin cell. Read the log after every world change.

---

## 6. World tools and in-game editing

All of these are in **seihai-servertools**, except `g3dedit`, which is in seihai-gserver.

### 6.1 `gen terrain` and `gen 3d`

```text
seihai-servertools gen terrain DIR --world NAME [--size WxH] [--seed N] [--base N] [--height N]
                   [--chaos F] [--islands] [--3d [--vscale F] [--trees N] [--stream]
                   [--playerworld [--v2]]]
seihai-servertools gen 3d GMAP DIR [--world NAME] [--vscale F] [--trees N] [--stream]
                   [--playerworld [--v2]]
```

- `gen terrain` makes a 2D heightfield world (levels and a gmap). `--3d` adds the same ground as
  a `.3ds`, tree and rock shapes, and a world file.
- `--stream` adds the streamed terrain: 256 chunks in the client's encoding, `heights.info` and
  its textures.
- `--playerworld` lays the folder out as a seihai-gserver world that serves as it is.
  `--playerworld --v2` lays it out for GServer-v2 instead.
- `gen 3d` does the same from an existing gmap with a `HEIGHTMAP` block.

### 6.2 `seihai-pw3d`: a 2D playerworld in 3D

```text
seihai-pw3d INPUT OUT [--start LEVEL] [--at X,Y] [--tileset PICS1.PNG] [--tiledefs FILE]
            [--objects DIR] [--images DIR]... [--meaning-maps] [--wall-height F]
            [--colour-bits N] [--separate-interiors] [--force]
```

It turns a folder of `.nw`, `.graal` or `.zelda` levels and gmaps into 3D worlds:

- each level becomes a coloured 3D ground from its tiles, with walls and sign boards;
- each gmap becomes one world;
- each house or cave reached from a hub goes into that hub's world, 1,536 units out, with a
  `portal` line per door;
- a `PW3DWalk` walker weapon carries each level's walk grid and links, so the arrow keys walk the
  player, walls stop it, and links lead where they did in 2D;
- `--objects DIR` places shapes for chosen tiles;
- `--separate-interiors` keeps every interior as its own world instead.

Turn on `graal3d_scope = on` when serving its output, so the portals work.

### 6.3 `seihai-regions`: big overworlds

```text
seihai-regions split WORLD.txt --root DIR --into FOLDER [--chunks N] [--out FILE]
seihai-regions stats WORLD.txt --root DIR [--chunks N] [--reach UNITS] [--budget N]
seihai-regions demo DIR [--regions CxR] [--chunks N] [--towns N] [--town-objects N] ...
```

- `split` cuts a world's terrain and objects into region folders and rewrites its `terrain` line
  as a `regions` line. (`seihai-servertools world3d split` is the same.)
- `stats` counts objects per region and the most within reach of any spot, against the 3,584 a
  client can hold.
- `demo` builds a test overworld with towns, trees and rocks.

### 6.4 `seihai-edit3d`: an offline editor

```text
seihai-edit3d FOLDER [--world NAME]                         # the window, with a live preview
seihai-edit3d show FOLDER [--world NAME]
seihai-edit3d add FOLDER NAME SHAPE X Y Z [--turn DEG] [--ground] [--for ACCOUNTS]
seihai-edit3d move FOLDER NAME X Y Z [--turn DEG] [--ground]
seihai-edit3d remove FOLDER NAME
seihai-edit3d spawn FOLDER X Y Z [--ground]
seihai-edit3d terrain FOLDER raise|lower|flatten|smooth|paint X Y RADIUS VALUE
seihai-edit3d render FOLDER OUT.png [--size WxH] [--eye X,Y,Z --yaw DEG --pitch DEG]
```

It edits a world file and its streamed terrain, saves with backups, and renders a preview. Use
it for terrain, which cannot be edited in game yet. It has not yet been used on a real client's
world, so check its output on a client.

### 6.5 Editing in game: `g3dedit`

The 5.12 carries Torque's `WorldEditor` and `TerrainEditor`, but against a remote server they
edit only objects the script made itself, and nothing is saved. So in-game editing goes through
the server. With `graal3d_edit = staff` on seihai-gserver, a script of a `STAFF` account sends:

```gs2
triggerserver("gui", "G3DEditor", "g3dedit", "list");
triggerserver("gui", "G3DEditor", "g3dedit", "add", "lamp1", "lamp.3ds", 10, -4, 0);
triggerserver("gui", "G3DEditor", "g3dedit", "move", "lamp1", 12, -4, 0, 0, 0, 1, 1.57);
triggerserver("gui", "G3DEditor", "g3dedit", "remove", "lamp1");
```

- The edit applies to the world the player is in. Everyone there sees it at once.
- The world file is saved with only that line changed. The old file is kept as
  `<file>.bak-<unix seconds>`.
- The answer comes back as `clientr.g3dedit`: `ok <op> <name>` or `error <why>`. `list` also fills
  `clientr.g3dedit_objects` with `name:shape:x:y:z:ax:ay:az:angle` entries.
- A real 5.12 always logs in as a guest, so it signs in for editing first:
  `triggerserver("gui", <weapon>, "g3dedit", "login", <account>, <password>)`, then `"logout"`.
  After three wrong passwords, that connection's logins are refused. The 3D link is not
  encrypted, so use editing logins on a LAN or lab server only.
- Region objects cannot be moved in game; edit their `region.txt`.

seihai-gserver ships an editor weapon, `docs/examples/g3deditor.gs2`:

| Key | Action |
|---|---|
| L | sign in (type the account, Enter, the password, Enter) |
| N, B | pick the next or previous object |
| arrows, Page Up, Page Down | move it |
| Q, E | turn it |
| C | copy it |
| Delete | remove it |

The camera follows the selected object. Give it to staff with `weapon3d G3DEditor
weapons/g3deditor.gs2`, with the file copied into the world folder.

---

## 7. Client scripting

### 7.1 How scripts reach the client

A `weapon3d <name> <file>` line sends a GS2 weapon to every 3D client in that world. The 3D
client needs **bytecode**: seihai-gserver compiles the part after `//#CLIENTSIDE` with
seihai-core's compiler (GS2, or GS1 if the file starts with `//#GS1`). The client caches the
compiled code as `weblevels/weapons/<server>/<weapon>.code`. A weapon the player got in 2D also
runs in 3D.

What reaches a script in 3D:

| From the script | Reaches |
|---|---|
| `triggerserver("gui"/"weapon", <weapon>, ...)` | the server, as a UDP text event; the server runs the named weapon's serverside, as from a 2D client, or acts on its own `g3d*` triggers |
| `player.chat = "..."` | every other 3D client, in the player's object update |
| typed chat | the TCP side, as in 2D |
| `client.x = ...` | the client only |
| `sendpm`, `setplayerprop` | dropped |

What reaches the script from the server:

| Value | Holds |
|---|---|
| `serverr.<name>` | server flags a 3D script can read. A `server.<name>` flag reads **empty** on a 5.12 (the key is there, the value is blanked by the client), so send `serverr.` flags. |
| `clientr.g3dpos` | the player's position as the server last set it |
| `clientr.g3dworld` | the world the player is in (`default` or a name) |
| `clientr.g3dregion` | the region the player stands in, on a `regions` world |
| `clientr.g3dedit`, `clientr.g3dedit_objects` | the last editing answer, and the object list |

The server's own triggers:

| Trigger | Does |
|---|---|
| `triggerserver(k, w, "g3dpos", x, y, z)` | moves the player's own object on every screen, and the camera with it |
| `triggerserver(k, w, "g3dworld", "<name>")` | switches the player to another world |
| `triggerserver(k, w, "g3dhide", "<object>")`, `"g3dshow"` | hides or shows a world object for this player only |
| `triggerserver(k, w, "g3dedit", ...)` | in-game editing ([6.5](#65-editing-in-game-g3dedit)) |

A 5.12 drops `triggerserver` calls made in a weapon's first ticks. A script that must tell the
server something at start should wait a few seconds.

### 7.2 Walking

A 5.12 does not move its own player. Its 3D key bindings call `moveForward2`, `moveBackward2`,
`moveLeft2`, `moveRight2` and `jump`, which only a script defines, and in practice the arrow keys
reach scripts as keys. So a walker weapon reads the keys on a timer, moves `player.position`, and
the client reports the new position to the server in its next packet. There is no collision: the
script decides where the player may go.

A small walker with a chase camera:

```gs2
// Walker: the arrow keys walk the player on flat ground; a camera follows.
//#CLIENTSIDE
function onCreated() {
  this.x = 12;     // start where the world's spawn is
  this.y = -12;
  this.z = 1;
  this.last = 0;
  setTimer(0.05);
}

function onTimeout() {
  temp.dx = 0;
  temp.dy = 0;
  if (keydown2(37, true)) temp.dx = temp.dx - 1;   // left: west
  if (keydown2(39, true)) temp.dx = temp.dx + 1;   // right: east
  if (keydown2(38, true)) temp.dy = temp.dy + 1;   // up: north (+y)
  if (keydown2(40, true)) temp.dy = temp.dy - 1;   // down: south
  // Move by the clock: a 5.12 ticks 7 to 15 times a second, not 20.
  temp.now = timevar2;
  temp.step = 0.25;
  if (temp.now > 0 && this.last > 0) temp.step = (temp.now - this.last) * 6;
  this.last = temp.now;
  if (temp.step > 0.6) temp.step = 0.6;
  if (temp.dx != 0 || temp.dy != 0) {
    this.x = this.x + temp.dx * temp.step;
    this.y = this.y + temp.dy * temp.step;
    player.position = {this.x, this.y, this.z};
  }
  placeCamera();
  setTimer(0.05);
}

// The camera 6 behind (south of) the player and 3 above, looking north and a little down.
function placeCamera() {
  temp.cam = ServerConnection.camera;
  if (temp.cam == NULL) return;
  temp.cam.cameramode = "free";
  temp.cam.position = format("%f %f %f", this.x, this.y - 6, this.z + 3);
  temp.cam.eulerrotation = "0.3 0 0";
  temp.cam.updatePosition();
}
```

Notes from the lab:

- `setTimer(0.05)` runs about 7 times a second when the window is not focused and 14 to 15 times
  when it is. That is the finest step a script gets; there is no per-frame event.
- `onKeyPressed` fires (and repeats while a key is held), but `onKeyDown` and `onKeyUp` never do.
  Reading `keydown2` on a timer is what works.
- The 5.12 running seihai-core's bytecode has misread a variable or parameter passed straight to
  `.pos()`, `.charat()` or an array index. Copy it into a `temp.` first, or pass an expression
  (`x + 0`).
- A steep camera pitch made upright things lean outward. Keep the pitch small.
- For a terrain world, the walker needs ground heights. `getz(x, y)` is in the 5.12 function list
  but has not been confirmed to return terrain heights in a live session. `seihai-pw3d`'s walker
  carries its own height grid instead.

### 7.3 Moving the camera

The camera is `ServerConnection.camera` (also `player.camera`). Set `cameramode = "free"`, then
`position` (three numbers as text) and `eulerrotation` (three angles in radians as text; the
first is the pitch, so `"0.3 0 0"` looks a little down), and call `updatePosition()`. Reads of the camera's position, rotation, vectors and `worldBox` are
live, so a script can track it. `fov` reads empty.

### 7.4 What a script can touch

The 5.12 registers 35 GS2 classes with 418 members. The ones a 3D script uses:

| Class | Notable members |
|---|---|
| `GameObject` | `position`, `transform`, `shape`, `skin`, `chat`, `nickname`, `nickcolor`, `alpha`, `solid`, `shadow`, `collision`, `movetype`, `velocity`, `attr`; `getdropz`, `checkCollision`, `mountObject`, `getNodePosition`, `findimg`, `hideimg`, `isDrawn`, `isInInterior` |
| `Camera` (a `GameObject`) | `cameramode`, `eulerrotation`, `lookatposition`, `lookvector`, `followattachedobject`, `updatePosition()` |
| `SceneObject` (every 3D object) | `position`, `rotation`, `eulerrotation`, `scale`, `forwardVector`, `upVector`, `rightVector`, `worldBox`, `x`, `y`, `z`, and their getters and setters |
| `GameConnection` | `camera`, `account`, `nick` |
| `Sky` | fog colours and volumes, `skysolidcolor`, `skyfadetime` |
| `fxSunLight` | 52 members, including `sunazimuth`, `sunelevation` |
| `DynamicShapeReplicator` | radius, counts, scales, rotations, slope and surface rules |
| `GameShapeDTS` | `playAnimation`, `stopAnimation`, `listNodes`, `materials` |
| `GameShape` | `vertexshader`, `pixelshader` (GLSL source; needs a GLSL driver) |
| `ActionMap` | `bind`, `unbind`, `push`, `pop` |

Global 3D functions include `castRay(start, end, typemask)`, `get3Dobjectsbybox`,
`get3Dobjectsbyradius`, `getz(x, y)`, `getTerrainTexture`, `play3D`, and about 30 vector and
matrix helpers. The full typed list is in
[../torque/gs2-3d-typed-surface-512-2026-11-26.md](../torque/gs2-3d-typed-surface-512-2026-11-26.md).
Whether each one runs in a live session is being checked build by build; trust only what you
test.

### 7.5 Events

| Fire in a 3D session | Never fire |
|---|---|
| `onCreated` | `onKeyDown`, `onKeyUp`, `onMouseWheel` |
| `onPlayerEnters` (once, for itself) | `onCollision`, `onWallCollision`, `onPlayerTouchsMe` |
| `onGraal3DLoginStep` (steps 4, 5, 6) | `onObjectClicked`, `onClick`, `onActionLeftMouse` |
| `onTimeout` | `onFrame`, `onRender`, `onCameraMove`, `onMove` |
| `onMouseDown`, `onMouseUp` (button, mouse x and y in tile units) | `onMount`, `onUnmount`, `onMovementFinished` |
| `onKeyPressed` (repeats while held) | `onGhostAlwaysStarted`, `onConnectionAccepted`, `onResize` |
| `onRemotePlayerChats` | |

### 7.6 What does not work from a script

- `new GameObject(...)` makes an object that is not drawn.
- `findobject` returns NULL for world objects and other players, so `mountObject`,
  `attachedtoobject` and friends have nothing to act on.
- The sky, fog and sun functions do not override the server's Sky and Sun.
- `WorldEditor`, `TerrainEditor` and `EditManager` open nothing useful against a remote server,
  and `savestring` writes no file.
- `Terraformer.loadGreyscale` crashed a 5.12 without a `TerrainBlock`.
- `makescreenshot2` writes nothing.
- `server.` flags read empty (use `serverr.`).

### 7.7 A HUD, text and chat

The 2D HUD (hearts, bars, chat line, player list) does not draw in the 3D view. A `showimg`
overlay does, and it moves with updates, so a HUD, minimap or compass can be drawn at timer rate.
Text depends on fonts: the client fetches a font by its lower-cased family name when a script
asks for it, and draws it when the server has the `.ttf`; otherwise it falls back to Arial.
`showtext` was not visible in one lab and did draw with a served font in another, so test it on
your build.

---

## 8. Writing your own server

This part explains the protocol well enough to write a 3D server in any language. It goes with
two things in this repository:

- [../torque/udp-session.md](../torque/udp-session.md), the full wire reference with test vectors;
- [examples/g3dmini/](examples/g3dmini/), a working protocol-24 server in one file of Python
  (standard library only), with tests.

`g3dmini` is checked against the published vectors, and against the community 5.12 client
library from graal-client-repro: that client reaches login step 6 on it, with the terrain, its
player, its camera, the Sun, the Sky and a world object ghosted, and all 256 terrain chunks.

### 8.1 The shape of a 3D server

```text
           TCP, listed port P                  UDP, port P + 1
client ─── gen-5 Graal login ───────┐   ┌───── Torque link (protocol 24) ───── client
           file requests (shapes,   │   │      handshake, then data packets:
           textures, heights.info)  │   │        game section (control object, camera)
           flags, weapons, warps    │   │        events (mission start, terrain, text)
                                    ▼   ▼        ghosts (Sun, Sky, terrain, objects)
                              one session per player
```

The two links live and die together. When TCP closes, the client sends a UDP disconnect. When the
UDP link goes quiet for 30 s, the client reports "The 3D server connection has timed out" and
drops TCP too. There is no resume: a rejoin builds a fresh session.

### 8.2 The TCP side's duties

A 3D server is a normal Graal server first. On top of that:

1. **Be listed as a 3D server.** The name in the list must start with `3 ` (HQ level 4 on the
   listserver). The client gets there by a `PLO_SERVERWARP` (178) to that entry.
2. **Expect both links at once.** The client starts the UDP handshake before or with the TCP
   connect. Do not answer the UDP connect request until that account's TCP login is done; the
   client repeats it for about 15 seconds.
3. **Tie the links together** by the account (the connect request's first argument) and the
   source address. A 5.x guest sends `guest`, not the guest name the server assigned.
4. **Send `PLO_SERVERLISTCONNECTED` (190).** Without it the "Connecting..." window stays over the
   3D view even at login step 6.
5. **Answer every file request**, with the file or with `PLO_FILESENDFAILED` (30). Step 6 waits
   for all of them.
6. **Find textures by their bare, lower-cased stem** ([5.4](#54-textures)).
7. **Push the terrain textures** at login if you want a first visit to be textured
   ([5.8](#58-terrain)).
8. While in 3D the client ignores TCP level boards, warps and flag packets. Flags and weapons for
   the 3D session go over UDP ([8.11](#811-the-text-channel)).

The gen-5 login itself is documented in [../protocol/](../protocol/) (`login-session-known.md`,
`codec-and-framing.md`, `gen5-cipher-step-5x.md`).

### 8.3 Bit streams

Everything on UDP is a Torque bit stream:

- bits are packed **least significant bit first** within each byte, and bytes go in order;
- `intN` is an N-bit unsigned field, low bit first; `u8` and `u32` are 8 and 32 bits;
- `flag` is one bit; `f32` is the 32 IEEE-754 bits as a `u32`;
- `string` (handshake packets): a flag (1 Huffman, 0 raw), a `u8` length, then the Huffman codes
  or the bytes. The Huffman tree is built from Torque's fixed character-frequency table;
- `pstring` (inside data packets): one more flag first. 1 means "keep the first `u8` characters
  of the previous string in this packet". A server can always write 0.

In Python:

```python
class BitWriter:
    def __init__(self):
        self.bits = []
    def flag(self, b):
        self.bits.append(1 if b else 0)
        return bool(b)
    def int(self, v, n):
        self.bits.extend((int(v) >> i) & 1 for i in range(n))
    def u32(self, v):
        self.int(v & 0xFFFFFFFF, 32)
    def f32(self, v):
        self.u32(struct.unpack("<I", struct.pack("<f", float(v)))[0])
    def bytes(self):
        out = bytearray((len(self.bits) + 7) // 8)
        for i, b in enumerate(self.bits):
            out[i >> 3] |= b << (i & 7)
        return bytes(out)
```

`g3dmini.py` has the reader, the Huffman coder and `string`/`pstring`.

### 8.4 The handshake

The first byte tells a handshake packet from a data packet: a data packet's first bit is 1, a
handshake packet's type byte is even.

| Packet | Byte | Body |
|---|---|---|
| challenge request | `0x1A` | `u32` connect sequence (the 5.12 uses `0x400`) |
| challenge response | `0x1E` | `u32` sequence, 4 × `u32` digest (any value you can check later, such as an HMAC of the address) |
| connect request | `0x20` | `u32` sequence, the digest echoed, `string` `GameConnection`, `u32` group 0, `u32` CRC `0xFFFFFFFF`, `string` `Graal3D`, `u32` protocol 24, `u32` minimum 24, `string` password, `u32` argc, then the arguments: account, nickname |
| connect accept | `0x24` | `u32` sequence, the class table, `u32` protocol 24 |
| connect reject | `0x22` | `u32` sequence, `string` reason |
| disconnect | `0x26` | `u32` sequence, `string` reason |

The **class table** is the server's numbering of class names. Each entry is `flag 1`, `int12`
type (0 object, 1 event), `int12` id, `string` name; a `flag 0` ends it. The client maps
classes by name, so any ids work. g3dmini sends the protocol-24 set:

- objects: `Camera`, `DynamicGrass`, `DynamicGrassReplicator`, `DynamicShapeReplicator`,
  `GameObject`, `Sky`, `Sun`, `TerrainBlock`, `WaterBlock`, `fxSunLight`;
- events: `BigDataChunkEvent`, `BigDataStartEvent`, `ConnectionMessageEvent`,
  `GhostAlwaysObjectEvent`, `NetStringEvent`, `RemoteCommandEvent`, `RequestReloadEvent`,
  `TerrainChunkEvent`, `TerrainRequestUpdatesEvent`.

That accept is 276 bytes; its exact bytes are a test vector in `udp-session.md` §3, and
`test_g3dmini.py` checks them. Answer a repeated connect request with the same accept: yours may
have been lost.

### 8.5 Data packets and acks

```text
flag 1
int1   connect sequence bit (the low bit of the connect sequence)
int9   this packet's sequence, mod 512
int9   highest sequence received from the other side, mod 512
int2   type: 0 data, 1 ping, 2 ack
int3   ack byte count, 0 to 4
int(8 × count)  ack mask: bit i = (highest received − i) arrived
data packets only:
  flag → int10 update delay (ms), int10 packet size   (current rate)
  flag → int10 update delay (ms), int10 packet size   (max rate)
```

- Number data packets 1, 2, 3, ... Ping and ack packets reuse the last number.
- When the other side's "highest received" moves forward, each of your packets from the old
  value + 1 to the new one is **delivered** (its mask bit set) or **lost**. That is the only
  delivery signal. Everything else builds on it.
- Keep at most 30 unacknowledged data packets in flight.
- Answer a ping with an ack. The 5.12 acks every server data packet at once.
- The 5.12's first packet asks for 32 ms and 450 bytes. seihai-gserver sends at most one packet
  every 50 ms, each under 400 bytes, and a keep-alive every second when idle.
- Time a link out after 30 s of silence.

The `Link` class in g3dmini (`header()` and `receive()`) is about 80 lines and is the whole
numbering and ack logic.

### 8.6 Events

After the game section ([8.7](#87-the-game-section)), every data packet carries two event lists:

```text
unguaranteed: { flag 1, int12 class id, int14 bit length, payload } ... flag 0
guaranteed:   { flag 1, flag "next in order" (else int7 sequence), int12 class id,
                int14 bit length, payload } ... flag 0
```

- Guaranteed events are numbered 0, 1, 2, ... in each direction. The receiver widens the 7-bit
  number and delivers strictly in order.
- An event is done when its packet is notified delivered; a lost packet's events are sent again,
  in order. Keep at most 126 events past the oldest unacknowledged one.
- Every payload has its bit length, so a reader can skip an event it does not know.
- An event of 16,384 bits or more cannot be sent: its length would wrap, and the 5.12 crashes on
  what follows.

| Event | Payload |
|---|---|
| `RemoteCommandEvent` | `int5` argc, then each argument: `int2` code (0 empty, 1 `pstring`, 2 tag `int5`, 3 integer: sign flag, then `flag` → `int7`, else `flag` → `int15`, else `int31`). Argument 0 is the command. |
| `NetStringEvent` | `int5` tag id, `pstring` text |
| `BigDataStartEvent` | `int16` transfer, `pstring` weapon, `pstring` type, `pstring` option, `int24` length, `int3` compression (0 none) |
| `BigDataChunkEvent` | `int16` transfer, `int8` length (at most 191), the bytes |
| `TerrainChunkEvent` | `int4` chunk x, `int4` chunk y, `u32` stamp, `int10` length, the zlib bytes |
| `TerrainRequestUpdatesEvent` | 256 × `u32`: the stamp of each chunk the client holds (0 for none), row by row |

Plain-text command names (code 1) work for the mission commands; you do not need tags. The client
answers with plain text.

### 8.7 The game section

Server to client, at the start of each data packet's body:

```text
flag A   always 1
  flag B   control object follows
    u32    server time (ms)
    int12  ghost index of the player's own GameObject
    ...    a GameObject update; 13 zero flags is fine (the ghost carries the state)
flag     camera follows → int12 ghost index of a Camera, flag 0
flag     field of view follows → int8
```

- Send the control object **once**, and only after `MissionStartPhase2Ack` **and** after the
  player's ghost create is acknowledged. Sent earlier, even in the same packet as phase 2, it
  leaves the client stuck at login step 4.
- Name the camera in **every** packet once its create is acknowledged. An index the client cannot
  resolve logs "Received unknown camera object" and loses the rest of the packet.

Client to server:

```text
flag     first person
f32 × 3  the control object's position (zeros before there is one)
flag     → int12 its ghost index
flag     → a GameObject update of its own object (transform, chat, shape changes)
flag     → int8 field of view
```

There are no moves on protocol 24. The position in every packet is where the player is. Relay it
to the other players as a transform update.

### 8.8 Ghosts and the object layouts

The ghost section ends each data packet:

```text
flag     ghosts follow
int4     index width W: the bit length of the highest index in this packet (at least 1)
repeat:  flag 1, intW index, flag deleted
         if not deleted: int12 class id, int14 bit length, payload
flag 0
```

- The first update of an index is the create and must carry the whole state. The class id comes
  with every update.
- Write deletes, then creates, then updates. Free an index only after its delete is
  acknowledged. Resend a lost create whole, and a lost update's sections.

**GameObject**: thirteen sections, each a flag and, when set, its payload. All thirteen flags are
always written.

| # | Section | Payload |
|---|---|---|
| 1 | name | `pstring` |
| 2 | scale | 3 × `f32` ((0,0,0) means normal size) |
| 3 | shape | `pstring` file name; the client fetches it over TCP |
| 4 | skin | `pstring` |
| 5 | transform | position 3 × `f32`, axis 3 × `f32`, angle `f32` (radians) |
| 6 | movetype | `pstring` `interpolate`, `list` or `rigid` |
| 7 | movement data | only after a movetype; write its flag as 0 otherwise |
| 8 | shape data | `int14` length, then animation thread data |
| 9 | chat | `pstring` |
| 10 | script classes | `pstring` |
| 11 | attributes | 8 × { flag → `pstring` } |
| 12 | nickname | `pstring`, then 4 × `u8` colour (R, G, B, A) |
| 13 | flags | `int16`: 0x08 solid, 0x10 shadow, 0x20 show terrain, 0x40 collision |

**Camera**: a GameObject update, then two flags (camera mode, followed object). Write both as 0;
client scripts set the mode.

**Sun**: flag 1, `pstring` `Sun`, direction 3 × `f32`, colour 4 × `f32`, ambient 4 × `f32`.

**Sky**: flag 1, `pstring` name, flag 1, `f32` visible distance, `pstring` six textures; then fog
colour 3 × `f32`, `u32` 0 fog volumes, `u8` and `u8` (switches 1 and 2), solid colour 3 × `f32`,
`u8` (switch 3), a flag 0, three empty cloud layers (`pstring` "", `f32` 0, `f32` 0), wind 3 ×
`f32` 0, `u32` 0, a flag 0 (no storm), and the trailing flags 0, 0, 1, 0, 0, 0, 0. The client
loads the Sky textures only when it reads the Sky, so send the Sky again once the textures have
downloaded (g3dmini does this after the control object is delivered).

**TerrainBlock**: flag 1, `pstring` `Terrain`, `u32` 0, `pstring` "", `pstring` "", `f32` 1.0,
`f32` 0.01, `u32` 8, `u32` square size, `u8` repeat.

`udp-session.md` §8 has the exact bytes of a GameObject (471 bits), a Sun (379 bits) and a Sky
(956 bits), and a whole five-packet server session. g3dmini's writers match all three.

### 8.9 The mission start, in order

This is the order that works on a real 5.12, and the order g3dmini follows:

1. Handshake. Hold the accept until the TCP login is done.
2. On the client's first data packet, send `MissionStartPhase1` (a `RemoteCommandEvent`).
   Start ghosting at once, in this order: the TerrainBlock, the player's own GameObject, its
   Camera, the Sun, the Sky, water and cover, the other players, then the world objects.
3. The client answers `MissionStartPhase1Ack` and, once it has the TerrainBlock, sends a
   `TerrainRequestUpdatesEvent`. Answer it with a `TerrainChunkEvent` for every chunk whose stamp
   differs.
4. Send `MissionStartPhase2` once the TerrainBlock, Sun, Sky and water creates are acknowledged
   and every chunk event is delivered (or after 15 s). This is when the client lights the world.
5. On `MissionStartPhase2Ack`, send the control object (once its create is acknowledged). The
   client switches to the 3D view: login step 5.
6. Name the camera in every packet. Send the Sky again. Once every TCP file request has been
   answered, the client reaches step 6.

After a world switch that brings a new terrain, water or Sun, send `MissionStartPhase2` again with
the same wait. The client acks it and keeps its link, view and weapons.

### 8.10 Terrain streaming

A chunk is 16 × 16 squares. Inflated, it is a bit stream:

```text
u8      mode 2 (hole flags at the end)
int16   the height of square (0, 0), in wire units (8 to a world unit)
256 × int8  height deltas, row by row (see below)
int6    N, the number of materials used
N × int5    the material ids (indices into heights.info), sorted
if N > 1: for each square, flag 0 (no blend), then int(bits for N − 1) index into the list
256 × flag  holes (0: solid)
```

The deltas use a two-pass predictor. Pass 1: the first row against its left neighbour, the
first column against the square above, and every other square against the mean of the square
above and the square to its left (integer halving). Pass 2, from the bottom-right corner back:
each delta less half the sum of the deltas above and to its left, truncating toward zero. Every
delta is clamped to −127..127, so steep steps are lossy.

The client re-encodes each chunk it gets and stamps **its own** encoding:
`stamp = crc32(inflated bytes) ^ 0xFFFFFFFF` (CRC-32 without the final inversion). If you send
anything else, the stamps never match and every chunk goes out again on every visit. So encode,
decode the way the client does, and encode again until the bytes stop changing.
`settle_chunk()` in g3dmini does exactly that, and its test checks the result is a fixed point.

- The client keeps chunks in `levels3d/heights/<server name, with spaces as %032>/` and asks
  for `heights.info` by its bare name.
- Compressed, a chunk must fit in 1,023 bytes (the `int10` length).
- The material list in `heights.info` is one name a line. The server's `setmaterials` text
  command uses commas.

### 8.11 The text channel

Graal sends its 2D-style text over two events: a `BigDataStartEvent`, then chunks of up to 191
bytes (uncompressed is fine). The type (s2) says what it is:

- `set` and `unset`: one flag;
- `events`: lines `s <flag>` and `t <target>,<kind>,<action>,<params>`;
- `addweapon`, `weaponscript`, `deleteweapon` (s3 is the weapon name; the script as bytecode);
- `addnpc`, `setmaterials`, `rpg`;
- a non-empty s1 sends the text to that weapon's `onReceiveText`.

The client sends one `events` message with lines `w <weapon>` (a getweapon), `s <name>=<value>`
(a flag set) and `t weapon,<name>,<params>` (a serverside trigger). That last one is how
`triggerserver` arrives. g3dmini logs these; a full server routes them to the world.

### 8.12 Several players

- Ghost every other player's GameObject to each client. When a client's reported position or
  its own object update changes, mark that player's object dirty on every other client.
- When a player leaves, send a delete of its object to every other client.
- Do not trust the reported position. Check speed and teleports on the server if it matters.

### 8.13 Running g3dmini

```text
cd graal3d/examples/g3dmini
python3 g3dmini.py --make-terrain hills          # 256 demo chunks and heights.info
python3 g3dmini.py --port 14901 --world world.txt
python3 -m pytest -q                             # the vector checks and a loopback login
```

The world file is a subset of seihai-gserver's: `object` (angle in radians), `sun`, `sky`,
`spawn`, `camera`, `playershape` and `terrain`. [examples/g3dmini/README.md](examples/g3dmini/README.md)
has a sample.

What it leaves out, on purpose:

- the TCP side ([8.2](#82-the-tcp-sides-duties)); it trusts the account in the connect request;
- water, ground cover, `weapon3d`, flags, scoping and several worlds;
- movetypes, and the protocol 19 and 21 differences.

To use it with a real 5.12, a TCP server must do the login, the warp, `PLO_SERVERLISTCONNECTED`
and the file answers for the same address. Read `src/graal3d/` in seihai-gserver for a complete
server.

### 8.14 Protocols 19 and 21

**Protocol 21** (the Mac 4.20r6) is protocol 24 with one difference found so far: every Sky must
be padded to 7 texture names, and a world with no Sky should still get a plain one.

**Protocol 19** (3.153, 4.04r2) is the stock Torque game layer:

- the class table has three types: object 0, datablock 1, event 2;
- the mission start has three phases (datablocks, ghosts, lighting). 4.04r2 numbers
  `DataBlocksDone` 5 and `DataBlocksDownloadDone` 6;
- the control object is a Torque `Player` (with `tgeplayershape`) or a `Camera`;
- the client sends **moves**, which the server applies and acks;
- the server's game section starts with a `u32` last move ack and damage-flash flags;
- 3.153 runs the phases in TorqueScript, and its acks carry the phase number as a second
  argument; 3.153 also asks for Sky textures as `.gif`.

The full layouts are in [../torque/protocol19-server.md](../torque/protocol19-server.md).

### 8.15 Pitfalls

| Symptom | Cause |
|---|---|
| "Connecting..." never closes | no `PLO_SERVERLISTCONNECTED`, or a file request left unanswered |
| stuck at login step 4 | the control object went before `MissionStartPhase2Ack`, or before its create was acknowledged |
| black 3D view | no Camera ghost, or the camera not named, or the ghost table filled before the camera was ghosted |
| the client drops the link after the accept | the class table, a string or the protocol number is off by a bit; check against the 276-byte vector |
| a crash right after a ghost or event | a length field that does not match its payload, or an event of 16,384 bits or more |
| every chunk downloads on every visit | chunks not in the client's settled encoding |
| terrain without slope shading | terrain or chunks arrived after phase 2 |
| white sky | the Sky was not sent again after its textures downloaded |
| white or missing textures | a file asked for by its bare name was not found by stem, or the format does not draw |
| a frozen sky-only frame after a switch | the new world has no terrain, water or Sun |
| no ground cover | the player is in the origin cell, or the replicator came before the ground |

---

## 9. Frankenstein 6.037 and what comes next

### 9.1 Frankenstein 6.037

A community-built experimental client in graal-client-repro: the 6.03r7 program with the 5.12 3D
link and a rebuilt 5.12-style renderer folded in, and UDP left on. It runs on Windows, Linux and
macOS from the same sources. Version 0.0.1, release tag `frankenstein-6037-v0.0.1`; hit or miss.

- It logs in with the 6.03r7 token and, when it is warped to a `3 ` server, opens the protocol-24
  link beside TCP, as a 5.12 does. seihai-gserver links it.
- It draws the sky, shapes, streamed terrain, water and name tags. The 6.x frame stays as a
  small inset.
- `--renderer auto|opengl|software`: OpenGL 3.2 core by default, falling back to software where
  3.2 is missing. `FRANK_GL_LIBRARY` names a GL library to load instead (for example Mesa's
  `opengl32.dll` on a Windows machine with no GPU driver).
- `--max-fps N` (60 by default; 0 for no cap), a frame counter (`--no-fps` hides it), and `--bench`
  for frame rates on test worlds.
- It reads `visibledistance3D` from a `game_config.txt` beside it (1,000 by default, at most
  2,400).

With software OpenGL on a 4-core cloud machine, the OpenGL renderer ran 2.4 to 12.8 times faster
than the software one, with pixels matching to within 0.01 %. A real GPU is much faster.

### 9.2 `seihai3d/1`: room to grow

The original clients are fixed. For features none of them has, seihai-core defines a versioned
extension handshake, `seihai3d/1`:

- A Seihai client adds a third connect argument, `seihai3d/<version>/<capabilities in hex>`.
- A Seihai server answers with a `RemoteCommandEvent` `seihai3d` before `MissionStartPhase1`,
  naming what it will use.
- The capability bits reserved so far: 0 frame stats, 1 chat in 3D, 2 a world terrain cache,
  3 chunk relight, 4 view distance, 5 fast pacing, 6 wide ghosts, 7 world chunks.

A real 4.20r8 or 5.x never sends the argument, so nothing changes for them. Only the wire
contract exists; no server or client uses it yet. The contract is in
[../torque/seihai3d-ext-v1.md](../torque/seihai3d-ext-v1.md).

---

## 10. Limits at a glance

All on a real 5.12 unless noted.

| Limit | Value | What to do |
|---|---|---|
| Ghosts a client holds | 4,096 | scoping; the server ghosts at most 3,584 world objects to one client |
| Terrain grid | 256 × 256 squares in 16 × 16 chunks, one `TerrainBlock` a world | large terrains slide the grid; regions |
| Terrain chunk | 1,023 bytes compressed | the tools keep chunks small |
| Square size | 1 to 64, use 8 | |
| Draw distance | 1,000 by default, at most 2,400 (the player's setting); fog at 0.85 times it | keep content within 1,000 of the camera |
| Field of view | 90° across, about 73.7° up and down at 4:3 | size sky faces to the window |
| Near-terrain band | within about 150 units the tile layer covers the terrain, fully below about 75 | a `TilesControl` weapon (sent by seihai-gserver) |
| Ground cover | none while the player is in the origin cell (\|x\| and \|y\| under 8) | spawn elsewhere |
| Lighting | only at `MissionStartPhase2` | hold phase 2; send it again after switches and slides |
| Shapes | `.dts` version 24; `.3ds` with a material; about 100k triangles or 2 MB a shape | the start-up check |
| `.3ds` mesh | 65,535 vertices | split meshes |
| Textures | 8-bit PNG, JPEG, GIF; up to 1,024 a side; no alpha blending | |
| Terrain textures | 256 × 256, 24-bit; named with extension in `heights.info` | |
| Packets | the client asks for 32 ms and 450 bytes; seihai-gserver sends 50 ms and 400 bytes | `graal3d_sendms` |
| Creates | about 130 to 140 a second at 50 ms | scoping; `graal3d_sendms` |
| Events | 126 in flight; under 16,384 bits each | |
| Timeouts | 30 s silence; about 15 s for the connect | |
| Memory | about 620 MB committed at the dense end, of the 2 GB a 5.12 can address | |
| Timer | `setTimer(0.05)` runs 7 to 15 times a second | move by the clock |
| Collision | none on the client | the script or the server decides |
| Script-made objects | not drawn | ghost them from the server |
| `findobject` on world objects | NULL | |
| `server.` flags | read empty | use `serverr.` |
| World switch | freezes into a world with no terrain, water or Sun | give every world a Sun |
| Full screen | stays at "Connecting..." | play in a window |
| Positions (seihai-gserver) | 100,000 units from the origin | |

## 11. Troubleshooting

**The client never leaves "Connecting...".** The server did not send `PLO_SERVERLISTCONNECTED`, or
a file request is unanswered. Check that every requested file got the file or a refusal.

**"The connection to the Graal3D server couldn't be established."** No accept came within about
15 s. Check that the UDP port is the TCP port + 1, that it is open, and that the TCP login came
from the same address with the same account (`guest` for a 5.x guest).

**Stuck at step 4, or the 3D GUI never appears.** The control object was sent too early ([8.7](#87-the-game-section)).

**The 3D view is black.** There is no Camera, or the client never got its create. On a big world,
the ghost table filled first: turn on scoping.

**The sky is white.** The Sky arrived before its textures. The server must send the Sky again
after the downloads. Check that the face names are found by their bare stem.

**Textures draw white.** The format does not draw on a 5.12 (BMP, TGA, DDS, 16-bit PNG), or the
file was not found by its lower-cased stem.

**A shape does not show.** A `.3ds` with no material draws nothing; a `.dts` must be version 24.
Read the start-up check. Script-made objects never draw.

**The terrain is white on the first visit.** Turn on `graal3d_pushterrain`, or relink: the
client fetches terrain textures on its second visit.

**The ground near the camera is all one texture (often water).** No `TilesControl` weapon. Send
the one in [5.8](#58-terrain).

**The terrain has no slope shading.** It arrived after phase 2. Use a server that holds phase 2,
and sends it again after a world switch or a terrain slide.

**Every chunk downloads every time.** The chunks are not in the client's settled encoding.
Regenerate them with `gen terrain --stream`.

**No grass.** The player stands in the origin cell, the grass names a shape instead of a texture,
the texture is mostly transparent, or there is no ground under the cells.

**The client freezes after a warp.** The new world has no terrain, water or Sun.

**`server.` flags are empty in a 3D script.** Use `serverr.` flags.

**Players walk through walls.** There is no client collision. The walker script must stop them.

**The player does not move.** The 5.12 does not walk by itself; send a walker weapon.

**A changed texture or shape does not show.** The client fetches a file once a session. Relink.
For a rollback, give the old file a new modification time.

**No chat in the 3D view.** The 2D chat line does not draw in 3D. A script's `player.chat` reaches
the other 3D players through the object's chat section, and they see it in `onRemotePlayerChats`.
Draw your own chat display with `showimg`.

**The client dropped with "corrupt deflate stream" right after the terrain push.** A gen-5 TCP
issue seen in 3 of 18 lab runs. seihai-gserver retries and logs it; the cause is still being
looked for.

**A client crashed on your content.** The 3D clients trust their files. Run the start-up check
with `graal3d_shapecheck = skip`, and keep shapes and images within the limits above.

## 12. Glossary

| Term | Meaning |
|---|---|
| Camera | the ghost the 5.x client draws its view through |
| chunk | 16 × 16 terrain squares, one `heights<x>-<y>.dat` file |
| class table | the server's numbering of class names, sent in the connect accept |
| control object | the player's own GameObject, named once in the game section |
| event | a message on the link; guaranteed events arrive in order |
| GameObject | Graal's drawable 3D object: a shape with a transform and Graal properties |
| ghost | an object the server mirrors to one client, by index |
| login step | the 5.12's progress through a 3D join, 2 to 6, seen by `onGraal3DLoginStep` |
| Mission Lighting | phase 2 of the mission start, when the client lights the world |
| notify | the per-packet "delivered or lost" signal everything is built on |
| portal | a world-file door that brings a far part of the same world into scope |
| protocol 19, 21, 24 | the Torque protocol versions of the 3.153/4.04r2, the Mac 4.20r6, and the 4.20r8/5.x clients |
| region | one folder of a world built from a grid of pieces |
| scoping | sending only the objects near a player |
| stamp | the CRC the client keeps for each chunk it holds |
| `TilesControl` | the client object the 5.x asks for near-terrain tiles |
| `weapon3d` | a GS2 weapon the server sends to 3D clients |

## 13. Where the facts come from

The behaviour in this guide was measured on real clients in headless lab VMs, against our own
servers, on a closed network; or read from the client programs, written up as behaviour. The
detailed notes are in this repository:

- the wire: [../torque/udp-session.md](../torque/udp-session.md),
  [../torque/protocol19-server.md](../torque/protocol19-server.md);
- terrain: [../torque/terrain-512.md](../torque/terrain-512.md);
- the research board, 167 questions of which about 157 are answered:
  [../torque/3d-capability-board.md](../torque/3d-capability-board.md);
- the conformance suite (the real 5.12 passes 37 of 40 cases run on it):
  [../torque/conformance/README.md](../torque/conformance/README.md);
- the GS2 surface: [../torque/gs2-3d-typed-surface-512-2026-11-26.md](../torque/gs2-3d-typed-surface-512-2026-11-26.md);
- sky, draw distance, shapes, two clients, events and the camera:
  [../torque/3d-win10-sky-prefs-scripting-512-2026-11-26.md](../torque/3d-win10-sky-prefs-scripting-512-2026-11-26.md);
- big worlds: [../torque/3d-big-world-streaming-512-2026-11-27.md](../torque/3d-big-world-streaming-512-2026-11-27.md);
- interiors: [../torque/3d-interiors-in-world-512-2026-11-27.md](../torque/3d-interiors-in-world-512-2026-11-27.md);
- world switches and lighting:
  [../torque/3d-worldswitch-terrain-lighting-512-2026-11-26.md](../torque/3d-worldswitch-terrain-lighting-512-2026-11-26.md);
- grass: [../torque/grass-512-sweep-2026-11-27.md](../torque/grass-512-sweep-2026-11-27.md);
- the extension contract: [../torque/seihai3d-ext-v1.md](../torque/seihai3d-ext-v1.md).

In the other Seihai repositories:

- seihai-gserver: `docs/GRAAL3D.md`, the server's own 3D manual, and `src/graal3d/`;
- seihai-gserver-v2: `bin/docs/graal3d.md` and `addons/graal3d/README.md`;
- seihai-servertools: `tools/gen`, `tools/pw3d`, `tools/regions`, `tools/edit3d`;
- graal-client-repro: `frankenstein-6037/README.md` and `common/cpp/graal3dengine/`.

Corrections and new findings are welcome as pull requests. Keep lab captures, raw logs, client
binaries and real server addresses out of them; write up the behaviour.

Seihai is a community project. It is not affiliated with GraalOnline.
