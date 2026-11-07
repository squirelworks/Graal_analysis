# The Torque engine in Graal: version, classes, 3D formats, rendering

Date: 2026-10-30. Tags as in `README.md`.

## Which Torque

- **3.04 Linux** says so itself: `getVersionNumber()` returns 1100, `getVersionString()` formats 1.1 as `"1.100"`, `getCompileTimeString()` is `"Jan  3 2004 at 22:32:08"`, the connect game string is TGE's default `"Torque Game Engine Demo"`, the home folder is `~/.garagegames/` (3.151 changed it to `~/.graal`), and source paths are TGE's (`game/gameConnection.cc`, `editor/missionAreaEditor.cc`). So 3.x is built on a TGE 1.1–1.2 era code base. **[bin]**
- **3.153 Mac** is the same engine for PowerPC/Carbon ("MacOS Torque Game Engine"), plus `AdvancedCamera`, `fxFoliageReplicator`, `twSurfaceReference`, `volumeLight` (community TGE resources of the time), a `Shape3ds` loader for 3D Studio models and an `Md3.cc` loader for Quake 3 player models (`_head.md3`, `_upper.md3`, `_lower.md3`). **[bin]**
- **4.04r2** `Graal3DEngine.dll` (built from `K:\src\graalv4\user\engine\…`) is still near-stock TGE: `Player`, `AIPlayer`, `Item`, `Projectile`, `Explosion`, `Debris`, `Splash`, `Precipitation`, `Lightning`, wheeled/flying/hover vehicles, `PathCamera`, `Trigger`, `PhysicalZone`, `InteriorInstance`, `TSStatic`, the `fx*` replicators and `fxLight`, `DecalManager`, and every matching `…Data` datablock. It imports 623 symbols from the 2D `GraalEngine.dll`. **[bin]**
- **5.12** `Graal3DEngine.dll` (Oct 2007) is one engine for 2D and 3D. It keeps Torque's core (console, `SimObject`/`SimSet`/`SimGroup`, `NetConnection`/`GameConnection`, ghosting, `SceneObject`, `TerrainBlock`, interiors, `TSShape` DTS, `Sky`, `Sun`, `WaterBlock`, `fxSunLight`, the world and terrain editors) but **drops the TGE game layer**: no datablocks, no `GameBase`/`ShapeBase`/`Player`/vehicles/projectiles/items, no `ScriptObject`, no audio emitters. Graal's own classes take their place (below). **[bin]**
- **4.20r6 Mac** (Sep 2006) already has the 5.12 model: `GameObject` and Graal's replicators, no datablocks, protocol 21. So the TGE game layer was dropped between 4.04r2 and 4.20r6. **[bin]** (`wire-by-build.md`)
- **5.24r3 onward** has no Torque 3D left (no `GameConnection`, `TerrainBlock`, `Interior` or DTS code); only the class name `GuiGraal3DCtrl` survives. **[bin]**

## The 5.12 3D object model

All script-visible through GS2 property and method tables. **[bin]**

| Class | What it is | Notable members (strings) |
|---|---|---|
| `GameObject` (a ghosted `SceneObject`) | every 3D thing in the world | `mountObject`, `unmountObject`, `getMountedObject…`, `getNodePosition/Transform`, `getInteriorObject`, `isInInterior`, `getdropz`, `checkCollisionByBox`, `clipPolygons`, `getControllingClient`, `findimg`/`hideimg` (Graal show-images on 3D objects), `onMount`, `onUnmount`, `onAdd`, `onRemove`; `TGameObjectVar` / `TGameObjectAttr` sync script variables to clients ("failed to send TGameObjectVar … object not ghosted yet") |
| `GameShapeDTS` | Torque DTS model | `playAnimation(slot, name, flags)` with flags 1 hold, 2 at end, 4 attack animation; `playAnimation2(slot, name, flags, startpos, endpos, timescale, transitiontime)`; `pauseAnimation`, `stopAnimation`, `forceAnimations`, `listNodes`, `materials`/`materiallist`; `DTSAniThread` objects; mount points and `collision-`/`los-` detail names; `onEndAnimation` |
| `GameShapeDIF` | Torque interior | `activateLight`, `deactivateLight` |
| `GameShape3DS` | 3D Studio model | collision hulls are meshes named `Col-…` (must be closed and convex); colours `3dscolorRGB` |
| `GameShapeFT` | 3D text from a TrueType font | FTGL-style vectoriser and tesselator |
| `GameShape` (base) | | `pixelshader`, `vertexshader` (GLSL through `glCreateShaderObjectARB`), fractal-tree fields (`gramma`, `branch`, `leaf`, `billboard`, `texBranch`, `texLeaf`) |
| `GameMovementInterpolate` / `…List` / `…Rigid` | how an object moves | `move3d`, `finishMoves`, `addRigidMove`, `applyImpulse`, `TMovementRigid.mass`, rigid-body events `onImpact`, `onCollision`, `onEnterLiquid`, `onLeaveLiquid` |
| `Camera` | the view | `cameramode` (`free`, `lookat`), `followattachedobject`, `lookatposition`, `lookvector`, `eulerrotation` |
| `DynamicGrass`, `DynamicGrassReplicator`, `DynamicShapeReplicator` | ground cover | terrain alignment, slope limits, allowed surfaces, per-grid object counts |
| `Sky`, `Sun`, `WaterBlock`, `fxSunLight`, `TerrainBlock` | stock Torque | three cloud layers, fog volumes, fog storms with server-synchronised time |

The 2D Graal player is still the player; 3D objects can carry ganis and show-images (`.gani`, `e:emoticon`).

## 3D resource formats

| Ext | Format | Where |
|---|---|---|
| `.dts` / `.dsq` | Torque shape / sequence (`TSShape`). 5.12 also rejects shapes that are too old ("not supported anymore"); 4.04r2 reads up to version 24 (v4 thread). | 3.x, 4.04r2, 5.12 |
| `.dif` | Torque interior (`InteriorResource`, with `ForceField` and `MirrorSubObject`) | all |
| `.ter` | Torque terrain file, read from `levels3d/terrain/` | 3.x, 4.04r2 |
| terrain chunks | 5.12 streams terrain from the server instead: `TerrainChunkEvent` ("sending/received terrain chunk (x, y): len n"), `TerrainRequestUpdatesEvent`, `heights` and `heights.info` names, "Loading terrain from terrain chunks." Terrain textures must be 256×256×24-bit. | 5.12 |
| `.3ds` | 3D Studio | 3.153 (`Shape3ds`), 4.04r2 (`Shape3ds`), 5.12 (`GameShape3DS`) |
| `.md3` | Quake 3 model, split head/upper/lower | 3.153 |
| `.mis` | Torque mission file | 3.x, 4.04r2 (5.12 has no `.mis` loader string and builds its `MissionGroup` from ghosts **[inf]**) |
| `.ml`, `.ifl` | material lists, image-file lists for animated textures | stock Torque |
| `.gft` | Torque cached GUI font (`%s%s_%d.gft`) | 3.x, 5.12 |
| `.dso` | compiled TorqueScript, see `scripting.md` | 3.x only |

3.153 also maps terrain textures to detail textures and footstep sound types in script (`addMaterialMapping`, see `scripting.md`). No `.dts`, `.dif`, `.ter` or `.mis` files ship with any Graal client: the 3D content always came from the server. **[file]**

## Rendering

- Stock Torque display devices in every build: `OpenGLDevice`, `D3DDevice` (Torque's OpenGL-to-Direct3D wrapper, `opengl2d3d.dll` / `glu2d3d.dll`) and `Voodoo2Device` (full-screen only). Minimum screen mode 640×480. **[bin]**
- 3.x on Linux uses SDL + OpenGL, on Mac AGL + DrawSprocket. 4.x and 5.12 on Windows: the Delphi launcher draws the 2D game with DirectDraw/Direct3D 7 and hosts the Torque canvas for 3D (`GuiGraal3DCtrl`, `runGraal3DEngine`, `resizeGraal3DWindow`, `toggleGraal3DFullScreen`). **[bin]**
- Under Wine 9 with Xvfb and Mesa (llvmpipe), the 5.12 launcher's 2D window runs. On switching to 3D the Torque side does start (`Activating the OpenGL display device`, Mesa llvmpipe, `Graal3D has been activated!`), but the launcher then faults re-initialising DirectDraw and stops calling `runGraal3DEngine`. Calling that export from an injected thread keeps Torque's networking running (enough for the full handshake, see `network.md`). A real GPU or a different Wine Direct3D setup is still needed to see the 3D view. **[run]**
- Scene lighting is Torque's (`SceneLighting`, lighting cached per mission), run as the last mission-load phase. **[bin]**
