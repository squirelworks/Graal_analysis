# Canonical version-token catalogue

Updated: 2026-11-15. **This is the sole maintained source of truth for the version-token map.** The token-first [human map](../VERSION-TOKENS.md) and [machine-readable associations](../version-profiles/version-token-map.tsv) are generated from the catalogue tables here by `tools/token-map/generate.py`. Edit this catalogue, then regenerate; do not maintain another token list.

Coverage: existing published desktop/Mac/Linux/mobile, Graal3D, RC/NC, server-recognition and connector studies audited through this date. This is a map of known evidence, **not** completion of every historical build or the 45-client/16-server research intake. A token is not a unique executable, platform, app or feature profile. Evidence applies per association; a captured sibling never upgrades an unobserved build. Modified/repacked inputs do not establish stock provenance.

Older partial lists (`version-tokens.md`, `version-id-map.md`, `archival/version-tokens-early.md`, `version-profiles/version-tokens-by-build.tsv`) remain historical source records, not competing catalogues. The external [core registry export](https://github.com/squirelworks/seihai-core/blob/main/documentation/version-tokens.tsv) is a consumer snapshot, not this research source: it omits some server-recognized tokens and tool roles, and its token-level grade cannot replace per-build evidence. Reproduction-folder columns below are historical observations, not a current consumer certification.

Sources include the older maps, build catalogue, protocol/login studies, lab profiles and the linked mobile/tool/server notes. This change credits and reconciles prior research; it adds no new binary reading or runtime experiment.

## Evidence grades

| Grade | Meaning |
|---|---|
| **W** wire | The token was seen in the original client's own first login frame, in a lab run against a lab server **[cap]**. |
| **B** binary | The token was read from the original executable (a string literal up to 1.37, and character immediates from 1.38 on), but the original's login has not been captured **[bin]**. |
| **L** list only | No executable has been read. The token comes only from the public version list (GServer-v2 `versions.txt` / `allowedversions.txt`, gs2lib's token table) **[srv]**. |
| **S** server-defined | The client stores no token. The server's connector script supplies the token at login **[lab][bin]**. |
| **U** unresolved | No token recovered or the production value is unestablished; not proof of no networking. |
| **C** script constant | Present in a published connector-script table, not bound to an observed client login. |
| **—** none | The build has no login token at all (no network login, or a pre-token protocol). |
| **B+** | Binary read, and the original logged in to a lab server whose allow-list names each token, but its login frame was not decoded. Strong, though not a byte-level wire record. |

**Re-read 2026-11-12 [bin].** The 54 Delphi client executables in the archive set (1.21's InstallShield package was not unpacked) and GraalX were scanned again with a fresh, independent scanner. The scanner matches token-shaped string literals and runs of one-byte character immediates. Every token in `build-catalogue.md` was reproduced, and no build produced a second candidate. The NewWorld beta 2 immediates needed a stride check: the token is the eight evenly spaced `mov bl` immediates, and one unrelated `mov al` byte in between gives a false ninth character. The 1998 betas, 1.1.9 and 1.1 have no token literal and no token-shaped immediates.

## Catalogue

"Repro" is the token the `graal-client-repro` folder sends. ✔ means it matches the evidence. "Repro label" is the label in that folder's release notes ("tested" = "tested against the real client", "token only", "none").

### Early families and Graal3D

| Build | Token | Grade | Source | Platform | Role | Repro | Repro label |
|---|---|---|---|---|---|---|---|
| Zelda Online 1 / 2 (Java) | none | — | `Z3-V1.02` / `Z3-V1.03` are level-format magics, not login tokens. ZO2 talks text lines to its GServ lobby | Java | no-token | ✔ none | (n/a) |
| 1st beta to 15th (b1–b15), 1.1.9, 1.1 | none | — | Peer relay protocol: no token and no compression (`protocol/relay-1998.md`). Re-read today: no literal and no immediates. The 1.1.9 bundled Gserver takes no token either | Windows | no-token | ✔ none | none |
| Graal3D (Feb 2000) | `GR3DV002` | W | Separate program with its own server on its own port. String literal in the exe | Windows | game-login | ✔ | tested |
| Graal3D, later beta ("New Graal 3D Beta Version") | `GR3DV003` | B | string literal, 2026-11-13. A bigger exe (630,272 bytes, against 605,184) that switches the renderer from Direct3D RM to Genesis3D (needs `genesis.dll`) and loads a local BSP world; login layout, packet ids and props are unchanged ([note](../graal3d/beta3-genesis.md)) | Windows | game-login | (no folder) |  |
| Graal GBC 1.10, Java Graal (2000), 39ster 1.00 | none | — | Offline only, or no Graal-protocol login | GBC/Java/Windows | no-token | ✔ none | none |

### GSERV era (1.21–1.32): protocol-revision tokens, not dates

| Build | Token | Grade | Source | Platform | Role | Repro | Repro label |
|---|---|---|---|---|---|---|---|
| 1.21 | `GSERV007` | W | `gserv-1999.md`, `live-trace-early.md` | Windows | game-login | ✔ | tested |
| 1.25 | `GSERV009` | B | string literal in the exe unpacked from the 1.25 installer, 2026-11-13; its RemoteControl sends `GSERV010` ([note](gserv-125-127-builds.md)) | Windows | game-login | (no folder) |  |
| 1.27 | `GSERV011` | B | string literal in the exe unpacked from the 1.27 installer, 2026-11-13. The RemoteControl in the same package is the one later shipped as RC 1.28; RC 1.3 also sends `GSERV011` [bin] ([note](gserv-125-127-builds.md)) | Windows | game-login | (no folder) |  |
| 1.28 beta 2 | `GSERV013` | W | `live-trace-early.md` | Windows | game-login | ✔ | tested |
| 1.3 test | `GSERV014` | W | `live-trace-early.md` (first frame decoded) | Windows | game-login | ✔ | tested |
| 1.31 | `GSERV016` | **W** | `live-trace-early.md`: both 1.31 and 1.32 sent their login frame to GServer13 and were refused as too new | Windows | game-login | ✔ | **token only (understated)** |
| 1.32 | `GSERV018` | **W** | as above | Windows | game-login | ✔ | **token only (understated)** |

### GNW gen 2 (1.33–1.39) and gen 3 (1.41–2.1 test)

| Build | Token | Grade | Source | Platform | Role | Repro | Repro label |
|---|---|---|---|---|---|---|---|
| 1.33 | `GNW20020` | **W** | literal; traffic captured and decoded under Wine (`versions-133-139.md`, "Live check") | Windows | game-login | ✔ | **token only (understated)** |
| 1.33 rev? | `GNW28020` | L | no client exe; in the 1.34 rev 1 server port's table between 1.33 and 1.34 (28 Feb 2000) [bin] (`server-notes/original-server-builds-1999-2007.md`) | unestablished | game-login | (no folder) |  |
| 1.34 | `GNW22030` | B+ | literal; logged in to the lab classic server (`tools/lab-servers/README.md`), frame not decoded | Windows | game-login | ✔ | token only |
| 1.34 rev 1 | `GNW27030` | L | no client exe; the only player token the 1.34 rev 1 server port lets in ("You need Graal version 1.34 rev1") [bin] (`server-notes/original-server-builds-1999-2007.md`) | unestablished | game-login | (no folder) |  |
| 1.35 | `GNW13040` | B+ | literal; logged in to the lab classic server (`tools/lab-servers/README.md`), frame not decoded | Windows | game-login | ✔ | token only |
| 1.36 | `GNW10050` | B+ | literal; logged in to the lab classic server (`tools/lab-servers/README.md`), frame not decoded | Windows | game-login | ✔ | token only |
| 1.37 | `GNW21050` | B+ | literal; logged in to the lab classic server (`tools/lab-servers/README.md`), frame not decoded | Windows | game-login | ✔ | token only |
| 1.38 | `GNW22060` | B+ | immediates (first char-built token); logged in to the lab classic server, frame not decoded | Windows | game-login | ✔ | token only |
| 1.38 rev 1 | `GNW02070` | L | no client exe; the 1.39 server's table and refusal text ("1.38 rev1 - 1.39 rev 1") [src][bin] (`server-notes/original-server-builds-1999-2007.md`) | unestablished | game-login | (no folder) |  |
| 1.39 baseline (FileVersion 1.3.8.0) | `GNW07080` | **W** | immediates; traffic captured and decoded (`versions-133-139.md`); also on the public list | Windows | game-login | ✔ | **token only (understated)** |
| 1.39 comparison (FileVersion 1.3.9.1) | `GNW07080` | B | [Exact input comparison](early-windows-callback-variants.md#139-comparison-client-fileversion-1391-token-gnw07080); same version field as a different-token 1.40 input | Windows | game-login | not assessed | |
| 1.391 (1.39 rev 1) | `GNW12080` | L | gs2lib table; the 1.39 server's table names it 1.39 rev 1 [src][bin] (`server-notes/original-server-builds-1999-2007.md`). The two FileVersion 1.3.9.1 executables read on 2026-11-13 send `GNW07080` and `GNW23090` instead ([note](graal2002-and-140-builds.md)) | unestablished | game-login | (no folder) |  |
| 1.40 comparison (FileVersion 1.3.9.1) | `GNW23090` | B | [Exact input comparison](graal2002-and-140-builds.md#what-the-140-builds-settle); version field alone is not identity | Windows | game-login | not assessed | |
| 1.40 rev1 (FileVersion 1.4.0.1) | `GNW23090` | B | [Exact input comparison](graal2002-and-140-builds.md#what-the-140-builds-settle); version field alone is not identity | Windows | game-login | not assessed | |
| 1.41 rev1 | `GNW13110` | W | lab capture | Windows | game-login | ✔ | tested |
| 1.41 rev1 body-entry comparison (FileVersion 1.4.1.1) | `GNW13110` | B | [Same-version input study](early-windows-callback-variants.md); token identity only, no stockness or runtime transfer | Windows | game-login | not assessed | |
| 1.41 rev1 return-entry comparison (FileVersion 1.4.1.1) | `GNW13110` | B | [Same-version input study](early-windows-callback-variants.md); token identity only, no stockness or runtime transfer | Windows | game-login | not assessed | |
| NewMain 24, 26 | `GNW08011` | W | lab capture; immediates in both exes | Windows | game-login | ✔ | tested |
| 2.00 | `GNW24011` | **W** | `decomp-findings-2026-10-24-b/07-lab-findings-46-186-200.md`: the 2.00 exe logged in to a lab gserver with type 0, the key byte and `GNW24011` | Windows | game-login | ✔ | **token only (understated)** |
| 2.00 rev1, rev2, rev3 | `GNW24011` | B | immediates. Same token as 2.00, which was seen on the wire | Windows | game-login | ✔ | token only |
| GraalX (2.01 pre-release) | `GNW23021` | **W** | immediates; the original's login was logged by a lab gserver on 2026-11-12 [lab] | Windows | game-login | ✔ | **token only (understated)** |
| 2.01 | `GNW23021` | W | immediates; the original 2.01's login was logged by a lab gserver on 2026-11-12 [lab]; capture applies to base build only | Windows | game-login | ✔ | **token only (understated)** |
| 2.01 rev1 | `GNW23021` | B | immediates; the original 2.01's login was logged by a lab gserver on 2026-11-12 [lab]; capture applies to base build only | Windows | game-login | ✔ | **token only (understated)** |
| 2.02 | `GNW15041` | W | immediates; the original 2.02's first frame was captured on loopback on 2026-11-12 [lab]; capture applies to base build only | Windows | game-login | ✔ | **token only (understated)** |
| 2.02 rev1 | `GNW15041` | B | immediates; the original 2.02's first frame was captured on loopback on 2026-11-12 [lab]; capture applies to base build only | Windows | game-login | ✔ | **token only (understated)** |
| 2.02 rev2 | `GNW20041` | **W** | immediates; first frame captured on loopback on 2026-11-12 [lab] | Windows | game-login | ✔ | **token only (understated)** |
| 2.03 | `GNW06051` | **W** | immediates; original's login logged by a lab gserver on 2026-11-12 [lab] | Windows | game-login | ✔ | **token only (understated)** |
| 2.04 | `GNW24061` | **W** | immediates; original's login logged by a lab gserver on 2026-11-12 [lab] | Windows | game-login | ✔ | **token only (understated)** |
| 2.05, 2.05 rev1 | `GNW03081` | B (token W via rev2) | immediates. The same token was seen on the wire from 2.05 rev2 | Windows | game-login | ✔ | token only |
| 2.05 rev2 | `GNW03081` | W | lab captures | Windows | game-login | ✔ | tested |
| NewWorld 1.39 | `G2N29070` | L | no client exe; the 1.39 server tree's NewWorld option ("Graal-Newworld version 1.39") [src] (`server-notes/original-server-builds-1999-2007.md`) | unestablished | game-login | (no folder) |  |
| NewWorld beta 1 (pre-update and final), beta 2 | `G2N15041` | W | lab captures; immediates in all three exes | Windows | game-login | ✔ | tested |
| 2.1 test 2, test 3 | `GNW03081` | W | still 2.05's token | Windows | game-login | ✔ | tested |

### 2.1–2.31 (gen 3 to gen 5)

| Build | Token | Grade | Source | Platform | Role | Repro | Repro label |
|---|---|---|---|---|---|---|---|
| Graal 2002 ver7 (FileVersion 2.1.0.0) | `GNW03081` | B | [Exact image construction](graal2002-and-140-builds.md#the-builds); same version field as the different-token public image, not wire-captured | Windows | game-login | not assessed | |
| Graal 2002 ver8 (FileVersion 2.1.0.0) | `GNW03081` | B | [Exact image construction](graal2002-and-140-builds.md#the-builds); same version field as the different-token public image, not wire-captured | Windows | game-login | not assessed | |
| Graal 2002 ver9 (FileVersion 2.1.0.0) | `GNW03081` | B | [Exact image construction](graal2002-and-140-builds.md#the-builds); same version field as the different-token public image, not wire-captured | Windows | game-login | not assessed | |
| Graal 2002 ver10 (FileVersion 2.1.0.2) | `GNW31101` | B | [Exact image construction](graal2002-and-140-builds.md#the-builds); shared token, not wire-captured | Windows | game-login | (no folder) |  |
| Graal 2002 ver13 (FileVersion 2.1.0.4) | `GNW31101` | B | [Exact image construction](graal2002-and-140-builds.md#the-builds); shared token, not wire-captured | Windows | game-login | (no folder) |  |
| Graal 2002 v22 (FileVersion 2.1.0.4) | `GNW31101` | B | [Exact image construction](graal2002-and-140-builds.md#the-builds); shared token, not wire-captured | Windows | game-login | (no folder) |  |
| 2.1.0.0 public release (FileVersion 2.1.0.0, built 2001-11-13) | `GNW31101` | B | immediates, 2026-11-13, in the exe from the 2001 auto-updater pack (a copy of the official download); confirms the public 2.1.0.0 sends the Graal 2002 ver10 token, not 2.05's. Its listserver request is `newmain`, where the Graal 2002 leaks ask for `graal2002` ([method](../protocol/login-tokens-3x-7x.md#reading-the-token-from-a-file)) | Windows | game-login | (no folder) |  |
| 2.12 | `GNW01012` | L | public list | unestablished | game-login | (no folder) |  |
| 2.13 | `GNW23012` | L | public list | unestablished | game-login | (no folder) |  |
| 2.14 | `GNW30042` | L | public list | unestablished | game-login | (no folder) |  |
| 2.15.0 | `GNW19052` | L | public list | unestablished | game-login | (no folder) |  |
| 2.15.1, 2.15.2 | `GNW20052` | L | public list | unestablished | game-login | (no folder) |  |
| 2.16 | `GNW12102` | L | public list | unestablished | game-login | (no folder) |  |
| 2.17.0 | `GNW22122` | L | Public version-list association; the cited lab capture is 2.17.1, not this sibling | Windows | game-login | ✔ | tested |
| 2.17.1 | `GNW22122` | W | lab capture of 2.17.1 | Windows | game-login | ✔ | tested |
| 2.18 | `GNW21033` | L | public list | unestablished | game-login | (no folder) |  |
| 2.19 | `GNW15053` | L | public list | unestablished | game-login | (no folder) |  |
| 2.2 | `GNW28063` | L | public list | unestablished | game-login | (no folder) |  |
| 2.21 | `GNW01113` | L | public list | unestablished | game-login | (no folder) |  |
| 2.22 | `GNW03014` | W | lab capture | Windows | game-login | ✔ | tested |
| **2.3** | `GNW14015` | **L** | public list only; see "2.3" below | Windows | game-login | ✔ (stand-in) | token only |
| 2.31 | `GNW28015` | W | lab capture | Windows | game-login | ✔ | tested |
| 2.22 / 2.31 listserver hello | `GNW30123` | W | listserver id 7, not a game token | Windows | list-login | ✔ |  |

### G3D era (3.0–6.03)

| Build | Token | Grade | Source | Platform | Role | Repro | Repro label |
|---|---|---|---|---|---|---|---|
| 3.0 (Linux 3.0beta) | `G3D16053` | B | connect-routine read of the Linux 3.0beta `graalexe` (after `upx -d`), 2026-11-13; matches gs2lib and the public list | Linux | game-login | (no folder) |  |
| 3.01 Linux | `G3D27063` | B | connect-routine read of the Linux 3.01 `graalexe`, 2026-11-13; matches the public list | Linux | game-login | (no folder) |  |
| 3.04 rev1 Linux | `G3D03014` | W | `lab-304-linux-2026-10-30.md`; `linux-local-login-matrix.md` | Linux | game-login | ✔ | tested |
| 3.151 Linux | `G3D27015` | B | connect-routine read of the Linux 3.151 `graalexe`, 2026-11-13 | Linux | game-login | (no folder) |  |
| 3.153 Mac (PPC), historical Tiger-lab attribution | `G3D28015` | **W** | `version-profiles/lab-mac-tiger-2026-10-31.md`, "Game login (captured)"; [identity limit](../version-profiles/macos-client-compatibility.md#archive-labels-and-the-historical-3153-claim): not yet linked to the matching later-labelled retained inputs | macOS | game-login | ✔ | **token only (understated)** |
| 3.x listserver hello | `G3D30123` | W | Tiger and 3.04 lab listserver logs | Linux/macOS | list-login | ✔ |  |
| 4.02.11 | `G3D28095` | L | public list | unestablished | game-login | (no folder) |  |
| 4.03r1 Linux | `G3D11125` | B | connect-routine read, 2026-11-13 | Linux | game-login | (no folder) |  |
| 4.03r3 Windows (4.0.3.3; public list: 4.03.4) | `G3D09125` | B | connect-routine read of the unpacked engine image taken from memory under Wine, 2026-11-13; read again from the `GraalEngine.dll` unpacked statically from the Thinstall package, same token ([note](../protocol/v4x-windows-403r3-411.md)); matches the public list's 4.03.4 | Windows | game-login | (no folder) |  |
| 4.04r2 Windows | `G3D17026` | W | lab capture | Windows | game-login | ✔ | tested |
| 4.04r2 Mac | `G3D18026` | W | `lab-mac-ppc-404r2-512-2026-11-13.md` | macOS | game-login | (no folder) |  |
| 4.04r2 Linux | `G3D19026` | W | `linux-local-login-matrix.md` | Linux | game-login | (no folder) |  |
| 4.10r2 Linux, 4.11 Linux | `G3D28076` | B | connect-routine read of both, 2026-11-13. Not the public list's 4.11 token: that one is the Windows build's | Linux | game-login | (no folder) |  |
| 4.11 Windows (4.1.1.0) | `G3D26076` | B | connect-routine read of the unpacked engine image from memory under Wine, 2026-11-13; read again from the `GraalEngine.dll` unpacked statically from the Thinstall package, same token ([note](../protocol/v4x-windows-403r3-411.md)); matches the public list | Windows | game-login | (no folder) |  |
| Mac PPC build of 2006-09-19 (archive label "4.20r6") | `G3D27076` | W | Tiger lab. The label looks wrong: the binary is dated 2006-09-19, and the Mac 4.10r2 download (2006-08-22) sends the same token, so this is a 4.10r2/4.11-era build | macOS | game-login | ✔ | tested |
| 4.10r2 Mac (PPC) | `G3D27076` | B | connect-routine read of the Mach-O (PPC register tracking), 2026-11-13; same token as the 2006-09-19 build | macOS | game-login | (no folder) |  |
| 4.20r6 Mac (PPC, binary 2006-12-21) | `G3D21126` | B | connect-routine read, 2026-11-13. This is the real Mac 4.20r6, from the official download of early 2007 | macOS | game-login | (no folder) |  |
| 4.20r6 / r8 Linux | `G3D22126` | W | `linux-local-login-matrix.md`. The 2007-01-15 Linux 4.20r8 build reads the same (connect-routine read, 2026-11-13) | Linux | game-login | (no folder) |  |
| 4.20r8 Windows | `G3D20126` | W | lab capture | Windows | game-login | ✔ | tested |
| 5.00r7 Windows | `G3D22067` | W | `lab-v5-2026-10-30.md` | Windows | game-login | ✔ | tested |
| 5.12 Windows | `G3D14097` | W | `v5v6-windows-unpacked.md` | Windows | game-login | (no folder) |  |
| 5.12 Mac | `G3D15097` | W | `lab-mac-ppc-404r2-512-2026-11-13.md` | macOS | game-login | (no folder) |  |
| 5.24r3, 5.24r4, 6.00 beta2 Windows | `G3D15010` | W | `v5v6-windows-unpacked.md` | Windows | game-login | (no folder) |  |
| 5.30r3, 5.31r4, 6.00r2, 6.00r4 Windows | `G3D26090` | W | `v5v6-windows-unpacked.md`. Static check 2026-11-13: the connect routine of the unpacked 5.30r3, 6.00r2 and 6.00r4 images builds `G3D26090` from eight one-character globals; no 6.03-style scrambled string in any of the three. The token date (26 Sep 2010) is three weeks before 5.30r3's compile date and was kept unchanged into 6.00r4 (June 2011) | Windows | game-login | ✔ (5.31r4) | tested |
| 6.00 beta1 Windows | `G3D03048` | W | `v5v6-windows-unpacked.md` | Windows | game-login | (no folder) |  |
| 6.x beta Linux (x86, x64; June 2011 beta download, probably 6.00r4) | `G3D28090` | B | connect-routine read of both, 2026-11-13. The binaries carry no version string. "6.00r4" is inferred: the Mac (6.004) and Windows (FileVersion 6.0.0.4) betas captured from the same folder on the same day share the file date. The token date is two days after Windows 6.00r4's `G3D26090` | Linux | game-login | (no folder) |  |
| 6.004 Mac (June 2011 beta) | `G3D27090` | B | connect-routine read of the x86_64 slice, 2026-11-13. One day before the Linux beta's `G3D28090` | macOS | game-login | (no folder) |  |
| 6.015 Mac | `G3D3107A` | B | connect-routine read of the x86_64 slice, 2026-11-13. One day after Windows 6.0.1.5's `G3D3007A` | macOS | game-login | (no folder) |  |
| 6.0.0.7, 6.0.1.5 Windows | `G3D3007A` | **W** | first login frame captured in a Windows 10 lab VM, 2026-11-13 (FileVersion 6.007 and 6.015); matches the public list | Windows | game-login | (no folder) |  |
| 6.01r1 Linux (x86, x64) | `G3D0108A` | **W** | `linux-local-login-matrix.md` (first-frame observation) | Linux | game-login | ✔ | **token only (understated)** |
| 6.0.3.4 Windows (FileVersion 6.034) | `G3D2505C` | B | read from a memory dump of the running client in a Windows 10 lab VM, 2026-11-13 (guest clock set to Oct 2012). Once the protector had decrypted the data section, the token sat as plain upper-case text next to "Connecting to the game server...". Matches the public list | Windows | game-login | (no folder) |  |
| 6.03r7 Windows | `G3D0311C` | W | `v5v6-windows-unpacked.md`; scrambled string in the exe | Windows | game-login | (no folder) |  |
| 6.03r7 Linux x64 | `G3D0511C` | **W** | `linux-local-login-matrix.md` | Linux | game-login | ✔ | **token only (understated)** |

### Server-defined login (6.11 and later)

| Build | Token | Grade | Source | Platform | Role | Repro | Repro label |
|---|---|---|---|---|---|---|---|
| 6.1.1.3 Windows | `GNP1905C` | S, W | `protocol/v6113-list-capture.md`; `protocol/v6-login-token-explained.md` | Windows | connector-game-login | ✔ | tested |
| 6.11r1 Mac | `GNP1905C` | S | [Connector replay](../protocol/v6-login-token-explained.md); supplied by the captured script, not a fixed build token | macOS | connector-game-login | none sent (scaffold) | none |
| Worlds 548, 610, 612, 613, 614, 71243; 7.0.1.7.5.0 | unknown | U | [v7 connector evidence](../protocol/v7-connector-live-20261111.md#1-self-identification-labbin); production token unestablished; do not substitute a stand-in token | Windows | connector-game-login | 614 stand-in sends `GNP1905C`; the others send none | none |

### iPhone

The published survey covers 27 packages / 26 unique executables, with 23 token-bearing unique executables (24 packages because Poker 1.2 is duplicated). All recovered values below are static construction/recovery, not device captures. Two other tokens remain server-table labels only. Alien Abuse 1.0/1.1 are unresolved, not proven offline; Era+ 1.0 declares encryption and its token remains unread. Details and scanner limits: [iphone-version-tokens.md](iphone-version-tokens.md).

| Build | Token | Grade | Source | Platform | Role | Repro | Repro label |
|---|---|---|---|---|---|---|---|
| Adrenaline Poker Online 1.2 (iOS) | `G3D04048` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| Belote (Expert Online) 1.2 (iOS) | `G3D04048` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| Adrenaline Pool Online 1.1 (iOS) | `G3D04048` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| AlloWin Pool 1.0 (iOS) | `G3D04048` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| Belote (Expert Online) 1.50 (iOS) | `G3D04048` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| Ace Tennis Online 1.1 (iOS) | `G3D04048` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| Ace Tennis Online 1.2 (iOS) | `G3D04048` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| Adrenaline Poker Online 1.60 (iOS) | `G3D04048` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| Adrenaline Pool Online 1.5 (iOS) | `G3D04048` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| Ace Tennis Online 1.3 (iOS) | `G3D04048` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| Alien Abuse 1.3 (iOS) | `G3D04048` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| Dino Smash 1.2 (iOS) | `G3D04048` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| Cocoto Kart Online 1.0 (iOS) | `G3D04048` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| Bomber Online 1.20 (iOS) | `G3D04048` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| Cocoto Magic Circus 1.0 (iOS) | `G3D18010` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| Cocoto Kart HD Online 1.1 (iOS) | `G3D18010` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| Ace Tennis HD Online 1.0 (iOS) | `G3D18010` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| Cocoto Kart Online 1.3 (iOS) | `G3D18010` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| Bomber Online 1.40 (iOS) | `G3D18010` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| AlloWin Pool 1.1 (iOS) | `G3D04048` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| AlloWin Pumpkins 1.0 (iOS) | `G3D04048` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| GraalOnline Classic+ 1.13 (iOS) | `G3D0208A` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence; [caller corroboration](classic-113-login-construction.md#scope-and-prior-work) | iOS | game-login | (not audited) |  |
| Dino Smash 1.4 (iOS) | `G3D18010` | B | [Published per-app construction survey](iphone-version-tokens.md#the-binaries-bin); static only, no capture; duplicate packages are not independent evidence | iOS | game-login | (not audited) |  |
| "iPhone 1.11" (app not identified) | `G3D29090` | L | [Mobile source audit](iphone-version-tokens.md#answer); gs2lib `CLVER_IPHONE_1_11`, app unbound | iOS | game-login | (no folder) |  |
| "iPhone Belote 1.5" (app not identified) | `G3D2504D` | L | [Mobile source audit](iphone-version-tokens.md#answer); gs2lib `CLVER_IPHONE_BELOTE_1_5` (added 2022), app unbound | iOS | game-login | (no folder) |  |
| Graal Era+ 1.0 (iPhone) | unknown | U | [Mobile survey](iphone-version-tokens.md); inspected copy declares cryptid 1, token unread | iOS | unknown-game-login | (no folder) |  |
| Alien Abuse 1.0 (iOS) | unknown | U | [Scanner boundary](iphone-version-tokens.md#scanner-boundary); no token recovered, offline status not established | iOS | unknown-game-login | (not audited) | |
| Alien Abuse 1.1 (iOS) | unknown | U | [Scanner boundary](iphone-version-tokens.md#scanner-boundary); no token recovered, offline status not established | iOS | unknown-game-login | (not audited) | |

### Android token coverage remains unresolved

| Build | Token | Grade | Source | Platform | Role | Repro | Repro label |
|---|---|---|---|---|---|---|---|
| Classic 1.6/1.7/1.8/2.0/2.2; Era 1.7/2.0 (seven inspected packages) | unknown | U | [Published Android study](android-classic.md#what-was-read) establishes package/host/selected engine coverage, not a login-token construction or capture; no iOS/desktop value is transferred | Android | unknown-game-login | not assessed | |

### Staff-tool login associations

These are tool-socket identities, not extra game-client releases. Static grades do not claim a stock/unmodified executable: the 2004 RC study includes community modifications. Shared tokens retain each known tool association.

| Build | Token | Grade | Source | Platform | Role | Repro | Repro label |
|---|---|---|---|---|---|---|---|
| RemoteControl shipped with 1.21 | `GSERV007` | B | [Staff-client static survey](../protocol/rc-list-online.md#who-sends-65-bin) | Windows | rc-login | not audited | |
| RemoteControl shipped with 1.25 | `GSERV010` | B | [Recovered installer study](gserv-125-127-builds.md#what-the-two-builds-settle) | Windows | rc-login | not audited | |
| RemoteControl shipped with 1.27 and 1.28 beta 2; RC 1.3 | `GSERV011` | B | [Installer identity comparison](gserv-125-127-builds.md#what-the-two-builds-settle); same executable across the first two packages | Windows | rc-login | not audited | |
| RemoteControl 1.33 | `GSERV014` | B | [Static lineage](../tools/remotecontrol-lineage.md#builds); no wire grade transferred from game 1.3 test | Windows | rc-login | not audited | |
| RemoteControl 2000-08-19 | `GSERV019` | B | [Static lineage](../tools/remotecontrol-lineage.md#builds) | Windows | rc-login | not audited | |
| RemoteControl 2000-10-25 | `GSERV020` | B | [Static lineage](../tools/remotecontrol-lineage.md#builds) | Windows | rc-login | not audited | |
| RemoteControl 2001-01-27 | `GSERV021` | B | [Static lineage](../tools/remotecontrol-lineage.md#builds) | Windows | rc-login | not audited | |
| RemoteControl 2001-08-20; 2002-01-04 | `GSERV022` | B | [Static lineage](../tools/remotecontrol-lineage.md#builds) | Windows | rc-login | not audited | |
| RemoteControl 2002-01-11; 2002-05-02 (1.41) | `GSERV023` | B | [Static lineage](../tools/remotecontrol-lineage.md#builds) | Windows | rc-login | not audited | |
| Delphi RemoteControl 2004-01-17 and inspected community variants | `GSERV024` | B | [Staff-client survey](../protocol/rc-list-online.md); modified variants do not authenticate stock provenance | Windows | rc-login | not audited | |
| RemoteControl 2005-01-24 | `GSERV024` | B | [RC/NC static survey](../protocol/unknown-ids-2026-11-06.md) | Linux | rc-login | not audited | |
| RemoteControl 2006-12-20 (RC2 2.05) | `GSERV025` | B | [Staff-client survey](../protocol/rc-list-online.md) | Windows | rc-login | not audited | |
| RemoteControl 2010-03-29 | `GSERV025` | B | [Staff-client survey](../protocol/rc-list-online.md) | Linux | rc-login | not audited | |
| RC3 (file date 2015) | `GSERV025` | B | [Staff-client survey](../protocol/rc-list-online.md); file date is not release authentication | Windows | rc-login | not audited | |
| NewWorld RemoteControl 2001-05-21; 2001-08-20 | `G2NRC006` | B | [Static lineage](../tools/remotecontrol-lineage.md#builds) | Windows | rc-login | not audited | |
| Standalone NPC Control 2001-03-19; 2001-05-21; 2001-07-13 | `NCL15031` | B | [Original tool survey](../server-notes/original-server-builds-1999-2007.md); same token, differing forms | Windows | nc-login | not audited | |
| NPC socket in RC 2002-01-11 / 1.41 and Delphi RC 2004 | `NCL11012` | B | [NC login](../protocol/npc-control.md#login); type 3, no key byte | Windows | nc-login | not audited | |
| NPC socket in RC 2005-01-24 | `NCL11012` | B | [RC/NC survey](../protocol/unknown-ids-2026-11-06.md) | Linux | nc-login | not audited | |
| NPC socket in RC 2006-12-20 | `NCL21075` | B | [RC/NC survey](../protocol/unknown-ids-2026-11-06.md) | Windows | nc-login | not audited | |
| NPC socket in RC 2010-03-29 | `NCL21075` | B | [RC/NC survey](../protocol/unknown-ids-2026-11-06.md) | Linux | nc-login | not audited | |

### Server-recognized or reported identities without a measured client association

L here means a server table, source expectation or refusal classification. It is not a binary or wire reading of the named client. Do not fill missing client versions by interpolation.

| Build | Token | Grade | Source | Platform | Role | Repro | Repro label |
|---|---|---|---|---|---|---|---|
| Unidentified GSERV-era client accepted by 1.25 server | `GSERV008` | L | [Exact server acceptance](../protocol/gserv-1999.md); client version unresolved | unestablished | server-game-recognition | not audited | |
| Unidentified GSERV-era client in 1.34 rev 1 server table | `GSERV012` | L | [Server recognition table](../server-notes/original-server-builds-1999-2007.md); no recovered client association | unestablished | server-game-recognition | not audited | |
| Unidentified client admitted by December 1999 Linux server | `GSERV015` | L | [Server acceptance](../server-notes/original-server-builds-1999-2007.md); do not infer a 1.30 executable | unestablished | server-game-recognition | not audited | |
| Graal3D beta 1 label, recognized but refused by archived server | `GR3DV001` | L | [Server classification](../graal3d/beta3-genesis.md#does-the-archived-server-accept-it); no beta 1 client read | unestablished | server-game-recognition | not audited | |
| NewWorld RC 2000-08-19 label | `G2NRC004` | L | [Server-tree expectation](../tools/remotecontrol-lineage.md#builds); no client capture | unestablished | server-rc-recognition | not audited | |
| NPC-server label in server library table | `GRNS0000` | L | [Server table](../protocol/login-and-walk.md); no original NPC-server login observed here | unestablished | npc-server-login | not audited | |
| NPC-server label in server library table | `LNX00001` | L | [Server table](../protocol/login-and-walk.md); prefix alone does not prove platform | unestablished | npc-server-login | not audited | |
| Worlds label in upstream server table | `G3D2204D` | L | [v7 self-identification](../protocol/v7-connector-live-20261111.md#1-self-identification-labbin); production connector token unestablished | unestablished | reported-game-login | not audited | |

### List services, connector constants and non-login version identifiers

These roles are deliberately separate. A service identifier, HTTP header or script constant is not an additional observed fixed game-login token.

| Build | Token | Grade | Source | Platform | Role | Repro | Repro label |
|---|---|---|---|---|---|---|---|
| Public 2.1.0.0 list service | `newmain` | B | [List identity](../protocol/login-tokens-3x-7x.md#reading-the-token-from-a-file) | Windows | list-service | not audited | |
| 2.22 and 2.31 list service | `newmain` | W | [List login](../protocol/listserver.md); accompanies GNW30123, not part of its eight bytes | Windows | list-service | not audited | |
| 3.x list service | `newmain` | W | [List identity](../protocol/login-tokens-3x-7x.md); accompanies G3D30123 | Linux/macOS | list-service | not audited | |
| Graal 2002 list service | `graal2002` | B | [List identity](../protocol/login-tokens-3x-7x.md#reading-the-token-from-a-file); distinct from game token GNW31101 | Windows | list-service | not audited | |
| Captured connector script legacy table | `G3D2204D` | C | [Script table](../protocol/connector-script.md); no per-client production login binding | connector script | connector-constant | not audited | |
| Captured connector script legacy table | `G3D2304D` | C | [Script table](../protocol/connector-script.md); no per-client production login binding | connector script | connector-constant | not audited | |
| Captured connector script legacy table | `G3D2404D` | C | [Script table](../protocol/connector-script.md); no per-client production login binding | connector script | connector-constant | not audited | |
| Captured connector script legacy table | `G3D2504D` | C | [Script table](../protocol/connector-script.md); do not bind it to Belote 1.50 | connector script | connector-constant | not audited | |
| Worlds 548, 610, 612 | `Graal/6.76` | B | [Static User-Agent split](../protocol/v7-connector-live-20261111.md#1-self-identification-labbin) | Windows | http-user-agent | not audited | |
| Worlds 613, 71243 | `Graal/6.77` | B | [Static User-Agent split](../protocol/v7-connector-live-20261111.md#1-self-identification-labbin); no wire grade from sibling 614 | Windows | http-user-agent | not audited | |
| Worlds 614 | `Graal/6.77` | W | [Live connector request](../protocol/v7-connector-live-20261111.md#1-self-identification-labbin); HTTP identification, not game login | Windows | http-user-agent | not audited | |
| Worlds 548, 610, 612, 613, 614, 71243 product metadata | `6.114` | B | [Version resource](../protocol/v7-connector-live-20261111.md#1-self-identification-labbin); distinct from HTTP version | Windows | product-version | not audited | |
| Inspected PowerPC Mac bundles | `0.6.1d1` | B | [Bundle metadata](mac-ppc-runtime-surface-2026-11-09.md#packaged-resources); shared label, not a release id or login token | macOS PPC | bundle-version | not audited | |

Level magics such as `GSERVL01`, `GLEVNW01`, short `NW01`/`NW51` strings and the stored lowercase `g3d…` intermediates are not alternate wire tokens. The login builder uppercases the latter. Case is preserved only for positively identified values in their documented role. An unsuccessful string search (including `gnp1905c`) is not a token discovery.

## Gaps and how far each can be closed

- **Per-build grades:** several token values and build associations remain B; shared captured siblings do not upgrade them. Every token from 1.31 to 2.05 has now been seen on the wire from at least one original build. Sibling builds that share a token (2.00 rev1 to rev3, 2.01 rev1, 2.02 rev1, 2.05, 2.05 rev1) are B per build. 1.34 to 1.38 (B+) logged in to a lab server, but their frames were not decoded. The 2.02 family imports a cdecl `zlib.dll` (zlib 1.2.3) and fails to start beside a stdcall zlib build.
- **L only, no binary in any collection:** 1.391, all 2.1.x releases from 2.12 to 2.21 except 2.17 (the seven inspected Graal 2002 images are distinguished above), 2.3 and 4.02.11. Only a new binary can close these. On 2026-11-13 copies of the official downloads closed 3.0, 3.01, 4.03.4 (as 4.03r3), 4.11 and 6.0.0.7 / 6.0.1.5. A 6.0.3.4 download was found too, and its token was read from a memory dump.
- **None:** the pre-1.21 relay builds really have no token. This is a protocol fact, not a missing record.
- **Server-defined:** one captured 6.11-era connector script supplies `GNP1905C`; this is not a permanent per-build identity. The v7 study establishes connector User-Agent values but not a production game-login token.

## 2.3

No real 2.3.0.0 binary has been read. The only package labelled 2.3 in the owner-held collections is a modified third-party repack. Its game client is byte-identical to the 2.31 client this repo already reads [bin], so it is a 2.31 install with a 2.3 label and sends `GNW28015`, not `GNW14015`. It does not close the 2.3 gap. The token `GNW14015` is supported by three things:

1. It is on the public version list as 2.3.0.0.
2. Its DDMMY stamp reads 14 Jan 2005, two weeks before 2.31's `GNW28015` (28 Jan 2005).
3. It falls between 2.22 and 2.31 in gs2lib's ordered table.

The repro's 2.3 folder is a 2.31 rebuild sending `GNW14015`. Its post-login tamper-check bytes (PLI 39) are 2.31's: two CRC-32 words over the 2.31 program image. A real 2.3 would send its own bytes. The lab servers read PLI 39 and ignore it, so the stand-in logs in, but its PLI 39 is known to be wrong. Grade stays **L** until a 2.3 binary is read.

## Other observations

- `version-tokens.md` lists the Windows 4.20r8 row twice. Its "lab capture" tags for 5.12 to 6.03r7 Windows agree with `v5v6-windows-unpacked.md`.
- The Mac build labelled "4.20r6" sends `G3D27076`, one day after the public list's Windows 4.11 `G3D26076`. Settled 2026-11-13: that build is dated 2006-09-19 and the Mac 4.10r2 download sends the same token, so it is a 4.10r2/4.11-era build with a wrong archive label. The real Mac 4.20r6 (2006-12-21) sends `G3D21126` (rows above). seihai-gs2lib now calls `G3D27076` `CLVER_4_102_MAC` and gives `G3D21126` `CLVER_4_206_MAC`.
- The public list's `G3D3007A` (6.0.0.7 / 6.0.1.5 Windows) and the Linux 6.01r1 `G3D0108A` are different builds, not a conflict. As with 4.04r2 and 6.03r7, each platform build has its own stamp.

## Open points

- [x] ~~Wire-capture 2.01, 2.03, 2.04 and GraalX.~~ Captured on loopback and logged by a lab gserver on 2026-11-12. Each first frame is type 0, the gen-3 key byte, the token, then the account and password as GCHAR strings. 2.02 rev2, 2.03 and 2.04 add PLI 37 (language) in the same frame.
- [x] ~~Wire-capture 2.02 and 2.02 rev2.~~ Captured 2026-11-12 with a cdecl zlib 1.2.3 beside the unchanged exe.
- [ ] Decode the 1.34–1.38 login frames (they reach their connect window; the dialog still has to be driven).
- [ ] Read a genuine 2.3 binary, if one turns up, and record its token and PLI 39 words.
- [ ] Trace a v7 Worlds login to confirm the connector path supplies its token.
- [x] ~~Read an iPhone client (a period IPA).~~ Belote 1.2/1.50 and Classic+ 1.13 read 2026-11-14 ([iphone-version-tokens.md](iphone-version-tokens.md)).
- [x] ~~Place `G3D18010`.~~ Read in six 2010–2013 builds ([iphone-version-tokens.md](iphone-version-tokens.md)).
- [ ] Place `G3D29090` and `G3D2504D` with another decrypted IPA, or capture one iPhone login in the lab ([iphone-version-tokens.md](iphone-version-tokens.md#how-to-close-it)).
