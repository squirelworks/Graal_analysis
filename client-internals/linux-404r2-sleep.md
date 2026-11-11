# Record Linux 4.04r2 sleep continuation preservation

Subject: the owner-labelled Linux 4.04r2 x86 ELF, researcher-supplied
executable SHA-256 `50f2057117cfafd5a1151d6e6fdd1413095fa71445ff274bf923ce7dc04198aa`. This identity does not establish equivalence with
a Windows component or another release bearing a similar label.

The publication editor reviewed the sanitized 2026-11-09 research handoff and
recorded its digest. Underlying evidence digests and observations are supplied by
the researcher; raw code, captures and client assets were not opened to fill gaps.
Source IDs resolve through [the evidence index](../docs/evidence-index.tsv).

## Saved continuation

`[cap]` A separate self-authored fixture replaced the persistent main-menu script
input. It requested a positive sleep, later resumed, and executed its following
statement. Native breakpoint observations connected the saved snapshot to its
later restoration: the next instruction was saved, the running position cleared,
and that same next instruction restored from the same snapshot. The requested
duration remained in the saved/restored state. Sources: `L404-SLEEP-FIXTURE`,
`L404-SUSPEND-TRACE` and `L404-SUSPEND-SAVE`.

`[cap]` Top-level output did not repeat between sleep and continuation. It did
repeat before the separately queued event. This is continuation preservation in
the tested persistent-object lifecycle, not a restart of the script at its first
instruction. It is separate from the temporary profile-object event fixture.

## Timing and capture limits

`[cap]` The requested duration was 0.15 seconds. Calibrated elapsed time, clock
rate, frame dependence and timeout precision were not measured. The experiment
does not establish an observed delay exactly equal to the requested duration.
Cancellation and replacement while suspended also remain unmeasured.

`[cap]` Before the experiment, the client initialized to the controlled script
input. Only that input was replaced. The researcher checked snapshot identity,
saved/restored instruction equality, output order and capture completeness.
After the continuation, explicit termination and owned-group cleanup were
verified. Server and server commit were none.

The approved redacted record name is `L404-SUSPEND-TRACE.json`. It aliases an
owner-held evidence carrier; no raw JSON export is published. Its indexed digest
identifies that original carrier, not hypothetical renamed-file contents.

The [later Windows engine clocks](gs2-vm-from-engines.md#timers) retain their
own scope. Their fixed-step observations are not a measurement of this Linux
experiment's timing.

- [x] ~~Connect a positive-sleep save to restoration and the following statement.~~
  Snapshot and next-instruction identity link the two observations.
- [ ] Calibrate elapsed timing and identify scheduling/frame dependence.
- [ ] Test cancellation and script replacement while suspended.
