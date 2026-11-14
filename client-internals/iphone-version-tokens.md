# iPhone client login tokens

Date: 2026-11-13, updated 2026-11-14 with three iPhone binaries read statically. What is
known about the eight-character login token the iPhone (iOS) Graal clients send. No device
was used and no public server was contacted.

Tags: **[bin]** read from a binary · **[srv]** read in a server's version table (gs2lib
source, or a server binary) · **[inf]** inferred.

## Answer

| Token | Read from an iPhone binary | Name in gs2lib | Grade |
|---|---|---|---|
| `G3D04048` | **Belote 1.2 and Belote 1.50** (Quattroplay "Belote Expert Online", 2008) **[bin]** | iPhone 1.1 | **B** |
| `G3D0208A` | **GraalOnline Classic+ 1.13** (2012) **[bin]** | not in the table | **B** |
| `G3D18010` | none read | iPhone 1.5 | L |
| `G3D29090` | none read | iPhone 1.11 | L |
| `G3D2504D` | none read | iPhone Belote 1.5 | L |

Two tokens are now read from real iPhone executables. The other three are still only in
server version tables. GraalOnline Era+ 1.0 was also found but is still App Store encrypted,
so its token could not be read.

Two results correct the table names:

- **`G3D04048` is the Belote app's token**, in both Belote versions read (1.2 and 1.50).
  gs2lib names it "iPhone 1.1". So "iPhone Belote 1.5" (`G3D2504D`) is **not** what
  Belote 1.50 sends. It may be a later Belote build; no binary for it is held.
- **Classic+ 1.13 sends `G3D0208A`, which no server table has.** A GServer-v2 with stock
  gs2lib gives it `CLVER_UNKNOWN`, which no `allowedversions.txt` line or range admits.

## The binaries **[bin]**

All four are public Internet Archive items (the iOS app preservation collection, and one
uploader's collection of the publisher's old apps). Each file's MD5 matched the archive's
listing. They were read statically only, in a cloud container, and never run.

| App | Bundle id | Bundle version | Executable date (zip entry) | Min. iOS / SDK | Encrypted | Token |
|---|---|---|---|---|---|---|
| Belote | `com.quattroplay.BeloteExpertOnline` | 1.2 | 2008-08-14 | n/a / not recorded | no (`cryptid` 0) | `G3D04048` |
| Belote | `com.quattroplay.BeloteExpertOnline` | 1.50 | 2008-10-27 | n/a / not recorded | no | `G3D04048` |
| GraalOnline Classic+ | `com.quattroplay.GraalClassicPlus` | 1.13 | 2012-02-29 | 3.0 / iphoneos4.2 | no | `G3D0208A` |
| Graal Era+ | `com.quattroplay.GraalEraPlus` | 1.0 | 2010-12-01 | 3.0 / iphoneos4.2 | **yes** (`cryptid` 1) | unreadable |

All four are single-slice 32-bit ARM (armv6) Mach-O files with stripped symbols.
Classic+ 1.13's store metadata gives a first release date of 16 Jan 2010 for the app.

**How the token is built.** It is the same connect routine as the desktop C++ engine
(`protocol/login-tokens-3x-7x.md`). The routine logs "Connecting to the game server...",
connects, logs "Done.", then appends eight one-character C strings to an empty string,
one call each. The compiler merged equal strings, so a repeated character is the same
string passed again from a saved register. In Belote the eight appends are `G`, `3`, `D`,
`0`, `4`, then the saved `0` and `4` again, then `8`. That gives `G3D04048`. Classic+ 1.13
appends `G`, `3`, `D`, `0`, `2`, `0`, `8`, `A`. The code is ARM mode, and string
addresses are formed PC-relative from a literal-pool word. The read followed those
literal-pool loads and the stack slots that hold reused characters. The reader is `tools/token-scan/iostok.py`. No scrambled
string (the 6.03 form) and no plain-text token is present in any of the three.

The binaries also contain the strings `GraalEngine`, and `Graal3D` in Belote. That fits
one engine shared with the desktop clients.

## What the stamps say **[inf]**

Each iPhone stamp falls a day to a few days after a desktop engine stamp. That is the same
per-platform pattern the Mac and Linux builds show:

| iPhone token | Nearest desktop stamps |
|---|---|
| `G3D04048` (Belote 1.2, 1.50) | 6.00 beta 1 Windows `G3D03048`, one day earlier. Belote 1.2's executable is dated Aug 2008, so the stamp is the engine's date, not the app's |
| `G3D18010` ("iPhone 1.5") | 5.24r3/5.24r4/6.00 beta 2 Windows `G3D15010`, three days earlier; Classic+ first went on sale on 16 Jan 2010 |
| `G3D29090` ("iPhone 1.11") | 5.30r3–6.00r4 Windows `G3D26090`, 6.004 Mac `G3D27090`, 6.x Linux beta `G3D28090`, one stamp a day from 26 to 29 Sep |
| `G3D0208A` (Classic+ 1.13) | 6.01r1 Linux `G3D0108A`, one day earlier |
| `G3D2504D` ("iPhone Belote 1.5") | Graal Worlds `G3D2204D`, three days earlier, same year character |

`G3D0208A` sits one day after Linux 6.01r1, so the iPhone line followed the 6.01 engine.
Classic+ 1.13 was built with the iOS 4.2 SDK and its executable is dated Feb 2012. That
fits "A" being 2011 better than 2010 (the repo's hex reading in
`protocol/login-tokens-3x-7x.md`), but a stamp can be older than the build, so this does
not settle the year character.

The gs2lib name "iPhone 1.11" probably means Classic+ (or Era+) 1.11, and "iPhone 1.5"
probably an early Classic+ version. Neither has been read.

## What is not known

- Which app and version send `G3D18010`, `G3D29090` and `G3D2504D`.
- Era+ 1.0's token: the copy found is encrypted.
- Present-day iOS apps. From 6.11 on, desktop clients carry no token, because the
  connector script builds the login (`protocol/connector-script.md`). The v7 clients
  identify only by `User-Agent` (`protocol/v7-connector-live-20261111.md`). A current iOS
  app most likely has no stored token **[inf]**.
- Anything else about the iPhone login: type byte, identity trailer, props. gs2lib has one
  iPhone packet comment, PLI 161 ("{INT5 modtime}{name} iPhone client") **[srv]**.

## How to close it

1. **More decrypted IPAs.** Any other old Classic+, Era+, Zone+ or Belote build would let
   the same read place `G3D18010`, `G3D29090` and `G3D2504D` (grade **B**).
2. **Lab capture.** An old iPhone or iPod running Belote or Classic+ 1.13, pointed at a lab
   GServer-v2 with a lab DNS override, would put the first login frame in the lab server's
   log. That would make these rows **W**. Use only a lab server, never a public one.
3. **Android cross-check.** The Android Classic packages (`android-classic.md`) come from
   the same mobile line, and Android binaries are not encrypted. A connect-routine read of
   their engines would show whether they send a token too.

## Sources

- Internet Archive items, read 2026-11-14: Belote 1.2 and 1.50 and GraalOnline Classic+ 1.13
  (iOS app preservation collection); Graal Era+ 1.0 (a collection of the publisher's old apps).
- gs2lib `src/IUtil.cpp` / `include/IUtil.h` (`clientVersions[]`, `CLVER_IPHONE_*`). The
  three "iPhone 1.x" entries are present at the 2019-05-21 split from GServer-v2. Belote 1.5
  was added 2022-08-30 and Worlds 2026-01-05.
- graalrelay2 (2024-07) `client/src/IUtil.cpp`, a copy of the older table.
- `server-notes/original-server-builds-1999-2007.md` (gs2emu 2010 tables), and
  `server-notes/public-allowed-versions.md` (the "1.41r1 - iPhone Belote 1.5" range).
