# 5.12 fxSunLight, replicators and a WaterBlock correction (2026-11-25)

Lab: the real 5.12 client on Mesa llvmpipe (OpenGL 4.6) in a VM, driven by a
probe server (gserver fork) that ghosts `fxSunLight`, the three replicator
classes and a `WaterBlock` with varied fields. Behaviour only; captures and
any crash dumps stay in the lab share, never in this repo. Board rows:
T3D-045, T3D-047, T3D-048. **[lab][cap]**

## fxSunLight (T3D-047)

- **Accepted on the wire.** The client creates the `fxSunLight` ghost and
  reads its update without rejecting it. The update layout is static:
  a flag word gates the optional fields, then the light's colour, the two
  flare texture names and the animation parameters follow in a fixed order
  (same reader shape as the other scene objects, no surprises).
- **Flare texture is downloaded, nothing is drawn.** With a valid flare and
  corona texture named, the client fetches both files, but no light, no
  corona and no lens flare appear in the scene — base, disabled and a bright
  red fxSunLight all render identically to no light at all. On a `.3ds`
  shape in the same world the fixed built-in light still does all the
  shading (see `live-512-lighting-and-sky-2026-11-25.md`); the fxSunLight
  contributes nothing on top of it.
- **All-16-flags + animation keys crashes the client.** Setting every flag
  bit at once together with animation-key strings in the update makes the
  client jump to a data address and fault (access violation). A single flag,
  or flags without the animation strings, is read without crashing. So the
  crash is in the animation-key path, reached only when the gating flags and
  the key strings are both present. (Crash address withheld per repo rules.)

## Replicators (T3D-048)

- **One shared reader for all three.** `DynamicGrass`,
  `DynamicGrassReplicator` and `DynamicShapeReplicator` are all accepted and
  all read through the same update layout — a shape/datablock reference, a
  placement area and a count/seed group — so on the wire they are one class
  family, not three readers.
- **No copies placed in the test worlds.** None of the three scattered any
  instances. The probe worlds had no `TerrainBlock`, and the replicators
  place against terrain, so with no terrain there is nothing to place on.
  This matches the GameObject/terrain pattern elsewhere: scene objects that
  need terrain draw nothing until a `TerrainBlock` exists.
- **Only DynamicShapeReplicator draws its own shape.** Independently of the
  scatter, `DynamicShapeReplicator` draws the single shape named in its
  datablock, the same way a GameObject draws a shape. `DynamicGrass` and
  `DynamicGrassReplicator` draw nothing at all (no billboard, no placeholder)
  even when their grass texture is downloaded. So of the three, only the
  shape replicator has a visible fallback without terrain.

## WaterBlock correction (T3D-045)

An earlier probe reported the surface oscillation as out of step between
axes with ~4.4 s and ~8.75 s periods. That was a probe artifact (the two
sampling passes were not phase-aligned). The clean series, sampled on one
aligned pass, is a single oscillation of **±0.5 × magnitude with a 6.0 s
period**; a per-tick grid fit is running to pin the waveform shape. The
layout, `liquidType` 0–7 and the sub-1024 "draws nothing" result from
`torque/terrain-512.md` are unchanged.
