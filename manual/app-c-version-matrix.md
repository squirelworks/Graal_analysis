<!-- manual: kind=reference status=draft -->
# Appendix C. Version matrix

Build and era names are defined in → §1.1 and → §1.6. Each cell points back to the canonical section; behaviour rules by build (timing, movement, combat, death) are tabulated in → §4.1 to → §4.4 and are not repeated here.

## C.1 Wire and scripting by era

| Era | Login token | Cipher gen | Message ids handled or sent | Props parsed | Scripting | Source |
| --- | --- | --- | --- | --- | --- | --- |
| Z | none | text lines (→ §2.3.1) | text lobby lines | n/a | none | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| A | none | 1 (no zlib) | relay lobby `N`, `P`, `C`, `D` lines; `D` payload types per build | relay `D` types | GS1-like; `this.` variables from 1.1 beta1 | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting); [bin] (client-internals/version-profiles/v1998-v11.toml) |
| B | `GSERV007` to `GSERV018` | 2 (zlib, no cipher) | GSERV id ranges (→ §2.3.2) | unmeasured | GS1; NPC weapons from 1.21 | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| 3D0 | `GR3DV002` | own (2D codec, no key byte) | own renumbered ids (→ §9) | 3D floats, 24-bit colours | none | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| C | `GNW20020` to `GNW07080` | 2 | 1.33: S→C 0–41, 100; C→S 0–31; 45 and 35 ids by 1.39 | own 0–33/34, others 21–23 ids | GS1, 88 to 111 commands | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting); [bin][doc] (client-internals/versions-133-139.md#protocol-changes) |
| D | `GNW13110` | 3 | 1.41 additions (→ C.2) | props to 36 | GS1, 126 commands | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| E | `GNW08011` to `GNW03081`; NewWorld `G2N15041` | 3 | 2.05: 59 S→C ids | to 42 (2.05) | GS1, 134 to 161 commands; ganis from 1.42 | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| F | `GNW31101` (2.1) to `GNW22122` (2.17) | 3 | 2.17: 79 S→C, 61 C→S; TAMPERCHECK (39) from 2.17 | to 74 (gani attributes from 2.16) | GS1 and gani scripts (2.1); `this.` client strings (2.19) | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| G | `GNW03014`, `GNW14015`, `GNW28015`; listserver `GNW30123` | 5 (compression byte, partial XOR, bz2) | 2.22: 80; 2.31: 81 | to 74 (2.22); 80 with X2/Y2/Z2 (2.31) | GS1; classic client-side NPC mode removed in 2.3 | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| H | `G3D03014`, `G3D28015`; listserver `G3D30123` | 5 | 79 (3.04); 88 (3.153) | as G | GS1 native, TorqueScript `.dso` for menus; NPC bytecode ids (3.153) | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| I | `G3D17026`, `G3D27076`, `G3D20126` | 5 | 98 to 101 | unmeasured | GS2 bytecode; server-pushed ganis (195); update packages `GRPKG001` | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| J | `G3D22067`, `G3D14097`, `G3D15010`, `G3D26090` | 5 | 95 to 100 | unmeasured | GS2; `GRESCR01` script cache; anti-cheat process scan (182, 183) | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| K | `G3D0108A`, `G3D0511C` (Linux), `G3D0311C` (Windows 6.03); 6.11 set by script | 5; 6.11 can switch to a script-defined header with RC4, AES or TLS | 91 to 97 | unmeasured | GS2; in 6.11 the packet id tables come from the server script (→ §2.10) | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |

Login-time extras a client must send: `PLI_LANGUAGE` (37) from 2.02 rev2 [bin] (version-profiles/matrix/README.md#thinks-wire-and-scripting); `PLI_TAMPERCHECK` (39) once per session in 2.17, on gmap crossings and level links in 2.22, and every 3.2 s in 2.31 [cap] (version-profiles/matrix/README.md#thinks-wire-and-scripting); machine-id MD5s after the password from 4.x on [bin] (version-profiles/matrix/README.md#thinks-wire-and-scripting). Server discovery by era is in → §6.

## C.2 Server-to-client ids handled, 1.33 to 2.1 tests

Ids are logical (→ §0.7) and count only ids that reach a real handler.

| Build | Change | Source |
| --- | --- | --- |
| 1.33 to 1.37 | 43 ids: 0–41, 100 | [bin] (client-internals/cross-version-timeline.md#server--client-packets) |
| 1.38 | + 43 | [bin] (client-internals/cross-version-timeline.md#server--client-packets) |
| 1.39 | + 75 (45 ids: 0–41, 43, 75, 100) | [bin] (client-internals/cross-version-timeline.md#server--client-packets) |
| 1.41 rev1 | same set as 1.39 | [bin] (client-internals/cross-version-timeline.md#server--client-packets) |
| NewMain 1.42 | + 42, 44, 45, 150, 151, 153 | [bin] (client-internals/cross-version-timeline.md#server--client-packets) |
| 2.0 | + 154, 155 | [bin] (client-internals/cross-version-timeline.md#server--client-packets) |
| 2.01 | + 46, 156 | [bin] (client-internals/cross-version-timeline.md#server--client-packets) |
| 2.02 rev2 | + 47 | [bin] (client-internals/cross-version-timeline.md#server--client-packets) |
| 2.03 | + 48, 165 | [bin] (client-internals/cross-version-timeline.md#server--client-packets) |
| 2.04 | + 166; − 26 | [bin] (client-internals/cross-version-timeline.md#server--client-packets) |
| 2.05 rev1, rev2 | + 168 | [bin] (client-internals/cross-version-timeline.md#server--client-packets) |
| NewWorld betas | 2.05 minus 2, 4, 17, 18, 154, 155 | [bin] (client-internals/cross-version-timeline.md#server--client-packets) |
| 2.1 tests | 2.05 plus 49, 169 | [bin] (client-internals/cross-version-timeline.md#server--client-packets) |

Later builds: → §2.5 and the per-build tables in `version-profiles/plo-handled-ids-by-build.tsv`, which App. A indexes.

## C.3 Prop parsers

| Parser | 1.33 | Added later | Source |
| --- | --- | --- | --- |
| player props | 0–33 [inf] | 34 (1.39); 35, 36 (1.41); 37–41 (2.02 rev2); 42 (2.04); 43–45 (2.1 tests) | [bin][inf] (client-internals/cross-version-timeline.md#prop-parsers) |
| NPC props | 0–34 [inf] | 35 (1.41); 36–40 (2.02 rev2); 41–43 (2.1 tests) | [bin][inf] (client-internals/cross-version-timeline.md#prop-parsers) |
| baddy props | 0–10 | none; the parser is gone in both NewWorld betas | [bin] (client-internals/cross-version-timeline.md#prop-parsers) |
| sparse player-prop sub-parser | 21 ids up to 51 | 23 ids (1.39); 31 ids (2.05); role unconfirmed, likely props of other players | [bin][inf] (client-internals/cross-version-timeline.md#prop-parsers) |

The 1.33 player/NPC split is assumed from 1.34, where the player parser is the one that calls the sparse sub-parser [inf] (client-internals/cross-version-timeline.md#prop-parsers). Prop encodings: → §2.6.

## C.4 UDP ids handled

| Build | Ids | Source |
| --- | --- | --- |
| 1.33 to 1.37 | 0, 10–23 | [bin] (client-internals/cross-version-timeline.md#udp-packets) |
| 1.38 | + 24 | [bin] (client-internals/cross-version-timeline.md#udp-packets) |
| 2.01 | + 25 | [bin] (client-internals/cross-version-timeline.md#udp-packets) |
| 2.03 | + 26 | [bin] (client-internals/cross-version-timeline.md#udp-packets) |
| 2.1 tests | + 27 | [bin] (client-internals/cross-version-timeline.md#udp-packets) |
| NewWorld betas | drop 16, 17 | [bin] (client-internals/cross-version-timeline.md#udp-packets) |

UDP messages: → §2.9.

## C.5 GS1 command table size

| Build | Commands | Added | Source |
| --- | ---: | --- | --- |
| 1.33 | 88 | — | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 1.34 | 93 | `dontblocklocal`, `blockagainlocal`, `showlocal`, `hidelocal`, `carryobject`, `throwcarry`, `setbacktile`; `seteffect` and `unseteffect` leave the table | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 1.35 | 93 | same table as 1.34 | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 1.36 | 104 | `lay2`, `take2`, `takehorse`, `takeplayerhorse`, `removebomb`, `removearrow`, `removeitem`, `removeexplo`, `removehorse`, `explodebomb`, `reflectarrow`; `lay` takes arguments | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 1.37 | 106 | `playlooped`, `stopsound` | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 1.38 | 109 | `setlevel2`, `changeimgpart`, `hitnpc`; `setlevel` takes arguments | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 1.39 | 111 | `setani`, `setcharani` | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 1.41 rev1 | 126 | `canwarp`, `callnpc`, `say2`, `break`, `continue`, `callweapon`, `spyfire`, `function`, `return`, `changeimgvis`, `setimg`, `setimgpart`, `drawovertrees`, `putexplosion2`, `showstats`; `putexplosion` takes arguments | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| NewMain 1.42 | 134 | `canwarp2`, `setshape`, `seteffect`, `setcoloreffect`, `setzoomeffect`, `drawaslight`, `changeimgcolors`, `changeimgzoom` | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 2.0 | 142 | `setgender`, `setchargender`, `join`, `freezeplayer2`, `unfreezeplayer`, `enabledefmovement`, `disabledefmovement`, `setmusicvolume` | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 2.01 | 144 | `openurl2`, `hitobjects`; `openurl` takes arguments | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 2.02 rev2 | 146 | `tokenize`, `tokenize2` | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 2.03 | 148 | `triggeraction`, `move` | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 2.04 | 157 | `addtiledef`, `addtiledef2`, `removetiledefs`, `replaceani`, `attachplayertoobj`, `detachplayer`, `setshape2`, `enableselectweapons`, `disableselectweapons`; `setshape` takes arguments | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 2.05 rev1, rev2 | 161 | `setbacktile2`, `setz`, `updateterrain`, `loadmap`; `setbacktile` takes arguments | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 2.1 tests | 161 | same table as 2.05 | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| NewWorld beta 1 | 161 | same table as 2.05 | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| NewWorld beta 2 | 165 | `addstring`, `insertstring`, `removestring`, `deletestring` | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |

A command in the table may have no executor case and be parsed and ignored; new commands are inserted mid-table, so command indexes differ between builds [bin] (client-internals/cross-version-timeline.md#gs1-commands). The commands themselves: → §8.2.

## C.6 Generation 2 builds, 1.21 to 1.32

| Build | S→C ids handled | Player props parsed | Player props sent | NPC props | Baddy props | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 1.21 | 0–34 except 30, plus 100 | 0–24 | 0–24 | 0–17 | 0–10 | [bin] (protocol/gserv-1999.md#message-ids); [bin] (protocol/gserv-1999.md#props-by-build) |
| 1.28 beta 2 | 0–38, plus 100 | 0–31 | 0–24, 26, 31 | 0–32 | 0–10 | [bin] (protocol/gserv-1999.md#message-ids); [bin] (protocol/gserv-1999.md#props-by-build) |
| 1.3 test | 0–39, plus 100 | 0–32 | 0–24, 26, 31, 32 | 0–34 | 0–10 | [bin] (protocol/gserv-1999.md#message-ids); [bin] (protocol/gserv-1999.md#props-by-build) |
| 1.31 | 0–40, plus 100 | 0–32 | 0–24, 26, 31, 32 | 0–34 | 0–10 | [bin] (protocol/gserv-1999.md#message-ids); [bin] (protocol/gserv-1999.md#props-by-build) |
| 1.32 | 0–41, plus 100 | 0–33 | 0–24, 26, 31–33 | 0–34 | 0–10 | [bin] (protocol/gserv-1999.md#message-ids); [bin] (protocol/gserv-1999.md#props-by-build) |

Prop numbers grow at the end, so a decoder can use the later tables and stop at the build's last id [bin] (protocol/gserv-1999.md#props-by-build). The meanings of ids 35 to 41 in this generation are unmeasured [bin] (protocol/gserv-1999.md#open-questions).

Client-to-server ids sent by these builds are in → §2.4.2.

## C.7 Lab runs of later real clients

Each run used an unmodified client against a GServer-v2 lab on a loopback-only network, with hosts redirected by name [cap] (version-profiles/lab-304-linux-2026-10-30.md#setup-for-repeating-it); [cap] (version-profiles/lab-v5-2026-10-30.md#setup-for-repeating-it).

| Builds | How it ran | What it settled | Source |
| --- | --- | --- | --- |
| 3.04 (Linux) | the original packed executable on Xvfb with software GL | the listserver login is one plain frame holding ids 7 and 1, answered in gen 5; the game login frame is plain zlib with 5, 37 and two 34 requests, and every later frame is gen 5, including a bz2 reply | [cap] (version-profiles/lab-304-linux-2026-10-30.md#startup-and-listserver); [cap] (version-profiles/lab-304-linux-2026-10-30.md#game-login) |
| 4.20r6, 3.153 (Mac) | Mac OS X 10.4 in an emulated PowerPC machine | 4.20r6 sends the login with a four-field comma list `mac`, an empty MAC hash, a 32-hex hash, and an empty field; 3.153 walks with X2 and Y2 | [cap] (version-profiles/lab-mac-tiger-2026-10-31.md#login-line-captured-run2pcap-proxylog); [cap] (version-profiles/lab-mac-tiger-2026-10-31.md#walking-x2y2-confirmed) |
| 5.00r7, 5.12, 5.24r4 | Wine on Xvfb behind a gen-5 logging proxy | the server reached through the license file is treated as the Login server, where no characters and no HUD are drawn; stock gs2lib does not know the 5.24 token and serves it the pre-2.1 file layout | [cap] (version-profiles/lab-v5-2026-10-30.md#login-mode-why-nothing-is-drawn-at-first); [cap] (version-profiles/lab-v5-2026-10-30.md#setup-for-repeating-it) |

The per-build profile files and lab tables behind these cells, with the build range each covers, are listed in → §1.8.8; the full build list is in → §1.8.
