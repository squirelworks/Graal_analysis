# v7 Graal3DEngine: GS2 / scripts / packages

Date: 2026-11-08

Target: WorldsSetup64-614 `unpacked_Graal3DEngine.dll`. Tags: **[bin]** · **[doc]** Preagonal / Seihai GS2 notes for bytecode vocabulary only (not a v7 dump of their C#).

No addresses in this file. Raw work: `_work/ghidra_v7_614/grescr_layout.json`, `props_gs2_*.json`.

---

## 1. Big picture **[bin]**

Native Graal script VM still runs inside the Unity plugin (types `TScriptUniverse`, `TScriptFunction`, `TActionScriptVar`, `TGraalVar`, `actionplayer`). Packages use **`GRESCR01`** + `.code`. Marker **`Ld/GS2`** appears inside bytecode blobs. Quattro bridges events back toward graalscript (deprecated EventManager string).

---

## 2. GRESCR01 container & load path **[bin]**

| Item | Behavior |
|---|---|
| Magic | `GRESCR01` (8 bytes) |
| Body | **DES-ECB**, 8-byte blocks (standard DES; self-test KATs match) |
| Key | caller-supplied 8 bytes — same contract as 5.x: **two GINT5 → LE key** on delivery / cache-hit packets **[doc]** |
| CRC | CRC32 of **plaintext**; compared to server checksum on cache load |
| On disk | magic \|\| ciphertext; **key never stored beside the file** |
| Paths | `.code` suffix; load by path or buffer |

Sibling magics: `GRMAP001`, `GRPKG001`, `GWEBL001`, `GR-V1.04` / `GR-V1.05`.

Maps/web: `GWEBL001` / `GRMAP001` remain on the download/cache path (not GS2-specific, same family).

---

## 3. Bytecode stream (what v7 accepts) **[bin][doc]**

**From the binary:** `Ld/GS2` embedded in non-string data; GRESCR decrypt then hands a buffer to the script loader. No cleartext opcode enum (`OP_ADD`, …) was recovered as a named table in this pass.

**Segment file shape** (industry/reimplementation consensus used as a map, not proven byte-for-byte on a Worlds capture) **[doc]**:

| Segment | Contents |
|---|---|
| 1 | flags word (often 0) |
| 2 | function table (op index + NUL name; `public.` stripped) |
| 3 | string table |
| 4 | opcodes + operand markers |
| trailer | often a newline byte |

Operand markers in that family: `F0`–`F2` string-table index widths; `F3`–`F5` signed ints; `F6` NUL decimal. **[doc]**

Official wire still distinguishes NPC bytecode (headerless segments) vs class/weapon script messages that carry type/name/cache/key/CRC — see 5.x notes. v7 loaders still understand GRESCR cache + CRC. **[bin][doc]**

---

## 4. VM / peephole / fused ops **[bin][inf]**

| Probe | Result |
|---|---|
| Peephole / superinstruction cleartext | **not found** |
| Fused-opcode table | **not recovered** in v7-614 |
| Built-in list as clear strings | partial host/script API surface only (`settimer`, connection methods, property names) — not a full opcode dump |

Do not claim a numeric opcode map for Worlds until a decrypted `Ld/GS2` body is stepped in the v7 VM.

---

## 5. Limits & security **[bin][inf]**

| Probe | Result |
|---|---|
| Event-queue / array / string caps as named constants | **not recovered** as clear symbols this pass |
| Script level / security level checks | script-level raising exists in the 5.x/6.x protocol family; v7 still has script objects + read-only var guard (`Write to read-only var `) |

Gap noted — no invented numbers.

---

## 6. Runtime types & prefixes **[bin]**

| Symbol | Role |
|---|---|
| `tclient_` / `adventure_` | client handler name prefixes |
| `TServerNPC` / `TServerWeapon` | objects that get the 95-name property registry |
| `StartScript_Connector` / `_Fail` / `_GraalGui` / … | bootstrap scripts |
| `scriptfiles/` | on-disk scripts |
| `/con.gs` | console script fragment |

`tclient_` builder stores metadata (flags, param type codes). Full name→native-slot order is **not** a static pointer table in the image (see PLI/PLO note).

---

## 7. Diff vs Preagonal GS2Compiler / Engine **[doc]**

Preagonal is an MPL-2.0 third-party compiler+VM. Useful as vocabulary only.

| Topic | Preagonal **[doc]** | v7 Worlds **[bin]** |
|---|---|---|
| Source → bytecode compiler | yes (C#) | client **runs** bytecode; does not ship that compiler |
| Four-segment file | yes | consistent with `Ld/GS2` + GRESCR plaintext payloads |
| Header flag for weapon/class | yes | GRESCR + server key/CRC path instead of their simplified header |
| Opcodes compiler emits but engine skips | several empty arms | **unknown** until v7 VM switch is mapped |
| `waitfor` | compiler emits; their engine no-ops | not confirmed in v7 |
| Host objects | C# `GuiControl` reflection | Quattro + Graal native objects |
| Timers | wall-clock quirks | not traced in v7 this pass |

**VM accepts that compiler may not emit / reverse:** unsettled for Worlds — needs a captured official bytecode vs Preagonal output lab. Do not treat Preagonal empty arms as v7 behavior.

---

## 8. Open

1. Decrypt a live GRESCR body and dump the opcode switch.  
2. Built-in / limit constants.  
3. Byte-level compare Worlds bytecode ↔ Preagonal / gs2-parser fixtures.
