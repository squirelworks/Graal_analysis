# Version-token catalogue, every known client build

Date: 2026-11-12. This note puts every known client build in one table: its login token, how strongly that token is evidenced, and whether the matching `graal-client-repro` folder sends the same value. It brings together `version-tokens.md`, `version-id-map.md`, `build-catalogue.md`, `protocol/login-tokens-3x-7x.md`, `protocol/gserv-1999.md`, `live-trace-early.md`, `protocol/linux-local-login-matrix.md` and the lab profiles. It adds one new static pass (below). No decompile material is used.

## Evidence grades

| Grade | Meaning |
|---|---|
| **W** wire | The token was seen in the original client's own first login frame, in a lab run against a lab server **[cap]**. |
| **B** binary | The token was read from the original executable (a string literal up to 1.37, and character immediates from 1.38 on), but the original's login has not been captured **[bin]**. |
| **L** list only | No executable has been read. The token comes only from the public version list (GServer-v2 `versions.txt` / `allowedversions.txt`, gs2lib's token table) **[srv]**. |
| **S** server-defined | The client stores no token. The server's connector script supplies the token at login **[lab][bin]**. |
| **—** none | The build has no login token at all (no network login, or a pre-token protocol). |
| **B+** | Binary read, and the original logged in to a lab server whose allow-list names each token, but its login frame was not decoded. Strong, though not a byte-level wire record. |

**Re-read 2026-11-12 [bin].** The 54 Delphi client executables in the archive set (1.21's InstallShield package was not unpacked) and GraalX were scanned again with a fresh, independent scanner. The scanner matches token-shaped string literals and runs of one-byte character immediates. Every token in `build-catalogue.md` was reproduced, and no build produced a second candidate. The NewWorld beta 2 immediates needed a stride check: the token is the eight evenly spaced `mov bl` immediates, and one unrelated `mov al` byte in between gives a false ninth character. The 1998 betas, 1.1.9 and 1.1 have no token literal and no token-shaped immediates.

## Catalogue

"Repro" is the token the `graal-client-repro` folder sends. ✔ means it matches the evidence. "Repro label" is the label in that folder's release notes ("tested" = "tested against the real client", "token only", "none").

### Gen 1 and Java precursors (1997–1999): no token

| Build | Token | Grade | Notes | Repro | Repro label |
|---|---|---|---|---|---|
| Zelda Online 1 / 2 (Java) | none | — | `Z3-V1.02` / `Z3-V1.03` are level-format magics, not login tokens. ZO2 talks text lines to its GServ lobby | ✔ none | (n/a) |
| 1st beta to 15th (b1–b15), 1.1.9, 1.1 | none | — | Peer relay protocol: no token and no compression (`protocol/relay-1998.md`). Re-read today: no literal and no immediates. The 1.1.9 bundled Gserver takes no token either | ✔ none | none |
| Graal3D (Feb 2000) | `GR3DV002` | W | Separate program with its own server on its own port. String literal in the exe | ✔ | tested |
| Graal3D, later beta ("New Graal 3D Beta Version") | `GR3DV003` | B | string literal, 2026-11-13. A bigger exe (630,272 bytes, against 605,184) that adds DirectInput and force feedback, camera distance settings and a deathmatch start ([note](graal2002-and-140-builds.md#other-builds-in-the-same-batch)) | (no folder) | |
| Graal GBC 1.10, Java Graal (2000), 39ster 1.00 | none | — | Offline only, or no Graal-protocol login | ✔ none | none |

### GSERV era (1.21–1.32): protocol-revision tokens, not dates

| Build | Token | Grade | Source | Repro | Repro label |
|---|---|---|---|---|---|
| 1.21 | `GSERV007` | W | `gserv-1999.md`, `live-trace-early.md` | ✔ | tested |
| 1.25 | `GSERV009` | L | public list only; no exe known | (no folder) | |
| 1.27 | `GSERV011` | L | public list only. RemoteControl 1.28 and 1.3 also send `GSERV011` [bin] | (no folder) | |
| 1.28 beta 2 | `GSERV013` | W | `live-trace-early.md` | ✔ | tested |
| 1.3 test | `GSERV014` | W | `live-trace-early.md` (first frame decoded) | ✔ | tested |
| 1.31 | `GSERV016` | **W** | `live-trace-early.md`: both 1.31 and 1.32 sent their login frame to GServer13 and were refused as too new | ✔ | **token only (understated)** |
| 1.32 | `GSERV018` | **W** | as above | ✔ | **token only (understated)** |

### GNW gen 2 (1.33–1.39) and gen 3 (1.41–2.1 test)

| Build | Token | Grade | Source | Repro | Repro label |
|---|---|---|---|---|---|
| 1.33 | `GNW20020` | **W** | literal; traffic captured and decoded under Wine (`versions-133-139.md`, "Live check") | ✔ | **token only (understated)** |
| 1.34 | `GNW22030` | B+ | literal; logged in to the lab classic server (`tools/lab-servers/README.md`), frame not decoded | ✔ | token only |
| 1.35 | `GNW13040` | B+ | literal; logged in to the lab classic server (`tools/lab-servers/README.md`), frame not decoded | ✔ | token only |
| 1.36 | `GNW10050` | B+ | literal; logged in to the lab classic server (`tools/lab-servers/README.md`), frame not decoded | ✔ | token only |
| 1.37 | `GNW21050` | B+ | literal; logged in to the lab classic server (`tools/lab-servers/README.md`), frame not decoded | ✔ | token only |
| 1.38 | `GNW22060` | B+ | immediates (first char-built token); logged in to the lab classic server, frame not decoded | ✔ | token only |
| 1.39 | `GNW07080` | **W** | immediates; traffic captured and decoded (`versions-133-139.md`); also on the public list | ✔ | **token only (understated)** |
| 1.391 | `GNW12080` | L | gs2lib table only. The two FileVersion 1.3.9.1 executables read on 2026-11-13 send `GNW07080` and `GNW23090` instead ([note](graal2002-and-140-builds.md)) | (no folder) | |
| 1.40, 1.40 rev1 | `GNW23090` | B | immediates in two executables (FileVersion 1.3.9.1 and 1.4.0.1), 2026-11-13; on no public list ([note](graal2002-and-140-builds.md)) | (no folder) | |
| 1.41 rev1 | `GNW13110` | W | lab capture | ✔ | tested |
| NewMain 24, 26 | `GNW08011` | W | lab capture; immediates in both exes | ✔ | tested |
| 2.00 | `GNW24011` | **W** | `decomp-findings-2026-10-24-b/07-lab-findings-46-186-200.md`: the 2.00 exe logged in to a lab gserver with type 0, the key byte and `GNW24011` | ✔ | **token only (understated)** |
| 2.00 rev1, rev2, rev3 | `GNW24011` | B | immediates. Same token as 2.00, which was seen on the wire | ✔ | token only |
| GraalX (2.01 pre-release) | `GNW23021` | **W** | immediates; the original's login was logged by a lab gserver on 2026-11-12 [lab] | ✔ | **token only (understated)** |
| 2.01, 2.01 rev1 | `GNW23021` | **W** (2.01) | immediates; the original 2.01's login was logged by a lab gserver on 2026-11-12 [lab] | ✔ | **token only (understated)** |
| 2.02, 2.02 rev1 | `GNW15041` | **W** (2.02) | immediates; the original 2.02's first frame was captured on loopback on 2026-11-12 [lab] | ✔ | **token only (understated)** |
| 2.02 rev2 | `GNW20041` | **W** | immediates; first frame captured on loopback on 2026-11-12 [lab] | ✔ | **token only (understated)** |
| 2.03 | `GNW06051` | **W** | immediates; original's login logged by a lab gserver on 2026-11-12 [lab] | ✔ | **token only (understated)** |
| 2.04 | `GNW24061` | **W** | immediates; original's login logged by a lab gserver on 2026-11-12 [lab] | ✔ | **token only (understated)** |
| 2.05, 2.05 rev1 | `GNW03081` | B (token W via rev2) | immediates. The same token was seen on the wire from 2.05 rev2 | ✔ | token only |
| 2.05 rev2 | `GNW03081` | W | lab captures | ✔ | tested |
| NewWorld beta 1 (pre-update and final), beta 2 | `G2N15041` | W | lab captures; immediates in all three exes | ✔ | tested |
| 2.1 test 2, test 3 | `GNW03081` | W | still 2.05's token | ✔ | tested |

### 2.1–2.31 (gen 3 to gen 5)

| Build | Token | Grade | Source | Repro | Repro label |
|---|---|---|---|---|---|
| Graal 2002 ver7–ver9 (FileVersion 2.1.0.0, Oct 2001) | `GNW03081` | B | immediates, 2026-11-13; still 2.05's token, like the 2.1 tests ([note](graal2002-and-140-builds.md)) | (no folder) | |
| 2.1.0.0–2.1.0.4 (Graal 2002 ver10, ver13, v22) | `GNW31101` | B | immediates in three executables (FileVersion 2.1.0.2 and 2.1.0.4), 2026-11-13; public list gives 2.1.0.0–2.1.0.3 ([note](graal2002-and-140-builds.md)) | (no folder) | |
| 2.12 | `GNW01012` | L | public list | (no folder) | |
| 2.13 | `GNW23012` | L | public list | (no folder) | |
| 2.14 | `GNW30042` | L | public list | (no folder) | |
| 2.15.0 | `GNW19052` | L | public list | (no folder) | |
| 2.15.1, 2.15.2 | `GNW20052` | L | public list | (no folder) | |
| 2.16 | `GNW12102` | L | public list | (no folder) | |
| 2.17.0, 2.17.1 | `GNW22122` | W | lab capture of 2.17.1 | ✔ | tested |
| 2.18 | `GNW21033` | L | public list | (no folder) | |
| 2.19 | `GNW15053` | L | public list | (no folder) | |
| 2.2 | `GNW28063` | L | public list | (no folder) | |
| 2.21 | `GNW01113` | L | public list | (no folder) | |
| 2.22 | `GNW03014` | W | lab capture | ✔ | tested |
| **2.3** | `GNW14015` | **L** | public list only; see "2.3" below | ✔ (stand-in) | token only |
| 2.31 | `GNW28015` | W | lab capture | ✔ | tested |
| 2.22 / 2.31 listserver hello | `GNW30123` + `newmain` | W | listserver id 7, not a game token | ✔ | |

### G3D era (3.0–6.03)

| Build | Token | Grade | Source | Repro | Repro label |
|---|---|---|---|---|---|
| 3.0 | `G3D16053` | L | gs2lib / public list; no binary known | (no folder) | |
| 3.01 | `G3D27063` | L | as above | (no folder) | |
| 3.04 rev1 Linux | `G3D03014` | W | `lab-304-linux-2026-10-30.md`; `linux-local-login-matrix.md` | ✔ | tested |
| 3.153 Mac (PPC) | `G3D28015` | **W** | `version-profiles/lab-mac-tiger-2026-10-31.md`, "Game login (captured)" | ✔ | **token only (understated)** |
| 3.x listserver hello | `G3D30123` + `newmain` | W | Tiger and 3.04 lab listserver logs | ✔ | |
| 4.02.11 | `G3D28095` | L | public list | (no folder) | |
| 4.03.4 | `G3D09125` | L | public list | (no folder) | |
| 4.04r2 Windows | `G3D17026` | W | lab capture | ✔ | tested |
| 4.04r2 Linux | `G3D19026` | W | `linux-local-login-matrix.md` | (no folder) | |
| 4.11 | `G3D26076` | L | public list | (no folder) | |
| 4.20r6 Mac | `G3D27076` | W | Tiger lab | ✔ | tested |
| 4.20r6 / r8 Linux | `G3D22126` | W | `linux-local-login-matrix.md` | (no folder) | |
| 4.20r8 Windows | `G3D20126` | W | lab capture | ✔ | tested |
| 5.00r7 Windows | `G3D22067` | W | `lab-v5-2026-10-30.md` | ✔ | tested |
| 5.12 Windows | `G3D14097` | W | `v5v6-windows-unpacked.md` | (no folder) | |
| 5.24r3, 5.24r4, 6.00 beta2 Windows | `G3D15010` | W | `v5v6-windows-unpacked.md` | (no folder) | |
| 5.30r3, 5.31r4, 6.00r2, 6.00r4 Windows | `G3D26090` | W | `v5v6-windows-unpacked.md` | ✔ (5.31r4) | tested |
| 6.00 beta1 Windows | `G3D03048` | W | `v5v6-windows-unpacked.md` | (no folder) | |
| 6.0.0.7, 6.0.1.5 Windows | `G3D3007A` | L | public list | (no folder) | |
| 6.01r1 Linux (x86, x64) | `G3D0108A` | **W** | `linux-local-login-matrix.md` (first-frame observation) | ✔ | **token only (understated)** |
| 6.0.3.4 Windows | `G3D2505C` | L | public list | (no folder) | |
| 6.03r7 Windows | `G3D0311C` | W | `v5v6-windows-unpacked.md`; scrambled string in the exe | (no folder) | |
| 6.03r7 Linux x64 | `G3D0511C` | **W** | `linux-local-login-matrix.md` | ✔ | **token only (understated)** |

### Server-defined login (6.11 and later)

| Build | Token | Grade | Source | Repro | Repro label |
|---|---|---|---|---|---|
| 6.1.1.3 Windows | `GNP1905C` in the one captured connector script | S, W | `protocol/v6113-list-capture.md`; `protocol/v6-login-token-explained.md` | ✔ | tested |
| 6.11r1 Mac | same connector script, `GNP1905C` when replayed | S | Lion replay (`v6-login-token-explained.md`) | none sent (scaffold) | none |
| Worlds 548–614, 71243, 7.0.1.7.5.0 | not stored in the client | S (assumed) | `v7x-protocol.md`; the v7 connector login path has not been traced | 614 stand-in sends `GNP1905C`; the others send none | none |

## Gaps and how far each can be closed

- **B only:** no token value is left at B. Every token from 1.31 to 2.05 has now been seen on the wire from at least one original build. Sibling builds that share a token (2.00 rev1 to rev3, 2.01 rev1, 2.02 rev1, 2.05, 2.05 rev1) are B per build. 1.34 to 1.38 (B+) logged in to a lab server, but their frames were not decoded. The 2.02 family imports a cdecl `zlib.dll` (zlib 1.2.3) and fails to start beside a stdcall zlib build.
- **L only, no binary in any collection:** 1.25, 1.27, 1.391, all 2.1.x releases from 2.12 to 2.21 except 2.17 (2.1.0.x now has three executables, see above), 2.3, 3.0, 3.01, 4.02.11, 4.03.4, 4.11, 6.0.0.7 / 6.0.1.5 and 6.0.3.4. Only a new binary can close these.
- **None:** the pre-1.21 relay builds really have no token. This is a protocol fact, not a missing record.
- **Server-defined:** a 6.11+ client sends whatever its connector script says. One captured script says `GNP1905C`. Any other server or day could say something else, so no per-client token exists to catalogue.

## 2.3

No real 2.3.0.0 binary has been read. The only package labelled 2.3 in the owner-held collections is a modified third-party repack. Its game client is byte-identical to the 2.31 client this repo already reads [bin], so it is a 2.31 install with a 2.3 label and sends `GNW28015`, not `GNW14015`. It does not close the 2.3 gap. The token `GNW14015` is supported by three things:

1. It is on the public version list as 2.3.0.0.
2. Its DDMMY stamp reads 14 Jan 2005, two weeks before 2.31's `GNW28015` (28 Jan 2005).
3. It falls between 2.22 and 2.31 in gs2lib's ordered table.

The repro's 2.3 folder is a 2.31 rebuild sending `GNW14015`. Its post-login tamper-check bytes (PLI 39) are 2.31's: two CRC-32 words over the 2.31 program image. A real 2.3 would send its own bytes. The lab servers read PLI 39 and ignore it, so the stand-in logs in, but its PLI 39 is known to be wrong. Grade stays **L** until a 2.3 binary is read.

## Other observations

- `version-tokens.md` lists the Windows 4.20r8 row twice. Its "lab capture" tags for 5.12 to 6.03r7 Windows agree with `v5v6-windows-unpacked.md`.
- Mac 4.20r6 sends `G3D27076`, but the public list gives 4.11 as `G3D26076`, one day apart. The wire capture stands; why the Mac build carries a 4.1-era stamp is still open (`protocol/login-tokens-3x-7x.md`).
- The public list's `G3D3007A` (6.0.0.7 / 6.0.1.5 Windows) and the Linux 6.01r1 `G3D0108A` are different builds, not a conflict. As with 4.04r2 and 6.03r7, each platform build has its own stamp.

## Open points

- [x] ~~Wire-capture 2.01, 2.03, 2.04 and GraalX.~~ Captured on loopback and logged by a lab gserver on 2026-11-12. Each first frame is type 0, the gen-3 key byte, the token, then the account and password as GCHAR strings. 2.02 rev2, 2.03 and 2.04 add PLI 37 (language) in the same frame.
- [x] ~~Wire-capture 2.02 and 2.02 rev2.~~ Captured 2026-11-12 with a cdecl zlib 1.2.3 beside the unchanged exe.
- [ ] Decode the 1.34–1.38 login frames (they reach their connect window; the dialog still has to be driven).
- [ ] Read a genuine 2.3 binary, if one turns up, and record its token and PLI 39 words.
- [ ] Trace a v7 Worlds login to confirm the connector path supplies its token.
