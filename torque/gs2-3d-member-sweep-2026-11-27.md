# Every typed GS2 3D member on a live client: 5.12 and 4.20r8 (T3D-150)

Date: 2026-11-27. Lab, seihai-gserver 833faba, single client per build, in headless
lab VMs on GwenTea2. Board row: [T3D-150](3d-capability-board.tsv). **[lab]**

The 5.12 typed surface ([T3D-096](gs2-3d-typed-surface-512-2026-11-26.md): 35 classes,
418 members) was turned into seven generated `weapon3d` probes, conformance cases
C049 to C055 ([`tools/conformance/gen_sweep.py`](../tools/conformance/gen_sweep.py)).
On an instance of each class, every property is read, written with a value of its type
and read back (numeric and bool ones also get the word `zz`, which a registered property
coerces and an unregistered name keeps), and every function is called once with
arguments of its declared types. The 13 global 3D functions are called too. The
per-member values and verdicts are in
[`conformance/sweep/results.tsv`](conformance/sweep/results.tsv), the counts in
[`conformance/sweep/RESULTS.md`](conformance/sweep/RESULTS.md).

## Counts

| Build | works | read-only | ran (void) | inert | absent | no instance | skipped (crash) | not run |
|---|---|---|---|---|---|---|---|---|
| 5.12 Windows (C049 to C055) | 228 | 5 | 43 | 68 | 3 | 35 | 49 | 0 |
| 4.20r8 Windows (C049 to C053) | 213 | 5 | 41 | 67 | 3 | 35 | 0 | 67 |

All 12 runs PASS (probe compiled, ran to `done`, client alive). 4.20r8 gives the same
verdict as 5.12 on every member both reached; the only class-level difference is
`GuiInputCtrl`, which 5.12 can create and 4.20r8 cannot.

## What it shows

- **Two crashers, both instance creation on 5.12.** Getting a `TGameObjectAttr`
  (`new TGameObjectAttr` / `attrobjects[0]`) and creating a `TerrainEditor` from a
  weapon end the client. (T3D-126 created a TerrainEditor in a different order without a
  crash; here it dies right after the first GameObjects are made.) Both are now in the
  sweep's skip list; with them skipped every other class runs.
- **No instance for 35 members.** The shape, animation-thread, material and movement
  classes (`GameShape*`, `DTSAniThread`, `TShapeMaterial`, `GameMovement*`,
  `TMovementRigid`) are not script-creatable and `shapeobject` / `movement` /
  `playAnimation` never hand one back, so their members stay untested. `new Camera`
  gives nothing; `ServerConnection.camera` does. `new GuiGraal3DCtrl` gives nothing.
- **Registered but inert.** E.g. `GameObject.velocity` (the write does not stick),
  `Camera.cameramode` (stays `free`), `fxSunLight.minsize`, `lerprotation`.
- **Absent on both builds.** `WaterBlock.submergeTexture0`, `submergeTexture1` and
  `GuiShapeNameHud.chatprofile` read and write as empty.
- **Value formats.** A four-component colour write (`Sky.skysolidcolor`,
  `GuiShapeNameHud.fillColor`) reads back with three (alpha dropped); `rotation` is
  normalised (axis, then angle); a float property given `zz` reads back -1, not 0;
  `GameConnection` (`ServerConnection`) reports its object type as `GameObject`;
  `unmountObject` returns 1 with nothing mounted; `Terraformer.saveGreyscale` returns 1.
- **Globals** run without error; with no terrain `castRay`, `getz` and
  `get3Dobjectsbyradius` give 0, `getTerrainTextureIndex` -1, `get3Dobjectsbybox` and
  `getTerrainTexture` empty.

## Limits of the verdicts

- A bool property whose default is already 1 and is written `true` counts as inert.
- A global returning `0` counts as works; read the value column, not only the verdict.
- 4.20r8 needs the client delivered on its own CD (it is not in the Windows base image)
  and Mesa forced to llvmpipe; on the D3D12 driver it drops its link at connect.

## Not done (left as exercises)

- 4.20r8: C054 (TerrainEditor) and C055 (TerrainBlock, Terraformer, globals).
- 6.037F (our Frankenstein 6.037): all seven cases (`[expect."6.037F"]` is in each).
- 4.04r2 (native Linux runs only, outside `run.py`) and 3.153 (Mac PPC, Mirae's Tiger VM):
  the runner has no backend for them yet.
- The 35 no-instance members need a way to reach a `GameShape`/`DTSAniThread`/movement
  object first (a server-ghosted object with a `.dts`, or another accessor).
