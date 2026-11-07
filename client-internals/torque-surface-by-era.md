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

| Module | 3.04 | Lineage |
| --- | --- | --- |
| Console and script loader | present | stock name; body uncompared. `.dso` literal not recovered in this listing |
| `SimObject` | present | stock name; body uncompared |
| `ActionMap` | present | stock name; body uncompared |
| `GuiCanvas` | present | stock name; body uncompared |
| `GuiControl` | present | stock name; body uncompared |
| `GBitmap` | present | stock name; body uncompared |
| Terrain (`TerrainBlock`) | present | stock name; body uncompared |
| Interiors (`InteriorInstance`) | present | stock name; body uncompared |
| DTS (`TSMesh`, `.dts`) | present | stock name; body uncompared |
| `GameConnection` | present | stock method names; body uncompared |
| `ShapeBase` | present | stock name; body uncompared |
| `Player` | present | stock name; body uncompared |
| Vehicles | present (`WheeledVehicle`, `FlyingVehicle`; `HoverVehicle` stub) | stock names; body uncompared |
| Datablocks (`SimDataBlock`, `transmitDataBlocks`) | present | stock name; body uncompared |
| `GameObject` | gone | Graal-only; not in this image |
| `GuiGraalCtrl` | present | Graal-only |
| `GuiGraal3DCtrl` | gone | Graal-only; not in this image |
| `TAdventure` | gone | Graal-only; not in this image |
| `TGraalVar` | gone | Graal-only; not in this image |
| `TScriptExecutionSpace` | gone | Graal-only; not in this image |
| `TShowImg` | gone | Graal-only; not in this image |

4.2.0.8, 5.0.0.7 and the later own-engine images are the following sections.
