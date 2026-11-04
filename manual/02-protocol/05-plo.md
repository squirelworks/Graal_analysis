<!-- manual: kind=reference status=draft -->
# 2.5 PLO message reference (server to client)

Field notation is in → §0.6, the message envelope in → §2.1.2, and the login reply sequences in → §2.3.6. The client-to-server messages that trigger many of these are in → §2.4, prop streams in → §2.6, and file downloads in → §2.7. Every id, with its wire byte, is indexed in → App. A.

> Status: draft. Layouts are given where a note measured or read them; ids with no layout in the notes say `unmeasured`. The staff tools' own server messages are in §7.

## 2.5.1 How a client reads a PLO

| Rule | Builds | Source |
| --- | --- | --- |
| Every handler checks a minimum length first and drops a short message silently | 2.05, 2.17.1, 2.22, 2.31 | [2.05] (protocol/packet-layouts.md#how-205-reads-a-message-205); [bin] (protocol/packet-layouts.md#server--client-ids-above-48-and-related-217-222-231-bin) |
| An id with no case in the receive switch falls to one shared default arm and is ignored without error | 2.05 to 2.31 | [2.05] (protocol/packet-ids.md#server--client-plo_); [bin][srv] (protocol/client-versions.md#server--client-ids-handled) |
| 2.05 keeps two level pointers: the *named level*, set by every `PLO_LEVELNAME`, and the *object level*, which receives NPC messages (3, 150, 151, 166) and is set by `PLO_SETACTIVELEVEL`, or by each `PLO_LEVELNAME` when there is no NPC server | 2.05 | [2.05] (protocol/packet-layouts.md#how-205-reads-a-message-205) |
| Handlers for level objects (bombs, arrows, items, explosions, hits, trigger actions, horses, push-away) act only while the player stands in the named level | 2.05 | [2.05] (protocol/packet-layouts.md#how-205-reads-a-message-205) |
| A message the server re-emits for another player starts with `s player id`; with an unknown id, bombs, arrows, explosions and items are still shown without an owner, while fire spy, throw carried and player hits are dropped | 2.05 | [2.05] (protocol/packet-layouts.md#how-205-reads-a-message-205) |
| 2.17.1, 2.22 and 2.31 read "comma text" through the client's comma-text parser, which allows double quotes | 2.17.1, 2.22, 2.31 | [bin] (protocol/packet-layouts.md#server--client-ids-above-48-and-related-217-222-231-bin) |
| The receive dispatcher takes the id as the first byte minus 32, checks it against a bound, and goes through an index table; the bound is id 185 in 2.17.1, 186 in 2.22 and 189 in 2.31 | 2.17.1, 2.22, 2.31 | [bin] (client-internals/decomp-findings-2026-10-24-b/02-server-to-client-layouts.md#dispatcher-shape-all-builds) |
| 4.20r6 and 4.20r8 take 100 and 108 before the main switch | 4.20r6, 4.20r8 | [bin] (protocol/v4x-clients.md#server--client-ids) |

## 2.5.2 Ids handled by build

Builds before 2.00 are in → App. C.2. *Bound* is the highest id the receive switch tests, written as in the source.

| Build | Count | Ids handled | Source |
| --- | ---: | --- | --- |
| NewMain 24, 26 | 51 | 0–45, 75, 100, 150, 151, 153 (bound `0x99`) | [bin] (version-profiles/plo-handled-ids-by-build.tsv) |
| 2.00 (rev0–rev3) | 53 | 0–45, 75, 100, 150, 151, 153–155 (bound `0x9b`) | [bin] (version-profiles/plo-handled-ids-by-build.tsv) ; [bin] (client-internals/decomp-findings-2026-10-24-b/04-v2.00-client.md#server---client-ids-handled-200) ; [bin] (client-internals/decomp-findings-2026-10-24-c/plo_handled_ids_by_build.tsv) |
| 2.01 (+rev1) | 55 | 0–46, 75, 100, 150, 151, 153–156 | [bin] (version-profiles/plo-handled-ids-by-build.tsv) ; [bin] (client-internals/decomp-findings-2026-10-24-c/plo_handled_ids_by_build.tsv) |
| 2.02 (rev0–rev2) | 56 | 0–47, 75, 100, 150, 151, 153–156; disputed for rev0 and rev1 → App. E#7 | [bin] (version-profiles/plo-handled-ids-by-build.tsv) ; [bin] (client-internals/decomp-findings-2026-10-24-c/plo_handled_ids_by_build.tsv) |
| 2.03 | 58 | 0–48, 75, 100, 150, 151, 153–156, 165 | [bin] (version-profiles/plo-handled-ids-by-build.tsv) ; [bin] (client-internals/decomp-findings-2026-10-24-c/plo_handled_ids_by_build.tsv) |
| 2.04 | 58 | 0–25, 27–48, 75, 100, 150, 151, 153–156, 165, 166 (26 dropped) | [bin] (version-profiles/plo-handled-ids-by-build.tsv) ; [bin] (client-internals/decomp-findings-2026-10-24-c/plo_handled_ids_by_build.tsv) |
| 2.05 (rev0–rev2) | 59 | 0–25, 27–48, 75, 100, 150, 151, 153–156, 165, 166, 168 (bound `0xa8`); disputed for rev0 → App. E#7 | [bin] (version-profiles/plo-handled-ids-by-build.tsv); [2.05] (protocol/packet-ids.md#server--client-plo_) ; [bin] (client-internals/decomp-findings-2026-10-24-c/plo_handled_ids_by_build.tsv) |
| 2.1 test 2, test 3 | 61 | the 2.05 set plus 49, 169 | [bin] (version-profiles/plo-handled-ids-by-build.tsv) ; [bin] (client-internals/decomp-findings-2026-10-24-c/plo_handled_ids_by_build.tsv) |
| NewWorld beta 1 | 53 | the 2.05 set without 2, 4, 17, 18, 154, 155 | [bin] (client-internals/decomp-findings-2026-10-24-c/08-test-builds-newworld-newmain.md#newworld-beta1--beta2) |
| NewWorld beta 2 | 55 | the beta 1 set plus 49, 169 | [bin] (client-internals/decomp-findings-2026-10-24-c/08-test-builds-newworld-newmain.md#newworld-beta1--beta2) |
| 2.17.1 | 79 | 0–25, 27–49, 68, 69, 75, 100, 150, 151, 153–156, 165, 166, 168–185 | [bin] (version-profiles/plo-handled-ids-by-build.tsv) |
| 2.22 | 80 | the 2.17.1 set plus 186 | [bin] (version-profiles/plo-handled-ids-by-build.tsv) |
| 2.31 | 81 | the 2.22 set without 44, plus 84 and 189 | [bin] (version-profiles/plo-handled-ids-by-build.tsv); [bin] (protocol/client-versions.md#server--client-ids-handled) |
| 3.04 (Linux) | 79 | 0–49, 68, 69, 75, 84, 100–102, 150, 151, 153–156, 165, 166, 168, 169, 171–176, 178–181, 184–186 | [bin] (protocol/v3x-clients.md#server--client-ids-handled) |
| 3.153 (Mac OS X) | 88 | the 3.04 set without 44, plus 67, 74, 82, 104, 131–134, 187, 189 | [bin] (protocol/v3x-clients.md#server--client-ids-handled) |
| 4.20r8 | 101 | 0–25, 27–43, 45–49, 67–69, 74, 75, 82, 84, 100–102, 104–108, 131–134, 150, 151, 153–156, 165, 166, 168–176, 178–187, 189–191, 193–196 | [bin] (protocol/v4x-clients.md#server--client-ids) |
| 4.20r6 (Mac) | 99 | the 4.20r8 set without 41 and 196 | [bin] (protocol/v4x-clients.md#server--client-ids) |
| 5.00r7 | 100 | 0–25, 27–43, 45–49, 67–69, 74, 75, 82, 84, 101, 102, 104–107, 131–134, 140, 150, 151, 153–156, 165, 166, 168–176, 178–187, 189–191, 193–195, 197 | [bin] (protocol/v5x-clients.md#server--client-ids-500r7) |
| 6.01r1 | 91 | the 6.03r7 set without 111 | [bin] (protocol/v6x-clients.md#server--client-ids-601-603) |
| 6.03r7 | 92 | 0–25, 27–40, 42, 43, 45–49, 67–69, 74, 82, 84, 101, 102, 104–107, 109, 111, 131, 134, 140, 150, 151, 153–156, 166, 168, 170, 172–174, 176, 178–180, 182, 183, 185–187, 189–191, 194, 195, 197, 198 | [bin] (protocol/v6x-clients.md#server--client-ids-601-603) |

| Rule | Builds | Source |
| --- | --- | --- |
| No build in the notes handles 26 (`PLO_NPCACTION`) after 2.03, or 152 and 167 | 2.04 to 2.31 | [bin] (protocol/packet-ids.md#server--client-plo_); [bin] (protocol/client-versions.md#server--client-ids-handled) |
| Revisions of one version share every handler shape (2.05 rev1 differs by one constant in 8), so any revision stands for the others; on the wire only 2.02 rev2 differs, by its token and id 37 | 2.00 to 2.05 | [bin] (client-internals/decomp-findings-2026-10-24-c/06-handler-changes-by-build.md#revisions-of-the-same-version) |
| 2.00 has no active-level reference, since 156 arrives in 2.01; level-addressed messages act on the current level | 2.00 | [bin] (client-internals/decomp-findings-2026-10-24-c/04-plo-server-to-client.md#active-level-gating) |
| 2.01 rewrites 0, 14 and 15 so the handler no longer waits for and then requests the level, the code side of map preloading; 154 and 155 go through a shared helper | 2.01 | [bin] (client-internals/decomp-findings-2026-10-24-c/06-handler-changes-by-build.md#200---201) |
| 0, 6 and 14 gain checks that skip reloading a level that is already loaded | 2.1 test 3 | [bin] (client-internals/decomp-findings-2026-10-24-c/06-handler-changes-by-build.md#21-test2---test3); [bin] (client-internals/decomp-findings-2026-10-24-c/08-test-builds-newworld-newmain.md#21-test2-and-test3) |
| NewMain 24 and 26 have one handler set between them, but differ from 2.00 more than any 2.0x revision does, so NewMain is a separate branch | NewMain | [bin] (client-internals/decomp-findings-2026-10-24-c/08-test-builds-newworld-newmain.md#newmain-24--26) |
| 2.31 drops 44 (`HASNPCSERVER`); the 2.3 release notes say Classic switched to the NPC server | 2.31 | [bin][doc] (protocol/client-versions.md#server--client-ids-handled) |
| 3.04 lacks 170, 177, 182 and 183, which 2.22 handles, and adds 84, 101 and 102 | 3.04 | [bin] (version-profiles/3.04-3.153.md#server--client-ids) |
| 4.20r8 drops nothing against 3.153 and adds 13 ids | 4.20r8 | [bin] (protocol/v4x-clients.md#server--client-ids) |
| 5.00r7's list does not include 100 | 5.00r7 | [bin] (protocol/v5x-clients.md#server--client-ids-500r7) |
| Against 5.00r7, 6.x drops 41, 75, 132, 133, 165, 169, 171, 175, 181, 184 and 193 and adds 109, 111 and 198 | 6.01r1, 6.03r7 | [bin] (protocol/v6x-clients.md#server--client-ids-601-603) |
| A later client (5.07 and up, or 6.037, as the source note marks each id) ignores 26, 41, 44, 55, 56, 60, 78, 80, 81, 83, 132, 157, 159–164, 165, 167, 171, 175, 188 and 192 | 5.07, 6.037 | [srv] (protocol/packet-ids.md#server--client-plo_) |

## 2.5.3 Level data

| Id | Name | Layout | Client action | Source |
| ---: | --- | --- | --- | --- |
| 0 | `PLO_LEVELBOARD` | a run of board changes, each `c x, c y, c w, c h` + w × h `s tile` (row-major), back to back; empty = "use your cached board" | parsing stops when fewer than 4 bytes are left or a run is shorter than `w*h*2+4`; a pending warp to this level completes first | [srv][2.05] (protocol/packet-layouts.md#level-data-server--client) |
| 1 | `PLO_LEVELLINK` | `rest` = `dest x y w h newx newy`, split on spaces | see the rules below | [srv][2.05] (protocol/packet-layouts.md#level-data-server--client); [bin] (version-profiles/plo-levellink-layouts.tsv) |
| 2 | `PLO_BADDYPROPS` | `c id` + BDPROP stream (→ §2.6) | an unknown id creates the baddy | [srv][2.05] (protocol/packet-layouts.md#level-data-server--client) |
| 3 | `PLO_NPCPROPS` | `i3 id` + NPCPROP stream (→ §2.6); id > 0 | ids below 1000 are level NPCs, created in the object level; 1000 and up are server-wide; a new NPC gets the `playerenters` event if the player is in that level | [srv][2.05] (protocol/packet-layouts.md#level-data-server--client) |
| 4 | `PLO_LEVELCHEST` | `c opened, c x, c y` (whole tiles); if not opened, also `c item, c signindex` | a closed chest with fewer than 5 bytes is dropped; an opened chest draws nothing by itself, so on a board with no chest tiles the short form leaves no trace | [srv][2.05] (protocol/packet-layouts.md#level-data-server--client); [cap] (client-internals/decomp-findings-2026-10-25-l/04-public-server-run.md#why-no-chests-were-drawn) |
| 5 | `PLO_LEVELSIGN` | `c x, c y` (whole tiles) + sign-alphabet text (→ §3) | needs at least 2 bytes | [srv][2.05] (protocol/packet-layouts.md#level-data-server--client) |
| 6 | `PLO_LEVELNAME` | `rest` = level file name | sets the named level, and the object level when there is no NPC server | [srv][2.05] (protocol/packet-layouts.md#level-data-server--client) |
| 7 | `PLO_BOARDMODIFY` | one run: `c x, c y, c w, c h` + w × h `s tile`, row-major | needs `len ≥ w*h*2+4` | [srv][2.05] (protocol/packet-layouts.md#level-data-server--client) |
| 10 | `PLO_ISLEADER` | empty | this client runs the level's baddies and timeouts; ignored unless the player's level is the active level | [srv][2.05] (protocol/packet-layouts.md#level-data-server--client) |
| 17 | `PLO_HORSEADD` | `c x×2, c y×2, c (dir & 3) + 4 × bushes` (bushes capped at 6), `rest` = image | `.gif` is added when the image has no extension | [srv][2.05] (protocol/packet-layouts.md#level-data-server--client) |
| 18 | `PLO_HORSEDEL` | `c x×2, c y×2`; no player id | removes any horse within 2 tiles of that point | [2.05] (protocol/packet-layouts.md#level-data-server--client) |
| 22 | `PLO_ITEMADD` | `c x×2, c y×2, c item` (0–24); optional `s player` in bytes 3–4 | unknown items ignored; with the player id, a dropped sword or shield copies that player's image | [srv][2.05] (protocol/packet-layouts.md#level-data-server--client) |
| 23 | `PLO_ITEMDEL` | `c x×2, c y×2`; no player id | removes the item at exactly that point | [srv][2.05] (protocol/packet-layouts.md#level-data-server--client) |
| 39 | `PLO_LEVELMODTIME` | 2.05: `i5 modtime`, exactly 5 bytes; 2.17 to 2.31: `rest`, unparsed | 2.05 writes the level to its web-level cache (→ §3); 2.17 to 2.31 hand the rest to the active gmap or level object, if one exists | [srv][2.05] (protocol/packet-layouts.md#level-data-server--client); [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 42 | `PLO_NEWWORLDTIME` | `i4 time` (`b0<<21 \| b1<<14 \| b2<<7 \| b3`) | needs at least 4 bytes | [srv][2.05] (protocol/packet-layouts.md#level-data-server--client) |
| 100 | `PLO_RAWDATA` | `i3 length` (→ §2.1.3) | the next *length* bytes are one message | [srv] (protocol/codec-and-framing.md#raw-data-escape); [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 101 | `PLO_BOARDPACKET` | behind 100: `i3 (8194)`, then `c 101` + 4096 × `u16le` raw tile ids + `\n` | replaces the 64 × 64 board | [srv] (protocol/packet-layouts.md#level-data-server--client) |
| 107 | `PLO_BOARDLAYER` | 4.20r8: layer, x, y (each under 64), width and height (1–64), then two bytes per tile | a board change on a layer; layer 0 also clears the level's pending changes; 5.00r7 raises the script level to at least 5 and passes the data to a script object | [bin] (protocol/v4x-clients.md#server--client-ids); [bin] (protocol/v5x-clients.md#server--client-ids-500r7) |
| 150 | `PLO_NPCDEL2` | `c n`, n-byte level name, `i3 npc id` | removes that NPC from that level | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 151 | `PLO_HIDENPCS` | empty | removes NPCs with ids 1 to 999 from the active level (id 0 excluded) | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 156 | `PLO_SETACTIVELEVEL` | `rest` = level or `.gmap` name | sets the object level; a `.gmap` is loaded and made active; 2.31 adds a follow-up step whose purpose is unresolved | [srv][2.05] (protocol/packet-layouts.md#level-data-server--client); [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 185 | `PLO_BOARDHEIGHTS` | `c mapX, c mapY, c blockX, c blockY, c w−1, c h−1`, then w × h cells of 2 raw bytes, row-major | height = `(b0 − 0x20 − 0x32) + (b1 − 0x20) / 128`; written into that gmap cell's height grid from `blockX, blockY`; mapX and mapY must lie in the gmap grid | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 186 | `PLO_BOARDMODIFY2` | `c mapX, c mapY, c x, c y, c w, c h`, then w × h `s tile`, row-major | tiles replace that gmap cell's board from `x, y`; needs `len ≥ 6 + 2*w*h` | [bin][cap] (version-profiles/plo-layouts-217-231.tsv) |

| Rule | Builds | Source |
| --- | --- | --- |
| A link needs at least 5 space-separated fields, else the client raises "Wrong link data!"; `x y w h` are whole tiles read as floats; `newx` and `newy` are fields 5 and 6 or empty, and the literal `-1` becomes `playerx` or `playery` | 2.00, 2.04, 2.05 rev2, 2.17.1, 2.22, 2.31 | [bin] (version-profiles/plo-levellink-layouts.tsv) |
| 2.17.1 and 2.22 also have a helper that builds a default link with `newx` and `newy` preset to `playerx` and `playery`, used for editor and edge cases | 2.17.1, 2.22 | [bin] (version-profiles/plo-levellink-layouts.tsv) |
| `dest` is field 0, so a level name with a space cannot be linked | 2.00 to 2.31 | [bin] (version-profiles/plo-levellink-layouts.tsv) |
| The client takes a link when one point enters its rectangle: the player's centre (x+1.5, y+2), 1 to 1.5 tiles ahead in the walking direction; a 1×1 link off that centre line is walked past. Measured to half a tile in straight walks only | 2.05 rev2 (lab, one fork server) | [cap] (protocol/link-test-2026-11-04.md#result) |
| Only `PLO_BOARDPACKET` carries raw little-endian tiles; every other board message uses GCHAR headers and GSHORT tiles | server | [srv] (protocol/packet-layouts.md#board-modify-correction) |
| 186: bytes after the tiles are not read, so a complete second record in the trailer is not applied; a payload one byte short is dropped silently with no disconnect; a block past column 63 is clipped | 2.22, 2.31 (lab, injected frames; no server seen sending 186) | [cap] (version-profiles/lab-boardmodify2-186-trailer.tsv); [bin][cap] (protocol/packet-ids.md#server--client-plo_); [cap] (client-internals/decomp-findings-2026-10-24-b/07-lab-findings-46-186-200.md#plo_boardmodify2-186-222-and-231-client-reaction-observed-frames-synthetic) |
| In a two-client capture the server sent `PLO_BOARDMODIFY` with the reported bytes to both clients, the reporter included, and 15.0 s later (`respawntime = 15`) sent the original tiles back | 2.05 with GServer-v2 | [cap] (protocol/packet-layouts.md#board-change-on-the-wire-cap) |
| On level entry an empty `PLO_LEVELBOARD` followed the board packet and `PLO_LEVELMODTIME` | 2.05 with GServer-v2 | [cap] (protocol/packet-layouts.md#board-change-on-the-wire-cap) |

### 2.5.3.1 Level send order (pre-2.1 server path)

| Step | Messages | Source |
| ---: | --- | --- |
| 1 | if the client's cached modtime matches: the board changes since then, and nothing else | [srv] (protocol/packet-layouts.md#pre-21-level-sequence-sendlevel141-used-for-205-srv) |
| 2 | otherwise: `RAWDATA` + `BOARDPACKET`, then `LEVELNAME` (first level only), `LEVELLINK` × n, `LEVELSIGN` × n, `LEVELMODTIME` | [srv] (protocol/packet-layouts.md#pre-21-level-sequence-sendlevel141-used-for-205-srv) |
| 3 | then board changes, `LEVELCHEST` × n, `HORSEADD` × n, `BADDYPROPS` × n, `ISLEADER` (if leader), `NEWWORLDTIME`, `NPCPROPS` × n, and `OTHERPLPROPS` for each player in the level | [srv] (protocol/packet-layouts.md#pre-21-level-sequence-sendlevel141-used-for-205-srv) |

## 2.5.4 Players and the local player

| Id | Name | Layout | Client action | Source |
| ---: | --- | --- | --- | --- |
| 8 | `PLO_OTHERPLPROPS` | `s id` + PLPROP stream (→ §2.6); at least 2 bytes | an unknown id creates the player | [srv][2.05] (protocol/packet-layouts.md#player-state-server--client) |
| 9 | `PLO_PLAYERPROPS` | PLPROP stream for the local player, no id (→ §2.6) | applies the props | [srv][2.05] (protocol/packet-layouts.md#player-state-server--client) |
| 14 | `PLO_PLAYERWARP` | `c x×2, c y×2`, `rest` = level | the warp stays pending until the level data arrives | [srv][2.05] (protocol/packet-layouts.md#player-state-server--client) |
| 15 | `PLO_WARPFAILED` | `rest` = level | 2.05 ignores the text and shows a short failed-warp state | [srv][2.05] (protocol/packet-layouts.md#player-state-server--client) |
| 16 | `PLO_DISCMESSAGE` | `rest` = text | stored as the disconnect reason; the server then closes the connection | [srv][2.05] (protocol/packet-layouts.md#player-state-server--client) |
| 25 | `PLO_SIGNATURE` | `c v` | 1: the client quits; 0: it quits unless the connected host is the loopback address; other values ignored | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 28 | `PLO_FLAGSET` | `rest` = `name` or `name=value` | adds the flag only if it is not already set | [srv][2.05] (protocol/packet-layouts.md#player-state-server--client) |
| 31 | `PLO_FLAGDEL` | `rest` = flag name | removes the flag | [srv][2.05] (protocol/packet-layouts.md#player-state-server--client) |
| 38 | `PLO_PUSHAWAY` | `c dx, c dy`, each `v/16 − 4` (±2 tiles in 1/16 steps) | ignored unless the player's level is the active level | [srv][2.05] (protocol/packet-layouts.md#player-state-server--client); [srv] (protocol/packet-ids.md#server--client-plo_) |
| 40 | `PLO_HURTPLAYER` | `s attacker, c dx, c dy, c power`, optional `i3 npc` | see → §2.5.5 | [srv][2.05] (protocol/packet-layouts.md#player-state-server--client) |
| 49 | `PLO_PLAYERWARP2` | `c x×2, c y×2, c z` (unused), `c gmapX, c gmapY`, `rest` = level | gmapX and gmapY apply only when the level name ends in `.gmap`: they are clamped to the grid and the name is replaced by that cell's level | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 154 | `PLO_FREEZEPLAYER2` | empty | freezes the local player for 600 ticks unless unfrozen; skipped while some dialogs are open | [srv][2.05] (protocol/packet-layouts.md#player-state-server--client); [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 155 | `PLO_UNFREEZEPLAYER` | empty | unfreezes the local player | [srv][2.05] (protocol/packet-layouts.md#player-state-server--client) |
| 168 | `PLO_UNKNOWN168` | payload ignored | resets the local player; sent by the login server | [bin] (protocol/packet-ids.md#server--client-plo_); [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 170 | `PLO_GHOSTMODE` | `c flag` | 2.17 to 2.31: ghost mode on when the flag is above 0; 5.00r7: stored as the connection mode, and a change resets a player field | [bin] (version-profiles/plo-layouts-217-231.tsv); [bin] (protocol/v5x-clients.md#server--client-ids-500r7) |
| 173 | `PLO_GHOSTTEXT` | `rest` = text | stored as the ghost-mode text | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 174 | `PLO_GHOSTICON` | `c flag` | shows the ghost icon when the flag is above 0 | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 181 | `PLO_UNKNOWN181` | `s player id, c toggle`; at least 3 bytes | sets a boolean on that player | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 55, 56 | `PLO_ADDPLAYER`, `PLO_DELPLAYER` | unmeasured | ignored by 5.07 and later | [srv] (protocol/packet-ids.md#server--client-plo_) |

## 2.5.5 Combat and level objects

These are the server's copies of the client actions in → §2.4.5; each carries the sender's `s player id` unless the row says otherwise.

| Id | Name | Layout | Client action | Source |
| ---: | --- | --- | --- | --- |
| 11 | `PLO_BOMBADD` | `s player, c x×2, c y×2, c power, c fuse` | power = `v & 7`; the value 8 (bit 3) marks the bomb as that player's | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 12 | `PLO_BOMBDEL` | `c x×2, c y×2`; no player id | removes the bomb at exactly that point | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 19 | `PLO_ARROWADD` | `s player` + the 5 bytes of `PLI_ARROWADD` | needs at least 5 bytes; the last byte is decoded as `b − 33` | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 20 | `PLO_FIRESPY` | `s player, c (a × 8 + b)` | only `a` is used | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 21 | `PLO_THROWCARRIED` | `s player` | dropped when the player is unknown | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 27 | `PLO_BADDYHURT` | `c id, c (dx + 4) × 16, c (dy + 4) × 16, c power` | applied only by the level leader | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 36 | `PLO_EXPLOSION` | `s player, c radius, c x×2, c y×2, c power` | power `& 7` clamped to 1–3; 8 (bit 3) = owned | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 40 | `PLO_HURTPLAYER` | `s attacker, c dx, c dy, c power`, optional `i3 npc` | see the rules below | [srv][2.05] (protocol/packet-layouts.md#hits-205) |
| 46 | `PLO_HITOBJECTS` | `s player, c power, c x×2, c y×2`, optional `i3 npc` | see the rules below | [srv][2.05] (protocol/packet-layouts.md#hits-205) |
| 48 | `PLO_TRIGGERACTION` | `s player, i3 npc, c x×2, c y×2`, `rest` = `action` or `action,params`; more than 5 bytes | fires `action` on the local player's scripts when the source is within 10 tiles; split at the first comma | [srv][2.05] (protocol/packet-layouts.md#hits-205) |
| 175 | `PLO_SHOOT` | `s player id`, `rest` = shot data (unmeasured) | only when the current level is the active level | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 191 | `PLO_SHOOT2` | 4.20r8: x, y, z, three angle and speed values, a gani name with optional parameters, then a script string; 5.00r7: `s id` + data routed to an object | a projectile | [bin] (protocol/v4x-clients.md#server--client-ids); [bin] (protocol/v5x-clients.md#server--client-ids-500r7) |

| Rule | Builds | Source |
| --- | --- | --- |
| `PLO_HURTPLAYER`: `dx`, `dy` decode as `(v − 0x60) / 16` (knockback −4 to 4) and `power` as `(v − 32) / 2` hearts, capped at 1.0 | 2.05 | [2.05] (protocol/packet-layouts.md#hits-205) |
| With 6 or more bytes after the player id, the hit came from an NPC (`i3`), and distance is measured from that NPC | 2.05 | [2.05] (protocol/packet-layouts.md#hits-205) |
| A hit applies only when the attacker (player or NPC) is within 10 tiles and the local player can be hurt at that moment | 2.05 | [2.05] (protocol/packet-layouts.md#hits-205) |
| `PLO_HITOBJECTS`: `power` is `(v − 32) / 2`, capped at 1.0; it hurts the local player only when the player's centre is within 2 tiles of `(x, y)` on each axis | 2.05 | [2.05] (protocol/packet-layouts.md#hits-205) |
| 40 and 46 share one handler, with one flag that picks the layout; the same handler takes UDP id 21 (→ §2.9) | 2.05 | [2.05] (protocol/packet-layouts.md#hits-205) |
| The trigger-action coordinates are half-tiles, not whole tiles as in the server source | 2.05 | [2.05] (protocol/packet-layouts.md#differences-from-gserver-worth-knowing-205) |

How damage is applied after a hit is in → §4.3.

## 2.5.6 NPCs, weapons and scripts

| Id | Name | Layout | Client action | Source |
| ---: | --- | --- | --- | --- |
| 24 | `PLO_NPCMOVED` | unmeasured | unmeasured | [srv] (protocol/packet-ids.md#server--client-plo_) |
| 26 | `PLO_NPCACTION` | `i3 npc id`, `rest` | handled by 2.00 to 2.03 only, and acts only while the player's level is the active level; purpose unknown | [srv] (protocol/packet-ids.md#server--client-plo_); [bin] (version-profiles/plo-handled-ids-by-build.tsv); [bin] (client-internals/decomp-findings-2026-10-24-c/04-plo-server-to-client.md#set-growth) |
| 29 | `PLO_NPCDEL` | unmeasured | unmeasured | [srv] (protocol/packet-ids.md#server--client-plo_) |
| 33 | `PLO_NPCWEAPONADD` | `str name` + NPCPROP stream (normally `c 0` IMAGE + `str image`, `c 1` SCRIPT + `s len` + GS1 text) | a name the player already has is ignored; the weapon gets the `playerenters` event; a script line break is `§`, byte `A7` from a latin-1 server and `C2 A7` from a UTF-8 server | [srv][2.05] (protocol/packet-layouts.md#weapons); [cap] (client-internals/decomp-findings-2026-10-25-l/04-public-server-run.md#weapon-scripts-and-line-breaks) |
| 34 | `PLO_NPCWEAPONDEL` | `rest` = weapon name | removes the weapon | [srv][2.05] (protocol/packet-layouts.md#weapons) |
| 43 | `PLO_DEFAULTWEAPON` | `c item index` (0–24: a built-in weapon such as bow, bomb, sword) | adds the built-in weapon | [srv][2.05] (protocol/packet-layouts.md#weapons) |
| 44 | `PLO_HASNPCSERVER` | empty | the client stops applying NPC props itself | [bin] (protocol/packet-ids.md#server--client-plo_); [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 131 | `PLO_NPCBYTECODE` | `i3 code`, bytecode | script and class registration (→ §8) | [srv] (protocol/packet-ids.md#server--client-plo_); [bin] (protocol/v3x-clients.md#server--client-ids-handled) |
| 133 | `PLO_UNKNOWN133` | `rest` = text | maybe registers a class script | [srv] (protocol/packet-ids.md#server--client-plo_) |
| 134 | `PLO_GANISCRIPT` | gani text | 3.153 parses the gani text in place | [srv] (protocol/packet-ids.md#server--client-plo_); [bin] (protocol/v3x-clients.md#server--client-ids-handled) |
| 140 | `PLO_NPCWEAPONSCRIPT` | `s info_length`, script | class and weapon script delivery (→ §8) | [srv] (protocol/packet-ids.md#server--client-plo_); [bin] (protocol/v5x-clients.md#server--client-ids-500r7) |
| 165 | `PLO_MOVE` | `i3 npc id` (> 0), `rest` = move data | passed to the NPC movement routine | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 166 | `PLO_SHOWIMGNPC` | `i3 npc id`, `rest` = props | applies the props to that NPC in the active level | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 189 | `PLO_MOVE2` | `i3 npc id`, `rest` | as 165, with an extra flag set | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 193 | `PLO_UNKNOWN193` | `i5` time, file name | 4.20r8 checks its cached copy (mod time, then CRC); 5.00r7 routes it to an NPC and raises the script level to at least 3 | [bin] (protocol/v4x-clients.md#server--client-ids); [bin] (protocol/v5x-clients.md#server--client-ids-500r7) |
| 194 | `PLO_CLEARWEAPONS` | empty; precedes the weapon list | 4.20r8 clears its weapon and class script lists; 5.00r7 clears every loaded level and the level caches | [srv] (protocol/packet-ids.md#server--client-plo_); [bin] (protocol/v4x-clients.md#server--client-ids); [bin] (protocol/v5x-clients.md#server--client-ids-500r7) |
| 195 | `PLO_LOADGANI` | `str gani`, then the gani text | loaded as a server-sent gani script | [srv] (protocol/packet-ids.md#server--client-plo_); [bin] (protocol/v4x-clients.md#server--client-ids) |
| 196 | (no gs2lib name) | as 193 | 4.20r8 reads it and does nothing else | [bin] (protocol/v4x-clients.md#server--client-ids) |
| 197 | `PLO_LOADSCRIPT` | a list `type,name,saveToDisk,desKey,crc32`; type weapon, npc, class or gani; the key is two `i5` | script delivery (→ §8) | [srv] (protocol/packet-ids.md#server--client-plo_); [bin] (protocol/v5x-clients.md#server--client-ids-500r7) |

| Rule | Builds | Source |
| --- | --- | --- |
| For v4 and later clients the server replaces the script prop with `NPCPROP_CLASS` and sends GS2 bytecode; 2.05 never sees that path | server | [srv] (protocol/packet-layouts.md#weapons) |

## 2.5.7 Files and update packages

The download sequence, sizes and failure handling are in → §2.7.

| Id | Name | Layout | Client action | Source |
| ---: | --- | --- | --- | --- |
| 30 | `PLO_FILESENDFAILED` | unmeasured | unmeasured | [srv] (protocol/packet-ids.md#server--client-plo_) |
| 45 | `PLO_FILEUPTODATE` | unmeasured | unmeasured | [srv] (protocol/packet-ids.md#server--client-plo_) |
| 68 | `PLO_LARGEFILESTART` | `rest` = file name | stores the name; 2.31 also clears the stored size | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 69 | `PLO_LARGEFILEEND` | `rest` = file name | if it equals the stored name, the accumulated stream is processed as one received file | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 84 | `PLO_LARGEFILESIZE` | `i5 size` | stored | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 102 | `PLO_FILE` | behind 100 (→ §2.7) | a received file | [srv] (protocol/codec-and-framing.md#raw-data-escape) |
| 105 | `PLO_UPDATEPACKAGESIZE` | package name and an `i5` size | sets a size or modification time on a cached object | [bin] (protocol/v4x-clients.md#server--client-ids); [bin] (protocol/v5x-clients.md#server--client-ids-500r7) |
| 106 | `PLO_UPDATEPACKAGEDONE` | unmeasured | fires `onUpdatePackageDownloaded`, and `onPackagesDownloadComplete` after the last one; 4.20r8 restarts itself when its own executable was in a package | [bin] (protocol/v4x-clients.md#server--client-ids); [bin] (protocol/v5x-clients.md#server--client-ids-500r7) |
| 109 | `PLO_UNKNOWN109` | `i5` time, then a `c`-length string A and a `c`-length string B | passes (B, A, time) to the file layer; most likely a file redirect | [bin][inf] (protocol/v6x-clients.md#server--client-ids-601-603) |
| 111 | `PLO_SETNETCOOKIE` | `rest`, no fields | written byte for byte to `creationtime.dat` in the client's folder, replacing it; nothing is sent back | [bin][inf] (protocol/v6x-clients.md#server--client-ids-601-603) |
| 187 | `PLO_UPDATEPACKAGEISUPDATED` | unmeasured | a package-update message | [srv] (protocol/packet-ids.md#server--client-plo_) |
| 198 | `PLO_SERVEROPTIONS` | `i5` value | stored on the connection; nothing else in 6.03 reads it | [bin] (protocol/v6x-clients.md#server--client-ids-601-603) |

## 2.5.8 Messages, windows and modes

Chat display and the private-message rules are in → §2.8.

| Id | Name | Layout | Client action | Source |
| ---: | --- | --- | --- | --- |
| 13 | `PLO_TOALL` | `s player id, str message` | shown as a toall message | [srv][2.05] (protocol/chat-pm-rc.md#toall) |
| 32 | `PLO_SHOWIMGPLAYER` | `s sender id` + the sender's id 24 payload, relayed unchanged | no visible reaction to any tested payload (→ §2.4.9) | [cap] (protocol/packet-ids.md#server--client-plo_); [cap] (version-profiles/lab-showimg24-relay.tsv) |
| 35 | `PLO_RC_ADMINMESSAGE` | `rest` = `Admin <account>:` + `0xA7` + text | shown as an admin message | [srv][2.05] (protocol/chat-pm-rc.md#admin-and-staff) |
| 37 | `PLO_PRIVATEMESSAGE` | `s from id`, `rest` = `"type","message"` as a quoted comma list; type is a label such as `"Server Message:"` or empty | shown as a PM | [srv][2.05] (protocol/chat-pm-rc.md#private-messages) |
| 41 | `PLO_STARTMESSAGE` | `rest` = RTF or HTML text | trimmed and stored as `servermessage.rtf` or `servermessage.html`; if it differs from the stored copy it is rewritten and shown in the start-message viewer | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 47 | `PLO_STAFFGUILDS` | comma text, `"guild",` repeated | stored as the staff-guild list; sent at login | [srv][2.05] (protocol/chat-pm-rc.md#admin-and-staff); [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 75 | `PLO_PROFILE` | repeated `c n` + n bytes (trimmed); field 0 = account | delivered to the open profile window of that player, or the best match in the player list; 2.05 needs at least 10 fields (→ §2.8) | [bin] (version-profiles/plo-layouts-217-231.tsv); [2.05] (protocol/chat-pm-rc.md#profiles) |
| 82 | `PLO_SERVERTEXT` | unmeasured | the reply to `PLI_REQUESTTEXT` and `PLI_SENDTEXT`; 3.153 raises it to script as `receivetext`; 5.00r7 also feeds the buddy list with it | [srv] (protocol/packet-ids.md#server--client-plo_); [bin] (protocol/v3x-clients.md#server--client-ids-handled); [bin][inf] (protocol/v5x-clients.md#server--client-ids-500r7) |
| 153 | `PLO_SAY2` | `rest` = text; `0xA7` = newline | shown as an NPC sign message; signs use it too | [srv][2.05] (protocol/packet-layouts.md#player-state-server--client); [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 169 | `PLO_UPGRADEURL` | `rest` = URL | stored; with a disconnect, the reconnect button becomes "Upgrade" and opens it | [bin] (protocol/packet-ids.md#server--client-plo_) |
| 171 | `PLO_BIGMAP` | comma text `txt,png,x,y`; at least 4 fields are used; x and y as floats | the big map | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 172 | `PLO_MINIMAP` | as 171 | the minimap | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 176 | `PLO_KINGDOMSMODE` | empty | switches the client to Kingdoms mode | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 177 | `PLO_NEWWORLDMODE` | empty | switches the client to New World mode | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 178 | `PLO_SERVERWARP` | comma text, at least 4 fields: 0 unused, 1 server name, 2 host, 3 port | see the rules below | [bin][cap] (version-profiles/plo-layouts-217-231.tsv); [cap] (version-profiles/lab-serverwarp178.tsv) |
| 179 | `PLO_RPGWINDOW` | `rest` = text | creates the RPG window on first use and gives it the text | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 180 | `PLO_STATUSLIST` | `rest` = text | passed to the status-list window if it exists | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 182 | `PLO_LISTPROCESSES` | empty | the client answers with `PLI_PROCESSLIST` (44); 4.20r8 lists the titles of all open windows | [bin] (version-profiles/plo-layouts-217-231.tsv); [bin] (protocol/v4x-clients.md#server--client-ids) |
| 183 | `PLO_HASPROCESSRUNNING` | `rest` = names | the client answers with `PLI_PROCESSRUNNING` (45): 1 if the string occurs in its own list, else 0 | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 184 | `PLO_TAKESCREENSHOT` | `rest` = file name | accepted only with a `.png` extension; saves a screenshot under the screenshots folder; sends nothing back | [bin] (version-profiles/plo-layouts-217-231.tsv) |
| 190 | `PLO_SERVERLISTCONNECTED` | unmeasured | fires `onServerListerConnect`: the `Login` server has accepted the session (→ §2.3) | [bin] (protocol/v4x-clients.md#server--client-ids); [bin] (protocol/v5x-clients.md#server--client-ids-500r7) |
| 108 | `PLO_UNKNOWN108` | a subtype, then data | 4.20r6 and 4.20r8: subtype 0 makes the client answer with id 162 (→ App. E#5); subtype 1 stores a value on the connection | [bin] (protocol/v4x-clients.md#server--client-ids) |
| 104 | `PLO_UNKNOWN104` | `str data` holding `c`, `i5`, `i5` | unmeasured | [srv] (protocol/packet-ids.md#server--client-plo_) |

| Rule | Builds | Source |
| --- | --- | --- |
| On 178 the client closes the old connection and connects to the host in field 2 and the port in field 3 with a fresh login (new key, same stored credentials), with no listserver step | 2.31 (lab) | [cap] (version-profiles/plo-layouts-217-231.tsv); [cap] (version-profiles/lab-serverwarp178.tsv); [cap] (client-internals/decomp-findings-2026-10-24-b/08-lab-findings-levelchange-24-178.md#c-plo_serverwarp-178) |
| Field 1 of 178 is not needed: a bogus name still connects; a decoy host in field 0 is never contacted | 2.31 (lab) | [cap] (version-profiles/lab-serverwarp178.tsv) |
| With host and port in other positions the client makes no connection, closes the old one and shows "The connection couldn't be established!"; with three fields it does nothing | 2.31 (lab) | [cap] (version-profiles/lab-serverwarp178.tsv) |
| The old connection closes 2 to 3 ms before the new connection's SYN | 2.31 (lab) | [cap] (version-profiles/lab-serverwarp178.tsv) |
| 178 is split by the client's comma-text reader: white space (bytes 1 to 0x20) before an item is skipped; a quoted item ends at its closing quote, two quotes in a row are one quote, and an unclosed quote runs to the end; an unquoted item ends at a comma or a byte of 0x20 or less; a comma at the very end adds no item, an empty item between commas is kept; a NUL ends the text | 2.17.1, 2.22, 2.31 | [bin] (client-internals/decomp-findings-2026-10-25-g/comma-text-rules.tsv) |
| So a server name with a space must be quoted: `x,Main Server,h,1` reads as five items and connects to the host `Server` | 2.17.1, 2.22, 2.31 | [bin] (client-internals/decomp-findings-2026-10-25-g/03-id178-comma-text.md#the-splitter) |
| Item 1 becomes the current server's name, without a two-character type prefix when its second character is a space; 2.31 also puts it in the window caption, alone if it contains "graal" in any case, else after `Graal: `; the name is not used to connect | 2.17.1 to 2.31; caption 2.31 | [bin] (client-internals/decomp-findings-2026-10-25-g/03-id178-comma-text.md#the-connect-routine) |
| A real service's 178 text, item 0 in particular, has never been captured | all | [doc] (client-internals/decomp-findings-2026-10-25-g/04-open-points.md) |
| 182 and 183 are a process scan used as an anti-cheat check (→ §4.10) | 5.00r7 | [bin][inf] (protocol/v5x-clients.md#server--client-ids-500r7) |

## 2.5.9 Staff and NPC-control messages

The RC ids (50 to 54, 57 to 59, 61 to 67, 70 to 74, 76, 77, 103) and the NC ids (78, 80, 157 to 164, 167, 188, 192) are documented with the staff tools in → §7. Game clients handle a few of them:

| Id | Name | Builds | Use in a game client | Source |
| ---: | --- | --- | --- | --- |
| 67 | `PLO_RC_FILEBROWSER_MESSAGE` | 3.153, 4.x, 5.00r7, 6.x | raised to script as a folder-log event | [bin] (protocol/v3x-clients.md#server--client-ids-handled) |
| 74 | `PLO_RC_CHAT` | 3.153, 4.x, 5.00r7, 6.x | raised to script as an RC-chat event | [bin] (protocol/v3x-clients.md#server--client-ids-handled) |
| 79 | `PLO_NPCSERVERADDR` | none in the notes | two bytes (0, 2), then `host,port` text; 5.x ignores it | [srv] (protocol/packet-ids.md#server--client-plo_) |

## 2.5.10 Other ids

| Id | Name | Layout | Client action | Source |
| ---: | --- | --- | --- | --- |
| 60 | `PLO_UNKNOWN60` | unmeasured | ignored by 5.07 and later | [srv] (protocol/packet-ids.md#server--client-plo_) |
| 81 | `PLO_UNKNOWN81` | unmeasured | ignored by 5.07 and later | [srv] (protocol/packet-ids.md#server--client-plo_) |
| 83 | `PLO_UNKNOWN83` | unmeasured | ignored by 5.07 and later | [srv] (protocol/packet-ids.md#server--client-plo_) |
| 110 | `PLO_UNKNOWN110` | unmeasured | ignored by clients | [srv] (protocol/packet-ids.md#server--client-plo_) |
| 124 | `PLO_UNKNOWN124` | unmeasured | seen by RC3; possibly player flags (untested) | [srv] (protocol/packet-ids.md#server--client-plo_) |
| 132 | `PLO_UNKNOWN132` | unmeasured | 5.07 only; 6.037 ignores it; 3.153 uses it for script and class registration | [srv] (protocol/packet-ids.md#server--client-plo_); [bin] (protocol/v3x-clients.md#server--client-ids-handled) |
| 252 | `PLO_SET_ENC_KEY` | sets the AES or RC4 key and IV; above 223, so not sendable as one GCHAR (→ §2.10) | unmeasured | [srv] (protocol/packet-ids.md#server--client-plo_) |
| 253 | `PLO_BUNDLE` | several messages in one (→ §2.10) | unmeasured | [srv] (protocol/packet-ids.md#server--client-plo_) |
