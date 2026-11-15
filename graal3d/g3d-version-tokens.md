# G3D version tokens vs the 2000 Graal3D product

Date: 2026-11-16

Two different things share the letters “G3D”. This note keeps them apart and points at the held token catalogue and the Torque 3D hand-off notes. No new captures; own notes only. Tags: **[bin]** **[cap]** **[file]** **[inf]** as in the linked pages. No hosts, secrets or binary addresses.

## Naming

| Family | What it is | In a 3D world? |
|---|---|---|
| **`GR3DV001` / `002` / `003`** | Standalone **February 2000** Graal3D (and Genesis beta). Own TCP world; levels as DirectX `.x` (or Genesis BSP in the beta). | Yes — that product. See `README.md`, `protocol.md`, `beta3-genesis.md`. **[bin]** |
| **`G3D` + date/rev** (eight characters, e.g. `G3D17026`) | Mainline **3.x–6.03** game (and 3.x list) **login version token**. Replaces `GNW…` from 2.x. Often built one character at a time (no cleartext literal). **[bin]** | **Token alone does not mean the client is in 3D mode.** The same string is used for ordinary 2D game login. |
| **`G3D30123`** (+ `newmain`) | 3.x **listserver** hello (parallel to `GNW30123`). **[cap][bin]** | List only. |

Full per-build rows: [`client-internals/version-token-catalogue.md`](../client-internals/version-token-catalogue.md) (section “G3D era”).  
“Are the G3D clients 3D?”: [`protocol/login-tokens-3x-7x.md`](../protocol/login-tokens-3x-7x.md).

Do not invent Worlds / 6.11+ wire tokens here: those builds often have **no** cleartext eight-character `G3D…` in the image. **[bin][inf]**

## When a `G3D…` client is Torque-3D capable

The `G3D` **prefix** runs 3.0–6.03. The **Torque 3D side** runs only **3.04–5.12**. From **5.24r3** onward only the leftover class name `GuiGraal3DCtrl` remains. **[bin]** (`login-tokens-3x-7x.md`, `torque/wire-by-build.md`)

“3D-capable” means the build can load a Torque / `Graal3DEngine` path and talk to a **3D-marked** game server (list name prefix **`"3 "`**). Evidence is ship layout and connect hand-off, not the `G3D` letters. Same host: Graal TCP on the listed port **and** Torque UDP on **port + 1**. **[bin]**

| Era | Token examples | Torque side (held) |
|---|---|---|
| 3.04 | `G3D03014` | Full TGE monolith; stock protocol **9** / game string `Torque Game Engine Demo`; no Graal 3D scripts shipped. **[bin]** |
| 3.153 | `G3D28015` | Graal-changed TGE; protocol **19** / `Graal3D`; `levels3d/` / `main3D.cs`. **[file][bin]** |
| 4.04r2 plug-in | `G3D17026` / `18026` / `19026` | `Graal3DEngine.dll` on demand; protocol **19**. **[bin]** See [`torque-engine-4x.md`](torque-engine-4x.md). |
| 4.20 | `G3D20126` / `21126` / `22126` | `GameObject` layer (no datablocks); protocol **21** (Mac 4.20r6 measured). **[bin]** |
| 5.00–5.12 | `G3D22067`, `G3D14097` / `15097` | `Graal3DEngine.dll` (separate in 5.00, unified by 5.12); protocol **24**. **[bin]** |
| 5.24r3 and later (`G3D15010`, `G3D26090`, `G3D0311C`, …) | Still `G3D…` login tokens | **No Torque 3D side.** **[bin]** |

Assets on the capable path are Torque mission / `levels3d/` / datablock or `GameObject` trees — **not** the 2000 `.x` meshes. **[file]**

Unmeasured siblings in the same era (early 3.0/3.01, some 4.03/4.10 tokens) keep the catalogue token grade; do not invent a protocol number without a handshake row in `torque/wire-by-build.md`.

## Related notes

- Token inventory: [`client-internals/version-token-catalogue.md`](../client-internals/version-token-catalogue.md)
- Token construction + “Are the G3D clients 3D?”: [`protocol/login-tokens-3x-7x.md`](../protocol/login-tokens-3x-7x.md)
- Build-by-build Torque wire: [`torque/wire-by-build.md`](../torque/wire-by-build.md)
- 4.x 3D hand-off: [`torque-engine-4x.md`](torque-engine-4x.md)
- February 2000 product (other line): [`README.md`](README.md), [`research-status-2026-11-16.md`](research-status-2026-11-16.md)
- v7 plugin branding without cleartext `G3D…`: `protocol/v7-graal3d-identity-and-builds.md`
