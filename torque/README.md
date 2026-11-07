# Graal on the Torque Game Engine (3.x to 5.12)

Date: 2026-10-30

From 2004 to 2007 the Graal client was built on GarageGames' **Torque Game Engine (TGE)**. Torque supplied the console, the TorqueScript VM, the GUI, the resource manager, the renderer, and (for 3D servers) the UDP netcode. Graal's own 2D game, the GS1/GS2 interpreters and the Graal TCP protocol were native C++ on top of it. This folder is the cross-version picture, written so that a later Seihai suite (launcher + legacy 2D client + Torque client) can be planned from it.

Tags: **[bin]** read from a client binary · **[file]** read from shipped data · **[run]** seen while running a real client under Wine · **[inf]** inferred.

- [network.md](network.md): how a client joins a 3D server, the Torque UDP handshake byte by byte (run live end to end against the real 5.12 client), the connect request in each version, 5.12's class-name table in the accept, the mission download phases.
- [scripting.md](scripting.md): the compiled TorqueScript (`.dso` v33) format with Graal's opcode table, the decoder in `tools/`, and what the 3.153 scripts do.
- [wire-by-build.md](wire-by-build.md): which builds are Torque, the handshake and class table per build (3.04, 3.153, 4.04r2, 4.20r6, 5.12), the networked class sets, the 5.12 game packets (no moves, client-reported position) and the 5.12 `GameObject` update.
- [engine-and-formats.md](engine-and-formats.md): engine version, classes per build, 3D resource formats (DTS, DIF, TER, 3DS), terrain streaming, rendering devices.
- [engine-304.md](engine-304.md): the 3.04 Linux binary read as an engine. Stock TGE is still compiled in, Graal's game is `GuiGraalCtrl`, and later builds drop the TGE game layer from this superset.
- [4208-launcher.md](4208-launcher.md), [4208-engine.md](4208-engine.md), [4208-g3d.md](4208-g3d.md): the unpacked Windows 4.2.0.8 launcher, `GraalEngine.dll` and `Graal3DEngine.dll`, read for behaviour. The launcher draws through 94 host slots until a 3D start replaces the draw slots; the engine runs `TAdventure` and GS2 with no `SimObject` console; the 3D DLL's `GameObject` is a `SceneObject`.
- [5007-launcher.md](5007-launcher.md), [5007-engine.md](5007-engine.md), [5007-g3d.md](5007-g3d.md): file version 5.0.0.7 read for behaviour. The Delphi launcher's 95 setters and when it loads each DLL, `TAdventure` and the script space inside `GraalEngine.dll`, and `GameObject`, the two mission phases, terrain-chunk files and the protocol-24 check inside `Graal3DEngine.dll`.
- [skipped-v4-read.md](skipped-v4-read.md): the two skipped Windows exe listings (labeled 4.04r2 and 4.20r8) are one file, and that file is the Thinstall outer loader. The wrapped client is not in the listing.
- [skipped-v5-read.md](skipped-v5-read.md): packed 5.12 still names its Delphi forms; the packed 5.2.4.3 and 5.24r4 exes do not; `fmod.dll` beside 5.0.0.7 is the UPX FMOD listing, same bytes as the 4.2.0.8 copy.
- [study-torque-clients.md](study-torque-clients.md): what each Torque-era client really is (Torque monolith 3.x, Delphi shell + C++ engine 4.x–5.12, Graal's own engine from 5.24r3), a marker scan of 17 binaries from 3.04 to 6.11, the 3.04 shipped files and formats, the native surface the 3.04 scripts need, the 4.x/5.00 draw-callback bridge that puts 2D content into the Torque world, and what the 2D rebuild lacks per era.
- v5 export, static read 2026-11-07, nothing run: [launcher-5007.md](launcher-5007.md) (Delphi `Graal.exe` 5.0.0.7), [engine-5007.md](engine-5007.md) (`GraalEngine.dll`, the `graal_set` API and Graal's game), [g3d-5007.md](g3d-5007.md) (`Graal3DEngine.dll`, GameObject-era Torque), [freetype6-5007.md](freetype6-5007.md) and [stub-fmod-5007.md](stub-fmod-5007.md) (the two libraries beside that client), [stub-512.md](stub-512.md), [stub-5243.md](stub-5243.md) and [stub-524r4.md](stub-524r4.md) (packer stubs, file versions `5.1.2.0`, `5.243`, `5.244`), [engine-530r3.md](engine-530r3.md) and [engine-531r4.md](engine-531r4.md) (unpacked single exes, file versions `5.303` and `5.314`).
- [skipped-version-stamps.md](skipped-version-stamps.md): version resources still present on the packer-stub exports the engine reads left unread (the identical 4.04r2 and 4.20r8 exe uploads, 5.12, 5.2.4.3, 5.24r4, fmod, and the packed 6.0.3.7 and 6.1.1.3 exes).
- [rebuild-plan-3.04.md](rebuild-plan-3.04.md): a staged plan for a Torque-faithful rebuild starting with 3.04, the test that ends each stage, and what "0.0.2" means for each era.
- `tools/`: `dsodis.py` / `dsodec.py` (DSO disassembler and decompiler), `tbits.py` (Torque bit stream and Huffman strings), `tq.py` (a minimal Torque server that completes the 5.12 handshake), `conn.c` (the injector that makes a real 5.12 client join a 3D server and drives its frames under Wine).

Related notes elsewhere: `protocol/v3x-clients.md` (3.04 / 3.153 Graal TCP side), `protocol/v4x-clients.md` and `graal3d/torque-engine-4x.md` (4.x, including the 4.04r2 `Graal3DEngine.dll` read: BigData events, commands, protocol 19), `protocol/v5x-clients.md` (5.x TCP side), `client-internals/skipped-v6-read.md` (the packed 6.037 and 6.113 listings: a `QPlay.exe` export directory, no Torque), `graal3d/` (the unrelated February 2000 DirectX Graal3D).

## Lineage at a glance

| Build | Date | Shape | Torque part | 3D world | Game string / protocol | Script language for menus |
|---|---|---|---|---|---|---|
| 3.04 Linux | Jan 2004 | one C++ binary (SDL, OpenAL) | full TGE, `getVersionNumber` = 1100 ("1.100"), built "Jan 3 2004 22:32:08" | TGE classes present, no 3D scripts shipped | `Torque Game Engine Demo`, 9 / 9 | TorqueScript `.dso` |
| 3.153 Mac | Feb 2005 | one C++ binary (Carbon, PPC) | full TGE, with Graal's net-layer changes (class table, 12-bit class ids, 14-bit lengths, BigData and terrain events) | stock TGE world + `main3D.cs` client scripts | `Graal3D`, 19 / 19 | TorqueScript `.dso` |
| 4.04r2 Win | Mar 2006 | Delphi launcher + `GraalEngine.dll` (2D) + `Graal3DEngine.dll` (3D plug-in) | 2D engine keeps Torque base classes only; the 3D DLL is near-stock TGE (Player, vehicles, datablocks, fxFoliage) | stock TGE with datablocks | `Graal3D`, 19 (from the v4 thread) | GS2 / native |
| 4.20r6 Mac | Sep 2006 | one C++ binary (PPC) | Torque core + netcode, Graal game layer | `GameObject` model as in 5.12, no datablocks | `Graal3D`, 21 / 21 | GS2 / native |
| 5.12 Win | Oct 2007 | Delphi launcher + one engine DLL, still named `Graal3DEngine.dll` | Torque core + netcode, but the game layer is Graal's own | `GameObject` + `GameShapeDTS/DIF/3DS/FT`, no datablocks, no `Player`/`ShapeBase` | `Graal3D`, 24 / 24 | GS2 / native |
| 5.24r3 and later | 2010+ | engine linked into `Graal.exe` | Torque 3D gone (only a leftover `GuiGraal3DCtrl` name) | none | n/a | GS2 |
| 6.x | 2010–2014 | native C++ per platform (`quattro_lib` on Windows 6.00) | no Torque 3D; GS2 keeps Torque control names (`client-internals/engine-600r2.md`) | none | n/a | GS2 |

All rows are **[bin]**, except the 3.153 script column (**[file]**). The 3.153 and 4.20r6 rows, and the per-build wire details, are in [wire-by-build.md](wire-by-build.md).

The 2026-11-07 v5 export agrees with the 5.00 split (Delphi launcher, `GraalEngine.dll`, `Graal3DEngine.dll`) and with 5.12's shape only as far as the packed exe: that zip has no engine DLL, file version `5.1.2.0`, and the decompile is a stub. The 5.00 3D DLL in the export is already the `GameObject` era (two mission phases, terrain chunks, a protocol check that passes only 24) and it does contain interior read strings. `ShapeBase` and a datablock phase are absent. The unpacked 5.30r3 and 5.31r4 exes are one binary each (`quattro_lib`, file versions `5.303` and `5.314`) with the GUI names left and no `graal_set`, `SimObject` or `GameConnection`. **[bin]** ([g3d-5007.md](g3d-5007.md), [engine-531r4.md](engine-531r4.md))

## What a Seihai suite would need, in order

1. **A launcher** that offers both clients. Graal itself did this from 4.x: the launcher shows the server list, and a server whose listed name starts with `"3 "` is a 3D server.
2. **A 3D server pair.** Every Graal3D server is a normal Graal TCP gserver on its listed port **plus** a Torque UDP server on **port + 1**. The TCP side carries the login, chat, GS2 and the player; the UDP side carries the 3D world. **[bin][run]**
3. **The Torque handshake**, which is small, fully known, and tested live against the real 5.12 client (see `network.md`). The class CRC that stock Torque checks is a constant `0xFFFFFFFF` in 5.12. Instead, the server's accept carries a table of class names and the ids it will use for them, so a Seihai server picks its own class ids and only needs Graal's class names. **[bin][run]**
4. **The 3D world.** Two choices: rebuild the 4.04r2 world (stock TGE datablocks, so an open TGE 1.x / Torque3D code base gets most of the way), or the 5.12 world (Graal's own `GameObject` model, scripted from GS2). 5.12 is the last and most Graal-specific; 4.04r2 is the easiest to reproduce. No 3D server software or 3D level data is in the archives yet, so either way the content must be made or found.
5. **Per-version profiles.** A profile picks the game string and protocol (`Torque Game Engine Demo`/9, `Graal3D`/19, `Graal3D`/21, `Graal3D`/24), whether the accept carries the class table (every build from 3.153 on) and with how many types (3 up to 4.04r2, 2 from 4.20r6), the mission phases (3 in TGE builds, 2 in 5.12), and whether menus are TorqueScript (3.x) or GS2 (4.x+).

## What is in the project folder (not in this repo)

`graal-decompile/torque/` in the project files holds the extracted 3.153 Mac and 3.04 Linux trees, all 44 decompiled 3.153 scripts (`dec3153/`), the 5.12 `Graal3DEngine.dll` Ghidra export and string/RTTI dumps (`g3de/`), and the Wine lab (`wine-3d-lab/`) with the live capture.

## Finding the addresses for `conn.c`

`conn.c` needs two addresses in `Graal3DEngine.dll` (5.12), passed as hex in the environment of the injected client. Addresses are not kept in the repo; find them on your own copy. If either one is unset, that step is skipped.

1. **`CON_PRINTF_HEX`, Torque's `Con::printf`.** Load the DLL in a disassembler and find the console strings the handshake logs, for example `Sending Connect challenge Request` or `Issuing Disconnect packet.` (the list is in `network.md`). Follow a reference to one of them: the call it is passed to, as the format argument, is `Con::printf`. Most of the engine's console strings go through that same function, which confirms it.
2. **`FLAG3D_HEX`, the 3D mode byte.** Start at the exported `connectToGraalServer`. Follow the branch taken when the server name starts with `"3 "` (it strips the prefix, remembers the listed port + 1, then asks the launcher through `graal_setStartGraal3D`; see `network.md`). On that branch, the global byte that is set non-zero before the launcher callbacks run is the flag (the exact value was not recorded) **[inf]**.
3. **Check for relocation.** Both addresses assume the DLL's preferred base. `conn.c` logs the engine module's base on its `=== conn4` line. If that base differs from the one your disassembler shows, add the difference to both values.
4. **Confirm.** Run `conn.c` against a `"3 "` name and check `conn.log`. It should contain `con:` lines with the handshake strings and a non-zero `flag3d=`. With a plain 2D name, it should read 0 **[inf]**.

