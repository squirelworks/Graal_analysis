# 5.12 on Windows 10: sky, shape limits, video prefs, two-client interaction and script surface (2026-11-26)

Date: 2026-11-26. Lab runs inside one headless Windows 10 lab VM with no network cable and the
clock held at 2007-11-19. Our own **seihai-gserver-v2 at `1d74282e`** (Windows CI build, world
`lab3d`) and the lobby/UDP relay ran inside the same guest on loopback, with up to two copies of
the real **5.12** client. Renderer: Windows' GDI Generic OpenGL 1.1 (software). Captures stay in
the owner-held lab kit. Board rows: T3D-086, T3D-037 (part 2), T3D-051, T3D-074, T3D-070,
T3D-116, T3D-134 to T3D-140; refines T3D-075. Part 1 of this batch:
[3d-scoping-interiors-limits-512-2026-11-26.md](3d-scoping-interiors-limits-512-2026-11-26.md).
**[lab]**

## T3D-075 refined: the draw cut is the client's `visibledistance3D`

The ~1000-unit cut found in part 1 is the client's own `visibledistance3D` setting in
`game_config.txt` (default 1000). Cubes at camera distances 300 … 4500, Sky distance field 5000:

| Set in game_config | Saved on exit | Effect |
|---|---|---|
| (defaults) | visible 1000, fog 850 | cubes to about 1000 drawn |
| visible 500 | visible 500, **fog 425** | only the 300-unit cube |
| visible 2000 | visible 2000, fog 1700 | cubes to 2000 drawn |
| visible 5000, fog 4000 | **visible 2400, fog 2040** | clamped at 2400 |
| fog 100 | **fog 850** | ignored |

- `visibledistance3D` is the draw distance, **clamped to 2400**; `fogdistance3D` is always reset to
  **0.85 × the visible distance**, whatever is written.
- The server never sees a player's draw distance, so content more than 1000 units from the
  camera is invisible to a default client.

## T3D-086: sky flags, cloud layers, bottom face, magnification

Six labelled 256×256 checker faces (one colour each, a line every 64 texels); camera 2 units
above spawn looking level, up (1.2 rad) or down; one change per run.

| Flags | Up | Level | Down |
|---|---|---|---|
| 000 | solid sky colour | solid colour + fog band; black below the horizon | black |
| 100 | **textured sky box** | textured side face to the horizon, fogged there; black below | black |
| 010 | solid colour | as 000 | **lower half in the solid colour** |
| 001 | as 000 | as 000 | as 000 |
| 111 | as 100 | as 100 | **bottom face drawn, textured** |

- **Flag 1 = use the sky textures** (off: the faces are downloaded but the solid colour draws).
- **Flag 2 = render the bottom** (off: black below the horizon, and camera moves leave trails
  there because it is never cleared).
- **Flag 3:** no visible change.
- **Face slots:** a camera facing +y sees the 3rd texture, with its label flipped, so the slots
  do not follow "front = +y".
- **Cloud layers:** with 1, 2 or 3 cloud textures after the six faces, or a cloud in slot 7, every
  file downloaded but **no cloud layer drew**. Either the cloud fields need the storm/wind
  sections our server leaves clear, or the software GL 1.1 renderer doesn't draw them. Open.

**The "2× magnification" is the field of view.** The 64-texel lines are evenly spaced so that
256 texels span the whole 3D view; from the horizon to the top edge there are about 94 texels,
which is tan(36.9°) × 128. So **one face fills exactly the 90° horizontal field of view**: a
256-px face on an 800-wide view shows at about 3.1 screen px per texel, a 512-px face on a
1024-wide view at 2×. **5.12's field of view is 90° horizontal, about 73.7° vertical at 4:3.**
For a sharp sky, use faces about as wide as the window.

## T3D-037 part 2: one shape's vertices and triangles

| Shape | File size | Drawn | Crash/hang |
|---|---|---|---|
| 968 tris, 529 verts, 1 mesh | 16 KB | yes | no |
| 10 082 tris, 5 184 verts | 163 KB | yes | no |
| 65 522 tris, 33 124 verts, 1 mesh | 1.05 MB | yes | no |
| 21 845 tris, **65 535 verts in one mesh** | 1.0 MB | yes | no |
| **131 070 verts** in one shape (2 meshes) | 2.0 MB | yes | no |
| 99 856 tris (2 meshes) | 1.6 MB | yes | no |
| 1 048 352 tris (16 meshes) | 16.8 MB | **no** | **stalled**: no download-done line; after "Initial Control Object" the client stopped answering on the 3D link and the server timed it out |

- **No per-shape vertex limit**: 131 070 vertices across two meshes drew. The only 16-bit limit
  is the `.3ds` per-mesh cap.
- **About 100k triangles (1.6 MB) per shape works; a 16.8 MB, 1M-triangle shape stalls 5.12**
  (download and parse were not separated). Keep shape files well under that.
- **10 000 objects:** the server filled its 4096-slot table and refused the Camera and 5907
  GameObjects; the client held the link without crashing. The ceiling is the server's (part 1).

## T3D-051: renderer pick and video prefs

- At start 5.12 logs Torque's device probe: an accelerated OpenGL device detected, no D3D device,
  no Voodoo 2; it activates the OpenGL device, windowed. GL reports the GDI Generic 1.1 renderer
  with only the paletted-texture extension. **There is no D3D switch for 3D**; in full screen the
  2D layer reports Direct3D 7.
- The 3D prefs in `game_config.txt`: `visibledistance3D` (default 1000), `fogdistance3D` (850),
  `detailfactor3D` (1), `startinfullscreen`, `fullscreenmode` (640x480), `fullscreenbitdepth`
  (16), `fullscreenrefresh`, `screenshotformat` (PNG), `lock3Darrays`; `defaultguistyle` is a
  client string.
- Effects: visible/fog as in the T3D-075 table; `detailfactor3D` 0.1 made no visible change
  (single-detail cubes); `startinfullscreen` gave a 640×480 full screen that stayed at
  "Connecting…" — **the 3D link never came up in full screen** in 45 s.

## T3D-074 + T3D-070: two 5.12 clients in a world with GameObjects

A at the spawn, B at the first ring point, a named Cube nearby.

**What A's own changes do (T3D-070):**

| A's script | Relayed to B | B's client |
|---|---|---|
| chat | yes | `onRemotePlayerChats` fires with the text |
| shape = a new `.3ds` | yes | **downloads the new shape from the server on demand** |
| attr[1] = an image | yes | no image request |
| nickname | yes | — |
| server `g3dpos` moves | yes | — |

**Interaction (T3D-074):**

| B's script | Result |
|---|---|
| `findobject` on A's player and on "Cube" | **NULL every time**: scripts can't reach other ghosts or world objects |
| `player.position` onto A, then into the Cube | accepted and relayed; `checkCollision()` 0, `getdropz()` 0, `isInInterior()` 0, no events |
| `mountObject` / `unmount` | 0; `isMounted()` 0 (NULL targets) |
| `player.attachedtoobject = A` | stays empty; does not follow A |
| `onCollision` / `onWallCollision` / `onMount` / `onUnmount` | never fired |

- **Players and shapes overlap freely; there is no client-side collision.**
- **Mount and attach can't be driven from the client**; they would need a server-set ghost field
  that our server does not send.
- **5.12 runs TCP weapon scripts in 3D:** B's weapon cached from a 2D visit ran in 3D, and its
  `player.x += 3` moved B's 3D object (relayed).

## T3D-116: 3D client and 2D client on the same server

A linked to 3D; B on the same server playing 2D with a test weapon.

| What | From | Reached the other client |
|---|---|---|
| chat | 2D (B) | **yes**: A's `onRemotePlayerChats`, through the server-made G2DPlayer ghost |
| chat | 3D (A) | the server turns it into A's TCP chat property, but **B's script can't see it** (B's `players` counts 2, with no usable entry for A) |
| B moves (`player.x += 3`) | 2D | the 2D ghost on A did not move |
| PM | 2D → 3D | **no** (nothing in the server log, no `onReceivePM`) |
| PM | 3D → 2D | no |
| `client.` flags | each | set locally only; the other side can't see them |
| `server.` flag via a serverside weapon action | both | inconclusive (no sign the action ran) |

## T3D-137: coordinates, units, rotation order

An axes shape (origin cube; red +x 6, green +y 4, blue +z 2) placed six times:

| Placement | Drawn |
|---|---|
| no rotation | red +x, green +y, blue +z |
| z +90° | red toward −y, green toward +x |
| x +90° | green −z, blue +y |
| y +90° | red +z, blue −x |
| axis (1,1,0) 60°, scale 2,1,1 | red doubled along the shape's own x, then rotated |

- **Axes:** Torque's, z up. **Units:** 1 unit = 1 tile on our server's mapping, with 3D (x, y) =
  tile (x, −y).
- **Origin:** the shape's own origin sits exactly on the world point.
- **Rotation sense: opposite to the right-hand rule** (positive about z is clockwise seen from
  above).
- **Order:** scale (shape axes), then one axis-angle rotation, then translation.
- **Script side:** `rotation` reads as axis + angle in degrees; `eulerrotation` only reflects
  values a script wrote.
- **2D tie:** our server ties 3D to 2D only for the player's TCP position, and only when x ≥ 0 and
  y ≤ 0 (it logs "tcp position not set … off the map" otherwise).

## T3D-138: 3D replaces the 2D view

No tiles, signs or level NPCs draw in 3D, and `player.level` reads empty. A **`showimg` overlay
does draw over the 3D view** and moves with updates. `showtext` and a new `GuiTextCtrl` were not
visible (the control was created but its object type read empty).

## T3D-139: clientside callbacks in a 3D session

- **Fire:** `onCreated`; `onPlayerEnters` (once, for itself); `onGraal3DLoginStep` (steps 4, 5,
  6); `onTimeout`; `onMouseDown` / `onMouseUp` (button, with mouse x/y in tile units);
  `onKeyPressed` (key code, repeats while held).
- **Never fire:** `onKeyDown`/`Up`, `onMouseWheel`, `onActionLeftMouse`, `onCollision`,
  `onWallCollision`, `onObjectClicked`, `onClick`, `onFrame`, `onRender`, `onCameraMove`/`Changed`,
  `onMove`, `onMovementFinished`, `onResize`, `onPlayerTouchsMe`, `onWeaponFired`,
  `onGhostAlwaysStarted`, `onConnectionAccepted`, and the movement/jump hooks.
- **No per-frame, object-click or camera-move event.**

## T3D-140: live pose and a tracking overlay

- **Timer cap:** `setTimer(0.05)` runs about 7 times a second unfocused and 14–15 focused; that
  is the finest pose sampling a script gets.
- **Pose:** camera and player position, `eulerrotation`, `rotation`, forward/up/right vectors and
  `worldBox` are all readable live; an orbit's read-backs matched each set value.
- **Overlay:** a `showimg` marker tracked the camera. So a HUD, minimap or compass is possible at
  timer rate.

## T3D-134 / 135 / 136: server-driven camera, level warp, per-player objects

- **T3D-134:** the client owns the camera. Scripts move `ServerConnection.camera`; our server
  sends the Camera ghost once and cannot update it at runtime; `fov` reads empty. A server-driven
  camera needs server work (runtime Camera ghost updates).
- **T3D-135 / T3D-136: blocked on the server.** Our server has one 3D world, no second 3D level
  and no per-client ghosting from GS2. Client scripts can't hide world objects either
  (`findobject` is NULL). Not run.

## For a server

- Default draw distance is 1000 (max 2400, set by the player); put important content within it.
- Sky: set flag 1 for textures, flag 2 for a bottom; size faces to the window width.
- Keep shape files ≲ 2 MB / 100k triangles; there is no per-shape vertex cap above the per-mesh
  `.3ds` limit.
- Collision, mounting, other-player PMs, per-player objects and camera control all have to be
  server features; the client script surface can't do them.
- Clientside scripts can build a HUD from live pose at ≤ 15 Hz, with `showimg`.
