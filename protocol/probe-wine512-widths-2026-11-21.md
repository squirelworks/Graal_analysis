# Windows 5.12 under Wine: 100 selected own-prop canary cases

Date: 2026-11-21. **[lab]** Evidence ID `WINE512-WIDTHS-20261121` in the
[evidence index](../docs/evidence-index.tsv). This covers the 91-case `widths.plan` scan and nine nonzero
`widths-fix.plan` follow-ups, not a complete semantic or width specification for 5.12.

## Controlled run

The retained Windows 5.12 client ran under Wine in a Debian lab VM, inside a
loopback-only network namespace. Authentication with `G3D14097`, a live-session
response and a readable grass/HUD scene preceded case execution. Independent
1/99 bomb-count references and a separate positive baseline calibrated the
canary. No native Windows run or new client build is claimed.

The world server was a retained build associated with reference-fork revision
`01bb0b3f9ebca7bb1044c151537c377fd4d5b9d7`, based on the retained source/build
tree and binary identity; no fresh reproducible build or embedded-commit
verification was performed. Entry used a separate retained login-server build
whose source revision was not independently bound.

Case payloads match [`widths.plan`](../tools/probe/lab/widths.plan) at
`9f3a4c5c2df889d60271f5b2c6be008208a1ffc8`. Startup waits/reference setup were
separated for a positive-control gate, without changing the case tail. The
retained launcher result records `PLAN_EXIT=0`. There are 91 distinct case
frames and 91 window-liveness marks, no missing expected frame and no plan
error or timeout. Independent review matched all 182 case injections against
the plan and recomputed the 91 case regions plus the extra baseline.

Each case resets bombs to 1, then injects one selected own-prop body followed
by `c:5 c:99` in the **same message**. The plan was originally written around
the documented 6.03r7 forms, not newly established 5.12 widths. Reaching 99
therefore records this payload's alignment outcome, not proof that every
preceding value has its intended meaning or was consumed at a uniquely
determined width. A lost canary is likewise not a whole-client failure.

## Results and the non-exact lost case

The 91 cases produced **88 landed, three lost and zero unclear canaries**.
The extra baseline is not a 92nd case. Case id 89 belongs to the 91 and landed.
The exact synthetic bodies and observations are in
[`probe-results.tsv`](probe-results.tsv); client replies were not scored.

| Selected prop/case | Body before trailing bomb canary | Observation |
| --- | --- | --- |
| 51 | no separate value | lost; bomb region matches reset reference |
| 76 | `i3:1252` | lost by the distance threshold; **does not exactly match either reference** |
| 83 | `i5:7` | lost; bomb region matches reset reference |
| The other 88 selected cases in the plan | see the pinned plan/result rows | landed; not a width or semantic proof for all 88 ids |

For case 76, mean grayscale distances are approximately **19.14 to the reset
reference** and **40.34 to the 99 reference**. The adapted
[canary rule](../tools/probe/canary.py) classifies lost when the first distance
is less than half the second. It passes that rule but is not an exact reset
match. Cases 51 and 83 have zero reset-reference distance. The baseline's 99
distance is zero. This distinction is retained rather than reporting all
three lost frames as identical to the reset control.

## Nine nonzero follow-ups

A separate authenticated session on the same client/server combination ran
[`widths-fix.plan`](../tools/probe/lab/widths-fix.plan) at the same pinned
revision. Fresh 1/99 references and an extra positive baseline passed the
control gate before case execution. Independent review matched all 18 case
injections, nine frames and nine liveness marks; the retained launcher records
`PLAN_EXIT=0`. All ten scored regions, including baseline, were recomputed
without disagreement. The local scoring port used the published ROI/distance
rule; execution of the original Pillow scorer is not claimed.

Eight cases landed: 24, 27, 28, 29, 30, 31, 36 and 42. Case 77 lost and
exactly matched the reset reference (mean distances 0 to reset and about
22.88 to 99). Each landed region matched its fresh 99 reference. The i3 cases
used `16511`; cases 30 and 77 used `i5:2080768`; case 42 also prefixed `c:0`.
The trailing bomb canary remained in the same injected message.

The earlier all-zero body for 77 landed, while this nonzero body lost.
Consequently the earlier acceptance does **not** establish a five-byte value
width for 77. This agrees with the separate core slice's failed i5 and landed
single-byte probes without proving complete value semantics.

Together the two slices contain **100 cases: 96 landed, four lost and zero
unclear**. The two extra baseline controls are not cases. The 91-case lost
case 76 retains its non-exact threshold qualification above; it is not an
exact reset match. These counts exclude the separate 32-case core slice.

## Limits and remaining plans

- [x] The 91 selected `widths` payloads on Windows 5.12 under Wine, with
  authenticated entry, calibrated controls and reviewed per-case outputs.
- [x] The nine selected nonzero `widths-fix` follow-ups, with fresh controls
  and independent receipt review; no complete-width claim follows.
- [ ] `bytes2x` and `baddytypes` on this client.
- [ ] Reconcile `loadgani3w` with the eight existing 5.12 PLO 195 rows before
  another GANI coverage claim or repeat run.
- [ ] Establish values, exceptional-input behavior, other-player/NPC streams
  and exact widths beyond what these selected canary bodies discriminate.

The separate [32-case core slice](https://github.com/squirelworks/Graal_analysis/pull/759)
has its own payloads and evidence; its counts are not merged into the 100 here.
G424 and G191 remain open for their wider scopes. Raw screenshots, logs,
client binaries, artifact digests and private retrieval details stay outside
the public repository. No additional lab run was needed for publication.
