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

### E#600 Tile layer as GraalEditor writes it

| Item | Content | Source |
| --- | --- | --- |
| Claim A | GraalEditor 2.3.1.1 writes `BOARD 0` as 64 lines of 64 decimal tile indices, which the client GLEVNW01 loader does not accept until rewritten as base64 runs | [GE] (tools/graaleditor.md#document-model); [GE] (formats/glevnw01.txt) |
| Claim B | the 2.05 and 2.22 built-in editors, from which GraalEditor is derived, write base64 `BOARD` rows | [2.22] (tools/level-editor/version-deltas.md#3-formats-per-build) |
| Open | which form a file saved by GraalEditor itself holds; the claim was never checked against such a file | [inf] (tools/level-editor/version-deltas.md#3-formats-per-build) |
| Settles it | saving a level from GraalEditor 2.3.1.1 and reading its `BOARD` rows | [inf] (tools/level-editor/version-deltas.md#3-formats-per-build) |

### E#601 Whether link arrival offsets are evaluated

| Item | Content | Source |
| --- | --- | --- |
| Claim A | link arrival fields may hold `playerx` or `playery` plus a signed offset such as `playery+10`; 21 arrivals in a 3113-level archive have that form, and the link dialog says math and variables may be used | [2.22] (tools/level-editor/222-reference.md#8-links) |
| Claim B | the editors store the arrival text verbatim and do not parse it | [2.22] (tools/level-editor/formats-crossref.md#batch-f-decomp-findings-2026-10-25-f-pr-39) |
| Open | whether the client evaluates the offset when the link fires, or treats it as the bare variable | [inf] (tools/level-editor/222-reference.md#16-open) |
| Settles it | a lab run through a link with an offset arrival, or a trace of the warp code | [inf] (tools/level-editor/222-reference.md#16-open) |
