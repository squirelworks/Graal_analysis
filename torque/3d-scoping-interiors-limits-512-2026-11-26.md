# 5.12 scoping, interiors, parity, ghost ceiling and frame rate (2026-11-26)

Date: 2026-11-26. Lab runs in a headless Debian lab VM, each in its own private network
namespace on loopback, against our own **seihai-gserver-v2 at `1d74282e`** (Linux CI build;
world `lab3d`, `graal3d` and `graal3dtrace` on). Clients: the real Windows **5.12**
(`G3D14097`) under Wine with Mesa llvmpipe, one Xvfb display and one Wine prefix per client;
the real **Linux 4.20r6** (`G3D22126`), native, Mesa llvmpipe. Shapes, worlds and textures were
generated for these runs; the `.dif` files are from the Marble Blast Gold demo. Captures stay in
the owner-held lab kit. Board rows: T3D-075, T3D-083, T3D-087, T3D-030, T3D-026, T3D-037
(part 1), T3D-113 (5.12 first pass). **[lab]**

## T3D-075 / T3D-083: how other players are scoped and drawn

Three real 5.12 clients (A, B, C), joined 20 s apart. Every player shape is an 8-unit red cube,
no ground; camera 40 back and 16 up from spawn. The server moved B outward along (0.3d, d, 0)
and back, 6 s per step; each step was judged on A's frame 3.5–5.8 s after the server relayed
B's position, by counting cube-coloured pixels (9045 = A's and C's own cubes only).

**Ghosts.** Each client got one GameObject `G3DPlayer_<account>` ghost per other player at link
time. None was deleted or re-created on the walk to 5000 units and back; the only kills came
when a client left. Our server does not scope by distance (every player is ghosted to every 3D
client) and the client never asked for scoping or dropped a ghost itself.

**What A draws** (Sky visible-distance field 500; a second run with 3000 gave the same counts):

| d | B→camera | cube px on A | drawn |
|---|---|---|---|
| 10 | 51 | 10390 | yes |
| 100 | 141 | 9802 | yes |
| 250 | 297 | 9232 | yes |
| 500 | 561 | 9101 | yes |
| 600 | 665 | 9078 | yes (≈2 px) |
| 1000 | 1082 | 9045 | **no** |
| 2000 / 5000 | 2126 / 5258 | 9045 | no |
| back down to 10 | | as on the way out | yes from 600 |

C saw the same as A at every step.

**Pinning the cut.** B stepped by camera distance 600 → 1200 in 50s, then 1500, 2000, and back
in 100s, once as an 8-unit cube and once scaled 10× (80 units, relayed by the server):

| Camera distance of B's centre | ≤ 1000 | 1050 | 1100–2000 | back 1100 | back ≤ 1000 |
|---|---|---|---|---|---|
| 80-unit cube | drawn | gone | gone | gone | drawn |
| 8-unit cube | drawn | gone | gone | gone | drawn |

- **5.12 stops drawing any object whose centre is more than about 1000–1050 units from the
  camera.** The cut is the same for an object ten times larger, so it is a centre-distance cut,
  not sub-pixel culling (the 8-unit cube would still be 3–4 px wide at 1082).
- The whole object goes at once, with **no fog fade and no hysteresis**, and the cut **ignores
  the Sky visible-distance field** (B drew at 665 with the field at 500).
- Client scripts never see other players: `players` stayed 0, `onPlayerEnters` fired once per
  client for itself only, and `onGhostAlwaysObjectReceived` never fired.

**Hide flags** (B parked at d = 50):

| B's script | reaches the server | drawn on A | drawn on B |
|---|---|---|---|
| `player.visible = false` (reads back 0) | no | yes | yes |
| `player.hidden = true` (reads back 1) | no | yes | yes |
| `player.scale = 0.01` | yes, relayed to the others | **no** | no |
| `player.scale = 1` | yes | yes again | yes |

The GameObject has no script-side hidden or visible property that takes effect or reaches the
server. The only client-side way to hide a player is to scale it to almost nothing; otherwise
the server must not ghost it, or must kill the ghost.

**Ghost cap per client:** one shared 4096-entry budget for player and object ghosts (below,
T3D-037).

## T3D-087 / T3D-030: interiors

One 5.12 client, one interior per run as a GameObject shape at the origin. The server serves
the file unchecked.

**Damaged v44 files** (source: an intact 27 KB MBG track):

| File | Client console | Drawn | Crash/hang |
|---|---|---|---|
| intact | "Room lit in 0.000 seconds" | yes | no |
| first 8 bytes only | "Interior::read: incompatible file version found." + "Unable to read detail level 0 in interior resource" | no | no |
| first 10 % / 50 % / 90 % | "Unable to read detail level 0 …" | no | no |
| last 16 bytes cut | **no error line**, no "lit" line | no | no |
| 2 KB zeroed mid-file | "Unable to read detail level 0 …" | no | no |
| version field set to all-ones | "incompatible file version found." | no | no |

- **All or nothing:** every damaged file is dropped whole; the rest of the world keeps drawing
  and the link holds. Nothing crashed or hung in 8 runs (agrees with T3D-038).
- **One silent case:** a file short by its last 16 bytes leaves no console message. A server
  should validate its own `.dif` files.

**Lightmaps.** A second v44 track drew untextured (its textures were not served); the console
said "Failed to load lightmap of Room, will regenerate it", then "Room lit", after the client
asked the server for a lightmap `.dat` file (not found). Rerunning the same `.dif` with the same
client folder gave "Loaded lightmap for Room from file": **5.12 caches interior lightmaps
locally and reuses them.** In one later run a cached `.dif` drew solid black with no "lit" or
lightmap line; the cause is not settled (rerun with the cache cleared).

**Player-carried camera.** A client script can drive the view: `ServerConnection.camera` is the
client's own Camera ghost (position, `cameramode` "free", `eulerrotation`). Setting position and
rotation every 0.25 s kept the camera 3 behind and 1.5 above the player while the server stepped
the player through the interior at floor height; the view followed it onto the track and drew
the floor up close. The player still passed through the geometry: no collision, no gravity.

**Client-driven movement:** none exists on this route. 5.12 never moves its own player; position
comes only from the server (`g3dpos`) or `player.position`. So collision under client movement
cannot be tested here.

**Portals and zones: still blocked.** No zone culling was seen from inside or outside, but both
tracks are open. None of the 12 MBG demo `.dif` files is an enclosed, zoned building and we
have no `.dif` authoring tool. The camera half of the test now works; it needs an enclosed v44
interior.

**4.04r2 and `.dif`:** the 4.04r2 engine does register `InteriorInstance` (T3D-081); it is the
5.12-class engine that lacks it and draws `.dif` as a GameObject shape. Our gserver cannot serve
one to 4.04r2: its protocol-19 ghost-class table is Camera, Player, Sky, TerrainBlock and
WaterBlock, and its protocol-19 path sends no world objects. That needs a server-side
`InteriorInstance` writer; not run.

## T3D-026: 4.20r6 vs 5.12 at the GameObject level

One world (a `.3ds` ground and cube, a DTS-24 octahedron, a v44 `.dif`, Sun, Sky, camera), the
same server binary, each client alone for 75 s, plus a control world without the DTS and DIF.

| | 5.12 | Linux 4.20r6 |
|---|---|---|
| Torque protocol | 24 | 24 |
| Ghost order | Ground, Cube, Octa, Room (GameObjects), Sun, Sky, own G3DPlayer, Camera | **identical** |
| Ghost update masks and sizes | GameObject, own player, Sun, Sky, Camera | identical (own player and Camera differ only by account-name length) |
| Mission start | Phase 1 "Download Ghost Objects", Phase 2 "Mission Lighting", both acked, then "Initial Control Object" | identical |
| Client sends | Phase 1 ack, Phase 2 ack, one control-object state change, then idle | identical |
| Files requested | shapes, `.dif` textures, stock interior textures, sky faces without extension | shapes and the `.dif`; **no textures** (known) |
| Drawn | ground, cube, octahedron, interior, sky box | same objects in the same places, untextured white; 640×480 window vs 800×600 |
| Crash/hang | none | none |

**Same at the GameObject level:** one server path serves both builds; the differences are
client-side only (no textures on 4.20r6, smaller window). Already on the board and not re-run:
DTS 17 froze 4.20 Linux, and 4.20r8 crashes on a TerrainBlock.

## T3D-037 part 1: object and ghost count (5.12)

| Objects (1-unit cubes) | Ghosts | Time to ghost | Drawn | Crash/hang |
|---|---|---|---|---|
| 2000 | 2004 | 14.4 s | yes | no |
| 4000 | 4004 | 30.3 s | yes | no |
| 4092 | 4096 (table full) | 30.7 s | yes | no |
| 4093 | 4096; server: "cannot ghost Camera: no class id or ghost slot" | 31 s | **black window** (no Camera) | no |
| 5000 | 4096; Camera and 907 GameObjects refused | — | black | no |

- **5.12 accepts and draws a full 4096-entry ghost table.** Our server's 4096-slot table runs
  out first, so the client's own ceiling was not reached.
- **Our server ghosts world objects before the Camera**, so a full table blacks out the view.
  A server should reserve the Camera's slot, or cap a world at 4092 minus the player count
  (4 fixed ghosts: Sun, Sky, own player, Camera).
- Ghosting rate: about 130–140 new ghosts per second on loopback.
- Not yet run: single-shape vertex and triangle limits (around the 65 535-vertex mark and up to
  1M triangles); those continue in the Windows 10 VM.

## T3D-113 on 5.12: frame rate (first pass)

FPS from Mesa's HUD counter, sampled each second; median and range over the last 15 s. Software
GL under Wine, so only relative scaling means anything. **The object-count rows are noisy**: the
VM was shared with another 5.12 run (load 2.5–7.4 on 2 vCPU); the triangle rows ran at steady
load (2.5–3.2).

| Scene | FPS median (range) | 4.20r6 Linux (T3D-113) |
|---|---|---|
| 1 cube | 62 (45–101) | 295 |
| 100 cubes | 55 (38–60) | 146 |
| 500 cubes | 21 (18–27) | 53 |
| 1000 cubes | 29 (22–33) | 28 |
| 10 shapes, ~1.4k triangles | 70 (56–79) | 227 |
| 10 shapes, ~9.7k | 58 (48–70) | 131 |
| 10 shapes, ~98k | 12.6 (8.4–13.4) | 18 |
| 10 shapes, ~500k | 2.8 (2.4–3.4) | 6 |

- **The triangle axis scales as on 4.20r6:** flat to about 10k, about 5× down by 100k and about
  4.5× more by 500k; it crosses 10 FPS a little above 100k triangles. In absolute terms it is
  2–3× slower under Wine.
- **Object-count axis:** to be rerun on an idle VM; 1000 cubes still drew at about 29 FPS with no
  stall.

## For a server

- Treat about **1000 units from the camera** as the 5.12 draw horizon; scoping ghosts further
  out than that saves bandwidth with no visible change.
- To hide a player, don't ghost it (or kill the ghost); the GameObject's `visible`/`hidden`
  never reach the server.
- Keep the Camera's ghost slot free; budget 4096 ghosts per client minus 4 fixed.
- Validate `.dif` files server-side; a slightly short file fails silently on the client.
- One GameObject path serves 4.20r6 and 5.12 alike.
