# How the 3.x to 7.x clients identify themselves at login

Date: 2026-11-11. This note pulls together what other notes in this repo already establish. It adds no new lab run. Every claim links to the note that holds the evidence, and the tags there still apply.

## The question

The question was whether clients from 3.x on build their version token differently from the 1.x and 2.x clients. They do not. Every client from 1.33 to 6.03 sends a fixed, eight-character token that names its build. The client does not compute it from anything at run time: no hash, no seed and no field from the server[^const]. What changed after 2.x is the token's prefix and where the token sits in the login. From 4.x the login also carries a machine identity. From 6.11 the client has no token of its own, because the server's connector script builds the login. So a client such as Ato can carry the token as a constant per profile, plus the right type byte and identity trailer, for every build up to 6.03.

## The token itself

The token is three letters and a five-character date stamp. The prefix is `GSERV` up to 1.32, `GNW` from 1.33 to 2.31, and `G3D` on every build from 3.0 on, including the 2D-only Windows and Linux builds of 4.x to 6.x[^tokens]. The date stamp is DDMMY: day, month, then one year character. It falls a little before each build's release[^date]. Up to 2009 the year character is the last digit of the year. From 2010 it is a letter: `A` in the 6.01 tokens (`G3D3007A`, `G3D0108A`) and `C` in the 6.03 tokens (`G3D2505C`, `G3D0311C`, `G3D0511C`). That reads as the year as a hex digit (A = 2010, C = 2012), but it is an inference from the dates[^date]. The community wiki's release dates back both readings: Windows 4.04 came out on 17 February 2006 (`G3D17026`), 4.206 on 21 December 2006 (Windows 4.20r8 sends `G3D20126`), 5.1 on 17 September 2007 (`G3D14097`, kept by 5.12), and 6.036 on 4 November 2012 for Windows and 10 November for Linux (`G3D0311C`, `G3D0511C`). A bug-fix release can keep the stamp of the release before it. The Mac 4.20r6 stamp `G3D27076` is the 4.1 release day, five months before 4.206 reached the Mac; why is open[^wiki].

The 3.x tokens reuse the 2D date stamps. 3.04 sends `G3D03014`, the same stamp as 2.22's `GNW03014`, and 3.153 sends `G3D28015`, the same as 2.31's `GNW28015`. 3.04 speaks the 2.22 protocol and 3.153 the 2.31 protocol, so the prefix is the only part of the token that changes[^v3]. From 4.x the stamp is the build's own date again[^v4].

Each platform build has its own stamp. Windows 4.04r2 sends `G3D17026` and Linux 4.04r2 sends `G3D19026`. Windows 4.20r8 sends `G3D20126`, Mac 4.20r6 sends `G3D27076`, and both Linux 4.20 builds send `G3D22126`. For 6.03r7, Windows sends `G3D0311C` and Linux sends `G3D0511C`[^lnx][^v6]. A server must list each platform's token, not one per version.

How the token is stored is the one real change, and it only affects static reading. Up to 6.01 the client builds the token one character at a time from immediates or one-character globals, so no string literal exists. That holds for the Delphi 2.x clients and for the C++ 3.x to 6.01 engines alike[^v3][^v5][^v6]. 6.03 stores it as one scrambled lower-case string (`g3d0511c`), decoded and upper-cased at run time[^v6][^hello]. Neither form changes the bytes on the wire.

## Reading the token from a file

The token can be read from the binary without running the client. This section records the method, the scripts and the builds it has been checked on. It was first worked out on 2026-11-11 from decompiles. That write-up stayed on an unmerged branch, and this section replaces it.

**Where the token is made.** Every build makes the login in one place, the game connection's connect routine. That routine logs "Connecting to the game server...", opens the socket, and logs "Done." if the connect worked. Straight after that it builds the token, then the login, sends them as id 5, and sends id 37 (language). Nothing else touches the token. **[bin]**

| Build | How the routine builds the token |
|---|---|
| 2.x Delphi | `_LStrFromChar` eight times with character immediates (`mov bl, imm8`, then `lea eax,[ebp-..]`, `mov edx,ebx`, call) |
| 3.04 Linux, 3.153 Mac | Eight appends of one-character C strings (`"G"`, `"3"`, `"D"`, …) to an empty `JString` |
| 4.04r2 and 4.20r8 Windows (`GraalEngine.dll`), 4.20r6 Mac | Eight `JString::operator<<` calls, each with a one-character global string. The linker can merge equal strings, so one global may be appended twice (4.20r8 has two `"2"`s) |
| 5.00r7, 5.12 Windows (`Graal3DEngine.dll`) | Eight one-character globals |
| 6.01r1 Linux | `"G"` plus seven one-character strings |
| 6.03r7 Linux and Windows | One scrambled eight-byte lower-case string, decoded and upper-cased (below) |
| 6.11 and later | No stored token; see "6.11 and 7.x" |

**The 6.03 scramble.** It is a per-byte transform that depends on the string length *n* and the byte position *i*. To decode byte *b*: take its bitwise NOT, add −10 − *n*, rotate the low byte right by two bits, then subtract *i*, all modulo 256. To encode, run the steps backwards: add *i*, rotate left by two, add 10 + *n*, then take the NOT. The stored bytes `50 1d 54 21 09 15 11 44` decode to `g3d0511c` (Linux 6.03r7), and `50 1d 54 21 11 15 11 44` in the unpacked Windows 6.03r7 decode to `g3d0311c`. A live gdb run of Linux 6.03r7 showed the routine decode this string, upper-case it and send it **[lab]**. To test a build for a token you expect, encode the token and search for the bytes.

**Scripts** (in [tools/token-scan/](../tools/token-scan/)):

- `conntok.py` reads Linux ELF clients from 3.x to 6.01, 32-bit and 64-bit, non-PIE. It finds the code references to "Connecting to the game server", then lists in order the one-character strings that the next 3000 bytes point at. It follows absolute 32-bit operands and, on x64, RIP-relative `lea`. The first eight characters are the token. UPX-packed 3.x files need `upx -d` first.
- `machotok.py` reads Mac OS X clients (Mach-O, thin or universal) with the same connect-routine method. On PowerPC it tracks `lis`/`addis`/`addi`/`ori`, the `bcl`+`mflr` base and loads through globals to resolve each one-character string. On x86_64 it follows RIP-relative `lea`. It falls back to the 6.03 decoder.
- `g3dref.py` reads the Windows engine DLLs, `GraalEngine.dll` in 4.x and `Graal3DEngine.dll` in 5.x, and also reads 32-bit ELF files. It maps every one-character string in the data sections, collects the code operands that point at them, groups those operands into runs, and matches `G3D` + `DDMMY`. Run it on the engine DLL. The Delphi launcher (`Graal.exe` / `Graal4.exe` in 4.20r8 to 5.12) holds no token.
- For the 2.x Delphi clients, the character-immediate scan in [graal2002-and-140-builds.md](../client-internals/graal2002-and-140-builds.md) applies.
- Packed Windows 4.x clients: the 4.03r3, 4.04r2 and 4.11 `Graal4Setup.exe` downloads are Thinstall 2.x packages that hold the whole client. A memory image taken under Wine reads with the same connect-routine method. Since 2026-11-13 the files can also be unpacked without running anything ([tools/thinstall-unpack](../tools/thinstall-unpack/)), and `g3dref.py` on the unpacked `GraalEngine.dll` gives the same tokens: 4.03r3 `G3D09125`, 4.04r2 `G3D17026` (the wire token) and 4.11 `G3D26076` ([note](v4x-windows-403r3-411.md)).

**Checked against tokens seen on the wire** (2026-11-13): Linux 4.04r2 `G3D19026`, Linux 4.20r6 and 4.20r8 (2007-01-17) `G3D22126`, Linux 6.01r1 x86 and x64 `G3D0108A`, Windows 4.04r2 `G3D17026`, Windows 4.20r8 `G3D20126`, Windows 5.12 `G3D14097`. All match. Linux 3.0beta and 3.01 also give the listed `G3D16053` and `G3D27063`.

**New reads** (2026-11-13, from copies of the official downloads; all in the [catalogue](../client-internals/version-token-catalogue.md)): Linux 3.151 `G3D27015`, Linux 4.03r1 `G3D11125`, Linux 4.10r2 and 4.11 `G3D28076`, Linux 4.20r8 (2007-01-15) `G3D22126`, the June 2011 Linux beta (x86 and x64, probably 6.00r4) `G3D28090`, Windows 4.03r3 `G3D09125` and Windows 4.11 `G3D26076` (both from the memory image), and the public Windows 2.1.0.0 `GNW31101`. Mac (Mach-O, same connect-routine method; PPC addresses followed through register pairs): 4.10r2 `G3D27076`, 4.20r6 (2006-12-21) `G3D21126`, 6.004 `G3D27090`, 6.015 `G3D3107A`. This Mac reader was first checked against the wire tokens of Mac 4.04r2 `G3D18026`, 5.12 `G3D15097` and the 2006-09-19 build `G3D27076`. Linux 4.11 and Windows 4.11 send different tokens, as other platform pairs do. The Mac and Windows 6.015 tokens, and the Mac 6.004 and Linux beta tokens, differ by one day.

## Where the token sits in the login

The first byte of the login is a client-type number, and the server uses it to pick the cipher. GServer-v2 reads it as a bit index: type 0 is the classic client (gen 2, or gen 3 when a key follows), type 4 is the 2.19 to 2.21 and 3.0 to 3.01 clients (gen 4), and type 5 is 2.22 and later (gen 5)[^gs2]. In the 2.05 era the login starts with type 0, then the gen-3 key byte, then the token[^walk]. Every 3.04 to 6.03 client starts with type 5, then a key byte (`rand & 0x7F`), then the token. The whole login goes in one frame in fixed mode 3: zlib, no cipher and no type byte. After it the socket switches to the gen-5 cipher, seeded `0x04A80B38` in both directions[^v3][^v4][^v6]. Earlier notes call this byte "login id 5". It is the same byte.

Account and password follow as GCHAR-length strings. 3.x sends them as plain strings and stops there. 3.x does not send a tamper check (PLI 39) after login, though 2.22 and 2.31 do[^v3].

From 4.x a comma-separated machine identity follows the password, as a string that runs to the end of the message[^v4][^v5]:

- Windows 4.x and 5.00r7: `win`, then MD5 hex of `DigitalProductId`, of the MAC address and of the `C:\` volume serial.
- 5.12 and later Windows builds add the quoted Windows version as a fifth field.
- Mac 4.20r6: `mac`, a hash of the Ethernet MAC, a hash of `stat("/etc")`, and an empty field.
- Linux 6.x: MD5 hex of the `eth0` MAC, MD5 hex of the inode number of `/etc`, an empty field, and the kernel release and version.

GServer-v2 stores only the first field (the platform) and passes the whole string on to its listserver[^gs2]. Every 3.x to 6.03 build then sends PLI 37 (language).

## The listserver and the Login server

3.x is the last generation with a separate listserver protocol. 3.04 and 3.153 send listserver id 7, a key byte and `G3D30123newmain`, which is 2.22's `GNW30123newmain` with the new prefix. Id 1 (account, password) follows in the same plain zlib frame, and the reply is gen 5. The host and port come from the RSA-signed `license.graal`, which names a host on port 14922[^v3][^tiger]. No `G3D30123` login has been tried against a public listserver yet, so the port status for 3.x stays "assumed"[^p3x].

From 4.x there is no listserver protocol. The client reads a host from `license.graal`, still RSA-signed and now on port 14900, and logs in to it as an ordinary game server named `Login`, with the game login above. That server sends the server list and the account screens as scripted GUI, and S→C 190 raises `onServerListerConnect`[^v4][^v5]. 6.01 and 6.03 keep this, but compile the hosts in, scrambled, and read no license file[^v6]. While the server name starts with "login", 4.x to 6.x clients draw no characters and no HUD. A server ends that mode with S→C 178 (server warp) to a server with another name[^play].

## 6.11 and 7.x

6.11 asks an HTTP connector for `conf.gs` and runs the reply as `StartScript_Connector`. That script picks the protocol and the cipher, connects to the game server and builds the login with `senddata`. So 6.11 has no fixed token. The token, packet ids, header and cipher are whatever the server's script says[^v6][^lion]. A lab replay later read one such script: it sends `GNP1905C` as a literal with `sendRaw`, after `setProtocol("EILLLT")` (see [v6-login-token-explained.md](v6-login-token-explained.md)). The 7.x clients use the same connector bootstrap; their framing and packet tables are in the `v7-graal3d-*` notes[^v7].

## Are the G3D clients 3D?

Only some of them. The `G3D` prefix runs from 3.0 to 6.03, but the Torque 3D side runs from 3.04 to 5.12[^wire]:

| Build | 3D side | Torque protocol |
|---|---|---|
| 3.04 Linux | the whole client is Torque, stock TGE networking, no 3D scripts shipped | 9 (`Torque Game Engine Demo`) |
| 3.153 Mac | Graal-changed TGE: class table in the accept, datablocks | 19 |
| 4.04r2 Windows | `Graal3DEngine.dll`, loaded the first time a 3D server is picked | 19 |
| 4.20r6 Mac | `GameObject` layer, no datablocks | 21 |
| 5.00r7, 5.12 Windows | `Graal3DEngine.dll` 5.0.0.7, `GameObject` layer | 24 |
| 5.24r3 and later | none; only the `GuiGraal3DCtrl` class name is left | — |

A server is 3D when its list name starts with `"3 "`. Picking one opens two connections to the same host: the normal Graal TCP login on the listed port, and a Torque UDP connection on port + 1. The 3D side lives only as long as the TCP session. The Torque connect request carries the game string `Graal3D`, the protocol twice, the account password in clear as the join password, and two arguments: account and nickname. The class CRC is a static `0xFFFFFFFF`, and the server sends its class names in the accept instead[^net][^g3d4]. A real 5.12 client got as far as "Connection established" against a small lab responder[^net].

One outside report agrees with this. A third-party C# gserver author said on Discord that a 5.007 client gets scripted 3D content from their server, over TCP on the gserver port and UDP on port + 1, and that Graal3D was gone from v6. The binaries put the cut a little earlier, at 5.24r3[^wire]. That server's source is not public, so it is cited here as a report only.

The Graal3D of February 2000 is a different program. It is a DirectX client with its own server on TCP 14901 and `GR3DV00x` tokens, and it shares nothing with the Torque side[^g3d2000].

## Open points

- [ ] Try the 3.x `G3D30123` listserver login against a public listserver on 14922, then 14923, to settle the "assumed" port status. Owner approval is needed for a public login (see `AGENTS.md`).
- [ ] Read the join password and arguments that 3.153 and 4.20r6 put in their Torque connect request. Both are still "not traced"[^net].
- [ ] Find a 3.0 or 3.01 binary. Their tokens (`G3D16053`, `G3D27063`) and the type-4, gen-4 login are known only from gs2lib's table[^gs2].
- [ ] Confirm, with build dates, that the 2010+ year character is a hex digit.
- [ ] The Torque game layer after the accept: the `GameObject` property map, the rotation packing, and the movement and shape payloads[^wire].

## Notes

[^const]: [version-tokens.md](../client-internals/version-tokens.md), the "Confirmed from the binaries" table; [version-id-map.md](../client-internals/version-id-map.md), "Construction (v2.05)".
[^tokens]: [version-id-map.md](../client-internals/version-id-map.md), the token table and the gs2lib table; [version-tokens.md](../client-internals/version-tokens.md).
[^date]: [v4x-clients.md](v4x-clients.md), "Version tokens"; [v5v6-windows-unpacked.md](v5v6-windows-unpacked.md), the paragraph after the token table **[inf]**.
[^v3]: [v3x-clients.md](v3x-clients.md), sections 3 and 4.
[^v4]: [v4x-clients.md](v4x-clients.md), "Version tokens", "Login packet" and "Login server and `license.graal`".
[^v5]: [v5x-clients.md](v5x-clients.md), "Login".
[^v6]: [v6x-clients.md](v6x-clients.md), "Login server", "Login message (6.01 and 6.03)" and "6.11 Mac".
[^lnx]: [linux-local-login-matrix.md](linux-local-login-matrix.md) and its JSON; first-frame observations on a lab GServer-v2.
[^hello]: [v6037-hello-diff.md](v6037-hello-diff.md).
[^gs2]: GServer-v2 (`squirelworks/seihai-gserver-v2`), `PlayerClient::handleLogin`; gs2lib (`squirelworks/seihai-gs2lib`), `PLTYPE_*` in `IEnums.h` and the token table in `IUtil.cpp`. Both are GPL; summarised, not copied.
[^walk]: [login-and-walk.md](login-and-walk.md); [session-opcodes-cleaned.md](session-opcodes-cleaned.md).
[^tiger]: [lab-304-linux-2026-10-30.md](../version-profiles/lab-304-linux-2026-10-30.md); [lab-mac-tiger-2026-10-31.md](../version-profiles/lab-mac-tiger-2026-10-31.md).
[^p3x]: [3.04-3.153.md](../version-profiles/3.04-3.153.md).
[^play]: [v5v6-lab-play.md](v5v6-lab-play.md), "The 'Login' server mode".
[^lion]: A Lion 10.7.5 lab run of 6.11r1 on 2026-11-11 (owner-held record) saw the HTTPS attempt, then the HTTP `conf.gs` request with `User-Agent: Graal/6.111`, as the static notes predict.
[^v7]: [v7x-protocol.md](v7x-protocol.md); [v7-graal3d-framing-and-packet-tables.md](v7-graal3d-framing-and-packet-tables.md); [v7-graal3d-identity-and-builds.md](v7-graal3d-identity-and-builds.md).
[^wire]: [wire-by-build.md](../torque/wire-by-build.md), "Which builds are Torque" and "The handshake per build"; [g3d-5007.md](../torque/g3d-5007.md), "Protocol window".
[^net]: [network.md](../torque/network.md).
[^g3d4]: [torque-engine-4x.md](../graal3d/torque-engine-4x.md).
[^wiki]: [graal-wiki-crosscheck-2026-11-11.md](../client-internals/graal-wiki-crosscheck-2026-11-11.md), "Release dates against the login-token date stamps" **[doc][bin]**.
[^g3d2000]: [graal3d/README.md](../graal3d/README.md); [graal3d/protocol.md](../graal3d/protocol.md).

## Bibliography

- Graal_analysis notes: `protocol/v3x-clients.md`, `v4x-clients.md`, `v5x-clients.md`, `v5v6-windows-unpacked.md`, `v5v6-lab-play.md`, `v6x-clients.md`, `v6037-hello-diff.md`, `linux-local-login-matrix.md`, `login-and-walk.md`, `codec-and-framing.md`, `v7x-protocol.md`; `client-internals/version-tokens.md`, `version-id-map.md`; `version-profiles/3.04-3.153.md`, `lab-304-linux-2026-10-30.md`, `lab-mac-tiger-2026-10-31.md`; `torque/network.md`, `wire-by-build.md`, `g3d-5007.md`; `graal3d/torque-engine-4x.md`, `README.md`, `protocol.md`.
- `squirelworks/seihai-gserver-v2`, `server/src/player/PlayerClient.cpp` (GPL-3.0).
- `squirelworks/seihai-gs2lib`, `include/IEnums.h`, `src/IUtil.cpp` (GPL-3.0).
- Discord report by the author of a private C# gserver, relayed by the owner on 2026-11-11 (no public source).
