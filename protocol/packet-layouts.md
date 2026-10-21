# Packet layouts

Date: 2026-10-14, revised 2026-10-21 (2.05 trace)

Sources: GServer-v2 `TLevel*.cpp`, `TPlayer.cpp`, `TWeapon.cpp` (GPLv3, summarized); client 2.05 rev 2 PLO dispatcher and PLI senders. Tags: **[srv]** server source · **[2.05]** read from the 2.05 receiver or sender · **[inf]**.

Notation: `c` GCHAR, `s` GSHORT, `i3` GINT3, `i4` GINT4, `i5` GINT5, `str` GSTRING (`c len` + bytes), `rest` = the rest of the message. `x×2` means the value is in half-tiles (the client divides by 2). Ids are logical, so add 0x20 for the wire byte. Ids and names are in `packet-ids.md`, prop encodings in `player-props.md`, UDP ids in `udp-p2p.md`.

## How 2.05 reads a message **[2.05]**
- Every handler checks a minimum length first and drops a short message silently. The minimums are given below where they matter.
- 2.05 keeps two level pointers. The **named level** is set by every LEVELNAME. The **object level** receives NPC packets (NPCPROPS, NPCDEL2, HIDENPCS, SHOWIMGNPC); SETACTIVELEVEL sets it, and without an NPC server each LEVELNAME sets it too.
- Handlers for level objects (bombs, arrows, items, explosions, hits, trigger actions, horses, push-away) only act when the player is standing in the named level.
- Packets that the server re-emits for another player start with `s player id`. With an unknown id, bombs, arrows, explosions and items are still shown (without an owner), while fire spy, throw carried and player hits are dropped.

## Level data (server → client)

| Id | Name | Layout | Tag |
|---:|------|--------|-----|
| 6 | LEVELNAME | rest = level filename. Sets the named level, and also the object level when there is no NPC server (no HASNPCSERVER) | [srv][2.05] |
| 100 → 101 | RAWDATA → BOARDPACKET | `i3(8194)`, then `c(101)` + 4096 × u16 **little-endian raw** tile ids + `\n` | [srv] |
| 0 | LEVELBOARD | a run of board changes, each `c x, c y, c w, c h` + w × h × `s tile` (row-major), back to back with no separator. Parsing stops when fewer than 4 bytes are left or a run is shorter than `w*h*2+4` (the rest is dropped). Empty = "use your cached board". If a warp to this level is pending, 2.05 completes the warp first and then applies the runs | [srv][2.05] |
| 7 | BOARDMODIFY | one run: `c x, c y, c w, c h` + w × h × `s tile`, row-major; needs `len ≥ w*h*2+4` | [srv][2.05] |
| 1 | LEVELLINK | rest = `"dest x y w h newx newy"`, split on spaces (`newx`/`newy` may be `playerx`/`playery`) | [srv][2.05] |
| 5 | LEVELSIGN | `c x, c y` (whole tiles) + sign-alphabet text (see `formats/sign-text.md`); needs ≥ 2 bytes | [srv][2.05] |
| 4 | LEVELCHEST | `c opened`, `c x`, `c y` (whole tiles); if not opened, also `c item`, `c signindex` (needs ≥ 5 bytes, else dropped) | [srv][2.05] |
| 2 | BADDYPROPS | `c id` + BDPROP stream. An unknown id creates the baddy | [srv][2.05] |
| 3 | NPCPROPS | `i3 id` + NPCPROP stream; needs id > 0. Ids below 1000 are level NPCs (created in the object level), 1000 and up are server-wide NPCs. A new NPC gets the `playerenters` event if the player is in that level | [srv][2.05] |
| 17 | HORSEADD | `c x×2, c y×2, c (dir & 3) + 4 × bushes` (bushes capped at 6) + rest = image (`.gif` is added if there is no extension) | [srv][2.05] |
| 18 | HORSEDEL | `c x×2, c y×2`; removes any horse within 2 tiles of that point | [2.05] |
| 22 | ITEMADD | `c x×2, c y×2, c item` (0–24, unknown items ignored). If the message is longer than 4 bytes, bytes 3–4 are `s player`: a dropped sword or shield then copies that player's image | [srv][2.05] |
| 23 | ITEMDEL | `c x×2, c y×2`; removes the item at exactly that point | [srv][2.05] |
| 39 | LEVELMODTIME | `i5 modtime`, exactly 5 bytes. 2.05 then writes the level to its web-level cache (`GWEBL001` format, see `formats/gwebl001-cache.md`) | [srv][2.05] |
| 10 | ISLEADER | empty: you run this level's baddies and timeouts. Ignored unless the player's level is the active level | [srv][2.05] |
| 42 | NEWWORLDTIME | `i4 time` (`b0<<21 \| b1<<14 \| b2<<7 \| b3`); needs ≥ 4 bytes | [srv][2.05] |
| 156 | SETACTIVELEVEL | rest = level that receives the following NPC packets (the object level) | [srv][2.05] |

### Pre-2.1 level sequence (`sendLevel141`, used for 2.05) **[srv]**
1. If the client's cached modtime matches: board changes since then, and nothing else.
2. Otherwise: `RAWDATA` + `BOARDPACKET`, then `LEVELNAME` (first level only), `LEVELLINK`×n, `LEVELSIGN`×n, `LEVELMODTIME`.
3. Then board changes, `LEVELCHEST`×n, `HORSEADD`×n, `BADDYPROPS`×n, `ISLEADER` (if leader), `NEWWORLDTIME`, `NPCPROPS`×n, and `OTHERPLPROPS` for each player in the level.

### Board modify correction
Earlier notes had `x:u8 y:u8 width:u8 height:u8 tiles:raw`. The header bytes are **GCHAR**s (+0x20), and each tile is a **GSHORT** (two 7-bit bytes, +0x20). Only `BOARDPACKET` (101) carries raw little-endian u16 tiles. **[srv]** The same shape is used client → server in `PLI_BOARDMODIFY` (1) for bush or sign pickups; 2.05 sends exactly one run. **[2.05]** The server rebroadcasts it as `PLO_BOARDMODIFY`.

### Board change on the wire **[cap]**
Lab capture, two 2.05 clients in one level (`tools/lab-setup.md`). Player B dropped a bomb next to a patch of bushes and grass.

1. **Bomb:**
   - B sent `PLI_BOMBADD` (4): `c x×2, c y×2, c owner_power, c fuse`. The values seen were x 78, y 28, `owner_power` 9 and fuse 55.
   - The server sends `PLO_BOMBADD` (11) to the other players: `s player id` followed by the same four bytes.
   - The 2.05 client writes the third byte as `power + 8`, where the 8 flag means "this bomb is mine". A receiver reads the power as `v & 7` and the owner flag from the value 8 (bit 3). So 9 is power 1 plus the owner flag. GServer's own reading, `(player << 2) | power`, does not match 2.05. **[2.05]** The fuse 55 is probably 0.05 s steps, about 2.75 s. **[inf]**
2. **Board change:**
   - When the bomb went off, **player A** sent eight `PLI_BOARDMODIFY` (1) messages in one frame, one per destroyed 2×2 patch. B, who owned the bomb, sent none. These sessions had no `ISLEADER`, so why A was the one to report is not settled. **[inf]**
   - Each message is `c x, c y, c w, c h` in whole tiles, then w × h GSHORT tile ids in row order. For example, x 39, y 14, 2 × 2, tiles 1834 1835 1850 1851 (a cut bush). A cut grass patch gave 677 678 693 694.
3. **Rebroadcast:**
   - In the same tick the server sent `PLO_BOARDMODIFY` (7) with exactly the same bytes to **both** clients, including the sender.
   - It interleaved them with its own `PLO_ITEMADD` (22) drops: `c x×2, c y×2, c item`, with items 1 and 4 seen. The drops come from the server, because `bushitems` was on. No client sent `PLI_ITEMADD`.
4. **Pickup:**
   - B walked over the drops and sent `PLI_ITEMDEL` (13): `c x×2, c y×2` for each.
   - The server sent `PLO_ITEMDEL` (23) to A only, not back to B.
5. **Respawn:**
   - Exactly 15.0 s after the change (`respawntime = 15`), the server sent `PLO_BOARDMODIFY` again for every patch, with the original tiles: bush 34 35 50 51, grass 2 3 18 19.
   - Clients do not request the respawn. It is pushed by the server.
6. **Level entry:** an empty `PLO_LEVELBOARD` (0) followed the board packet and `LEVELMODTIME` on level entry, as described above.

## Player state (server → client)

| Id | Name | Layout | Tag |
|---:|------|--------|-----|
| 9 | PLAYERPROPS | PLPROP stream (self) | [srv][2.05] |
| 8 | OTHERPLPROPS | `s id` + PLPROP stream; needs ≥ 2 bytes. An unknown id creates the player | [srv][2.05] |
| 14 | PLAYERWARP | `c x×2, c y×2` + rest = level. The warp stays pending until the level data arrives | [srv][2.05] |
| 15 | WARPFAILED | rest = level; 2.05 ignores the text and just shows a short failed-warp state | [srv][2.05] |
| 16 | DISCMESSAGE | rest = text, stored as the disconnect reason; the server then closes the connection | [srv][2.05] |
| 40 | HURTPLAYER | `s attacker` + `c dx, c dy, c power` [+ `i3 npc`]: see "Hits" below | [srv][2.05] |
| 38 | PUSHAWAY | `c dx, c dy`, each `v/16 − 4`; ignored unless the player's level is the active level | [srv][2.05] |
| 28 / 31 | FLAGSET / FLAGDEL | rest = `name` or `name=value`. FLAGSET adds a flag only if it is not already set | [srv][2.05] |
| 154 / 155 | FREEZEPLAYER2 / UNFREEZEPLAYER | empty. Freeze lasts 600 ticks unless unfrozen | [srv][2.05] |
| 153 | SAY2 | rest = text, `\xa7` = newline | [srv][2.05] |

## Combat and objects (both directions)

The client sends its own action. The server re-emits it to the rest of the level with `s player id` added in front. **[srv]** In 2.05 most of these also go peer to peer over UDP; the TCP copy is sent only when some player in the level has no UDP port, or when the server has an NPC server (HASNPCSERVER). See `udp-p2p.md`. **[2.05]** This rule covers these level-object packets only. Player props still go over TCP while UDP is active (seen in the lab captures, `tools/lab-setup.md`).

| PLI | PLO | Name | Client layout (PLI) | Server copy as 2.05 reads it (PLO) | Tag |
|----:|----:|------|---------------------|-----------------------------------|-----|
| 4 | 11 | BOMBADD | `c x×2, c y×2, c power (+8 = the bomb is the sender's), c fuse` | `s player` + the same 4 bytes; power = `v & 7`, value 8 (bit 3) = owned by that player | [srv][2.05] |
| 5 | 12 | BOMBDEL | `c x×2, c y×2` | **no player id**: `c x×2, c y×2`; removes the bomb at exactly that point | [srv][2.05] |
| 9 | 19 | ARROWADD | `c x×2, c y×2, c flags, c type`, then one byte sent as `v + 33` instead of `v + 32`; flags = `dir & 3`, +4 extra effect, +8 owned | `s player` + the same 5 bytes; needs ≥ 5 | [srv][2.05] |
| 10 | 20 | FIRESPY | `c (a × 8 + b)` | `s player` + that byte; the receiver uses only `a` | [srv][2.05] |
| 11 | 21 | THROWCARRIED | empty | `s player` only | [srv][2.05] |
| 26 | 40 | HURTPLAYER | `s victim, c (dx+4)×16, c (dy+4)×16, c power` [+ `i3 npc`] | `s attacker` + `c dx, c dy, c power` [+ `i3 npc`] | [srv][2.05] |
| 27 | 36 | EXPLOSION | `c radius, c x×2, c y×2, c power (+8 = the explosion is the sender's)` | `s player` + the same 4 bytes; power `& 7` clamped to 1–3, value 8 (bit 3) = owned | [srv][2.05] |
| 36 | 46 | HITOBJECTS | `c power×2, c x×2, c y×2` [+ `i3 npc`] | `s player` + the same bytes | [srv][2.05] |
| 15 | 2 | BADDYPROPS | rest = `c id` + BDPROP stream (passed through) | `c id` + BDPROP stream | [srv][2.05] |
| 16 | 27 | BADDYHURT | `c id, c (dx+4)×16, c (dy+4)×16, c power` | same; applied only by the level leader | [srv][2.05] |
| 17 | — | BADDYADD | `c x×2, c y×2, c type, c power` + rest = image | (the server answers with BADDYPROPS) | [srv][2.05] |
| 20 | 4 | OPENCHEST | `c x, c y` (whole tiles); server replies LEVELCHEST opened=1 | see LEVELCHEST | [srv][2.05] |
| 12 / 13 | 22 / 23 | ITEMADD / ITEMDEL | ITEMADD `c x×2, c y×2, c item`; ITEMDEL `c x×2, c y×2` | see the level table | [srv][2.05] |
| 32 | — | ITEMTAKE | `c x×2, c y×2, c item` | — | [2.05] |
| 38 | 48 | TRIGGERACTION | `i3 npc` (0 = none), `c x×2, c y×2` + rest = `action` or `action,params` | `s player` + the same; needs > 5 bytes | [srv][2.05] |

### Hits **[2.05]**
- **HURTPLAYER (40)**: `dx`, `dy` decode as `(v − 0x60) / 16` (knockback, −4..4) and `power` as `(v − 32) / 2` hearts, capped at 1.0. With 6 or more bytes after the player id, the hit came from an NPC (`i3`), and distance is measured from that NPC. The hit is applied only if the attacker (player or NPC) is within 10 tiles and the local player can be hurt at that moment.
- **HITOBJECTS (46)**: `power` is `(v − 32) / 2`, capped at 1.0, then `x`, `y` in half-tiles, and an optional `i3 npc`. It hurts the local player only when the player's centre is within 2 tiles of `(x, y)` in each axis.
- Both share one handler and one flag that picks the layout. The same handler also takes UDP id 21 (GS1 `hitplayer`).
- **TRIGGERACTION (48)** fires the `action` event on the local player's scripts only when the source (the NPC if `npc > 0`, else the sending player) is within 10 tiles. The split is at the first comma.

## Level navigation (client → server)

| Id | Name | Layout | Tag |
|---:|------|--------|-----|
| 0 | LEVELWARP | `c x×2, c y×2` + rest = level | [srv][2.05] |
| 30 | LEVELWARPMOD | `i5 modtime, c x×2, c y×2` + rest = level. 2.05 sends this instead of LEVELWARP when it has the level cached (in memory or in its web-level cache), so the server can answer with only the changes | [srv][2.05] |
| 35 | ADJACENTLEVEL | `i5 modtime` + rest = level (gmap preload). The modtime is all zeros when the level is not cached | [srv][2.05] |

In most states, a warp to the level the player is already in just moves the player and sends nothing. A real warp also sends UDP id 24 to gmap neighbours. **[2.05]**

## Other client → server senders **[2.05]**

| Id | Name | Layout |
|---:|------|--------|
| 2 / 3 | PLAYERPROPS / NPCPROPS | rest = prop stream (passed through) |
| 7 / 8 | HORSEADD / HORSEDEL | HORSEADD `c x×2, c y×2, c dir + 4 × bushes` + image filename; HORSEDEL `c x×2, c y×2` |
| 14 | CLAIMPKER | `s player id` |
| 18 / 19 | FLAGSET / FLAGDEL | rest = flag; flags that start with `local.` are never sent |
| 21 | PUTNPC | `str image`, `str script file`, `c x×2, c y×2` |
| 22 | NPCDEL | `i3 npc id` (only for NPCs with id > 0). If the NPC is one of the player's weapons, 2.05 sends NPCWEAPONDEL (29) with the weapon name instead |
| 23 | WANTFILE | rest = filename |
| 24 | SHOWIMG | rest (passed through; also UDP 15) |
| 34 | UPDATEFILE | `i5 modtime` + filename |
| 80 / 81 | PROFILEGET / PROFILESET | see `chat-pm-rc.md` |

## Weapons

| Id | Name | Layout | Tag |
|---:|------|--------|-----|
| PLO 33 | NPCWEAPONADD | `str name` + NPCPROP stream (normally `c 0 (IMAGE)` + `str image`, `c 1 (SCRIPT)` + `s len` + GS1 text). A name the player already has is ignored. The weapon gets the `playerenters` event | [srv][2.05] |
| PLO 34 | NPCWEAPONDEL | rest = name | [srv][2.05] |
| PLO 43 | DEFAULTWEAPON | `c item index` (0–24; built-in weapon: bow, bomb, sword, …) | [srv][2.05] |
| PLI 33 | WEAPONADD | `c type`: 0 → `c item index`; 1 → `i3 npc id` (copy an NPC's script as a weapon). **2.05 only sends type 0** | [srv][2.05] |
| PLI 29 | NPCWEAPONDEL | rest = name | [srv][2.05] |

For v4+ clients the script prop is replaced by `NPCPROP_CLASS` + `PLO_UNKNOWN197` (GS2 bytecode). 2.05 never sees that path. **[srv]**

## GANI

The GANI file format is in `formats/gani.txt`. On the wire, animation is only a prop: `PLPROP_GANI` (10) and `NPCPROP_GANI` (12) carry the GANI name, and the client fetches the file with `PLI_WANTFILE` like any other asset. Pre-2.1 clients (2.05) use slot 10 as BOWGIF. **[srv]** Gani attribute props (`PLPROP_GATTRIB*`) are strings that GANI `PARAM`/`ATTR` placeholders resolve against. **[inf]** 2.05 sends and receives GATTRIB1–5 (props 37–41, `#P1`–`#P5`), but its expression table has no `gattrib` entry. **[2.05]**

## Differences from GServer worth knowing **[2.05]**
- PLO BOMBDEL, HORSEDEL and ITEMDEL carry no player id. Only the coordinates are read.
- PLO HURTPLAYER and HITOBJECTS take an optional trailing `i3 npc`.
- The arrow's last byte is offset by 33 (decoded as `b − 33`), not a plain GCHAR.
- TRIGGERACTION coordinates are half-tiles, not whole tiles.
