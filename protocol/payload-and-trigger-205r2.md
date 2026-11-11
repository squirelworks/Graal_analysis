# NPC script property, NPC movement records and the trigger gates in 2.05r2

Evidence IDs GRAAL-205-PAYLOAD-SEMANTICS-20261109-01 (receive payloads) and SCRIPT-PACKET-BRIDGE-205R2-20261109-01 (trigger bridge). Target: the original Windows 2.05 revision 2 executable, SHA-256 `b0e39a04ca0891d0f02282a113a1cd80ddf7a1880a786c5831f26a452e8cbb08`. Both are static reads of that one build, checked with synthetic model tests (10 for the payloads, 22 for the trigger bridge). No client was run and no packet was captured for this note. Ids are logical; on the wire each byte is the id plus 32.

This note adds to `packet-layouts.md`, which has the general 2.05 layouts. Where the two differ, this note is the narrower and later read of the exact build.

## NPC props (PLO 3) and the script property

[2.05][bin] PLO 3 is a GINT3 NPC id and then NPC props. Ids below 1000 are looked up in the level's local NPC list; higher ids use the global registry. This matches `packet-layouts.md`.

[2.05][bin] **The script property (NPCPROP 1) is applied only once.** Its payload is a GSHORT byte length and that many bytes. The setter runs only when the NPC's existing script, trimmed of bytes 0x20 and below at both ends, is empty. A non-empty script is left unchanged, but the declared bytes are still consumed and the properties after it are still applied. A server or reimplementation that assigns the script unconditionally behaves differently from this client.

[2.05][bin] The client keeps script text in memory with a per-byte transform (a complement plus an addition) and reverses it on read. This is local obfuscation, not packet encryption. Setting the script clears the compiled program and cache objects.

## NPC movement (PLO 165)

[2.05][bin] PLO 165 is a GINT3 NPC id followed by **complete 7-byte records**:

| Bytes | Field |
|---:|---|
| 1 | x, half-tiles (value / 2) |
| 1 | y, half-tiles (value / 2) |
| 1 | dx, half-tiles, biased by 50 tiles (value / 2 − 50) |
| 1 | dy, half-tiles, biased by 50 tiles (value / 2 − 50) |
| 2 | duration, GSHORT in twentieths of a second (value / 20) |
| 1 | options byte (the `move` options described in `npc-library/gs1-move-205r2.md`) |

[2.05][bin] A record for an NPC the client does not have does not create it. A trailing incomplete record is ignored. The record layout is from the static read and the model tests; the bias and scale of dx/dy are as recorded there and were not checked against a capture.

## Other payload details

[2.05][bin] PLO 0 and PLO 7 carry zero or more board-change rectangles: four GCHARs (x, y, w, h) followed by w × h row-major GSHORT tiles. Processing stops at incomplete data. Raw PLO 101 is an 8,192-byte board copied in directly as a 64 × 64 grid of little-endian 16-bit words. Both agree with `manual/02-protocol/05-plo.md`.

[2.05][bin] PLO 33 is a GSTRING weapon name and then NPC props. An unknown name creates the weapon and its NPC, applies the props, queues `playerenters` and adds and selects the weapon; a duplicate name is ignored. In 2.05r2 the script is GS1 text with its own two-digit length, not a GS2 container.

[2.05][bin] On the send side: the chat text is cut to 200 bytes; file-update and adjacent-level requests carry 5 metadata bytes in front (see `file-205r2-prefix-lf.md`); and a private message is sent even when the local echo guard fails.

[2.05][bin] PLO 40 and PLO 46 share one handler with a hidden mode flag of 0 or 1, as `packet-layouts.md` says. For 40 the payload after the attacker id is a signed fine knockback, then damage; for 46 it is damage, then a position from which the knockback vector is derived. How damage is scaled and capped is not settled by this read: "halved and capped at one" in the source record is ambiguous and needs the instructions before it is used.

## Trigger actions

### Sending (PLI 38)

[2.05][bin] GS1 `triggeraction` is statement 144 with argument letters `RRSS`. The client sends logical 38 (wire byte 70) to the server and 26 to peers over UDP; it receives logical 48 (wire byte 80).

[2.05][bin] The body is a three-digit, 7-bit-biased NPC source id (three spaces when there is none), the biased half-tile X and Y, then the action, with `,params` added only when the parameters are not empty. The sender quantizes coordinates as `floor(value × 2 + 0.0001)`.

### Receiving (PLO 48)

[2.05][bin] Server to client, a two-digit player id comes first. The receiver needs at least six more bytes, a local level and no pending warp. The text is split at the **first** comma only; there is no CSV or quote handling.

[2.05][bin] **Gate 1, the source.** A positive NPC id must name an NPC in the active level, or the message is dropped. Otherwise there must be a resolved player source whose stored context field matches (the meaning of that field is not known). The squared distance from the source to the player must be below 100, that is within 10 tiles. For an NPC the source point is its centre, using half its image size in tiles, measured against the player's anchor at (1.5, 2).

[2.05][bin] **Gate 2, weapons (new).** For the player's own weapon scripts there is a second check: the routed source must not be the local player, and the target coordinates must be **strictly** within 2 tiles of the player's (1.5, 2) anchor on each axis. Exactly 2 tiles is outside. `packet-layouts.md` and the manual previously listed only the 10-tile source gate.

[2.05][bin] Incoming packets switch off the router's pass over level NPCs. The local `triggeraction` command switches it on and uses the NPC point-hit test.

[2.05][bin] **Events.** The event name is prefixed with the action. An identical name that is already pending is ignored, and so is a new action-prefixed event while any pending name has that prefix. Accepted events are queued, not run at once.

## Limits

Only this build is covered, and only statically. Nothing here was observed on a running client: the gates, the first-write rule for scripts and the 165 record layout are code reads checked by model tests. The 40/46 damage scale and the stored context field in gate 1 remain open. Raw instructions, addresses and private evidence stay with the evidence owner; see `docs/evidence-index.tsv`.
