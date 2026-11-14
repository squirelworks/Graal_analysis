# iPhone client login tokens

Date: 2026-11-13, updated 2026-11-14 with 26 iPhone binaries from the same publisher read statically. What is
known about the eight-character login token the iPhone (iOS) Graal clients send. No device
was used and no public server was contacted.

Tags: **[bin]** read from a binary · **[srv]** read in a server's version table (gs2lib
source, or a server binary) · **[inf]** inferred.

## Answer

| Token | Read from an iPhone binary | Name in gs2lib | Grade |
|---|---|---|---|
| `G3D04048` | **16 builds of 2008–2010**: Belote 1.2/1.50, Adrenaline Poker 1.2/1.60, Adrenaline Pool 1.1/1.5, AlloWin Pool 1.0/1.1, AlloWin Pumpkins 1.0, Ace Tennis 1.1/1.2/1.3, Alien Abuse 1.3, Dino Smash 1.2, Cocoto Kart Online 1.0, Bomber Online 1.20 **[bin]** | iPhone 1.1 | **B** |
| `G3D18010` | **6 builds of 2010–2013**: Cocoto Magic Circus 1.0, Cocoto Kart HD 1.1, Ace Tennis HD 1.0, Cocoto Kart Online 1.3, Bomber Online 1.40, Dino Smash 1.4 **[bin]** | iPhone 1.5 | **B** |
| `G3D0208A` | **GraalOnline Classic+ 1.13** (2012) **[bin]** | not in the table | **B** |
| `G3D29090` | none read | iPhone 1.11 | L |
| `G3D2504D` | none read | iPhone Belote 1.5 | L |

Three tokens are now read from real iPhone executables. The other two are still only in
server version tables. GraalOnline Era+ 1.0 was also found but is still App Store encrypted,
so its token could not be read.

**The iPhone tokens name engine generations, not apps.** The same publisher shipped about a
dozen iPhone games on the Graal C++ engine (card, pool, tennis, kart, arcade), and every one
of them logs in with the engine's token. `G3D04048` is the 2008 engine and `G3D18010` the
2010 one. An app keeps its engine's token across updates, and a later build can still be
on the old engine: AlloWin Pool 1.1 (Sep 2010) sends `G3D04048`, while Dino Smash 1.4 (May
2013) sends `G3D18010`. Cocoto Kart Online crosses over: 1.0 (Oct 2009) sends `G3D04048` and
1.3 (Jun 2010) sends `G3D18010`. So gs2lib's "iPhone 1.1" and "iPhone 1.5" are best read as engine
1.1 and 1.5. Classic+ 1.13 (`G3D0208A`) is on a later, 6.01-era engine.

Two results correct the table names:

- **Belote 1.50 sends `G3D04048`** (gs2lib's "iPhone 1.1"), like every 2008 build. So
  "iPhone Belote 1.5" (`G3D2504D`) is **not** what Belote 1.50 sends. It may be a later
  Belote build; no binary for it is held.
- **Classic+ 1.13 sends `G3D0208A`, which no server table has.** A GServer-v2 with stock
  gs2lib gives it `CLVER_UNKNOWN`, which no `allowedversions.txt` line or range admits.

## The binaries **[bin]**

All are copies of the official downloads that we hold. They were read statically only, in
a cloud container, and never run. Every one ships the Graal C++ engine (the `GraalEngine`
string), and all but Era+ are unencrypted.

| App | Version | Executable date (zip entry) | Token |
|---|---|---|---|
| Adrenaline Poker Online | 1.2 (two copies) | 2008-08-14 | `G3D04048` |
| Belote (Expert Online) | 1.2 | 2008-08-14 | `G3D04048` |
| Adrenaline Pool Online | 1.1 | 2008-10-10 | `G3D04048` |
| AlloWin Pool | 1.0 | 2008-10-23 | `G3D04048` |
| Belote (Expert Online) | 1.50 | 2008-10-27 | `G3D04048` |
| Ace Tennis Online | 1.1 | 2008-11-21 | `G3D04048` |
| Ace Tennis Online | 1.2 | 2008-12-01 | `G3D04048` |
| Adrenaline Poker Online | 1.60 | 2008-12-13 | `G3D04048` |
| Adrenaline Pool Online | 1.5 | 2008-12-24 | `G3D04048` |
| Ace Tennis Online | 1.3 | 2009-02-22 | `G3D04048` |
| Alien Abuse | 1.0 | 2009-03-17 | none: no connect routine (offline build) |
| Alien Abuse | 1.1 | 2009-03-29 | none: no connect routine (offline build) |
| Alien Abuse | 1.3 | 2009-06-24 | `G3D04048` |
| Dino Smash | 1.2 | 2009-09-26 | `G3D04048` |
| Cocoto Kart Online | 1.0 | 2009-10-02 | `G3D04048` |
| Bomber Online | 1.20 | 2009-12-22 | `G3D04048` |
| Cocoto Magic Circus | 1.0 | 2010-03-03 | `G3D18010` |
| Cocoto Kart HD Online | 1.1 | 2010-05-03 | `G3D18010` |
| Ace Tennis HD Online | 1.0 | 2010-05-26 | `G3D18010` |
| Cocoto Kart Online | 1.3 | 2010-06-23 | `G3D18010` |
| Bomber Online | 1.40 | 2010-09-17 | `G3D18010` |
| AlloWin Pool | 1.1 | 2010-09-20 | `G3D04048` |
| AlloWin Pumpkins | 1.0 | 2010-09-20 | `G3D04048` |
| Graal Era+ | 1.0 | 2010-12-01 | encrypted (`cryptid` 1), unread |
| GraalOnline Classic+ | 1.13 | 2012-02-29 | `G3D0208A` |
| Dino Smash | 1.4 | 2013-05-16 | `G3D18010` |

All are single-slice 32-bit ARM (armv6) Mach-O files with stripped symbols. Classic+ and
Era+ were built with the iOS 4.2 SDK, and Classic+ 1.13's store metadata gives a first
release date of 16 Jan 2010 for the app.

**How the token is built.** It is the same connect routine as the desktop C++ engine
(`protocol/login-tokens-3x-7x.md`). The routine logs "Connecting to the game server...",
connects, logs "Done.", then appends eight one-character C strings to an empty string,
one call each. The compiler merged equal strings, so a repeated character is the same
string passed again from a saved register. In the 2008 builds the eight appends are `G`, `3`, `D`,
`0`, `4`, then the saved `0` and `4` again, then `8`. That gives `G3D04048`. Classic+ 1.13
appends `G`, `3`, `D`, `0`, `2`, `0`, `8`, `A`. The code is ARM mode, and string
addresses are formed PC-relative from a literal-pool word. The read followed those
literal-pool loads and the stack slots that hold reused characters. The reader is `tools/token-scan/iostok.py`. No scrambled
string (the 6.03 form) and no plain-text token is present in any of them.

The binaries also contain the strings `GraalEngine`, and `Graal3D` in Belote. That fits
one engine shared with the desktop clients.

## What the stamps say **[inf]**

Each iPhone stamp falls a day to a few days after a desktop engine stamp. That is the same
per-platform pattern the Mac and Linux builds show:

| iPhone token | Nearest desktop stamps |
|---|---|
| `G3D04048` (2008 engine) | 6.00 beta 1 Windows `G3D03048`, one day earlier. The first builds are dated Aug 2008, so the stamp is the engine's date, not the app's |
| `G3D18010` (2010 engine) | 5.24r3/5.24r4/6.00 beta 2 Windows `G3D15010`, three days earlier. The first build read is dated Mar 2010 |
| `G3D29090` ("iPhone 1.11") | 5.30r3–6.00r4 Windows `G3D26090`, 6.004 Mac `G3D27090`, 6.x Linux beta `G3D28090`, one stamp a day from 26 to 29 Sep |
| `G3D0208A` (Classic+ 1.13) | 6.01r1 Linux `G3D0108A`, one day earlier |
| `G3D2504D` ("iPhone Belote 1.5") | Graal Worlds `G3D2204D`, three days earlier, same year character |

`G3D0208A` sits one day after Linux 6.01r1, so the iPhone line followed the 6.01 engine.
Classic+ 1.13 was built with the iOS 4.2 SDK and its executable is dated Feb 2012. That
fits "A" being 2011 better than 2010 (the repo's hex reading in
`protocol/login-tokens-3x-7x.md`), but a stamp can be older than the build, so this does
not settle the year character.

gs2lib's "iPhone 1.11" (`G3D29090`) would then be engine 1.11, stamped in Sep 2010, and is
the likeliest token for Era+ 1.0 (built Dec 2010). That is unread.

## What is not known

- Which builds send `G3D29090` and `G3D2504D`.
- Era+ 1.0's token: the copy found is encrypted.
- Present-day iOS apps. From 6.11 on, desktop clients carry no token, because the
  connector script builds the login (`protocol/connector-script.md`). The v7 clients
  identify only by `User-Agent` (`protocol/v7-connector-live-20261111.md`). A current iOS
  app most likely has no stored token **[inf]**.
- Anything else about the iPhone login: type byte, identity trailer, props. gs2lib has one
  iPhone packet comment, PLI 161 ("{INT5 modtime}{name} iPhone client") **[srv]**.

## How to close it

1. **More decrypted IPAs.** An unencrypted Era+, Zone+ or later Classic+ or Belote build would
   let the same read place `G3D29090` and `G3D2504D` (grade **B**). Two searches for copies of the
   official downloads found no other build from this publisher: no Checkers Online, Adrenaline
   Golf, Poker Online, Scorched 3D, Zone, Zone+, or later Classic+ or Belote.
2. **Lab capture.** An old iPhone or iPod running Belote or Classic+ 1.13, pointed at a lab
   GServer-v2 with a lab DNS override, would put the first login frame in the lab server's
   log. That would make these rows **W**. Use only a lab server, never a public one.
3. **Android cross-check.** The Android Classic packages (`android-classic.md`) come from
   the same mobile line, and Android binaries are not encrypted. A connect-routine read of
   their engines would show whether they send a token too.

## Sources

- Copies of the official downloads we hold: the 26 builds in the table above.
- gs2lib `src/IUtil.cpp` / `include/IUtil.h` (`clientVersions[]`, `CLVER_IPHONE_*`). The
  three "iPhone 1.x" entries are present at the 2019-05-21 split from GServer-v2. Belote 1.5
  was added 2022-08-30 and Worlds 2026-01-05.
- graalrelay2 (2024-07) `client/src/IUtil.cpp`, a copy of the older table.
- `server-notes/original-server-builds-1999-2007.md` (gs2emu 2010 tables), and
  `server-notes/public-allowed-versions.md` (the "1.41r1 - iPhone Belote 1.5" range).
