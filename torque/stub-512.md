# Graal.exe 5.12, packer stub

Date: 2026-11-07. Static read of `Graal 5.12.exe` in the v5 export. Nothing was run. **[bin]**

## What the decompile is

The version resource strings are file version `5.1.2.0`, file description `Graal Online client`, product name `Graal`, original filename `Graal.exe`. **[bin]**

The recovered code is a packer stub. One `entry` runs into overlapping instructions and stops. There are no string literals. `VirtualAlloc` is not named. `GuiCanvas`, `SimObject`, `GameConnection`, `GameObject`, `ShapeBase`, `ActionMap`, `.dso`, `TAdventure`, `graal_set` and `Graal3DEngine` are absent. **[bin]**

This zip is the packed executable only. It does not contain `Graal3DEngine.dll`, so the 5.12 engine (one DLL, `GameObject`, protocol 24, no datablocks) is not remeasured here. **[bin]**
