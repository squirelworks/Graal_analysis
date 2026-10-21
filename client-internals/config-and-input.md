# Config and input

Date: 2026-10-14

Derived from observed client behavior, the public config key list, and format notes. No decompile material.

## graalconfig.txt

> **Superseded** by `graalconfig-reference.md`, which lists every key 2.05 reads and writes. `serveraddr`, `loadcolorsfromserver` and `gamemode` below are not read by 2.05. The "password mask literal" is the fixed DES key for saved passwords (`saved-passwords.md`).

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

## Update 2026-10-21: 2.05 vs 2.22 graalconfig

Compared the 2.22 `graalconfig.txt` (user's Drive, 86 keys) with the 2.05 string table. **[2.05][doc]**

- **Present in 2.05:** `compabilitydraw`, `dontconnectlevels`, `dontloadlistheads`, `dontsavepasswords`, `dontsavepms`, `dontusedirectx7`, `fixedport`, `fixedudpport`, `font`, `fontsize`, `fullscreenmode`, `head`, `joyselected`, `joystickon`, `language`, `limitnicknames`, `nicknamelimit`, `nodecompressionerror`, `nodirectinput`, `nohtmlimages`, `nohtmlinpms`, `nomassmessages`, `notoalls`, `noudp`, `reversestereo`, `saveimages`, `sortplayersbyname`, `waitvertical`, `musicon`. That is about 29 keys, which fits the "~27 keys" estimate above.
- **Key bindings:** the only related 2.05 string is the bare prefix `keyset_`, so 2.05 probably builds `keyset_<action>_key0..2` and `keyset_<action>_joystickbutton` names at runtime [inf]. The actions in 2.22 are up, left, down, right, item, attack, action, map, switchtochat, itemlist, and pause, with defaults arrows/IJKL, D, S/space, A, M, Tab, Q, and P.
- **2.22-only** (absent in 2.05): `automapping`, the `micro*`/`voice*` voice-chat keys, `midivolume`/`mp3volume`/`radiovolume`/`sfxvolume`, `startinfullscreen`, `quickplayerworlds`.
- `fixedudpport` defaults to 14899 and `noudp=true` in 2.22. In 2.05 the UDP channel is a peer-to-peer channel between players; see `protocol/udp-p2p.md`.
