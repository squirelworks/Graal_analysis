# GraalEngine.dll 5.0.0.7

Date: 2026-11-07. Static read of the engine decompile. Nothing was run. **[bin]**

The launcher beside this DLL is file version `5.0.0.7` ([5007-launcher.md](5007-launcher.md#startup)). This DLL defines the setters and the game. The 3D world is the other DLL ([5007-g3d.md](5007-g3d.md#gameobject)). **[bin]**

## Session

`TAdventure` is the level session. Its constructor initialises graphics and installs the status set `Online,Away,DND`. The global client pointer starts empty. **[bin]**

`connectToGraalServer` stores the server name, the host and the port and calls the connect routine. `openGraalServerList` does the same with the name `Login` when an account and a password are already set and no client exists yet. **[bin]**

The connect routine refuses to run while a busy flag is set. If the server name is longer than one character and the second character is a space, it deletes the first two characters. It then tests the original name against the prefix `3 `. **[bin]**

- When the prefix matches and 3D is not already on, it calls the launcher callback registered with `graal_setStartGraal3D`, passing the name, host and port. A non-zero return cancels the connect.
- It pops `ServerListGui` off `GuiCanvas` when that control exists, destroys any current client, and stores the name, host and port.
- For a `3 ` server it sets the 3D flag, remembers listed port + 1, and calls the callback registered with `graal_setConnectTo3DServer` with the host, that port and a flag.
- For any other server it clears the 3D flag and runs the Graal GUI host described below, then allocates the client object.

`TAdventure::timer` is the frame. It samples wall-clock milliseconds against `GetTickCount` about once a second. When those two diverge by more than 100, three times, it formats a message and passes it on; the callee was not read. It then calls `handleClient`, drains a pending connect list, ticks the draw list and the client, checks a queued secure URL, and if `GuiCanvas` exists calls its frame virtual. **[bin]**

`handleClient` returns when there is no client. It clears a per-object mark, and if the client's disconnect flag is still clear it keeps reading. A nested state of 4 that has lasted five seconds sets the disconnect flag. The flag calls `clientDisconnected`. Afterwards, a listed object with an empty name whose timestamp is more than five seconds old raises `onPlayerLogout` on the universe when its id is above 99999, and is deleted. **[bin]**

`clientDisconnected` destroys the client. If there was no message and the link state was 2, the text is `Couldn't connect to the server`. The message is shown when the caller asked for that. If the server name was `Login` and the link state was 1 or 2, it walks the stored login hosts and connects to the next one that differs. It also calls the callback registered with `graal_setRemoveGraal3DConnection`. **[bin]**

`graal_engineInitialize` records the exe path on the first call, checks that `license/sig.graal`, `license/sig.graallib` and `license/sig.license` exist, checks the exe and `GraalEngine.dll` against their signature files, and loads `license/license.graal` as lines (host, port, and further hosts). It deletes `graal4console.log` and `game_console.log` if they exist. The paths this decompile shows return success. A second call only initialises the script environment and returns success. **[bin]**

## How a script runs

A script object is a `TGraalVar`. `createScriptSpace` allocates a `TScriptExecutionSpace` and stores it on the var. `setScript` attaches the script text. `activateScript` adds the var to the universe's active list, at the front when the universe is not paused and the var's script id matches the current one. `runScript` on the var calls `runScript` on that space. **[bin]**

`TScriptExecutionSpace::runScript` returns immediately if the owner var is paused or its stop flag is set, or if there is no universe. It then updates classes and runs scheduled events. If a class download is still in progress it sets a flag and waits. When that flag clears it raises `onClassesDownloaded` and runs the owner's update. It then walks the action list and calls `executeAction` on each, stopping early if the owner is stopped, and frees the actions afterwards. While that walk runs it records elapsed time against the var's name, up to 10000 entries. **[bin]**

`executeFunction` takes a `TScriptFunction`, an argument var and a flag. It borrows a `TGraalMachine` from the universe, runs the function on that machine, and returns the machine to the free list. If the flag is set and the machine stops in state 3, it builds a result `TGraalVar` from the machine's stack. Otherwise the result is empty. **[bin]**

`setClasses` leaves every class, ensures a script is attached, splits the argument on commas, and `joinClass`es each name, then runs the class-update action. **[bin]**

`catchEvent` records an event the space wants. An empty target means the space's own owner. The target `universe` is the universe var. Any other name is looked up with `getVar`, and that var gets a script space if it has none. The event name is stored on the catching space. **[bin]**

`TGraalVar::executeFunction` is the var-facing wrapper. It finds the named function on the var or its classes and calls the space. `scheduleEvent` queues a later event; `receiveEvent` is what a raised event hits. The machine's opcode loop was not read. **[bin]**

## The Graal control

`GuiGraalCtrl`'s property table is parented on `GuiControl`. The constructor adds no properties of its own. **[bin]**

The 2D connect path builds the GUI like this. It finds or creates a static var named `StartScript_GraalGui`, decompresses an embedded buffer into that var with `setScript`, and calls two virtuals on it. It looks up `GUIContainer`, casts that `TGraalVar` to `GuiControl`, and if `GuiCanvas` exists calls `setContentControl`. It then looks up `GraalControl3D` and `GraalControl`, casts each to `GuiControl`, and passes them to two virtuals on the container. **[bin]**

When a script creates an object, the factory looks the type up by name. If the type is `GuiGraalCtrl` or `GuiGraal3DCtrl`, it drops the type record so the name is not constructed as an ordinary script object, unless the caller's flag says to keep it. A missing type adds a script error of the form couldn't create object, type is not existing. A new object is added to the universe's static objects and can inherit vars and a script space from the value it replaces. **[bin]**

`invokeGraalKeyboardEvent` and `invokeGraalMouseEvent` do nothing when `GuiCanvas` is null. Otherwise they fill an input event and call `GuiCanvas::processInputEvent`. Shift, control and alt are rewritten to the left-key codes before that. **[bin]**

## Setters the launcher does not resolve

This DLL defines `graal_engineInitialize` and 118 `graal_set*` functions. Each setter stores the function pointer it is given. The launcher resolves 95 of those setters ([5007-launcher.md](5007-launcher.md#what-it-resolves)). The other 23 are below. The 3D DLL calls 20 of them, passing its own routines, and also re-registers the shared draw and window setters before it calls `graal_engineInitialize` again ([5007-g3d.md](5007-g3d.md#gameobject)). **[bin]**

The 3D DLL is the only caller of these. **[bin]**

| Job | Setters |
|---|---|
| Connect | `graal_setConnectTo3DServer`, `graal_setRemoveGraal3DConnection`, `graal_setRemoveGraal3DMissionGroup`, `graal_setOnGraalFileDownloaded` |
| World | `graal_setCreateGraal3DGameObject`, `graal_setDeleteGraal3DLightInfo`, `graal_setGetGraal3DTerrainHeight`, `graal_setGetGraalPlayerScriptObject`, `graal_setFreeGraalTexture` |
| Script and text | `graal_setSendGraal3DScriptEvent`, `graal_setSendGraal3DScriptEvents`, `graal_setSendGraal3DServerText`, `graal_setLogGraalMessage` |
| Window and cursor | `graal_setIsOpenGLEnvironment`, `graal_setGetAllowCursorOff`, `graal_setGetHardwareCursorVisible`, `graal_setSetGraalFullScreenMode`, `graal_setSetGraalWindowLocked`, `graal_setSetGraalWindowMode`, `graal_setSetMinimumFrameTicks` |

`graal_setLogGraalMessage` is one the 4.2.0.8 launcher still resolved. This launcher does not ([5007-launcher.md](5007-launcher.md#what-it-resolves)). **[bin]**

Defined here and called by neither host in this export: `graal_setOpenExternalHistory`, `graal_setOpenExternalLogWindow`, `graal_setOpenExternalPM`. The 4.2.0.8 launcher did resolve those three. **[bin]**

## No SimObject and no .dso

`SimObject`, `.dso`, `ActionMap`, `GameConnection`, `ShapeBase` and `OpenGLDevice` do not occur in this DLL. Torque that is compiled here is the GUI and the math: `GuiCanvas`, `GuiControl`, `GuiControlProfile`, `GBitmap`, `MatrixF`. `GameObject` is not a class body in this DLL. It is the setter `graal_setCreateGraal3DGameObject`, which the 3D DLL fills in. **[bin]**
