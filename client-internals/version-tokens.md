# Version tokens

Date: 2026-10-14

Internal version strings recovered from the public version list. No decompile material.

| Token | Build notes |
|-------|-------------|
| GNW07080 | 1.39 |
| GNW03081 | 2.05 rev 2 (= 2002ver9 leak build); gen-3 cipher, pre-2.1 code paths |
| GNW31101 | 2.1.0.0–2.1.0.3 (version string not updated) |
| GNW30042 | 2.1.4.0 (first with server-list tabs) |
| GNW15053 | 2.1.9.0 (bz2 + new encryption, new server-list gfx) |
| GNW01113 | 2.2.1.1 (plaintext and zlib; extra compression byte) |
| GNW14015 | 2.3.0.0 |
| GNW28015 | 2.3.1.0 |
| G3D03014 | Linux 3.04 (Torque rewrite; 2.22 protocol, see `protocol/v3x-clients.md`) |
| G3D28015 | Mac OS X 3.153 (2.31 protocol) |
| G3D30123 | 3.x listserver token (the 3.x form of GNW30123) |
| G3D27076 | Mac OS X 4.20r6 (Delphi launcher + C++ engine era; see `protocol/v4x-clients.md`) |
| G3D20126 | Windows 4.20r8 (`GraalEngine.dll`) |
| G3D20126 | Windows 4.20r8 (engine DLL; logs into the `Login` game server) |
| G3D22067 | Windows 5.00r7 (engine DLL, Jul 2007; see `protocol/v5x-clients.md`) |
| G3D14097 | Windows 5.12 (lab capture; see `protocol/v5v6-windows-unpacked.md`) |
| G3D03048 | Windows 6.00 beta1 (lab capture) |
| G3D15010 | Windows 6.00 beta2, 5.24r3, 5.24r4 (lab capture) |
| G3D26090 | Windows 5.30r3, 5.31r4, 6.00r2, 6.00r4 (lab capture) |
| G3D0311C | Windows 6.03r7 (lab capture; Linux 6.03r7 sends G3D0511C) |
| G3D0108A | Linux 6.01r1 (see `protocol/v6x-clients.md`) |
| G3D0511C | Linux 6.03r7 |

Filename builds in the client tree: Graal_2171 = 2.171, Graal_222 = 2.22, Graal_231 = 2.31.

From 2.3 the editor and the online client are separate executables. PE FileVersion is authoritative for the editor (2.3.1.1).

The early-client transition (14801 → 14900 → length+zlib) is the protocol-side counterpart of the same era.

## Confirmed from the binaries (2026-10-24)

The 2.0x family tokens below were read from the character immediates of each client's login builder, so they are confirmed per build rather than taken from a token list. Every value matches the earlier tables here and in `version-id-map.md`. Machine-readable copy: `version-profiles/version-tokens-by-build.tsv`.

| Token | Build | Source |
|-------|-------|--------|
| GNW24011 | 2.00 and rev1, rev2, rev3 (all four exes) | login builder |
| GNW23021 | 2.01, 2.01 rev1 | login builder |
| GNW15041 | 2.02, 2.02 rev1 | login builder |
| GNW20041 | 2.02 rev2 | login builder |
| GNW06051 | 2.03 | login builder |
| GNW24061 | 2.04 | login builder |
| GNW03081 | 2.05, rev1, rev2; also the 2.1 test builds (`graal21test2`, `graal21test3`), which still send the 2.05 token | login builder |
| GNW08011 | NewMain 24 and 26 | login builder |
| GNW13110 | 1.411 | login builder |
| GNW07080 | 1.39 | login builder |
| GNW22060 | 1.38 | login builder |
| GNW22122 | 2.17.1 | lab capture and exe |
| GNW03014 | 2.22 game login | exe |
| GNW28015 | 2.31 game login | lab capture |
| GNW30123 + `newmain` | 2.22 and 2.31 listserver hello (not a game build) | exe and lab |

A lab GServer-v2 only needs the token in its allowed-versions list to let a client in. For 2.00 (`GNW24011`) that is a config entry, not a code patch (`client-internals/decomp-findings-2026-10-24-b/04-v2.00-client.md`).
