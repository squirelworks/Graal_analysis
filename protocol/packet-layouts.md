# Packet layouts

Date: 2026-10-14, revised 2026-10-21

Sources: GServer-v2 `TLevel*.cpp`, `TPlayer.cpp`, `TWeapon.cpp` (GPLv3, summarized); 2.05 jump table. Tags: **[srv]** server source · **[2.05]** handler exists in 2.05 (layout not yet traced) · **[inf]**.

Notation: `c` GCHAR, `s` GSHORT, `i3` GINT3, `i5` GINT5, `str` GSTRING, `rest` = the rest of the message. Ids are logical, so add 0x20 for the wire byte. Ids and names are in `packet-ids.md`, prop encodings in `player-props.md`.

## Level data (server → client)

| Id | Name | Layout | Tag |
|---:|------|--------|-----|
| 6 | LEVELNAME | rest = level filename | [srv][2.05] |
| 100 → 101 | RAWDATA → BOARDPACKET | `i3(8194)`, then `c(101)` + 4096 × u16 **little-endian raw** tile ids + `\n` | [srv] |
| 0 | LEVELBOARD | empty = "use your cached board"; otherwise a run of board changes, same shape as 7 | [srv][2.05] |
| 7 | BOARDMODIFY | `c x, c y, c w, c h` + w × h × `s tile` | [srv][2.05] |
| 1 | LEVELLINK | rest = `"dest x y w h newx newy"` (space separated; `newx`/`newy` may be `playerx`/`playery`) | [srv][2.05] |
| 5 | LEVELSIGN | `c x, c y` + sign-alphabet text (see `formats/sign-text.md`) | [srv][2.05] |
| 4 | LEVELCHEST | `c opened(0/1), c x, c y` [+ `c item, c signindex` if not opened] | [srv][2.05] |
| 2 | BADDYPROPS | `c id` + BDPROP stream | [srv][2.05] |
| 3 | NPCPROPS | `i3 id` + NPCPROP stream | [srv][2.05] |
| 17 | HORSEADD | horse string (x, y, image, …) | [srv][2.05] |
| 22 / 23 | ITEMADD / ITEMDEL | `c x×2, c y×2, c item` | [srv][2.05] |
| 39 | LEVELMODTIME | `i5 modtime` | [srv][2.05] |
| 10 | ISLEADER | empty: you run this level's baddies and timeouts | [srv][2.05] |
| 42 | NEWWORLDTIME | `i4 time` | [srv][2.05] |
| 156 | SETACTIVELEVEL | rest = level that receives the following object packets | [srv][2.05] |

### Pre-2.1 level sequence (`sendLevel141`, used for 2.05) **[srv]**
1. If the client's cached modtime matches: board changes since then, and nothing else.
2. Otherwise: `RAWDATA` + `BOARDPACKET`, then `LEVELNAME` (first level only), `LEVELLINK`×n, `LEVELSIGN`×n, `LEVELMODTIME`.
3. Then board changes, `LEVELCHEST`×n, `HORSEADD`×n, `BADDYPROPS`×n, `ISLEADER` (if leader), `NEWWORLDTIME`, `NPCPROPS`×n, and `OTHERPLPROPS` for each player in the level.

### Board modify correction
Earlier notes had `x:u8 y:u8 width:u8 height:u8 tiles:raw`. The header bytes are **GCHAR**s (+0x20), and each tile is a **GSHORT** (two 7-bit bytes, +0x20). Only `BOARDPACKET` (101) carries raw little-endian u16 tiles. **[srv]** The same shape is used client → server in `PLI_BOARDMODIFY` (1) for bush or sign pickups. The server rebroadcasts it as `PLO_BOARDMODIFY`.

### Board change on the wire **[cap]**
Lab capture, two 2.05 clients in one level (`tools/lab-setup.md`). Player B dropped a bomb next to a patch of bushes and grass.

1. **Bomb:**
   - B sent `PLI_BOMBADD` (4): `c x×2, c y×2, c owner_power, c fuse`. The values seen were x 78, y 28, `owner_power` 9 and fuse 55.
   - The server sends `PLO_BOMBADD` (11) to the other players: `s player id` followed by the same four bytes.
   - In the server source the third byte is `(player << 2) | power`, and the fuse counts in 0.05 s steps, so 55 is about 2.75 s. **[srv][inf]**
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
| 8 | OTHERPLPROPS | `s id` + PLPROP stream | [srv][2.05] |
| 14 | PLAYERWARP | `c x×2, c y×2` + rest = level | [srv][2.05] |
| 15 | WARPFAILED | rest = level | [srv][2.05] |
| 16 | DISCMESSAGE | rest = text; the server then closes the connection | [srv][2.05] |
| 40 | HURTPLAYER | `s attacker, c dx, c dy, c power, i3 npc` | [srv][2.05] |
| 38 | PUSHAWAY | `c dx, c dy` (scaled `v × 0.0625 − 4`) | [srv][2.05] |
| 28 / 31 | FLAGSET / FLAGDEL | rest = `name` or `name=value` | [srv][2.05] |
| 154 / 155 | FREEZEPLAYER2 / UNFREEZEPLAYER | empty | [srv][2.05] |
| 153 | SAY2 | rest = text, `\xa7` = newline | [srv][2.05] |

## Combat and objects (both directions)

The client sends its own action. The server re-emits it to the rest of the level with `s player id` added in front. **[srv]**

| PLI | PLO | Name | Client layout | Tag |
|----:|----:|------|---------------|-----|
| 4 | 11 | BOMBADD | `c x×2, c y×2, c power, c fuse` (fuse in 0.05 s steps, default 55) | [srv][2.05] |
| 5 | 12 | BOMBDEL | same as add | [srv][2.05] |
| 9 | 19 | ARROWADD | x, y, dir (passed through) | [srv][2.05] |
| 10 | 20 | FIRESPY | passed through | [srv][2.05] |
| 11 | 21 | THROWCARRIED | passed through | [srv][2.05] |
| 26 | 40 | HURTPLAYER | `s victim, c dx, c dy, c power, i3 npc` | [srv][2.05] |
| 27 | 36 | EXPLOSION | `c radius, c x×2, c y×2, c power` | [srv][2.05] |
| 36 | 46 | HITOBJECTS | power, x, y [, npc] | [srv][2.05] |
| 15/16/17 | 2/27 | BADDYPROPS / HURT / ADD | `c id` + BDPROP stream | [srv][2.05] |
| 20 | 4 | OPENCHEST | `c x, c y`; server replies LEVELCHEST opened=1 | [srv][2.05] |
| 12 / 13 | 22 / 23 | ITEMADD / ITEMDEL | `c x×2, c y×2, c item` | [srv][2.05] |
| 38 | 48 | TRIGGERACTION | `i3 npc, c x×2, c y×2` + rest = `action,params` | [srv][2.05] |

## Level navigation (client → server)

| Id | Name | Layout | Tag |
|---:|------|--------|-----|
| 0 | LEVELWARP | `c x×2, c y×2` + rest = level | [srv][2.05] |
| 30 | LEVELWARPMOD | `i5 modtime, c x×2, c y×2` + rest = level | [srv][2.05] |
| 35 | ADJACENTLEVEL | `i5 modtime` + rest = level (gmap preload) | [srv][2.05] |

## Weapons

| Id | Name | Layout | Tag |
|---:|------|--------|-----|
| PLO 33 | NPCWEAPONADD | `str name`, `c 0 (NPCPROP_IMAGE)` + `str image`, `c 1 (NPCPROP_SCRIPT)` + `s len` + GS1 text | [srv][2.05] |
| PLO 34 | NPCWEAPONDEL | rest = name | [srv][2.05] |
| PLO 43 | DEFAULTWEAPON | `c item index` (built-in weapon: bow, bomb, sword, …) | [srv][2.05] |
| PLI 33 | WEAPONADD | `c type`: 0 → `c item index`; 1 → `i3 npc id` (copy an NPC's script as a weapon) | [srv][2.05] |
| PLI 29 | NPCWEAPONDEL | rest = name | [srv][2.05] |

For v4+ clients the script prop is replaced by `NPCPROP_CLASS` + `PLO_UNKNOWN197` (GS2 bytecode). 2.05 never sees that path. **[srv]**

## GANI

The GANI file format is in `formats/gani.txt`. On the wire, animation is only a prop: `PLPROP_GANI` (10) and `NPCPROP_GANI` (12) carry the GANI name, and the client fetches the file with `PLI_WANTFILE` like any other asset. Pre-2.1 clients (2.05) use slot 10 as BOWGIF. **[srv]** Gani attribute props (`PLPROP_GATTRIB*`) are strings that GANI `PARAM`/`ATTR` placeholders resolve against. **[inf]** 2.05 sends and receives GATTRIB1–5 (props 37–41, `#P1`–`#P5`), but its expression table has no `gattrib` entry. **[2.05]**
