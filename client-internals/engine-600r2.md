# Windows 6.00r2: Graal's own engine

Date: 2026-11-07. Static read of the unpacked `GraalSetup` export whose version resource says product Graal, product version 6.002, company Linux Cyberjoueurs. The image carries the compiler date 12 June 2011 and the time 18:47:49. Nothing was run. Tags: **[bin]**.

The paired build two weeks later is `engine-600r4.md`. Protocol for this generation stays in `protocol/v6x-clients.md` and `protocol/v5v6-windows-unpacked.md`.

## What the export is

One native Windows program. Source paths are `quattro_lib` (DES, JPEG 2000). The play side uses the name `Quattro_Play`. There is no Delphi launcher and no second engine DLL. `ExeReplacer.exe` is still started for the package update; a failure is reported as not being able to start it. **[bin]**

The dump still ends in the packer's dword loop. That loop is the stub, not the client. The engine is the `quattro_lib` body. **[bin]**

## No Torque 3D

Absent, as names and as code: `GameConnection`, `TerrainBlock`, `Interior`, DTS, `SimObject`, `SimGroup`, `NetConnection`, Torque console, TorqueScript, datablocks, `.mis`, `.ter`, `.dts`, `.dif`, `.dso`. No SDL. **[bin]**

`GuiGraal3DCtrl` is not an unused leftover and not a Torque viewport. The GUI walk compares a control's type with `GuiGraalCtrl` and with `GuiGraal3DCtrl`, and drops either one when a flag on the parent is clear. Both names are the playfield control. **[bin]**

## How the program is split

Four pieces, all in this executable. **[bin]**

- **Drawing.** OpenGL, with a Direct3D 9 device created first so the script can read adapter capabilities. Named passes cover the world, then the GUI.
- **GUI.** GS2 controls. Torque's control class names are the vocabulary. Graal's own controls are the playfield, show-images, PM, start menu and the rest below. The shell dialogs are scripts (`StartScript_GraalGui`, profiles, connect message, message box, setup, file select, file scan).
- **Script.** `TGraalVar` values, classes, and the world types (`TServerPlayer` and the other `TServer*` objects). A profiler times script and the draw passes.
- **Network.** `TSocket` for the game session. `THTTPRequest` and `TRTMPClient` are separate. There is no Torque UDP connection.

## Drawing

Startup loads `d3d9.dll` and calls `Direct3DCreate9`. Failure text is "Failed to create DirectX9 device". The script-visible window object `TWindow` reports the graphics card, driver, hardware flag, maximum texture size, non-power-of-two textures and "DirectX9 capabilities", plus the screen size and the fullscreen modes. **[bin]**

The frame is OpenGL. `TWindowOpenGL::setScreenMode` has its own failure text. The image logs "Initialized OpenGL." Shaders are ARB program objects: `.vert` and `.frag` files, compile and link logs, and a default set (texture, alpha test, cull, colour array, fixed colour) with uniforms for two textures, the model and projection matrices and a fixed colour. Framebuffer and renderbuffer entry points are loaded by name. The switch list includes `-opengl` and `-window`; no call site for `-opengl` was recovered past that list. **[bin]**

World and GUI are separate passes. The world passes are `Game_Draw`, `Game_Draw_GetDrawObjects`, `Game_Draw_Player` and `Game_Draw_Texts`. Then `Draw_Tiles`, `Draw_ShowImg`, `Draw_Particles`, `Draw_Polygon` and `Draw_Clip`. `RenderGUI` is its own scope, and each control type has a `Draw_*` routine (`Draw_WindowCtrl`, `Draw_ScrollCtrl`, `Draw_MLTextCtrl`, `Draw_GuiShowImgCtrl`, and the button, bitmap, text and slideshow routines). Those names are registered once, the same way the script profiler names a scope. **[bin]**

Sound is FMOD (open failure, EAX misuse, music metadata, play at a point or at the player). Not SDL_mixer. Video is optional FFMPEG (`avcodec-51.dll`, `avformat-51.dll`, `avutil-49.dll`) for FLV and a recorded take, including a path that refuses flash-video encoding. **[bin]**

Images include PNG, GIF, JPEG and JPEG 2000. The JPEG 2000 decoder is JasPer, compiled inside `quattro_lib`. Levels are `GR-V1.00` through `GR-V1.05`. Packages are `GRPKG001`. The script cache magic `GRESCR01` is present. bzip2's own banner is 1.0.4, 20 December 2006. **[bin]**

## GUI and script objects

The shell is not a built-in form. Startup builds script objects `StartScript_Profiles`, `StartScript_GraalGui`, `StartScript_MessageBoxDialog`, `StartScript_SetupDialog`, `StartScript_SelectFileDialog`, `StartScript_FileScanDialog` and the connect message. The server list and account screens are that GUI. `ChatBar` is the name the engine looks up for chat, as in the later 5.x/6.x lab notes. **[bin]**

A control is a script object: events such as `onWake`, `onShow`, `onHide`, `onAction`, mouse and key events, and first-responder events (`onBecomeFirstResponder`, `onLoseFirstResponder`, `onFirstResponderChanges`). There is no `makeFirstResponder`, and no `horizSizing`, `vertSizing`, `minExtent`, `fontType`, `fillColor` or `pushToBack`. Profiles remain (`GuiControlProfile`, `GuiDefaultProfile`, hint and menu profiles) and drawing reads `profile.fontcolor`, alignment and an opaque fill. **[bin]**

`GuiTilesCtrl` is not in this image. Tiles are the `Draw_Tiles` pass. **[bin]**

| Class | What it does |
|---|---|
| `GuiGraalCtrl` | Playfield. Its text says whether the game is rendered. The GUI walk treats it as the game view. |
| `GuiGraal3DCtrl` | Same walk as `GuiGraalCtrl`. No scene graph behind the name. |
| `GuiShowImgCtrl` | Draws a show-image. World object `TShowImg`; one flag name is `forceaboveterrain`. |
| `GuiPMCtrl`, `GuiPMEditCtrl`, `GuiPMHistoryCtrl` | Private messages: compose, history, append a received PM. |
| `GuiStartMenuCtrl` | Start menu (places, programs, user pane) and `GuiTaskbar`. |
| `GuiAccountPasswordCtrl` | Account password field. |
| `GuiSlideShowCtrl` | Animates slides. |
| `GuiAccordionCtrl` | Accordion of entries. |
| `GuiAnimationCtrl` | Moves an entry; `onAnimationStart` / `onAnimationEnd`. |
| `GuiDrawingPanel` | Script drawing surface: image, line, curve, text, filters. |
| `GuiWindowCtrl`, `GuiScrollCtrl`, `GuiMLTextCtrl`, `GuiButtonCtrl`, `GuiTextEditCtrl`, `GuiTextListCtrl`, `GuiCheckBoxCtrl` and the other `Gui*` controls | Torque's names, each with its own draw routine and the events above. |
| `TWindow` | Display size, fullscreen modes, devices, DirectX 9 capabilities. |
| `TGraalVar` | Script value: arrays, join a class, timeouts, load and save XML and INI. `TScriptUniverse` and `TScriptFunction` are the class machine. `TActionScriptVar` and `MovieClip` (`onEnterFrame`, `onPress`) are the ActionScript-compatible surface. |
| `TServerPlayer`, `TServerNPC`, `TServerLevel`, `TServerLevelLink`, `TServerWeapon` | The online world the script sees. |
| `TServerBomb`, `TServerCarry`, `TServerChest`, `TServerHorse`, `TServerSign`, `TServerLeap`, `TServerFlying`, `TServerExtra` | Level objects. |
| `TBaddy`, `TExplosion`, `TLevelObject`, `TDrawableObject` | Baddy, explosion, and the drawable base. |
| `TGaniObject`, `TGraalAni` and its part, sprite, sound and step types | Gani playback. |
| `TSocket` | Script socket: connect, bind, accept, close. |
| `THTTPRequest` | HTTP/1.0 fetch and redirects. Objects are named with an `HTTP_` prefix. |
| `TRTMPClient`, `TRTMPStream` | RTMP handshake, publish, remote call, metadata, record to FLV. |

`MissionGroup` is looked up by that name as a script object. It is not a `SimGroup`. **[bin]**

One registered builtin is described as changing the colour of the 3D terrain. The event `onMouseYawPitch` is described as the mouse moving in 3D mode, with yaw and pitch. `levels3d` is still a content folder beside `levels/` and `translations/`, and beside shapes and update packages. `graal3://` sits in the option-string list next to `graal://`, `-connect`, `-rtmp` and `-stream`; no call site was recovered for it. **[bin]**

## Network

The game session is the Graal socket, not Torque. Script events are `onConnectingToServer` (server name and address), `onConnect`, `onConnectFailed`, `onServerLogin`, `onPlayerLogin` and `onServerListerConnect` (the text calls it the server-lister). Status text includes connecting to the login server and connecting to the game server. The server name `Login` is present. Outgoing data that contains a newline is refused with "Illegal characters in the outgoing data", and incoming data can be "Received illegal data". **[bin]**

`resolveHost` is not in this build (it appears in 6.00r4). Crypto sources named in this image are `quattro_lib` `des.c`, `rsa.c` and `sha1.c`. **[bin]**

## What Torque names remain

Live GUI vocabulary, not a Torque subsystem: the `Gui*` control classes and `GuiControlProfile`, each implemented here with a draw routine. Live but not a 3D engine: `GuiGraal3DCtrl` (playfield type), `MissionGroup` (script object name), `onMouseYawPitch` and the 3D-terrain colour builtin (script text), `levels3d` (folder), `graal3://` (option string). **[bin]**
