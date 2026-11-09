# Turning retained research into usable references and tests

Planning snapshot: 9 November 2026, reviewed main `a997346`. Publication editor,
Linux, macOS, Windows, GitHub publisher and supervisor consultation. This is a
prioritized work plan, not a new client-behavior specification or an execution
report. “Completed handoff” means sanitized findings exist for editorial review;
it does not mean the proposed public change has passed review or CI.

The useful outputs are focused behavior notes, exact-input comparisons,
independently authored test fixtures and a navigable evidence history. Retained
native exports supply research leads and provenance; their acquisition counts
do not measure semantic completeness. New supported PRs may be opened
concurrently. Repair and combined-main validation are performed serially when
main advances. The supervisor retains review and merge authority.

## Published baseline to reuse

The reviewed snapshot includes analysis PRs through #340. Before starting any
item below, fetch main and check both open and merged work for overlap.

- [Linux embedded-input comparisons](../client-internals/linux-cross-version-embedded-controls.md),
  [dispatch observations](../client-internals/linux-cross-version-dispatch.md),
  [receive paths](../protocol/linux-cross-version-receive.md),
  [reader/fusion](../client-internals/linux-420r6-reader-fusion.md),
  [saved-state limits](../client-internals/linux-420r6-selector11.md) and
  [clock/property evidence](../client-internals/linux-420r6-clock-property.md)
  already have their own build scope. Extend their measured contracts rather
  than opening another copy of the same acquisition or correction report.
- [Original Windows 2.05r2 truth/folding](../npc-library/gs1-condition-truth-205r2.md),
  [message selectors](../npc-library/gs1-message-codes-205r2.md),
  [object-member bindings](../npc-library/gs1-object-members-205r2.md),
  [event parameters](../npc-library/gs1-event-parameters-205r2.md) and
  [movement queues](../npc-library/gs1-move-205r2.md) are published. Keep residual
  lifecycle and helper questions separate from those resolved slices.
- [macOS compatibility](../workingpapers/macos/client-compatibility.md),
  [bounded debugger checks](../workingpapers/macos/debugger-validation-2026-11-09.md)
  and [extracted-resource identity](../workingpapers/macos/resource-identity.md)
  are published. Static subsystem and runtime findings require their own review.

## 1. Publish completed handoffs first

Status: completed sanitized intake nominated by researchers or screened by the
publisher; each proposed scope still needs source registration, overlap review,
manual integration and exact-head checks. The source owner prepares its branch;
the GitHub publisher handles PR metadata and readiness. A future experiment is
not a gate on publishing a supported static result.

- [ ] **Linux: network-delivered GS2.** Publish the later class-reader,
  weapon-executor and sleep-continuation observations together with the corrected
  descriptor/body boundary. Preserve authored-proxy versus normal-server
  delivery, reader return versus script result, and measured delay versus
  scheduler guarantees. Connect only the supported increment to E#202/E#207.
- [ ] **Linux: exact-input login profiles.** Publish the seven-unique-input
  local-login matrix with actual version tokens, server source/binary pin and
  independent codec checks. Keep authentication, reconnect, UI, script execution
  and rendered gameplay as separate outcomes.
- [ ] **Linux: original 3.04 GS1 controls.** Publish source-weapon event/readback
  results and predicate distinctions without transferring the Windows 2.05r2
  truth rule or calling Torque/GS2 results GS1 evidence.
- [ ] **Linux: later native deltas.** Split the incremental review into coherent
  revision/architecture comparisons, concrete native-object bridge evidence,
  class/cache contracts and the legacy first-handler stopping point. Subtract
  material already published in #325–332.
- [ ] **Linux: seven-operation Torque contract.** Publish static stack/branch/
  return and signed-formatting results with independently authored expectations.
  Label vectors static-derived until an original-client run supplies an oracle.
- [ ] **Windows: installed 5.00 candidate queue.** Publish bounded delivery,
  deduplication, priority and overrun branches with synthetic queue-state vectors.
  Preserve used/updated/patched installation provenance, named/enum path
  distinctions and unmeasured runtime scheduling.
- [ ] **Windows: 6.03 weapon-cache gate.** Publish the inspected success-output,
  checksum/transform and header-only negative contracts with small authored
  vectors. Keep unpacked analysis input, weapon caller, static derivation and
  missing positive cache execution explicit.
- [ ] **macOS: static subsystem deltas.** Review finalized Carbon startup/input,
  lifecycle/GUI routing, framing, resource and format handoffs as separate
  candidates. Preserve failed queries and exact PowerPC build scope. Entry-level
  debugger success does not complete these runtime contracts.

## 2. Build an evidence-to-question index

Status: proposed derived-data work; start with already published sources.
Extend [the evidence index](../workingpapers/sources.tsv),
[manual source map](../manual/sources.tsv) and
[existing navigator](../tools/navigator/README.md) rather than building a second
unrelated catalog.

- [ ] Add a small machine-readable claim ledger keyed by exact input hash,
  platform/architecture, claim ID, source ID, manual section and open question.
- [ ] Track acquisition/review coverage separately from semantic validation:
  static path, structural parse, entry stop, handler observation, completed
  authored fixture, wire observation and rendered interaction are distinct
  evidence scopes. A stronger-looking scope does not subsume a different claim.
- [ ] Include observation, inference, proposed expectation and unknown as
  explicit statuses. Missing measurements remain unknown; missing a string,
  resource or dispatch case is bounded to its actual scan/path.
- [ ] Record supersedes/qualifies links without replacing historical source
  hashes. Distinguish original carrier, sanitized record and executable hashes;
  a proposed citation alias is not a newly materialized evidence record.
- [ ] Add a focused validator for source resolution, duplicate claim IDs,
  scope/date completeness and explicit supersession. It must not certify an
  unreviewed behavioral claim merely because the schema is valid.

First useful slice: published GS2 delivery/reader/executor/cache claims and
E#202/E#207. Acceptance: a reviewer can follow each row to its exact evidence,
current manual disposition and remaining question, with no raw artifact needed
in the public repository.

## 3. Publish comparisons with explicit unknown cells

Status: proposed synthesis from reviewed source notes; new experiments only
where the evidence is missing.

- [ ] Build a contract matrix by executable identity, platform and architecture:
  delivery routes, container variants, operand handling, internal transforms,
  event delivery, continuation and cache acceptance.
- [ ] Separate identical packaged bytes, identical decoded payloads and
  equivalent observed behavior. Identical scripts do not imply identical native
  layouts or callback ABI. An x86 result does not certify its x64/PPC counterpart.
- [ ] Produce focused API deltas from reviewed script-facing declarations:
  added/removed members and ownership corrections relevant to an actual
  question. Declaration membership alone does not establish binding behavior.
- [ ] Add installation/resource destination maps and duplicate-content summaries
  where they explain bootstrap differences. Mark generated launchers and prepared
  trees separately from original package contents.

Start with one Linux revision pair and one independently supported Windows or
macOS comparison. Do not turn a release label into a cross-platform identity.
Acceptance: each populated comparison cell cites evidence; absence of a result
is visible, and every claimed difference uses comparable tested conditions.

## 4. Turn observations into portable fixtures and diagnostic tools

Status: proposed research tooling. Keep implementation-derived material in this
analysis repository under [the repository handling rules](../AGENTS.md).
Independent implementation projects may link to reviewed notes and use their
own permitted specifications/tests; this plan authorizes no copying across that
boundary.

- [ ] Publish independently authored GS2 descriptor/body boundary vectors and
  bounded framing/stream-state replay checks. Keep transport state, script
  envelope, segment stream and cache carrier as separate layers.
- [ ] Publish small DSO/container serialization fixtures with independently
  specified tables, operands, relocations and expected bytes. Original packaged
  script bodies and assets stay private.
- [ ] Publish static-derived versus original-executed conformance vectors for
  branch stack consumption, signed formatting, queue insertion/overrun and cache
  negative gates. Preserve which oracle supports each expectation.
- [ ] Extend existing decoders with human-readable structure/diagnostic output
  before building a broad disassembler or speculative source decompiler.
- [ ] Add truncation, boundary-length, index and unsupported-operation cases.
  Distinguish a strict validator's rejection policy from observed native
  fallback; round-tripping a valid corpus proves neither malformed-input
  equivalence nor execution semantics.

Acceptance: reproducible authored input bytes/hash, provenance, a reviewed
expected result independent of the implementation under test, bounded resource
use and a clear unsupported/unmeasured outcome. Tests must answer a meaningful
contract question rather than mirror the implementation.

## 5. Direct the next experiments toward decisive contracts

Status: assigned research direction, not completed runs. Researchers should use
the strongest existing isolated positive control, confirm feasibility and report
the first missing prerequisite. Keep VM-intensive work bounded. No new broad
acquisition pass is required to start these experiments.

- [ ] **Linux, first: cache acceptance.** On the working exact 6.03 input,
  establish one independently authored positive cache round-trip, then vary
  valid/wrong/zero expected checksum and header-only/truncated input. Observe
  status, selected body/reader and refresh request separately. If the writer or
  transform prerequisite is unknown, establish it before interpreting negatives.
- [ ] **Linux, next: event identity and suspended replacement.** Identify the
  event behind the working network weapon route; compare original/replacement
  program identities, saved next positions and ordered continuation markers.
  Measure cancellation/replacement rather than inferring it from activation count.
- [ ] **Linux, focused GS1 comparison.** Fresh-state zero/positive/fractional/
  negative values and named-flag collision controls should distinguish numeric
  truth from name parsing and variable storage on original 3.04.
- [ ] **Windows, first: nested event parameters.** Use the strongest runnable
  original-client event control. Record outer-before, inner delivery and
  outer-after parameters, queue versus immediate execution and owner teardown.
  This targets lifetime/reentrancy left by the published producer mapping.
- [ ] **Windows, next: setters and movement.** Test read-before/write/read-after
  plus a real state effect for one member; then one movement option/obstacle in
  a known scene. Keep binding, setter effect, scheduling and collision eligibility
  as separate measured contracts.
- [ ] **macOS, first: a controlled PPC path.** Use the working runtime to obtain
  one known-mode framing success or independently authored loader/reader return.
  Only then vary four-byte grouping/caps or input bounds. Packaged gmap structure,
  actual loader consumption and rendering need separate checks. Report the
  runnable prerequisite before expanding to Lion/v6.

Every run records exact client identity, server source/build if used, authored
fixture identity, before/action/after, observed stopping point, positive control,
capture completeness and owned-process cleanup. All services remain within the
authorized isolated lab. A failed marker alone is not a VM-semantic result.

## 6. Keep evidence durable and old claims findable

Status: proposed curation alongside publication; no deletion instruction.

- [ ] Preserve canonical inputs, original carriers, tool versions and private
  retrieval mappings with integrity checks. A portable sanitized note bundle
  alone is not a reproduction package.
- [ ] Refresh platform indexes and task lists when a later result qualifies an
  older stopping point. Preserve the historical dated observation and link the
  new result rather than rewriting history as though it was measured earlier.
- [ ] Reconcile older broad open-question lists with the exact-build resolutions
  through #340. Keep the remaining builds, helpers and lifecycles open.
- [ ] Add a bootstrap gate ledger: accepted login, reconnect, registration,
  delivery, parse, handler/continuation, visible scene and user interaction.
  A blank screen and a successful script probe can coexist.
- [ ] Record server/compiler crashes and fixes with source pins and reproduction
  cases in their owning project; link reviewed results here. Upstream source
  changes and local runtime verification remain separate facts.

## Immediate coordination

- [x] ~~Audit current publication baseline and request platform-owner priorities.~~
  The supervisor and publisher confirm through #340; researchers are screening
  the remaining sanitized intake against that baseline.
- [x] ~~Assign focused next experiments and distribute writing ownership.~~
  Platform researchers own their new isolated publication branches and report
  feasibility/results; the publication editor owns this shared plan.
- [ ] Open the nominated completed scopes as independent reviewable PRs when
  their branches are prepared. Do not cap concurrent publication.
- [ ] Start the evidence index and a small authored fixture set from reviewed
  material, with explicit owners and independently reviewed acceptance criteria.
- [ ] Update this snapshot as source-owner reviews, experiments and merges
  change the queue; do not treat a proposal as a completed observation.
