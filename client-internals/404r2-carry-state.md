# Windows 4.04r2: native pickup and carrying states

Scope: the supplied Windows x86 carrier labelled 4.04r2. The label is not a
compilation-date measurement. This note restates the research owner's sanitized
handoff `W404-HANDOFF-20261109`; the editor verified that handoff's digest.
Underlying static evidence digests are researcher-supplied and were not
independently checked against raw artifacts by the publication editor.

## Board matching

`[bin]` Sources `W404-NATIVE` and `W404-MECHANIC-TABLES` describe an
attack-linked tile-edit path that requires a complete two-by-two pattern.
Its first pattern and replacement also occur in the pickup path. That pickup
category is the category tested by the bush property. This connects the native
bush board-edit and pickup paths; it is not a captured successful sword cut.

## Pickup, carrying and hiding

`[bin]` Source `W404-NATIVE` separates three state relationships:

- Pickup selects a transitional action and initializes a countdown; a later
  update sets the boolean carrying flag.
- The carried category and the boolean carrying property read different state.
  Selecting the bush category therefore does not by itself establish that the
  pickup transition has finished.
- A carrying action checks the bush and two stone categories, or a carried-object
  pointer, before selecting a hiding-related state and hidden animation.

`[bin]` A movement branch for the hiding-related state starts with a smaller
movement magnitude. Release creates a level carry entity and clears the player's
carry fields, subject to animation-dependent conditions. The separate exit helper
has additional conditions that remain untraced; it is not established as a
universal drop or unhide operation. Source: `W404-NATIVE`.

## Timing and input limits

`[bin]` The pickup countdown is initialized to five, but its relationship to
simulation updates, animation frames and elapsed time is unmeasured here.
Neither a five-frame lift nor a 250-millisecond duration follows from that
initial value. Physical key mapping, distance per real-time tick and the
pickup-bound field's meaning were not measured. Source: `W404-NATIVE`.

`[cap]` The Windows startup and offline captures did not verify cutting,
lifting, hiding, throwing, walking or collision. The instrumented offline
transition allocated an adventure object and retained message-loop callbacks;
it did not establish a complete gameplay scene. Sources: `WIN-STARTUP`,
`WIN-OFFLINE` and `WIN-OFFLINE-TRACE`.

The [2.05 carry note](carry-hide-and-glove.md) and
[later Windows lab](../protocol/v5v6-lab-play.md) keep their own timings and
input observations. None is a substitute measurement for this 4.04r2 input.

## Open questions

- [x] ~~Separate pickup action, carried category and carrying flag in the static handoff.~~
  The relationships above establish this distinction.
- [ ] Identify the pickup-bound field before comparing it with older glove formulas.
- [ ] Trace the configured physical key-to-action path.
- [ ] Measure simulation, animation and rendering clocks before converting countdowns to time.
- [ ] Capture a complete scene and before/after state for each selected interaction.
- [ ] Verify the provisional second cut-pattern asset mapping and effect callback
  before publishing a tall-grass identity for this build.

Evidence identities and researcher-supplied digests are in the
[source index](../workingpapers/sources.tsv). No raw artifact or private access
path is included here.
