# v7 Worlds: Unity / GameAssembly ↔ Graal3DEngine bridge

Date: 2026-11-08

Target: WorldsSetup64-614 (same export set on 548–613; 71243 renames the DLL to Flavor0). Tags: **[bin]**

No addresses in this file.

---

## 1. Split of responsibility

| Layer | DLL | Role |
|---|---|---|
| C# / IL2CPP | `GameAssembly.dll` | Unity gameplay, Quattro C# types, UI, asset bundles |
| Native Graal | `Graal3DEngine*.dll` | Classic Graal netcode, remapper, props, GRESCR/GS2 VM, ciphers, file cache |

GameAssembly does **not** reimplement PLI/PLO. It calls into the native plugin through exported C entry points and Quattro frame hooks.

---

## 2. Exports GameAssembly-facing (native) **[bin]**

### Frame / lifecycle

| Export | Role |
|---|---|
| `QuattroUpdate` | per-frame tick into native |
| `QuattroFixedUpdate` | fixed-step tick |
| `QuattroInitializedReturn` | init handshake / ready |
| `Init` | plugin init |
| `Update3D` | 3D path update |

### Render / mesh

| Export | Role |
|---|---|
| `DoRenderGraalControl` | Graal control render |
| `GetRenderEventFunc` / `…WithMeshPointer` | render-event callbacks |
| `StartRenderEvent` / `OnRenderEventIsDone` | render-event lifecycle |
| `UpdateMeshFromCpp` / `SendTileMeshUvsPointer` / `ResetUvsUpdated` | mesh/UV sync from C++ |
| `FillPointerWithTexture` / `ForceLoadTexture` / `GetTextureSize` | texture bridge |

### Files / HTTP

| Export | Role |
|---|---|
| `TFileDownload_CanDownload` / `_Download` / `_Update` | native download object |
| `SendFileToCpp` / `SendFileToHttpRequest` | push file bytes / HTTP |
| `AskFileExists` / `FillPointerWithFile` | file probes |

### Player / level hooks

| Export | Role |
|---|---|
| `SetPlayerPosition` | C# → native position |
| `SendPlayerCurModified` | dirty player cursor/state |
| `OnLevel3DEnter` / `OnLevel3DLoaded` | 3D level lifecycle |

### Crypto (also used by Graal framing)

| Export | Role |
|---|---|
| `Arc4Process` / `Arc4SetKey` | RC4 |
| `AesCbcEncrypt` / `AesCbcDecrypt` / `AesSetKey` / `AesSetIV` | AES-CBC |
| CyaSSL_* family | TLS |

LiteNetLib / MLAPI **native invoke** stubs also appear in the export list — those serve Unity net plugins, not the classic Graal TCP remapper.

---

## 3. What stays in C++ vs C#

| In native Graal3DEngine | Forwarded / owned by C# |
|---|---|
| Socket framing, remapper, PLI/PLO natives | Quattro UI, tiles, cameras, tweens |
| Property encode/decode, GRESCR/GS2 VM | AssetBundle download UX |
| RC4/AES install for Graal streams | Xsolla / PlayMaker / Cinemachine |
| `.code` / `.gupd` / weblevel cache magics | IL2CPP game logic |

Deprecated Quattro EventManager copy still mentions sending events “back to graalscript” — native script remains authoritative for weapon/NPC GS2. **[bin]**

---

## 4. Build note

548–614: export DLL `Graal3DEngineObfuscated.dll`.  
71243: `Graal3DEngineFlavor0.dll` — same Quattro/crypto/file-download export **names**.
