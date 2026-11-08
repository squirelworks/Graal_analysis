# Bound Linux 4.04r2 opcode dispatch and frame evidence

Subject: the owner-labelled Linux 4.04r2 x86 ELF, researcher-supplied
executable SHA-256 `50f2057117cfafd5a1151d6e6fdd1413095fa71445ff274bf923ce7dc04198aa`. This identity does not establish equivalence with
a Windows component or another release bearing a similar label.

The publication editor reviewed the sanitized 2026-11-09 research handoff and
recorded its digest. Underlying evidence digests and observations are supplied by
the researcher; raw code, captures and client assets were not opened to fill gaps.
Source IDs resolve through [the evidence index](../workingpapers/sources.tsv).

## Earlier dispatch boundary

`[bin]` The executor range check ends at opcode 190. The indexed table therefore
has 191 slots; 119 select paths other than its common skip path. Slot 11 selects
that skip path. The researcher checked the range and entries against executable
bytes as well as decompilation. The later fused-opcode range is outside this
table. Sources: `L404-DISPATCH` and `L404-EXECUTOR`.

`[bin]` Every opcode used by the fourteen extracted script streams selects a
non-skip slot. This checks those streams against dispatch coverage; it does not
recover every selected helper's semantics or prove all streams ran.

`[cap]` Inserting slot 11 into the event-control fixture left the tested event
order unchanged and permitted completion. That one insertion context does not
establish every possible meaning of the value. Source: `L404-SLOT11-CONTROL`.

`[cap]` Before this control, the owned executable was stopped at the profile-loader
boundary. A self-authored fixture with one added opcode 11 replaced only its
in-process input buffer and length. No executable, signature file or signature-check
instruction was patched. The script-running caller returned after the observed
event sequence; the inferior was explicitly terminated. Server and server commit
were none. The researcher reported an untruncated capture, debugger exit zero,
temporary-state removal and verified owned-group cleanup with no unverified processes.

The approved redacted record name is `L404-SLOT11-CONTROL.json`, an alias for
the original owner-held carrier. The indexed digest identifies that carrier;
no raw or newly renamed JSON export is published.

## Guarded frame transition

`[bin]` A reviewed helper checks call depth, reports overrun on its guarded path,
creates a frame-like object, saves the prior execution position, pushes the
frame and changes active state. Semantic field names remain inferred. No new
successful live stop in this helper was obtained; earlier breakpoint misses
are inconclusive. Source: `L404-FRAME-TRANSITION`.

## Version and semantic limits

The [later Windows opcode study](../protocol/gs2-client-vm.md) and
[client-only opcode note](../protocol/gs2-client-only-opcodes.md) concern different
subjects. Their slot-11 wait behavior and fused opcodes are not transferred to
this earlier Linux executable. This is a versioned scope difference, not proof
that those later readings are wrong.

- [x] ~~Bound the earlier table and test one slot-11 insertion.~~ The checks above do so.
- [ ] Recover the selected helper semantics and exact cross-platform correspondence.
- [ ] Confirm the static frame operation at a successful live helper stop.
- [ ] Identify fields before reusing another build's frame layout.
