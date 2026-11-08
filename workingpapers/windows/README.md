# Windows teardown workingpapers

The owner-held collection contains recovered-image analysis, engine and shell
metadata, player dossiers, original REA records, runtime traces and lab harnesses.
Raw code and binary details are not reproduced here.

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

- [ ] Establish a complete controlled scene before treating offline initialization as gameplay.
- [ ] Validate each selected mechanic with before/after state and captured user action.
- [ ] Record harness and fixture digests at capture start for reproducible follow-up.

Sources and digests are in [the source index](../sources.tsv). Existing cleaned
mechanic notes elsewhere in this repository retain their own evidence scope;
this collection does not supersede them.
