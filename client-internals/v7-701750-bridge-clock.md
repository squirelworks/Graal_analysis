# Supplied 701750 input: managed/native bridge and clock checkpoint

## Exact input and verification boundary

[file] This scope concerns the supplied Windows x64 recovered native engine image SHA-256 `a9638a50797fe978746a6ec27caced9effaf540d723609466d29a659ebc1a3e0` and managed GameAssembly analysis image SHA-256 `e724d62e2953c5f6edbf79b1df5364301edf59ab9454aa01bba681573c605349`. The embedded application string 701750 is not independently authenticated release provenance; Unity's engine version is a separate identifier. Original-to-recovered derivation was not independently reproduced by the publisher. These are analysis-image identities, not a claim of original packed-byte identity.

[bin] The researcher reports ten focused Ghidra 12.1.4 functions using explicit original PE exception ranges, plus an independently bounded short leaf where no exception record exists. Every selected Ghidra instruction start matches the independent Capstone decoding, with no missing starts or selected failure markers. Whole-program auto-analysis was disabled. Earlier placeholder extents were superseded by the range-corrected pass. This establishes selected-range agreement, not recovered source-level types, every indirect target or whole-program completeness. The publisher reviewed the sanitized receipt, retained structured validation and input linkage; no executable was rehashed/decoded or target run performed by the publisher.

## Distinct managed update edges

[bin] Managed `UnityMain.Update` calls native `QuattroUpdate`. Managed `UnityMain.FixedUpdate` has a conditional tail jump to its corresponding native bridge. They are distinct static call paths; they do not establish one universal simulation frequency, actual invocation cadence or runtime branch reachability.

## Native clock and guarded event path

[bin] `QuattroUpdate` increments a counter and obtains a clock value through a wrapper whose import slot is `kernel32` `GetTickCount`. The caller stores the returned value as 32 bits. A pseudocode-inferred void wrapper type is not authoritative over that caller register/store flow. Exact cadence, elapsed-time consumption, wrap handling and catch-up policy remain unresolved.

[bin] `QuattroFixedUpdate` checks state guards. On the admitted path it iterates a registered collection and invokes a dispatcher with literal event name `onFixedUpdate` and an empty argument string. The complete semantic identity of that collection and every callback implementation are unresolved. This does not establish full event scheduling, object lifecycle or live event delivery.

## Update3D is a state getter in this input

[bin] The inspected `Update3D` is a small wrapper around a one-byte state getter. Its export name does not establish a scene simulation loop. The [older build-614 bridge inventory](v7-graal3d-unity-bridge.md) retains its own target and evidence scope; shared export names are not whole-function identity or evidence for transferring this result to build 614, v6 or older clients.

## Evidence and remaining questions

No client, DLL entry point, VM or imported script was executed for the source pass. Its initial REA query timed out without a dossier; the completed focused local Ghidra pass used an isolated settings/cache location, 2 GiB heap and two analysis CPUs. Those failure/success stages remain distinct. Generated pseudocode and original native material stay private and are not clean-room implementation source. Server and server commit: none.

Source `W701750-FOCUSED-NATIVE-20261109` identifies the actual sanitized receipt, SHA-256 `bcab277fb582f58b74e30f564b31a1389f736e0324f5c0a26925e304b0336f9c`. Its digest was matched by the publisher; native input identities and observations remain researcher-supplied. Retained RTTI/source-path leads do not establish a precise Torque version, all component presence/absence or full engine recovery. No cadence, rendering, simulation, lifecycle or whole-program conclusion is closed by this checkpoint. The older-client frame-driver question in E#301 remains open.

- [x] ~~Publish the bounded supplied-input bridge and clock checkpoint.~~
- [ ] Keep cadence, wrap/catch-up, callback/collection and lifecycle semantics unvalidated until separately qualified evidence exists.
