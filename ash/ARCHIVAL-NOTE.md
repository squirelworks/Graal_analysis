# Archival Note — 39ster 2.1 GServer Analysis (October 2026)

This directory contains reverse-engineered architecture notes from the decommissioned Graal 39sters gServer analysis project.

## What is preserved here

- `ARCHITECTURE.md` — system context, process model, class graph, data stores.
- `INDEX.md` — pack overview.
- `ALGORITHMS.md` — GCHAR codec, zlib framing, PLAYER descramble (LCG `iterator = iterator * 0x8088405 + key`, start `0x04A80B38`), GR-V1 tile bitstream, ID generation, outbound/inbound packet handling.
- Existing `OPCODE-MAP.md` already cross-references 39ster names against modern tables.

## Prior attempts documented

The original analysis produced:

1. A complete museum copy of the 39ster 2.1 source tree + debug data (`39sters-2.1-Gserver/`).
2. The Ash blueprint pack (these files).
3. A C++ reference rebuild called **Phoenix** that implemented:
   - GR-V1 `.graal` loading
   - WANTGIF file serve
   - Account txt save/load
   - Board-modify and combat packet relays
   - RC account editor opcodes 70–87
   - Protocol: 2-byte BE length + zlib + newline-separated messages
   - Player decrypt via the LCG above

Phoenix had no `.nw` parser, no GS script VM, and only a listserver stub.

## Full archive

The complete original data, Phoenix source, and earlier analysis packs were zipped as **Graal 39sters gServer.zip** and placed on Google Drive under `/[Grok/[Projects/` on 2026-10-28.

This PR stores the key archival notes so they remain discoverable inside Graal_analysis without requiring the external zip.

## Suggested use for Seihai / future work

- Align client scramble and framing notes against the exact 2006 LCG and GCHAR rules.
- Use the GR-V1 bitstream description when validating level loaders.
- The start map for the stub account loader was `level13.graal`.
- Default port was 14822.

These notes describe the **2006 server as written**. Later open-source servers (GServer-v2, etc.) evolved beyond it.
