# v4 builds (inventory)

Date: 2026-11-08 · Tags: **[bin]**

Primary set (Unpacked tree):

| File | Size | Role |
|---|---:|---|
| `Graal 4.2.0.8.exe` | 982,528 | Borland/Delphi host UI; loads engines |
| `GraalEngine.dll` | 2,908,160 | 2D/net/script/packages — **primary protocol surface** |
| `Graal3DEngine.dll` | 1,417,216 | 3D / Torque residual (`SimObject`, `DTS`, `NetConnection`) |
| `fmod.dll` | 162,816 | UPX audio |
| `freetype6.dll` / `zlib1.dll` | — | support |

VERSIONINFO on exe: FileVersion **4.2.0.8**, Company **Linux Cyberjoueur**, Product **Graal**, description **Graal Online client**.

Also in `older/v4/`: installers (Linux/Mac/Win); **Packet Logger** 7z (`g4_PackLog.dll` + `main.cpp` proving `id = first_byte - 32` on newline lines). Prefer Unpacked tree for analysis; use logger source for framing proof.

Root `Graal 4.04r2/` Win exe deferred — 4.2.0.8 set is sufficient this pass.
