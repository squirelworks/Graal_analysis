# Graal 5.x Windows clients: 5.00r7, 5.12, 5.24, 5.30, 5.31

Date: 2026-10-28

Sources: six Windows uploads, read statically. Nothing was run. Only 5.00r7 came unpacked, so most of this page is from that build. Tags: **[bin]** read from the client binaries · **[file]** read from shipped data files · **[inf]** inferred.

## What the uploads are

| Upload | Contents | Wrapper |
|---|---|---|
| 5.00r7 "Unpacked, CRC patch" | A complete installed game folder: Delphi launcher `Graal.exe`, engine `GraalEngine.dll`, `Graal3DEngine.dll`, the self-updater `ExeReplacer.exe`, `license/`, `updatepackages/` and caches. Engine and launcher are dated July 2007. It also holds `GraalEngine.dll.bak` (the unpatched engine) and `Graal5 CRC Patch.exe`. | None (unpacked dump) |
| 5.12, 5.24r3, 5.24r4 | One setup executable each | Every section has the same name (`.data`, `.udata` or `.CRT$XIA`), the only imports are LoadLibraryA and VirtualAlloc, and an encrypted file bundle sits in the overlay. This looks like a MoleBox-style virtualising wrapper, the same one seen on 4.04r2. |
| 5.30r3 (Oct 2010), 5.31r4 (Jan 2011) | One setup executable each, Authenticode-signed | Themida / WinLicense 2.x: blank and random 8-letter section names, a single import, VC 2008 linker. The Windows 6.00r2+ builds use the same wrapper. |

The wrapped builds can't be read without unpacking them, and both wrappers need to run to unpack. So 5.12 to 5.31 are only identified here, not analysed. **[bin]**

The 5.00r7 folder had been used by a player and later updated by the auto-updater: its update packages already name `Graal4.exe` 7.20 and `Graal6.exe` 6.036. **[file]**

## Architecture

- This is the same split as 4.20: a **Delphi launcher** (window, DirectDraw/Direct3D 7, DirectInput, Flash panels) and an **MSVC 6 C++ engine DLL**. The DLL holds the game, the network code and the scripting. It uses the Torque-derived base classes (`GuiControl`, `GuiCanvas`, `MatrixF`, `GBitmap`) and exports about 2,170 decorated C++ names (`TGraalVar`, `TShowImg`, `TScriptExecutionSpace`, `TGraalUniverse`, `TAdventure`, `TParticleEmitter`, `JString`). **[bin]**
- The launcher calls `graal_engineInitialize` and hands the engine its callbacks through the `graal_set*` exports (`graal_setOnServerLogin`, `graal_setOnServerListerConnect`, …). If initialisation fails, the launcher shows "The execution file is corrupted". **[bin]**
- `Graal3DEngine.dll` links against the engine DLL (about 700 imports) and exports only `loadGraal3DEngine`, `runGraal3DEngine`, `endGraal3DEngine`, `resizeGraal3DWindow` and `toggleGraal3DFullScreen`. **[bin]**
- The engine's own source tree is named `graallib`. It contains its own crypto (`crypto/sha1.c`, `rsa.c`, `des.c`, plus Blowfish and MD5), zlib, bzip2, libjpeg, JasPer, giflib 4.0 and fmod. **[bin]**

## License file and signatures

- `license/license.graal` is still a CRLF text file: host, port, site name, signup URL, translate URL, then two fallback hosts. The stock values are `loginserver.graalonline.com`, port **14900**, with `loginserver2`/`loginserver3` as fallbacks (the same as 4.20). At least 5 lines are required. Line 2 has a suffix appended. **[bin][file]**
- There are **four files**, as in 4.20 for Windows: `sig.graal` signs the launcher executable, `sig.graallib` signs `GraalEngine.dll`, and `sig.license` signs `license.graal`. Each is RSA-1024 with PKCS#1 v1.5 over SHA-1, e = 17, using the **same public key as 3.x and 4.x**. **[bin]**
- The engine checks the files in this order: all four present, then exe → DLL → license, and it **stops on any failure** ("The license file(s) have not been found." / "The license file is invalid."). The 4.20r8 Windows engine checks the same chain and also stops on failure. **[bin]**

### The "CRC patch" (third-party)

- The patched `GraalEngine.dll` differs from the original in **8 bytes**, all in the license loader. **[bin]**
  1. A conditional jump becomes unconditional, so the "files not found" exit is skipped.
  2. A conditional jump becomes unconditional, so the "license is invalid" exit is skipped.
  3. A 6-byte conditional jump becomes NOPs, which removes the "at least 5 lines" check.
- So the patched client accepts any `license.graal`, including a missing or bad signature. In this folder the file had been edited to point at a private LAN host on port 14900, with `.graal.in` fallbacks, which suggests a private or emulated login server. **[file][inf]**
- None of the three signature files in the folder match the files beside them. The signatures decode to a valid SHA-1 DigestInfo, so they belong to other file versions. **[bin][file]**
- `Graal5 CRC Patch.exe` itself is a small Delphi program packed with UPX 0.72, which is too old for current UPX to unpack. It wasn't unpacked; the byte diff above shows what it does. **[bin]**

## Login

- **The separate list-server protocol is gone.** The client opens a normal game connection to a server named `Login`, at the host and port from `license.graal`. The server list and account screens are then served by that Login server as scripted GUI. S→C 190 raises the script event `onServerListerConnect`. The 3.x listserver ids (7 `G3D30123newmain`, then 1 account/password) are no longer used. **[bin]**
- The first message is id **5**, sent in mode 3 (zlib, no cipher, no type byte): **[bin]**
  1. key GCHAR (`rand & 0x7F`), sent only on the first message
  2. token **`G3D22067`**, assembled from eight one-character globals, so no literal exists
  3. `GCHAR len` + account
  4. `GCHAR len` + password (a password of 0xE0 bytes or more is sent as 0xFF followed by its first 0xDF bytes)
  5. a comma-separated list of four fields: `win`, then the MD5 hex of the Windows `DigitalProductId` registry value, the MD5 hex of the network adapter MAC address (if that isn't available, the node part of `UuidCreateSequential`), and the MD5 hex of the `C:\` volume serial number
- These four fields are **hardware identifiers**, which are new since 3.x. They let the server ban per machine. The 4.20r8 Windows client sends the same layout with token `G3D20126`. **[bin][inf]**
- Next comes id **37**, the language, as in 3.x. Then the socket switches to dynamic mode. **[bin]**
- Id 93 (a long payload) is sent with a GINT3 length through id 50 first. **[bin]**

## Cipher

**Gen 5, unchanged from 2.22, 2.31, 3.x and 4.20.** **[bin]**

- The LCG is `it = it*0x08088405 + key`, and both directions are seeded with `0x04A80B38`.
- The frame is a `u16be` length, then a type byte in dynamic mode:
  - 2 = raw (under 0x30 bytes)
  - 4 = zlib (under 0x1000 bytes)
  - 6 = bzip2 (larger)
- Type 2 XORs at most 12 dwords; types 4 and 6 XOR at most 4.
- Outgoing data is cut into 1000-byte chunks. A build switch can move the socket onto its own network thread.

## Server → client ids (5.00r7)

100 ids are handled: 0–25, 27–43, 45–49, 67, 68, 69, 74, 75, 82, 84, 101, 102, 104–107, 131–134, 140, 150, 151, 153–156, 165, 166, 168–176, 178–187, 189, 190, 191, 193, 194, 195, 197. **[bin]**

Compared with Mac 3.153 (`v3x-clients.md`), 5.00r7 drops 100 and adds the following:

| Id | What the handler does |
|---|---|
| 105 | Name + GINT5: sets a size or modification time on a cached object |
| 106 | Update packages: raises `onUpdatePackageDownloaded` / `onPackagesDownloadComplete` |
| 107 | Raises the script level to at least 5, then passes data to a script object |
| 140, 197 | Class / weapon script delivery (see GRESCR01 below) |
| 170 | GCHAR stored as the connection mode; a mode change resets a player field |
| 182 | **Process list request**: the client answers with C→S 44 and the comma list of its running processes |
| 183 | **"Is process running?"**: the client checks one process name against the same list and reports back |
| 190 | `onServerListerConnect` (the Login server's server-list screen) |
| 191 | GSHORT id + data, routed to an object by id |
| 193 | GINT5 + name, routed to an NPC (raises the script level to at least 3) |
| 194 | Clears every loaded level and the level caches |
| 195 | Gani name + gani text, loaded into the named gani (server-sent gani script) |

S→C 82 (server text) now also feeds the buddy list (`getbuddylist`, `lister`). Ids 182/183 are an anti-cheat process scan. **[bin][inf]**

## Client → server ids (5.00r7)

From the connection's send wrappers: 1, 2, 4, 5, 6, 7, 8, 9, 10, 12–19, 21–24, 26, 28, 29, 32–36, 37, 41, 44, 47, 50, 79, 80, 81, 92, 93, 96, 97, 98, 130, 152, 154–159, 161. Ids sent through a variable aren't captured, so treat this list as a floor. **[bin]**

## File formats

| Magic | Notes |
|---|---|
| `GR-V1.00` – `GR-V1.04` | As in 3.x |
| **`GR-V1.05`** | New. It is GR-V1.04 with **tile layers**: after the magic comes a GCHAR layer count, then one 64×64 board per layer (13-bit tiles, as in 1.02+). The rest of the body follows as in 1.04. It is accepted in local levels and in the web-level cache. **[bin]** |
| `GLEVNW01`, `GSERVL01` | Text levels, as in 3.x |
| `GWEBL001` | Web-level cache, as in 3.x. It now accepts GR-V1.03/1.04/1.05 bodies. **[bin]** |
| `GRMAP001` | gmap, as in 3.x |
| **`GRESCR01`** | New. A **script cache**: the magic, then a body encrypted with **DES-ECB** (8-byte blocks, 8-byte key). On load, the client takes the CRC32 of the plain body and compares it with the value the server sends; on a mismatch the client asks the server for the script again. It caches class and weapon scripts. **[bin]** |
| **`GRPKG001`** | Update package (`.gupd`), a text file with the keys `NAME`, `VERSION`, `PLATFORM`, `DESCRIPTION…DESCRIPTIONEND`, `MODE` (`required`), `ISMAINEXECUTABLE`, `PROTECTOVERWRITE`, `USECHECKSUM`, `SUBPACKAGE`, `FLAG`, `FILE`. Packages nest through `SUBPACKAGE`, with per-platform variants (`_win`, `_mac`, `_linux`). **[file][bin]** |

Other files: `game_config.txt` (key=value options, including voice chat, video recording and a fixed UDP port, default 14899), `localversions.txt`, and web caches whose names are percent-encoded with decimal codes (`%058` = `:`, `%047` = `/`). The console log is still `graal4console.log`. **[file][bin]**

## Not done

- Unpacking the 5.12–5.24 bundle and the 5.30/5.31 Themida builds (both wrappers need to run)
- The DES key source for GRESCR01
- Names for the new C→S ids
- The Graal3DEngine protocol
