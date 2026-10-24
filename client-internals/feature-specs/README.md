# Seihai laundry list: the 14 "Not yet discussed" topics

Written 2026-10-24 (Asia/Tokyo, JST). Sources checked: Graal_analysis `8da6800` (main), Seihai `06aacfd` (main, 2026-10-24 03:23 JST), GServer-v2 source (local checkout), graal-serverlist source, the offline lab, and the public-server report of 2026-10-24 17:56 JST (structure only; no addresses copied).
Nothing was run against the lab or any public server for this pass. No decompiler output, addresses or auto-generated names appear in these files. GServer behaviour is described in my own words with function names only.

## Sufficiency table

"Enough" means Claude can implement the topic against the lab with what is already written. Value = worth to a playable client (1-5). Effort = work (1-5, 1 = a few hours). Score = value / effort.

| # | Topic | Existing material enough? | Value | Effort | Score | Rank | NEEDS |
|--:|---|---|:-:|:-:|:-:|:-:|---|
| 13 | [Ban and kick handling](13-ban-kick.md) | Yes | 3 | 1 | 3.0 | 1 | nothing |
| 12 | [Server MOTD and rules](12-motd-rules.md) | Yes | 3 | 1 | 3.0 | 2 | nothing |
| 04 | [Death, respawn, regen](04-death-respawn.md) | Yes (server side and 2.05 client side, from the 2.05 decompile) | 4 | 2 | 2.0 | 3 | nothing; open: the "same name group" respawn-point rule, 1.39 death handler |
| 08 | [Tampercheck 39 (+ process list 182)](08-tampercheck.md) | Yes (constants for 2.17, 2.22 and 2.31 captured; derivation decoded) | 2 | 1 | 2.0 | 4 | nothing. Derivation settled (two chained CRC-32 words over the client's own image; per-build constants for 2.17, 2.22, 2.31). Left: whether any server enforces it (cannot be settled offline) |
| 03 | [Inventory, items, chests](03-inventory.md) | Yes | 5 | 3 | 1.7 | 5 | nothing |
| 14 | [Friends, ignore, mute, status](14-friends-ignore.md) | 2.05 (local files) yes; 2.22 buddy/ignore local and mute payload captured; listserver buddy requests unseen | 3 | 2 | 1.5 | 6 | only if buddies should go through a listserver: a capture of `verifybuddies`/`addbuddy`/`deletebuddy` (needs a database-backed listserver or another trigger) |
| 02 | [Weapons and combat](02-weapons-combat.md) | Yes for the protocol; 2.05 sword hit box and swing sender known from the decompile | 5 | 4 | 1.25 | 7 | nothing for interop; open: whether the attacker also sends HURTPLAYER (26) on a sword hit |
| 06 | [GMAP overworld and map links](06-gmap-overworld.md) | Server side, file format and 2.22 client crossing behaviour yes (lab capture); 2.31 crossing captured (lab, batch b2) | 4 | 4 | 1.0 | 8 | nothing for 2.22. 2.31 crossing now captured in the lab (cell prop plus wrapped coordinate, PLI 46 before it); left, thin evidence: the Z2 prop and the overview layout on the map screen |
| 11 | [Emotes and non-walk GANIs](11-emotes-ganis.md) | Yes (2.22+ names are strings; 2.05 wire sprite formula and Ctrl+letter lookup known from the decompile) | 3 | 3 | 1.0 | 9 | nothing to build; open: how other players see a key emote, swim on the wire (none in 2.05) |

| 01 | [Sound and music](01-sound.md) | Yes for WAV effects | 3 | 3 | 1.0 | 10 | nothing |
| 09 | [In-game options](09-options.md) | Yes | 2 | 2 | 1.0 | 11 | nothing |
| 10 | [Right-click context menu](10-right-click-menu.md) | Yes (2.05 F7 popup order and rules known from the decompile; no world right-click exists) | 2 | 3 | 0.7 | 12 | nothing; open: 1.39 popup, History window contents |
| 07 | [UDP peer channel](07-udp-peer.md) | Yes | 1 | 3 | 0.3 | 13 | nothing (UDP is optional; TCP fallback covers it) |
| 05 | [Player save and load](05-save-load.md) | Yes (server-owned) | n/a | 0 | n/a | n/a | nothing, nothing to build |

Suggested build order (dependencies, not just score): 13, 12, 08 (opt-in), 03, 02 with 04 together, 14 (ignore first), 11, 01, 09, 06 (after the lab capture), 10, 07.

## Items that truly need a new decompile or capture
1. ~~Decompile, 2.05: the death handler (topic 04).~~ **Filled** by the 2026-10-24 2.05 decompile (timings, input lock, hearts by AP, destination, no respawn packet, CLAIMPKER from the victim). Left: the "same name group" respawn-point rule.
2. ~~Decompile or capture, 2.05: the sprite-index to animation table and the Ctrl+letter emoticon mapping (topic 11).~~ **Filled**: wire sprite formula and step table, and the Ctrl+letter lookup (a local prefix match on `emoticon_<letter>`, no packet). Left: how other players see an emote, and swim on the wire (none in 2.05).
3. ~~Decompile or screenshot, 2.05: the F7 popup and right-click handler (topic 10).~~ **Filled**: item order Message, History, Buddy, Ignore, Profile; `TPersonAction` is the NPC script editor, not a player menu; no world right-click exists.
4. ~~**Lab capture, 2.22**: crossing a gmap edge in a 2x2 gmap (topic 06).~~ **Filled** (see `06-gmap-overworld.md`; 2.31 crossing also captured, see `../decomp-findings-2026-10-24-b/07-lab-findings-46-186-200.md`).
5. **Still open: lab capture, 2.22, with an extended listserver stub**: add/verify/delete buddy and the playerlist Mute item (topic 14).
6. ~~**Lab captures**: the id-39 constant for 2.17 and 2.31 (topic 08).~~ **Filled**: constants captured for 2.17, 2.22 and 2.31, and the builder decoded (`../decomp-findings-2026-10-24-b/01-tamper-check-id39.md`). Nothing left to decompile; only whether a server enforces the value is unknown.
7. ~~Optional, feel only: the 2.05 sword hit box (topic 02).~~ **Filled**: the victim's client evaluates the hit (reach 0 to 4 tiles, lateral under 2, AP 100 immune). Left: when 2.05 sends HITOBJECTS in a swing and the real damage formula.

### Settled index (cross-cutting items, status as of the lab batch c, 2026-10-24)
These are protocol items from the laundry triage that are no longer "needs decompile or capture". Detail and provenance are in the linked notes; nothing here is new evidence.

| Item | Status | What is settled | Still open | Where |
|---|---|---|---|---|
| `PLI_ENTERLEVEL` (46), 2.31 | **Settled** (lab, real client) | Payload is always `GCHAR 1`. Sent on every level entry (login, each gmap edge crossing, doors and edge links, server-side warps), just before the first props of the new level: in the same frame as a cached-level link request, otherwise in the first frame after the server's level answer. 2.31 does not re-send id 39 at any of these. 2.22 never sends 46 (0 of 8 transitions) but sends 39 after each client-initiated link request. Not sent by 2.17. | Script-initiated warps (`setlevel2`) not captured. | `../decomp-findings-2026-10-24-b/07-lab-findings-46-186-200.md`, `../decomp-findings-2026-10-24-b/08-lab-findings-levelchange-24-178.md`, `08-tampercheck.md` |
| `PLO_SERVERWARP` (178), 2.31 | **Settled** for the client side (lab: one real chain, field-order cases synthetic) | Four comma fields: field 0 unused, 1 = name, 2 = host, 3 = port. The client closes the old connection and logs in again to field 2 and 3 with a new key and the same stored credentials; no listserver step. Fewer than four fields is ignored; swapped host and port fails to connect. | The text a real service sends is unobserved (the lab text came from the open-source listserver reimplementation). 2.22 untested. | `../decomp-findings-2026-10-24-b/08-lab-findings-levelchange-24-178.md` |
| `PLI_SHOWIMGPLAYER` (24) relay | **Partly settled** (lab) | 2.31 sends `GCHAR 9` at login and about every 5.13 s; 2.22 sends it too, but only with another player in the level. The stock server relays any payload unchanged as `PLO_SHOWIMGPLAYER` (32) to the others in the level; injected payloads (synthetic) caused no disconnect and no visible reaction. | What the 9 means; what a receiver does with it; the exact 2.22 condition. | same note |
| `PLO_BOARDMODIFY2` (186), 2.22 and 2.31 | **Settled** for the client reaction (synthetic frames) | Layout `c mapX, c mapY, c x, c y, c w, c h` + `w*h` GSHORT tiles. Bytes after the tiles are unread padding (a second record there is not applied). One byte short is dropped silently. A block past column 63 is clipped, not rejected. Identical on 2.22 and 2.31. | No server has been seen sending 186. `mapX`/`mapY` other than the current cell untested. | same note; `../../protocol/packet-ids.md` |
| 2.00 listserver, client side | **Partly settled** | Client sends one plain zlib frame `GCHAR 0` + `newmain`, no account or password, then goes straight to the gserver (no second listserver connection). 2.00 accepts a 2.17-style list reply. | The reply format of a real 2.00-era listserver is **unobserved** (the lab reply was synthetic). | same note; `../decomp-findings-2026-10-24-b/04-v2.00-client.md` |
| Tamper check (PLI 39) derivation | **Settled** | Two chained CRC-32 words over the client's own memory image, each written as 5 bytes in a non-GINT5, unmasked form; a constant per build. 2.31 re-sends every 3.2 s; 2.22 at a gmap crossing; 2.17 once. | Whether any server enforces it. | `08-tampercheck.md`, `../decomp-findings-2026-10-24-b/01-tamper-check-id39.md`, `../../version-profiles/tampercheck-words.tsv` |
| `PLO_HIDENPCS` (151) | **Settled** | No payload; removes the NPCs with ids 1 to 999 of the active level (id 0 excluded). Wire format unchanged from 2.17.1 to 2.22. | none | `../decomp-findings-2026-10-24-b/02-server-to-client-layouts.md`, `../../protocol/packet-ids.md` |
| `PLO_SIGNATURE` (25) quit rule | **Settled** | Value 1 quits; value 0 quits unless the connected host string is the loopback address; any other value is ignored. The public-server value 73 is in the ignored group, so it never triggers the quit rule. Same in 2.17.1, 2.22, 2.31; the id is handled from 2.00. | none | `../decomp-findings-2026-10-24-b/05-open-items.md`, table below |

Not settled, for contrast (all in `../decomp-findings-2026-10-24-b/05-open-items.md`): `PLI_SHOWIMGPLAYER` (24) payload meaning, the extra 2.31 step after `PLO_SETACTIVELEVEL` (156), client ids 36/42/45 in 2.22, the 2.31 window-title scan.

### Still open after the 2026-10-24 decompile pass (new or remaining)
- How other players see a Ctrl+letter emote (topic 11): the key path sends nothing, and the captured SHOWIMG frames are unexplained. A lab capture of a real 2.05 client would settle it.
- Swim on the wire (topic 11, 04): none found in 2.05; swim is a local mode.
- Damage formula (topic 02): inferred sword power / 2, unconfirmed.
- Unlabelled STATUS bit 0x20 and a few player-mode values (topics 04, 11).
- The "same name group" rule for the saved respawn point (topic 04).
- 1.39: F7 popup items, death handler and sword hit box were not read (topics 10, 04, 02).
- History window contents and the ignore auto-reply send condition (topic 10).

Tag note: `[dec]` marks a fact derived from the 2026-10-24 static analysis of a client build (behaviour only, no code); `[srv]`, `[cap]`, `[inf]` and version tags keep their earlier meaning (server source, capture, inferred).

Corrections made on 2026-10-24 from the decompile pass: topic 11 no longer says Ctrl+letter sends `PLI_SHOWIMG` (24) (only the script command `showimg` does), and topic 10 no longer lists `TPersonAction` as an unexplained player form. Facts are derived; see `../decomp-findings-2026-10-24/`.

## Public-server "unhandled" ids, identified from GServer-v2 and placed

| Id | Name | Direction | Meaning in one line | Topic |
|---:|---|---|---|---|
| 10 | ISLEADER | S to C | you run this level's baddies and timeouts | 02, 04 (07 for routing) |
| 25 | SIGNATURE | S to C | one byte, 73 = more than eight players; sent at every login. Client rule (2.17–2.31 handlers, 2026-10-24): value 1 quits, value 0 quits unless the host is 127.0.0.1, any other value (such as 73) is ignored, so 73 never triggers the quit rule (settled, see the settled index above) | cross-cutting (below) |
| 39 | LEVELMODTIME | S to C | `i5` level modification time for the client cache (not the same as PLI 39) | 06 |
| 41 | STARTMESSAGE | S to C | server message text (HTML, one line) | 12 |
| 44 | HASNPCSERVER | S to C | only with the NPC-server build; the lab build does not send it | 07 |
| 47 | STAFFGUILDS | S to C | guild names that count as staff in the player list | 10 |
| 156 | SETACTIVELEVEL | S to C | level name that receives following NPC/chest/baddy packets (the gmap name on a gmap) | 06 |
| 168 | UNKNOWN168 | S to C | blank packet the login server sends | cross-cutting |
| 171 | BIGMAP | S to C | `text,image,x,y` big map settings (2.1+) | 06 |
| 172 | MINIMAP | S to C | `text,image,x,y` minimap settings (2.1+) | 06 |
| 174 | GHOSTICON | S to C | 1 = ghost players present (free accounts); GServer sends 0 per level | cross-cutting |
| 179 | RPGWINDOW | S to C | two greeting lines in quotes | 12 |
| 180 | STATUSLIST | S to C | player-list status names (Online, Away, ...) | 14 |
| 182 | LISTPROCESSES | S to C | process-list request (anti-cheat), client reply is PLI 44 | 08 |

Cross-cutting handling, all one-liners: store 25 and 168 and ignore; store the ghost flag from 174; none of these changes play. Also note `PLI 39` (client to server) is the tampercheck in the Graal_analysis notes and `PLI_MAPINFO` in the older GServer-v2 header (topic 08).

## Facts worth knowing before writing code
- **GServer-v2 drops a client after the 6th unknown packet id** (`msgPLI_NULL`). Never send an id that is not in the profile's `pli` set, and never `PLI 43` (mute) to it (topic 14).
- **Most of the game is client-authoritative.** The server clips and forwards. Inventory counts, hearts (not above the server value under 40 AP), death bit and combat events all come from the client (topics 02, 03, 04).
- **Lab server facts**: built without the NPC-server flag; options in `servers/lab/config/serveroptions.txt` (bushitems, respawntime 15, apsystem on, maxplayers 128); `maps`, `gmaps`, `bigmap` and `minimap` are all empty; `servermessage.html` is the stock sample. To test a topic, edit a **copy** of the config and restart the lab gserver; use display :9 only.
- **Privacy**: the pcaps contain the lab password in plaintext. Use the cleaned decoded frames (`examples/lab_replay`) and never commit pcaps or the box-only files.
- **Snapshots**: laundry list "Done" items (warp, other players, DELPLAYER, file transfer) match later Seihai work than the older local clones; these notes use `main` at `06aacfd`.

## Rules these notes follow
Specs are derived notes and are untested. GServer-v2 is described, not copied. Graal_analysis boundary: derived, cleaned notes only.
