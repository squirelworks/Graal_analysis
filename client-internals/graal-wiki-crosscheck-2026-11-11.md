# The community Graal wiki checked against this repo

Date: 2026-11-11

The community Graal wiki (the "Graal Bible", MediaWiki, now at `wiki.gscript.dev`) was read in full: 491 articles, fetched once through its API at one request every two seconds. Most of it is world and staff lore. The parts that matter here are the client release notes (`Creation/Dev/Releases/Client/…`, 1.3 to 6.036), the old GS1 command list (`Creation/Dev/Old GScript`), the GS2 function lists, the gani, gmap and update-package pages, and the server options page. Each was compared with the notes in this repo. Tags: **[doc]** wiki text · **[bin]** our client reads · **[file]** shipped files · **[srv]** server source · **[inf]** inferred.

The wiki's 1.3, 1.4 and 2.x release notes are the same text as the `newfeatures*.txt` files the clients shipped, which this repo already uses (`feature-timeline.md`, `versions-133-139.md`). What is new to this repo is the v3 notes (`NewFeatures2003v3`, `NewFeatures2004v3`), the 4.x, 5.x and 6.x notes, the gani and update-package keyword pages and the server options list.

## Where the wiki and this repo agree

| Point | Wiki | This repo |
| --- | --- | --- |
| 1.36 raises the server from 220 to 28000 players | 1.36 notes **[doc]** | the player id in `PLO_OTHERPLPROPS` grows from one GCHAR (to 1.35) to two 7-bit characters (from 1.36) **[bin]** (`protocol/player-props.md`). The two fit: one GCHAR holds about 220 ids, two 7-bit characters about 28000. |
| 3.04 is the 2.22 release for v3 | 3.04 notes are the 2.22 notes word for word (third server-list tab, `gravity`, `downloadsize`) **[doc]** | `G3D03014` and `GNW03014` share a date stamp, and 3.04 speaks the 2.22 protocol **[bin]** (`protocol/v3x-clients.md`) |
| 3.03 carries the 2.21 network changes | "includes the new additions from Graal v2.21: faster network code, less traffic" **[doc]** | 2.21 is the compression-byte change **[srv]** (`feature-timeline.md`) |
| Files over 32000 bytes go in chunks | 2.14: files over 64k can be downloaded; 3.04/2.22: `downloadsize` is set for "a big file (>32k)" **[doc]** | from 2.14, files over 32000 bytes are wrapped in `LARGEFILESTART`/`LARGEFILESIZE`/`LARGEFILEEND` **[srv]** (`protocol/file-transfer.md`) |
| Graal 2D runs at 20 frames a second | 4.03 ("in Graal2D there are always 20 fps"), 5.1, 6.0 **[doc]**; 3.04 projectile z drops 0.1 a frame, 2 a second | one tick is 50 ms in every Delphi build **[bin]** (§4.1) |
| `GRMAP001` keywords | `WIDTH`, `HEIGHT`, `GENERATED`, `LEVELNAMES`, `MAPIMG`, `MINIMAPIMG`, `NOAUTOMAPPING`, `LOADFULLMAP`, `LOADATSTART`, the `GEN*`/`LEV*` terrain keys, `HEIGHTMAP`, `RANDOMSEEDS` **[doc]** | the same set **[bin]** (`formats/gmap.md`) |
| Player and NPC z | server option `lockplayerz`: z outside −50..170 counts as undefined **[doc]** | `c(z + 50)`, z −50..170 **[srv][2.22]** (`protocol/player-props.md`) |
| AP recharge defaults | `aptime0`–`aptime4` default to 30, 90, 300, 600, 1200 s **[doc]** | the same in GServer-v2 **[srv]** (§4.4) |
| NPC server tick | 0.1 s main loop (`Creation/Dev/NPC-Server`, the official NPC server text) **[doc]** | 0.1 s **[doc]** (`tools/npcserver-2001.md`) |
| `carryobject` and `throwcarry` | announced in the 1.37 notes **[doc]** | in the command table from 1.34 **[bin]**; `versions-133-139.md` already says a table entry does not prove the command worked |
| Delphi and DelphiX | "originally written in Delphi … a modified DelphiX" **[doc]** | DelphiX `TDXDraw`/`TDXTimer` in the clients **[bin]** (`graal3d/README.md`) |

## Release dates against the login-token date stamps

The tokens are `G3D` plus a `DDMMY` stamp (`protocol/login-tokens-3x-7x.md`). The wiki gives release dates for the same builds, so the stamp rule can now be checked against a written date instead of only file dates **[doc][bin]**:

| Token | Build | Stamp | Wiki release |
| --- | --- | --- | --- |
| `G3D17026` | Windows 4.04r2 | 17 Feb 2006 | 4.04: 17 Feb 2006 |
| `G3D27076` | Mac 4.20r6 | 27 Jul 2006 | 4.1: 27 Jul 2006 (4.206 for Mac, Linux and Windows: 21 Dec 2006) |
| `G3D20126` | Windows 4.20r8 | 20 Dec 2006 | 4.206: 21 Dec 2006; 4.208: 12 Jan 2007 (Windows) |
| `G3D22067` | 5.00r7 | 22 Jun 2007 | 5.006: 13 Jul 2007; 5.007: 18 Jul 2007 |
| `G3D14097` | 5.12 | 14 Sep 2007 | 5.1: 17 Sep 2007; 5.12: 19 Oct 2007 |
| `G3D0311C` | Windows 6.03r7 (6.037) | 3 Nov 2012 | 6.036: 4 Nov 2012 (Windows and Mac) |
| `G3D0511C` | Linux 6.03r7 | 5 Nov 2012 | 6.036: 10 Nov 2012 (Linux) |

- Every stamp falls on or a few days to a few weeks before a release, and a bug-fix release can keep the stamp of the release before it (4.208 keeps 4.206's, 5.12 keeps 5.1's, 6.037 keeps 6.036's). **[doc][bin]**
- The 6.036 dates back the reading of the year letter `C` as 2012 (`login-tokens-3x-7x.md`): the Windows and Linux stamps land one and five days before the platform release dates. **[doc][bin]**
- The Mac build called 4.20r6 carries the stamp of the 4.1 release day, five months before the wiki's 4.206 release for Mac. Either the Mac token was not updated for 4.20, or that build is older than its name. Open. **[doc][bin][inf]**

## Where the wiki corrects or extends this repo

- **Gani slot keywords are written with the slot number glued on.** Real files say `DEFAULTATTR1 hat5.png`, `DEFAULTPARAM1 …`, `PARAM1 0 0` and `ATTR4 8 16`, not `DEFAULTATTR 1 …` (wiki gani FAQ **[doc]**; all 234 ganis in the NewWorld beta and NewMain folders of the shared client archive **[file]**). The grammar in `formats/gani.txt` and §3.3.2 wrote a space; both are fixed in this change. Whether the parser also accepts a space was not checked.
- **`ROTATEPROJECTILE` is a gani header keyword from 6.036.** A projectile using such a gani is turned to its flight path; the gani must also be `SINGLEDIRECTION` and drawn facing right (6.036 notes **[doc]**). It is not in our grammar, which comes from editor and 2.x reads. Added to §3.3.4 as **[doc]**, not yet seen in a binary.
- **GS1 left the client in 5.1.** "GS1 has been removed, Graal is now always using GS2" (5.1, 17 Sep 2007) **[doc]**. Our GS1 table scan stops at 5.00r7, which still has 193 commands (`npc-library/gs1-commands-by-version.md`). So 5.12 and later should have no GS1 command table. Recorded there as an expectation, not a read.
- **v4 sends bytecode only.** The v4 announcement (Aug 2005) says servers stop sending script text, send compiled bytecode, and the client can no longer compile scripts; scripts are cached on disk; a "computer id" can be banned **[doc]**. This matches eras I and J in App. C (GS2 bytecode, `GRESCR01` cache, machine-id hashes after the password) **[bin]**; the wiki adds the date and the reason.
- **Update packages (`GRPKG001`).** Our notes only name the magic. The wiki gives the keywords: `NAME`, `VERSION`, `PLATFORM` (`mac`, `win`, `linux`, `any`), `SUBPACKAGE`, `USECHECKSUM`, `PROTECTOVERWRITE`, `FLAG popupforoptionalpackages=…`, `MODE` (`base`: checked at every login; `required`: checked when the version differs; `optional`, the default: only on request), `DESCRIPTION` … `DESCRIPTIONEND` and `FILE <path>`; the root is `basepackage.gupd` **[doc]**. Not yet checked in a binary.
- **Linux and Mac data folders.** v5 and earlier keep files in `~/.graal/graal4` (Mac from 4.02); v6 on Mac uses `~/Library/Application Support/Graal`, and v6 on Linux the executable's folder **[doc]**.

## Where this repo corrects the wiki

- The `Graal` page says Graal "started its existence in the early 2000 as a relatively simple Java game". The Java precursors are the 1997–98 Zelda Online applets, and the Delphi Graal client runs from the 1998 betas (§1.1.1, §1.6). By 2000 Graal was at 1.3x. **[bin][file]**
- The `Graal Client` page says the client is written in C++. That is true from 3.x (Torque) and of the 4.x–5.12 engine DLL; 1st Graal to 2.31 is Delphi, and 4.04r2 to 5.12 on Windows still start from a Delphi launcher (§1). **[bin]**
- Small text slips: in `Old GScript`, `copyflagss` has a doubled s and `changeimg part` is `changeimgpart`; on the GMap page `HEIGHMAP` is `HEIGHTMAP`. **[bin]**
- The 1.3 notes' "1.36: the server can now hold 28000 players" has a wire side the wiki does not give: the player-id width change above.

## Leads not yet researched here

- [ ] **5.1 projectiles.** "Projectiles are sent with higher precision and can use different gravity" (5.1) **[doc]**. Our 4.20r8 read of id 191 (`SHOOT2`) lists x, y, z, angles and speed but no gravity (`protocol/v4x-clients.md`); GServer-v2 reads a gravity byte after power in `PLI_SHOOT2` **[srv]**. Check 5.12's 191 for the gravity byte.
- [ ] **Confirm GS1 is gone in 5.12** with the `tools/gs1-table-scan` scanner on the 5.12 engine.
- [ ] **`-listscriptfunctions`.** The 4.03 and 6.036 notes say the client prints its script-function documentation with this switch; our launcher reads list the switch (`torque/4208-launcher.md`, `torque/5007-launcher.md`). Run once in a sandbox to get each build's GS2 function list. The wiki's `Creation/Dev/Script/Client` and `Script Functions: NPC Server` pages are such dumps (2006–2010): 70 of the 90 client functions and 52 of the 222 NPC-server functions appear somewhere in this repo.
- [ ] **Server options.** The wiki lists 99 `serveroptions` keys; 71 are not mentioned in this repo and 36 are not read by GServer-v2 (for example `weaponorder`, `ghostmodeenabled`, `spawnrate*`, `newtilesets`/`newtilesetlevels`, `syncdistancex`/`y`, `speedhacktolerance`, `sendtoallattr`, `serverlanguage`/`defaultlanguage`/`translatedlanguages`). A reference table would help GServer-v2 and Seihai.
- [ ] **Early AP timing.** The 1.4 notes give AP recharge every 30 s under 20 AP, every 2 min under 40, and every 30 min at 80 and over, with no 90 cap **[doc]**; the later defaults above are 30/90/300/600/1200 s. Check a 1.4x-era server.
- [ ] **GS1 server-only commands.** The `Old GScript` list has server commands our client tables lack: `addguildmember`, `removeguildmember`, `removeguild`, `copylevel`, `deletelevel`, `saveinfo`, `copystrings`, `updateboard2` **[doc]**. They belong in the NPC-server notes (`tools/npcserver-2001.md`) once a server build confirms them.
- [ ] **4.02 server notes.** gmaps and `.gupd` files are updated by file checksum and cached in memory; RC script limit raised from 28k to about 100k; scripts over 28k break old-engine clients **[doc]**.
- [ ] **4.03 UDP default.** UDP is off by default from 4.03 and is switched on for voice chat **[doc]**; compare with `protocol/udp-p2p.md`.
