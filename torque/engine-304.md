# The 3.04 Linux engine: stock TGE plus a Graal game

Date: 2026-11-07. Tags as in `README.md`.

Read from a decompile export of the Linux `graalexe` 3.04 (the same program as `G3D03014`: Unix platform files, SDL, the `graal/` sources). Nothing here was run. No code addresses are kept. The console registrar decoded from that export is [console-304.tsv](console-304.tsv) (857 entries). This note is what that export adds to [study-torque-clients.md](study-torque-clients.md) and [engine-and-formats.md](engine-and-formats.md).

## The split

3.04 does not replace Torque's game. It compiles stock TGE and a second game beside it. **[bin]**

| Side | What is in the binary |
|---|---|
| Stock TGE | Console, sim objects, resource manager, GUI, OpenGL texture manager, `ActionMap`, terrain, interiors, DTS, sky, water, the world and terrain editors, and the TGE game layer (`Player`, `ShapeBase`, vehicles, items, projectiles, triggers, lightning, precipitation). Source paths are TGE's (`console/`, `sim/`, `dgl/`, `gui/`, `game/`, `terrain/`, `interior/`, `ts/`, `editor/`, `platformX86UNIX/`). |
| Graal | Twenty `graal/*.cpp` translation units, plus `gui/guiGraalCtrl.cc`. The 2D game is the console class `GuiGraalCtrl`. |
| Not a Torque class | Graal's draw types and `TGraalConnection` (below). They do not appear in the console registrar. |

`fxSunLight` (51 decoded methods) is the community sunlight class, already in this binary, not a 3.153 addition. Stock TGE's OpenAL console functions are registered, and the binary also contains the failure string for opening fmod. Crypto++ (RSA) is compiled in next to `license/license.graal` and `license/sig.graal`.

The Graal prefs this binary names, all under `$pref::Graal::`, are `nickname`, `accountname`, `language`, `automapping`, `notoalls`, `dontloadlistheads`, `fixedport`, `fixedudpport`, `noudp`, `dontconnectlevels`, `limitnicknames`, `nicknamelimit` and `defaultfontsize`.

## Argument counts

Every decoded entry has a minimum and a maximum. The count includes the command name. On a method it also includes the object id, which is the second value Torque passes. A maximum of 0 means there is no upper limit (`error` is 2 and 0, and its usage says the text may repeat). **[bin]**

So `strlen(str)` is 2–2 (the name plus the string), `file.writeLine(text)` is 3–3 (the name, the object, the text), and `GuiGraalCtrl::moveUp` at 3–3 takes one script argument. `openServerList` at 2–2 takes none. Graal registered every `GuiGraalCtrl` method with an empty usage string `()`; the counts are the only signature in the binary.

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

`playerListProfile` is on this table. The 3.153 method table's `setNickName`, `setAccountName`, `setLanguage` and `retrieveAccountFields` are not. Nickname, account and language are the `$pref::Graal::` variables above. The six `do*` names are four-byte strings; they sit between `moveRight` and `doMicro` and spell `doA`, `doS`, `doD`, `doQ`, `doP`, `doM`.

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

Decoded console methods on classes that the 5.12 engine no longer has (see [engine-and-formats.md](engine-and-formats.md)). A class can still be present with a name and no method in this decode. **[bin]**

| Console class | Decoded methods in 3.04 | In 5.12 |
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
| `Camera`, `WheeledVehicle`, `Precipitation`, `Lightning`, `TriggerData` | 3 each | game-layer classes dropped; `WheeledVehicle` is one of three vehicle classes that have methods (`FlyingVehicle` has 1; `HoverVehicle` and `Vehicle` have a class name and no decoded method) |
| `Projectile`, `ScriptObject`, `AudioEmitter` | class name, no decoded method | dropped |

The shell a 3.04 rebuild has to run is the console, the sim objects, the GUI canvas, fonts, themes and `ActionMap`, plus `GuiGraalCtrl`. The stock 3D classes are in the binary and unused by the shipped 2D scripts. Later clients delete that game layer instead of adding one. A module shaped like 3.04 can drop those classes for 4.20 and 5.12; it cannot start from 5.12 and grow them back.

## Translation units

Graal files compiled into this binary. **[bin]**

| File | String in that file |
|---|---|
| `graal/adventure.cpp` | `state.png`, `sprites.png`, `bomb1.png`, `bomb2.png` |
| `graal/baddies.cpp` | (path only) |
| `graal/client.cpp` | (path only) |
| `graal/convertedclasses.cpp` | (path only) |
| `graal/descipher.cpp` | (path only) |
| `graal/ganis.cpp` | (path only) |
| `graal/graalconnection.cpp` | (path only) |
| `graal/graalplayer.cpp` | `Player enters local level %s.` |
| `graal/graphics.cpp` | (path only) |
| `graal/levels.cpp` | (path only) |
| `graal/npcs.cpp` | the trigger name `playerenters` |
| `graal/playerlist.cpp` | `PrivateMessageSendButton.setText($language::Send);` |
| `graal/scriptfunctions.cpp` | `shapetiletypes` |
| `graal/serverlist.cpp` | `Canvas.setContent(AdventureGui);` |
| `graal/serverplayer.cpp` | (path only) |
| `graal/showimgs.cpp` | `polygon` |
| `graal/sounds.cpp` | (path only) |
| `graal/surfaceowner.cpp` | (path only) |
| `graal/tiles.cpp` | (path only) |
| `graal/weapons.cpp` | (path only) |
| `gui/guiGraalCtrl.cc` | the `GuiGraalCtrl` method table |

## Catalogue

[console-304.tsv](console-304.tsv) is every decoded console function and method: namespace, name, usage string, minimum, maximum. `(global)` is a function. Any other namespace is a method on that console class. Short method names that the export stored only as raw bytes are recovered where the usage string or the byte string names them (`ActionMap.push` and `pop`, `SimObject.dump`, the editor undo/redo, and the six `do*` methods). **[bin]**
