# macOS debugger validation and remaining client tests

This note records the researcher's sanitized 2026-11-09 handoff. The editor
verified the sanitized record digests, not the underlying debugger logs or binaries.
Source identities below refer to owner-held records; no raw material is published.

## PowerPC entry checks

`[cap]` Source `MAC-PPC-ENTRY-20261109` reports tests on Mac OS X 10.4 build
8A428 under Power Mac/G4 emulation, using Apple GDB build 437 in synchronous
mode and resource-complete experiment copies. Server and server commit were none.
Four distinct executable digests cover nine archived main-executable copies:
the two v3-labelled inputs share one digest, the v4.04r2 and v4.20r6 inputs are
distinct, and the v5.12-labelled input shares its digest with four unknown-v5 copies.
Archive labels are not independently authenticated release numbers.

`[cap]` Before each check, the researcher verified input identity. The debugger
then stopped at entry, read registers, stack memory and an instruction, and
stepped one instruction with a changed program counter. Inferior termination
and process cleanup passed for all four distinct inputs. A separate harmless
program smoke test exercised a backtrace; that does not establish Graal stack unwinding.

`[cap]` Source `MAC-PPC-ENTRY-WARNINGS-20261109` retains startup memory-access
warnings for every distinct executable. Passing entry checks does not establish
general symbolic unwinding, long-running debugger stability, a visible window,
renderer initialization, audio, input, login or gameplay. No such result is
claimed by this collection.

The [earlier cloud Tiger runs](../../version-profiles/lab-mac-tiger-2026-10-31.md)
retain their own build identities, renderer adaptations and capture limits.
These later entry checks neither replace nor independently reproduce them.

## Intel v6 and Lion

`[lab]` Source `MAC-LION-BOOT-20261109` is an as-of troubleshooting record for
Lion 10.7.5 build 11G63. Kernel/base-system startup reached a single-user shell,
but Lion was not installed and v6.11r1 was not executed. The graphical installer
was not reached in this evidence snapshot.

`[lab]` The enclosing installer volume and package were readable. Creating an
expected temporary package link advanced startup beyond one waiting helper to
another waiting utility. Increasing memory from two to four GiB did not clear
the original wait. A two-CPU test produced a CPU power-management panic;
changing the clock mode did not resolve it. These observations do not establish
the original stall's sole cause or v6 runtime compatibility. Later troubleshooting
needs a new evidence revision rather than replacing this snapshot's digest.

## Follow-up

- [x] ~~Verify bounded PowerPC entry stops, reads, stepping and cleanup.~~
  The four-input check above supplies that result, with warnings retained.
- [ ] Record offline window and renderer initialization for each distinct PowerPC input.
- [ ] Compare resources separately where main-executable digests match.
- [ ] Finish Lion installation and validate a compatible Intel process debugger.
- [ ] Test the exact v6 input before asserting launch or gameplay compatibility.

The [source index](../sources.tsv) records the sanitized evidence digests.
