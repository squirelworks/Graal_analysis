# Argon/Grok handoff, 2026-11-07

Static read of one handoff archive (seven markdown files, about 20 KB). No binaries, no captures, no script dumps. The archive is a tasking pack: a decision log, a roadmap for historical-client folders, an issue list, and two cleaned summaries that say they were paused on 2026-10-22. It points at a Gemini pack (a script dump and a disassembler project) that is not in the archive. Those files stay out.

Nothing here replaces `protocol/v3x-clients.md`, `protocol/v4x-clients.md`, `protocol/v5x-clients.md`, `protocol/v6x-clients.md`, `torque/`, or `client-internals/precursors-and-fan-builds.md`. Those notes are later and more specific. Claim ids are stable names so a second ingest of a different archive can drop duplicates.

Public hostnames appeared in two summary lines and are omitted. The archive warns that a used 5.00r7 folder holds private messages, profiles and a buddy list. That folder is not in the archive. No credentials were present.

## Verdicts

| Id | Verdict | Why |
|---|---|---|
| ARGON-FLUSH | Dropped | The 3.x summary puts a flush between listserver id 7 (`G3D30123newmain`) and id 1. The 3.04 lab frame holds both messages (`protocol/v3x-clients.md`, `version-profiles/lab-304-linux-2026-10-30.md`). |
| ARGON-UDP-DEFAULT | Dropped | The 3.x summary treats the Torque address parser's no-port default as the 3D server port. 3D UDP is the listed port plus one (`protocol/v3x-clients.md`, `torque/network.md`). |
| ARGON-GRMAP-GAINS | Dropped | The summary says 3.x `GRMAP001` gains `HEIGHTMAP` and `RANDOMSEEDS`. 3.x reads the same keys as 2.22/2.31, and no 3.x-only key was found (`protocol/v3x-clients.md`). |
| ARGON-V3-IDS | Already documented | 79 ids in 3.04, 88 in 3.153, id 84 kept, id 44 dropped in 3.153, and 3.153's 67, 74, 82, 104, 131–134, 187, 189 are the table in `protocol/v3x-clients.md`. The summary's "open" client-to-server vtable pass is stale: the 3.04 sent-id set is already complete. |
| ARGON-V3-LOGIN | Already documented | Tokens `G3D03014` / `G3D28015`, id 37 next, no id 39, gen 5, category prefixes, RSA-signed `license.graal` on port 14922, `.dso` version 33, `GR-V1.04` heights, `GSERVL01` on the text parser, `GWEBL001` still DES. The Mac "3.04" upload being the 3.153 image, and the damaged 3.151 installer, are the same note. |
| ARGON-V4-LISTSERVER | Dropped | The 4.x summary calls the license target a list server and spells a public hostname. From 4.x the client logs into a game server named `Login` on port 14900. There is no separate listserver protocol (`protocol/v4x-clients.md`). |
| ARGON-V4-LOGGER | Already documented | Incoming zlib only, cut to the compressed length, is the packet-logger section of `protocol/v4x-clients.md`, which also says outgoing frames are not logged. |
| ARGON-V4-MAGICS | Dropped | "Same magics as 3.x" skips `GRPKG001`, which 4.x adds (`protocol/v4x-clients.md`). |
| ARGON-V5-TOKEN | Dropped | `G3D22067` is the 5.00r7 token. Later 5.x builds use other tokens (`protocol/v5x-clients.md`, `protocol/v5v6-windows-unpacked.md`). |
| ARGON-V5-PACK | Already documented | 5.00r7 unpacked with a Delphi launcher and `GraalEngine.dll`; 5.12–5.24 MoleBox-style; 5.30/5.31 Themida. The summary's "MoleBox or Themida" for everything after 5.00r7 is the looser form. The CRC patch (skip missing file, bad signature, and line count) is `protocol/v5x-clients.md`. |
| ARGON-V6-UNRECOVERED | Dropped | The summary says the 6.x login token, cipher and packet ids are still unknown. `protocol/v6x-clients.md` has `G3D0108A` and `G3D0511C`, gen 5, and the handled-id lists. Hosts are compiled in and scrambled. A plain string search misses them. |
| ARGON-JSON | Dropped | "6.03 adds JSON parsing" has no file, no fields and no call. PEM/RSA/DSA on 6.03 is already in `protocol/v6x-clients.md`. |
| ARGON-TGE-12 | Dropped | "TGE 1.2-era, do not re-litigate" flattens a checked split. 3.04 reports `getVersionNumber` 1100, formatted 1.100, on a TGE 1.1–1.2 code base (`torque/engine-and-formats.md`). The 4.04r2 3D plug-in is the TGE 1.2/1.3 line (`graal3d/torque-engine-4x.md`). |
| ARGON-RESIDUAL | Dropped | "3.x monolith, 4.x hybrid, early 5.x residual, 6.x gone" does not match the three eras in `torque/study-torque-clients.md`. 5.12 still has Torque netcode. Torque 3D is gone from 5.24r3, with GS2 GUI names left. Windows 4.x is a Delphi launcher plus engine DLL plus an on-demand 3D DLL; Mac 4.20r6 is one binary. |
| ARGON-7X-UNITY | Dropped | "7.x Worlds is Unity plus `Graal3DEngine.dll`" is an assertion with no observation in the archive. That DLL name is already the 4.x/5.12 3D plug-in (`torque/README.md`). Open PR #260 adds 7.x protocol tables and does not describe a Unity client. |
| ARGON-CLASSES | Already documented | `NetConnection`, `GameConnection`, `TGraalConnection`, `ConnectionProtocol`, ghosting and datablocks are named in `torque/engine-and-formats.md` and `protocol/v3x-clients.md`. The archive asks which of them the Graal layer called, and does not answer. |
| ARGON-BITS | Already documented | Code widths (11-bit `Z3-V1.02`, 12-bit `Z3-V1.03`/`1.04` and `GR-V1.00`/`01`, 13-bit `GR-V1.02`/`03`) are `client-internals/precursors-and-fan-builds.md`. The board is least-significant-bit first (`formats/level-binary.md`). |
| ARGON-PRECURSORS | Already documented | Zelda Online 1 (single-player Java 1.0, class files 16 May 1998), Zelda Online 2 (Java 1.1, local lobby), ZeldaEditor (Delphi 3, about 25 July 1998), Java Graal (July 2000, relay on 14802) and the 1999 Game Boy Color demo are `client-internals/precursors-and-fan-builds.md`. Zelda Online 2's files span 18–26 July 1998. The archive's single day, and a Java Graal day-of-month, are not kept. |
| ARGON-GBC-FONT | Already documented | The Game Boy demo's text alphabet is a straight run, distinct from the PC sign alphabet (`client-internals/gameboy-demo.md`). |
| ARGON-GRAALX | Already documented | Linked 2001-03-07, keeps the `GLEVNW01` reader and writer that 2.0 and 2.01 dropped (`client-internals/build-catalogue.md`). "Restored" is the wrong verb. |
| ARGON-OBJECTS | Already documented | The `objects.dat` stamp layout used by ZeldaEditor is the layout shipped with Graal 1.21 (`client-internals/precursors-and-fan-builds.md`). |
| ARGON-POLICY | Dropped | The decision log says to treat as fixed: Torque work outranks the server suite, historical clients get a `common/torque/{full,hybrid,residual}` scaffold, and a modular replacement login. That is owner priority, not a checked behaviour. It is not adopted here. |
| ARGON-ISSUES | Already filed | Graal_analysis #257, #258, #259 and #243, and graal-client-repro #148 and #150–#154, match this pack's titles. Filling #257–#259 from this text would republish the rows dropped above. #242 is already merged. |
| ARGON-SIZE | Dropped | "Linux 3.04 unpacks to about 7 MB" is not checked from this archive. |

## Left for the owner

- Graal_analysis #243 and graal-client-repro #110 leave the Torque rebuild's language to the owner. This note does not start the observatory, the scaffold, a 3.04 stage-0 capture, or a 7.x Unity pass.
- `docs/NEXT.md` item 13, tracked in #247, stays the owner's call. This archive does not contain a 5.x/6.x `Login` capture.

## Dirty pack, same day

A second archive from this pass was read after the table above. It holds address dumps, local paths, string scans, and a cleaned 7.x write-up. Addresses, paths, hosts, and the bundles are not copied.

The 3.04 string list matches the study: one binary, with SimObject, NetConnection, GameConnection, TGraalConnection, datablocks, and the console compiler. [bin]

Scans of the 4.20r8 and 5.00r7 engine DLLs find TGraalConnection and do not find NetConnection, GameConnection, SimObject, or datablock. Hits on "ghost" are Graal words (ghostani, ghostsnear, a ghost-always login event) and the colour name ghostwhite. Those scans did not include a separate 3D plug-in, so they do not change the plug-in finding in `torque/study-torque-clients.md`. [bin]

The 6.x scan's seven "Torque" hits are that colour name, a printmap datablock tool, two `t2d` datablock constructor strings, and TGraalConnection. Those constructor strings are not a Torque 2D engine. [bin]

The pack's cleaned note still says 7.x is a Unity host around `Graal3DEngine.dll`, under an internal name Quattro. The only support in the archive is an address-level index, which is not copied. Issues #257, #258, and #259 stay open.
