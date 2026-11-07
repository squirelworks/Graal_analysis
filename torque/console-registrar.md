# Torque's script-command registry

Date: 2026-11-07. Tags as in `README.md`.

While Graal shipped on Torque, script called native code through one registry. This note is how that registry worked, counted from the 3.04 Linux export, and how later clients shrink it. It records the shape of an entry, the class counts and the `GuiGraalCtrl` argument counts. The class totals are the same static read as [engine-304.md](engine-304.md).

## How a command is registered

Torque registers every script-callable name at startup. Each entry is a namespace (a console class, or the global namespace), a name, a help sentence, and a minimum and maximum argument count. The 3.04 binary has five registrars of that record. They differ only in which callback field they fill. **[bin]** Those fields correspond to Torque's five script return kinds: string, integer, float, void and bool. **[inf]**

The count includes the command name. On a method it also includes the object, which is the second value Torque passes. A maximum of 0 means there is no upper limit. A global command such as `echo` is registered at 2–0: one required script argument, and no upper limit. A method at 3–3 takes one script argument. A method at 2–2 takes none. **[bin]**

## The 3.04 Linux registry

The 3.04 Linux registrar holds 857 entries: 252 global commands and 605 methods on 67 console classes. Almost all of them are stock Torque (string and file helpers, sim objects, the GUI canvas, video and math, and the 3D game classes). Graal's own addition is `GuiGraalCtrl`, below. **[bin]**

| Methods | Console classes |
|---:|---|
| 252 | global namespace |
| 79 | `ShapeBase` |
| 51 | `fxSunLight` |
| 32 | `Terraformer` |
| 31 | `GuiGraalCtrl` |
| 30 | `GameConnection` |
| 26 | `TerrainEditor` |
| 21 | `WorldEditor` |
| 20 | `GuiTextListCtrl` |
| 19 | `GuiCanvas` |
| 17 | `GuiPopUpMenuCtrl` |
| 13 | `GuiControl`, `GuiFrameSetCtrl`, `GuiMenuBar` |
| 12 | `MessageVector` |
| 11 | `ActionMap` |
| 10 | `SimObject` |
| 9 | `AIPlayer`, `CreatorTree`, `GuiEditCtrl`, `NetConnection`, `SceneObject`, `SimSet` |
| 8 | `DbgFileView`, `InteriorInstance`, `Player` |
| 7 | `AIConnection`, `FileObject`, `GuiMLTextCtrl`, `GuiTerrPreviewCtrl`, `Sky` |
| 5 | `BanList`, `GuiInspector`, `Item`, `TerrainBlock` |
| 4 | `DebugView`, `EditTSCtrl`, `MissionAreaEditor`, `TCPObject` |
| 3 | `Camera`, `GuiButtonBaseCtrl`, `GuiFilterCtrl`, `Lightning`, `NetObject`, `Precipitation`, `TriggerData`, `WheeledVehicle` |
| 2 | `EditManager`, `GameBase`, `GuiBitmapCtrl`, `GuiClockHud`, `GuiMessageVectorCtrl`, `GuiScrollCtrl`, `GuiTextEditCtrl`, `HTTPObject`, `MissionArea`, `PhysicalZone`, `ShapeBaseData`, `StaticShape`, `Trigger` |
| 1 | `Debris`, `FlyingVehicle`, `GuiChunkedBitmapCtrl`, `GuiSliderCtrl`, `GuiTextCtrl`, `GuiTreeViewCtrl`, `SimpleNetObject`, `WaterBlock` |

`ShapeBase` is the large one (79). `fxSunLight`, `GameConnection` and the terrain and world editors are a few dozen each. `Player`, `AIPlayer`, `Item`, the wheeled vehicle, `Trigger` and `TriggerData`, `Lightning` and `Precipitation` are present as console classes. **[bin]**

## GuiGraalCtrl

Thirty-one methods, in registration order. Each one was registered with an empty help sentence, so the argument counts are the only signature. **[bin]**

| Method | Min | Max | Script arguments |
|---|---|---|---|
| `moveUp`, `moveLeft`, `moveDown`, `moveRight` | 3 | 3 | 1 |
| `doA`, `doS`, `doD`, `doQ`, `doP`, `doM` | 3 | 3 | 1 |
| `doMicro` | 3 | 3 | 1 |
| `setChat` | 3 | 3 | 1 |
| `setPassWord` | 3 | 3 | 1 |
| `openServerList` | 2 | 2 | 0 |
| `selectServer` | 3 | 3 | 1 |
| `selectServerCategory` | 3 | 3 | 1 |
| `startOfflineMode` | 2 | 2 | 0 |
| `connectToSelectedServer` | 2 | 2 | 0 |
| `serverDirectConnect` | 3 | 3 | 1 |
| `privateMessageSend` | 2 | 2 | 0 |
| `playerListOpenPlayer` | 3 | 3 | 1 |
| `playerListProfile` | 3 | 3 | 1 |
| `updateLoadLevelFields` | 2 | 2 | 0 |
| `loadLevel` | 5 | 5 | 3 |
| `updatePlayerProfile` | 12 | 12 | 10 |
| `updatePlayerMuted` | 3 | 3 | 1 |
| `updateMidiVolume`, `updateMp3Volume`, `updateRadioVolume`, `updateMicroActivationLevel`, `updateGraalOptions` | 2 | 2 | 0 |

`setNickName`, `setAccountName`, `setLanguage` and `retrieveAccountFields` are not on this table. Nickname, account and language are `$pref::Graal::` variables ([engine-304.md](engine-304.md#the-split)). **[bin]**

## Classes with a name and no method

The same export registers 161 console classes. 94 of them have a class name and no decoded method. `Projectile`, `HoverVehicle`, `ScriptObject` and `AudioEmitter` are in that set, and so is `Vehicle`. `FlyingVehicle` has the one method in the table above. **[bin]**

## What Graal did not register

Graal's draw objects and `TGraalConnection` are not console classes. `TGraalConnection` is not a child of `NetConnection` and has no console methods ([engine-304.md](engine-304.md#graal-types)). Stock `GameConnection` in 3.04 is still the Torque demo protocol: game string `Torque Game Engine Demo`, protocol 9, and no class table in the accept ([wire-by-build.md](wire-by-build.md#the-handshake-per-build)). **[bin]**

`GuiGraal3DCtrl` is not a console class in this binary. **[bin]**

## Later clients

The registry shrinks after 3.04. The evidence is the marker scan's string hits. **[bin]** ([study-torque-clients.md](study-torque-clients.md#2-marker-scan))

The 4.x and 5.00 2D engine keeps Torque's GUI classes and has no `SimObject` console and no `.dso`. The Torque engine proper is the 3D DLL, which keeps `SimObject` and `GameConnection`. In 4.04r2 that DLL is still the stock TGE world; from the 5.00 DLL it is the `GameObject` world. Those 3D DLLs have no `.dso`. **[bin]** ([study-torque-clients.md](study-torque-clients.md#1-the-short-answer), [study-torque-clients.md](study-torque-clients.md#6-what-the-2d-delphi-engine-lacks-per-era), [engine-and-formats.md](engine-and-formats.md#which-torque))

From 5.24r3 Graal's own engine replaces Torque. The marker scan covers the unpacked 5.24r3 and 5.31r4 single executables (that era also includes 5.30). `SimObject`, `GameConnection` and `.dso` are gone, and so are the `graal_set…` host callbacks of the split engine. What remains are GUI class and field names, plus `GuiGraalCtrl` and, on those Windows executables, `GuiGraal3DCtrl`. **[bin]** ([study-torque-clients.md](study-torque-clients.md#1-the-short-answer), [study-torque-clients.md](study-torque-clients.md#2-marker-scan), [study-torque-clients.md](study-torque-clients.md#6-what-the-2d-delphi-engine-lacks-per-era), [engine-and-formats.md](engine-and-formats.md#which-torque))
