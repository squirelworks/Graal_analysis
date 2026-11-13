# older/ v3–v5 inventory (confirmed)

Date: 2026-11-08 · Tags: **[bin]**

Re-measured against the owner-held client images. Prefer dumps; skip live Themida when a sibling dump exists.

## Priority targets

| Pri | Path | Size | Packing | FileVersion | Company |
|---:|---|---:|---|---|---|
| 1 | `v5/…/unpacked_Graal_v5.31r4.exe` | 6,605,824 | Scylla `.SCY` | **5.314** | Linux Cyberjoueurs |
| 1 | `v5/…/unpacked_Graalsetup v5.30r3.exe` | 6,561,792 | Scylla `.SCY` | **5.303** | Linux Cyberjoueurs |
| 2 | `v5/…/Graal 5.0.0.7.exe` | 941,568 | clear | **5.0.0.7** | Linux Cyberjoueur |
| 2 | `…/GraalEngine.dll` | 2,867,200 | clear | — | early 5.x 2D |
| 2 | `…/Graal3DEngine.dll` | 1,331,200 | clear | — | early 5.x 3D |
| 3 | `v4/…/Graal 4.2.0.8.exe` + engines | 982,528+ | clear | **4.2.0.8** | Linux Cyberjoueur |
| 4 | `v3/…/graalexe 3.0.4` | 6,963,812 | ELF32 | 3.04 | Linux Torque |

## Deferred unless needed

| Path | FileVersion | Note |
|---|---|---|
| `Graal 5.12/Graal 5.12.exe` | 5.1.2.0 | multi-`.data` residue |
| `Graal 5.2.4r3/Graal 5.2.4.3.exe` | 5.243 | wrapped-looking |

## Late-5 vs early-6 signals (string presence)

| Signal | 5.303 / 5.314 | 6.037 | 6.113 |
|---|---|---|---|
| `quattro_lib` | yes | yes | yes |
| Classic `Illegal characters…` | yes | yes | yes |
| `<login-host>` + `14900` | **yes** | no (as ASCII) | no |
| `StartScript_Connector` / AES / `onSend*` | no | no | **yes** |
| Clear `account,alpha,ani…` registry | no | yes (96) | yes (95) |
