<!-- manual: kind=reference status=draft -->
# 8.3 GS2 language

GS2 is the script language of the 4.x and later clients. Where it appears and how it is delivered are below. The script machine in GraalEngine 4.2.0.8, GraalEngine 5.0.0.7 and the unpacked 6.00 clients is → §8.3.6. Syntax and the standard library stay open (→ App. E#207). GS1 is in → §8.1.

> Status: draft. The machine in those three engines is in §8.3.6; syntax and the standard library stay open (→ App. E#207).

## 8.3.1 Where GS2 appears

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

## 8.3.3 Names seen in clients and labs

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

## 8.3.4 Tools around GS1 and GS2

| Tool | Relevance | Source |
| --- | --- | --- |
| LevelScriptEditor | lists every NPC of a folder of `.nw` levels and replaces identical scripts in one go; it reads like a tool for porting GS1 scripts to GS2 on a big world | [src][inf] (client-internals/reference-reimplementations/levelscripteditor.md#what-it-is) |

## 8.3.5 A third-party compiler and VM

| Item | Rule | Source |
| --- | --- | --- |
| What it is | a public C# compiler and a public C# VM, both MPL-2.0; a lead for a later clean-room machine | [doc] (npc-library/preagonal-gs2.md#licence) |
| What runs | the compiler takes GS2 source; the engine loads bytecode, and its tests pass the compiler's bytes in | [doc] (npc-library/preagonal-gs2.md#pipeline) |
| Open | → App. E#207 stays open for syntax, the standard library, and the event model. The note records a third-party tree, which is not a reading of the clients | [doc] (npc-library/preagonal-gs2.md#what-this-does-not-settle) [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |

## 8.3.6 What the clients run

The bytecode these clients run is a big-endian four-segment container. Segment lengths are raw 32-bit counts, so they are not GSHORT (→ §2.1.1). The container is not OpenGS1's layout (→ §8.4.3). Packet 140 and packet 197 stay the envelopes in → §8.3.2. The script object parses the segments, not the `0xAC` file wrapper in → §8.3.5. The runner that executes it is → §8.3.7.

| Item | Rule | Source |
| --- | --- | --- |
| segments | types 1–4: event mask, functions, strings, opcodes; markers `F0`–`F6` | [bin] (protocol/gs2-client-vm.md#container-the-client-reads) |
| 4.2.0.8 weapons | `weblevels` `.code` by CRC32; no `GRESCR01`; 195 is a gani | [bin] (protocol/gs2-client-vm.md#how-4208-loads-a-weapon-or-a-class) |
| 5.x and 6.00 | `GRESCR01` cache; the wire header is unchanged from → §8.3.2 | [bin] (protocol/gs2-client-vm.md#script-cache) |
| 6.113 | no container and no opcode switch in the Windows listing. It adds nothing past 6.00's cases 54 and 121 and folds 234–242, and it cannot show whether 48 and 49 returned | [bin] (protocol/gs2-6113.md#what-6113-cannot-show) |
| unpacked 6.1.1.3 | the switch is present and adds no case past that 6.00 set; 48 and 49 stay absent (→ §8.4.4) | [bin] (protocol/gs2-unpacked-6113.md#what-the-dispatcher-adds-past-600) |
| compiler lead | the MPL-2.0 checklist in → §8.3.5, compared with these clients | [doc] (protocol/gs2-client-vm.md#compiler-and-builtins) |

The opcode names, the peephole, and the bytes the client runs which that compiler does not emit stay in the note [bin] (protocol/gs2-client-vm.md#what-differs). The effect of each of those bytes is [bin] (protocol/gs2-client-only-opcodes.md).

## 8.3.7 The script machine in the 4.2, 5.0 and 6.00 engines

GraalEngine 4.2.0.8, GraalEngine 5.0.0.7 and unpacked 6.00r2 and 6.00r4 each contain this runner. The 3.04 Linux client is TorqueScript menus plus native GS1. The container is → §8.3.6. The opcode names, including opcodes 9 and 10, are in `protocol/gs2-client-vm.md`. The fusion numbers and the per-version case list stay in the note. [bin] (client-internals/gs2-vm-from-engines.md#which-binaries-contain-the-machine)

| Item | Rule | Source |
| --- | --- | --- |
| Script object | a `TGraalVar` owns one `TScriptExecutionSpace`. Player, NPC and level are `TServerPlayer`, `TServerNPC` and `TServerLevel`. A class is a `TGraalScript` in a global table, joined onto the runner. A weapon is a named variable given bytecode, with an encrypted `.code` cache | [bin] (client-internals/gs2-vm-from-engines.md#script-objects) |
| Call | the name on top is looked up in this script, then in the other object's script, then in the built-in commands. Too few arguments is `Not enough parameters for`. A miss becomes the number 0. More than 9999 frames already stacked is `Callstack overrun` | [bin] (client-internals/gs2-vm-from-engines.md#how-a-call-finds-a-function) |
| Unqualified name | `temp`, `params`, `this`, `thiso`, `player`, `playero`, `level`, then `client` / `clientr` / `serverr`. Then `with` objects, the active frame, a property of `thiso`, the level, the universe, and `playero`. No leading `$` | [bin] (client-internals/gs2-vm-from-engines.md#how-an-unqualified-name-is-resolved) |
| Events | functions. The runner queues `created`, `initialized` and `istimeout`. A leading `on` is stripped by `waitfor`. `playerenters` is the first name in the `script_event` mask | [bin] (client-internals/gs2-vm-from-engines.md#events) |
| Clock | one double. In 2D, each script pass adds 0.05 once the clock is non-zero. Otherwise it is seconds from the performance counter. Opcode 9 adds 1 and stops with `Loop limit exceeded` when the count is greater than 10000 | [bin] (client-internals/gs2-vm-from-engines.md#timers); [bin] (protocol/gs2-client-vm.md#names-the-client-gives-the-opcodes) |
| Bytecode | segment layout is → §8.3.6. A trailing `0x0A` is not required. Id 131 is a three-byte Graal integer then the bytes. Id 140 stays an envelope (→ §8.3.6) and is not a case of this engine's control dispatch | [bin] (client-internals/gs2-vm-from-engines.md#bytecode-and-source) |
| Stack | tags 0..5. The value stack grows by 100 and the cap is 10000, not 256. Opcode 10 stores that height on the frame and does not jump. Other jumps are the truncated operand plus the current list's base | [bin] (client-internals/gs2-vm-from-engines.md#opcodes); [bin] (protocol/gs2-client-vm.md#names-the-client-gives-the-opcodes) |
| 5.0 and 6.00 | 5.0 adds opcodes 48, 49, 54 and 121 and the same 0.05 clock. 6.00r2 and 6.00r4 add 54, 121 and 234..242; the 0.05 step was not found there | [bin] (client-internals/gs2-vm-from-engines.md#differences-between-the-three-engines) |

## 8.3.9 Linux 4.04r2 sleep continuation

| Condition | Observation | Unmeasured | Source |
| --- | --- | --- | --- |
| Controlled persistent main-menu script requests positive sleep | Saves the next instruction, clears the running position, restores the same snapshot and next instruction, then executes the following statement | Cancellation and replacement while suspended | [cap] (client-internals/linux-404r2-sleep.md#saved-continuation) |
| Sleep versus another queued event | Top-level output does not recur for the continuation, but recurs before the separately queued event | Other object lifecycles | [cap] (client-internals/linux-404r2-sleep.md#saved-continuation) |
| Requested sleep 0.15 seconds | Requested duration is retained across save/restore | Calibrated elapsed delay, clock rate, frame dependence and timeout precision; no exact wall-clock duration established | [cap] (client-internals/linux-404r2-sleep.md#timing-and-capture-limits) |

This is an input-substitution experiment with no server or server commit; later Windows fixed-step clocks are not imported. Remaining scheduler questions → App. E#207. [cap] (client-internals/linux-404r2-sleep.md#timing-and-capture-limits)
