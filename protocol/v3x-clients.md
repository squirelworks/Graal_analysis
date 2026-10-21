# Graal 3.x clients: Linux 3.04 and Mac OS X 3.153

Date: 2026-10-21

Sources: the Graal 3.04 Linux installer (Makeself and a 2014 tgz repack, same game files) and the Graal 3.153 Mac OS X disk image, read statically. A third upload, a 3.151 Linux installer, is damaged (see the end). Tags: **[bin]** read from the client binaries · **[file]** read from shipped data files · **[inf]** inferred.

## What these clients are

- 3.x is a **C++ rewrite on the Torque Game Engine** (GarageGames). It is not Delphi. The menus, prefs and key binds are compiled TorqueScript (`.dso`, format version 33). Levels, NPCs, GS1, ganis and the Graal network protocol are native code. **[bin][file]**
- Linux 3.04 (Jan 2004): i386 ELF, UPX-packed, stripped. Uses SDL 1.2, OpenAL and fmod. Mac 3.153 (Feb 2005): PowerPC Mach-O, Carbon, stripped. Both were built by "Linux Cyberjoueurs" (Paris). **[bin][file]**
- Neither build has a usable symbol table. Naming comes from RTTI class names (e.g. `TGraalConnection`, `TServerListClient`, `TServerLevel`, `TServerNPC`, `TGraalScript`, `GuiGraalCtrl`), from source file names left in allocation tracking (`graal/client.cpp`, `graal/serverlist.cpp`, `graal/levels.cpp`, `graal/npcs.cpp`, `graal/descipher.cpp`, …) and from the Torque console method table. This is a different code base from the Delphi 2.x clients, so the names do not carry over to them. **[bin]**
- The 3.153 data tree adds a 3D mode (`levels3d/`, `scripts/` with Torque mission, terrain and `GameConnection` scripts). 3D servers run the Torque engine's own UDP protocol on port 28000, alongside the Graal TCP protocol. **[file][bin]**

## Version tokens

| Use | 3.04 Linux | 3.153 Mac | Windows counterpart |
|---|---|---|---|
| Game-server login | `G3D03014` | `G3D28015` | `GNW03014` (2.22) / `GNW28015` (2.31) |
| Listserver | `G3D30123` | `G3D30123` | `GNW30123` (2.22, 2.31) |

The 3.x tokens are the Windows tokens with the `GNW` prefix replaced by `G3D`. The date stamp is unchanged. So 3.04 speaks the 2.22 protocol and 3.153 speaks the 2.31 protocol. As in every Delphi build, the token is assembled one character at a time, so no string literal exists. **[bin]**

## Listserver

- **Host and port are not compiled in.** They come from `license/license.graal`, a short CRLF text file: the primary host `listserver.graalonline.com`, port `14922`, the site name, the signup and translate URLs, then `listserver2` and `listserver3` as fallbacks. **[file]**
- The file is **RSA-signed**. `license/sig.license` holds a 1024-bit RSA signature (PKCS#1 v1.5 over SHA-1, public exponent 17) as 256 hex characters. `license/sig.graal` signs the shipped (packed) executable file in the same way. The public key is embedded in the client as a hex-encoded DER key. All three signatures check out against it, so the client can tell if the host list or the executable has been edited. **[bin][file]**
- Login sequence: **[bin]**
  1. id 7: key GCHAR, then `G3D30123newmain`. This is the first message of the connection. It is sent in fixed mode 3 (zlib, no cipher, no type byte).
  2. Flush. The socket switches to gen 5.
  3. id 1: `str account`, `str password`.
- Server → client: 0 server list, 2 account status text (shown on the server list screen; marks the login as accepted), 4 error text (message box). 1, 3, 5 and 6 are accepted and ignored. **[bin]**
- Server list (id 0): `GCHAR count`, then per server `GCHAR fieldcount` and that many `str`. Field 0 is the name and field 5 the player count. **[bin]**
- **Category prefix on the server name.** It decides which tab lists the server: **[bin]**

| Prefix | Tab |
|---|---|
| `P ` | Graal Gold |
| `3 ` | Graal 3D |
| `H ` | Hosted |
| `U ` | not listed |
| none | Classic |

## Game-server login and cipher

- Login: id **5**, key GCHAR (`rand & 0x7F`), token, `str account`, `str password`. Then id **37** (language). Neither build sends id 39 (`PLI_TAMPERCHECK`) after login, which 2.22 and 2.31 do. The account and password are used as plain strings, with no `dec(b) = (~b − 10)` step as in 2.17+. **[bin]**
- **Cipher and framing are gen 5, the same as the 2.22/2.31 Windows clients.** The same LCG (`it = it * 0x08088405 + key`, seed `0x04A80B38`, one iterator per direction). Login frame in fixed mode 3, then dynamic: type 2 (raw) or 4 (zlib) under 0x30 bytes, 4 under 0x1000, otherwise 6 (bz2). Even types are partially XORed (at most 12 dwords for type 2, 4 for types 4 and 6). Frame `u16be (len + 1)`, type byte, body. See `codec-and-framing.md` and `client-versions.md` on the cross-version branch for the full rule. **[bin]**

## Server → client ids handled

Read from each build's main receive switch. Names from gs2lib. **[bin]**

| Ids | 3.04 | 3.153 | Notes |
|---|:-:|:-:|---|
| 0–25, 27–43, 45–49 | ✔ | ✔ | |
| 44 `HASNPCSERVER` | ✔ | · | dropped in 3.153, as in 2.31 |
| 67 | · | ✔ | raised to script as a folder-log event |
| 68, 69 `LARGEFILESTART` / `END` | ✔ | ✔ | |
| 74 | · | ✔ | raised to script as an RC-chat event |
| 75 `PROFILE` | ✔ | ✔ | |
| 82 `SERVERTEXT` | · | ✔ | raised to script as `receivetext` |
| 84 `LARGEFILESIZE` | ✔ | ✔ | |
| 100, 101, 102 | ✔ | ✔ | |
| 104 | · | ✔ | |
| 131 `NPCBYTECODE`, 132, 133 | · | ✔ | script and class registration (`joinedclasses`, `public.` variables) |
| 134 `GANISCRIPT` | · | ✔ | gani text parsed in place |
| 150, 151, 153–156, 165, 166, 168 | ✔ | ✔ | |
| 169, 171–176, 178–181, 184, 185, 186 | ✔ | ✔ | 3.04 lacks 170, 177, 182 and 183, which 2.22 handles |
| 187, 189 `MOVE2` | · | ✔ | |

Counts: 3.04 handles 79 ids, 3.153 handles 88.

Client → server: login 5 and language 37 are confirmed. Most other sends go through an indirect call, so the full table is still open.

## File formats

- **`GR-V1.04`** is `GR-V1.03` plus a heights block after the NPC section: `HEIGHTS`, then 9 lines of 9 comma-separated floats, then `HEIGHTSEND`. The client writes 1.04 only when the level has heights, otherwise 1.03. This pairs with server → client id 185 (`BOARDHEIGHTS`). **[bin]**
- **`GSERVL01`** is a second text-level magic, read by the same parser as `GLEVNW01`. Keywords: `BOARD`, `LINK`, `CHEST`, `SIGN`, `NPC`…`NPCEND`, `BADDY`…`BADDYEND`, `HEIGHTS`…`HEIGHTSEND`, and `REPLACENPCS`…`REPLACENPCSEND` (skipped by the client). **[bin]**
- **`GWEBL001`** (downloaded-level cache): magic, `str` server name, two 7-bit characters of protocol version, a GINT5 modification time, `str` level name, then a `GR-V1.03`/`1.04` body. The cache is only used when the server name, version and level name match. As in 2.05, a seed of `0x04A80B38 × product(level-name bytes)` is computed before the read, and the DES unit is still linked. **[bin][inf]**
- **`GRMAP001`** gains keys for 3D/heightmapped maps: `GENSEED`, `LEVHEIGHT`, `LEVCHAOS`, `MINIMAPIMG`, `NOAUTOMAPPING`, `HEIGHTMAP`…`HEIGHTMAPEND`, and `RANDOMSEEDS`…`RANDOMSEEDSEND`, besides `WIDTH`, `HEIGHT`, `GENERATED` and `LEVELNAMES`. **[bin]**

## The uploads, for the record

- The two Mac uploads ("3.04" and "3.15r2") are byte-identical. Both are the 3.153 image.
- The 3.04 "Obsolete" installer and the 3.04 "Fixed" tgz hold the same game files. The tgz only adds x86_64 builds of the Loki installer.
- The 3.151 Linux installer ("Broken") is 139 bytes short. Its gzip payload contains no CR LF pairs at all, where about 140 would be expected. It went through an ASCII-mode FTP transfer that turned every CR LF into LF. Only the installer metadata at the start survives: version 3.151, with the same `languages3D` / `levels3d` / `scripts*` layout as the Mac 3.153. The game binary needs a clean copy.
