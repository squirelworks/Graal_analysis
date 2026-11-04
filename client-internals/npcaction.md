# PLO_NPCACTION (26): replace an NPC's script

What the client does with server-to-client id 26 (`PLO_NPCACTION` in gs2lib's names), read from the receive switch of every 1.3x and 2.0x build that handles it. Static read only: the dispatcher case, the routines it calls, and their other callers. Nothing here was seen on a wire or in the lab.

Cleaned note: no addresses, no decompiler output, no generated names.

## Short answer

`PLO_NPCACTION` **replaces the script of an NPC the client already has**. It is the only packet in these builds that can do that, because the SCRIPT prop (NPCPROP 1) is ignored once an NPC has a script.

```
{26 + 32} {GINT3 npc id} {script text, to the end of the message}
```

- The script is **not length-prefixed**. It runs to the end of the message (the `\n` that ends every message is the only terminator).
- Line breaks inside the script are `§` (byte `A7`), as in the SCRIPT prop. A raw `\n` would end the message. (2.00's own new-NPC template script ends its line with `§`, which is how the client holds script text in memory. **[bin][inf]**)
- The client does nothing in reply and sends nothing.

## Builds

| Build | Handles 26 | Handler read |
|---|---|---|
| 1.31, 1.32, 1.33 | yes | yes, same shape as 2.00 |
| 1.38, 1.39, 1.41 rev1 | yes (`cross-version-timeline.md`: ids 0–41 from 1.33) | no (the switch was not located in these binaries by this pass) |
| NewMain 24 | yes | yes, same shape |
| 2.00, 2.00 rev1 | yes | yes |
| 2.01, 2.02, 2.03 | yes | yes, same shape (field offsets move, nothing else) |
| 2.04 and every later client | no | removed in 2.04 (`decomp-findings-2026-10-24-c/04-plo-server-to-client.md`) |

So the earlier "2.00 to 2.03" range in the protocol notes is the 2.0x part of it; the packet is at least as old as 1.31 (early 2000). Older builds (1.1.9, 1.28 beta 2) use a different receive switch and were not checked. **[bin]**

## What the handler does, step by step

Same in every build read. **[bin]**

1. **Length guard.** A message body shorter than 3 bytes is dropped.
2. **NPC id.** The first 3 bytes are a GINT3 (`(b0-32)<<14 | (b1-32)<<7 | (b2-32)`).
3. **Lookup.** The id is looked up in the client's list of all NPCs it knows (every loaded level, not only the current one). An unknown id drops the message. The packet never creates an NPC.
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
| `playerenters` | yes, if the NPC is in the active level and the player is there | for a newly created NPC when the player is in its level (`../protocol/packet-layouts.md`) |
| Line breaks | `§` | `§` |

## For a server sending it

- Send it only to 1.31 to 2.03 clients. 2.04 and later fall to the silent default arm, so sending it to them is harmless but does nothing.
- The NPC must already exist on the client (send `PLO_NPCPROPS` first).
- Encode line breaks as `A7`. Wrapping the message in `PLO_RAWDATA` (100) would let raw newlines through, but the client's own scripts use `§`, so stay with `A7`. **[inf]**
- Lab confirmation is still open: a loopback server that sends 26 to a 2.00 client and checks that the NPC's behaviour changes.
