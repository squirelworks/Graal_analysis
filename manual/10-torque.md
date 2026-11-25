<!-- manual: kind=reference status=draft -->
# 10 Torque-era 3D (3.x to 5.12)

From 2004 to 2007 the Graal client was built on GarageGames' Torque Game Engine (TGE). Torque gave the console, the script VM, the GUI, the resource manager, the renderer and, for 3D servers, the UDP netcode; Graal's 2D game, GS1/GS2 and the Graal TCP protocol stayed native code on top. The February 2000 DirectX Graal3D is unrelated (→ §9).

> Status: draft.

## 10.0 Reading this Part

The Torque years are best understood as three different programs that share the name "Graal" and some of the same code. Before treating any table below as describing "the 3.x–5.x client", fix which of the three a build is. [bin] (torque/study-torque-clients.md#1-the-short-answer)

**First, the monolith.** The 3.x clients (3.04 Linux, 3.151 Linux, 3.153 Mac) are Torque applications. TGE boots them, compiled TorqueScript draws every menu, and Torque's canvas holds the screen. Graal's 2D game is one native GUI control, `GuiGraalCtrl`, inside that canvas. The engine reports TGE version 1100 and still carries the stock game classes it does not use. [bin] (torque/study-torque-clients.md#1-the-short-answer); [bin] (torque/engine-304.md#the-split) 3.04 has none of Graal's net-layer changes. 3.153 already has them, which makes 3.153, not 3.04, the first build whose UDP wire a compatible 3D server has to speak. [bin] (torque/wire-by-build.md#the-handshake-per-build)

**Second, the split programs.** From 4.04r2 to 5.12 on Windows, a Delphi launcher drives `GraalEngine.dll`, a C++ 2D engine that keeps Torque's GUI classes but draws only through callbacks into its host. Torque proper survives only in the optional `Graal3DEngine.dll`, which takes over drawing when the player joins a 3D server. [bin] (torque/study-torque-clients.md#1-the-short-answer); [bin] (torque/engine-4208.md#how-the-three-fit) Inside this era the 3D DLL changes character. 4.04r2's DLL is near-stock TGE with datablocks and `Player`. By 4.20r6 that game layer is gone and every 3D thing is a Graal `GameObject`. The break falls between the February and July 2006 tokens. [bin] (torque/engine-and-formats.md#which-torque); [bin] (torque/wire-by-build.md#the-handshake-per-build) So "the 4.x 3D client" is two incompatible object models, and the protocol number (19, 21, 24) is the reliable way to tell them apart. [bin] (torque/network.md#the-connect-request-by-version)

**Third, after Torque.** From 5.24r3, and in every 6.x build, there is no Torque engine. What survives is the GS2 GUI vocabulary: Torque's control class names, plus its field names up to 5.31r4, re-implemented by Graal's own `quattro_lib`. [bin] (client-internals/torque-surface-by-era.md#530r3-and-531r4); [bin] (client-internals/torque-surface-by-era.md#600r2-and-600r4) The 6.x reads gathered in §10.1.6 and §10.1.9 are here to document that absence. The 6.x engine itself is Part I's subject (→ §1.8.7).

**What is measured, and what is not.** The UDP handshake is the strongest material in this Part. 5.12 was driven live against a lab server through challenge, connect, accept and its first data packets, and the minimal accept it takes is known. [run] (torque/network.md#the-full-handshake-live) Everything after the accept rests on static reads, and no Graal client has been seen drawing a 3D world: under Wine, 5.12's launcher faults when it switches to 3D. [run] (torque/engine-and-formats.md#rendering) No 3D content shipped with any client, because missions, terrain and shapes always came from the server, and no Graal 3D server or level data is in the archives. [file] (torque/engine-and-formats.md#3d-resource-formats) The open points that would change an implementation are listed in §10.3.2–E#503: the 4.04r2 class CRC, and whether 4.04r2 loads `.mis` and `.dso` files.

**How the later sections are scoped.** §10.7.1 to §10.7.6 record exact-build observations on Linux 3.04 and 4.20r6: script reading, packaged streams, a seven-operation executor subset and native-call boundaries. Each is deliberately narrow. A finding there holds for that input and that path, and it is not a general statement about TorqueScript execution in Graal. [bin] (torque/linux-304-seven-operation-contract.md)

## 10.1 Engine lineage

### 10.1.1 Builds

The Torque era spans several builds and platforms. Each row gives one build with its date, its shape, how much of Torque it carries, its 3D world, its game string and its menu scripts [bin] (torque/wire-by-build.md#which-builds-are-torque).

| Build | Date | Shape | Torque part | 3D world | Game string / protocol | Menu scripts | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1998 to 2.31 | — | Delphi | none | none | n/a | n/a | [bin] (torque/wire-by-build.md#which-builds-are-torque) |
| 3.04 Linux | Jan 2004 | one C++ binary (SDL 1.2, FMOD 3.70; [build and linkage](../client-internals/linux-304-executable-build.md)) | full TGE, version number 1100 | TGE classes, no 3D scripts shipped | `Torque Game Engine Demo` / 9 | TorqueScript `.dso` | [bin] (torque/README.md#lineage-at-a-glance) |
| 3.153 Mac | Feb 2005 | one C++ binary (Carbon, PPC) | full TGE with Graal's net-layer changes | stock TGE world and `main3D.cs` client scripts | `Graal3D` / 19 | TorqueScript `.dso` | [bin][file] (torque/README.md#lineage-at-a-glance) |
| 4.04r2 Win | Mar 2006 | Delphi launcher, `GraalEngine.dll` (2D) and `Graal3DEngine.dll` (3D plug-in) | 2D engine on Torque base classes; the 3D DLL near-stock TGE | stock TGE with datablocks | `Graal3D` / 19 | GS2 and native | [bin] (torque/README.md#lineage-at-a-glance) |
| 4.20r6 Mac | Dec 2006 | one C++ binary (PPC) | Torque core and netcode, Graal game layer | `GameObject` model, no datablocks | `Graal3D` / 24 (a lab copy labelled Mac 4.20r6 with protocol 21 is the Mac 4.11 build) | GS2 and native | [bin] (torque/wire-by-build.md#which-builds-are-torque); [bin] (torque/3d-engines-5007-512-and-403-411-2026-11-25.md#t3d-004-linux-and-mac-against-their-windows-twins) |
| 4.20r8 Win | Jan 2007 | 2D engine on Torque base classes | — | packet-logger upload has no `Graal3DEngine.dll` (later file-version 4.2.0.8 export: → §10.1.5) | unmeasured | GS2 and native | [bin] (torque/wire-by-build.md#which-builds-are-torque) [bin] (torque/engine-4208.md#how-the-three-fit) |
| 5.12 Win | Oct 2007 | Delphi launcher and one engine DLL, still named `Graal3DEngine.dll` | Torque core and netcode; the game layer is Graal's own | `GameObject` and `GameShape*`, no datablocks, no `Player`/`ShapeBase` | `Graal3D` / 24 | GS2 and native | [bin] (torque/README.md#lineage-at-a-glance) |
| 5.24r3 and later | 2010+ | engine linked into `Graal.exe` | no Torque 3D (what Windows 6.00 still names → §10.1.8) | none | n/a | GS2 | [bin] (torque/engine-and-formats.md#which-torque) |
| 6.x | 2010–2014 | native C++ per platform | no Torque 3D; GS2 keeps Torque control names (→ §10.1.8) | none | n/a | GS2 | [bin] (torque/README.md#lineage-at-a-glance); [bin] (client-internals/engine-600r2.md#what-torque-names-remain) |

### 10.1.2 Engine version and changes

The facts below give the Torque version each build reports and what Graal changed or added to the engine [bin] (torque/engine-and-formats.md#which-torque).

| Fact | Source |
| --- | --- |
| 3.04 reports version 1100 (formatted "1.100"), uses TGE's default game string, the home folder `~/.garagegames/` (3.151 changed it to `~/.graal`) and TGE source paths, so 3.x is built on a TGE 1.1–1.2 era code base | [bin] (torque/engine-and-formats.md#which-torque) |
| 3.153 is the same engine for PowerPC and Carbon, plus the community resources `AdvancedCamera`, `fxFoliageReplicator`, `twSurfaceReference` and `volumeLight`, a 3D Studio loader and a Quake 3 `.md3` loader | [bin] (torque/engine-and-formats.md#which-torque) |
| The 4.04r2 `Graal3DEngine.dll` is near-stock TGE (`Player`, `AIPlayer`, vehicles, projectiles, `InteriorInstance`, `TSStatic`, the `fx*` replicators, every matching datablock) and imports 623 symbols from `GraalEngine.dll` | [bin] (torque/engine-and-formats.md#which-torque) |
| The 4.04r2 DLL matches open TGE 1.x in its out-of-band packets, packet header, Huffman table, rate limits, DTS/DIF/TER versions and class list, and lacks TGE 1.4's lighting, so it is of the TGE 1.2/1.3 line | [bin][inf] (graal3d/torque-engine-4x.md#torque-version) |
| 5.12 keeps Torque's core (console, sim objects, `NetConnection`/`GameConnection`, ghosting, `SceneObject`, terrain, interiors, DTS, sky, sun, water, the editors) but drops the TGE game layer: no datablocks, no `GameBase`/`ShapeBase`/`Player`, vehicles, projectiles, items, `ScriptObject` or audio emitters | [bin] (torque/engine-and-formats.md#which-torque) |
| 4.20r6 already has the 5.12 model, so the TGE game layer was dropped between 4.04r2 (Feb 2006 token) and 4.20r6 (Jul 2006 token) | [bin] (torque/wire-by-build.md#the-handshake-per-build) |
| 3.04 has no Graal changes in Torque's net layer and none of the Graal net classes | [bin] (torque/wire-by-build.md#the-handshake-per-build) |
| Graal's net-layer changes (class table in the accept, 12-bit class ids, 14-bit length prefixes, BigData and terrain events) are already in 3.153 | [bin] (torque/wire-by-build.md#the-handshake-per-build) |

The Graal changes a compatible peer adds to open TGE [bin] (graal3d/torque-engine-4x.md#torque-version):

| Change | Source |
| --- | --- |
| a class table in the connect accept, with 12-bit class ids in the server's numbering (→ §10.3.3) | [bin] (graal3d/torque-engine-4x.md#torque-version) |
| a 14-bit length prefix on every event, ghost update and datablock | [bin] (graal3d/torque-engine-4x.md#length-prefixes-graal-change) |
| a class id on every ghost update and a raw index width | [bin] (graal3d/torque-engine-4x.md#ghosts-graal-changes) |
| 12-bit datablock ids (TGE uses 10) | [bin] (graal3d/torque-engine-4x.md#events) |
| a server time and client-reported state in the game packets (→ §10.3.5) | [bin] (graal3d/torque-engine-4x.md#server--client-data-packet) |
| mission acks without a sequence number (4.04r2) | [bin] (graal3d/torque-engine-4x.md#mission-start) |
| the BigData and terrain events (→ §10.5.3) | [bin] (graal3d/torque-engine-4x.md#graal-events-and-text-big-data-channel) |
| GS2 in place of TorqueScript, from 4.x on | [bin] (graal3d/torque-engine-4x.md#overview) |

### 10.1.3 Rendering

The facts below give the display devices every build has and how each platform draws [bin] (torque/engine-and-formats.md#rendering).

| Fact | Source |
| --- | --- |
| Every build has Torque's display devices: OpenGL, a Direct3D wrapper (`opengl2d3d.dll` / `glu2d3d.dll`) and Voodoo2 (full screen only); the minimum mode is 640×480 | [bin] (torque/engine-and-formats.md#rendering) |
| 3.x uses SDL and OpenGL on Linux, AGL and DrawSprocket on Mac; 4.x and 5.12 on Windows draw 2D with DirectDraw/Direct3D 7 in the Delphi launcher and host the Torque canvas for 3D (`GuiGraal3DCtrl`) | [bin] (torque/engine-and-formats.md#rendering) |
| In 4.04r2 the loaded plug-in registers its own handler for every drawing callback of the 2D engine, so in 3D mode the Torque DLL owns the window and the 2D game draws through Torque's canvas | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |
| Scene lighting is Torque's, cached per mission and run as the last mission-load phase | [bin] (torque/engine-and-formats.md#rendering) |
| Under Wine with software OpenGL the 5.12 Torque side starts on switching to 3D, but the launcher faults re-initialising DirectDraw and stops driving the engine's frame export; the 3D view was not seen | [run] (torque/engine-and-formats.md#rendering) |

### 10.1.4 Era A: what 3.04 contains

3.04 Linux compiles stock TGE beside a Graal game. The stock game classes are still in the binary; Graal's 2D game is the console class `GuiGraalCtrl`, not a replacement of `Player`. [bin] (torque/engine-304.md#the-split)

| Fact | Source |
| --- | --- |
| `GuiGraalCtrl` registers 31 methods, in order `moveUp`, `moveLeft`, `moveDown`, `moveRight`, `doA`, `doS`, `doD`, `doQ`, `doP`, `doM`, `doMicro`, `setChat`, `setPassWord`, `openServerList`, `selectServer`, `selectServerCategory`, `startOfflineMode`, `connectToSelectedServer`, `serverDirectConnect`, `privateMessageSend`, `playerListOpenPlayer`, `playerListProfile`, `updateLoadLevelFields`, `loadLevel`, `updatePlayerProfile`, `updatePlayerMuted`, and the four volume and options setters | [bin] (torque/engine-304.md#guigraalctrl) |
| Those methods have an empty usage string. Counts include the command name and, for a method, the object. `moveUp` is 3–3 (one script argument). `openServerList` is 2–2 (none). `loadLevel` is 5–5 (three). `updatePlayerProfile` is 12–12 (ten). A maximum of 0 means no upper limit | [bin] (torque/engine-304.md#argument-counts) |
| `setNickName`, `setAccountName`, `setLanguage` and `retrieveAccountFields` are not on this table. Nickname, account and language are `$pref::Graal::` variables | [bin] (torque/engine-304.md#guigraalctrl) |
| Graal's C++ draw types are `TDrawableObject`, `TLevelObject`, `TGaniObject`, `TServerPlayer`, `TDrawableSurface` and `TSurfaceOwner`, plus `TGraalConnection`. None of them is a Torque console class, and `TGraalConnection` is not a child of `NetConnection` | [bin] (torque/engine-304.md#graal-types) |
| `ShapeBase` still has 79 decoded methods here, `fxSunLight` 51 and `GameConnection` 30. The classes 5.12 drops are the TGE game layer (`Player`, vehicles, items, projectiles), not the console or the editors | [bin] (torque/engine-304.md#what-later-builds-drop) |
| The console surface is 857 functions and methods, almost all of them stock TGE | [bin] (torque/engine-304.md#the-split) |

#### The game components

Linux 3.04 keeps stock Torque (`GameConnection`, `NetConnection`, and the `sim/netConnection.cc` / `game/gameConnection.cc` sources) beside Graal's own 2D game. `TGraalConnection` is a separate C++ type with no base class. The binary has no `Graal3D` string and no `BigData` event. [bin] (torque/304-net.md#beside-torque)

| Component | What the 3.04 units do | Source |
| --- | --- | --- |
| Session (`adventure.cpp`, `GuiGraalCtrl`, levels, the local player) | Wakes once, opens the three license files, loads the HUD sheets, and logs a local level entry only for seven file magics | [bin] (torque/304-adventure.md#session-start) |
| Drawing | The `TDrawableObject` family, `pics1.png` and tiledefs, gani text, polygon show-images | [bin] (torque/304-draw.md#types) |
| NPCs and script | `playerenters` and the other trigger names, bow baddies, weapon rectangles, `shapetiletypes` | [bin] (torque/304-npcs.md#triggers) |
| Graal TCP | Login id 5 then language id 37, the server list into `AdventureGui`, the player list and profiles | [bin] (torque/304-net.md#the-game-connection) |
| Sound | fmod at mix rate 44100, wav samples, mid modules, and the mp3-class streams | [bin] (torque/304-audio-ui.md#fmod) |

### 10.1.5 Era B: the Windows 4.2.0.8 split

Two exports named as the 4.04r2 and 4.20r8 executables are one packer stub, byte for byte, with no Graal or Torque class. The file-version 4.2.0.8 archive is the client that can be read, and it includes `Graal3DEngine.dll`, which the packet-logger upload did not. [bin] (torque/v4-404r2-exe.md; torque/v4-420r8-exe.md) [bin] (torque/engine-4208.md#how-the-three-fit)

A later original-carrier 4.04r2 recovery supplies a separate shape-based 3D component that retains `ShapeBase`; it is distinct from the later 4.2.0.8 `GameObject` image below. Its repaired import directory cannot independently verify the earlier named-import count. Recovery availability and load-only limits: → §1.8.5. [bin] (torque/v4-404r2-exe.md#later-recovery-does-not-change-this-exports-identity)

| Fact | Source |
| --- | --- |
| The launcher registers 94 `graal_set…` callbacks and loads `GraalEngine.dll`. The 3D DLL adds 19 names the launcher does not register, including `CreateGraal3DGameObject`, `GetGraal3DTerrainHeight` and `SendGraal3DScriptEvent` | [bin] (torque/engine-4208.md#how-the-three-fit) |
| `GraalEngine.dll` keeps Torque's `GuiCanvas` and `GuiControl` and has no `SimObject`, `ActionMap` or `.dso`. The game is `TAdventure`, `TShowImg` and `TGraalAni`. Scripts are `TGraalVar` and `TScriptExecutionSpace` | [bin] (torque/engine-4208.md#graalenginedll-torque-gui-beside-graals-game) |
| The engine builds a `TGraalVar` for `StartScript_GraalGui`, `StartScript_MoveMap2D`, `StartScript_MoveMap3D` and the other start scripts, and it special-cases the control names `GuiGraalCtrl` and `GuiGraal3DCtrl` | [bin] (torque/engine-4208.md#graalenginedll-torque-gui-beside-graals-game) |
| `Graal3DEngine.dll` is the `GameObject` world: `GameConnection`, `TerrainBlock`, interiors, two login phases (`onGraal3DLoginStep`), and `TerrainChunkEvent`. `ShapeBase` and Torque's `Player` are absent | [bin] (torque/engine-4208.md#graal3denginedll-gameobject-torque) |

#### How the three programs run

The unpacked 4.2.0.8 launcher, `GraalEngine.dll` and `Graal3DEngine.dll` are three programs. The launcher resolves 94 `graal_set` slots and calls `renderGraalCanvas` from the main form's frame; `renderGraal` is resolved and never called. A 3D start loads the 3D DLL, which keeps drawing, tiles, text, panels and the clipboard, while the launcher takes back Flash and the external windows. [bin] (torque/4208-launcher.md#when-drawing-happens); [bin] (torque/4208-launcher.md#starting-3d)

`TAdventure::timer` runs from the canvas frame and pumps the client, nearby-player expiry and keys. `TGraalVar` stores a float, a string, or a link, and `TScriptExecutionSpace` refuses a paused owner. `loadGraalGui` builds the `StartScript_` objects in a fixed order. `GuiGraalCtrl` and `GuiGraal3DCtrl` are not constructed by the script builder. The DLL has no `SimObject` console and no `.dso`. [bin] (torque/4208-engine.md#how-a-session-runs); [bin] (torque/4208-engine.md#how-a-script-runs); [bin] (torque/4208-engine.md#what-is-absent)

`GameObject` is a `SceneObject` with script properties for shape, motion, mounting and interiors. `onGraal3DLoginStep` is raised for ghost objects (step 2), then mission lighting (step 3), and again when `GUIContainer3D` is installed (step 6). A terrain chunk is a compressed square; the byte layout is not in the decompile. `Interior::read` rejects a non-zero first value. `ShapeBase` and Torque's `Player` are absent. [bin] (torque/4208-g3d.md#what-gameobject-is); [bin] (torque/4208-g3d.md#the-login-steps); [bin] (torque/4208-g3d.md#what-a-terrain-chunk-is); [bin] (torque/4208-g3d.md#what-an-interior-read-rejects)

A loose 4.20 engine core, recovered from an archive labelled 4.20r8 and kept apart from the 4.2.0.8 export, has two render entry points that each check their target first: the adventure entry returns without drawing when there is no adventure, the canvas entry returns without drawing when there is no canvas and otherwise asks for one frame, and setting the drawing callback only stores it. These rules do not show what paint draws or when start-up is ready to draw. [bin] (client-internals/windows-420-render-seams.md#the-two-render-entry-points)

### 10.1.6 Era B: Windows 5.0.0.7 and the later v5 exports

File version `5.0.0.7` is a Delphi launcher, `GraalEngine.dll`, and `Graal3DEngine.dll`. The launcher resolves 95 `graal_set*` names and loads the engine before it registers them. A zero return from `graal_engineInitialize` shows `The execution file is corrupted.` [bin] (torque/5007-launcher.md#startup); [bin] (torque/5007-launcher.md#what-it-resolves)

Against the 4.2.0.8 launcher's 94 names, this launcher adds the colour-matrix pair, fullscreen get and set, `graal_setShowGraalWindow`, screen capture, Flash clipping and forced texture transparency. It no longer resolves the external history, log and PM setters, stretched graphics, the screenshot setter, Flash panel size, or `graal_setLogGraalMessage`. [bin] (torque/5007-launcher.md#what-it-resolves)

The engine defines 118 setters. The 23 the launcher does not resolve are the 3D bridge (connect, `GameObject`, terrain height, script events, window lock) and three external-window setters neither host calls. `SimObject` and `.dso` are absent from `GraalEngine.dll`. [bin] (torque/5007-engine.md#setters-the-launcher-does-not-resolve); [bin] (torque/5007-engine.md#no-simobject-and-no-dso)

`TAdventure` is the session. A server name whose second character is a space loses its first two characters, and a name that starts with `3 ` asks the launcher through `graal_setStartGraal3D` and then connects the 3D side at listed port + 1. Any other server puts `GUIContainer` on `GuiCanvas`. The timer calls `handleClient`, which drops a dead link and raises `onPlayerLogout`. [bin] (torque/5007-engine.md#session)

A script object is a `TGraalVar` with a `TScriptExecutionSpace`. `runScript` walks that space's actions on a machine borrowed from the universe. The factory refuses to build `GuiGraalCtrl` or `GuiGraal3DCtrl` as an ordinary object. [bin] (torque/5007-engine.md#how-a-script-runs); [bin] (torque/5007-engine.md#the-graal-control)

In the 3D DLL, `GameObject`'s property table is parented on `SceneObject`. Two mission steps download ghosts and then light the mission, and the following step sets the canvas to `GUIContainer`. A terrain chunk load reads a compressed file under `levels3d`/`heights` for that server. The connect check reads 4 bytes and accepts only 24; any other value returns `CHR_PROTOCOL`. An interior file's first 4 bytes must be 0, and an interior resource's first 4 bytes must be 44. [bin] (torque/5007-g3d.md#gameobject); [bin] (torque/5007-g3d.md#mission-phases); [bin] (torque/5007-g3d.md#terrain-chunks); [bin] (torque/5007-g3d.md#protocol); [bin] (torque/5007-g3d.md#interiors)

#### The rest of that v5 export

One static read of a v5 export (nothing run). File-version strings below are the version resources in that export [bin] (torque/launcher-5007.md#what-the-decompile-is):

| Fact | Source |
| --- | --- |
| `Graal.exe` 5.0.0.7 is a Delphi launcher. It loads `GRAALENGINE.DLL` and `GRAAL3DENGINE.DLL`, resolves `graal_engineInitialize` and 95 `graal_set*` names, and shows a warning that the execution file is corrupted if initialisation fails | [bin] (torque/launcher-5007.md#what-it-loads) |
| `GraalEngine.dll` defines `TAdventure`, `TGraalVar`, `TShowImg`, `TGraalAni`, `GuiGraalCtrl` and Torque GUI classes (`GuiCanvas`, `GuiControl`). It defines 118 `graal_set*` setters. `SimObject`, `GameConnection`, `ActionMap` and `.dso` are absent | [bin] (torque/engine-5007.md#graals-game; torque/engine-5007.md#torque-that-remains) |
| The launcher resolves the Flash, external-window, login and `graal_setStartGraal3D` setters. The 3D DLL calls the OpenGL and `GameObject` setters, then `graal_engineInitialize`. Three external-window setters are defined and named by neither host | [bin] (torque/engine-5007.md#who-calls-the-setters) |
| `Graal3DEngine.dll` in this export is the `GameObject` era: `SimObject`, `GameConnection`, `ActionMap`, `TerrainBlock`, terrain chunks, `GameShapeDTS` / `DIF` / `FT`. `ShapeBase`, `PlayerData` and a datablock download phase are absent. Interior read strings are present | [bin] (torque/g3d-5007.md#torque-that-is-still-here; torque/g3d-5007.md#interiors-and-terrain) |
| Mission logs are a ghost-object download (step 2), mission lighting (step 3), lighting done (step 4), the initial control object (step 5), then step 6 attaches `GUIContainer` | [bin] (torque/g3d-5007.md#mission-phases) |
| A check writes `CHR_PROTOCOL` unless the tested value is greater than 23 and less than 25 | [bin] (torque/g3d-5007.md#protocol-window) |
| The packed 5.12 exe's version resource is `5.1.2.0` and the decompile is a stub. That zip has no `Graal3DEngine.dll` | [bin] (torque/stub-512.md#what-the-decompile-is) |
| The packed exes named 5.2.4.3 and 5.24r4 have version resources `5.243` and `5.244`. Both decompiles are stubs | [bin] (torque/stub-5243.md#what-the-decompile-is; torque/stub-524r4.md#what-the-decompile-is) |
| `freetype6.dll` is FreeType 2.1.10.2079. The `fmod.dll` version resource says FMOD 3.75 and the recovered code is a packer stub | [bin] (torque/freetype6-5007.md#what-the-decompile-is; torque/stub-fmod-5007.md#what-the-decompile-is) |
| Unpacked 5.30r3 and 5.31r4 are one exe each, file versions `5.303` (compile string `Oct 18 2010`) and `5.314` (compile string `Jan 5 2011`), source tree `quattro_lib`. `graal_set`, `SimObject` and `GameConnection` are absent. `GuiGraalCtrl`, `GuiGraal3DCtrl` and the Torque GUI field names remain | [bin] (torque/engine-530r3.md#what-the-decompile-is; torque/engine-530r3.md#torque; torque/engine-531r4.md#what-the-decompile-is; torque/engine-531r4.md#torque) |

The inspected reconstructed 5.30r3 window method registers a class, computes and conditionally adjusts its rectangle, creates a native window and stores its handle in an object. The registered procedure matches incoming handles to window objects, calls the matching object's message handler and uses a default-window fallback for unmatched handles or the ordinary unhandled-result path; a separate close-message branch returns directly. The reconstructed import names mix ANSI and Unicode variants, whose original bindings remain unverified. This is a bounded native window/object boundary, not a protected-entry-to-play-loop trace or proof that no engine module is loaded dynamically. Original unpacking lineage and runtime behavior remain open. [bin][inf] (torque/engine-530r3.md#native-window-and-object-message-boundary)

### 10.1.7 Which modules each era still has

A module is present when that image registers it, recovers methods, records the C++ type, or emits a `Class::method` error. A stub is the name alone. The 4.2.0.8 and 5.0.0.7 launchers are omitted below: both listings have DirectDraw and none of these modules. [bin] (client-internals/torque-surface-by-era.md#how-a-cell-is-counted); [bin] (client-internals/torque-surface-by-era.md#the-table)

| Era | What of Torque is in the image | Source |
| --- | --- | --- |
| 3.04 Linux | Console, `SimObject`, `ActionMap`, `GuiCanvas`, `GuiControl`, `GBitmap`, terrain, interiors, DTS, `GameConnection`, `ShapeBase`, `Player`, vehicles and datablocks. Graal's console class is `GuiGraalCtrl` | [bin] (client-internals/torque-surface-by-era.md#304-linux) |
| 4.2.0.8 and 5.0.0.7 engine DLL | `GuiCanvas`, `GuiControl` and `GBitmap`. No console, `SimObject` or `ActionMap`. The game types are `TAdventure`, `TGraalVar`, `TScriptExecutionSpace` and `TShowImg` | [bin] (client-internals/torque-surface-by-era.md#4208-windows); [bin] (client-internals/torque-surface-by-era.md#5007-windows) |
| 4.2.0.8 and 5.0.0.7 3D DLL | `SimObject`, `ActionMap`, terrain, interiors, DTS, `GameConnection` and `GameObject`. No `ShapeBase`, `Player`, vehicles or datablock class. 5.0.0.7 adds the names `GameShapeDTS`, `GameShapeDIF` and `GameShapeFT` | [bin] (client-internals/torque-surface-by-era.md#4208-windows); [bin] (client-internals/torque-surface-by-era.md#5007-windows) |
| 5.30r3 and 5.31r4 | No Torque world and no `GuiCanvas`. Control names remain, and so do `horizSizing`, `vertSizing`, `minExtent`, `fontType`, `fillColor`, `makeFirstResponder` and `pushToBack` | [bin] (client-internals/torque-surface-by-era.md#530r3-and-531r4) |
| 6.00r2 and 6.00r4 | The same control names, without those field names. `TAdventure` does not occur | [bin] (client-internals/torque-surface-by-era.md#600r2-and-600r4) |
| Packed 5.12, 5.24, 6.037 and 6.113 | Packer listings. None of the module names | [bin] (client-internals/torque-surface-by-era.md#packed-listings) |

`GameConnection` in 3.04 uses the stock method names. `BigDataStartEvent` and `TerrainChunkEvent` on the 4.2.0.8 and 5.0.0.7 3D DLLs are the Graal patch. `GameObject`, `GuiGraalCtrl`, `TAdventure`, `TGraalVar`, `TScriptExecutionSpace` and `TShowImg` are Graal-only. A stock name whose body was not diffed against a TGE tree is uncompared. [bin] (client-internals/torque-surface-by-era.md#against-stock-tge)

### 10.1.8 After Torque: what the 6.x images still name

This section records absence. Each 6.x image below was read to establish which Torque names survive once Graal's own engine replaced Torque. The engine itself is described in §1.8.7. The table gives the cut, and the builds follow in date order. [doc] (client-internals/issho-cut.md#ato-v3-to-v5)

| What | Who | Source |
| --- | --- | --- |
| Torque console, `SimObject`, `GameConnection`, and UDP on the listed port plus one | v3 to v5 | [doc] (client-internals/issho-cut.md#ato-v3-to-v5) |
| `quattro_lib`, `TSocket`, `TServerPlayer`, OpenGL, `fmod`, `GRESCR01` and the GS2 switch | unpacked 6.037 and 6.1.1.3 | [bin] (client-internals/issho-cut.md#issho-from-these-two-images) |
| `GuiWindowCtrl` and `GuiControlProfile` remain as strings. `SimObject` and `GameConnection` do not | both unpacked images | [bin] (client-internals/issho-cut.md#issho-from-these-two-images) |

#### Windows 6.00r2 and 6.00r4

Unpacked Windows 6.00r2 (product version 6.002, 12 June 2011) and 6.00r4 (6.004, 26 June 2011) are Graal's `quattro_lib` program [bin] (client-internals/engine-600r2.md#what-the-export-is); [bin] (client-internals/engine-600r4.md#what-the-export-is). The drawing, GUI, script and socket split is in §1.8.7.

| What remains | In these two builds | Source |
| --- | --- | --- |
| Torque 3D classes and formats (`GameConnection`, `TerrainBlock`, `Interior`, DTS, `SimObject`, `.mis`, `.ter`, `.dts`) | absent | [bin] (client-internals/engine-600r2.md#no-torque-3d) |
| Torque GUI field names (`horizSizing`, `vertSizing`, `minExtent`, `fontType`, `fillColor`, `makeFirstResponder`, `pushToBack`) | absent; those names are a 5.24r3 finding | [bin] (client-internals/engine-600r2.md#gui-and-script-objects); [bin] (torque/study-torque-clients.md#524r3--6x) |
| `GuiControl`, `GuiControlProfile`, `GuiScrollCtrl`, `GuiWindowCtrl`, `GuiMLTextCtrl` and the other Torque control names | live GS2 controls, each with its own draw routine | [bin] (client-internals/engine-600r2.md#gui-and-script-objects) |
| `GuiGraal3DCtrl` | live type in the GUI walk, same branch as `GuiGraalCtrl` | [bin] (client-internals/engine-600r2.md#no-torque-3d) |
| `GuiTilesCtrl` | absent; tiles are the `Draw_Tiles` pass | [bin] (client-internals/engine-600r2.md#gui-and-script-objects) |
| `MissionGroup` | script object looked up by name | [bin] (client-internals/engine-600r2.md#gui-and-script-objects) |
| `onMouseYawPitch`, and a builtin described as changing the colour of the 3D terrain | script text; no terrain block | [bin] (client-internals/engine-600r2.md#gui-and-script-objects) |
| `levels3d`, `graal3://` | a content folder, and an option-list string with no recovered call | [bin] (client-internals/engine-600r2.md#gui-and-script-objects) |

#### Unpacked Windows 6.037

The unpacked 6.037 listing is one GUI executable, product version `6.037` (fixed words 6.0.3.7), compiler banner 16 November 2012 18:58:51. The code section holds `quattro_lib` and `TSocket`. It is not the packed 6.037 shell. [bin] (client-internals/unpacked-6037.md#what-this-file-is)

| What the listing shows | Unpacked 6.037 | Source |
| --- | --- | --- |
| Program | One `quattro_lib` executable. No Delphi launcher, no engine DLL, no SDL. `ExeReplacer.exe` is still launched | [bin] (client-internals/unpacked-6037.md#one-program) |
| Packer residue | Seven sections, including a blank name, two eight-letter names and `.SCY`. The export directory is still named `QPlay.exe`. The entry is the C runtime cookie setup | [bin] (client-internals/unpacked-6037.md#what-this-file-is) |
| Connection | `TSocket`, newline refused, key byte masked to seven bits, gen-3/5 seed, next field 3. No plaintext `G3D` token. The receive switch is the 92-id Linux 6.03r7 set | [bin] (client-internals/unpacked-6037.md#connection) |
| TLS | CyaSSL is called with the SSLv3 client method. `zlibVersion` returns `1.2.3`; inflate callers pass `1.2.5` | [bin] (client-internals/unpacked-6037.md#what-this-file-is); [bin] (client-internals/unpacked-6037.md#connection) |
| GS2 | Cases 54, 121 and 200–242. No case 48 or 49, and nothing above 242, as in unpacked 6.00. `GRESCR01` on a `.code` file of at least eight bytes | [bin] (client-internals/unpacked-6037.md#gs2) |
| `GuiGraalCtrl` | Still the type the GUI walk drops | [bin] (client-internals/unpacked-6037.md#gui) |
| `GuiGraal3DCtrl` | Absent. The shell looks up `GraalControl` and `GraalControl3D` | [bin] (client-internals/unpacked-6037.md#gui) |
| `GuiTilesCtrl` | Constructed. Unpacked 6.00 does not have the name (above) | [bin] (client-internals/unpacked-6037.md#gui); [bin] (client-internals/engine-600r2.md#gui-and-script-objects) |
| `horizSizing` and the other Torque field names | Absent, as in unpacked 6.00 | [bin] (client-internals/unpacked-6037.md#gui) |
| Torque modules | `GameConnection`, `SimObject`, DTS, `TAdventure` and SDL are absent. `-printmap` writes Torque 2D datablock text and does not run a module | [bin] (client-internals/unpacked-6037.md#torque-names-that-remain) |

#### Unpacked Windows 6.1.1.3

A later listing of the same 8 August 2014 executable decompiles the engine. The upload is a Ghidra C listing and an HTML listing, not a raw executable and not `Graal.exe` plus a DLL. The version resource, the timestamp and the virtual image size match the stub in §10.1.9. The header entry is the Visual C++ security-cookie initializer, and about 9,300 functions recover. [bin] (client-internals/unpacked-6113.md#what-the-image-is); [bin] (client-internals/unpacked-6113.md#the-engine-is-visible)

| What this listing shows | Unpacked 6.1.1.3 | Source |
| --- | --- | --- |
| Version | String `6.113`, fixed words 6.1.1.3, Eurocenter Games, copyright 2014. Compiler strings `Aug 8 2014` and `17:16:33`. Image timestamp 8 August 2014, 13:19:46 UTC. Linker major 9, minor 0 | [bin] (client-internals/unpacked-6113.md#what-the-image-is) |
| Shape | One 32-bit GUI image, seven sections. `.text` is marked initialized data. `.SCY` is marked code. Virtual image 6,504,448 bytes | [bin] (client-internals/unpacked-6113.md#what-the-image-is) |
| Engine | `quattro_lib` / `Quattro Play`, `TSocket`, `TServerPlayer`, `GuiGraalCtrl`, OpenGL, FMOD, `GRESCR01`. Original file name `Graal.exe` | [bin] (client-internals/unpacked-6113.md#the-engine-is-visible) |
| Packer left behind | Export directory still named `QPlay.exe` (in `fbndyrix`). Import directory in `.SCY`. Blank section still holds `Themida`, `WinLicense` and Oreans driver names | [bin] (client-internals/unpacked-6113.md#packer-names-that-remain) |

Against unpacked 6.00 (above), this image still has no `SimObject`, `GameConnection`, `TerrainBlock`, `MissionGroup`, `TAdventure`, `graal_set` or `horizSizing`. The GUI walk compares `GuiGraalCtrl`. `GuiGraal3DCtrl` is not a string here; the shell looks up `GraalControl3D` beside `GUIContainer`. `GuiTilesCtrl` is registered beside `GuiControl`, which the 6.00 notes recorded as absent. A file reader matches five `new t2d…(` constructors, and `-printmap` takes a datablock file and a level file. That is text, not a Torque console. The hold on writing the module stands. [bin] (client-internals/unpacked-6113.md#torque-names-against-unpacked-600)

### 10.1.9 Packer stubs and version resources

Several uploads named after real clients are packer shells, not the client. They are listed here so that nobody reads them as engine evidence. Their version resources are still useful for identification. [bin] (torque/skipped-version-stamps.md#what-was-skipped)

#### The packed listings

The two v4 exe listings are one file. The program is the Thinstall outer loader: `TS_LOADER` or the module path, `LoaderFlags` as the table offset, magic `0x82D0B188`, a stored block or the range coder, then relocations, imports and a jump to the unpacked entry. The import directory adds one import from each DLL of the wrapped program (registry, shell, save dialog, image list, OLE, joystick, printer). Winsock, DirectDraw, OpenGL and `GraalEngine.dll` are not in that listing. [bin] (torque/skipped-v4-read.md#one-listing); [bin] (torque/skipped-v4-read.md#what-the-loader-does); [bin] (torque/skipped-v4-read.md#what-is-in-the-clear)

Packed 5.12 keeps Delphi form resources (`TGRAALWINDOW`, `TPLAYERLIST`, and the options, profile, URL, controls and short-message forms) plus `DVCLAL`. Its recovered code does not call `LoadLibraryA`. The packed 5.2.4.3 and 5.24r4 exes bind only `LoadLibraryA` and `VirtualAlloc` and name no form. [bin] (torque/skipped-v5-read.md#the-512-resource-directory); [bin] (torque/skipped-v5-read.md#the-later-packed-exes)

`fmod.dll` in the 5.0.0.7 archive is the same UPX listing as the 4.2.0.8 copy. The export names are FMOD's sample, stream, 3D, DSP and music API, including net streams, and the recovered body is the decompressor. [bin] (torque/skipped-v5-read.md#fmod)

The packed 6.037 and 6.113 exes are distinct. Each export directory is named `QPlay.exe` and lists a CyaSSL client, zlib, and a hash and cipher set; the 6.113 names add TLS 1.0 through 1.2, DTLS and AES-CBC. The bytes at those exports are not that library, and neither listing names a Torque class. [bin] (client-internals/skipped-v6-read.md#the-stub); [bin] (client-internals/skipped-v6-read.md#the-export-directory); [bin] (client-internals/skipped-v6-read.md#absent-from-both)

#### Version resources

Packer-stub uploads from the v4, v5 and v6 decompile sets still carry a version resource. The recovered code is not the client. [bin] (torque/skipped-version-stamps.md#what-was-skipped)

The `4.0.4.2` exe stub and the `5.1.2.0` stub share one string table: four-part file version, a one-character product version, description `Graal Online client`, internal name `Graal client`, company `Linux Cyberjoueur`, no year. From `5.243` on, the file and product strings are the collapsed form (`5.243`, `5.244`, `6.037`, `6.113`) and the fixed words stay four-part (`5.2.4.3`, `5.2.4.4`, `6.0.3.7`, `6.1.1.3`). Those later Graal stubs name `Linux Cyberjoueurs` or `Eurocenter Games` and a copyright year (`2010`, `2012`, `2014`). [bin] (torque/skipped-version-stamps.md#two-layouts)

| Upload | Code | File version string | Fixed words | Product version string | Original file | Company and year | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Graal 4.04r2.exe` and `Graal v4.20r8[Windows].exe` (one decompile) | stub | `4.0.4.2` | `4.0.4.2` | `4` | `Graal.exe` | `Linux Cyberjoueur`, no year | [bin] (torque/skipped-version-stamps.md#v4-exe-pair) |
| `Graal 5.12.exe` | stub | `5.1.2.0` | `5.1.2.0` | `5` | `Graal.exe` | `Linux Cyberjoueur`, no year | [bin] (torque/skipped-version-stamps.md#graal-512) |
| `Graal 5.2.4.3.exe` | stub | `5.243` | `5.2.4.3` | `5.243` | `Graal.exe` | `Linux Cyberjoueurs`, `2010` | [bin] (torque/skipped-version-stamps.md#graal-5243) |
| `Graal v5.24r4.exe` | stub | `5.244` | `5.2.4.4` | `5.244` | `Graal.exe` | `Linux Cyberjoueurs`, `2010` | [bin] (torque/skipped-version-stamps.md#graal-524r4) |
| `fmod.dll` in the 4.2.0.8 and 5.0.0.7 archives (one decompile) | stub | `3.75` | `3.7.5.0` | `3.75` | `fmod.dll` | Firelight Technologies, `1994-2005` | [bin] (torque/skipped-version-stamps.md#fmod) |
| `Graal 6.0.3.7.exe` | stub | `6.037` | `6.0.3.7` | `6.037` | `Graal.exe` | `Linux Cyberjoueurs`, `2012` | [bin] (torque/skipped-version-stamps.md#graal-6037) |
| `Graal 6.1.1.3.exe` | stub | `6.113` | `6.1.1.3` | `6.113` | `Graal.exe` | `Eurocenter Games`, `2014` | [bin] (torque/skipped-version-stamps.md#graal-6113) |

#### Packed Windows 6.1.1.3

The 2026-11-07 gap archive did not contain an unpacked 6.113 image. The Windows file is still one GUI executable whose export directory is named `QPlay.exe` and whose only import is `SetCurrentDirectoryA`, which the stub does not call. [bin] (client-internals/engine-6113.md#still-no-engine-image); [bin] (client-internals/engine-6113.md#the-one-import-and-the-entry)

| What the listing shows | 6.1.1.3 | Source |
| --- | --- | --- |
| Version | String `6.113`, fixed words 6.1.1.3, Eurocenter Games, copyright 2014, image timestamp 8 August 2014. No version token | [bin] (client-internals/engine-6113.md#what-this-file-is) |
| Connection, GS2 VM, property parsers, file cache, GUI classes | Absent. The recovered code is the dword walk and a breakpoint | [bin] (client-internals/engine-6113.md#subsystem-map) |
| Export names | CyaSSL through TLS 1.2, DTLS, AES-CBC, HMAC, SHA-256, and zlib. The bytes at those exports are not the library | [bin] (client-internals/engine-6113.md#the-export-surface) |
| Login, framing, packet ids, property streams, `GRESCR01` | Not in this image. Neighbour notes disagree on the key byte, the 6.03 token, ids 100 and 108, and the oldest level magics | [bin][cap] (protocol/v6113-wire.md#contradictions) |
| GS2 | No opcode switch. Unpacked 6.00 already has cases 54 and 121 and folds 234–242, and does not have 48 or 49. This file cannot extend that | [bin] (protocol/gs2-6113.md#what-6113-cannot-show) |
| Torque names | Console, `SimObject`, `GameConnection`, `ShapeBase`, `Player`, `graal_set`, `horizSizing`, `GuiTilesCtrl` and `TAdventure` are already gone in unpacked 6.00. `GuiGraalCtrl` and `GuiGraal3DCtrl` are that build's playfield. This listing has none of those names. Issho is v6; v7 Unity is not a profile this file supports | [bin] (client-internals/engine-6113.md#what-is-gone-by-6113) |

The 6.1.1.3 decompile is 106 functions in a 227,199-byte listing. Three are the entry, which clears a breakpoint byte, mixes four kilobytes and then breakpoints. The other 103 are export names for a `CyaInt` TLS client, AES-CBC, HMAC, SHA-256 and RSA; those bodies do not implement the named calls, several names share one body, and the zlib names are not functions in the listing. The file has no GS2 switch, GUI class or socket import. [bin] (client-internals/decompile-6113.md#how-the-bytes-split)

### 10.1.10 Linux 3.04 build and dependency evidence

The revision-1 executable and shipped installer were inspected statically; nothing was run for this study. UPX restoration agrees with the pack-header size/checksum, and object comments identify predominantly GCC 2.96 with five NASM entries. The stripped executable retains a pre-GCC-3 C++ ABI, so a modern symbol/demangler assumption is inappropriate. These checks concern the retained input and unpacking, not authenticated release provenance. [bin] (client-internals/linux-304-executable-build.md#packing); (client-internals/linux-304-executable-build.md#toolchain)

| Component | Static evidence and limit | Source |
| --- | --- | --- |
| Audio/windowing | bundled FMOD 3.70 and SDL 1.2 are explicit dynamic dependencies; FMOD has 24 effect and six music imports, SDL 48 imports | [bin] (client-internals/linux-304-executable-build.md#linkage) |
| Graphics | X11 is an explicit dependency; no GL imports, but SDL's GL loader and library names support runtime GL loading | [bin] (client-internals/linux-304-executable-build.md#linkage) |
| OpenAL | compiled driver-layer console names exist, but no OpenAL library name or audio import was found; reachability of that layer remains unestablished | [bin] (client-internals/linux-304-executable-build.md#linkage) |
| C++ runtime | no dynamic C++/libgcc runtime dependency; runtime definitions are present in the executable. Its 396 named dynamic symbols comprise 310 imports and 86 runtime/stdio definitions, with no exported game function identified | [bin] (client-internals/linux-304-executable-build.md#linkage) |
| Symbol-version floor | required libc/pthread/math versions top out at 2.2 / 2.1.1 / 2.1 respectively; satisfying these version labels alone does not demonstrate loader, graphics or gameplay compatibility | [bin] (client-internals/linux-304-executable-build.md#linkage) |
| Embedded libraries | banners identify zlib 1.1.3, libmng 1.0.5, GIFLIB 4.0 and the IJG JPEG decoder | [bin] (client-internals/linux-304-executable-build.md#linkage) |
| Installation | Loki Setup metadata and the post-install launcher arrange the bundled library search path through `LD_LIBRARY_PATH`; GL/X11 receive no separate launcher override. These are file observations, not a new installation recipe or runtime test | [file] (client-internals/linux-304-executable-build.md#installer-and-launcher) |

The installer library list mentions voice packaging and the executable has microphone/voice controls, but the stripped image supplies no identifying GSM/LPC strings. This establishes neither the presence nor absence of those codecs. Follow the selected-codec consumer to resolve that question; separately establish whether the OpenAL layer is reachable before treating a console name or an earlier lab's installed package as a required backend. [file][bin][inf] (client-internals/linux-304-executable-build.md#still-open)

### 10.1.11 The inspected Windows 4.04r2 components

This component map concerns a packed carrier on disk and four mapped images retained from a prior controlled load-only capture; no server/login occurred in that capture, and nothing was run for the static component report. Keep it separate from the earlier aliased packer export and the 4.2.0.8 engine in §10.1.5. Headers, exports and class-name inventories establish component surfaces, not complete call behavior. [bin][cap] (client-internals/windows-404r2-components.md#how-this-was-checked)

| Component | Observed role/metadata | Source |
| --- | --- | --- |
| Packed carrier | MSVC linker metadata, one section, July 2003 header date; version resource agrees with the shell | [bin] (client-internals/windows-404r2-components.md) |
| Delphi shell | Delphi/VCL UI, FileVersion 4.0.4.2; its fixed Delphi header stamp is not a release date. Only the version resource was covered, not the forms/event handlers | [cap] (client-internals/windows-404r2-components.md) |
| Game engine | combined Graal/Torque-derived engine; March 2006 header date; 1651 named exports, split into 980 methods, 443 constructors/destructors/operators and 228 plain names | [cap] (client-internals/windows-404r2-components.md#graalenginedll-exports) |
| 3D engine | distinct Torque component with load/run/end exports and March 2006 header date; 338 RTTI class names versus 242 in the game engine | [cap] (client-internals/windows-404r2-components.md#source-areas-visible-in-the-engines) |
| Audio module | FMOD 3.7, itself packed, 222 exports and September 2003 header date | [cap] (client-internals/windows-404r2-components.md) |
| Separate updater | helper on disk, August 2005 header date, imports from kernel/shell libraries | [bin] (client-internals/windows-404r2-components.md) |

The game engine export inventory includes Torque GUI/math classes, Graal script/world/container classes, an initialization entry and 100 launcher-setter names. Export presence does not show that a particular launcher resolves or calls every name; the separately studied 5.00r7 launcher resolves 95. Voice packaging is compiled into this game engine (17 voice and eight related crypto exports), rather than supplied as the separate voice DLL described for later clients. This surface alone is not a codec-selection or packet-format contract. [cap] (client-internals/windows-404r2-components.md#graalenginedll-exports)

Header-date differences leave repack-versus-later-build lineage open; date the release independently before choosing either account. The RTTI counts still need a stock-Torque-versus-Graal class map, and shell forms/event handlers remain unread in this report. Embedded library/source-area names are leads for that work, not recovered implementations; detailed counts and source-area inventory stay in the source. [cap][inf] (client-internals/windows-404r2-components.md#notes-on-dating); (client-internals/windows-404r2-components.md#still-open)

### 10.1.12 The 3D engine DLL as a whole (4.20r8, 5.00r7)

5.12's engine is packed inside its exe, so the 4.20r8 and 5.00r7 `Graal3DEngine.dll` stand in for it. The rules give what the DLL exposes and how the client drives it [bin] (torque/3d-engine-static-reads-2026-11-25.md#the-engine-dll-as-a-whole-t3d-093-to-t3d-104-bin-420r8-500r7).

| Rule | Source |
| --- | --- |
| 4.20r8 exports about 200 names, including the 76 `graal_set*` callback setters; 5.00r7 exports five: load, run, end, resize and toggle full screen | [bin] (torque/3d-engine-static-reads-2026-11-25.md#the-engine-dll-as-a-whole-t3d-093-to-t3d-104-bin-420r8-500r7) |
| Both import most of their runtime from `GraalEngine.dll` (strings, file streams, the GS2 variable and object types, and in 5.x the maths types) | [bin] (torque/3d-engine-static-reads-2026-11-25.md#the-engine-dll-as-a-whole-t3d-093-to-t3d-104-bin-420r8-500r7) |
| The 5.00r7 exe loads the DLL by name and resolves load, run and end; no version check between exe and DLL was found | [bin] (torque/3d-engine-static-reads-2026-11-25.md#the-engine-dll-as-a-whole-t3d-093-to-t3d-104-bin-420r8-500r7) |
| In 5.x the 78 `graal_set*` names exist but are not exported, so the callbacks come in through the load entry point; against 4.20r8, 5.x adds ScreenCapture, ForceTextureTransparency, PushColorMatrix and PopColorMatrix, and drops MakeGraalScreenshot and DrawGraphicsStretched | [bin] (torque/3d-engine-static-reads-2026-11-25.md#the-engine-dll-as-a-whole-t3d-093-to-t3d-104-bin-420r8-500r7) |
| Neither DLL carries a TGE version banner; neither can exec TorqueScript; 5.00r7 has no `SimDataBlockEvent`, so no datablocks | [bin] (torque/3d-engine-static-reads-2026-11-25.md#the-engine-dll-as-a-whole-t3d-093-to-t3d-104-bin-420r8-500r7) |
| The engine logs to `console.log` in the client folder and saves terrain under `levels3d/terrain/` | [bin] (torque/3d-engine-static-reads-2026-11-25.md#the-engine-dll-as-a-whole-t3d-093-to-t3d-104-bin-420r8-500r7) |
| It creates no threads and imports no DirectInput: it is single-threaded, ticked by the client, and gets input through the client's action names; it binds the `moveMap2D` move commands itself | [bin] (torque/3d-engine-static-reads-2026-11-25.md#the-engine-dll-as-a-whole-t3d-093-to-t3d-104-bin-420r8-500r7); [bin] (torque/3d-engine-static-reads-2026-11-25.md#input-t3d-057) |
| The connect reject has separate texts for a protocol too old, a protocol too new and a wrong game; the held builds use protocols 19, 21 and 24 | [bin] (torque/3d-engine-static-reads-2026-11-25.md#protocol-check-t3d-072-t3d-080) |
| `.3ds`, `.dts` and `.dif` loaders are registered; the DIF and ForceField readers check their version numbers; the terrain loader requires 256 × 256 24-bit textures | [bin] (torque/3d-engine-static-reads-2026-11-25.md#loaders-t3d-098) |
| By protocol, class set and GS2 3D object set, 5.00r7 is 3D-equal to 5.12: protocol 24 with the same three rejects, the same 28 registered classes (none a datablock; 27 in the first count, which missed `fxSunLight`) and the same 37 GS2 3D object owners; 5.12 links the engine into its image instead of shipping a DLL, and lab copies labelled as a 5.12 3D DLL are the 5.00r7 file | [bin] (torque/3d-engines-5007-512-and-403-411-2026-11-25.md#t3d-005-500r7-is-3d-equal-to-512) |
| 4.03r3 equals 4.04r2 (protocol 19, 117 classes, 29 in the datablock family with `fxLightData`); 4.11 has protocol 21, 32 classes and `GameObject`, with the datablock layer, the stock game, vehicle, mission and audio classes and `ScriptObject` dropped; 4.20r8 drops `FileObject`, `SimpleMessageEvent`, `SimpleNetObject` and `twSurfaceReference` and moves to protocol 24, with 28 classes. A first scan missed the `fx` family and gave 108, 30 and 27 | [bin] (torque/3d-engines-5007-512-and-403-411-2026-11-25.md#t3d-003-411-is-the-switch-point); [bin] (torque/3d-engines-5007-512-and-403-411-2026-11-25.md#t3d-004-linux-and-mac-against-their-windows-twins) |
| The switch to `GameObject` is earlier than 4.11: Linux and Mac 4.10r2 (August 2006) already have protocol 21, the 32-class set and no datablocks, so it falls between 4.04r2 (March 2006) and 4.10r2; 4.20r6 (December 2006) already has protocol 24 and the 28-class set | [bin] (torque/3d-engines-5007-512-and-403-411-2026-11-25.md#t3d-004-linux-and-mac-against-their-windows-twins) |
| Linux and Mac builds link the 3D engine into the main binary. Linux and Mac 4.0x swap one class against Windows 4.0x (`AIWheeledVehicle` only on Linux and Mac, `MissionArea` only on Windows); every later Linux and Mac build has the class set of its Windows twin, so Linux 4.20r6 and 4.20r8 can stand in for Windows 4.20r8 on the 3D wire. Mac builds are PPC only | [bin] (torque/3d-engines-5007-512-and-403-411-2026-11-25.md#t3d-004-linux-and-mac-against-their-windows-twins) |
| A protocol-19 server that ghosts a `MissionArea` to a Linux or Mac 4.0x client would send a class that client lacks | [inf] (torque/3d-engines-5007-512-and-403-411-2026-11-25.md#t3d-004-linux-and-mac-against-their-windows-twins) |
| Torque particles (`ParticleEmitterNode`, `ParticleEmitterNodeData`, `ParticleEmitterData`, `ParticleData`) are registered in 4.04r2 and absent from the 28-class set of 4.20r6 and later; the 4.20r8, 5.00r7 and 5.12 GS2 dumps have none of them. Particle content belongs to protocol-19 engines; 5.12 has a GS2 particle system instead (→ §8.5.4) | [bin] (torque/3d-particles-512-vs-404r2-2026-11-25.md#class-evidence-bin) |
| A ghost of a particle class sent to a 5.12-class client would name an unknown class and drop the link; not run, because the lab server has no way to send one | [inf] (torque/3d-particles-512-vs-404r2-2026-11-25.md#not-driven-live-this-session-and-why) |

## 10.2 Join sequence

Joining a 3D server runs the same routine in several builds. The steps below are in order [bin] (protocol/v3x-clients.md#listserver).

| Step | What happens | Source |
| ---: | --- | --- |
| 1 | The server list marks a 3D server with the name prefix `3 ` (the "Graal 3D" tab) | [bin] (protocol/v3x-clients.md#listserver) |
| 2 | Choosing it runs one routine in 3.153, 4.04r2 and 5.12: strip the two-character prefix, remember UDP port = listed port + 1, set the 3D-mode flag and start the Torque side | [bin] (torque/network.md#how-a-client-gets-to-a-3d-server) |
| 3a | 3.153 creates a `SimGroup` named `MissionGroup` and runs `main3D.cs`, which creates `GameConnection(ServerConnection)` and calls `connect()` with the stored address | [bin][file] (torque/network.md#how-a-client-gets-to-a-3d-server) |
| 3b | 4.04r2 and 5.12 first ask the launcher (a non-zero answer cancels), then have it connect to host, port + 1, with the UDP option; 4.04r2 loads `Graal3DEngine.dll` on demand at this point | [bin] (torque/network.md#how-a-client-gets-to-a-3d-server) |
| 4 | In both 2D and 3D the client opens the normal Graal TCP connection to the listed port and logs in as usual (→ §2.3) | [bin] (torque/network.md#how-a-client-gets-to-a-3d-server) |
| 5 | The Torque handshake runs on UDP (→ §10.3), then the mission download (→ §10.3.6) | [bin][run] (torque/network.md#the-full-handshake-live) |

The rules below give how a 3D server is split across two ports and how the client picks its own UDP port [bin][run] (torque/network.md#how-a-client-gets-to-a-3d-server).

| Rule | Source |
| --- | --- |
| A 3D server is two servers on one host: a Graal gserver on TCP *P* and a Torque server on UDP *P* + 1 | [bin][run] (torque/network.md#how-a-client-gets-to-a-3d-server) |
| The client's own UDP port is random unless the fixed-port option is on, then `fixedudpport` (default 14899) | [bin][file] (torque/network.md#how-a-client-gets-to-a-3d-server) |
| 28000 is only the Torque address parser's default for an address without a port | [bin] (torque/wire-by-build.md#the-handshake-per-build) |
| Seen live: the 5.12 client sent the Torque challenge to UDP *P* + 1 and opened TCP *P* in the same millisecond; the TCP side carried the ordinary 5.x login frame with the built-in guest account, then ids 37 and 23 | [run] (torque/network.md#how-a-client-gets-to-a-3d-server) |
| The 6.113 full capture does not show that pair. TCP 14900 and TCP 14882 carry the Graal hello, and neither remote has a UDP datagram. No UDP port in the file is a TCP port plus one | [cap] (protocol/v6113-udp.md#against-port-plus-one) |
| The 3D connection lives only as long as the TCP one: when the lab TCP listener closed, the client reported "You have been disconnected from the game server." and sent a Torque disconnect | [run] (torque/network.md#the-full-handshake-live) |
| In 4.04r2 a Torque time-out ("The 3D server connection has timed out") also drops the TCP session | [bin] (graal3d/torque-engine-4x.md#callbacks-the-dll-gives-the-engine) |
| 4.04r2 gives the 3D side the account name, nickname and password through the engine; no session key or cookie is passed | [bin] (graal3d/torque-engine-4x.md#state-the-dll-receives) |
| If the 4.04r2 plug-in is missing, the launcher has the text "You need to download Graal3D at … for playing this server!"; when it shows it was not traced | [bin][inf] (graal3d/torque-engine-4x.md#connecting) |
| The 4.04r2 launcher still registers `graal3://` against `Graal3.exe`, the 3.x name | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |
| Each outcome fires a GS2 event: `onConnectionAccepted`, `onConnectRequestTimedOut`, `onConnectRequestRejected`, `onConnectionDropped`, `onConnectionError` | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |

TCP traffic in 3D mode, 4.04r2 [bin] (graal3d/torque-engine-4x.md#the-tcp-gserver-connection-in-3d-mode):

| Traffic | In 3D mode | Source |
| --- | --- | --- |
| S→C 0 `LEVELBOARD`, 14 `PLAYERWARP`, 28 `FLAGSET`, 31 `FLAGDEL`, 49 `PLAYERWARP2`, 101 `BOARDPACKET` | ignored; level, warps and flags come from the 3D server | [bin] (graal3d/torque-engine-4x.md#the-tcp-gserver-connection-in-3d-mode) |
| level requests at start-up, getweapon, client-variable and flag sets, server-side triggers | rerouted to the 3D server (→ §10.5.3) | [bin] (graal3d/torque-engine-4x.md#the-tcp-gserver-connection-in-3d-mode) |
| chat, PMs, the player list, file transfer, RC | not touched by the switch, so presumably still TCP | [inf] (graal3d/torque-engine-4x.md#the-tcp-gserver-connection-in-3d-mode) |
| missing 3D resources | one observed resource-miss branch normalizes the name, extracts its extension and requests a download only when it differs from `.dso`, `.cs` and `.ter`; this does not establish absence of local readers (→ §2.7) | [bin] (torque/404r2-resource-filter.md#download-filter) |

## 10.3 Handshake by build

### 10.3.1 Info packets

The first bit of a datagram picks the kind: 1 is a data packet of an established connection, 0 an info packet whose first byte is the type; all integers are little-endian [bin] (torque/network.md#torque-packet-framing).

| Type | Name | Direction | Body | Source |
| ---: | --- | --- | --- | --- |
| 26 (0x1A) | ConnectChallengeRequest | C→S | U32 connect sequence | [bin][run] (torque/network.md#torque-packet-framing) |
| 28 (0x1C) | ConnectChallengeReject | S→C | not handled by the Graal clients | [bin] (torque/network.md#torque-packet-framing) |
| 30 (0x1E) | ConnectChallengeResponse | S→C | U32 sequence, 4 × U32 address digest | [bin][run] (torque/network.md#torque-packet-framing) |
| 32 (0x20) | ConnectRequest | C→S | U32 sequence, 4 × U32 digest, string `GameConnection`, then the request fields (→ §10.3.2) | [bin][run] (torque/network.md#torque-packet-framing) |
| 34 (0x22) | ConnectReject | S→C | U32 sequence, string reason | [bin] (torque/network.md#torque-packet-framing) |
| 36 (0x24) | ConnectAccept | S→C | U32 sequence, the class table (from 3.153), U32 protocol (→ §10.3.3) | [bin][run] (torque/network.md#torque-packet-framing) |
| 38 (0x26) | Disconnect | both | U32 sequence, string reason | [bin][run] (torque/network.md#torque-packet-framing) |

Torque info packets come before the connection. The rules below say how they are routed and how strings in them are encoded [bin] (torque/network.md#torque-packet-framing).

| Rule | Source |
| --- | --- |
| Types below 23 go to the master-server and LAN query handler | [bin] (torque/network.md#torque-packet-framing) |
| A string is Torque `writeString`: one flag bit (1 = Huffman with Torque's fixed tree, 0 = raw), a U8 length, then the codes or bytes; fields after the first string are not byte-aligned | [bin][run] (torque/network.md#torque-packet-framing) |
| The address digest is TGE's MD5 over the client address, the sequence and a random server key | [bin][inf] (graal3d/torque-engine-4x.md#out-of-band-handshake) |
| There is no encryption beyond Torque's framing; the join password travels in clear | [bin] (torque/network.md#the-connect-request-by-version) |

### 10.3.2 Connect request by build

The request writes the net class group (U32, 0 = game) and the class CRC (U32), then the `GameConnection` fields [bin] (torque/network.md#the-connect-request-by-version).

| Field | 3.04 | 3.153 | 4.04r2 | 4.20r6 | 5.12 | Source |
| --- | --- | --- | --- | --- | --- | --- |
| game string | `Torque Game Engine Demo` | `Graal3D` | `Graal3D` | `Graal3D` | `Graal3D` | [bin] (torque/wire-by-build.md#the-handshake-per-build) |
| current = minimum protocol | 9 | 19 | 19 | 21 | 24 | [bin] (torque/wire-by-build.md#the-handshake-per-build) |
| class CRC | stock table, value unmeasured | unmeasured | `0xFFFFFFFF`, group 0 (captured from the Linux build; → §10.3.2) | unmeasured | `0xFFFFFFFF` (static table, never written) | [bin][run] (torque/wire-by-build.md#the-handshake-per-build); [lab] (protocol/lab-appe-hosta-2026-11-20.md#404r2-3d-connect-request-e501) |
| join password | the server-password pref | set by the engine, not traced | the account password, plain text | not traced | the account password, plain text | [bin] (torque/network.md#the-connect-request-by-version) |
| argc (at most 16), then strings | script args | engine-set, not traced | 2: account, nickname | not traced | 2: account, nickname | [bin] (torque/network.md#the-connect-request-by-version) |
| server side of the request | stock script `onConnectRequest` | stock script `onConnectRequest` | native | native | native | [bin] (torque/wire-by-build.md#the-handshake-per-build) |

**Settled question, formerly E#501: class CRC of the 4.04r2 3D plug-in.** Which class CRC a real 4.04r2 client sends in its 3D connect request was open between a stock-Torque reading and a static-table reading; a decoded capture settled it [lab] (protocol/lab-appe-hosta-2026-11-20.md#404r2-3d-connect-request-e501).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: the stock Torque class CRC, so a server must match the networked classes. B: a static table holding `0xFFFFFFFF` for group 0, computed by nothing | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll); [bin] (torque/wire-by-build.md#the-handshake-per-build) |
| Settled | The connect request of native Linux 4.04r2 (`G3D19026`), decoded from a lab capture, carries net class group 0 and class CRC `0xFFFFFFFF` | [lab] (protocol/lab-appe-hosta-2026-11-20.md#404r2-3d-connect-request-e501) |
| Verdict | Verified for the Linux build: Claim B holds. Windows 4.04r2 page-faults at the 3D start under Wine, so it was not captured | [lab] (protocol/lab-appe-hosta-2026-11-20.md#404r2-3d-connect-request-e501) |

The connect request differs by build. The rules below record a live 5.12 request decoded in full and how a 5.12 server rejects a wrong game string [run] (torque/network.md#the-full-handshake-live).

| Rule | Source |
| --- | --- |
| The live 5.12 request was 71 bytes and decoded completely: group 0, CRC `0xFFFFFFFF`, `Graal3D`, 24/24, the built-in guest password as join password, argc 2 (`guest`, empty nickname), no bits left over | [run] (torque/network.md#the-full-handshake-live) |
| A 5.12 server rejects a game string other than `Graal3D` with `CHR_GAME` ("Only official Graal clients are allowed to connect."), current < 24 with `CHR_PROTOCOL_LESS`, minimum > 24 with `CHR_PROTOCOL_GREATER`, and argc > 16 with `CR_INVALID_ARGS` | [bin] (torque/network.md#the-connect-request-by-version) |
| 4.04r2 knows the same reasons plus `CHR_PROTOCOL` and `CHR_INVALID`; it rejects < 19 and a minimum ≥ 20 | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |
| Stock Torque rejects a CRC mismatch with `CHR_INVALID`; in 5.12 the class table in the accept takes the CRC's place | [bin][run] (torque/network.md#the-connect-request-by-version) |

### 10.3.3 Connect accept and class table

The connect accept carries a class table. Each row gives one field of a table entry, its width and its meaning [bin][run] (torque/network.md#the-connect-request-by-version).

| Field | Width | Meaning | Source |
| --- | --- | --- | --- |
| flag | 1 bit | 1 = another entry follows, 0 = end of table | [bin][run] (torque/network.md#the-connect-request-by-version) |
| class type | 12 bits | 0 object, 1 datablock, 2 event (3.153, 4.04r2); 0 object, 1 event (4.20r6, 5.12; the event meaning is inferred) | [bin][inf] (torque/network.md#the-connect-request-by-version) |
| server class id | 12 bits | 0 to 255 | [bin] (torque/network.md#the-connect-request-by-version) |
| class name | string | Huffman string, such as `NetStringEvent` | [bin] (torque/network.md#the-connect-request-by-version) |
| protocol | U32 | after the end flag; must equal the build's protocol | [bin][run] (torque/network.md#the-connect-request-by-version) |

The rules below give how the client matches those entries to its own classes [bin] (torque/network.md#the-connect-request-by-version).

| Rule | Source |
| --- | --- |
| For each entry the client finds its own class of that name, type and group and records server id ↔ local id in two maps of 256 slots per group and type; class ids on the wire are then the server's | [bin] (torque/network.md#the-connect-request-by-version) |
| A name the client does not know maps to "unknown" and its data is skipped | [bin] (graal3d/torque-engine-4x.md#out-of-band-handshake) |
| Until a table is read the map is the identity (3.153) | [bin] (torque/wire-by-build.md#the-handshake-per-build) |
| An accept with an empty table (one 0 bit) and protocol 24 is enough for 5.12 to reach "Connection established" | [run] (torque/network.md#the-connect-request-by-version) |
| A stock accept without the table bit is read one bit off, gives protocol 12 and is silently rejected by 5.12 | [run] (torque/network.md#the-connect-request-by-version) |
| The class table is in 3.153 and 4.04r2 with three types, in 4.20r6 and 5.12 with two types; 3.04 has none | [bin] (torque/wire-by-build.md#the-handshake-per-build) |
| Each build accepts exactly its own protocol (9, 19, 19, 21, 24); anything else gives `CHR_PROTOCOL` | [bin] (torque/network.md#the-connect-request-by-version) |

### 10.3.4 Live handshake (5.12)

A live 5.12 handshake was captured. Each row is one packet, with its time from the first and its direction [run] (torque/network.md#the-full-handshake-live).

| Time | Direction | Packet | Source |
| --- | --- | --- | --- |
| +0.000 s | C→S | challenge request, sequence 1024 | [run] (torque/network.md#the-full-handshake-live) |
| +0.000 s | S→C | challenge response with the lab server's digest | [run] (torque/network.md#the-full-handshake-live) |
| +3.009 s | C→S | connect request, 71 bytes (the 3 s gap was the lab injector's own wait) | [run] (torque/network.md#the-full-handshake-live) |
| +3.009 s | S→C | connect accept: sequence, empty class table, protocol 24 | [run] (torque/network.md#the-full-handshake-live) |
| +3.043 s | C→S | first data packet, sequence 1, with the "max rate" flag and two 12-bit values (2080 and 368 in the stock field order) | [run] (torque/network.md#after-the-connection-is-accepted) |
| then | C→S | one 17-byte data packet a second with no events, and a ping after about 4.6 s with nothing acknowledged | [run] (torque/network.md#after-the-connection-is-accepted) |
| +18.02 s | C→S | disconnect, sequence 1024, empty reason | [run] (torque/network.md#the-full-handshake-live) |

The client's console logged the same steps: "Sending Connect challenge Request", "Got Connect challenge Response", "Sending Connect Request", "Connection established", and at the end "Issuing Disconnect packet." [run] (torque/network.md#the-full-handshake-live).

### 10.3.5 Data packets

The rules below give the header of a Torque data packet as stock TGE writes it [bin][run] (torque/network.md#after-the-connection-is-accepted).

| Rule | Source |
| --- | --- |
| Header (stock TGE): flag 1, a sequence-parity bit, 9-bit sequence, 9-bit highest ack, 2-bit type (0 data, 1 ping, 2 ack), 3-bit ack byte count, then the ack mask | [bin][run] (torque/network.md#after-the-connection-is-accepted) |
| Then a flag → 10-bit update delay and 10-bit packet size, and a flag → two 10-bit max-rate values | [bin] (graal3d/torque-engine-4x.md#packet-header-and-rates) |
| 4.04r2 rate prefs: to server 32 (8–32), to client 32 (1–32), packet size 800 with an allowed range of 100–450; the update delay is 1024 / rate ms, so in practice 32 packets/s of 450 bytes | [bin] (graal3d/torque-engine-4x.md#packet-header-and-rates) |

Game-packet bodies after the header [bin] (graal3d/torque-engine-4x.md#server--client-data-packet); [bin] (torque/wire-by-build.md#512-game-packets-the-gameobject-era):

| Part | 4.04r2 | 4.20r6, 5.12 | Source |
| --- | --- | --- | --- |
| S→C move ack | int32 last move ack | none | [bin] (torque/wire-by-build.md#512-game-packets-the-gameobject-era) |
| S→C damage flash and white-out | flag → { flag → float7; flag → float7 } | none | [bin] (graal3d/torque-engine-4x.md#server--client-data-packet) |
| S→C control object | flag → flag (dirty) → u32 server time, int12 ghost index, the object's data; else 3 × F32 compression point | flag → flag → u32 server time (ms), int12 ghost index of a `GameObject`, its data; the first control object starts login step 5 | [bin] (torque/wire-by-build.md#512-game-packets-the-gameobject-era) |
| S→C camera | flag → int12 camera ghost, flag → camera data | the same; no flag clears the camera | [bin] (torque/wire-by-build.md#512-game-packets-the-gameobject-era) |
| S→C field of view | flag → int8 | flag → int8 | [bin] (torque/wire-by-build.md#512-game-packets-the-gameobject-era) |
| C→S first flag | first person [inf] | set when a connection float is 0; meaning not traced | [inf] (torque/wire-by-build.md#512-game-packets-the-gameobject-era) |
| C→S position | 3 × F32 position of the control object, flag → int12 its ghost index | the same, or the ghost of the object it is mounted on | [bin] (torque/wire-by-build.md#512-game-packets-the-gameobject-era) |
| C→S state | flag → the control object's data; else int32 first move index, int5 move count (up to 30), the moves | flag → the control object's data; no move branch | [bin] (torque/wire-by-build.md#512-game-packets-the-gameobject-era) |
| C→S field of view | flag → int8 | flag → int8, clamped to 1–179 | [bin] (torque/wire-by-build.md#512-game-packets-the-gameobject-era) |
| Both, then | events, then ghosts | events, then ghosts | [bin] (torque/wire-by-build.md#512-game-packets-the-gameobject-era) |

Graal adds to the stock data packet. The rules below give those additions and what 5.12 reports in them [bin] (graal3d/torque-engine-4x.md#server--client-data-packet).

| Rule | Source |
| --- | --- |
| The u32 server time is a Graal addition; the client keeps it as its synchronised clock | [bin] (graal3d/torque-engine-4x.md#server--client-data-packet) |
| In 5.12 the client always reports its own position and never sends a Torque `Move`; position is client-reported as in 2D Graal | [bin] (torque/wire-by-build.md#512-game-packets-the-gameobject-era) |
| Unguaranteed events: flag 1, int12 class id, sized payload, …, flag 0; guaranteed-ordered events add a flag (next in sequence) else int7 sequence | [bin] (graal3d/torque-engine-4x.md#events) |
| Ghosts: flag, int4 index width (sent as is; TGE sends width − 3), then per ghost flag 1, index, flag (delete), and if not deleted int12 class id on every update and the sized data; flag 0 ends | [bin] (graal3d/torque-engine-4x.md#ghosts-graal-changes) |
| The 12-bit ghost index and the 4-bit width field are the TGE-line constants `GhostIdBitSize = 12` and `GhostIndexBitSize = 4`, as in Torque2D. Torque3D raised `GhostIdBitSize` to 18, so a server that copies Torque3D's constants writes every ghost index 6 bits too wide | [doc][bin] (torque/open-source-lineage.md#what-matches) |
| New ghosts go into the client's `MissionGroup`; in 4.04r2 they wait while TCP file downloads are running | [bin] (graal3d/torque-engine-4x.md#ghosts-graal-changes) |
| In 5.12 the class id reader takes 12 bits and applies the server-to-local map; events and ghosts each have their own length wrappers | [bin] (torque/wire-by-build.md#512-game-packets-the-gameobject-era) |

### 10.3.6 Mission download

Mission download runs in phases, and 5.12 drops one. Each row gives a group of builds and its phases [bin][file] (torque/network.md#after-the-connection-is-accepted).

| Build | Phases | Source |
| --- | --- | --- |
| 3.153, 4.04r2 (stock TGE) | 1 "Download Datablocks & Targets", 2 "Download Ghost Objects", 3 "Mission Lighting" | [bin][file] (torque/network.md#after-the-connection-is-accepted) |
| 5.12 | 1 "Download Ghost Objects", 2 "Mission Lighting" | [bin] (torque/network.md#after-the-connection-is-accepted) |

The rules below give how the server drives the phases and how the client answers [bin] (torque/network.md#after-the-connection-is-accepted).

| Rule | Source |
| --- | --- |
| The server drives the phases with `MissionStartPhaseN` remote commands and the client answers `MissionStartPhaseNAck` | [bin] (torque/network.md#after-the-connection-is-accepted) |
| In 3.153 these are script functions; phase 1 acks with the sequence number, and phase 3 lights the scene and acks when lighting is done | [file] (torque/network.md#after-the-connection-is-accepted) |
| In 4.04r2 they are native; the acks carry only the command tag, no sequence number; every other `commandToClient` name is ignored | [bin] (graal3d/torque-engine-4x.md#mission-start) |
| 4.04r2 raises `onGraal3DLoginStep` 1 to 5: phases 1, 2 and 3, lighting done (`$missionRunning = 1`), and the first control object (switch to the 3D GUI) | [bin] (graal3d/torque-engine-4x.md#mission-start) |
| Mac 4.04r2 raises the same 1 to 5. Step 5 looks up `GUIContainer3D` and attaches it if a condition holds. This was read in the Mac executable itself, not carried over from the Windows plug-in. | [bin] (client-internals/mac-ppc-runtime-surface-2026-11-09.md#3d-mission-stages-in-mac-404r2) |
| 5.12 starts the value at −1 and raises 2 (phase 1), 3 (phase 2), 4 (lighting done), 5 (first control object) and 6 (TCP file downloads finished, the `GraalControl3D` GUI attached) | [bin] (torque/wire-by-build.md#512-game-packets-the-gameobject-era) |
| The 3.153 loading screen is a snowball rolling across `LoadingGui`, with the Christmas 2004 3D images | [file] (torque/scripting.md#what-the-3153-scripts-do) |

The retained Windows 4.04r2 review traces native datablock/ghost/lighting phase dispatch and network-class construction into the mission group, with a deferred-preload path. This is positive network-mission evidence; a 2026-11-20 lab session with marker files beside the client opened no local `.mis`, `.cs` or `.dso` (→ §10, the settled questions formerly E#502 and E#503). [bin] (torque/404r2-resource-filter.md#positive-native-mission-path)

### 10.3.7 The session from a client's side

The UDP session has been run end to end with a real 5.12 client against a lab server, through login step 6 and a drawn 3D view; 4.20r6's protocol 21 shares its packet shapes. The rules below are what a clean-room client needs beyond the layouts above [lab][bin] (torque/udp-session.md#1-two-connections-one-session).

| Rule | Source |
| --- | --- |
| The 3D decision is made on the server name alone; no login type or packet flag says "3D". A `PLO_SERVERWARP` to a name starting `3 ` opens the two links as picking it from the list does | [bin] (torque/udp-session.md#1-two-connections-one-session) |
| The challenge request leaves before, or in the same millisecond as, the TCP connect, so a client must not wait for the TCP login before starting the handshake | [run] (torque/udp-session.md#ordering-and-matching) |
| A server ties the UDP link to the TCP session by the account name in the connect request and the source address. A 5.x guest sends `guest` there, not its assigned guest name. The client repeats the connect request until it is accepted, and gives up after about 15 s with "The connection to the Graal3D server couldn't be established." | [lab] (torque/udp-session.md#ordering-and-matching) |
| For the 5.12 3D view to show, every TCP file request the world causes must be answered, with the file or `PLO_FILESENDFAILED`, because login step 6 waits for them all; and the "Connecting..." window closes only on `PLO_SERVERLISTCONNECTED` | [lab] (torque/udp-session.md#what-a-512-client-needs-on-tcp-for-the-3d-view-to-show) |
| Bits are packed least significant first. Strings inside data packets carry one extra flag before the usual string: set, it reuses a prefix of the previous string in the same packet. This holds for protocol 24 in both directions; a writer may always send the flag clear | [lab] (torque/udp-session.md#2-bit-stream-conventions) |
| Protocol 9 (Linux 3.04) is stock TGE 1.x networking with no Graal changes and ships no 3D scripts; no 3D server for it is known | [bin] (torque/udp-session.md#10-protocol-19-3153-404r2-what-differs) |

### 10.3.8 A full 5.12 session, decoded

A real Windows 5.12 client was traced from inside its own process against a lab server holding a ground, a cube, sun, sky, a camera and one GS2 movement weapon. All 319 datagrams of an idle session decode with the layouts above, and a second run of 583 datagrams added walking and closing. The rules below are what the traces settle [lab] (torque/lab-2026-11-12-udp-trace.md#what-the-trace-settles).

| Rule | Source |
| --- | --- |
| Order: challenge, response, connect request (with `guest` and the nickname), the TCP login burst, the accept (10 object and 9 event classes, protocol 24), then the client's first data packet with its rate pair (32 ms, 450 bytes). The server never sent a rate field | [lab] (torque/lab-2026-11-12-udp-trace.md#timeline) |
| The mission acks go as `RemoteCommandEvent` plain strings, not tags; every client event is guaranteed-ordered | [lab] (torque/lab-2026-11-12-udp-trace.md#what-the-trace-settles) |
| The client acks every server data packet at once with a 5-byte ack packet; 124 of its 191 data-link packets were acks. Idle, it sent a data packet every 1.7 s on average, the server about every 0.9 s | [lab] (torque/lab-2026-11-12-udp-trace.md#what-the-trace-settles) |
| Padding bits are not always zero, so a reader stops at the last field. Connect sequence 0 is valid | [lab] (torque/lab-2026-11-12-udp-trace.md#what-the-trace-settles) |
| On taking its control object the client echoes that object's shape, transform and flags once; a zero rotation comes back as axis (1, 0, 0). Later packets carry an empty update and the position | [lab][inf] (torque/lab-2026-11-12-udp-trace.md#what-the-trace-settles) |
| The client re-sends `w <weapon>` for its movement weapon about every 2.3 s, so a server must treat a repeated `w` as harmless | [lab][inf] (torque/lab-2026-11-12-udp-trace.md#what-the-trace-settles) |
| The ghost index width is the bit count of the highest index in that packet | [lab] (torque/lab-2026-11-12-udp-trace.md#what-the-trace-settles) |
| After the first 1.35 s the client sent nothing on TCP. Killed, it sends no UDP disconnect; the server notices the TCP close | [lab] (torque/lab-2026-11-12-udp-trace.md#what-the-trace-settles) |
| Walking sends nothing new: the arrow keys reached the GS2 script, but every client packet stayed the same apart from counters, because protocol 24 has no moves and the client cannot move its own control object. A server has to drive the player's movement, with a movetype and movement data on the control object (settled below). Enter opened no chat bar in the 3D view | [lab] (torque/lab-2026-11-12-udp-trace.md#lab-12b-walking-chat-and-closing-rerun) |

**Settled question, formerly E#505: How a server makes a 5.12 player move in 3D.** How a server is meant to move a 5.12 player in 3D, when protocol 24 has no moves and the client's script cannot move its control object, was open. A lab server that gave the control object a movetype and movement data settled it [lab] (protocol/lab-appe-hosta-2026-11-20d.md#how-a-server-moves-a-512-player-in-3d-e505).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | With a movetype and movement data on its control object, 5.12 moves the object itself and reports where it is: interpolate and rigid glide with a lag of 0.25 to 0.5 units, list jumps exactly onto each position | [lab] (protocol/lab-appe-hosta-2026-11-20d.md#how-a-server-moves-a-512-player-in-3d-e505) |
| Settled | What the client echoes: interpolate sends section 7 every update, list sends section 5 every update, rigid sends no object section; interpolate and list also send sections 3, 5, 6 and 13 once at the start. Without a movetype it sends only its position | [lab] (protocol/lab-appe-hosta-2026-11-20d.md#how-a-server-moves-a-512-player-in-3d-e505) |
| Verdict | Verified on Windows 5.12; the best guess holds, and the movement-data layout as read was accepted with no desync | [lab] (protocol/lab-appe-hosta-2026-11-20d.md#how-a-server-moves-a-512-player-in-3d-e505) |
| Left over | Keyboard input together with a movetype, and a view that follows the player object | [lab] (protocol/lab-appe-hosta-2026-11-20d.md#how-a-server-moves-a-512-player-in-3d-e505) |

### 10.3.9 Protocol 19 past the handshake: what a server sends

Protocol 19 has static layout evidence, earlier partial GPL-server runs and separate later native Linux 4.04r2 and shimmed Mac 3.153 camera-path observations. The later Mac study uses the Rust Seihai gserver; these cohorts do not revalidate the unchanged GPL fixture or its intended Windows 4.04r2 input. The retained `P19-LATER-LAB-20261114` receipt reports GPL revision `c4f786be`; reviewed logs do not independently bind that executable to the revision. Their reported provenance and limits are qualified in [lab] (torque/protocol19-server.md#10-later-lab-scope). A static read of the 4.04r2 plug-in and the 3.153 mission scripts gives what a server must send, using the smallest control object these clients take, a stock `Camera`. The handshake, header, rate fields, string buffer, event lists and ghost section are those of protocol 24; the accept's class table has three types: object, datablock, event [bin] (torque/protocol19-server.md#1-what-is-the-same-as-protocol-24).

| Rule | Source |
| --- | --- |
| A move is three optional `int16` rotations (sent only when non-zero), `int6` x, y and z with 16 for no movement, then a free-look flag and ten trigger flags; a move with no rotation is 32 bits. A `Camera` or `Player` client sends moves; only a control object with the vehicle type bit sends its own state | [bin] (torque/protocol19-server.md#3-client--server-game-section) |
| The camera ghost must be a `ShapeBase`, or the client logs "Received unknown camera object" and drops the rest of the packet; the client drops queued moves up to the server's move ack | [bin] (torque/protocol19-server.md#2-server--client-game-section) |
| Connection messages use TGE 1.x numbering: 0 ghost-always done, 1 ready for normal ghosts, 2 end ghosting, 3 ghost-always starting, 5 datablocks done, 6 datablocks download done. Torque3D numbers the last pair 6 and 7. Messages 0, 2, 3 and 4 before a ghost table exists are refused as "Invalid packet" | [bin] (torque/protocol19-server.md#4-connection-messages-tge-1x-numbering) |
| A workable order: phase 1; on its ack the datablocks, then message 5; on message 6, phase 2, message 3 and the ghosts; when phase 2 is acked, message 0 and phase 3; on phase 3's ack, the control object. A ghost naming a datablock the client has not loaded drops the connection | [bin][srv] (torque/protocol19-server.md#5-mission-start) |
| The smallest `CameraData` is 137 bits with empty names; the `Camera` ghost update and packet data carry position, two rotation angles and a mode (0 stationary to 4 orbit point) | [bin][srv] (torque/protocol19-server.md#7-cameradata--shapebasedata-nothing-of-its-own) |
| Still unread: `ShapeBase`'s main update section and the `Player` layouts, which other players need; 3.153 matches 4.04r2 on the camera path (settled below) | [bin][inf] (torque/protocol19-server.md#open) |

**Settled question, formerly E#506: Protocol 19 against a real 3.153 or 4.04r2 client.** Whether a real 3.153 or 4.04r2 accepts the protocol-19 server order read statically was open. 4.04r2 ran it earlier; the Mac PowerPC 3.153 on a Tiger guest settled the rest [lab] (protocol/lab-appe-hostb-2026-11-20d.md#protocol-19-on-the-mac-3153-e506).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | The real 3.153 completes the camera path: UDP challenge, phases 1 to 3, the `Camera` and `Sky` ghosts and the initial control object, then keeps the link (61 moves over about 2.5 minutes) with no crash | [lab] (protocol/lab-appe-hostb-2026-11-20d.md#protocol-19-on-the-mac-3153-e506) |
| Settled | 3.153 picks a 3D server from the list tag: a server listed at HQ level 1 (tag `H `) is filed as Hosted and treated as 2D, and no UDP is sent; HQ level 4 (tag `3 `) works | [lab] (protocol/lab-appe-hostb-2026-11-20d.md#protocol-19-on-the-mac-3153-e506) |
| Verdict | Verified for the camera path on 3.153 and 4.04r2; the best guess holds | [lab] (protocol/lab-appe-hostb-2026-11-20d.md#protocol-19-on-the-mac-3153-e506) |
| Left over | Other players need the unread `Player` layouts and a real `.dts` player shape, which is not held; the drawn view under QEMU's software renderer was not checked | [inf] (torque/protocol19-server.md#open) |

### 10.3.10 3.153 and 4.04r2 against a lab server

Both older builds were run against the project's own gserver in 3D mode. The table gives what each did; the script side is in → §8.5.1 and → §8.5.7 [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md).

| Item | 3.153 (Mac OS X PPC) | 4.04r2 | Source |
| --- | --- | --- | --- |
| acceptance | protocol 19, no special handling by the server | ran under Wine on Linux; crashes at start on the Windows 10 VM | [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#3153); [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#404r2) |
| mission phases | all three stock phases | all three: datablocks, ghosts, lighting | [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#3153); [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#404r2) |
| control object | stock `Player` | stock `Player`; the client sends Torque moves only, no position reports | [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#3153); [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#404r2) |
| requirements seen | crashes without a ghosted `Sky`; with one, holds the link about three minutes and quits cleanly | n/a | [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#3153) |
| what it requests | `.dts` shapes and textures by bare name; sky textures as `.gif`, never `.png`; never `.cs`, `.dso` or `.ter` | unmeasured | [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#3153) |
| terrain | a `TerrainBlock` makes it request chunks and `heights.info`; with no terrain on the server it then crashes | n/a | [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#3153) |
| what drew | nothing 3D; the screen stayed on the loading picture | only the sky gradient | [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#3153); [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#404r2) |

### 10.3.11 Several clients in one world: first lab pairs

Real clients were paired against the project's own gserver while its relay of other players was still changing. The table records what the clients did on that build; it is a state on 2026-11-25, not a settled rule [lab] (torque/multi-client-3d-lab-2026-11-25.md).

| Pair | What the clients did | Source |
| --- | --- | --- |
| 5.24r3 2D and 5.12 3D, one level | the 2D client's `players` count was 2 but the 3D entry was empty and never drew; the 3D client never saw the 2D player (`players` 0, no ghost); 2D chat reached the 3D client as `onRemotePlayerChats` over TCP; 3D chat and flags never reached the 2D client; neither side got a leave event | [lab][cap] (torque/multi-client-3d-lab-2026-11-25.md#h1-a-2d-client-and-a-3d-client-in-one-level) |
| two 5.12 3D clients | each got a `G3DPlayer_<other>` object within the same second of the other's join; chat was relayed but positions were not, so each kept the other at the shared spawn; `players` stayed 0 and no per-player events fired; no ghost delete on leave, and the ghost returned under the same index on reconnect | [lab][cap] (torque/multi-client-3d-lab-2026-11-25.md#s1-two-3d-clients-in-one-world) |

### 10.3.12 Malformed server packets (network fuzz, tier 1)

Real 5.12 and 4.04r2 clients were fed one seeded mutation per link from the project's own server: 27 runs on 5.12 and 9 on 4.04r2 under Wine; both baselines load cleanly [lab][cap] (torque/3d-fuzz-net-tier1-2026-11-25.md). The table gives each kind of mutation and what the clients did.

| Mutation | 5.12 | 4.04r2 | Source |
| --- | --- | --- | --- |
| `RemoteCommandEvent` one bit shorter than its declared length | one seed ran a garbled remote command and then crashed in the 3D engine; the other seeds survived; the event length wrapper is trusted | survived where run | [lab][cap] (torque/3d-fuzz-net-tier1-2026-11-25.md#crashes-and-bad-behaviour) |
| update to a ghost index never created | logs and drops the update (all three seeds) | crash (access violation) | [lab][cap] (torque/3d-fuzz-net-tier1-2026-11-25.md#crashes-and-bad-behaviour) |
| wrong protocol number in the connect accept | link dropped within about 70 ms, black screen, no message | the same | [lab][cap] (torque/3d-fuzz-net-tier1-2026-11-25.md#crashes-and-bad-behaviour) |
| event classes dropped or renamed in the class table; unknown event class; double ghost delete; a different ghost-index width; control object set to a `Sky` or `Sun` ghost; control object deleted | survived, some logging "Invalid event received (unknown event type)" or "(wrong direction)" | survived where run | [lab][cap] (torque/3d-fuzz-net-tier1-2026-11-25.md#survived-sometimes-with-a-console-line) |

### 10.3.13 When UDP or TCP drops (Linux 4.20r6)

A Linux 4.20r6 client (3D-equal to Windows 4.20r8, → §10.1.12) was run on loopback against the project's own 3D lab server, through a relay that could drop UDP or close TCP; each change was made at 40 s, after the world was up [lab] (torque/3d-link-drop-420r6-2026-11-25.md#lab-lab).

| Rule | Source |
| --- | --- |
| Every 4500 ms without a sent ping or a received packet, the client sends a ping; after 8 unanswered pings it times the connection out, so a silent server is dropped about 40.5 s after its last packet | [bin] (torque/3d-link-drop-420r6-2026-11-25.md#static-the-ping-and-timeout-rule-bin) |
| A received packet resets the ping count | [inf] (torque/3d-link-drop-420r6-2026-11-25.md#static-the-ping-and-timeout-rule-bin) |
| UDP lost for 10 s with TCP kept: nothing visible or logged, and the link healed silently when UDP returned, with no new connect | [lab] (torque/3d-link-drop-420r6-2026-11-25.md#lab-lab) |
| UDP lost for good: 8 pings 4.51 s apart, updates stop after 30 unacknowledged, timeout 40.6 s after the last server packet; the client sends a 7-byte disconnect, closes its own TCP to the gserver and returns to the login screen ("The 3D server connection has timed out") | [lab] (torque/3d-link-drop-420r6-2026-11-25.md#lab-lab) |
| Both TCP legs closed: the server sent a UDP disconnect within 1 ms and the client returned to login ("The Graal3D server has dropped the connection: …"); only the client's TCP leg closed: the client sent a UDP disconnect within about 10 ms and returned to login | [lab] (torque/3d-link-drop-420r6-2026-11-25.md#lab-lab) |
| No run crashed the client and none made it reconnect on its own; the 3D link never outlives the TCP link | [lab] (torque/3d-link-drop-420r6-2026-11-25.md#for-server-work) |

### 10.3.14 Script events from client to server (Linux 4.20r6)

In builds where the 2D and 3D engines share a binary, the 3D side gives the 2D side a hook that queues a line for the 3D server and a per-frame flush that sends the queued lines [bin] (torque/3d-client-events-420r6-2026-11-25.md#static-bin). What a weapon script sees is in → §8.5.7.

| Rule | Source |
| --- | --- |
| Each queued line starts with a one-letter code: `t` trigger (`triggerserver`, weapon or rc form), `o` object, `g` class or gani request, `w` weapon request, `s` flag write | [bin] (torque/3d-client-events-420r6-2026-11-25.md#static-bin) |
| At the end of each 2D object tick the lines are joined with newlines and sent as one BigData text of kind `events`, with an empty weapon name and option, over the Torque UDP link | [bin] (torque/3d-client-events-420r6-2026-11-25.md#static-bin) |
| The same code handles server-to-client texts of kinds `set`, `unset`, `events`, `addweapon`, `weaponscript`, `deleteweapon`, `npcscript`, `classscript`, `ganiscript`, `setmaterials` and `rpg` | [bin] (torque/3d-client-events-420r6-2026-11-25.md#static-bin) |
| Live: `triggerserver("weapon","Ev3D",…)` went out as `t weapon,Ev3D,<params>`, a flag write as `s client.evflag3=<value>`, and after `weaponscript` arrived the client sent `w Ev3D` | [lab] (torque/3d-client-events-420r6-2026-11-25.md#lab-lab) |
| Live, the 2D TCP link carried only start-up file requests, update checks, a one-byte id 24 about every 0.4 s, id 162 every 30 s (answered by 108) and typed chat as player prop 12; no script marker went over TCP | [lab] (torque/3d-client-events-420r6-2026-11-25.md#lab-lab) |
| So a 3D server reads script triggers, flag writes and requests from the UDP `events` text, script chat from the player's object update, and typed chat from TCP; script PMs and `setplayerprop` never arrive | [lab] (torque/3d-client-events-420r6-2026-11-25.md#for-server-work) |

### 10.3.15 Local files against the server's copy (Linux 4.20r6)

When the 3D world names a file, a Linux 4.20r6 client checks it over the 2D TCP link, and the server decides which copy is used [lab] (torque/3d-file-preference-420r6-2026-11-25.md#the-check-on-the-wire-lab).

| Rule | Source |
| --- | --- |
| If the client has the file it sends `PLI_UPDATEFILE` (34) with a GINT5 modtime (the local file's Unix mtime in seconds) and the name; if not, `PLI_WANTFILE` (23) with the name | [lab] (torque/3d-file-preference-420r6-2026-11-25.md#the-check-on-the-wire-lab) |
| If the server's copy is newer it sends the file (`PLO_RAWDATA` 100, then `PLO_FILE` 102 carrying the server's modtime); otherwise it answers `PLO_FILEUPTODATE` (45). The client compares nothing itself | [lab] (torque/3d-file-preference-420r6-2026-11-25.md#the-check-on-the-wire-lab) |
| Between two local copies (data folder and user folder `levels3d/`), the newer one is sent and drawn, whichever folder it is in | [lab] (torque/3d-file-preference-420r6-2026-11-25.md#lab-lab) |
| A download is saved in the user folder under `levels3d/images/` with the server's modtime, never over a data-folder copy, and keeps winning in later sessions while it is the newest | [lab] (torque/3d-file-preference-420r6-2026-11-25.md#lab-lab) |
| The client never wrote `FILENAMECACHE.txt` in seven sessions, so a stale cache could not be tested | [lab] (torque/3d-file-preference-420r6-2026-11-25.md#answers) |
| Zip members are never checked (→ §10.6), so a zip in `levels3d/` overrides the server whatever the modtimes | [lab] (torque/3d-file-preference-420r6-2026-11-25.md#answers) |

### 10.3.16 2D level packets in a 3D session (Linux 4.20r6)

Once the 3D world was up, the lab server sent a Linux 4.20r6 client (3D-equal to Windows 4.20r8) the normal 2D level packets over TCP: `PLO_LEVELNAME` (6), `PLO_BOARDPACKET` (101), `PLO_NPCPROPS` (3), `PLO_LEVELSIGN` (5), `PLO_LEVELLINK` (1), `PLO_LEVELCHEST` (4) and `PLO_BADDYPROPS` (2) [lab] (torque/3d-2d-level-packets-420r6-2026-11-25.md#results-lab).

| Rule | Source |
| --- | --- |
| The gserver already sends the start level's name, board and chests at login, so 2D level content reaches a 3D session even when nothing is injected | [lab] (torque/3d-2d-level-packets-420r6-2026-11-25.md#results-lab) |
| Every packet arrived and was accepted without a disconnect | [lab] (torque/3d-2d-level-packets-420r6-2026-11-25.md#results-lab) |
| Nothing was drawn: every screenshot matched the plain 3D view | [lab] (torque/3d-2d-level-packets-420r6-2026-11-25.md#results-lab) |
| The client acted on none of it: no NPC or baddy image request, no further packets but heartbeats | [lab] (torque/3d-2d-level-packets-420r6-2026-11-25.md#results-lab) |
| The packets are dropped because the 3D view control owns the screen and the 2D level renderer is not shown; no static trace was done | [inf] (torque/3d-2d-level-packets-420r6-2026-11-25.md#results-lab) |

### 10.3.17 A world past its limits (Linux 4.20r6)

A Linux 4.20r6 client (3D-equal to Windows 4.20r8) was fed far positions, odd shapes and many `GameObject`s from the project's own 3D lab server; every run reached "Graal3D has been activated!", stayed connected and logged no error, clamp or "too many" [lab] (torque/3d-world-limits-420r6-2026-11-25.md#results-lab).

| Rule | Source |
| --- | --- |
| Finite positions up to ±1e9 on any axis are accepted, ghosted and drawn, with no clamp | [lab] (torque/3d-world-limits-420r6-2026-11-25.md#findings) |
| The project's gserver refuses to ghost a `GameObject` with an `inf` or `nan` position, so the client's own handling of a non-finite ghost was not exercised | [lab] (torque/3d-world-limits-420r6-2026-11-25.md#findings) |
| A shape about 5000 units across draws (the camera ends up inside it); a negative-size shape draws; a `.3ds` with a NaN vertex draws as a normal cube | [lab] (torque/3d-world-limits-420r6-2026-11-25.md#findings) |
| 100 and 1000 `GameObject`s were all created and drawn, with no ghost-count limit and no disconnect over 55 s; frame rate was not measured | [lab] (torque/3d-world-limits-420r6-2026-11-25.md#findings) |

## 10.4 DSO v33

Graal 3.x keeps menus, options, key binds, message boxes and the 3D mission-loading flow in compiled TorqueScript; from 4.x on no `.dso` files ship [file] (torque/scripting.md#torquescript-in-graal-3x-the-dso-format-and-the-shipped-scripts).

### 10.4.1 Shipped scripts

Each build ships its own set of compiled scripts. The table gives a build and what its scripts cover [file] (torque/scripting.md#torquescript-in-graal-3x-the-dso-format-and-the-shipped-scripts).

| Build | Scripts | Source |
| --- | --- | --- |
| 3.04 Linux | 39 compiled scripts in the TGE starter layout; a PM window and a player list in script; no 3D scripts | [file] (torque/scripting.md#torquescript-in-graal-3x-the-dso-format-and-the-shipped-scripts) |
| 3.153 Mac | 44 compiled scripts (`scripts/`, `scripts2D/`, `scriptsgui/`) and 13 plain `.cs` files (prefs, key configs, nine language tables); adds the 3D client scripts | [file] (torque/scripting.md#torquescript-in-graal-3x-the-dso-format-and-the-shipped-scripts) |
| 4.x and later | none; menus are native or GS2 | [file] (torque/scripting.md#torquescript-in-graal-3x-the-dso-format-and-the-shipped-scripts) |

### 10.4.2 File layout

All integers little-endian [file] (torque/scripting.md#file-format-version-33).

| Field | Notes | Source |
| --- | --- | --- |
| U32 version | 33 | [file] (torque/scripting.md#file-format-version-33) |
| U32 size, bytes | global string table, NUL-separated | [file] (torque/scripting.md#file-format-version-33) |
| U32 count, count × F64 | global float table | [file] (torque/scripting.md#file-format-version-33) |
| U32 size, bytes | function string table | [file] (torque/scripting.md#file-format-version-33) |
| U32 count, count × F64 | function float table | [file] (torque/scripting.md#file-format-version-33) |
| U32 codeLength, U32 lineBreakPairCount | | [file] (torque/scripting.md#file-format-version-33) |
| code | `codeLength` words; each one byte, or `0xFF` then a U32 | [file] (torque/scripting.md#file-format-version-33) |
| lineBreakPairCount × 2 × U32 | line and ip pairs | [file] (torque/scripting.md#file-format-version-33) |
| U32 identCount, then per ident U32 string offset, U32 count, count × U32 ip | patches identifier words in the code with global-string entries | [file] (torque/scripting.md#file-format-version-33) |

Compiled TorqueScript files have tables for strings and numbers. The rules below give how they are used and one byte-order difference on the Mac [file] (torque/scripting.md#file-format-version-33).

| Rule | Source |
| --- | --- |
| Code inside a function body uses the function tables; code outside uses the global tables | [file] (torque/scripting.md#file-format-version-33) |
| The Mac PPC build writes the F64 tables big-endian while the rest stays little-endian; the 3.04 Linux files are little-endian throughout | [file] (torque/scripting.md#file-format-version-33) |
| An argument the body never uses gets an ident offset just past the end of the global string table, so its name is lost | [file] (torque/scripting.md#file-format-version-33) |
| All 83 shipped files decode with the opcode table below and no other | [file] (torque/scripting.md#graals-opcode-table) |

### 10.4.3 Opcodes

The numbering is stock TGE 1.0–1.3 (DSO version 33): two unused opcodes follow `CREATE_OBJECT` and one follows `CALLFUNC`; TGE 1.4 dropped those slots [file] (torque/scripting.md#graals-opcode-table); [doc] (torque/open-source-lineage.md#what-matches).

| # | Opcode | # | Opcode | # | Opcode | Source |
| ---: | --- | ---: | --- | ---: | --- | --- |
| 0 | FUNC_DECL | 28 | SHL | 56 | STR_TO_UINT | [file] (torque/scripting.md#graals-opcode-table) |
| 1 | CREATE_OBJECT | 29 | AND | 57 | STR_TO_FLT | [file] (torque/scripting.md#graals-opcode-table) |
| 2 | unused | 30 | OR | 58 | STR_TO_NONE | [file] (torque/scripting.md#graals-opcode-table) |
| 3 | unused | 31 | ADD | 59 | FLT_TO_UINT | [file] (torque/scripting.md#graals-opcode-table) |
| 4 | ADD_OBJECT | 32 | SUB | 60 | FLT_TO_STR | [file] (torque/scripting.md#graals-opcode-table) |
| 5 | END_OBJECT | 33 | MUL | 61 | FLT_TO_NONE | [file] (torque/scripting.md#graals-opcode-table) |
| 6 | JMPIFFNOT | 34 | DIV | 62 | UINT_TO_FLT | [file] (torque/scripting.md#graals-opcode-table) |
| 7 | JMPIFNOT | 35 | NEG | 63 | UINT_TO_STR | [file] (torque/scripting.md#graals-opcode-table) |
| 8 | JMPIFF | 36 | SETCURVAR | 64 | UINT_TO_NONE | [file] (torque/scripting.md#graals-opcode-table) |
| 9 | JMPIF | 37 | SETCURVAR_CREATE | 65 | LOADIMMED_UINT | [file] (torque/scripting.md#graals-opcode-table) |
| 10 | JMPIFNOT_NP | 38 | SETCURVAR_ARRAY | 66 | LOADIMMED_FLT | [file] (torque/scripting.md#graals-opcode-table) |
| 11 | JMPIF_NP | 39 | SETCURVAR_ARRAY_CREATE | 67 | TAG_TO_STR | [file] (torque/scripting.md#graals-opcode-table) |
| 12 | JMP | 40 | LOADVAR_UINT | 68 | LOADIMMED_STR | [file] (torque/scripting.md#graals-opcode-table) |
| 13 | RETURN | 41 | LOADVAR_FLT | 69 | LOADIMMED_IDENT | [file] (torque/scripting.md#graals-opcode-table) |
| 14 | CMPEQ | 42 | LOADVAR_STR | 70 | CALLFUNC_RESOLVE | [file] (torque/scripting.md#graals-opcode-table) |
| 15 | CMPGR | 43 | SAVEVAR_UINT | 71 | CALLFUNC | [file] (torque/scripting.md#graals-opcode-table) |
| 16 | CMPGE | 44 | SAVEVAR_FLT | 72 | unused | [file] (torque/scripting.md#graals-opcode-table) |
| 17 | CMPLT | 45 | SAVEVAR_STR | 73 | ADVANCE_STR | [file] (torque/scripting.md#graals-opcode-table) |
| 18 | CMPLE | 46 | SETCUROBJECT | 74 | ADVANCE_STR_APPENDCHAR | [file] (torque/scripting.md#graals-opcode-table) |
| 19 | CMPNE | 47 | SETCUROBJECT_NEW | 75 | ADVANCE_STR_COMMA | [file] (torque/scripting.md#graals-opcode-table) |
| 20 | XOR | 48 | SETCURFIELD | 76 | ADVANCE_STR_NUL | [file] (torque/scripting.md#graals-opcode-table) |
| 21 | MOD | 49 | SETCURFIELD_ARRAY | 77 | REWIND_STR | [file] (torque/scripting.md#graals-opcode-table) |
| 22 | BITAND | 50 | LOADFIELD_UINT | 78 | TERMINATE_REWIND_STR | [file] (torque/scripting.md#graals-opcode-table) |
| 23 | BITOR | 51 | LOADFIELD_FLT | 79 | COMPARE_STR | [file] (torque/scripting.md#graals-opcode-table) |
| 24 | NOT | 52 | LOADFIELD_STR | 80 | PUSH | [file] (torque/scripting.md#graals-opcode-table) |
| 25 | NOTF | 53 | SAVEFIELD_UINT | 81 | PUSH_FRAME | [file] (torque/scripting.md#graals-opcode-table) |
| 26 | ONESCOMPLEMENT | 54 | SAVEFIELD_FLT | 82 | BREAK | [file] (torque/scripting.md#graals-opcode-table) |
| 27 | SHR | 55 | SAVEFIELD_STR | — | — | [file] (torque/scripting.md#graals-opcode-table) |

The rules below give the operands of the opcodes that take them [file] (torque/scripting.md#graals-opcode-table).

| Rule | Source |
| --- | --- |
| Operands: `FUNC_DECL` name, namespace, package, hasBody, end ip, argc, then argc arg idents; `CREATE_OBJECT` parent ident, isDatablock, fail ip; `ADD_OBJECT` and `END_OBJECT` one flag; jumps one target | [file] (torque/scripting.md#graals-opcode-table) |
| `SETCURVAR`, `SETCURVAR_CREATE`, `SETCURFIELD`, the `LOADIMMED_*` opcodes, `TAG_TO_STR` and `ADVANCE_STR_APPENDCHAR` take one operand; `CALLFUNC` and `CALLFUNC_RESOLVE` take name, namespace and call type (0 function, 1 method, 2 parent); the rest take none | [file] (torque/scripting.md#graals-opcode-table) |
| The operand shape is the same as stock TGE 1.x; opcodes 2, 3 and 72 never occur, so what they were is unknown | [file] (torque/scripting.md#graals-opcode-table) |
| The repo has a disassembler and a decompiler for this format under `torque/tools/` | [doc] (torque/scripting.md#the-decoder) |

### 10.4.4 What the 3.153 scripts do

The 3.153 scripts run the menus and settings. Each row gives one script area and what it does [file] (torque/scripting.md#what-the-3153-scripts-do).

| Script area | Behaviour | Source |
| --- | --- | --- |
| start-up | `main.cs` opens the console, runs `main2D.cs` and writes default prefs (fixed UDP port 14899, font size 22, OpenAL); `main2D.cs` loads the GUI and binds and shows the 2D main menu; the 2D game is the native control `Adventure` (`GuiGraalCtrl`) | [file] (torque/scripting.md#what-the-3153-scripts-do) |
| menus | call native `Adventure.*` methods (nickname, account, password, language, server list, offline mode, direct connect, connect, account fields); with `$serverstartconnect` set and an account filled in, the menu goes straight to the server list, which is how `-connect` and `graal://` links join | [file] (torque/scripting.md#what-the-3153-scripts-do) |
| 2D keys | arrows move, A/S/D act (Space = S), Q, P, M, T microphone, F5 load level, F7 player list, F8 server list; global F1 help, F2 console, F3 options, Alt+Enter full screen, Esc | [file] (torque/scripting.md#what-the-3153-scripts-do) |
| 3D keys | WASD and arrows move and also drive the Graal player; mouse look with sensitivity clamped to 0.05–2.0 and scaled by FOV/90; Space jump, left mouse fire, right mouse first person, E free look | [file] (torque/scripting.md#what-the-3153-scripts-do) |
| 3D start | `main3D.cs` maps nine terrain textures to detail textures and footstep sounds, loads the play, loading and download GUIs, sets net port 0, creates `GameConnection(ServerConnection)` and connects | [file] (torque/scripting.md#what-the-3153-scripts-do) |
| connection errors | every Torque reject code maps to a message box, including the Graal protocol-less and protocol-greater texts | [file] (torque/scripting.md#what-the-3153-scripts-do) |
| chat over Torque | stock `clientCmdChatMessage` / `clientCmdServerMessage`, ending in native `onChatMessage` / `onServerMessage` | [file] (torque/scripting.md#what-the-3153-scripts-do) |
| 3.04 | the key map equals 3.153's 2D map, named `moveMap`, with F3 bound in the map | [file] (torque/scripting.md#what-the-3153-scripts-do) |

## 10.5 Object model

### 10.5.1 Networked classes

Each build registers its own set of networked classes. The table gives each build's set [bin] (torque/wire-by-build.md#the-handshake-per-build).

| Build | Networked classes | Source |
| --- | --- | --- |
| 3.04 | stock TGE; no Graal net classes | [bin] (torque/wire-by-build.md#the-handshake-per-build) |
| 3.153 | the TGE game, datablock and Graal event classes of 4.04r2, without `AudioProfile` | [bin] (torque/wire-by-build.md#the-networked-class-sets) |
| 4.04r2 | 117 class registrations, 98 networked: 49 objects, 34 datablocks, 15 events | [bin] (torque/wire-by-build.md#the-networked-class-sets) |
| 4.20r6 objects | `Camera`, `DynamicGrass`, `DynamicGrassReplicator`, `DynamicShapeReplicator`, `GameObject`, `SimpleNetObject`, `Sky`, `Sun`, `TerrainBlock`, `WaterBlock`, `fxSunLight`, `twSurfaceReference` | [bin] (torque/wire-by-build.md#the-networked-class-sets) |
| 4.20r6 events | `BigDataChunkEvent`, `BigDataStartEvent`, `ConnectionMessageEvent`, `GhostAlwaysObjectEvent`, `NetStringEvent`, `RemoteCommandEvent`, `RequestReloadEvent` (C→S), `SimpleMessageEvent`, `TerrainChunkEvent`, `TerrainRequestUpdatesEvent` (C→S) | [bin] (torque/wire-by-build.md#the-networked-class-sets) |
| 5.12 | 10 objects (4.20r6's without `SimpleNetObject` and `twSurfaceReference`) and 9 events (without `SimpleMessageEvent`) | [bin] (torque/wire-by-build.md#the-networked-class-sets) |

4.04r2 networked classes, all stock TGE unless marked [bin] (graal3d/torque-engine-4x.md#ghosts-graal-changes):

| Group | Classes | Source |
| --- | --- | --- |
| shapes and players | `AIPlayer`, `Player`, `ShapeBase`, `StaticShape`, `Item`, `TSStatic`, `Shape3ds` (Graal), `Projectile`, `Debris`, `Splash` | [bin] (graal3d/torque-engine-4x.md#ghosts-graal-changes) |
| vehicles | `FlyingVehicle`, `HoverVehicle`, `WheeledVehicle`, `VehicleBlocker` | [bin] (graal3d/torque-engine-4x.md#ghosts-graal-changes) |
| cameras | `Camera`, `PathCamera`, `AdvancedCamera` | [bin] (graal3d/torque-engine-4x.md#ghosts-graal-changes) |
| world | `InteriorInstance`, `PathedInterior`, `TerrainBlock`, `WaterBlock`, `Sky`, `Sun`, `Precipitation`, `Lightning` | [bin] (graal3d/torque-engine-4x.md#ghosts-graal-changes) |
| mission and markers | `GameBase`, `Marker`, `MissionArea`, `MissionMarker`, `SpawnSphere`, `WayPoint`, `Trigger`, `PhysicalZone`, `ScopeAlwaysShape`, `SimpleNetObject` | [bin] (graal3d/torque-engine-4x.md#ghosts-graal-changes) |
| effects | `AudioEmitter`, `ParticleEmitterNode`, `FractalTree`, `fxFoliageReplicator`, `fxGrassReplicator`, `fxShapeReplicator`, `fxShapeReplicatedStatic`, `fxLight`, `fxSunLight`, `volumeLight`, `twSurfaceReference` | [bin] (graal3d/torque-engine-4x.md#ghosts-graal-changes) |
| Graal replicators | `DynamicGrass`, `DynamicGrassReplicator`, `DynamicShapeReplicator` | [bin] (graal3d/torque-engine-4x.md#ghosts-graal-changes) |
| datablocks | the stock `…Data` classes for shapes, images, items, players, cameras, vehicles, projectiles, effects, particles, audio, markers, interiors and triggers | [bin] (graal3d/torque-engine-4x.md#ghosts-graal-changes) |

The rules below give details of those classes in 4.04r2 that a string search would miss [bin] (torque/wire-by-build.md#the-networked-class-sets).

| Rule | Source |
| --- | --- |
| In 4.04r2 `Item`, `Sky`, `Sun` and `Path` register by string address, so a plain string search misses them | [bin] (torque/wire-by-build.md#the-networked-class-sets) |
| In 4.04r2 `ShapeBase` carries a Graal `chat` string drawn above the head, with emoticon handling; how the client's own chat reaches the 3D server was not found and probably goes over TCP | [bin][inf] (graal3d/torque-engine-4x.md#ghosts-graal-changes) |
| Every other class registers with group mask 0 (not networked); the `GameShape*` classes ride inside a `GameObject` update | [bin] (torque/wire-by-build.md#the-networked-class-sets) |

### 10.5.2 The 5.12 `GameObject` model

All classes are script-visible through GS2 property and method tables [bin] (torque/engine-and-formats.md#the-512-3d-object-model).

| Class | What it is | Notable members | Source |
| --- | --- | --- | --- |
| `GameObject` | every 3D thing, a ghosted `SceneObject` | mounting, node position and transform, interior checks, drop height, box collision, the controlling client, show-images on 3D objects, `onMount`, `onUnmount`, `onAdd`, `onRemove`; script variables and attributes synced to clients | [bin] (torque/engine-and-formats.md#the-512-3d-object-model) |
| `GameShapeDTS` | Torque DTS model | `playAnimation(slot, name, flags)` with flags 1 hold, 2 at end, 4 attack; `playAnimation2` with start, end, time scale and transition; pause, stop, node and material lists, `onEndAnimation` | [bin] (torque/engine-and-formats.md#the-512-3d-object-model) |
| `GameShapeDIF` | Torque interior | `activateLight`, `deactivateLight` | [bin] (torque/engine-and-formats.md#the-512-3d-object-model) |
| `GameShape3DS` | 3D Studio model | collision hulls are meshes named `Col-…`, closed and convex | [bin] (torque/engine-and-formats.md#the-512-3d-object-model) |
| `GameShapeFT` | 3D text from a TrueType font | | [bin] (torque/engine-and-formats.md#the-512-3d-object-model) |
| `GameShape` | base class | pixel and vertex shaders (GLSL), fractal-tree fields | [bin] (torque/engine-and-formats.md#the-512-3d-object-model) |
| `GameMovementInterpolate`, `…List`, `…Rigid` | how an object moves | `move3d`, `finishMoves`, `addRigidMove`, `applyImpulse`, mass, `onImpact`, `onCollision`, `onEnterLiquid`, `onLeaveLiquid` | [bin] (torque/engine-and-formats.md#the-512-3d-object-model) |
| `Camera` | the view | modes `free` and `lookat`, follow an attached object, look position and vector, Euler rotation | [bin] (torque/engine-and-formats.md#the-512-3d-object-model) |
| `DynamicGrass`, `DynamicGrassReplicator`, `DynamicShapeReplicator` | ground cover | terrain alignment, slope limits, allowed surfaces, per-grid counts | [bin] (torque/engine-and-formats.md#the-512-3d-object-model) |
| `Sky`, `Sun`, `WaterBlock`, `fxSunLight`, `TerrainBlock` | stock Torque | three cloud layers, fog volumes, fog storms with server-synchronised time | [bin] (torque/engine-and-formats.md#the-512-3d-object-model) |

5.12 adds a `GameObject` class that bridges 3D and 2D Graal. The rules below give its model and its GS2 properties [bin] (torque/engine-and-formats.md#the-512-3d-object-model).

| Rule | Source |
| --- | --- |
| The 2D Graal player is still the player; 3D objects can carry ganis and show-images | [bin] (torque/engine-and-formats.md#the-512-3d-object-model) |
| The GS2 properties on `GameObject` are `alpha`, `attachedtoobject`, `attr`, `attrobjects`, `chat`, `collision`, `iseditorobject`, `liquidheight`, `liquidtype`, `movetype`, `nickcolor`, `nickname`, `scaledshapebox`, `shadow`, `shape`, `shapebox`, `showterrain`, `skin`, `solid`, `velocity`, `watercoverage` | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |

`GameObject` update, 5.12: thirteen flag-guarded sections; the mask bits are the server's dirty bits, and on the wire each section is one flag [bin] (torque/wire-by-build.md#the-512-gameobject-update).

| # | Dirty bits | Payload after the flag | Source |
| ---: | --- | --- | --- |
| 1 | `0x1` | string, the object's name | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 2 | `0x2` or `0x200` | 3 × F32, the shape's scale about its origin (live 5.12; earlier read as velocity) | [bin][lab] (torque/wire-by-build.md#the-512-gameobject-update) |
| 3 | `0x8` | string, a setting of the movement object | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 4 | `0x10` | string, also passed to the movement object | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 5 | `0x20` | transform: position 3 × F32, then rotation as axis 3 × F32 and angle in radians F32 (Torque's axis-angle write); no scale | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 6 | `0x80` | string that creates or replaces the shape object (`shape`, inferred) | [bin][inf] (torque/wire-by-build.md#the-512-gameobject-update) |
| 7 | `0x40`, with a shape object | the shape object's own data | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 8 | any of `0xF00`, with a movement object | int14 bit length, then the movement object's data | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 9 | `0x1000` | string, the chat text (with emoticons) | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 10 | always 0 from this DLL | the reader takes a string and loads it as a script or image; what a real server sent is unknown | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 11 | any of `0x3FC000` | the attribute list | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 12 | `0x400000` | string, then 4 colour bytes RGBA 0–255 (nickname and `nickcolor`, inferred) | [bin][inf] (torque/wire-by-build.md#the-512-gameobject-update) |
| 13 | `0x800000` | int16 of booleans; bits `0x01`, `0x04`, `0x08`, `0x10`, `0x20`, `0x40` are used | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |

The rules below give what a live 5.12 did with single `GameObject` fields sent one at a time [lab][cap] (torque/live-512-gameobject-fields-2026-11-25.md).

| Rule | Source |
| --- | --- |
| Section 2 scales the shape about its origin: (2, 2, 2) doubles it, (1, 1, 3) makes it three times taller, 0.5 halves it; (0, 0, 0) draws it at normal size, so that value means unset | [lab][cap] (torque/live-512-gameobject-fields-2026-11-25.md#section-2-is-scale-not-velocity) |
| Rotations about x, y and z all apply | [lab][cap] (torque/live-512-gameobject-fields-2026-11-25.md#rotation-and-visibility-flags) |
| Of the section-13 flags only `0x0004` hides the object; `0x01`, `0x02`, `0x08`, `0x10`, `0x40`, `0x80` and `0x100` each drew a pixel-identical frame; `0x20` is being rerun | [lab][cap] (torque/live-512-gameobject-fields-2026-11-25.md#rotation-and-visibility-flags) |
| On a static scenery `GameObject`, skin (with or without `.png`), chat, `attr1` to `attr3` and nickname with colour are accepted but show nothing: no pixels, no file request, no name tag and no chat bubble; a skin is never requested for a `.3ds` shape | [lab][cap] (torque/live-512-gameobject-fields-2026-11-25.md#fields-accepted-but-not-drawn-on-a-static-gameobject); [lab] (torque/live-512-gameobject-fields-2026-11-25.md#sky-bottom-face-and-ft) |

### 10.5.3 Graal events over Torque

Graal sends its own events over the Torque connection. Each row gives an event, its direction and its layout [bin] (graal3d/torque-engine-4x.md#graal-events-and-text-big-data-channel).

| Event | Direction | Layout | Source |
| --- | --- | --- | --- |
| `BigDataStartEvent` | both | int16 transfer id, three strings (`s1`, `s2`, `s3`, each up to 255 characters), int24 total length, int3 coding (0 none, 1 zlib, 2 bzip2) | [bin] (graal3d/torque-engine-4x.md#graal-events-and-text-big-data-channel) |
| `BigDataChunkEvent` | both | int16 transfer id, int8 length (up to 191), the bytes | [bin] (graal3d/torque-engine-4x.md#graal-events-and-text-big-data-channel) |
| `TerrainChunkEvent` | S→C | int4 chunk x, int4 chunk y, raw 32 stamp (ignored by the receiver), int10 length, then a zlib 16 × 16 piece of heights, materials and holes; 16 × 16 chunks make a 256 × 256 terrain (→ §10.5.4) | [bin] (torque/terrain-512.md#2-terrainchunkevent-server--client) |
| `TerrainRequestUpdatesEvent` | C→S | 256 raw 32-bit stamps, index y × 16 + x, telling the server what the client already has; 0 means no data (→ §10.5.4) | [bin] (torque/terrain-512.md#3-terrainrequestupdatesevent-client--server) |
| `RequestReloadEvent` | C→S | asks the server to resend an object | [bin] (graal3d/torque-engine-4x.md#events) |
| `SimDataBlockEvent` (4.04r2) | S→C | int12 (id − 3), int12 class id, int12 index, int13 total, sized datablock data | [bin] (graal3d/torque-engine-4x.md#events) |
| `RemoteCommandEvent` | both | int5 argc, tagged-string arguments; the 4.04r2 client acts only on the mission phases | [bin] (graal3d/torque-engine-4x.md#events) |
| others | — | `GhostAlwaysObjectEvent`, `NetStringEvent`, `ConnectionMessageEvent`, `PathManagerEvent`, `SimpleMessageEvent`, the audio and lightning events, stock TGE | [bin] (graal3d/torque-engine-4x.md#events) |

The rules below give how a BigData message is shaped and how the sender compresses and splits it [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll).

| Rule | Source |
| --- | --- |
| A BigData message has the shape of GS2 `sendtext`: weapon, type, option, data | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |
| The sender uses zlib from 50 bytes and bzip2 from 4096 bytes, and sends the start event then up to 16 chunks per call; the TCP framing uses nearly the same limits (48 and 4096, → §2.2) | [bin] (graal3d/torque-engine-4x.md#graal-events-and-text-big-data-channel); [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |
| S→C with `s1` set: the weapon of that name gets `onReceiveText(s2, s3, params)` | [bin] (graal3d/torque-engine-4x.md#graal-events-and-text-big-data-channel) |
| S→C with `s1` empty, `s2` is a command: `set` / `unset` a player flag; `events` (lines `s <flag>`, or `t <target>,<kind>,<action>,<params>` on a weapon, GUI or NPC; kind `rc` goes to `onRCChat` and `torque` is ignored); `addweapon` (with a 5-byte Graal integer, a time stamp inferred); `weaponscript`; `deleteweapon`; `addnpc` (a script for a named client-side object); `setmaterials` (terrain materials); `rpg` (→ `onRPGMessage`) | [bin][inf] (graal3d/torque-engine-4x.md#graal-events-and-text-big-data-channel) |
| In 3D mode the 3D server, not the TCP gserver, delivers the client's GS2 weapons and flags | [bin][inf] (graal3d/torque-engine-4x.md#graal-events-and-text-big-data-channel) |
| C→S the engine batches its game events as one message with `s2 = "events"`: `w <weapon>` from getweapon, `s <name>=<value>` from client-variable and flag sets, `t weapon,<name>,<params>` from a server-side trigger | [bin] (graal3d/torque-engine-4x.md#graal-events-and-text-big-data-channel) |
| The 4.04r2 DLL's server-side BigData handler is empty | [bin] (graal3d/torque-engine-4x.md#graal-events-and-text-big-data-channel) |
| The 5.12 client streams terrain from the server instead of reading `.ter` files ("Loading terrain from terrain chunks."); terrain textures must be 256×256 at 24 bits | [bin] (torque/engine-and-formats.md#3d-resource-formats) |
| The 4.04r2 client caches terrain under `levels3d/terrain/` and never requests `.ter` over TCP | [bin][inf] (graal3d/torque-engine-4x.md#terrain-streaming-graal) |

### 10.5.4 Streamed terrain (5.12)

Graal's terrain is a 256 × 256 grid of squares, but 5.12 never reads it from a `.ter` file. The server ghosts a `TerrainBlock` that carries only settings, then streams heights, materials and holes as 256 chunks of 16 × 16 squares; the client caches every chunk per server and tells the server which chunks it already has [bin] (torque/terrain-512.md#graal-512-streamed-terrain-terrainblock-chunk-events-and-the-heights-cache). What a script can do with the terrain is in → §8.5.8. All fields are Torque bit-stream fields; "raw" values are copied through the stream's byte write at the current bit position [bin] (torque/terrain-512.md#graal-512-streamed-terrain-terrainblock-chunk-events-and-the-heights-cache).

`TerrainBlock` update, 5.12: one guarded block. Each row gives a field in wire order [bin] (torque/terrain-512.md#1-the-terrainblock-ghost).

| # | Field | Width | Client use | Source |
| ---: | --- | --- | --- | --- |
| 1 | init | flag | 0: nothing more follows; a create with init 0 is still added and still loads and streams terrain, with no name and a zero square size | [bin][lab] (torque/terrain-512.md#1-the-terrainblock-ghost) |
| 2 | object name | `pstring` | the object's name (use `Terrain`) | [bin] (torque/terrain-512.md#1-the-terrainblock-ghost) |
| 3 | value | raw 32 | stored, then reset to 1 when the block is added | [bin] (torque/terrain-512.md#1-the-terrainblock-ghost) |
| 4, 5 | text | `pstring` each | read and dropped (the stock writer sends empty strings) | [bin] (torque/terrain-512.md#1-the-terrainblock-ghost) |
| 6, 7, 8 | values | raw 32 each | dropped (the stock writer sends 1.0, 0.01 and the integer 8) | [bin] (torque/terrain-512.md#1-the-terrainblock-ghost) |
| 9 | square size | raw 32, integer | metres per square; use 8 | [bin] (torque/terrain-512.md#1-the-terrainblock-ghost) |
| 10 | repeat | raw 8 | non-zero: the terrain tiles beyond its edges | [bin] (torque/terrain-512.md#1-the-terrainblock-ghost) |

When the block is first added, the client does the steps below in order [bin] (torque/terrain-512.md#1-the-terrainblock-ghost).

| Step | What the client does | Source |
| ---: | --- | --- |
| 1 | becomes the current terrain if there is none (a later block named `Terrain` replaces it) | [bin] (torque/terrain-512.md#1-the-terrainblock-ghost) |
| 2 | places the corner at (−128 × square size, −128 × square size, 0), so the grid is centred on the origin; chunk (0, 0) is the −x, −y corner and chunk rows grow toward +y | [bin][lab] (torque/terrain-512.md#1-the-terrainblock-ghost) |
| 3 | logs "Loading terrain from terrain chunks." | [bin] (torque/terrain-512.md#1-the-terrainblock-ghost) |
| 4 | loads the material list from `heights.info` in the cache folder, or asks for it with the normal Graal file request over TCP; an empty answer leaves the list as it was | [bin] (torque/terrain-512.md#1-the-terrainblock-ghost) |
| 5 | loads each cached chunk file that exists | [bin] (torque/terrain-512.md#1-the-terrainblock-ghost) |
| 6 | sends one `TerrainRequestUpdatesEvent` with the stamp of every chunk | [bin] (torque/terrain-512.md#1-the-terrainblock-ghost) |

Chunk data, after inflating the zlib stream (RFC 1950, with its 2-byte header) of a `TerrainChunkEvent`. Each row gives a field in order [bin] (torque/terrain-512.md#chunk-data-inflated).

| Field | Width | Meaning | Source |
| --- | --- | --- | --- |
| mode | int8 | 2: hole flags follow at the end; 1: clear all holes in the chunk; 0: leave holes; any other value behaves like 0 for holes | [bin][lab] (torque/terrain-512.md#chunk-data-inflated); [lab] (torque/terrain-512.md#edge-cases-seen-live) |
| h0 | int16 | height of square (0, 0) of the chunk | [bin] (torque/terrain-512.md#chunk-data-inflated) |
| deltas | 256 raw bytes | signed deltas `d[y][x]`, rows then columns | [bin] (torque/terrain-512.md#chunk-data-inflated) |
| N | int6 | number of materials used in the chunk (only ids 0–31 make sense) | [bin] (torque/terrain-512.md#chunk-data-inflated) |
| ids | N × int5 | material ids, indices into the `heights.info` list | [bin] (torque/terrain-512.md#chunk-data-inflated) |
| squares | if N > 1, per square, rows then columns | flag blend; intW primary index; if blend, intW secondary index and int4 `a`; W is the bit count for N choices (N rounded up to a power of two, then its base-2 logarithm); with N of 0 or 1 every square takes the first id | [bin] (torque/terrain-512.md#chunk-data-inflated) |
| holes | if mode 2, 256 flags | rows then columns; 1 = hole (bit 3 of the square's flag byte, as in stock TGE) | [bin][inf] (torque/terrain-512.md#chunk-data-inflated) |

The rules below give how heights, materials and stamps are decoded and computed [bin][lab] (torque/terrain-512.md#chunk-data-inflated).

| Rule | Source |
| --- | --- |
| Decoding, 16-bit for heights and 8-bit signed for deltas, `/2` truncating toward zero: `h[0][0] = h0`; row 0 `h[0][x] = h[0][x−1] + d[0][x]`; column 0 `h[y][0] = h[y−1][0] + d[y][0]`; elsewhere `d[y][x] += (d[y−1][x] + d[y][x−1]) / 2` over already-decoded neighbours, then `h[y][x] = (h[y−1][x] + h[y][x−1]) / 2 + d[y][x]` | [bin] (torque/terrain-512.md#chunk-data-inflated) |
| The writer clamps first-pass deltas to −127…127 against the same predictors, then replaces each with itself minus the mean of its upper and left first-pass deltas, clamped again; large steps are lossy | [bin] (torque/terrain-512.md#chunk-data-inflated) |
| The client stores each decoded height shifted up 2 bits; one world unit is 8 wire units (a flat chunk at 3200 reports `getdropz` 400), so only 14 bits of `h0` survive and heights are not clamped | [bin][lab] (torque/terrain-512.md#chunk-data-inflated); [lab] (torque/terrain-512.md#edge-cases-seen-live) |
| Materials: the primary's alpha becomes `a` × 16 and the secondary's 255 − `a` × 16, every other material's 0; without blend the primary's alpha is 255; the writer takes the largest-alpha material as primary and sends its alpha divided by 16 | [bin] (torque/terrain-512.md#chunk-data-inflated) |
| On receipt with length > 0 and a current terrain, the client inflates, applies, re-encodes with its own writer, stores the new stamp, writes the cache file and rebuilds that area; length 0 is ignored; a chunk before the `TerrainBlock` is added is logged but not stored | [bin][lab] (torque/terrain-512.md#2-terrainchunkevent-server--client) |
| A corrupt or truncated zlib stream is applied as zeros and cached that way; a short plain stream reads the missing fields as zero; trailing bytes are ignored; the same chunk twice: the second wins; no chunk case crashed 5.12 | [lab] (torque/terrain-512.md#2-terrainchunkevent-server--client); [lab] (torque/terrain-512.md#edge-cases-seen-live) |
| Canonical re-encoding: mode always 2, the material list holds only the ids used, sorted ascending (per-square indices remapped), and a blend is stored with the larger-alpha material as primary; the file is that stream at zlib's default level | [bin][lab] (torque/terrain-512.md#3-terrainrequestupdatesevent-client--server) |
| Stamp = the standard CRC-32 table (polynomial 0xEDB88320), start 0xFFFFFFFF, no final inversion, over the client's re-encoded bytes, not the bytes sent; in zlib terms `crc32(data) XOR 0xFFFFFFFF`; the stamp in the event is ignored | [bin][lab] (torque/terrain-512.md#3-terrainrequestupdatesevent-client--server); [lab] (torque/terrain-512.md#edge-cases-seen-live) |
| A server answers the request with a `TerrainChunkEvent` for every chunk whose stamp differs from its own; a real 5.12 matched all 256 stamps on reconnect against a generated world, so none were resent | [bin][lab] (torque/terrain-512.md#3-terrainrequestupdatesevent-client--server); [lab] (torque/terrain-512.md#lab-results) |
| Cache folder: the user folder, then `levels3d/heights/<server>/`, a space in the server name written `%032`; `heights.info` holds up to 32 texture names, one per line (a comma does not separate names); `heights<x>-<y>.dat` holds one re-encoded chunk, x and y in unpadded decimal | [bin][lab] (torque/terrain-512.md#4-the-cache-folder) |
| Cached chunks go through the same decoder as received ones, so a server or a lab can pre-seed a client by shipping these files | [bin][lab] (torque/terrain-512.md#4-the-cache-folder); [lab] (torque/terrain-512.md#lab-results) |
| Terrain textures are requested by name and cached as `levels3d/images/<name>`; they must be 256 × 256 at 24 bits, else "Terrain texture of bad format (must be 256x256x24)" and `default`; a missing one logs "Missing terrain texture" | [bin][lab] (torque/terrain-512.md#4-the-cache-folder) |
| Texture fetching is one visit late: the first visit fetches only `heights.info`; the second logs "Missing terrain texture" per name, then downloads each and saves it under exactly the listed name; list names with their extension, since extensionless cached textures failed to load on later visits in another lab | [lab] (torque/terrain-512.md#4-the-cache-folder) |
| A later 5.12 run drew the terrain white with names given bare and with `.png`, and never requested the textures; why it differs from the one-visit-late run is open | [lab] (torque/live-512-gs2-3d-probe-2026-11-25.md#terrain-textures-t3d-044-follow-up) |
| 3.153 streams too: a ghosted `TerrainBlock` makes it send `TerrainRequestUpdatesEvent` and ask for `heights.info` | [lab] (torque/live-3153-and-404r2-sessions-2026-11-25.md#3153) |
| The BigData `setmaterials` message sets the list with comma-separated names (it is not split at newlines) and the client persists it as a 32-line CRLF `heights.info` in the cache folder | [lab] (torque/terrain-512.md#4-the-cache-folder) |
| 4.04r2 and 3.153 keep stock Torque's `.ter` path: a block whose `terrainFile` names a `.ter` that loads logs "Loaded terrain from terrain file." and asks for no chunks; the network update never sets `terrainFile`, so a ghosted block always streams; 5.12 only streams | [bin][inf] (torque/terrain-512.md#8-older-builds-the-ter-file-path) |
| 4.20r8 logs the chunk line, requests chunks and saves the first ones as 5.12 does; it crashed in runs with `GameObject`s at ground level and a low spawn, and ran 110 s with no objects and a high spawn; a `WaterBlock` alone is fine; collision versus shadow is not yet separated | [lab] (torque/terrain-512.md#lab-results) |

### 10.5.5 `WaterBlock` update (5.12)

Unlike `TerrainBlock`, only the name is guarded and every update carries the whole block. Field names come from the class's own property names in the order the stock TGE 1.x writer used; the meaning of each float is stock Torque's [bin][inf] (torque/terrain-512.md#5-waterblock-read-beside-the-terrain).

| # | Field | Width | Source |
| ---: | --- | --- | --- |
| 1 | name follows | flag, then `pstring` object name | [bin] (torque/terrain-512.md#5-waterblock-read-beside-the-terrain) |
| 2 | transform | position 3 × `f32`, then a quaternion as x, y, z 3 × `f32` and a flag "w is negative" (w = √(1 − x² − y² − z²)); Torque's compact matrix read, not the `GameObject` axis-angle | [bin] (torque/terrain-512.md#5-waterblock-read-beside-the-terrain) |
| 3 | scale | 3 × `f32`, the water's extent in metres; taken only when x and y are both at least 1024 (512 drew nothing live) | [bin][lab] (torque/terrain-512.md#5-waterblock-read-beside-the-terrain); [lab] (torque/terrain-512.md#lab-results) |
| 4 | textures | 5 × `pstring`: surface, specular mask, environment map over, environment map under, shore | [bin] (torque/terrain-512.md#5-waterblock-read-beside-the-terrain) |
| 5 | submerge textures | 2 × `pstring` | [bin] (torque/terrain-512.md#5-waterblock-read-beside-the-terrain) |
| 6 | liquid type | raw 32 integer; 0 to 7 all accepted live (stock names: water, ocean, river, stagnant, lava, hot lava, crusty lava, quicksand) | [bin][inf] (torque/terrain-512.md#5-waterblock-read-beside-the-terrain); [lab] (torque/terrain-512.md#lab-results) |
| 7 | physics and look | 5 × raw 32 floats: density, viscosity, wave magnitude, surface opacity, environment-map intensity | [bin] (torque/terrain-512.md#5-waterblock-read-beside-the-terrain) |
| 8 | switches | 2 × raw 8: remove wet edges, use depth mask | [bin] (torque/terrain-512.md#5-waterblock-read-beside-the-terrain) |
| 9 | shading | 12 × raw 32 floats: surface and shore tessellation, surface parallax, flow angle, flow rate, distortion grid scale, magnitude and time, shore depth, minimum and maximum alpha, depth gradient | [bin] (torque/terrain-512.md#5-waterblock-read-beside-the-terrain) |
| 10 | specular colour | 4 × `int8` RGBA, divided by 255 | [bin] (torque/terrain-512.md#5-waterblock-read-beside-the-terrain) |
| 11 | specular power | raw 32 float | [bin] (torque/terrain-512.md#5-waterblock-read-beside-the-terrain) |
| 12 | ignore terrain | raw 8 | [bin] (torque/terrain-512.md#5-waterblock-read-beside-the-terrain) |

Live on 5.12 the surface texture was fetched over TCP and a large surface drawn [lab] (torque/terrain-512.md#lab-results).

### 10.5.6 Lighting, sky and view (5.12, live)

These runs used the real 5.12 on a GLSL-capable driver (Mesa llvmpipe) with a lighting probe and a sky grid [lab][cap] (torque/live-512-lighting-and-sky-2026-11-25.md).

| Rule | Source |
| --- | --- |
| On a `.3ds` shape the `Sun`'s direction, colour and ambient have no effect: with a `Sun` each face draws at material × texture, times 1.0 for faces whose world-space normal points −y, −x or up and 0.85 for +x or +y; with no `Sun` every face is exactly one quarter and the background 0. So the `Sun` is an on/off switch for full brightness, and the shading comes from a fixed built-in light | [lab][cap] (torque/live-512-lighting-and-sky-2026-11-25.md#lighting-on-3ds-shapes-t3d-047-t3d-052) |
| The `Sun` shades nothing on a `.dts`, a `.dif` or streamed terrain either; with no `Sun` the `.dts` is not drawn or black, the `.dif` is entirely black, and terrain is unchanged | [lab][cap] (torque/live-512-lighting-and-sky-2026-11-25.md#lighting-on-3ds-shapes-t3d-047-t3d-052) |
| A positive rotation about +z turns a shape clockwise seen from above (at +90 degrees the +x face looks toward −y), the same sense as the camera | [lab] (torque/live-512-lighting-and-sky-2026-11-25.md#shape-rotation) |
| Sky texture entries: 2 is ahead (+y), 1 right, 0 behind, 3 left, 4 up; side faces are upright and mirrored left to right; entry 5 (bottom) is not drawn with the default options, and draws as a floor below the horizon with sky flags `1 1 1`; one face spans the full screen width | [lab] (torque/live-512-lighting-and-sky-2026-11-25.md#sky-geometry-and-field-of-view-t3d-046-t3d-055); [lab][cap] (torque/live-512-own-server-textures-2026-11-25.md#sky-t3d-046-partial); [lab] (torque/live-512-gameobject-fields-2026-11-25.md#sky-bottom-face-and-ft) |
| The default horizontal field of view is 90 degrees (measured 89.4) | [lab] (torque/live-512-lighting-and-sky-2026-11-25.md#sky-geometry-and-field-of-view-t3d-046-t3d-055) |
| Below the horizon the sky shows the fog colour on Mesa; on a GDI OpenGL 1.1 driver it was black with a fog-coloured band | [lab] (torque/live-512-lighting-and-sky-2026-11-25.md#sky-geometry-and-field-of-view-t3d-046-t3d-055); [lab][cap] (torque/live-512-own-server-textures-2026-11-25.md#sky-t3d-046-partial) |
| The sky's visible-distance field did not clip or fog anything on the client in the runs so far | [lab][cap] (torque/live-512-own-server-textures-2026-11-25.md#sky-t3d-046-partial) |

## 10.6 3D formats

The Torque clients read Torque's 3D formats. Each row gives an extension, its format and the builds that read it [bin] (torque/engine-and-formats.md#3d-resource-formats).

| Ext | Format | Builds | Source |
| --- | --- | --- | --- |
| `.dts`, `.dsq` | Torque shape and sequence; 4.04r2 reads up to version 24; 5.12 rejects shapes that are too old | 3.x, 4.04r2, 5.12 | [bin] (torque/engine-and-formats.md#3d-resource-formats); [bin] (graal3d/torque-engine-4x.md#files) |
| `.dif` | Torque interior; 4.04r2 reads resource version 44, interior version 0 | all | [bin] (graal3d/torque-engine-4x.md#files) |
| `.ter` | Torque terrain, version 3 or older, from `levels3d/terrain/` | 3.x, 4.04r2 | [bin] (graal3d/torque-engine-4x.md#files) |
| terrain chunks | streamed with `TerrainChunkEvent` (→ §10.5.4) | 5.12 | [bin] (torque/engine-and-formats.md#3d-resource-formats) |
| `.3ds` | 3D Studio (`Shape3ds`, then `GameShape3DS`) | 3.153, 4.04r2, 5.12 | [bin] (torque/engine-and-formats.md#3d-resource-formats) |
| `.md3` | Quake 3 model in head, upper and lower parts, version 15 | 3.153, 4.04r2 | [bin] (torque/engine-and-formats.md#3d-resource-formats); [bin] (graal3d/torque-engine-4x.md#files) |
| `.mis` | Torque mission file; 5.12 has no `.mis` loader and builds its `MissionGroup` from ghosts (inferred) | 3.x; 4.04r2 not: no `.mis` is opened in a lab session (settled below) | [bin][inf] (torque/engine-and-formats.md#3d-resource-formats); [bin][inf] (graal3d/torque-engine-4x.md#files) |
| `.ml`, `.ifl`, `.dml` | material lists and image-file lists for animated textures | stock Torque | [bin] (torque/engine-and-formats.md#3d-resource-formats); [bin] (graal3d/torque-engine-4x.md#files) |
| `.gft` | Torque cached GUI font | 3.x, 4.04r2, 5.12 | [bin] (torque/engine-and-formats.md#3d-resource-formats); [bin] (graal3d/torque-engine-4x.md#files) |
| `.dso` | compiled TorqueScript (→ §10.4) | 3.x; 4.04r2 not: no `.cs` or `.dso` is opened in a lab session (settled below) | [file] (torque/scripting.md#torquescript-in-graal-3x-the-dso-format-and-the-shipped-scripts); [bin] (graal3d/torque-engine-4x.md#files); [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#mis-and-dso-in-the-404r2-3d-plug-in-e502-e503) |
| images | `.png`, `.jpg`, `.jp2`, `.jng`, `.mng`, `.gif`, `.bmp`, `.bm8`, `.tga`, `.dds` | 4.04r2 | [bin] (graal3d/torque-engine-4x.md#files) |
| `.zip`, `.gpake` | archives the resource manager opens | 4.04r2 | [bin] (graal3d/torque-engine-4x.md#files) |

**Settled question, formerly E#503: Whether 4.04r2 reads `.dso` compiled TorqueScript.** Whether 4.04r2 still reads compiled TorqueScript was open. The same 3D session with `.cs` and `.dso` markers beside the client settled it [lab] (protocol/lab-appe-hostb-2026-11-20c.md#mis-and-dso-beside-the-404r2-client-e502-e503).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | `main.cs`, `main.cs.dso` and mission `.dso` files in the client folder and under `levels3d` were listed by the folder scan but never opened, with no console output | [lab] (protocol/lab-appe-hostb-2026-11-20c.md#mis-and-dso-beside-the-404r2-client-e502-e503) |
| Verdict | Verified for a normal 3D session: 4.04r2 opens no `.cs` or `.dso` beside it, as the read predicted | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#mis-and-dso-in-the-404r2-3d-plug-in-e502-e503) |
| Left over | A compiled-code reader linked in but never called can't be ruled out from the stripped image or a run | [inf] (protocol/lab-appe-hostb-2026-11-20c.md#mis-and-dso-beside-the-404r2-client-e502-e503) |

**Settled question, formerly E#502: Whether 4.04r2 loads `.mis` mission files.** Whether 4.04r2 can load a local `.mis` as well as receiving its mission over the network was open. A 3D session with marker missions beside the client settled it [lab] (protocol/lab-appe-hostb-2026-11-20c.md#mis-and-dso-beside-the-404r2-client-e502-e503).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | Marker `.mis` files in the client folder and under `levels3d` were listed by the client's folder scan but never opened, and no marker reached the console; the mission was built from the network | [lab] (protocol/lab-appe-hostb-2026-11-20c.md#mis-and-dso-beside-the-404r2-client-e502-e503) |
| Verdict | Verified for a normal 3D session, and it agrees with the read (no `exec` or `compile` command, no `.mis` literal) | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#mis-and-dso-in-the-404r2-3d-plug-in-e502-e503) |
| Left over | A file reader linked in but never called can't be ruled out by a run | [inf] (protocol/lab-appe-hostb-2026-11-20c.md#mis-and-dso-beside-the-404r2-client-e502-e503) |

The rules below give how a live 5.12 handled shape content, one change per run [lab][cap] (torque/live-512-shapes-2026-11-25.md).

| Rule | Source |
| --- | --- |
| `.3ds`: a mesh with no material is not drawn; a colour-only material draws its diffuse colour; a material naming a missing texture draws white | [lab][cap] (torque/live-512-shapes-2026-11-25.md#3ds-materials-and-meshes-t3d-032) |
| `.3ds`: `Col-` collision meshes are drawn; there is no back-face culling (both windings draw, the two-sided flag changes nothing); material transparency is ignored | [lab][cap] (torque/live-512-shapes-2026-11-25.md#3ds-materials-and-meshes-t3d-032) |
| `.3ds`: 400 objects in one file, and one mesh at the u16 cap (32,761 vertices, 64,800 faces), both drew | [lab][cap] (torque/live-512-shapes-2026-11-25.md#3ds-materials-and-meshes-t3d-032) |
| `.dts` version word on a v24 body: 16 rejected ("not supported anymore", play continues); 17 and 18 hang on a black view; 19 and 22 crash; 23 loads and draws nothing; 24 draws; 25 rejected ("only version 24 and before"). So the header accepts 17 to 24 and the reader trusts the version word without checking the body; genuine old-version shapes were not tested | [lab][cap] (torque/live-512-shapes-2026-11-25.md#dts-versions-t3d-029) |
| Stock v24 `.dts` shapes (with sequences) and a v44 `.dif` draw; the client also asks for `lightfalloffmono` | [lab][cap] (torque/live-512-shapes-2026-11-25.md#dts--dif-that-do-draw) |
| A `.ft` text-shape `GameObject` never drew (flags 0, `0x08`, `0x18`; levels 1, 2, 6; malformed), though the file and its texture downloaded and nothing was logged | [lab][cap] (torque/live-512-shapes-2026-11-25.md#ft-text-shapes-t3d-036) |
| 4.20r8 matched 5.12 on these fuzz rows, including the crash on a huge `TerrainBlock` square size | [lab] (torque/live-512-shapes-2026-11-25.md#420r8) |

The rules below give how a Linux 4.20r6 client (3D-equal to Windows 4.20r8) names, fetches and applies a `GameObject` shape's textures, with one textured `.3ds` cube and only the material's texture name varied (T3D-090) [lab] (torque/3d-shape-textures-420r6-2026-11-25.md#results-lab).

| Rule | Source |
| --- | --- |
| The client strips the texture name to its leaf (`sub/subtex` → `subtex`) and drops `.png`, asks for the bare name once, and does not ask again after a failure (`PLO_FILESENDFAILED`, 30) | [lab] (torque/3d-shape-textures-420r6-2026-11-25.md#naming-rules-lab) |
| A download is saved under the user folder's `levels3d/images/` exactly as requested, so without an extension; the part of a name before the first `_` becomes a subfolder (`sky_fr` → `images/sky/sky_fr`); shapes keep `.3ds` | [lab] (torque/3d-shape-textures-420r6-2026-11-25.md#naming-rules-lab) |
| The shape always draws; a missing or unapplied texture leaves it white | [lab] (torque/3d-shape-textures-420r6-2026-11-25.md#does-the-shape-draw-and-does-the-texture-apply) |
| A texture downloaded during the session is not applied, because the material loader looks for `<name>.png` and the download has no extension; the same material drew textured when `labtex.png` was already on disk. So the texture must be on disk as `<name>.png` before the shape binds: shipped, in a mounted zip, or kept from an earlier session. Whether a later re-bind picks up the download was not seen in 55 s | [lab] (torque/3d-shape-textures-420r6-2026-11-25.md#does-the-shape-draw-and-does-the-texture-apply) |

The rules below give which image files the same Linux 4.20r6 client decodes for shape and sky textures, each pre-placed on disk with its real extension (T3D-077) [lab] (torque/3d-texture-formats-420r6-2026-11-25.md#formats-and-bit-depths-lab).

| Rule | Source |
| --- | --- |
| PNG (8-bit indexed, 24-bit, 32-bit), JPEG, GIF, BMP (24-bit) and TGA (24 and 32-bit) all draw with correct colours and orientation | [lab] (torque/3d-texture-formats-420r6-2026-11-25.md#formats-and-bit-depths-lab) |
| DDS (BC1/DXT1) is not decoded: the shape stays white with no error, though the GL driver offers S3TC | [lab] (torque/3d-texture-formats-420r6-2026-11-25.md#formats-and-bit-depths-lab) |
| 100 × 100, 32 × 256, 1 × 1 and 2048 × 2048 PNGs all draw; no size ceiling was found | [lab] (torque/3d-texture-formats-420r6-2026-11-25.md#sizes-lab-png-24-base) |
| The sky box uses the same loader: pre-placed PNG faces drew; six JPEG faces delivered by the server were downloaded but not applied, as with shape textures | [lab] (torque/3d-texture-formats-420r6-2026-11-25.md#sky-textures) |
| This differs from 5.12, which drew BMP and TGA white (→ §8.5.11) | [lab] (torque/3d-texture-formats-420r6-2026-11-25.md#formats-and-bit-depths-lab); [lab][cap] (torque/live-512-own-server-textures-2026-11-25.md#texture-formats-t3d-032) |

The rules below give how the 3D side mounts archives of content (T3D-012) [bin][lab] (torque/3d-archives-404r2-512-2026-11-25.md).

| Rule | Source |
| --- | --- |
| 4.04r2 and 5.12 mount `.zip` and `.gpake` files as archives, automatically, whenever a file with that extension enters the resource registry; 5.12 and Linux 4.20r6 use a linked-in minizip; 5.12 also mounts `.wba` | [bin] (torque/3d-archives-404r2-512-2026-11-25.md#what-each-build-has) |
| A plain `.gpak` is never mounted: the registry returns before adding it, although the 2D side saves downloaded `.gpak` files to `levels3d/gpaks/` | [bin] (torque/3d-archives-404r2-512-2026-11-25.md#what-each-build-has) |
| A `.gpake` is read encrypted only if the 2D engine has stored a key for that file name; otherwise it is read as a plain zip. 5.12 also has `.enc` for single encrypted files | [bin] (torque/3d-archives-404r2-512-2026-11-25.md#what-each-build-has) |
| Archive members are registered by lower-cased bare file name, so a shape is found in whichever archive or folder holds it; archives anywhere under the data or user folder are mounted, apart from the folders the start-up scan skips (`src`, `ignore`, and in 4.04r2 also `pms`, `profiles`, `weblevels`, `scriptfiles`, `updatepackages`) | [bin] (torque/3d-archives-404r2-512-2026-11-25.md#what-each-build-has) |
| Live on Linux 4.20r6: a `.zip` in `levels3d/` holding a `.dts`, a `.3ds` and a PNG texture was mounted at start-up and both shapes drew with the zip's texture; the same bytes as `.gpak` were ignored; loose copies drew the same but were still requested from the server | [lab] (torque/3d-archives-404r2-512-2026-11-25.md#lab-linux-420r6-zip420-2026-11-25) |
| Archive members are never requested from the server, so a newer copy on the server would not replace a zip member | [inf] (torque/3d-archives-404r2-512-2026-11-25.md#lab-linux-420r6-zip420-2026-11-25) |
| A zip delivered mid-session was not reached: the client fetches only shape-type files for a `GameObject`, so mounting without a restart is untested; statically a saved file goes through the same registry entry | [lab][inf] (torque/3d-archives-404r2-512-2026-11-25.md#lab-linux-420r6-zip420-2026-11-25) |

The rules below give where 3D content came from and how terrain textures are mapped [file] (torque/engine-and-formats.md#3d-resource-formats).

| Rule | Source |
| --- | --- |
| No `.dts`, `.dif`, `.ter` or `.mis` file ships with any Graal client: the 3D content always came from the server | [file] (torque/engine-and-formats.md#3d-resource-formats) |
| 3.153 maps terrain textures to detail textures and footstep sound types in script (→ §10.4.4) | [file] (torque/engine-and-formats.md#3d-resource-formats) |
| 4.04r2 ships 3D GUI skins in `levels3d/gui/`, help pages in `levels3d/help/*.hfl` and nine `languages3D/language*.cs` tables of `$language::Name = "text";` lines, probably loaded by server GUI scripts | [file][inf] (graal3d/torque-engine-4x.md#files) |

## 10.7 Linux 3.04 and 4.20r6 internals

The sections below (→ §10.7.1 to §10.7.8) hold the static and lab reads of the Linux Torque-era clients' internals: how 3.04 starts and reads its compiled scripts, what its packaged streams hold, a small subset of its script executor, 4.20r6's native-object bridge, the show-image constants, the local value helpers, one menu walk, and where 3.04 gets its tile types. They are evidence boundaries for a reimplementer more than a protocol, and each says what it does not establish.

### 10.7.1 Startup and compiled-script reading (3.04)

[bin] The two 3.04-labelled unpacked trees are identical across 528 regular files each; the packed original is a separate input. [cap] The tested unpacked initializer fails its first observed signature check. The unchanged original passes both checks after its temporary/display environment is corrected. The comparison does not isolate packing as the cause. [bin] (client-internals/linux-304-startup-reader.md); [cap] (client-internals/linux-304-startup-reader.md)


[cap] In another original-input launch, the compiled reader returns true for `common/main.cs`: post-read state has 474 code words and 39 line pairs, matching the packaged version-33, 1,903-byte compiled file. The boolean is its low return byte, not unspecified upper bits. Packaged-file identity is retained; runtime memory-payload hashing and instruction execution are unmeasured. Termination and cleanup follow the reader return. No server, offline game or Windows E#503 resolution is claimed. [cap] (client-internals/linux-304-startup-reader.md)

[cap] A separate later unchanged-packed-input probe follows the same program object in one thread from compiled reading through first code-word fetch to native handler entry; next index is one. Of 474 words, 401 nonrelocation positions match and 73 relocation positions are excluded. Termination occurs at handler entry: no handler/script completion or gameplay is proved. Earlier reader-only and unpacked-startup failures retain their own stopping points. Server/commit: none; observations and original-carrier audit remain researcher-supplied. [cap] (client-internals/linux-304-startup-reader.md#later-relocation-aware-first-handler-checkpoint)

### 10.7.2 Packaged Torque streams and the later trees (3.04)

[bin] Each duplicate 3.04 label has the same 39 version-33 streams, 48,310 numeric words and 733 line pairs. Independent serialization reproduces every stream byte-for-byte. Numeric line-pair meanings remain unassigned; out-of-range identifier-pool selections remain flagged, separately from the reader's empty-string fallback. [bin] (formats/linux-torque-resource-scope.md)


[bin] A 1,463-file inventory across eight prepared trees (including eight generated launchers and both duplicate 3.04 labels; not pristine installer counts) finds no packaged `.dso` or offset-zero version-33 candidate in the six later supplied trees. All nine supplied localization script resources match across the three 4.x labels; older counterparts differ. The supplied standalone 6.x folders originally held only executables; each second prepared-tree file is a generated launcher. These are two 6.01r1 architectures and 6.03r7 x64, not three releases. The 4.x trees are 4.04r2, 4.20r6 and 4.20r8 as identified in the source note. These offline results exclude neither embedded/downloaded streams nor an engine/compiler. No process/server ran; later execution and Windows E#503 remain unproved. [bin] (formats/linux-torque-resource-scope.md)

### 10.7.3 A seven-operation executor subset (3.04)

[bin] Selected Linux 3.04 static paths establish bit-preserving immediate load, one-entry discard, consuming zero/nonzero conditional branches, absolute code-word targets, signed decimal conversion and return of the current string position. The analysis ELF and original packed executable retain distinct identities. [bin] (torque/linux-304-seven-operation-contract.md).

[inf] Seven independently authored acceptance vectors distinguish formatting and branch/stack behavior. They have not been executed in the original client; fresh invocation state, errors, string lifetime and complete VM equivalence remain unproved. The implementation comparison is pinned to its inspected snapshot. No runtime or server was started for this publication. [inf] (torque/linux-304-seven-operation-contract.md).

#### Native-call evidence boundary

[bin] A retained exact-input Linux 3.04 static review distinguishes script-defined recursive entry from registered native callback dispatch with argument-count checks; a selected resolved-call path can rewrite its word or operand to a cached form. Some registry helpers remain outside the selected export. This is static path evidence, not callback execution or complete lookup/caching policy. [bin] (torque/linux-304-seven-operation-contract.md#native-call-evidence-beyond-the-seven-operations)

[inf] Published inclusive command/method counts do not establish argument representation or callback ABI. The seven-operation executor return does not establish native callback result conversion or lifetime. Case/namespace precedence, duplicates, coercions, arity failures, cache invalidation and echo behavior remain unqualified; independent API policy tests are not original-client oracles. No new native inspection or runtime work was done for publication. [inf] (torque/linux-304-seven-operation-contract.md#native-call-evidence-beyond-the-seven-operations)


### 10.7.4 Native-object registration (4.20r6)

[bin] In the selected Linux 4.20r6 paths, constructor stores and runtime type metadata identify concrete SimGroup and GameConnection objects, each containing a Graal scripting-variable base subobject. The creation callback registers those base-subobject pointers on the scripting side, exposing a concrete static native-object bridge. Names alone are not the identification evidence. [bin] (client-internals/linux-420-native-object-bridge.md).

[bin] A tail-call forwarding path does not establish an ordinary C callback ABI; an optional fast path remains unresolved. The separate r8 review shows that equal embedded payloads do not imply equal execution-state layouts. Initializer execution, live TorqueScript, GUI/input and a working 3D session remain unobserved in this scope. No runtime or server was started for publication preparation. [bin] (client-internals/linux-420-native-object-bridge.md).

[bin] A selected r6 follow-up now connects the actual creation caller through that tail jump: three prepared stack words reach a target that consumes all three, and the caller does not consume a creation result before subsequent allocation. Separate lookup and optional adapters pass one and three words respectively and use only a zero-extended result byte. The representation helper unwraps a pointer/fallback without allocation or retention; this does not establish ownership. Optional target, other register/argument conventions, other callers, lifetime and runtime initialization remain open, so these selected boundaries are not a complete callback ABI. [bin][inf] (client-internals/linux-420-native-object-bridge.md#selected-stack-interfaces-2026-11-22).

### 10.7.5 Show-image wrapper constants (3.04)

[bin] Retained exact-input static findings bind showimg/showimg2 to mode 0, showani/showani2 to mode 4, showpoly/showpoly2 to mode 3 and showtext/showtext2 to mode 2, with respective flags 0/1 in every pair. These internal constants add precision to already documented command presence and polygon machinery; mode 1, signature-letter grammar, flag meaning and rendered results remain unqualified. [bin] (torque/304-draw.md#exact-show-image-wrapper-constants-retained-static-review)

[bin] A selected common helper uses a numeric-derived integer display key and finds or creates its indexed object. Lookup/insertion compares that key; the insertion helper rejects an equal key and otherwise inserts by position. This is a sorted integer-key container, not a generic name map. Numeric conversion edges, ownership, full helper ABI and corruption handling remain open. [bin] (torque/304-draw.md#exact-show-image-wrapper-constants-retained-static-review)

[inf] Local insertion rejection does not establish repeated-command behavior or console/namespace duplicate policy. These are retained static assertions, not new native execution or a general interpreter/callback contract; no cross-build behavior is inferred. Document digests are checked while underlying native observations remain researcher-supplied. [inf] (torque/304-draw.md#provenance-and-scope-of-this-addition)

### 10.7.6 Local value helpers (3.04)

[bin] Retained exact-input static review records a numeric accessor returning zero for null input, reading a stored double on its reviewed type/slot-absent branch and otherwise dispatching through a type-specific slot. A string-result accessor dispatches through its type-specific slot or a fallback initializer. A separate assignment helper includes scalar/numeric-array paths, element conversion and selected index-guarded writes. [bin] (torque/304-npcs.md#retained-local-numeric-and-string-helper-branches)

[inf] These are local branch observations, not a complete coercion, array/index or formatting specification. They do not establish universal variable defaults, an empty-string result, every runtime type, rounding/exceptional-value policy, parser grammar or storage lifetime. They are separate from the published Torque integer-to-string operation and do not establish a native callback result adapter or ABI. Underlying static findings remain researcher-supplied; only retained documents were reviewed for publication and no original-client conversion result is claimed. [inf] (torque/304-npcs.md#evidence-and-remaining-conversion-gaps)

### 10.7.7 Stage-0 menu walk (3.04)

The first stage-0 capture of the archived Linux 3.04 executable. `main.cs` already sets log mode 6 when no log switch is given, so the executable was not changed. The first session had no network. The second could reach only a lab listserver on port 14922. The display was 1024 by 768 and the client opened its default 800 by 600 window. Logs and screenshots stay owner-held; nothing in them names a host. [lab] (live-runs/open-issues-2026-11-14/README.md#6-243-linux-304-stage-0-capture)

| Item | What the run showed | Source |
| --- | --- | --- |
| console | engine init, then eight missing `glVertexBuffer` functions, then the OpenGL extension lists. The driver reported was Mesa llvmpipe | [lab] (live-runs/open-issues-2026-11-14/README.md#6-243-linux-304-stage-0-capture) |
| server list | `onDNSResolved` and `onConnected` are logged as having no namespace when the list connects. The list showed one tab, because the lab list had one server in one category | [lab] (live-runs/open-issues-2026-11-14/README.md#6-243-linux-304-stage-0-capture) |
| leaving | `quit` typed in the console without parentheses is a syntax error. The client then exits and writes its prefs and key map. The password is not saved | [lab] (live-runs/open-issues-2026-11-14/README.md#6-243-linux-304-stage-0-capture) |
| not covered | a four-tab server list, and any in-game screen. Tutorial was not opened | [lab] (live-runs/open-issues-2026-11-14/README.md#6-243-linux-304-stage-0-capture) |

### 10.7.8 Where tile types come from (3.04)

3.04 has no `arrays.dat` and no tile-type file or packet. The tile lists the 2.x clients read from `arrays.dat` are compiled into the executable as sorted lists of tile ids, and they equal 2.22's except that the water list lacks ids 1824 and 1825. Which rule judges a tile depends on the sheet type `tiledefs` picks for the level (→ §4.2) [bin][file] (torque/304-tile-types.md#short-answer).

| Rule | Source |
| --- | --- |
| Sheet type 0, the classic `pics1.png`: a tile is walkable only if its id is in the walkable list or the water list; any other id is a wall. Off-board positions use id 632, which is in neither, so they block | [bin] (torque/304-tile-types.md#the-walk-test-onwall-and-movement) |
| Sheet types 1 and 2, such as the offline tutorial's `picso.png`: no lists. With row = id / 16 and col = id % 16, a tile blocks when id is 32, or row is 26 or 27 with col ≥ 2, or row is in 30–47, 84–95 or 116–127, or row ≥ 128 with bit 16 of row set | [bin] (torque/304-tile-types.md#the-walk-test-onwall-and-movement) |
| Type tests (3, 4, 5, water 11, 12, 20, ledge 21) use the matching list on sheet type 0 and fixed id ranges on types 1 and 2; a failed test falls back to the level's objects | [bin] (torque/304-tile-types.md#type-tests) |
| `tiledefs<server>.txt` lines are `image,levelprefix,type[,x,y]`; on entering a level the longest matching prefix of type 0, 1, 2 or 5 wins, else `pics1.png` type 0. The scripts' `addtiledef`, `addtiledef2` and `removetiledefs` change the entries. The package ships only `tiledefsOffline.txt` for the tutorial | [bin][file] (torque/304-tile-types.md#how-the-sheet-type-is-chosen) |
| So a rebuild that shows 3.04 grass as a wall is applying another rule: a per-tile type table, the range rule on a `pics1` level, or the wrong board on a gmap | [inf] (torque/304-tile-types.md#what-this-means-for-the-rebuild) |
| The sheet type is one global value reset to 0 on level entry; there is no per-level tile-type table, and `tiletype` returns −1 on type 0. Type 5 makes the walk and type tests ignore tile ids, so only the level's `setshape2` shapes block | [bin] (client-internals/static-reads-appendix-e-2026-11-20-hostb-final.md#what-304-uses-for-tile-types-when-no-addtiledef-arrives-e507) |
| A loopback GServer-v2 / gs2emu login that admits `G3D03014` sends no `addtiledef` / `addtiledef2` / `removetiledefs` (no `NPCWEAPONADD`; clear/delete only) | [cap] (torque/304-tile-types.md#login-capture-2026-11-24) |

## 10.8 The 3D mode in the 2D clients

From 3.0 to 6.03 every client sends a `G3D` login token, but only some of them can enter a 3D world, and the token alone never says a session is 3D: the same string logs an ordinary 2D session in. "3D mode" here means the Torque side that a 3D-capable build starts beside its 2D game when the player picks a 3D server [bin] (graal3d/g3d-version-tokens.md#naming); [bin] (protocol/login-tokens-3x-7x.md#are-the-g3d-clients-3d). The February 2000 Graal3D is a different program with its own server and `GR3DV00x` tokens (→ §9).

| Build | 3D side | Torque protocol | Source |
| --- | --- | --- | --- |
| 3.04 Linux | the whole client is Torque, stock TGE networking, no 3D scripts shipped | 9 (`Torque Game Engine Demo`) | [bin] (protocol/login-tokens-3x-7x.md#are-the-g3d-clients-3d) |
| 3.153 Mac | Graal-changed TGE: a class table in the accept, datablocks, `levels3d/` and `main3D.cs` | 19 (`Graal3D`) | [bin][file] (graal3d/g3d-version-tokens.md#when-a-g3d-client-is-torque-3d-capable) |
| 4.03r3, 4.04r2 Windows | `Graal3DEngine.dll`, a separate engine with three exports (load, run, end), loaded the first time a 3D server is picked | 19 | [bin] (protocol/v4x-windows-403r3-411.md#the-3d-engine-became-a-library-in-411); [bin] (protocol/login-tokens-3x-7x.md#are-the-g3d-clients-3d) |
| 4.11 Windows | `Graal3DEngine.dll` becomes a library of 206 exports (among them `resizeGraal3DWindow` and `toggleGraal3DFullScreen`) that the 2D engine calls into, with new 2D-engine callbacks to create 3D game objects and read terrain height | unmeasured | [bin][inf] (protocol/v4x-windows-403r3-411.md#the-3d-engine-became-a-library-in-411); [bin] (protocol/v4x-windows-403r3-411.md#what-the-engine-gained) |
| 4.20 (Windows 4.20r8, Mac 4.20r6) | the `GameObject` layer, no datablocks (→ §10.5) | 21 (Mac 4.20r6 measured) | [bin] (graal3d/g3d-version-tokens.md#when-a-g3d-client-is-torque-3d-capable) |
| 5.00r7, 5.12 Windows | `Graal3DEngine.dll` 5.0.0.7, `GameObject` layer | 24 | [bin] (protocol/login-tokens-3x-7x.md#are-the-g3d-clients-3d) |
| 5.24r3 and every later build | none; only the `GuiGraal3DCtrl` class name is left | n/a | [bin] (protocol/login-tokens-3x-7x.md#are-the-g3d-clients-3d) |

The rules below give how a 3D-capable client enters 3D mode and what it carries. The step-by-step join is in → §10.2 and the handshake by build in → §10.3 [bin] (protocol/login-tokens-3x-7x.md#are-the-g3d-clients-3d).

| Rule | Detail | Source |
| --- | --- | --- |
| which server | a server is 3D when its list name starts with `3 `; picking one, or a server warp to such a name, opens the Torque side | [bin] (protocol/login-tokens-3x-7x.md#are-the-g3d-clients-3d) |
| two connections | the normal Graal TCP login on the listed port, and a Torque UDP connection to the same host on port + 1; the 3D side lives only as long as the TCP session | [bin] (protocol/login-tokens-3x-7x.md#are-the-g3d-clients-3d) |
| connect request | the game string `Graal3D`, the protocol twice, the account password in clear as the join password, and two arguments, account and nickname; the class CRC is a static `0xFFFFFFFF`, and the server sends its class names in the accept instead | [bin] (protocol/login-tokens-3x-7x.md#are-the-g3d-clients-3d) |
| who owns the window | in 3D mode the Torque DLL owns the window and the OpenGL output; the 2D engine still runs the game logic, GS2 and the Graal connection, and draws through the plug-in (→ §10.1.5) | [bin] (protocol/login-tokens-3x-7x.md#are-the-g3d-clients-3d) |
| content | no `.dts`, `.dif`, `.ter` or `.mis` file ships with a client; missions, `levels3d/` trees and `GameObject` data come from the server (→ §10.6) | [file] (graal3d/g3d-version-tokens.md#when-a-g3d-client-is-torque-3d-capable) |
| lab reach | a real 5.12 reached "Connection established" against a small lab responder; under Wine the same build stops at "Starting 3D mode" when its 3D side starts; native Linux 4.04r2 reached the mission start and printed "Graal3D has been activated!" | [bin] (protocol/login-tokens-3x-7x.md#are-the-g3d-clients-3d); [lab] (protocol/lab-appe-hosta-2026-11-20.md#not-run-in-the-final-batch); [lab] (protocol/lab-appe-hosta-2026-11-20.md#protocol-19-on-404r2-e506-half) |
| outside report | a third-party server author reported that a 5.007 client gets scripted 3D content over TCP on the game port and UDP on port + 1, and that 3D was gone from v6; the binaries put the cut at 5.24r3. That server's source is not public, so this is a report only | [doc] (protocol/login-tokens-3x-7x.md#are-the-g3d-clients-3d) |

How a server moves a 5.12 player in 3D is settled in §10.3 (a movetype and movement data on the control object); the join arguments of 3.153 and 4.20r6 are open [inf] (protocol/login-tokens-3x-7x.md#open-points).
