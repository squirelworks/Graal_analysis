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
