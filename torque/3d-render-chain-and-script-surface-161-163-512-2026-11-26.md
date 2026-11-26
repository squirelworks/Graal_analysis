# Render transform chain and the weapon3d script surface (T3D-161, T3D-163)

Date: 2026-11-26. Lab: one instrumented real 5.12 session (G3D14097) in a Windows
10 VM, loopback, against seihai-gserver main (8800c2b). World: spawn `0 0 1`,
`camera 0 -6 3 1 0 0 -0.3`, a ConfCube at `0 4 1`, a ConfTexCube at `3 6 1`
turned 0.7854 rad about z. Two probe weapon3ds (`probe_reach163`, `probe_reach163b`)
enumerated every reachable handle and read the pose members; a screenshot confirmed
the camera tilt. Behaviour only; captures stay in the lab kit. **[lab][cap]**

These two rows finish the replica-renderer and replica-script-host picture: T3D-161
is the transform/pose chain a replica renderer must reproduce; T3D-163 is the script
surface a replica must present so existing weapon3d code runs unchanged. Builds on
[the typed GS2 3D surface](gs2-3d-typed-surface-512-2026-11-26.md) (T3D-096/150, the
static member table) and [the coordinate note](#) T3D-137, which this confirms live.

## T3D-163 — what a weapon3d can reach

A 5.12 weapon3d sees an almost-empty scene graph. It reaches **only two objects**:

- **`player`** — not the GameConnection. Its `objecttype()` is **GameObject**, its
  name is the literal **`ServerConnection`**, and `account`/`nick` are the account.
  `player.getcount()` is **0** — it is not a walkable group. `player.camera` resolves
  to the camera object.
- **`player.camera`** — a Camera named **`G3DCamera_<acct>`**.

Everything else is empty or absent:
- `players.size()`, `allplayers.size()`, `npcs.size()` are all **0**; `weapons.size()`
  is 3 (the loaded weapons).
- `MissionGroup` exists as an object but `MissionGroup.getcount()`/`.getobject()` are
  "Function … not found" — it cannot be walked.
- `ServerConnection` (as a global) exists, `getcount()` 0. `RootGroup` is **null**.
  `findobject` is **not available** (T3D-126).

**So a weapon3d has no *enumeration* of world objects, other players, or ghosts — no
group walk, no array, no `findobject`.** The rendered world objects (the two cubes)
are drawn from the server ghost set but cannot be discovered from script. This
confirms the static root of T3D-016: a client script cannot walk or manipulate the
ghosted scene. (One refinement, from the two-client run below: a **known-name handle
to another *player's* object does resolve** via `makevar`, so the barrier is
discovery/enumeration, not an absolute handle ban — but there is still no way to reach
non-player world objects.)

Member lists recorded (for a replica script host to reproduce):
- **`player.getvarnames()` — 55:** account, alpha, attachedtoobject, attr,
  attrobjects, camera, chat, client, clientr, collision, communityname,
  eulerrotation, forwardvector, initialized, iseditorobject, isobserver, ispaused,
  joinedclasses, liquidheight, liquidtype, maxlooplimit, movetype, name, nick,
  nickcolor, nickname, objectbox, pixelshader, position, renderposition, rightvector,
  rotation, scale, scaledobjectbox, scaledshapebox, scripterrors,
  scriptlogmissingfunctions, shadow, shape, shapebox, showterrain, skin, solid,
  timeout, transform, upvector, velocity, vertexshader, watercoverage, worldbox,
  worldboxcenter, x, y, z. `getdynamicvarnames()`: client, clientr.
- **`camera.getvarnames()` — 52:** the same core minus
  account/camera/communityname/isobserver/pixelshader/vertexshader, plus
  **cameramode, followattachedobject, lookatposition, lookvector**.

## T3D-161 — the pose/transform chain

**Value formats** (all comma lists, read from the own object and the camera):
- `transform` = `"x,y,z,axisx,axisy,axisz,angle"` — the angle is in **degrees**.
- `rotation` = `"axisx,axisy,axisz,angle"` (angle in degrees).
- `eulerrotation` = `"x,y,z"`.

**Own object** at spawn `0 0 1`: `position` `"0,0,1"`, `renderposition` `"0,0,1"`,
`transform` `"0,0,1,1,0,0,0"` (identity rotation), `eulerrotation` `"0,0,0"`,
`forwardvector` `"0,1,0"` (**faces +y**), `worldbox`
`"-0.5,-0.5,0.5,0.5,0.5,1.5"` — the 1 m playershape cube around `0,0,1`.

**Camera** from the world line `camera 0 -6 3 1 0 0 -0.3`:
- `position`/`renderposition` `"0,-6,4"` = spawn `(0,0,1)` + the world offset
  `(0,-6,3)`. **The camera offset in the world line is relative to the spawn / own
  object**, not absolute.
- `rotation` `"-1,0,0,17.188731121"`: the line's `1 0 0 -0.3` rad is shown with the
  **axis flipped and the angle positive** (0.3 rad = 17.19°).
- `forwardvector` `"0,0.955336511,0.295520216"` — **the view looks UP 17.2°**,
  confirmed by the screenshot (mostly sky, the cubes near the bottom edge).
  `lookvector` `"0,0,-1"`, `lookatposition` `"0,0,0"`, `cameramode` `"free"`,
  `eulerrotation` `"0,0,0"`.

**Sign of the camera pitch:** on 5.12 a **negative** angle about **+x** in the camera
line tilts the view **UP** (an earlier lab's `+1.5708` looked straight down). So
`GRAAL3D.md`'s example `camera 0 -8 3 1 0 0 -0.3` reads like a *downward* tilt but
actually tilts up — that doc example should be corrected (tracked for the server
repo that owns GRAAL3D.md).

The ConfTexCube's 45° z-turn drew as sent, but **no script value could be read for
it** — world objects are unreachable (T3D-163).

## Cross-player read and draw — two 5.12 clients (T3D-066 on-screen half)

A second run (two real 5.12, run R8e) settled what one 5.12 draws and reads for
*another* player. pc:1's weapon3d set `player.chat="hello from pc1"` and
`player.nick="NickOne"`; each client printed both players' `.nickname` and `.chat`.

- **Drawn by default:** only the other player's **shape** (the world playershape).
  5.12 draws **no nick and no chat label** over another player's GameObject — a world
  script (or a replica) must draw those itself.
- **Readable by script — chat yes, via a known name.** pc:2 read pc:1's object as
  `nick=[pc:1] chat=[hello from pc1]`, and pc:1 read its own the same. The handle is
  `makevar("G3DPlayer_pc:1")` — a **direct** `G3DPlayer_pc:1.chat` does **not compile**
  ("expected `)`") because guest accounts are named `pc:N` with a colon; `makevar` of
  the name string works around it. `findobject()` still returned 0, so this is a
  name-built handle, not enumeration.
- **A 3D-set nick never propagates.** After `player.nick="NickOne"`, both clients
  still read `"pc:1"` (the account name) — and the 2D view (2.22) also kept `"pc:1"`.
  So a 3D script's nick change is not carried to other clients; chat is.
- **showtext y-clip gotcha:** showtext near the top of the 3D view (y ≈ 20–70) is not
  drawn; at y ≈ 300+ it draws. A HUD/overlay must stay clear of the top band.

So for a replica or a world script: the other player's shape is drawn, and its chat is
readable by `makevar`'d name, but nick/chat are **not** auto-drawn and a 3D-set nick
does **not** sync — draw labels yourself and don't rely on 3D `player.nick` writes.

## For a replica

- **Renderer (T3D-161):** camera pose = spawn + the world camera offset; rotation is
  axis+angle with the angle in **degrees** and the sign convention above (negative
  angle about +x = look up); own-object forward is +y; the playershape worldbox is a
  1 m cube at the object position. Reproduce the degrees/axis-flip exactly so a world
  authored for 5.12 frames the same way.
- **Script host (T3D-163):** present `player` as a **GameObject** named
  `ServerConnection` (not a GameConnection), expose `player.camera` as
  `G3DCamera_<acct>`, and leave `players`/`allplayers`/`npcs`/`RootGroup`/`findobject`
  empty/absent. A weapon3d that tries to reach world objects or other players must get
  nothing back, exactly as on 5.12 — the script surface is deliberately narrow.

## Summary

| row | verdict |
| --- | --- |
| T3D-161 | pose formats: transform `x,y,z,ax,ay,az,deg`, rotation `ax,ay,az,deg`, euler `x,y,z`; camera = spawn + world camera offset; `camera … 1 0 0 -0.3` → rotation `-1,0,0,+17.19` with forward `(0,0.955,0.296)` = view tilts UP for a negative angle about +x; own forward +y; worldbox = playershape box at spawn; world-object poses not script-readable; GRAAL3D.md tilt example should be corrected |
| T3D-163 | a weapon3d reaches only `player` (GameObject named ServerConnection, getcount 0) and `player.camera` (Camera G3DCamera_<acct>); players/allplayers/npcs empty, weapons 3; MissionGroup/ServerConnection exist but aren't walkable; RootGroup null; no findobject — no handle on world objects or other players; member lists recorded (player 55, camera 52) |
