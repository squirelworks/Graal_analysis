# The 5.12 GS2 3D scripting surface, typed: every class, property and function with its argument types (T3D-096)

Date: 2026-11-26. Static read of the GS2 (TGraalVar) registration tables in the
Windows `Graal3DEngine.dll` for 5.00r7 (the engine shipped as "5.12",
[T3D-005](3d-engines-5007-512-and-403-411-2026-11-25.md)) and a comparison with
4.04r2. Nothing was run. Behaviour only: names and argument/return **types**, no
addresses or decompiled text. Board row:
[T3D-096](3d-capability-board.tsv). **[bin]**

This types the surface that [gs2-3d-objects-404r2-512.md](gs2-3d-objects-404r2-512.md)
listed by name. A clientside GS2 weapon or NPC script drives a 5.12 client through
exactly these calls, so the argument types below are what a lab probe or a server
script must pass.

## How the registry is read

Each GS2 class is a `TProperties` registered with its name and its parent class;
its members live in a hash list, one record each. Two record shapes:

- **Property** — a type code and a getter, optionally a setter. Rendered below as
  `name — type, writable|read-only`. "writable" means a setter is registered
  (a script can assign it); "read-only" means getter only.
- **Function** — a return-type code and an **argument-type string**, one code per
  argument, plus the handler. Rendered as `name(argtypes) → return`.

The type codes are a single letter in the record: `i` int, `f`/`d` a number
(float/double), `s` string, `b` bool, `o` object handle, `v` void (functions
only). An empty argument list means the function takes no arguments. These are the
**declared** types the engine coerces to; a string-typed property often carries a
vector or a transform as text (e.g. `position`, `velocity`, `transform`).

This is the engine's own registration, so it is the ground truth for arity and
type, independent of any `-listscriptfunctions` dump.

## The model: 35 classes, 418 members (5.12)

Parent class is shown after each class name. A class with 0 members adds no GS2
surface of its own (it inherits its parent's). The editor classes (`WorldEditor`,
`TerrainEditor`, `EditManager`) are script-creatable GUI controls
([T3D-020](3d-capability-board.tsv)); their large surfaces are the in-client
editors.

### `ActionMap` → `TGraalVar` (8 members)
- `bind(string,string,string)` → void
- `getBinding(string)` → string
- `getCommand(string,string)` → string
- `load()` → bool
- `pop()` → void
- `push()` → void
- `save()` → void
- `unbind(string,string)` → void

### `Camera` → `GameObject` (6 members)
- `cameramode` — *string, writable*
- `eulerrotation` — *string, writable*
- `followattachedobject` — *object, writable*
- `lookatposition` — *string, writable*
- `lookvector` — *string, writable*
- `updatePosition()` → void

### `DTSAniThread` → `TGraalVar` (13 members)
- `aniindex` — *int, writable*
- `atend` — *bool, writable*
- `attack` — *bool, writable*
- `endpos` — *float, writable*
- `hold` — *bool, writable*
- `position` — *float, writable*
- `sequence` — *string, writable*
- `startpos` — *float, writable*
- `state` — *string, writable*
- `timescale` — *float, writable*
- `transtitiontime` — *float, writable*
- `play()` → void
- `isintransition()` → bool

### `DynamicGrass` → `DynamicShapeReplicator` (0 members)

### `DynamicGrassReplicator` → `DynamicShapeReplicator` (0 members)

### `DynamicShapeReplicator` → `GameObject` (23 members)
- `allowedterrainslope` — *int, writable*
- `allowonterrain` — *bool, writable*
- `allowoninteriors` — *bool, writable*
- `allowonstatics` — *bool, writable*
- `allowonwater` — *bool, writable*
- `allowwatersurface` — *bool, writable*
- `aligntoterrain` — *bool, writable*
- `boxmin` — *string, writable*
- `boxmax` — *string, writable*
- `hidereplications` — *bool, writable*
- `mingridobjects` — *int, writable*
- `maxgridobjects` — *int, writable*
- `offsetz` — *float, writable*
- `radius` — *int, writable*
- `seed` — *int, writable*
- `shapefiles` — *string, writable*
- `shaperotatemin` — *string, writable*
- `shaperotatemax` — *string, writable*
- `shapescalemin` — *string, writable*
- `shapescalemax` — *string, writable*
- `surfaceexclusionmode` — *bool, writable*
- `surfacetype` — *int, writable*
- `terrainalignment` — *string, writable*

### `EditManager` → `GuiControl` (0 members)

### `GameConnection` → `SimGroup` (5 members)
- `camera` — *object, writable*
- `account` — *string, writable*
- `nick` — *string, writable*
- `objecttype()` → string
- `showprofile()` → void

### `GameMovementInterpolate` → `TGraalVar` (2 members)
- `rigid` — *object, writable*
- `applyImpulse(string,string)` → void

### `GameMovementList` → `TGraalVar` (2 members)
- `move3d(string,num,int)` → void
- `finishMoves()` → void

### `GameMovementRigid` → `GameMovementInterpolate` (1 members)
- `addRigidMove(string,string)` → void

### `GameObject` → `SceneObject` (49 members)
- `alpha` — *float, writable*
- `attachedtoobject` — *object, writable*
- `attr` — *object, writable*
- `attrobjects` — *object, writable*
- `chat` — *string, writable*
- `collision` — *bool, writable*
- `iseditorobject` — *bool, writable*
- `liquidheight` — *float, writable*
- `liquidtype` — *string, writable*
- `movetype` — *string, writable*
- `nickcolor` — *string, writable*
- `nickname` — *string, writable*
- `position` — *string, writable*
- `scaledshapebox` — *string, writable*
- `shadow` — *bool, writable*
- `shape` — *string, writable*
- `shapebox` — *string, writable*
- `showterrain` — *bool, writable*
- `skin` — *string, writable*
- `solid` — *bool, writable*
- `transform` — *string, writable*
- `velocity` — *string, writable*
- `watercoverage` — *float, writable*
- `checkCollision(string,string)` → object
- `checkCollisionByBox(string,string,string)` → object
- `clipPolygons(string)` → object
- `findimg(int)` → object
- `getControllingClient()` → object
- `getControllingObject()` → object
- `getdropz(string)` → float
- `getInteriorObject()` → object
- `getMountedObject(int)` → object
- `getMountedObjectCount()` → int
- `getMountedObjectNode(int)` → int
- `getMountNodeObject(int)` → object
- `getMountTransform(int)` → string
- `getMountPosition(int)` → string
- `getNodeTransform(string)` → string
- `getNodePosition(string)` → string
- `getObjectMount()` → object
- `hideimg(int)` → void
- `hideimgs(int,int)` → void
- `isDrawn()` → bool
- `isInInterior()` → bool
- `isMounted()` → bool
- `mountObject(object,int)` → bool
- `setDirection(string)` → void
- `unmount()` → void
- `unmountObject(object)` → bool

### `GameShape` → `TGraalVar` (2 members)
- `vertexshader` — *string, writable*
- `pixelshader` — *string, writable*

### `GameShapeDIF` → `GameShape` (2 members)
- `activateLight(string)` → void
- `deactivateLight(string)` → void

### `GameShapeDTS` → `GameShape` (9 members)
- `materiallist` — *object, writable*
- `materials` — *object, writable*
- `forceAnimations()` → void
- `getAnimation(int)` → object
- `listNodes()` → object
- `pauseAnimation(int)` → void
- `playAnimation(int,string,int)` → object
- `playAnimation2(int,string,int,float,float,float,float)` → object
- `stopAnimation(int)` → void

### `GameShapeFT` → `GameShape` (2 members)
- `seed` — *int, writable*
- `levels` — *int, writable*

### `GuiGraal3DCtrl` → `GuiControl` (0 members)

### `GuiInputCtrl` → `GuiControl` (0 members)

### `GuiMapOverviewCtrl` → `GuiBitmapCtrl` (2 members)
- `mapalpha` — *float, writable*
- `pointsize` — *float, writable*

### `GuiPlayerView` → `GuiControl` (8 members)
- `ambientcolor` — *string, writable*
- `cameraz` — *float, writable*
- `lightcolor` — *string, writable*
- `lightdirection` — *string, writable*
- `modelrotx` — *float, writable*
- `modelrotz` — *float, writable*
- `shape` — *string, writable*
- `shapeobject` — *object, writable*

### `GuiShapeNameHud` → `GuiControl` (14 members)
- `alignBottom` — *bool, writable*
- `chatprofile` — *string, writable*
- `damageAlignBottom` — *bool, writable*
- `damageOffset` — *string, writable*
- `damageTimeout` — *float, writable*
- `verticalDamageOffset` — *float, writable*
- `useShapeSize` — *bool, writable*
- `fillColor` — *string, writable*
- `frameColor` — *string, writable*
- `maxDistance` — *float, writable*
- `showFill` — *bool, writable*
- `showFrame` — *bool, writable*
- `verticalOffset` — *float, writable*
- `distanceFade` — *float, writable*

### `SceneObject` → `SimObject` (32 members)
- `eulerrotation` — *string, writable*
- `forwardVector` — *string, writable*
- `objectBox` — *string, writable*
- `position` — *string, writable*
- `renderposition` — *string, writable*
- `rightVector` — *string, writable*
- `rotation` — *string, writable*
- `scale` — *string, writable*
- `scaledobjectbox` — *string, writable*
- `transform` — *string, writable*
- `upVector` — *string, writable*
- `worldBox` — *string, writable*
- `worldBoxCenter` — *string, writable*
- `x` — *float, writable*
- `y` — *float, writable*
- `z` — *float, writable*
- `light()` → void
- `getForwardVector()` → string
- `setForwardVector(string)` → void
- `getObjectBox()` → string
- `getPosition()` → string
- `setPosition(string)` → void
- `getRightVector()` → string
- `setRightVector(string)` → void
- `getScale()` → string
- `setScale(string)` → void
- `getTransform()` → string
- `setTransform(string)` → void
- `getUpVector()` → string
- `setUpVector(string)` → void
- `getWorldBox()` → string
- `getWorldBoxCenter()` → string

### `SimGroup` → `SimObject` (1 members)
- `addcontrol(object)` → void

### `SimObject` → `TGraalVar` (0 members)

### `Sky` → `SceneObject` (30 members)
- `cloudHeight1` — *float, writable*
- `cloudHeight2` — *float, writable*
- `cloudHeight3` — *float, writable*
- `cloudSpeed1` — *float, writable*
- `cloudSpeed2` — *float, writable*
- `cloudSpeed3` — *float, writable*
- `fogColor` — *string, writable*
- `fogStorm1` — *bool, writable*
- `fogStorm2` — *bool, writable*
- `fogStorm3` — *bool, writable*
- `fogVolume1` — *string, writable*
- `fogVolume2` — *string, writable*
- `fogVolume3` — *string, writable*
- `fogVolumeColor1` — *string, writable*
- `fogVolumeColor2` — *string, writable*
- `fogVolumeColor3` — *string, writable*
- `materialList` — *string, writable*
- `norenderbans` — *bool, writable*
- `renderbottomtexture` — *bool, writable*
- `skyfadetime` — *float, writable*
- `skysolidcolor` — *string, writable*
- `useskytextures` — *bool, writable*
- `windeffectprecipitation` — *bool, writable*
- `windVelocity` — *string, writable*
- `getWindowVelocity()` → string
- `stormClouds(bool,num)` → void
- `stormFog(num,num)` → void
- `realFog(bool,num,num,num)` → void
- `stormCloudsShow(bool)` → void
- `stormFogShow(bool)` → void

### `Sun` → `SimObject` (3 members)
- `direction` — *string, writable*
- `color` — *string, writable*
- `ambient` — *string, writable*

### `TGameObjectAttr` → `TGraalVar` (0 members)

### `TMovementRigid` → `TGraalVar` (1 members)
- `mass` — *float, writable*

### `TShapeMaterial` → `TGraalVar` (1 members)
- `specularpower` — *int, writable*

### `Terraformer` → `TGraalVar` (4 members)
- `loadGrayscale(int,string)` → bool
- `loadGreyscale(int,string)` → bool
- `saveGreyscale(int,string)` → bool
- `setTerrain(int)` → bool

### `TerrainBlock` → `SceneObject` (3 members)
- `terrainFile` — *string, writable*
- `squareSize` — *int, writable*
- `repeatTerrain` — *bool, writable*

### `TerrainEditor` → `GuiControl` (47 members)
- `isDirty` — *bool, writable*
- `isMissionDirty` — *bool, writable*
- `renderBorder` — *bool, writable*
- `borderHeight` — *float, writable*
- `borderFillColor` — *string, writable*
- `borderFrameColor` — *string, writable*
- `borderLineMode` — *bool, writable*
- `selectionHidden` — *bool, writable*
- `enableSoftBrushes` — *bool, writable*
- `renderVertexSelection` — *bool, writable*
- `processUsesBrush` — *bool, writable*
- `brushPos` — *string, writable*
- `adjustHeightVal` — *float, writable*
- `setHeightVal` — *float, writable*
- `scaleVal` — *float, writable*
- `smoothFactor` — *float, writable*
- `materialGroup` — *int, writable*
- `softSelectRadius` — *float, writable*
- `softSelectFilter` — *string, writable*
- `softSelectDefaultFilter` — *string, writable*
- `adjustHeightMouseScale` — *float, writable*
- `paintMaterial` — *string, writable*
- `attachTerrain(string)` → void
- `getTerrainMaterials()` → object
- `setTerrainMaterials(string)` → void
- `setBrushType(string)` → void
- `setBrushSize(int,int)` → void
- `getBrushPos()` → string
- `setBrushPos(string)` → void
- `setAction(string)` → void
- `getNumActions()` → int
- `getActionName(int)` → string
- `getCurrentAction()` → string
- `resetSelWeights(bool)` → void
- `undo()` → void
- `redo()` → void
- `clearSelection()` → void
- `processAction(string)` → void
- `buildMaterialMap()` → void
- `getNumTextures()` → int
- `getTextureName(int)` → string
- `markEmptySquares()` → void
- `clearModifiedFlags()` → void
- `mirrorTerrain(int)` → void
- `pushBaseMaterialInfo()` → void
- `popBaseMaterialInfo()` → void
- `setLoneBaseMaterial(string)` → void

### `WaterBlock` → `SceneObject` (30 members)
- `ignoreterrain` — *bool, writable*
- `useDepthMask` — *bool, writable*
- `surfaceTexture` — *string, writable*
- `shoreTexture` — *string, writable*
- `envMapOverTexture` — *string, writable*
- `envMapUnderTexture` — *string, writable*
- `submergeTexture0` — *string, writable*
- `submergeTexture1` — *string, writable*
- `specularMaskTex` — *string, writable*
- `liquidType` — *string, writable*
- `density` — *float, writable*
- `viscosity` — *float, writable*
- `waveMagnitude` — *float, writable*
- `surfaceOpacity` — *float, writable*
- `envMapIntensity` — *float, writable*
- `tessSurface` — *float, writable*
- `tessShore` — *float, writable*
- `surfaceParallax` — *float, writable*
- `flowAngle` — *float, writable*
- `flowRate` — *float, writable*
- `distortGridScale` — *float, writable*
- `distortMag` — *float, writable*
- `distortTime` — *float, writable*
- `shoreDepth` — *float, writable*
- `depthGradient` — *float, writable*
- `minAlpha` — *float, writable*
- `maxAlpha` — *float, writable*
- `removeWetEdges` — *bool, writable*
- `specularColor` — *string, writable*
- `specularPower` — *float, writable*

### `WorldEditor` → `GuiControl` (66 members)
- `automaticsync` — *bool, writable*
- `isDirty` — *bool, writable*
- `planarMovement` — *bool, writable*
- `undoLimit` — *int, writable*
- `dropType` — *string, writable*
- `projectDistance` — *float, writable*
- `boundingBoxCollision` — *bool, writable*
- `renderPlane` — *bool, writable*
- `renderPlaneHashes` — *bool, writable*
- `gridColor` — *string, writable*
- `planeDim` — *float, writable*
- `gridSize` — *string, writable*
- `renderPopupBackground` — *bool, writable*
- `popupBackgroundColor` — *string, writable*
- `popupTextColor` — *string, writable*
- `objectTextColor` — *string, writable*
- `objectsUseBoxCenter` — *bool, writable*
- `axisGizmoMaxScreenLen` — *int, writable*
- `axisGizmoActive` — *bool, writable*
- `mouseMoveScale` — *float, writable*
- `mouseRotateScale` — *float, writable*
- `mouseScaleScale` — *float, writable*
- `minScaleFactor` — *float, writable*
- `maxScaleFactor` — *float, writable*
- `objSelectColor` — *string, writable*
- `objMouseOverSelectColor` — *string, writable*
- `objMouseOverColor` — *string, writable*
- `showMousePopupInfo` — *bool, writable*
- `dragRectColor` — *string, writable*
- `renderObjText` — *bool, writable*
- `renderObjHandle` — *bool, writable*
- `objTextFormat` — *string, writable*
- `faceSelectColor` — *string, writable*
- `renderSelectionBox` — *bool, writable*
- `selectionBoxColor` — *string, writable*
- `selectionLocked` — *bool, writable*
- `snapToGrid` — *bool, writable*
- `snapRotations` — *bool, writable*
- `rotationSnap` — *float, writable*
- `toggleIgnoreList` — *bool, writable*
- `renderNav` — *bool, writable*
- `selectHandle` — *string, read-only*
- `defaultHandle` — *string, read-only*
- `lockedHandle` — *string, read-only*
- `nameMaxDistance` — *float, read-only*
- `nameDistanceFade` — *float, read-only*
- `ignoreObjClass(string)` → void
- `clearIgnoreList()` → void
- `getSelectedObject(int)` → object
- `getSelectionSize()` → int
- `undo()` → void
- `redo()` → void
- `clearSelection()` → void
- `selectObject(object)` → void
- `unselectObject(object)` → void
- `getSelectionCentroid()` → string
- `dropSelection()` → void
- `deleteSelection()` → void
- `getMode()` → string
- `setMode(string)` → void
- `hideSelection(bool)` → void
- `lockSelection(bool)` → void
- `addUndoState()` → void
- `lightSelection()` → void
- `syncSelection()` → void
- `reloadSelection()` → void

### `fxSunLight` → `SceneObject` (52 members)
- `enable` — *bool, writable*
- `localflarebitmap` — *string, writable*
- `remoteflarebitmap` — *string, writable*
- `sunazimuth` — *float, writable*
- `sunelevation` — *float, writable*
- `flaretp` — *bool, writable*
- `colour` — *string, writable*
- `brightness` — *float, writable*
- `flaresize` — *float, writable*
- `fadetime` — *float, writable*
- `blendmode` — *int, writable*
- `animcolour` — *bool, writable*
- `animbrightness` — *bool, writable*
- `animrotation` — *bool, writable*
- `animsize` — *bool, writable*
- `animazimuth` — *bool, writable*
- `animelevation` — *bool, writable*
- `lerpcolour` — *bool, writable*
- `lerpbrightness` — *bool, writable*
- `lerprotation` — *bool, writable*
- `lerpsize` — *bool, writable*
- `lerpazimuth` — *bool, writable*
- `lerpelevation` — *bool, writable*
- `linkflaresize` — *bool, writable*
- `singlecolourkeys` — *bool, writable*
- `mincolour` — *string, writable*
- `maxcolour` — *string, writable*
- `minbrightness` — *float, writable*
- `maxbrightness` — *float, writable*
- `minrotation` — *float, writable*
- `maxrotation` — *float, writable*
- `minsize` — *float, writable*
- `maxsize` — *float, writable*
- `minazimuth` — *float, writable*
- `maxazimuth` — *float, writable*
- `minelevation` — *float, writable*
- `maxelevation` — *float, writable*
- `redkeys` — *string, writable*
- `greenkeys` — *string, writable*
- `bluekeys` — *string, writable*
- `brightnesskeys` — *string, writable*
- `rotationkeys` — *string, writable*
- `sizekeys` — *string, writable*
- `azimuthkeys` — *string, writable*
- `elevationkeys` — *string, writable*
- `colourtime` — *float, writable*
- `brightnesstime` — *float, writable*
- `rotationtime` — *float, writable*
- `sizetime` — *float, writable*
- `azimuthtime` — *float, writable*
- `elevationtime` — *float, writable*
- `reset()` → void


## 4.04r2 for comparison

4.04r2's 3D engine registers **133** GS2 members (its stock-Torque game and camera
layer; the class grouping is not symbol-recoverable in that build, so this is the
flat set). The split against 5.12 is the camera/control story of
[T3D-088](3d-gs2-functions-by-build-2026-11-25.md), now at member granularity:

**Registered on 4.04r2, gone on 5.12** (54) — the stock-TGE control, camera,
vehicle and AI surface:

`checkDismountPoint clearAim clearControlObject clearPlayerObject clearTargetObject getAimLocation getAimObject getCameraPosition getControlObject getDamageLocation getGodViewOffset getLookAtOffset getMoveDestination getState getThirdPersonOffset getWheelCount hide isMoving modifyStorm mountShape setActionThread setAimLocation setAimObject setCameraPosition setControlObject setFlyMode setFollowTerrainMode setGodViewMode setGodViewOffset setLookAtOffset setModel setMoveDestination setMoveSpeed setOrbitChangeAngle setOrbitChangeZoom setOrbitMinMaxDeclination setOrbitMinMaxZoom setOrbitMode setPlayerObject setTargetObject setThirdPersonMode setThirdPersonOffset setThirdPersonPanMode setThirdPersonTargetMode setTrackMode setWheelPowered setWheelSpring setWheelSteering setWheelTire show startFade stop unmountShape useCreateHeight`

These are the third-person/orbit camera (`setThirdPersonMode`, `setOrbitMode`,
`setGodViewMode`, `getCameraPosition`…), the wheeled-vehicle controls
(`setWheel*`), the control-object and aim API (`setControlObject`,
`setAimObject`, `getMoveDestination`, `getState`) and `mountShape`/`unmountShape`.
A 5.12 script cannot call any of them.

**Registered on 5.12, not on 4.04r2** (44) — the GameObject method set that
replaced them:

`activateLight addRigidMove applyImpulse checkCollision checkCollisionByBox clipPolygons deactivateLight findimg finishMoves forceAnimations getAnimation getControllingClient getControllingObject getInteriorObject getMountNodeObject getMountPosition getMountTransform getMountedObject getMountedObjectCount getMountedObjectNode getNodePosition getNodeTransform getObjectMount getdropz hideimg hideimgs isDrawn isInInterior isMounted isintransition listNodes mountObject move3d pauseAnimation play playAnimation playAnimation2 reset setDirection showprofile stopAnimation unmount unmountObject updatePosition`

i.e. `mountObject`/`unmountObject`, `checkCollision`/`checkCollisionByBox`,
`findimg`/`hideimg`, `play`/`playAnimation`, `move3d`, `getdropz`, the mount-node
queries and the control-object getters. This is the GameObject drawable model
([T3D-081](3d-object-classes-by-build-2026-11-25.md)) at the script level: one
object type with a fixed typed method set, in place of the per-class datablock
control API.

## The global 3D functions

A handful of 3D functions are not class members but global GS2 functions, dispatched
by name in the engine rather than through the `TProperties` tables
([3d-gs2-functions-by-build](3d-gs2-functions-by-build-2026-11-25.md) lists them by
name). Their arity, read from each handler body on 5.12: **[bin]**

- `castRay(start, end, typemask)` — two points (as strings) and a type mask; returns
  an array var (hit object, hit point, normal).
- `get3Dobjectsbybox` / `get3Dobjectsbyradius` — spatial queries returning object
  lists.
- `getz(x, y)` → float — terrain/collision height at a point.
- `getTerrainTexture` / `getTerrainTextureIndex` — terrain-texture queries.
- The sky/fog/time setters (`setSunColors`, `setFogColors`, `setSkyBandColors`,
  `setSkyBandSizes`, `syncTimeOfDay`, `updateVisibleDistance`, `lightScene`) each
  take one list or no argument and fill a client-side keyframe table
  ([3d-engine-static-reads](3d-engine-static-reads-2026-11-25.md), T3D-063).

## For a server and for lab rows

- The tables above are the exact call shapes for a 5.12-class client. A probe that
  exercises a function should pass the declared types: e.g. `mountObject(object,
  int)`, `findimg(int)`, `getdropz(string)` (a position string), `hideimgs(int,
  int)`, `checkCollisionByBox(string, string, string)`.
- A string-typed property that holds geometry (`position`, `velocity`,
  `transform`, `shapebox`, `scaledshapebox`, the sky/water vectors) takes
  space-separated numbers as text, not a number type.
- `GameObject`'s 23 properties and 26 methods are the whole drawable-object script
  API; `Sky` (30), `WaterBlock` (30) and `fxSunLight` (52) are the scene-effect
  surfaces; `WorldEditor` (66) and `TerrainEditor` (47) are the in-client editors.
- The 4.04r2-only camera/vehicle functions must **not** be used against a 5.12
  client; use `cameramode` plus the GameObject method set instead.
