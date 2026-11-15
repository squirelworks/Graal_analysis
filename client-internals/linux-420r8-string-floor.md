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

## Open

- [x] ~~Compare the protocol-keyword strings of the two Linux 4.20 rev 8 images.~~ Empty delta, as above.
- [ ] Read the 2007-01-15 receive dispatcher before treating its id set as the 2007-01-17 set.
- [ ] Read a level or gmap parser body before treating these literals as handler behaviour in either image.
