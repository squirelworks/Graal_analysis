# The GS2 3D objects: what scripts can create (4.04r2, 5.12)

Date: 2026-11-25. Static reads of the Windows 4.04r2 and 5.12 `Graal3DEngine.dll`. Behaviour only;
no decompiled text, no addresses. Board rows T3D-014, T3D-016, T3D-019, T3D-020, T3D-050
([board](3d-capability-board.md)). Tags: **[bin]** static read, **[inf]** inference.

## How a class becomes scriptable

Both engines register each script-creatable class with the engine's object-creator registry (the
constructor GraalEngine exports as `TObjectCreator`): a class name and a factory that makes an object
of that class from a name. It is the same registry the 2D GS2 classes use (`GuiButtonCtrl`,
`Array`, `Date`, `Sound` and the rest sit in it in 5.12), so these are the names a GS2
`new ClassName("name")` can make. **[bin][inf]** Each class also registers its script properties and
functions with its parent class, which gives the inheritance below. **[bin]**

## 4.04r2: 86 registrations in the 3D plug-in

One name was not recovered; the other 85 are `SimObject`, `SimGroup`, `EditManager`, `Terraformer`, `TerrainEditor`, `WorldEditor`;
the Torque game layer with its datablocks: `Player`, `PlayerData`, `AIPlayer`, `Item`,
`ItemData`, `ShapeBase`, `ShapeBaseData`, `ShapeBaseImageData`, `StaticShape`,
`StaticShapeData`, `TSStatic`, `Shape3ds`, `Projectile`, `ProjectileData`, `Explosion`,
`ExplosionData`, `DebrisData`, `Splash`, `SplashData`, `Trigger`, `TriggerData`,
`MissionArea`, `MissionMarker`, `MissionMarkerData`, `SpawnSphere`, `Marker`, `PathCamera`,
`CameraData`, `AdvancedCameraData`, `GameBaseData`, `TSShapeConstructor`, `DecalData`;
vehicles (`FlyingVehicle`, `HoverVehicle`, `WheeledVehicle` and their data, tire and spring);
effects (`ParticleEmitter`, `ParticleEmitterNode`, `ParticleData`, `ParticleEmitterData`,
`ParticleEmitterNodeData`, `Precipitation`, `PrecipitationData`, `Lightning`,
`LightningData`, `fxLight`, `fxLightData`, `fxSunLight`, `volumeLight`, `FractalTree`,
`fxFoliageReplicator`, `fxGrassReplicator`, `fxShapeReplicator`, `twSurfaceReference`);
the world (`SceneObject`, `Sky`, `Sun`, `TerrainBlock`, `WaterBlock`, `InteriorInstance`,
`PathedInterior`, `PathedInteriorData`, `AudioEmitter`, `AudioProfile`,
`AudioDescription`); Graal's own `DynamicGrass`, `DynamicGrassReplicator`,
`DynamicShapeReplicator`; 3D GUI controls `GuiGraal3DCtrl`, `GuiCrossHairHud`,
`GuiMapOverviewCtrl`, `GuiPlayerView`, `GuiShapeNameHud`; and `ActionMap`. **[bin]**

So in 4.04r2 the whole Torque game layer, datablocks included, is reachable from GS2 by name. That
is how a 4.04r2-era script could set up players, vehicles, particles and weather without
TorqueScript, which the plug-in no longer compiles
([script-and-terrain-tools-by-build.md](script-and-terrain-tools-by-build.md)). **[bin][inf]**

## 5.12: 68 classes, 22 of them 3D

The 5.12 engine holds the 2D and 3D sides in one DLL, so its registry has both. The 3D and editor
part: `SimObject`, `SimGroup`, `SceneObject`, `GameObject`, `Sky`, `Sun`, `TerrainBlock`,
`WaterBlock`, `fxSunLight`, `DynamicShapeReplicator`, `DynamicGrass`,
`DynamicGrassReplicator`, `EditManager`, `WorldEditor`, `TerrainEditor`, `Terraformer`,
`GuiGraal3DCtrl`, `GuiInputCtrl`, `GuiMapOverviewCtrl`, `GuiPlayerView`, `GuiShapeNameHud`,
`ActionMap`. The rest are 2D GS2 classes (GUI controls, `TStaticVar`, `Color`, `Array`,
`Sound`, `Date`, `String`, two random generators). **[bin]**

Player, vehicles, projectiles, particles, datablocks, interiors and audio emitters are gone; a
`GameObject` with a shape takes their place. **[bin]**

### Script properties and functions in 5.12

Names as registered, in registration order; inherited names are not repeated. **[bin]** `Sky` and
`Sun` register differently and were not listed in this pass.

| Class | Parent | Count | Names |
|---|---|---|---|
| `SimObject` | `TGraalVar` | 0 | – |
| `SimGroup` | `SimObject` | 1 | `addcontrol` |
| `EditManager` | `GuiControl` | 0 | – |
| `Terraformer` | `TGraalVar` | 4 | `loadGrayscale`, `loadGreyscale`, `saveGreyscale`, `setTerrain` |
| `TerrainEditor` | `GuiControl` | 45 | `isDirty`, `isMissionDirty`, `renderBorder`, `borderHeight`, `borderFillColor`, `borderFrameColor`, `borderLineMode`, `selectionHidden`, `enableSoftBrushes`, `renderVertexSelection`, `processUsesBrush`, `brushPos`, `adjustHeightVal`, `setHeightVal`, `scaleVal`, `smoothFactor`, `materialGroup`, `softSelectRadius`, `softSelectFilter`, `softSelectDefaultFilter`, `adjustHeightMouseScale`, `paintMaterial`, `attachTerrain`, `getTerrainMaterials`, `setTerrainMaterials`, `setBrushType`, `setBrushSize`, `getBrushPos`, `setBrushPos`, `setAction`, `getNumActions`, `getActionName`, `getCurrentAction`, `resetSelWeights`, `clearSelection`, `processAction`, `buildMaterialMap`, `getNumTextures`, `getTextureName`, `markEmptySquares`, `clearModifiedFlags`, `mirrorTerrain`, `pushBaseMaterialInfo`, `popBaseMaterialInfo`, `setLoneBaseMaterial` |
| `WorldEditor` | `GuiControl` | 64 | `automaticsync`, `isDirty`, `planarMovement`, `undoLimit`, `dropType`, `projectDistance`, `boundingBoxCollision`, `renderPlane`, `renderPlaneHashes`, `gridColor`, `planeDim`, `gridSize`, `renderPopupBackground`, `popupBackgroundColor`, `popupTextColor`, `objectTextColor`, `objectsUseBoxCenter`, `axisGizmoMaxScreenLen`, `axisGizmoActive`, `mouseMoveScale`, `mouseRotateScale`, `mouseScaleScale`, `minScaleFactor`, `maxScaleFactor`, `objSelectColor`, `objMouseOverSelectColor`, `objMouseOverColor`, `showMousePopupInfo`, `dragRectColor`, `renderObjText`, `renderObjHandle`, `objTextFormat`, `faceSelectColor`, `renderSelectionBox`, `selectionBoxColor`, `selectionLocked`, `snapToGrid`, `snapRotations`, `rotationSnap`, `toggleIgnoreList`, `renderNav`, `selectHandle`, `defaultHandle`, `lockedHandle`, `nameMaxDistance`, `nameDistanceFade`, `ignoreObjClass`, `clearIgnoreList`, `getSelectedObject`, `getSelectionSize`, `clearSelection`, `selectObject`, `unselectObject`, `getSelectionCentroid`, `dropSelection`, `deleteSelection`, `getMode`, `setMode`, `hideSelection`, `lockSelection`, `addUndoState`, `lightSelection`, `syncSelection`, `reloadSelection` |
| `DynamicGrass` | `DynamicShapeReplicator` | 0 | – |
| `DynamicGrassReplicator` | `DynamicShapeReplicator` | 0 | – |
| `DynamicShapeReplicator` | `GameObject` | 22 | `allowedterrainslope`, `allowonterrain`, `allowoninteriors`, `allowonstatics`, `allowonwater`, `allowwatersurface`, `aligntoterrain`, `boxmin`, `boxmax`, `hidereplications`, `mingridobjects`, `maxgridobjects`, `offsetz`, `radius`, `shapefiles`, `shaperotatemin`, `shaperotatemax`, `shapescalemin`, `shapescalemax`, `surfaceexclusionmode`, `surfacetype`, `terrainalignment` |
| `fxSunLight` | `SceneObject` | 52 | `enable`, `localflarebitmap`, `remoteflarebitmap`, `sunazimuth`, `sunelevation`, `flaretp`, `colour`, `brightness`, `flaresize`, `fadetime`, `blendmode`, `animcolour`, `animbrightness`, `animrotation`, `animsize`, `animazimuth`, `animelevation`, `lerpcolour`, `lerpbrightness`, `lerprotation`, `lerpsize`, `lerpazimuth`, `lerpelevation`, `linkflaresize`, `singlecolourkeys`, `mincolour`, `maxcolour`, `minbrightness`, `maxbrightness`, `minrotation`, `maxrotation`, `minsize`, `maxsize`, `minazimuth`, `maxazimuth`, `minelevation`, `maxelevation`, `redkeys`, `greenkeys`, `bluekeys`, `brightnesskeys`, `rotationkeys`, `sizekeys`, `azimuthkeys`, `elevationkeys`, `colourtime`, `brightnesstime`, `rotationtime`, `sizetime`, `azimuthtime`, `elevationtime`, `reset` |
| `GameObject` | `SceneObject` | 46 | `alpha`, `attachedtoobject`, `attrobjects`, `collision`, `iseditorobject`, `liquidheight`, `liquidtype`, `movetype`, `nickcolor`, `nickname`, `position`, `scaledshapebox`, `shadow`, `shape`, `shapebox`, `showterrain`, `solid`, `transform`, `velocity`, `watercoverage`, `checkCollision`, `checkCollisionByBox`, `clipPolygons`, `findimg`, `getControllingClient`, `getControllingObject`, `getdropz`, `getInteriorObject`, `getMountedObject`, `getMountedObjectCount`, `getMountedObjectNode`, `getMountNodeObject`, `getMountTransform`, `getMountPosition`, `getNodeTransform`, `getNodePosition`, `getObjectMount`, `hideimg`, `hideimgs`, `isDrawn`, `isInInterior`, `isMounted`, `mountObject`, `setDirection`, `unmount`, `unmountObject` |
| `GuiGraal3DCtrl` | `GuiControl` | 0 | – |
| `GuiInputCtrl` | `GuiControl` | 0 | – |
| `GuiMapOverviewCtrl` | `GuiBitmapCtrl` | 2 | `mapalpha`, `pointsize` |
| `GuiPlayerView` | `GuiControl` | 8 | `ambientcolor`, `cameraz`, `lightcolor`, `lightdirection`, `modelrotx`, `modelrotz`, `shape`, `shapeobject` |
| `GuiShapeNameHud` | `GuiControl` | 14 | `alignBottom`, `chatprofile`, `damageAlignBottom`, `damageOffset`, `damageTimeout`, `verticalDamageOffset`, `useShapeSize`, `fillColor`, `frameColor`, `maxDistance`, `showFill`, `showFrame`, `verticalOffset`, `distanceFade` |
| `ActionMap` | `TGraalVar` | 3 | `getBinding`, `getCommand`, `unbind` |
| `SceneObject` | `SimObject` | 29 | `eulerrotation`, `forwardVector`, `objectBox`, `position`, `renderposition`, `rightVector`, `rotation`, `scale`, `scaledobjectbox`, `transform`, `upVector`, `worldBox`, `worldBoxCenter`, `light`, `getForwardVector`, `setForwardVector`, `getObjectBox`, `getPosition`, `setPosition`, `getRightVector`, `setRightVector`, `getScale`, `setScale`, `getTransform`, `setTransform`, `getUpVector`, `setUpVector`, `getWorldBox`, `getWorldBoxCenter` |
| `TerrainBlock` | `SceneObject` | 3 | `terrainFile`, `squareSize`, `repeatTerrain` |
| `WaterBlock` | `SceneObject` | 30 | `ignoreterrain`, `useDepthMask`, `surfaceTexture`, `shoreTexture`, `envMapOverTexture`, `envMapUnderTexture`, `submergeTexture0`, `submergeTexture1`, `specularMaskTex`, `liquidType`, `density`, `viscosity`, `waveMagnitude`, `surfaceOpacity`, `envMapIntensity`, `tessSurface`, `tessShore`, `surfaceParallax`, `flowAngle`, `flowRate`, `distortGridScale`, `distortMag`, `distortTime`, `shoreDepth`, `depthGradient`, `minAlpha`, `maxAlpha`, `removeWetEdges`, `specularColor`, `specularPower` |

Notes:

- `GameObject` has the movement and mounting functions a script needs to drive an object
  (`mountObject`, `unmount`, `getMountTransform`, `getNodePosition`, `setDirection`,
  `getdropz`, `checkCollision`, `checkCollisionByBox`) and the image calls
  `findimg`/`hideimg`/`hideimgs`, so 2D-style show-images work on 3D objects. **[bin][inf]**
- `WorldEditor` and `TerrainEditor` are GUI controls with their full stock editing set, and
  `EditManager` is registered too, so the client carries a scriptable 3D world and terrain editor.
  Whether a server-sent GS2 GUI can open them in a session is open (T3D-020). **[bin][inf]**
- `Terraformer.setTerrain` (read by the terrain lab): it does nothing and returns false unless a
  `TerrainBlock` is the client's current terrain; otherwise it copies the 256 by 256 register into
  that terrain's heights with the rows flipped, rebuilds the grid, relights it with a fixed light and
  returns true. No chunk-cache write or stamp update was seen on that path, so it changes the live
  view only. **[bin]**

## `getz` in 3D mode (5.12)

The GS2 function `getz(x, y)` picks its source by mode. In 3D mode it asks the 3D world: a ray straight
down from z = 2000 to z = −2000 at (x, y) against terrain objects, returning the hit height, or 0 if
nothing is hit. In 2D mode it returns the 2D board height (the level's heights, as before). So a 3D
session reads terrain height from the `TerrainBlock`, not from a level's `HEIGHTS` block, and no path
from 2D heights into a `TerrainBlock` was seen (T3D-042). **[bin][inf]**

## 3D event names (5.12)

Among the GS2 event names the 5.12 engine dispatches, these belong to the 3D side:
`onGraal3DConnectionEstablished`, `onGraal3DLoginStep`, `onGhostAlwaysStarted`,
`onGhostAlwaysObjectReceived`, `onCollision`, `onImpact`, `onEnterLiquid`, `onLeaveLiquid`,
`onMount`, `onUnmount` and `onMouseYawPitch`; `onRPGMessage` and `onRCChat` come from the BigData
text channel. Which object receives each, and with what parameters, was not read (T3D-021). **[bin]**

## Open

- [ ] T3D-016: create a `GameObject`, `Sky` and `Sun` from a client weapon with no server ghost,
  and see whether they draw.
- [ ] T3D-050: `new Terraformer`, `loadGreyscale` and `setTerrain` on a live client with a
  streamed `TerrainBlock`.
- [ ] T3D-020: open `WorldEditor` / `TerrainEditor` from a GS2 GUI in a 3D session.
- [ ] T3D-014: the 4.04r2 per-class property lists, and `Sky`/`Sun` in 5.12.
