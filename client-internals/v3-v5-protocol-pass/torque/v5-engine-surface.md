# v5 — engine surface

Date: 2026-11-08 · Tags: **[bin]**

## Late 5 is one exe · **high**

5.303 and 5.314 are unpacked monoliths. There is no sibling `GraalEngine.dll` in those folders.

| Signal | 5.303 / 5.314 |
|---|---|
| `quattro_lib` crypto paths (`sha1.c`, des/3des) | yes |
| `fmod` | yes |
| `Torque`, `SimObject`, `Con::` | **no** |
| `switchToOpenGL` / `switchToDirectX` script verbs | yes |
| `onReceiveUDPData`, `onBind`, `onConnect` | yes |
| Baked `<login-host>` and `14900` | yes |
| `StartScript_Connector` | **no** |

Rendering and netcode live in the exe. Torque is gone. UDP is a script socket (`onReceiveUDPData`), not a pref named `fixedudpport` (that string is absent here; it is present on 5.0.0.7).

## 5.0.0.7 is still split · **high**

| Module | What the strings show |
|---|---|
| `Graal 5.0.0.7.exe` | Host. `graal://` / `graal3://`, `setGraalProtocol`, `fixedudpport`, `noudp`, `14899`, `guest`. No `14900`, no `loginserver` |
| `GraalEngine.dll` | Game + script + `hcrypt` / HVDI, `Illegal characters`, `setplayerprop`. No `quattro_lib` |
| `Graal3DEngine.dll` | `SimObject` (Torque residual). Also `showimg`. No `Con::` |

Same cut as v4: 2D path in the engine DLL, 3D plugin still Torque-derived. Late 5 drops that split and the Torque token.

## Cipher names · **medium**

Late 5 names DES/3des under `quattro_lib` and lists `RC4` inside a crypto catalog. It does not export `Arc4Process` and does not contain the 6.113 `DOQLHRbY` selector. 5.0.0.7’s `hcrypt` / HVDI strings sit on `GraalEngine.dll`, matching the v4 voice path rather than the game-line cipher.

## vs v4 and v6 · **high**

| | 5.0.0.7 | Late 5 | v6.113 |
|---|---|---|---|
| Process shape | exe + two DLLs | one exe | one exe |
| Torque `SimObject` | 3D DLL only | no | no |
| `quattro_lib` | no | yes | yes |
| Baked login `:14900` | no | yes | no |
| `onSend*` | no | no | yes |
