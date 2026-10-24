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
| 08 | [Tampercheck 39 (+ process list 182)](08-tampercheck.md) | Yes for 2.22 (constant known); 2.17/2.31 values missing | 2 | 1 | 2.0 | 4 | nothing for the lab; 2.17 and 2.31 values by lab capture; the 2.22 value builder only if a server enforces it |
| 03 | [Inventory, items, chests](03-inventory.md) | Yes | 5 | 3 | 1.7 | 5 | nothing |
| 14 | [Friends, ignore, mute, status](14-friends-ignore.md) | 2.05 (local files) yes; 2.17+ buddy and mute no | 3 | 2 | 1.5 | 6 | a real 2.22 capture of buddy requests and the mute item |
| 02 | [Weapons and combat](02-weapons-combat.md) | Yes for the protocol; 2.05 hit box known (decompile); feel only approximate | 5 | 4 | 1.25 | 7 | nothing for interop; optional: when 2.05 sends HITOBJECTS, the real damage formula (inferred power / 2) |
| 06 | [GMAP overworld and map links](06-gmap-overworld.md) | Server side and file format yes; client crossing behaviour no | 4 | 4 | 1.0 | 8 | a lab capture of a 2.22 client crossing a gmap edge (no decompile) |
| 11 | [Emotes and non-walk GANIs](11-emotes-ganis.md) | 2.22+ yes; 2.05 sprite table and Ctrl+letter lookup known (decompile) | 3 | 3 | 1.0 | 9 | nothing to build; open: how other players see a key emote, swim on the wire (none in 2.05) |
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
4. **Lab capture, 2.22**: crossing a gmap edge in a 2x2 gmap (topic 06). The lab can make it; no decompile.
5. **Lab capture, 2.22, with an extended listserver stub**: add/verify/delete buddy and the playerlist Mute item (topic 14).
6. **Lab captures**: the id-39 constant for 2.17 and 2.31 (topic 08). A decompile of the 2.22 id-39 value builder is only needed if some server is seen to enforce the value.
7. ~~Optional, feel only: the 2.05 sword hit box (topic 02).~~ **Filled**: the victim's client evaluates the hit (reach 0 to 4 tiles, lateral under 2, AP 100 immune). Left: when 2.05 sends HITOBJECTS in a swing and the real damage formula.

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
| 25 | SIGNATURE | S to C | one byte, 73 = more than eight players; sent at every login | cross-cutting (below) |
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
