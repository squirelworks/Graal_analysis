# Prior attempts to understand the Graal environment

Date: 2026-10-28

Cleaned summary of the analysis passes that preceded the current notes. No raw dumps.

## Timeline of understanding

| Period | Focus | Outcome |
|--------|-------|---------|
| 2026-09-30 | Entry, forms, formats, config, render, input, anti-debug | Architecture collapsed; GLEVNW01, drop-files, idle/frame identified |
| 2026-10-02 | GS1 dispatch, row table, pattern letters, list flush | DispatchGs1 plated; zlib framing confirmed; version token located |
| 2026-10-03 | Session VMT, sign decode, tile walk, debugger runs | SessionRecv cases, DecodeSignText, type-0 vs type-1/2 collision |
| 2026-10-04 | List ports, world logins, cross-version tokens | 14921/14922/14923 behaviour; GNW03081 construction; world rejections |
| 2026-10-14 | Seihai drop-ins, offline slice | Formats locked; script shape known; pics1 blit and CmdCall still open |

## What remained open at decommission

- Full recovery of type-0 allow lists (GZF lacked PE image)
- Fifteen unplated GS1 opcodes that share the default slot
- Raw gserver pcap (described but never archived)
- List-host S-boxes and remaining needles

These gaps are documented in the Drive zip and in the later cleaned notes of this repository. They are not blockers for the offline slice already exercised by Seihai.

## Relationship to Seihai

The cleaned notes here (tile-walk, sign-text, gs1-commands, session-opcodes, config, rendering, offline-training) were written so Seihai could continue without the raw decompile corpus. The Drive zip preserves the original passes for anyone who later needs the full trail.
