<!-- manual: kind=reference status=draft -->
# Appendix E. Open questions and disagreements

Each entry quotes the claims, names their sources, and says what would settle it. No entry is resolved by guess (→ §0.4). Entries are numbered in the order they were added; the number never changes.

> Status: draft. Seeded from each part as it was written, and from the 0.0.2 disagreements chapter and CONSOLIDATED.md (E#600–608). Id ranges: E#1–99 front matter, Part I and Part II; E#100s Part III; E#200s Part VIII; E#300s Part IV; E#400s Parts V–VII; E#500s Parts IX–X; E#600s Part XI and the seed.

### E#1 Compiler of the early Delphi builds

Two clues about the compiler of the earliest builds point to different Delphi versions. The question stays open until their runtime library is matched against candidates [bin] (client-internals/build-catalogue.md#patterns-worth-knowing).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | 1st Graal, 3rd Graal to 1.1.9 and 1.21 use the Delphi 2 class-metadata layout (self pointer 64, class name 32 bytes before the VMT) | [bin] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| Claim B | the same builds carry the RTL copyright "1983,97 Borland", a year late for Delphi 2 | [bin] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| Open | which compiler built them; a Delphi-2-level compiler shipped in 1997, such as C++Builder 1's, would fit both, but it has not been checked | [inf] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| Settles it | matching the RTL of these builds against C++Builder 1 and Delphi 2 runtime libraries | [inf] (client-internals/build-catalogue.md#patterns-worth-knowing) |

### E#2 Generation-5 step count of 5.12

Two reads disagree on how many iterator steps 5.12 takes for a short compressed frame. Only a capture that holds such a frame can tell them apart [bin][wire] (protocol/v5v6-lab-play.md#512s-cipher-step-count).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | 5.12's frame decoder steps the iterator `len / 4` times, rounded down, for zlib and bz2 frames (capped at 4), and rounds up for raw frames; it encodes the same way; a proxy that re-encodes with round-down stepping lets 5.12 play against GServer-v2 | [bin][wire] (protocol/v5v6-lab-play.md#512s-cipher-step-count) |
| Claim B | every later frame of ten 5.x and 6.x Windows captures, 5.12 among them, decodes with one step per group present, rounded up | [cap] (protocol/v5v6-windows-unpacked.md) |
| Open | whether the 5.12 captures held a compressed frame short enough (under 16 bytes, length not a multiple of 4) to tell the rules apart | [inf] (protocol/v5v6-lab-play.md#512s-cipher-step-count) |
| Settles it | decoding a 5.12 capture that contains such a frame under both rules | [inf] (protocol/v5v6-lab-play.md#512s-cipher-step-count) |

Separately, four exact Mac PowerPC receivers use whole-group compressed advancement and partial-group raw advancement. This static Mac result does not resolve the Windows capture disagreement or prove outgoing symmetry. [bin] (protocol/macos-ppc-receive-framing.md)

### E#3 Public `Login` server session (5.x, 6.x)

Nobody has recorded what a public 5.x or 6.x `Login` server sends. Each row is one thing still unobserved; settling them needs the owner's permission [doc] (protocol/login-session-known.md#still-unobserved).

| Item | Content | Source |
| --- | --- | --- |
| Unobserved | the bytes a public 5.x or 6.x `Login` server sends, including the payload of S→C 190 | [doc] (protocol/login-session-known.md#still-unobserved) |
| Unobserved | the GUI script text for the server list, the account screens and the `ChatBar` control | [doc] (protocol/login-session-known.md#still-unobserved) |
| Unobserved | the file list inside that server's `basepackage.gupd`, and any later update package | [doc] (protocol/login-session-known.md#still-unobserved) |
| Unobserved | the backdrop level that server chooses | [doc] (protocol/login-session-known.md#still-unobserved) |
| Unobserved | the 6.11 connector script body, and with it the framing, cipher and login token a 6.11 client uses | [doc] (protocol/login-session-known.md#still-unobserved) |
| Settles it | a capture of a real `Login` session, which needs the owner's written permission because it touches a public server | [doc] (AGENTS.md#labs) |

### E#4 Whether 5.00r7 sends id 11

Two lists of the ids 5.00r7 sends disagree on id 11. A later static read sides with the list that includes it, and a capture is still missing [bin] (protocol/v5x-clients.md#client--server-ids-500r7).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the 5.00r7 send wrappers send 1, 2, 4–10, 12–19, …: no 11 (`PLI_THROWCARRIED`) | [bin] (protocol/v5x-clients.md#client--server-ids-500r7) |
| Claim B | the 5.00r7 profile lists 4–19, which includes 11; 5.12, 5.24r4 and 5.30r3 were seen sending 11 in captures | [bin][cap] (version-profiles/5.00-6.03.toml) |
| Open | which list is right for 5.00r7; both are floors, since sends through a variable are not captured | [bin] (protocol/v5x-clients.md#client--server-ids-500r7) |
| Settles it | a 5.00r7 capture of a throw, or a re-read of the send wrappers for id 11 | [inf] (protocol/v5x-clients.md#client--server-ids-500r7) |
| Static resolution | the 5.00r7 backup engine's carried-object throw path sends id 11 with an empty body; the earlier wrapper list missed it. Claim B holds for that engine; a capture is still missing | [bin] (client-internals/windows-404r2-500r7-static-2026-11-09.md#500r7-sends-id-11-when-throwing) |

### E#5 Meaning of id 162 from the client (settled)

Three readings of client id 162 turned out to be one message, a ping answer. The entry is kept to show how it was settled [srv] (protocol/packet-ids.md#client--server-pli_).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the 2026-10 gs2lib named 162 `PLI_RC_UNKNOWN162` (upstream now `PLI_PONG`): an empty message from the RC3 beta | [srv] (protocol/packet-ids.md#client--server-pli_) |
| Claim B | 4.20r8 sends 162 as the answer to S→C 108 | [bin] (protocol/v4x-clients.md#client--server-ids) |
| Claim C | 6.01r1 and 6.03r7 send 162 as a reply to a server request: `!` followed by a 2-byte value (two 7-bit groups, capped at `0x6FFF`) the server sent; probably the ping answer that 6.11 calls `onSendPingAnswer` | [bin][inf] (protocol/v6x-clients.md#client--server-ids-601-603) |
| Open | ~~whether B and C are the same message, and how the RC3 beta's empty 162 relates to them~~ settled below | [inf] (protocol/v6x-clients.md#client--server-ids-601-603) |
| Settles it | a capture of a 4.x or 6.x client answering S→C 108 | [inf] (protocol/v4x-clients.md#client--server-ids) |
| Settled | one message, a ping: 4.20r6, 4.20r8, 6.01r1 and 6.03r7 send 162 only from their 108 handler, with the same code in 4.20r8 and 6.03r7; the 2010 RC and RC3 send it empty every 60 s and have no 108 handler; a capture of the game-client answer is still missing | [bin] (protocol/unknown-ids-2026-11-06.md) |

### E#6 Client-to-server constants of 1.21 and 1.32

Two reads of the 1.21 and 1.32 send sites disagree on ids 14 and 22 [bin] (protocol/gserv-1999.md#message-ids).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the ids visible as constants are 0 and 10 to 26 in 1.21, and 0 and 10 to 30 in 1.32 | [bin] (protocol/gserv-1999.md#message-ids) |
| Claim B | the per-build profile lists 1.21 as 0, 10–13, 15–26 (no 14) and 1.32 as 0, 10–21, 23–30 (no 22) | [bin] (client-internals/version-profiles/v121-v132.toml) |
| Open | whether A is a range summary of B or B missed a send site; both are floors, since some sends pass the id in a register | [bin] (client-internals/version-profiles/v121-v132.toml) |
| Settles it | a re-read of the 1.21 and 1.32 send sites for ids 14 and 22 | [inf] (protocol/gserv-1999.md#open-questions) |

### E#7 Receive-branch revision discrepancy (settled for the checked inputs)

Two tables placed ids 47 and 168 in different revisions. A static check settled it for the revisions that were read; the scope row says how far that goes [bin] (client-internals/cross-version-timeline.md#server--client-packets).

| Item | Content | Source |
| --- | --- | --- |
| Historical claim A | the timeline formerly placed 47 at 2.02 rev2 and 168 at 2.05 rev1; those revision labels are corrected | [bin] (client-internals/cross-version-timeline.md#server--client-packets) |
| Historical claim B | the per-build table already included 47 in 2.02 revisions 0 and 1 and 168 in 2.05 revision 0 | [bin] (version-profiles/plo-handled-ids-by-build.tsv); [bin] (client-internals/decomp-findings-2026-10-24-c/04-plo-server-to-client.md#set-growth) |
| Resolution | the exact-input static check corroborates Claim B for Windows x86 2.02 revisions 0–2 and 2.05 revisions 0–2; counts and ID sets are in → §2.5.2 | [bin] (client-internals/receive-dispatch-revision-boundaries-2026-11-09.md#distinct-receive-routes) |
| Scope limit | this settles route presence in those inputs; successful runtime handling, payload semantics and first occurrence across all historical branches are not established | [bin] (client-internals/receive-dispatch-revision-boundaries-2026-11-09.md#validation-and-limits) |

### E#8 Prop parser ranges of 2.00

Two sources disagreed on whether 2.00 parses player prop 36 and NPC prop 36. A re-read of the 2.0x jump tables settles it: Claim A holds [bin] (protocol/player-props.md#parsers-in-200-to-205-re-read-2026-11-12-bin).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the cross-version timeline has the player-prop parser gain 35 and 36 in 1.41, and the NPC-prop parser gain 36 to 40 only in 2.02 rev2 | [bin][inf] (client-internals/cross-version-timeline.md#prop-parsers) |
| Claim B | the 2.00 layout tables have the self and other-player streams accept 0–35 (no 36) and the NPC stream accept 0–36 | [bin] (version-profiles/plo-playerprops-layouts.tsv); [bin] (version-profiles/plo-npcprops-layouts.tsv) |
| Resolution | the 2.00 and 2.01 self switch covers 0–36 and the NPC switch 0–35; NPC 36–40 arrive in 2.02 rev2. Claim A is right for both | [bin] (protocol/player-props.md#parsers-in-200-to-205-re-read-2026-11-12-bin) |
| Other players | the 2.00 and 2.01 other-player switch also accepts 36 (and 50, 51), with the same sparse stops as 2.05 | [bin] (protocol/player-props.md#parsers-in-200-to-205-re-read-2026-11-12-bin) |

### E#9 Uploads from game clients

One source says game clients never upload, while the late clients send the upload ids. Which feature sends them, and whether a server accepts them, is open [srv] (protocol/file-transfer.md#upload-rc-only).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | game clients cannot upload; the RC file-browser ids are for RemoteControl only | [srv] (protocol/file-transfer.md#upload-rc-only) |
| Claim B | 6.01r1 and 6.03r7 send the file-browser and upload ids (93, 96–98, 155, 156) with an upload queue, and 3.153 and 5.00r7 send several of them | [bin] (protocol/v6x-clients.md#client--server-ids-601-603); [bin] (version-profiles/3.04-3.153.md#client--server-ids) |
| Open | whether a server accepts these from a game connection, and which game feature sends them | [inf] (protocol/v6x-clients.md#client--server-ids-601-603) |
| Settles it | a capture of a 6.x game client using the upload path against a server | [inf] (protocol/v6x-clients.md#client--server-ids-601-603) |

### E#10 When the `maps` download folder arrived

No surviving build shows when downloads began going to a `maps` folder [bin] (client-internals/decomp-findings-2026-10-25-k/03-open-points.md).

| Item | Content | Source |
| --- | --- | --- |
| Open | the 2.1 test builds save downloads with no `maps` rule and 2.17.1 has one; no client between them has been found, so the build that added it is unknown | [bin] (client-internals/decomp-findings-2026-10-25-k/03-open-points.md) |
| Settles it | the save routine of any client from 2.1 to 2.16, if one turns up | [inf] (client-internals/decomp-findings-2026-10-25-e/03-open-points.md) |

### E#11 Client-to-server ids the NewWorld betas lack

Two reads of the NewWorld betas disagree on whether they send ids 8 and 20 [bin] (client-internals/version-profiles/141-217.toml).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the betas send the 2.1 test set without 7, 8, 11, 15, 16, 17 and 20 | [bin] (client-internals/version-profiles/141-217.toml) |
| Claim B | the betas send 34 ids, the 2.1 test set without 7, 11, 15, 16 and 17 only | [bin] (client-internals/decomp-findings-2026-10-24-c/08-test-builds-newworld-newmain.md#newworld-beta1--beta2) |
| Open | ~~the two reads disagree on 8 (`HORSEDEL`) and 20 (`OPENCHEST`); Claim B's count of 34 is 39 less five~~ settled below | [inf] (client-internals/decomp-findings-2026-10-24-c/05-pli-client-to-server.md) |
| Settles it | a re-read of the beta send sites for constants 8 and 20 | [inf] (client-internals/decomp-findings-2026-10-24-c/08-test-builds-newworld-newmain.md#newworld-beta1--beta2) |
| Settled | Claim A: a re-read of every send site in both betas finds no send of 8 or 20 (nor of 7, 11, 15, 16, 17), and no send that passes the id in a register; the betas send 32 ids | [bin] (version-profiles/pli-send-sites-141-217.md#newworld-betas-ids-8-and-20-app-e11) |

### E#12 Whether the token digits are a build date

Reading the `GNW` digits as a build date fits well, but nothing in the binaries states it [bin] (client-internals/build-catalogue.md#patterns-worth-knowing).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the `GNW` digits are DDMMY, on or a few days before the link date | [bin] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| Claim B | the dates fit the change-log order of 2.01 to 2.05, but nothing in the binary names the format | [inf] (client-internals/decomp-findings-2026-10-24-c/10-open-questions-and-corrections.md#open) |
| Open | the reading is a strong fit, not a stated format | [inf] (client-internals/decomp-findings-2026-10-24-c/02-login-token-and-version.md#reading-the-digits-inferred) |
| Settles it | a vendor note or server source that decodes the token | [inf] (client-internals/decomp-findings-2026-10-24-c/10-open-questions-and-corrections.md#open) |

### E#13 Gmap neighbour overwrite on classic-login 2.x clients

A static read predicts that GServer-v2's classic path makes 2.17 and older clients copy each gmap neighbour onto the player's own level [bin][srv] (protocol/gmap-adjacent-level-target.md#short-answer).

| Item | Content | Source |
| --- | --- | --- |
| Prediction | with stock `PlayerClientOriginal`, a 2.17.1 client on a 2x2 gmap shows neighbour boards and links on its own level | [srv][inf] (protocol/gmap-adjacent-level-target.md#what-gserver-v2-sends-srv) |
| Prediction | ending a neighbour reply with the player's cell level name, not the gmap name, keeps `BOARDMODIFY` and chest updates working on 2.17.1 and 2.22 | [bin][inf] (protocol/gmap-adjacent-level-target.md#what-gserver-v2-sends-srv) |
| Not checked | 2.05 rev 2 sends 35 for `bigmap.txt` neighbours and was not read further | [bin] (protocol/gmap-adjacent-level-target.md#limits) |
| Settles it | a loopback lab with a 2x2 gmap: 2.17.1 against stock and fixed framing, and 2.22 against the fixed framing | [inf] (protocol/gmap-adjacent-level-target.md#limits) |

### E#14 Expiry dates of the Themida 5.x/6.00 builds

Four protected builds exit on today's date; where their cutoff lies was not read [bin][lab] (client-internals/v5v6-expiry-and-black-screen.md#open).

| Item | Content | Source |
| --- | --- | --- |
| Open | the cutoff dates of 5.30r3, 5.31r4, 6.00r2 and 6.00r4 (known to run with the clock at 2011-06-14 and 2011-06-28 for 6.00r2 and 6.00r4) | [lab] (client-internals/v5v6-expiry-and-black-screen.md#how-the-expiry-works-530r3-to-600r4) |
| Open | whether the check is WinLicense's own expiration feature or a check inside its VM macros | [inf] (client-internals/v5v6-expiry-and-black-screen.md#how-the-expiry-works-530r3-to-600r4) |
| Open | whether the Themida builds' timer check uses 5.24r4's thresholds | [bin] (client-internals/v5v6-expiry-and-black-screen.md#open) |
| Settles it | a binary search on the guest clock for each build | [inf] (client-internals/v5v6-expiry-and-black-screen.md#open) |

### E#100 Collision of the Bush stamp tiles

Whether a placed bush blocks the player is a runtime question. File membership alone cannot answer it [file] (formats/arrays-membership-2026-11-09.md#structure-and-exact-input).

| Item | Content | Source |
| --- | --- | --- |
| Established file result | the inspected first two arrays exclude Bush values 2, 3, 18 and 19; the earlier membership assertion is superseded within that collection | [file] (formats/arrays-membership-2026-11-09.md#structure-and-exact-input) |
| Existing type-table evidence | the outside client's type bytes describe walls; they do not establish the selected official client's active collision path | [src] (formats/tiletypes.txt) |
| Open | actual blocking of a placed bush for an exact client, table and selected sheet | [file] (formats/arrays-membership-2026-11-09.md#what-the-counts-settle) |
| Settles it | identify that exact consumer or record a controlled scene; file membership alone does not settle runtime collision | [inf] (formats/arrays-membership-2026-11-09.md#what-the-counts-settle) |

### E#101 Size of the type-0 allow lists

An earlier mask count of walkable tiles cannot yet be linked to the lists read from the exact file [file] (formats/arrays-membership-2026-11-09.md#structure-and-exact-input).

| Item | Content | Source |
| --- | --- | --- |
| Established file result | the exact-input lengths, overlap and union are in → §3.5.3.1; they do not reproduce the earlier mask count | [file] (formats/arrays-membership-2026-11-09.md#structure-and-exact-input) |
| Earlier mask | the export counted 3195 non-blocking and 682 blocking tiles | [live] (formats/tile-walk.md#type-0-allow-lists) |
| Open | mask producer, coverage, mapping and selected sheet remain unlinked to the inspected input; no runtime walkability total follows | [file] (formats/arrays-membership-2026-11-09.md#what-the-counts-settle) |
| Settles it | link the original mask and exact file to the producing client path and sheet before interpreting or comparing runtime categories | [inf] (formats/arrays-membership-2026-11-09.md#what-the-counts-settle) |

### E#102 Tile id to pixel position on pics1

Two formulas map a tile id to its place on `pics1.png`. The manual follows the later one, and a 4.04r2 code read agrees with it [file] (formats/tiletypes.txt).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | `col = id % 128`, `row = id / 128`, pixel `(col * 16, row * 16)` | [file] (formats/tiletypes.txt) |
| Claim B | `col = (id % 16) + (id // 512) * 16`, `row = (id // 16) % 32`: eight side-by-side blocks of 512 ids, each 16 columns by 32 rows; Claim A is called wrong in a correction dated 2026-10-25 | [file] (client-internals/client-assets.md#tile-sheets) |
| Open | the manual follows Claim B, the later correction; Claim A's note has not been updated | [inf] (client-internals/client-assets.md#tile-sheets) |
| Settles it | correcting `formats/tiletypes.txt`, or rendering a known board with both rules against a client screenshot | [inf] (client-internals/client-assets.md#tile-sheets) |
| Windows 4.04r2 code | the tile draw path and its invalidation path both compute Claim B's formula before optional tiledef remapping | [bin] (client-internals/windows-404r2-500r7-static-2026-11-09.md#404r2-tile-sheet-layout) |

### E#200 When a GS1 condition counts as true

When a GS1 condition counts as true is now settled for one exact build. Each row gives that result, its exceptions and what stays open in other builds [2.05][bin][lab] (npc-library/gs1-condition-truth-205r2.md#condition-execution-and-parsing).

| Item | Content | Source |
| --- | --- | --- |
| Exact-build resolution | checked original Windows 2.05 revision 2 IF uses zero/nonzero for ordinary finite computed results; computed positive and negative halves are true, computed zero false | [2.05][bin][lab] (npc-library/gs1-condition-truth-205r2.md#condition-execution-and-parsing) |
| Parsing qualification | bare `0.5` and bare `1` are false despite numeric displays 0.5 and 1 (computed `(1+0)` is true); `created` is true despite numeric display zero. Condition-name resolution and numeric message expansion are separate | [2.05][bin][lab] (npc-library/gs1-condition-truth-205r2.md#condition-execution-and-parsing) |
| Separate defect | constant numeric comparisons fold to zero in this build, while dynamic comparison controls work; mechanism and observations carried in §8.1.3 | [2.05][bin][lab] (npc-library/gs1-condition-truth-205r2.md#constant-comparison-folding) |
| Open | other builds, nonfinite/malformed values, complete aliases/precedence and named-flag collisions | [lab] (npc-library/gs1-condition-truth-205r2.md#verification-and-limits) |
| Linux positive follow-up | An independently authored source weapon on original Linux 3.04 produces created/playerenters flag messages and fresh-account persistence. Numeric readbacks and explicit positive comparisons work while tested bare predicates do not activate. This is a separate build scope from the Windows 2.05r2 resolution; no universal numeric threshold or complete predicate/name-lookup rule is established. | [lab][cap] (npc-library/linux-304-gs1-runtime.md) |


### E#201 Four GS1 argument signatures in 2.05

The stored argument letters of four GS1 commands were re-read. What they mean at run time is still open [bin] (npc-library/gs1-signatures-205-followup.md#stored-letters).

| Item | Content | Source |
| --- | --- | --- |
| Static resolution | exact-input stored letters are recorded in → §8.2; the follow-up agrees with the earlier reference and corrects the command reference's alternatives | [bin] (npc-library/gs1-signatures-205-followup.md#stored-letters) |
| Superseded claim | the command reference formerly printed `M`, `F,R,R`, `R,F,R,R` and `S,S` respectively; those are not the stored sequences for the four commands in the checked input | [bin] (npc-library/gs1-signatures-205-followup.md#stored-letters) |
| Open | whether differing argument descriptions express equivalent runtime semantics; conversion and coercion remain untested | [bin] (npc-library/gs1-signatures-205-followup.md#checks-and-limits) |
| Settles it | targeted parser/executor observations or controlled runtime tests of argument conversion in that exact build | [inf] (npc-library/gs1-signatures-205-followup.md#checks-and-limits) |

### E#202 Which message carries GS2 bytecode

Three sources name different messages as the carrier of GS2 bytecode. The Linux rows add partial results without closing the question [srv] (protocol/packet-ids.md; protocol/graphics-movement-bytecode.md#on-wire).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | NPC bytecode is `PLO_NPCBYTECODE`, id 131, sent to clients at or above `CLVER_4_0211` and wrapped in `PLO_RAWDATA` | [srv] (protocol/packet-ids.md; protocol/graphics-movement-bytecode.md#on-wire) |
| Claim B | for v4 and later clients the script prop is replaced by `NPCPROP_CLASS` plus id 197 (`PLO_UNKNOWN197`, "GS2 bytecode"); the weapon-list note also lists 197 as the bytecode that replaces the script for GS2 | [srv] (protocol/packet-layouts.md; client-internals/feature-specs/02-weapons-combat.md#weapon-lists-server-to-client-srv205) |
| Claim C | id 197 is `PLO_LOADSCRIPT`, a list `type,name,saveToDisk,desKey,crc32` | [srv] (protocol/packet-ids.md) |
| Open | whether 197 carries bytecode, a script-load descriptor, or both in different server versions, and how it relates to 131 | [inf] (protocol/packet-ids.md; protocol/packet-layouts.md) |
| Settles it | a capture of a 4.x or 5.x client receiving an NPC with a GS2 script from a lab server | [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |
| Linux 4.04r2 partial result | A static message-131 path strips a three-byte identifier and reaches the compiled-segment reader. No network fixture was delivered; lookup roles, the indirect initialization callback, messages 140/197 and cache validation remain unresolved. The 97-case switch count is not a complete handled-ID count (→ §2.5.12) | [bin] (protocol/linux-404r2-receive-scope.md) |
| Linux cross-version follow-up | Preserve tag normalization and exact-build case behavior without publishing an unproved delivery grammar. The broader question remains partial (→ §2.5.12) | [bin] (protocol/linux-cross-version-receive.md) |
| Linux positive follow-up | Three exact Linux 6.03r7 x64 probes establish class parsing, explicitly registered weapon instruction execution and later continuation at the saved next position. The proxy-origin bodies and corrected descriptor-length boundary are independently reviewed. This is not normal server compiler/writer validation, a script return-value oracle, exact sleep timing, cache-hit proof or rendered gameplay. | [lab][cap] (protocol/linux-603-network-gs2.md) |
| Windows 6.113 capture | 19 decrypted cache bodies: 197 is the descriptor `type,name,1,key,crc`, the CRC covers the stored encrypted body, and the body arrives from the cache or from 140, never inside 197. 4.x ids 131 and 197 are not covered by this capture | [cap] (protocol/gs2-official-bytecode-6113.md#what-this-settles) |
| Linux 6.x class cache | On Linux 6.03r7 x64 and 6.01r1 x86, 197 is a metadata list with the expected CRC and 140 carries the body; a header-only cache file can never be a class hit; a class miss sends 161 with the stored-body CRC. Other builds and server generations stay open (→ §3.8.9) | [bin] (formats/linux-6x-class-cache.md) |


### E#203 The 2.05 `#` message-code set

The full set of `#` message codes in 2.05 is partly recovered. Each row gives a part that is settled and the fields that remain open [bin] (npc-library/gs1-message-codes-205r2.md#selector-membership-and-coverage).

| Item | Content | Source |
| --- | --- | --- |
| Partial resolution | exact original 2.05r2 outer dispatch has 44 selector bytes / 53 family-expanded spellings, including preserved display codes and empty-output #7; supported contract carried in §8.1.11 | [bin] (npc-library/gs1-message-codes-205r2.md#selector-membership-and-coverage) |
| Runtime controls | thirty qualified outputs from three usable offline scenes support bounded expansion behavior; fourth scene diagnostic only | [lab] (npc-library/gs1-message-codes-205r2.md#new-original-client-controls) |
| Field identities | `#a` is the account name and `#L` the recorded level name; `#E` was a space in one context, writer unresolved; a positive pickup/drop control showed `#6` as the carried NPC's lowercased image name, then empty | [2.05][bin][lab] (npc-library/gs1-message-codes-205r2.md#field-identities-a-l-e-and-a-positive-carry-control) |
| Open | the #E writer, quoted scanners, exact numeric formatting and downstream renderer semantics; other builds and live remote selectors unqualified | [bin][lab] (npc-library/gs1-message-codes-205r2.md#new-original-client-controls) |
| Boundary | accepted C5 storage read does not prove a sixth clothing color or alter the five-byte wire color property; property setters have a separate grammar | [bin] (npc-library/gs1-message-codes-205r2.md#character-selectors) |
| Exact 2.05r2 #6 follow-up | carried-NPC image association independently linked to selected pickup/throw/clear paths; runtime, complete selectors/eligibility/lifetime and receiver identity remain unvalidated; other field identities remain open | [bin] (npc-library/gs1-message-codes-205r2.md#independent-carried-npc-association-checkpoint) |
| Exact 2.05r2 #p follow-up | shared parameter list is produced by dispatch splitting actor pending text, distinct from tokenize; callnpc/callweapon use empty-parameter queue wrappers. Only producer linkage is resolved; other E#203 fields remain open | [bin][lab] (npc-library/gs1-event-parameters-205r2.md#producer-and-consumer-linkage; npc-library/gs1-event-parameters-205r2.md#new-end-to-end-original-client-controls) |

### E#204 Member names of the GS1 object arrays

The member names of the GS1 object arrays are settled for one build. What writing to them does, and how they change across builds, is still open [bin] (npc-library/gs1-object-members-205r2.md#parser-binding).

| Item | Content | Source |
| --- | --- | --- |
| Checked-build resolution | explicit suffix records and first-success parser establish the seven families' name-to-ID mappings: 36 records, 35 distinct spellings; carried in §8.2 | [bin] (npc-library/gs1-object-members-205r2.md#parser-binding) |
| Arrow defect | dx663 binds first; duplicate dx664 vertical getter is shadowed. No builtin dy spelling; observing unassigned dy0 does not establish general fallback or no vertical movement | [bin][lab] (npc-library/gs1-object-members-205r2.md#parser-binding; npc-library/gs1-object-members-205r2.md#original-client-corroboration) |
| Open | writes/setter side effects, unknown-member fallback, scanner details, enum meanings, specialized getters/integrity consequences and cross-version changes | [bin] (npc-library/gs1-object-members-205r2.md#coverage-and-limits) |

### E#205 Index of the hare baddy (settled)

The hare baddy's type index is settled: it is type 5, shared with the frog [file][2.05] (npc-library/gs1-reference-205.md#constants-doc; npc-library/gs1-command-reference-205.md#name-tables).

| Item | Content | Source |
| --- | --- | --- |
| Known | 2.05 ships `baddyhare.gif`, so a hare baddy type exists; the baddy name table has 10 names, 0–9 | [file][2.05] (npc-library/gs1-reference-205.md#constants-doc; npc-library/gs1-command-reference-205.md#name-tables) |
| Open | ~~the hare's type index~~ settled below, see `client-internals/baddies-222.md` | [doc] (npc-library/gs1-reference-205.md#constants-doc) |
| Settles it | reading the 2.05 baddy image selection by type | [inf] (npc-library/gs1-reference-205.md#constants-doc) |
| Settled | type 5 (`frog`): the 2.22 client draws type 5 with `baddyhare.png` and plays `frog.wav` for it; the hare and the frog are one type | [2.22] (client-internals/baddies-222.md#types-222) |

### E#206 `move` option bits in 2.05

The `move` command's queued consumer is read for one build. The caller side and some edge cases are still open [2.05][bin] (npc-library/gs1-move-205r2.md).

| Item | Content | Source |
| --- | --- | --- |
| Established | the exact Windows 2.05r2 queued consumer now supplies static replacement, progression, collision and option behavior → §8.2.9 | [2.05][bin] (npc-library/gs1-move-205r2.md) |
| Open | caller frequency/catch-up, complete collision eligibility, unidentified object collection, later event execution, exceptional numeric inputs and bits outside the consumer | [2.05][bin] (npc-library/gs1-move-205r2.md#evidence-and-limits) |
| Settles it | targeted exact-input caller/state tracing and controlled runtime observations for these residuals | [inf] (npc-library/gs1-move-205r2.md#evidence-and-limits) |

### E#207 GS2 language and bytecode format

GS2 syntax, its library and its event model are the largest open question in the manual. Each row adds a result from one build without closing it [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting).

| Item | Content | Source |
| --- | --- | --- |
| Known | 4.x and later clients run GS2 and receive it compiled; 3.153 already handles the NPC bytecode ids | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| Known | 4.2.0.8, 5.0.0.7, and unpacked 6.00 parse one four-segment container, do not share OpenGS1's layout, and run the switch in → §8.4.2 and → §8.3.3. The value stack caps at 10000. Opcode 9 stops past 10000. Opcode 10 stores the stack height and does not jump | [bin] (protocol/gs2-client-vm.md#container-the-client-reads); [bin] (client-internals/gs2-vm-from-engines.md#opcodes) |
| Open | GS2 syntax, the standard library and the event model. The container and the dispatcher for those builds are recorded. Still open: the opcode helpers the engine note did not open, which gameplay site fires each `script_event` name, and packet id 140's own framing | [bin] (client-internals/gs2-vm-from-engines.md#what-is-still-missing-before-a-seihai-vm-can-be-written); [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |
| Settles it | a lab note decoding a captured bytecode message from a 4.x client session, a reading of the built-in command table and the source compiler's grammar, and a note on the GS2 documentation in the archived websites | [bin] (client-internals/gs2-vm-from-engines.md#what-is-still-missing-before-a-seihai-vm-can-be-written); [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |
| Linux 4.04r2 event result | Two instrumented dispatches repeat top-level execution; queued delivery follows the running handler. This partially qualifies the event question, without closing joined-class or other lifecycle semantics (→ §8.3.4) | [cap] (client-internals/linux-404r2-events.md) |
| Linux 4.04r2 continuation result | A positive-sleep snapshot preserves the next instruction through restore; elapsed timing, cancellation and replacement remain unmeasured (→ §8.3.4) | [cap] (client-internals/linux-404r2-sleep.md) |
| Linux 4.04r2 catalog correction | Correct grouping gives 176 types and 332 globals, restoring 38 root-object declarations; binding, conversion and inherited behavior remain unmeasured (→ §8.3.5) | [test] (client-internals/linux-404r2-api-ownership.md) |
| Earlier Linux 4.04r2 VM boundary | Dispatch ends at 190 and slot 11 selects a common skip path; one insertion control completes unchanged. Static frame fields and helper semantics remain qualified (→ §8.4.4) | [bin][cap] (client-internals/linux-404r2-vm-dispatch.md) |
| Linux 4.04r2 embedded linkage | Fourteen structurally validated script candidates include one profile payload matched to live input before executor entry; this is not corpus-wide execution or historical server-content recovery (→ §8.4.7) | [bin][cap] (client-internals/linux-404r2-embedded-scripts.md) |
| Linux cross-version follow-up | Use whole-payload equality and round-trip controls without asserting feature removal or native semantic equivalence. The broader question remains partial (→ §8.4.7) | [bin] (client-internals/linux-cross-version-embedded-controls.md) |
| Linux cross-version follow-up | Separate static selector classifications, executor-entry stops and three observed startup cached jumps. The broader question remains partial (→ §8.4.4) | [bin] [cap] (client-internals/linux-cross-version-dispatch.md) |
| Linux cross-version follow-up | Document static state saving and first-match pending-record replacement without inventing wait/timeout API results. The broader question remains partial (→ §8.3.4) | [bin] (client-internals/linux-420r6-selector11.md) |
| Linux cross-version follow-up | Explain serialized tags versus fused internal selectors while preserving native/validator error-handling differences. The broader question remains partial (→ §8.4.6) | [bin] (client-internals/linux-420r6-reader-fusion.md) |
| Windows 5.00 installed-input boundary | Named/enum delivery queues separately from service; limit-before-dedup and named lifecycle priority are statically bounded for a used/patched backup input. Gates, conversions, reentrancy and runtime timing remain open (→ §8.3.4) | [bin][inf] (client-internals/windows-500-event-queue.md) |
| Linux positive follow-up | Three exact Linux 6.03r7 x64 probes establish class parsing, explicitly registered weapon instruction execution and later continuation at the saved next position. The proxy-origin bodies and corrected descriptor-length boundary are independently reviewed. This is not normal server compiler/writer validation, a script return-value oracle, exact sleep timing, cache-hit proof or rendered gameplay. | [lab][cap] (protocol/linux-603-network-gs2.md) |
| Linux 6.01 x86 static increment | Distinguishes reader/postpass/executor preparation and mixed saved-state handling without claiming full handler recovery, runtime restore or cross-architecture layout equivalence | [bin] (client-internals/linux-601-x86-program-state.md) |
| Official bytecode, 6.113 caches | 19 real server-compiled bodies walk with the 4.2–6.00 container reader: segments 1–4 in order, segment 1 zero, `F0`–`F6` operands in range, no trailing newline, no opcode ≥ 200; the official compiler emits 190 `loadparams`, which the third-party compiler does not | [cap] (protocol/gs2-official-bytecode-6113.md#container-what-all-19-bodies-show) |
| Mac OS X 6.11r1 runner | Decoded 40-byte records with cached handlers, an appended end marker 164, a per-record loop check with default limit 10000, snapshot-based sleep and waitfor, and calls that can suspend on `classesdownloaded`. Table extent, opcode 7, arithmetic handlers and runtime behaviour stay open (→ §8.4.4) | [bin] (client-internals/mac-611r1-gs2-runner.md) |

| Playerworld corpus survey | Three owner-held script sets rank the GS2 constructs real 2007–2008 scripts use (joins, methods, for-each, `switch`, GUI `new`, code outside functions) and the GS1 commands a port must replace; no message code sits inside a GS2 string literal. Language use only, not official compiler output | [lab] (npc-library/gs2-world-corpus-2026-11-12.md) |

### E#208 What the OpenGS1 opcode set describes

Two notes disagree on whether the OpenGS1 opcode set describes official bytecode [src] (protocol/graphics-movement-bytecode.md#scripting--gs1-bytecode).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the graphics-and-bytecode note calls the OpenGS1 VM "GS1 bytecode" and lists the full GS1 opcode set and constant-table layout as known | [src] (protocol/graphics-movement-bytecode.md#scripting--gs1-bytecode) |
| Claim B | 2.05 does not compile GS1 to bytecode; OpenGS1's opcode set is an independent reimplementation that 2.05 does not share | [2.05] (npc-library/gs1-reference-205.md#execution-model-205; npc-library/gs1-commands.md#update-2026-10-21) |
| Known | 4.2.0.8, 5.0.0.7, and unpacked 6.00 do not use OpenGS1's layout | [bin] (protocol/gs2-client-vm.md#container-the-client-reads) |
| Official 6.113 output | real server-compiled GS2 bodies use the four-segment container, not OpenGS1's body offset, constant tables and packed values | [cap] (protocol/gs2-official-bytecode-6113.md#what-this-settles) |
| Open | whether 3.153's bytecode matches OpenGS1, or only OpenGS1 itself | [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |
| Settles it | comparing a captured official bytecode message (→ App. E#207) with the OpenGS1 layout | [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |

### E#209 GS2 VM: what the per-build reading left open

The six-VM reading of 3.153 to 6.03r7 leaves these items open [bin] (client-internals/gs2-vm-by-version.md#not-known).

| Item | Content | Source |
| --- | --- | --- |
| Opcode 54 | a three-operand member store from 5.00r7; what it stores is unknown | [bin] (client-internals/gs2-vm-by-version.md#opcodes-the-open-compilers-do-not-name) |
| Opcodes 48, 49 | operand order unread | [bin] (client-internals/gs2-vm-by-version.md#not-known) |
| `waitfor` timeout | the value given when the timeout runs out; 0 is assumed | [inf] (client-internals/gs2-vm-by-version.md#named-opcodes-with-version-notes) |
| 6.x loop limit | the scrambled property name | [bin] (client-internals/gs2-vm-by-version.md#limits) |
| Unread builds | 4.04r2, 5.12 to 5.31r4, 6.00r2, 6.00r4 and 7.x borrow or lack a VM reading | [inf] (client-internals/gs2-vm-by-version.md#what-was-read) |

### E#300 Frame driver of 4th Graal alpha, 5th Graal and 5th Graal alpha

These three early builds were first said to have no frame timer. An exact read found one in each, and their real tick timing is still unmeasured [bin] (client-internals/early-form-timers-2026-11-09.md#stored-configuration).

| Item | Content | Source |
| --- | --- | --- |
| Superseded observation | the survey formerly reported no form timer for these three builds; the exact-input follow-up finds a configured timer in every one | [bin] (client-internals/early-form-timers-2026-11-09.md#stored-configuration) |
| Static resolution | the configured timer and its static binding are described in → §4.1.2; the three survey interval cells are corrected | [bin] (client-internals/early-form-timers-2026-11-09.md#stored-configuration) |
| Callback execution | a debugger breakpoint counted 61, 61 and 60 callback hits in 3 s for the three builds; this proves execution, not cadence | [lab] (client-internals/early-form-timers-2026-11-09.md#callback-execution) |
| Open | elapsed tick timing, runtime configuration changes and programmatic idle-handler installation remain unmeasured | [bin] (client-internals/early-form-timers-2026-11-09.md#validation-and-remaining-questions) |
| Settles it | runtime observation of those exact builds, preserving the distinction between declared interval and elapsed time | [inf] (client-internals/early-form-timers-2026-11-09.md#validation-and-remaining-questions) |

### E#301 Frame loop of the 3.x and 4.x clients (settled)

The frame loop of the 3.x and 4.x clients was untimed. A 2026-11 lab settled it: every 3.04, 4.04r2, 4.20r6 and 6.03r7 client steps every 50 ms [lab] (client-internals/update-cadence-3x-6x.md).

| Item | Content | Source |
| --- | --- | --- |
| Unobserved | the 3.x and 4.x Torque-era clients' tick length and loop driver; the 5.x and 6.x clients are timed only from their 50 ms position messages | [wire] (protocol/v5v6-lab-play.md); [doc] (version-profiles/matrix/README.md#acts-timing-movement-and-rules) |
| Settles it | a timed walk of a 3.x and a 4.x client on the lab server | [inf] (version-profiles/matrix/README.md#what-is-still-unknown) |
| Windows 4.04r2 clocks | three time notions are traced statically (elapsed ticks via `GetTickCount`, a GS2 script clock advancing 0.05 per pass, legacy `timeout` pass counts); no update rate is measured | [bin][cap] (client-internals/windows-404r2-500r7-static-2026-11-09.md#404r2-clocks) |
| Linux cross-version follow-up | Tie six observed updater returns to a directly registered state predicate without inferring frame cadence or live 3D (→ §4.1.6) | [bin] [cap] (client-internals/linux-420r6-clock-property.md) |
| Settled | 50 ms steps, one render per step, 8 px per walk step; 3.x and 4.x slow down when behind, 6.03r7 makes up one step and drops the rest; GS1 `timeout` counts whole steps rounded down on the C++ engine (→ §4.1.7) | [lab][cap] (client-internals/update-cadence-3x-6x.md#measurements) |
| Still open | 6.03r7's script timer; the `timeout` sweep on 5.x, 6.x and the 1.x/2.x engines; walk GANI timing at run time | [lab] (client-internals/update-cadence-3x-6x.md#not-measured) |

### E#302 Walking speed factors other than 1.0, 1.2 and the hidden 0.2

Two walking speed factors, 0.4 and 0.8, exist in the code, but the states that use them are unknown [2.05] (client-internals/decomp-findings-2026-10-25-l/01-walking-body-box.md#step).

| Item | Content | Source |
| --- | --- | --- |
| Known | the walking code multiplies the half-tile step by a speed factor: 1.0 on foot, 1.2 in a high speed state; hiding gives 0.1 tile per tick | [2.05] (client-internals/decomp-findings-2026-10-25-l/01-walking-body-box.md#step); [live] (client-internals/player-mannerisms-live.md#lifting-carrying-hiding-and-throwing-live) |
| Open | factors 0.4 and 0.8 also exist (0.8 depends on a carried object); which states use them is not traced; carrying measured live does not slow the walk | [bin] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |
| Settles it | a lab walk in each candidate state (riding, shield, carrying each object kind) on 2.05 | [inf] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |

### E#303 Two unidentified lists in the blocked-point test

Two object lists in the blocked-point test have not been identified [bin] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv).

| Item | Content | Source |
| --- | --- | --- |
| Open | the blocked-point test reads a list of objects with two flags and a player-sized body box (only with a client option on), and a list of 1.5 × 2 boxes with an enabled flag; neither is identified (signs, baddies, dropped objects and other players are candidates) | [bin] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |
| Settles it | tracing what fills each list, or a lab test of walking into each kind of level object | [inf] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |

### E#304 Stopping positions and the wire rounding of nudged positions

The stopping positions after a blocked step are read from code but not confirmed live, and the wire rounding of a nudged position is not captured [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#on-a-refused-step).

| Item | Content | Source |
| --- | --- | --- |
| Known | the flush snap and the 0.1 nudges are read from the 2.05, 2.17.1, 2.22 and 2.31 walking routines | [2.05][2.22][2.31] (client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md#on-a-refused-step) |
| Open | the stopping positions are not confirmed on a live client; how the client rounds a position that is not on a half-tile when it sends it is not captured | [bin] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |
| Settles it | a lab walk towards a rock from both half-tile alignments on 2.22, with the props messages captured | [inf] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |

### E#305 The 2.22 push frame field

A memory trace of 2.22 does not match the push timing expected from 2.05 [live][2.22] (client-internals/player-mannerisms-live.md#cross-version-table).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | 2.22 plays `push` as 5 frames × 4 ticks, looping, as 2.05 does | [live][2.22] (client-internals/player-mannerisms-live.md#cross-version-table) |
| Claim B | a memory trace of 2.22 against a public server showed a push frame field cycling 0 to 3 every tick from the moment the blocked count passed 18 | [live] (live-runs/2gta-222-2026-10-30/README.md) |
| Open | whether the traced field is the gani frame or another per-tick counter; the second run used the server's own push gani | [inf] (live-runs/2gta-222-2026-10-30/README.md) |
| Settles it | reading the gani frame field of 2.22 offline with the stock `push.gani` | [inf] (client-internals/player-mannerisms-live.md#open) |

### E#306 The flag that picks `lift2.wav` for a pull

The flag that chooses between the two pull sounds was not traced [2.05] (client-internals/ledges-push-pull.md#grabbing-and-pulling).

| Item | Content | Source |
| --- | --- | --- |
| Open | a successful pull plays `lift.wav`, or `lift2.wav` by a player flag that was not traced | [2.05] (client-internals/ledges-push-pull.md#grabbing-and-pulling) |
| Settles it | tracing the flag in 2.05's pull routine | [inf] (client-internals/ledges-push-pull.md#open) |

### E#307 Probe, nudge and step tables of 1st Graal and 1.39

1st Graal's movement tables are now read. The 1.39 tables are still missing [bin] (client-internals/first-graal-movement-2026-11-09.md).

| Item | Content | Source |
| --- | --- | --- |
| Established for 1st Graal | exact-input static step, six ordered probes, one-eighth-tile nudges and stepped-axis snapping are in → §4.2.2.3; the older unread-table and free-axis descriptions are superseded | [bin] (client-internals/first-graal-movement-2026-11-09.md) |
| Existing 1.39 evidence | six probes and the blocked-step counter shape were read, without the numeric tables | [1.39] (version-profiles/matrix/rules-139.md#wall--walk-test-bin-lab) |
| Open | 1.39 numeric tables, cross-build equality, and complete exceptional gates/runtime cadence for the new static 1st Graal finding | [bin] (client-internals/first-graal-movement-2026-11-09.md#verification-and-limits); [1.39] (version-profiles/matrix/rules-139.md#still-open) |
| Settles it | recover the 1.39 tables independently and validate unresolved runtime/state gates on exact inputs | [inf] (client-internals/first-graal-movement-2026-11-09.md#verification-and-limits) |

### E#308 Link probe offsets and the neighbour-table flag

The offsets used to probe for links, and the flag that skips the neighbour table, are unread [2.05] (client-internals/decomp-findings-2026-10-28/03-edge-links.md#open).

| Item | Content | Source |
| --- | --- | --- |
| Open | the per-facing probe offsets for link following; the flag that skips the 3 × 3 neighbour table; which big map 2.05 uses offline and whether 2.22 does the same with `PLO_BIGMAP` (171); how walking behaves past the edge before the link fires when the neighbour is loaded | [2.05] (client-internals/decomp-findings-2026-10-28/03-edge-links.md#open) |
| Settles it | reading the probe table and the flag in 2.05, and a lab crossing on 2.22 with a big map | [inf] (client-internals/decomp-findings-2026-10-28/03-edge-links.md#open) |

### E#309 Knockback distance of 1.39

The 1.39 binary gives five tiles of knockback, while a live run measured four [1.39] (version-profiles/matrix/rules-139.md#hurt-and-knockback-bin).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the 1.39 binary moves the player one tile per tick while the hurt counter reads 39 down to 35: five steps | [1.39] (version-profiles/matrix/rules-139.md#hurt-and-knockback-bin) |
| Claim B | the offline 1.39 run measured four tiles of knockback on the touch-NPC test | [live][1.39] (client-internals/player-mannerisms-live.md#cross-version-table) |
| Open | whether the live run lost a step to collision or to the ±1 tick of the video timing | [inf] (version-profiles/matrix/rules-139.md#hurt-and-knockback-bin) |
| Settles it | a fresh 1.39 knockback re-measure on open ground | [inf] (version-profiles/matrix/rules-139.md#still-open) |

### E#310 Where the once-per-second hit stamp sits

Two reads disagree on which hit paths share the once-per-second stamp [2.05][2.22] (client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md#gates-shared-by-the-sword-and-the-packets).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the per-attacker second-of-day stamp is shared by the sword and both hit messages, and is stored before the guild test | [2.05][2.22] (client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md#gates-shared-by-the-sword-and-the-packets); [2.05] (client-internals/decomp-findings-2026-10-24-d/03-hit-gates-and-open-points.md#gates) |
| Claim B | in 2.00 to 2.05 rev 2 the stamp is in the hurt-message path only; it was not found in the sword judge of any build | [2.00][2.05] (client-internals/combat-200-204.md#what-changes-by-build) |
| Settles it | a lab test of two sword hits from one attacker inside one second on 2.05 | [inf] (client-internals/combat-200-204.md#confirmed-inferred-not-tested) |

### E#311 Blast hit zone and the occasional full-heart hit

The blast hit zone read from code does not match the pattern of hits measured in the 2.22 lab [2.05] (client-internals/damage-sources.md#bombs-and-explosions).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | a blast piece hurts when its centre, offset by one tile, is under one tile from the player's centre on both axes | [2.05] (client-internals/damage-sources.md#bombs-and-explosions) |
| Claim B | in the 2.22 lab, with a bomb 0.5 or 1.5 tiles off the victim's row, hits came at y offsets +1, +3 and -3 but not at 0 or ±2, and at x offsets ±4 and +5 but not 0 or ±1: a pattern keyed on the bomb's half-tile y rather than a plain radius; a few trials took a full heart instead of a half without a clear rule | [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#b-bombs-arrows-baddies-who-owns-the-damage-part-2-fresh-runs) |
| Settles it | reading the 2.22 explosion routine and repeating the sweep with one bomb per trial | [inf] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#b-bombs-arrows-baddies-who-owns-the-damage-part-2-fresh-runs) |

### E#312 The last byte of a shot

Lab tests suggest the last byte of a shot does more than name its type [2.05] (client-internals/damage-sources.md#shot-19).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the last byte of `PLO_ARROWADD` (19) is the shot type, `byte - 33` | [2.05] (client-internals/damage-sources.md#shot-19) |
| Claim B | in the 2.22 lab an injected shot hurt only when that byte was `0x23` or more; `0x20` to `0x22` did nothing, and a real arrow from another 2.22 client carried `0x21` and never hurt | [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#b-bombs-arrows-baddies-who-owns-the-damage-part-2-fresh-runs) |
| Settles it | reading the 2.22 shot receiver, or a capture of a real arrow that hurts | [inf] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#b-bombs-arrows-baddies-who-owns-the-damage-part-2-fresh-runs) |

### E#313 Do arrows and fireballs pass walls

The code suggests arrows and fireballs fly through walls, but this has not been tested [2.05] (client-internals/damage-sources.md#open).

| Item | Content | Source |
| --- | --- | --- |
| Open | in the 2.05 shot flow types 0 and 1 skip the blocking test that stops types 2 and 3, which would let arrows and fireballs fly through walls; the test's arguments were not recovered | [2.05] (client-internals/damage-sources.md#open) |
| Settles it | a lab shot at a wall on 2.05 | [inf] (client-internals/damage-sources.md#open) |

### E#314 Gmap list order and the level-entry save

Whether entering a gmap from outside saves the respawn point depends on an order that has not been read [2.05] (client-internals/decomp-findings-2026-10-24-d/open-questions.tsv).

| Item | Content | Source |
| --- | --- | --- |
| Open | the order of the gmap's level list and when it is updated against the entry save decide whether entering a gmap from outside saves the respawn point | [2.05] (client-internals/decomp-findings-2026-10-24-d/open-questions.tsv) |
| Settles it | a lab walk from a plain level into a gmap and back on 2.05, dying on each side | [inf] (client-internals/decomp-findings-2026-10-24-d/open-questions.tsv) |

### E#315 The level-entry save in the 2.1 test builds

The level-entry save in the 2.1 test builds is expected to differ from 2.05's, but it was not read [bin][inf] (client-internals/decomp-findings-2026-10-24-d/02-respawn-entry-save.md#which-builds-have-the-group-test).

| Item | Content | Source |
| --- | --- | --- |
| Open | 2.1 test 2 and 3 lack the delimiter constant of the name-group test, so they are expected to have no group test; their entry code was not read | [bin][inf] (client-internals/decomp-findings-2026-10-24-d/02-respawn-entry-save.md#which-builds-have-the-group-test) |
| Settles it | reading the entry routine of the two builds | [inf] (client-internals/decomp-findings-2026-10-24-d/open-questions.tsv) |

### E#316 Glove power steps

Two readings disagree on which objects each glove power can lift [2.05][srv] (client-internals/carry-hide-and-glove.md#glove-power-and-the-lift-table).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | every player starts at glove 1, which lifts the bush, sign and pot; `glove1` adds the light stone and `glove2` the black stone | [2.05][srv] (client-internals/carry-hide-and-glove.md#glove-power-and-the-lift-table) |
| Claim B | a bare hand lifts the first two entries, power 1 adds the pot, power 2 the light and black stones together | [2.05] (client-internals/decomp-findings-2026-10-25-l/03-cut-lift-chest.md#lift-a-key) |
| Settles it | a lab lift of each object on 2.05 at glove 0, 1, 2 and 3 | [inf] (client-internals/carry-hide-and-glove.md#glove-power-and-the-lift-table) |

### E#317 The 1.x pickup box and item draw order

The 1.x pickup box and whether items draw under or over players are unknown [bin] (client-internals/item-drops.md#open).

| Item | Content | Source |
| --- | --- | --- |
| Open | only 1.3's pixel overlap for picking up a floor item was read; the 1.x box in tiles, and whether items are drawn under or over players, are not known | [bin] (client-internals/item-drops.md#open) |
| Settles it | reading the pickup test of 1.39, and a screenshot of a player standing on an item | [inf] (client-internals/item-drops.md#open) |

### E#318 Level reload on re-entry offline

Whether offline 2.05 reloads a level on re-entry, which would bring a cut bush back, is untested [bin] (client-internals/board-respawn.md#open).

| Item | Content | Source |
| --- | --- | --- |
| Open | ~~whether 2.05 offline reloads a level from disk when the player re-enters it, which would bring a cut bush back~~ settled below | [bin] (client-internals/board-respawn.md#open) |
| Settles it | a lab run on 2.05 offline: cut a bush, leave the level, come back and read the board | [inf] (client-internals/board-respawn.md#open) |
| Settled | no reload: 2.05 rev2 keeps the edited level in memory for the session, so cut and thrown bushes stay gone after leaving and re-entering (3/3) and after loading the level again (2/2); the files on disk are unchanged | [lab] (client-internals/lab-cells-200-205-2026-11-13.md#205-rev2-offline-re-entering-a-level) |

### E#319 The single-player start levels

Three level names trigger an extra setup step in 2.05 that was not traced [2.05] (client-internals/offline-tutorial-205.md#special-level-names).

| Item | Content | Source |
| --- | --- | --- |
| Open | loading `level1.graal`, `YoshiClanR2.zelda` or `YoshiClanFields.zelda` runs an extra setup step in 2.05; what the step does was not traced | [2.05] (client-internals/offline-tutorial-205.md#special-level-names) |
| Settles it | loading each name offline on 2.05 in the lab and comparing the player and level state with another level | [inf] (client-internals/offline-tutorial-205.md#special-level-names) |

### E#320 Does any server check the tamper check

No server is known to check the tamper-check value [srv][cap] (client-internals/feature-specs/08-tampercheck.md#public-servers).

| Item | Content | Source |
| --- | --- | --- |
| Open | the clients only send `PLI_TAMPERCHECK` (39); the open-source server discards it, and four public servers accepted a 2.22 login without it for 20 s; whether any server checks the value, or its periodic re-send from 2.31, is unknown | [srv][cap] (client-internals/feature-specs/08-tampercheck.md#public-servers) |
| Settles it | a 2.31 session on a public server with the re-send withheld or altered, which needs the user's approval for a public login | [inf] (client-internals/feature-specs/08-tampercheck.md#needs) |

### E#321 The 2.31 window blacklist

The 2.31 window blacklist and the client's reaction to a match are not decoded [bin] (client-internals/feature-specs/README.md#settled-index-cross-cutting-items-status-as-of-the-lab-batch-c-2026-10-24).

| Item | Content | Source |
| --- | --- | --- |
| Open | 2.31 compares top-level window titles and classes with an obfuscated list every 3.2 s; the list and the client's reaction to a match are not decoded | [bin] (client-internals/feature-specs/README.md#settled-index-cross-cutting-items-status-as-of-the-lab-batch-c-2026-10-24) |
| Settles it | decoding the list in 2.31 and a lab run with a window of a listed title open | [inf] (client-internals/decomp-findings-2026-10-24-b/05-open-items.md) |

### E#322 How others see a key emote

A key emote is drawn locally and not sent, yet captures show an image being re-sent. The source of those frames is unknown [2.05][cap] (client-internals/feature-specs/11-emotes-ganis.md#b-emotes).

| Item | Content | Source |
| --- | --- | --- |
| Open | the 2.05 Ctrl+letter path draws the emote locally and sends nothing, yet captures show `PLI_SHOWIMG` frames re-sending an AFK image about every 3 s; they may come from a server script calling `showimg` or from an untraced path | [2.05][cap] (client-internals/feature-specs/11-emotes-ganis.md#b-emotes) |
| Settles it | a lab capture of a real 2.05 client pressing Ctrl+A next to a second client | [inf] (client-internals/feature-specs/README.md#still-open-after-the-2026-10-24-decompile-pass-new-or-remaining) |
### E#323 Level-object routines not read (2.22)

Several 2.22 level-object routines were not read. The row lists them [bin] (client-internals/decomp-findings-2026-10-25-l/open-questions.tsv).

| Item | Content | Source |
| --- | --- | --- |
| Open | the throw of a lifted object, what a cut or lift drops, the carrying pose, the chest and sign probe points, the glove property value the server sends, snapping after a step, and the swim and carry speed factors were not read | [bin] (client-internals/decomp-findings-2026-10-25-l/open-questions.tsv) |
| Settles it | reading those routines in the 2.22 client, or a lab run per item | [inf] (client-internals/decomp-findings-2026-10-25-l/open-questions.tsv) |

### E#324 Combat rules the 1.21 to 2.31 pass left open

The static pass over 35 builds left four gates unidentified. A follow-up read settled them [bin] (client-internals/combat-baddy-tile-by-version.md#not-known). What stays open is listed below.

| Item | Content | Source |
| --- | --- | --- |
| 1.x packet hits | settled: 1.39 and 1.41 rev 1 handle id 40; open: the extra fields 1.41 rev 1 reads from a body of 6 bytes or more | [bin] (client-internals/combat-baddy-tile-by-version.md#hits-by-packet-ids-40-and-46) |
| Player mode 7 | settled: attached to another local player in same-PC play (carried, or a horse passenger) | [bin] (client-internals/combat-baddy-tile-by-version.md#the-sword-box-the-victim-judging-another-players-swing) |
| Extra victim test | settled: ghost mode (170); the 2.17.1+ judge also stops in Kingdoms or New World mode (176, 177) | [bin] (client-internals/combat-baddy-tile-by-version.md#sword-judge-gates) |
| Respawn AP bands | settled: from 1.41 rev 1, the same bands as 2.05 | [bin] (client-internals/combat-baddy-tile-by-version.md#death) |
| Live checks | the 2-tile sideways edge, a 2.05 no-drop control, 1.21, the sword spark | [inf] (client-internals/combat-baddy-tile-by-version.md#not-known) |

### E#400 Two projects called Ash

Two different things are called Ash in the notes. The manual keeps them apart until their archives are compared [src] (server-notes/01-lineage.md#what-is-binary--world-only).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | Ash is a Python rewrite of the gs2emu protocol, with its own world and default port 14812; it is not the Reborn 2.4 binary | [src] (server-notes/01-lineage.md#what-is-binary--world-only); [src] (server-notes/ash-overview.md) |
| Claim B | Ash is the blueprint pack of the 2006 39ster 2.1 GServer, which describes that server as written, not a rewrite; default port 14822 | [src] (ash/INDEX.md); [src] (ash/ARCHIVAL-NOTE.md) |
| Open | whether the two are one project at two stages or two projects that share a name; the manual keeps them apart (→ §5.2, → §5.3.1) | [inf] (ash/ARCHIVAL-NOTE.md) |
| Settles it | the Drive archives of both, compared by date and content | [doc] (ash/ARCHIVAL-NOTE.md#full-archive) |

### E#401 Listserver reply ids 1 and 2

Listserver ids 1 and 2 are read differently by RC 1.41 and by later clients [srv] (protocol/listserver.md#listserver--client).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | id 1 is NULL (empty) and id 2 is STATUS text with `\r` as a line break; 2.17, 2.22 and the public service send status text as id 2 | [srv] (protocol/listserver.md#listserver--client); [cap] (protocol/public-listserver-2026-10-25.md#frame-and-field-layout-derived) |
| Claim B | RC 1.41 (2002) reads id 1 as one more server entry and id 2 as the end of the list, then disconnects | [bin] (tools/npc-control.md#listserver-login-new-in-141-bin) |
| Open | whether the 2002 listserver used 1 and 2 differently from the later Reborn listserver, or the RC reads them its own way | [inf] (tools/npc-control.md#listserver-login-new-in-141-bin) |
| Settles it | a 2002-era listserver binary or capture, or a re-read of the 2.05 handler for id 1 | [inf] (protocol/listserver.md#205-specifics-205) |

### E#402 The 2000-era listserver reply

Whether today's legacy listserver reply matches the service of 2000 to 2002 is unknown [cap] (protocol/public-listserver-2026-10-25.md#what-the-runs-settle).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the real 2.00-era listserver reply is observed: one plain zlib frame, id 0 only, 4 rows, no status, site or upgrade lines (the public service's 14923 reply to a classic login) | [cap] (protocol/public-listserver-2026-10-25.md#what-the-runs-settle) |
| Claim B | what a real 2.00-era listserver sends is still unobserved; the two-frame list that 2.00 accepted in the lab came from a lab forwarder | [lab] (protocol/listserver.md#205-specifics-205) |
| Open | whether today's 14923 legacy reply is the same as the service of 2000 to 2002 | [inf] (protocol/listserver-login-type-matrix-2026-10-25.md#result) |
| Settles it | a capture of a real 2.00 or 2.05 against the 14923 service, or a 2000-era listserver binary | [inf] (protocol/login-frames-by-version-2026-10-25.md#captures-that-would-settle-it-all-read-only-list-requests) |

### E#403 Classic logins on port 14922

A real 2.17.1 sends a classic login to a port that does not answer it today [cap] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | a real 2.17.1 sends a classic login (shape B) to port 14922, the port in its signed `arrays2.dat` | [cap] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes) |
| Claim B | the public 14922 accepts a classic login and never answers it; the 2001-era tools put pre-2.2 clients on 14923 | [cap] (protocol/listserver-login-type-matrix-2026-10-25.md#result); [src] (tools/server-tools-2001.md#gs2emu-serverlist-thedgtl-snapshot-de66a3f) |
| Open | whether the 2001-era service answered classic logins on 14922, whether 2.17.1 was built for another listserver, and whether the zlib header (`78 DA` against `78 9C`) matters for a classic frame | [inf] (server-notes/lab-servers-2026-10-30.md#real-clients-against-it-today-lab); [inf] (protocol/login-frames-by-version-2026-10-25.md#does-the-evidence-support-classic-logins-look-fake) |
| Settles it | a list-only capture of a pristine 2.17.1 against the public service; this touches a public server and needs the owner's written permission | [doc] (AGENTS.md#labs) |

### E#404 A public server refusing 2.05 inside its own range

A public server refused 2.05 although its printed range seems to include it [src][inf] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the server's printed range runs from 1.41r1 to iPhone Belote 1.5, which in the current version table covers every 2.x to 6.x entry, 2.05 included | [src][inf] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x) |
| Claim B | the same server refused 2.05 (`GNW03081`) | [cap] (server-notes/public-allowed-versions.md#the-refusals-on-record) |
| Open | which version table the server runs; an older table with no 2.05 entry would explain both | [inf] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x) |
| Settles it | one 5.00r7 or 6.03r7 login to that server, with the owner's written permission | [inf] (server-notes/public-allowed-versions.md#open) |

### E#405 RC token `GSERV025`

The server knows an RC token that no RC build read so far sends [srv] (protocol/chat-pm-rc.md#admin-and-staff).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the server knows the RC tokens `GSERV023` to `GSERV025` | [srv] (protocol/chat-pm-rc.md#admin-and-staff) |
| Claim B | the RC builds read send `GSERV007`, `GSERV011`, `GSERV014` and `GSERV019` to `GSERV024`; none sends `GSERV025` | [bin] (protocol/gserv-1999.md#login); [bin] (tools/remotecontrol-lineage.md#builds); [bin] (tools/remotecontrol.md#logins-bin) |
| Open | which RC build sends `GSERV025`, and with which login type | [inf] (tools/remotecontrol-lineage.md) |
| Settles it | a static read of the later RC builds in the Drive RC folder (rc2, the custom RemoteControl, the RC3 beta) | [inf] (protocol/npc-control.md#drive-material-inventory-only-not-in-git) |

### E#406 How the official listserver assigns PC ids

The game server forwards the client's machine fields and stores the PC id the listserver returns; the rule in between is not held [src] (protocol/pcid.md#can-a-pcid-be-derived-from-the-login-fields).

| Item | Content | Source |
| --- | --- | --- |
| Known | the id is a signed 64-bit decimal from `SVI_ASSIGNPCID`; its inputs available to the listserver are the identity string, account, password and the game server | [src] (protocol/pcid.md#can-a-pcid-be-derived-from-the-login-fields) |
| Guess | a row number in a listserver table of machines matched on the hardware hashes; a truncated hash of the fields would fit too | [inf] (protocol/pcid.md#can-a-pcid-be-derived-from-the-login-fields) |
| Also open | whether 5.12 reads the product id as 5.24+ does; what `getlockcomputer` compares; what 6.11+ connector scripts send as machine fields; a lab confirmation of the empty product id under 64-bit Windows | [inf] (protocol/pcid.md#open) |
| Settles it | the official listserver, or captures of its `ASSIGNPCID` replies for known inputs (public servers need the owner's written OK) | [inf] (protocol/pcid.md#can-a-pcid-be-derived-from-the-login-fields) |

### E#420 Flag and chest counts in the RC props tail

The RC props tail holds two counts, and it is not known which counts flags and which counts chests [cap] (protocol/rc-capture-2026-11-04.md#player-props).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the tail after the props block in 72 and 76 holds two `s` counts, then the weapons; one counts flags and one opened chests | [cap] (protocol/rc-capture-2026-11-04.md#player-props) |
| Open | which `s` is which; both were 0 in the only capture | [cap] (protocol/rc-capture-2026-11-04.md#player-props) |
| Settles it | a capture of 72 for a player with some flags and no opened chests | [inf] (protocol/rc-capture-2026-11-04.md#player-props) |

### E#421 The last byte of RC_PLAYERPROPSSET2

The 2004 RC adds one byte the server's message lacks, and its meaning is unknown [cap] (protocol/rc-capture-2026-11-04.md#player-props).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the 2004 RC's 76 ends with one byte after the weapons, 0 in the only capture | [cap] (protocol/rc-capture-2026-11-04.md#player-props) |
| Open | what the byte means; the server's 72 has no such byte | [cap] (protocol/rc-capture-2026-11-04.md#player-props) |
| Settles it | a static read of the RC's 76 builder, or a capture after changing other dialog fields | [inf] (protocol/rc-capture-2026-11-04.md#player-props) |

### E#422 Quoting of folder rights

The 2004 RC and a server fork quote folder rights differently [cap] (protocol/rc-capture-2026-11-04.md#rights).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the 2004 RC sends folder rights lines as CSV, so `rw levels/*` goes out quoted, and splits what it reads back the same way | [cap] (protocol/rc-capture-2026-11-04.md#rights) |
| Claim B | a GServer-v2 fork returned the line unquoted, and the RC showed it as two lines | [cap] (protocol/rc-capture-2026-11-04.md#rights) |
| Open | whether the original server stored and returned the CSV form, which would make the fork's reply a fork bug | [inf] (protocol/rc-capture-2026-11-04.md#rights) |
| Settles it | a capture of 62 from an original 2.x GServer, or a static read of its rights reply | [inf] (protocol/rc-capture-2026-11-04.md#rights) |

### E#423 The 1999 servers: what the static read left open

The read of GServer 1.28 beta 2 and 1.3 leaves these open [bin] (server-notes/gserver-1999-rules.md#not-known).

| Item | Content | Source |
| --- | --- | --- |
| PM reply | which older builds get the "cannot answer" reply | [bin] (server-notes/gserver-1999-rules.md#client-messages) |
| Other levels | how the nickname and head of players in other levels are sent | [bin] (server-notes/gserver-1999-rules.md#own-props) |
| Prop limits | server-side limits beyond the counted props | [bin] (server-notes/gserver-1999-rules.md#own-props) |
| Real-client check | the 1.3 test client against a server running these rules | [inf] (server-notes/gserver-1999-rules.md#not-known) |

### E#424 RC2's Admins folder against a one-space level

RC2 2.05 tests an entry's level by length with no trim, and GServer-v2 sends RCs a level of one space [bin][srv] (protocol/rc-list-online.md#how-rc2-205-shows-them-bin).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the 2001 servers send RCs an empty level, which puts them in RC2's Admins folder | [src][bin] (protocol/rc-list-online.md#how-rc2-205-shows-them-bin) |
| Claim B | GServer-v2 sends one space, so RC2 2.05 would most likely list other RCs under Players | [inf] (protocol/rc-list-online.md#how-rc2-205-shows-them-bin) |
| Also open | the send path of the 2005 Linux i386 RC (unpacked, not read) | [bin] (protocol/rc-list-online.md#open) |
| Settles it | a lab run with RC2 2.05 and two RC logins against the GServer-v2 fork | [inf] (protocol/rc-list-online.md#open) |

### E#500 Back clipping plane of the Graal3D client (settled)

Which back clipping plane the Graal3D client uses was open. A static re-read settled it: 5000 [bin] (graal3d/camera.md#back-clipping-plane-re-read-2026-11-13).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the Direct3D retained-mode library's initial back plane is 100, and the February 2000 client sets no field of its own | [doc] (graal3d/camera.md#field-of-view) |
| Claim B | a later public DelphiX fork calls `SetBack(5000)` during retained-mode init | [doc] (graal3d/camera.md#back-clipping-plane-re-read-2026-11-13) |
| Settled | the February 2000 exe calls `SetBack(5000)` right after `CreateViewport`, the only constant `SetBack` in the exe; Claim B's value holds for this client, and Claim A's 100 is overridden | [bin] (graal3d/camera.md#back-clipping-plane-re-read-2026-11-13) |
| Still open | the value at draw time in a live run with native `d3drm.dll` | [inf] (graal3d/camera.md#still-needed) |

### E#501 Class CRC of the 4.04r2 3D plug-in

Two reads disagree on whether 4.04r2 sends a real class CRC [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the 4.04r2 connect request carries the stock Torque class CRC, so a server needs exactly the same list of networked classes or the client is rejected with `CHR_INVALID` | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |
| Claim B | the 4.04r2 CRC table is static data holding `0xFFFFFFFF` for group 0 with no writer, so nothing computes a CRC, as in 5.12 | [bin] (torque/wire-by-build.md#the-handshake-per-build) |
| Open | which value a real 4.04r2 client sends; Claim B is the later, more specific read, and the 4.x plug-in note now defers to it | [inf] (graal3d/torque-engine-4x.md#not-done) |
| Settles it | a capture of a 4.04r2 connect request | [inf] (graal3d/torque-engine-4x.md#not-done) |

### E#502 Whether 4.04r2 loads `.mis` mission files

Whether 4.04r2 can load a local `.mis` file is open. The network path is confirmed, but a local reader is neither found nor ruled out [bin] (torque/engine-and-formats.md#3d-resource-formats).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | `.mis` mission files are used by 3.x and 4.04r2 | [bin] (torque/engine-and-formats.md#3d-resource-formats) |
| Claim B | the 4.04r2 plug-in does not use `.mis`; the mission arrives over the network | [bin][inf] (graal3d/torque-engine-4x.md#files) |
| Retained-code result | Native mission phases and network ghost construction populate the mission group, including deferred preloading; this is a positive network path, not proof that a separate local mission reader is absent | [bin] (torque/404r2-resource-filter.md#positive-native-mission-path) |
| Open | whether a separate 4.04r2 local mission reader exists and is reachable; the positive network path does not close that question | [bin][inf] (torque/404r2-resource-filter.md#positive-native-mission-path) |
| Settles it | a static read of the 4.04r2 plug-in for the mission loader and its callers, or a capture from a 4.04r2 3D session | [inf] (graal3d/torque-engine-4x.md#not-done) |

### E#503 Whether 4.04r2 reads `.dso` compiled TorqueScript

Whether 4.04r2 still reads compiled TorqueScript is open. The corrected evidence row narrows what the strings show [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the 4.04r2 plug-in's formats include `.dso` compiled TorqueScript | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |
| Historical Claim B | the earlier note inferred no TorqueScript compiler/console and no `.dso`/`.cs` use; the retained-code result narrows download exclusion to one branch and does not establish absence of local readers | [bin] (graal3d/torque-engine-4x.md#overview); [bin] (torque/404r2-resource-filter.md#download-filter) |
| Open | whether a `.dso` reader remains in the plug-in without being reachable | [inf] (graal3d/torque-engine-4x.md#files) |
| Settles it | a static read of the 4.04r2 plug-in for the code-block loader and its callers | [inf] (graal3d/torque-engine-4x.md#not-done) |
| Corrected evidence | Short `.dso` and `.cs` literals occur in the retained 4.04r2 image and participate with `.ter` in a resource-miss download exclusion filter. The earlier defined-string export omitted them; the no-`.dso`-strings claim is withdrawn for this image. Later 5.00r7/5.12 scans are not re-evaluated | [bin] (torque/404r2-resource-filter.md#download-filter) |

### E#504 The `GR3DV003` beta at run time

The later Graal3D beta is known only from static reads [bin] (graal3d/beta3-genesis.md#open-points).

| Item | Content | Source |
| --- | --- | --- |
| Open | whether the public Genesis3D 1.x SDK `genesis.dll` and demo art load in the beta | [inf] (graal3d/beta3-genesis.md#open-points) |
| Open | the built-in defaults of the new physics and camera keys | [bin] (graal3d/beta3-genesis.md#open-points) |
| Open | whether the beta's UDP datagrams match `GR3DV002` byte for byte | [bin] (graal3d/beta3-genesis.md#open-points) |
| Settles it | a lab run with the SDK engine DLL and art against a server patched to accept `GR3DV003` | [inf] (graal3d/beta3-genesis.md#open-points) |

### E#600 Tile layer as GraalEditor writes it

Which board form GraalEditor writes has never been checked against a file it saved [GE] (tools/graaleditor.md#document-model).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | GraalEditor 2.3.1.1 writes `BOARD 0` as 64 lines of 64 decimal tile indices, which the client GLEVNW01 loader does not accept until rewritten as base64 runs | [GE] (tools/graaleditor.md#document-model); [GE] (formats/glevnw01.txt) |
| Claim B | the 2.05 and 2.22 built-in editors, from which GraalEditor is derived, write base64 `BOARD` rows | [2.22] (tools/level-editor/version-deltas.md#3-formats-per-build) |
| Open | which form a file saved by GraalEditor itself holds; the claim was never checked against such a file | [inf] (tools/level-editor/version-deltas.md#3-formats-per-build) |
| Settles it | saving a level from GraalEditor 2.3.1.1 and reading its `BOARD` rows | [inf] (tools/level-editor/version-deltas.md#3-formats-per-build) |

### E#601 Whether link arrival offsets are evaluated

Whether the client evaluates an offset in a link's arrival field is untested [2.22] (tools/level-editor/222-reference.md#8-links).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | link arrival fields may hold `playerx` or `playery` plus a signed offset such as `playery+10`; 21 arrivals in a 3113-level archive have that form, and the link dialog says math and variables may be used | [2.22] (tools/level-editor/222-reference.md#8-links) |
| Claim B | the editors store the arrival text verbatim and do not parse it | [2.22] (tools/level-editor/formats-crossref.md#batch-f-decomp-findings-2026-10-25-f-pr-39) |
| Open | whether the client evaluates the offset when the link fires, or treats it as the bare variable | [inf] (tools/level-editor/222-reference.md#16-open) |
| Settles it | a lab run through a link with an offset arrival, or a trace of the warp code | [inf] (tools/level-editor/222-reference.md#16-open) |

### E#602 Code width of `Z3-V1` boards

Two sources give different board code widths for `Z3-V1.02` [srv] (formats/level-binary.md#z3-v1-differences).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | `Z3-V1.02` uses 11-bit codes and `Z3-V1.03`/`.04` use 12; only the 1998 Java Zelda Online games read `.02` | [srv] (formats/level-binary.md#z3-v1-differences) |
| Claim B | the 2.05 and 2.31 readers use 12 bits for both `Z3-V1` versions they handle; the 2.05 string table lists `.03` and `.04` only | [2.05][2.31] (formats/level-binary-client.md) |
| Open | the two agree on `.03` and `.04`; read as a width for every Z3 file they do not, and whether 2.05's reader is ever called on a `.02` magic is unmeasured | [doc] (docs/book/04-where-the-notes-disagree.md#how-many-bits-a-z3-code-uses) |
| Settles it | a `Z3-V1.02` file decoded both ways, and a trace of whether 2.05 reads that magic | [doc] (docs/book/04-where-the-notes-disagree.md#how-many-bits-a-z3-code-uses) |

### E#603 Whole tiles and fractions in level records

Which level-record fields are whole tiles and which take fractions is not fully listed. A 4.04r2 read covers one reader [srv] (formats/level-binary.md#records).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | coordinates in the binary level records are whole tiles | [srv] (formats/level-binary.md#records) |
| Claim B | `Z3-V1.03` link numbers are floating point and include halves such as `43.5`; GLEVNW01 allows fractional NPC positions; of 18,710 arrival fields in an archive, 12,035 were plain numbers, halves included | [srv] (formats/level-binary.md#z3-v1-differences); [GE] (formats/glevnw01.txt); [test] (client-internals/decomp-findings-2026-10-25-f/02-link-arrival-expressions.md) |
| Open | which fields the whole-tile sentence covers | [doc] (docs/book/04-where-the-notes-disagree.md#whole-tiles-and-fractions) |
| Settles it | a field list for link box, link arrival, baddy, NPC, chest and sign, each with its stated type and one real file of each magic | [doc] (docs/book/04-where-the-notes-disagree.md#whole-tiles-and-fractions) |
| Windows 4.04r2 reader | link boxes are floating point; arrivals stay text; baddy positions are raw bytes and NPC, chest and sign positions bytes minus 32, all whole numbers without half-tile scaling; cross-magic examples still missing | [bin][file] (client-internals/windows-404r2-500r7-static-2026-11-09.md#404r2-binary-level-records) |

### E#604 Where a binary sign list ends

Where a binary sign list ends differs between readers [2.05][2.31] (formats/level-binary-client.md#agreement-with-level-binarymd).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | 2.05 reads signs to the end of the file; 2.31 stops at the first empty line, because a `HEIGHTS` block can follow | [2.05][2.31] (formats/level-binary-client.md#agreement-with-level-binarymd) |
| Claim B | the sign section runs until an empty line or the end of the file | [srv] (formats/level-binary.md#layout) |
| Open | both client behaviours fit Claim B but not each other on a file with signs, a blank line and a `HEIGHTS` block; the server layout does not say which bytes are signs there | [doc] (docs/book/04-where-the-notes-disagree.md#where-a-sign-list-ends) |
| Settles it | one such file read by the 2.05, 2.31 and server readers, with the sign count each keeps | [doc] (docs/book/04-where-the-notes-disagree.md#where-a-sign-list-ends) |
| Windows 4.04r2 reader | the sign reader stops after a line shorter than two bytes or at end of file and does not recognize `HEIGHTS`; only the web-level cache reader reads heights after it | [bin] (client-internals/windows-404r2-500r7-static-2026-11-09.md#404r2-binary-level-records) |

### E#605 Client listserver frames in two vocabularies

Two descriptions of the client's listserver frames use different words and have not been set beside a capture [cap] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | 2.00 and 2.05 send id 0 and `newmain` in one plain zlib frame; 2.17 adds id 1 with account and password; 2.22 and 2.31 send id 7, a key byte, `GNW30123` and `newmain`, then a generation-5 frame with id 1 | [cap] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes) |
| Claim B | the classic Server Lister ELF acts on two client lines, an edition line (id 0) and an account line (id 1), and has no version token and no later cipher | [bin] (tools/classic-tools/serverlist3.md#what-a-client-sends) |
| Open | whether "edition" and "list id 0 and `newmain`" are one observation, and whether "no version token" and "the client sends `GNW30123`" describe two programs; no capture has been laid beside both | [doc] (docs/book/04-where-the-notes-disagree.md#listserver-shapes) |
| Settles it | loopback captures of 2.05, 2.17 and 2.22 written out frame by frame beside both descriptions | [doc] (docs/book/04-where-the-notes-disagree.md#listserver-shapes) |

### E#606 Whether a gmap carries `HEIGHTS` blocks

Whether a gmap holds per-level `HEIGHTS` blocks is settled for one reader. The remaining limit says what is still unknown [doc] (protocol/format-notes-from-salvage.md).

| Item | Content | Source |
| --- | --- | --- |
| Clarified Claim A | the salvage note describes a level grid rather than a tile board; its wording now names coarse and per-level height forms with explicit Windows 4.04r2 reader scope | [doc] (protocol/format-notes-from-salvage.md); [bin][file] (formats/gmap-heights-404r2.md) |
| Historical Claim B | `HEIGHTS` belongs to level files and `HEIGHTMAP` to the generator gmap; writer/server variants differ. Read as exclusive placement, this claim is too broad for the later evidence | [bin] (formats/grmap001.txt); [srv] (formats/gmap.md); [bin][file] (formats/gmap-heights-404r2.md) |
| Bounded resolution | Windows 4.04r2 reads both coarse `HEIGHTMAP` and named per-level `HEIGHTS` inside a gmap; a separate archive-labelled Mac 4.04r2 fixture contains both forms, and the native readers in four Mac PowerPC builds handle both forms too. `HEIGHTS` is not confined to level files (→ §3.2.4) | [bin][file] (formats/gmap-heights-404r2.md); [bin] (formats/gmap-heights-mac-ppc.md#the-reader-in-all-four-builds) |
| Remaining limit | The salvage author's historical intent, rendering, server support and original Windows fixture packaging are not established. Its wording is corrected to state the measured build scope | [bin][file] (formats/gmap-heights-404r2.md#correction-and-limits) |

### E#607 Leftover lines in the protocol cheat sheet

An old protocol cheat sheet still carries lines that later notes withdrew [doc] (protocol/PROTOCOL-CHEATSHEET.md).

| Item | Content | Source |
| --- | --- | --- |
| Claim A | the cheat sheet still shows a raw byte after the version, says RC clients do not scramble, names 100, 101 and 102 as file length, tiles and file blob, and cuts frames into 1,024-byte slices; the recovery note shows guessed ids 1 (login), 16 (level request) and 32 (player update) | [doc] (protocol/PROTOCOL-CHEATSHEET.md); [doc] (protocol/login-recovery-start.md) |
| Claim B | the login has no mystery byte (the extra byte is the generation-3 insertion, and RC 1.x is generation 3 too); 100, 101 and 102 are raw-data, board and file; no 1,024-byte slice is given; the login is type 0, the level request client id 0 and a walk client id 2; directions are 0 up, 1 left, 2 down, 3 right | [doc] (protocol/login-and-walk.md); [doc] (protocol/codec-and-framing.md) |
| Open | these are withdrawals written in the later notes; the manual follows the later notes (→ §2.1–2.3), but no capture has been set beside each leftover line | [doc] (docs/book/04-where-the-notes-disagree.md#a-sketch-that-still-prints-another-frame) |
| Settles it | a 2.05 login, a generation-3 RC session, a generation-5 flush and four labelled facings, each set beside the line it tests | [doc] (docs/book/04-where-the-notes-disagree.md#a-sketch-that-still-prints-another-frame) |

### E#608 How many `arrays.dat` lists make a tile passable

Two summaries disagree on how many `arrays.dat` lists decide walkability, and no runtime consumer has been traced [doc] (CONSOLIDATED.md#tiles).

| Item | Content | Source |
| --- | --- | --- |
| Existing one-list claim | the first array supplies passable tiles and all others are walls | [doc] (CONSOLIDATED.md#tiles) |
| Existing two-list claim | the old-mode 2.05 path checks arrays 0 and 1 | [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| Established file distinction | the operations differ for the exact inspected input → §3.5.3.1; this does not identify a runtime consumer | [file] (formats/arrays-membership-2026-11-09.md#what-the-counts-settle) |
| Open | which operation each exact client path uses, and how the older summary relates to it; the new inspection did not trace consumers | [file] (formats/arrays-membership-2026-11-09.md#what-the-counts-settle) |
| Settles it | trace the exact consumer or test distinguishing list-1-only values in a controlled client scene | [inf] (formats/arrays-membership-2026-11-09.md#what-the-counts-settle) |

### E#609 macOS archive labels and application identity

The macOS archive labels cannot yet be tied to the historical 3.153 build [bin] (version-profiles/macos-client-compatibility.md#archive-labels-and-the-historical-3153-claim).

| Item | Content | Source |
| --- | --- | --- |
| Historical claim | The earlier upload comparison explicitly identifies its Mac uploads labelled 3.04 and 3.15r2 as byte-identical copies of the 3.153 image | [bin] (version-profiles/macos-client-compatibility.md#archive-labels-and-the-historical-3153-claim) |
| Current observation | The newer collection's two v3-labelled main executables share a PowerPC digest, but this collection did not independently authenticate their release version; its five v5 copies also share a main-executable digest | [bin] (version-profiles/macos-client-compatibility.md) |
| Evidence limit | The earlier published note supplies no full input digest for comparison with the current record. It remains unverified whether its image comparison concerns these exact inputs; equality of current main executables is narrower than whole-image or resource equality | [bin] (version-profiles/macos-client-compatibility.md#archive-labels-and-the-historical-3153-claim) |
| Resource follow-up | Regular-file contents and relative names match across two v3 extractions of 718 files each and five v5 extractions of 73 files each; timestamps, permissions, empty directories and original containers were not compared | [test] (version-profiles/macos-resource-identity.md) |
| Open | Exact-input linkage to the historical 3.153 attribution; extracted regular-file equality does not authenticate historical labels or original containers | [bin] (version-profiles/macos-client-compatibility.md#archive-labels-and-the-historical-3153-claim); [test] (version-profiles/macos-resource-identity.md) |
| Settles it | A sanitized comparison supplying the earlier inputs' full digests and authenticated build metadata alongside this collection's identities; broader container/metadata equivalence requires separate evidence if claimed | [inf] (version-profiles/macos-client-compatibility.md#archive-labels-and-the-historical-3153-claim); [test] (version-profiles/macos-resource-identity.md) |

### E#610 Windows 4.04r2 offline initialization versus gameplay

A 4.04r2 offline transition was observed under a harness, but no gameplay was. The rows say what was seen and what is open [cap] (version-profiles/windows-404r2-teardown.md#controlled-offline-transition).

| Item | Content | Source |
| --- | --- | --- |
| Observed | Instrumentation changes the offline-mode flag, allocates an adventure object and observes continued message-loop callbacks | [cap] (version-profiles/windows-404r2-teardown.md#controlled-offline-transition) |
| Open | A complete rendered offline level, player movement and selected cutting, lifting, carrying or hiding behavior in the exact captured build | [cap] (version-profiles/windows-404r2-teardown.md#controlled-offline-transition) |
| Settles it | A version-specific controlled scene with captured user actions and before/after state for each mechanic, preserving fixture and harness identities | [inf] (version-profiles/windows-404r2-teardown.md#controlled-offline-transition) |

### E#611 Windows 4.04r2 pickup semantics and input qualification

4.04r2's pickup state is recovered statically, but no interaction was captured [bin][cap] (client-internals/404r2-carry-state.md).

| Item | Content | Source |
| --- | --- | --- |
| Observed | Static recovery separates pickup action, carried category and carrying flag; no interaction was captured successfully | [bin][cap] (client-internals/404r2-carry-state.md) |
| Open | Meaning of the pickup-bound field, configured physical key-to-action path, and asset/effect qualification of the provisional second cut pattern | [bin] (client-internals/404r2-carry-state.md#open-questions) |
| Settles it | A version-specific semantic read for the bound field and input route, separate asset mapping, and a complete scene capturing each selected action before and after | [inf] (client-internals/404r2-carry-state.md#open-questions) |
| Timing dependency | The countdown cannot supply elapsed timing without the clocks in → App. E#301 | [bin] (client-internals/404r2-carry-state.md#timing-and-input-limits) |
