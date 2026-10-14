# Config and input

Date: 2026-10-14

Derived from observed client behavior, the public config key list, and format notes. No decompile material.

## graalconfig.txt

The client reads approximately 27 keys from `graalconfig.txt`. Known keys fall into four groups:

**Connection**
- `serveraddr` — host override
- `fixedport` — TCP port override
- `fixedudpport` — UDP port override
- `dontconnectlevels` — skip automatic level connect
- `dontloadlistheads` — skip list header images
- `loadcolorsfromserver` — pull color table from server

**UI**
- `sortplayersbyname`
- `limitnicknames` / `nicknamelimit`
- `gamemode`
- `language`
- `font` / `fontsize`

**Audio and input**
- `musicon`
- `joystickon`
- `nodirectinput`
- `noudp`
- `reversestereo`

**Compatibility**
- `nodecompressionerror`
- `nohtmlimages` / `nohtmlinpms`
- `nomassmessages` / `notoalls`
- `saveimages`
- `compabilitydraw` — toggles a DirectDraw compatibility path

A password mask literal exists in the binary and is not decrypted. It is used only for display.

## Device path

Joystick support is present. The device is activated when a specific internal bit is set. The WinMM joystick identifier is stored separately from the main window object. An offline session that does not need joystick input can ignore this path.

## Drop files

Dragging a file onto the client window is handled only when an internal flag is set (the same flag that enables the editor drop target).

- A single `.txt` extension spawns a script NPC.
- Three specific image extensions (`.gif`, `.png`, `.mng`) spawn an image NPC.
- Anything else is treated as a level load.

This matches the offline observation that local level files, GANIs, and NPCs can be loaded from a `levels/` tree. An offline session that already accepts a dropped `.nw` or `.graal` file is exercising the same path.

## Offline implication

None of the config keys are required for the offline slice. The drop-files behavior is the only part that intersects with current offline work: a dropped level file should load, and a dropped image or script should spawn the corresponding NPC. That is already the expected next step after collision and CmdCall.
