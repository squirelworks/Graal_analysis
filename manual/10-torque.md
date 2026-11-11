<!-- manual: kind=reference status=draft -->
# 10 Torque-era 3D (3.x to 5.12)

From 2004 to 2007 the Graal client was built on GarageGames' Torque Game Engine (TGE). Torque gave the console, the script VM, the GUI, the resource manager, the renderer and, for 3D servers, the UDP netcode; Graal's 2D game, GS1/GS2 and the Graal TCP protocol stayed native code on top. The February 2000 DirectX Graal3D is unrelated (→ §9).

> Status: draft.

## 10.0 Reading this Part

The Torque years are best understood as three different programs that share the name "Graal" and some of the same code. Before treating any table below as describing "the 3.x–5.x client", fix which of the three a build is. [bin] (torque/study-torque-clients.md#1-the-short-answer)

**First, the monolith.** The 3.x clients (3.04 Linux, 3.151 Linux, 3.153 Mac) are Torque applications. TGE boots them, compiled TorqueScript draws every menu, and Torque's canvas holds the screen. Graal's 2D game is one native GUI control, `GuiGraalCtrl`, inside that canvas. The engine reports TGE version 1100 and still carries the stock game classes it does not use. [bin] (torque/study-torque-clients.md#1-the-short-answer); [bin] (torque/engine-304.md#the-split) 3.04 has none of Graal's net-layer changes. 3.153 already has them, which makes 3.153, not 3.04, the first build whose UDP wire a compatible 3D server has to speak. [bin] (torque/wire-by-build.md#the-handshake-per-build)

**Second, the split programs.** From 4.04r2 to 5.12 on Windows, a Delphi launcher drives `GraalEngine.dll`, a C++ 2D engine that keeps Torque's GUI classes but draws only through callbacks into its host. Torque proper survives only in the optional `Graal3DEngine.dll`, which takes over drawing when the player joins a 3D server. [bin] (torque/study-torque-clients.md#1-the-short-answer); [bin] (torque/engine-4208.md#how-the-three-fit) Inside this era the 3D DLL changes character. 4.04r2's DLL is near-stock TGE with datablocks and `Player`. By 4.20r6 that game layer is gone and every 3D thing is a Graal `GameObject`. The break falls between the February and July 2006 tokens. [bin] (torque/engine-and-formats.md#which-torque); [bin] (torque/wire-by-build.md#the-handshake-per-build) So "the 4.x 3D client" is two incompatible object models, and the protocol number (19, 21, 24) is the reliable way to tell them apart. [bin] (torque/network.md#the-connect-request-by-version)

**Third, after Torque.** From 5.24r3, and in every 6.x build, there is no Torque engine. What survives is the GS2 GUI vocabulary: Torque's control class names, plus its field names up to 5.31r4, re-implemented by Graal's own `quattro_lib`. [bin] (client-internals/torque-surface-by-era.md#530r3-and-531r4); [bin] (client-internals/torque-surface-by-era.md#600r2-and-600r4) The 6.x reads gathered in §10.1.6 and §10.1.9 are here to document that absence. The 6.x engine itself is Part I's subject (→ §1.8.7).

**What is measured, and what is not.** The UDP handshake is the strongest material in this Part. 5.12 was driven live against a lab server through challenge, connect, accept and its first data packets, and the minimal accept it takes is known. [run] (torque/network.md#the-full-handshake-live) Everything after the accept rests on static reads, and no Graal client has been seen drawing a 3D world: under Wine, 5.12's launcher faults when it switches to 3D. [run] (torque/engine-and-formats.md#rendering) No 3D content shipped with any client, because missions, terrain and shapes always came from the server, and no Graal 3D server or level data is in the archives. [file] (torque/engine-and-formats.md#3d-resource-formats) The open points that would change an implementation are listed in App. E#501–E#503: the 4.04r2 class CRC, and whether 4.04r2 loads `.mis` and `.dso` files.

**How the later sections are scoped.** §10.7 to §10.12 record exact-build observations on Linux 3.04 and 4.20r6: script reading, packaged streams, a seven-operation executor subset and native-call boundaries. Each is deliberately narrow. A finding there holds for that input and that path, and it is not a general statement about TorqueScript execution in Graal. [bin] (torque/linux-304-seven-operation-contract.md)

## 10.1 Engine lineage

### 10.1.1 Builds

| Build | Date | Shape | Torque part | 3D world | Game string / protocol | Menu scripts | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1998 to 2.31 | — | Delphi | none | none | n/a | n/a | [bin] (torque/wire-by-build.md#which-builds-are-torque) |
| 3.04 Linux | Jan 2004 | one C++ binary (SDL, OpenAL) | full TGE, version number 1100 | TGE classes, no 3D scripts shipped | `Torque Game Engine Demo` / 9 | TorqueScript `.dso` | [bin] (torque/README.md#lineage-at-a-glance) |
| 3.153 Mac | Feb 2005 | one C++ binary (Carbon, PPC) | full TGE with Graal's net-layer changes | stock TGE world and `main3D.cs` client scripts | `Graal3D` / 19 | TorqueScript `.dso` | [bin][file] (torque/README.md#lineage-at-a-glance) |
| 4.04r2 Win | Mar 2006 | Delphi launcher, `GraalEngine.dll` (2D) and `Graal3DEngine.dll` (3D plug-in) | 2D engine on Torque base classes; the 3D DLL near-stock TGE | stock TGE with datablocks | `Graal3D` / 19 | GS2 and native | [bin] (torque/README.md#lineage-at-a-glance) |
| 4.20r6 Mac | Sep 2006 | one C++ binary (PPC) | Torque core and netcode, Graal game layer | `GameObject` model, no datablocks | `Graal3D` / 21 | GS2 and native | [bin] (torque/wire-by-build.md#which-builds-are-torque) |
| 4.20r8 Win | Jan 2007 | 2D engine on Torque base classes | — | packet-logger upload has no `Graal3DEngine.dll` (later file-version 4.2.0.8 export: → §10.1.5) | unmeasured | GS2 and native | [bin] (torque/wire-by-build.md#which-builds-are-torque) [bin] (torque/engine-4208.md#how-the-three-fit) |
| 5.12 Win | Oct 2007 | Delphi launcher and one engine DLL, still named `Graal3DEngine.dll` | Torque core and netcode; the game layer is Graal's own | `GameObject` and `GameShape*`, no datablocks, no `Player`/`ShapeBase` | `Graal3D` / 24 | GS2 and native | [bin] (torque/README.md#lineage-at-a-glance) |
| 5.24r3 and later | 2010+ | engine linked into `Graal.exe` | no Torque 3D (what Windows 6.00 still names → §10.1.8) | none | n/a | GS2 | [bin] (torque/engine-and-formats.md#which-torque) |
| 6.x | 2010–2014 | native C++ per platform | no Torque 3D; GS2 keeps Torque control names (→ §10.1.8) | none | n/a | GS2 | [bin] (torque/README.md#lineage-at-a-glance); [bin] (client-internals/engine-600r2.md#what-torque-names-remain) |

### 10.1.2 Engine version and changes

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
| Torque GUI field names (`horizSizing`, `vertSizing`, `minExtent`, `fontType`, `fillColor`, `makeFirstResponder`, `pushToBack`) | absent; those names are a 5.24r3 finding | [bin] (client-internals/engine-600r2.md#gui-and-script-objects); [bin] (torque/study-torque-clients.md#524r3-6x) |
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

## 10.2 Join sequence

| Step | What happens | Source |
| ---: | --- | --- |
| 1 | The server list marks a 3D server with the name prefix `3 ` (the "Graal 3D" tab) | [bin] (protocol/v3x-clients.md#listserver) |
| 2 | Choosing it runs one routine in 3.153, 4.04r2 and 5.12: strip the two-character prefix, remember UDP port = listed port + 1, set the 3D-mode flag and start the Torque side | [bin] (torque/network.md#how-a-client-gets-to-a-3d-server) |
| 3a | 3.153 creates a `SimGroup` named `MissionGroup` and runs `main3D.cs`, which creates `GameConnection(ServerConnection)` and calls `connect()` with the stored address | [bin][file] (torque/network.md#how-a-client-gets-to-a-3d-server) |
| 3b | 4.04r2 and 5.12 first ask the launcher (a non-zero answer cancels), then have it connect to host, port + 1, with the UDP option; 4.04r2 loads `Graal3DEngine.dll` on demand at this point | [bin] (torque/network.md#how-a-client-gets-to-a-3d-server) |
| 4 | In both 2D and 3D the client opens the normal Graal TCP connection to the listed port and logs in as usual (→ §2.3) | [bin] (torque/network.md#how-a-client-gets-to-a-3d-server) |
| 5 | The Torque handshake runs on UDP (→ §10.3), then the mission download (→ §10.3.6) | [bin][run] (torque/network.md#the-full-handshake-live) |

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
| class CRC | stock table, value unmeasured | unmeasured | disputed → App. E#501 | unmeasured | `0xFFFFFFFF` (static table, never written) | [bin][run] (torque/wire-by-build.md#the-handshake-per-build) |
| join password | the server-password pref | set by the engine, not traced | the account password, plain text | not traced | the account password, plain text | [bin] (torque/network.md#the-connect-request-by-version) |
| argc (at most 16), then strings | script args | engine-set, not traced | 2: account, nickname | not traced | 2: account, nickname | [bin] (torque/network.md#the-connect-request-by-version) |
| server side of the request | stock script `onConnectRequest` | stock script `onConnectRequest` | native | native | native | [bin] (torque/wire-by-build.md#the-handshake-per-build) |

| Rule | Source |
| --- | --- |
| The live 5.12 request was 71 bytes and decoded completely: group 0, CRC `0xFFFFFFFF`, `Graal3D`, 24/24, the built-in guest password as join password, argc 2 (`guest`, empty nickname), no bits left over | [run] (torque/network.md#the-full-handshake-live) |
| A 5.12 server rejects a game string other than `Graal3D` with `CHR_GAME` ("Only official Graal clients are allowed to connect."), current < 24 with `CHR_PROTOCOL_LESS`, minimum > 24 with `CHR_PROTOCOL_GREATER`, and argc > 16 with `CR_INVALID_ARGS` | [bin] (torque/network.md#the-connect-request-by-version) |
| 4.04r2 knows the same reasons plus `CHR_PROTOCOL` and `CHR_INVALID`; it rejects < 19 and a minimum ≥ 20 | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |
| Stock Torque rejects a CRC mismatch with `CHR_INVALID`; in 5.12 the class table in the accept takes the CRC's place | [bin][run] (torque/network.md#the-connect-request-by-version) |

### 10.3.3 Connect accept and class table

| Field | Width | Meaning | Source |
| --- | --- | --- | --- |
| flag | 1 bit | 1 = another entry follows, 0 = end of table | [bin][run] (torque/network.md#the-connect-request-by-version) |
| class type | 12 bits | 0 object, 1 datablock, 2 event (3.153, 4.04r2); 0 object, 1 event (4.20r6, 5.12; the event meaning is inferred) | [bin][inf] (torque/network.md#the-connect-request-by-version) |
| server class id | 12 bits | 0 to 255 | [bin] (torque/network.md#the-connect-request-by-version) |
| class name | string | Huffman string, such as `NetStringEvent` | [bin] (torque/network.md#the-connect-request-by-version) |
| protocol | U32 | after the end flag; must equal the build's protocol | [bin][run] (torque/network.md#the-connect-request-by-version) |

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

| Rule | Source |
| --- | --- |
| The u32 server time is a Graal addition; the client keeps it as its synchronised clock | [bin] (graal3d/torque-engine-4x.md#server--client-data-packet) |
| In 5.12 the client always reports its own position and never sends a Torque `Move`; position is client-reported as in 2D Graal | [bin] (torque/wire-by-build.md#512-game-packets-the-gameobject-era) |
| Unguaranteed events: flag 1, int12 class id, sized payload, …, flag 0; guaranteed-ordered events add a flag (next in sequence) else int7 sequence | [bin] (graal3d/torque-engine-4x.md#events) |
| Ghosts: flag, int4 index width (sent as is; TGE sends width − 3), then per ghost flag 1, index, flag (delete), and if not deleted int12 class id on every update and the sized data; flag 0 ends | [bin] (graal3d/torque-engine-4x.md#ghosts-graal-changes) |
| New ghosts go into the client's `MissionGroup`; in 4.04r2 they wait while TCP file downloads are running | [bin] (graal3d/torque-engine-4x.md#ghosts-graal-changes) |
| In 5.12 the class id reader takes 12 bits and applies the server-to-local map; events and ghosts each have their own length wrappers | [bin] (torque/wire-by-build.md#512-game-packets-the-gameobject-era) |

### 10.3.6 Mission download

| Build | Phases | Source |
| --- | --- | --- |
| 3.153, 4.04r2 (stock TGE) | 1 "Download Datablocks & Targets", 2 "Download Ghost Objects", 3 "Mission Lighting" | [bin][file] (torque/network.md#after-the-connection-is-accepted) |
| 5.12 | 1 "Download Ghost Objects", 2 "Mission Lighting" | [bin] (torque/network.md#after-the-connection-is-accepted) |

| Rule | Source |
| --- | --- |
| The server drives the phases with `MissionStartPhaseN` remote commands and the client answers `MissionStartPhaseNAck` | [bin] (torque/network.md#after-the-connection-is-accepted) |
| In 3.153 these are script functions; phase 1 acks with the sequence number, and phase 3 lights the scene and acks when lighting is done | [file] (torque/network.md#after-the-connection-is-accepted) |
| In 4.04r2 they are native; the acks carry only the command tag, no sequence number; every other `commandToClient` name is ignored | [bin] (graal3d/torque-engine-4x.md#mission-start) |
| 4.04r2 raises `onGraal3DLoginStep` 1 to 5: phases 1, 2 and 3, lighting done (`$missionRunning = 1`), and the first control object (switch to the 3D GUI) | [bin] (graal3d/torque-engine-4x.md#mission-start) |
| 5.12 starts the value at −1 and raises 2 (phase 1), 3 (phase 2), 4 (lighting done), 5 (first control object) and 6 (TCP file downloads finished, the `GraalControl3D` GUI attached) | [bin] (torque/wire-by-build.md#512-game-packets-the-gameobject-era) |
| The 3.153 loading screen is a snowball rolling across `LoadingGui`, with the Christmas 2004 3D images | [file] (torque/scripting.md#what-the-3153-scripts-do) |

The retained Windows 4.04r2 review traces native datablock/ghost/lighting phase dispatch and network-class construction into the mission group, with a deferred-preload path. This is positive network-mission evidence; separate local mission/script readers remain unresolved (→ App. E#502, → App. E#503). No new 3D session or file-loading trace was obtained. [bin] (torque/404r2-resource-filter.md#positive-native-mission-path)

## 10.4 DSO v33

Graal 3.x keeps menus, options, key binds, message boxes and the 3D mission-loading flow in compiled TorqueScript; from 4.x on no `.dso` files ship [file] (torque/scripting.md#torquescript-in-graal-3x-the-dso-format-and-the-shipped-scripts).

### 10.4.1 Shipped scripts

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

| Rule | Source |
| --- | --- |
| Code inside a function body uses the function tables; code outside uses the global tables | [file] (torque/scripting.md#file-format-version-33) |
| The Mac PPC build writes the F64 tables big-endian while the rest stays little-endian; the 3.04 Linux files are little-endian throughout | [file] (torque/scripting.md#file-format-version-33) |
| An argument the body never uses gets an ident offset just past the end of the global string table, so its name is lost | [file] (torque/scripting.md#file-format-version-33) |
| All 83 shipped files decode with the opcode table below and no other | [file] (torque/scripting.md#graals-opcode-table) |

### 10.4.3 Opcodes

The numbering differs from stock TGE 1.x: two unused opcodes follow `CREATE_OBJECT` and one follows `CALLFUNC` [file] (torque/scripting.md#graals-opcode-table).

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

| Rule | Source |
| --- | --- |
| Operands: `FUNC_DECL` name, namespace, package, hasBody, end ip, argc, then argc arg idents; `CREATE_OBJECT` parent ident, isDatablock, fail ip; `ADD_OBJECT` and `END_OBJECT` one flag; jumps one target | [file] (torque/scripting.md#graals-opcode-table) |
| `SETCURVAR`, `SETCURVAR_CREATE`, `SETCURFIELD`, the `LOADIMMED_*` opcodes, `TAG_TO_STR` and `ADVANCE_STR_APPENDCHAR` take one operand; `CALLFUNC` and `CALLFUNC_RESOLVE` take name, namespace and call type (0 function, 1 method, 2 parent); the rest take none | [file] (torque/scripting.md#graals-opcode-table) |
| The operand shape is the same as stock TGE 1.x; opcodes 2, 3 and 72 never occur, so what they were is unknown | [file] (torque/scripting.md#graals-opcode-table) |
| The repo has a disassembler and a decompiler for this format under `torque/tools/` | [doc] (torque/scripting.md#the-decoder) |

### 10.4.4 What the 3.153 scripts do

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

| Rule | Source |
| --- | --- |
| The 2D Graal player is still the player; 3D objects can carry ganis and show-images | [bin] (torque/engine-and-formats.md#the-512-3d-object-model) |
| The GS2 properties on `GameObject` are `alpha`, `attachedtoobject`, `attr`, `attrobjects`, `chat`, `collision`, `iseditorobject`, `liquidheight`, `liquidtype`, `movetype`, `nickcolor`, `nickname`, `scaledshapebox`, `shadow`, `shape`, `shapebox`, `showterrain`, `skin`, `solid`, `velocity`, `watercoverage` | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |

`GameObject` update, 5.12: thirteen flag-guarded sections; the mask bits are the server's dirty bits, and on the wire each section is one flag [bin] (torque/wire-by-build.md#the-512-gameobject-update).

| # | Dirty bits | Payload after the flag | Source |
| ---: | --- | --- | --- |
| 1 | `0x1` | string, the object's name | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 2 | `0x2` or `0x200` | 3 × 32 bits (velocity, inferred) | [bin][inf] (torque/wire-by-build.md#the-512-gameobject-update) |
| 3 | `0x8` | string, a setting of the movement object | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 4 | `0x10` | string, also passed to the movement object | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 5 | `0x20` | transform: position, rotation, then 32 bits; the packing is unmeasured | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 6 | `0x80` | string that creates or replaces the shape object (`shape`, inferred) | [bin][inf] (torque/wire-by-build.md#the-512-gameobject-update) |
| 7 | `0x40`, with a shape object | the shape object's own data | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 8 | any of `0xF00`, with a movement object | int14 bit length, then the movement object's data | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 9 | `0x1000` | string, the chat text (with emoticons) | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 10 | always 0 from this DLL | the reader takes a string and loads it as a script or image; what a real server sent is unknown | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 11 | any of `0x3FC000` | the attribute list | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |
| 12 | `0x400000` | string, then 4 colour bytes RGBA 0–255 (nickname and `nickcolor`, inferred) | [bin][inf] (torque/wire-by-build.md#the-512-gameobject-update) |
| 13 | `0x800000` | int16 of booleans; bits `0x01`, `0x04`, `0x08`, `0x10`, `0x20`, `0x40` are used | [bin] (torque/wire-by-build.md#the-512-gameobject-update) |

### 10.5.3 Graal events over Torque

| Event | Direction | Layout | Source |
| --- | --- | --- | --- |
| `BigDataStartEvent` | both | int16 transfer id, three strings (`s1`, `s2`, `s3`, each up to 255 characters), int24 total length, int3 coding (0 none, 1 zlib, 2 bzip2) | [bin] (graal3d/torque-engine-4x.md#graal-events-and-text-big-data-channel) |
| `BigDataChunkEvent` | both | int16 transfer id, int8 length (up to 191), the bytes | [bin] (graal3d/torque-engine-4x.md#graal-events-and-text-big-data-channel) |
| `TerrainChunkEvent` | S→C | int4 chunk x, int4 chunk y, u32 (a stamp, inferred), int10 length, then a zlib 16 × 16 piece of heights and materials; 16 × 16 chunks make a 256 × 256 terrain | [bin][inf] (graal3d/torque-engine-4x.md#terrain-streaming-graal) |
| `TerrainRequestUpdatesEvent` | C→S | 256 × u32, one per chunk, telling the server what the client already has | [bin] (graal3d/torque-engine-4x.md#events) |
| `RequestReloadEvent` | C→S | asks the server to resend an object | [bin] (graal3d/torque-engine-4x.md#events) |
| `SimDataBlockEvent` (4.04r2) | S→C | int12 (id − 3), int12 class id, int12 index, int13 total, sized datablock data | [bin] (graal3d/torque-engine-4x.md#events) |
| `RemoteCommandEvent` | both | int5 argc, tagged-string arguments; the 4.04r2 client acts only on the mission phases | [bin] (graal3d/torque-engine-4x.md#events) |
| others | — | `GhostAlwaysObjectEvent`, `NetStringEvent`, `ConnectionMessageEvent`, `PathManagerEvent`, `SimpleMessageEvent`, the audio and lightning events, stock TGE | [bin] (graal3d/torque-engine-4x.md#events) |

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

## 10.6 3D formats

| Ext | Format | Builds | Source |
| --- | --- | --- | --- |
| `.dts`, `.dsq` | Torque shape and sequence; 4.04r2 reads up to version 24; 5.12 rejects shapes that are too old | 3.x, 4.04r2, 5.12 | [bin] (torque/engine-and-formats.md#3d-resource-formats); [bin] (graal3d/torque-engine-4x.md#files) |
| `.dif` | Torque interior; 4.04r2 reads resource version 44, interior version 0 | all | [bin] (graal3d/torque-engine-4x.md#files) |
| `.ter` | Torque terrain, version 3 or older, from `levels3d/terrain/` | 3.x, 4.04r2 | [bin] (graal3d/torque-engine-4x.md#files) |
| terrain chunks | streamed with `TerrainChunkEvent` (→ §10.5.3) | 5.12 | [bin] (torque/engine-and-formats.md#3d-resource-formats) |
| `.3ds` | 3D Studio (`Shape3ds`, then `GameShape3DS`) | 3.153, 4.04r2, 5.12 | [bin] (torque/engine-and-formats.md#3d-resource-formats) |
| `.md3` | Quake 3 model in head, upper and lower parts, version 15 | 3.153, 4.04r2 | [bin] (torque/engine-and-formats.md#3d-resource-formats); [bin] (graal3d/torque-engine-4x.md#files) |
| `.mis` | Torque mission file; 5.12 has no `.mis` loader and builds its `MissionGroup` from ghosts (inferred) | 3.x; 4.04r2 disputed → App. E#502 | [bin][inf] (torque/engine-and-formats.md#3d-resource-formats); [bin][inf] (graal3d/torque-engine-4x.md#files) |
| `.ml`, `.ifl`, `.dml` | material lists and image-file lists for animated textures | stock Torque | [bin] (torque/engine-and-formats.md#3d-resource-formats); [bin] (graal3d/torque-engine-4x.md#files) |
| `.gft` | Torque cached GUI font | 3.x, 4.04r2, 5.12 | [bin] (torque/engine-and-formats.md#3d-resource-formats); [bin] (graal3d/torque-engine-4x.md#files) |
| `.dso` | compiled TorqueScript (→ §10.4) | 3.x; 4.04r2 disputed → App. E#503 | [file] (torque/scripting.md#torquescript-in-graal-3x-the-dso-format-and-the-shipped-scripts); [bin] (graal3d/torque-engine-4x.md#files) |
| images | `.png`, `.jpg`, `.jp2`, `.jng`, `.mng`, `.gif`, `.bmp`, `.bm8`, `.tga`, `.dds` | 4.04r2 | [bin] (graal3d/torque-engine-4x.md#files) |
| `.zip`, `.gpake` | archives the resource manager opens | 4.04r2 | [bin] (graal3d/torque-engine-4x.md#files) |

| Rule | Source |
| --- | --- |
| No `.dts`, `.dif`, `.ter` or `.mis` file ships with any Graal client: the 3D content always came from the server | [file] (torque/engine-and-formats.md#3d-resource-formats) |
| 3.153 maps terrain textures to detail textures and footstep sound types in script (→ §10.4.4) | [file] (torque/engine-and-formats.md#3d-resource-formats) |
| 4.04r2 ships 3D GUI skins in `levels3d/gui/`, help pages in `levels3d/help/*.hfl` and nine `languages3D/language*.cs` tables of `$language::Name = "text";` lines, probably loaded by server GUI scripts | [file][inf] (graal3d/torque-engine-4x.md#files) |

## 10.7 Linux 3.04: startup and compiled-script reading

[bin] The two 3.04-labelled unpacked trees are identical across 528 regular files each; the packed original is a separate input. [cap] The tested unpacked initializer fails its first observed signature check. The unchanged original passes both checks after its temporary/display environment is corrected. The comparison does not isolate packing as the cause. [bin] (client-internals/linux-304-startup-reader.md); [cap] (client-internals/linux-304-startup-reader.md)


[cap] In another original-input launch, the compiled reader returns true for `common/main.cs`: post-read state has 474 code words and 39 line pairs, matching the packaged version-33, 1,903-byte compiled file. The boolean is its low return byte, not unspecified upper bits. Packaged-file identity is retained; runtime memory-payload hashing and instruction execution are unmeasured. Termination and cleanup follow the reader return. No server, offline game or Windows E#503 resolution is claimed. [cap] (client-internals/linux-304-startup-reader.md)

[cap] A separate later unchanged-packed-input probe follows the same program object in one thread from compiled reading through first code-word fetch to native handler entry; next index is one. Of 474 words, 401 nonrelocation positions match and 73 relocation positions are excluded. Termination occurs at handler entry: no handler/script completion or gameplay is proved. Earlier reader-only and unpacked-startup failures retain their own stopping points. Server/commit: none; observations and original-carrier audit remain researcher-supplied. [cap] (client-internals/linux-304-startup-reader.md#later-relocation-aware-first-handler-checkpoint)

## 10.8 Linux 3.04: packaged Torque streams and the later trees

[bin] Each duplicate 3.04 label has the same 39 version-33 streams, 48,310 numeric words and 733 line pairs. Independent serialization reproduces every stream byte-for-byte. Numeric line-pair meanings remain unassigned; out-of-range identifier-pool selections remain flagged, separately from the reader's empty-string fallback. [bin] (formats/linux-torque-resource-scope.md)


[bin] A 1,463-file inventory across eight prepared trees (including eight generated launchers and both duplicate 3.04 labels; not pristine installer counts) finds no packaged `.dso` or offset-zero version-33 candidate in the six later supplied trees. All nine supplied localization script resources match across the three 4.x labels; older counterparts differ. The supplied standalone 6.x folders originally held only executables; each second prepared-tree file is a generated launcher. These are two 6.01r1 architectures and 6.03r7 x64, not three releases. The 4.x trees are 4.04r2, 4.20r6 and 4.20r8 as identified in the source note. These offline results exclude neither embedded/downloaded streams nor an engine/compiler. No process/server ran; later execution and Windows E#503 remain unproved. [bin] (formats/linux-torque-resource-scope.md)

## 10.9 Linux 3.04: a seven-operation executor subset

[bin] Selected Linux 3.04 static paths establish bit-preserving immediate load, one-entry discard, consuming zero/nonzero conditional branches, absolute code-word targets, signed decimal conversion and return of the current string position. The analysis ELF and original packed executable retain distinct identities. [bin] (torque/linux-304-seven-operation-contract.md).

[inf] Seven independently authored acceptance vectors distinguish formatting and branch/stack behavior. They have not been executed in the original client; fresh invocation state, errors, string lifetime and complete VM equivalence remain unproved. The implementation comparison is pinned to its inspected snapshot. No runtime or server was started for this publication. [inf] (torque/linux-304-seven-operation-contract.md).

### Native-call evidence boundary

[bin] A retained exact-input Linux 3.04 static review distinguishes script-defined recursive entry from registered native callback dispatch with argument-count checks; a selected resolved-call path can rewrite its word or operand to a cached form. Some registry helpers remain outside the selected export. This is static path evidence, not callback execution or complete lookup/caching policy. [bin] (torque/linux-304-seven-operation-contract.md#native-call-evidence-beyond-the-seven-operations)

[inf] Published inclusive command/method counts do not establish argument representation or callback ABI. The seven-operation executor return does not establish native callback result conversion or lifetime. Case/namespace precedence, duplicates, coercions, arity failures, cache invalidation and echo behavior remain unqualified; independent API policy tests are not original-client oracles. No new native inspection or runtime work was done for publication. [inf] (torque/linux-304-seven-operation-contract.md#native-call-evidence-beyond-the-seven-operations)


## 10.10 Linux 4.20r6: native-object registration

[bin] In the selected Linux 4.20r6 paths, constructor stores and runtime type metadata identify concrete SimGroup and GameConnection objects, each containing a Graal scripting-variable base subobject. The creation callback registers those base-subobject pointers on the scripting side, exposing a concrete static native-object bridge. Names alone are not the identification evidence. [bin] (client-internals/linux-420-native-object-bridge.md).

[bin] A tail-call forwarding path does not establish an ordinary C callback ABI; an optional fast path remains unresolved. The separate r8 review shows that equal embedded payloads do not imply equal execution-state layouts. Initializer execution, live TorqueScript, GUI/input and a working 3D session remain unobserved in this scope. No runtime or server was started for publication preparation. [bin] (client-internals/linux-420-native-object-bridge.md).

## 10.11 Linux 3.04: show-image wrapper constants

[bin] Retained exact-input static findings bind showimg/showimg2 to mode 0, showani/showani2 to mode 4, showpoly/showpoly2 to mode 3 and showtext/showtext2 to mode 2, with respective flags 0/1 in every pair. These internal constants add precision to already documented command presence and polygon machinery; mode 1, signature-letter grammar, flag meaning and rendered results remain unqualified. [bin] (torque/304-draw.md#exact-show-image-wrapper-constants-retained-static-review)

[bin] A selected common helper uses a numeric-derived integer display key and finds or creates its indexed object. Lookup/insertion compares that key; the insertion helper rejects an equal key and otherwise inserts by position. This is a sorted integer-key container, not a generic name map. Numeric conversion edges, ownership, full helper ABI and corruption handling remain open. [bin] (torque/304-draw.md#exact-show-image-wrapper-constants-retained-static-review)

[inf] Local insertion rejection does not establish repeated-command behavior or console/namespace duplicate policy. These are retained static assertions, not new native execution or a general interpreter/callback contract; no cross-build behavior is inferred. Document digests are checked while underlying native observations remain researcher-supplied. [inf] (torque/304-draw.md#provenance-and-scope-of-this-addition)

## 10.12 Linux 3.04: local value helpers

[bin] Retained exact-input static review records a numeric accessor returning zero for null input, reading a stored double on its reviewed type/slot-absent branch and otherwise dispatching through a type-specific slot. A string-result accessor dispatches through its type-specific slot or a fallback initializer. A separate assignment helper includes scalar/numeric-array paths, element conversion and selected index-guarded writes. [bin] (torque/304-npcs.md#retained-local-numeric-and-string-helper-branches)

[inf] These are local branch observations, not a complete coercion, array/index or formatting specification. They do not establish universal variable defaults, an empty-string result, every runtime type, rounding/exceptional-value policy, parser grammar or storage lifetime. They are separate from the published Torque integer-to-string operation and do not establish a native callback result adapter or ABI. Underlying static findings remain researcher-supplied; only retained documents were reviewed for publication and no original-client conversion result is claimed. [inf] (torque/304-npcs.md#evidence-and-remaining-conversion-gaps)
