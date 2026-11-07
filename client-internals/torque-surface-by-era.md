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

## The table

Launchers are one column: the 4.2.0.8 and 5.0.0.7 launcher listings match each other on this list (DirectDraw, and none of these names). 5.30r3 and 5.31r4 match each other. 6.00r2 and 6.00r4 match each other. Packed listings are under [Packed listings](#packed-listings), not in the table.

| Module | 3.04 | Launchers | 4.2 engine | 4.2 3D | 5.0 engine | 5.0 3D | 5.30 and 5.31 | 6.00 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Console and script loader | present | gone | gone | gone | gone | gone | gone | gone |
| `SimObject` | present | gone | gone | present | gone | present | gone | gone |
| `ActionMap` | present | gone | gone | present | gone | present | gone | gone |
| `GuiCanvas` | present | gone | present | stub | present | stub | gone | gone |
| `GuiControl` | present | gone | present | present | present | present | stub | stub |
| `GBitmap` | present | gone | present | stub | present | stub | gone | gone |
| Terrain | present | gone | gone | present | gone | present | gone | gone |
| Interiors | present | gone | gone | present | gone | present | gone | gone |
| DTS | present | gone | gone | present | gone | present | gone | gone |
| `GameConnection` | present | gone | gone | present | gone | present | gone | gone |
| `ShapeBase` | present | gone | gone | gone | gone | gone | gone | gone |
| `Player` | present | gone | gone | gone | gone | gone | gone | gone |
| Vehicles | present | gone | gone | gone | gone | gone | gone | gone |
| Datablocks | present | gone | gone | stub | gone | stub | gone | gone |
| `GameObject` | gone | gone | gone | present | gone | present | gone | gone |
| `GameShape` | gone | gone | gone | gone | gone | stub | gone | gone |
| `GuiGraalCtrl` | present | gone | stub | gone | stub | gone | stub | stub |
| `GuiGraal3DCtrl` | gone | gone | stub | gone | stub | stub | stub | stub |
| `TAdventure` | gone | gone | present | stub | present | stub | gone | gone |
| `TGraalVar` | gone | gone | present | present | present | present | stub | stub |
| `TScriptExecutionSpace` | gone | gone | present | stub | present | stub | gone | gone |
| `TShowImg` | gone | gone | present | stub | present | stub | stub | stub |

## 4.2.0.8 Windows

Three images. The launcher listing has DirectDraw and none of the module names in the table. What the 94 host slots do is `torque/4208-launcher.md`. **[bin]**

`GraalEngine.dll` keeps Torque's canvas, controls and bitmap reader, and drops the console. `GuiCanvas` has 55 methods (`renderFrame`, dialogs, mouse lock, hints). `GuiControl` has 85. `GBitmap` has 38, and the readers are PNG, JPEG, GIF, DDS, TGA, BMP and JPEG 2000. There is no `SimObject`, no `ActionMap`, no `.dso`, no `GameConnection`, no terrain, no interior, no DTS, no `ShapeBase`, no `Player`, no vehicle and no datablock class. The Torque GUI field names (`horizSizing`, `vertSizing`, `minExtent`, `fontType`, `fillColor`, `makeFirstResponder`, `pushToBack`) are still in this DLL. **[bin]**

The Graal types that 3.04 does not have are C++ classes here. `TAdventure` has 27 methods: client pump, keys, mouse, paint, warp, chat, level coordinates. `TScriptExecutionSpace` has 26: run, join and leave class, schedule, ignore events. `TGraalVar` has 85: script vars, arrays, XML, `runScript`. `TShowImg` has 66, including image, polygon, text, shape, layer and a 3D attach. `TGraalUniverse` has 5 (`addStaticObject`, `removeStaticObject`, `clearVars`). `GuiGraalCtrl` and `GuiGraal3DCtrl` are names, not method classes. How a session and a show-image actually run is `torque/4208-engine.md`. **[bin]**

`Graal3DEngine.dll` is the Torque world with Graal's object, not 3.04's game layer. Types: `SimObject`, `SimSet`, `SimGroup`, `NetObject`, `SceneObject`, `NetConnection`, `GameConnection`, `TerrainBlock`, `GameObject`. Error strings name `ActionMap`, `Interior`, `InteriorResource`, `TSShapeInstance`, `TSThread`, `Terraformer`, `TerrainEditor`, `SceneLighting` and `LightManager`. Event names `BigDataStartEvent`, `BigDataChunkEvent` and `TerrainChunkEvent` are the Graal net patch. Display-device names are OpenGL, Voodoo2 and the OpenGL-to-Direct3D wrapper. `WaterBlock`, `fxSunLight` and the sky field names are present. `ShapeBase`, `Player`, the vehicle classes and `SimDataBlock` are absent; `datablock` survives as a field name. `GameShape`, `GameShapeDTS`, `GameShapeDIF` and `GameShapeFT` do not occur. What `GameObject` exposes, and what an interior read rejects, is `torque/4208-g3d.md`. **[bin]**

## 5.0.0.7 Windows

Same split as 4.2.0.8. The launcher listing has DirectDraw and none of the module names. **[bin]**

The engine DLL is the 4.2 set with a few more methods. `GuiCanvas` has 58, adding drop-file acceptance and `playSound` to the 4.2 list. `GuiControl` has 103. `GBitmap` has 42, adding `forceTextureTransparency`, `allocateFromAnimation`, `updateBytesPerPixel` and `initObject` to the 4.2 readers. `TAdventure` has the same 27 names. `TScriptExecutionSpace` has 29. `TGraalVar` has 95, adding a loop limit, a protected object and an ini read. `TShowImg` has 67. `TGraalUniverse` has 19: script machines, a garbage collect, and class lookup, where 4.2.0.8 only adds, removes and clears static objects. New type names in this DLL are `MovieClip`, `TFlashCharacter` and `TScriptFunction`. `GuiGraalCtrl` is still a name. There is still no console, `SimObject`, `ActionMap`, `GameConnection`, terrain, `ShapeBase` or `Player`. The seven GUI field names listed for 4.2.0.8 are still here. **[bin]**

The 3D DLL still has `SimObject` (error strings; the type descriptor was recovered in 4.2.0.8 and not in this listing), `ActionMap`, `Interior`, `InteriorResource`, `TSShapeInstance`, `TerrainBlock`, `GameObject`, `GameConnection`, `BigDataStartEvent`, `BigDataChunkEvent`, `TerrainChunkEvent`, and the same OpenGL, Voodoo2 and wrapper device names. `ShapeBase`, `Player`, the vehicle classes and `SimDataBlock` are still absent, and `datablock` is still a field name. New names, with no recovered method: `GameShape`, `GameShapeDTS`, `GameShapeDIF`, `GameShapeFT` and `GuiGraal3DCtrl`. `GameShape3DS` does not occur. **[bin]**

## 5.30r3 and 5.31r4

Both unpacked images name `quattro_lib`. Their `Gui*` and Graal `T*` identifier sets are the same. Torque's console, `SimObject`, `ActionMap`, `GuiCanvas`, `GBitmap`, terrain, interiors, DTS, `GameConnection`, `ShapeBase`, `Player`, vehicles, datablock classes and `GameObject` do not occur. `TAdventure` and `TScriptExecutionSpace` do not occur. **[bin]**

What remains of Torque's GUI is names: `GuiControl`, `GuiControlProfile`, the stock control names (`GuiWindowCtrl`, `GuiScrollCtrl`, `GuiMLTextCtrl`, `GuiTextEditCtrl`, `GuiButtonCtrl`, and the rest of that list), plus Graal names `GuiGraalCtrl`, `GuiGraal3DCtrl`, `GuiShowImgCtrl`, `GuiPMCtrl`, `GuiStartMenuCtrl`, `GuiAccountPasswordCtrl`, `GuiSlideShowCtrl`, `GuiAccordionCtrl` and `GuiAnimationCtrl`. `GuiTilesCtrl` does not occur. The field names `horizSizing`, `vertSizing`, `minExtent`, `fontType`, `fillColor`, `makeFirstResponder` and `pushToBack` are in both images. This listing recovers no methods on those names. `TGraalVar`, `TShowImg`, `TDrawableObject`, `TLevelObject`, `TGaniObject` and the `TServer*` names are present as names. `TPlayer` here is that Graal name, not Torque's `Player`. **[bin]**

## 6.00r2 and 6.00r4

The two unpacked images have the same `Gui*` and Graal `T*` identifier set as 5.30r3 and 5.31r4, including `GuiGraalCtrl` and `GuiGraal3DCtrl`, and the same absences (`TAdventure`, `TScriptExecutionSpace`, `GuiCanvas`, `SimObject`, `GameConnection`, terrain, DTS). The seven field names in the 5.30 section do not occur in either 6.00 image. `client-internals/engine-600r2.md` reads the 6.00 control names as live GUI types; this pass only scores the names. **[bin]**

## Packed listings

The packed 5.12, 5.24r4, 5.2.4.3, 6.037 and 6.113 listings contain none of the module names in the table. They are packer stubs. The 6.113 listing's recovered type is a TLS integer helper, not a Torque class. Do not read an engine out of them. What the stubs do contain is already in `torque/skipped-v5-read.md` and `client-internals/skipped-v6-read.md`. **[bin]**

## Against stock TGE

A module whose name is already used for TGE in `torque/engine-and-formats.md`, and which 3.04 still registers, is a stock name. Its body is uncompared: this read did not diff it against a TGE tree.

`GameConnection` in 3.04 is the stock name set (ghosting, demo, voice, commander map, `transmitDataBlocks`, `setJoinPassword`). No method name on that class is Graal-only. On the 4.2.0.8 and 5.0.0.7 3D DLLs the same class sits next to `BigDataStartEvent`, `BigDataChunkEvent` and `TerrainChunkEvent`, which are the Graal patch. **[bin]**

`GuiCanvas` and `GBitmap` in the two engine DLLs use the stock method names (`renderFrame`, the bitmap readers). 5.0.0.7 adds drop-file methods on the canvas and four bitmap methods that 4.2.0.8 does not have. Those additions are a Graal patch relative to 4.2.0.8. Whether they exist in stock TGE is uncompared. **[bin]**

`GameObject`, `GameShape`, `GameShapeDTS`, `GameShapeDIF`, `GameShapeFT`, `GuiGraalCtrl`, `GuiGraal3DCtrl`, `TAdventure`, `TGraalVar`, `TScriptExecutionSpace` and `TShowImg` are Graal-only. **[bin]**

## For graal-client-repro issues

Comments for squirelworks/graal-client-repro. Not posted: `gh` in this environment is read-only for writes.

### #151

The TGE 1.2 surface is the 3.04 Linux binary, and only that one. It still registers the console (`exec`, `setModPaths`, `CodeBlock`), `SimObject`, `ActionMap`, `GuiCanvas`, `GuiControl`, `GBitmap`, terrain, interiors, DTS, `GameConnection`, `ShapeBase`, `Player`, vehicles and datablocks. Graal's game on that console is `GuiGraalCtrl` (31 methods). `TGraalConnection` is a C++ type and is not a console `NetConnection`. From 4.2.0.8 the 2D engine does not call that console. It calls `GuiCanvas`, `GuiControl` and `GBitmap`, and the loop is `TAdventure` with `TGraalVar` and `TScriptExecutionSpace`. The 3D DLL is a separate, smaller Torque world (`SimObject`, `GameConnection`, terrain, interiors, DTS) whose game class is `GameObject`, not `Player`. 5.0.0.7 is that same split, plus the names `GameShapeDTS`, `GameShapeDIF` and `GameShapeFT`. Unpacked 5.30, 5.31, 6.00r2 and 6.00r4 have no Torque console, sim, canvas class, bitmap class, or 3D classes. What the later script layer still names is the control set (`GuiControl` and the other `Gui*` names, including `GuiGraalCtrl` and `GuiGraal3DCtrl`). The field names `horizSizing`, `vertSizing`, `minExtent`, `fontType`, `fillColor`, `makeFirstResponder` and `pushToBack` are in 5.30 and 5.31 and are absent from both 6.00 images. `TAdventure` and `TScriptExecutionSpace` are gone by 5.30. `TGraalVar` and `TShowImg` remain as names.

### #152

`common/torque/full` matches 3.04 only.

4.2.0.8 and 5.0.0.7 are not one hybrid module. The engine DLL is GUI plus `GBitmap` plus `TAdventure`, `TGraalVar`, `TScriptExecutionSpace` and `TShowImg`, with no `SimObject` and no `ActionMap`. The 3D DLL is the residual Torque world: `SimObject`, `GameConnection`, terrain, interiors, DTS, and `GameObject` instead of `Player`, vehicles and datablocks. 5.0.0.7's 3D DLL adds the `GameShapeDTS`, `GameShapeDIF` and `GameShapeFT` names.

5.30 and 5.31 do not use that residual world. They are the own-engine program (`quattro_lib`) with Torque control names and the GUI field names. They belong beside `common/cpp`, not under `common/torque/residual`.

6.00r2 and 6.00r4 keep that control-name set and drop the field names. `common/cpp` is the right base. No Torque module.

### #153

no Torque change

### #154

no Torque change

### #155

The parked module shaped like 3.04 is the right shape for 3.04: console, sim, GUI, `ActionMap`, and `GuiGraalCtrl` with 31 methods. The stock game classes are in that binary so a later build can leave them out.

It is the wrong shape for the 4.2.0.8 and 5.0.0.7 engine DLL. Those DLLs do not construct `GuiGraalCtrl`. The 2D loop is `TAdventure`. Script state is `TGraalVar` and `TScriptExecutionSpace`. `TShowImg` is the show-image, including a 3D attach. By 5.0.0.7 `TGraalUniverse` also runs script machines and a garbage collect. 4.2.0.8's universe object only adds, removes and clears static objects.

It is the wrong shape for those builds' 3D DLL. `Player`, `ShapeBase`, vehicles and datablock classes are already gone. The world type is `GameObject`. 5.0.0.7 adds `GameShapeDTS`, `GameShapeDIF`, `GameShapeFT` and the `GuiGraal3DCtrl` name, which 4.2.0.8's 3D DLL does not have. Dropping `Player` from a 3.04-shaped module does not produce that DLL.

5.30 onward should not link the Torque module. `TAdventure` is not in those images. The hold stands: this is a surface note, not a unit on a build path.
