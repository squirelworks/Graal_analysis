# The 5.0.0.7 Delphi launcher

Date: 2026-11-07. Static read of the launcher decompile. Nothing was run. **[bin]**

The version resource string is file version `5.0.0.7`. The file description is `Graal Online client`, the product name is `Graal`, and the original filename is `Graal.exe`. **[bin]**

## Startup

This is a Delphi program. It opens the Borland Delphi RTL and locale keys, builds a window class with `Delphi%.8X`, and draws with DirectDraw (create, initialise, resize, finalise, delete) and DirectInput. A log line records 2D drawing during a 3D scene. **[bin]**

Before the forms are created it walks its arguments. The switches it recognises are `-setup`, `-silentsetup`, `-connect` plus the next argument, `-listscriptfunctions`, `-error`, `-message`, `-startedbyexereplacer`, `-opengl`, `-window` plus a window handle, `-guestaccount`, `-plugincookie`, and `-nologging`. An argument that starts with `graal://` or `graal3://` is stored as the connect target with that prefix removed (8 characters, or 9). **[bin]**

If a file named `game_temp.exe` is present beside the executable, the launcher loads the engine and takes an early path that can skip the normal windows. That is the exe-replacer hand-off. The normal path creates the application windows, loads the engine, and registers callbacks. **[bin]**

## What it resolves

`GRAALENGINE.DLL` is loaded once. The launcher then resolves `graal_engineInitialize` and 95 `graal_set*` names, plus the direct exports it calls itself (`connectToGraalServer`, `renderGraal`, `renderGraalCanvas`, the music and microphone calls, `openGraalServerList`, `loadGraalGui`, `enableScriptedControls`, and the same kind of entry). **[bin]**

The 95 setters fall into these jobs. **[bin]**

| Job | What the names cover |
|---|---|
| Tiles and drawing | 2D and 3D tiles, tile buffers, text and text metrics, lines, polygons, screen fill, clipping, texture size and transparency |
| Panels | creating, drawing, filling and saving a drawing panel, including a triangle strip |
| Matrices | the 2D matrix stack, and push/pop of a colour matrix |
| Window | screen size, show the window, fullscreen get and set, whether the application is active, shutdown, setup mode, a path dialog, status icons, a screen capture |
| Login and files | home directory, server login, listserver connect, server text, file update, two URL openers, language, translation URL |
| External windows | options, a message box, the external player list, a profile |
| Flash | create, delete, clip, file, play, stop, visibility, looping, vars, and calling a Flash function |
| Microphone | whether info is required, activated, volume |
| 3D entry | `graal_setStartGraal3D` only |

After the names are resolved, one routine calls every setter and then `graal_engineInitialize`. A zero return shows a warning whose text is `The execution file is corrupted.` and sets the quit flag. The engine routine that return comes from checks the signature files and loads the license text; the paths recovered in the engine decompile return success, so the zero case is the launcher's check rather than a failure branch this read recovered. **[bin]**

The 4.2.0.8 launcher decompile resolves 94 `graal_set*` names. This launcher adds eight and drops seven. **[bin]**

Added here: `graal_setPushColorMatrix`, `graal_setPopColorMatrix`, `graal_setGetGraalIsFullscreen`, `graal_setSetGraalFullscreen`, `graal_setShowGraalWindow`, `graal_setGetGraalScreenCapture`, `graal_setSetFlashPanelClipping`, `graal_setForceTextureTransparency`.

Missing here: `graal_setDrawGraphicsStretched`, `graal_setMakeGraalScreenshot`, `graal_setSetFlashPanelSize`, `graal_setLogGraalMessage`, `graal_setOpenExternalHistory`, `graal_setOpenExternalLogWindow`, `graal_setOpenExternalPM`.

## When the DLLs load

`GRAALENGINE.DLL` loads on the normal startup path, before callbacks are registered, and also on the `game_temp.exe` path. A loaded-flag stops a second load. **[bin]**

`GRAAL3DENGINE.DLL` has two call sites. **[bin]**

- If a flag is already set when the message loop is about to start, the launcher loads the DLL, resolves `loadGraal3DEngine`, `runGraal3DEngine`, `endGraal3DEngine`, `resizeGraal3DWindow` and `toggleGraal3DFullScreen`, calls `loadGraal3DEngine`, and re-registers a shorter callback set (window, player list, Flash, login, URLs). That shorter path does not call `graal_engineInitialize` again. The decompile tests the flag and never assigns it, so what sets it is not visible here.
- If a different flag is set, startup skips the forms and the engine initialiser and only calls `LoadLibrary` on the 3D DLL. That site does not resolve the exports. What sets this flag is not visible either.

Choosing a server whose name starts with `3 ` is handled in the engine, which then calls the launcher through `graal_setStartGraal3D` ([5007-engine.md](5007-engine.md#session)). The function the launcher passes into that setter was not recovered: the registration calls lose their arguments in this decompile. The only direct call of the full 3D load is the startup-flag path above. **[bin]**
