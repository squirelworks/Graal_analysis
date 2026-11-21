# Packet probe: Windows 5.12 under Wine, core slice

Date: 2026-11-21. Evidence: **[lab]**, `WINE512-CORE-20261121` in the
[evidence index](../docs/evidence-index.tsv). This adds 32 measured cases to
[`probe-results.tsv`](probe-results.tsv), separate from the eight existing
5.12 GANI-header rows. It does not complete the 5.12 probe campaign.

## Setup and controls

The retained Windows 5.12 client ran under Wine in a Debian lab VM, inside a
loopback-only network namespace. The world proxy recorded authenticated login
with `G3D14097` and a live session before cases were released. The grass scene
and bomb-count HUD were readable. No native Windows result is claimed.

The game server was a retained build associated with the reference fork at
`01bb0b3f9ebca7bb1044c151537c377fd4d5b9d7`. The association comes from the retained
source/build tree and binary identity, not a fresh reproducible build or an
embedded commit check. A separate retained login-server build routed entry;
its source revision was not independently bound. This slice measures client
response to proxy injections, not original-server behavior.

The case payloads match
[`wine-core.plan`](../tools/probe/lab/wine-core.plan) at repository revision
`9f3a4c5c2df889d60271f5b2c6be008208a1ffc8`. Startup waits and reference setup
were separated from the unchanged case tail so a manual positive-control
gate could precede case one. The plan returned zero; all 32 expected case
frames and liveness marks were retained, with no plan error or timeout.

The bomb count was first set to 1 and 99 to establish lost/landed references;
a separate baseline control matched 99. Each case reset it to 1 before the
test. For own props, the trailing `c:5 c:99` was in the **same** prop message.
For the five PLO ids, the canary was in a **subsequent** own-prop message.
Those observations test different boundaries.

The [canary distance rule](../tools/probe/canary.py) was applied to the bomb
digits using calibrated references and an adapted scorer. Independent review
recomputed all 32 case regions plus the baseline: each matched its reference
exactly, with mean grayscale distance about 22.88 from the other reference.
The three lost frames and representative landed frames were also visually
checked. Raw captures, screenshots, client files and original artifact
digests remain outside the repository.

## Results

All cases remained visibly alive. There were **29 landed and 3 lost canaries**,
with none unclear. The exact synthetic payload for each case is in the plan
and the derived result rows.

| Case family | Canary observation | Limit |
| --- | --- | --- |
| Own props 77 and 83 with one-byte values | trailing 99 lands | selected payloads only |
| Own props 77 and 83 with five-byte values | stays at reset value 1 | lost canary, not a crash or proof of a five-byte handler |
| Own props 78/79/80 with `s:` values; 81 with `c:`; 82 with `str:x`; 3 with `i3:` | trailing 99 lands | agrees with the selected parser-width expectations; not a complete width sweep |
| Own prop 90 with `c:1` versus `i3:300000` | one-byte case lands; three-byte case stays at 1 | selected unknown-prop alignment check, not a semantic assignment for 90 |
| PLO 60/78/81/83/110, each empty, `c:1`, text, or `ff00ff00` | all 20 subsequent canaries land | no visible client loss for these bodies; does not prove absence of all handlers, side effects or replies |

For the three lost cases, the injected multi-byte value precedes the canary
inside the same message. A parser that consumes a different width can treat
remaining value bytes as further ids, so a lost canary alone does not identify
which handler or stop caused it. The one-byte controls and the published
[5.x static parser case sets](v5-props.md#5x-one-parser-set-for-the-whole-era)
provide separate context. No whole-client/parser failure or full 0–90 width
table follows from this slice. Replies were not scored as an outcome here.

## Coverage and remaining work

- [x] The 32-case `wine-core` slice on Windows 5.12 under Wine, with positive
  session/HUD controls and per-case evidence.
- [ ] `widths`, `widths-fix`, `bytes2x` and `baddytypes` on this client.
- [ ] Reconcile `loadgani3w` with the eight already published 5.12 PLO 195
  rows before claiming or repeating any additional GANI coverage.
- [ ] The wider 0–90 own-prop sweep, other-player/NPC streams, script read-back
  and remaining builds of G191/G424.

An older attempted batch produced a completion marker but no authenticated
session or accepted case outputs. It contributes **zero** rows here. Accepted
coverage comes from the controlled run above, not a marker, process count or
runner success message. The separate runner exit-status repair does not
retroactively validate that attempt.
