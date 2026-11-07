# Gemini handoff, 2026-11-07

Static read of a seven-file markdown tarball (`graal-cursor-handoff-2026-11-07`). No binaries, captures, scripts, or dumps. It says it continues a 2026-11-06 pack that was not in this archive. Compared with the notes already on main. Nothing was run.

No new client behaviour. The useful sentences are already written more precisely. The sentences that disagree with those notes are wrong. Open issues #257, #258 and #259 ask for the same text; this package does not answer them.

## Already written

- **Engine line.** 3.04 reports TGE `getVersionNumber` 1100 (`"1.100"`, built 3 Jan 2004). The study splits the clients into a Torque monolith (3.x), a Delphi shell plus a C++ engine with Torque only in the 3D plug-in (4.04r2 through 5.12), and Graal's own engine from 5.24r3, with 6.x in that last group. Marker counts for seventeen binaries are in `torque/study-torque-clients.md`. The 4.04r2 plug-in matches open TGE 1.x and lacks TGE 1.4 lighting, so that DLL is read as the 1.2/1.3 line (`graal3d/torque-engine-4x.md`).
- **3.x protocol and files.** Tokens `G3D03014` / `G3D28015`, list login `G3D30123newmain`, no tamper check, signed `license.graal`, category prefixes, 79 and 88 server ids, `GR-V1.04` heights, `GSERVL01`, and the DES `GWEBL001` cache are in `protocol/v3x-clients.md`. The two Mac uploads named 3.04 and 3.15r2 are the same 3.153 image. The 3.151 Linux installer is the ASCII-mode FTP casualty described there.
- **4.x–6.x.** Launcher / engine split, gen 5, the third-party inflate logger (incoming zlib only, cut to the compressed length), login id 5 with the machine-id list, token `G3D22067`, and the 8-byte licence patch are in `protocol/v4x-clients.md` and `protocol/v5x-clients.md`. Tokens and id tables for the packed 5.12–6.03 builds are in `protocol/v5v6-windows-unpacked.md`. 6.03's PEM/RSA/DSA handling and the scrambled host list are in `protocol/v6x-clients.md`.
- **1998–2001 side builds.** Dates, the 11/12/13-bit board widths, `objects.dat` still in the 1.21 stamp format, the Game Boy font (not the PC sign alphabet), and GraalX keeping `GLEVNW01` are in `client-internals/precursors-and-fan-builds.md`, `formats/level-binary.md` and `client-internals/build-catalogue.md`.

## Dropped

- **"TGE 1.2-era, do not re-litigate."** 3.04's own version call is 1.100. Calling every later build 1.2 flattens the 1.2/1.3 reading of the 4.04r2 plug-in and the 5.24 cut.
- **"Modern Torque3D is the wrong base."** Settled owner direction, not a measurement of a client. Seihai builds its own engine and does not bring in Torque3D. graal-client-repro is the separate project for historical fidelity. `torque/README.md` already says an open TGE 1.x base covers most of the 4.04r2 world, while 5.12's `GameObject` layer is Graal's.
- **Monolith, then hybrid, then "residual" early 5.x, then 6.x.** 4.20r6 Mac is one binary, not a Delphi hybrid. 5.00r7 and 5.12 still ship a Torque 3D plug-in (`SimObject`, `GameConnection`, terrain, DTS). Torque's engine is already gone in 5.24r3, before 6.x. "Residual" is not a behaviour.
- **3D servers use the Torque parser's default UDP port.** `protocol/v3x-clients.md` already says that number is only the default when no port is given. The client uses the listed port plus one.
- **List login flushes between id 7 and id 1.** The 3.04 lab sent both in one plain zlib frame (`version-profiles/lab-304-linux-2026-10-30.md`). The handoff repeats the static-read mistake that note corrected.
- **`GRMAP001` gains `HEIGHTMAP` and `RANDOMSEEDS` in 3.x.** 2.22 and 2.31 already read those keys. No 3.x-only key was found.
- **"Editing the list host requires patching the signature."** Editing the signed file does. The 3.04 lab redirected the name with a hosts entry and left the signature alone.
- **4.x "list server" on a public login host, port 14900.** 4.x and 5.x open a game connection to a server named Login. There is no separate list protocol. The host string in the handoff is a real public name and is not copied here.
- **"v4/v5/v6 tokens and packet tables are not recovered" (paused 2026-10-22).** Recovered in the notes named above. 6.03's hosts are scrambled and decoded at runtime; they are not absent.
- **6.03 "adds JSON parsing."** PEM/RSA/DSA is already noted. JSON is one unverified word, with no string or library name in this archive.
- **7.x Worlds is Unity IL2CPP plus `Graal3DEngine.dll`.** No strings, file lists, or dumps here. The only "7" already on main is an updater package inside a used 5.00r7 folder naming `Graal4.exe` 7.20, which is not a client engine. Issue #257 asks for this paragraph. Left open.
- **Precursor table, bit widths, GraalX, the CRC patch, the packet logger.** Same facts, fewer of them, and the CRC patch omits the 8-byte diff.
- **Roadmap for another repository** (`common/torque/{full,hybrid,residual}`, a modular login, a new encrypted handshake). Layout and policy, not observed client behaviour. No Torque code was added anywhere, and nothing in the Seihai repos was changed.
- **Issue #243** (land the Torque study and capture 3.04 stage 0). The study is already on main (`torque/study-torque-clients.md`, merged as #242). This archive has no `console.log`, screenshots, or `prefs.cs`.
- **Decision log, "treat as fixed."** The split is settled owner direction: Seihai uses its own engine, and graal-client-repro pursues historical fidelity. It is not observed client behaviour. The archive's `common/torque/{full,hybrid,residual}` layout stays a plan, not a behaviour.

## Left out of the repo

The stalled-client note names a public login host. That string is not in this commit. The archive itself has no passwords, keys, or player messages. It only warns that some 5.00r7 folder elsewhere holds private messages, profiles, and a buddy list; those files were not in the tarball. No decompiled C and no binary addresses.

## Dirty pack, same day

A second archive from this pass was read after the note above. It holds address dumps, local paths, string scans, and a cleaned 7.x write-up. Addresses, paths, hosts, and the bundles are not copied.

The 3.04 string list matches the study: one binary, with SimObject, NetConnection, GameConnection, TGraalConnection, datablocks, and the console compiler. [bin]

Scans of the 4.20r8 and 5.00r7 engine DLLs find TGraalConnection and do not find NetConnection, GameConnection, SimObject, or datablock. Hits on "ghost" are Graal words (ghostani, ghostsnear, a ghost-always login event) and the colour name ghostwhite. Those scans did not include a separate 3D plug-in, so they do not change the plug-in finding in `torque/study-torque-clients.md`. [bin]

The 6.x scan's seven "Torque" hits are that colour name, a printmap datablock tool, two `t2d` datablock constructor strings, and TGraalConnection. Those constructor strings are not a Torque 2D engine. [bin]

The pack's cleaned note still says 7.x is a Unity host around `Graal3DEngine.dll`, under an internal name Quattro. The only support in the archive is an address-level index, which is not copied. Issues #257, #258, and #259 stay open.
