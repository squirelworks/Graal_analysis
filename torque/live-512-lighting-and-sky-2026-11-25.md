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
- One visible side draws at 0.85 of that (109 against 217), and that factor
  does not change with the Sun. Its rule (which face, and why) is a
  follow-up.
- With no Sun at all (L7), every face is exactly one quarter (32, 64, 32),
  and the background is 0.

So the Sun acts as an on/off switch for full brightness on a `.3ds` shape,
not as a directional light. Whether it shades `.dts`, `.dif` or terrain is a
follow-up.

## Shape rotation

The client turns a shape by the right-hand rule: a positive angle is
counter-clockwise about +z. That is the opposite sense to the camera's turn
rule.

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
