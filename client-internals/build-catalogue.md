# Client build catalogue (1998–2001)

Date: 2026-10-21

This covers every client in the uploaded archive set: 39 top-level archives plus 16 from the second upload, 55 in total.
There are 52 Delphi client executables, the Graal3D side project, and the 1998 Java precursor.
Everything here comes from static reads of the binaries (PE headers, resources, strings, and immediates in the code)
and from the release notes shipped beside each exe. Nothing in this file comes from a decompiler.

## How each column was read

| Column | Source |
|---|---|
| MD5 / size | The exe as shipped in the archive. |
| Compiled | The resource-directory timestamp, a DOS date/time that Delphi sets at link time, in local time. The COFF timestamp is useless for these builds because every Delphi build carries the fixed 1992-06-19 value. |
| FileVersion | The VERSIONINFO resource. It only exists from 1.37 on and is sometimes stale (2.05 still says 2.0.4.0). |
| Token | The login version string. Up to 1.37 it is a plain string literal. From 1.38 on it is built one character at a time, so `strings` misses it, and it has to be read from the immediates passed to the char-to-string helper. |
| Gen | The encryption generation, using the GServer-v2 numbering. 1 means no compression. 2 means zlib with no encryption (a `nodecompressionerror` option exists). 3 means zlib plus the one-byte LCG insertion (see `protocol/` codec notes). Gen 3 is detected by the connection-object initialiser storing seed `0x04A80B38` and then the `Random & 0x7F` key. Two other uses of the same seed (web-level cache file encryption, from 1.3 on) are excluded. |
| Server / list | 1.39 and earlier: the default host:port the connect dialog is pre-filled with (no listserver support). 1.4x and later: the listserver host:port and the list name sent after connecting. |
| Levels | Which level and map magics the loader compares against. `Z3-V` is `.zelda`, `GR-V` is `.graal`, `GLEVNW01` is `.nw`, and `GRMAP001` is `.gmap`. `Graalsav` is the save-game magic. |

## Catalogue

Sorted by compile date. "Archive" is the archive file name without `.7z`.

| Archive | Release name | Compiled | FileVersion | MD5 | Size | Token | Gen | Server / list | Levels and saves | Notable |
|---|---|---|---|---|---|---|---|---|---|---|
| zeldaonline2 | Zelda Online (Java applet) | 1997–98 | – | – | – | none | text lines | host:14801 | `Z3-V1.02`/`1.03` | Java predecessor, see `zelda-online-1998.md` |
| 1stgraal-1 | first Delphi beta | 1998-09-06 23:54 | – | 07452f8941fdfcdce878b035156e701c | 654336 | none | 1 | 127.0.0.1:14801 | Z3-V1.03/1.04 only; Graalsav1 | Two-player local game, no `.graal` loader yet, no DirectSound |
| 2ndgraal | beta | 1998-09-16 01:33 | – | f74b35fc7975a4873087f7fd2aa1d79b | 777216 | none | 1 | 127.0.0.1:14801 | + GR-V1.00–1.01; Graalsav1 | First `.graal` loader |
| 3rdgraal | beta | 1998-09-30 01:47 | – | fc78fbc96bdbc6ca22ae56d3ed8635ab | 665600 | none | 1 | 127.0.0.1:14801, dialog 14802 | GR-V1.00–1.01; Graalsav1 | Connect dialog gains a second port field (14802) |
| 4thgraal | beta | 1998-10-05 01:33 | – | e040af2e19912419ab80aa6dd202b4ea | 666112 | none | 1 | as above | GR-V1.00–1.01; Graalsav1 | |
| 4thgraalalpha | beta (alpha) | 1998-10-12 22:54 | – | 8cae23a58e1b1b10f3149bdbe53d0431 | 711680 | none | 1 | 127.0.0.1:14801 | GR-V1.00–1.01; Graalsav2 | Built after 4thgraal despite the name; DirectSound appears |
| 5thgraal | beta | 1998-10-19 02:27 | – | 0e7c3573f0a916f8b2376060e768fe96 | 723968 | none | 1 | 127.0.0.1:14801, dialog 14802 | GR-V1.00–1.02; Graalsav2 | GR-V1.02 |
| 5thgraalalpha | beta (alpha) | 1998-10-29 02:21 | – | e54397e7d4f59d30b77d5cf0475335a1 | 739840 | none | 1 | 127.0.0.1:14801 | GR-V1.00–1.02; Graalsav2 | Built after 5thgraal |
| 6thgraal | beta5 | 1998-11-09 02:08 | – | 53c3caf3d930534db3f44f346f5d651a | 750080 | none | 1 | 127.0.0.1:14801, dialog 14802 | GR-V1.00–1.02; Graalsav3 | Published by Cyberjoueur; web levels from cyberjoueur.com |
| 7thgraal | beta7 | 1998-12-04 00:28 | – | deb40c31268e499fc4436b8d0687f05d | 766976 | none | 1 | as above | GR-V1.00–1.03; Graalsav4 | First GR-V1.03 (the last `.graal` revision any build here reads) |
| 8thgraal | beta8 | 1998-12-08 01:13 | – | a49aa1b773e41741f211867fd5ea55d7 | 775680 | none | 1 | as above | GR-V1.00–1.03; Graalsav4 | |
| 9thgraalalpha | beta9 (alpha) | 1998-12-16 02:36 | – | e226e1b83fd437b0aede968fb395b911 | 788992 | none | 1 | as above | GR-V1.00–1.03; Graalsav5 | Built before 9thgraal |
| 9thgraal | beta9 | 1998-12-18 01:53 | – | f0185ff8525a13f2f4e5997f649bc250 | 793088 | none | 1 | as above | GR-V1.00–1.03; Graalsav5 | |
| 10thgraal | V1.0 | 1998-12-22 03:24 | – | f1f34b4479a8ad7614bd8f7ce56112c6 | 795648 | none | 1 | as above | GR-V1.00–1.03; Graalsav5 | 1.0 final: map heads, Alt+1/2 screenshots, Alt+3 minimap |
| 11thgraal | V1.0 | 1998-12-23 01:00 | – | a255212621907affc94a4483c6dfc8e3 | 795648 | none | 1 | as above | GR-V1.00–1.03; Graalsav5 | Adds the altern.org RealWorld web level |
| 12thgraal | V1.0 | 1999-01-05 01:04 | – | 788ae59e9419806024d14d3e5b611971 | 794624 | none | 1 | as above | GR-V1.00–1.03; Graalsav5 | |
| 13thgraal | V1.1 beta1 | 1999-01-12 01:15 | – | a211a0ecf3b58daa2f46759444e18bd3 | 797184 | none | 1 | as above | GR-V1.00–1.03; Graalsav6 | `this.` vars, canbepushed/pulled, sleeping/sitting, `.gsave` |
| 14thgraal | V1.1 | 1999-01-15 02:20 | – | d0999d44fcd9c226f350fcf204618885 | 858112 | none | 1 | as above | GR-V1.00–1.03; Graalsav7 | |
| 15thgraal | V1.1 | 1999-01-25 00:12 | – | 9a7d66dd5c8c506ad4d3e63ee4a9a1f1 | 878592 | none | 1 | as above | GR-V1.00–1.03; Graalsav7 | Faster script interpreter, IP caching, `puthorse` boats |
| graal1.1.9 | V1.1.9 Gold Edition | 1999-02-11 23:50 | – | 0a6eef88acb4c0fce6e84eee3e76c04a | 882176 | none | 1 | as above | GR-V1.00–1.03; Graalsav7/8 | Ships `Gserver.exe` (1999-01-22, port 14802, no token); home moves to graalonline.com |
| graal1.1 | V1.1 (readme) | 1999-02-14 23:03 | – | 1a9580655cce686c602c01daa251c453 | 882176 | none | 1 | as above | GR-V1.00–1.03; Graalsav7/8 | Same size as 1.1.9 but linked 3 days later |
| graal121 | V1.2.1 | 1999-05-10 18:29 | – | 8da2e8284dd8b315a28e2d4fccae79ac | 973824 | `GSERV007` | 2 | www.graalonline.com:14804 | GR-V1.00–1.03; reads Graalsav9/Graalsv10/Graalsv11, writes Graalsv11 | InstallShield 3 package (the exe is inside `_SETUP.1`); "packet compression" (zlib 1.0.4); NPC weapons; GServer and RC on the same token |
| graal128b2 | v1.28 beta2 | 1999-11-23 01:09 | – | 8e3c1a7233864da994a0db26f1811212 | 1196544 | `GSERV013` | 2 | www.graalonline.com:14804 | GR-V1.00–1.03; reads Graalsav9/Graalsv10/Graalsv11, writes Graalsv11 | "Direct data packages" (positions sent straight to room players); ships GServer (accepts GSERV007–013) and RC 1.28 (GSERV011) |
| graal13b | v1.3 test | 1999-11-29 02:03 | – | b62aaa4d606a519e7f4689b33983429b | 1311744 | `GSERV014` | 2 | www.graalonline.com:14804 | GR-V1.00–1.03; reads Graalsav9/Graalsv10/Graalsv11, writes Graalsv11 | Alignment system; levels cached on disk (web-level cache seed first appears); ships GServer13 (accepts 007–014) |
| graal131 | V1.31 | 1999-12-07 02:56 | – | bff87a95a34399b2d35b243f281169a7 | 1318400 | `GSERV016` | 2 | www.graalonline.com:14900 | GR-V1.00–1.03; reads Graalsav9/Graalsv10/Graalsv11, writes Graalsv11 | Default port moves to 14900; UDP options (`noudp`, fixed port 14899) |
| graal132 | V1.32 | 2000-01-12 01:13 | – | 42b2596af4b75bcf82db03e0fc274f7d | 1328128 | `GSERV018` | 2 | www.graalonline.com:14900 | GR-V1.00–1.03; reads Graalsav9/Graalsv10/Graalsv11, writes Graalsv11 | Double-click fullscreen |
| graal3d | Graal3D | 2000-02-05 01:57 | – | 305c985a020cec6ab8d81ac95d447343 | 605184 | none | own | 127.0.0.1:14901 (UDP 14898) | none | Separate 3D client plus its own GServer.exe (14901); zlib linked, no Graal level loaders |
| graal133 | V1.33 | 2000-02-21 00:36 | – | a3667ce55a5c67cf025882014b9540b0 | 1350144 | `GNW20020` | 2 | www.graalonline.com:14900 | GR-V1.00–1.03; carries Graalsav9/Graalsv10/Graalsv11 (string scan) | First GNW token; PNG support; 4-section player list |
| graal134 | V1.34 | 2000-03-23 00:38 | – | 9e403616e73a6079ac37d65d475c81cd | 1349632 | `GNW22030` | 2 | as above | GR-V1.00–1.03; carries Graalsav9/Graalsv10/Graalsv11 (string scan) | Script debugger (F6); MNG appears |
| graal135 | V1.35 | 2000-04-13 23:17 | – | fe9d99c4bf6e6bc9b1b127823f39646f | 1389568 | `GNW13040` | 2 | as above | GR-V1.00–1.03; carries Graalsav9/Graalsv10/Graalsv11 (string scan) | |
| graal136 | V1.36 | 2000-05-12 17:34 | – | 018f51662c7c8862cafb9bfbd14dea41 | 1399296 | `GNW10050` | 2 | as above | GR-V1.00–1.03; carries Graalsav9/Graalsv10/Graalsv11 (string scan) | Server player cap 220 → 28000; nickname limit |
| graal137 | V1.37 | 2000-05-23 02:40 | 1.3.7.0 | 5e966a9d1a079af6d682b2618674edb1 | 1401344 | `GNW21050` | 2 | as above | GR-V1.00–1.03; carries Graalsav9/Graalsv10/Graalsv11 (string scan) | First VERSIONINFO; new sound-effects system |
| graal138 | V1.38 | 2000-06-23 22:11 | 1.3.8.0 | 4401f7d02966af709c2df662cebe34a1 | 1426432 | `GNW22060` | 2 | as above | GR-V1.00–1.03; carries Graalsav9/Graalsv10/Graalsv11 (string scan) | Token now built char by char; `setnick`, `warpto` |
| graal139 | V1.39 | 2000-08-07 02:49 | 1.3.8.0 | 62513ab884f1802a0bcd8114abe349b9 | 1448960 | `GNW07080` | 2 | as above | GR-V1.00–1.03; carries Graalsav9/Graalsv10/Graalsv11 (string scan) | New head-image handling; profiles. FileVersion not bumped |
| graal_gr1411 | V1.41 rev1 (graal.in-patched copy) | – (resource stamp missing) | 1.4.1.1 | a97740e711ffe9b698ec03712d4c06af | 1506816 | `GNW13110` | **3** | list `listserver.graal.in`:14923 | GR-V1.00–1.03, GLEVNW01; carries Graalsav9/Graalsv10/Graalsv11 (string scan) | First server-list window (from 1.4) and first gen 3 build. See the note below on the patching |
| graalnm24 | NewMain client (1.42 notes) | 2001-01-10 19:55 | 1.4.1.1 | 229f05de7a43b98e223d8e1b58bffc63 | 1783296 | `GNW08011` | 3 | list www.graalonline.com:14921, "newmain" (plain) | GR-V1.00–1.03, GLEVNW01 | First `.gani` animation system; ships GraalShop and RC-NewMain (GSERV021) |
| graalnm26 | NewMain client (1.42 notes) | 2001-01-12 21:19 | 1.4.1.1 | 22a08ed154f67948e01b969b68cdb05e | 1784320 | `GNW08011` | 3 | as above | GR-V1.00–1.03, GLEVNW01 | Adds GraalLevelGen 1.0 |
| Graal-v2.0 | v2.00 | 2001-02-01 14:54 | 2.0.0.0 | c93e659e2cda36379aaea4706db20b38 | 1812480 | `GNW24011` | 3 | list www.graalonline.com:14921, "newmain" (host DES-hidden) | GR-V1.00–1.03 (no `.nw`) | No 2/3/4-player mode; tutorial levels; server-side bush rupees. First DES-hidden list host |
| Graal-v2.0-rev1 | v2.00 rev1 | 2001-02-02 19:19 | 2.0.0.1 | 30bd230e578d3a347866a87060efec20 | 1812992 | `GNW24011` | 3 | as above | as above | |
| Graal-v2.0-rev2 | v2.00 rev2 | 2001-02-05 02:32 | 2.0.0.2 | fc4bb7e3b7ca9cd8ea6693a033635534 | 1815040 | `GNW24011` | 3 | as above | as above | |
| Graal-v2.0-rev3 | v2.00 rev3 | 2001-02-07 01:05 | 2.0.0.3 | 1ce5c1662b65246ae1c6559af5ff71f0 | 1815040 | `GNW24011` | 3 | as above | as above | |
| Graal-v2.01 | v2.01 | 2001-03-08 14:59 | 2.0.1.0 | 08340a8868f1d11e0285cc70e51200fe | 1815552 | `GNW23021` | 3 | as above | as above | Level preloading on the map; showimg fixes |
| Graal-v2.01-rev1 | v2.01 rev1 | 2001-03-15 21:10 | 2.0.1.0 | 010a32afce66729b838258809a97c0d9 | 1815552 | `GNW23021` | 3 | as above | as above | |
| Graal-v2.02 | v2.02 | 2001-04-15 20:48 | 2.0.2.0 | 60018a19ef671c506743826728c49718 | 1808384 | `GNW15041` | 3 | as above | as above | Hats; HTML window navigation |
| Graal-v2.02-rev1 | v2.02 rev1 | 2001-04-15 23:16 | 2.0.2.0 | e06ff79aded885a223b933617d456577 | 1808896 | `GNW15041` | 3 | as above | as above | Speed-cheat protection; client language sent to server |
| Graal-v2.02-rev2 | v2.02 rev2 | 2001-04-20 18:48 | 2.0.2.2 | 993a1829dbb6acaa2b46063f5efe636c | 1807872 | `GNW20041` | 3 | as above | as above | |
| Graal-v2.03 | v2.03 | 2001-05-07 15:31 | 2.0.3.0 | 36972c74baad09ceb33dad94b0eb1e33 | 1836032 | `GNW06051` | 3 | as above | as above | `triggeraction`, `move`; NPC-server support |
| Graal-v2.04 | v2.04 | 2001-06-25 07:42 | 2.0.4.0 | a40608308d4f890cb5e4efdd45b38ba4 | 1872384 | `GNW24061` | 3 | as above | as above | `replacegani`, `addtiledef`/`addtiledef2` |
| Graal-v2.05 | v2.05 | 2001-08-03 19:12 | 2.0.4.0 (stale) | 9abce477945a1307bb2be9ed47d2f170 | 1891328 | `GNW03081` | 3 | as above | GR-V1.00–1.03, **GLEVNW01, GRMAP001** | `.nw` and `.gmap` return; script-editor button; `setshape2` arrays |
| Graal-v2.05-rev1 | v2.05 rev1 | 2001-08-04 03:26 | 2.0.5.0 | 2780f2f370396c580e1648696698c871 | 1895936 | `GNW03081` | 3 | as above | as above | |
| graalnwb1 | NewWorld beta 1 | 2001-08-06 04:13 | 2.0.5.0 | 88d1f84c96da1dcc3942b139fbd741c9 | 1820672 | `G2N15041` | 3 | list www.graalonline.com:14921, "newworld" (DES) | as 2.05 | String arrays, terrain heights; ships NPCControl, LevelFiller, TerrainGenerator, Greaditor and other tools |
| Graal-v2.05-rev2 | v2.05 rev2 | 2001-08-16 17:24 | 2.0.5.2 | f3fdf54d943fa91c89acba5bb695db99 | 1891840 | `GNW03081` | 3 | list www.graalonline.com:14921, "newmain" (DES) | as 2.05 | The decompile target; same bytes as `Graal_v2.05_rev2.exe` |
| graal21test2 | v2.1 test 2 | 2001-09-21 17:54 | 2.1.0.0 | d15d877822ad4145578107857c90fb3c | 1748480 | `GNW03081` | 3 | list www.graalonline.com:**14922**, "newmain" (DES) | as 2.05 | New tiles, new starting window; the token is still 2.05's |
| graal21test3 | v2.1 test 3 | 2001-09-27 21:11 | 2.1.0.0 | 2116a7ba03648dcc004035534ec94de8 | 1753600 | `GNW03081` | 3 | as above | as 2.05 | |
| graalnwb2 | NewWorld beta 2 | 2001-10-03 20:46 | 2.1.0.0 | af2d21066659bed6af6c77e52b2cc0e1 | 1613824 | `G2N15041` | 3 | list www.graalonline.com:14922, "newworld" (DES) | as 2.05 | |

## Patterns worth knowing

**The GNW token is a build date.** It is `GNW` followed by DDMMY, with Y being the last digit of the year.
Every build from 1.33 to 2.05 fits, and the token date is on or a few days before the link date:
GNW20020 is 20 Feb 2000 (1.33, linked 21 Feb), GNW07080 is 7 Aug 2000 (1.39, linked 7 Aug), and GNW03081 is 3 Aug 2001 (2.05, linked 3 Aug).
A rev that does not touch the protocol keeps the previous token (2.0 rev1–3, 2.01 rev1, 2.02 rev1, 2.05 rev1–2), and so does the 2.1 test line.
So an unmapped token like GNW30123 can be read as 30 Dec 200x, which probably points to a 2.1-era build, since 2.1.0.x is known to use GNW31101.

**Before GNW, the token was a protocol revision.** `GSERVnnn` went 007 (1.21), 011 (RC 1.28), 013 (1.28b2), 014 (1.3 test), 016 (1.31), 018 (1.32), and 021 (RC-NewMain, Jan 2001).
The bundled GServers accept a range rather than one token: GServer 1.28 accepts GSERV007–013 and GServer13 accepts 007–014.

**Encryption generations by build.**

| Gen | Builds | How it was determined |
|---|---|---|
| 1 | 1st Graal through 1.1.9 | No zlib linked; no decompression-error option |
| 2 | 1.21 through 1.39 | zlib 1.0.4 linked; the 1.2 notes say "packet compression"; `nodecompressionerror` from 1.28b2 |
| 3 | 1.41 rev1, NewMain 1.42, all 2.0x, 2.1 tests, NW betas | Connection initialiser seeds the insertion LCG with `0x04A80B38` and a 7-bit random key. 1.39 lacks it |

**Server discovery.** 1.39 and earlier have no listserver: the connect dialog is pre-filled with a host:port and the player edits it.
The defaults were 127.0.0.1:14801 for the 1998 betas through 1.1.9, www.graalonline.com:14804 for 1.21–1.3 test, and www.graalonline.com:14900 for 1.31–1.39.
The server-list window arrives with 1.4. NewMain 1.42 writes host, port and list name as plain char-by-char strings.
From 2.0 the host is DES-hidden with the bit-reversed key described in the 2.05 notes. The key and ciphertext are the same in every 2.0x build and decrypt to `www.graalonline.com`.
The list name chooses the main list ("newmain") or the NewWorld list ("newworld"). The port moves from 14921 to 14922 with the 2.1 test builds.

**The 1.41 rev1 copy is patched.** It contains both "Graalonline.com Server List" and "Graal.in Server List", `www.graal.in` register and homepage links, and `listserver.graal.in:14923`.
Its resource-directory timestamp is zeroed, which is what a resource editor leaves behind.
This is the only 1.41 copy available, so the listserver host and port it shows may not be the original 1.41 values. The token (GNW13110 = 13 Nov 2000) and the code-level facts look untouched.

**`.nw` support is not monotonic.** NewMain 1.42 (Jan 2001) and the 1.41 rev1 copy contain the GLEVNW01 loader, but 2.00–2.04 contain no GLEVNW01 or GRMAP001 string, even as char-built strings.
Both reappear in 2.05 (Aug 2001) together with gmap support. This suggests 2.0 branched from a pre-NewMain tree and the NewWorld code was merged back for 2.05.
That conclusion is an inference from strings only. A live check (loading a `.nw` level in 2.04) would confirm it.

**Save magics after 1.1.9.** 1.21 to 1.32 write `Graalsv11` (with `sav` shortened to `sv` so the magic stays 9 characters) and read `Graalsav9` and `Graalsv10` too. A search for `Graalsav` misses the last two. 1.33 to 1.39 and the 1.41 rev1 copy carry the same three magic strings, but only a string scan was done for those builds, so which one they write isn't confirmed. See `formats/graalsav.md`.

**Compiler.** Every build is Borland Delphi with linker 2.25, DelphiX for DirectDraw, and an RTL copyright reading "1983,97 Borland".
Two compilers are in use, and the class metadata tells them apart. In the older layout the VMT self pointer sits 64 bytes before the VMT and the class name 32 bytes before it, which is the Delphi 2 layout. In the newer layout those offsets are 76 and 44, which is the layout from Delphi 3 on.
Only 2nd Graal and 1.28 beta 2 onwards use the newer layout. They also link `TMultiReadExclusiveWriteSynchronizer`, which arrived in SysUtils with Delphi 4, so they are Delphi 4 builds.
1st Graal, 3rd Graal to 1.1.9, and 1.21 use the older layout and lack that class. Their exact compiler is unresolved: the layout says Delphi 2, but the RTL string "1983,97" is a year late for Delphi 2. A Delphi-2-level compiler shipped in 1997, such as C++Builder 1's, would fit both, but that hasn't been checked.
Either way the switch to Delphi 4 happened between 1.21 (May 1999) and 1.28 beta 2 (Nov 1999), and 2nd Graal is an outlier built with the newer compiler.
(An earlier version of this note said every build from 2nd Graal on has the class. A per-build check shows otherwise.)

**Archive naming vs build order.** The "Nth graal" archive names are not strictly chronological. 4thgraalalpha and 5thgraalalpha were linked after their non-alpha namesakes, and 9thgraalalpha before 9thgraal.
`graal1.1` and `graal1.1.9` have identical sizes, but graal1.1 was linked three days after the Gold Edition.

## Other executables in the archives

| Archive | File | Compiled | MD5 | Token | Port |
|---|---|---|---|---|---|
| graal1.1.9 | Gserver.exe | 1999-01-22 | 7882dba6ebb2ab1026de260c3043fa47 | none | 14802 |
| graal121 | GServer.exe | 1999-05-09 | bfcdaae0217d953124a9b21ff7858967 | GSERV007 | 14804 |
| graal121 | remotecontrol.exe | 1999-05-10 | 5932d6baa08289a65515342dfc4b9f5a | GSERV007 | 14804 |
| graal128b2 | GServerv.exe | 1999-11-22 | 8d6bff85bda6e6c9558503afa6b7259d | accepts GSERV007–013 | 14804 |
| graal128b2 | RemoteControl1.28.exe | 1999-10-20 | d7150d1385ea11b812d10d30212f9757 | GSERV011 | 14804 |
| graal13b | GServer13.exe | 1999-11-29 | d1d0470e53a60b8f000b9ea5da9d37b6 | accepts GSERV007–014 | 14804 |
| graal13b | RemoteControl13.exe | 1999-11-29 | 1f2c19ab385c8b8af6236197f98ad735 | GSERV011 | 14804 |
| graal3d | GServer.exe | 2000-02-05 | aab1a34a1f196d4f4fddf12112ccbf52 | none | 14901 |
| graalnm24/26 | RemoteControl-NewMain.exe | 2001-01-08 | bc2b8a2e80acc09a6bb418970cff5a64 | GSERV021 | 14804 |
| graalnwb1 | RemoteControl-NW.exe | 2001-05-22 | 6fe24bdd4e135900fc40d7fb70bdcdd2 | – | 14804 |
| graalnwb2 | RemoteControl-NW.exe | 2001-08-27 | ce454437af8880f61ac2173b0bd11047 | – | 14804 |

Also present: gif2mng (2000-06-12, identical in every archive that has it), GraalShop (gani editor, 2000-12 and 2001-04), GraalLevelGen and GraalLevelGenNW, NPCControl (2001-07-13),
LevelFiller with levelviewer, TerrainGenerator, PNGView, YoshiChess, and Greaditor (UPX-packed).
