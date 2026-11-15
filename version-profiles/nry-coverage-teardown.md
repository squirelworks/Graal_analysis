# Coverage string scan, 2026-11-15

A strings scan of staged client builds. It is not a connect-routine login-token
read, and it is not a packet teardown. Nothing was executed.

Login tokens that are already published stay in
`client-internals/version-token-catalogue.md`. This note does not replace
that table. `GSERVL01` and `GLEVNW01` are level-file magics already described
in `protocol/v3x-clients.md`. A hit on those strings is not a new login token.
`NW01` and `NW51` in the table below are short literals from this scan, not
the eight-character login token.

Rows are in `nry-tokens-by-build.tsv`. The `string_hits` column is this scan.
The `other_literals` column keeps version and save-tag literals. Board-link
lines that start with `graal` and a number are recorded only as "board-link
graal strings"; the coordinate text is not copied. A public web-host literal
is recorded without the name.

## What was scanned

- [bin] ASCII and UTF-16 strings, plus a `strings` scan, for `GNW`, `G3D`,
  `GSERV`, `NW` followed by digits, `VERGRAAL`, and nearby version literals.
  Launcher-only builds were also scanned in the companion engine image when
  one was present.
- [bin] 1.25 and 1.27: the InstallShield cabinet was extracted statically.
  The installer was not run. The inner client is the one that carries
  `GSERV009` (1.25) and `GSERV011` (1.27). Those tokens, the GS1 counts and
  the handled server ids are already in
  `client-internals/gserv-125-127-builds.md`. This pass only adds that the
  wrapper also holds a short `GNW` (1.25) or `Gnw` (1.27) literal, beside
  `Graal v1.2.5` on the 1.25 wrapper.
- [bin] Early coverage used a short analyzer budget that stopped several 4.x
  Linux images and one 2.1.0.4 image. A longer budget finished those opens.
  That is a limit of the first pass, not a packer.

## Still open

- [inf] Neighbour diffs, sent and handled packet ids, and prop layouts were
  out of scope. Do not treat a gap here as "the repo has no table" where
  `version-token-catalogue.md`, `protocol/v3x-clients.md` or
  `gserv-125-127-builds.md` already has one.
- [bin] The unpacked 3.x Linux images are still not fully decompiled. On
  3.04 the overview hit the analyzer's client deadline; a later overview of
  the unpacked image reported 13465 procedures and 8420 defined strings.
  Linkage (FMOD 3.70, SDL 1.2, pthread, libc, libdl, libm, X11) is already
  in `client-internals/linux-304-executable-build.md`. A packed-only
  `g3dg15` hit is not an unpacked protocol token.
- [inf] Mac images: entropy and `Info.plist` were read, and a guest ran
  `lipo`, `file` and `codesign`. `otool` was absent, the Mach-O inspector
  did not run, and Ghidra did not open the Mach-O images on the Linux
  analyzer. PowerPC decompile is still open. Load-command lists from this
  pass are not published. `CFBundleVersion` `0.6.1d1` on the PowerPC
  bundles is already recorded as not a release id
  (`client-internals/mac-ppc-runtime-surface-2026-11-09.md`).

## String hits by era

| Era | Folder tags | What this scan saw |
|---|---|---|
| 1.2x installers | `1.25-installer`, `1.27-installer` | Wrapper `GNW` / `Gnw` and `Graal v1.2.5`; inner `GSERV009` / `GSERV011` and `VERGRAAL`. See the existing 1.25/1.27 note for the login token. |
| 1.3.9.1 and 1.4.x | `1.3.9.1-*`, `1.4.0.1`, `1.4.1.1-*` | FileVersions 1.3.9.1, 1.4.0.1 and 1.4.1.1. `VERGRAAL`. Save tags `Graalsav9` / `Graalsv10` / `Graalsv11` (the same tags the build catalogue already records from 1.21). `NW01` on both 1.4.1.1 variants. The catalogue's 1.39 row is FileVersion 1.3.8.0; this scan did not re-read that row's login token. |
| 2.1, 2.22, GraalX | `2.1.0.0-*`, `2.1.0.2-*`, `2.1.0.4-*`, `2.22-*`, `graalx-2.0.0.3` | `NW01`, the literal `Graal 2001`, and board-link `graal` lines. FileVersions 2.1.0.0, 2.1.0.2, 2.1.0.4, 2.2.2.0 and 2.0.0.3. Not a login token. |
| 3.x Linux | `3.0beta-*`, `3.01-*`, `3.04-linux`, `3.151-*` | UPX-packed. After a static unpack: `GSERVL01` and `GLEVNW01` (level magics). `NW51` on 3.0beta and 3.01. `g3d` on 3.01. Login tokens stay the catalogue's connect-routine reads. |
| 4.x Linux and Windows | `4.03r1` through `4.20r8b`, the two Windows installers, `4.20r8-*` | `GSERVL01`, `NW01` and `Graal 4` on the Linux images. The 4.20r8 unpacked launcher alone is quiet; the packet-logger build's scan shows `GSERVL01` and `NW01`. Installer FileVersions 4.0.3.3 and 4.1.1.0. |
| 5.x Windows | `5.00r7-unpacked`, `5.12-untouched-unpacked` | FileVersions 5.0.0.7 and 5.1.2.0. String hits `GSERVL01` and `NW01`. This pass did not show that the 5.1.2.0 image is a different client from 5.0.0.7. |
| 6.x | `6.0.0.7`, `6.0.1.5`, `6.0.3.4`, `6.x-beta-*`, `mac-6.*` | Setup FileVersions 6.007, 6.015 and 6.034. Short hits `G3d` / `g3D`. Linux beta: `GSERVL01` and `NW01`. Mac 6.004: `GSERVL01`, `NW01`, `gServices`, bundle version 6.004. Mac 6.015: `gServices`, bundle version 6.015. |
| PowerPC Mac | `mac-ppc-*` | Bundle version `0.6.1d1` (not a release id). String hits `GSERVL01`, `NW01`, `gServices`, and `Graal 4` on the three later images. Deep Mach-O is still open, as above. |
| Side branch | `graal3d-beta` | The literal `Graal 3`. No `GNW` / `G3D` / `GSERV` token literal in this scan. |

## Tags

[bin] is a string or resource read in this pass. [inf] is a limit of the
pass, not a client behaviour.
