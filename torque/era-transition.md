# From a Torque monolith to Graal's own engine

Date: 2026-11-07. Nothing was run. This page names the four stages the clients pass through. The per-build readings stay in the notes it cites. Tags: **[bin]** a client binary, **[inf]** inferred from those readings.

`study-torque-clients.md` groups the same years into three eras (monolith, Delphi shell, own engine). The shell era covers two different Torque surfaces, so this note splits it into hybrid and residual. The gone cut stays at 5.24r3, where that study puts it, not at 6.x.

## The base is TGE 1.2, not a later Torque

3.04's own version call returns 1100, formatted `1.100`, compiled 3 January 2004, and the connect string is `Torque Game Engine Demo`. That is a TGE 1.1–1.2 era tree. **[bin]** (`engine-and-formats.md#which-torque`)

The 4.04r2 `Graal3DEngine.dll` matches open TGE 1.x on its out-of-band packets, packet header, Huffman table, rate limits, DTS, DIF and TER versions and class list, and it does not have TGE 1.4's lighting. It is the same TGE 1.2/1.3 line. **[bin][inf]** (`../graal3d/torque-engine-4x.md#torque-version`)

3.04 still compiles `ShapeBase`, `Player`, terrain and interiors. The 2D game is the console class `GuiGraalCtrl` inside that program, not a separate 2D engine. **[bin]** (`engine-304.md#the-split`)

A host taken from current Torque3D does not match these readings. The notes' base for the formats and the low-level net layer is open TGE 1.3 to 1.5, and that host still has to add Graal's class table, length prefixes and events. **[inf]** (`../graal3d/torque-engine-4x.md#torque-version`)

## Four stages

| Stage | Torque's job | Builds |
| --- | --- | --- |
| Monolith | Torque boots the process, runs the `.dso` menus and owns the canvas. Graal is `GuiGraalCtrl` plus the Graal TCP protocol. | 3.04 Linux, 3.153 Mac |
| Hybrid | A Delphi launcher draws. `GraalEngine.dll` keeps Torque GUI classes and runs the session. `Graal3DEngine.dll` is the Torque world, and only a 3D server loads it. | 4.04r2, unpacked 4.2.0.8, 4.20r6 Mac |
| Residual | Torque's sim and net code are still on the 3D side. The TGE game layer (`ShapeBase`, `Player`, datablocks) is gone. | 5.0.0.7, 5.12 |
| Gone | No Torque console, sim, net or 3D format. The program is Graal's own C++. | 5.24r3 and later, including unpacked 6.00 |

6.x does not put Torque back. **[bin]** (`engine-and-formats.md#which-torque`)

### Monolith (3.x)

One binary. Menus are TorqueScript `.dso`. Keys go through `ActionMap`. Stock TGE classes are compiled in, including the 3D game layer, whether or not a 3D script ships. **[bin]** (`study-torque-clients.md#1-the-short-answer`); **[bin]** (`engine-304.md#what-later-builds-drop`)

### Hybrid (4.x)

4.04r2's 3D DLL is near-stock TGE: `Player`, vehicles and datablocks. The 2D engine beside it keeps Torque base classes and does not keep the console. **[bin]** (`engine-and-formats.md#which-torque`)

Unpacked 4.2.0.8 is the same three files with a thinner surface. `GraalEngine.dll` uses `GuiCanvas` and `GuiControl`, and it has no `SimObject` and no `.dso`. The session object is `TAdventure`. `Graal3DEngine.dll` still has `SimObject`, `GameConnection`, `TerrainBlock` and interiors. Its player is `GameObject`. `ShapeBase` and Torque's `Player` do not occur in that DLL. **[bin]** (`4208-engine.md#what-is-absent`); **[bin]** (`4208-g3d.md#what-gameobject-is`)

4.20r6 Mac is one binary and already uses that `GameObject` model, with no datablocks. **[bin]** (`engine-and-formats.md#which-torque`)

### Residual (early 5.x)

5.0.0.7 keeps the 4.2.0.8 split. The 2D DLL still has no `SimObject` console. The 3D DLL still has `GameObject` and `GameConnection`, and its connect check accepts only protocol 24. **[bin]** (`5007-engine.md#no-simobject-and-no-dso`); **[bin]** (`5007-g3d.md#protocol`)

5.12 is one `Graal3DEngine.dll`. It keeps Torque's core (`SimObject`, `GameConnection`, ghosting, terrain, interiors, DTS) and drops the TGE game layer. **[bin]** (`engine-and-formats.md#which-torque`)

### Gone (5.24r3 and 6.x)

From 5.24r3 the executable has no `GameConnection`, `TerrainBlock`, interior code or DTS. **[bin]** (`engine-and-formats.md#which-torque`)

Unpacked Windows 6.00 is `quattro_lib`. Drawing is OpenGL. The session socket is `TSocket`. There is no Torque UDP connection and no `.dso`. `GuiGraalCtrl` and `GuiGraal3DCtrl` are playfield type names, not a Torque viewport. **[bin]** (`../client-internals/engine-600r2.md#no-torque-3d`); **[bin]** (`../client-internals/engine-600r2.md#how-the-program-is-split`)

## What a later host must not assume

- One Torque surface for 3.x through 6.x. 3.x calls the console and `.dso`. 4.x and early 5.x call a shrinking set. From 5.24r3 the Torque modules are gone.
- That `Graal3DEngine.dll` is one program. In 4.04r2 it is near-stock TGE. In 4.2.0.8 and 5.0.0.7 it is the `GameObject` world. Unpacked 6.00 has no such DLL.
- That 6.x is a thinner Torque client. It is `quattro_lib`, with `TSocket` instead of `GameConnection`.
