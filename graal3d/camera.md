# Graal3D camera (February 2000 client)

Date: 2026-10-31

Follow-camera behaviour in `Graal3D.exe` (resource stamp 2000-02-05), from a static PE float and control-flow read. No decompile text, no binary addresses. Units are Direct3D Retained Mode world units; one frame tick is the 50 ms `TDXTimer`. Tags: **[bin]** unless marked **[doc]** or **[inf]**.

Related: walking controls and the short camera summary in [client-behaviour.md](client-behaviour.md). Collision is separate ([collision.md](collision.md)).

## Status for G3D-2

| Need | Value | Tag |
|---|---|---|
| Follow distance | **220** behind the player | [bin] |
| Camera height / look height | follow target **80** above the player on Y | [bin] |
| Field of view | library field **0.5**; opening **2×atan(0.5)** ≈ **53.13°** on either axis of that square window | [doc] for 0.5; [inf] for the degrees; [bin] that the exe does not set it |
| Follow rule | see below | [bin] |

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

The main `DXDraw` surface in the form resource is **640×456**. That is the pixel target. The field below stays a square window at any pixel size. **[bin]**

## Field of view

The February 2000 exe leaves the field at the library initial value. The static PE read behind this note found no FOV constant and no `SetPerspective` call. **[bin]** The binary is not in the repo and was not opened again for this section.

Immediately after Direct3DRM creates a viewport, and before any `SetField`, the library state is:

| Quantity | Value | Tag |
|---|---|---|
| Field (`SetField` / `GetField`) | **0.5** | [doc] |
| Window on the front clipping plane | left **−0.5**, right **0.5**, bottom **−0.5**, top **0.5** | [doc] |
| Front clipping plane | **1** | [doc] |
| Projection | perspective | [doc] |
| Opening of that window, along either axis | **2×atan(0.5 / 1)** ≈ **53.13°** | [inf] |

**0.5 is the library field parameter.** Degrees in the last row are arithmetic on that window: `SetField` builds a centered square on the front clipping plane, half the window is 0.5, and the front plane sits at distance 1, so each axis opens by `2×atan(0.5)`. X and Y use that same angle. A modern camera that takes a 53.13° vertical angle and then widens X to the 640×456 pixel ratio is a different window; this note does not give that widened angle. The retained-mode viewport uses one scale on X and Y, taken from the longer pixel side (same conformance test). That scale was not turned into a second degree figure.

Two public texts agree on the field value. The DirectX SDK retained-mode viewport reference says the initial field is 0.5 (`SetField` remarks) and the initial front plane is 1 (`SetFront` remarks). `SetPlane` is an arbitrary window on that front plane, and `SetField` is the centered form of the same window. Wine’s `d3drm` conformance test (`dlls/d3drm/tests/d3drm.c`, `test_Viewport`) expects the same state right after init: field 0.5, plane ±0.5 on all four sides, front 1, back 100, projection perspective. That test builds the viewport from a 640×480 window and still records the square plane. The test is written to match Microsoft’s `d3drm`. This note did not re-run it.

The back clipping plane of this client stays open. The library default back plane is 100. **[doc]** A later public DelphiX (unDelphiX `Source/DXDraws.pas`, retained-mode init) calls `CreateViewport` and `SetBack(5000)` and does not call `SetField` or `SetPlane`. That fork starts after 2004, so it is not the unit linked in February 2000, and this client’s far plane was not re-read. The same init leaves the field alone. A field override compiled into `Graal3D.exe` would have been a float constant; the PE read found none.

## Still needed

- ~~FOV from a library default or a lab measurement.~~ **Closed** above: field **0.5**, opening ≈ 53.13°.
- **Far plane stays open.** The library's initial back plane is 100. **[doc]** A later public DelphiX (unDelphiX `Source/DXDraws.pas`) calls `SetBack(5000)` during retained-mode init and leaves the field alone. That fork starts after 2004. The static PE read that found no field constant and no `SetPerspective` did not re-read `SetBack`. The binary is not in the repo, and no other note gives a back-plane number for the February 2000 exe. 100 and 5000 are both sourced. Neither is tagged as this client's far plane.
- Live confirmation of the 220 / 80 / 5° / −0.15 rad figures, and of this field, under Wine with native `d3drm.dll` (Wine’s RM stubs break camera frames; see [lab-2026-10-30.md](lab-2026-10-30.md)).
