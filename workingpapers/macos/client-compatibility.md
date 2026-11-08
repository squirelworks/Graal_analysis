# Archived macOS client compatibility

`[bin]` Source `MAC-CLIENTS` inventories ten archived Graal main executables by
Mach-O header and load commands without executing them.

- v3.04 and v3.15r2 are PowerPC.
- v4.04r2 and v4.20r6 are PowerPC.
- All five archived v5 copies, including v5.12 and the four unknown-version copies,
  are PowerPC. Folder labels alone do not establish distinct release versions.
- v6.11r1 is Intel 64-bit and declares OS X 10.7.0 as its minimum.

`[bin]` The PowerPC clients reference Carbon, AGL, OpenGL, CoreFoundation,
CoreServices, DrawSprocket, IOKit and the system library. Their inspected headers
do not declare an exact minimum OS version. Tiger was selected as a test environment;
its suitability still requires client runtime testing.

`[bin]` The v6 build references the Intel-era system, graphics, audio and Objective-C
frameworks recorded in the private inventory. A declared OS minimum does not prove
that a particular virtual GPU or debugger is compatible.

`[lab]` The PowerPC and Intel executables need separate machine architectures.
The current Tiger machine emulates a PowerPC Mac; the prepared Lion machine is
an Intel VM. No successful macOS client launch, rendering, input or game-mechanic
test is established by this inventory.
