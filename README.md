# Graal Analysis

Cleaned notes on Graal formats, protocol, NPC scripting, and level design. No decompile material.

## Contents

- `npc-library/` — 3,172 unique NPC scripts scraped from GR-V1 `.graal` levels, plus tile-neighbor patterns. See also `gs1-commands.md` for the cleaned command catalog and `gs1-reference-205.md` for the 2.05 command, function, and constant tables. Archival notes on a prior larger documented extract are in `npc-library/archival-scripting-notes.md`.
- `formats/` — GLEVNW01, GANI, GRMAP001, tiletypes, board and system notes, and save games (`graalsav.md`). See also `tile-walk.md`, `sign-text.md`, `gobjset01.md`, `level-binary.md` (GR-V1/Z3-V1), and `gmap.md`.
- `protocol/` — packet layouts, login/walk framing, version tokens, capture notes. See also `session-opcodes-cleaned.md`, `codec-and-framing.md`, `packet-ids.md`, `player-props.md`, `file-transfer.md`, `chat-pm-rc.md`, `listserver.md` (with `public-listserver-2026-10-25.md`, the first observed public replies), `udp-p2p.md`, `v3x-clients.md` (Graal 3.x Linux/Mac clients), `v4x-clients.md` (Graal 4.x Windows/Mac clients), `v5x-clients.md` (Graal 5.x Windows clients), `v6x-clients.md` (Graal 6.x Linux, Mac and Windows clients, incl. the 6.11 server-defined protocol), `v5v6-windows-unpacked.md` (the packed 5.12–6.03 Windows builds, unpacked and run: tokens, logins, id tables), `relay-1998.md` (the 1998 text relay), and `gserv-1999.md` (GSERV007–018 logins, gen 2).
- `client-internals/` — version-id map, offline-play notes, Zelda Online 1998 precursor analysis. See also `config-and-input.md`, `rendering-observations.md`, `offline-training.md`, `client-assets.md`, `foot-test.md`, `version-tokens.md`, `client-architecture-205.md`, `des-and-hidden-strings.md` (hidden hosts, 2.22 saved passwords), and `newworld-betas.md` (the two NewWorld beta clients).
- `graal3d/` — the February 2000 Graal3D client and its GServer: protocol (TCP + peer-to-peer UDP), props, accounts, `.x` levels, and how it relates to the 2D GServer.
- `tools/` — cleaned notes on GraalEditor, GraalShop, generators, gif2mng, RemoteControl, and `lab-setup.md` (the offline capture lab).
- `archive/` — archival notes on decommissioned experimental walkers and tileset work (Ember / Avelan). Full assets live in a Drive zip; see `archive/ember-avelan-experimental.md`.

## Newly scaffolded (2026-10-14)

These notes expand the existing foundation without adding raw decompile material:

- `formats/tile-walk.md` — sheet selection, type-0 allow lists, wall/water rules, stamp ids.
- `formats/sign-text.md` — network alphabet vs file alphabet, controls, drop-in decoder note.
- `formats/gobjset01.md` — stamp format and the 2×2 Bush example.
- `npc-library/gs1-commands.md` — control flow, common commands, pattern letters, offline wiring priority.
- `protocol/session-opcodes-cleaned.md` — common server-to-client meanings that match GLEVNW01 records.
- `client-internals/config-and-input.md` — graalconfig keys, device path, drop-files behavior.
- `client-internals/rendering-observations.md` — frame loop, draw path, offline blit next step.
- `client-internals/water-and-ganis.md` — the built-in animation name table, swim and lava, splashes, break-effect sounds (2.05).
- `client-internals/status-display.md` — the HUD: `state.png` rects, screen positions, heart rows and `showstats` bits (2.05 routine; 2.22 sheet and picture match).
- `client-internals/bare-level-names.md` — no client from 1st Graal to 2.05 adds `.zelda` to a bare level name or falls back between extensions; the editor adds `.graal` on save.
- `client-internals/id24-205.md` — id 24 in 2.05 is the same weapon-image list as later (tags 0 to 6, 60-call full-list countdown, UDP id 15 twin); corrects the "four-field form" note.
- `client-internals/damage-sources.md` — hearts taken by bombs, blasts, arrows and the other shots, thrown objects and baddies; hit boxes and the no-kill rule (2.05).
- `client-internals/status-bit-0x20.md` — STATUS bit 0x20 is the `hidesword` timer; how it is set and what it gates (2.05).
- `client-internals/sign-panel.md` — the sign panel from `letters.png` (glyph grid, frame, `#` button codes, paging keys) and what an NPC with no image draws (2.05).
- `client-internals/ledges-push-pull.md` — ledge jumps (array 8 per facing, the 8-tick curves), pushing and pulling stone blocks (array 16), the held grab, the futile pull, and the `pushed`/`pulled` trigger actions (2.05).
- `client-internals/live-trace-205.md` — live 2.05 traces: the client reports its own CURPOWER on a hit, ledge-jump timing and running in place, deep water, lava swim and the 101-tick burn, and the death/respawn sequence after a server CURPOWER 0 (respawn at the login point, CURPOWER 6, death loop).
- `client-internals/body-colours-and-attributes.md` — how 2.05 colours a body (palette entries per slot, the 20 colours, new-player defaults), what the looks commands change, and GANI attribute sprites and `DEFAULTATTR` (the hat, props 37–41).
- `client-internals/carry-hide-and-glove.md` — hiding under a carried bush or stone with D (mode 14, poses, sprites, STATUS 0x02), the glove scale (players start at 1, so pots lift) and lifting `canbecarried` NPCs (2.05).
- `client-internals/offline-training.md` — embedded tutorial levels vs session levels.
- `client-internals/client-assets.md` — pics1/picso sizes, tiledef line, levels/ counts.
- `client-internals/lab-captures-2026-10-25/` — real 2.22 lab captures: chests (open facing up only), packet 40 gates, CURPOWER units, respawn target, default weapon image ids.
- `client-internals/foot-test.md` — single-point movement test and wall/water predicates (the 2.05 client's real wall test is a box: see `client-internals/decomp-findings-2026-10-25-l/`).
- `client-internals/version-tokens.md` — public GNW token map and filename builds.
- `client-internals/build-catalogue.md` — every archived client build 1998–2001: hash, link date, token, encryption gen, list host, level formats.
- `client-internals/build-diff-204-205.md` — function-level diff of 2.04, 2.05 rev1 and 2.05 rev2 (NewWorld merge, VMT shift, ADP anti-debug).
- `client-internals/cross-version-timeline.md` — classes, GS1 commands and handled packet ids from 1.33 to the 2.1 tests.
- `client-internals/version-profiles/` — per-version client profiles 1.41–2.17 (TOML + resolver): wire ids sent and handled, props, login, files, and player-visible features, with a source tag on every value.
- `tools/` — index plus notes on the editor, shop, generators, gif2mng, RemoteControl, and the 2001 NPC server (`npcserver-2001.md`).

## Gap-fill pass (2026-10-21)

Sources: GServer-v2 and gs2-parser (GPLv3), gs2lib, graal-serverlist, OpenGS1 (MIT), the Graal Reborn 2.22 docs, and observed behavior of client 2.05 rev 2. The open-source refs are summarized and cited, not copied. Every new fact carries a tag: **[2.05]** confirmed in 2.05, **[srv]** server source only, **[doc]** 2.22 docs, **[cap]** captures, **[inf]** inferred.

- `protocol/codec-and-framing.md` — G-types, u16be+zlib frames, RAWDATA, encryption gens 1–6, the 2.05 gen-3 insertion.
- `protocol/packet-ids.md` — full PLO/PLI tables with 2.05 coverage (59 handled ids).
- `protocol/player-props.md` — PLPROP, NPCPROP, and BDPROP ids and encodings; 2.05 knows 0–42, 50, 51.
- `protocol/file-transfer.md`, `protocol/chat-pm-rc.md`, `protocol/listserver.md`, `protocol/udp-p2p.md`.
- `formats/level-binary.md`, `formats/gmap.md`.
- `npc-library/gs1-reference-205.md`, `client-internals/client-architecture-205.md`.
- Corrections, listed in CONSOLIDATED.md: login key, PLAYERPROPS movement, directions, the GR-V1 bit stream, BoardModify, no GS1 bytecode in 2.05.

## Added 2026-10-21: editor, offline mode, sound

- `client-internals/level-editor-205.md`: the level editor built into the 2.05 client (keys, tile undo, object dialogs, save formats).
- `client-internals/offline-tutorial-205.md`: how 2.05 goes offline, where offline levels come from, and the 13 embedded tutorial levels.
- `client-internals/sound-and-music.md`: 2.05 effects, MIDI over MCI, and the Winamp hook, compared with BASS and voice chat in 2.17/2.22/2.31.
- `tools/graaleditor-vs-205.md`: GraalEditor 2.3.1.1 and GraalShop compared with the built-in editor.
- `formats/grv1-decoder/`: a small GR-V1 / Z3-V1 level decoder.

## Cross-version pass (2026-10-21)

Static read of the 2.05, 2.17, 2.22, and 2.31 clients and `RemoteControl.exe` from the Graal Reborn 2.2.2.0 folder. Tag **[bin]**.

- `protocol/client-versions.md`: login type, token, cipher, and framing per client; client-side gen-5 send rules; server→client id sets per version; listserver logins (`GNW30123` mapped) and the `arrays2.dat` list config.
- `client-internals/feature-timeline.md`: release-note timeline 2.00–2.31, tied to the protocol changes.
- `tools/remotecontrol.md`: RC (type 6, `GSERV024`, gen 5) and NC (type 3, `NCL11012`) logins and id sets.

## Version profiles

- `version-profiles/2.22-2.31.md` and `.toml`: per-version profiles for 2.22, 2.3 (inferred) and 2.31. Covers the wire protocol, the start window, server-list tabs, editor presence, options, GS1 symbol changes, and feature switches for Seihai.

## Decompile findings, batch b (2026-10-24)

- `client-internals/decomp-findings-2026-10-24-b/`: tamper-check (PLI 39) derivation, 2.31 periodic traffic, payload layouts of server ids above 48 (2.17.1, 2.22, 2.31), the 2.00 client, open items, and a cross-check against the repo. Tables are in `version-profiles/` (`plo-layouts-217-231.tsv`, `plo-handled-ids-by-build.tsv`, `pli-sent-ids-by-build-20x.tsv`, `tampercheck-words.tsv`, `version-tokens-by-build.tsv`, `drive-clients-exes.tsv`).
- `client-internals/drive-clients-inventory.md`: what the Drive clients set contains and which builds are still missing.

## Decompile findings, batch c (2026-10-24)

- `client-internals/decomp-findings-2026-10-24-c/`: 20 builds from 2.00 to the 2.1 tests, NewWorld betas and NewMain 24/26 (Ghidra + IDR). Login tokens, handled server ids and sent client ids per build, handler changes by build, UDP channel, test builds, vocabulary, and corrections to batch b. Tables are in the same folder. The 2.1 test decompiles are lossy, so only their structure is reliable.

## Decompile findings, batch d (2026-10-25)

- `client-internals/decomp-findings-2026-10-24-d/`: sword damage (attacker's sword power in half hearts, heal rule, hurt mode, the sword-power byte), the extra gates on a hit, and the respawn entry-save rule (gmap-list test, the 2.05-only name group) from the 2.05 rev 2, 2.17.1, 2.22 and 2.31 clients. Tables are in the same folder. Static read only, nothing was seen on a wire.

## Decompile findings, batch e (2026-10-25)

- `client-internals/decomp-findings-2026-10-25-e/`: file-transfer caching rules (the three name lists, the window of four requests per kind, how replies settle names, when a local file counts as checked, where downloads are saved and with which time) from the 2.00, 2.05 rev 2, 2.17.1, 2.22 and 2.31 clients, checked against the 2.17, 2.22 and 2.31 captures already summarised in earlier notes. Tables are in the same folder.

## Decompile findings, batch f (2026-10-25)

- `client-internals/decomp-findings-2026-10-25-f/`: what real `GR-V1.03` levels show (two supplied files and an archive of 3113 binary levels): section shapes and the no-sign file ending, link arrivals written as `playerx`/`playery` plus an offset, the baddy section ending only at a first byte of 0x80 or more (x = 0 is a valid baddy), sign `#K(n)` escapes, chest sign index -1, and aggregate counts. Counts and structure only; no level content or file names. The table `corpus-stats.tsv` is in the same folder. Small corrections to the `grv1.py` decoder and `level-binary.md` are in a separate commit.

## Level editor notes (2026-10-25)

- `tools/level-editor/`: the classic Graal level editor, with the editor built into the 2.22 client as the primary reference (`222-reference.md`) and every other build as a delta (`version-deltas.md`: 1st Graal to 2.31, the New World betas, the standalone GraalEditor). Also a cross-reference to the format notes and batch f (`formats-crossref.md`) and a Seihai tracking checklist (`seihai-tracking.md`, 2.22 feature list in implementation order, then per-version deltas). New: the text reader's `BOARD` rules, the 9 x 9 `HEIGHTS` block, save format by file extension, the warp-field defaults, the key map additions, change-log dated features, and a class timeline across every build. Mouse handling and two mode flags are structure-only. Corrections: the tile id to sheet mapping in `client-internals/client-assets.md`, and the baddy section ending in `client-internals/level-editor-205.md`.

## Decompile findings, batch g (2026-10-25)

- `client-internals/decomp-findings-2026-10-25-g/`: the three fields that were still unknown. Client id 24 (relayed as 32) is the sender's list of weapon-script images, and the one byte every real client sends is its "full list" marker with no images; the format, the sender's wrap timing, why 2.22 sends only with another player present, and the receiver's rules. Client id 46 is a content-free level-switch notice with a literal 1 (one send site, 2.31 only). Server id 178 is read with the clients' comma-text rules (white space splits unquoted items, so names with spaces must be quoted; the type prefix is dropped from the name). What a real list service sends for 178 is still unobserved. Tables are in the same folder. Static read plus source of the open-source servers; nothing new was seen on a wire.
- `client-internals/decomp-findings-2026-10-25-j/`: `Z3-V1` (`.zelda`) levels checked against 139 distinct real files (663 copies, 1st Graal to 15th Graal and the Java Zelda Online folder) and the Java, 1st Graal and 1.39 loaders. All files read to exactly their end. Findings: `Z3-V1.03` links carry decimals (124 of 207 have a decimal x, y, width or height) and negative arrivals mean "keep the player's coordinate" (151 links; 805 `GR-V1` links too); computer records are `x y type` plus a rest-of-line that is empty in `.03` and a three-verse text in `.04`, with `0x0A` allowed as a coordinate; the extension decides nothing (31 `Z3-V1.04` files sit under `.graal`, 694 `.zelda`-named files are `GR-V1`); every Graal client binary carries both magics. Counts and structure only; the tables `by-build.tsv` and `format-stats.tsv` are in the same folder.

## Decompile findings, batch k (2026-10-25)

- `client-internals/decomp-findings-2026-10-25-k/`: the leftovers of the damage and file-transfer notes. A hit pushes the player one tile a tick for five ticks along a unit vector (zero means east), undoing a step when one of twelve body-box points is blocked (identical in 2.05 rev 2, 2.17.1, 2.22 and 2.31); packets 40 and 46 go through the sword's gates (AP 100, the shared once-a-second stamp taken before the guild test, the guild tag) with no attacker status test, power capped at one heart and 0 accepted; packet 46 is a box of strictly under 2 tiles around the centre (X+1.5, Y+2.0). The save-folder layouts per build: 1.33 to 1.41 save everything in one folder, 2.00 and 2.01 have no `hats`, both 2.1 test builds have no `maps`, and every build ignores a zero-length stream. Static read; nothing new was seen on a wire.

## Decompile findings, 2026-10-28 (b)

- `client-internals/decomp-findings-2026-10-28-b/`: how 2.05 decides tile types. The default tileset has no type table, and each type test asks one `arrays.dat` list (array 2 throw-through, 4 chair, 5 and 6 bed, 1 water with lava included, 3 lava, 8 jumping stone per direction). Tilesets of the new kind use a fixed rule by sheet position. `tiletype()` returns -1 on the default tileset. Static read; `tile-type-lists.tsv` is in the same folder.

## Precursors and fan builds (2026-10-29)

- `client-internals/precursors-and-fan-builds.md`: Zelda Online 1 and 2, Knorr's 1998 ZeldaEditor (whose dialogs became 1st Graal's editor), the GServ lobby with source, password saves, `objects.dat` and `arrays.dat`, Java Graal (2000), the Graal Game Boy Color demo (1999), 39ster's 2014 offline client, and how they relate.
- `client-internals/gameboy-demo.md`: the full disassembly of the Game Boy Color demo. It covers the GBDK/LCC build, the bank map, the room format (links, texts, NPC records) and all seven rooms, the 31 character types, controls, lifting, entity states and the sound player. The disassembly itself is in the project's shared folder.
- `client-internals/precursor-runs-2026-10-30.md`: Zelda Online 2, Java Graal and the Game Boy Color demo run for real. It gives the game-feel numbers from the Java sources (20 Hz ticks, the 0.9 s push pose and 1.4 s stone push, the bush drop table, no respawn timer, chat as outlined text with no bubble) and what the wire showed (room names, a doubled relay when two clients pair at once).

## Boundary

Raw decompiles stay out of this repository. These notes are derived from public server sources, observed packet shapes, format documentation, and observed client behavior. They contain no code or addresses from the binaries.

## Version profiles 1.33–1.39 (2026-10-23)

- `client-internals/versions-133-139.md`: what changes between the seven gen-2 GNW clients, on the wire and for the player (HUD art, tiles, windows, controls, rules).
- `client-internals/version-profiles/v133-v139.toml`: the same as a machine-readable table, one `[[version]]` per build, with confidence notes and first-build feature flags.

## Archive (2026-10-28)

- `archive/ember-avelan-experimental.md`: archival notes on the decommissioned Ember/Avelan experimental walkers, tileset variants, and the type-0 mask. Full project zip is on Google Drive under `/[Grok/[Projects/Graal Enigma Playerworld.zip`.

## Graal 4.x clients (2026-10-29)

- `protocol/v4x-clients.md`: Windows 4.20r8 (a third-party packet-logger build) and Mac OS X 4.20r6, read statically. The Delphi launcher plus C++ `GraalEngine.dll` split, `loginserver.graalonline.com:14900` with no separate listserver protocol, tokens `G3D27076` / `G3D20126`, the login's PC-id fields, saved-password DES, gen 5 unchanged, 101 handled server ids (13 new over 3.153), the `GRPKG001` update packages, what the packet logger really logs, and the 4.04r2 Windows client unpacked from its Thinstall installer (token `G3D17026`, the `Graal3DEngine.dll` plug-in, 98 server ids).
