# Graal Analysis

Cleaned notes on Graal formats, protocol, NPC scripting, and level design. No decompile material.

## Contents

- `npc-library/` — 3,187 unique NPC scripts scraped from GR-V1 `.graal` levels, plus tile-neighbor patterns. See also `gs1-commands.md` for the cleaned command catalog.
- `formats/` — GLEVNW01, GANI, GRMAP001, tiletypes, board and system notes. See also `tile-walk.md`, `sign-text.md`, and `gobjset01.md`.
- `protocol/` — packet layouts, login/walk framing, version tokens, capture notes. See also `session-opcodes-cleaned.md`.
- `client-internals/` — version-id map, offline-play notes, Zelda Online 1998 precursor analysis. See also `config-and-input.md`, `rendering-observations.md`, `offline-training.md`, `client-assets.md`, `foot-test.md`, and `version-tokens.md`.
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

## Added 2026-10-21: editor, offline mode, sound

- `client-internals/level-editor-205.md`: the level editor built into the 2.05 client (keys, tile undo, object dialogs, save formats).
- `client-internals/offline-tutorial-205.md`: how 2.05 goes offline, where offline levels come from, and the 13 embedded tutorial levels.
- `client-internals/sound-and-music.md`: 2.05 effects, MIDI over MCI, and the Winamp hook, compared with BASS and voice chat in 2.17/2.22/2.31.
- `tools/graaleditor-vs-205.md`: GraalEditor 2.3.1.1 and GraalShop compared with the built-in editor.
- `formats/grv1-decoder/`: a small GR-V1 / Z3-V1 level decoder.

## Boundary

Raw decompiles stay out of this repository. These notes are derived from public server sources, observed packet shapes, and format documentation.
