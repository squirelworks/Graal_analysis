# Linux 4.20 native objects and the Graal scripting bridge

## Exact inputs and scope

[bin] This offline review concerns archive-labelled Linux 4.20r6 x86, executable SHA-256 `a994afd24f5ebdcf73647ffe8b6752274a6c874058cb0db05c525bab060224d0`, with a separate selected 4.20r8 comparison, executable SHA-256 `566cd371464568436265c32976babf2faa95b5fc71cce1f26cbd860b406c2a91`. Their shared wire token and equal recovered embedded payloads do not make their executables or execution-state layouts interchangeable.

[bin] The new contribution is a concrete native-object-to-script registration boundary. Earlier published notes already cover [receive paths](../protocol/linux-cross-version-receive.md), [saved-state selection](linux-420r6-selector11.md), [reader fusion](linux-420r6-reader-fusion.md), [clock/state predicates](linux-420r6-clock-property.md), [dispatch coverage](linux-cross-version-dispatch.md) and [embedded-payload comparisons](linux-cross-version-embedded-controls.md). Those results are dependencies, not new discoveries repeated by this note.

## Concrete native-object bridge

[bin] In the selected 4.20r6 paths, constructor stores and runtime type metadata independently identify concrete SimGroup and GameConnection objects. Conventional instance names alone are not the identification evidence. Each object includes a Graal scripting-variable base subobject.

[bin] The creation callback passes pointers to those base subobjects into static-object registration. The selected registration body exposes duplicate-name handling. This supplies a static connection from concrete Torque-facing native objects to the Graal scripting-variable surface. It does not imply that every native field is exposed, that every registered property is writable or that the older engine's complete console is active.

[bin] A creation dispatcher forwards through a tail call. Consequently an inferred ordinary C prototype is insufficient to establish the callback ABI. An optional fast-path callback slot is still unresolved. Calling-convention or layout assumptions should not be exported from these observations as a runtime contract.

## Separate revision comparison

[bin] The selected 4.20r8 native review corroborates the earlier r6 compiled-input reader and associated state-saving routes, while exposing differences in execution-state layout despite equal recovered embedded inputs. This is a reason to retain revision-specific structures. It is not proof of complete semantic equivalence or evidence that every r6 bridge callback has been independently confirmed in r8.

[inf] For research tooling, keep artifact identity, serialized input, decoded instruction shape and native object/frame layout as separate keys. Payload equality is useful for a controlled comparison; it cannot substitute for matching native structures or observing callback execution.

## Validation and unresolved gates

[bin] Source material is the sanitized incremental handoff listed below. The editor checks its document hash and exact-input identity record; the underlying selected native observations and private-carrier digests remain researcher-supplied. The selected r6 bridge proof and r8 comparison are distinct inputs to that handoff. Counts of exported functions are retrieval coverage, not recovered original source or whole-engine correctness.

[bin] Before this review, object names and separate scripting/native paths did not establish this concrete base-subobject registration boundary. The researcher compared retained constructor/type and registration evidence offline. Afterward the static pointer relationship above was supported, while callback ABI and initializer execution remained open. No client, debugger or server was launched for this publication; server and server commit are none.

- [x] ~~Identify the selected concrete native objects and their scripting-variable registration boundary.~~
- [ ] Observe initializer and callback execution, including the unresolved optional path.
- [ ] Establish callback ABI independently before any reconstruction uses it.
- [ ] Test GUI/input dispatch and an actual 3D session separately.

This note does not demonstrate an active TorqueScript interpreter, a working 3D session, complete GUI startup or Windows-specific Appendix E#503.

## Evidence lineage

`LNX420-BRIDGE-INCREMENTAL-HANDOFF` identifies the owner-held sanitized incremental handoff; `LNX420-BRIDGE-IDENTITIES` identifies its sanitized exact-input record. Document hashes are registered in [the source index](../workingpapers/sources.tsv). Neither key is a newly invented raw-capture alias. Raw native code, addresses, assets and private retrieval locations are excluded.
