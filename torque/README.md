# Graal on the Torque Game Engine (3.x to 5.12)

Date: 2026-10-30

From 2004 to 2007 the Graal client was built on GarageGames' **Torque Game Engine (TGE)**. Torque supplied the console, the TorqueScript VM, the GUI, the resource manager, the renderer, and (for 3D servers) the UDP netcode. Graal's own 2D game, the GS1/GS2 interpreters and the Graal TCP protocol were native C++ on top of it. This folder is the cross-version picture, written so that a later Seihai suite (launcher + legacy 2D client + Torque client) can be planned from it.

Tags: **[bin]** read from a client binary · **[file]** read from shipped data · **[run]** seen while running a real client under Wine · **[inf]** inferred.

- [network.md](network.md): how a client joins a 3D server, the Torque UDP handshake byte by byte (run live end to end against the real 5.12 client), the connect request in each version, 5.12's class-name table in the accept, the mission download phases.
- [scripting.md](scripting.md): the compiled TorqueScript (`.dso` v33) format with Graal's opcode table, the decoder in `tools/`, and what the 3.153 scripts do.
- [wire-by-build.md](wire-by-build.md): which builds are Torque, the handshake and class table per build (3.04, 3.153, 4.04r2, 4.20r6, 5.12), the networked class sets, the 5.12 game packets (no moves, client-reported position) and the 5.12 `GameObject` update.
- [engine-and-formats.md](engine-and-formats.md): engine version, classes per build, 3D resource formats (DTS, DIF, TER, 3DS), terrain streaming, rendering devices.
- `tools/`: `dsodis.py` / `dsodec.py` (DSO disassembler and decompiler), `tbits.py` (Torque bit stream and Huffman strings), `tq.py` (a minimal Torque server that completes the 5.12 handshake), `conn.c` (the injector that makes a real 5.12 client join a 3D server and drives its frames under Wine).

Related notes elsewhere: `protocol/v3x-clients.md` (3.04 / 3.153 Graal TCP side), `protocol/v4x-clients.md` and `graal3d/torque-engine-4x.md` (4.x, including the 4.04r2 `Graal3DEngine.dll` read: BigData events, commands, protocol 19), `protocol/v5x-clients.md` (5.x TCP side), `graal3d/` (the unrelated February 2000 DirectX Graal3D).

## Lineage at a glance

| Build | Date | Shape | Torque part | 3D world | Game string / protocol | Script language for menus |
|---|---|---|---|---|---|---|
| 3.04 Linux | Jan 2004 | one C++ binary (SDL, OpenAL) | full TGE, `getVersionNumber` = 1100 ("1.100"), built "Jan 3 2004 22:32:08" | TGE classes present, no 3D scripts shipped | `Torque Game Engine Demo`, 9 / 9 | TorqueScript `.dso` |
| 3.153 Mac | Feb 2005 | one C++ binary (Carbon, PPC) | full TGE, with Graal's net-layer changes (class table, 12-bit class ids, 14-bit lengths, BigData and terrain events) | stock TGE world + `main3D.cs` client scripts | `Graal3D`, 19 / 19 | TorqueScript `.dso` |
| 4.04r2 Win | Mar 2006 | Delphi launcher + `GraalEngine.dll` (2D) + `Graal3DEngine.dll` (3D plug-in) | 2D engine keeps Torque base classes only; the 3D DLL is near-stock TGE (Player, vehicles, datablocks, fxFoliage) | stock TGE with datablocks | `Graal3D`, 19 (from the v4 thread) | GS2 / native |
| 4.20r6 Mac | Sep 2006 | one C++ binary (PPC) | Torque core + netcode, Graal game layer | `GameObject` model as in 5.12, no datablocks | `Graal3D`, 21 / 21 | GS2 / native |
| 5.12 Win | Oct 2007 | Delphi launcher + one engine DLL, still named `Graal3DEngine.dll` | Torque core + netcode, but the game layer is Graal's own | `GameObject` + `GameShapeDTS/DIF/3DS/FT`, no datablocks, no `Player`/`ShapeBase` | `Graal3D`, 24 / 24 | GS2 / native |
| 5.24r3 and later | 2010+ | engine linked into `Graal.exe` | Torque 3D gone (only a leftover `GuiGraal3DCtrl` name) | none | n/a | GS2 |
| 6.x | 2010–2014 | native C++ per platform | none (see `protocol/v6x-clients.md`) | none | n/a | GS2 |

All rows are **[bin]**, except the 3.153 script column (**[file]**). The 3.153 and 4.20r6 rows, and the per-build wire details, are in [wire-by-build.md](wire-by-build.md).

## What a Seihai suite would need, in order

1. **A launcher** that offers both clients. Graal itself did this from 4.x: the launcher shows the server list, and a server whose listed name starts with `"3 "` is a 3D server.
2. **A 3D server pair.** Every Graal3D server is a normal Graal TCP gserver on its listed port **plus** a Torque UDP server on **port + 1**. The TCP side carries the login, chat, GS2 and the player; the UDP side carries the 3D world. **[bin][run]**
3. **The Torque handshake**, which is small, fully known, and tested live against the real 5.12 client (see `network.md`). The class CRC that stock Torque checks is a constant `0xFFFFFFFF` in 5.12. Instead, the server's accept carries a table of class names and the ids it will use for them, so a Seihai server picks its own class ids and only needs Graal's class names. **[bin][run]**
4. **The 3D world.** Two choices: rebuild the 4.04r2 world (stock TGE datablocks, so an open TGE 1.x / Torque3D code base gets most of the way), or the 5.12 world (Graal's own `GameObject` model, scripted from GS2). 5.12 is the last and most Graal-specific; 4.04r2 is the easiest to reproduce. No 3D server software or 3D level data is in the archives yet, so either way the content must be made or found.
5. **Per-version profiles.** A profile picks the game string and protocol (`Torque Game Engine Demo`/9, `Graal3D`/19, `Graal3D`/21, `Graal3D`/24), whether the accept carries the class table (every build from 3.153 on) and with how many types (3 up to 4.04r2, 2 from 4.20r6), the mission phases (3 in TGE builds, 2 in 5.12), and whether menus are TorqueScript (3.x) or GS2 (4.x+).

## What is in the project folder (not in this repo)

`graal-decompile/torque/` in the project files holds the extracted 3.153 Mac and 3.04 Linux trees, all 44 decompiled 3.153 scripts (`dec3153/`), the 5.12 `Graal3DEngine.dll` Ghidra export and string/RTTI dumps (`g3de/`), and the Wine lab (`wine-3d-lab/`) with the live capture.
