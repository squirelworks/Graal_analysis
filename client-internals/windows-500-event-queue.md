# Windows 5.00 candidate: event delivery and script service

9 November 2026. Evidence W500-EVENT-QUEUE-20261109. Static retained-code findings, not a runtime trace. Input SHA-256: `dde0fc851e8aaba165a83578745cf10372eca3786219e917966ab3230c7c6bf1`.

The input is the backup engine from an installed archive labelled 5.00r7. The installed folder had been used, updated and patched; a backup filename does not authenticate vendor-original provenance. Do not transfer these exact rules to another build without verification.

## Positive findings

Event delivery and execution are separate operations in the inspected paths. The object-level named-event route can create an execution space and forward an event. The enum-event route requires an existing execution space and an interest check. Both have additional object/virtual gates whose complete semantics were not resolved here.

The execution-space receivers allocate and queue an action, then activate the owner when present. They do not directly call the inspected script-service routine. That routine separately checks gates and the current universe, checks updated classes and scheduled events, and executes queued actions. This is actual native queue/execution code, not a conclusion drawn from GUI names. It does not establish a TorqueScript DSO loader.

Both receivers reject delivery when the existing queue contains 1,000 or more actions, recording an event-overrun script error. This check precedes duplicate suppression. Allocation failure behaviour is outside this handoff.

For the string-named receiver, a null argument object enables duplicate suppression: matching routing string and event name with null stored argument suppresses insertion. This is pending-queue suppression, not a permanent ban on firing the event again. At more than nine queued actions, additional suppression compares argument objects' string representations. The exact string-conversion semantics and identity collisions remain unresolved; do not replace that branch with pointer equality.

The string-named receiver inserts `istimeout`, `created` and `initialized` at the front; other accepted names append. These are internal literal spellings, not automatically the public source-language spellings. The separately inspected enum receiver appends its accepted action: do not apply string-path priority rules globally without mapping and tracing its caller.

Activation checks list membership and avoids adding the same owner again in the inspected path. There is a special front-insertion case outside an ongoing universe service pass; its object category was not resolved here. Universe servicing has a per-pass marker and list-mutation handling. Full reentrant scheduling fairness/order is not established by this review.

## Small synthetic implementation contract

Build a queue-only test around one synthetic owner, a named-event receiver and a recording executor. All argument objects are null; no scripts, historical assets, network or clock are needed. Assume the receiver gates permit delivery and allocation succeeds.

1. Deliver route `fixture` / event `alpha`. Expect one pending action and no execution marker.
2. Deliver the same route/event again. Expect one pending action, still no execution marker.
3. Deliver the same route / event `beta`. Expect pending order `alpha, beta`.
4. Deliver the same route / event `created`. Expect pending order `created, alpha, beta`.
5. Explicitly service the queue through the synthetic executor. Expect those three markers in order. This step tests the proposed reproduction queue adapter; full historical execute-action semantics, deferred scripts and reentrant insertion are outside the fixture.
6. In a fresh queue, deliver 1,000 distinct ordinary names. Expect 1,000 pending actions. The next delivery must report overrun and leave the count unchanged, even if it duplicates an existing event, because the limit check runs first.

These expected outcomes are derived from static branches, not official recorded output. Keep event delivery separate from the scheduler so this slice can be tested before implementing bytecode execution. Do not infer a 20 Hz scheduler from this result: the universe service has clock-related logic, but its real caller cadence and constants have not been resolved by this pass.

## Remaining questions

Resolve event-enum values and their public aliases; trace event-interest checks and virtual gates; verify string conversion used for high-backlog suppression; determine class-download/deferred-action behaviour; and measure the caller of universe script service in an interactive isolated session. Named-event priority does not by itself prove visible creation/timeout ordering across different owners.

Ten retained source digests were verified and matching assembly was retained privately. This note contains no implementation bodies or code locations.

## Evidence and fixture status

[bin] Evidence W500-EVENT-QUEUE-20261109 identifies the owner-held static record. Its researcher-supplied SHA-256 is `e8554b6f05eb6c0c8aa7a3d624bea23d679be222b3004f3b3af429bc783a8cf3`. The publishing preparation checks the sanitized handoff and fixture digests; it does not independently authenticate the historical distribution or turn retained instructions into a new runtime experiment. Server and server commit: none; no new client/server run was performed.

[inf] The adjacent [queue fixture contract](windows-500-queue-conformance.static-derived.json) is independently authored. Every expected result is explicitly **static-derived**, and original-client execution is false. It is a receiver/helper boundary contract, not a capture or complete VM acceptance test.
