# Archived macOS client compatibility

`[bin]` Source `MAC-CLIENTS` inventories ten archived Graal main executables by
Mach-O header and load commands without executing them.
The researcher-supplied sanitized record `MAC-V3-ARCHIVE-IDENTITY-20261109`
separately confirms the v3 executable comparison; the editor verified that
record's owner-held digest, not the original binaries.

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

`[bin]` The main-executable inventory alone does not establish identical resources,
complete application bundles or authenticated release names. A separate
[resource comparison](resource-identity.md) now establishes matching regular-file
contents and relative names within the extracted v3 and v5 groups. It does not
authenticate original containers, filesystem metadata or release names. `[test]`

## Archive labels and the historical 3.153 claim

`[bin]` The earlier [upload comparison](../../protocol/v3x-clients.md#the-uploads-for-the-record)
explicitly reports that the Mac uploads labelled 3.04 and 3.15r2 are byte-identical
and both are the 3.153 image. This is an existing release-identification claim,
not merely a study of an unrelated version, and it is retained as that author's evidence.

`[bin]` The current `MAC-V3-ARCHIVE-IDENTITY-20261109` record independently reports
matching main-executable digests for the two archive labels, but says release
authentication was not performed. The earlier note does not provide a full input
digest that can be compared with this record. Consequently, whether the earlier
image comparison used these exact inputs remains unverified by this collection.
Executable equality here supports the earlier equality claim in shape; it does
not independently authenticate its 3.153 attribution or whole-image equality.

`[inf]` A sanitized comparison tying the earlier inputs' full digests and build
metadata to this collection would settle that linkage. Until then, retain both
the historical 3.153 attribution and the newer record's narrower identity limits.

`[lab]` The PowerPC and Intel executables need separate machine architectures.
The current Tiger machine emulates a PowerPC Mac; the prepared Lion machine is
an Intel VM. No successful macOS client launch, rendering, input or game-mechanic
test is established by this inventory. Earlier cloud runs of 3.153 and 4.20r6
are documented separately in the [Tiger lab note](../../version-profiles/lab-mac-tiger-2026-10-31.md);
the absence of execution in this inventory does not invalidate those observations.

- [ ] Authenticate the two v3 archive labels against the separately studied 3.153 input.
- [x] ~~Compare extracted regular-file resources where executable digests match.~~
  [Revision 1](resource-identity.md) supplies that result; original containers and
  filesystem metadata remain outside the comparison.
