# Supplied 701750 input: managed/native bridge and clock checkpoint

## Exact input and verification boundary

[file] This scope concerns the supplied Windows x64 recovered native engine and managed GameAssembly analysis images. Their exact SHA-256 identities remain in the owner-held receipt and are not published. The embedded application string 701750 is not independently authenticated release provenance; Unity's engine version is a separate identifier. Original-to-recovered derivation was not independently reproduced by the publisher. These are analysis-image identities, not a claim of original packed-byte identity.

[bin] The retained validation contains ten selected engine-function records in total, including the independently bounded short leaf; the leaf is not an eleventh function. The pass used Ghidra 12.1.4 with original PE exception ranges where available. Every selected Ghidra instruction start matches the independent Capstone decoding, with no missing starts or selected failure markers. Whole-program auto-analysis was disabled. Earlier placeholder extents were superseded by the range-corrected pass. This establishes selected-range agreement, not recovered source-level types, every indirect target or whole-program completeness. The publisher reviewed the sanitized receipt, retained structured validation and input linkage; no executable was rehashed/decoded or target run performed by the publisher.

## Distinct managed update edges

[bin] Managed `UnityMain.Update` calls native `QuattroUpdate`. Managed `UnityMain.FixedUpdate` has a conditional tail jump to its corresponding native bridge. They are distinct static call paths; they do not establish one universal simulation frequency, actual invocation cadence or runtime branch reachability.

## Native clock and guarded event path

[bin] `QuattroUpdate` increments a counter and obtains a clock value through a wrapper whose import slot is `kernel32` `GetTickCount`. The caller stores the returned value as 32 bits. A pseudocode-inferred void wrapper type is not authoritative over that caller register/store flow. Exact cadence, elapsed-time consumption, wrap handling and catch-up policy remain unresolved.

[bin] `QuattroFixedUpdate` checks state guards. On the admitted path it iterates a registered collection and invokes a dispatcher with literal event name `onFixedUpdate` and an empty argument string. The complete semantic identity of that collection and every callback implementation are unresolved. This does not establish full event scheduling, object lifecycle or live event delivery.

## Update3D is a state getter in this input

[bin] The inspected `Update3D` is a small wrapper around a one-byte state getter. Its export name does not establish a scene simulation loop. The [older build-614 bridge inventory](v7-graal3d-unity-bridge.md) retains its own target and evidence scope; shared export names are not whole-function identity or evidence for transferring this result to build 614, v6 or older clients.

## Screened receipt readback

[file] The retained receipt and structured validation were read for this correction. The validation has ten function records, all marked passed, with matching independent instruction starts and no missing starts or selected failure markers. Two managed entry-edge records are separate from that engine-function count.

[bin] Six recorded roles support this publication: the two native update bridges, the clock wrapper, the dispatcher, the Update3D wrapper and its state getter. The four remaining records concern coordinate and level-bridge work, which this note does not publish. The selected receipt supports the managed/native edges, imported clock call and caller's 32-bit store, guarded dispatch with empty arguments, and one-byte getter described above.

This is readback of researcher-produced records, not a fresh native decoding or runtime validation. Exact input identities, ranges, raw listings and private retrieval locations remain owner-held.

## Evidence and remaining questions

No client, DLL entry point, VM or imported script was executed for the source pass. Its initial REA query timed out without a dossier; the completed focused local Ghidra pass used an isolated settings/cache location, 2 GiB heap and two analysis CPUs. Those failure/success stages remain distinct. Generated pseudocode and original native material stay private and are not clean-room implementation source. Server and server commit: none.

The public source identifier `W701750-FOCUSED-NATIVE-20261109` refers to the screened receipt. The publisher matched its privately retained digest; native input identities and observations remain researcher-supplied. Retained RTTI/source-path leads do not establish a precise Torque version, all component presence/absence or full engine recovery. No cadence, rendering, simulation, lifecycle or whole-program conclusion is closed by this checkpoint. The older-client frame-driver question in E#301 remains open.

- [x] ~~Publish the bounded supplied-input bridge and clock checkpoint.~~
- [ ] Keep cadence, wrap/catch-up, callback/collection and lifecycle semantics unvalidated until separately qualified evidence exists.
