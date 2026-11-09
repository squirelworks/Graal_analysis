# Linux teardown workingpapers

Curated public summary of a Linux client teardown, collected on 2026-11-09.
Raw research artifacts, private bundles, exact source filenames and retrieval
identifiers are not included. See the [public evidence index](../sources.tsv)
and [handling policy](../handling.md).

For later, separately scoped results, see the [network/bootstrap gate guide](../../version-profiles/linux-network-bootstrap-evidence.md) and its frozen seven-input dataset, and the [3.04 startup/reader study](../../client-internals/linux-304-startup-reader.md). The failures recorded below remain historical observations of their identified unpacked/packed startup attempts; later packed-input reading and network results do not establish unpacked startup success or gameplay.

## Coverage and architecture

`[bin]` Sources `LINUX-TEARDOWN`, `LINUX-CODE`, and `LINUX-VALIDATION` cover eight
archive variants and seven unique unpacked executables: two 3.04 packages,
4.04r2, 4.20r6, 4.20r8, 6.01r1 for both Intel word sizes, and 6.03r7 for the
larger word size. The two 3.04 executables are byte-identical after unpacking.
Archive labels are retained; a command-line banner does not independently
establish those version identities.

`[bin]` Older clients retain Torque console/object/game infrastructure and
Graal-specific session, level, player, animation, connection and script-binding
anchors. A reviewed GUI activation routine directly calls Graal session
initialization (`LINUX-REVIEW`). The engines are embedded in client executables;
grouped recovery output does not establish separate buildable libraries.

`[bin]` Source `LINUX-REVIEW` records a script frame transition that checks depth,
reports overflow, saves prior execution state and installs a new frame. A later
build has a related guarded transition with a different layout. A rendering
candidate dispatches vertex/pixel shader compilation and reports logs. These
are selected reviewed operations, not complete VM or rendering recovery.

`[inf]` Scanned later builds retain Graal-specific identifiers while lacking
the scanned older Torque identifiers (`LINUX-TEARDOWN`). This supports a change
in visible infrastructure; marker absence cannot prove removal of all inherited
code. Native class candidates and published scripting type hierarchies are
separate evidence classes, not interchangeable object layouts.

`[bin]` Sources `LINUX-CODE` and `LINUX-VALIDATION` index the initial 289 selected recovered
function dossiers and full per-build function inventories. Source `LINUX-API`
verifies six complete client-published catalogs containing globals, properties
and functions. The two 6.01 catalogs are byte-identical. Catalog differences
alone do not demonstrate behaviour changes.

## Recorded runtime scope

`[cap]` Sources `LINUX-RUNTIME` and `LINUX-REVIEW` describe prior owner-authorized
isolated Linux VM experiments. Client/version: all eight variants above. Server
and server commit: none. Before: unpacked working copies and compatibility
libraries. Action: bounded launches and actual program-entry debugger stops.
After: all variants reached entry; v4/v6 initialized graphics, while unpacked
3.04 exited early for an unresolved reason. A packed 3.04 comparison had a
separate startup compatibility failure.

`[cap]` A further 4.20r8 experiment stopped in the reviewed script frame transition
during startup and captured stack and state. This confirms that selected routine
executes; it does not recover the whole instruction set or validate gameplay.
The underlying capture filenames and raw debugger records remain private.

`[lab]` Runs used separate writable copies and private network namespaces.
Installer-supplied license directory layout was restored for older runtime
copies; executable checks were not patched. No online login or gameplay was
exercised. Client/debugger processes were explicitly cleaned up. Organizing
this handoff started no client, server, debugger or VM.

## Distribution boundary

This public handoff contains selected findings and their limits, not the raw
code, addresses, debugger records, private filenames, or an artifact retrieval
map. Exact source identities and full artifact manifests remain owner-held.

- [x] Index the completed Linux teardown separately from Windows and macOS.
- [x] Preserve source identities and distinguish static and runtime findings.
- [ ] Resolve the 3.04 early exit in a separately authorized sandbox experiment.
- [ ] Validate gameplay claims with a controlled fixture and recorded server commit.
- [ ] Confirm inferred field meanings and indirect dispatch before relying on them.

Follow [AGENTS.md](../../AGENTS.md): research agents publish reviewed behaviour
notes here. Implementation repositories may link here and must use their own
independent specifications and tests.

## Later exact-build selected review

The [Linux 6.01 x86 program/state note](../../client-internals/linux-601-x86-program-state.md) records a later host-verified pass of 299 selected C exports and 20 reviewed artifacts. Those figures describe a different acquisition/review stage from the initial dossier inventory above. They must not be added as disjoint functions or treated as complete original-source or opcode recovery. Its static findings and unresolved handler/lifecycle gates remain explicitly qualified.

## Imported-document provenance

The [imported Linux notes review](imported-provenance-and-gaps.md) preserves scoped third-party recovery leads and duplicate-document observations; exact document hashes and private source identities remain owner-held. Imported extraction claims and binary identities remain unverified; this is document-provenance context, not new scripting, cache or runtime evidence.
