<!-- manual: kind=reference status=draft -->
# 8.5 3D scripting (Torque-era clients)

This chapter is the script author's view of the 3D side of the 3.x to 5.12 clients: which language a build runs for 3D (§8.5.1), how GS2 reaches the Torque engine (§8.5.2), the classes, properties and functions it can use (§8.5.3 to §8.5.6), the 3D events and login steps (§8.5.7), terrain and water, including the streamed terrain a script reads (§8.5.8), sky, lighting, camera and shaders (§8.5.9), what a script can build without a server (§8.5.10), the session and content rules a 3D script runs under (§8.5.11), what each build allows (§8.5.12) and what is still open (§8.5.13). The wire, the object model and the file formats stay canonical in Part X (→ §10.3, §10.5, §10.6); this chapter points there instead of repeating them. The February 2000 DirectX Graal3D has no NPC scripting at all (→ §9.0).

> Status: draft. Built from the Torque-era 3D capability board and its result notes as of 2026-11-25; each row says whether it is a static read, a live run or an inference, and §8.5.13 lists what is open. A narrative companion for general readers, the Graal3D community guide, is kept outside this repository; it is not a source for this chapter, and nor is any third-party 3D server.

## 8.5.1 Which language drives the 3D side

From 4.x on, GS2 replaced TorqueScript on the 3D side. Only 3.153 (and the stock 3.04 TGE base) still compiles and runs Torque scripts [bin] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files). The table gives, for each build read, what survives of TorqueScript.

| Item | 3.153 Mac | 4.04r2 Win plug-in | 5.12 Win engine | Source |
| --- | --- | --- | --- | --- |
| TorqueScript compiler messages | present | absent | absent | [bin] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files) |
| `exec`, `compile` console names | present | absent | absent | [bin] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files) |
| `eval` | present | a string only, not a registered function | absent | [bin] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files) |
| `schedule`, `dumpConsoleFunctions` | present | present | absent | [bin] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files) |
| ships TorqueScript | yes (`main3D.cs` and `.dso` files) | no | no | [bin][file] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files) |
| can a server push new TorqueScript | no path found | no | no | [bin][inf] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files) |

The rules below say why a server cannot push TorqueScript to any of these builds [bin] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files).

| Rule | Source |
| --- | --- |
| Every build read (3.153, 4.04r2, 5.12) asks the server for any missing resource except `.dso`, `.cs` and `.ter` | [bin] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files) |
| 3.153's download sorter files a pushed file by extension under `levels/` or `levels3d/` and has no rule that executes what it stores | [bin] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files) |
| In 3.153 only the shipped scripts call `exec`, each on a fixed list | [file] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files) |
| A 3.153 server reaches client script only through `commandToClient` and the `clientCmd` handlers the shipped scripts define: the centre and bottom print and clear handlers, `clientCmdChatMessage`, `clientCmdServerMessage`, `clientCmdMissionStart`, `clientCmdMissionEnd`, `clientCmdSyncClock` and `clientCmdMissionStartPhase1` to `3`; none of their files contains `exec` or `eval` | [file][inf] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files) |
| Live on 3.153 against a lab server, a `.cs` was never fetched and the marker script never ran; the client never asked for `.cs`, `.dso` or `.ter`, so a server cannot push script | [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#3153) |
| Live on 3.153 all 12 handlers arrive and are dispatched: the centre and bottom print and `SyncClock` handlers call GUI objects that do not exist; `ChatMessage` and `ServerMessage` call `onChatMessage` and `onServerMessage`, which do not exist; the two clears, `MissionStart` and `MissionEnd` log nothing; `MissionStartPhase1` to `3` rerun the phases and acknowledge each; an unknown `clientCmd` is dropped silently | [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#3153) |
| At start 3.153 execs `clientprefs3D.cs` (twice), `keysconfig2D.cs`, `keysconfig3D.cs` and `languageEnglish.cs` and writes `.dso` files next to them | [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#3153) |
| 4.04r2 still registers about 277 stock console functions, but none is `exec`, `eval` or `compile`, so no text reaches a TorqueScript interpreter | [bin][inf] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files) |
| In a 4.04r2 3D session, `.cs`, `.dso` and `.mis` files beside the client are listed by the folder scan but never opened (→ §10.6) | [lab] (protocol/lab-appe-hostb-2026-11-20c.md#mis-and-dso-beside-the-404r2-client-e502-e503) |
| The `.cs` in 5.12's extension list is the file-access gate of the GS2 file functions (read and write, `getFileModTime`, `requestURL`), not a script loader; a path must also sit under `levels/`, `levels3d/`, `translations/`, `offline/`, `tileobjects/` or `updatepackages/`, and one that fails returns empty | [bin] (torque/3d-formats-renderer-camera-by-build.md#the-cs-entry-in-512s-file-list-t3d-013) |

The compiled TorqueScript format and the 3.x shipped scripts are in → §10.4. GS2 itself is in → §8.3 and → §8.4.

## 8.5.2 How GS2 reaches the 3D engine

The 4.x and 5.x clients have no console bridge: GS2 reaches the 3D side only through classes the engine registers with GS2. The rules give the path a script has, and the ones it does not have [bin] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files).

| Rule | Source |
| --- | --- |
| Each script-creatable 3D class is registered in the engine's object-creator registry, the same one the 2D GS2 classes (`GuiButtonCtrl`, `Array`, `Date`, `Sound`) use, so these are the names `new ClassName("name")` can make | [bin][inf] (torque/gs2-3d-objects-404r2-512.md#how-a-class-becomes-scriptable) |
| Each class registers its script properties and functions with its parent class, which gives the inheritance used in §8.5.4 | [bin] (torque/gs2-3d-objects-404r2-512.md#how-a-class-becomes-scriptable) |
| The 4.04r2 plug-in exports three functions (load, run and end the engine); the host hands it 77 `graal_set…` callbacks, none of which takes a function name to run on the Torque side | [bin] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files) |
| The callbacks that cross from the 2D engine to the 3D side carry data, not code: script events, server text, datablock properties, the player's script object, files, drawing and window state | [bin] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files) |
| So 4.04r2's registered console functions are reachable only from native code inside the plug-in, not from GS2 by name | [bin][inf] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files) |
| In 3D mode the 3D server, not the TCP game server, delivers the client's GS2 weapons and flags, as text commands on the BigData channel (→ §10.5.3) | [bin][inf] (graal3d/torque-engine-4x.md#graal-events-and-text-big-data-channel) |

The text-channel functions and events a 3D script shares with 2D GS2 (`sendtext`, `receivetext`, `onRCChat`, `onRPGMessage`, `getDatablockProperties`) are listed with the published API in → §8.3.5.

## 8.5.3 Classes a script can create

The two builds read register very different 3D sets. 4.04r2 exposes the whole Torque game layer; 5.12 replaces it with `GameObject` [bin] (torque/gs2-3d-objects-404r2-512.md#404r2-86-registrations-in-the-3d-plug-in). The table groups the classes; `·` means the build does not register the group.

| Group | 4.04r2 (86 registrations, one name not recovered) | 5.12 (68 classes, 22 of them 3D) | Source |
| --- | --- | --- | --- |
| base and scene | `SimObject`, `SimGroup`, `SceneObject` | `SimObject`, `SimGroup`, `SceneObject` | [bin] (torque/gs2-3d-objects-404r2-512.md#404r2-86-registrations-in-the-3d-plug-in); [bin] (torque/gs2-3d-objects-404r2-512.md#512-68-classes-22-of-them-3d) |
| Graal's 3D object | · | `GameObject` | [bin] (torque/gs2-3d-objects-404r2-512.md#512-68-classes-22-of-them-3d) |
| players, items, shapes | `Player`, `PlayerData`, `AIPlayer`, `Item`, `ItemData`, `ShapeBase`, `ShapeBaseData`, `ShapeBaseImageData`, `StaticShape`, `StaticShapeData`, `TSStatic`, `Shape3ds`, `TSShapeConstructor`, `GameBaseData` | · | [bin] (torque/gs2-3d-objects-404r2-512.md#404r2-86-registrations-in-the-3d-plug-in) |
| weapons and effects | `Projectile`, `ProjectileData`, `Explosion`, `ExplosionData`, `DebrisData`, `Splash`, `SplashData`, `DecalData`, particle emitters, nodes and their data, `Precipitation`, `Lightning`, `fxLight`, `volumeLight` | · | [bin] (torque/gs2-3d-objects-404r2-512.md#404r2-86-registrations-in-the-3d-plug-in) |
| vehicles | `FlyingVehicle`, `HoverVehicle`, `WheeledVehicle`, their data, tire and spring | · | [bin] (torque/gs2-3d-objects-404r2-512.md#404r2-86-registrations-in-the-3d-plug-in) |
| mission markers | `Trigger`, `TriggerData`, `MissionArea`, `MissionMarker`, `MissionMarkerData`, `SpawnSphere`, `Marker`, `PathCamera`, `CameraData`, `AdvancedCameraData` | · | [bin] (torque/gs2-3d-objects-404r2-512.md#404r2-86-registrations-in-the-3d-plug-in) |
| world | `Sky`, `Sun`, `TerrainBlock`, `WaterBlock`, `InteriorInstance`, `PathedInterior`, `PathedInteriorData`, `fxSunLight` | `Sky`, `Sun`, `TerrainBlock`, `WaterBlock`, `fxSunLight` | [bin] (torque/gs2-3d-objects-404r2-512.md#404r2-86-registrations-in-the-3d-plug-in); [bin] (torque/gs2-3d-objects-404r2-512.md#512-68-classes-22-of-them-3d) |
| ground cover | `FractalTree`, `fxFoliageReplicator`, `fxGrassReplicator`, `fxShapeReplicator`, `twSurfaceReference`, `DynamicGrass`, `DynamicGrassReplicator`, `DynamicShapeReplicator` | `DynamicGrass`, `DynamicGrassReplicator`, `DynamicShapeReplicator` | [bin] (torque/gs2-3d-objects-404r2-512.md#404r2-86-registrations-in-the-3d-plug-in); [bin] (torque/gs2-3d-objects-404r2-512.md#512-68-classes-22-of-them-3d) |
| audio | `AudioEmitter`, `AudioProfile`, `AudioDescription` | · | [bin] (torque/gs2-3d-objects-404r2-512.md#404r2-86-registrations-in-the-3d-plug-in) |
| editors and terrain tools | `EditManager`, `WorldEditor`, `TerrainEditor`, `Terraformer` | `EditManager`, `WorldEditor`, `TerrainEditor`, `Terraformer` | [bin] (torque/gs2-3d-objects-404r2-512.md#404r2-86-registrations-in-the-3d-plug-in); [bin] (torque/gs2-3d-objects-404r2-512.md#512-68-classes-22-of-them-3d) |
| 3D GUI and input | `GuiGraal3DCtrl`, `GuiCrossHairHud`, `GuiMapOverviewCtrl`, `GuiPlayerView`, `GuiShapeNameHud`, `ActionMap` | `GuiGraal3DCtrl`, `GuiInputCtrl`, `GuiMapOverviewCtrl`, `GuiPlayerView`, `GuiShapeNameHud`, `ActionMap` | [bin] (torque/gs2-3d-objects-404r2-512.md#404r2-86-registrations-in-the-3d-plug-in); [bin] (torque/gs2-3d-objects-404r2-512.md#512-68-classes-22-of-them-3d) |

What follows from the two sets:

| Rule | Source |
| --- | --- |
| A 4.04r2-era script could set up players, vehicles, particles and weather by name without TorqueScript, which the plug-in no longer compiles | [bin][inf] (torque/gs2-3d-objects-404r2-512.md#404r2-86-registrations-in-the-3d-plug-in) |
| In 5.12, players, vehicles, projectiles, particles, datablocks, interiors and audio emitters are gone; a `GameObject` with a shape takes their place | [bin] (torque/gs2-3d-objects-404r2-512.md#512-68-classes-22-of-them-3d) |
| The other 46 classes in 5.12's registry are 2D GS2 classes (GUI controls, `TStaticVar`, `Color`, `Array`, `Sound`, `Date`, `String`, two random generators) | [bin] (torque/gs2-3d-objects-404r2-512.md#512-68-classes-22-of-them-3d) |
| 4.20r6 already has the `GameObject` layer in place of the game classes; its GS2 class list has not been read | [bin] (torque/wire-by-build.md#the-networked-class-sets) |

## 8.5.4 Properties and functions in 5.12

Names are given as registered; inherited names are not repeated [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512). `Sky` and `Sun` register their names another way and were not listed in that pass (→ §8.5.13).

| Class | Parent | Names | Source |
| --- | --- | --- | --- |
| `SceneObject` | `SimObject` | `eulerrotation`, `forwardVector`, `objectBox`, `position`, `renderposition`, `rightVector`, `rotation`, `scale`, `scaledobjectbox`, `transform`, `upVector`, `worldBox`, `worldBoxCenter`, `light`, and `get…`/`set…` for the forward, right and up vectors, position, scale and transform, with `getObjectBox`, `getWorldBox`, `getWorldBoxCenter` (29 names) | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| `GameObject` properties | `SceneObject` | `alpha`, `attachedtoobject`, `attrobjects`, `collision`, `iseditorobject`, `liquidheight`, `liquidtype`, `movetype`, `nickcolor`, `nickname`, `position`, `scaledshapebox`, `shadow`, `shape`, `shapebox`, `showterrain`, `solid`, `transform`, `velocity`, `watercoverage` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| `GameObject` functions | `SceneObject` | `checkCollision`, `checkCollisionByBox`, `clipPolygons`, `findimg`, `getControllingClient`, `getControllingObject`, `getdropz`, `getInteriorObject`, `getMountedObject`, `getMountedObjectCount`, `getMountedObjectNode`, `getMountNodeObject`, `getMountTransform`, `getMountPosition`, `getNodeTransform`, `getNodePosition`, `getObjectMount`, `hideimg`, `hideimgs`, `isDrawn`, `isInInterior`, `isMounted`, `mountObject`, `setDirection`, `unmount`, `unmountObject` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| `TerrainBlock` | `SceneObject` | `terrainFile`, `squareSize`, `repeatTerrain` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| `WaterBlock` | `SceneObject` | `ignoreterrain`, `useDepthMask`, the surface, shore, environment-map, submerge and specular-mask textures, `liquidType`, `density`, `viscosity`, `waveMagnitude`, `surfaceOpacity`, `envMapIntensity`, tessellation, parallax, flow, distortion, shore depth, depth gradient, `minAlpha`, `maxAlpha`, `removeWetEdges`, `specularColor`, `specularPower` (30 names) | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| `fxSunLight` | `SceneObject` | 52 names: `enable`, flare bitmaps and size, `sunazimuth`, `sunelevation`, colour and brightness, and animation (`anim…`), interpolation (`lerp…`), range (`min…`/`max…`), key (`…keys`) and time (`…time`) settings for colour, brightness, rotation, size, azimuth and elevation, then `reset` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| `DynamicShapeReplicator` | `GameObject` | `allowedterrainslope`, `allowonterrain`, `allowoninteriors`, `allowonstatics`, `allowonwater`, `allowwatersurface`, `aligntoterrain`, `boxmin`, `boxmax`, `hidereplications`, `mingridobjects`, `maxgridobjects`, `offsetz`, `radius`, `shapefiles`, `shaperotatemin`, `shaperotatemax`, `shapescalemin`, `shapescalemax`, `surfaceexclusionmode`, `surfacetype`, `terrainalignment`; `DynamicGrass` and `DynamicGrassReplicator` add none | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| `Terraformer` | `TGraalVar` | `loadGrayscale`, `loadGreyscale`, `saveGreyscale`, `setTerrain` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| `TerrainEditor` | `GuiControl` | the stock brush, selection, height, smoothing, material and action set (45 names, among them `setHeightVal`, `adjustHeightVal`, `smoothFactor`, `paintMaterial`, `attachTerrain`, `getTerrainMaterials`, `setTerrainMaterials`, `mirrorTerrain`, `processAction`) | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| `WorldEditor` | `GuiControl` | the stock selection, gizmo, grid, snap, undo and drawing set (64 names, among them `selectObject`, `dropSelection`, `deleteSelection`, `setMode`, `addUndoState`, `syncSelection`, `reloadSelection`) | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| `SimGroup` | `SimObject` | `addcontrol` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| `ActionMap` | `TGraalVar` | `getBinding`, `getCommand`, `unbind` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| `GuiPlayerView` | `GuiControl` | `ambientcolor`, `cameraz`, `lightcolor`, `lightdirection`, `modelrotx`, `modelrotz`, `shape`, `shapeobject` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| `GuiShapeNameHud` | `GuiControl` | `alignBottom`, `chatprofile`, `damageAlignBottom`, `damageOffset`, `damageTimeout`, `verticalDamageOffset`, `useShapeSize`, `fillColor`, `frameColor`, `maxDistance`, `showFill`, `showFrame`, `verticalOffset`, `distanceFade` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| `GuiMapOverviewCtrl` | `GuiBitmapCtrl` | `mapalpha`, `pointsize` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| `SimObject`, `EditManager`, `GuiGraal3DCtrl`, `GuiInputCtrl` | as registered | none of their own | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |

What a script can do with them:

| Rule | Source |
| --- | --- |
| `GameObject` carries the calls a script needs to drive an object: mounting, node transforms, `setDirection`, `getdropz` and the two collision checks | [bin][inf] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| Live on 5.12, a static scenery `GameObject` accepts skin, chat, `attr1` to `attr3` and nickname but draws none of them, and a `.ft` text shape never drew; only flag `0x0004` hides an object (→ §10.5.2, §10.6) | [lab][cap] (torque/live-512-gameobject-fields-2026-11-25.md#fields-accepted-but-not-drawn-on-a-static-gameobject); [lab][cap] (torque/live-512-shapes-2026-11-25.md#ft-text-shapes-t3d-036) |
| `findimg`, `hideimg` and `hideimgs` on `GameObject` mean 2D-style show-images work on 3D objects (→ §8.3.8) | [bin][inf] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| The client carries a scriptable 3D world and terrain editor: `WorldEditor`, `TerrainEditor` and `EditManager` are registered GUI controls with their full stock sets | [bin][inf] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512) |
| The shape subclasses (`GameShapeDTS` animation calls, `GameShapeDIF` lights, `GameShape` shaders) and how each `GameObject` property travels on the wire are in → §10.5.2 | [bin] (torque/engine-and-formats.md#the-512-3d-object-model) |

## 8.5.5 Properties and functions in 4.04r2

Read the same way from the 4.04r2 plug-in; `Player` registers the same list as `AIPlayer`. A name equal to a class name is a field that holds an object of that class [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-404r2). The table keeps the classes a game script would touch; the editors match 5.12 except that `WorldEditor` has 62 names (no `nameMaxDistance`, `nameDistanceFade`) and `GuiShapeNameHud` has no `maxDistance`.

| Class | Names | Source |
| --- | --- | --- |
| `AIPlayer` (and `Player`) | `clearAim`, `setMoveSpeed`, `setMoveDestination`, `getMoveDestination`, `setAimLocation`, `getAimLocation`, `setAimObject`, `getAimObject`, `isMoving`, `maxTurnPitch`, `maxTurnYaw`, `simpleMovement`, `wallcheck` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-404r2) |
| `PlayerData` | 24 fields: decal, footstep and dust emitters, splash, footstep and impact sounds per surface, water entry and breathing sounds, `JumpingSound`, `AudioProfile` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-404r2) |
| `ProjectileData` | `lightRadius`, `velInheritFactor`, `muzzleVelocity`, `lifetime`, `armingDelay`, `fadeDelay`, `bounceElasticity`, `bounceFriction`, `gravityMod`, `ParticleEmitterData`, `ExplosionData` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-404r2) |
| `Projectile` | `ProjectileData`, `initialPosition`, `initialVelocity`, `sourceObject` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-404r2) |
| `WheeledVehicle` | `WheeledVehicleData`, `getWheelCount`, `setWheelPowered`, `setWheelSpring`, `setWheelSteering`, `setWheelTire` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-404r2) |
| `Precipitation` | `maxspeed`, `minspeed`, `maxmass`, `minmass`, `percentage`, `modifyStorm` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-404r2) |
| `Sky` | `materialList`, `skyfadetime`, `windVelocity`, `getWindowVelocity`, `stormClouds`, `stormFog`, `realFog`, `stormCloudsShow`, `stormFogShow` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-404r2) |
| `TerrainBlock` | `detailTexture`, `terrainFile`, `squareSize`, `bumpTexture`, `bumpScale`, `bumpOffset`, `zeroBumpScale` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-404r2) |
| `WaterBlock` | 28 names: 5.12's set without `ignoreterrain` and the two submerge textures, with `AudioEnvironment` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-404r2) |
| `InteriorInstance` | `interiorFile`, `showTerrainInside`, `AudioProfile`, `AudioEnvironment` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-404r2) |
| `GuiPlayerView` | `ambientcolor`, `cameraz`, `lightcolor`, `lightdirection`, `modelrotx`, `modelrotz`, `mountShape`, `setModel`, `unmountShape` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-404r2) |
| `DynamicShapeReplicator` | `boxmin`, `boxmax`, `mingridobjects`, `maxgridobjects`, `radius`, `shapefiles`, `surfacetype` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-404r2) |
| `SimObject` | `isdatablock` | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-404r2) |
| camera functions | `setCameraPosition`, `getCameraPosition`, `setCameraFov`, `getCameraFov`, `setControlCameraFov`, `getControlCameraFov`, `shakeCamera` | [bin] (torque/3d-formats-renderer-camera-by-build.md#camera-classes-t3d-055) |

So a 4.04r2 script can tune only a few fields of each datablock (a `PlayerData`'s sounds and emitters, a `ProjectileData`'s speed, life and bounce) and steer a `Player` or `AIPlayer` with the stock AI calls; the rest of each datablock keeps its native defaults [bin][inf] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-404r2).

## 8.5.6 Global 3D functions (5.12)

The 5.12 engine registers 262 GS2 global functions; these act on the 3D side [bin] (torque/gs2-3d-objects-404r2-512.md#global-3d-functions-512). Their argument lists were not read.

| Group | Functions | Source |
| --- | --- | --- |
| entering 3D | `switchToOpenGL`: calls the launcher's start-3D callback with an empty server name and port 0 (→ §8.5.10) | [bin] (torque/gs2-3d-objects-404r2-512.md#global-3d-functions-512) |
| lighting, sky and fog | `lightScene`, `syncTimeOfDay`, `setSunColors`, `setSkyBandColors`, `setSkyBandSizes`, `setFogColors`, `updateVisibleDistance`, `setInteriorRenderMode` | [bin] (torque/gs2-3d-objects-404r2-512.md#global-3d-functions-512) |
| terrain | `getz`, `getdropz`, `update3DTerrain`, `updateterrain`, `getTerrainTexture`, `getTerrainTextureIndex`, `setTerrainRenderMode`, `addMaterialMapping` | [bin] (torque/gs2-3d-objects-404r2-512.md#global-3d-functions-512) |
| picking and screen | `get3DScreenPosition`, `get3DObjectByRay`, `worldx`, `worldy`, `screenx`, `screeny` | [bin] (torque/gs2-3d-objects-404r2-512.md#global-3d-functions-512) |
| sound | `play3D` | [bin] (torque/gs2-3d-objects-404r2-512.md#global-3d-functions-512) |
| player and objects | `attachplayertoobj`, `detachplayer` | [bin] (torque/gs2-3d-objects-404r2-512.md#global-3d-functions-512) |
| vectors | `getanglesfromvector`, `getvectorfromangles`, `vectoradd`, `vectorsub`, `vectorscale`, `vectornormalize`, `vectordot`, `vectorcross`, `vectordist`, `vectorlen`, `vectororthobasis` | [bin] (torque/gs2-3d-objects-404r2-512.md#global-3d-functions-512) |
| rotations and matrices | `rotationadd`, `rotationsub`, `rotationaddeuler`, `rotationtoeuler`, `rotationfromeuler`, `matrixcreate`, `matrixcreatefromeuler`, `matrixmultiply`, `matrixmulvector`, `matrixmulpoint` | [bin] (torque/gs2-3d-objects-404r2-512.md#global-3d-functions-512) |
| boxes and angles | `getBoxCenter`, `boxscale`, `boxcontainsvector`, `boxcontains`, `boxoverlaps`, `boxintersect`, `degtorad`, `radtodeg` | [bin] (torque/gs2-3d-objects-404r2-512.md#global-3d-functions-512) |
| mode test | `isgraal3d` reads true in 3D; `isGraal3DMode` does not exist in 5.12 | [lab] (torque/live-512-gs2-3d-probe-2026-11-25.md#entering-3d-and-events-t3d-021) |

## 8.5.7 3D events and login steps

Among the GS2 event names the 5.12 engine dispatches, these belong to the 3D side: `onGraal3DConnectionEstablished`, `onGraal3DLoginStep`, `onGhostAlwaysStarted`, `onGhostAlwaysObjectReceived`, `onCollision`, `onImpact`, `onEnterLiquid`, `onLeaveLiquid`, `onMount`, `onUnmount` and `onMouseYawPitch`; `onRPGMessage` and `onRCChat` come from the text channel [bin] (torque/gs2-3d-objects-404r2-512.md#3d-event-names-512). Which object receives each, and with what parameters, was not read (→ §8.5.13). Which engine images hold each name as a literal is in → §8.3.11.

Neither 4.04r2 nor 5.12 has TorqueScript, so the mission-phase handlers are native. At each step the client logs a line and fires `onGraal3DLoginStep` with an integer; the value starts at −1 [bin] (torque/gs2-3d-objects-404r2-512.md#mission-phases-and-ongraal3dloginstep-404r2-512). The table gives what raises each step.

| Step | 4.04r2 | 5.12 | Source |
| ---: | --- | --- | --- |
| 1 | `MissionStartPhase1`, "Phase 1: Download Datablocks" | n/a | [bin] (torque/gs2-3d-objects-404r2-512.md#mission-phases-and-ongraal3dloginstep-404r2-512) |
| 2 | `MissionStartPhase2`, "Phase 2: Download Ghost Objects" | `MissionStartPhase1`, "Phase 1: Download Ghost Objects" | [bin] (torque/gs2-3d-objects-404r2-512.md#mission-phases-and-ongraal3dloginstep-404r2-512) |
| 3 | `MissionStartPhase3`, "Phase 3: Mission Lighting"; lighting starts | `MissionStartPhase2`, "Phase 2: Mission Lighting"; lighting starts | [bin] (torque/gs2-3d-objects-404r2-512.md#mission-phases-and-ongraal3dloginstep-404r2-512) |
| 4 | lighting done; the client sends `MissionStartPhase3Ack` | lighting done; the client sends `MissionStartPhase2Ack` | [bin] (torque/gs2-3d-objects-404r2-512.md#mission-phases-and-ongraal3dloginstep-404r2-512) |
| 5 | the first control object arrives | the same | [bin] (torque/gs2-3d-objects-404r2-512.md#mission-phases-and-ongraal3dloginstep-404r2-512) |
| 6 | n/a | right after step 5, the client adds `GraalControl3D` to the GUI and the 3D view appears | [bin] (torque/gs2-3d-objects-404r2-512.md#mission-phases-and-ongraal3dloginstep-404r2-512) |

The rules below give how the steps behave [bin] (torque/gs2-3d-objects-404r2-512.md#mission-phases-and-ongraal3dloginstep-404r2-512).

| Rule | Source |
| --- | --- |
| 5.12 dropped the datablock phase and renumbered the other two but kept the step numbers, so a 5.12 script never sees step 1 | [bin] (torque/gs2-3d-objects-404r2-512.md#mission-phases-and-ongraal3dloginstep-404r2-512) |
| A server that sends no phase commands skips steps 2 to 4; the client goes straight to 5 and 6 when the first control object arrives, and lighting runs only when the lighting phase is sent | [bin] (torque/gs2-3d-objects-404r2-512.md#mission-phases-and-ongraal3dloginstep-404r2-512) |
| Live on 5.12, a weapon received `onGraal3DLoginStep` with steps 4, 5 and 6 | [lab] (torque/live-512-gs2-3d-probe-2026-11-25.md#entering-3d-and-events-t3d-021) |
| Live on 4.04r2 (all three phases), a probe weapon received `onGraal3DLoginStep` 2, 4 and 5, and `onGhostAlwaysStarted` 2 | [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#404r2) |
| The `on…` events fired for each 3D connection outcome (`onConnectionAccepted` and the rest) are listed in → §8.3.5 | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |

## 8.5.8 Terrain and water from script

Torque ships two terrain tools as engine classes, the procedural `Terraformer` and the brush editor `TerrainEditor`. Both survive in all three builds read, cut down differently [bin] (torque/script-and-terrain-tools-by-build.md#the-terrain-tools-inside-the-client).

| Item | 3.153 | 4.04r2 | 5.12 | Source |
| --- | --- | --- | --- | --- |
| `Terraformer` generator operations (`rigidMultiFractal`, `turbulence`, `erodeHydraulic`, `erodeThermal`, `smoothRidges`, `generateSeed`, `previewScaled`, `terrainData`) | present | absent | absent | [bin] (torque/script-and-terrain-tools-by-build.md#the-terrain-tools-inside-the-client) |
| `Terraformer` functions kept | full stock set | `loadGrayscale`, `loadGreyscale`, `saveGreyscale`, `setTerrain` | the same four | [bin] (torque/script-and-terrain-tools-by-build.md#the-terrain-tools-inside-the-client) |
| how `Terraformer` is exposed | TorqueScript console class | a Graal script object | a subclass of Graal's script variable object | [bin] (torque/script-and-terrain-tools-by-build.md#the-terrain-tools-inside-the-client) |
| `TerrainEditor` | stock | stock set, as script properties | the same set, as a GUI control | [bin] (torque/script-and-terrain-tools-by-build.md#the-terrain-tools-inside-the-client) |
| local `.ter` load message | present | present | absent | [bin] (torque/script-and-terrain-tools-by-build.md#the-terrain-tools-inside-the-client) |
| chunk load message ("Loading terrain from terrain chunks.") | present | present | present | [bin] (torque/script-and-terrain-tools-by-build.md#the-terrain-tools-inside-the-client) |

The rules below give what a script can do with terrain, with the live results so far [bin][lab] (torque/live-512-gs2-3d-probe-2026-11-25.md#terrain-t3d-019-t3d-050).

| Rule | Source |
| --- | --- |
| The 4.x and 5.x clients cannot generate terrain procedurally; they keep import, export and apply: read a greyscale image as heights, save heights as an image, and apply the result to a `TerrainBlock` | [bin][inf] (torque/script-and-terrain-tools-by-build.md#the-terrain-tools-inside-the-client) |
| `Terraformer.setTerrain` returns false and does nothing unless a streamed `TerrainBlock` is the client's current terrain; otherwise it copies the 256 × 256 register into its heights with the rows flipped (register row 255 becomes terrain row 0), rebuilds the grid, relights it with a fixed light (direction 0.5, 0.5, −0.5; ambient 0.35; colour 0.8) and returns true | [bin] (torque/terrain-512.md#7-script-access-terraformersetterrain) |
| Live on 5.12, a GS2 weapon creates a `Terraformer` with `new`; `setTerrain` returned 0 with no `TerrainBlock` and 1 with one, the chunk cache files were byte-identical before and after, and the stamps on the next connect were unchanged, so it changes the live view only | [lab] (torque/terrain-512.md#7-script-access-terraformersetterrain) |
| `loadGreyscale(register, file)` reads the image as at least three bytes per pixel, turns each pixel into a 0–1 value with luminance weights (0.299 R, 0.587 G, 0.114 B, over 256) and reads the image bottom row first, so with `setTerrain`'s own flip image row r lands on terrain row r; it does not check the image's depth or size | [bin] (torque/terrain-512.md#7-script-access-terraformersetterrain) |
| `loadGreyscale` resolves the name through the client's own file system and asks the server for the file over TCP when it is not cached; it returns 0 until the file has arrived | [lab] (torque/terrain-512.md#7-script-access-terraformersetterrain) |
| 32-bit RGBA PNGs of 64 × 64 and 128 × 128 load; 256 × 256 RGBA returned 1 once but crashed in other runs, including on the first call once the file was cached, with and without a `TerrainBlock`, so the block is not the factor; 512 × 512 and 256 × 128 RGBA crashed; 24-bit RGB and 8-bit grey PNGs crash at once. The safe use is a 64 or 128 square RGBA image; nothing at 256 or above is reliable | [lab] (torque/terrain-512.md#7-script-access-terraformersetterrain) |
| In 3D mode `getz(x, y)` casts a ray straight down from z = 2000 to z = −2000 against terrain objects and returns the hit height, or 0 on no hit; in 2D mode it returns the level's board height | [bin][inf] (torque/gs2-3d-objects-404r2-512.md#getz-in-3d-mode-512) |
| Live on 5.12, `getz` returned 0 everywhere in a world with no terrain | [lab] (torque/live-512-gs2-3d-probe-2026-11-25.md#terrain-t3d-019-t3d-050) |
| The client does not clamp a script-moved `GameObject` to the terrain: its z stays as set while `getdropz(x, y, 500)` reports the ground below; every `getdropz` value over the terrain was a multiple of 1/8, and `player.getdropz()` returned 0 | [lab] (torque/terrain-512.md#7-script-access-terraformersetterrain) |
| In 4.04r2 a script's `new TerrainBlock(...)` is created and `terrainFile` reads back as set, but the block loads no terrain by either path; only a ghosted block does | [lab] (torque/terrain-512.md#8-older-builds-the-ter-file-path) |
| The 4.04r2 `.ter` file path is taken only for a block whose `terrainFile` names a `.ter` that loads, which the network update never sets, so it is reachable only from a script-made block and was not reached live; 5.12 keeps the property name but only streams | [bin][inf] (torque/terrain-512.md#8-older-builds-the-ter-file-path) |
| No path from a 2D level's `HEIGHTS` block into a `TerrainBlock` was seen; the 2001–2003 `TerrainGenerator` writes 2D gmaps and levels, not Torque terrain | [bin][inf] (torque/script-and-terrain-tools-by-build.md#the-original-terraingenerator-is-a-different-tool) |
| The terrain and water wire layouts are in → §10.5.4 and → §10.5.5 | [bin] (graal3d/torque-engine-4x.md#terrain-streaming-graal) |

**The streamed terrain a script reads (5.12).** In 5.12 the terrain never comes from a `.ter` file: the server ghosts a `TerrainBlock` that carries only settings and then streams heights, materials and holes as 256 chunks of 16 × 16 squares, which the client caches per server [bin] (torque/terrain-512.md#graal-512-streamed-terrain-terrainblock-chunk-events-and-the-heights-cache). The rules give what a script sees of it; the chunk layout, stamp rule and cache files are in → §10.5.4.

| Rule | Source |
| --- | --- |
| The grid is 256 × 256 squares; its corner is at (−128 × square size, −128 × square size, 0), so it is centred on the origin; chunk (0, 0) is the −x, −y corner and chunk rows grow toward +y | [bin][lab] (torque/terrain-512.md#1-the-terrainblock-ghost) |
| The square size (metres per square, usually 8) and a repeat switch come from the `TerrainBlock` update; the script names `squareSize` and `repeatTerrain` are in §8.5.4 | [bin] (torque/terrain-512.md#1-the-terrainblock-ghost) |
| One world unit is 8 wire height units: a flat chunk sent at 3200 reports `getdropz` 400 at square size 8 and 2 alike | [lab] (torque/terrain-512.md#chunk-data-inflated) |
| `getdropz` blends the last square before +128 × square size toward the opposite edge's first vertex, and returns 0 at or beyond +128 × square size and below −128 × square size when repeat is off | [lab] (torque/terrain-512.md#lab-results) |
| When the block is added the client logs "Loading terrain from terrain chunks.", loads the material list `heights.info` and the cached chunk files from `levels3d/heights/<server>/` (a space in the server name is written `%032`), and sends one request with the stamp of every chunk | [bin][lab] (torque/terrain-512.md#1-the-terrainblock-ghost); [bin][lab] (torque/terrain-512.md#4-the-cache-folder) |
| A chunk that arrives before the `TerrainBlock` is added is logged but not stored; a corrupt zlib stream is applied as flat ground and cached that way; no chunk case crashed the client | [bin][lab] (torque/terrain-512.md#2-terrainchunkevent-server--client) |
| Each terrain texture named in `heights.info` (one name per line, up to 32) must be 256 × 256 at 24 bits, or the client logs "Terrain texture of bad format" and uses `default`; a missing one logs "Missing terrain texture" | [bin][lab] (torque/terrain-512.md#4-the-cache-folder) |
| Texture fetching is one visit late: on the first visit the client fetches only `heights.info`; on the second it logs "Missing terrain texture" for each name, then downloads each and saves it under exactly the listed name; extensionless cached textures failed to load on later visits in another lab, so list names with their extension | [lab] (torque/terrain-512.md#4-the-cache-folder) |
| In a later 5.12 run the terrain drew white with the texture names given both bare and with `.png`, and the client never requested the textures; why this differs from the one-visit-late run is open | [lab] (torque/live-512-gs2-3d-probe-2026-11-25.md#terrain-textures-t3d-044-follow-up) |
| 3.153 also uses the chunked terrain: a `TerrainBlock` makes it send the stamp request and ask for `heights.info` | [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#3153) |
| The `setmaterials` text message changes the list during play; its names are separated by commas, not newlines, and the client saves the list to the cache `heights.info` as 32 CRLF lines and reloads it on the next connect | [lab] (torque/terrain-512.md#4-the-cache-folder) |
| 4.20r8 logs the chunk line, requests chunks and saves the first ones byte for byte as 5.12 does; it crashed in runs that also had `GameObject`s at ground level and a low spawn, and ran 110 s without a crash with no objects and a high spawn; a `WaterBlock` alone is fine. So the crash needs an object near the terrain surface; collision versus shadow is not yet separated | [lab] (torque/terrain-512.md#lab-results) |

**Water.** A `WaterBlock` is a ghosted object; its script names per build are in §8.5.4 and §8.5.5 [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-512). The rules give what a live 5.12 client does with it.

| Rule | Source |
| --- | --- |
| Every update carries the whole block: name, position and rotation, scale, five textures and two submerge textures, liquid type, five physics and look floats, two switches, twelve shading floats, specular colour and power, and an ignore-terrain switch | [bin] (torque/terrain-512.md#5-waterblock-read-beside-the-terrain) |
| The client takes the scale only when its x and y are both at least 1024; a block of scale 512 drew nothing, 1024 and 4096 were created | [bin][lab] (torque/terrain-512.md#5-waterblock-read-beside-the-terrain); [lab] (torque/terrain-512.md#lab-results) |
| The surface texture is fetched over TCP and a large surface is drawn; liquid types 0 to 7 were all accepted (stock Torque names them water, ocean, river, stagnant, lava, hot lava, crusty lava, quicksand) | [lab][inf] (torque/terrain-512.md#lab-results); [inf] (torque/terrain-512.md#5-waterblock-read-beside-the-terrain) |

## 8.5.9 Sky, lighting, camera and shaders from script

The rules give what a 5.12 script can change in how the world is drawn, and what the live runs showed [bin][lab] (torque/3d-formats-renderer-camera-by-build.md#camera-classes-t3d-055).

| Rule | Source |
| --- | --- |
| Live on 5.12, none of `setSkyBandColors`, `setSkyBandSizes`, `setFogColors`, `setSunColors`, `lightScene`, `updateVisibleDistance`, `syncTimeOfDay` or `setInteriorRenderMode` changed a pixel; the ghosted `Sky` and `Sun` stayed as they were while a script camera move redrew at once | [lab] (torque/live-512-gs2-3d-probe-2026-11-25.md#sky-fog-sun-and-view-distance-functions-t3d-063) |
| Why: in the 5.00r7 engine, `setSunColors`, `setSkyBandColors`, `setFogColors` and `setSkyBandSizes` each take one list and fill a client-side day and night keyframe table; they do not touch the ghosted `Sky` or `Sun` | [bin] (torque/3d-engine-static-reads-2026-11-25.md#sky-fog-and-view-functions-t3d-063) |
| `syncTimeOfDay` takes two numbers; `updateVisibleDistance` takes no argument and re-reads `$pref::Video::visibleDistance`; there is no `updateFogDistance`; `lightScene` does a full relight | [bin] (torque/3d-engine-static-reads-2026-11-25.md#sky-fog-and-view-functions-t3d-063) |
| Lighting is not a script tool on 5.12: the ghosted `Sun` only switches shapes to full brightness and shades nothing by direction or colour (→ §10.5.6) | [lab][cap] (torque/live-512-lighting-and-sky-2026-11-25.md#lighting-on-3ds-shapes-t3d-047-t3d-052) |
| A script that sets a rotation should expect a positive angle about +z to turn a shape clockwise seen from above; the default horizontal field of view is 90 degrees (→ §10.5.6) | [lab] (torque/live-512-lighting-and-sky-2026-11-25.md#shape-rotation); [lab] (torque/live-512-lighting-and-sky-2026-11-25.md#sky-geometry-and-field-of-view-t3d-046-t3d-055) |
| `GuiShapeNameHud` has `nameMaxDistance` and `nameDistanceFade` and reads the `GameObject` fields `nickname`, `nickcolor`, `movetype` and `liquidtype` | [bin] (torque/3d-engine-static-reads-2026-11-25.md#name-tags-t3d-065) |
| 5.12 gives GS2 no camera functions and no camera properties; the only camera-named property is `cameraz` on the `GuiPlayerView` preview widget, and there is no first-person toggle name; the 3D camera is driven only by the server through the `Camera` ghost when it is the control object | [bin] (torque/3d-formats-renderer-camera-by-build.md#camera-classes-t3d-055) |
| `PathCamera` and `AdvancedCamera` are 4.04r2 only; 5.12 keeps `Camera` | [bin] (torque/3d-formats-renderer-camera-by-build.md#camera-classes-t3d-055) |
| 5.12's `GameShape` has `vertexshader` and `pixelshader`; the value is GLSL source text, which the client compiles and links, writing "Compilation of …: failed" or "…: successful" and the driver log to the `graphics` log category; each draw sets `camPos`, `tex` and `tex2`; 4.04r2 has neither property and no shader calls | [bin] (torque/3d-formats-renderer-camera-by-build.md#gameshape-shaders-in-512-t3d-039) |
| Live on 5.12, both shader strings were stored and read back exactly, no file was requested, and neither arrives from the server: only client script sets them; on a driver with no GLSL nothing compiled and the picture did not change | [lab] (torque/3d-formats-renderer-camera-by-build.md#gameshape-shaders-in-512-t3d-039) |
| Live on 5.12 with a GLSL-capable driver (Mesa llvmpipe), GLSL source in `pixelshader` and `vertexshader` works: a test fragment shader drew a shape solid magenta; a file name in either field does nothing; no compile log text was found in any log file. So a client script can replace the material of any shape it can reach with its own shader | [lab] (torque/3d-formats-renderer-camera-by-build.md#gameshape-shaders-in-512-t3d-039) |
| 5.12 keeps eight `$pref::Video::` names (`resolution`, `fullScreenMode`, `windowMode`, `detailFactor`, `fogDistance`, `visibleDistance`, `screenShotFormat`, `defaultguistyle`) and no `$pref::OpenGL::` names; 4.04r2 keeps the full stock set | [bin] (torque/3d-formats-renderer-camera-by-build.md#renderer-and-video-settings-t3d-051) |

## 8.5.10 What a script can build without the server

A client cannot build a 3D world by itself. The rules give the live 5.12 results [lab] (torque/live-512-gs2-3d-probe-2026-11-25.md#local-3d-with-no-server-t3d-064).

| Rule | Source |
| --- | --- |
| A script-made `GameObject` is created and the client fetches its shape, but the object never draws | [lab] (torque/live-512-gs2-3d-probe-2026-11-25.md#objects-a-script-makes-t3d-016) |
| Script-made `Sky`, `Sun` and `WorldEditor` objects show nothing; only ghosted objects from the server drew | [lab] (torque/live-512-gs2-3d-probe-2026-11-25.md#objects-a-script-makes-t3d-016) |
| `switchToOpenGL` on a 2D server starts the 3D engine and opens its OpenGL window, and the 2D HUD disappears, but the client connects nowhere, has no camera and draws no 3D view; locally made objects do not draw | [lab] (torque/live-512-gs2-3d-probe-2026-11-25.md#local-3d-with-no-server-t3d-064) |

## 8.5.11 Session and content rules a 3D script runs under

A 3D script runs inside a session that the server list and the 3D server set up. The rules a script author or server writer meets first are below; the wire itself is in → §10.2 and → §10.3.

| Rule | Source |
| --- | --- |
| A server-list entry is a 3D server when its listed name starts with exactly `3 `; if a name's second character is a space, the first two characters are dropped from the stored name, whatever the first one is | [bin] (torque/3d-server-entry-and-udp-port.md#picking-a-server-from-the-list-t3d-059) |
| Picked in 2D mode, a 3D entry makes the client ask its host to start the 3D engine, and the pick is replayed; in 3D mode the client connects to the host on the listed port + 1 for UDP | [bin] (torque/3d-server-entry-and-udp-port.md#picking-a-server-from-the-list-t3d-059) |
| The 3D UDP port is always the listed port + 1, and nothing the server sends changes it; only the client's own UDP port can be set (`fixedport`, `fixedudpport` default 14899, `noudp`), and with `fixedport` off the operating system picks it | [bin] (torque/3d-server-entry-and-udp-port.md#udp-ports-t3d-028) |
| A 5.12 weapon file saved with CRLF line ends is not compiled, so the client runs nothing from it; weapon scripts must be served with LF line ends | [lab] (torque/live-512-gs2-3d-probe-2026-11-25.md#entering-3d-and-events-t3d-021) |
| 5.12 caches each 3D weapon's compiled script as `weblevels/weapons/<server>/<weapon>.code` | [lab] (torque/3d-formats-renderer-camera-by-build.md#gameshape-shaders-in-512-t3d-039) |
| 5.12 drops any image extension (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`, `.tga`, `.dds`) from material and sky texture names, lower-cases the name and requests the bare name; shape names keep their extension; after "not found" it does not ask again | [lab][cap] (torque/live-512-own-server-textures-2026-11-25.md#texture-names-t3d-033-final) |
| A bare texture name with an underscore is stored in a subfolder named after the part before the first underscore; others go to `images/` | [lab][cap] (torque/live-512-own-server-textures-2026-11-25.md#texture-names-t3d-033-final) |
| 5.12 decodes a texture by content: 8-bit PNG (RGB, RGBA, paletted, grey, interlaced), JPEG and GIF draw; 16-bit PNG, BMP, TGA and DDS draw white, as does a missing texture; alpha 0 is cut out and alpha 128 draws opaque | [lab][cap] (torque/live-512-own-server-textures-2026-11-25.md#texture-formats-t3d-032) |
| Whatever the control object's class, the 5.12 client sends its position plus an update in the `GameObject` layout: a `Camera` sends the transform once and then an empty update each second; a `GameObject` sends shape, transform and flags | [lab][cap] (torque/live-512-own-server-textures-2026-11-25.md#what-the-client-sends-for-its-control-object-t3d-023) |
| With `levels3d/` deleted but `FILENAMECACHE.txt` kept, 5.12 requests no meshes and then crashes; this is a client cache state a server cannot cause | [lab] (torque/live-512-own-server-textures-2026-11-25.md#client-fault) |
| Live on 4.04r2 the control object is the stock TGE `Player`; the client sends Torque moves only, no position reports; the server walked the Player while keys were held, but the script `player` object still read the spawn position, so the 2D player position does not follow the 3D Player | [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#404r2) |
| First multi-client runs on the project's early lab server (its relay of other players was still changing, so these describe that build, not settled client rules): a 5.12 3D client received a 2D client's chat as `onRemotePlayerChats` over TCP while its `players` count stayed 0; a 2D 5.24r3 client counted the 3D player but drew nothing; no leave event reached either side (→ §10.3.11) | [lab] (torque/multi-client-3d-lab-2026-11-25.md#h1-a-2d-client-and-a-3d-client-in-one-level) |
| A `RemoteCommandEvent` one bit shorter than its declared length made 5.12 run a garbled remote command and then crash, so a server's event lengths must be exact; 4.04r2 crashes on an update to a ghost index it never created (→ §10.3.12) | [lab][cap] (torque/3d-fuzz-net-tier1-2026-11-25.md#crashes-and-bad-behaviour) |
| 3.153 asks for `.dts` shapes and textures by bare name and for sky textures as `.gif`, never `.png` | [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#3153) |
| 5.12 asks the TCP connection for any missing 3D resource except `.dso`, `.cs` and `.ter` | [bin] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files) |

The 3D file formats and the builds that read them are in → §10.6.

## 8.5.12 What each build's 3D script can do

The table puts the chapter together by build. A cell says `unmeasured` where no note read that build for the item (→ §0.4).

| Item | 3.153 | 4.04r2 | 4.20r6 / 4.20r8 | 5.12 | 5.24r3 and later | Source |
| --- | --- | --- | --- | --- | --- | --- |
| script language on the 3D side | TorqueScript (shipped) | GS2 | GS2 | GS2 | n/a: no Torque 3D | [bin] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files); [bin] (torque/engine-and-formats.md#which-torque) |
| object model a script drives | stock TGE game layer | stock TGE game layer with datablocks, 86 GS2 classes | `GameObject` layer | `GameObject` layer, 22 3D GS2 classes | n/a | [bin] (torque/gs2-3d-objects-404r2-512.md#404r2-86-registrations-in-the-3d-plug-in); [bin] (torque/wire-by-build.md#the-networked-class-sets) |
| GS2 3D class and name lists | n/a | read | unmeasured | read | n/a | [bin] (torque/gs2-3d-objects-404r2-512.md#script-properties-and-functions-in-404r2) |
| login-step events | `clientCmdMissionStartPhase1`–`3` in script | steps 1 to 5 | unmeasured | steps 2 to 6 | n/a | [file] (torque/script-and-terrain-tools-by-build.md#does-the-client-take-and-run-torque-files); [bin] (torque/gs2-3d-objects-404r2-512.md#mission-phases-and-ongraal3dloginstep-404r2-512) |
| camera from script | unmeasured | seven camera functions, `PathCamera`, `AdvancedCamera` | unmeasured | none; server `Camera` ghost only | n/a | [bin] (torque/3d-formats-renderer-camera-by-build.md#camera-classes-t3d-055) |
| procedural terrain | full `Terraformer` | import, export and apply only | unmeasured | import, export and apply only | n/a | [bin] (torque/script-and-terrain-tools-by-build.md#the-terrain-tools-inside-the-client) |
| terrain source | streamed chunks seen live (`.ter` path in the binary) | ghosted block streams chunks; `.ter` only for a script-made block (not reached live) | 4.20r8 streams, and crashes with objects near the terrain surface | streamed chunks only | n/a | [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#3153); [bin][lab] (torque/terrain-512.md#8-older-builds-the-ter-file-path); [lab] (torque/terrain-512.md#lab-results) |
| GLSL shaders on shapes | unmeasured | no | unmeasured | yes, compile needs a GLSL driver | n/a | [bin] (torque/3d-formats-renderer-camera-by-build.md#gameshape-shaders-in-512-t3d-039) |
| live-run evidence | protocol 19 session: three stock phases, a `Player` control object, nothing 3D drawn; crashes without a `Sky` | marker-file session; a probe session under Wine with all three phases (only the sky gradient drew) | 4.20r8 terrain runs | GS2 probe, textures, terrain tools, GLSL shaders | n/a | [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#3153); [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#404r2); [lab] (protocol/lab-appe-hostb-2026-11-20c.md#mis-and-dso-beside-the-404r2-client-e502-e503); [lab] (torque/3d-capability-board.tsv); [lab] (torque/live-512-gs2-3d-probe-2026-11-25.md) |

The network protocol number of each build, which is the reliable way to tell the 4.x object models apart, is in → §10.3.2.

## 8.5.13 Confirmed, inferred and open

Each row is one board question that bears on 3D scripting, with where it stands. "Confirmed" means a static read and a live run agree, "read" a static read only, "inferred" an inference the note marks, and "open" no answer yet [doc] (torque/3d-capability-board.md#how-the-board-is-worked).

| Question | State | Source |
| --- | --- | --- |
| Does any 4.x or 5.x client run TorqueScript it is given (T3D-006 to T3D-009) | confirmed no for 3.153 and 4.04r2 (read and lab), read no for 5.12; 3.153 runs only its shipped scripts | [bin][lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#3153) |
| Which GS2 classes and names the 3D engine adds (T3D-014) | read for 4.04r2 and 5.12; `Sky` and `Sun` names in 5.12 open | [bin] (torque/3d-capability-board.tsv) |
| Whether a client weapon can create, move and delete 3D objects locally (T3D-016) | partial: created, shape fetched, never drawn | [lab] (torque/3d-capability-board.tsv) |
| What each `GameObject` property maps to on the wire (T3D-015) | assigned; the update layout is in §10.5.2 | [bin] (torque/3d-capability-board.tsv) |
| What the BigData text actions do on a live client (T3D-017) | assigned; the static read is in §10.5.3 | [bin] (torque/3d-capability-board.tsv) |
| What reaches the 3D server on `triggerserver`, `setplayerprop`, chat and PM in 3D mode (T3D-018) | open | [doc] (torque/3d-capability-board.tsv) |
| Whether the terrain functions are callable from GS2 and what `setTerrain` writes (T3D-019, T3D-050) | confirmed callable; `setTerrain` changes the live view only; `loadGreyscale` is safe only for 64 or 128 square RGBA images, with or without a `TerrainBlock`; why larger or non-RGBA images crash is open | [bin][lab] (torque/terrain-512.md#7-script-access-terraformersetterrain) |
| Streamed terrain and its cache (T3D-040) | confirmed: layout read and a real 5.12 matched all 256 stamps on reconnect | [bin][lab] (torque/terrain-512.md#lab-results) |
| Terrain texture rules (T3D-044) | partial: 256 × 256 × 24 required (read); one run fetched textures a visit late, another drew white and never requested them; why is open | [bin][lab] (torque/terrain-512.md#lab-results); [lab] (torque/live-512-gs2-3d-probe-2026-11-25.md#terrain-textures-t3d-044-follow-up) |
| What the `WaterBlock` fields do on screen (T3D-045) | partial: created and drawn; per-field effect open | [lab] (torque/terrain-512.md#lab-results) |
| Why 4.20r8 crashes with a `TerrainBlock` and objects near its surface | partial: needs an object near the surface; collision versus shadow open | [lab] (torque/terrain-512.md#lab-results) |
| Whether a server-sent GS2 GUI can open `WorldEditor` or `TerrainEditor` (T3D-020) | read: registered; opening one live is open | [bin] (torque/3d-capability-board.tsv) |
| Which 3D events fire, on which object, with which parameters (T3D-021) | partial: login steps 4 to 6 seen on a weapon; other receivers open | [lab] (torque/3d-capability-board.tsv) |
| What the shader properties do (T3D-039) | confirmed: GLSL source replaces a shape's material on a GLSL-capable driver; where the compile log goes is open | [bin][lab] (torque/3d-formats-renderer-camera-by-build.md#gameshape-shaders-in-512-t3d-039) |
| How a 5.12 player moves in 3D (T3D-054) | answered (read): 5.12 always reports its own position and sends no Torque `Move` (→ §10.3.5); how a server moves it is in §10.3.8 | [bin] (torque/wire-by-build.md#512-game-packets-the-gameobject-era) |
| Whether the sky, fog, sun and lighting functions override the ghosted `Sky` and `Sun` (T3D-063) | answered: the functions fill a client-side keyframe table and never touch the ghosted `Sky` or `Sun` (read, 5.00r7), which fits no pixel changing live | [bin][lab] (torque/3d-engine-static-reads-2026-11-25.md#sky-fog-and-view-functions-t3d-063) |
| What the `Sun` does to shapes (T3D-047, T3D-052) | answered (live 5.12): an on/off brightness switch; no directional shading on `.3ds`, `.dts`, `.dif` or terrain | [lab][cap] (torque/live-512-lighting-and-sky-2026-11-25.md#lighting-on-3ds-shapes-t3d-047-t3d-052) |
| Whether `switchToOpenGL` can build a world with no server (T3D-064) | confirmed no | [lab] (torque/3d-capability-board.tsv) |
| The 4.20r6 and 4.20r8 GS2 3D surface | unmeasured | [bin] (torque/gs2-3d-objects-404r2-512.md#open) |
