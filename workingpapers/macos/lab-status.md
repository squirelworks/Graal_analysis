# macOS lab status on 2026-11-08

## PowerPC Tiger

`[lab]` Source `TIGER-STATUS` records QEMU Power Mac emulation with a G4 CPU,
one GiB guest memory and a dynamic twenty-GiB disk. The PowerPC Tiger installer
reached its graphical installation interface. No Graal client or server was
executed in the recorded macOS tests; server and server commit are none.

`[lab]` Source `TIGER-INSTALL` reports successful disc-one package installation:
37,622 expected files and 37,622 files written. During finalization, Apple's
boot-configuration utility crashed on a null-pointer access. The installed
volume retained its pending multi-disc-install marker. A later disk boot waited
for application services. Disc two was attached for recovery; successful
continuation and completion are not confirmed in this collection.

`[lab]` Source `TIGER-GDB` records a whole-machine firmware test that read CPU
registers and memory, stepped one instruction, observed changed register state
and detached. This is not a Darwin process-debugging or Graal test. An Apple GDB
binary and guest helpers are prepared, but in-guest execution remains unverified.

- [ ] Confirm that Tiger finishes the remaining installation stage.
- [ ] Verify a clean hard-disk boot and the guest OS version.
- [ ] Verify in-guest process breakpoints, registers, stack reads and cleanup on a harmless program.
- [ ] Test each PowerPC client's launch, input and rendering with a complete copied resource directory.
- [ ] Record a bounded, version-specific client experiment before asserting any game behaviour.

## Intel Lion

`[lab]` Source `LION-MEDIA` identifies Apple's downloaded installer and its
embedded base system as Lion 10.7.5, build 11G63. The extracted installation image
was converted to an uncompressed image and a logical comparison matched its
source. VirtualBox accepted the resulting image as DVD media.

`[lab]` A separate Lion VM was configured with two GiB guest memory, one CPU,
a dynamic thirty-two-GiB disk and no guest network adapter. It remained powered
off throughout preparation. Source `LION-CLIENT` identifies the copied v6.11r1 input.

- [ ] Boot-test the prepared Lion installation media when resources permit.
- [ ] Complete installation and preserve a baseline.
- [ ] Configure and verify a Lion-compatible Intel process debugger.
- [ ] Test v6.11r1 launch, graphics and a chosen runtime observation.

Prepared media and VM configuration are not an installed OS or a validated client.
