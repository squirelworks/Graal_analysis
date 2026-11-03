# Graal Analysis 0.0.1

Document PDFs of the notes. Chiaki tags `v0.0.1`.
Start with `ch-00-contents.pdf`.

The notes viewer is part of the source tree at `tools/navigator/`.
After `git pull` of the tagged source:
`python3 tools/navigator/navigator.py` on loopback port 8765 (no venv).

Built from commit `398aab7deec9fda9bc5b9c7ed411d2befb467ae1`.
Page counts below are `pdfinfo` measurements of the PDFs in this folder.
`tools/release/build_book.py` writes this list.

| Kind | # | PDF | Title | Pages | Sections |
| --- | ---: | --- | --- | ---: | ---: |
| Contents | 0 | `ch-00-contents.pdf` | Contents | 2 | 1 |
| Chapter | 1 | `ch-01-how-to-read.pdf` | How to read these notes | 14 | 4 |
| Chapter | 2 | `ch-02-formats.pdf` | Formats | 29 | 16 |
| Chapter | 3 | `ch-03-protocol-part-1.pdf` | Protocol | 59 | 24 |
| Chapter | 3 | `ch-03-protocol-part-2.pdf` | Protocol | 48 | 13 |
| Chapter | 4 | `ch-04-client-internals-and-version-profiles-part-1.pdf` | Client internals and version profiles | 80 | 27 |
| Chapter | 4 | `ch-04-client-internals-and-version-profiles-part-2.pdf` | Client internals and version profiles | 72 | 20 |
| Chapter | 4 | `ch-04-client-internals-and-version-profiles-part-3.pdf` | Client internals and version profiles | 74 | 37 |
| Chapter | 4 | `ch-04-client-internals-and-version-profiles-part-4.pdf` | Client internals and version profiles | 74 | 73 |
| Chapter | 5 | `ch-05-graal3d-and-torque.pdf` | Graal3D and Torque | 42 | 14 |
| Chapter | 6 | `ch-06-tools-labs-and-level-conversion.pdf` | Tools, labs, and level conversion | 68 | 33 |
| Chapter | 7 | `ch-07-npc-scripting-overview.pdf` | NPC scripting overview | 25 | 7 |
| Appendix | 1 | `ap-01-recovered-tools-and-trainers-part-1.pdf` | Recovered tools and trainers | 48 | 31 |
| Appendix | 1 | `ap-01-recovered-tools-and-trainers-part-2.pdf` | Recovered tools and trainers | 43 | 20 |
| Appendix | 2 | `ap-02-game-asset-inventories.pdf` | Game-asset inventories | 20 | 5 |
| Appendix | 3 | `ap-03-server-and-other-notes.pdf` | Server notes and other indexes | 40 | 21 |
| Appendix | 4 | `ap-04-npc-script-names-part-1.pdf` | NPC script names | 73 | 5 |
| Appendix | 4 | `ap-04-npc-script-names-part-2.pdf` | NPC script names | 57 | 11 |

18 PDFs, 868 pages. Each PDF is at most 100 pages.

## What each PDF contains

### Contents 0: `ch-00-contents.pdf`

Graal Analysis 0.0.1 — contents. 2 pages.

- `release/0.0.1/contents.md`

### Chapter 1: `ch-01-how-to-read.pdf`

How to read these notes. 14 pages.

- `AGENTS.md`
- `docs/NEXT.md`
- `README.md`
- `tools/release/how-to-read.md`

### Chapter 2: `ch-02-formats.pdf`

Formats. 29 pages.

- `formats/arrays-and-signatures.md`
- `formats/gmap.md`
- `formats/gobjset01.md`
- `formats/graalsav.md`
- `formats/grv1-decoder/README.md`
- `formats/gwebl001-cache.md`
- `formats/level-binary-client.md`
- `formats/level-binary.md`
- `formats/seihai-boards.md`
- `formats/seihai-systems.md`
- `formats/sign-text.md`
- `formats/tile-walk.md`
- `formats/glevnw01.txt`
- `formats/gani.txt`
- `formats/grmap001.txt`
- `formats/tiletypes.txt`

### Chapter 3: `ch-03-protocol-part-1.pdf`

Protocol, part 1 of 2. 59 pages.

- `protocol/chat-pm-rc.md`
- `protocol/client-versions.md`
- `protocol/codec-and-framing.md`
- `protocol/cross-version-anchors.md`
- `protocol/crosscheck-captures-vs-research.md`
- `protocol/file-transfer.md`
- `protocol/format-notes-from-salvage.md`
- `protocol/graphics-movement-bytecode.md`
- `protocol/gserv-1999.md`
- `protocol/lab-checks-2026-10-24.md`
- `protocol/listserver-login-type-matrix-2026-10-25.md`
- `protocol/listserver.md`
- `protocol/login-and-walk.md`
- `protocol/login-frames-by-version-2026-10-25.md`
- `protocol/login-recovery-start.md`
- `protocol/login-session-known.md`
- `protocol/medium-term-expansion.md`
- `protocol/medium-term-slice.md`
- `protocol/npc-control.md`
- `protocol/offline-expansion.md`
- `protocol/OPCODE-SUMMARY.md`
- `protocol/packet-id-diff.md`
- `protocol/packet-ids.md`
- `protocol/packet-layouts.md`

### Chapter 3: `ch-03-protocol-part-2.pdf`

Protocol, part 2 of 2. 48 pages.

- `protocol/pcap-2026-10-04.md`
- `protocol/player-props.md`
- `protocol/PROTOCOL-CHEATSHEET.md`
- `protocol/public-listserver-2026-10-25.md`
- `protocol/relay-1998.md`
- `protocol/session-opcodes-cleaned.md`
- `protocol/udp-p2p.md`
- `protocol/v3x-clients.md`
- `protocol/v4x-clients.md`
- `protocol/v5v6-lab-play.md`
- `protocol/v5v6-windows-unpacked.md`
- `protocol/v5x-clients.md`
- `protocol/v6x-clients.md`

### Chapter 4: `ch-04-client-internals-and-version-profiles-part-1.pdf`

Client internals and version profiles, part 1 of 4. 80 pages.

- `client-internals/prior-attempts.md`
- `client-internals/client-architecture-205.md`
- `client-internals/client-assets.md`
- `client-internals/build-catalogue.md`
- `client-internals/drive-clients-inventory.md`
- `client-internals/version-id-map.md`
- `client-internals/version-tokens.md`
- `client-internals/version/README.md`
- `client-internals/version/VERSION.md`
- `client-internals/version/docs/GraalEditor-README.md`
- `client-internals/version/docs/GraalEditor-architecture.md`
- `client-internals/version-profiles/README.md`
- `client-internals/version-profiles/list-ports.md`
- `version-profiles/matrix/README.md`
- `version-profiles/matrix/seihai-gaps.md`
- `version-profiles/version-coverage-2026-10-24.md`
- `client-internals/reference-reimplementations/README.md`
- `client-internals/reference-reimplementations/2dadventureclient.md`
- `client-internals/reference-reimplementations/levelscripteditor.md`
- `client-internals/zelda-online-1998.md`
- `client-internals/precursors-and-fan-builds.md`
- `client-internals/precursor-runs-2026-10-30.md`
- `client-internals/early-clients.md`
- `version-profiles/matrix/rules-1st-graal.md`
- `client-internals/gameboy-demo.md`
- `client-internals/relay-room-bridge.md`
- `client-internals/live-trace-early.md`

### Chapter 4: `ch-04-client-internals-and-version-profiles-part-2.pdf`

Client internals and version profiles, part 2 of 4. 72 pages.

- `client-internals/live-gserver13.md`
- `client-internals/versions-133-139.md`
- `version-profiles/matrix/rules-139.md`
- `client-internals/cross-version-timeline.md`
- `client-internals/newworld-betas.md`
- `client-internals/v2.00-connect-path.md`
- `client-internals/build-diff-204-205.md`
- `client-internals/feature-timeline.md`
- `client-internals/live-trace-205.md`
- `version-profiles/2.22-2.31.md`
- `client-internals/live-checks-editor-offline-sound.md`
- `client-internals/player-mannerisms-live.md`
- `version-profiles/matrix/builds-deltas.md`
- `version-profiles/matrix/live-runs-2026-10-30.md`
- `version-profiles/3.04-3.153.md`
- `version-profiles/lab-304-linux-2026-10-30.md`
- `client-internals/live-behaviour-404.md`
- `version-profiles/lab-mac-tiger-2026-10-31.md`
- `version-profiles/lab-v5-2026-10-30.md`
- `client-internals/feature-specs/README.md`

### Chapter 4: `ch-04-client-internals-and-version-profiles-part-3.pdf`

Client internals and version profiles, part 3 of 4. 74 pages.

- `client-internals/foot-test.md`
- `client-internals/ledges-push-pull.md`
- `client-internals/carry-hide-and-glove.md`
- `client-internals/water-and-ganis.md`
- `client-internals/feature-specs/11-emotes-ganis.md`
- `client-internals/feature-specs/06-gmap-overworld.md`
- `client-internals/feature-specs/02-weapons-combat.md`
- `client-internals/combat-200-204.md`
- `client-internals/damage-sources.md`
- `client-internals/status-bit-0x20.md`
- `client-internals/item-drops.md`
- `client-internals/board-respawn.md`
- `client-internals/feature-specs/04-death-respawn.md`
- `client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md`
- `client-internals/feature-specs/03-inventory.md`
- `client-internals/id24-205.md`
- `client-internals/rendering-observations.md`
- `client-internals/status-display.md`
- `client-internals/body-colours-and-attributes.md`
- `client-internals/chat-text.md`
- `client-internals/sign-panel.md`
- `client-internals/feature-specs/09-options.md`
- `client-internals/feature-specs/10-right-click-menu.md`
- `client-internals/feature-specs/12-motd-rules.md`
- `client-internals/feature-specs/13-ban-kick.md`
- `client-internals/feature-specs/14-friends-ignore.md`
- `client-internals/feature-specs/01-sound.md`
- `client-internals/sound-and-music.md`
- `client-internals/bare-level-names.md`
- `client-internals/feature-specs/05-save-load.md`
- `client-internals/config-and-input.md`
- `client-internals/graalconfig-reference.md`
- `client-internals/saved-passwords.md`
- `client-internals/des-and-hidden-strings.md`
- `client-internals/feature-specs/08-tampercheck.md`
- `client-internals/feature-specs/07-udp-peer.md`
- `client-internals/offline-play.md`

### Chapter 4: `ch-04-client-internals-and-version-profiles-part-4.pdf`

Client internals and version profiles, part 4 of 4. 74 pages.

- `client-internals/offline-training.md`
- `client-internals/offline-tutorial-205.md`
- `client-internals/level-editor-205.md`
- `client-internals/decomp-findings-2026-10-24/README.md`
- `client-internals/decomp-findings-2026-10-24/01-death-respawn.md`
- `client-internals/decomp-findings-2026-10-24/02-sprites-poses-emotes.md`
- `client-internals/decomp-findings-2026-10-24/03-player-list-popup.md`
- `client-internals/decomp-findings-2026-10-24/04-sword-hitbox.md`
- `client-internals/decomp-findings-2026-10-24/05-205-props-misc.md`
- `client-internals/decomp-findings-2026-10-24/06-first-graal.md`
- `client-internals/decomp-findings-2026-10-24/07-graal-139.md`
- `client-internals/decomp-findings-2026-10-24/08-contradictions.md`
- `client-internals/decomp-findings-2026-10-24-b/README.md`
- `client-internals/decomp-findings-2026-10-24-b/01-tamper-check-id39.md`
- `client-internals/decomp-findings-2026-10-24-b/02-server-to-client-layouts.md`
- `client-internals/decomp-findings-2026-10-24-b/03-periodic-ids-2.31.md`
- `client-internals/decomp-findings-2026-10-24-b/04-v2.00-client.md`
- `client-internals/decomp-findings-2026-10-24-b/05-open-items.md`
- `client-internals/decomp-findings-2026-10-24-b/06-crosscheck.md`
- `client-internals/decomp-findings-2026-10-24-b/07-lab-findings-46-186-200.md`
- `client-internals/decomp-findings-2026-10-24-b/08-lab-findings-levelchange-24-178.md`
- `client-internals/decomp-findings-2026-10-24-c/README.md`
- `client-internals/decomp-findings-2026-10-24-c/01-toolchain-and-coverage.md`
- `client-internals/decomp-findings-2026-10-24-c/02-login-token-and-version.md`
- `client-internals/decomp-findings-2026-10-24-c/03-framing-and-encryption.md`
- `client-internals/decomp-findings-2026-10-24-c/04-plo-server-to-client.md`
- `client-internals/decomp-findings-2026-10-24-c/05-pli-client-to-server.md`
- `client-internals/decomp-findings-2026-10-24-c/06-handler-changes-by-build.md`
- `client-internals/decomp-findings-2026-10-24-c/07-udp-channel.md`
- `client-internals/decomp-findings-2026-10-24-c/08-test-builds-newworld-newmain.md`
- `client-internals/decomp-findings-2026-10-24-c/09-features-classes-vocabulary.md`
- `client-internals/decomp-findings-2026-10-24-c/10-open-questions-and-corrections.md`
- `client-internals/decomp-findings-2026-10-24-d/README.md`
- `client-internals/decomp-findings-2026-10-24-d/01-sword-damage.md`
- `client-internals/decomp-findings-2026-10-24-d/02-respawn-entry-save.md`
- `client-internals/decomp-findings-2026-10-24-d/03-hit-gates-and-open-points.md`
- `client-internals/decomp-findings-2026-10-25-e/README.md`
- `client-internals/decomp-findings-2026-10-25-e/01-request-lists.md`
- `client-internals/decomp-findings-2026-10-25-e/02-save-rules.md`
- `client-internals/decomp-findings-2026-10-25-e/03-open-points.md`
- `client-internals/decomp-findings-2026-10-25-e/04-name-index-case-link.md`
- `client-internals/decomp-findings-2026-10-25-f/README.md`
- `client-internals/decomp-findings-2026-10-25-f/01-section-shapes.md`
- `client-internals/decomp-findings-2026-10-25-f/02-link-arrival-expressions.md`
- `client-internals/decomp-findings-2026-10-25-f/03-baddy-terminator.md`
- `client-internals/decomp-findings-2026-10-25-f/04-sign-and-chest-details.md`
- `client-internals/decomp-findings-2026-10-25-g/README.md`
- `client-internals/decomp-findings-2026-10-25-g/01-id24-image-list.md`
- `client-internals/decomp-findings-2026-10-25-g/02-id46-level-switch.md`
- `client-internals/decomp-findings-2026-10-25-g/03-id178-comma-text.md`
- `client-internals/decomp-findings-2026-10-25-g/04-open-points.md`
- `client-internals/decomp-findings-2026-10-25-j/README.md`
- `client-internals/decomp-findings-2026-10-25-j/01-record-shapes.md`
- `client-internals/decomp-findings-2026-10-25-j/02-links-and-arrivals.md`
- `client-internals/decomp-findings-2026-10-25-j/03-extensions-and-magic.md`
- `client-internals/decomp-findings-2026-10-25-j/04-loader-rules-compared.md`
- `client-internals/decomp-findings-2026-10-25-j/05-old-reader-failures.md`
- `client-internals/decomp-findings-2026-10-25-k/README.md`
- `client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md`
- `client-internals/decomp-findings-2026-10-25-k/02-save-folders-by-build.md`
- `client-internals/decomp-findings-2026-10-25-k/03-open-points.md`
- `client-internals/decomp-findings-2026-10-25-l/README.md`
- `client-internals/decomp-findings-2026-10-25-l/01-walking-body-box.md`
- `client-internals/decomp-findings-2026-10-25-l/02-arrays-dat.md`
- `client-internals/decomp-findings-2026-10-25-l/03-cut-lift-chest.md`
- `client-internals/decomp-findings-2026-10-25-l/04-public-server-run.md`
- `client-internals/decomp-findings-2026-10-25-m/README.md`
- `client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md`
- `client-internals/decomp-findings-2026-10-28/01-sword-while-carrying.md`
- `client-internals/decomp-findings-2026-10-28/02-item-list.md`
- `client-internals/decomp-findings-2026-10-28/03-edge-links.md`
- `client-internals/decomp-findings-2026-10-28-b/README.md`
- `client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md`

### Chapter 5: `ch-05-graal3d-and-torque.pdf`

Graal3D and Torque. 42 pages.

- `graal3d/camera.md`
- `graal3d/client-behaviour.md`
- `graal3d/collision.md`
- `graal3d/formats.md`
- `graal3d/lab-2026-10-30.md`
- `graal3d/protocol.md`
- `graal3d/README.md`
- `graal3d/reference-server/README.md`
- `graal3d/torque-engine-4x.md`
- `torque/engine-and-formats.md`
- `torque/network.md`
- `torque/README.md`
- `torque/scripting.md`
- `torque/wire-by-build.md`

### Chapter 6: `ch-06-tools-labs-and-level-conversion.pdf`

Tools, labs, and level conversion. 68 pages.

- `tools/build-diff/README.md`
- `tools/classic-tools/character-designer.md`
- `tools/classic-tools/graal-level-gen.md`
- `tools/classic-tools/gserverstat.md`
- `tools/classic-tools/README.md`
- `tools/classic-tools/serverlist3.md`
- `tools/classic-tools/text-convert.md`
- `tools/generators-222/README.md`
- `tools/generators.md`
- `tools/ghidra/README.md`
- `tools/gif2mng.md`
- `tools/graaleditor-vs-205.md`
- `tools/graaleditor.md`
- `tools/graalshop.md`
- `tools/lab-servers/README.md`
- `tools/lab-setup.md`
- `tools/level-convert/README.md`
- `tools/level-convert/SEIHAI-FORMAT.md`
- `tools/level-editor/222-reference.md`
- `tools/level-editor/formats-crossref.md`
- `tools/level-editor/README.md`
- `tools/level-editor/seihai-tracking.md`
- `tools/level-editor/version-deltas.md`
- `tools/level-tools-gaps/README.md`
- `tools/navigator/README.md`
- `tools/npc-control.md`
- `tools/npcserver-2001.md`
- `tools/README.md`
- `tools/remotecontrol-lineage.md`
- `tools/remotecontrol.md`
- `tools/respawn-lab/README.md`
- `tools/server-tools-2001.md`
- `live-runs/2gta-222-2026-10-30/README.md`

### Chapter 7: `ch-07-npc-scripting-overview.pdf`

NPC scripting overview. 25 pages.

- `npc-library/archival-scripting-notes.md`
- `npc-library/gs1-command-reference-205.md`
- `npc-library/gs1-commands.md`
- `npc-library/gs1-reference-205.md`
- `npc-library/README.md`
- `npc-library/tile-patterns.md`
- `server-notes/setcharprop-hash-n.md`

### Appendix 1: `ap-01-recovered-tools-and-trainers-part-1.pdf`

Recovered tools and trainers, part 1 of 2. 48 pages.

- `recovered-drive-tools/ghidra-analysis/Assimilator/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/BytecodeViewer/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/DClient_setup/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/GCD/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/GChar/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/Graal_Auto_Key/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/Graal_Digger/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/GraalLevelGenNW/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/gserver-linux/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/gserver-win/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/gserver13/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/gserver_pe_GServersource/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/gserverstat/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/gserverstat2/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/ListServer/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/Matriark_gserver/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/NPCControl/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/PNGView/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/README.md`
- `recovered-drive-tools/ghidra-analysis/RemoteControl-NW/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/RemoteControl3/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/RemoteControl_classic/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/remotecontrol_custom/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/scripteditor/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/serverlist3/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/TextConvert/SUMMARY.md`
- `recovered-drive-tools/ghidra-analysis/TilesEditor/SUMMARY.md`
- `recovered-drive-tools/INVENTORY.md`
- `recovered-drive-tools/SALVAGE_CANDIDATES.md`
- `recovered-drive-tools/SALVAGE_PLACEMENT.md`
- `recovered-drive-tools/SEIHAI_SERVERTOOLS_MAP.md`

### Appendix 1: `ap-01-recovered-tools-and-trainers-part-2.pdf`

Recovered tools and trainers, part 2 of 2. 43 pages.

- `recovered-hacks/behaviour-models.md`
- `recovered-hacks/defense-checklist.md`
- `recovered-hacks/DEFENSE_PROPOSALS.md`
- `recovered-hacks/ghidra-analysis/AFK_Bot/SUMMARY.md`
- `recovered-hacks/ghidra-analysis/Graal_Digger/SUMMARY.md`
- `recovered-hacks/ghidra-analysis/Graal_Prayer/SUMMARY.md`
- `recovered-hacks/ghidra-analysis/Graal_Prayer_data/SUMMARY.md`
- `recovered-hacks/ghidra-analysis/GTS/SUMMARY.md`
- `recovered-hacks/INVENTORY.md`
- `recovered-hacks/remaining-2026-11-01.md`
- `recovered-hacks/static-2026-11-01/autod.md`
- `recovered-hacks/static-2026-11-01/autoidle.md`
- `recovered-hacks/static-2026-11-01/autos.md`
- `recovered-hacks/static-2026-11-01/capslock.md`
- `recovered-hacks/static-2026-11-01/listserver.md`
- `recovered-hacks/static-2026-11-01/random-walker.md`
- `recovered-hacks/static-2026-11-01/README.md`
- `recovered-hacks/static-2026-11-01/waterget.md`
- `recovered-hacks/THREAT_TAXONOMY.md`
- `recovered-hacks/TRAINER_RE_NOTES.md`

### Appendix 2: `ap-02-game-asset-inventories.pdf`

Game-asset inventories. 20 pages.

- `archive/ember-avelan-experimental.md`
- `archive/game-assets-2026-11-01.md`
- `archive/game-assets-graphics-sound-2026-11-01.md`
- `archive/game-assets-websites-2026-11-01.md`
- `archive/game-assets-worlds-2026-11-01.md`

### Appendix 3: `ap-03-server-and-other-notes.pdf`

Server notes and other indexes. 40 pages.

- `ARCHIVAL.md`
- `archival/client-assets-measured.md`
- `archival/foot-test-sdl.md`
- `archival/README.md`
- `archival/tools-early.md`
- `archival/version-tokens-early.md`
- `ARCHIVE.md`
- `ash/ALGORITHMS.md`
- `ash/ARCHITECTURE.md`
- `ash/ARCHIVAL-NOTE.md`
- `ash/BLUEPRINT.md`
- `ash/INDEX.md`
- `ash/OPCODE-MAP.md`
- `CONSOLIDATED.md`
- `server-notes/01-lineage.md`
- `server-notes/03-protocol.md`
- `server-notes/04-algorithms.md`
- `server-notes/ash-overview.md`
- `server-notes/lab-servers-2026-10-30.md`
- `server-notes/public-allowed-versions.md`
- `server-notes/README.md`

### Appendix 4: `ap-04-npc-script-names-part-1.pdf`

NPC script names, part 1 of 2. 73 pages.

- `npc-library/combat/baddies`
- `npc-library/combat/hazards`
- `npc-library/combat/targets`
- `npc-library/combat/weapons`
- `npc-library/dialogue/speech`

### Appendix 4: `ap-04-npc-script-names-part-2.pdf`

NPC script names, part 2 of 2. 57 pages.

- `npc-library/interaction/flags`
- `npc-library/interaction/triggers`
- `npc-library/interaction/visibility`
- `npc-library/misc/other`
- `npc-library/object/blocks`
- `npc-library/object/chests`
- `npc-library/object/doors`
- `npc-library/object/signs`
- `npc-library/spawn/timers`
- `npc-library/transport/level-warps`
- `npc-library/transport/local-warps`
