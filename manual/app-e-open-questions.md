<!-- manual: kind=reference status=draft -->
# Appendix E. Open questions and disagreements

Each entry quotes the claims, names their sources, and says what would settle it. No entry is resolved by guess (→ §0.4). Entries are numbered in the order they were added; the number never changes.

> Status: draft. Seeded from Part I; the full seed from the 0.0.2 disagreements chapter and the corrections in CONSOLIDATED.md comes with work-plan PR 14.

### E#1 Compiler of the early Delphi builds

| Item | Content | Source |
| --- | --- | --- |
| Claim A | 1st Graal, 3rd Graal to 1.1.9 and 1.21 use the Delphi 2 class-metadata layout (self pointer 64, class name 32 bytes before the VMT) | [bin] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| Claim B | the same builds carry the RTL copyright "1983,97 Borland", a year late for Delphi 2 | [bin] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| Open | which compiler built them; a Delphi-2-level compiler shipped in 1997, such as C++Builder 1's, would fit both, but it has not been checked | [inf] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| Settles it | matching the RTL of these builds against C++Builder 1 and Delphi 2 runtime libraries | [inf] (client-internals/build-catalogue.md#patterns-worth-knowing) |

### E#2 Generation-5 step count of 5.12

| Item | Content | Source |
| --- | --- | --- |
| Claim A | 5.12's frame decoder steps the iterator `len / 4` times, rounded down, for zlib and bz2 frames (capped at 4), and rounds up for raw frames; it encodes the same way; a proxy that re-encodes with round-down stepping lets 5.12 play against GServer-v2 | [bin][wire] (protocol/v5v6-lab-play.md#512s-cipher-step-count) |
| Claim B | every later frame of ten 5.x and 6.x Windows captures, 5.12 among them, decodes with one step per group present, rounded up | [cap] (protocol/v5v6-windows-unpacked.md) |
| Open | whether the 5.12 captures held a compressed frame short enough (under 16 bytes, length not a multiple of 4) to tell the rules apart | [inf] (protocol/v5v6-lab-play.md#512s-cipher-step-count) |
| Settles it | decoding a 5.12 capture that contains such a frame under both rules | [inf] (protocol/v5v6-lab-play.md#512s-cipher-step-count) |

### E#3 Public `Login` server session (5.x, 6.x)

| Item | Content | Source |
| --- | --- | --- |
| Unobserved | the bytes a public 5.x or 6.x `Login` server sends, including the payload of S→C 190 | [doc] (protocol/login-session-known.md#still-unobserved) |
| Unobserved | the GUI script text for the server list, the account screens and the `ChatBar` control | [doc] (protocol/login-session-known.md#still-unobserved) |
| Unobserved | the file list inside that server's `basepackage.gupd`, and any later update package | [doc] (protocol/login-session-known.md#still-unobserved) |
| Unobserved | the backdrop level that server chooses | [doc] (protocol/login-session-known.md#still-unobserved) |
| Unobserved | the 6.11 connector script body, and with it the framing, cipher and login token a 6.11 client uses | [doc] (protocol/login-session-known.md#still-unobserved) |
| Settles it | a capture of a real `Login` session, which needs the owner's written permission because it touches a public server | [doc] (AGENTS.md#labs) |

### E#4 Whether 5.00r7 sends id 11

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the 5.00r7 send wrappers send 1, 2, 4–10, 12–19, …: no 11 (`PLI_THROWCARRIED`) | [bin] (protocol/v5x-clients.md#client--server-ids-500r7) |
| Claim B | the 5.00r7 profile lists 4–19, which includes 11; 5.12, 5.24r4 and 5.30r3 were seen sending 11 in captures | [bin][cap] (version-profiles/5.00-6.03.toml) |
| Open | which list is right for 5.00r7; both are floors, since sends through a variable are not captured | [bin] (protocol/v5x-clients.md#client--server-ids-500r7) |
| Settles it | a 5.00r7 capture of a throw, or a re-read of the send wrappers for id 11 | [inf] (protocol/v5x-clients.md#client--server-ids-500r7) |

### E#5 Meaning of id 162 from the client

| Item | Content | Source |
| --- | --- | --- |
| Claim A | gs2lib names 162 `PLI_RC_UNKNOWN162`: an empty message from the RC3 beta | [srv] (protocol/packet-ids.md#client--server-pli_) |
| Claim B | 4.20r8 sends 162 as the answer to S→C 108 | [bin] (protocol/v4x-clients.md#client--server-ids) |
| Claim C | 6.01r1 and 6.03r7 send 162 as a reply to a server request: `!` followed by a 2-byte value (two 7-bit groups, capped at `0x6FFF`) the server sent; probably the ping answer that 6.11 calls `onSendPingAnswer` | [bin][inf] (protocol/v6x-clients.md#client--server-ids-601-603) |
| Open | whether B and C are the same message, and how the RC3 beta's empty 162 relates to them | [inf] (protocol/v6x-clients.md#client--server-ids-601-603) |
| Settles it | a capture of a 4.x or 6.x client answering S→C 108 | [inf] (protocol/v4x-clients.md#client--server-ids) |

### E#6 Client-to-server constants of 1.21 and 1.32

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the ids visible as constants are 0 and 10 to 26 in 1.21, and 0 and 10 to 30 in 1.32 | [bin] (protocol/gserv-1999.md#message-ids) |
| Claim B | the per-build profile lists 1.21 as 0, 10–13, 15–26 (no 14) and 1.32 as 0, 10–21, 23–30 (no 22) | [bin] (client-internals/version-profiles/v121-v132.toml) |
| Open | whether A is a range summary of B or B missed a send site; both are floors, since some sends pass the id in a register | [bin] (client-internals/version-profiles/v121-v132.toml) |
| Settles it | a re-read of the 1.21 and 1.32 send sites for ids 14 and 22 | [inf] (protocol/gserv-1999.md#open-questions) |

### E#7 First builds that handle S→C 47 and 168

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the cross-version timeline adds 47 at 2.02 rev2 and 168 at 2.05 rev1 | [bin] (client-internals/cross-version-timeline.md#server--client-packets) |
| Claim B | the per-build handled-id table lists 47 already in 2.02 and 2.02 rev1, and 168 already in 2.05 rev0 | [bin] (version-profiles/plo-handled-ids-by-build.tsv) |
| Open | whether the timeline grouped the revisions or the table read the wrong revision | [inf] (version-profiles/plo-handled-ids-by-build.tsv) |
| Settles it | a re-read of the receive switch of 2.02 rev0 and 2.05 rev0 for cases 47 and 168 | [inf] (version-profiles/plo-handled-ids-by-build.tsv) |

### E#8 Prop parser ranges of 2.00

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the cross-version timeline has the player-prop parser gain 35 and 36 in 1.41, and the NPC-prop parser gain 36 to 40 only in 2.02 rev2 | [bin][inf] (client-internals/cross-version-timeline.md#prop-parsers) |
| Claim B | the 2.00 layout tables have the self and other-player streams accept 0–35 (no 36) and the NPC stream accept 0–36 | [bin] (version-profiles/plo-playerprops-layouts.tsv); [bin] (version-profiles/plo-npcprops-layouts.tsv) |
| Open | whether 2.00 parses player prop 36 and NPC prop 36 | [inf] (version-profiles/plo-npcprops-layouts.tsv) |
| Settles it | a re-read of the 2.00 prop switches at ids 36 | [inf] (version-profiles/plo-playerprops-layouts.tsv) |

### E#9 Uploads from game clients

| Item | Content | Source |
| --- | --- | --- |
| Claim A | game clients cannot upload; the RC file-browser ids are for RemoteControl only | [srv] (protocol/file-transfer.md#upload-rc-only) |
| Claim B | 6.01r1 and 6.03r7 send the file-browser and upload ids (93, 96–98, 155, 156) with an upload queue, and 3.153 and 5.00r7 send several of them | [bin] (protocol/v6x-clients.md#client--server-ids-601-603); [bin] (version-profiles/3.04-3.153.md#client--server-ids) |
| Open | whether a server accepts these from a game connection, and which game feature sends them | [inf] (protocol/v6x-clients.md#client--server-ids-601-603) |
| Settles it | a capture of a 6.x game client using the upload path against a server | [inf] (protocol/v6x-clients.md#client--server-ids-601-603) |

### E#100 Collision of the Bush stamp tiles

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the 2×2 Bush stamp writes ids 2, 3, 18 and 19, whose type bytes are 20 and 22, so the bush is wall | [file] (formats/gobjset01.md); [src] (formats/tiletypes.txt) |
| Claim B | ids 2, 3, 18 and 19 appear in the type-0 walk tables and are therefore walkable when the sheet is type 0 | [live] (formats/tile-walk.md#stamp-vocabulary) |
| Open | Claim A reads a 4096-byte type table kept by an outside client; Claim B reads the official client's type-0 allow lists; which one the official client applies to these ids on a type-0 sheet is not settled | [inf] (formats/tiletypes.txt) |
| Settles it | looking up ids 2, 3, 18 and 19 in arrays 0 and 1 of a shipped `arrays.dat` (→ §3.5.3), or walking into a placed bush in a lab client | [inf] (formats/tile-walk.md#type-0-allow-lists) |

### E#101 Size of the type-0 allow lists

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the type-0 allow lists are arrays 0 and 1 of `arrays.dat`, of 934 and 116 tile ids | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| Claim B | one exported type-0 mask counted 3195 non-blocking and 682 blocking tiles | [live] (formats/tile-walk.md#type-0-allow-lists) |
| Open | 934 + 116 ids do not add up to 3195 walkable tiles, and 3195 + 682 is not 4096; the notes do not say how the exported mask was made | [inf] (formats/tile-walk.md#type-0-allow-lists) |
| Settles it | rebuilding the mask from arrays 0 and 1 of a shipped `arrays.dat` and comparing it with the exported one | [inf] (formats/arrays-and-signatures.md#arraysdat) |

### E#102 Tile id to pixel position on pics1

| Item | Content | Source |
| --- | --- | --- |
| Claim A | `col = id % 128`, `row = id / 128`, pixel `(col * 16, row * 16)` | [file] (formats/tiletypes.txt) |
| Claim B | `col = (id % 16) + (id // 512) * 16`, `row = (id // 16) % 32`: eight side-by-side blocks of 512 ids, each 16 columns by 32 rows; Claim A is called wrong in a correction dated 2026-10-25 | [file] (client-internals/client-assets.md#tile-sheets) |
| Open | the manual follows Claim B, the later correction; Claim A's note has not been updated | [inf] (client-internals/client-assets.md#tile-sheets) |
| Settles it | correcting `formats/tiletypes.txt`, or rendering a known board with both rules against a client screenshot | [inf] (client-internals/client-assets.md#tile-sheets) |

### E#200 When a GS1 condition counts as true

| Item | Content | Source |
| --- | --- | --- |
| Claim A | in 2.05 a condition counts as true when it evaluates to 1.0 or more | [2.05] (npc-library/gs1-reference-205.md#execution-model-205) |
| Claim B | `if` evaluates its expression and jumps past its block when it is 0 | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| Open | how 2.05 treats a condition between 0 and 1, or a negative one; the claims agree only for 0 and for values of 1 or more | [inf] (npc-library/gs1-reference-205.md#execution-model-205; npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| Settles it | reading the 2.05 `if` executor's comparison, or running `if (0.5)` and `if (-1)` in a lab | [inf] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |

### E#201 Four GS1 argument signatures in 2.05

| Item | Content | Source |
| --- | --- | --- |
| Claim A | `toinventory` is `S`; `puthorse` is `MRR`; `showimg` is `RMRR`; `replaceani` is `MM` | [2.05] (npc-library/gs1-reference-205.md#commands-161-205) |
| Claim B | `toinventory` is `M`; `puthorse` is `F,R,R`; `showimg` is `R,F,R,R`; `replaceani` is `S,S` | [2.05] (npc-library/gs1-command-reference-205.md#commands) |
| Open | which letters the 2.05 table holds for these four commands; both notes say they read the same table | [inf] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#commands) |
| Settles it | re-reading the signature strings of ops 632, 640, 657 and 749 in the 2.05 rev 2 table | [inf] (npc-library/gs1-reference-205.md#commands-161-205) |

### E#202 Which message carries GS2 bytecode

| Item | Content | Source |
| --- | --- | --- |
| Claim A | NPC bytecode is `PLO_NPCBYTECODE`, id 131, sent to clients at or above `CLVER_4_0211` and wrapped in `PLO_RAWDATA` | [srv] (protocol/packet-ids.md; protocol/graphics-movement-bytecode.md#on-wire) |
| Claim B | for v4 and later clients the script prop is replaced by `NPCPROP_CLASS` plus id 197 (`PLO_UNKNOWN197`, "GS2 bytecode"); the weapon-list note also lists 197 as the bytecode that replaces the script for GS2 | [srv] (protocol/packet-layouts.md; client-internals/feature-specs/02-weapons-combat.md#weapon-lists-server-to-client-srv205) |
| Claim C | id 197 is `PLO_LOADSCRIPT`, a list `type,name,saveToDisk,desKey,crc32` | [srv] (protocol/packet-ids.md) |
| Open | whether 197 carries bytecode, a script-load descriptor, or both in different server versions, and how it relates to 131 | [inf] (protocol/packet-ids.md; protocol/packet-layouts.md) |
| Settles it | a capture of a 4.x or 5.x client receiving an NPC with a GS2 script from a lab server | [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |

### E#203 The 2.05 `#` message-code set

| Item | Content | Source |
| --- | --- | --- |
| Known | codes such as `#s(var)`, `#v(expr)`, `#c`, `#p(n)` and the `setcharprop` property codes are in use | [doc] (npc-library/gs1-reference-205.md#operators-and-syntax-doc); [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| Open | the full set of `#` codes 2.05 expands in string arguments | [doc] (npc-library/gs1-reference-205.md#operators-and-syntax-doc) |
| Settles it | reading the 2.05 message-code expander | [inf] (npc-library/gs1-reference-205.md#operators-and-syntax-doc) |

### E#204 Member names of the GS1 object arrays

| Item | Content | Source |
| --- | --- | --- |
| Known | each of `compus[i]`, `bombs[i]`, `arrows[i]`, `items[i]`, `explos[i]`, `horses[i]` and `signs[i]` has as many member ids in 2.05 as the 2.22 documentation has names | [2.05][doc] (npc-library/gs1-reference-205.md#functions-and-variables-205) |
| Open | which name maps to which id; the manual gives the documentation's names in its order, which is an inference | [inf] (npc-library/gs1-reference-205.md#functions-and-variables-205) |
| Settles it | tracing the 2.05 member parser | [inf] (npc-library/gs1-reference-205.md#functions-and-variables-205) |

### E#205 Index of the hare baddy

| Item | Content | Source |
| --- | --- | --- |
| Known | 2.05 ships `baddyhare.gif`, so a hare baddy type exists; the baddy name table has 10 names, 0–9 | [file][2.05] (npc-library/gs1-reference-205.md#constants-doc; npc-library/gs1-command-reference-205.md#name-tables) |
| Open | the hare's type index | [doc] (npc-library/gs1-reference-205.md#constants-doc) |
| Settles it | reading the 2.05 baddy image selection by type | [inf] (npc-library/gs1-reference-205.md#constants-doc) |

### E#206 `move` option bits in 2.05

| Item | Content | Source |
| --- | --- | --- |
| Known | the documentation gives cachetype 0–2, +4 block check, +8 event when done, +16 apply direction | [doc] (npc-library/gs1-reference-205.md#constants-doc) |
| Open | how 2.05 handles each bit; the 2.05 reading did not decode them | [inf] (npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) |
| Settles it | reading the 2.05 `move` executor | [inf] (npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) |

### E#207 GS2 language and bytecode format

| Item | Content | Source |
| --- | --- | --- |
| Known | 4.x and later clients run GS2 and receive it compiled; 3.153 already handles the NPC bytecode ids | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| Open | GS2 syntax, standard library and event model; the bytecode format; how the client stores received bytecode; whether later clients use another format | [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |
| Settles it | a lab note decoding a captured bytecode message from a 4.x client session, and a note on the GS2 documentation in the archived websites | [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |

### E#208 What the OpenGS1 opcode set describes

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the graphics-and-bytecode note calls the OpenGS1 VM "GS1 bytecode" and lists the full GS1 opcode set and constant-table layout as known | [src] (protocol/graphics-movement-bytecode.md#scripting--gs1-bytecode) |
| Claim B | 2.05 does not compile GS1 to bytecode; OpenGS1's opcode set is an independent reimplementation that 2.05 does not share | [2.05] (npc-library/gs1-reference-205.md#execution-model-205; npc-library/gs1-commands.md#update-2026-10-21) |
| Open | whether OpenGS1's format matches any official client's bytecode (3.153 or 4.x), or only OpenGS1 itself | [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |
| Settles it | comparing a captured official bytecode message (→ App. E#207) with the OpenGS1 layout | [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |

### E#300 Frame driver of 4th Graal alpha, 5th Graal and 5th Graal alpha

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the static survey records no form timer for 4th Graal alpha, 5th Graal and 5th Graal alpha (idle loop), while 4th Graal and 6th Graal on either side have the 50 ms form timer | [bin] (version-profiles/matrix/builds-static-survey.tsv) |
| Claim B | eras A to D all drive the tick from a DelphiX timer with interval 50 on the main form | [bin] (version-profiles/matrix/README.md#acts-timing-movement-and-rules) |
| Open | whether these three builds run from the idle handler, or keep a timer the survey did not find; the tick length is 50 ms either way only if the idle gate is 50 ms there too | [inf] (version-profiles/matrix/builds-static-survey.tsv) |
| Settles it | reading the main form and the frame routine of the three builds | [inf] (version-profiles/matrix/README.md#what-is-still-unknown) |

### E#301 Frame loop of the 3.x and 4.x clients

| Item | Content | Source |
| --- | --- | --- |
| Unobserved | the 3.x and 4.x Torque-era clients' tick length and loop driver; the 5.x and 6.x clients are timed only from their 50 ms position messages | [wire] (protocol/v5v6-lab-play.md); [doc] (version-profiles/matrix/README.md#acts-timing-movement-and-rules) |
| Settles it | a timed walk of a 3.x and a 4.x client on the lab server | [inf] (version-profiles/matrix/README.md#what-is-still-unknown) |

### E#302 Walking speed factors other than 1.0, 1.2 and the hidden 0.2

| Item | Content | Source |
| --- | --- | --- |
| Known | the walking code multiplies the half-tile step by a speed factor: 1.0 on foot, 1.2 in a high speed state; hiding gives 0.1 tile per tick | [2.05] (client-internals/decomp-findings-2026-10-25-l/01-walking-body-box.md#step); [live] (client-internals/player-mannerisms-live.md#lifting-carrying-hiding-and-throwing-live) |
| Open | factors 0.4 and 0.8 also exist (0.8 depends on a carried object); which states use them is not traced; carrying measured live does not slow the walk | [bin] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |
| Settles it | a lab walk in each candidate state (riding, shield, carrying each object kind) on 2.05 | [inf] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |

### E#303 Two unidentified lists in the blocked-point test

| Item | Content | Source |
| --- | --- | --- |
| Open | the blocked-point test reads a list of objects with two flags and a player-sized body box (only with a client option on), and a list of 1.5 × 2 boxes with an enabled flag; neither is identified (signs, baddies, dropped objects and other players are candidates) | [bin] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |
| Settles it | tracing what fills each list, or a lab test of walking into each kind of level object | [inf] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |

### E#304 Stopping positions and the wire rounding of nudged positions

| Item | Content | Source |
| --- | --- | --- |
| Known | the flush snap and the 0.1 nudges are read from the 2.05, 2.17.1, 2.22 and 2.31 walking routines | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#on-a-refused-step) |
| Open | the stopping positions are not confirmed on a live client; how the client rounds a position that is not on a half-tile when it sends it is not captured | [bin] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |
| Settles it | a lab walk towards a rock from both half-tile alignments on 2.22, with the props messages captured | [inf] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |

### E#305 The 2.22 push frame field

| Item | Content | Source |
| --- | --- | --- |
| Claim A | 2.22 plays `push` as 5 frames × 4 ticks, looping, as 2.05 does | [live][2.22] (client-internals/player-mannerisms-live.md#cross-version-table) |
| Claim B | a memory trace of 2.22 against a public server showed a push frame field cycling 0 to 3 every tick from the moment the blocked count passed 18 | [live] (live-runs/2gta-222-2026-10-30/README.md) |
| Open | whether the traced field is the gani frame or another per-tick counter; the second run used the server's own push gani | [inf] (live-runs/2gta-222-2026-10-30/README.md) |
| Settles it | reading the gani frame field of 2.22 offline with the stock `push.gani` | [inf] (client-internals/player-mannerisms-live.md#open) |

### E#306 The flag that picks `lift2.wav` for a pull

| Item | Content | Source |
| --- | --- | --- |
| Open | a successful pull plays `lift.wav`, or `lift2.wav` by a player flag that was not traced | [2.05] (client-internals/ledges-push-pull.md#grabbing-and-pulling) |
| Settles it | tracing the flag in 2.05's pull routine | [inf] (client-internals/ledges-push-pull.md#open) |

### E#307 Probe, nudge and step tables of 1st Graal and 1.39

| Item | Content | Source |
| --- | --- | --- |
| Known | both builds test six probes per facing step and use the 18 / 38 blocked-step counter; 1st Graal has a nudge table | [bin] (version-profiles/matrix/rules-1st-graal.md#wall-and-walk-test-bin); [1.39] (version-profiles/matrix/rules-139.md#wall--walk-test-bin-lab) |
| Open | the numeric probe offsets, nudge offsets and step table of both builds; whether they equal 2.05's | [bin] (version-profiles/matrix/rules-139.md#still-open) |
| Settles it | reading the tables from both exports | [inf] (version-profiles/matrix/rules-1st-graal.md) |

### E#308 Link probe offsets and the neighbour-table flag

| Item | Content | Source |
| --- | --- | --- |
| Open | the per-facing probe offsets for link following; the flag that skips the 3 × 3 neighbour table; which big map 2.05 uses offline and whether 2.22 does the same with `PLO_BIGMAP` (171); how walking behaves past the edge before the link fires when the neighbour is loaded | [2.05] (client-internals/decomp-findings-2026-10-28/03-edge-links.md#open) |
| Settles it | reading the probe table and the flag in 2.05, and a lab crossing on 2.22 with a big map | [inf] (client-internals/decomp-findings-2026-10-28/03-edge-links.md#open) |
### E#400 Two projects called Ash

| Item | Content | Source |
| --- | --- | --- |
| Claim A | Ash is a Python rewrite of the gs2emu protocol, with its own world and default port 14812; it is not the Reborn 2.4 binary | [src] (server-notes/01-lineage.md#what-is-binary--world-only); [src] (server-notes/ash-overview.md) |
| Claim B | Ash is the blueprint pack of the 2006 39ster 2.1 GServer, which describes that server as written, not a rewrite; default port 14822 | [src] (ash/INDEX.md); [src] (ash/ARCHIVAL-NOTE.md) |
| Open | whether the two are one project at two stages or two projects that share a name; the manual keeps them apart (→ §5.2, → §5.3.1) | [inf] (ash/ARCHIVAL-NOTE.md) |
| Settles it | the Drive archives of both, compared by date and content | [doc] (ash/ARCHIVAL-NOTE.md#full-archive) |

### E#401 Listserver reply ids 1 and 2

| Item | Content | Source |
| --- | --- | --- |
| Claim A | id 1 is NULL (empty) and id 2 is STATUS text with `\r` as a line break; 2.17, 2.22 and the public service send status text as id 2 | [srv] (protocol/listserver.md#listserver--client); [cap] (protocol/public-listserver-2026-10-25.md#frame-and-field-layout-derived) |
| Claim B | RC 1.41 (2002) reads id 1 as one more server entry and id 2 as the end of the list, then disconnects | [bin] (tools/npc-control.md#listserver-login-new-in-141-bin) |
| Open | whether the 2002 listserver used 1 and 2 differently from the later Reborn listserver, or the RC reads them its own way | [inf] (tools/npc-control.md#listserver-login-new-in-141-bin) |
| Settles it | a 2002-era listserver binary or capture, or a re-read of the 2.05 handler for id 1 | [inf] (protocol/listserver.md#205-specifics-205) |

### E#402 The 2000-era listserver reply

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the real 2.00-era listserver reply is observed: one plain zlib frame, id 0 only, 4 rows, no status, site or upgrade lines (the public service's 14923 reply to a classic login) | [cap] (protocol/public-listserver-2026-10-25.md#what-the-runs-settle) |
| Claim B | what a real 2.00-era listserver sends is still unobserved; the two-frame list that 2.00 accepted in the lab came from a lab forwarder | [lab] (protocol/listserver.md#205-specifics-205) |
| Open | whether today's 14923 legacy reply is the same as the service of 2000 to 2002 | [inf] (protocol/listserver-login-type-matrix-2026-10-25.md#result) |
| Settles it | a capture of a real 2.00 or 2.05 against the 14923 service, or a 2000-era listserver binary | [inf] (protocol/login-frames-by-version-2026-10-25.md#captures-that-would-settle-it-all-read-only-list-requests) |

### E#403 Classic logins on port 14922

| Item | Content | Source |
| --- | --- | --- |
| Claim A | a real 2.17.1 sends a classic login (shape B) to port 14922, the port in its signed `arrays2.dat` | [cap] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes) |
| Claim B | the public 14922 accepts a classic login and never answers it; the 2001-era tools put pre-2.2 clients on 14923 | [cap] (protocol/listserver-login-type-matrix-2026-10-25.md#result); [src] (tools/server-tools-2001.md#gs2emu-serverlist-thedgtl-snapshot-de66a3f) |
| Open | whether the 2001-era service answered classic logins on 14922, whether 2.17.1 was built for another listserver, and whether the zlib header (`78 DA` against `78 9C`) matters for a classic frame | [inf] (server-notes/lab-servers-2026-10-30.md#real-clients-against-it-today-lab); [inf] (protocol/login-frames-by-version-2026-10-25.md#does-the-evidence-support-classic-logins-look-fake) |
| Settles it | a list-only capture of a pristine 2.17.1 against the public service; this touches a public server and needs the owner's written permission | [doc] (AGENTS.md#labs) |

### E#404 A public server refusing 2.05 inside its own range

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the server's printed range runs from 1.41r1 to iPhone Belote 1.5, which in the current version table covers every 2.x to 6.x entry, 2.05 included | [src][inf] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x) |
| Claim B | the same server refused 2.05 (`GNW03081`) | [cap] (server-notes/public-allowed-versions.md#the-refusals-on-record) |
| Open | which version table the server runs; an older table with no 2.05 entry would explain both | [inf] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x) |
| Settles it | one 5.00r7 or 6.03r7 login to that server, with the owner's written permission | [inf] (server-notes/public-allowed-versions.md#open) |

### E#405 RC token `GSERV025`

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the server knows the RC tokens `GSERV023` to `GSERV025` | [srv] (protocol/chat-pm-rc.md#admin-and-staff) |
| Claim B | the RC builds read send `GSERV007`, `GSERV011`, `GSERV014` and `GSERV019` to `GSERV024`; none sends `GSERV025` | [bin] (protocol/gserv-1999.md#login); [bin] (tools/remotecontrol-lineage.md#builds); [bin] (tools/remotecontrol.md#logins-bin) |
| Open | which RC build sends `GSERV025`, and with which login type | [inf] (tools/remotecontrol-lineage.md) |
| Settles it | a static read of the later RC builds in the Drive RC folder (rc2, the custom RemoteControl, the RC3 beta) | [inf] (protocol/npc-control.md#drive-material-inventory-only-not-in-git) |
