# GraalEngine.dll 5.0.0.7

Date: 2026-11-07. Static read of the decompile in the v5 export. Nothing was run. **[bin]**

The launcher's version resource is `5.0.0.7` ([launcher-5007.md](launcher-5007.md#what-the-decompile-is)). This DLL's decompile has no file-version string. Its source paths sit under a graallib tree on a fixed drive. **[bin]**

## Graal's game

The DLL defines the Graal types. `TAdventure` has constructors and methods (`localToScreenY`, `getMouseLevelX`, `getMouseLevelY`). Also present: `TGraalVar`, `TScriptExecutionSpace`, `TShowImg` (Flash, gani, image, poly, shape, text), `TGraalAni` and its part, sound, sprite and step types, `TGraalUniverse`, `TPlayer`, `TServerPlayer`, `GuiGraalCtrl`, `GuiGraal3DCtrl`. **[bin]**

Level and cache magics in the string table: `GR-V1.00` through `GR-V1.05`, `Z3-V1.03`, `Z3-V1.04`. License paths: `license/license.graal`, `license/sig.graal`, `license/sig.graallib`, `license/sig.license`. The console log name is `graal4console.log`. FMOD is used by name (`Failed to open fmod audio`); the separate `fmod.dll` in this export is a packer stub ([stub-fmod-5007.md](stub-fmod-5007.md#what-the-decompile-is)). **[bin]**

No `G3D` login-token literal is in the string table. **[bin]**

## Torque that remains

Torque's GUI is compiled in. `GuiCanvas` methods are defined here (`setRenderFront`, `isCursorON`, `setCursorPos`, and others), along with `GuiControl`, `GuiScrollCtrl`, `GuiWindowCtrl`, `GuiControlProfile`, `GBitmap` and `MatrixF`. **[bin]**

Absent from this DLL: `SimObject`, `GameConnection`, `ActionMap`, `.dso`, `OpenGLDevice`, `ShapeBase`. `GameObject` appears only as the `graal_setCreateGraal3DGameObject` setter, not as a Torque class body. The 3D world is the other DLL ([g3d-5007.md](g3d-5007.md#torque-that-is-still-here)). **[bin]**

## Who registers the setters

`graal_engineInitialize` and 118 `graal_set*` functions are defined here. Each setter stores the function pointer it is given. The engine is the registration API. The launcher and `Graal3DEngine.dll` call the setters; they do not define them. **[bin]**

### Who calls the setters

| Who | What it does with `graal_set*` |
|---|---|
| This DLL | Defines all 118 setters and `graal_engineInitialize`. |
| Launcher | Resolves `graal_engineInitialize` and 95 setters by name. |
| `Graal3DEngine.dll` | Calls 78 setters, then calls `graal_engineInitialize`. |

Every name the launcher resolves, and every name the 3D DLL calls, is defined here. **[bin]**

The launcher alone names 37 setters: Flash panels, the external player list, options, profile and message box, starting and ending a tile draw, whether the application is active and whether it is fullscreen, the microphone, the server-list connect, server login and received server text, language, status icons and a translation URL, the file-scan message, the path dialog, showing the window, starting 3D, and setup mode. A rebuild of that host needs `graal_setStartGraal3D`, `graal_setOnServerLogin`, `graal_setOnServerListerConnect` and `graal_setShowGraalWindow` from this group. **[bin]**

The 3D DLL alone names 20 setters: connecting, creating the 3D game object, lights, textures, the cursor, terrain height, the player script object, whether this is an OpenGL environment, a log line, a finished file download, removing the connection and the mission group, one script event and a batch of them, server text, fullscreen, the window lock, the window mode, and the minimum frame ticks. A rebuild of that host needs `graal_setConnectTo3DServer`, `graal_setCreateGraal3DGameObject` and `graal_setIsOpenGLEnvironment`. **[bin]**

Three setters are defined here and named by neither host: opening an external history, an external log window, and an external private-message window. **[bin]**

Both hosts name the other 58 setters. That shared draw set is tiles (draw, clear, a buffer, scroll, size, delete and clip, in 2D and 3D), text and graphics, pushing and popping a 2D matrix and a colour matrix, panels, the clipboard, the home directory, two URL openers, a file-update notice, and shutdown in two steps (prepare, then shut down). **[bin]**
