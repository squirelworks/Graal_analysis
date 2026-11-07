# Windows file version 4.2.0.8: launcher, Graal engine, Torque 3D

Date: 2026-11-07. Tags as in `README.md`.

Read from a decompile export named 4.2.0.8. Nothing was run. No code addresses are kept. The existing notes already call Windows 4.20r8's file version 4.2.0.8, and they say that upload had no `Graal3DEngine.dll` ([study-torque-clients.md](study-torque-clients.md)). This export has three programs, plus FreeType and fmod as their own DLLs:

| Module | What it is |
|---|---|
| `Graal.exe` | Delphi launcher. DirectDraw. Registers the draw and window callbacks. |
| `GraalEngine.dll` | Graal's 2D engine. Torque's GUI, bitmaps and math. Graal's game and GS2. No Torque console, no `.dso`, no `SimObject`. |
| `Graal3DEngine.dll` | Torque after the game layer was dropped. `GameObject`, `GameConnection`, terrain chunks, interiors. No `ShapeBase`, no `Player`. |

## How the three fit

The launcher is Delphi. It draws with DirectDraw, loads `GRAALENGINE.DLL`, and registers `graal_set…` callbacks (94 names). It does not contain the game. Every name the launcher registers also appears in the engine. The engine has 19 further names that the launcher does not register. All of those also appear in the 3D DLL, and the 3D DLL has no callback name that the engine lacks. **[bin]**

The 19 are the 3D bridge: `graal_setConnectTo3DServer`, `graal_setCreateGraal3DGameObject`, `graal_setDeleteGraal3DLightInfo`, `graal_setGetGraal3DTerrainHeight`, `graal_setGetGraalPlayerScriptObject`, `graal_setSendGraal3DScriptEvent`, `graal_setSendGraal3DScriptEvents`, `graal_setSendGraal3DServerText`, `graal_setRemoveGraal3DConnection`, `graal_setRemoveGraal3DMissionGroup`, `graal_setIsOpenGLEnvironment`, `graal_setFreeGraalTexture`, `graal_setGetAllowCursorOff`, `graal_setGetHardwareCursorVisible`, `graal_setOnGraalFileDownloaded`, `graal_setSetGraalFullScreenMode`, `graal_setSetGraalWindowLocked`, `graal_setSetGraalWindowMode`, `graal_setSetMinimumFrameTicks`.

So the 2D engine owns the callback table. The launcher fills the draw and window slots. When the 3D DLL loads it fills the 3D slots, the same split as 4.04r2, with `GameObject` in place of `Player`. **[bin]** ([protocol/v4x-clients.md](../protocol/v4x-clients.md))

The launcher's own draw slots include `Draw2DTile`, `Draw3DTile`, `CreateTilesBuffer`, `DrawTilesOnScreen`, `PushGraal2DMatrix`, `PopGraal2DMatrix`, `GetGraal2DMatrix`, `IsGraal2DMatrixActivated`, `DrawTriangleStripPanel`, `DrawPolygonEx`, and `StartGraal3D`. Tiles and images can take a 2D matrix before a 3D host is asked for terrain height. **[bin]**

## GraalEngine.dll: Torque GUI beside Graal's game

Torque that is still a C++ class here: `GuiCanvas` (60 methods), `GuiControl` (99), `GuiControlProfile`, `GuiBitmapCtrl`, `GBitmap`, `Stream`, `FileStream`, `MatrixF`, `QuatF`, the point and box types. RTTI also names `GuiWindowCtrl`, `GuiTextEditCtrl`, `GuiTextListCtrl`, `GuiScrollCtrl`, `GuiMLTextCtrl`, `GuiPopUpMenuCtrl`, `GuiProgressCtrl`, `GuiCursor`. **[bin]**

Absent: `SimObject`, `ActionMap`, `GameConnection`, `.dso`, `setModPaths`, `ShapeBase`. This is not the 3.04 monolith. **[bin]**

Graal beside that GUI:

| Class | Methods | Role |
|---|---|---|
| `TGraalVar` | 96 | script values, arrays, `activateScript`, scheduled events |
| `TScriptExecutionSpace` | 48 | runs an action, catches it, updates classes, checks scheduled events |
| `TShowImg` | 72 | a show-image, including attach node, attach offset and euler rotation |
| `TAdventure` | 33 | the level session: keys, the client link, mouse on the level, nearby players |
| `TParticleEmitter` | 28 | particles, drawn with the other objects |
| `TDrawableObject` | 19 | draw list, sort, draw matrix. Parent of the show-image side |
| `TGraalAni` | 16 | a gani, `loadScriptEncrypted` |
| `TGraalClientVar` | 16 | a client copy of a var, with `send` |
| `TGraalUniverse` | 5 | static objects |
| `TFlashMatrix` | 15 | the Flash panel's matrix, separate from Torque's `MatrixF` |

The engine compares a control's name to `GuiGraalCtrl` and `GuiGraal3DCtrl` and, on a match, drops that control so it is not resolved as an ordinary object. It also builds a `TGraalVar` for each start script it knows: `StartScript_GraalGui`, `StartScript_GraalGui3D`, `StartScript_MainMenu`, `StartScript_MoveMap2D`, `StartScript_MoveMap3D`, `StartScript_OptionsWindow`, `StartScript_PlayerProfile`, `StartScript_LoadLevelGui`, `StartScript_MessageBoxDialog`, `StartScript_Profiles`, `StartScript_QuitDialog`, `StartScript_SelectFileDialog`, `StartScript_SetupDialog`. String names next to those are `MainMenuGui2D`, `ServerListGui`, `PlayerProfileGui`. Menus are Graal script objects with Torque control names, not compiled TorqueScript. **[bin]**

`TShowImg` can name an attach node and an euler rotation, so a 2D image already has a place to sit on a 3D object. The height under it comes from the 3D callback `graal_setGetGraal3DTerrainHeight`, which this DLL names and the 3D DLL also names. **[bin]**

## Graal3DEngine.dll: GameObject Torque

RTTI classes include `GameObject`, `GameConnection`, `NetConnection`, `NetObject`, `SimObject`, `SimSet`, `SimGroup`, `SceneObject`, `TerrainBlock`. A type walk compares `GameObject` with `SceneObject`, so `GameObject` is a scene object. `ShapeBase` and Torque's `Player` do not occur. A placeholder `TPlayer` type does. **[bin]**

The 3D DLL still has Graal types, thinner than the 2D engine: `TGraalVar` (20 methods, including `runScript`, `executeFunction`, `createScriptSpace`), `TScriptExecutionSpace`, `TShowImg`, `TAdventure` (`handleMouseWheelEvent`, `timer`), `TGraalUniverse`, `TGraalAni` (`saveScriptEncrypted`). The script VM is Graal's. Torque's console is only what `GameObject` networking needs: `SimObject`, `ActionMap` device names, mission group, ghost scope. **[bin]**

Login steps are two, and both call `onGraal3DLoginStep`: a string that starts `*** Phase 1: Download Ghost Obje`, then `*** Phase 2: Mission Lighting`. The same routine names `MissionStartPhase1Ack` and `MissionStartPhase2Ack`, and phase 2 also has `Mission lighting done`. There is no datablock-download phase. In the interior code, `datablock` is one key of a sub-object stream, beside `class`, `rotation` and `scale`; any other key is `Bad key in subObject stream!`. That is not a Player datablock. `Interior::read` still rejects an incompatible interior file. **[bin]**

Terrain is already chunked. `TerrainChunkEvent` and `TerrainRequestUpdatesEvent` are net events, and a string says it is sending a terrain chunk. `WaterBlock`, `MissionGroup` and `TSShapeInstance` are present. Scene lighting can fail with "no game connection". **[bin]**

3D text is FTGL (`FTFont`, `FTGLTextureFont`) on the FreeType DLL, not Torque's `.gft` cache. **[bin]**

## What a later module keeps

Era B in the client rebuild is this split, not a copy of the 3.04 monolith.

| Piece | 4.2.0.8 | Dropped from 3.04 |
|---|---|---|
| Launcher draws through callbacks | yes | 3.04 had no launcher |
| Torque GUI classes, no script VM | the 2D engine | 3.04's console ran `.dso` |
| GS2 as `TGraalVar` / `TScriptExecutionSpace` | yes | 3.04 menus were TorqueScript |
| `GameObject` world, no `Player` | the 3D DLL | 3.04 still had `Player` and `ShapeBase` |
| Two mission phases, terrain chunks | the 3D DLL | 3.04 shipped no 3D scripts |

4.04r2's 3D DLL is the older shape (stock TGE, `Player`, three mission phases). It is not in this folder. The two exe-only zips are one packer stub ([v4-404r2-exe.md](v4-404r2-exe.md), [v4-420r8-exe.md](v4-420r8-exe.md)).
