# Graal3D collision (February 2000 client)

Date: 2026-10-31

Per-face movement test in `Graal3D.exe` (resource stamp 2000-02-05), recovered by static float and control-flow reading of the PE only. No decompile text, no binary addresses. Units are Direct3D Retained Mode world units. Tags: **[bin]** unless marked **[inf]**.

Walking, running and the world clamp that feed this test are in [client-behaviour.md](client-behaviour.md). A Wine lab cannot exercise this path without Microsoft's `d3drm.dll` (Wine's `GetFaces` is a stub; see [lab-2026-10-30.md](lab-2026-10-30.md)).

## What the Collider needs

| Quantity | Value | Tag |
|---|---|---|
| Horizontal body half-extent (radius) | **5** | [bin] |
| Upper-body probe height | **+35** above the feet position | [bin] |
| Upper-body lateral probe half-span | **10** (probes at 0, +10, −10 on the strafe axis only) | [bin] |
| Max step height (onto a walkable face) | **30** | [bin] |
| Walkable face normal | upward component **> 0** | [bin] |
| Feet-mesh attach slope | upward normal **> 0.2** (about 78.5° from horizontal); steeper walkable faces still snap the point but skip the mesh attach | [bin] |
| Wall “already clear” distance | current signed distance **≥ 3** → no wall hit | [bin] |
| Wall “started inside” distance | previous signed distance **< −5** → no wall hit | [bin] |
| World clamp (x and z) | **±4000**; a step that would leave is dropped | [bin] |

Sliding: on a hit the client projects the test point onto the face plane along the face normal (subtract `dist × normal` from the point). **[bin]**

## Order of tests (one attempted step)

1. Build the candidate position from the walk/run/jump delta (see [client-behaviour.md](client-behaviour.md)).
2. Load every face of the level mesh (the face list filled at level load).
3. Transform face vertices into world space.
4. Run the **body probes** below against every face.
5. Reject the step if a probe reports blocked; otherwise keep the (possibly slid) position.
6. Drop the step if the resulting x or z is outside ±4000.

## Body probes

From the candidate feet position the client tests these points, in order. A probe that returns blocked stops the rest for that step.

**Ground / step probes** (flag “floor”): four points in the horizontal plane of the feet, offset by **±5** along the facing axis and by **±5** along the strafe axis (a plus shape, not a filled disc). **[bin]**

**Upper probes** (flag “wall only”): raise Y by **35**, then test at lateral offsets **0**, **+10** and **−10** on the strafe axis only. These probes do not run the floor/step path; they only participate in the wall/ceiling path. **[bin]**

## Per-face test

For each face the client has the face vertices and a face normal.

### Over-face test

Before using a face as a floor or wall, the probe’s **(x, z)** must lie inside the face’s horizontal polygon: a winding / cross-product test on the projected edges (both edge orders are tried). If the point is outside, the face is skipped. **[bin]**

### Walkable faces (normal Y > 0)

Only the ground probes use this path.

1. Signed distance of the probe to the face plane: `dot(probe − vertex0, normal)`.
2. If distance **> 30**: treat as landing on this face (place the player on the plane, set the landed / not-jumping flags). Used when the feet are far above the face (for example after a jump). **[bin]**
3. If distance **< −30**: fail this face (step too high; the ledge is more than 30 below the feet along the normal). **[bin]**
4. Otherwise (−30 ≤ dist ≤ 30): **slide** the probe onto the plane. If normal Y **> 0.2**, also attach / orient the player mesh to the face; if 0 < normal Y ≤ 0.2 the point still slides but the mesh attach is skipped. **[bin]**

So the **step height is 30**: a walkable ledge up to 30 units above the feet can be stepped onto; taller ledges are blocked. **[bin]**

### Walls and ceilings (normal Y ≤ 0)

Used by ground and upper probes.

1. Signed distance of the **new** probe position to the plane, and of the **previous** position.
2. Drop the face if the new distance is **≥ 3** (still clear of the wall). **[bin]**
3. Drop the face if the previous distance is **< −5** (started already deep inside). **[bin]**
4. Drop the face if the move vector’s length squared is **≤ 0**. **[bin]**
5. Otherwise **slide** the new point onto the plane (same projection as above). **[bin]**

## What this does not settle

- Exact player capsule vs the plus-shaped probe set (a disc of radius 5 would be an approximation, not what the binary runs). **[inf]** if a reimplementation substitutes a disc.
- Floor friction, ground stickiness beyond the slide-to-plane rule, or separate ceiling thickness. Nothing else showed up in the float set of this routine. **[bin]** for absence in this path.
- Live confirmation under Wine still needs native `d3drm.dll`. **[inf]** until a lab run.
