# Graal.exe 5.31r4 (file version 5.314)

Date: 2026-11-07. Static read of the unpacked executable in the v5 export. Nothing was run. **[bin]**

## What the decompile is

One executable. The version resource strings are file version `5.314`, original filename `Graal.exe`, copyright 2011. A compile-date string in the binary is `Jan 5 2011`, next to `02:56:36` and the script names `Adventure getBuildTime` and `Adventure checkExeSignature`. Source paths are `..\quattro_lib\` (`sha1.c`, `des.c`, `rsa.c`, jpeg2000). The named exports in the listing are zlib's, not `graal_set`. **[bin]**

`graal_set` is absent. There is no Delphi launcher split and no `GraalEngine.dll` / `Graal3DEngine.dll` pair inside this file. **[bin]**

## Torque

Absent: `GuiCanvas`, `SimObject`, `GameConnection`, `GameObject`, `ShapeBase`, `ActionMap`, `.dso`, `OpenGLDevice`, `TAdventure`, `TScriptExecutionSpace`, `TerrainChunk`, `datablock`, `Interior::read`, mission-phase logs, `CHR_PROTOCOL`. **[bin]**

GUI names that remain: `GuiControl`, `GuiTextCtrl`, `GuiTextEditCtrl`, `GuiTextListCtrl`, `GuiMLTextCtrl`, `GuiMLTextEditCtrl`, `GuiScrollCtrl`, `GuiWindowCtrl`, `GuiBitmapCtrl`, `GuiBitmapButtonCtrl`, `GuiBitmapBorderCtrl`, `GuiShowImgCtrl`, `GuiPMCtrl`, `GuiGraalCtrl`, `GuiGraal3DCtrl`, `GuiControlProfile`, `horizSizing`, `vertSizing`, `fillColor`, `makeFirstResponder`, `pushToBack`. `MissionGroup` is still a string passed to a lookup. `$pref::Graal::` keys remain (`fixedudpport`, `language`, `nicknamelimit`, and others). **[bin]**

## Graal's game

`TGraalVar`, `TShowImg`, `TGraalAni` (part, sound, sprite, step), `TGraalClientVar`, `TPlayer`, `TServerPlayer`, `TScriptFunction`, `TScriptUniverse`. The script object is `Adventure`: `Adventure getBuildTime`, `Adventure checkExeSignature`, `Adventure fileExists`, `Adventure getFileContent`, `Adventure setFileModTime`, `Adventure openDefaultViewer`, `Adventure disablePingConnection`. **[bin]**

Drawing: `Initialized OpenGL.`, `TWindowOpenGL::setScreenMode` failure strings, the switch `-opengl`, and `glLinkProgramARB` / `glUseProgramObjectARB`. The string `Direct3DCreate9` is present. `DirectDraw` is absent. **[bin]**

Files: `GR-V1.00` through `GR-V1.05`, `Z3-V1.03`, `Z3-V1.04`, `basepackage.gupd`, and the install-list name `graal_installfiles.txt`. FMOD is still named (`Failed to open fmod audio`). `DigitalProductId` and `DigitalProductId4` are both strings. No `G3D` login-token literal. **[bin]**

## Differences from 5.30r3

Strings in this build that the October executable does not have: `Jan 5 2011`, `Adventure openDefaultViewer`, `clearEmptyGlobalVars`, `fromplayerid`, `onRemotePlayerChats` (5.30 has `@onRemotePlayerChats`), and a `C:\Windows\Fonts\` path. The October build's `Graal has been activated!`, `StartScript QuitDialog`, and the extension list that includes `gxml` are absent here; a lone `.gxml` string remains. File version `5.303` versus `5.314`. The Torque and Graal-type picture above is the same in both. **[bin]**
