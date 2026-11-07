<!-- manual: kind=reference status=draft -->
# 8.3 GS2 language

GS2 is the script language of the 4.x and later clients. The notes record where GS2 appears, how it is delivered and the names of the events and functions seen in clients and labs. They do not document its syntax, standard library or event model; that gap is → App. E#207. GS1 is in → §8.1.

> Status: draft. Complete for what the notes hold; the language itself is open (→ App. E#207).

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
| Open | → App. E#207 stays open. The note records a third-party tree | [doc] (npc-library/preagonal-gs2.md#what-this-does-not-settle) [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |
