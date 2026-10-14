# Config and input

Date: 2026-10-14

Derived from observed client behavior and the public config key list. No decompile material.

## graalconfig.txt keys

The client reads approximately 27 keys. Known ones include:

- Connection: `serveraddr`, `fixedport`, `fixedudpport`, `dontconnectlevels`, `dontloadlistheads`, `loadcolorsfromserver`
- UI: `sortplayersbyname`, `limitnicknames`, `nicknamelimit`, `gamemode`, `language`, `font`, `fontsize`
- Audio / input: `musicon`, `joystickon`, `nodirectinput`, `noudp`, `reversestereo`
- Compatibility: `nodecompressionerror`, `nohtmlimages`, `nohtmlinpms`, `nomassmessages`, `notoalls`, `saveimages`, `compabilitydraw`

A password mask literal exists in the binary and is not decrypted.

## Device path

Joystick support is present. The device is activated when a specific bit is set on an internal flag. The WinMM joystick id is stored separately from the main window object.

## Drop files

Dragging a file onto the client window is handled only when an internal flag is set.

- A single `.txt` extension spawns a script NPC.
- Three specific image extensions spawn an image NPC.
- Anything else is treated as a level load.

This matches the offline observation that local level files, GANIs, and NPCs can be loaded from a `levels/` tree.
