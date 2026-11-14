<!-- manual: kind=reference status=draft -->
# 8.3 GS2 language

GS2 is the script language of the 4.x and later clients. This chapter covers where it appears and how the server delivers it (§8.3.1, §8.3.2), the script machine the 4.2, 5.0 and 6.00 engines contain (§8.3.3), how events, waits and the action queue are scheduled (§8.3.4), the names and API the clients publish (§8.3.5), and the tools and third-party compilers around the language (§8.3.6). The compiled container and the opcode dispatch are in → §8.4. GS1 is in → §8.1.

> Status: draft. The machine in those three engines is in §8.3.3; syntax and the standard library stay open (→ App. E#207).

## 8.3.1 Where GS2 appears

GS2 replaces client-side GS1 in steps. Each row gives a group of builds and the scripting they run [doc] (client-internals/feature-timeline.md).

| Builds | Scripting | Source |
| --- | --- | --- |
| 2.3 | classic client-side NPC mode removed; Classic moves to the NPC server | [doc] (client-internals/feature-timeline.md) |
| 2.22, 2.31 | GS1 only | [bin][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| 3.x (`G3D03014`, `G3D28015`) | GS1 natively, with TorqueScript `.dso` files for menus; 3.153 handles the NPC bytecode ids | [bin] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| 4.x (`G3D17026`, `G3D27076`, `G3D20126`) | GS2 bytecode, server-pushed ganis (PLO 195), update packages `GRPKG001` | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| 4.04 rev 2 | still runs GS1 weapon scripts and sends only `client.` string flags (→ §8.1.1) | [live] (client-internals/live-behaviour-404.md) |
| 4.x 3D engine | the Torque console and TorqueScript are gone; every engine object is exposed to Graal's GS2 script objects; there is no TorqueScript compiler and `.dso` files are never requested | [bin] (graal3d/torque-engine-4x.md#overview) |
| 5.x (`G3D22067`, `G3D14097`, `G3D15010`, `G3D26090`) | GS2, with the `GRESCR01` script cache | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| 6.x | GS2; in 6.11 even the packet id tables come from the server's script | [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |

## 8.3.2 Delivery

How the server hands GS2 code to a client. Which message id carries the compiled code is disputed → App. E#202.

| Item | Rule | Source |
| --- | --- | --- |
| NPC script | for v4 and later clients the NPC script prop is replaced by `NPCPROP_CLASS` plus a bytecode message; 2.05 never sees that path | [srv] (protocol/packet-layouts.md); [srv][2.05] (client-internals/feature-specs/02-weapons-combat.md#weapon-lists-server-to-client-srv205) |
| NPC bytecode | `PLO_NPCBYTECODE` (131), `i3 code` then the bytecode; layout and version gate → §8.4.1 | [srv] (protocol/packet-ids.md; protocol/graphics-movement-bytecode.md#on-wire) |
| weapon script | `PLO_NPCWEAPONSCRIPT` (140): `s info_length`, then the script | [srv] (protocol/packet-ids.md) |
| script load | `PLO_LOADSCRIPT` (197): a list `type,name,saveToDisk,desKey,crc32`; type is weapon, npc, class or gani; the key is two `i5` | [srv] (protocol/packet-ids.md) |
| 3D mode | the 3D server, not the TCP game server, delivers the client's GS2 weapons and flags in 3D mode, as text commands `addweapon`, `weaponscript`, `deleteweapon` and `addnpc` (gives a named client-side object its script) | [bin][inf] (graal3d/torque-engine-4x.md); [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |

## 8.3.3 The script machine in the 4.2, 5.0 and 6.00 engines

GraalEngine 4.2.0.8, GraalEngine 5.0.0.7 and unpacked 6.00r2 and 6.00r4 each contain this runner. The 3.04 Linux client is TorqueScript menus plus native GS1. The container is → §8.4.2. The opcode names, including opcodes 9 and 10, are in `protocol/gs2-client-vm.md`. The fusion numbers and the per-version case list stay in the note. [bin] (client-internals/gs2-vm-from-engines.md#which-binaries-contain-the-machine)

| Item | Rule | Source |
| --- | --- | --- |
| Script object | a `TGraalVar` owns one `TScriptExecutionSpace`. Player, NPC and level are `TServerPlayer`, `TServerNPC` and `TServerLevel`. A class is a `TGraalScript` in a global table, joined onto the runner. A weapon is a named variable given bytecode, with an encrypted `.code` cache | [bin] (client-internals/gs2-vm-from-engines.md#script-objects) |
| Call | the name on top is looked up in this script, then in the other object's script, then in the built-in commands. Too few arguments is `Not enough parameters for`. A miss becomes the number 0. More than 9999 frames already stacked is `Callstack overrun` | [bin] (client-internals/gs2-vm-from-engines.md#how-a-call-finds-a-function) |
| Unqualified name | `temp`, `params`, `this`, `thiso`, `player`, `playero`, `level`, then `client` / `clientr` / `serverr`. Then `with` objects, the active frame, a property of `thiso`, the level, the universe, and `playero`. No leading `$` | [bin] (client-internals/gs2-vm-from-engines.md#how-an-unqualified-name-is-resolved) |
| Events | functions. The runner queues `created`, `initialized` and `istimeout`. A leading `on` is stripped by `waitfor`. `playerenters` is the first name in the `script_event` mask | [bin] (client-internals/gs2-vm-from-engines.md#events) |
| Clock | one double. In 2D, each script pass adds 0.05 once the clock is non-zero. Otherwise it is seconds from the performance counter. Opcode 9 adds 1 and stops with `Loop limit exceeded` when the count is greater than 10000 | [bin] (client-internals/gs2-vm-from-engines.md#timers); [bin] (protocol/gs2-client-vm.md#names-the-client-gives-the-opcodes) |
| Bytecode | segment layout is → §8.4.2. A trailing `0x0A` is not required. Id 131 is a three-byte Graal integer then the bytes. Id 140 stays an envelope (→ §8.4.2) and is not a case of this engine's control dispatch | [bin] (client-internals/gs2-vm-from-engines.md#bytecode-and-source) |
| Stack | tags 0..5. The value stack grows by 100 and the cap is 10000, not 256. Opcode 10 stores that height on the frame and does not jump. Other jumps are the truncated operand plus the current list's base | [bin] (client-internals/gs2-vm-from-engines.md#opcodes); [bin] (protocol/gs2-client-vm.md#names-the-client-gives-the-opcodes) |
| 5.0 and 6.00 | 5.0 adds opcodes 48, 49, 54 and 121 and the same 0.05 clock. 6.00r2 and 6.00r4 add 54, 121 and 234..242; the 0.05 step was not found there | [bin] (client-internals/gs2-vm-from-engines.md#differences-between-the-three-engines) |

#### Android Classic 1.8

The Android Classic 1.8 x86 engine reads the same four-segment container, decoded into 20-byte records with 165 dispatcher cases. Its rules were read statically for this one build and are not assumed for the Windows engines. [bin] (protocol/gs2-android-classic-18.md#the-container)

[bin] The machine advances the index before dispatch, and an opcode without a handler continues without a pop. Two conditional branches always pop; the short-circuit pair keeps the value when it jumps. The loop budget is 10,000 per generation, and the call stack refuses a frame at 10,000, but the value stack has no 10,000 cap here. [bin] (protocol/gs2-android-classic-18.md#control-flow-and-the-stack)

[bin] Division and remainder by zero give 0, and remainder uses floor. Numbers compare equal within 0.0001. Inside the machine any non-zero number is true, but a boolean passed to a native call uses `floor(v + 0.0001)`, so 0.5 is true in the machine and false for a native call. Strings compare without case; substring and search count bytes. Arrays read 0 out of bounds, do not grow on write, and clamp to 0 to 10,000. [bin] (protocol/gs2-android-classic-18.md#numbers-and-truth); [bin] (protocol/gs2-android-classic-18.md#strings); [bin] (protocol/gs2-android-classic-18.md#arrays)

[bin] The event queue refuses at 1,000 and drops `onAllRCChat` silently at the limit; `istimeout`, `created` and `initialized` go to the front. Scheduled events refuse negative delays and lowercase the name. Joining a class appends it once, raises its count and installs its event catchers. 173 native bindings are registered, 172 with recovered names. [bin] (protocol/gs2-android-classic-18.md#events-time-and-classes); [bin] (protocol/gs2-android-classic-18.md#native-bindings)

## 8.3.4 Events, waits and the event queue

The runner in §8.3.3 treats events as functions. How a queued event, a `sleep` and a pending wait are scheduled has been observed or read build by build; each reading below holds for its own build and input, and none is an all-version rule (→ App. E#207). [bin] (client-internals/gs2-vm-from-engines.md#events)

#### Linux 4.04r2: event ordering

Event order was tested on Linux 4.04r2 with instrumented scripts. Each row gives one condition, what was seen and the limit of that test [cap] (client-internals/linux-404r2-events.md#observed-dispatch-sequence).

| Tested condition | Observation | Limit | Source |
| --- | --- | --- | --- |
| Instrumented profile-script fixture | Top-level statements run before the creation handler and again before the queued handler; a second control reproduces the order | Two tested event dispatches in one lifecycle, not an all-version rule | [cap] (client-internals/linux-404r2-events.md#observed-dispatch-sequence) |
| Handler queues another event | Its following statement runs before the queued handler | Delivery is deferred in this experiment; other event sources remain unmeasured | [cap] (client-internals/linux-404r2-events.md#observed-dispatch-sequence) |
| Trigger arity control | Event name alone is rejected; an additional value permits delivery | This fixture's call only, not a universal variadic signature | [cap] (client-internals/linux-404r2-events.md#observed-dispatch-sequence) |

The fixture replaces process input, not the executable file or its signature checks. Server and server commit are none. Joined classes, public calls and complete event semantics remain open → App. E#207. [cap] (client-internals/linux-404r2-events.md#experiment-boundary)

#### Linux 4.04r2: sleep continuation

`sleep` was tested the same way. Each row gives a condition, what happened and what was not measured [cap] (client-internals/linux-404r2-sleep.md#saved-continuation).

| Condition | Observation | Unmeasured | Source |
| --- | --- | --- | --- |
| Controlled persistent main-menu script requests positive sleep | Saves the next instruction, clears the running position, restores the same snapshot and next instruction, then executes the following statement | Cancellation and replacement while suspended | [cap] (client-internals/linux-404r2-sleep.md#saved-continuation) |
| Sleep versus another queued event | Top-level output does not recur for the continuation, but recurs before the separately queued event | Other object lifecycles | [cap] (client-internals/linux-404r2-sleep.md#saved-continuation) |
| Requested sleep 0.15 seconds | Requested duration is retained across save/restore | Calibrated elapsed delay, clock rate, frame dependence and timeout precision; no exact wall-clock duration established | [cap] (client-internals/linux-404r2-sleep.md#timing-and-capture-limits) |

This is an input-substitution experiment with no server or server commit; later Windows fixed-step clocks are not imported. Remaining scheduler questions → App. E#207. [cap] (client-internals/linux-404r2-sleep.md#timing-and-capture-limits)

#### Linux 4.20r6: selector 11, saved state and registration

[bin] Selector 11 is a handler in examined 4.20/6.x builds, unlike the 4.04 skip path; the detailed result is r6-only. It consumes one numeric and two string-like values. Saving requires a nonempty name, ordered positive numeric input and contexts; zero does not enter this path as an indefinite wait. Registration precedes caller lowercase/leading-`on` removal. Empty/current-owner, distinguished global and named routes do not establish full comparison or subscription rules. [bin] (client-internals/linux-420r6-selector11.md)


[bin] State saving transfers the next instruction, clears active execution, copies typed values and transfers/reconstructs collections. Insertion normalizes the key; an empty requested target permits comparison against the current owner's name as a conditional, asymmetric matching fallback. Canonical rewriting of stored or query targets is not established. Only the first matching pending record is removed; insertion destroys it and appends the new record. It does not establish uniqueness, complete cancellation or delivery order. Capacity grows by 100 up to 10,000; the requested single slot and alternate numeric branch values are not event/timeout success semantics. The stock corpus has no selector-11 input or public-prefix directory entry. No new runtime experiment/server ran; coercion, resume and lifecycle semantics remain open in E#207. [bin] (client-internals/linux-420r6-selector11.md)

#### Windows 5.00: event delivery and the action queue

[bin] In the exact backup engine from a used, updated and patched install labelled 5.00r7, delivery and execution are separate. The named route can create an execution space; the enum route needs one and an event-interest check. Both retain additional unresolved gates. Accepted actions are queued and their owner activated; script service separately checks gates/universe, updated classes and scheduled events before execution. This is not a TorqueScript loader finding. [bin] (client-internals/windows-500-event-queue.md)

[bin] Both inspected receivers reject when the existing queue has 1,000 actions, before duplicate suppression. The named route suppresses matching route/name with null arguments; above nine pending entries its additional non-null comparison uses argument string representations, not pointer equality. Internal names istimeout, created and initialized prepend; other names append. The enum route appends. These internal names are not a proven public event mapping. Activation avoids duplicate owners and has an unresolved special front-insertion category; per-pass markers and list mutation handling do not establish fairness or reentrancy. [bin] (client-internals/windows-500-event-queue.md)

[inf] Independently authored queue contracts cover null-argument duplicates, lifecycle insertion and overrun-before-dedup, with a synthetic recording executor only. They are static-derived, not original-client output. Allocation failure, argument conversion/collisions, class-download deferral, complete virtual gates, cross-owner ordering and actual scheduler cadence remain open. Do not import this input's limit into another build or infer 20 Hz service. Broader event semantics remain partial in App. E#207. [inf] (client-internals/windows-500-event-queue.md)

## 8.3.5 Names and the published API

#### Names seen in clients and labs

These GS2 names appear in the notes; each row gives only what the source says about it:

| Name | Kind | What the source says | Source |
| --- | --- | --- | --- |
| `sendtext` | function | a message of four strings `(weapon, type, option, data)`; the 3D plug-in's text messages have this shape | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |
| `receivetext` | event | a weapon named in such a message receives it | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |
| `onRCChat` | event | receives messages of type `rc` | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll; graal3d/torque-engine-4x.md) |
| `onRPGMessage(data)` | event | receives the `rpg` command | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll; graal3d/torque-engine-4x.md) |
| `action<name>` | event | a `t` line in an `events` message triggers it on a weapon or GUI (`weapon`, `gui`) or an NPC (`npc`) | [bin] (graal3d/torque-engine-4x.md) |
| `trigger`, `getweapon` | client events | the client batches them per connection as `t …` and `w …` lines (others as `s …`) in one `events` message | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |
| `onConnectionAccepted`, `onConnectRequestTimedOut`, `onConnectRequestRejected`, `onConnectionDropped`, `onConnectionError` | events on the universe | fired for each 3D connection outcome | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |
| `onGraal3DLoginStep` | event | reports the three Torque mission-load phases, with the datablock and ghost events | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |
| `getDatablockProperties(obj, list)` | function | lists datablock fields (name, type and attributes) for GS2 scripts | [bin] (graal3d/torque-engine-4x.md; protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |
| `addtiledef("pics1.png", "", 0)` | function | called from a GS2 weapon `-System` on a 5.x/6.x lab server; the full level drew after the warp with or without that weapon | [shot] (protocol/v5v6-lab-play.md#the-login-server-mode) |

#### Linux 4.04r2: published API membership

Linux 4.04r2 publishes a catalogue of script types and globals. The table gives what the exact input shows and where that stops [test] (client-internals/linux-404r2-api-ownership.md#declaration-ownership-correction).

| Catalog fact | Exact-input result | Limit | Source |
| --- | --- | --- | --- |
| Correct declaration grouping | 176 published types and 332 globals; 38 declarations belong to the root script object rather than globals | Total declaration count unchanged; this corrects derived metadata, not runtime behavior | [test] (client-internals/linux-404r2-api-ownership.md#declaration-ownership-correction) |
| Evidence class | Client-published scripting surface | Binding effects, conversions, inherited behavior and native C++ layout are not established by declaration membership | [test] (client-internals/linux-404r2-api-ownership.md#what-membership-does-not-establish) |

Other catalog builds require their own correction records; these counts are not generalized. Standard-library semantics remain open → App. E#207. [test] (client-internals/linux-404r2-api-ownership.md#declaration-ownership-correction)

## 8.3.6 Tools, compilers and reimplementations

#### Tools around GS1 and GS2

One tool from the period works on GS1 and GS2 levels. The row says what it does and why it matters [src][inf] (client-internals/reference-reimplementations/levelscripteditor.md#what-it-is).

| Tool | Relevance | Source |
| --- | --- | --- |
| LevelScriptEditor | lists every NPC of a folder of `.nw` levels and replaces identical scripts in one go; it reads like a tool for porting GS1 scripts to GS2 on a big world | [src][inf] (client-internals/reference-reimplementations/levelscripteditor.md#what-it-is) |

#### A third-party compiler and VM

A modern third-party compiler and VM exist for GS2. The rules below say what they are, what runs, and what they leave open [doc] (npc-library/preagonal-gs2.md#licence).

| Item | Rule | Source |
| --- | --- | --- |
| What it is | a public C# compiler and a public C# VM, both MPL-2.0; a lead for a later clean-room machine | [doc] (npc-library/preagonal-gs2.md#licence) |
| What runs | the compiler takes GS2 source; the engine loads bytecode, and its tests pass the compiler's bytes in | [doc] (npc-library/preagonal-gs2.md#pipeline) |
| Open | → App. E#207 stays open for syntax, the standard library, and the event model. The note records a third-party tree, which is not a reading of the clients | [doc] (npc-library/preagonal-gs2.md#what-this-does-not-settle) [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |

## 8.3.7 Loose spellings the compilers accept

34 authored one-quirk probes, each with a clean twin, were compiled as black boxes by the two public GS2 compilers. A quirk is tolerated when both accept it with the clean twin's bytes [test] (npc-library/gs2-strict-probes-2026-11-13.md).

| Item | Rule | Source |
| --- | --- | --- |
| tolerated, same bytes | a brace-less function body, a call of a call's result, `elseif`, a stray `;` or empty statement, a function with no body, `<>`/`=<`/`=>`/`:=`, an unterminated `/*` at the end of the file | [test] (npc-library/gs2-strict-probes-2026-11-13.md#tolerated-both-accept-same-bytes-as-the-clean-spelling) |
| accepted, other bytes | assignment in a condition, a bare expression, a declaration before the body, a duplicate function, a bare GS1 command, a run-time name assignment, a string parameter name | [test] (npc-library/gs2-strict-probes-2026-11-13.md#accepted-with-different-bytes) |
| rejected by both | comma statements, text enums, `global enum`, GS1 commands with comma arguments, nested comments, a function inside a block, missing semicolons, a bare `/word`, an unclosed block | [test] (npc-library/gs2-strict-probes-2026-11-13.md#rejected-by-both) |
| split | a GS1 message code and a GS1 range: Preagonal rejects, gs2-parser accepts | [test] (npc-library/gs2-strict-probes-2026-11-13.md#split) |
| GS1 inside a GS2 file | compiled as GS2 it loses its GS1 meaning; on 5.x that changes the HUD (→ §4.6.8) | [lab] (client-internals/gs1-on-5x-hud-and-flags.md#the-hud-difference-on-5x) |

## 8.3.8 Show-images, the particle emitter, `indexof` and `format`

Static reads of the Windows 4.20r8 GraalEngine.dll (4.2.0.8) and the Linux 6.03 x64 client; nothing was executed. Most rows come from 6.03, the clearer read [bin] (client-internals/showimg-particles-and-gs2-format.md#show-images-the-particle-emitter-and-gs2-indexof-and-format).

#### `GuiShowImgCtrl`

| Rule | Source |
| --- | --- |
| A `GuiShowImgCtrl` owns one `TShowImg` and has no picture code of its own; it places it at the control's screen position plus (`offsetx`, `offsety`), moving it (and an attached emitter) only when that position changes, and draws it before its child controls | [bin] (client-internals/showimg-particles-and-gs2-format.md#guishowimgctrl-and-tshowimg) |
| The 6.03 control adds `red`, `green`, `blue`, `alpha`, `mode`, `style` and `rotation` to the show-image's properties; for one show-image kind a mouse hit counts only where the picture is hit | [bin][inf] (client-internals/showimg-particles-and-gs2-format.md#guishowimgctrl-and-tshowimg) |
| An ani show-image takes head, body, sword, shield and `attr[]` from the owner while `playerlook` is true (the default); false takes them from `showimg.actor.*` | [doc] (client-internals/showimg-particles-and-gs2-format.md#guishowimgctrl-and-tshowimg) |
| `mode` blends 0 add, 1 transparent, 2 subtract, 3 day-night; a particle with default colour and mode 0 or 1 leaves the blend state alone | [doc][bin] (client-internals/showimg-particles-and-gs2-format.md#guishowimgctrl-and-tshowimg) |

#### The particle emitter (`TParticleEmitter`)

| Rule | Source |
| --- | --- |
| Properties (same names in 4.2.0.8 and 6.03): `attachposition`, `autorotation`, `checkbelowterrain`, `clippingbox`, `cliptoscreen`, `continueafterdestroy`, `currentparticlecount`, `delaymin`, `delaymax`, `dropemitter`, `dropwateremitter`, `emissionoffset`, `emitatterrainheight`, `emitautomatically`, `emittedparticles`, `firstinfront`, `isfrozen`, `maxparticles`, `movementfactor`, `nrofparticles`, `particle`, `particletypes`, `wraptoclippingbox`; methods `addglobalmodifier`, `addlocalmodifier`, `addemitmodifier`, `advancetime`, `emitat`, `removemodifiers`, `removeparticles` | [bin] (client-internals/showimg-particles-and-gs2-format.md#properties) |
| With `emitautomatically`, bursts come every delay drawn uniformly from [`delaymin`, `delaymax`] seconds; the first tick only starts the timer; a burst emits `min(nrofparticles, maxparticles − currentparticlecount)`, each particle copying a random template from `particletypes` | [bin][inf] (client-internals/showimg-particles-and-gs2-format.md#properties) |
| `emissionoffset` is added to each new particle's position, scaled by the emitter's movement scale and rotated by its turn angle; the same scale multiplies `movex`/`movey`/`movez` and the `add` modifier on `x`, `y`, `z`; that scale is probably `movementfactor` | [bin][inf] (client-internals/showimg-particles-and-gs2-format.md#properties) |
| A particle leaving the clipping box (or the screen) is removed, or with wrap moved back by whole box widths; `checkbelowterrain` lifts or removes particles under the terrain; `isfrozen` stops movement and emission | [bin][doc] (client-internals/showimg-particles-and-gs2-format.md#properties) |
| Modifier fields, index 0 to 17: `x, y, z, movex, movey, movez, angle, zangle, speed, rotation, spin, stretchx, stretchy, red, green, blue, alpha, zoom`; `lifetime` is in seconds, angles in radians, rotation += spin × dt, colours 0 to 1; `sound` plays at emission, one picked at random | [bin][doc][inf] (client-internals/showimg-particles-and-gs2-format.md#particle-fields) |
| `addXmodifier(type, time1, time2, field, operation, min, max)` has signature `sffssff`; type `once`, `impulse` or `range`; operation `replace`, `add` or `multiply`; unknown types are refused and a list caps at 1000 | [bin] (client-internals/showimg-particles-and-gs2-format.md#modifiers) |
| `once` fires once at a time drawn from [`time1`, `time2`]; `impulse` fires at such a time and again after each new draw; `range` applies every frame while the age is in [`time1`, `time2`], `replace` interpolating min→max (then max), `add` as a per-second rate, `multiply` doing nothing, and only its first non-multiply entry applying | [bin] (client-internals/showimg-particles-and-gs2-format.md#modifiers) |
| `addlocalmodifier` runs a clock per particle from its emission; `addglobalmodifier` one emitter clock that changes every live particle when it fires; `addemitmodifier` the emitter clock, changing the templates and so later particles | [bin] (client-internals/showimg-particles-and-gs2-format.md#modifiers) |
| New particles go to the front of the list; with `firstinfront` false (default) the newest draw on top, with true the oldest; sub-emitters draw before the emitter's own particles | [bin] (client-internals/showimg-particles-and-gs2-format.md#draw-order) |

#### Opcodes 82 (`indexof`) and 84 (`format`)

| Rule | Source |
| --- | --- |
| 82: stack `…, list, value` → `…, index`; `list` is used as an object as is; an empty or non-object list gives −1; a number matches by float equality, a string by string equality, an object by identity, any other type gives −1; at least two slots are required | [bin] (client-internals/showimg-particles-and-gs2-format.md#gs2-opcode-82-indexof) |
| 84: stack `…, marker, argN, …, arg1, fmt` → `…, result` in the marker's slot; no marker empties the stack; a marker on top gives the empty string | [bin] (client-internals/showimg-particles-and-gs2-format.md#gs2-opcode-84-format) |
| The formatter is Graal's own: flags `+`, `-`, `#`; width and `.precision` each capped at 120; positional `n$`, after which arguments continue from that point; one `l` accepted and ignored | [bin] (client-internals/showimg-particles-and-gs2-format.md#gs2-opcode-84-format) |
| Conversions `%%`, `%d`/`%i` (precision zero-pads, width space-pads), `%u`, `%x`/`%X`, `%c`, `%f`, `%s` (precision truncates); any other letter prints nothing | [bin] (client-internals/showimg-particles-and-gs2-format.md#gs2-opcode-84-format) |
| Missing arguments: `%s` prints empty (still padded), `%d`/`%i`/`%u` print `0`, `%f` likely 0; a positional past the end counts as missing; extra arguments are ignored | [bin][inf] (client-internals/showimg-particles-and-gs2-format.md#gs2-opcode-84-format) |
| Open: whether `removemodifiers` clears the emit list, when a global clock starts, the particle kinds (image, ani, text), `indexof` case handling and `%d` rounding → App. E#210 | [inf] (client-internals/showimg-particles-and-gs2-format.md#not-settled) |
