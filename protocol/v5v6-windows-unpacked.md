# Graal 5.x and 6.x Windows clients, unpacked and run

Date: 2026-10-29

`v5x-clients.md` and `v6x-clients.md` could only identify the packed Windows builds, because both wrappers have to run to unpack. This page covers those ten builds after running them under Wine, dumping them from memory, and capturing their logins against a local listener. Tags: **[bin]** read from the unpacked binaries · **[cap]** seen on the wire from the running client · **[file]** read from bundled files · **[inf]** inferred.

The unpacked files, the bundled game files, the raw captures and the scripts to redo all of it are kept in the project folder under `graal-decompile/unpacked-installers/` (see `README-v5-v6.md` there). They are not in this repo.

## The builds

| Build | Exe date | Wrapper | Bundled files | Engine |
|---|---|---|---|---|
| 5.12 | Oct 19 2007 | MoleBox | 64, incl. `Graal3DEngine.dll` and a signed `license/` | Delphi launcher + `Graal3DEngine.dll` (MSVC, `F:\graallib\…`) |
| 6.00 beta1 | Jan 8 2010 | MoleBox | 65 | one exe (`F:\quattroengine\quattro_lib\…`) |
| 6.00 beta2 | Jan 15 2010 | MoleBox | 65 | one exe |
| 5.24r3 | Jan 22 2010 | MoleBox | 65 | one exe |
| 5.24r4 | Feb 1 2010 | MoleBox | 65 | one exe |
| 5.30r3 | Oct 18 2010 | Themida / WinLicense 2.x | none | one exe |
| 5.31r4 | Jan 5 2011 | Themida / WinLicense 2.x | none | one exe |
| 6.00r2 | Jun 12 2011 | Themida / WinLicense 2.x | none | one exe |
| 6.00r4 | Jun 26 2011 | Themida / WinLicense 2.x | none | one exe |
| 6.03r7 | Nov 16 2012 | Themida / WinLicense 2.x | none | one exe |

Dates are the compile dates in the binaries (`__DATE__` strings and PE timestamps). **[bin]**

- The wrapper on 5.12–5.24 and on the two 6.00 betas is **MoleBox** (its runtime DLL drops as `%APPDATA%\.#\MBX@…###`). It serves the bundled files to the game through hooked file APIs, so they never touch the disk. **[bin]**
- From 5.24 on (and in the 6.00 betas) the Delphi launcher and the separate engine DLL are gone: the game is **one MSVC executable**. The source tree is renamed from `graallib` to `quattroengine\quattro_lib`. **[bin]**
- The Themida builds bundle **nothing**. They start with only the exe and fetch their base files from the server (the first requests are for `basepackage.gupd`, see below). **[cap]**
- The 6.00 betas are older than 5.24r3. 6.00 beta2 even sends the same login token as 5.24r3/r4, so the two lines shared one code base in early 2010. **[bin][cap]**

### Running them

- Stock Wine 9.0 crashes the Themida stub ("An internal exception occured"). The cause is a Wine bug: `VirtualProtect` with a NULL old-protection pointer dereferences it after the call fails, where Windows just returns FALSE. With that patched, Themida runs. **[bin]**
- Named `GraalSetup.exe`, the clients open an install-folder prompt first. Named `Graal.exe` they start the game directly. **[cap]**
- **5.30r3, 5.31r4, 6.00r2 and 6.00r4 have an expiry date.** On the current date they log "This is a beta release of Graal. If it's not working on your computer then please download a new version…" and exit. With the system clock set back to their build month they run normally. The check sits in Themida-virtualised code, so it was not read. 6.03r7 has no such check. **[cap][inf]**

## Login server and license

| Build | Login host | License file |
|---|---|---|
| 5.12 | from `license/license.graal`: `loginserver.graalonline.com`, port 14900, fallbacks `loginserver2`/`loginserver3` | **two files**: `license.graal` + `sig.license`. The bundled signature verifies (RSA-1024, e = 17, PKCS#1 SHA-1, the same key as 3.x–5.00). |
| 5.24r3 and later | the same three hosts, compiled in | none; no `license/` path is referenced any more |

5.00r7 had four license files (`license.graal` plus `sig.graal`, `sig.graallib` and `sig.license`). 5.12 only signs the license text, and from 5.24 the license mechanism is gone. All Windows builds still connect to the game server named `Login` on port 14900. **[bin][file][cap]**

## Login message

Every build logs in by itself as guest once it reaches the login screen. The first frame is the gen-5 login frame: `u16be` length, zlib, no cipher, no compression byte. **[cap]**

`5` + key + token + `GCHAR len` + account + `GCHAR len` + password + a comma list:

```
%kG3D14097%guest(7Y3bdzjfwin,<md5>,<md5>,<md5>,"6.2 9200 "
```

- **The key byte is sent as a GCHAR.** The wire byte minus 32 is the cipher key (`k`, 0x6B, on the wire above means key 0x4B). Wire bytes above 0x7F occur (0x98, 0x99), since the key itself goes up to 0x7F. **[cap]**
- **Guest login:** account `guest`, password **`7Y3bdzjf`** in every Windows build here. This is the plain form of the 8-byte guest password the Linux 6.x builds decrypt at run time. **[cap][inf]**
- **Machine fields:** `win`, then the MD5 hex of the Windows product id, of the network adapter MAC and of the `C:\` volume serial, as in 5.00r7, then **a fifth field**, the quoted Windows version `"<major>.<minor> <build> <service pack>"` (here `"6.2 9200 "`, which is what Windows 8 and later report to an exe without a manifest). The product-id hash differs between 5.12 and 5.24+, because 5.24 also reads `DigitalProductId4`. **[cap][bin]**
- Then **37** (language, `English`), and file requests: **23** `basepackage.gupd` (twice), then `arial.ttf`, `bigmap.txt` or `minimap.txt` depending on the build, and **34** (file request with a modification time) for `guigames_arcmessage2.png`. **[cap]**

### Tokens

| Build | Token | Platform field |
|---|---|---|
| 5.00r7 (from `v5x-clients.md`) | `G3D22067` | `win` |
| 5.12 | **`G3D14097`** | `win` |
| 6.00 beta1 | **`G3D03048`** | `win` |
| 6.00 beta2, 5.24r3, 5.24r4 | **`G3D15010`** | `win` |
| 5.30r3, 5.31r4, 6.00r2, 6.00r4 | **`G3D26090`** | `win` |
| 6.03r7 Windows | **`G3D0311C`** | `win` |
| 6.01r1 Linux (from `v6x-clients.md`) | `G3D0108A` | `linux` |
| 6.03r7 Linux (from `v6x-clients.md`) | `G3D0511C` | `linux` |

- The token belongs to the protocol revision, not the release: four builds over nine months (5.30r3 to 6.00r4) share `G3D26090`. **[cap]**
- The digits read as a day and month shortly before each build (`G3D26090` = 26 Sep for an Oct 2010 build, `G3D15010` = 15 Jan for Jan 2010 builds), matching the 2.x `GNW` tokens. The fifth character is a year digit up to 2010 (7, 8, 0) and a letter in 6.01/6.03. **[inf]**
- **Windows 6.03r7 and Linux 6.03r7 send different tokens** (`G3D0311C` and `G3D0511C`). A server that accepts one does not necessarily accept the other. **[cap][bin]**

## Cipher and framing

Gen 5, unchanged, confirmed by decoding the captures: seed `0x04A80B38`, `it = it*0x08088405 + key`, compression byte after the length, partial XOR of up to 12 dwords (`0x02`) or 4 dwords (`0x04`/`0x06`), one iterator step per group present. Every later frame of all ten captures decodes and decompresses. **[cap]**

5.12 sends even short bodies zlib-compressed (`0x04`); 5.24r3 and later send them uncompressed (`0x02`), like 2.22. **[cap]**

No build here has the 6.11 connector, `setprotocol` or the script-set id tables. LibTomCrypt (RC4, AES and others, "Ciphers built-in") is linked into all of them, including 5.12, but nothing uses it for the game socket. **[bin]**

## Server → client ids

From each build's receive dispatcher (the switch on the packet id that also reaches the `onServerListerConnect` handler, S→C 190).

| Builds | Ids | Set |
|---|---:|---|
| 5.12 | 100 | 0–25, 27–43, 45–49, 67–69, 74, 75, 82, 84, 101, 102, 104–107, 131–134, 140, 150, 151, 153–156, 165, 166, 168–176, 178–187, 189–191, 193–195, 197 (identical to 5.00r7) |
| 6.00 beta1, 6.00 beta2, 5.24r3, 5.24r4 | 97 | 0–25, 27–43, 45–49, 67–69, 74, 82, 84, 101, 102, 104–107, 109, 131, 134, 140, 150, 151, 153–156, 165, 166, 168–170, 172–176, 178–187, 189–191, 194, 195, 197, 198 |
| 5.30r3, 5.31r4 | 95 | as 5.24 without 41 and 181 |
| 6.00r2, 6.00r4 | 93 | as 5.30 without 165 and 169 |
| 6.03r7 | 92 | 0–25, 27–40, 42, 43, 45–49, 67–69, 74, 82, 84, 101, 102, 104–107, 109, 111, 131, 134, 140, 150, 151, 153–156, 166, 168, 170, 172–174, 176, 178–180, 182, 183, 185–187, 189–191, 194, 195, 197, 198 |

**[bin]**

Read in order, the id set changes like this:

- 5.00r7 and 5.12 → 5.24 (and the 6.00 betas): drops 75, 132, 133, 171, 193; adds **109** and **198**. So 109 and 198, first noted in Linux 6.01, are already in the early-2010 Windows builds. **[bin]**
- 5.24r4 → 5.30r3: drops 41 and 181. **[bin]**
- 5.31r4 → 6.00r4: drops 165 and 169. **[bin]**
- 6.00r4 → 6.03r7: drops 175 and 184; adds **111** (writes `creationtime.dat`). The Windows 6.03r7 set is identical to the Linux 6.03r7 set in `v6x-clients.md`. **[bin]**

## File formats and bundled files

- All builds carry `GR-V1.00`–`GR-V1.05`, `GLEVNW01`, `GWEBL001`, `GRMAP001`, `GRPKG001` and `GRESCR01`, as in 5.00r7. 6.03r7 drops the reader strings for `GR-V1.00`–`GR-V1.02` and `GLEVNW01`. **[bin]**
- The MoleBox bundle is the same small base set in every build: GUI skins under `levels3d/gui/` (`guiblue_*`, `default*`, player-list and PM icons, `graalv4title.png`), translations `gui_{en,de,fr}.po` and `guiwindows_{en,de,fr}.po`, `tempsitc.ttf`, `fmod.dll`, `ExeReplacer_temp.exe`, two monster ganis and images, one sound, and the list `graalv4_installfiles.txt` (57 lines, identical in all five builds). **[file]**
- The Themida builds read `graal_installfiles.txt` instead and expect the server to supply the files. **[bin][cap]**

## Still open

- ~~A server reply~~ and ~~client → server ids beyond 5, 37, 23 and 34~~: answered in `v5v6-lab-play.md` (2026-10-30), from runs against a lab server.
- The expiry check itself (Themida VM code).
