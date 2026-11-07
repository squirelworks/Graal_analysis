# Graal.exe 5.30r3 (file version 5.303)

Date: 2026-11-07. Static read of the unpacked executable in the v5 export. Nothing was run. **[bin]**

## What the decompile is

One executable. The version resource strings are file version `5.303`, original filename `Graal.exe`, copyright 2010. A compile-date string in the binary is `Oct 18 2010`. Source paths are `..\quattro_lib\` (crypto `sha1.c`, `des.c`, `rsa.c`, and jpeg2000). The named exports in the listing are zlib's (`crc32`, `deflate`, `inflate`, and the rest), not `graal_set`. **[bin]**

`graal_set` is absent. The Delphi launcher and the separate engine DLL of 5.0.0.7 are not in this file. **[bin]**

## Torque

Absent: `GuiCanvas`, `SimObject`, `GameConnection`, `GameObject`, `ShapeBase`, `ActionMap`, `.dso`, `TAdventure`, `TScriptExecutionSpace`, `TerrainChunk`, `datablock`, mission-phase logs. **[bin]**

Still present as GUI names: `GuiControl`, `GuiGraalCtrl`, `GuiGraal3DCtrl`, `GuiShowImgCtrl`, `GuiControlProfile`, `horizSizing`, `vertSizing`, `fillColor`, `makeFirstResponder`, `pushToBack`. `MissionGroup` is a string. `$pref::Graal::` keys are present, including `fixedudpport`. **[bin]**

## Graal's game

`TGraalVar`, `TShowImg`, `TGraalAni`, `TPlayer`, `TServerPlayer`, `TScriptFunction`, `TScriptUniverse`. Script methods are named `Adventure …`, including `Adventure getBuildTime`. Drawing is OpenGL (`Initialized OpenGL.` and `TWindowOpenGL::setScreenMode` messages). The string `Direct3DCreate9` is present. `DirectDraw` is absent. **[bin]**

Level magics `GR-V1.00` through `GR-V1.05` are present, as are `GRESCR` and `GRPKG` hits in the same way as 5.31. FMOD is still named (`Failed to open fmod audio`). **[bin]**

## Differences from 5.31r4

The two unpacked exes are the same program a few months apart, not copies. Only this build logs that Graal has been activated, names a quit-dialog start script, and lists the extensions zip, gpak, app, nw, graal, gmap and gxml. Its compile banner is 18 October 2010. What only 5.31r4 has is in [engine-531r4.md](engine-531r4.md#differences-from-530r3). Both still have a separate `.gxml` string. **[bin]**
