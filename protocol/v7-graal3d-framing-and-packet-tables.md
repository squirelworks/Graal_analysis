# v7 Graal3DEngine: identity, framing, PLO/PLI tables

Date: 2026-11-08

Target: Worlds `WorldsSetup64-614` `unpacked_Graal3DEngine.dll` (Themida-unpacked Unity native plugin). Cross-checks: same DLL in 548 / 71243; Windows `6.0.3.7` and `6.1.1.3` unpacked exes. Tags: **[bin]** this pass · **[doc]** prior 6.11 reading used only as a map for string clusters that reappear in v7.

Ghidra: `~/ghidra-stable` 12.1.4 PyGhidra project `Graal3D_v7_614` (import + auto-analysis complete). No addresses or `FUN_` names in this file.

---

## 1. Identity

| Field | v7-614 Graal3DEngine **[bin]** |
|---|---|
| On-disk role | `Worlds_data/Plugins/x86_64/Graal3DEngine.dll` (Unity plugin) |
| Export directory name | `Graal3DEngineObfuscated.dll` (548–614); `Graal3DEngineFlavor0.dll` on 71243 |
| VERSIONINFO | Company `Toonslab Ltd`, Product/File `Graal` **6.114**, OriginalFilename `Graal.exe`, ©2017 |
| Status / diag labels | `Client-version:`, `GRAALRELOADED-version:` (plus OS/CPU/memory lines) |
| Quattro surface | Heavy `Quattro*` / `Quattro3D_*` type and bridge strings; frame hooks exported as `QuattroUpdate` / `QuattroFixedUpdate` / `QuattroInitializedReturn` |
| Cache / package magics (same family as 6.x) | `GRESCR01` + `.code`, `GRMAP001`, `GRPKG001`, `GWEBL001`, `GR-V1.04` / `GR-V1.05` |

**Diff vs 6.0.3.7 / 6.1.1.3:** same Toonslab/Graal VERSIONINFO lineage and the same four cache magics. v7 adds the `GRAALRELOADED-version` label next to `Client-version` and ships as a Quattro/Unity plugin instead of a standalone `Graal.exe`. **[bin]**

Login **token string** (eight-character `G……` wire token) is **not** cleartext in this image (no `G3D…` / `GNW…` style literal). `guest` is present; expect the production token/password to come from the connector script or a scrambled blob, same pattern as 6.x hidden hosts. **[bin][inf]**

---

## 2. Framing: two paths confirmed in decomp

Socket object field **framing mode**:

| Mode value | Path |
|---|---|
| `0` | Classic gen-5 |
| `1` | Server-defined template (`setprotocol`) |

### Classic path (mode 0) **[bin]**

Outgoing send:

- Reject text still present: `Illegal characters in the outgoing data`.
- Body must not contain newline (`0x0A`); otherwise abort with that string.
- Wire form: `(id + 0x20)` + body + `'\n'`.
- Optional one-byte “compression/extra” nibble inserted after the id when a sticky flag is set.
- Special internal ids **`0x5D`** and **`0xA3`**: take body length, encode length as **3-byte GCHAR** (`n + 0x20` with 7-bit chunks), then recursively send as id **`0x32`**.
- Flush when outbound buffer ≥ `0x1000`.

Incoming receive:

- 2-byte big-endian length; if length == `0xFFFF`, read a further 4-byte length (6-byte header total).
- Optional lightweight XOR/decode passes keyed off a per-socket compression mode (`1`–`6`).
- Message split on newline; first byte decoded as `id = byte - 0x20`, then dispatched through the socket vtable.

Socket guards: `Cannot send data, socket is not initialized yet.`, `socketerror`, `Received invalid data (1|2|3) from …`.

### Server-defined path (mode 1) **[bin]**

`setprotocol(template)` is implemented: it forces mode `1` and parses the template for field letters. The letter / cipher strings sit as adjacent cleartext next to the invalid-data(3) string:

| Letter | Role | Socket fields filled |
|---|---|---|
| `I` | Counter | offset + width |
| `L` | Length | offset + width |
| `T` | Packet id / type | offset + width |
| `E` | Extra (compression flag nibble) | offset + width |

Widths are 1–4 bytes. A shared writer packs integers into the chosen width/endianness for the outbound header.

Template receive:

- Reads length / type / counter / extra from the configured offsets.
- Mode byte `2` skips leading `0xFF` padding before the header.
- Extra field low nibble selects payload treatment: `0` raw copy, `1` inflate-style, `2` alternate inflate.
- Counter must be previous+1 (masked to the counter width); failure → `Received invalid data (3) from …` and socket kill.
- Dispatch: vtable call with `(packet_id & 0xff, payload)`.
- Special packet-id equal to a configured “nested” id re-enters the same parser (framed-in-framed).

### Directional stream ciphers **[bin]**

Cleartext names **`RC4`** and **`AES`** are real protocol selectors (not only SSL suite strings).

| Direction | Mode byte | Primitive |
|---|---|---|
| Outbound | `1` | `Arc4Process` (exported) |
| Outbound | `2` | `AesCbcEncrypt`; pads with `0xFF` up to 16-byte boundary |
| Inbound | `1` | `Arc4Process` |
| Inbound | `2` | `AesCbcDecrypt` on 16-byte aligned chunks |

A small setup helper chooses RC4 vs AES from a GCHAR’d type byte (`type = byte - 0x20`: `1`→RC4, `2`→AES), then installs key/IV. Related string `DOQLHRbY` appears on that setup path (key-scramble / unwrap — not fully named here).

Connector / script bootstrap **[bin]** (same names as 6.11):

- `StartScript_Connector`
- `StartScript_Fail`
- On the fail object: `onCreated`, `scriptip`, `scriptsslcipher`, `scriptsslsubject`, `scriptsslissuer`
- UI copy: `Problem setting up the networking`, `Connecting to %s...` (+ DE/other locales)

So v7 Graal3D still carries **both** classic gen-5 framing and the **script-selected header / cipher** path. **Default before any connector script runs is mode `0` (classic).** `StartScript_Connector` / `setprotocol` can flip it to mode `1`. Whether Worlds production leaves it classic or switches on connect is a live-session question; the binary default is classic. **[bin][inf]**

**Diff vs 6.0.3.7:** 6.0.3.7 has the classic reject string and cache magics but **not** this connector / `I L T E` / RC4-AES cluster. **[bin]**  
**Diff vs 6.1.1.3:** 6.1.1.3 already has connector + cleartext `onSend*` event names; v7 keeps connector + cipher/template markers but stores `onSend…` names **encrypted** (recovered below). **[bin]**

---

## 3. Remapper / PLO–PLI model **[bin]**

### Cleartext enum names

| Pattern | v7 Graal3DEngine | 6.1.1.3 | 6.0.3.7 |
|---|---|---|---|
| `PLO_*` / `PLI_*` spellings | **absent** | absent | absent |
| Famous payload words (`LEVELBOARD`, `PLAYERPROPS`, …) | almost all absent; `LEVELNAME` appears | richer script/`onSend*` surface | thinner |
| `onSendPlayerProperties`, … as cleartext | **absent** (encrypted) | **present** | mostly absent |

### Two remapper directions

**A. Outgoing PLI remapper** (internal message → wire id / script)

1. Init fills a **256-entry dword** table with `-1`.
2. Script loader: take a numeric array, `memcpy` up to 256 dwords into that table.
3. Per-message bridges (41 slots recovered with names): read `table[slot]`; if value is **`0xFE`**, fire the matching **`onSend*`** script event; otherwise use the value as the wire id / native send path.

**B. Wire-id → handler installer** (pairs from a script byte array)

Installer walks `(id, slot)` pairs:

| Slot byte | Meaning **[bin]** |
|---|---|
| `< 0x5F` | native handler from a **95-entry** function table (~slots 0–94; 90 nonzero) |
| `0xFC` | special — stash id, point at a fixed stub |
| `0xFD` | special — stash id, null handler |
| `0xFE` | script |
| `0xFF` | ignore |

Two more 256-dword tables exist in parallel (same init/loader shape); roles not fully named yet (likely sibling remap / flag tables).

### String codec (for encrypted `onSend*` names) **[bin]**

Stored names are Graal-encrypted. Decrypt (length `L`, index `i`, byte `b`):

```
(( (~signed(b) - L - 10) >> 2 ) & 0x3f)  XOR  ((~b - L - 2) * 0x40)  - i
```

A few strings decrypt with a single interior `NUL`; those letters were restored from the classic onSend lexicon where the match was unique. One name stays unresolved: raw `onsendi\x00pker` → `onsendi?pker`.

### Outgoing PLI slot → `onSend*` event(s)

Slot = internal remapper index (not the on-wire id). The v7 string-recovery pass sometimes listed **two** decrypted names on one even slot (shared DAT / adjacent bridges). The **authoritative 1:1 naming** for slots 0…56 is the 6.11 cleartext table; every v7-recovered name matches its 6.11 slot when present. **[bin][doc]**

| Slot | onSend* (6.11 / v7) | Slot | onSend* |
|---:|---|---:|---|
| 0 | WantWeaponScript | 29 | FileDeletion |
| 1 | WantClassScript | 30 | FolderDeletion |
| 2 | WantGaniScript | 31 | FileRename |
| 3 | ToAllChat | 32 | FilesMove |
| 4 | IsPKer | 33 | HaveWindow |
| 5 | CarryThrown | 34 | EnterLevel |
| 6 | AddHorse | 35 | WantImage |
| 7 | DelHorse | 36 | ImageUpdate |
| 8 | AddBomb | 37 | ImageUpdateCRC |
| 9 | DelBomb | 38 | LevelWarp |
| 10 | ServerWarp | 39 | LevelWarpModtime |
| 11 | TriggerAction | 40 | DownloadFile |
| 12 | FireSpying | 41 | BoardModify |
| 13 | Explosion | 42 | BoardModify2 |
| 14 | WeaponHit | 43 | PreloadLevel |
| 15 | PlayerHurt | 44 | PlayerProperties |
| 16 | DeleteNPC | 45 | NPCProperties |
| 17 | DeleteWeapon | 46 | Flag |
| 18 | Extra | 47 | UnsetFlag |
| 19 | TakeExtra | 48 | Projectile |
| 20 | RemoveExtra | 49 | UpdatePackage |
| 21 | OpenChest | 50 | PrivateMessage |
| 22 | Shot | 51 | UploadStart |
| 23 | BaddyProperties | 52 | SaveFile |
| 24 | BaddyHurt | 53 | UploadEnd |
| 25 | WeaponImage | 54 | *(unused / unrecovered)* |
| 26 | RCChat | 55 | PingAnswer |
| 27 | RequestText | 56 | WindowList |
| 28 | SetText |  |  |

Prefix with `onsend` / `onSend` as needed. Canonical PLI/PLO tables: `protocol/v7-graal3d-pli-plo-tables.md`. Machine JSON: `_work/ghidra_v7_614/pli_plo_tables.json`.

### Native inbound handlers (`< 0x5F`) **[bin][doc]**

The pair-installer’s native table has **95** slots. Bodies are present but almost nameless in cleartext. **Best names** = the 6.11 `onSend*` list above for slots 0…56 (same indices the PLI bridges use). Remaining slots 57…94 are allocated but unnamed in this pass.

**Wire id → handler cannot be dumped statically:** the 256-dword inbound remapper is filled at runtime from script `(wire_id, slot)` pairs. Without a live session remapper image you only get:

1. Native slot index → handler function (table in binary).
2. Slot index → `onSend*` / semantic name (6.11 + v7 string recovery).
3. Not: production wire id numbers for each slot.

Classic gen-5 reference ids (for lab servers still on unmapped ids) remain in **[doc]** `packet-ids.md` (`PLI_PLAYERPROPS=2`, `PLI_BOARDMODIFY=1`, …) — those are **not** proven as Worlds/v7 wire ids after remapping.

### What is *not* claimed yet

- Live **wire-id → native-slot** contents for a Worlds session (needs remapper memory dump / script that installs it).
- Whether Worlds production calls `setprotocol` after connect (binary default = classic).
- Login eight-char token plaintext (not in image).
- ~~Resolved identity of `onsendi?pker`~~ → `onsendispker` / `onSendIsPKer`.

---

## 4. Working checklist (updated)

Done:

1. Framing switch + `I/L/T/E` template + RC4/AES install; default mode 0.
2. Remapper init/loaders; `0xFC`–`0xFF` and `< 0x5F`; `0xFE`→script on PLI bridges.
3. Decrypted `onSend*` names; correlated 1:1 with 6.11 slot table (0…56).
4. Classic dispatch — `id = byte - 0x20`; GCHAR length helper for special ids `0x5D` / `0xA3` → `0x32`.
5. Player-properties encode/decode = classic PLPROP stream (see properties note).
6. GRESCR01 = DES-ECB + server-supplied 8-byte key (see GS2 note).

Still needs a live session:

| Artifact | Why static is insufficient |
|---|---|
| Wire id → slot map | Script-filled remapper |
| Login token | Not cleartext in DLL |
| Production framing mode | Connector may `setprotocol` after start |

No addresses in the published tables.

---

## 5. Short diff vs 6.0.3.7 / 6.1.1.3 (this topic only)

| Topic | 6.0.3.7 | 6.1.1.3 | v7 Graal3D (614) |
|---|---|---|---|
| Classic newline / GCHAR send guard | yes | yes | yes **[bin decomp]** |
| Connector scripts | no | yes | yes |
| `I L T E` + RC4/AES cluster | no | yes (with richer script API text) | yes **[bin decomp]** |
| Cleartext `onSend*` PLI-side events | no | yes | **no** |
| Cleartext `PLO_`/`PLI_` names | no | no | no |
| Remapper 256-dword + `0xFE`→script | — | **[doc]** | **[bin]** |
| `GRAALRELOADED-version` diag | no | no | yes |
| Ship form | standalone exe | standalone exe | Unity plugin + Quattro |

---

## 6. Output location

All of this lives under `~/Cursor/rea-teardown/Graal_analysis/` (not the older FU tree). Sidecar PE teardowns for the same builds remain in `~/Cursor/rea-teardown/WorldsSetup64-*/`. Raw Ghidra extracts (addresses OK) stay under `Graal_analysis/_work/ghidra_v7_614/` and are not part of the published notes.
