# 3D network fuzz, tier 1: malformed server packets on 5.12 and 4.04r2 (2026-11-25)

Lab: the real 5.12 and 4.04r2 clients in VMs against our own gserver with its
lab mutation hook (`graal3dmutate`, PR #154 at 8b08c949). One seeded mutation
per link. Behaviour only; the mutated bytes and timings are in the lab share
(`runs.tsv`). Board rows: T3D-038, T3D-097, T3D-105, T3D-114. **[lab][cap]**

Runs: 27 on 5.12 (9 kinds x seeds 1-3) and 9 on 4.04r2 (Wine, seed 1). Both
baselines load cleanly.

## Crashes and bad behaviour

- **5.12, `event-bad-length` (seed 1): a garbled remote command ran, then a
  crash.** A RemoteCommandEvent claimed 38 bits but carried 37. The client
  executed a garbled remote command ("vni ttt...") and then hit an access
  violation in the 3D engine. So the client does not fully bound-check an
  event's declared length against its payload before acting on it, and an
  under-length RemoteCommandEvent can both run the wrong command and crash
  the client. This is the most serious tier-1 finding.
- **4.04r2, `ghost-uncreated`: crash.** An update addressed to a ghost index
  that was never created gave an access violation. 5.12 survives this kind
  on all three seeds (it logs and drops the update), so 5.12 added the guard
  that 4.04r2 lacks.
- **Both clients, `accept-protocol`: clean drop.** A wrong protocol number in
  the connect accept drops the link within ~70 ms with no message (black
  screen). Expected, but note there is no user-facing reason shown.

## Survived (sometimes with a console line)

On 5.12 (and 4.04r2 where run), these did not crash; some logged "Invalid
event received (unknown event type)" or "(wrong direction)":

- `accept-classtable` (dropped or renamed event classes)
- `event-unknown-class`
- the other `event-bad-length` seeds
- `ghost-double-delete`
- `ghost-index-width` (a different raw 4-bit width)
- `control-wrong-class` (control object set to a Sky or Sun ghost)
- `control-deleted`

## Takeaways

- A single under-length event is enough to crash 5.12 and, worse, to make it
  run an unintended remote command. The event length wrapper is trusted.
- 4.04r2 crashes on an unknown ghost index that 5.12 tolerates.
- The next tier is the file loaders (`.3ds`, `.dts`, `.dif`, textures) from
  the fuzz target list (`3d-fuzz-targets-by-build.md`).
