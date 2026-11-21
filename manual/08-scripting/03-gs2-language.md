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
| server content, 2002 and 2019 backups of one server | 2002: GS1 only, with no `function onX()`, `join` or `trigger*`. 2019 level NPCs are mixed: 190 files have `function onX()` handlers, 122 still use GS1 `if (created)`, and 100 use both; the 2019 server scripts are full GS2 | [file] (server-notes/hubserver-037-and-delteria-2026-11-18.md#script-dialects) |

## 8.3.2 Delivery

How the server hands GS2 code to a client. NPC bodies travel in 131 behind 100 on 4.20r8, 5.24r4 and 6.03r7; on 6.x a class or weapon arrives as a 197 descriptor and a 140 body, a path 4.20r8 does not honour as sent (→ §8.4.1) [lab] (protocol/script-fuzz-2026-11-19.md); [lab] (protocol/lab-appe-hosta-2026-11-20.md#gs2-class-path-on-420r8-e202-leftover).

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

#### Engine event names by build

The `on…` names each engine image holds are the events it can pass to a script by name: GUI callbacks, engine and network hooks, and platform hooks. They are not the GS1-mask events, which are built at run time from the bare name, and a literal is not proof that the event fires [bin][inf] (client-internals/gs2-engine-event-names.md#what-this-list-is).

| Build | `on…` names | Source |
| --- | ---: | --- |
| 4.04r2 | 76 | [bin] (client-internals/gs2-engine-event-names.md#counts) |
| 4.20r8 | 81 | [bin] (client-internals/gs2-engine-event-names.md#counts) |
| 5.30r3 | 107 | [bin] (client-internals/gs2-engine-event-names.md#counts) |
| 6.00r2 | 111 | [bin] (client-internals/gs2-engine-event-names.md#counts) |
| 6.1.1.3 | 170 | [bin] (client-internals/gs2-engine-event-names.md#counts) |
| Linux 6.03r7 x64 | 106 | [bin] (client-internals/gs2-engine-event-names.md#counts) |
| Android Classic 1.8 | 157 | [bin] (client-internals/gs2-engine-event-names.md#counts) |
| Android Classic 2.2 | 36 (a floor; names probably stored another way) | [bin][inf] (client-internals/gs2-engine-event-names.md#counts) |
| 7.12.43 | 40 (a floor; names probably stored another way) | [bin][inf] (client-internals/gs2-engine-event-names.md#counts) |

| Rule | Builds | Source |
| --- | --- | --- |
| 221 distinct names across the nine builds | all nine | [bin] (client-internals/gs2-engine-event-names.md#counts) |
| 6.1.1.3 adds 55 `onSend…` hooks, one per outgoing message, matching its 55 script-filled send slots; Android 1.8 has 51 of them plus `onSendNPCProperties`; 6.00r2 and Linux 6.03r7 have none | 6.1.1.3; Android 1.8 | [bin] (client-internals/gs2-engine-event-names.md#what-changes-between-builds) |
| 6.1.1.3 adds `onCreated`, `onAllRCChat`, `onReconnect`, `onDisconnected`, `onServerWarp` and `onFileRequests` | 6.1.1.3 and later | [bin] (client-internals/gs2-engine-event-names.md#what-changes-between-builds) |
| `onInitialize`, `onKeyPress`, `onLoad` and `onUnload` exist only in 4.04r2 and 4.20r8; 5.30r3 adds the Flash-style and connection names (`onRollOver`, `onConnect`, `onHandShake`, `onMetaData`) | 4.x; 5.30r3 | [bin] (client-internals/gs2-engine-event-names.md#what-changes-between-builds) |
| Android adds store and platform hooks; 7.12.43 adds Unity-era hooks (`onUpdate`, `onFixedUpdate`, `onLevel3DEnter`, `onDeeplink`) | Android; 7.12.43 | [bin] (client-internals/gs2-engine-event-names.md#what-changes-between-builds) |

Which call site fires each name is unread → App. E#207 [inf] (client-internals/gs2-engine-event-names.md#still-open).

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

#### Linux 6.03r7: the script function table

The Linux 6.03r7 client keeps its engine-provided script functions in one table: each entry holds the name, the return type, an argument signature (`s` string, `i` int, `d` double, `b` bool, `o` object, `X` variable) and the handler, and lookup ignores case. The names are stored lightly obfuscated, one byte per character, so the table was decoded by fitting known names; after about the twelfth character the decode is ambiguous, and a decoded `q` is probably a `2`. [bin] (protocol/named-login-5x-6x.md#how-603r7-stores-its-script-function-names)

| Group | Names (argument signature) | Source |
| --- | --- | --- |
| account | `adventure_setaccountname(s)`, `adventure_setpassword(s)`, `adventure_setnickname(s)`, `getloginaccountname()`, `adventure_geteditnickname()`, `adventure_geteditaccountnames()` | [bin] (protocol/named-login-5x-6x.md#how-603r7-stores-its-script-function-names) |
| connection | `adventure_reconnect()`, `adventure_openserverlist()`, `isofflinemode()` | [bin] (protocol/named-login-5x-6x.md#how-603r7-stores-its-script-function-names) |
| options and window | `adventure_savegraaloptions()`, `adventure_setgraalcontrolrecreate(b)`, `adventure_setfullscreen(b)`, `isfullscreenmode()` | [bin] (protocol/named-login-5x-6x.md#how-603r7-stores-its-script-function-names) |
| chat, input and files | `adventure_setchat(s)`, `adventure_openexternalpm(o)`, `adventure_invokekeyevent(i,i,s,i)`, `adventure_invokemouseevent(i,i,d,d,i,b)`, `adventure_uploadfile(s)` and request calls to delete, rename and move files and folders | [bin] (protocol/named-login-5x-6x.md#how-603r7-stores-its-script-function-names) |
| install | `adventure_getwindowlist()`, `adventure_getinstallationpath()`, `adventure_installgraal(s,b,b)`, `adventure_addmenulink(s,s,s)`, `adventure_adddesktopicon(s,s,s)` | [bin] (protocol/named-login-5x-6x.md#how-603r7-stores-its-script-function-names) |

Only the two account setters were exercised. On 5.24r4 and 6.03r7 a clientside weapon on the `Login` server that calls them in `onCreated` makes the client log in to the next server under the set account, with no delay needed; the server must run clientside scripts as GS2 for this. `getloginaccountname()` still returned `guest` afterwards on 6.03r7. The 3.x form `Adventure.setAccountName(...)` is "not found" on 6.03r7 (→ §2.3.5). [lab] (protocol/named-login-5x-6x.md#524r4-and-603r7)

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

## 8.3.9 What weapon scripts ask of a 4.x to 6.x client

A survey of the client half of real GS2 weapon scripts counts which events, commands and `player` members they use. Only aggregates are published: no script text or world, weapon or class name. Set B is a 2007 world export (554 weapons, 522 with a client part), written for 4.20r8 and 5.00r7; set E is a 2018 playerworld export (854 weapons, 811 with a client part), written for 5.x and 6.x. The bytecode counts come from compiling the client parts with an open compiler, not from official bytecode [lab][inf] (npc-library/gs2-weapon-corpus-2026-11-14.md#the-sets).

| Event | Set E weapons | Set B weapons | What fires it | Source |
| --- | ---: | ---: | --- | --- |
| `onCreated` | 539 | 460 | the script loading | [lab] (npc-library/gs2-weapon-corpus-2026-11-14.md#events) |
| `onWeaponFired` | 445 | 18 | the player using the selected weapon | [lab] (npc-library/gs2-weapon-corpus-2026-11-14.md#events) |
| `onTimeout` | 342 | 264 | a timer running out | [lab] (npc-library/gs2-weapon-corpus-2026-11-14.md#events) |
| `onPlayerEnters` | 208 | 79 | the player arriving in a level | [lab] (npc-library/gs2-weapon-corpus-2026-11-14.md#events) |
| `onPlayerChats` | 200 | 98 | the player's own chat line | [lab] (npc-library/gs2-weapon-corpus-2026-11-14.md#events) |
| `onActionClientSide` | 194 | 58 | the server's 48 with `clientside,<weapon>,…` (→ §2.5); on 6.03r7 the client queues it (up to 100) until a weapon of exactly that name is loaded, then fires `actionclientside` on it | [lab][srv] (npc-library/gs2-weapon-corpus-2026-11-14.md#events); [bin] (client-internals/static-reads-appendix-e-2026-11-20-j.md#how-a-server-trigger-reaches-a-weapon-603r7) |
| `onKeyPressed` | 180 | 41 | a key, with key code and key in `params` | [lab] (npc-library/gs2-weapon-corpus-2026-11-14.md#events) |
| `onMouseDown` | 76 | 14 | a mouse press on the play area | [lab] (npc-library/gs2-weapon-corpus-2026-11-14.md#events) |
| `onPlayerHurt`, `onPlayerDies` | 38, 15 | 0, 0 | the player taking damage or dying | [lab] (npc-library/gs2-weapon-corpus-2026-11-14.md#events) |
| any other `on…` function | 255 | 258 | `scheduleevent`, `trigger` or another script's call | [lab] (npc-library/gs2-weapon-corpus-2026-11-14.md#events) |

The table below gives the commands that eight or more of those weapons call in their client part, by weapon count. "yes" in the GS1 column means the name is in the GS1 command list of 3.04, 4.04r2, 4.20r8 and 5.00r7, and "—" means it is a GS2 name or an expression function. Every name with a set B count above 0 already existed in the mid-2007 clients [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands).

| Command | Set E weapons | Set B weapons | In the GS1 command list | Source |
| --- | ---: | ---: | --- | --- |
| `setTimer` | 323 | 269 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `triggerserver` | 388 | 75 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `setani` | 355 | 83 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `triggeraction` | 102 | 270 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `join` | 8 | 358 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `freezeplayer` | 265 | 60 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `findweapon` | 28 | 224 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `addcontrol` | 140 | 84 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `keydown` | 181 | 26 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `hideimg` | 128 | 53 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `scheduleevent` | 161 | 8 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `findimg` | 101 | 61 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `hideimgs` | 91 | 52 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `replaceani` | 122 | 7 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `showimg` | 91 | 32 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `destroy` | 63 | 38 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `setshootparams` | 67 | 29 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `shoot` | 67 | 25 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `md5` | 1 | 81 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `say2` | 67 | 8 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `keydown2` | 62 | 10 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `onwall2` | 61 | 9 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `enabledefmovement` | 64 | 6 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `disabledefmovement` | 56 | 8 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `changeimgcolors` | 57 | 13 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `changeimgvis` | 57 | 12 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `clearrows`, `addrow`, `setselectedrow` | 50, 51, 38 | 18, 14, 10 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `echo` | 27 | 36 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `enableweapons` | 59 | 3 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `disableweapons` | 52 | 3 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `play` | 59 | 3 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `showtext` | 43 | 14 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `getimgwidth`, `getimgheight` | 33, 32 | 12, 11 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `cancelevents` | 43 | 0 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `showpoly` | 23 | 20 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `changeimgzoom` | 36 | 5 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `changeimgpart` | 23 | 16 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `showani` | 13 | 20 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `setfocus`, `resetfocus` | 26, 29 | 3, 3 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `seticonsize` | 23 | 9 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `keycode`, `getkeycode` | 32, 21 | 0, 8 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `onwall` | 21 | 6 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `findplayer` | 11 | 15 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `testnpc` | 16 | 6 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `seteffect` | 16 | 4 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `serverwarp` | 6 | 14 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `showstats` | 15 | 4 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `lowercase` | 8 | 11 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `onwater`, `onwater2` | 14, 14 | 4, 0 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `getstringkeys` | 2 | 15 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `gettextwidth` | 6 | 11 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `putleaps` | 14 | 1 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `hideplayer` | 15 | 0 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `enablepause`, `disablepause` | 10, 13 | 0, 2 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `changeimgmode` | 13 | 2 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `addlocalmodifier` | 14 | 0 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `disableselectweapons`, `enableselectweapons` | 13, 9 | 1, 0 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `enablefeatures` | 11 | 3 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `isobject` | 12 | 0 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `playlooped`, `play2` | 11, 9 | 0, 0 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `noplayerkilling` | 8 | 3 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `requesttext` | 2 | 9 | — | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |
| `putbomb`, `shootarrow`, `shootfireball`, `shootnuke` | 5, 4, 5, 5 | 0 | yes | [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands) |

Beyond the GUI row methods, the methods these scripts call on objects are `destroy` (151 set E weapons, 82 set B), `show` and `hide` on controls (32, 31), `lower` (21), `isinclass` (18), `drawimage` and `drawimagerectangle` on drawing panels (18, 11), `showtop` (15), `objecttype` (10), `scrolltobottom` (9), `scheduleevent` on an object (9) and `trigger` (7 set E, 15 set B). Set B's 224 `findweapon` calls mostly serve to call another weapon's `public function` [lab][bin] (npc-library/gs2-weapon-corpus-2026-11-14.md#commands).

The rules below summarise what those scripts do, and so what a client has to run first [lab] (npc-library/gs2-weapon-corpus-2026-11-14.md#what-onweaponfired-does-set-e-445-handlers).

| Rule | Source |
| --- | --- |
| The two worlds fire weapons differently: set E uses `onWeaponFired`; set B fires spells from a world key handler that calls a world event on the weapon, so `findweapon` and calls into another weapon's public functions matter more there | [lab] (npc-library/gs2-weapon-corpus-2026-11-14.md#the-sets) |
| A typical fired weapon checks a cooldown or level rule (and says so in `player.chat`), plays an attack gani with the player held for its length, tells the server, and releases on a timer. The commonest calls in the handlers are `setani` (164), `freezeplayer` (98), `triggerserver` (93), `setTimer` (59) and `say2` (45) | [lab] (npc-library/gs2-weapon-corpus-2026-11-14.md#what-onweaponfired-does-set-e-445-handlers) |
| `triggerserver` and `triggeraction(0, 0, "serverside", …)` both end as client 38 with `serverside,<weapon>,<params>`, which GServer-v2 turns into the weapon's `onActionServerSide`; that `triggerserver` sends exactly this is read from scripts and server, not a client | [srv][inf] (npc-library/gs2-weapon-corpus-2026-11-14.md#implementation-order) |
| The `player` members used most in set E are `chat` 413, `y` 327, `x` 325, `level` 287, `dir` 264, `account` 234 and `ani` 136; set B adds `target` and many world-defined members | [lab] (npc-library/gs2-weapon-corpus-2026-11-14.md#player-members-read-or-written) |
| The opcodes these scripts lean on beyond calls and arithmetic are list membership (`in`, 81 and 80), `getangle` (95), list `add` (136), `tokenize` (118) and `getdir` (96); `waitfor` (11) is rare and 4.20r8 on only (→ §8.4.4) | [lab] (npc-library/gs2-weapon-corpus-2026-11-14.md#opcodes-the-repro-machine-still-refuses) |
| All eight GS2-only names checked (`triggerserver`, `scheduleevent`, `findimg`, `findweapon`, `md5`, `cancelevents`, `keydown2`, `onwall2`) are in the January 2007 4.20 engine and in 5.00r7 to 5.30r3. A call to a missing name logs "not found", gives 0 and the script goes on (settled below); 4.04r2 and 4.11 are not read | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#gs2-only-names-in-the-engines-e215); [inf] (npc-library/gs2-weapon-corpus-2026-11-14.md#not-settled) |

**Settled question, formerly E#215: When GS2-only names arrived, and what a missing name does.** Which 4.x build first has each GS2-only name, and what a client does when a script calls a name it lacks, were open. Engine reads and a bytecode run on four builds settled the behaviour [lab] (protocol/lab-appe-hosta-2026-11-20b.md#a-gs2-call-to-a-name-the-client-lacks-e215); [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#gs2-only-names-in-the-engines-e215).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | All eight names are in the January 2007 4.20 engine and in 5.00r7 to 5.30r3; `md5`, `keydown2`, `findimg`, `findweapon` and `onwall2` were called and worked on 4.20r8, 5.12, 5.24r4 and 6.03r7 | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#gs2-only-names-in-the-engines-e215); [lab] (protocol/lab-appe-hosta-2026-11-20b.md#a-gs2-call-to-a-name-the-client-lacks-e215) |
| Settled | A call to a missing name, as a statement, a value or a method, logs one "Function NAME not found …" line and gives 0; the script goes on. Reading a missing attribute gives 0 and logs nothing. The same on 4.20r8, 5.12, 5.24r4 and 6.03r7 | [lab] (protocol/lab-appe-hosta-2026-11-20b.md#a-gs2-call-to-a-name-the-client-lacks-e215) |
| Verdict | Verified for 4.20r8 to 6.03r7; the best guess holds | [lab] (protocol/lab-appe-hosta-2026-11-20b.md#a-gs2-call-to-a-name-the-client-lacks-e215) |
| Left over | Whether 4.04r2 or 4.11 already has the names needs an unpacked engine of those builds, which is not held | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#gs2-only-names-in-the-engines-e215) |


## 8.3.10 Value rules measured by script fuzzing (4.20r8, 5.24r4, 6.03r7)

849 generated GS2 cases on 4.20r8 and 5.24r4 and 603 on 6.03r7 were delivered as bytecode in 131 behind 100 on a loopback lab, each script reporting one computed value through the player's chat. The rules below hold on all three clients unless a row names one; the byte-level results are in → §8.4.11 [lab] (protocol/script-fuzz-2026-11-19.md#gs2-value-rules-that-differ-from-seihais-vm).

| Rule | Detail | Source |
| --- | --- | --- |
| text that is not a number | converts to −1, not 0: `min(1000000000, "q")` is −1, `arctan("a")` −0.785398…, and `format("<%5.2f>", "  pad  ")` `<-1.00>`; `"1e3"` reads as 1000 | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-value-rules-that-differ-from-seihais-vm) |
| the text-to-number order (read in 6.03r7, inferred for the others) | `""` is 0, `"true"` 1 and `"false"` 0; a text starting `0x` is read as hex, any other through `strtod`; a zero result stands only for exactly `"0"` or `"0x0"` (and `"0.0"` on 6.03r7); anything else that reads as zero is −1 | [bin][lab] (protocol/script-fuzz-2026-11-19.md#gs2-which-texts-read-as-1) |
| texts that read as −1 | `"00"`, `" 0"`, `"0 "`, `"+0"`, `"-0"`, `".0"`, `"0."`, `"0e5"`, `"0abc"`, `"abc"`, `"a1"`, `" "`, `"null"` and `"-1"`, and `"0.0"` on 4.20r8 and 5.24r4; `"true"`, `"1"`, `"000001"` and `"1abc"` read as 1 | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-which-texts-read-as-1) |
| what a script notices | `!` of any −1 text is 0, `== 0` false and `== -1` true: `this.mode == 0` is false when it holds a name, and a text flag `"true"` equals 1 | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-which-texts-read-as-1) |
| `tokenize` | `tokenize().size()` of a single value is 1, of `"a,b,c"` 3 | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-value-rules-that-differ-from-seihais-vm) |
| `format` | `%f` and `%5.2f` follow C printf: `<%5.2f>` of 31 is `<31.00>` | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-value-rules-that-differ-from-seihais-vm) |
| `substring` | a text as the length returns the rest of the string | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-value-rules-that-differ-from-seihais-vm) |
| `in` with text members | `("abc" in \|"a,b,c", "1.00000"\|)` is 0 | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-value-rules-that-differ-from-seihais-vm) |
| precision | 5.24r4 computes in single precision: `3.14159265358979` prints 3.141592656, `0.123456789999` 0.123456792, and `getangle` and `arctan` differ in the last digits | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-value-rules-that-differ-from-seihais-vm) |
| integer edges | `(-1 & -2147483649)` gives 2147483647 on 6.03r7; `x >> "a,b,c"` −1 on 6.03r7 and 0 on 5.24r4; `-2147483648 % -1` −2147483647 on 5.24r4 | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-value-rules-that-differ-from-seihais-vm) |
| loop passes | a 10001-pass `while` finishes on 6.03r7 and is stopped on 5.24r4 and 4.20r8; `maxlooplimit` 50 reads back as 100 (clamped from below), after which a 120-pass loop finishes on 6.03r7 and 5.24r4; with `maxlooplimit` 2000000 a 20000-pass loop stops | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-limits) |
| call depth | recursion 9999, 10000 and 10001 deep finishes with the value 0 on all three | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-limits) |
| delivery | 131 behind 100 runs an NPC body with no image or level step needed; GS1 never arrives as bytecode | [lab] (protocol/script-fuzz-2026-11-19.md#method) |

Opcodes 48 and 49 on a build that dispatches them (5.00r7 or 5.12), the value `waitfor` gives when its time runs out, and why one random expression crashes 6.03r7 are open [lab] (protocol/script-fuzz-2026-11-19.md#still-open).

## 8.3.11 Engine event names by build

The table lists every `on…` name the engine images hold as a literal, so a script can be passed that event by name (→ §8.3.4). An `x` means the image holds the literal and `·` means it does not. Holding a name does not show which gameplay site fires it, which is still open (→ App. E#207) [bin] (client-internals/gs2-engine-event-names.md#the-table).

| Event | 4.04r2 | 4.20r8 | 5.30r3 | 6.00r2 | 6.1.1.3 | Linux 6.03r7 | Android 1.8 | Android 2.2 | 7.12.43 | Source |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | --- |
| `onAction` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onAdd` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onAllRCChat` | · | · | · | · | x | · | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onAmazonHistory` | · | · | · | · | · | · | x | x | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onAmazonHistoryDone` | · | · | · | · | · | · | x | x | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onAmazonPurchase` | · | · | · | · | · | · | x | x | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onAmazonUser` | · | · | · | · | · | · | x | x | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onAnimationEnd` | · | · | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onAnimationFinished` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onAnimationStart` | · | · | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onAppActive` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onAppEnterBackground` | · | · | · | · | · | · | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onAppInactive` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onAppLeaveBackground` | · | · | · | · | · | · | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onAppResume` | · | · | · | · | · | · | · | x | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onAssetBundleDownloaded` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onBecomeFirstResponder` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onBind` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onBindFailed` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onCall` | · | · | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onCancel` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onChangeMode3D` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onClassesDownloaded` | · | · | x | x | x | x | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onClassLoaded` | · | · | x | x | x | x | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onClose` | · | · | x | x | x | x | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onCloseQuery` | x | x | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onConnect` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onConnectFailed` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onConnectingToServer` | · | · | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onControlKeyDown` | · | · | · | x | · | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onControlKeyUp` | · | · | · | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onCreated` | · | · | · | · | x | · | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onCursorLineChanged` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onData` | x | x | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onDblClick` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onDeeplink` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onDefaultStyleChanges` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onDeleteKey` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onDeselect` | x | x | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onDeviceBackButton` | · | · | · | · | · | · | x | x | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onDialogPop` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onDialogPush` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onDisconnected` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onDropFiles` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onEnterFrame` | x | x | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onExpand` | x | x | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onExternalStyleChanges` | · | · | · | · | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onFileChunkReceived` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onFileDownloaded` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onFileRequests` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onFilesUploaded` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onFirstResponderChanges` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onFixedUpdate` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onFold` | x | x | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onFolderLog` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onGeneratedThumbnail` | · | · | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onGooglePlayInitialized` | · | · | · | · | · | · | x | x | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onGooglePlayPurchase` | · | · | · | · | · | · | x | x | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onGraal3DConnectionEstablished` | · | x | · | · | · | · | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onHandShake` | · | · | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onHide` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onIconResized` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onInitFrame` | · | · | x | x | x | x | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onInitialize` | x | x | · | · | · | · | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onKeyDown` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onKeyEvent` | · | · | · | · | · | · | · | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onKeyPress` | x | x | · | · | · | · | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onKeyUp` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onLevel3DEnter` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onLevel3DLoaded` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onLevelFileUpdated` | · | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onLoad` | x | x | · | · | · | · | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onLogMessage` | x | x | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onLoseFirstResponder` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onLowMemory` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMapClick` | x | x | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMetaData` | · | · | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMobirooInAppItems` | · | · | · | · | · | · | x | x | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMobirooPurchase` | · | · | · | · | · | · | x | x | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMobirooPurchaseUpdate` | · | · | · | · | · | · | x | x | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMobirooUser` | · | · | · | · | · | · | x | x | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMouseDown` | x | x | x | x | x | x | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMouseDragged` | x | x | x | x | x | x | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMouseEnter` | x | x | x | x | x | x | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMouseLeave` | x | x | · | · | x | x | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMouseMove` | x | x | · | · | · | x | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMouseOverCell` | · | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMouseUp` | x | x | x | x | x | x | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMouseWheelDown` | x | x | x | x | x | x | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMouseWheelUp` | x | x | x | x | x | x | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMouseYawPitch` | x | x | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMove` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onMusicDataReceived` | x | x | x | x | x | · | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onNewClient` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onOpenHelpWindow` | x | x | x | x | · | · | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onOpenLogWindow` | x | x | x | x | · | · | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onOpenMenu` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onOpenOptionsWindow` | x | x | x | x | · | · | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onOpenPlayerList` | · | · | x | x | · | · | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onOpenPlayerPositionWindow` | x | x | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onOpenProfileWindow` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onOpenServerList` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onPackagesDownloadComplete` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onPackagesDownloaded` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onPf` | · | · | x | x | x | · | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onPlayerChanges` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onPlayerLanguageChanges` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onPlayerLogin` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onPlayerLogout` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onPM` | x | x | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onPress` | x | x | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onPushNotification` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onPushNotificationFireBase` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onQuattro3DLoaded` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onRCChat` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onReceiveData` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onReceiveDataPackage` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onReceiveUDPData` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onReconnect` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onReflow` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onRegisterPushNotifications` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onRegisterPushNotificationsFireBase` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onRelease` | x | x | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onReleaseSlider` | x | x | x | x | x | · | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onRemotePlayerChats` | x | x | · | x | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onRemove` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onResize` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onRightMouseDown` | x | x | x | x | x | x | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onRightMouseDragged` | x | x | x | x | x | x | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onRightMouseUp` | x | x | x | x | x | x | x | x | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onRightSelectTag` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onRollOut` | · | · | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onRollOver` | · | · | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onRotationChanged` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onScriptFunctionCall` | · | · | · | · | · | · | x | x | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onScrolled` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSelect` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSelectedFileForUpload` | · | · | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSelectedPath` | x | x | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSelectTag` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendAddBomb` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendAddHorse` | · | · | · | · | x | · | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendBaddyHurt` | · | · | · | · | x | · | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendBaddyProperties` | · | · | · | · | x | · | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendBoardModify` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendBoardModify2` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendCarryThrown` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendDelBomb` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendDeleteNPC` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendDeleteWeapon` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendDelHorse` | · | · | · | · | x | · | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendDownloadFile` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendEnterLevel` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendExplosion` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendExtra` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendFileDeletion` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendFileRename` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendFilesMove` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendFireSpying` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendFlag` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendFolderDeletion` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendHaveWindow` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendImageUpdate` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendImageUpdateCRC` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendIsPKer` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendLevelWarp` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendLevelWarpModtime` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendNPCProperties` | · | · | · | · | · | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendOpenChest` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendPingAnswer` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendPlayerHurt` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendPlayerProperties` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendPreloadLevel` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendPrivateMessage` | · | · | · | · | x | · | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendProjectile` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendRCChat` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendRemoveExtra` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendRequestText` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendSaveFile` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendServerWarp` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendSetText` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendShot` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendTakeExtra` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendToAllChat` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendTriggerAction` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendUnsetFlag` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendUpdatePackage` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendUploadEnd` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendUploadStart` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendWantClassScript` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendWantGaniScript` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendWantImage` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendWantWeaponScript` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendWeaponHit` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendWeaponImage` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSendWindowList` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onServerListerConnect` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onServerLogin` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onServerSetPlayerX` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onServerSetPlayerY` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onServerSetPlayerZ` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onServerWarp` | · | · | · | · | x | · | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onShow` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onSleep` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onStartDrag` | · | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onStartedWithURL` | · | · | · | · | · | · | x | x | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onStopDrag` | · | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onStyleChanges` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onTabComplete` | x | x | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onTextChanged` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onTextEditStart` | · | · | · | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onTFontOptionsProblem` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onToall` | x | x | x | x | x | x | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onTranslationUpdated` | · | · | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onUnload` | x | x | · | · | · | · | · | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onUpdate` | · | · | · | · | · | · | · | · | x | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onUpdatePackageDownloaded` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onURL` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onVideoFinished` | · | · | · | · | · | · | x | x | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onVideoLoaded` | · | · | · | · | · | · | x | x | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
| `onWake` | x | x | x | x | x | x | x | · | · | [bin] (client-internals/gs2-engine-event-names.md#the-table) |
