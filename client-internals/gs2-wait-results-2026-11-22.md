# Saved results of selected GS2 waits

Date: 2026-11-22. Static source, selected instruction and data reads; no client was executed for this study. **[bin]**

This follows two separate inputs: an archive-labelled Windows 5.00r7 backup and the recorded Linux 6.03r7 x64 executable. The backup's label does not authenticate a vendor release or establish genuine 5.12 behavior. The Linux input matches its retained static export; that does not independently bind it to every historical lab executable. Neither input is evidence of all builds. **[bin][inf]**

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

## What remains open

The three-case experiment's [open timeout question](../protocol/script-fuzz-2026-11-19.md#still-open) remains a lab question. This static read does not supply a new native run, authenticate a genuine 5.12 engine, settle 4.20r8, establish source-language event priority or cover every error and ownership path. The older [loader comparison](gs2-vm-loader-diff.md#500r7-and-512) records broader historical readings; the two inputs audited here should not silently expand their version scope. **[bin][inf]**
