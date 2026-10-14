# Graal Analysis

Cleaned notes on Graal formats, protocol, NPC scripting, and level design. No decompile material.

## Contents

- `npc-library/` — 3,187 unique NPC scripts scraped from GR-V1 `.graal` levels, plus tile-neighbor patterns. See also `gs1-commands.md` for the cleaned command catalog.
- `formats/` — GLEVNW01, GANI, GRMAP001, tiletypes, board and system notes. See also `tile-walk.md` and `sign-text.md`.
- `protocol/` — packet layouts, login/walk framing, version tokens, capture notes. See also `session-opcodes-cleaned.md`.
- `client-internals/` — version-id map, offline-play notes, Zelda Online 1998 precursor analysis. See also `config-and-input.md`, `rendering-observations.md`, and `offline-training.md`.

## Newly scaffolded (2026-10-14)

These notes expand the existing foundation without adding raw decompile material:

- `formats/tile-walk.md` — sheet selection, type-0 allow lists, wall/water rules, stamp ids.
- `formats/sign-text.md` — network alphabet vs file alphabet, controls, drop-in decoder note.
- `npc-library/gs1-commands.md` — control flow, common commands, pattern letters, offline wiring priority.
- `protocol/session-opcodes-cleaned.md` — common server-to-client meanings that match GLEVNW01 records.
- `client-internals/config-and-input.md` — graalconfig keys, device path, drop-files behavior.
- `client-internals/rendering-observations.md` — frame loop, draw path, offline blit next step.
- `client-internals/offline-training.md` — embedded tutorial levels vs session levels.

## Boundary

Raw decompiles stay out of this repository. These notes are derived from public server sources, observed packet shapes, and format documentation.
