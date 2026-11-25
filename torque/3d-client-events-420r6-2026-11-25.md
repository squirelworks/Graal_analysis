# What a client weapon sends in 3D mode: triggerserver, flags, chat and PM (T3D-018, Linux 4.20r6)

Date: 2026-11-25. Static read of the Linux 4.20r6 client, then a loopback lab run of the same client against our own 3D lab server (runs `ev420-a`, `ev420-b`; no movement input). The 2D link was logged packet by packet through the lab's decrypting proxy, and the UDP link was searched for markers at every bit offset. Linux 4.20r6 is 3D-equal to Windows 4.20r8 ([T3D-004](3d-engines-5007-512-and-403-411-2026-11-25.md#t3d-004-linux-and-mac-against-their-windows-twins)). Board row: [T3D-018](3d-capability-board.tsv).

## Static **[bin]**

In this build the 2D and 3D engines share one binary, and the 3D side registers callbacks with the 2D side at start-up.

- **A "queue a line for the 3D server" hook.** The 2D engine calls it with a keyword and a text, and each call becomes a line with a one-letter code: `trigger` → `t`, `object` → `o`, `getclass`/`getgani` → `g`, `getweapon` → `w`, and a flag write → `s`. The callers are the `triggerserver`/triggeraction path (both the weapon/serverside form and an "rc" form), the flag-set path, and the weapon, class and gani requests.
- **A per-frame flush hook**, called at the end of the 2D object tick, joins the queued lines with newlines. It sends them as one BigData text of kind `events` (empty weapon name and option) over the Torque UDP link.
- Server-to-client texts handled by the same code have the kinds `set`, `unset`, `events`, `addweapon`, `weaponscript`, `deleteweapon`, `npcscript`, `classscript`, `ganiscript`, `setmaterials` and `rpg`.
- No chat or PM keyword goes through the hook.

## Lab **[lab]**

A weapon delivered by the server's BigData `addweapon` + `weaponscript` stepped through one call every 3 s, each with its own marker string. Then one chat line was typed.

| Call | Link | What went out |
| --- | --- | --- |
| `triggerserver("weapon","Ev3D",…)` | UDP | an `events` line `t weapon,Ev3D,<params>`, which the server took as a weapon trigger |
| `triggerserver("gui","Ev3D",…)` | UDP | an `events` line `t gui,Ev3D,<params>` (the lab server ignored it) |
| `client.evflag3 = …` | UDP | an `events` line `s client.evflag3=<value>` |
| `player.chat = …` (after the world is up) | UDP | not an events line, but the chat field of the client's own control-object update |
| `player.chat = …` in `onCreated` | – | nothing seen; set before the control object existed [inf] |
| `sendpm(…)`, `player.sendpm(…)`, `setplayerprop("#c",…)` | – | nothing on either link |
| `clientr.… = …` | – | nothing (read-only on the client) |
| a typed chat line | TCP | the normal 2D `PLI_PLAYERPROPS` chat prop (12), not UDP |

- **A 3D weapon must be GS2 bytecode.** The same steps sent as GS1 source text (`ev420-a`) were delivered but never ran. Bytecode compiled by our own compiler (`ev420-b`) ran.
- Right after `weaponscript` arrived, the client sent an `events` line `w Ev3D`, a weapon request. Shortly before, the lab server's 2D side had sent a bare `PLO_NPCWEAPONADD` (33) for the same weapon; why was not traced.
- Over the whole session the 2D link carried only start-up file requests and update checks, a one-byte id 24 every ~0.4 s, id 162 every 30 s (answered by 108), and the typed chat. No script marker went over TCP.

## For server work

In 3D mode a server reads script triggers, flag writes and requests from the BigData `events` text on UDP. It reads script chat from the player's 3D object update and typed chat from the 2D TCP link. Script PMs and `setplayerprop` are dropped by the client and never arrive.
