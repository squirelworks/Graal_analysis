# Drive clients set: what it contains (2026-10-24)

Derived facts from a shared Drive archive of old client builds (one zip, about 122 MB). It holds 73 exes in 55 folders. Full list with sizes and PE file versions: `version-profiles/drive-clients-exes.tsv`. The PE timestamps in these exes are all the same dummy 1992 date, so they say nothing about build date; only the file-version strings are useful, where present.

## Versions present
- Early: 1st, 2nd, 3rd, 4th (+alpha), 5th (+alpha), 6th to 15th Graal ("Nth graal" folders), 1.1, 1.1.9 (+ Gserver), 1.21 (setup only), 1.28b2 (+ GServer, RemoteControl), 1.3b (GServer, RemoteControl), 1.31 to 1.39, 1.411, Graal 3D (+ GServer).
- 2.x: **2.00 (file version 2.0.0.0, 1,812,480 bytes) and rev1 (2.0.0.1), rev2 (2.0.0.2), rev3 (2.0.0.3)**; 2.01 (+ rev1); 2.02 (+ rev1, rev2); 2.03; 2.04; 2.05 (+ rev1, rev2).
- 2.1 test builds `graal21test2` and `graal21test3` (file version 2.1.0.0, about 1.75 MB). They still send the 2.05 token.
- NewMain 24 and 26 (file version 1.4.1.1, token `GNW08011`, with GraalShop, RemoteControl and LevelGen); NewWorld betas 1 and 2 (`Graal-NW.exe`, file versions 2.0.5.0 and 2.1.0.0).
- **Not present:** any 2.1.x release, 2.2x or 2.3x. There is no 2.17, 2.22 or 2.31 exe in this set, and nothing between 2.05 and 2.17 except the two 2.1 test builds. The 2.1 to 2.16 and 2.3 rows therefore stay inferred (`version-profiles/version-coverage-2026-10-24.md`).
- What the set does close: the missing real 2.00 exe, plus three revisions of it.

## Running them (Wine)
- Wine 10 starts the 2.00, 2.05 rev2 and graal21test3 exes (the process stays alive and a window is created).
- Each one stops at "Cannot open file ... commands.rtf", because the Drive folders for 2.0x contain only the exe (and sometimes an `.idc`). The exes need their data files beside them: `commands.rtf`, the image folders and the language files.
- With the data files of another build (checked: 2.00 exe plus NewMain 26 data files) the 2.00 start screen draws normally.
- Run settings: new prefix, loopback-only lab network, private display. Nothing contacted a public network.
- Not run: any login to the lab, any 2.0x network flow, and the 1.x builds.

## Candidates for the next decompile pass
2.01 to 2.04 and the two 2.1 test builds have no decompile yet. A static pass over them would settle the per-build handler differences in `version-profiles/plo-handled-ids-by-build.tsv`, which were read from dispatch tables only.
