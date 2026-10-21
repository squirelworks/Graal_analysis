# Graal Analysis

Cleaned notes on Graal formats, protocol, NPC scripting, and level design. No decompile material.

## Contents

- `npc-library/` — 3,187 unique NPC scripts scraped from GR-V1 `.graal` levels, plus tile-neighbor patterns. See also `gs1-commands.md` for the cleaned command catalog and `gs1-reference-205.md` for the 2.05 command, function, and constant tables.
- `formats/` — GLEVNW01, GANI, GRMAP001, tiletypes, board and system notes. See also `tile-walk.md`, `sign-text.md`, `gobjset01.md`, `level-binary.md` (GR-V1/Z3-V1), and `gmap.md`.
- `protocol/` — packet layouts, login/walk framing, version tokens, capture notes. See also `session-opcodes-cleaned.md`, `codec-and-framing.md`, `packet-ids.md`, `player-props.md`, `file-transfer.md`, `chat-pm-rc.md`, `listserver.md`, and `udp-p2p.md`.
- `client-internals/` — version-id map, offline-play notes, Zelda Online 1998 precursor analysis. See also `config-and-input.md`, `rendering-observations.md`, `offline-training.md`, `client-assets.md`, `foot-test.md`, `version-tokens.md`, and `client-architecture-205.md`.
- `tools/` — cleaned notes on GraalEditor, GraalShop, generators, gif2mng, and RemoteControl.

## Newly scaffolded (2026-10-14)

These notes expand the existing foundation without adding raw decompile material:

- `formats/tile-walk.md` — sheet selection, type-0 allow lists, wall/water rules, stamp ids.
- `formats/sign-text.md` — network alphabet vs file alphabet, controls, drop-in decoder note.
- `formats/gobjset01.md` — stamp format and the 2×2 Bush example.
- `npc-library/gs1-commands.md` — control flow, common commands, pattern letters, offline wiring priority.
- `protocol/session-opcodes-cleaned.md` — common server-to-client meanings that match GLEVNW01 records.
- `client-internals/config-and-input.md` — graalconfig keys, device path, drop-files behavior.
- `client-internals/rendering-observations.md` — frame loop, draw path, offline blit next step.
- `client-internals/offline-training.md` — embedded tutorial levels vs session levels.
- `client-internals/client-assets.md` — pics1/picso sizes, tiledef line, levels/ counts.
- `client-internals/foot-test.md` — single-point movement test and wall/water predicates.
- `client-internals/version-tokens.md` — public GNW token map and filename builds.
- `tools/` — index plus notes on the editor, shop, generators, gif2mng, and RemoteControl.

## Gap-fill pass (2026-10-21)

Sources: GServer-v2 and gs2-parser (GPLv3), gs2lib, graal-serverlist, OpenGS1 (MIT), the Graal Reborn 2.22 docs, and observed behavior of client 2.05 rev 2. The open-source refs are summarized and cited, not copied. Every new fact carries a tag: **[2.05]** confirmed in 2.05, **[srv]** server source only, **[doc]** 2.22 docs, **[cap]** captures, **[inf]** inferred.

- `protocol/codec-and-framing.md` — G-types, u16be+zlib frames, RAWDATA, encryption gens 1–6, the 2.05 gen-3 insertion.
- `protocol/packet-ids.md` — full PLO/PLI tables with 2.05 coverage (59 handled ids).
- `protocol/player-props.md` — PLPROP, NPCPROP, and BDPROP ids and encodings; 2.05 knows 0–42, 50, 51.
- `protocol/file-transfer.md`, `protocol/chat-pm-rc.md`, `protocol/listserver.md`, `protocol/udp-p2p.md`.
- `formats/level-binary.md`, `formats/gmap.md`.
- `npc-library/gs1-reference-205.md`, `client-internals/client-architecture-205.md`.
- Corrections, listed in CONSOLIDATED.md: login key, PLAYERPROPS movement, directions, the GR-V1 bit stream, BoardModify, no GS1 bytecode in 2.05.

## Cross-version pass (2026-10-21)

Static read of the 2.05, 2.17, 2.22, and 2.31 clients and `RemoteControl.exe` from the Graal Reborn 2.2.2.0 folder. Tag **[bin]**.

- `protocol/client-versions.md`: login type, token, cipher, and framing per client; client-side gen-5 send rules; server→client id sets per version; listserver logins (`GNW30123` mapped) and the `arrays2.dat` list config.
- `client-internals/feature-timeline.md`: release-note timeline 2.00–2.31, tied to the protocol changes.
- `tools/remotecontrol.md`: RC (type 6, `GSERV024`, gen 5) and NC (type 3, `NCL11012`) logins and id sets.

## Boundary

Raw decompiles stay out of this repository. These notes are derived from public server sources, observed packet shapes, format documentation, and observed client behavior. They contain no code or addresses from the binaries.
