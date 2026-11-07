# The 3.04 Linux engine: stock TGE plus a Graal game

Date: 2026-11-07. Tags as in `README.md`.

Read from the Linux `graalexe` 3.04 binary (the same program as `G3D03014`: Unix platform files, SDL). Nothing here was run. This note is what that read adds to [study-torque-clients.md](study-torque-clients.md) and [engine-and-formats.md](engine-and-formats.md).

## The split

3.04 does not replace Torque's game. It compiles stock TGE and a second game beside it. **[bin]**

Stock TGE is still the console, the sim objects, the resource manager, the GUI, the OpenGL texture manager, `ActionMap`, terrain, interiors, DTS shapes, sky, water, the world and terrain editors, and the TGE game layer (`Player`, `ShapeBase`, vehicles, items, projectiles, triggers, lightning, precipitation). The console surface is 857 functions and methods. Almost all of them are that stock engine. How Torque fills that list, the count by class, and how later clients shrink it, is [console-registrar.md](console-registrar.md).

Graal's game is the console class `GuiGraalCtrl`. The `graal/` sources cover the adventure client, baddies, the connection and the player, ganis, graphics, levels, NPCs, the player list, script functions, the server list, show images, sounds, surfaces, tiles, weapons, the cipher and the converted classes.

Graal's draw types and `TGraalConnection` (below) are not Torque console classes. They are absent from the console registrar.

`fxSunLight` (51 methods) is the community sunlight class, already in this binary, not a 3.153 addition. OpenAL is the registered sound console, and fmod is linked as well. Crypto++ (RSA) is compiled in beside the shipped license files.

The Graal prefs this binary names, all under `$pref::Graal::`, are `nickname`, `accountname`, `language`, `automapping`, `notoalls`, `dontloadlistheads`, `fixedport`, `fixedudpport`, `noudp`, `dontconnectlevels`, `limitnicknames`, `nicknamelimit` and `defaultfontsize`.

## Argument counts

Every console entry has a minimum and a maximum. The count includes the command name. On a method it also includes the object, which is the second value Torque passes. A maximum of 0 means there is no upper limit. **[bin]**

`GuiGraalCtrl::moveUp` at 3–3 takes one script argument. `openServerList` at 2–2 takes none. `loadLevel` at 5–5 takes three. `updatePlayerProfile` at 12–12 takes ten. Graal registered every `GuiGraalCtrl` method with an empty usage string, so the counts are the only signature.

## GuiGraalCtrl

Thirty-one methods, in registration order. **[bin]**

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

`playerListProfile` is on this table. The 3.153 method table's `setNickName`, `setAccountName`, `setLanguage` and `retrieveAccountFields` are not. Nickname, account and language are the `$pref::Graal::` variables above.

`loadLevel` takes three script arguments. `updatePlayerProfile` takes ten. The empty usage strings do not name them.

## Graal types

C++ type info in this binary, parent first. None of these names is a console class. **[bin]**

| Type | Parent |
|---|---|
| `TDrawableObject` | (none recorded) |
| `TLevelObject` | `TDrawableObject` |
| `TGaniObject` | `TLevelObject` |
| `TServerPlayer` | `TGaniObject` |
| `TDrawableSurface` | `TDrawableObject` |
| `TSurfaceOwner` | `TDrawableSurface` |
| `TGraalConnection` | (none recorded) |

`TGraalConnection` is not a child of Torque's `NetConnection` in this type info, and it has no console methods. That matches the earlier finding that 3.04 does not put Graal classes on Torque's net layer. The 3.153 names `TGraalUniverse`, `TShowImg`, `TTilesVar` and `GuiPlayerView` do not occur here.

## What later builds drop

Console methods on classes that the 5.12 engine no longer has (see [engine-and-formats.md](engine-and-formats.md)). A class can still be present with a name and no method in this read. **[bin]**

| Console class | Methods in 3.04 | In 5.12 |
|---|---|---|
| `ShapeBase` | 79 | dropped with the TGE game layer |
| `fxSunLight` | 51 | kept |
| `GameConnection` | 30 | kept, different protocol |
| `Terraformer` | 32 | kept (editors stay) |
| `TerrainEditor` | 26 | kept |
| `WorldEditor` | 21 | kept |
| `ActionMap` | 11 | dropped with the Torque console (era C) |
| `Player` | 8 | dropped |
| `AIPlayer` | 9 | dropped |
| `InteriorInstance` | 8 | dropped by the `GameObject` era |
| `Sky` | 7 | kept into 5.12 |
| `Item` | 5 | dropped |
| `TerrainBlock` | 5 | kept |
| `Camera`, `WheeledVehicle`, `Precipitation`, `Lightning`, `TriggerData` | 3 each | game-layer classes dropped; `WheeledVehicle` is one of three vehicle classes that have methods (`FlyingVehicle` has 1; `HoverVehicle` and `Vehicle` have a class name and no method) |
| `Projectile`, `ScriptObject`, `AudioEmitter` | class name, no method | dropped |

The shell a 3.04 rebuild has to run is the console, the sim objects, the GUI canvas, fonts, themes and `ActionMap`, plus `GuiGraalCtrl`. The stock 3D classes are in the binary and unused by the shipped 2D scripts. Later clients delete that game layer instead of adding one. A module shaped like 3.04 can drop those classes for 4.20 and 5.12; it cannot start from 5.12 and grow them back.
