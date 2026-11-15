# String hits, 2026-11-15

A strings scan of client builds. Evidence ID `NRY-COVERAGE-STRINGS-20261115`
([evidence index](../docs/evidence-index.tsv)). It is a strings read only:
not a connect-routine login-token read, and not a runtime or packet
teardown. Nothing was executed.

Login tokens that are already published stay in
`client-internals/version-token-catalogue.md`. This note does not replace
that table. `GSERVL01` and `GLEVNW01` are level-file magics already described
in `protocol/v3x-clients.md`. A hit on those strings is not a login token.
`NW01` and `NW51` below are short literals from this scan, not the
eight-character login token.

Rows are in `nry-tokens-by-build.tsv`. `string_hits` is this scan.
`other_literals` keeps version literals and save tags. Host-name text is
not copied.

## What the scan read

- [bin] ASCII and UTF-16 strings were scanned for short `GNW`, `G3D` and
  `NW` literals, `VERGRAAL`, the level magics, save tags and version
  literals.
- [bin] The Windows 1.25 and 1.27 installers were read statically. The
  installers were not run. This pass adds a short `GNW` on the 1.25
  wrapper, beside `Graal v1.2.5` and `VERGRAAL`, and a short `Gnw` on the
  1.27 wrapper, beside `VERGRAAL`. The login tokens, GS1 counts and handled
  server ids stay in `client-internals/gserv-125-127-builds.md`.

## String hits

These are the literals this scan saw. Connect-routine tokens for the same
builds stay in the catalogue and in `protocol/login-tokens-3x-7x.md`.

| Builds (names the manual already uses) | String hits | Other literals |
|---|---|---|
| Windows 1.25 installer | `GNW`, `VERGRAAL` | `Graal v1.2.5` |
| Windows 1.27 installer | `Gnw`, `VERGRAAL` | |
| Windows FileVersions 1.3.9.1 and 1.4.0.1 | `VERGRAAL` | `Graal v1.3`; save tags `Graalsav9`, `Graalsv10`, `Graalsv11` (the same tags the build catalogue already records from 1.21) |
| Windows FileVersion 1.4.1.1 | `NW01`, `VERGRAAL` | `Graal v1.3` and the same three save tags. The catalogue's 1.39 row is FileVersion 1.3.8.0; this scan did not re-read that row's login token. |
| Windows 2.1.0.0, 2.1.0.2, 2.1.0.4, 2.22 (FileVersion 2.2.2.0) and GraalX 2.0.0.3 | `NW01` | `Graal 2001`. Not a login token. |
| Linux 3.0 beta and Linux 3.01, read from the unpacked images | `NW51`, `GSERVL01`, `GLEVNW01` | `g3d` on 3.01. Level magics, not login tokens. |
| Linux 3.04 and Linux 3.151, read from the unpacked images | `GSERVL01`, `GLEVNW01` | Level magics, not login tokens. |
| Linux 4.03r1, 4.04r2, 4.10r2, 4.11, 4.20r6 and 4.20r8 | `GSERVL01`, `NW01` | `Graal 4` |
| Windows 4.03r3 installer (FileVersion 4.0.3.3) | | `GnW` |
| Windows 4.11 installer (FileVersion 4.1.1.0) | | |
| Windows 4.20r8 launcher | | |
| Windows 4.20r8 packet logger | `GSERVL01`, `NW01` | `Graal 4` |
| Windows 5.00r7 (FileVersion 5.0.0.7) | `GSERVL01`, `NW01` | |
| 5.12-labelled launcher (FileVersion 5.1.2.0) | `GSERVL01`, `NW01` | See the identity sentence below. |
| Windows 6.007 | `G3d` | |
| Windows 6.015 | | `g3D` |
| Windows 6.034 | | |
| June 2011 Linux beta | `GSERVL01`, `NW01` | |
| Graal3D beta | | `Graal 3`. No `GNW`, `G3D` or `GSERV` token literal in this scan. |
| Mac 6.004 | `GSERVL01`, `NW01`, `gServices` | bundle version 6.004 |
| Mac 6.015 | `gServices` | bundle version 6.015 |
| Mac PowerPC 4.10r2, 4.11 and 4.20r6, and one further Mac PowerPC image | `GSERVL01`, `NW01`, `gServices` | `Graal 4` on 4.10r2, 4.11 and 4.20r6. Bundle version `0.6.1d1` is not a release id (`client-internals/mac-ppc-runtime-surface-2026-11-09.md`). |

The 5.12-labelled Windows image (FileVersion 5.1.2.0) is the re-labelled 5.00r7 launcher identified in [launchers-420r8-500r7-512.md](../client-internals/launchers-420r8-500r7-512.md); this strings scan does not claim a new identity.

The 4.20r8 launcher row has none of the scanned literals. The packet-logger build's scan shows `GSERVL01` and `NW01`. That split is a strings result. What those two copies are is already settled in the same launcher note.

## Tags

[bin] is a string or resource read in this pass. A strings hit is not a
connect-routine result and not a runtime result.
