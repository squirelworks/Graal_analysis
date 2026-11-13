# iPhone client login tokens

Date: 2026-11-13. A desk check: what is known about the eight-character login token the
iPhone (iOS) Graal clients send, from material already held and from the public
GServer-v2 / gs2lib version tables. No iOS binary has been read, no device was used,
and no public server was contacted.

Tags: **[srv]** read in a server's version table (gs2lib source, or a server binary)
· **[bin]** read from a binary · **[inf]** inferred.

## Answer

Four iPhone tokens are on record. All four come from **server-side version tables**;
none has been read from an iPhone client or seen on the wire. In the catalogue's
grades they are **L** (list only).

| Token | Name in the table | DDMMY stamp | Where it is on record |
|---|---|---|---|
| `G3D04048` | iPhone 1.1 | 04 Apr 2008 | gs2lib since the 2019 split from GServer-v2 (`CLVER_IPHONE_1_1`) **[srv]**; the token-to-name table of the 2010 community gs2emu server (at least its 2.3.1 build of Aug 2010; `server-notes/original-server-builds-1999-2007.md`, "Community servers of 2007–2010") **[bin]** |
| `G3D18010` | iPhone 1.5 | 18 Jan 2010 | gs2lib since 2019 (`CLVER_IPHONE_1_5`) **[srv]**; the gs2emu 2.3.1 (Aug 2010) table **[bin]** |
| `G3D29090` | iPhone 1.11 | 29 Sep 2010 | gs2lib since 2019 (`CLVER_IPHONE_1_11`) **[srv]**; also in the 2024 graalrelay2 copy of gs2lib's table **[srv]** |
| `G3D2504D` | iPhone Belote 1.5 | 25 Apr, "D" year | gs2lib, added upstream 2022-08-30 ("Add client version", `CLVER_IPHONE_BELOTE_1_5`) **[srv]** |

The order in gs2lib's `clientVersions[]` is 1.1, 1.5, 1.11, Belote 1.5 (then `G3D2204D`
Graal Worlds). It is the last block of game-client tokens, after 6.03r7.

`iPhone Belote 1.5` is the upper end of the range one public gs2 server prints in its
refusal (`1.41r1 - iPhone Belote 1.5`, `server-notes/public-allowed-versions.md`). That
shows the token is in at least one live server's table, nothing more.

## What the stamps say **[inf]**

The tokens follow the same `G3D` + DDMMY shape as the desktop 3.x to 6.x clients
(`protocol/login-tokens-3x-7x.md`), and each iPhone stamp falls a day or a few days after
a desktop engine stamp. That fits the pattern already seen for Mac and Linux, where each
platform build of the same engine gets its own stamp a day or so apart:

| iPhone token | Nearest desktop stamps |
|---|---|
| `G3D04048` (iPhone 1.1) | 6.00 beta 1 Windows `G3D03048`, one day earlier |
| `G3D18010` (iPhone 1.5) | 5.24r3/5.24r4/6.00 beta 2 Windows `G3D15010`, three days earlier |
| `G3D29090` (iPhone 1.11) | 5.30r3–6.00r4 Windows `G3D26090`, 6.004 Mac `G3D27090`, 6.x Linux beta `G3D28090`: a run of 26, 27, 28 and 29 Sep |
| `G3D2504D` (iPhone Belote 1.5) | Graal Worlds `G3D2204D`, three days earlier, same year character |

So the iPhone clients are most likely builds of the same C++ engine, stamped from the same
source tree a few days after the desktop builds. "1.11" being later than "1.5" matches the
dates (Jan 2010, then Sep 2010). The 2008 stamp for "iPhone 1.1" predates the App Store,
so it may be the engine base date rather than the app's release; nothing held settles it.
The "D" year character reads as 2013 under the repo's hex-digit reading (A = 2010), but
that reading is itself an inference (`protocol/login-tokens-3x-7x.md`).

"Belote" is a card game, not a Graal world. The table lists it as a client version, so a
Belote iPhone app evidently logged in to Graal-protocol servers; which app that was is
not established.

## What is not known

- **No iPhone client has been read.** There is no IPA, no extracted app bundle and no
  strings dump of an iOS Graal client in the held archives or in this repo. The one
  iPhone-labelled item on record is a 524 KB "iPhone overworld" level RAR in the Classic
  playerworld packs (`archive/game-assets-2026-11-01.md`), which is level data, not a client.
- **Which App Store releases map to which token.** The table names (1.1, 1.5, 1.11) are
  app versions, but which world's app (Classic, Era, Zone, …) each one was is not recorded.
- **Current iOS apps.** From 6.11 on, desktop clients carry no token: the server's
  connector script builds the login (`protocol/connector-script.md`), and the v7 Unity
  clients identify to the connector only by `User-Agent` (`protocol/v7-connector-live-20261111.md`,
  which also records an iOS-specific connector host with a numbered fallback). So a
  present-day iOS app most likely has no stored token, and what it sends depends on the
  script its connector returns. That is **[inf]** until an iOS login is traced.
- **Packet differences.** gs2lib carries one iPhone-specific client packet comment
  (PLI 161, "{INT5 modtime}{name} iPhone client") **[srv]**. Nothing else about the iPhone
  login (type byte, identity trailer, props) is on record.

## How to close it

1. **Read a period IPA.** A legitimately obtained, decrypted IPA of an old iPhone Graal app
   (2009–2013) would let `tools/token-scan/` methods find the token in the connect routine
   (one-character appends up to 6.01, the 6.03 scramble after). That turns an **L** row into **B**.
2. **Capture a device login in the lab.** An old iPhone/iPod running one of those apps,
   pointed at a lab GServer-v2 through a lab DNS override, would put the first login frame
   in the lab server's log. That makes it **W**. Only a lab server; no public server.
3. **Current app.** Tracing the current App Store app's connector exchange on a lab network
   would show whether it sends a token at all and, if so, which. That needs a real device;
   App Store builds are encrypted and cannot be read statically without one.

## Sources

- gs2lib `src/IUtil.cpp` and `include/IUtil.h`: `clientVersions[]`, `clientVersionString[]`
  and the `CLVER_IPHONE_*` enum (upstream history: the three iPhone 1.x entries are present
  at the 2019-05-21 split from GServer-v2; Belote 1.5 added 2022-08-30; Worlds added 2026-01-05).
- graalrelay2 (2024-07) `client/src/IUtil.cpp`: a copy of the older table with the three
  iPhone 1.x entries and no Belote entry.
- `server-notes/original-server-builds-1999-2007.md` (gs2emu 2010 tables).
- `server-notes/public-allowed-versions.md` (the S2 range).
