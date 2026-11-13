# v4 — engine surface (Torque vs custom)

Date: 2026-11-08 · Tags: **[bin]**

## Split · **high**

| Module | Engine signal |
|---|---|
| `Graal 4.2.0.8.exe` | Borland/Delphi host; DirectDraw/Direct3D/DirectInput; loads DLLs |
| `GraalEngine.dll` | Custom C++/VCL-ish net + GS1 script + packages; **no** `Torque`/`Con::`/`quattro_lib` |
| `Graal3DEngine.dll` | **Torque residual**: `SimObject`, `DTS` / `GameShapeDTS`, `BitStream`, `NetConnection`, `TSimObjectProperty` |

**Cut reading:** 2D online path is already the custom Engine DLL. 3D mode still links a Torque-derived plugin. Full Torque host (as on Linux 3.04) is **gone** from the Win 4.2 2D stack.

## UDP · **high** (optional)

Prefs `noudp`, `fixedudpport` (default **14899**), UI warnings that UDP may fail — peer/data-package UDP exists but is disableable. Not a mandatory Quattro `onReceiveUDPData` script hook naming (that string appears later).

## Voice · **high**

HVDI encode/decode (+ optional hcrypt) lives on `GraalEngine.dll` — audio path, not Torque and not PLI/PLO.

## vs late-5 / v6 · **high**

Late-5+ ship as Quattro monolith (`quattro_lib`). v4 keeps split engines + Torque 3D DLL island. Game PL is classic `id+0x20`/newline without FE remapper.
