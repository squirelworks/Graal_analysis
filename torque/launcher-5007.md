# Graal.exe 5.0.0.7, the Delphi launcher

Date: 2026-11-07. Static read of the decompile in the v5 export. Nothing was run. **[bin]**

## What the decompile is

This is the real launcher, not a packer stub. The version resource strings are file version `5.0.0.7`, file description `Graal Online client`, product name `Graal`, original filename `Graal.exe`. **[bin]**

It is a Delphi program. It opens `SOFTWARE\Borland\Delphi\RTL` and `Software\Borland\Delphi\Locales`, builds a window class with `Delphi%.8X`, and resolves `setUseDelphiCommaTexts` from the engine. DirectDraw names are present. **[bin]**

## What it loads

It loads `GRAALENGINE.DLL` and resolves `graal_engineInitialize` plus 95 `graal_set*` names with `GetProcAddress`. If that initialisation fails it shows "The execution file is corrupted." It also resolves `startGraalExeReplacer` and `startGraalProfiler`. It loads `GRAAL3DENGINE.DLL` from two call sites. **[bin]**

The names it resolves, and the ones only the 3D DLL calls, are listed in [engine-5007.md](engine-5007.md#who-calls-the-setters). This launcher resolves the Flash panels, the external player list and options windows, the microphone, `graal_setOnServerLogin`, `graal_setOnServerListerConnect`, `graal_setStartGraal3D`, `graal_setShowGraalWindow`, and the language and translation-URL setters. It does not resolve the 3D-only setters (`graal_setIsOpenGLEnvironment`, `graal_setCreateGraal3DGameObject`, `graal_setConnectTo3DServer`, and the rest of that list). **[bin]**

## Torque and the Graal game

`GuiCanvas`, `SimObject`, `GameConnection`, `GameObject`, `ShapeBase`, `ActionMap` and `.dso` are absent. `TAdventure`, `TGraalVar`, `TShowImg` and `GuiGraalCtrl` are absent. The Graal game and the Torque GUI classes live in `GraalEngine.dll`; the Torque world lives in `Graal3DEngine.dll`. **[bin]**
