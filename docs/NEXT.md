# Next work (ordered)

One change per branch and PR. Verify `origin/main` and the open PR list before
starting; do not stack on unmerged PRs. Skip items that say "Squirrel decides" or
that need missing Squirrel-only files; take the next task. Binding rules live in
`AGENTS.md` and `.cursor/rules/graal-analysis.mdc`.

Done-checks also require: leak check clean, `README.md` contents updated, matching
open-point closed.

macOS CI is paused until the polish stage.

## Tasks

- [x] **Bound the Windows 2.22-labelled verifier variant difference.** ~~Locate the four changed code sites and distinguish them from the earlier control patch.~~ [Static comparison](../formats/windows-222-verifier-variants.md); broader control differences and startup effects remain open there.
- [x] **Fold in the 2026-11-13 research.** ~~Publish the findings that shipped in the Seihai repos as behaviour notes, with manual and App. C/E carries.~~
  - [x] ~~GS2 VM semantics by client version, 3.153 to 6.03r7.~~ [Note](../client-internals/gs2-vm-by-version.md); manual §8.4.9, App. C.8, E#209.
  - [x] ~~Strict GS2 quirk probes.~~ [Note](../npc-library/gs2-strict-probes-2026-11-13.md); manual §8.3.7.
  - [x] ~~GS1 per build: tables, statements, conditions, message codes.~~ [Note](../npc-library/gs1-per-build-2026-11-13.md); manual §8.2.11, App. C.5.
  - [x] ~~Combat, baddy and lava rules, 1.21 to 2.31.~~ [Note](../client-internals/combat-baddy-tile-by-version.md); manual §4.3.3, §4.3.8, App. C.9, E#324.
  - [x] ~~Game rules of the 1999 servers.~~ [Note](../server-notes/gserver-1999-rules.md); manual §5.1.6, E#423.
  - [x] ~~Settle E#301: the 3.x, 4.x and 6.x cadence and GS1 `timeout` rounding.~~ [Note](../client-internals/update-cadence-3x-6x.md); manual §4.1.7, App. C.7.
  - [x] ~~Mac PowerPC 4.04r2 and 5.12 live logins (#399 item 3).~~ [Note](../version-profiles/lab-mac-ppc-404r2-512-2026-11-13.md); manual §1.2.2, §1.8.5, App. C.7.
  - [x] ~~The 5.x HUD no-PK icon and 99/99, and 5.x flag and built-in probes.~~ [Note](../client-internals/gs1-on-5x-hud-and-flags.md); manual §4.6.8.
  - [ ] Run `while (1)`, `##` in the 2.17 engine, and the 2.17 message codes in a populated context on real clients.
  - [ ] Table events, flags, variables and functions per 1.x build.
  - [ ] Run the GS1 `timeout` sweep on 5.x, 6.x and the 1.x/2.x engines; time 6.03r7's script timer. 1.33 to 2.31 and 5.00r7 done ([run](../live-runs/open-issues-2026-11-14/README.md#2a-gs1-timeout-sweep-offline-engines): all round down); 6.x needs a server that compiles GS2.
  - [ ] Read the Mac 4.20r6 and Windows 4.04r2 frame-cipher step rule, and the Mac server-to-client switch for 4.04r2 and 5.12.
  - [ ] Client test harness (#398): run 4.20r8, 5.00r7, 5.12, 6.03r7 and 6.113 on the Windows lab desktop; 1.x to 2.31 are in `live-runs/client-harness-2026-11-13`; 5.00r7 partial (walk, sword) in [the 2026-11-14 run](../live-runs/open-issues-2026-11-14/README.md#5-398-action-list-on-420r86113-partial-500r7-only).
  - [x] ~~Rerun 5.12 Mac against a server whose version table knows the Mac tokens (#399).~~ [Note](../version-profiles/lab-mac-ppc-315-512-flags-2026-11-14.md): tileset sent, level draws; 3.153 and 5.12 send id 18 only for `client.` flags.
  - [x] ~~Settle E#324's static items (1.x packet hits, mode 7, the 2.17.1+ victim test, the respawn AP bands).~~ [Note](../client-internals/combat-baddy-tile-by-version.md#not-known) (#444); the live checks stay open.
  - [ ] Settle E#209 (opcode 54, `waitfor` timeout) and E#423 (1999 server open points).

- [ ] **Builds with no binary (#439).** Catalogue the client hunt and keep the no-binary profiles honest.
  - [x] ~~Catalogue the hunt's finds by token, grade and source.~~ [Token catalogue](../client-internals/version-token-catalogue.md) (#440, #446, #448, #450): 2.1.0.x, 1.40, 1.25, 1.27, 3.0, 3.01, 4.03.4, 4.11, 6.0.0.7 and 6.0.1.5 now have executables.
  - [x] ~~Mark the no-binary profiles as inferred in data, with a CI check.~~ `inferred = true` on 2.1 and 2.12 to 2.16 in [141-217.toml](../client-internals/version-profiles/141-217.toml) (2.3 already had it); [test_inferred.py](../client-internals/version-profiles/test_inferred.py) fails when a list-only (L) token's profile lacks the flag. seihai-core's `Basis::Inferred` rows match.
  - [ ] Still with no executable: 1.391, 2.12 to 2.16, 2.18 to 2.21, 2.3 and 4.02.11. Record the search for copies of the official downloads, including searches that found nothing.
  - [ ] Date each 2.1x feature to a token from `newfeatures200x.txt` and the GServer-v2 version branches.

- [x] **Inference ledger and stale prop cells (2026-11-13).** ~~List the manual's rows that rest on inference alone; correct App. C.1 cells that said "unmeasured" where a note already had the read.~~ [Ledger](../manual/inference-ledger.tsv) (52 rows, checked in CI); C.1 now carries the 1.21–1.32, 4.04r2/4.20r8 and 6.x prop reads.
  - [x] ~~Read the 5.00r7 and 5.12 prop parsers (the one era with no read), and find where 6.x parses the prop strings it stores.~~ [v5-props](../protocol/v5-props.md): 5.00r7, 5.12, 5.30r3 and 5.31r4 share 4.x's parsers plus 82; 6.x still parses natively (6.0.3.7 from the packet switch, 6.1.1.3 through `tclient_set*props`).
  - [ ] What 6.x own-prop 83 sets, and a wire check of the one-byte skip on a 5.x or 6.x client.
  - [ ] Settle or relabel ledger rows, starting with the 2.14–2.16 and 6.00r2/r4/6.015 client-id sets in §2.4.

- [x] **Mac PowerPC start-up and input.** ~~Carry the one-shot engine timer, event registration and the input translator for 4.04r2, 4.20r6 and v5.~~ [Source](../client-internals/mac-ppc-startup-input-2026-11-09.md).
  - [ ] Read the v5 end consumers per event type, the key lookup table and the two post-window start-up helpers; then observe input delivery in a guest.

- [x] **Windows 4.20 render entry points and the 4.04r2 R01 run.** ~~Publish the render-seam check and the instrumented tutorial run.~~ [Render](../client-internals/windows-420-render-seams.md); [R01](../version-profiles/windows-404r2-teardown.md#instrumented-tutorial-run-r01); the core update rate and a rendered scene remain open (App. E#301, E#610).

- [x] **Publish the Android Classic static reading.** ~~Host, frame gate, collision, board, render, chat and the Classic 1.8 GS2 machine.~~ [Host and engine](../client-internals/android-classic.md); [GS2](../protocol/gs2-android-classic-18.md).
  - [x] ~~Decode the opaque Classic 1.8+ GANIs with a known-plaintext round trip.~~ [Resources](../client-internals/android-classic.md#resources): per-file DES, 47/47 round trip; decoder `tools/file-formats/classicgani.py`.
  - [ ] Run the GS2 loop-budget and event-queue boundaries in an Android runtime; read how 2.2 loads its six double-encrypted GANIs.

- [x] **Record what the early Windows clients show when started.** ~~v0, v1 and v2 screenshot review.~~ [Source](../version-profiles/early-windows-screen-review-2026-11.md); scene and mechanic validation remain open (App. E#610).

- [x] **Qualify the supplied 701750 bridge and clock checkpoint.** [Note](../client-internals/v7-701750-bridge-clock.md) and manual §4.1.7 record the bounded static result. The ten retained function-validation records include the short getter; two managed-edge records are counted separately. Cadence, wrap/catch-up, collection/lifecycle semantics and older-build equivalence remain unresolved.

- [x] **Linux 3.04 local value-helper branches.** ~~Publish supported retained local conversion/assignment distinctions after overlap review.~~ [Source](../torque/304-npcs.md#retained-local-numeric-and-string-helper-branches) keeps type-specific behavior and general coercion unresolved.

- [x] **Exact Linux 3.04 show-image wrapper constants.** ~~Resolve the retained eight-wrapper mapping after document-only overlap review.~~ [Source](../torque/304-draw.md#exact-show-image-wrapper-constants-retained-static-review) separates internal constants/container behavior from known command presence and untested rendering.

- [x] **Linux 3.04 native-call evidence boundary.** ~~Review retained callback evidence without redoing native work.~~ [Qualification](../torque/linux-304-seven-operation-contract.md#native-call-evidence-beyond-the-seven-operations) separates static dispatch from unknown argument/results and registry policies.

- [x] **Qualify the imported Windows v4 alias.** ~~Corroborate retained carrier hash and PE resource fields.~~ [Source](../version-profiles/windows-v4-import-provenance.md); official package/release provenance remains unresolved.

- [x] **Correct exact build-614 encoder dispatch counts and selected arithmetic observations.** ~~Separate selector/target/default counts from emitted-property and name claims.~~ [Source](../protocol/v7-graal3d-player-properties.md#3-wire-codec-classic-plprop-still-in-v7-bin); exact IDs 15/16 conversion order/range and runtime remain unvalidated.

- [x] **Linux 6.01 x86 static program/state increment.** ~~Separate decoded preparation and selected saved-state behavior.~~ [Source](../client-internals/linux-601-x86-program-state.md); full handler recovery and lifecycle remain unresolved.

- [x] **Bound the exact Linux 6.03 local-file cache helper.** ~~Carry retained recognition, key/mode and stored-body/status distinctions.~~ [Source](../formats/linux-603-local-cache-helper.md); static-derived cases are not executed native results.

- [x] **Bound the Linux 6.x class-cache path.** ~~Carry the 197 metadata list, the zero-CRC path, the 161 request and the 6.01 x86 delivery split.~~ [Source](../formats/linux-6x-class-cache.md); fixtures, malformed files and execution remain untested.

- [x] **Publish the Windows 5.00r7 request and segment vectors.** ~~Carry the four authored vectors for the 158/161 requests, the mask-only container and the 4.04r2 `client.` flag.~~ [Source](../client-internals/windows-404r2-500r7-static-2026-11-09.md#four-authored-vectors-for-these-boundaries); none was captured or sent.

- [x] **Read the Mac OS X 6.11r1 GS2 runner.** ~~Carry selected handlers, the loop check, snapshot sleep/waitfor and calls.~~ [Source](../client-internals/mac-611r1-gs2-runner.md).
  - [ ] Authenticate the Mac 6.11r1 handler-table extent, read opcode 7 and the arithmetic/comparison handlers, and trace the snapshot queue's clock.

- [x] **Publish the later Linux 3.04 first-handler checkpoint.** ~~Carry same-object/thread and relocation-aware linkage.~~ [Source](../client-internals/linux-304-startup-reader.md#later-relocation-aware-first-handler-checkpoint); completion and original-client vector execution remain unproved.

- [x] **Identify the exact 2.05r2 `#6` association.** ~~Corroborate selected actor carried-NPC image and bounded producer/consumer paths.~~ [Checkpoint](../npc-library/gs1-message-codes-205r2.md#independent-carried-npc-association-checkpoint); full eligibility, selectors, receiver identity, lifetime and runtime remain open.

- [x] **Correct exact build-614 special-length arithmetic.** ~~Carry the retained static erratum.~~ [Note](../protocol/v7-graal3d-framing-and-packet-tables.md#classic-path-mode-0-bin); runtime and extreme-size handling remain unvalidated.

- [x] **Imported Linux provenance.** ~~Review imported documents and separate recovery leads from established behavior.~~ An owner-held note registers document hashes and limits.
  - [ ] Obtain full imported installer/executable identities and intact replacement archives before promoting reported 3.151/5.12 recovery failures into independently verified findings.

- [x] **Document shared Mac v5 animation-group lifecycle.** ~~Publish the bounded static result.~~ [Source](../client-internals/macos-v5-animation-group-lifecycle.md) retains native-runtime limits.
  - [ ] Obtain one naturally reached unchanged-client reader positive control; entry, consumed fields, successful return and rendering remain separate.
- [x] **Publish the rest of the Mac PowerPC broad static pass.** ~~Decompression workspace policy, the four gmap readers with 4.04r2 board dispatch, graphics context setup, transport, machine identity, event names, resource routing and the packaged-resource survey.~~ [Decompression](../protocol/macos-ppc-receive-decompression.md); [gmap readers](../formats/gmap-heights-mac-ppc.md); [runtime surfaces](../client-internals/mac-ppc-runtime-surface-2026-11-09.md).
  - [ ] Run an unchanged Mac client to the context helpers and record the real arguments. Record success and visible output separately.
  - [ ] Validate the `RANDOMSEEDS` row bound, and open the board helper that receives 12 or 13.
  - [ ] Feed valid zlib members to an unchanged receiver near each build's capacity boundary, after a raw-frame positive control.
- [x] **Qualify Mac PowerPC receive stepping.** ~~Publish the bounded static result.~~ [Source](../protocol/macos-ppc-receive-framing.md) retains native-runtime limits.
  - [ ] Obtain one naturally reached unchanged-client reader positive control; entry, consumed fields, successful return and rendering remain separate.
- [x] **Linux 4.20 native-object bridge.** ~~Identify the selected concrete object-to-script registration boundary.~~ [Note](../client-internals/linux-420-native-object-bridge.md).
  - [ ] Observe the bridge initializer/callback and establish its ABI; static registration is not a live 3D session.
- [x] **Linux 3.04 selected Torque contract.** ~~Document the seven-operation static subset.~~ [Contract](../torque/linux-304-seven-operation-contract.md) preserves identity and runtime limits.
  - [ ] Validate independently authored Torque vectors on the exact original input; this note supplies no native execution results.
- [x] **Publish the Linux network/bootstrap evidence ledger.** ~~Convert the sanitized cohort summaries into a versioned coverage reference.~~ [Gate guide and data](../version-profiles/linux-network-bootstrap-evidence.md) preserve exact inputs, source lineage and distinct unknowns.
  - [ ] Extend measured gate coverage only with a qualified positive control and pinned new evidence; do not equate login, header recognition, parsing, execution and gameplay.
- [x] **Bound unpacked Windows 6.03 weapon-cache success.** ~~Publish the retained static increment.~~ [Source](../formats/windows-603-weapon-cache.md) preserves exact-input provenance and static-derived fixture status.
  - [ ] Validate a positive weapon-cache case and other callers in an identified runnable build; header recognition alone is insufficient.
- [x] **Bound installed Windows 5.00 event queue delivery.** ~~Publish the retained static increment.~~ [Source](../client-internals/windows-500-event-queue.md) preserves exact-input provenance and static-derived fixture status.
  - [ ] Validate named/enum gates, non-null argument stringification and runtime queue/service behavior in a positively controlled matching build.
- [x] **Bound Linux 3.04 GS1 source-weapon events and predicates.** ~~Carry the completed bounded research.~~ [Note](../npc-library/linux-304-gs1-runtime.md); remaining gates retain their own open scope.
- [x] **Record seven exact Linux client local-login baselines.** ~~Carry the completed bounded research.~~ [Note](../protocol/linux-local-login-matrix.md); remaining gates retain their own open scope.
- [x] **Observe Linux 6.03 network GS2 execution and continuation.** ~~Carry the completed bounded research.~~ [Note](../protocol/linux-603-network-gs2.md); remaining gates retain their own open scope.
- [x] **Plan further use of the retained platform research.** ~~Audit the publication baseline and assign next directions.~~ [Publication and experiment plan](research-data-publication-plan.md) separates completed intake, proposed derived references and assigned experiments.
  - [ ] Publish the nominated completed platform scopes, then build a claim-to-evidence index and a small independently authored fixture set with reviewed acceptance criteria; keep unknown build/lifecycle cells explicit.

- [x] **Link the exact 2.05r2 #p producer.** ~~Trace dispatch to its shared parameter list.~~ [Source](../npc-library/gs1-event-parameters-205r2.md) corrects callnpc delivery and retains queue/lifetime limits.
  - [ ] Extend event-parameter checks to nested contexts, scheduling, case/escaping, other event/source categories and builds; other E#203 field/format/render gaps remain.
- [x] **Resolve E#204 checked-build name-to-ID mapping.** ~~Replace documentation-order inference.~~ [Source](../npc-library/gs1-object-members-205r2.md) preserves first-match duplicate arrow dx and bounded getter semantics.
  - [ ] Extend object-member research to writes, fallback/scanner behavior, enum meanings, specialized getters and other builds.
- [x] **Catalog the exact 2.05r2 outer message selectors.** ~~Extract outer membership and bounded effects.~~ [Source](../npc-library/gs1-message-codes-205r2.md) separates catalog coverage from runtime/helper semantics.
  - [x] ~~Complete E#203 field identities (#6/#a/#L).~~ [Field identities](../npc-library/gs1-message-codes-205r2.md#field-identities-a-l-e-and-a-positive-carry-control): #a account name, #L recorded level name, positive #6 carry control.
  - [ ] Trace the #E writer; quoted scanners, numeric formatting and downstream rendering remain.
- [x] **Settle E#200 for the checked original 2.05 revision 2.** ~~Resolve the conflicting truth threshold.~~ [Source](../npc-library/gs1-condition-truth-205r2.md) separates zero/nonzero execution, name parsing and constant-comparison folding.
  - [x] ~~Extend condition checks to other builds.~~ [Per-build note](../npc-library/gs1-per-build-2026-11-13.md#conditions-bare-numbers-are-flag-names): bare numbers are false in 1.41r1 to 2.31; constant comparisons are 0 before 2.17.
  - [ ] Nonfinite/malformed values, aliases/precedence and named-flag collisions.

- [x] **Bound Linux 4.20r6 clock updates and advertised 3D-state predicate.** ~~Publish the completed sanitized scope.~~ [Source note](../client-internals/linux-420r6-clock-property.md) retains exact-build limits and remaining measurements.

- [x] **Bound Linux 4.20r6 container operands and post-load fusion.** ~~Publish the completed sanitized scope.~~ [Source note](../client-internals/linux-420r6-reader-fusion.md) retains exact-build limits and remaining measurements.

- [x] **Bound Linux 4.20r6 selector-11 saved-state and registration paths.** ~~Publish the completed sanitized scope.~~ [Source note](../client-internals/linux-420r6-selector11.md) retains exact-build limits and remaining measurements.

- [x] **Compare Linux receive cases and the 4.20r6 compiled-input chain.** ~~Publish the completed sanitized scope.~~ [Source note](../protocol/linux-cross-version-receive.md) retains exact-build limits and remaining measurements.

- [x] **Bound later Linux dispatch ranges and observed cached jumps.** ~~Publish the completed sanitized scope.~~ [Source note](../client-internals/linux-cross-version-dispatch.md) retains exact-build limits and remaining measurements.

- [x] **Compare bounded Linux embedded-script corpora across builds.** ~~Publish the completed sanitized scope.~~ [Source note](../client-internals/linux-cross-version-embedded-controls.md) retains exact-build limits and remaining measurements.

- [x] **Bound Linux packaged Torque streams and resource comparisons.** ~~Publish the completed sanitized scope.~~ [Source note](../formats/linux-torque-resource-scope.md) retains exact-build limits and remaining measurements.

- [x] **Bound Linux 3.04 startup and successful compiled-script reading.** ~~Publish the completed sanitized scope.~~ [Source note](../client-internals/linux-304-startup-reader.md) retains exact-build limits and remaining measurements.

- [x] **Correct the 4.04r2 script-extension absence claim.** ~~Recheck the defined-string export against retained code.~~ [Filter and native mission evidence](../torque/404r2-resource-filter.md) corrects the missing-literal inference; E#502–503 remain partially open for local-reader reachability.

- [x] **Narrow Appendix E#606 height-block placement.** ~~Test the exclusive claim that HEIGHTS belongs only in level files.~~ [Reader and fixture evidence](../formats/gmap-heights-404r2.md) supports named gmap blocks for Windows 4.04r2; rendering, server and packaging claims remain unmeasured.

- [x] **Compare macOS extracted resources.** ~~Extend the executable-only comparison with regular-file content and relative-name checks.~~ [Resource identity revision 1](../version-profiles/macos-resource-identity.md) records matching v3/v5 groups; historical attribution and original-container identity remain unverified.

- [x] **Link a recovered Linux 4.04r2 script to live loading.** ~~Carry the completed sanitized finding into reference documentation.~~ [Source note](../client-internals/linux-404r2-embedded-scripts.md) preserves the exact-build scope and remaining questions.

- [x] **Bound Linux 4.04r2 opcode dispatch and frame evidence.** ~~Carry the completed sanitized finding into reference documentation.~~ [Source note](../client-internals/linux-404r2-vm-dispatch.md) preserves the exact-build scope and remaining questions.

- [x] **Record Linux 4.04r2 sleep continuation preservation.** ~~Carry the completed sanitized finding into reference documentation.~~ [Source note](../client-internals/linux-404r2-sleep.md) preserves the exact-build scope and remaining questions.

- [x] **Record Linux 4.04r2 event ordering and deferred delivery.** ~~Carry the completed sanitized finding into reference documentation.~~ [Source note](../client-internals/linux-404r2-events.md) preserves the exact-build scope and remaining questions.

- [x] **Trace Linux 4.04r2 object-script delivery.** ~~Carry the static message-131 path and receive-switch scope into reference documentation.~~ [Source note](../protocol/linux-404r2-receive-scope.md) preserves network-fixture, lookup, callback and transport limits.

- [x] **Correct Linux 4.04r2 script API declaration ownership.** ~~Carry the completed sanitized finding into reference documentation.~~ [Source note](../client-internals/linux-404r2-api-ownership.md) preserves the exact-build scope and remaining questions.

- [x] **Publish the reviewed 4.04r2 carry-state relationships.** ~~Separate pickup transition, carried category and boolean carrying state.~~ [Static note](../client-internals/404r2-carry-state.md) and §4.5 carry the relationships; timing, keys, glove bounds and scene validation remain open in App. E#611.

- [x] **Carry bounded 4.04r2 initialization into the manual.** ~~Distinguish startup and instrumented offline state changes from gameplay.~~ [§4.8.5](../manual/04-behaviour/08-offline.md#485-windows-404r2-bounded-initialization-evidence) carries the observations; complete-scene validation remains open in App. E#610.

- [x] **Update the macOS preparation handoff.** ~~Record the later bounded PowerPC debugger checks and initial Lion boot test.~~ An owner-held follow-up preserves warnings and pending renderer/gameplay validation; Lion/v6 remains unvalidated.

- [x] **Carry macOS executable compatibility into the manual.** ~~Register the reviewed architecture and minimum-OS inventory as reference evidence.~~ [Compatibility note](../version-profiles/macos-client-compatibility.md) feeds §1.9; archive-label and resource equivalence remain open in App. E#609.

- [x] **Reconcile the 4.04r2 artifact-availability gap.** ~~Link the historical packer-stub note to the later recovered components.~~ [Recovery scope](../torque/v4-404r2-exe.md#later-recovery-does-not-change-this-exports-identity) closes availability only; static claim comparison and a complete 3D session remain open.

- [x] **Completed Linux teardown summary (2026-11-09).** ~~Collect Linux engine recovery in a dedicated retrieval folder.~~ [Linux handoff](../version-profiles/linux-teardown.md) indexes architecture findings, selected function recovery, complete scripting catalogs and bounded runtime evidence. Raw artifacts remain owner-held.

- [x] **Completed Windows teardown summary (2026-11-09).** ~~Refresh the owner-held collection after full component recovery and give Windows its own retrieval folder.~~ [Windows handoff](../version-profiles/windows-404r2-teardown.md) indexes the completed export, editable project, private package and original-carrier 3D provenance; raw material stays outside Git.

- [x] **Retire the public `workingpapers/` folder (2026-11-11).** ~~Move cited findings into topical notes and keep working papers private.~~ Findings moved to `version-profiles/`, `client-internals/` and `protocol/`; the evidence ID list moved to [docs/evidence-index.tsv](evidence-index.tsv); lab-status and handoff notes are owner-held.

- [x] **Platform workingpapers handoff (2026-11-08).** ~~Index the collected platform research and separate macOS teardown material.~~ Its curated findings now live in topical notes (see [Windows](../version-profiles/windows-404r2-teardown.md), [Linux](../version-profiles/linux-teardown.md) and [macOS compatibility](../version-profiles/macos-client-compatibility.md)), with evidence identities and explicit remaining runtime tests. Raw artifacts remain in owner-held project files.

- [x] **Bound arrays.dat membership claims.** ~~Check the disputed list membership and union counts.~~ [Static file note](../formats/arrays-membership-2026-11-09.md) preserves input identity and E#100/E#101/E#608 runtime questions.

- [x] **Correct E#201 stored signatures.** ~~Reconcile four literal GS1 letter sequences.~~ [Exact-input note](../npc-library/gs1-signatures-205-followup.md) corrects the table; runtime argument semantics remain open.

- [x] **Correct E#300 static timer presence.** ~~Reconcile the three missing survey timer cells.~~ [Exact-build note](../client-internals/early-form-timers-2026-11-09.md) records stored configuration; runtime timing remains open.
  - [x] ~~Show the callbacks execute.~~ [Callback execution](../client-internals/early-form-timers-2026-11-09.md#callback-execution): 61, 61 and 60 hits in 3 s.
  - [ ] Measure elapsed cadence without debugger overhead, and runtime timer/idle changes.

- [x] **Resolve E#7 receive-revision discrepancy.** ~~Check the disputed 47/168 revision boundaries.~~ [Exact-input note](../client-internals/receive-dispatch-revision-boundaries-2026-11-09.md) settles static route presence only.

- [x] **Locate the 1st Graal death-counter increment.** ~~Resolve the earlier limited-export gap.~~ [Static counter note](../client-internals/first-graal-death-counter-2026-11-09.md) establishes progression to 30 without a wall-clock duration.

- [x] **Recover the 1st Graal half of E#307.** ~~Read exact step, probe and nudge tables.~~ [Static geometry](../client-internals/first-graal-movement-2026-11-09.md) preserves 1.39 and runtime-state limits.

- [x] **Correct original 2.05r2 FILE framing.** ~~Separate receiver evidence from historical server branches.~~ [Exact-input note](../protocol/file-205r2-prefix-lf.md) keeps persistence and fixture residuals open; server patches remain deferred.
- [x] **Decode bounded E#206 movement options.** ~~Read the exact queued consumer.~~ [Static follow-up](../npc-library/gs1-move-205r2.md) keeps scheduling and collision residuals open.

- [x] **1. Repo rules and task list.** Add `AGENTS.md`, `.cursor/rules/graal-analysis.mdc`,
  and this file. Fix the README opening line to match its Boundary section
  ("no raw decompiles, code or binary addresses").
  *Done in #152.*

- [x] **2. Leak scrub.** One PR per kind: (a) #154 `.pyc`; (b) #153 `FUN_` names;
  (c) #156 IPs/LAN/personal machines; (d) #157 official hostnames; follow-up #158
  loopback dotted literals → plain words / `<loopback>`. Guest password untouched.
  *Done when* the four leak greps in `AGENTS.md` return nothing (third line: review
  hits by eye).

- [x] **3. CI for the checks.** `.github/workflows/checks.yml`: four AGENTS.md leak
  greps (fail on any hit; IP grep has no loopback whitelist), `pytest tools/lab-servers`,
  smoke `resolve.py` + synthetic GR-V1 `grv1-decoder`. Fail-demo branch
  `cursor/ci-leak-checks-fail-demo-b5fd` proved the IP step red.
  *Done in #159.*

- [x] **4. pyReborn study into the repo.** ~~Add as `client-internals/pyreborn-study/`
  with the MIT note; keep `file:line` citations; drop pasted pyReborn code.~~
  [Study](../client-internals/pyreborn-study/README.md), from the public MIT
  `hosler/pyreborn` and its siblings (#244).

- [x] **5. Graal3D collision as plain behaviour (unblocks `seihai-g3d` G3D-1).**
  Per-face step test in `graal3d/collision.md` with tags: radius 5, step height 30,
  slope (ny > 0 / attach > 0.2), wall distances 3 / −5, probe order. Static PE float
  read of `Graal3D.exe` (no decompile on Drive; no C committed). Wine lab still needs
  native `d3drm.dll` for live confirmation.
  *Done in #164.*

- [x] **6. Graal3D camera (unblocks G3D-2).** Follow distance 220, look height +80,
  turn ±5°/tick, pitch −0.15 rad, follow rule **[bin]** (`graal3d/camera.md`, #163).
  Field of view is the Direct3DRM initial field **0.5**: a square window from −0.5
  to 0.5 on the front plane at distance 1, opening `2×atan(0.5)` ≈ 53.13° on either
  axis. No field constant in the client PE **[bin]**; the value is the library
  default **[doc]** (SDK `SetField` / `SetFront` remarks, and Wine's native-matching
  `d3drm` viewport test). The degree figure is arithmetic on that plane **[inf]**.
  Live confirmation of the follow numbers still needs native `d3drm.dll`.
  ~~The far plane stays open.~~ Settled 2026-11-13: the February 2000 exe calls
  `SetBack(5000)` right after `CreateViewport` **[bin]** (`graal3d/camera.md`,
  App. E#500).
  *FOV pinned in `graal3d/camera.md`.*

- [x] **7. NPC-Control protocol note (unblocks `seihai-rc` stage 5).** Write
  `protocol/npc-control.md` from `tools/remotecontrol.md`, Squirrel's `npccontrol`
  material and a loopback NC run against the GServer-v2 lab.
  *Done in #155.*

- [x] **8. `#n` in `setcharprop` (server brief A3.6).** What original servers did with
  `#n` in a `setcharprop` value, from lab evidence (GServer13 1999 under Wine on
  loopback, and the 2.05 client). Add to `npc-library/gs1-reference-205.md` or a short
  `server-notes/` note.
  *Answer in `server-notes/setcharprop-hash-n.md` (#160): value `#n` → action player's
  nick **[srv]**; GServer13 has no `setcharprop` **[bin]**; live GServer-v2+2.05 lab
  still open.*

- [ ] **9. Damage and file-transfer open points (loopback captures).** Partial close
  without new Wine (#165): strike + link for bomb/arrow/baddy powers
  (`damage-sources.md`), CURPOWER + respawn + default-weapon partial
  (`lab-captures-2026-10-25`), GWEBL001/`PLO_LEVELMODTIME`
  (`formats/gwebl001-cache.md`), save folders 1.39/2.00 + empty-stream guard (batch k),
  pre-2.1 settled-name no re-check (batch e `01-request-lists`). Static read of 2.05 rev 2
  and 2.22 (`decomp-findings-2026-10-25-e/04-name-index-case-link.md`): file-index order
  (newer file in 2.22, first hit in 2.05), plain A–Z case fold, and packet 40's link
  (a horse does not change it). **Still open:** full vs empty login default checks
  (the set, and whether they share a frame; the full-folder side is done for 2.22 in
  `live-runs/client-harness-2026-11-13`, the near-empty side is still to run); maps folder
  in 2.1–2.16 (the client archive still has no build between the 2.1 test builds and 2.22).
  Tracked in #245.

- [x] **10. Long handler layouts per build.** PLAYERPROPS (9), OTHERPLPROPS (8),
  NPCPROPS (3) and LEVELLINK (1) for 2.00, 2.04, 2.05 rev 2, 2.17.1, 2.22 and 2.31,
  plus UDP ids 0/15/22 for 2.00–2.04 and gen-3 insertion for 2.01–2.04.
  Tables: `version-profiles/plo-*-layouts.tsv`, `udp-ids-200-204.tsv`,
  `gen3-insertion-200-205.tsv`. Open questions 1, 3, 4 in batch-c `10-…` struck.
  *Done in #162.* (2.04 / 2.01–2.03 `.c` not on Drive; those rows are endpoint +
  batch-c bracketed.)

- [x] **11. 1998 to 1.41 rules (matrix unknown #1).** Death, hurt and knockback, sword
  reach and the wall test for 1.39 first, then 1.32 and ~~1st Graal~~. Decompiles plus Wine
  runs against GServer13 or the 1998 relay on loopback.
  *1.39 done in #161 / `version-profiles/matrix/rules-139.md`. 1st Graal done in
  `version-profiles/matrix/rules-1st-graal.md` (static read of the VCL-lossy export;
  the death-counter increment is not tagged). 1.32 done in
  `version-profiles/matrix/rules-132.md` (static read of a 1.32 export; respawn
  heart value not tagged).* Closes #246.

- [ ] **12. Keep Seihai's fixture reader working.** Any PR that edits
  `version-profiles/*.toml` or `client-internals/version-profiles/*.toml` runs Seihai's
  `tools/gen_profile_fixture.py` against the edited file. Do not commit the generated
  fixture to `seihai` from here.

- [x] **13. A capture of a real 5.x/6.x `Login` session** (matrix unknown #3). Done 2026-11-13
  against a community Login server with the Windows 6.03r7: `protocol/login-session-observed.md`.
  The official server's look (matrix unknown #3) is still open. History of this task:
  On hold. Do not connect. Tracked by GitHub issue #247. The decision stays open.
  `protocol/login-session-known.md` records what a Login server is already known to
  send and which steps are still unobserved. Resume only in this order, the same
  order as #247: (1) the owner comments yes or no on #247; (2) if yes, write the
  capture plan before any connection; (3) redact per `AGENTS.md` and write the note;
  (4) tick this task. Public servers stay off until that written yes is on the issue.
  - [x] Owner-supplied capture, 2026-11-07, port 14900, Windows 6.113.
    The clear hello is `GNP1905C`; the bytes after it are ciphertext, so the
    Login server's packet ids stay unobserved.
    `protocol/v6113-list-capture.md`. The parent item stays open.
  - [x] Full capture, 2026-11-07, 241 s, 46225 frames. UDP ports are
    inventoried in `protocol/v6113-udp.md`. The same clear hello is on
    TCP 14900 and TCP 14882. No UDP is on those remotes, and no UDP
    port is one above a TCP port. The bytes after the hello are still
    ciphertext. The parent item stays open.
  - [x] Full capture, 2026-11-07, 15236 frames. TCP 14900 is present.
    Three completed sessions start with `GNP1905C`; one SYN is unanswered.
    No UDP datagram to those remotes, and no UDP on 14900, 14901 or 14899.
    `protocol/v6113-udp.md`. The parent item stays open.
- [x] **14. Graal Technical Reference Manual: the 15-PR work plan.** Spec: issue #191.
  All fifteen PRs merged; `manual/` is on main with the checker, the carry check and
  the PDF build (Linux and Windows; macOS CI paused since 2026-11-08). TRM 0.0.3 (347 pages) and 0.0.4 (377 pages) are published; 0.0.5 (304 pages, sources footnoted, every table introduced, wide tables on landscape pages, an A3 system map with an A4 print copy and A3 insert) is built and waits for its tag.

- [ ] **15. TRM roadmap to 1.0.0.** The checklist is in issue #191 ("Roadmap to
  1.0.0"): 0.0.5 publishes the current research (built, awaiting its tag), then
  0.0.6 coverage, 0.0.7 implementability, 0.0.8 triage of the unknowns, 0.0.9
  release quality, 1.0.0 sign-off (Squirrel's call). Research toward 1.0.0 is #370. Tick the items in #191 as PRs land.

- [ ] **16. Torque study and the 3.04 plan. Live work, top priority** (Squirrel,
  2026-11-13: there is no Torque hold; the 2026-11-05 "on hold" note was an agent error).
  The study and plan are merged (#242, stage checklist #250):
  `torque/study-torque-clients.md`, `torque/rebuild-plan-3.04.md`. Follow-ups wait in
  #243 (stage 0 reference captures of the real 3.04, the TGE 1.x licence check, Part X).
  The rebuild is graal-client-repro's (squirelworks/graal-client-repro#303).
  - [x] v5 export, static read only (2026-11-07): `torque/launcher-5007.md`,
    `torque/engine-5007.md`, `torque/g3d-5007.md`, the 5.12 / 5.243 / 5.244 stubs,
    unpacked `torque/engine-530r3.md` and `torque/engine-531r4.md`.
  - [x] Component pass of the Linux 3.04 game units (the 2D session, drawing, NPCs and
    script, Graal TCP beside stock Torque, fmod): `torque/304-adventure.md`,
    `torque/304-draw.md`, `torque/304-npcs.md`, `torque/304-net.md`,
    `torque/304-audio-ui.md`.
  - [x] The two exe exports are one packer stub, and a later file-version 4.2.0.8 export includes the launcher, `GraalEngine.dll` and `Graal3DEngine.dll` (`torque/v4-404r2-exe.md`, `torque/v4-420r8-exe.md`, `torque/engine-4208.md`).
  - [x] Read the 3.04 Linux engine (2026-11-07): `torque/engine-304.md`.
    Stock TGE stays in the binary; Graal's game is `GuiGraalCtrl`.
  - [x] Unpacked Windows 6.00r2 and 6.00r4 (static read): no Torque 3D subsystem.
    `GuiGraal3DCtrl` is a GUI type beside `GuiGraalCtrl`. Torque field names and
    `GuiTilesCtrl` are absent from these two images.
    `client-internals/engine-600r2.md`, `client-internals/engine-600r4.md`.
   
  - [x] Read the skipped packed listings (2026-11-07). The two v4 exe
    listings are one Thinstall loader. Packed 5.12 still names its Delphi
    forms. `fmod.dll` is the UPX export list. Packed 6.037 and 6.113 export
    a `QPlay.exe` TLS surface and not Torque.
    `torque/skipped-v4-read.md`, `torque/skipped-v5-read.md`,
    `client-internals/skipped-v6-read.md`.
  - [x] Unpacked Windows 4.2.0.8, static read (2026-11-07). The launcher
    draws by host slots until a 3D start replaces them. `GraalEngine.dll`
    runs the session and has no `SimObject` console. `GameObject` in
    `Graal3DEngine.dll` is a `SceneObject`. `torque/4208-launcher.md`,
    `torque/4208-engine.md`, `torque/4208-g3d.md`.
  - [x] GS2 script machine in GraalEngine 4.2.0.8 and GraalEngine 5.0.0.7
    (2026-11-07), static read. `client-internals/gs2-vm-from-engines.md`. No Seihai crate was started.
  - [x] Cross-version Torque surface (2026-11-07): which modules are
    present, only a name, or absent from 3.04 through unpacked 6.00.
    `client-internals/torque-surface-by-era.md`.
  - [x] Read 5.0.0.7 for behaviour (2026-11-07): the launcher session,
    `TAdventure` and the script space, and the 3D mission, terrain and
    protocol-24 check. `torque/5007-launcher.md`, `torque/5007-engine.md`,
    `torque/5007-g3d.md`. The hold on writing the module stands.
  - [x] Unpacked Windows 6.1.1.3 against the 6.00 notes (2026-11-07).
    No `SimObject` console. `GuiTilesCtrl` is registered.
    `GuiGraal3DCtrl` is not a string; `GraalControl3D` is looked up
    beside `GUIContainer`. Five `new t2d` constructors are file text.
    `client-internals/unpacked-6113.md`.

- [x] **17. v6 own-engine reading.** The 6.x clients are Graal's engine. This pass
  is the June 2011 Windows exports and two packed exes. The packed shells stay
  unreadable, but unpacked images of both builds were read later on 2026-11-07
  (`client-internals/unpacked-6037.md`, `client-internals/unpacked-6113.md`), so
  a readable engine exists for both. Closed by those two notes.
  - [x] Unpacked 6.00r2 and 6.00r4 are `quattro_lib`: OpenGL drawing, a GS2
    shell, `TServer*` world objects and `TSocket`. Packed 6.037 and 6.113
    decompile as packer stubs. `client-internals/engine-600r2.md`,
    `engine-600r4.md`, `packed-6037.md`, `packed-6113.md`.
  - [x] The packed 6.037 and 6.113 listings were read past the stub
    (2026-11-07). The export directory is named `QPlay.exe` and lists
    CyaSSL, zlib and ciphers; the bytes at those exports are not the
    library, and the engine is still not in these two files.
    `client-internals/skipped-v6-read.md`. Item 17 stays open.
  - [x] The GS2 opcode switch in unpacked 6.00r2 and 6.00r4 (2026-11-07),
    same note as the 4.2 and 5.0 engines:
    `client-internals/gs2-vm-from-engines.md`. Item 17 stays open for the
    packed 6.037 and 6.113 executables. No Seihai crate was started.
  - [x] GS2 container, opcodes, and weapon/class load for 4.2.0.8,
    5.0.0.7, and unpacked 6.00r2 and 6.00r4.
    `protocol/gs2-client-vm.md`. Item 17 stays open.
  - [x] Effects of the GS2 opcodes the client VM accepts and the
    Preagonal compiler does not emit, including folds 200–242.
    `protocol/gs2-client-only-opcodes.md`. Item 17 stays open.
  - [x] Windows 6.1.1.3 re-read after the 2026-11-07 gap archive.
    The archive is the existing cleaned notes, not an unpacked image.
    The executable is still the `QPlay.exe` stub: one `KERNEL32` import,
    CyaSSL and zlib export names, no login, no GS2 switch, no Torque class.
    Neighbour diff against unpacked 6.00: `client-internals/engine-6113.md`,
    `protocol/v6113-wire.md`, `protocol/gs2-6113.md`. Issho is not
    implemented. Item 17 stays open.
  - [x] 6.1.1.3's engine is inside a Themida shell and is not in the
    Ghidra export. `client-internals/themida-pack.md`. Item 17 stays open.
  - [x] Read the 6.1.1.3 decompile itself (2026-11-07). The listing is
    106 functions. Three are the entry (clear a breakpoint byte, mix four
    kilobytes, breakpoint). The other 103 are export names whose bodies
    do not implement the CyaSSL or zlib calls, and the file has no GS2
    switch, GUI class or socket import.
    `client-internals/decompile-6113.md`. Item 17 stays open.
  - [x] Unpacked Windows 6.1.1.3 image read (2026-11-07). The upload is a
    Ghidra listing of the 8 August 2014 executable, not a raw exe. The
    `quattro_lib` engine is visible (about 9,300 functions). Packer
    section names and Oreans strings remain.
    `client-internals/unpacked-6113.md`. Item 17 stays open.
  - [x] Unpacked 6.1.1.3 wire and GS2 (2026-11-07). Generation-5 LCG,
    no compiled-in token, `0xFE` send slots, and the 6.00 GS2 switch
    (cases 54 and 121, folds 234–242, no 48 or 49).
    `protocol/unpacked-6113-wire.md`, `protocol/gs2-unpacked-6113.md`.
  - [x] Unpacked Windows 6.037 (static read, 2026-11-07). The listing
    is the `quattro_lib` engine: a code section, `TSocket`, and a GS2
    switch with cases 54, 121 and 200–242 and without 48 or 49.
    `GuiTilesCtrl` is constructed. `GuiGraal3DCtrl` is not a string.
    The packed 6.037 shell is unchanged. `client-internals/unpacked-6037.md`.
    Item 17 stays open.
  - [x] Static read for the 6.x repro checks (2026-11-07). The setprotocol
    header is filled `T`, then `I`, then `E`, then `L`. Ids 93 and 163 on
    the 6.1.1.3 generation-5 path send id 50 first. `onToall` takes a
    player and a text. The bind method's name was not found; the events
    are `onBind` and `onBindFailed`. `protocol/v6-repro-facts.md`.
    Item 17 stays open.
  - [x] Version resources on the skipped packer stubs (2026-11-07):
    `torque/skipped-version-stamps.md`. The two v4 exe uploads are one
    decompile, file version 4.0.4.2. The hold on writing the module stands.
    Manual §10.1.9.

## Handoff (2026-11-07, historical)

The project moved to Cursor on 2026-11-07. Graal_analysis work there continues
from this list and #191 (TRM 0.0.5 is next). Start with graal-delphi's
`HANDOFF-CURSOR.md` (state of both repos, rules, on-hold work, open decisions),
then this file and `AGENTS.md`.
