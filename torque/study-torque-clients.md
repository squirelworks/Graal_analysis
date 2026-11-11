# The Torque-era Graal clients: what each one really is, and what a rebuild must reproduce

Date: 2026-11-05. Tags as in `README.md` (**[bin]** client binary, **[file]** shipped data, **[run]**/**[cap]** lab run, **[inf]** inferred).

This note pulls the Torque findings together per client and answers one question: what does a faithful rebuild of a 3.x-and-later client need that the 2D rebuild (the 2.22 Delphi engine with each version's network layer on top) does not have? It adds new evidence where the older notes had gaps: a marker scan of seventeen binaries from 3.04 to 6.11, the shipped-script dependency list of 3.04, the 4.x/5.00 draw-callback bridge between the 2D engine and Torque, and the heights data in the shipped tutorial gmap. The plan that follows from it is [rebuild-plan-3.04.md](rebuild-plan-3.04.md).

Sources: the 3.04 Linux and 3.153 Mac trees and their decompiled scripts (project folder `graal-decompile/torque/`), the string tables of `graalexe` 3.04 (unpacked), `Graal` 3.153, the 4.04r2 `Graal4.exe` / `GraalEngine.dll` / `Graal3DEngine.dll`, the 4.20r8 `Graal4.exe` / `GraalEngine.dll` (the third-party packet-logger upload, see `protocol/v4x-clients.md`), the 5.00r7 `Graal.exe` / `GraalEngine.dll.bak` (the unpatched engine) / `Graal3DEngine.dll`, 5.12, the unpacked 5.24r3, 5.31r4, 6.00r2 and 6.03r7 Windows dumps, Linux 6.01r1 and 6.03r7, and Mac 6.11. Nothing was run for this note. 4.20r6 Mac is covered from `wire-by-build.md` (only its decompile is in the project folder).

## 1. The short answer

Squirrel's point is right, and it is bigger than 3.04. "Graal on Torque" means three different programs over time:

| Era | Builds | What the program is | Where Torque sits |
|---|---|---|---|
| **A. Torque monolith** | 3.04 Linux, 3.151 Linux, 3.153 Mac (4.20r6 Mac is a late hybrid, see §3) | One C++ program on TGE 1.1–1.2. The **whole client is a Torque app**: Torque's `main.cs` boots it, TorqueScript `.dso` files build every menu, the Torque GUI canvas holds the screen, Torque's texture manager and OpenGL draw it. The Graal 2D game is **one native GUI control** (`GuiGraalCtrl`, named `Adventure`) inside that canvas. | Everything except the Graal game and the Graal TCP protocol. |
| **B. Delphi shell + C++ engine + optional Torque 3D** | 4.04r2, 4.20r8, 5.00r7, 5.12 (Windows) | A **Delphi** launcher (window, DirectDraw / Direct3D 7, input, Flash panels, external windows) loads `GraalEngine.dll`, a C++ engine that still uses Torque's GUI classes (`GuiCanvas`, `GuiControl`, `GBitmap`, `Point2I`, `MatrixF`) but **draws nothing itself**: it calls back into whoever hosts it. On a 3D server `Graal3DEngine.dll` (stock-ish TGE in 4.04r2, Graal's `GameObject` layer from 4.20) becomes the host and draws the same 2D game through Torque's OpenGL. | GUI class library always; the full engine only when the 3D DLL is loaded. |
| **C. Graal's own engine** | 5.24r3 and later (5.30, 5.31, 6.00–6.03 Windows, 6.01/6.03 Linux, 6.11 Mac) | One native program per platform drawing with OpenGL (SDL on Linux). No Torque console, script VM, texture manager, scene graph or netcode. What survives is the **GS2 GUI API**: Torque's control class names and field names (`GuiControlProfile`, `GuiScrollCtrl`, `horizSizing`, `makeFirstResponder`, …) re-implemented by Graal. | Names only. |

So the graal-delphi folders get these three eras wrong in three different ways:

- **Era A (3.04, 3.153):** the folders are a Delphi 2D window with no Torque at all. The real program's menus, start screen, server list, options, key binds, console, fonts and theme come from **files the client ships** (`.dso`, `.gui`, `.gft`, theme PNGs) and are run by a TorqueScript VM. A faithful rebuild has to run those files, not redraw look-alike screens.
- **Era B (4.04r2–5.12 Windows):** the launcher really **is** Delphi, so a Delphi front end is the right shape here, but the engine behind it is a renderer-agnostic C++ core with a ~115-entry callback table, and 3D servers swap the renderer for Torque. A faithful rebuild needs that split (front end ↔ engine via callbacks), and the 3D side needs a Torque-compatible client.
- **Era C (5.24r3+ and 6.x):** no Torque engine to reproduce. These are honestly "the 2D engine plus a newer protocol", but drawn with OpenGL and with GS2 GUI controls that follow Torque's GUI model. The folders for 6.01r1 and 6.03r7 are therefore closer to the truth than the 3.x/4.x ones, though they still lack the GS2 GUI.

**After 6.x: 7.x Worlds.** The 7.x Worlds client is outside this Delphi → TGE → hybrid → own-engine line. The host is Unity: `GameAssembly.dll` (IL2CPP) owns gameplay, UI and asset bundles, and it calls a native `Graal3DEngine*.dll` plugin through exported `Quattro*` frame hooks. **[bin]** (`protocol/v7-graal3d-identity-and-builds.md`, `client-internals/v7-graal3d-unity-bridge.md`) Only the host is a clean break. The plugin still carries the 6.x Graal core: classic netcode and gen-5 framing, PLI/PLO props, the GS2 VM, the ciphers and the file cache. It reports FileVersion 6.114 and builds its login like the 6.11 connector. **[bin][inf]** (`protocol/v7x-protocol.md`) No Torque surface is involved.

## 2. Marker scan

Counts of string hits per binary (both 8-bit and UTF-16 strings). 0 means the marker is absent. "eng" = `GraalEngine.dll`, "g3d" = `Graal3DEngine.dll`, "exe" = the launcher or single executable. **[bin]**

| Marker | 3.04 | 3.153 | 4.04r2 exe | 4.04r2 eng | 4.04r2 g3d | 4.20r8 eng | 5.00r7 exe | 5.00r7 eng | 5.00r7 g3d | 5.12 g3d | 5.24r3 | 5.31r4 | 6.00r2 | 6.01r1 L | 6.03r7 L | 6.03r7 W | 6.11 Mac |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `GuiCanvas` | 2 | 3 | 0 | 64 | 12 | 65 | 0 | 67 | 13 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 10 |
| `GuiControl` (exact) | 1 | 2 | 0 | 103 | 69 | 109 | 0 | 122 | 78 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| `SimObject` | 1 | 5 | 0 | 0 | 4 | 0 | 0 | 0 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Texture manager | 2 | 2 | 0 | 0 | 2 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `GBitmap` | 1 | 1 | 0 | 52 | 22 | 54 | 0 | 58 | 25 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `.dso` / `exec(` / `setModPaths` | yes | yes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `OpenGLDevice` | 2 | 2 | 0 | 0 | 7 | 0 | 0 | 0 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| DirectDraw | 0 | 0 | 32 | 0 | 0 | 0 | 33 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gl…` entry names | (Torque loader) | (Torque loader) | 0 | 0 | — | 0 | 0 | 0 | — | — | 367 | 367 | 367 | 78 | 78 | 368 | 47 |
| `GameConnection` | 2 | 4 | 0 | 0 | 4 | 0 | 0 | 0 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `TerrainBlock` | 8 | 6 | 0 | 0 | 5 | 0 | 0 | 0 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `TSShape` / `.dts` | 12 | 16 | 0 | 0 | 11 | 0 | 0 | 0 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `GuiGraalCtrl` | 2 | 3 | 0 | 3 | 0 | 3 | 0 | 3 | 0 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 17 |
| `GuiGraal3DCtrl` | 0 | 3 | 0 | 1 | 3 | 1 | 0 | 1 | 3 | 3 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| `GuiScrollCtrl` | 2 | 5 | 0 | 4 | 0 | 4 | 0 | 6 | 0 | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 29 |
| `ActionMap` | 8 | 10 | 0 | 0 | 8 | 0 | 0 | 0 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| SDL | 65 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 4 | 0 | 0 |

"—" means not counted. Reading it:

- 3.04 and 3.153 have every Torque layer: console and script (`exec`, `setModPaths`, `.dso`), `SimObject`, the texture manager (`dgl/gTexManager.cc`, "Resurrecting the texture manager..."), `GFont` with `.gft` caches (`%s%s_%d.gft`, "Error, The Arial Font must always be available!"), `ActionMap`, `OpenGLDevice`, and the whole 3D side. 3.04's source paths include `dgl/bitmapPng.cc`, `dgl/gFont.cc`, `game/gameConnection.cc`, `editor/terrainEditor.cc`.
- The 4.x/5.00 engine DLLs export Torque's GUI and bitmap classes as C++ symbols (`GuiCanvas::renderFrame`, `GuiControl::onRender`, `GuiControl::renderChildControls`, `GBitmap::readPNG`, `GBitmap::readJPEG2000`, `GBitmap::readDDS`, …) but have **no console, no `SimObject`, no texture manager, no `OpenGLDevice`, no `ActionMap`**. Their launchers have DirectDraw and no OpenGL. The Torque engine proper only appears in `Graal3DEngine.dll`.
- From 5.24r3 the single executable carries OpenGL entry names (367 on Windows) and no Torque class beyond the GUI names; Linux 6.x uses SDL + OpenGL.

## 3. Per client

### 3.04 Linux (Jan 2004, token `G3D03014`)

| | |
|---|---|
| Engine | TGE 1.1–1.2 code base: `getVersionNumber` 1100, compile time "Jan 3 2004 at 22:32:08", game string `Torque Game Engine Demo`, protocol 9, home `~/.garagegames/`. **[bin]** (`engine-and-formats.md`) |
| Platform layer | SDL 1.2 (window, input, `SDL_WM_ToggleFullScreen`), OpenGL 1.3, fmod 3.70 for sound and MIDI, hvdi voice packaging with GSM and LPC codecs for the microphone. `lib/librariesinfo.txt` lists zlib 1.1.3, libmng 1.0.5, hvdi 0.9, SDL 1.2, OpenGL 1.3, fmod. **[file][bin]** |
| Torque subsystems used | Console and TorqueScript VM (`.dso` v33), resource manager with mod paths, GUI canvas and ~30 stock GUI control classes, GUI profiles and themes, `GFont` + `.gft` cache, texture manager, `ActionMap` input, prefs export, console window (F2), help system (`.hfl`), OpenGL device. The 3D classes are compiled in but no 3D script ships. **[bin][file]** |
| Not Torque | The 2D game (`graal/adventure.cpp`, `levels.cpp`, `npcs.cpp`, `ganis.cpp`, `tiles.cpp`, `graphics.cpp`, `showimgs.cpp`, …), GS1, the Graal TCP protocol (gen 5, same as 2.22), the 2.05-style UDP channel between players, the listserver client. **[bin]** (`../client-internals/` and `v3x/FINDINGS.md` in the project folder) |
| Boot | `graalexe` runs the plain-text root `main.cs`: `setLogMode(6)`, `setModPaths("common;graaldata")`, `exec("common/main.cs")`, `exec("graaldata/main.cs")`, `onStart()`. `graaldata/main.cs` loads defaults and prefs and activates package `graal`; `initClient()` calls `initBaseClient()`, `initCanvas("Graal")`, execs `customProfiles.cs`, nine `.gui` files, four scripts and `config.cs`, then `Canvas.setContent(mainMenuGui)`. **[file]** |
| The 2D game on screen | `GraalGui.gui` creates `GuiControl(AdventureGui)` holding `GuiGraalCtrl(Adventure)` (640 × 480, relative sizing) with a child `GuiTextEditCtrl(ChatBar)` whose `altCommand` is `Adventure.setChat(ChatBar.getValue());`. `AdventureGui::onWake` pushes `moveMap`; `onSleep` pops it. **[file]** |
| Input | Keys go through Torque's `ActionMap` (`moveMap`) to script, which calls the native control: `Adventure.moveUp/Down/Left/Right`, `doA`, `doS`, `doD`, `doQ`, `doP`, `doM`, `doMicro`. **[file][bin]** (3.153 method table; 3.04's binds use the same map) |
| Lab | Runs natively on Linux; draws the classic top-down view with the stock HUD and white chat with a blue shadow. **[run]** (`version-profiles/lab-304-linux-2026-10-30.md`) |
| Console surface | 31 methods on `GuiGraalCtrl`, including `playerListProfile` and `doA`/`doS`/`doD`/`doQ`/`doP`/`doM`. No `setNickName`, `setAccountName`, `setLanguage` or `retrieveAccountFields` (those are the 3.153 table). Argument counts: `engine-304.md`. **[bin]** |

### 3.153 Mac (Feb 2005, token `G3D28015`)

Same engine as 3.04 for PPC/Carbon/AGL, plus Graal's Torque net changes (`Graal3D` protocol 19, class table, 12-bit class ids, BigData and terrain events), community TGE resources (`AdvancedCamera`, `fxFoliageReplicator`, `volumeLight`), `Shape3ds` and `Md3` loaders. Ships 44 `.dso` (`scripts/`, `scripts2D/`, `scriptsgui/`) and 13 plain `.cs`. **[bin][file]** (`wire-by-build.md`, `scripting.md`)

- 2D: `main2D.cs` (package `graal`) does `initCanvas("Graal3D")`, loads `GraalGui.gui` and shows `MainMenuGui2D`; `start2D()` sets `Canvas.setContent(Adventure)`. **[file]**
- 3D: `main3D.cs` (package `graal3D`, which deactivates `graal`) loads `playGui.gui`, whose root is **`GuiGraal3DCtrl(PlayGui)`** with `LagIcon` and `ChatBar3D` children. `PlayGui::onWake` pushes **both** `moveMap2D` and `moveMap`, so one key press moves the 3D view and the Graal 2D player at once. Then `new GameConnection(ServerConnection)` and `connect()`. **[file]**
- Native script surface: the console method table registers 22 methods on `GuiGraalCtrl` (the movement and action calls above, `setChat`, `retrieveAccountFields`, `setNickName`, `setAccountName`, `setPassWord`, `setLanguage`, `selectServer`, `selectServerCategory`, `serverDirectConnect`, `updatePlayerProfile`, `updatePlayerMuted`) next to the stock TGE ones (`fxSunLight` 49, `GuiMenuBar` 11, `AdvancedCamera` 8, `Terraformer` 7, …). **[bin]**
- RTTI shows the Graal-side draw classes: `TGraalUniverse`, `TDrawableObject`, `TLevelObject`, `TGaniObject`, `TShowImg`, `TShowImgMount`, `TTilesVar`, `GuiPlayerView`, each with a `…Properties` script binding class. **[bin]**

### 4.04r2 Windows (Mar 2006, `G3D17026`)

- `Graal4.exe` (Delphi, DirectDraw/Direct3D 7) + `GraalEngine.dll` (C++; Torque GUI classes, no console) + `Graal3DEngine.dll` (near-stock TGE: `Player`, datablocks, vehicles, `fx*` replicators; `Graal3D` protocol 19). **[bin]** (`graal3d/torque-engine-4x.md`)
- The bridge: the engine draws only through callbacks the host registers (`graal_setDraw2DTile`, `graal_setDraw3DTile`, `graal_setClear3DTile`, `graal_setCreateTilesBuffer`, `graal_setScrollTilesBuffer`, `graal_setDrawTilesOnScreen`, `graal_setStartTilesDrawing`/`EndTilesDrawing`, `graal_setDrawGraphics…`, `graal_setDrawText`, `graal_setDrawShadowedText`, `graal_setGetTextWidth`, …, plus `graal_setStartGraal3D`, `graal_setConnectTo3DServer`, `graal_setRemoveGraal3DDatablocks`, `graal_setRemoveGraal3DMissionGroup`, `graal_setSendGraal3DScriptEvent(s)`, `graal_setSendGraal3DServerText`). When the 3D DLL loads it registers its own set and the 2D game draws through Torque's canvas. **[bin]**
- Data: `levels3d/gui/` (44 GUI skin PNGs), `levels3d/help/*.hfl`, `languages3D/language*.cs` (9 plain TorqueScript tables), the 2D `levels/` tree (tiles, ganis, images, the offline tutorial). No `.dso`. **[file]**

### 4.20r6 Mac (Sep 2006, `G3D27076`) and 4.20r8 Windows (Jan 2007, `G3D20126`)

- 4.20r6 is again one PPC binary with the Torque core and netcode, but with Graal's `GameObject` model, protocol 21, and GS2/native menus: no `.dso` ships. So it sits between eras A and B: a Torque program like 3.153, with the 4.x engine and GUI inside it. Its rebuild follows 3.153's 3D stages with the 4.x 2D engine. **[bin][file]** (`wire-by-build.md`, `README.md`)
- 4.20r8 (`Graal4.exe` FileVersion 4.2.0.8): same split as 4.04r2. The engine adds `graal_setGetGraal2DMatrix`, `PushGraal2DMatrix`, `PopGraal2DMatrix`, `IsGraal2DMatrixActivated`, `GetGraal3DTerrainHeight`, `CreateGraal3DGameObject`, `DeleteGraal3DLightInfo`, `IsOpenGLEnvironment`, `DrawTriangleStripPanel`. So by 4.20 the 2D game can draw a tile or image with a 3D transform and ask the 3D host for the terrain height under it: this is how 2D content (tiles, ganis, show-images) sits in the Torque world. The packet-logger upload has no 3D DLL. A later export named 4.2.0.8 does include `Graal3DEngine.dll` ([engine-4208.md](engine-4208.md)). **[bin][inf]**

### 5.00r7 Windows (Jul 2007, `G3D22067`) and 5.12 (Oct 2007)

- 5.00r7 (`Graal.exe` FileVersion 5.0.0.7): same split; the unpatched engine has the 4.20r8 callback set plus `PushColorMatrix`/`PopColorMatrix`. `Graal3DEngine.dll` (Jul 2007) is the `GameObject`-era Torque (`OpenGLDevice`, `D3DDevice`, `GameConnection`, `TerrainBlock`, `TSShape`; no interiors in the string table) and imports `graal_set…` names from the engine. Data adds `levels3d/gui2/` (51 PNGs) and `levels3d/db/`. **[bin][file]**
- 5.12: one engine DLL still named `Graal3DEngine.dll` for 2D and 3D, `Graal3D` protocol 24. **[bin]** (`engine-and-formats.md`)

### 5.24r3 → 6.x

No Torque engine (see §2). 6.01r1 and 6.03r7 Linux use SDL + OpenGL; Windows 5.24r3 to 6.03r7 carry ~367 OpenGL entry names; Mac 6.11 has its own build. The GS2 GUI keeps Torque's control names (`GuiControlProfile`, `GuiWindowCtrl`, `GuiScrollCtrl`, `GuiMLTextCtrl`, `GuiBitmapButtonCtrl`, `GuiTextListCtrl`, …) and adds Graal ones (`GuiShowImgCtrl`, `GuiTilesCtrl`, `GuiPMCtrl`, `GuiStartMenuCtrl`, `GuiAccountPasswordCtrl`, `GuiSlideShowCtrl`, `GuiAccordionCtrl`, `GuiAnimationCtrl`). 5.24r3 still carries Torque field names (`horizSizing`, `vertSizing`, `minExtent`, `fontType`, `fillColor`, `makeFirstResponder`, `pushToBack`). **[bin]**

Unpacked Windows 6.00r2 and 6.00r4 (12 and 26 June 2011) agree there is no Torque 3D. They do not contain `GuiTilesCtrl` or those field names; the field names stay a 5.24r3 finding. `GuiGraal3DCtrl` is a live GUI type beside `GuiGraalCtrl`. See `client-internals/engine-600r2.md`. **[bin]**

## 4. What ships, and in what format (3.04)

The 3.04 `release/` tree, 556 files. **[file]**

| Folder | Count | Format | Read by |
|---|---|---|---|
| `main.cs` | 1 | plain TorqueScript (root boot script) | Torque |
| `common/client`, `common/ui`, `common/main.cs` | 19 | `.dso` v33 (TGE starter "common" mod: canvas, cursor, message boxes, console, GUI editor, inspector, help, load/save file dialogs, default profiles) | Torque |
| `common/ui/cache` | 14 | `.gft` Torque font caches: Arial 12–36, Arial Bold 14/16, Isabelle 14/20, Isabelle Bold 14, Lucida Console 12/14. Header starts with U32 1, then height, baseline and glyph count (Arial 14: 14, 11, 224). | Torque `GFont` |
| `common/ui/themes/{default,mac,windows}` | 31 | PNG bitmap arrays (button, window, scroll, check, radio, slider, menu, text edit, border, cursor) + `.th` theme scripts (`GuiDefaultProfile.fillColor = "0 128 0";` …) | Torque GUI profiles |
| `common/help` | 6 | `.hfl` help pages + JPEGs | Torque help dialog |
| `graaldata/client`, `graaldata/main.cs` | 20 | `.dso` v33 (Graal menus: main menu, server list, options, remap, player list, PMs, profile, load level, `GraalGui`) | Torque |
| `graaldata/languages` | 11 | `.dso` language tables (`languageEnglish`, `languageDeutsch`, …) | Torque |
| `levels/tiles` | 2 | `pics1.png`, `picso.png` | Graal |
| `levels/tiledefs` | 1 | `tiledefsOffline.txt`: `picso.png,offlinetutorial,1,0,0` | Graal |
| `levels/tutorial` | 9 | `GR-V1.03` binary levels `offlinetutorial_{a,b,c}-{1,2,3}.graal` | Graal |
| `maps` | 8 | `offlinetutorial.gmap` (`GRMAP001`), `bigmap.txt`, `minimap.txt`, `newmainmap.txt`, map PNGs | Graal |
| `levels/ganis` | 91 | `.gani` (84) + images | Graal |
| `levels/{bodies,heads,swords,shields,hats,horses,baddies,emoticons,smilies,images,letters,npcs,weapons,webgifs,backpals,snapshot}` | ~220 | PNG, MNG (19 animated) | Graal |
| `levels/midis`, `sounds` | 93 | MIDI (43), WAV (50) | fmod |
| `license` | 3 | `license.graal` (CRLF text, listserver host list), `sig.graal`, `sig.license` (RSA-1024 / SHA-1 signatures) | Graal |
| `lib` | 3 | `libSDL-1.2.so.0`, `libfmod-3.70.so`, `librariesinfo.txt` | loader |

The shipped tutorial gmap carries **height data**: `GENSEED`, `GENBASE`, `GENEVENBORDERS`, `GENHEIGHT`, `GENCHAOS`, `LEVHEIGHT 5.81535`, `LEVCHAOS 0.55`, a 4 × 4 `HEIGHTMAP`, `RANDOMSEEDS` (3 × 3), and one `HEIGHTS <level> 8 8` block per level, each 9 lines of 9 comma-separated floats (9 blocks). It has no `LEVELNAMES` block: the nine names appear only in the `HEIGHTS` headers and `GENERATED`. The levels themselves are `GR-V1.03` with no `HEIGHTS` section. 4.04r2 ships the same tutorial and gmap byte layout. **[file]** Whether the 2D view of 3.04 uses these heights at all is open; the lab screenshots are flat top-down. The 4.20 callbacks (`GetGraal3DTerrainHeight`, the 2D matrix) are the first point where a 2D object is placed on 3D terrain. **[inf]**

## 5. What the shipped 3.04 scripts need from the engine

Read from the 39 decompiled 3.04 scripts (`dec304/`). This is the native surface a script VM has to provide before the real 3.04 menus can run from their own files. **[file]**

- **Objects created** (31 classes): `GuiTextCtrl` (52 instances), `GuiButtonCtrl` (51), `GuiControlProfile` (45), `GuiControl` (29), `GuiTextEditCtrl` (29), `GuiScrollCtrl` (16), `GuiWindowCtrl` (15), `GuiCheckBoxCtrl` (11), `GuiPopUpMenuCtrl` (10), `GuiTextListCtrl` (7), `GuiMLTextCtrl` (7), `GuiSliderCtrl` (6), `GuiChunkedBitmapCtrl` (4), and one or two each of `GuiTreeViewCtrl`, `GuiInspector`, `GuiControlListPopUp`, `GuiCursor`, `GuiMLTextEditCtrl`, `GuiBitmapBorderCtrl`, `GuiBitmapCtrl`, `GuiRadioCtrl`, `GuiConsole`, `GuiConsoleEditCtrl`, `GuiConsoleTextCtrl`, `GuiEditCtrl`, `GuiFrameSetCtrl`, `GuiProgressCtrl`, `GuiInputCtrl`, `FileObject`, `ActionMap`, and **`GuiGraalCtrl`**.
- **Global functions** (stock TGE unless marked): `activatePackage`, `deactivatePackage`, `exec`, `export`, `echo`, `error`, `quit`, `schedule`, `isObject`, `isFile`, `expandFilename`, `fileBase`, `fileName`, `filePath`, `findFirstFile`, `findNextFile`, string helpers (`getWord`, `getWords`, `getWordCount`, `firstWord`, `getField`, `getFieldCount`, `getSubStr`, `strlen`, `strstr`, `stripMLControlChars`), `setRandomSeed`, video (`createCanvas`, `setDisplayDevice`, `getDisplayDeviceList`, `getResolutionList`, `getDesktopResolution`, `isDeviceFullScreenOnly`, `setScreenMode`, `toggleFullScreen`, `videoSetGammaCorrection`, the `setOpenGL…` hints), input (`activateKeyboard`, `deactivateKeyboard`, `lockMouse`), `gotoWebPage`.
- **Methods**: stock GUI and object methods (`setContent`, `pushDialog`, `bind`, `bindCmd`, `getBinding`, `push`, `pop`, `save`, `setValue`, `getValue`, `setText`, `addRow`, `setRowById`, `sort`, `sortNumerical`, `setSelectedRow`, `setActive`, `setVisible`, `resize`, `getExtent`, `forceReflow`, `performClick`, `openForRead`, `readLine`, `isEOF`, …) and **Graal's native ones**: `openServerList`, `selectServer`, `selectServerCategory`, `serverDirectConnect`, `connectToSelectedServer`, `startOfflineMode`, `loadLevel`, `setChat`, `setPassWord`, `updateGraalOptions`, `updateLoadLevelFields`, `updatePlayerProfile`, `updatePlayerMuted`, `playerListOpenPlayer`, `privateMessageSend`, `updateMidiVolume`, `updateMp3Volume`, `updateRadioVolume`, `updateMicroActivationLevel`.

That list is small enough to build and test against the shipped files one by one: every 3.04 script must load, every `.gui` must build its control tree, and the main menu must come up from `Canvas.setContent(mainMenuGui)` with the shipped theme and fonts.

## 6. What the 2D Delphi engine lacks, per era

| Needed | Era A (3.04, 3.153) | Era B (4.04r2–5.12 Windows) | Era C (5.24r3+, 6.x) |
|---|---|---|---|
| Boot from the client's own `main.cs` with mod paths | **yes** | no | no |
| TorqueScript VM that runs `.dso` v33 (Graal opcode table, big-endian floats on PPC) and plain `.cs` | **yes** | 4.04r2 local-reader/VM reachability remains unmeasured: [retained code](404r2-resource-filter.md) contains short `.dso`/`.cs` literals in a download filter, invalidating the earlier absence claim. The earlier 5.00r7/5.12 defined-string scans reported no `exec`, `.dso` or script-compiler strings; those inputs are not rechecked here | no |
| Console object model (`SimObject`, `SimGroup`, names, fields, packages, namespaces, `schedule`) | **yes** | 3D DLL keeps `SimObject`/`SimGroup`; the earlier "without a script language" conclusion is a disputed inference. Local VM reachability remains unmeasured (see [retained-code follow-up](404r2-resource-filter.md) and [App. E#503](../manual/app-e-open-questions.md#e503-whether-404r2-reads-dso-compiled-torquescript)) | no |
| Torque GUI canvas + stock control set + profiles + themes, sized from `.gui` files | **yes** | engine DLL keeps the class model, launcher draws | GS2 re-implementation of the same model |
| `.gft` font cache reader and Torque text rendering | **yes** | 3D DLL | no (TrueType: Tempus Sans, Arial) |
| Torque texture manager over OpenGL (PNG/JPEG/GIF/MNG/JPEG 2000 via `GBitmap`) | **yes** | 3D DLL | own OpenGL |
| `ActionMap` input routed through script to `Adventure.*` | **yes** | no (launcher DirectInput) | no |
| Console window (F2), log file, prefs `export("$pref::*")`, `config.cs` key map save | **yes** | 3D DLL console log only | no |
| `GuiGraalCtrl`: the Graal 2D game as a GUI control inside the canvas | **yes** | yes (drawn by host callbacks) | yes |
| Draw-callback split between front end and engine | no | **yes** (~115 `graal_set…` callbacks) | no |
| Torque UDP `GameConnection` on listed port + 1, mission download, ghosts | 3.153 only | when a `"3 "` server is chosen | no |
| Torque 3D world (terrain, DTS, DIF, sky, water, `GameObject`) | 3.153 only | 3D DLL | no |
| 2D content in 3D (`GuiGraal3DCtrl`, 2D matrix, terrain height under a tile) | 3.153 (dual key maps) | 4.20r8+ callbacks | no |

## 7. Open points

- How `GuiGraalCtrl::onRender` in 3.04 draws tiles (batched textured quads from `pics1.png`, or per-tile bitmap blits) is not read yet. It matters for pixel-exact output; a first rebuild can use the documented 2D result as the reference picture and compare against lab screenshots.
- Whether 3.04 uses the gmap `HEIGHTS` data in 2D (see §4).
- 3.04's UDP between players is the 2.05 channel (`protocol/udp-p2p.md`), not Torque netcode; the two-player lab capture already shows it. The voice (`doMicro`, GSM/LPC) payload is not decoded.
- No 3D server data (missions, `.ter`, `.dts`, `.dif`) ships with any client; the 3D world has to be authored or found before any 3D stage can be checked against a real server.
- 4.20r6's own binary is not in the project folder (only its decompile), so it was not in the marker scan.
