# 7.x protocol notes

Cleaned observations from the 7.x native plugin. No addresses.

## Framing

Each connection supports two modes.

### Classic gen-5
- 2-byte big-endian length; `0xFFFF` escape + 4-byte length for large payloads.
- 1-byte compression tag (raw, zlib, or bzip2).
- LCG XOR: `state = state * 0x08088405 + key`, seed `0x04A80B38`.
- XOR window is limited (tens of bytes).
- `PLO_RAWDATA` (100) sets an exact length for the next packet.

### Server-defined
Activated by a header template string. Four big-endian fields:

| Field | Role |
|-------|------|
| Sequence | Incrementing; mismatch disconnects |
| Total length | Header + payload |
| Opcode | Packet ID |
| Compression | Low nibble: 0 raw, 1 zlib, 2 secondary |

A designated container opcode recursively unpacks its payload as more packets.

### Extra cipher
Optional full-stream layer (RC4 or AES-CBC) keyed from a handshake. AES pads with `0xFF` to 16-byte blocks.

## Remapping

Wire IDs can be reassigned at runtime. Defaults are the classic numbers below.

- Incoming: wire opcode → handler index (0–94), or `0xFE` script-only, `0xFD` container, `0xFC` marker, `0xFF` clear.
- Outgoing: logical slot → wire ID. Slot `0xFE` means do not send; give to script.

A server that never remaps uses the classic IDs.

## PLO (server → client) — classic IDs

| ID | Name | Payload sketch |
|---:|------|----------------|
| 0 | LEVELBOARD | Board / tile data |
| 1 | LEVELLINK | Link definition |
| 2 | BADDYPROPS | Baddy id + props |
| 3 | NPCPROPS | NPC id + props |
| 4 | LEVELCHEST | Chest / horse / bush |
| 5 | LEVELSIGN | x, y + text |
| 6 | LEVELNAME | Set level context |
| 7 | BOARDMODIFY | Optional layer + x,y,w,h + tiles |
| 8 | OTHERPLPROPS | Other player props |
| 9 | PLAYERWARP | x, y + level |
| 10 | BOMBADD | Bomb |
| 11 | BOMBDEL | Remove bomb |
| 12 | TOALL | Chat |
| 13 | PLAYERPROPS | Local player props |
| 14 | NPCDEL | Delete global NPC |
| 15 | RC_ADMINMESSAGE | Dialog text |
| 16 | HURTPLAYER | Hurt (vector) |
| 17 | EXPLOSION | Explosion |
| 18 | PRIVATEMESSAGE | PM |
| 19 | NPCWEAPONDEL | Remove weapon |
| 20 | LEVELMODTIME | Level cache write |
| 21 | PACKETCOUNT | Mode + value |
| 22 | WEAPONADD | Classic weapon |
| 23 | FILE | File data |
| 24 | Baddy hurt | Id + delta + power |
| 25 | Push / slide | 2× offset |
| 26 | NPC bytecode | NPC id + GS2 bytecode |
| 27 | BADDYADD | Baddy |
| 28 | FLAGSET | Flag |
| 29 | NPCDEL2 | Delete level NPC |
| 30 | FILESENDFAILED | File not found |
| 31 | Open chest | x, y |
| 32 | Carry / lift | Player id |
| 33 | NPCWEAPONADD | Length-prefixed weapon |
| 34 | RC_CHAT | RC console |
| 37 | THROWCARRIED | Throw |
| 38 | ITEMADD | Floor item |
| 39 | ITEMDEL | Remove floor item |
| 40 | Hurt (position) | Attacker, power, x, y |
| 41 | ARROWADD | Arrow / dart |
| 42 | Inventory item | Item index |
| 47 | FILEUPTODATE | File verified |
| 48 | Move NPC | NPC warp |
| 49 | Staff guilds | Comma list |
| 50 | TRIGGERACTION | Triggeraction |
| 51 | PLAYERWARP2 | Warp with z / gmap |
| 54 | FREEZEPLAYER2 | Freeze (600 ticks) |
| 55 | UNFREEZEPLAYER | Unfreeze |
| 67 | NEWWORLDTIME | Server time |
| 68 | LARGEFILESTART | Large download start |
| 69 | LARGEFILEEND | Large download end |
| 100 | RAWDATA | Exact length of next packet |
| 104 | ENCFILEKEY | Per-file key |
| 105 | CLEARLOCALNPCS | Clear local NPCs |
| 131 | GANI script | Gani name + body |
| 134 | Clear + load board | Reset objects, load board |
| 140 | TILEDEF | Tile definition |
| 151 | LARGEFILESIZE | Large file size |
| 152 | SERVERTEXT | category,cmd,sub,params |
| 156 | SETACTIVELEVEL | Active level / gmap |
| 160 | Hide login overlay | — |
| 169 | NPC waypoints | NPC id + path |
| 172 | Status / ghost | Status code |
| 175 | GANI attributes | Gani name + attrs |
| 178 | Server switch | Hand-off text |
| 182 | Full process list | Request process list |
| 183 | Check process | Search string |
| 189 | PACKAGESIZE | Package expected size |
| 190 | PACKAGEDONE | Package complete |
| 191 | SHOOT / SHOOT2 | Shoot |
| 192 | GMAPBOARDMODIFY | Gmap board modify |
| 193 | TERRAINHEIGHTS | 9×9 heights |
| 194 | URLFILE | HTTP redirect |
| 195 | CODEHEADER | Compiled script header |
| 196 | CODEBODY | Compiled script body |
| 197 | RETRYFILE | Retry file |
| 198 | SERVEROPTIONS | Server options |
| 199 | Status icons | Playerlist icon suffixes |

## PLI (client → server) — classic IDs

| Classic ID | Name | Payload sketch |
|-----------:|------|----------------|
| 0 | LEVELWARP | Login line or level + coords |
| 1 | BOARDMODIFY / CRC | crc + filename, or board modify |
| 2 | PLAYERPROPS | Local prop stream |
| 3 | Chat / toall | len + text (max 220) |
| 4 | ARROWADD / BOMBADD | coords + flags |
| 5 | BOMBDEL | coords |
| 6 | Language / toall | string |
| 7 | HORSEADD | coords + type |
| 8 | THROWCARRIED | packed byte |
| 9 | ITEMADD | coords + item |
| 10 | ITEMTAKE | coords + item |
| 11 | HURTPLAYER | victim + delta + power |
| 12 | EXPLOSION | coords + radius/flags |
| 14 | OTHERPLPROPS style | player or npc id |
| 15 | Ping / BADDYPROPS | empty or string |
| 16 | BADDYHURT | id + delta + power |
| 17 | OPENCHEST | x, y |
| 18 | PUTNPC / pos | 2× byte |
| 19 | NPCPROPS text | string |
| 20 | NPCDEL | npc id or name |
| 21 | BADDYADD | string |
| 23 | WANTFILE | filename |
| 24 | SHOWIMG / download | strings |
| 26 | WEAPONADD | name |
| 27 | WEAPONDEL | name |
| 28 | PRIVATEMESSAGE | count + ids + message |
| 31 | TRIGGERACTION | npc id + coords + action + params |
| 32 | MAPINFO | two strings |
| 33 | Savelog | two strings |
| 35 | LEVELWARPMOD / LEVELCHECK | modtime + coords + level |
| 36 | FLAGSET / CLIENTFLAGSET | string |
| 37 | CLIENTFLAGSET | client.… |
| 39 | Process check / list | flag + string or list |
| 50 | RAWDATA / ping | single ! |
| 57 / 159 | SHOOT / SHOOT2 | offsets + tile + angle/z/speed + gani |
| 96 | VERIFYWANTSEND | modtime + filename |
| 101 | LARGEFILESTART | filename |
| 102 | LARGEFILEEND | filename |
| 103 | FILEDATA upload | filename + chunk (≤32 KB; 20 MB cap) |
| 152 | SERVERTEXT | comma-joined |
| 158 | UPDATEFILE / PACKAGECHECK | crc + filename |
| 162 | Ping / reply | ! + short |

Coordinate bytes use the usual biased form (`*2` or `*2+0.5`).
