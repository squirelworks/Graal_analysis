# A Torque-faithful rebuild, starting with 3.04: stages, checks, and what "0.0.2" means

Date: 2026-11-05. Follows from [study-torque-clients.md](study-torque-clients.md). This is a plan, not a finding; facts it relies on carry their source note.

## Why the current 3.x folders are not 0.0.2

The graal-delphi 3.04 folder is the 2.22 rebuild with 3.04's wire changes. On the wire that is close to right (3.04 speaks 2.22's protocol), but the program around it is not 3.04: the real client is a Torque application that boots from its own `main.cs`, builds every screen from shipped `.dso`/`.gui` files, draws with Torque's GUI and fonts, routes keys through `ActionMap`, and hosts the Graal game as a single GUI control (`GuiGraalCtrl` named `Adventure`). None of that exists in the folder. So it stays at **0.0.1 (wire reproduction)**, and the same holds for every 3.x+ folder built the same way.

## What "0.0.2" should mean for each era

| Era | Builds | 0.0.2 means |
|---|---|---|
| A. Torque monolith | 3.04, 3.153 | The rebuild **boots from the client's own root `main.cs`** with mod paths, **runs the shipped `.dso` scripts unmodified** (no redrawn menus), builds the real main menu from the shipped `.gui`, `.gft` fonts and theme PNGs, has the F2 console and `ActionMap` key binds from the shipped `default.bind.cs`, and reaches a lab server **through the script path** (`Adventure.openServerList` → `selectServer` → `connectToSelectedServer`) to play the 2D game inside `GuiGraalCtrl`. Checked against lab screenshots and the real client's console log. 3D is not part of 0.0.2. |
| A/B hybrid | 4.20r6 Mac | Deferred until 3.153 3D works (one Torque binary, GS2 menus, `GameObject` world). |
| B. Delphi shell + C++ engine | 4.04r2, 4.20r8, 5.00r7, 5.12 | A Delphi launcher (the right shape here) and a separate engine that **draws only through a callback table** modelled on the `graal_set…` set (2D tiles, tile buffers, graphics, text, panels, 2D matrix), with the engine's GUI following Torque's control model. 3D servers are out of scope for 0.0.2. |
| C. Graal's own engine | 5.24r3+, 6.01r1, 6.03r7 | No Torque engine to reproduce. 0.0.2 keeps the 2D-engine meaning, plus the GS2 GUI control model (Torque names and fields). |

A folder that only changes the wire is labelled 0.0.1 and says so in its README. Nothing ships as 0.0.2 for era A or B until the checks below pass.

## Decision for Squirrel: which language for the Torque layer

graal-delphi's rule is "in the language they were written in". 3.x was C++ on Torque. Two honest options:

1. **Object Pascal in graal-delphi** (recommended): a shared `common/torque/` layer (script VM, sim objects, GUI, fonts, textures, input) written from public TGE 1.x behaviour and our own notes. It reuses the 2D game already written in Pascal for 2.22 (3.04 speaks 2.22's protocol), and era B's launchers are Delphi anyway. The README rule gets one line: era A's shell is a Pascal re-implementation of a C++ engine, judged by running the client's own files.
2. **C++** in a separate tree, written to TGE 1.x's structure. Closest in language, but it cannot reuse the Pascal 2D game, so the Graal side is written twice.

Either way the yardstick is the same: the original client's own script, GUI and font files run unmodified and the result matches the lab captures. Torque source may be read for behaviour only under its own licence (Torque3D is MIT; check TGE 1.x's terms before reading it), and no Graal decompile goes into the rebuild, as now.

## Checklist

Tick a stage when its test passes. The rebuild work is tracked in
squirelworks/graal-delphi#109 (on hold), the research follow-ups here in #243.

- [ ] Decision: the Torque layer's language (squirelworks/graal-delphi#110)
- [ ] Stage 0: reference captures of the real 3.04
- [ ] Stage 1: script VM and sim objects
- [ ] Stage 2: GUI canvas, controls, profiles, fonts, theme
- [ ] Stage 3: input, console, prefs
- [ ] Stage 4: `GuiGraalCtrl` (0.0.2 for 3.04)
- [ ] Stage 5: 2D parity (0.0.3 for 3.04)
- [ ] Stage 6: 3.153 shell
- [ ] Stage 7: 3.153 Torque UDP link
- [ ] Stage 8: 3.153 3D play
- [ ] Stage 9: 4.04r2 launcher and engine split
- [ ] Stage 10: 4.20r8 and 5.00r7

## Stages for 3.04

Each stage ends in a test that can fail. "Real" means the original `graalexe` 3.04 run in the existing lab (Linux, loopback servers); reference shots are in the project folder (`graal-decompile/v3x/lab/shots/`, `ato/stage1-start-window-304.png`).

### Stage 0: reference captures (no rebuild code)

- Run the real 3.04 once more in the lab and keep: its `console.log` (log mode 6 writes one per session), every menu screen at the default size, the options tabs, the server list with all four tabs, the F2 console, the `prefs.cs` and `config.cs` it writes on exit.
- **Proves:** there is ground truth for each later stage. Without the console log, stage 1 cannot be checked.

### Stage 1: script VM and sim objects

- Load DSO v33 with Graal's opcode table (`scripting.md`), the plain root `main.cs`, and run them: globals, locals, string stack, `CALLFUNC` resolution, namespaces and `Parent::`, packages (`activatePackage`, `deactivatePackage`), `SimObject` with names and dynamic fields, `SimGroup`/`SimSet`, `new` blocks, `schedule`, `exec`, `export`, `FileObject`.
- The stock functions the 3.04 scripts call are listed in the study (§5); stub the video and canvas ones for now.
- **Test:** all 39 3.04 `.dso` and `main.cs` execute without an unknown-opcode or unknown-function error; the sequence of `exec` calls and `echo` lines matches the real `console.log`; `export("$pref::*")` writes a `prefs.cs` that matches the real one for the same settings.
- **Proves:** the client's own scripts run, so menus and binds can come from the real files from here on.

### Stage 2: GUI canvas, controls, profiles, fonts, theme

- `GuiCanvas` with `setContent`, `pushDialog`, `popDialog`, cursor; the 31 control classes the scripts create, in the order of how often they occur (text, button, profile, plain control, text edit, scroll, window, check box, pop-up menu, text list, ML text, slider, chunked bitmap, then the rest); `GuiControlProfile` fields; theme bitmap arrays from `common/ui/themes/*` and the `.th` scripts; `.gft` reader (study §4) and Torque-style text layout; relative/right/top sizing.
- Rendering: OpenGL through the existing window layer, or the software surface first with the same coordinates. The check is the picture, not the API.
- **Test:** `Canvas.setContent(mainMenuGui)` from the shipped `init.cs` shows the main menu; pixel diff against the lab shot within a stated tolerance (fonts and theme exact, anti-aliasing tolerated). Same for the server list, options and message boxes.
- **Proves:** the start screen is the real one, built from 3.04's own files.

### Stage 3: input, console, prefs

- `ActionMap` (`bind`, `bindCmd`, `push`, `pop`, `save`), `GlobalActionMap`, F2 `ConsoleDlg` with `GuiConsole`, the remap dialog writing `config.cs`, keyboard activation and full-screen toggling.
- **Test:** a scripted key press goes binding → script → command (log the call chain); the remap dialog saves a `config.cs` that matches the real one; the console accepts `echo("x");`.
- **Proves:** keys reach the game the way 3.04 routed them.

### Stage 4: `GuiGraalCtrl` (0.0.2 for 3.04)

- A GUI control class that hosts the existing 2D game (levels, ganis, GS1, the 3.04 protocol), sized by `GraalGui.gui`, with the `ChatBar` child and the 31 native methods `engine-304.md` lists for this binary: `moveUp/Left/Down/Right`, `doA/S/D/Q/P/M`, `doMicro`, `setChat`, `setPassWord`, `openServerList`, `selectServer`, `selectServerCategory`, `startOfflineMode`, `connectToSelectedServer`, `serverDirectConnect`, `privateMessageSend`, `playerListOpenPlayer`, `playerListProfile`, `updateLoadLevelFields`, `loadLevel` (three script arguments), `updatePlayerProfile` (ten), `updatePlayerMuted`, and the volume and options setters. Nickname, account and language are `$pref::Graal::` variables in 3.04. `setNickName`, `setAccountName`, `setLanguage` and `retrieveAccountFields` are the 3.153 table, not this one.
- The server list fills the shipped `ServerListGui` with the name-prefix tabs (Gold, 3D, Classic, Hosted, hidden).
- **Test:** from the real main menu, log into the lab listserver, pick the lab server on the Classic tab, play: the capture has the same shape as `run1-304-online` (login frame, 37, 34s, props 75 `linux`, no 39), walk/sword/chat screenshots match the real client's, the player list and PM windows open from F7 and the script.
- **Proves:** 3.04 rebuilt as what it is: a Torque shell with the Graal game in one control. This is the 0.0.2 bar.

### Stage 5: 2D parity (0.0.3 for 3.04)

- Draw the game through the texture manager path, the 2.05 UDP channel between players (with the voice payload left out until decoded), GS1's 496 names, offline mode limits, the `GSERVL01` and `GR-V1.04` readers, `GWEBL001` cache, `license.graal` signature check (verification only).
- **Test:** two-player lab run against the real 3.04 on the same server, both directions.

## After 3.04

| Stage | Build | Adds | Proves |
|---|---|---|---|
| 6 | 3.153 | PPC DSO quirk (big-endian float tables), the `scripts2D/`, `scripts/`, `scriptsgui/` layout, `main2D.cs` with `MainMenuGui2D`, protocol 2.31 on the wire | The Torque shell is generic, not 3.04-shaped |
| 7 | 3.153 | Torque UDP `NetConnection`/`GameConnection` client: `Graal3D` protocol 19, class table, 12-bit ids, 14-bit lengths, `BigData…` and `Terrain…` events, mission phases (`network.md`, `wire-by-build.md`) against a lab Torque server built from `tools/tq.py` | The 3D link works end to end, with no 3D drawing yet |
| 8 | 3.153 | `GuiGraal3DCtrl(PlayGui)`, terrain, sky, DTS, the `moveMap2D` + `moveMap` dual binding, 2D overlay | A 3D server can be played; needs authored 3D content (none ships) |
| 9 | 4.04r2 | Delphi launcher + engine split with the draw-callback table; then `Graal3DEngine` as an alternate host | Era B's architecture |
| 10 | 4.20r8, 5.00r7 | 2D matrix, terrain height, `GameObject` creation callbacks | 2D content placed on 3D terrain |

## What happens to graal-delphi #95

It stays on hold. When stages 1–4 land, the 3.04 folder is rebuilt on the Torque layer and #95's wire work (already correct for 0.0.1) moves under it unchanged.
