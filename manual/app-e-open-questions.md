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
