# GraalEngine.dll in Windows 4.2.0.8

Date: 2026-11-07. Static read of `GraalEngine.dll` from the unpacked 4.2.0.8 set. Nothing was run. Tags: **[bin]**.

The DLL is the session: input, the level, scripts, files and the Graal connection. It does not draw pixels. Each draw, text, tile and panel operation calls the host pointer installed by `graal_set…`, and does nothing when that pointer is empty. `GuiCanvas` is the screen object. This is the engine half of the split in `torque/4208-launcher.md`, and it confirms `torque/study-torque-clients.md`: Torque GUI classes, no console of its own. The packet-logger modification described in `protocol/v4x-clients.md` is not re-checked here. **[bin]**

## How a session runs

`TAdventure` is a small object. `loadGraalGui` creates the canvas first; `startOfflineMode` creates `TAdventure` if it does not exist, runs one timer tick, and loads `offlinetutorial.gmap`. **[bin]**

`renderGraalCanvas` calls `GuiCanvas::renderFrame`, which calls `TAdventure::timer` before it draws. The timer, about once a second while a flag is clear, compares a wall-clock millisecond count with `GetTickCount`. A difference of more than 100 ms increments a counter. On the third such gap it logs and calls a routine with a zero argument. The decompile does not name that routine. The timer then runs `handleClient`, walks a drawable list and calls each object's timer, and once a second snapshots three counters and clears them. **[bin]**

`handleClient` returns immediately when there is no client. Otherwise it clears a byte on every entry of `allplayers`, pumps the client, and if the client is marked disconnected it runs `clientDisconnected`. It then walks `allplayers` again. A second list drops an entry whose name is empty and whose timestamp is more than five seconds old. If that entry's id is above 99999 it fires `onPlayerLogout` on the universe, then deletes the entry. **[bin]**

`clientDisconnected` destroys the client. If the failure text is empty and the mode is 2, the text becomes a could-not-connect message. A mode of 2 whose server name is `Login` is treated specially: a saved address that differs from the current one is dialled again as `Login`. Otherwise the message is logged and the canvas content is set back to `MainMenuGui2D`. **[bin]**

Choosing a server pops `ServerListGui`. A name whose second character is a space has those two characters removed. A prefix test then selects the 3D path: the 3D flag is set, `StartScript_GraalGui3D` is loaded, and the connect-to-3D callback is invoked with the port plus one. Any other name clears the 3D flag and loads `StartScript_GraalGui`. The stored prefix bytes are not a recovered string, so this read does not repeat them; the two-character strip matches the `3 ` marker in `protocol/v4x-clients.md` and `torque/network.md`. **[bin]**

Keys arrive as `invokeGraalKeyboardEvent`, which builds an input event and gives it to `GuiCanvas::processInputEvent`. `TAdventure::invokeKeyPressed` ignores a zero key whose character is below the space character. Otherwise it builds a text of the key code, the character when it is printable, and a modifier, and posts event 16. Key-up clears one flag when the key byte is `0x32` and then releases the key. The decompile does not name that flag. **[bin]**

`invokeGraalMouseEvent` also becomes an input event. Button 0 is the unnamed button, 1 is `middle`, 2 is `right`. A release posts event 11. A press posts event 10, and when the click count is an even number of at least 2 it also posts `double` and `doublemouse`. In 2D a press converts the cursor with `getMouseLevelX` and `getMouseLevelY`, notifies the level, and if a client exists notifies the server with coordinates relative to the player's level origin. A per-player mode of 1, 2 or 3, behind a one-word decrypted flag, selects a warp, a right-click player test, or an early return. The decompile does not show the flag's meaning beyond that test. `handleMouseMove` in 2D, when a player bit is set, asks `getNearOtherListAsString` and shows the result as a canvas hint, or hides the hint when the list is empty. **[bin]**

`paintGraphics`, reached only from the unused `renderGraal` export, updates the drawable list and, when a debug flag is set, draws one shadowed line. It is not the frame. **[bin]**

## How a script runs

`TScriptExecutionSpace::executeScript` refuses a missing script, a missing owner, or an owner whose pause byte is set. It installs a `TGraalMachine` as `currentmachine`, binds the script buffer, and if the owner is a `TServerNPC` with a comma-text builds that text into the argument variable. It then runs the machine. A saved state can point at another object's space: the machine records the suspended event and asks that object to run it. `executeFunction` runs one function index on the same machine and, when asked, returns a new `TGraalVar` filled from the machine stack. A paused variable's `setPaused` also frees the space's pending actions. **[bin]**

`TGraalVar` is a named hash-list object. Its children live in a hash. Its class is another object, and `getVarType` reads that object's name. The script space hangs off the variable; `joinClass` and `leaveClass` create the space if needed. A variable marked static is added to the universe and removed from it on destruction. **[bin]**

A value has a kind. Kind 1 is a float: `writeFloat` stores the number and clears the string. Kind 2 is a string: `writeString` stores the text and also the result of parsing it as a float. Kind 3 is a link: `readFloat`, `readString` and `readObject` follow the linked variable, and `linkValueTo` refuses a link to itself. Reading a float with an empty string and a non-zero number formats the number, except a magnitude below 0.0001, which becomes the empty numeric text. An array is a list of cells. Each cell answers as a float, a string, or an object; an out-of-range index reads as 0, an empty string, or no object. `setVarValue` of one string splits on the first `=`. A static variable refuses `writeFloat` and `writeString` unless its class allows the write. The decompile does not show a single C union for the value; the kind and the three stores are the behaviour. **[bin]**

## How a show-image is drawn and attached

`TShowImg` is constructed with a `TServerLevel`. `showImage` sets the image type to 0 unless the type is already 3, in which case a different setter runs. `writeString` dispatches on the first character: `#` a polygon, `%` a textured polygon, `&` an animation, `@` text, a pound sign a shape, a sprite marker or a numeric string a sprite, and anything else an image. **[bin]**

`draw` calls the image child's draw and, if present, the particle emitter's draw. `addDrawObjects` copies a matrix onto the player. When a field on the show-image is greater than 9 it marks the player, scales and rotates by 16, and concatenates the image position. A non-identity scale or rotation on the child adds a further transform. `drawWithImgTransform` pushes that transform around the draw and pops it. `playAnimation` advances a spin while a rate is set, and while an attachment exists and a flag is set and the same field is below 10 it copies position from the attachment plus offsets. **[bin]**

The 3D object is separate. It stays empty until a shape string is assigned. The assignment calls the create-object host callback, stores the result, and sets the `shape` property on it. See `torque/4208-g3d.md`. **[bin]**

## How the canvas hosts the playfield

`GuiCanvas::renderFrame` sets the clip to the screen size, fits the main controls, checks the hint, forces the cursor on when the application is not active, runs the adventure timer, and pre-renders. Unless the caller asked to skip drawing, it walks the child list and calls render on each child that is visible. `renderGraalCanvas` passes "do draw". **[bin]**

`setContentControl` is how a script object becomes the screen. `MainMenuGui2D`, `GUIContainer` and `SetupDialog_Back` are installed that way, and a disconnect puts `MainMenuGui2D` back. **[bin]**

While the script builder is resolving a class, a class named `GuiGraalCtrl` or `GuiGraal3DCtrl` is discarded, so the script does not construct either type. Both names are engine types. The decompile does not show a separate render method under either name; they are drawn only if a script places one in the canvas child list. **[bin]**

## The order StartScript objects are created

`loadGraalGui`, when the canvas does not yet exist: **[bin]**

1. `StartScript_Profiles`. The script is decompressed into the variable, two virtual calls run, and the variable is destroyed. It is not added to the universe.
2. The `GuiCanvas`, then a `DefaultCursor` drawable from `defaultCursor.png`, set as the canvas cursor.
3. If a setup test fails, a setup helper and then `StartScript_SetupDialog`. That dialog becomes the content, and `SetupDialog_PathEdit` is filled. If the test passes, `StartScript_MainMenu` instead, and `MainMenuGui2D` becomes the content.
4. `StartScript_OptionsWindow`. Unlike the others it does not receive the second virtual call.
5. `StartScript_PlayerProfile`, `StartScript_LoadLevelGui`, `StartScript_QuitDialog`.
6. A pre-render call whose target the decompile does not recover.
7. `StartScript_MessageBoxDialog`, `StartScript_SelectFileDialog`.
8. `StartScript_MoveMap2D` and `StartScript_MoveMap3D`, which are created, run, and destroyed.

Each kept script is created only if the universe does not already have that name, marked static, filled from a decompressed buffer, and run. Calling `loadGraalGui` again, when the canvas exists, only rebuilds graphics if an adventure or a player exists, then runs the two move-map scripts again. **[bin]**

`StartScript_GraalGui` is not in that list. `startOfflineMode` and the 2D connect path load it, and the 2D path then makes `GUIContainer` the content. The 3D connect path loads `StartScript_GraalGui3D` instead. **[bin]**

## What is absent

No `SimObject`, no `SimGroup`, no console (`Con::` does not occur), no TorqueScript, and no `.dso`. `GuiCanvas`, `GuiControl` and `Point2I` are present and used. The 3D classes live in the other DLL. **[bin]**

In 3D mode, file fetches that 2D sends as client packets are script events instead: `getgani`, `getweapon` and `getclass` go through `SendGraal3DScriptEvent`. A client variable send does the same, under a name the decompile does not recover as text. A `serverside` weapon trigger whose argument list has more than one cell is sent as a `trigger` event with a `weapon:` prefix, again only on this path. The 2D path of each of those still builds a packet. **[bin]**
