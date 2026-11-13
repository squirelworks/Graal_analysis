# Unpacked and dumped client images: which note covers each

Date: 2026-11-13. Static inventory only. Nothing was run. Tags: **[bin]**.

The owner-held client archive holds packed releases and, beside several of them, unpacked or dumped images (Themida removed, or an installed folder with the real launcher and engine DLLs). This index lists every such image found in a full recursive sweep of the archive, what it is, and which note in this repo analyses it. Paths and digests stay owner-held.

**Plaintext tokens.** **[bin]** No image in the sweep holds a clear eight-character login token from [version-token-catalogue.md](version-token-catalogue.md) (`G3D…`, `GNW…`, `GNP…`, `G2N…`, `GSERV…`, `GR3DV…`). That matches the token notes: 4.x–6.x build their tokens at run time, and v7 sends none.

## Windows 4.x–6.x

| Image | File version | PE stamp | Packer residue | Code present | Covered by |
|---|---|---|---|---|---|
| 4.20r8 installed folder: `Graal4.exe` | 4.2.0.8 | Delphi default | none (Delphi `CODE`/`DATA`/`BSS`) | yes | [launchers-420r8-500r7-512.md](launchers-420r8-500r7-512.md), [torque/4208-launcher.md](../torque/4208-launcher.md) |
| 4.20r8 `GraalEngine.dll` | – | 2007-01-12 | none | yes | [torque/engine-4208.md](../torque/engine-4208.md), [torque/4208-engine.md](../torque/4208-engine.md) |
| 4.20r8 `Graal3DEngine.dll` | – | 2007-01-12 | none | yes | [torque/4208-g3d.md](../torque/4208-g3d.md), [windows-404r2-500r7-static-2026-11-09.md](windows-404r2-500r7-static-2026-11-09.md) |
| 5.00r7 "CRC patch" folder: `Graal.exe` | 5.0.0.7 | Delphi default | none | yes | [torque/launcher-5007.md](../torque/launcher-5007.md), [launchers-420r8-500r7-512.md](launchers-420r8-500r7-512.md) |
| 5.00r7 `GraalEngine.dll` (patched) | – | 2007-07-16 | none | yes | [torque/engine-5007.md](../torque/engine-5007.md), [protocol/v5x-clients.md](../protocol/v5x-clients.md) (the 8-byte licence-loader patch) |
| 5.00r7 `Graal3DEngine.dll` | – | 2007-07-16 | none | yes | [torque/g3d-5007.md](../torque/g3d-5007.md) |
| 5.00r7 `Graal5 CRC Patch.exe` | – | Delphi default | UPX (old) | packed | [protocol/v5x-clients.md](../protocol/v5x-clients.md); not unpacked, its effect is read from the byte diff |
| 5.30r3 `unpacked_Graalsetup.exe` | 5.303 | 2010-10-18 | Themida names + `.SCY` | yes | [torque/engine-530r3.md](../torque/engine-530r3.md) |
| 6.00r2 `unpacked_GraalSetup` | 6.002 | 2011-06-12 | Themida names + `.SCY` | yes | [engine-600r2.md](engine-600r2.md) |
| 6.00r4 `unpacked_GraalSetup` | 6.004 | 2011-06-26 | Themida names + `.SCY` | yes | [engine-600r4.md](engine-600r4.md) |
| `unpacked_Graal 6.0.3.7.exe` | 6.037 | 2012-11-16 | Themida names + `.SCY` | yes | [unpacked-6037.md](unpacked-6037.md) |
| `unpacked_Graal 6.1.1.3.exe` | 6.113 | 2014-08-08 | Themida names + `.SCY` | yes | [unpacked-6113.md](unpacked-6113.md), [engine-6113.md](engine-6113.md) |

The unpacked 5.30r3 and 6.x images keep their packed siblings' section names (blank, two random eight-letter names, `.idata`) and add `.text` and `.SCY`, as [themida-pack.md](themida-pack.md) describes. Each unpacked image's PE stamp and version equal its packed original's. **[bin]**

Packed originals beside them (not unpacked in the archive): 4.04r2/4.20r8 Windows setup (one stub, shared by both labels), 5.12, 5.24r3 and 5.24r4 (virtualising wrapper), 5.31r4 (Themida; no unpacked image in this archive folder; [torque/engine-531r4.md](../torque/engine-531r4.md) reads an unpacked 5.31r4 from a separate decompile export), and the 4.x/5.x Linux installers. **[bin]**

## v7 Worlds (Unity)

| Image | Builds | Code present | Covered by |
|---|---|---|---|
| `unpacked_Graal3DEngine.dll` | 548, 610, 612, 613, 614, 71243 | yes | `protocol/v7-graal3d-*.md`, [v7-graal3d-unity-bridge.md](v7-graal3d-unity-bridge.md) |
| `unpacked_GameAssembly.dll` (IL2CPP) | 548, 610, 612, 613, 614, 71243 | yes | [v7-gameassembly-il2cpp.md](v7-gameassembly-il2cpp.md) (new: before this, inventory only) |

Both v7 dumps keep `.themida` and `.boot` as dead sections and add `.text` and `.SCY`. The installed 2026 Worlds client (Unity 6000.0) is packed only. **[bin]**

## Result of the sweep

Every unpacked Windows 4.x–6.x image in the archive already had a full note. The only images with no analysis were the six v7 `GameAssembly.dll` dumps, now covered.
