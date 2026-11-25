# 5.12 `.dif` interiors: draw and collision (2026-11-25)

Lab: the real 5.12 client under Wine on Mesa llvmpipe, against our own
Seihai gserver on loopback (never a third-party server). Question
(T3D-030 / T3D-087): does a `.dif` interior **draw**, and does the 3D player
**collide** with it? Behaviour only; captures stay in the lab kit.
**[lab][cap]**

Interior used: a v44 `.dif` from the lab kit — a blue-grid U-track with
white edge trim, textures `grid_cool2.jpg` + `edge_white.jpg`.

## Draw — yes

The interior renders: the blue grid floor with white edge trim draws
correctly. Console, in order: the `.dif` downloaded, each texture resolved
(`grid_cool2`, `edge_white`), then **"Room lit in 0.000 seconds"**. No
version error and no crash.

**Version gate: v44 only.** v44 is accepted silently; the earlier lab had
v43 and v45 both rejected with `InteriorResource::read: incompatible file
version found`. (This matches the static DIF version check in
`torque/3d-engine-static-reads-2026-11-25.md`.)

The client also requests a handful of stock interior lightmaps / default
textures (`null`, `whitealpha255`, `whitenoalpha`, `lightfalloffmono`); the
server has none, each returns "not found", and the draw is unaffected.

## Collision — none on the server-positioned player

In the way 5.12 actually runs against our gserver, the 3D player is a
**server-positioned marker**: its position is server-authoritative, it does
not self-move, and it has no gravity.

- Holding forward (W / Up) moved the player on neither the Wine nor the
  Windows client — the trace shows the client sent only its initial state,
  no movement input.
- A player spawned above the track did **not** fall: no gravity, no floor
  support.

So the player was driven by server step and its position logged every 0.5 s:

- **Horizontal sweep** (x −60 → +60, just above the floor): the position
  reads the commanded value at every step — a straight line across the floor
  and *through* the raised edge walls. No deflection, no stop.
- **Drop test** (z 3 → −12): the player goes straight down through the floor
  and stays at −12, never stopped or lifted.

The interior applies **no collision** to the player: it passes through walls
and floor, with no floor support and no gravity. This is consistent with
everything else seen about the 5.12 3D player — it is a server-driven ghost,
not a client-physics body. As the client actually runs, a `.dif` interior is
**visual geometry only**; the server owns position, and interior collision
is not applied client-side in this mode.

## Portals / zones — not meaningfully testable here

The track is open (no enclosed doorway), and the camera is a fixed world
camera, not carried by the player. Moving the server-positioned player
through the geometry triggers no zone or portal transition, and from outside
the whole interior draws with no zone-culling gaps. A real portal/zone test
would need an **enclosed** interior and a **first-person, player-carried**
camera — a mode this server-positioned-player setup does not provide — so
this is left open.

## Conclusion

- **Draw:** `.dif` interiors draw on 5.12, textures and all, with a strict
  **v44-only** version gate (v43/v45 rejected). No crash on a well-formed
  file — consistent with the fuzz finding that `.dif` is the most robust of
  the content formats.
- **Collision:** the server-positioned 5.12 player does **not** collide with
  interior geometry and has no gravity; position is purely server-authoritative.
  So interiors are drawn but not collided against in the client's normal mode.
- **Portals/zones:** open — needs an enclosed interior and a player-carried
  camera to exercise, which this mode doesn't expose.
