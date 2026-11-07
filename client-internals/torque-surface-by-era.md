# Torque surface by era

Date: 2026-11-07. Tags: **[bin]** a static read of a decompile already on disk. Nothing was run.

One comparison, not a second copy of `torque/engine-304.md` or `torque/4208-engine.md`. Those notes keep the method tables and the 4.2.0.8 session. This note says, for each era, whether a Torque module is present, only a name, or absent, and whether that module is a stock TGE name, a Graal patch, Graal-only, or uncompared.

Read: Linux `graalexe` 3.04; Windows 4.2.0.8 launcher, `GraalEngine.dll` and `Graal3DEngine.dll`; Windows 5.0.0.7 launcher, `GraalEngine.dll` and `Graal3DEngine.dll`; unpacked 5.30r3, 5.31r4, 6.00r2 and 6.00r4. The packed 5.12, 5.24 and 6.x executables are packer listings. They are not an engine.

## How a cell is counted

**Present** means the image registers the class on the console, recovers methods, records a C++ type, or emits an error whose text is `Class::method`. **Stub** means the name occurs and none of those do. **Gone** means the name does not occur.

A packed listing is a packer stub. A miss there means the listing does not contain the engine, not that the packed program lacked the module.

**Stock name** means the module is one already named as TGE in `torque/engine-and-formats.md`, and 3.04 still has it. **Patched** means this read shows a Graal-only method or event on that module. **Graal-only** means the name is not a TGE module. **Uncompared** means the body was not diffed against a TGE tree. No TGE source was downloaded.

## 3.04 Linux

3.04 is the only image in this set that still registers Torque's console. The registrar covers 66 classes that have at least one named method, plus global functions that include `exec`, `setModPaths`, `createCanvas`, `setScreenMode`, `getVersionNumber`, `getVersionString` and `getCompileTimeString`. `CodeBlock` reports an illegal path when a file has no mod directory. The listing names `main.cs` and the font-cache suffix `.gft`, and it registers a `.dts` reader beside the extension group `.ter` `.dif` `.dts`. A standalone `.dso` literal was not recovered here; the shipped `.dso` v33 layout stays in `torque/scripting.md`. **[bin]**

Graal's console class is `GuiGraalCtrl`, 31 registrations: 25 with a literal name (`moveUp`, `moveLeft`, `moveDown`, `moveRight`, `doMicro`, `setChat`, `setPassWord`, `openServerList`, `selectServer`, `selectServerCategory`, `startOfflineMode`, `connectToSelectedServer`, `serverDirectConnect`, `privateMessageSend`, `playerListOpenPlayer`, `playerListProfile`, `updateLoadLevelFields`, `loadLevel`, `updatePlayerProfile`, `updatePlayerMuted`, and the four volume and options setters) and six whose names are not literals in this listing. `torque/engine-304.md` names those six. `setNickName` is not among the literals. **[bin]**

`GameConnection` has 32 console methods. The names are ghosting, demo record and playback, voice listen and encode, the commander map, `transmitDataBlocks`, camera control, `setConnectArgs`, `setJoinPassword` and `setMissionCRC`. None of those names is Graal-only. The body is uncompared. **[bin]**

Other stock names that have console methods here: `SimObject` 10, `SimSet` 9, `ActionMap` 11, `GuiCanvas` 19, `GuiControl` 13, `TerrainBlock` 5, `InteriorInstance` 8, `ShapeBase` 79, `Player` 8, `AIPlayer` 9, `WheeledVehicle` 3, `FlyingVehicle` 1, `Item` 5, `Sky` 7, `Camera` 3, `Lightning` 3, `Precipitation` 3, `TriggerData` 3, `TerrainEditor` 26, `WorldEditor` 21, `Terraformer` 33, `fxSunLight` 51. `SimDataBlock`, `Vehicle`, `VehicleData`, `GameBase` and `ShapeBaseData` are C++ types. `HoverVehicle` and `Projectile` occur as a class name and have no console method (stub). The bitmap module is compiled in (`GBitmap`). `OpenGLDevice::setVerticalSync` is named and reported unimplemented. **[bin]**

C++ types that are not console classes: `TDrawableObject`, `TLevelObject`, `TGaniObject`, `TServerPlayer`, `TDrawableSurface`, `TSurfaceOwner`, `TGraalConnection`. Absent: `TAdventure`, `TGraalVar`, `TScriptExecutionSpace`, `TShowImg`, `GuiGraal3DCtrl`, `GameObject`, and every `GameShape` name. **[bin]**

| Module | 3.04 | 4.2 launcher | 4.2 engine | 4.2 3D | Lineage where it is present |
| --- | --- | --- | --- | --- | --- |
| Console and script loader | present | gone | gone | gone | stock name in 3.04; body uncompared |
| `SimObject` | present | gone | gone | present | stock name; body uncompared |
| `ActionMap` | present | gone | gone | present | stock name; body uncompared |
| `GuiCanvas` | present | gone | present | stub | stock name; body uncompared. The 3D DLL calls the engine's canvas |
| `GuiControl` | present | gone | present | present | stock name; body uncompared. The 3D image has the type |
| `GBitmap` | present | gone | present | stub | stock name; body uncompared. The 3D image has `GBitmapInstance` only |
| Terrain | present | gone | gone | present | stock name; body uncompared. 4.2 adds `TerrainChunkEvent` |
| Interiors | present | gone | gone | present | stock name; body uncompared. 4.2 keeps `Interior::read` |
| DTS | present | gone | gone | present | stock name; body uncompared. 4.2 names `TSShapeInstance` |
| `GameConnection` | present | gone | gone | present | 3.04 method names are stock; body uncompared. 4.2 adds `BigDataStartEvent` and `BigDataChunkEvent` (patched) |
| `ShapeBase` | present | gone | gone | gone | stock name in 3.04; body uncompared |
| `Player` | present | gone | gone | gone | stock name in 3.04; body uncompared |
| Vehicles | present | gone | gone | gone | stock names in 3.04; `HoverVehicle` is a 3.04 stub |
| Datablocks | present | gone | gone | stub | stock class in 3.04. 4.2 keeps the field name `datablock` and not `SimDataBlock` |
| `GameObject` | gone | gone | gone | present | Graal-only |
| `GuiGraalCtrl` | present | gone | stub | gone | Graal-only. 4.2 engine keeps the name and does not build the class |
| `GuiGraal3DCtrl` | gone | gone | stub | gone | Graal-only name on the 4.2 engine only |
| `TAdventure` | gone | gone | present | stub | Graal-only. Methods are on the engine; the 3D DLL only names the type |
| `TGraalVar` | gone | gone | present | present | Graal-only |
| `TScriptExecutionSpace` | gone | gone | present | stub | Graal-only. Methods are on the engine |
| `TShowImg` | gone | gone | present | stub | Graal-only. Methods are on the engine |

## 4.2.0.8 Windows

Three images. The launcher listing has DirectDraw and none of the module names in the table. What the 94 host slots do is `torque/4208-launcher.md`. **[bin]**

`GraalEngine.dll` keeps Torque's canvas, controls and bitmap reader, and drops the console. `GuiCanvas` has 55 methods (`renderFrame`, dialogs, mouse lock, hints). `GuiControl` has 85. `GBitmap` has 38, and the readers are PNG, JPEG, GIF, DDS, TGA, BMP and JPEG 2000. There is no `SimObject`, no `ActionMap`, no `.dso`, no `GameConnection`, no terrain, no interior, no DTS, no `ShapeBase`, no `Player`, no vehicle and no datablock class. The Torque GUI field names (`horizSizing`, `vertSizing`, `minExtent`, `fontType`, `fillColor`, `makeFirstResponder`, `pushToBack`) are still in this DLL. **[bin]**

The Graal types that 3.04 does not have are C++ classes here. `TAdventure` has 27 methods: client pump, keys, mouse, paint, warp, chat, level coordinates. `TScriptExecutionSpace` has 26: run, join and leave class, schedule, ignore events. `TGraalVar` has 85: script vars, arrays, XML, `runScript`. `TShowImg` has 66, including image, polygon, text, shape, layer and a 3D attach. `TGraalUniverse` has 5 (`addStaticObject`, `removeStaticObject`, `clearVars`). `GuiGraalCtrl` and `GuiGraal3DCtrl` are names, not method classes. How a session and a show-image actually run is `torque/4208-engine.md`. **[bin]**

`Graal3DEngine.dll` is the Torque world with Graal's object, not 3.04's game layer. Types: `SimObject`, `SimSet`, `SimGroup`, `NetObject`, `SceneObject`, `NetConnection`, `GameConnection`, `TerrainBlock`, `GameObject`. Error strings name `ActionMap`, `Interior`, `InteriorResource`, `TSShapeInstance`, `TSThread`, `Terraformer`, `TerrainEditor`, `SceneLighting` and `LightManager`. Event names `BigDataStartEvent`, `BigDataChunkEvent` and `TerrainChunkEvent` are the Graal net patch. Display-device names are OpenGL, Voodoo2 and the OpenGL-to-Direct3D wrapper. `WaterBlock`, `fxSunLight` and the sky field names are present. `ShapeBase`, `Player`, the vehicle classes and `SimDataBlock` are absent; `datablock` survives as a field name. `GameShape`, `GameShapeDTS`, `GameShapeDIF` and `GameShapeFT` do not occur. What `GameObject` exposes, and what an interior read rejects, is `torque/4208-g3d.md`. **[bin]**

5.0.0.7 and the own-engine images are the following sections.
