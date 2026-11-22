# Linux 6.01 x86: decoded program and saved-state boundaries

## Exact input and added scope

[bin] The subject is archive-labelled Linux 6.01r1 x86, i386 ELF32, executable SHA-256 `9a2cd037cd3de2ed1dcfc6e9665f5d11854862ef521397f593fa7dd8ffd64a3d`. The retained identity record gives the same digest for original and analysis copies. That record is researcher-supplied; publication preparation checks its document bytes rather than rerunning the executable or authenticating the historical release label.

[bin] The existing [cross-version dispatch note](linux-cross-version-dispatch.md) already records selector classifications, executor-entry stops and a bounded cached jump. This increment adds the selected x86 reader/postpass/preparation sequence and static saved-state distinctions. The separate [4.20r6 reader study](linux-420r6-reader-fusion.md) and [saved-state study](linux-420r6-selector11.md) retain their own inputs; their layouts are not transplanted into this build.

## Decoded records have distinct preparation stages

[bin] The reviewed four-segment reader creates decoded records with initially empty native targets. A later postpass constructs additional fused internal tags and, on one selected path, caches a registry pointer. The executor separately prepares native jump targets and adds a termination record.

[inf] These observations distinguish serialized tags, rewritten tags, a selected registry cache and executor-prepared jump destinations. They do not establish additional source-language operations or a portable representation of native pointers. An internal fused selector must not be treated as a newly observed serialized opcode merely because the executor can dispatch it.

## Saved-state handling is not a uniform deep copy

[bin] The selected saved-state recovery mixes copying, transfer and selective cloning. It forms a deadline from a scripting clock plus positive input. Registration, first-match removal and replacement calls are visible in the selected static paths. The reviewed call-frame layout differs from 4.20.

[bin] This does not establish execution of a trigger or restore, complete subscription lifetime, cancellation order, clock cadence, elapsed delay or a public success value. Selective cloning is not a specification that every referenced object is cloned, and observed transfers do not establish ownership for every unreviewed field. The result supplies neither a complete snapshot layout nor an ABI for another architecture.

## Selected ownership and cache lifecycles (2026-11-22)

[bin] This follow-up reads retained exact-input source and selected instructions directly, rather than only the original sanitized handoff. Additional bounded helper reads use a carrier checked against the same recorded identity above; that check authenticates neither the release label nor runtime behavior. No executable was run. Evidence: LNX601-X86-LIFECYCLE-20261122 in the [source index](../docs/evidence-index.tsv).

[bin] Snapshot creation allocates fresh typed-value holders, but selected string payloads share backing through reference counting and other paths copy pointer words. Only selected references receive temporary marked wrappers; their virtual creation/resolution methods do not establish a universal deep clone. Owner binding is reference-based rather than a copied owner object. Recovered typed-switch labels have selected instruction corroboration, not a new complete dispatch-table proof.

[bin] The collection helper first frees the destination's pointer array, then on its successful allocation path shallow-copies source pointer entries into new destination storage. It does not steal the source array or clone its elements. Frame and temporary callers separately clear source containers; the clear helper frees pointer-array storage without destroying pointees. Restore copies or resolves selected values, reconnects collections and finally destroys the consumed snapshot. This is not an immutable replayable snapshot. Cleanup distinguishes allocated value holders, temporary elements and a context-list container whose elements are not directly destroyed by its selected loop. A selected frame-retention helper returns for null or already-present pointers and otherwise attempts to append the same frame to its receiver's list; membership uses exact pointer equality. Dynamic reference/object lifetimes and allocation success remain unresolved.

[bin] Program reload first destroys prior record strings, frees the contiguous decoded-record array and clears selected program collections, then rebuilds records and postpasses. Embedded registry-reference and native-jump fields therefore disappear with the old array on that selected reload path. Program destructors also use this reset. This does not establish every live-update or joined-program invalidation path.

[bin] Registry-reference rewriting and native execution preparation are distinct: the postpass replaces a name with a registry-record pointer on a selected guarded path; the executor separately checks the first record's native-target sentinel, appends a termination record and fills native jump destinations. The selected cached handler copies the registry pointer into a prepared typed value, advances to the next record and dispatches through its native target. That block does not dereference the registry record, invoke a callback or retain the reference; later value consumers and alternate capacity paths remain unreviewed. A first-record sentinel is not proof that every target is valid, nor does absence of a visible retain establish registry-pointer ownership.

[bin] A third indexed reset clears selected records' numeric payloads under its own flag and traverses joined programs; it does not clear either pointer field. Function entry participates in that flag cycle. Registry replacement/removal, the cached record's complete consumer, all binding/update invalidations, allocation/exception behavior and runtime continuation remain open. These are field-specific static lifecycles, not a portable layout, complete ownership model or cross-architecture ABI.

## Recovery completeness versus semantic coverage

[bin] The retained acquisition record reports 299 selected C exports and host verification, including recovery of two delivery-budget records. Twenty selected native artifacts were reviewed with private evidence bindings and byte-identical local copies. These counts describe selected acquisition and review coverage. In particular, the threaded-executor export did not reconstruct the full indirect handler table, despite complete delivery of that export. Export completion is not complete opcode semantics or original source recovery.

[bin] Before this static increment, the broader dispatch classification and bounded entry/jump observations were recorded. The researcher reviewed retained selected native artifacts; afterward the exact-build preparation and saved-state distinctions above were supported. No new original-client execution, continuation, graphical interaction or runtime acceptance result follows from this review. No client, server, debugger or native provider was started for publication preparation; server and server commit are none.

- [x] ~~Document the selected exact-build decoded-program and saved-state distinctions.~~
- [x] ~~Trace selected exact-input holder/string/container cleanup and distinct decoded-record cache lifecycles.~~ See the dated follow-up.
- [ ] Complete remaining handler, dynamic-reference and registry ownership/lifecycle contracts, allocation behavior and runtime acceptance before relying on them.

This note adds no networking details, local-cache acceptance claim or Linux 6.01 x64 equivalence. Appendix E#207 remains partial.

## Evidence provenance

`LNX601-X86-PROGRAM-STATE-HANDOFF` identifies the materialized sanitized incremental handoff; `LNX601-X86-PROGRAM-STATE-IDENTITIES` identifies the approved sanitized identity record. Their document digests are checked during publication preparation and registered in [the source index](../docs/evidence-index.tsv). Underlying native observations remain researcher-supplied, not independently rerun by the editor.

The handoff supplies these original private-carrier keys and digests: `LNX601-X86-REVIEW-FINDINGS`, SHA-256 `3b34e8ea06d90a556bfd621793d9cf82d131397fd82a02d0b6ae99b3d7f68d79`; `LNX601-X86-REVIEW-VERIFICATION`, SHA-256 `4168cbb8bd63ca1d20f69d590d822ae01e2256ac355c24f1c51425bd0f709f13`; and `LNX601-X86-REVIEW-ARTIFACTS`, SHA-256 `f1fb2a8f72e6bda0c3a8bcf7b9b4097000f3e4d73034095457850b3c8da8956b`. These are retained provenance keys, not newly created raw captures or publicly attached native exports. Raw code, addresses, assets and private access details are excluded.
