# Graal 4.x clients: Windows 4.20r8, Mac OS X 4.20r6, Windows 4.04r2

Date: 2026-10-29 (4.04r2 section added the same day, after the installer was unpacked)

Sources: five uploads, read statically. Nothing was run. Tags: **[bin]** read from the client binaries · **[file]** read from shipped data files · **[src]** read from source code shipped with an upload · **[inf]** inferred.

| Upload | What it holds |
|---|---|
| Windows 4.20r8 "Packet Logger v2" | `Graal4.exe` launcher, `GraalEngine.dll` (link date January 2007), `g4_PackLog.dll`. **The engine DLL is modified by a third party** (see "Packet logger"). |
| Windows 4.20r8 "Packet Logger v1 Only" | The Code::Blocks / MinGW project and C++ source of `g4_PackLog.dll` (June 2007). Same DLL as in v2. |
| Mac OS X 4.20r6 | HFS+ disk image: `Graal.app` (PowerPC, September 2006, "© 2006 Linux Cyberjoueurs"), `ExeReplacer`, `license/`, `languages3D/`, `levels/`, `levels3d/gui`, `sounds/`. |
| Windows 4.04r2 installer | `Graal4Setup.exe`, a **Thinstall** (2003) virtualised bundle. Unpacked: `Graal4.exe`, `GraalEngine.dll` (March 2006), **`Graal3DEngine.dll`**, `fmod.dll`, `ExeReplacer_temp.exe`, `license/` and the data tree (see "Windows 4.04r2"). Stock, unmodified. |
| Windows 4.20r8 "Unpacked" | Password-protected 7z with encrypted headers. No password is known, so it was skipped. |

So the readable game code is the **4.04r2 Windows engine** (stock), the **4.20r8 Windows engine** (third-party modified) and the **4.20r6 Mac client** (stock).

## What these clients are

- On Windows, 4.x splits into two parts. **[bin]**
  - `Graal4.exe` is a **Delphi** launcher. It does the window, DirectDraw drawing, input, the web panel and the external windows (PM, player list, profile, options). It registers the `graal://` and `graal3://` URL handlers, reads `graal4config.txt` and `HKCU\Software\Graal\Client`, writes `graal4console.log`, and can start `Graal3.exe` for 3D.
  - `GraalEngine.dll` is **MSVC C++** on the same Torque-derived base classes as 3.x (`JString`, `TList`, `TGraalVar`, `GuiCanvas`, …). It holds the game, scripts, files and network, and imports WinSock and fmod. It exports about 2,000 C++ symbols, including the `graal_engineInitialize` / `graal_setHomeDirectory` entry points and about 115 `graal_set…` calls through which the launcher hands it drawing, text, Flash-panel, window and login callbacks.
- The Mac client is one PowerPC binary built from the same engine source. It ships `ExeReplacer`, a small helper that swaps in a new executable and restarts it (it only uses `chmod` and `execvp`), for the update system below. **[bin][inf]**
- The engine's own source tree is `K:\src\graalv4\…`. Crypto is **libtomcrypt** (`crypt.c, des.c, packet.c, prime.c, rsa.c, rsa_sys.c, sha1.c`), not Crypto++ as in 3.x. The other libraries are zlib, bzip2, JasPer, giflib 4.0, libjpeg and libpng. **[bin]**
- At start-up the engine makes between 0 and 1,023 heap allocations of random size, creates the main player object, then frees them. This puts the player object at a different heap address on each run, which defeats simple memory scanners. **[bin]**

So the line is: 2.x is Delphi only, 3.x is a Torque C++ monolith, and 4.x is a Delphi front end on a C++ engine.

## Login server and `license.graal`

- The host comes from `license/license.graal`, as in 3.x. The 4.20r6 file reads `loginserver.graalonline.com`, port **14900**, `Graalonline.com`, the signup URL, the translate URL, then `loginserver2.graalonline.com` and `loginserver3.graalonline.com`. (3.x: `listserver.graalonline.com:14922`.) Lines used: 0 host, 1 port, 2 site name, 3 signup URL, 4 translate URL, 5 and 6 fallbacks. **[file][bin]**
- **There is no separate listserver protocol any more.** The client connects to the license host as an ordinary game server named `Login`, with the normal game login below; the server list is served inside that session. If it fails, the next host in the list is tried. **[bin]**
- Signatures use the **same RSA-1024 key as 3.x** (PKCS#1 v1.5 over SHA-1, e = 17, the key embedded as hex DER). The Mac `sig.license` verifies against `license.graal` and `sig.graal` against the Mac executable. **[bin][file]**
- Windows adds a fourth file, **`license/sig.graallib`**, the signature of `GraalEngine.dll`. The check runs in order: exe, then DLL (Windows only), then license. Any missing file stops the client with "The license file(s) have not been found", and any bad signature stops it before the license is read. The Mac client checks exe and license the same way. **[bin]**
- The stock 4.04r2 engine confirms this: when any of the three signatures fails it shows "The license file is invalid!" and stops. All three of its shipped signatures verify against its own files.
- The packet-logger copy of the 4.20r8 engine has this check disabled by a one-byte patch. A conditional jump after the result test has become an unconditional jump, so the "bad signature" branch is never taken. This is a third-party change, not 4.20r8 behaviour. **[bin][inf]**

## Version tokens

| Build | Game login token | Date stamp |
|---|---|---|
| Windows 4.04r2 | `G3D17026` | 17 February 2006 |
| Mac OS X 4.20r6 | `G3D27076` | 27 July 2006 |
| Windows 4.20r8 | `G3D20126` | 20 December 2006 |

The tokens follow the 3.x pattern: `G3D`, then a `DDMMY` date. The dates fit the builds (March 2006 4.04r2 engine, September 2006 Mac build, January 2007 4.20r8 engine), as they do for `G3D16053` (3.0), `G3D03014` (3.04) and `G3D28015` (3.153). Each token is still assembled one character at a time, so there is no string literal. **[bin][inf]**

## Login packet

The first packet on a connection (gen 5, fixed mode 3: zlib, no cipher, no type byte, then the socket switches to dynamic mode). **[bin]**

1. id **5**, key GCHAR, the 8-character token.
2. GCHAR-length account, GCHAR-length password. (Lengths of 224 or more are sent as 0xFF followed by the first 223 bytes.)
3. A comma-text list that identifies the machine:

| Field | Windows 4.20r8 | Mac 4.20r6 |
|---|---|---|
| 1 | `win` | `mac` |
| 2 | MD5 hex of the Windows `DigitalProductId` | hash of the primary Ethernet MAC (IOKit) |
| 3 | MD5 hex of the MAC address (from `UuidCreateSequential`, or `UuidCreate`) | hash of 4 bytes of `stat("/etc")` |
| 4 | MD5 hex of the `C:\` volume serial | empty |

Then id **37** with the language name. So 4.x sends a stable PC id at every login; 2.x and 3.x did not. **[bin]**

## Saved passwords

- Accounts named `guest` or starting with `guest` are never saved. **[bin]**
- The password is stored in the registry under `password` and under `<account>_pass` as `1` followed by 48 characters. The 48 characters are a 24-byte block written as nibbles plus 0x20. The block is a length byte, up to 23 password bytes and random padding, encrypted with libtomcrypt **DES** (three 8-byte blocks). **[bin]**
- The 8-byte DES key is built on the machine: two fixed bytes, four bytes of the MAC address, and two bytes of a byte sum over `DigitalProductId`, each XORed with a constant (fixed fallback bytes when the MAC or the product id is missing). So a saved password only decrypts on the PC that saved it. Compare the 2.22 scheme in `client-internals/saved-passwords.md`. **[bin]**

## Cipher and framing

**Gen 5, the same as 2.22, 2.31 and 3.x.** Both directions are seeded with `0x04A80B38`, the generator is `it = it * 0x08088405 + key`, and the key is a random 0–127 sent in the login. Frames are `u16be length`, a type byte, then the body: under 0x30 bytes type 2 (raw), under 0x1000 type 4 (zlib), otherwise type 6 (bzip2). Type 2 XORs at most 12 dwords and types 4 and 6 at most 4. Packets are `id + 32`, the body and `\n`. **[bin]**

Large packets: before a payload sent as id 93, the client sends id 50 with a 3-byte GINT length (capped at 0x37FFFF). Incoming id 100 sets the length of the next raw (newline-free) packet. **[bin]**

## Server → client ids

**Windows 4.20r8 handles 101 ids:** 0–25, 27–43, 45–49, 67, 68, 69, 74, 75, 82, 84, 100, 101, 102, 104–108, 131–134, 150, 151, 153–156, 165, 166, 168–176, 178–187, 189, 190, 191, 193–196. **[bin]**

Compared with 3.153 (`v3x-clients.md`), nothing is dropped and 13 ids are new. The meanings below come from the handlers; the names follow `packet-ids.md` where it has one.

| id | What the 4.20r8 handler does |
|---|---|
| 105 | Update package size: package name and a 5-byte GINT size. |
| 106 | Update package done: fires `onUpdatePackageDownloaded`, and `onPackagesDownloadComplete` when the last one ends; if the client's own executable was in a package, the client restarts itself. |
| 107 | Board change on a **layer**: layer, x, y (each under 64), width and height (1–64), then two bytes per tile. Layer 0 also clears the level's pending changes. |
| 108 | Two subtypes. 0: the client answers with id **162**, `!` and a 2-byte value. 1: stores a value on the connection. |
| 170 | Ghost mode on or off (`GHOSTMODE`). |
| 182 | The client answers with id **44**: a comma list of the titles of all open windows (`EnumWindows`). |
| 183 | The client checks whether a given string is in that window list and answers. |
| 190 | Fires `onServerListerConnect` (the `Login` server has accepted the session). |
| 191 | A projectile (`SHOOT2`): x, y, z, three angle and speed values, a gani name with optional parameters, then a script string. |
| 193 | A 5-byte GINT time and a file name: the client checks its cached copy (mod time, then CRC). |
| 194 | Clears the client's lists of weapon and class scripts and their name index. |
| 195 | A gani name and gani text: the client loads it as a gani (server-pushed gani scripts). |
| 196 | Same layout as 193; the 4.20r8 handler reads it and does nothing else. |

Mac 4.20r6 handles 97 of these: the same set without 41 and 196 (196 is the newest; 41 may be handled elsewhere in the Mac build). 44 is still missing in both, as in 3.153. **[bin]**

## Client → server ids

Sent from the connection code (provisional, as in 3.x: some sends pass the id in a register): **[bin]**

1, 2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 26, 28, 29, 32, 33, 35, 36, 37, 41, 44, 50, 79, 80, 81, 92, 96, 130, 152, 154, 157, 158, 161, 162.

New compared with what 3.x showed: 44 (the window list for 182), 50 (large-packet length), 157 and 161 (file requests that carry a 5-byte GINT time), 158 (asks for a weapon by name, the `getweapon` path), 162 (the answer to 108). The others match the 2.x/3.x meanings in `packet-ids.md`.

## File formats

| Magic | Notes |
|---|---|
| `GR-V1.00`–`GR-V1.04`, `Z3-V1.03`, `Z3-V1.04`, `GLEVNW01` | Levels. The level loader accepts all of these magics (see `formats/level-binary.md`). No `GR-V1.05` yet: board layers exist on the wire (id 107) but not in the file format. **[bin]** |
| `GSERVL01`, `GWEBL001`, `GRMAP001` | As in 3.x. **[bin]** |
| **`GRPKG001`** | New: the **update package** manifest (`.gupd`). Text lines `NAME`, `FLAG`, `VERSION`, `PLATFORM` (`any`, `win`, `mac`), `ACCOUNTS` (comma list), `MODE`, `SUBPACKAGE` (another `.gupd`), `FILE`, `DESCRIPTION … DESCRIPTIONEND`, `USECHECKSUM`, `ISMAINEXECUTABLE`, `PROTECTOVERWRITE`. Files ending `.exe`, `.lexe`, `.bat` or `.com` get extra checks before they are written; folder names are checked too. Local versions are kept in `localversions.txt`. Ties in with server ids 105, 106, 193 and 196, and with `ExeReplacer` on the Mac. **[bin]** |
| `license.graal`, `sig.*` | See above. |

## Packet logger (third-party build)

**[src][bin]**

- `g4_PackLog.dll` exports `LogIncomingPacket(char*, unsigned)`, `LogOutgoingPacket(char*, unsigned)` and `LogGraalInfo(char*)`. It appends to `Packets_In.log`, `Packets_Out.log` and `Packets_In_and_Out.log` in the working folder. It splits the buffer on `\n` and writes each line as `[id]rest`, with id = first byte − 32. `LogGraalInfo` also writes to `Packets_In.log`, because the source defines the info log name as the same file.
- The hook is in the modified `GraalEngine.dll`. A small block added at the end of the code section loads `g4_PackLog.dll` on first use and looks up the three functions. It calls `LoadLibraryA` and `GetProcAddress` at fixed kernel32 addresses (those of Windows XP SP2), so it works on that one Windows build only. It keeps the three function pointers in spare bytes at the end of `Graal4.exe`'s data section, which only works while the exe loads at its default base.
- Only one call site is wired: the end-of-stream return in zlib's `inflate`. There it logs the engine's shared decompression buffer, with the length taken from the stream's **input** count (the compressed size). In practice:
  - Only incoming **zlib** frames are logged (type 4 and the login reply), already decrypted and decompressed. Raw (type 2) and bzip2 (type 6) frames are not logged.
  - Nothing outgoing is logged. The outgoing and info stubs are in the added block, but nothing jumps to them.
  - Each record is cut to the compressed length, so long packets come out truncated.
  - Any other zlib use (resources decompressed at start-up) fires the hook too.
- The signature-check bypass above is part of the same modification.

## Windows 4.04r2

### How the installer is packed

`Graal4Setup.exe` is a **Thinstall** bundle. Thinstall was Jitit's 2003 application virtualiser, later VMware ThinApp; its stub names itself `X:\thinstall\stub\ts_stub.cc`. It has two layers. **[bin]**

1. **The outer loader.** The PE header's `LoaderFlags` field holds the file offset of a 56-byte table (magic `0x82D0B188`). The table's first record gives the inner stub: offset, mapped size (324 KB) and packed size (101 KB). The loader decodes it into memory, applies relocations, resolves imports and jumps to it. The decoded image has its DOS header blanked except `e_lfanew`. The outer import table keeps only the first import of each DLL of the wrapped Delphi program, as a decoy. `TS_LOADER` in the environment makes the loader read another file.
2. **The inner stub** (Thinstall runtime, linked July 2003). It reads the rest of the table: the file count (151), and the offset, packed size and unpacked size of a compressed directory. The directory holds the runtime settings (install path `%InstallPath%\Graal4`, log `thinstall.log`, `TS_EXECUTE_EXTERNAL`, message strings) and then one record per file: flags, name, data offset, size, two FILETIMEs, an 8-byte hash, and the packed sizes of the file's 64 KB blocks. Fourteen of the records are folders. It then hooks file APIs so the program sees the bundle as real files.

Every block, the stub and the directory included, starts with a tag byte:

| Tag | Coding |
|---|---|
| `0xD9` | stored |
| `0xD7` | a small LZ77 bit-stream coder |
| `0xD8` | the same, then every byte XORed with `0xF0` |
| `0xDE` | an adaptive range coder (the outer stub only) |

In this installer the stub is `0xDE`, the directory is `0xD7`, and the file blocks are 186 × `0xD7` and 46 × `0xD9`. The 137 files come to 7.0 MB. The extraction was checked end to end: `sig.graal` verifies against `Graal4.exe`, `sig.graallib` against `GraalEngine.dll` and `sig.license` against `license.graal`, with the 3.x key. The installer was never run; only its two decoding routines were executed, in a CPU emulator. **[bin]**

### What 4.04r2 ships

- `Graal4.exe` (Delphi launcher), `GraalEngine.dll` (linked 3 March 2006, about 1,650 exports), `fmod.dll` (UPX), `ExeReplacer_temp.exe` (August 2005, the Windows twin of the Mac `ExeReplacer`), and `graalv4_installfiles.txt`, a list of the installed files. **[bin][file]**
- **`Graal3DEngine.dll`** (linked 3 March 2006): the Torque 3D world as a separate DLL. It exports `loadGraal3DEngine`, `runGraal3DEngine` and `endGraal3DEngine`, and imports 623 symbols from `GraalEngine.dll`. Its source paths are `K:\src\graalv4\user\engine\…` (Torque's `console`, `core`, `dgl`, `game/net`, …). So 3D is a plug-in on top of the 2D engine in 4.x; the 4.20r8 packet-logger set does not include this DLL. **[bin]**
- `license.graal` is byte-identical to the Mac 4.20r6 one (`loginserver.graalonline.com:14900`). `levels/`, `levels3d/gui`, `levels3d/help`, `languages3D/` and `sounds/` match the Mac 4.20r6 tree; `pics1.png` is byte-identical. **[file]**

### Protocol and engine differences from 4.20r8

- Same login as 4.20r8, with token `G3D17026`: id 5, key, token, account, password, then `win` and the three MD5s (product id, MAC, `C:\` serial), then id 37. Gen 5, the same framing. **[bin]**
- `GRPKG001` update packages, `localversions.txt`, `onUpdatePackageDownloaded`, `onServerListerConnect` and the window-list answer to 182 are already there in 4.04r2. **[bin]**
- **Server → client: 98 ids**, which is 4.20r8's set without 107 (layered board change), 108 and 196. 4.04r2 handles 100 inside the main switch; 4.20r8 takes 100 and 108 before it. 4.04r2 does handle 41, so the gap in the Mac 4.20r6 set is a Mac quirk. **[bin]**
- Saved passwords: 4.04r2 keeps one `password` value; the per-account `<account>_pass` copies are new in 4.20. **[bin]**
- Engine changes visible in the strings from 4.04r2 to 4.20r8: a separate network thread (`Error creating network thread`), an XML parser (Mini-XML), `GuiBrowserCtrl`, `GuiArrayCtrl`, `GuiStretchCtrl`, reconnect and "cheat window" checks, and a better random generator (`MRandomLCG`). 4.04r2 still has a few 3D-side names in the 2D engine (`getObjectByRay`, `getdatablockvars`, `graal_setGetDatablockProperties`) and a `decryptGraalMemoryDES` routine that 4.20r8 no longer has. **[bin]**

## Open items

- A function-level diff of the 4.04r2 and 4.20r8 engines, and a read of `Graal3DEngine.dll` (its own protocol to 3D servers).
- The ids sent through a register, for a complete client → server list.
- Where the Mac 4.20r6 build handles id 41, if it does.
- A clean, unmodified 4.20r8 `GraalEngine.dll` (the "Unpacked" archive, if its password turns up) to confirm the patch points by diff.
