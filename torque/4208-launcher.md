# Windows 4.2.0.8 launcher

Date: 2026-11-07. Static read of the unpacked Delphi launcher whose version resource is Graal 4.2.0.8, together with the calls it makes into `GraalEngine.dll` and `Graal3DEngine.dll`. Nothing was run. Tags: **[bin]**.

Windows 4.2.0.8 is three programs: a Delphi launcher, `GraalEngine.dll` for the session, and `Graal3DEngine.dll`, which replaces the draw callbacks when a 3D server is started. The packed exe listing is a different file, the Thinstall loader (`torque/skipped-v4-read.md`). This note is the unpacked launcher. The engine is the packet-logger build in `protocol/v4x-clients.md`; that note's third-party change is the signature check, which this read did not re-open.

This confirms the era-B split in `torque/study-torque-clients.md`: the launcher owns the window and DirectDraw, and the engine draws only by calling back. **[bin]**

## Who owns the window

Startup is a Delphi application. It creates the usual application window, then a set of forms, and sets the main form's caption from the spaced title "G r a a l". The message loop is the application's. A method pointer on the application object receives keyboard messages for the main form's window (and for one other window the code compares against the form handle). That hook accepts key-down, key-up, character and system-key messages, skips system keys whose virtual key sits in the F-key range, runs `ToAscii` on a key-down, and forwards the key into the engine. One configured virtual key is also reported as the microphone key. **[bin]**

`-window` takes the next argument as a window handle. If that window has a real rectangle, the launcher sizes itself from it; an empty rectangle becomes 640 by 480. Flash and the same external-window path parent to that handle when it is set, and to the main form when it is not. The decompile does not show the 3D DLL creating a second top-level window during its load. It does register window-mode and fullscreen callbacks, so those changes are no longer the launcher's once 3D has started. **[bin]**

The command line also accepts `-setup`, `-silentsetup`, `-connect` plus a name, `graal://` (eight characters stripped), `graal3://` (nine characters stripped), `-listscriptfunctions`, `-error`, `-message`, `-startedbyexereplacer`, `-opengl` and `-guestaccount`. The branch polarity of those tests is not trustworthy in this decompile: one stale flag is reused for every comparison. The strings and the strip lengths are. **[bin]**

If engine initialisation returns failure, the launcher shows a warning that the execution file should be checked (virus checker, drivers) and does not enter the form loop. **[bin]**

## When drawing happens

The launcher resolves `renderGraal` and `renderGraalCanvas`. `renderGraal` has one reference, the resolve itself: this launcher never calls it. `renderGraalCanvas` is called from the main form's frame method. **[bin]**

That method advances a frame counter, adds 50 to a tick, and treats the form as paintable when it is visible. On a system whose version is above 4 it also requires `SwitchDesktop` of the thread's desktop to succeed, and clears the paintable flag when that fails. With an external window it treats the frame as paintable and, the first time, copies that window's size (again 640 by 480 if the rectangle is empty). While a mode byte is clear and the frame is paintable, a gate function must also agree; then the launcher calls `renderGraalCanvas`. The same method still walks scripted controls, the microphone key and the external windows in both modes. The decompile does not show what stores the mode byte, and it does not show what calls the frame method. The keyboard hook is a different function. **[bin]**

`renderGraalCanvas` asks `GuiCanvas` to render one frame, which runs `TAdventure::timer` and then each visible child's render. Tile, text, image and panel pixels leave through the host callbacks the engine invokes during that walk. In this launcher those callbacks are the DirectDraw 7 device (`DirectDrawCreateEx`, `IDirectDraw7`, a surface, a clipper and a palette). The registration calls do not recover the Delphi function pointer for each slot, so the per-slot body is not named here. **[bin]**

## The 94 slots, by job

Loading `GRAALENGINE.DLL` resolves 94 `graal_set` exports. A later call invokes each one. Those calls do not show their arguments. On the engine side each export stores one function pointer, and the matching draw helper calls it only when the pointer is set. **[bin]**

**Tiles.** Create, delete, resize and scroll a tile buffer; draw and clear a 2D tile; draw and clear a 3D tile; begin and end a tile batch; draw the buffer on screen. The engine's 2D-tile helper passes six arguments. **[bin]**

**Text and pictures.** Draw text and shadowed text; measure width, height, ascent and descent; draw a graphic and a stretched graphic; fill a screen rectangle; draw two kinds of line and a polygon; read a texture's width, height and one pixel; test a pixel and a rectangle for transparency; read bitmap-array rectangles. Screen width and height, and the clip rectangle, are the same family. **[bin]**

**A 2D matrix.** Push, pop, test and read a 2D matrix. This is the extra set `torque/study-torque-clients.md` already listed for 4.20r8. The launcher resolves it; the decompile does not show the launcher applying a matrix of its own. **[bin]**

**Panels.** Create and delete a drawing panel; draw a graphic, a stretched graphic, a palette image and raw pixels into it; fill a rectangle; draw the panel; draw a triangle strip; save the panel. **[bin]**

**Flash.** Create and delete a panel, set its size, file, visibility and looping, play and stop, get and set a Flash variable, call a Flash function, and push a Graal variable in. The control is an ActiveX object. Its version, divided by 65536, must be at least 7. Below that the launcher logs that the Flash control failed to load and records the version it found, and it does not keep the control. A kept control is parented to the main form or to the external window, given a fixed style, and stored in a list. **[bin]**

**Clipboard.** Set and get. The launcher opens the clipboard on a window handle, empties it, and reads and writes text formats (format 1 and format 9). **[bin]**

**The rest of the shell.** These are not drawing. External player list (open, update, delete), external PM, history and profile, options, message box, two URL openers, the path dialog, the log window, file-scan progress, a file-update notice, language and a translation URL, status icons, a screenshot, the action-key text, the virtual-key code, whether the application is active, microphone required / activated / volume, log a message, receive server text, server login, and the server-lister connect. Shutdown is two steps, prepare and then shut down. `graal_setStartGraal3D` is the engine asking the launcher to bring the 3D DLL in. **[bin]**

## Starting 3D

`GRAAL3DENGINE.DLL` is loaded only on the 3D path. The launcher shows a progress form whose text is "Starting Graal3D...", hides the form's cancel control, reinstalls the host callbacks, sets a flag, and resolves `loadGraal3DEngine`, `runGraal3DEngine`, `endGraal3DEngine`, `resizeGraal3DWindow` and `toggleGraal3DFullScreen`. If no external window was given it reads the main form's handle first. It then calls `loadGraal3DEngine`. The decompile does not show that handle being passed in. It then reinstalls only the non-drawing slots: scripted controls and the player list, the log, the external windows, the microphone, server text, login, the lister, options, the message box, status icons, both URL openers, the log window, the application-active query, the file-scan message, and every Flash slot. Drawing, tiles, text, panels, the matrix, clipboard, clipping and the screen size stay with whoever `loadGraal3DEngine` registered, which is the 3D DLL. The progress form is then hidden. **[bin]**

The flag that selects this path before the message loop is only read. The decompile does not show who sets it. The engine's own decision, once a name is chosen, is in `torque/4208-engine.md`. **[bin]**

`runGraal3DEngine` is resolved and this launcher never calls it. **[bin]**
