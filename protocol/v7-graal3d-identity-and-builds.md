# v7 Worlds: identity, token, six-build diff

Date: 2026-11-08

Targets: WorldsSetup64-**548, 610, 612, 613, 614, 71243** `unpacked_Graal3DEngine.dll` (+ GameAssembly inventory; the GameAssembly read is [v7-gameassembly-il2cpp.md](../client-internals/v7-gameassembly-il2cpp.md)). Tags: **[bin]** PE/string inventory · **[inf]** where token construction is absent.

No addresses in this file.

---

## 1. How the client reports itself **[bin]**

| Field | 548–614 | 71243 |
|---|---|---|
| Product brand | Toonslab Ltd / **Graal** | Graal (VERSIONINFO thinner / partially stripped in dump) |
| FileVersion / ProductVersion | **6.114** | not recovered as clear VERSIONINFO in the 71243 teardown |
| Export DLL name | `Graal3DEngineObfuscated.dll` | **`Graal3DEngineFlavor0.dll`** |
| Status lines | `Client-version: ` · `GRAALRELOADED-version: ` | same pair present |
| Unity host | GameAssembly IL2CPP (Unity ~2023.2 on 614) | GameAssembly present |
| PE stamp (614) | 2024-04-21 | 2024-10-15 |

Diag copy also emits OS/CPU/memory style lines next to those version prefixes (framing note).

---

## 2. Login token **[bin][inf]**

| Probe | Result |
|---|---|
| Cleartext eight-char `G3D…` / `GNW…` / `GNP…` | **absent** in v7-614 (and string inventories of the sibling builds) |
| `guest` account string | **present** |
| Token construction site | **not recovered** as a clear assembler of `G` + digits |

Reading: Worlds follows the **6.11 connector** pattern — version token / login fields come from **StartScript_Connector** (or scrambled blobs), not from a fixed eight-char literal baked like Linux 6.01/6.03. Do not invent a GNP/G3D string for this family. **[inf]**

---

## 3. Six-build diff (strings / exports) **[bin]**

| Build | Export name | FileVersion | Notes |
|---|---|---|---|
| 548 | Obfuscated | 6.114 | baseline Quattro + AES/RC4 exports |
| 610 | Obfuscated | 6.114 | same Quattro/crypto export set |
| 612 | Obfuscated | 6.114 | same |
| 613 | Obfuscated | 6.114 | same |
| 614 | Obfuscated | 6.114 | **current Ghidra project** |
| 71243 | **Flavor0** | (not in VERSIONINFO dump) | newer stamp; larger native image; same QuattroUpdate/FixedUpdate/InitializedReturn + AES/RC4 symbols |

**Quattro / crypto export set** (names shared across all six): `QuattroUpdate`, `QuattroFixedUpdate`, `QuattroInitializedReturn`, `DoRenderGraalControl`, `Arc4Process`/`Arc4SetKey`, `AesCbcEncrypt`/`AesCbcDecrypt`/`AesSetKey`/`AesSetIV`, plus CyaSSL and file-download helpers (`TFileDownload_*`, `SendFileToHttpRequest`, …).

No build in this set exposed a new cleartext login token or a different `Client-version` / `GRAALRELOADED-version` label spelling.

---

## 4. vs 6.0.3.7 / 6.1.1.3 **[bin][doc]**

| | 6.0.3.7 | 6.1.1.3 | v7 Worlds |
|---|---|---|---|
| Ship form | standalone exe | standalone exe | Unity plugin + GameAssembly |
| Version label | Graal 6.0x | Graal 6.11x | Graal **6.114** + GRAALRELOADED line |
| Login token cleartext | often yes (6.0x Linux) | connector-script | **not cleartext** |
| Connector scripts | no | yes | yes |
