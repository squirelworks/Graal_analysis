# v3 (Linux 3.0.4) — identity and framing

Date: 2026-11-08 · Target: clear ELF32 `graalexe 3.0.4` from the unpacked Linux 3.04 tree. Tags: **[bin]** · **[inf]**.

---

## Identity · **high** (binary) · **medium** (runtime version string)

| Field | Value |
|---|---|
| Image | `graalexe 3.0.4` — ELF32 i386, dynamically linked, not packed |
| Toolchain | GCC 2.96 (Red Hat 7.3) + NASM 0.98 |
| Product banner in-image | **Torque Game Engine Demo** (full host) |
| Graal layer | `graal/*.cpp` (`client`, `graalconnection`, `descipher`, `levels`, `npcs`, `scriptfunctions`, …) |
| Config dir hint | `$HOME/.garagegames/%s` |
| Company / FileVersion PE | **None** (not the later “Linux Cyberjoueur / 4.2.0.8” VERSIONINFO) |

Version is exposed to script/UI as `getVersionString` / `graalversion` (server-list field “Graal version”). A baked eight-char token (`G3D` / `GNW` / `GNP`) and a literal `3.0.4` inside the image were **not** found. The `3.0.4` token is the **filename**.

### Ports · **high** (prefs) · **low** (numeric default)

| Pref / UI | Meaning |
|---|---|
| `$pref::Graal::fixedport` | fixed port (options copy: “Use fixed port for UDP”) |
| `$pref::Graal::fixedudpport` | fixed UDP port |
| `$pref::Graal::noudp` | disable UDP |
| Runtime | `UDP initialized on port %d` |

No baked `14900` / `loginserver` string (that shows up in late-5).

---

## Login · **high** (surface)

`Connecting to the game server...`, account pref, password, server lister (`ServerGraalVersion`, `Disconnected from serverlister`), `Disconnection reason: %s`. List traffic is a separate lister client from the game session.

---

## Framing · **high** (two layers) · **medium** (which bytes are on the socket)

### 1. Torque net (the host)

Full `NetConnection` / `BitStream`, UDP init, master-server list packets, telnet console. This is the process transport, not a leftover DLL.

### 2. Graal payload (classic GCHAR)

Player/property updates use **`id + 0x20`** bytes (same family as v4): a dispatcher switches on wire bytes `0x20` and `0x2b`–`0x3d`, and the property codec emits `value + 0x20` / length-prefixed strings. Newline padding appears in the script cipher (below), which fits text lines.

There is **no** `onSend*` / `0xFE` remapper and **no** v4 `hcrypt` voice API.

### 3. `descipher` (`.code` scripts, not the game socket)

Compiled scripts named `.code` are wrapped by `graal/descipher`:

1. Pad with newline (`0x0A`) to a multiple of 8.
2. Prefix a 4-byte length = padded size + 8.
3. Each 8-byte block is mixed with an LCG keystream (`state * 0x8088405 + 1`) and a block transform.
4. An 8-byte additive checksum is appended and checked on load.

---

## Diff vs v4 (identity + framing)

| Topic | v3.0.4 | v4.2.0.8 |
|---|---|---|
| Ship | one Torque+Graal ELF | Delphi exe + Engine + 3DEngine |
| Version | filename `3.0.4`; `getVersionString` | PE FileVersion 4.2.0.8, Cyberjoueur |
| Protocol URL | no `graal://` parser found | `setGraalProtocolString` |
| Game PL | GCHAR `id+0x20` (partial table) | GCHAR `id+0x20` (logged + full send wrappers) |
| Extra cipher | **descipher on `.code`** | **hcrypt on HVDI voice** |
| UDP | Torque UDP + `noudp` | optional package UDP, default 14899 |
