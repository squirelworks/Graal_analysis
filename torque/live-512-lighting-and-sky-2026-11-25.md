# 5.12 lighting and sky geometry on a GLSL driver (2026-11-25)

Lab: the real 5.12 client on Mesa llvmpipe (OpenGL 4.6) in a VM, with a
lighting probe (`.3ds` cubes and a Sun at several directions, colours and
ambient levels) and a sky grid. Behaviour only; captures stay in the lab
share. Board rows: T3D-046, T3D-047, T3D-052, T3D-055. **[lab][cap]**

## Lighting on `.3ds` shapes (T3D-047, T3D-052)

Runs L1 to L6 put the Sun down, to the side and diagonal, with different
colours and ambient. The cubes were pixel-identical across all of them, so
on a `.3ds` shape the Sun's direction, colour and ambient have no effect.

- With a Sun present, each face draws at exactly material x texture (grey
  128 draws 128, white 255 draws 255, a mid texture 128).
- The 0.85 factor is set by the face's **world-space normal**, not the model
  face and not the camera: faces pointing -y, -x or up draw at 1.0; faces
  pointing +x or +y draw at 0.85. No in-between levels appear. This is
  consistent with a fixed built-in light from about (-x, -y, +z) with 0.85
  as the floor, not the Sun object.
- With no Sun at all (L7), every `.3ds` face is exactly one quarter (32, 64,
  32), and the background is 0.

So the Sun acts as an on/off switch for full brightness on a `.3ds` shape,
not as a directional light.

**Other content (follow-up 11).** The Sun's direction and colour shade
nothing on a `.dts` (MBG `superJump.dts`), a `.dif` (MBG `training1.dif`) or
streamed terrain: a side-lit run and a top-lit run were pixel-identical.
With no Sun at all, the `.dts` is not drawn or is black, the `.dif` is
entirely black (it shows no lightmap shading), and terrain is unchanged.
Native terrain: the client downloaded `heights.info` and the chunks, logged
"Terrain lit", never requested the (`.png`-named) terrain textures, and drew
the ground white; it also requested `lightfalloffmono`.

## Shape rotation

The client turns a shape by a positive angle about +z as **clockwise seen
from above** (at +90 degrees the +x face looks toward -y), the same sense as
the camera. (An earlier note here said the opposite; this run corrects it.)

## Sky geometry and field of view (T3D-046, T3D-055)

Sky grid run S1 confirms and extends the earlier face order:

- Entry 2 is ahead (+y), 1 is right, 0 is behind, 3 is left, 4 is up.
- The side faces are mirrored left to right and are upright.
- The up face's top-left corner lands bottom-left when looking up from +y.
- One sky face spans the full screen width.
- Markers at -30, 0 and +30 degrees give a horizontal field of view of
  89.4 degrees, so the default is 90.
- Below the horizon is the fog colour (Mesa), matching the earlier
  correction.
