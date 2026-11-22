# Linux 4.20 rev 8: the 15 January and 17 January images share a protocol-string floor

Date: 2026-11-15. Static printable-string compare of two Linux executables. Nothing was run. **[bin]**

## Images

| Image | Date | Size (bytes) | Already on record |
|---|---|---:|---|
| Linux 4.20 rev 8 | 2007-01-15 | 7,868,224 | Login token `G3D22126` by a connect-routine read ([VERSION-TOKENS.md](../VERSION-TOKENS.md)) |
| Linux 4.20 rev 8 rebuild | 2007-01-17 | 7,876,188 | The Linux 4.20r8 executable in [the receive-path note](../protocol/linux-cross-version-receive.md#exact-executable-inputs) |

The later image is 7,964 bytes larger. The two files are not the same bytes. The byte-count difference does not prove handler behaviour.

## What was read

A protocol-keyword filter over the printable strings of each image. The receive dispatcher of the 2007-01-15 image was not read. The 2007-01-17 image already has the limited case notes in the receive-path note (131 and 193 take distinct paths, 140 falls through, 197 sits outside the guard). This compare does not extend that note to a full id table, and it does not copy those cases onto the earlier image. Those case notes are receive cases for the 2007-01-17 image alone. They are not a parser-body read of these level and gmap literals, and no such parser-body note is cited for the 2007-01-15 image. No level or gmap parser body was read for this compare. String equality does not prove handler behaviour.

## Strings present on both

`GSERVL01`, `GLEVNW01`, `GRMAP001`, and `LEVELNAMES` through `LEVELNAMESEND` are present level and gmap literals in both images, with conventional meanings level-file magic, level-file magic, gmap-file magic, and gmap level-name block. Those meanings are the conventional names of the literals. This printable-string compare did not trace a parser in the 2007-01-15 image. The remaining rows are present strings from the same filter. They are not a new server-to-client id list.

| Literal | Presence | Meaning recorded |
|---|---|---|
| `GSERVL01` | present in both images | conventional level-file magic |
| `GLEVNW01` | present in both images | conventional level-file magic |
| `GRMAP001` | present in both images | conventional gmap-file magic |
| `LEVELNAMES` through `LEVELNAMESEND` | present in both images | conventional gmap level-name block |
| `Graal 4` | present in both images | banner text; not a login token |
| updater file names (`ExeReplacer.exe`, `updatepackages`) | present in both images | update-path names; not a play packet |

The filtered protocol-keyword sets have an empty delta. The extra 7,964 bytes are not a new level magic, gmap key, or protocol keyword on this filter.

## Neighbour

The Windows 4.20r8 engine's 101-id receive set stays the Windows read. It is not a measured set for either Linux image.

`G3D22126` stays the catalogued login token for Linux 4.20r6 and 4.20r8. This string pass did not see that token as one contiguous literal, and it did not re-trace the login builder. No client-to-server send site was read.

## Selected January 17 parser bodies

Added 2026-11-22. The following static instruction and referenced-data reads belong only to the 7,876,188-byte January 17 image. They extend the original string comparison, not the January 15 parser or receive table. Evidence: LNX420R8-PARSERS-20261122 in the [evidence index](../docs/evidence-index.tsv). **[bin]**

The selected level reader obtains an LF-delimited first line, removing a preceding CR. Exact `GLEVNW01` or `GSERVL01` passes its header gate; if neither header matches, it takes cleanup and returns. A selected `BOARD` record consumes four integer tokens and a data token. Its application path checks nominal coordinates in 0–63, positive run length, end coordinate at most 64, and at least two data bytes per position. It decodes pairs through a mutable alphabet and writes words in row-major order in the selected layer. Earlier writes can remain when a later pair fails alphabet lookup. This is not an atomic validation pass, a complete numeric grammar, an overflow/allocation safety proof or a complete level parser. Other records and multiline branches remain outside this selected contract.

The selected gmap reader checks the first string for exact `GRMAP001`, then dispatches exact keys. GMAP key-line tokenization trims edge bytes representing ASCII space or its high-bit counterpart and splits on literal ASCII space; it does not establish tab/general-whitespace splitting, case folding or quoted key-line arguments. The key token is removed before value processing. `WIDTH` and `HEIGHT` use the first remaining token and store dimensions before the selected consumer's positive-dimension guards. Numeric conversion includes decimal, hexadecimal and special-token paths; strict decimal-only validation and a maximum dimension are not established.

`LEVELNAMES` clears one destination list, then parses following raw rows until an exact whole-line `LEVELNAMESEND` or input exhaustion. Parsed fields append in row/field order into that one list using shared string holders, not proved deep byte copies. The loop does not clamp each row to `WIDTH` or validate the number of rows against `HEIGHT`. Its row parser has quoted-comma, doubled-quote and conditional backslash paths, but the complete escape set and malformed-row grammar remain unbound. Allocation-rounding comparisons do not establish a 255-name limit. Other selected keys have dispatch/storage paths, but terrain, image loading and rendering are not demonstrated here.

These reads establish selected reader behavior beyond literal presence. Caller acceptance, complete grammar, malformed-input safety, terrain/rendering and native runtime behavior remain open. Nothing here transfers the findings to January 15 or to another platform.

## Open

- [x] ~~Compare the protocol-keyword strings of the two Linux 4.20 rev 8 images.~~ Empty delta, as above.
- [ ] Read the 2007-01-15 receive dispatcher before treating its id set as the 2007-01-17 set.
- [ ] Complete the level/gmap parser contract: selected January 17 header, BOARD and LEVELNAMES paths are now read above; January 15, remaining grammar, callers and runtime behavior remain open.
