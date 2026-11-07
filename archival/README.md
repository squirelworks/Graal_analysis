# Archival notes

Date: 2026-10-28

Prior attempts and early reconstructions of the Graal environment, preserved for reference. These notes predate the later decompile-finding batches and the Seihai walking-collision recovery. They remain useful as a record of the measurement path that locked formats, stamps, and the type table.

No raw decompile material is included.

## Contents

- `foot-test-sdl.md` — the single-point wall test recovered from the SDL reimplementation (2dadventureclient). The real client uses a six-probe body-box routine; see Seihai `documentation/walking-collision.md` and the later Graal_analysis client notes for the current description.
- `client-assets-measured.md` — measured sizes and counts from the official client install (pics1 2048×512, picso, levels/ subdirectory counts, offline tiledef line).
- `version-tokens-early.md` — early public token map (GNW07080 = 1.39, GNW03081 = 2.05, through GNW28015 = 2.3.1.0) and filename builds.
- `tools-early.md` — short notes on GraalEditor, GraalShop, the three generators, gif2mng, and RemoteControl as first measured from format output.

These files are snapshots. Later work in `client-internals/`, `protocol/`, and `tools/` supersedes them where they conflict.
