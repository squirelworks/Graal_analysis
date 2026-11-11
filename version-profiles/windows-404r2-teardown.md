# Windows 4.04r2 teardown summary

The owner-held collection contains recovered-image analysis, engine and shell
metadata, player dossiers, original REA records, runtime traces and lab harnesses.
Raw code and binary details are not reproduced here.

## Completed code-recovery collection

`[bin]` The owner's Windows collection was refreshed on 2026-11-09 after the
Graal 4.04r2 code export completed. Source `WIN-CODE-COVERAGE` records five
analyzed components: the main engine, the original carrier's separate 3D engine,
the client shell, audio library and updater helper. Of 19,724 identified
functions, 19,721 produced decompiler output; three retained assembly-only
coverage after bounded retries. These counts describe identified functions,
not a percentage of original source recovered or a successful rebuild.

Private artifact manifests, editable analysis projects, package names, retrieval
roots, and exact digests remain owner-held. This public note reports the reviewed
scope and limitations without providing a path to the underlying files.

`[cap]` `WIN-3D-PROVENANCE` records a controlled load-only capture of the separate
3D module from the original packed client. Server and server commit were none.
The harness requested the client's existing module-loading operation; the
recorded before/after state changed from no loaded module to a valid loaded
module with a complete mapped-image capture. It did not invoke 3D gameplay
initialization. An adjacent archived engine was not substituted.

`[inf]` The recovered code requires further reconstruction before it can build.
Static code and a loaded module do not establish playable 3D, exact gameplay
mechanics or independent clean-room implementation. Research agents should
publish reviewed plain-behaviour findings here; implementing agents follow
[the handling boundary](../AGENTS.md) and their own specifications and tests.

- [x] ~~Collect the completed Windows code export and provenance in a dedicated folder.~~ Its private custody is tracked outside this public repository.
- [ ] Resolve or document the three remaining decompiler timeouts before claiming complete identified-function C coverage.
- [ ] Validate reconstructed behaviour independently before using it as an implementation requirement.

## Startup capture

`[cap]` Source `WIN-STARTUP` analyzes `WIN-TRACE`, a 51.760-second controlled
startup capture of Graal 4.04r2 containing 1,709 records. Server and server commit
are none; no login or successful server connection was tested.

`[cap]` The capture recorded native game/UI window construction and a successful
DirectDraw initialization call. It recorded opens of copied configuration/cache
files, GUI assets and four supplied animations. These observations establish
that initialization reached those calls. They do not establish that every window
was visible, that a file decoded correctly, or that a gameplay scene rendered.

`[cap]` The trace did not exercise movement, bush interactions, login or level
traversal. An asset being opened does not prove its embedded callback executed.
Recorded event counts are hook observations, not unique filesystem operations.

## Controlled offline transition

`[cap]` Source `WIN-OFFLINE` analyzes `WIN-OFFLINE-TRACE`. The harness deliberately
invoked an internal offline transition at a selected UI-thread execution point;
this was instrumentation, not normal user input or a documented client API.
The recorded before/after state changed from online-mode flag clear with no
adventure object to offline-mode flag set with an allocated adventure object.
Observed message-loop callbacks continued for 20.031 seconds after the call returned.

`[cap]` This does not prove a playable level, correct rendering, player movement,
cutting, lifting, carrying or hiding under bushes. Earlier harness revisions
failed before a successful transition and must not be counted as successful runs.

## Instrumented tutorial run (R01)

`[cap]` Run R01 is a later, separate run from the transition above; the two are not one run counted twice. It ended on 8 November 2026 at 16:41:11 UTC. The client ran in the non-interactive Windows session with instrumentation, not from the menus. Evidence `W404-R01-TUTORIAL-20261108`.

`[cap]` The run recorded the instrumented offline transition, allocated adventure and level state, and a tutorial board loaded from a fixture taken from the Mac distribution. The shell's callbacks kept running: 539 shell ticks with a median interval of about 50.27 ms. No visible game was recorded, and no periodic core update or render hook fired.

`[cap]` So the shell's roughly 50 ms timer kept going while the core neither updated nor drew on a schedule that the hooks could see. The run does not measure the core or player simulation rate, a frame rate, a natural start-up, gameplay under controlled input or 3D. The window and DirectDraw results above belong to the startup capture, not to R01. A static reading of the 4.20 render entry points is in [windows-420-render-seams.md](../client-internals/windows-420-render-seams.md).

- [ ] Establish a complete controlled scene before treating offline initialization as gameplay.
- [ ] Validate each selected mechanic with before/after state and captured user action.
- [ ] Record harness and fixture digests at capture start for reproducible follow-up.

Public evidence categories are listed in [the source index](../docs/evidence-index.tsv).
Exact source identities remain private. Existing cleaned mechanic notes elsewhere
in this repository retain their own evidence scope; this collection does not
supersede them.

- [Imported v4 alias and retained identity](windows-v4-import-provenance.md): separately corroborated resource fields; supplied alias, collection label and official release provenance remain distinct.
