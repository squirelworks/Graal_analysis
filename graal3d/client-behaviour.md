# Graal3D client behaviour

Date: 2026-10-30

How the February 2000 `Graal3D.exe` moves the player, drives the camera and shows chat, read from the binary for a per-version client profile. **[bin]** unless tagged. Units are Direct3D RM world units; one frame tick is the 50 ms `TDXTimer`.

## Controls

| Key | Action |
|---|---|
| Numpad 8 / 2 | Forward / back, relative to the camera's view direction |
| Numpad 4 / 6 | Step left / right (strafe), at right angles to the view direction |
| Numpad 5 | Jump |
| Numpad 0 | Toggles the camera mode flag (follow camera on or off) |
| Enter | Sends the chat line |
| Ctrl+Enter | Fullscreen on or off |
| F1 / F2 | Hardware options / Player look |
| Esc | Quit |

Movement keys are read with `GetAsyncKeyState`, and only while the chat line does not have focus and the window is active.

## Walking and running

- Walking speed is **8 units per tick** (160 per second).
- After **25 ticks** (1.25 s) of walking without stopping, speed becomes ×1.5 (12 per tick, 240 per second). Stopping resets the count.
- Holding only "back" walks backwards along the direction the player faced when the key went down, instead of following the camera.
- The world is ±4000 units on x and z. A step that would leave it is dropped. This matches the wire range of props 1–3 (`(v − 8000) / 2`, so −4000 to 4095.5 in half-unit steps).
- Collision tests the new position against every face of the level mesh (the faces are loaded with the level). Numbers for a `Collider` (radius 5, step height 30, slope and wall rules, probe order) are in [collision.md](collision.md).
- While walking, the body bobs: y gets `|sin(3.14 × 2 × (anim − 1) / 40)| × 3` added (the program uses 3.14, not π).

## Animation counter (prop 5)

Prop 5 is a tick counter for the walk and jump poses, not a pose id.

- Starting to walk sets it to 0 or 20 at random, so two players do not step in time.
- A jump sets it to 40.
- Where the counter is advanced each tick was not traced; that standing still freezes it is **[inf]**.

## Jumping

- The jump is a fixed table of upward speeds per tick: **10, 10, 9, 8, 6, 3, 1** (47 units up in 7 ticks).
- At the top, the same table is walked back down with negative speeds (−1, −3, −6, −8, −9, −10), and then −10 per tick until the player lands.
- **Letting go of the key early** cuts the climb: the fall starts at once from the top of the table, so a tap gives a short hop.
- A new jump needs the key released and pressed again.

## Camera

Full write-up: [camera.md](camera.md).

- A follow camera stays about **220 units** behind the player. It closes the gap by a factor of `((d − 220) / 220)² / 10` per tick, with the sign of `d − 220`.
- The Y follow target is **80** above the player (`(player_y + 80 − camera_y) / 10` per tick).
- It turns towards the player by up to **5 degrees per tick**, more when the player is behind it, then pitches **−0.15 rad**.
- Field of view is the Direct3DRM initial field **0.5** (square window, opening about 53.13° on either axis). This exe does not set it. See [camera.md](camera.md). **[doc][bin]**
- The player's facing (prop 4) is the angle of the camera-to-player direction, in degrees, sent as `degrees / 2`.

## Chat

There are **no chat bubbles** in Graal3D.

- A chat line (prop 13, or a UDP chat datagram) is added to a **chat log** as `nickname: text`.
- The log is drawn at the bottom left of the 3D view: x = 5, newest line at y ≈ 451, older lines above it.
- The font is "Dialog", 14 px, white.
- Each line stays for **10 seconds** (200 ticks at the default 50 ms timer) and is then removed.
- Your own chat goes to UDP peers right away and to the server in the next props diff. A line longer than 200 characters is cut and ends in `...`.

## Look

- The player is eight meshes: body, head, two arms, two hands, two feet.
- Props 6–9 name the body and head meshes and textures; props 10, 11 and 17 colour the arms, feet and hands.
- The defaults are in [formats.md](formats.md).
- The "Player look" window edits them, and they are saved in `graal3dconfig.txt`.
