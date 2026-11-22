# Saved results of selected GS2 waits

Date: 2026-11-22. Static source, selected instruction and data reads; no client was executed for this study. **[bin]**

The first two chains follow an archive-labelled Windows 5.00r7 backup and the recorded Linux 6.03r7 x64 executable. The backup's label does not authenticate a vendor release or establish genuine 5.12 behavior. The Linux input matches its retained static export; that does not independently bind it to every historical lab executable. A separate older archive-labelled input is followed below. These inputs are not evidence of all builds. **[bin][inf]**

Owner-held evidence: GS2-WAIT-RESULT-20261122 in the [evidence index](../docs/evidence-index.tsv). **[bin]**

## Wait entry and saved value

In both selected entries, opcode 11 accesses a duration and two string holders. A nonempty event, an ordered positive duration and the required owner/context enter the successful path. The ordinary rejected-input path pushes numeric zero. Stack underflow, allocation and exceptional capacity paths are separate; zero is not their universal outcome. These direct typed accesses do not establish generic coercion or source-expression evaluation order. **[bin]**

The successful path requests event registration, normalizes the event name, snapshots the continuation and prepares a numeric result of one. Registration is a request, not a delivery guarantee: the selected backup registration routine can return early, while the Linux registration routine returns a success flag that this entry does not inspect. The prefix literal's spelling was not independently bound in this study. **[bin]**

The two implementations have different insertion order. In the selected Windows backup, the ready flag and numeric result are attached before the snapshot is inserted. In the exact Linux path, the snapshot helper inserts the state before returning it to the entry, which then attaches readiness and numeric one. No concurrent observation or reentry guarantee follows from this static sequence. **[bin]**

## Deadline processing

The selected Windows backup stores an absolute deadline from the clock plus duration when the required universe exists. Its deadline pass requires a positive deadline and a strict comparison against the clock plus its small tolerance. It clears the deadline before requesting the saved source/event. If a result exists, it clears the numeric payload without replacing the tag or ready flag. For the numeric wait state just described, that changes the prepared result from one to zero. **[bin]**

The exact Linux deadline pass independently requires an ordered positive deadline and `clock + 0.0001 > deadline`; equality or an unordered comparison does not expire it on this path. It clears the deadline, zeroes an existing result's numeric payload and then requests the continuation event with null arguments. This conclusion comes from that executable's own handler, state fields, constant data and consumer instructions, rather than transferring the backup's layout. **[bin]**

In each selected local service loop, deadline processing precedes pending-action processing. A matching action already queued can therefore encounter a saved value that the deadline pass has changed. This is local execution order, not an event-arrival timestamp rule, fairness guarantee or proof that all event orders are equivalent. **[bin][inf]**

## Matching and restoration

A matching resume restores the prepared value; it does not simply substitute the arriving event's arguments for the wait result. Readiness and execution eligibility still matter. The selected Linux path can discard a saved continuation when the script has been updated. Its numeric restore route copies the complete numeric payload, and its capacity path can grow the node pool; successful allocation is not guaranteed by this read. The backup has its own capacity gate and must not inherit the Linux policy by analogy. **[bin]**

Consequently, one is the prepared successful-wait value, and zero is the value explicitly prepared by selected deadline processing before a successful restore. Queue suppression, registration failure, script changes and other eligibility conditions can prevent that restore. Clearing a deadline before the event request does not establish an automatic retry if the request is suppressed. These are mechanisms, not an unconditional runtime return-value promise. **[bin][inf]**

## Separately retained 4.20r8-labelled input

This additional Windows input is labelled 4.20r8 by its archive provenance. Its retained carrier, source export, instruction listing and bounded data reads agree on one input identity; that does not authenticate a vendor release or bind it to a historical lab process. Evidence: W420-WAIT-RESULT-20261122 in the [evidence index](../docs/evidence-index.tsv). **[bin][inf]**

Its opcode-11 route is independently linked through the decoded opcode translation and handler tables. The entry directly accesses a duration and two string holders, requires a nonempty event, an ordered positive duration and the required owner/context, and otherwise has a separately gated immediate-zero path. Insufficient stack and capacity failure are separate. Neither a nearby opcode name nor another build's dispatch table supplies this binding. **[bin]**

The successful path requests string-source event registration, normalizes the event, snapshots the run and attaches source, event, an absolute deadline, readiness and numeric one. It then saves the state. This is result-before-insertion, unlike the Linux sequence above. The registration call is not evidence of subscription success or safe allocation failure; the selected helper's allocation-null branches continue. The source expression evaluation order and prefix literal's spelling remain outside this read. **[bin]**

Its runner ends that path by returning from the current invocation. There is no explicit suspension-status-two assignment on this selected path. The Linux status convention must not be assigned to this older runner merely because both save a wait. **[bin]**

This input's own deadline consumer independently requires an ordered positive deadline and `clock + 0.0001 > deadline`. It clears the deadline and, when a result exists, both numeric payload words before requesting the saved source/event with null arguments. It leaves the prepared tag and readiness intact. Its local service loop performs this check before pending actions. This again supports a selected prepared-one-to-zero transition, not a wall-clock arrival priority or guaranteed delivery. **[bin][inf]**

Matching compares source and normalized event and removes the selected saved state before eligible execution. Restoration pushes the prepared numeric value only when the ready and capacity checks succeed; its numeric copy route is independently linked by table data and copies both words. This input grows the value pool by one hundred slots and refuses growth above ten thousand. A skipped result push still destroys the consumed state. This is its own resource policy, not the Linux growth path or a promise of retry, memory safety or eventual delivery. No Linux script-update cancellation rule is inferred here. **[bin]**

The older [version note](gs2-vm-by-version.md#named-opcodes-with-version-notes) had left timeout zero as an assumption. This supplies a static mechanism for the separately identified archive-labelled input; it does not retrospectively authenticate every image or run covered by that older version label. **[bin][inf]**

## What remains open

The three-case experiment's [open timeout question](../protocol/script-fuzz-2026-11-19.md#still-open) remains a lab question. These static reads do not supply a new native run, authenticate genuine 4.20r8 or 5.12 behavior, establish source-language event priority or cover every error and ownership path. The older [loader comparison](gs2-vm-loader-diff.md#500r7-and-512) records broader historical readings; the selected inputs audited here should not silently expand their version scope. **[bin][inf]**
