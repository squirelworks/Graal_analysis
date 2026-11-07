# PLO_NPCACTION (26): replace an NPC's script

What the client does with server-to-client id 26 (`PLO_NPCACTION` in gs2lib's names), read from the receive switch of every pre-2.04 build that handles it, and confirmed with a real 2.00 client in a loopback lab (see *Lab run* below).

Cleaned note: no addresses, no decompiler output, no generated names.

## Short answer

`PLO_NPCACTION` **replaces the script of a server-wide NPC (id 1000 or more) that the client already has**, and fires `playerenters` on it at once. It is the only packet in these builds that can do that, because the SCRIPT prop (NPCPROP 1) is ignored once an NPC has a script. **[bin][lab]**

```
{26 + 32} {GINT3 npc id} {script text, to the end of the message}
```

- The script is **not length-prefixed**. It runs to the end of the message (the `\n` that ends every message is the only terminator).
- Line breaks inside the script are `§` (byte `A7`), as in the SCRIPT prop. A raw `\n` would end the message. (2.00's own new-NPC template script ends its line with `§`, which is how the client holds script text in memory. **[bin][inf]**)
- **Only ids 1000 and up work.** The lookup searches the client's list of server-wide NPCs. Level NPCs (ids below 1000, which live in their level's own list, see `../protocol/packet-layouts.md`) are never found, so a 26 for one of them is ignored. **[bin][lab]**
- The packet itself gets no reply. Anything the client sends afterwards comes from the new script running.

## Builds

| Build | Handles 26 | How checked |
|---|---|---|
| 1.1.9 | no | relay-era protocol; the client has no NPC script setter of this kind and no handler of this shape (`../protocol/relay-1998.md`) |
| 1.21 | not checked | the archive is an InstallShield set that was not unpacked for this pass |
| 1.28 beta 2 | **yes** | case 26 of the receive switch, same shape as 2.00 (earliest build seen with it) |
| 1.3 test | yes | case 26, same shape |
| 1.31, 1.32, 1.33 | yes | case 26, same shape |
| 1.38, 1.39, 1.41 rev1 | yes | in the handled set (`cross-version-timeline.md`: ids 0–41 from 1.33); handler not re-read, the switch was not located in these binaries by this pass |
| NewMain 24, NewMain 26 | yes | in both switches; NewMain 24's case re-read, same shape |
| 2.00, 2.00 rev1 | yes | case 26 read; **2.00 confirmed in the lab** |
| 2.01, 2.02, 2.03 | yes | case 26, same shape (field offsets move, nothing else) |
| 2.04 | no | removed (`decomp-findings-2026-10-24-c/04-plo-server-to-client.md`); re-checked: the 2.04 switch has no arm for 26 |
| 2.05, rev1, rev2; 2.1 test2/test3; NewWorld betas | no | `../protocol/packet-ids.md`, `decomp-findings-2026-10-24-c/04-plo-server-to-client.md` |
| 2.17.1, 2.22, 2.31 | no | `../protocol/client-versions.md` |
| 3.04, 3.153 | no | `../protocol/v3x-clients.md` (0–25, 27–…) |
| 4.04r2, 4.20r6 (Mac), 4.20r8 | no | `../protocol/v4x-clients.md` |
| 5.00r7, 5.12, 5.24r3/r4 | no | `../protocol/v5x-clients.md`, `../protocol/v5v6-windows-unpacked.md` |
| 6.00 to 6.03r7 | no | `../protocol/v5v6-windows-unpacked.md`, `../protocol/v6x-clients.md` |

So the packet lives from **1.28 beta 2 (1999) to 2.03 (May 2001)** and never comes back: no later client in these notes has an arm for 26. **[bin]**

## What the handler does, step by step

Same in every build read. **[bin]**

1. **Length guard.** A message body shorter than 3 bytes is dropped.
2. **NPC id.** The first 3 bytes are a GINT3 (`(b0-32)<<14 | (b1-32)<<7 | (b2-32)`).
3. **Lookup.** The id is looked up in the client's list of server-wide NPCs (ids 1000 and up; `PLO_NPCPROPS` puts those there and puts lower ids in the level's own list). Not found, including any level NPC, drops the message. The packet never creates an NPC.
4. **Replace the script.** Everything from the 4th byte to the end of the message becomes the NPC's new script text. The text is stored through the same setter the SCRIPT prop, the level loader and the NPC copy code use (which keeps the script lightly scrambled in memory; that is internal and not on the wire).
5. **Drop the old compiled script.** The NPC's parsed command list and its pending state are cleared, so the new text is parsed fresh on its next run. Whether running timeouts and `sleep`s are cut as well was not followed to the end. **[inf]**
6. **`playerenters`.** If the player's level is the active level (2.01 and later: the one `PLO_SETACTIVELEVEL` named; 2.00 and 1.3x: the level last sent by the server) and the NPC belongs to that level, the client runs the NPC's `playerenters` event straight away. Otherwise the new script waits until the NPC next gets an event.

## Why it exists

- In 2.00 the SCRIPT prop inside `PLO_NPCPROPS` (3) is applied only while the NPC's script is empty (after trimming). A second SCRIPT for the same NPC is ignored. 2.05 has the same rule (`../protocol/player-props.md#npcprop`). The 1.3x and 2.01 to 2.03 prop parsers were not re-read. **[bin]**
- `PLO_NPCACTION` is the way round it: same text format, no "only if empty" test, and a fresh `playerenters` so the NPC starts over.
- The 1.3x era had online level editing, and the 2001 NPC server has an `update script` command that replaces a live NPC's script (`../tools/npcserver-2001.md`). Either would need exactly this packet. Which server sent it is **not known**: no server source in these notes is known to send 26, and no capture has it. **[inf]**
- 2.04 removed the handler. From 2.04 a server can only change a client-side script by deleting the NPC (29) and sending it again with new props.

## Compared with the SCRIPT prop

| | `PLO_NPCACTION` (26) | NPCPROP 1 SCRIPT in `PLO_NPCPROPS` (3) |
|---|---|---|
| Length | none, rest of the message | 2-byte length (`(b0-32)<<7 | (b1-32)`) before the text |
| NPC must exist | yes, otherwise ignored | no, NPCPROPS creates it |
| Existing script | replaced | kept; the new text is ignored |
| Compiled script | cleared | untouched |
| NPC ids | 1000 and up only | any |
| `playerenters` | yes, if the NPC is in the active level and the player is there | for a newly created NPC when the player is in its level (`../protocol/packet-layouts.md`) |
| Line breaks | `§` | `§` |

## For a server sending it

- Send it only to 1.28 beta 2 to 2.03 clients. 2.04 and later fall to the silent default arm, so sending it to them is harmless but does nothing.
- The NPC must already exist on the client (send `PLO_NPCPROPS` first).
- Encode line breaks as `A7`. Wrapping the message in `PLO_RAWDATA` (100) would let raw newlines through, but the client's own scripts use `§`, so stay with `A7`. **[inf]**
- Use an NPC id of 1000 or more. A level NPC cannot be changed this way.

## Lab run (2026-11-04) **[lab]**

- Client: real Graal 2.00 (`GNW24011`) under Wine 9.0 in a cloud container, in a network namespace whose only interface is loopback. Data folder: the Reborn 2.22 folder plus `objects.dat` from NewMain 26 (`v2.00-connect-path.md`).
- Server: a small Python list host and gserver written for this run (loopback only). It logs any account in, sends a 64×64 board, and injects messages on command. The script, the log and the screenshots are in the project files (`npcaction-lab-2026-11-04/`), not in this repository.
- Steps and results:
  1. Level NPC id 1 with `if (playerenters) {§message ORIGINAL;§}§`. On login the client ran it and reported the `message` back as a props update. 
  2. Server-wide NPC id 1000 by `PLO_NPCPROPS` with `if (playerenters) {§message GLOBAL-ORIGINAL;§}§`. Shown at once, and reported back.
  3. **Control:** `PLO_NPCPROPS` for id 1000 again, SCRIPT `…message PROP-SCRIPT-AGAIN;…`. Nothing changed and the client sent nothing: the second SCRIPT prop is ignored.
  4. **`PLO_NPCACTION`:** `3a 20 27 88` + `if (playerenters) {§message SWAPPED-BY-NPCACTION;§}§` (A7 for `§`) + `0a`. Within a second the NPC's text changed to `SWAPPED-BY-NPCACTION`, and the client sent a props update for NPC 1000 carrying the new message. So the script was replaced and `playerenters` ran straight away.
  5. `PLO_NPCACTION` for the level NPC id 1 (scripts on `playerenters` and on `playertouchsme`): no effect, no reply, touching the NPC did nothing new. That matches the id ≥ 1000 lookup.
- Not tested in the lab: 1.x builds, 2.01 to 2.03 (same handler shape), an NPC in another level, running `timeout` or `sleep` across the swap.
