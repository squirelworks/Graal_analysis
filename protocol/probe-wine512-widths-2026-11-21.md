# Windows 5.12 under Wine: 91 selected own-prop canary cases

Date: 2026-11-21. **[lab]** Evidence ID `WINE512-WIDTHS-20261121` in the
[evidence index](../docs/evidence-index.tsv). This is the `widths.plan` payload
scan, not a complete semantic or width specification for 5.12.

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

## Limits and remaining plans

- [x] The 91 selected `widths` payloads on Windows 5.12 under Wine, with
  authenticated entry, calibrated controls and reviewed per-case outputs.
- [ ] `widths-fix`: the nine follow-up cases have not been run in this slice.
- [ ] `bytes2x` and `baddytypes` on this client.
- [ ] Reconcile `loadgani3w` with the eight existing 5.12 PLO 195 rows before
  another GANI coverage claim or repeat run.
- [ ] Establish values, exceptional-input behavior, other-player/NPC streams
  and exact widths beyond what these selected canary bodies discriminate.

The separate [32-case core slice](https://github.com/squirelworks/Graal_analysis/pull/759)
has its own payloads and evidence; its counts are not merged into the 91 here.
G424 and G191 remain open for their wider scopes. Raw screenshots, logs,
client binaries, artifact digests and private retrieval details stay outside
the public repository. No additional lab run was needed for publication.
