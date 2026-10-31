# Graal3D camera (February 2000 client)

Date: 2026-10-31

Follow-camera behaviour in `Graal3D.exe` (resource stamp 2000-02-05), from a static PE float and control-flow read. No decompile text, no binary addresses. Units are Direct3D Retained Mode world units; one frame tick is the 50 ms `TDXTimer`. Tags: **[bin]** unless marked **[inf]**.

Related: walking controls and the short camera summary in [client-behaviour.md](client-behaviour.md). Collision is separate ([collision.md](collision.md) on the collision branch / once merged).

## Status for G3D-2

| Need | Value | Tag |
|---|---|---|
| Follow distance | **220** behind the player | [bin] |
| Camera height / look height | follow target **80** above the player on Y | [bin] |
| Field of view | **not pinned** — no FOV constant or `SetPerspective` call in this client binary; likely the DelphiX / Direct3DRM library default | [inf] |
| Follow rule | see below | [bin] |

Task 6 is **not done** until FOV is tagged from a library-default proof or a lab measurement (native `d3drm.dll` under Wine). Do not invent a degree number.

## Follow rule (Numpad 0 toggles follow on/off)

When the follow flag is on, each tick:

1. Measure the horizontal distance `d` from the camera frame to the player.
2. Close the gap by factor `((d − 220) / 220)² / 10`, with the sign of `d − 220` (move toward the 220-unit target). Skip the move if the factor is 0 or ≥ 100. **[bin]**
3. On Y, move by `(player_y + 80 − camera_y) / 10` (target **80** above the player). **[bin]**
4. Turn the camera toward the player by up to **±5 degrees** per tick (more when the player is behind the camera). **[bin]**
5. Aim at the player (`LookAt`), then pitch by **−0.15 radians** (~−8.6°) about the camera’s local X axis. **[bin]**

When follow is off, the follow translation path is skipped (the camera is left where it is for that step). **[bin]**

The player’s facing (prop 4) is the angle of the camera-to-player direction, in degrees, sent as `degrees / 2`. **[bin]**

## Display size (aspect context only)

The main `DXDraw` surface in the form resource is **640×456**. That is the draw surface size, not a FOV. **[bin]**

## Still needed

- **FOV** in degrees or radians, from the DelphiX retained-mode default used by this build, or from a lab capture with a known calibration object. **[inf]**
- Live confirmation of the 220 / 80 / 5° / −0.15 rad figures under Wine with native `d3drm.dll` (Wine’s RM stubs break camera frames; see [lab-2026-10-30.md](lab-2026-10-30.md)).
