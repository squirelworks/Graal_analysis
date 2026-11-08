# Archived macOS client compatibility

`[bin]` Source `MAC-CLIENTS` inventories ten archived Graal main executables by
Mach-O header and load commands without executing them.
The researcher-supplied sanitized record `MAC-V3-ARCHIVE-IDENTITY-20261109`
separately confirms the v3 executable comparison; the editor verified that
record's digest, not the original binaries.

- Inputs archived under v3.04 and v3.15r2 labels are PowerPC and share one
  main-executable digest. These labels do not establish two distinct builds.
- v4.04r2 and v4.20r6 are distinct PowerPC main executables.
- All five archived v5 copies, including the v5.12-labelled input and four
  unknown-version copies, are PowerPC and share one main-executable digest.
  Folder labels alone do not establish distinct release versions.
- v6.11r1 is Intel 64-bit and declares OS X 10.7.0 as its minimum.

`[bin]` The PowerPC clients reference Carbon, AGL, OpenGL, CoreFoundation,
CoreServices, DrawSprocket, IOKit and the system library. Their inspected headers
do not declare an exact minimum OS version. Tiger was selected as a test environment;
its suitability still requires client runtime testing.

`[bin]` The v6 build references the Intel-era system, graphics, audio and Objective-C
frameworks recorded in the private inventory. A declared OS minimum does not prove
that a particular virtual GPU or debugger is compatible.

`[bin]` These comparisons concern main executables only. They do not establish
identical resources, complete application bundles or authenticated release names.
The separate published [3.153 study](../../protocol/v3x-clients.md) retains its
own input identity; equivalence with these archive-labelled inputs is unmeasured.

`[lab]` The PowerPC and Intel executables need separate machine architectures.
The current Tiger machine emulates a PowerPC Mac; the prepared Lion machine is
an Intel VM. No successful macOS client launch, rendering, input or game-mechanic
test is established by this inventory. Earlier cloud runs of 3.153 and 4.20r6
are documented separately in the [Tiger lab note](../../version-profiles/lab-mac-tiger-2026-10-31.md);
the absence of execution in this inventory does not invalidate those observations.

- [ ] Authenticate the two v3 archive labels against the separately studied 3.153 input.
- [ ] Compare resource manifests before asserting whole-bundle equivalence.
