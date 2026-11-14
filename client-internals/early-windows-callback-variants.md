# Early Windows variants: program-check callback binding

Date: 2026-11-14. Static comparison of owner-held Windows clients; evidence ID
`WIN-CLASSIC-CALLBACK-20261114` ([evidence index](../docs/evidence-index.tsv)).
No original client was executed. Tags: **[bin]** for the observed bindings and
instructions; **[inf]** for conclusions about what remains to investigate.

The [earlier build comparison](graal2002-and-140-builds.md) already establishes
the version fields, tokens, GS1 command counts and receive-dispatch floors for
this group. This note extends its statement that the additional 1.41 rev 1
copies differ in bytes. It does not reclassify them as separate releases.

## The new 1.41 rev 1 result

Two same-version copies have identical resource payloads, import sequences and
non-code sections, but differ at 22 bytes in the code section. Twenty-one
differences are character constants used in string construction. Their eventual
use was not traced here, so those changes do not establish a different login
protocol or the reachability of a changed endpoint. **[bin]**

The remaining difference changes the code pointer in a named Delphi method-table
record. The form resource binds an active program-check component's error event
to that record's method name. Each compared image has a coherent 57-entry method
table: its record lengths, identifier names and executable code mappings were
checked, rather than treating a nearby address as a function entry. **[bin]**

At that event binding, one copy selects the beginning of a handler body. The
other copy and the previously catalogued baseline select the final return of
that same body. Thus resolving the latter binding reaches an immediate return
instead of executing the preceding handler operations. The body bytes are
otherwise shared between these two copies. **[bin]**

The handler calls several helpers, builds text-like values, sets a byte of state
and makes a final direct call before cleanup. One observed direct callee was
read separately: it tests the result of a helper and conditionally calls another
helper, then returns. Those helper effects were not independently identified.
This note therefore does **not** establish a warning dialog, application exit,
the condition that raises the event, or a general program-check bypass. **[bin]**

The default analysis did not recognize the changed sites as belonging to
procedures. The body above was recovered in a separate analysis project from the
validated event entry, with automatic analysis disabled. The one callee was
seeded only after its direct call site was checked. These are analyst-seeded
boundaries, not complete default-analysis coverage; exception-cleanup tails and
inferred decompiler types remain qualifications. No original bytes were changed.
**[bin]**

## Coverage and next question for each compared client

The five entries below distinguish research inputs by established version/token
identity and the new callback observation. They are not claims about which
copy is an unmodified release. Artifact identities remain in owner-held evidence.

### 1.39 comparison client: FileVersion 1.3.9.1, token GNW07080

- [x] Prior coverage: the earlier note establishes the token and 111 GS1 commands.
  The baseline labelled 1.39 has FileVersion 1.3.8.0; the version field alone
  does not settle the behaviour difference.
- [x] This comparison: the import sequence matches that baseline, while code and
  some resource payloads differ. This is not a version-resource-only change.
- [ ] Next: compare matched changed routines, beginning with login construction
  and receive-dispatch destinations. Resolve the earlier note's unfilled
  per-input handler-count entry without presenting its published token or
  command count as new research.

### 1.40 comparison client: FileVersion 1.3.9.1, token GNW23090

- [x] Prior coverage: the earlier note establishes the token, 125 GS1 commands
  and the 45-id receive-dispatch set.
- [x] This comparison: four imports are added relative to the preceding
  comparison client, including registry operations and a keyboard-event API.
  Import presence does not establish how or whether the program uses them.
- [ ] Next: trace the changed call sites and message layouts, separating new
  behaviour from layout and relocation differences.

### 1.40 rev 1: FileVersion 1.4.0.1, token GNW23090

- [x] Prior coverage: token, command count and receive-dispatch floor are already
  documented in the earlier note.
- [x] This comparison: equal file size and matching import sequences do not make
  this client identical to the preceding 1.40 comparison client; code and three
  resource payloads differ.
- [ ] Next: compare matched changed routines and the three resource differences
  to distinguish functional revision changes from presentation changes.

### 1.41 rev 1: binding to the handler body

- [x] Prior coverage: FileVersion 1.4.1.1, token GNW13110, 126 GS1 commands and
  the same published receive-dispatch set as the baseline.
- [x] New result: the program-check error binding selects the validated body
  entry described above.
- [ ] Next: identify the event's triggering conditions and the handler's helper
  effects before attributing an observable response to this copy.

### 1.41 rev 1: binding to the handler's final return

- [x] Prior coverage: the same version, token, command count and dispatch floor
  as the preceding copy are already documented.
- [x] New result: the corresponding binding selects the body's final return,
  as does the catalogued baseline. This identifies a static callback-routing
  difference, not the history or intent of the change.
- [ ] Next: establish the lineage of this binding and compare its event response
  with the body-entry copy only if the static trigger/helper study leaves a
  precise runtime discriminator.

## Limits on implementation

These observations do not justify a new client release profile, a changed
packet layout, or a reproduction-side program-check policy. Keep those questions
open until the relevant changed routine or a controlled exact-build observation
establishes the behaviour. The signed-sword contract in the later Quattro engine
is a separate investigation; no inference from these early variants settles it.
