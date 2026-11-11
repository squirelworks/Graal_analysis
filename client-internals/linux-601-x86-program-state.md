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

## Recovery completeness versus semantic coverage

[bin] The retained acquisition record reports 299 selected C exports and host verification, including recovery of two delivery-budget records. Twenty selected native artifacts were reviewed with private evidence bindings and byte-identical local copies. These counts describe selected acquisition and review coverage. In particular, the threaded-executor export did not reconstruct the full indirect handler table, despite complete delivery of that export. Export completion is not complete opcode semantics or original source recovery.

[bin] Before this static increment, the broader dispatch classification and bounded entry/jump observations were recorded. The researcher reviewed retained selected native artifacts; afterward the exact-build preparation and saved-state distinctions above were supported. No new original-client execution, continuation, graphical interaction or runtime acceptance result follows from this review. No client, server, debugger or native provider was started for publication preparation; server and server commit are none.

- [x] ~~Document the selected exact-build decoded-program and saved-state distinctions.~~
- [ ] Establish the unresolved handler meanings, state ownership and lifecycle contracts independently before relying on them.

This note adds no networking details, local-cache acceptance claim or Linux 6.01 x64 equivalence. Appendix E#207 remains partial.

## Evidence provenance

`LNX601-X86-PROGRAM-STATE-HANDOFF` identifies the materialized sanitized incremental handoff; `LNX601-X86-PROGRAM-STATE-IDENTITIES` identifies the approved sanitized identity record. Their document digests are checked during publication preparation and registered in [the source index](../docs/evidence-index.tsv). Underlying native observations remain researcher-supplied, not independently rerun by the editor.

The handoff supplies these original private-carrier keys and digests: `LNX601-X86-REVIEW-FINDINGS`, SHA-256 `3b34e8ea06d90a556bfd621793d9cf82d131397fd82a02d0b6ae99b3d7f68d79`; `LNX601-X86-REVIEW-VERIFICATION`, SHA-256 `4168cbb8bd63ca1d20f69d590d822ae01e2256ac355c24f1c51425bd0f709f13`; and `LNX601-X86-REVIEW-ARTIFACTS`, SHA-256 `f1fb2a8f72e6bda0c3a8bcf7b9b4097000f3e4d73034095457850b3c8da8956b`. These are retained provenance keys, not newly created raw captures or publicly attached native exports. Raw code, addresses, assets and private access details are excluded.
