# What a level author can place in a 3D world, and what draws per build (T3D-106)

Date: 2026-11-25. Read of the lab gserver's 3D scene-file parser and per-protocol ghost logic, synthesised with T3D-081 (networked classes), T3D-109 (two protocol encodings) and T3D-088 (GS2 surface). Board row: [T3D-106](3d-capability-board.tsv). "Lab gserver" is our own loopback 3D server (the facts below are its current authoring surface, not a client limit unless noted).

## The authoring surface the lab gserver accepts **[srv]**

The 3D scene file accepts **exactly these 10 keywords**; `#` starts a comment, and an unrecognised keyword or wrong field count is logged and ignored.

| keyword | fields | notes |
| --- | --- | --- |
| `object NAME SHAPE x y z [ax ay az angle]` | name, shape file, position (3), optional rotation (axis + angle; default `0 0 1 0`) | a **GameObject**. No scale, no skin/texture, no flags field — only name/shape/position/rotation |
| `sun dx dy dz  cr cg cb ca  ar ag ab aa` | direction (3), colour RGBA (4), ambient RGBA (4) | the directional light |
| `sky MATERIALS [distance] [fogR fogG fogB]` | texture list (comma-joined, `-` = none), visible distance, fog colour | the sky box; 2, 3 or 6 tokens |
| `skyoptions b0 b1 b2 solidR solidG solidB` | 3 bool flags + solid colour — modifies the most recent `sky` | needs a preceding `sky` |
| `playershape SHAPE` | shape file | the protocol-24 player control object's shape (a GameObject) |
| `tgeplayershape SHAPE` | shape file | the protocol-19 TGE Player/Camera control shape (a `.dts`) |
| `tgecontrol player\|camera` | one word | protocol-19 control mode (walking Player vs free Camera) |
| `spawn x y z` | position (3) | where the control object starts |
| `camera x y z [ax ay az angle]` | offset from spawn (3) + optional rotation | the Camera ghost's placement |
| `weapon3d NAME FILE` | weapon name, script file (plain relative path) | a client-side GS2 weapon over the 3D text channel |

**That is the whole author surface today.** There is no keyword for terrain, water, interiors, items, triggers, particles, markers, audio emitters, precipitation or lightning — none of the 11 TGE content classes ([T3D-081](3d-object-classes-by-build-2026-11-25.md)) can be written into a lab world file, because the server has no syntax and no emit path for them.

### GameObject fields that reach the client

The server sends a GameObject create with NAME, TRANSFORM and FLAGS always, and SHAPE / VELOCITY / SKIN / CHAT / NICKNAME / per-slot ATTR only when non-empty. From a world `object` line only **name, shape, position, rotation** are set, so those (plus default flags) are what reach the client. The other GameObject fields exist in the protocol but are **not author-settable from the world file** — skin/texture override, chat, nickname, attributes and velocity are set at runtime (the player's own updates or script), never by the `object` line. (A shape's own material texture is authored inside the `.3ds`, [T3D-090](3d-shape-textures-420r6-2026-11-25.md), not as a world field.)

## What reaches and draws on each build **[lab/bin]**

The server branches on the client's protocol at login (confirmed in source, live in [T3D-109](3d-shared-world-subset-2026-11-25.md)):

- **Protocol 24 (5.12-class: 4.20r6/r8, 5.00r7, 5.12):** sends every scene object — Sun, Sky, all `object` GameObjects — plus the player control GameObject, any other players as GameObjects, and the client's own Camera.
- **Protocol 19 (4.04r2):** sends **only the Sky** from the scene (a plain one if the world has none), plus the stock TGE control — a `TgePlayer` (from `tgeplayershape`, with `tgecontrol player`) or a `TgeCamera` — preceded by its datablock. **Sun and GameObjects are skipped entirely for protocol 19.**

| placeable | fields | draws on 24? | draws on 19? |
| --- | --- | --- | --- |
| `object` (GameObject) | name, shape, pos, rot | yes — drawn at its transform ([T3D-090](3d-shape-textures-420r6-2026-11-25.md)/[T3D-091](3d-world-limits-420r6-2026-11-25.md)) | no — not sent to a 19 client (authorable-but-inert for 19) |
| `sun` | direction, colour, ambient | yes — Sun ghost drives lighting ([T3D-111](3d-state-authority-420r6-2026-11-25.md)) | no Sun ghost — 19 is lit by its own Mission-Lighting phase |
| `sky` | materials, distance, fog | yes — Sky ghost | yes — Sky ghost (padded for TGE) |
| `skyoptions` | 3 bools, solid colour | yes — modifies the Sky | yes — part of the Sky sent to 19 |
| `playershape` | shape | yes — the 24 control GameObject | inert — 19 uses `tgeplayershape` |
| `tgeplayershape` | shape | inert — 24 uses `playershape`/GameObject | yes — the TGE control shape ([T3D-109](3d-shared-world-subset-2026-11-25.md)) |
| `tgecontrol` | player/camera | inert — 24 always uses a GameObject control + its own Camera | yes — walking Player vs free Camera on 19 |
| `spawn` | pos | yes | yes |
| `camera` | offset, rot | yes — the Camera ghost | yes — the Camera |
| `weapon3d` | name, file | yes — GS2 weapon runs ([T3D-018](3d-client-events-420r6-2026-11-25.md)) | likely (4.04r2 has the GS2 console, [T3D-088](3d-gs2-functions-by-build-2026-11-25.md)); delivery/run on 19 not confirmed |

## Author-facing summary

- **For a 5.12-class (protocol-24) world**, the placeable set that draws is essentially `{ sky (+skyoptions), sun, camera, object = GameObject shape (name, shape, position, rotation), playershape, weapon3d }`. The author-settable GameObject fields that reach the client are **name, shape, position, rotation** — nothing else (no scale, no per-object skin/texture, no flags beyond default).
- **For a 4.04r2 (protocol-19) client**, the gserver currently emits only `{ sky, stock TGE Player/Camera (tgeplayershape + tgecontrol), camera, spawn }`. The author's `sun` and `object`/GameObject lines are **dropped for 19**. The full TGE datablock content ([T3D-081](3d-object-classes-by-build-2026-11-25.md)) is **not authorable at all** on this server — no world syntax, no emit path.

### Three categories for an author

- **Authorable and draws:** the "yes" rows above, per protocol.
- **Authorable but inert on a given protocol:** `sun` and `object` on a 19 client; `tgeplayershape`/`tgecontrol`/`playershape` on a 24 client; `skyoptions` with no preceding `sky`.
- **Not authorable at all on the current server:** terrain/water, and all 11 TGE content classes (interiors, items, static shapes, triggers, markers, zones, particles, audio emitters, precipitation, lightning); also per-object GameObject skin/texture, chat, nickname, attributes, velocity (protocol fields with no world syntax).
