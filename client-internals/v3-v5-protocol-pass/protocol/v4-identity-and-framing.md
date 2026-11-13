# v4 (4.2.0.8) — identity and framing

Date: 2026-11-08 · Targets: Unpacked `Graal 4.2.0.8.exe` + `GraalEngine.dll`. Tags: **[bin]** · **[inf]**.

---

## Identity · **high** (PE)

| Field | Value |
|---|---|
| FileVersion | **4.2.0.8** |
| Company | Linux Cyberjoueur |
| Product / description | Graal / Graal Online client |
| InternalName | Graal client |
| Architecture | Delphi/Borland **host exe** + `GRAALENGINE.DLL` + optional `GRAAL3DENGINE.DLL` |

### Version / protocol token · **high** (parser) · **low** (production value)

| Probe | Result |
|---|---|
| Cleartext `G3D` / `GNW` / `GNP` eight-char | **Absent** as a fixed literal |
| Guest | `guest` / `guest_` / `-guestaccount` / `setDefaultGuestAccount` |
| Protocol API | **`setGraalProtocolString`** |
| HTTP UA prefix | `User-Agent: Graal/` |

**Parser:** strip `graal://` (8) or `graal3://` (9); split on `/`; first segment = protocol token, remainder stored separately. Production token string is runtime-supplied (not baked).

### Ports · **high**

| Pref / UI | Meaning |
|---|---|
| `fixedport` | fixed TCP data port |
| `fixedudpport` | fixed UDP port (**default 14899** in shipped `graal4config.txt` + Engine string) |
| `noudp` | disable UDP packages (shipped config often `true`) |

No baked `loginserver…:14900` (that is late-5).

---

## Login / connect · **high**

`connectToGraalServer(host, …)` → internal connect helper. Status/events: `Connecting to the game server...`, `onServerLogin`, `onServerListerConnect`, `onPlayerLogin`, disconnect banner. Account HTTP is separate (`<public-host>/accounts/login.php`).

---

## Framing · **high** (cleartext PL) · **high** (voice hcrypt) · **low** (TCP length header)

### Game packets (cleartext logical form)

Proven by:

1. Era packet logger (`g4_PackLog`) formatting: newline-split lines, print `first_byte - 32` as the id.  
2. Inbound dispatcher: read byte at index 1, `id = byte - 0x20`, `switch` on the wire byte.  
3. Outbound wrappers: `vtable+8(opcode, payload)` and GCHAR payload bytes as `value + 0x20`.

| Piece | Rule |
|---|---|
| Record | newline-delimited line |
| First byte | `opcode + 0x20` (GCHAR) |
| Payload | GCHAR / GINT7 / length-prefixed strings (`len+0x20` then bytes; long strings use 0xDF chunking) |
| Remapper | **none** (no `onSend*` / `0xFE`) |

This **is** the classic gen-5 cleartext family, even though late-5’s “Illegal characters…” reject strings are absent from this image.

### Voice path (HVDI) — separate

`hvdiPacketEncode` / `Decode`: type in low 6 bits; **`0x40`** = 2-byte BE sequence; **`0x80`** = body encrypted with **`hcryptEncryptPacket` / `DecryptPacket`** (8-byte OFB-like XOR core). Codecs 1–10 / VOX / AGC. Not the PLI/PLO opcode table.

### Send trampoline

`sendOutgoingData` → `connection_vtable+0xC`. Opcode sends use **`connection_vtable+0x8(opcode, payload)`**.

### Compression

`CompressBuf` / `DecompressBuf` present (zlib in ship). Not required for every PL line.

UDP: optional package path; `noudp` disables.

---

## Diff vs v5 / v6 (identity + framing)

| Topic | v4.2.0.8 | Late v5 | v6.113 |
|---|---|---|---|
| Ship | exe + Engine + 3DEngine | Quattro dump | Quattro |
| Cleartext `id+0x20` / newline | **yes** | yes | yes (pre-FE) |
| Baked login `:14900` | no | **yes** | no |
| FE `onSend*` remapper | no | no | **yes** |
| hcrypt | **voice (HVDI)** | — | AES/RC4 game path |
| Default UDP pref | **14899** | era-specific | era-specific |
