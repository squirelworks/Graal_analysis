<!-- manual: kind=reference status=draft -->
# 2.6 Props

Props are the typed fields of players, NPCs and baddies. The messages that carry them are in → §2.4.4 and → §2.5; field types are in → §0.6. Every prop id is indexed in → App. B.

> Status: draft.

## 2.6.1 Prop streams

| Rule | Builds | Source |
| --- | --- | --- |
| A prop stream is `(c id, value)*` running to the end of the message, with no length per prop | all binary generations | [srv] (protocol/player-props.md) |
| Streams appear in `PLI_PLAYERPROPS` (2), `PLO_PLAYERPROPS` (9, the local player, no prefix), `PLO_OTHERPLPROPS` (8, `s player id` first), `PLO_NPCPROPS` (3, `i3 npc id` first), `PLO_BADDYPROPS` (2, `c baddy id` first) and, for NPC props, `PLO_NPCWEAPONADD` (33) | server; 2.05 | [srv] (protocol/player-props.md); [2.05] (protocol/player-props.md#unknown-prop-ids-205-checked-against-222-and-231) |
| A reader must know the encoding of every id up to the highest it expects, since nothing marks where a prop ends | all | [srv] (protocol/player-props.md) |
| Each client parser is a loop over `(id, value)` with a switch on the id; an id the switch does not know ends the loop, the rest of the message is ignored, and props already applied stay applied | 2.05, 2.22, 2.31 | [2.05][2.22][2.31] (protocol/player-props.md#unknown-prop-ids-205-checked-against-222-and-231) |
| An unknown id therefore cannot crash these clients, but one unknown prop placed early hides every prop after it | 2.05, 2.22, 2.31 | [2.05] (protocol/player-props.md#unknown-prop-ids-205-checked-against-222-and-231) |
| The other-player stream checks the remaining length before multi-byte props and clamps string lengths; the self stream does not length-check the fixed-size props 3, 13, 14 and 24, so a truncated one reads a few bytes of garbage before the loop ends | 2.05 | [2.05] (protocol/player-props.md#unknown-prop-ids-205-checked-against-222-and-231) |
| The self stream needs at least 2 bytes left to start a prop; a lone trailing id byte is dropped | 2.00, 2.05 | [bin] (version-profiles/plo-playerprops-layouts.tsv) |
| The other-player prefix is two 7-bit bytes, `(b0 − 0x20) × 0x80 + (b1 − 0x20)`; an unknown id creates the player record | 2.00 to 2.31 | [bin] (version-profiles/plo-otherplprops-layouts.tsv) |
| The NPC prefix is three 7-bit bytes; the handler needs more than 2 bytes; ids below 1000 are level NPCs, 1000 and up server-wide | 2.00 to 2.31 | [bin] (version-profiles/plo-npcprops-layouts.tsv) |

## 2.6.2 PLPROP (player)

Encodings use the short names of → §0.6; `c(v + k)` means the value plus *k*, sent as a GCHAR.

| Id | Name | Encoding | Notes | Source |
| ---: | --- | --- | --- | --- |
| 0 | NICKNAME | str | — | [srv] (protocol/player-props.md#plprop-player) |
| 1 | MAXPOWER | c | heart containers | [srv] (protocol/player-props.md#plprop-player) |
| 2 | CURPOWER | c | hearts × 2 | [srv] (protocol/player-props.md#plprop-player) |
| 3 | RUPEESCOUNT | i3 | gralats | [srv] (protocol/player-props.md#plprop-player) |
| 4 | ARROWSCOUNT | c | — | [srv] (protocol/player-props.md#plprop-player) |
| 5 | BOMBSCOUNT | c | — | [srv] (protocol/player-props.md#plprop-player) |
| 6 | GLOVEPOWER | c | — | [srv] (protocol/player-props.md#plprop-player) |
| 7 | BOMBPOWER | c | — | [srv] (protocol/player-props.md#plprop-player) |
| 8 | SWORDPOWER | c(power + 30) + str(image) | — | [srv] (protocol/player-props.md#plprop-player) |
| 9 | SHIELDPOWER | c(power + 10) + str(image) | — | [srv] (protocol/player-props.md#plprop-player) |
| 10 | GANI / BOWGIF | str (≥ 2.1) · pre-2.1: c(10 + len) + image, or c(bowpower) if no image | **2.05 uses the pre-2.1 form** | [srv][inf] (protocol/player-props.md#plprop-player) |
| 11 | HEADGIF | c(len + 100) + image | — | [srv] (protocol/player-props.md#plprop-player) |
| 12 | CURCHAT | str | chat bubble text | [srv] (protocol/player-props.md#plprop-player) |
| 13 | COLORS | 5 × c | colour indexes in the order skin, coat, sleeves, shoes, belt (→ §2.6.3) | [srv] (protocol/player-props.md#plprop-player) |
| 14 | ID | s | — | [srv] (protocol/player-props.md#plprop-player) |
| 15 | X | c(x × 2) | half-tile | [srv] (protocol/player-props.md#plprop-player) |
| 16 | Y | c(y × 2) | — | [srv] (protocol/player-props.md#plprop-player) |
| 17 | SPRITE | c | `% 4` = direction | [srv] (protocol/player-props.md#plprop-player) |
| 18 | STATUS | c | bit flags, see below | [srv] (protocol/player-props.md#plprop-player) |
| 19 | CARRYSPRITE | c | — | [srv] (protocol/player-props.md#plprop-player) |
| 20 | CURLEVEL | str | gmap name when on a gmap | [srv] (protocol/player-props.md#plprop-player) |
| 21 | HORSEGIF | str | — | [srv] (protocol/player-props.md#plprop-player) |
| 22 | HORSEBUSHES | c | — | [srv] (protocol/player-props.md#plprop-player) |
| 23 | EFFECTCOLORS | c | server always sends 0 | [srv] (protocol/player-props.md#plprop-player) |
| 24 | CARRYNPC | i3 | npc id | [srv] (protocol/player-props.md#plprop-player) |
| 25 | APCOUNTER | s(+1) | — | [srv] (protocol/player-props.md#plprop-player) |
| 26 | MAGICPOINTS | c | — | [srv] (protocol/player-props.md#plprop-player) |
| 27 | KILLSCOUNT | i3 | — | [srv] (protocol/player-props.md#plprop-player) |
| 28 | DEATHSCOUNT | i3 | — | [srv] (protocol/player-props.md#plprop-player) |
| 29 | ONLINESECS | i3 | — | [srv] (protocol/player-props.md#plprop-player) |
| 30 | IPADDR | i5 | — | [srv] (protocol/player-props.md#plprop-player) |
| 31 | UDPPORT | i3 | — | [srv] (protocol/player-props.md#plprop-player) |
| 32 | ALIGNMENT | c | AP 0–100 | [srv] (protocol/player-props.md#plprop-player) |
| 33 | ADDITFLAGS | c | — | [srv] (protocol/player-props.md#plprop-player) |
| 34 | ACCOUNTNAME | str | — | [srv] (protocol/player-props.md#plprop-player) |
| 35 | BODYIMG | str | — | [srv] (protocol/player-props.md#plprop-player) |
| 36 | RATING | i3 | `(rating & 0xFFF) << 9 \| (deviation & 0x1FF)` | [srv] (protocol/player-props.md#plprop-player) |
| 37–41 | GATTRIB1–5 | str (≤ 223) | — | [srv] (protocol/player-props.md#plprop-player) |
| 42 | ATTACHNPC | c(type, 0 = npc) + i3(id) | — | [srv] (protocol/player-props.md#plprop-player) |
| 43 / 44 | GMAPLEVELX / Y | c | — | [srv] (protocol/player-props.md#plprop-player) |
| 45 | Z | c(z + 0.5 + 50) | — | [srv] (protocol/player-props.md#plprop-player) |
| 46–49 | GATTRIB6–9 | str | — | [srv] (protocol/player-props.md#plprop-player) |
| 50 | JOINLEAVELVL | c | 1 join, 0 leave | [srv] (protocol/player-props.md#plprop-player) |
| 51 | PCONNECTED | — | no payload; marks disconnect | [srv] (protocol/player-props.md#plprop-player) |
| 52 | PLANGUAGE | str | — | [srv] (protocol/player-props.md#plprop-player) |
| 53 | PSTATUSMSG | c | index into the server's status list | [srv] (protocol/player-props.md#plprop-player) |
| 54–74 | GATTRIB10–30 | str | — | [srv] (protocol/player-props.md#plprop-player) |
| 75 | OSTYPE | str | 2.19+ (`wind`) | [srv] (protocol/player-props.md#plprop-player) |
| 76 | TEXTCODEPAGE | i3 | 2.19+ | [srv] (protocol/player-props.md#plprop-player) |
| 77 | UNKNOWN77 | ? | no client checked parses it (2.05, 2.22, 2.31); sending it aborts the rest of the stream | [srv][2.05][2.22][2.31] (protocol/player-props.md#plprop-player) |
| 78–80 | X2 / Y2 / Z2 | s: `abs(v × 16) << 1`, low bit = sign | pixel precision, newer clients only | [srv] (protocol/player-props.md#plprop-player) |
| 81 | UNKNOWN81 | c | player-list tab flag (unconfirmed). Above the highest id that 2.31 parses (80), so 2.31 and older stop reading at it | [srv][2.31] (protocol/player-props.md#plprop-player) |
| 82 | COMMUNITYNAME | str | — | [srv] (protocol/player-props.md#plprop-player) |

### 2.6.2.1 STATUS bits (prop 18)

| Bit | Meaning | Source |
| --- | --- | --- |
| `0x01` | paused | [srv] (protocol/player-props.md#status-bits-prop-18-srv) |
| `0x02` | hidden | [srv] (protocol/player-props.md#status-bits-prop-18-srv) |
| `0x04` | male | [srv] (protocol/player-props.md#status-bits-prop-18-srv) |
| `0x08` | dead | [srv] (protocol/player-props.md#status-bits-prop-18-srv) |
| `0x10` | allow weapons | [srv] (protocol/player-props.md#status-bits-prop-18-srv) |
| `0x20` | hide sword | [srv] (protocol/player-props.md#status-bits-prop-18-srv) |
| `0x40` | has spin attack | [srv] (protocol/player-props.md#status-bits-prop-18-srv) |

### 2.6.2.2 ADDITFLAGS bits (prop 33)

| Bit | Meaning | Source |
| --- | --- | --- |
| `0x01` | no mass message | [srv] (protocol/player-props.md#additflags-srv) |
| `0x02` | only show one level | [srv] (protocol/player-props.md#additflags-srv) |
| `0x04` | no toall | [srv] (protocol/player-props.md#additflags-srv) |
| `0x08` | voice disabled | [srv] (protocol/player-props.md#additflags-srv) |

### 2.6.2.3 Encodings as 2.05 reads them

| Prop | Rule | Source |
| --- | --- | --- |
| 8 SWORDPOWER | 0–4 = the default `sword<n>.gif`; otherwise power + 30, then `str` image | [2.05] (protocol/player-props.md#205-coverage-update-2026-10-21-205) |
| 9 SHIELDPOWER | 0–3 = the defaults; otherwise power + 10, then `str` image | [2.05] (protocol/player-props.md#205-coverage-update-2026-10-21-205) |
| 10 | the bow image or weapon (pre-2.1 BOWGIF), not GANI | [2.05] (protocol/player-props.md#205-coverage-update-2026-10-21-205) |
| 11 HEADGIF | `c n` below 100 → `head<n>.gif`; otherwise `c (len + 100)` + name, at most 100 bytes | [2.05] (protocol/player-props.md#205-coverage-update-2026-10-21-205) |
| 15, 16 X, Y | one GCHAR each, half-tiles | [2.05] (protocol/player-props.md#205-coverage-update-2026-10-21-205) |
| 17 SPRITE | direction + 4 × animation index; `0x80` in one special state | [2.05] (protocol/player-props.md#205-coverage-update-2026-10-21-205) |
| 19 CARRYSPRITE | −1 none, 0, 200, 201, or tile-based values | [2.05] (protocol/player-props.md#205-coverage-update-2026-10-21-205) |
| 30, 31 IPADDR, UDPPORT | feed the UDP peer channel (→ §2.9) | [2.05] (protocol/player-props.md#205-coverage-update-2026-10-21-205) |
| 36 RATING | rating = `b0 × 32 + ((b1 & 0x7F) >> 2)`, deviation = `(b1 & 3) × 128 + b2` | [2.05] (protocol/player-props.md#205-coverage-update-2026-10-21-205) |
| 51 PCONNECTED | no payload, but 2.05 skips one byte after it; harmless because the player is removed at once, but a server should put no props behind it | [2.05] (protocol/player-props.md#205-coverage-update-2026-10-21-205) |
| 7, 23 | sent as constants: bomb power `*` (10) and effect colours 0 | [2.05] (protocol/player-props.md#205-coverage-update-2026-10-21-205) |

## 2.6.3 Body colours and attributes

| Rule | Builds | Source |
| --- | --- | --- |
| A body picture is a palette image; before drawing, palette entry 5 takes the skin colour, 6 the coat, 4 the sleeves, 3 the shoes and 1 the belt; entry 0 always takes colour 18 (black, the outline) | 2.05 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| The five colours of prop 13 are in the order skin, coat, sleeves, shoes, belt | 2.05 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| The stock bodies follow that palette layout, and entry 2 is the clear colour | 2.22 files | [file] (client-internals/body-colours-and-attributes.md#body-colours) |
| A new player is orange, darkred, black, darkred, black (2, 5, 18, 5, 18), with `body.png` and `head0.gif`; GServer-v2 gives a new account 2, 0, 10, 4, 18 instead | 2.05; server | [2.05][srv] (client-internals/body-colours-and-attributes.md#body-colours) |
| A GANI sprite whose picture is `ATTR1` to `ATTR5` draws the player's attribute 1 to 5, which are props 37 to 41; 2.05 reads them for other players too | 2.05 | [2.05] (client-internals/body-colours-and-attributes.md#gani-attributes) |
| A player with no attribute of their own draws the GANI's `DEFAULTATTR1` to `DEFAULTATTR5`; the stock `idle.gani` names `hat0.png` as attribute 1 | 2.22 files | [file] (client-internals/body-colours-and-attributes.md#gani-attributes) |
| GANI attribute props are strings that GANI `PARAM`/`ATTR` placeholders resolve against; 2.05 sends and receives GATTRIB1–5 but its expression table has no `gattrib` entry | 2.05 | [inf][2.05] (protocol/packet-layouts.md#gani) |
| On the wire, animation is only a prop: `PLPROP_GANI` (10) and `NPCPROP_GANI` (12) carry the GANI name, and the client fetches the file with `PLI_WANTFILE` | server | [srv] (protocol/packet-layouts.md#gani) |

| Index | Colour | RGB | Source |
| ---: | --- | --- | --- |
| 0 | white | 255, 255, 255 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 1 | yellow | 255, 255, 0 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 2 | orange | 255, 173, 107 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 3 | pink | 255, 132, 132 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 4 | red | 255, 0, 0 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 5 | darkred | 206, 24, 41 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 6 | lightgreen | 132, 255, 132 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 7 | green | 0, 255, 0 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 8 | darkgreen | 0, 198, 0 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 9 | lightblue | 132, 132, 255 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 10 | blue | 0, 0, 255 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 11 | darkblue | 0, 0, 198 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 12 | brown | 132, 0, 0 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 13 | cynober | 0, 255, 255 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 14 | purple | 255, 0, 255 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 15 | darkpurple | 132, 0, 132 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 16 | lightgray | 206, 206, 206 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 17 | gray | 132, 132, 132 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 18 | black | 0, 0, 8 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |
| 19 | transparent | 0, 0, 0 | [2.05] (client-internals/body-colours-and-attributes.md#body-colours) |

The looks commands that change these props are GS1 behaviour (→ §8).

## 2.6.4 NPCPROP

| Id | Name | Encoding | Source |
| ---: | --- | --- | --- |
| 0 | IMAGE | str | [srv] (protocol/player-props.md#npcprop) |
| 1 | SCRIPT | s(len ≤ 0x3FFF) + text | [srv] (protocol/player-props.md#npcprop) |
| 2 | X | c(px / 8) = half-tiles | [srv] (protocol/player-props.md#npcprop) |
| 3 | Y | c(px / 8) | [srv] (protocol/player-props.md#npcprop) |
| 4 | POWER | c | [srv] (protocol/player-props.md#npcprop) |
| 5 | RUPEES | i3 | [srv] (protocol/player-props.md#npcprop) |
| 6 | ARROWS | c | [srv] (protocol/player-props.md#npcprop) |
| 7 | BOMBS | c | [srv] (protocol/player-props.md#npcprop) |
| 8 | GLOVEPOWER | c | [srv] (protocol/player-props.md#npcprop) |
| 9 | BOMBPOWER | c | [srv] (protocol/player-props.md#npcprop) |
| 10 | SWORDIMAGE | c(power + 30) + str, or c(0) | [srv] (protocol/player-props.md#npcprop) |
| 11 | SHIELDIMAGE | c(power + 10) + str, or c(0) | [srv] (protocol/player-props.md#npcprop) |
| 12 | GANI / BOWGIF | str | [srv] (protocol/player-props.md#npcprop) |
| 13 | VISFLAGS | c | [srv] (protocol/player-props.md#npcprop) |
| 14 | BLOCKFLAGS | c | [srv] (protocol/player-props.md#npcprop) |
| 15 | MESSAGE | str | [srv] (protocol/player-props.md#npcprop) |
| 16 | HURTDXDY | c(dx × 32 + 32), c(dy × 32 + 32) | [srv] (protocol/player-props.md#npcprop) |
| 17 | ID | i3 | [srv] (protocol/player-props.md#npcprop) |
| 18 | SPRITE | c (pre-2.x clients get `% 4`) | [srv] (protocol/player-props.md#npcprop) |
| 19 | COLORS | 5 × c | [srv] (protocol/player-props.md#npcprop) |
| 20 | NICKNAME | str | [srv] (protocol/player-props.md#npcprop) |
| 21 | HORSEIMAGE | str | [srv] (protocol/player-props.md#npcprop) |
| 22 | HEADIMAGE | c(len + 100) + image | [srv] (protocol/player-props.md#npcprop) |
| 23–32 | SAVE0–9 | c each | [srv] (protocol/player-props.md#npcprop) |
| 33 | ALIGNMENT | c | [srv] (protocol/player-props.md#npcprop) |
| 34 | IMAGEPART | `s x, s y, c w, c h` (x, y clamped to 0–16000, w, h to 0–220) | [srv][2.05] (protocol/player-props.md#npcprop) |
| 35 | BODYIMAGE | str | [srv] (protocol/player-props.md#npcprop) |
| 36–40 | GATTRIB1–5 | str | [srv] (protocol/player-props.md#npcprop) |
| 41 / 42 | GMAPLEVELX / Y | c | [srv] (protocol/player-props.md#npcprop) |
| 43 | Z | c(z + 50), z −50..170 (2.22, 2.31) | [srv][2.22] (protocol/player-props.md#npcprop) |
| 44–47 | GATTRIB6–9 | str | [srv] (protocol/player-props.md#npcprop) |
| 48 | UNKNOWN48 | not parsed by 2.05, 2.22 or 2.31; aborts the stream | [srv][2.22][2.31] (protocol/player-props.md#npcprop) |
| 49–52 | SCRIPTER, NAME, TYPE, CURLEVEL | str | [srv] (protocol/player-props.md#npcprop) |
| 53–73 | GATTRIB10–30 | str | [srv] (protocol/player-props.md#npcprop) |
| 74 | CLASS | NPC-server class | [srv] (protocol/player-props.md#npcprop) |
| 75 / 76 | X2 / Y2 | as PLPROP X2/Y2 | [srv] (protocol/player-props.md#npcprop) |
| 77 | Z2 | 2 bytes, decoded like X2/Y2; sets the same Z (2.31) | [srv][2.31] (protocol/player-props.md#npcprop) |

| Rule | Builds | Source |
| --- | --- | --- |
| The SCRIPT prop (1) carries GS1 source text, not bytecode, for pre-4.0 clients | server; 2.05 | [srv][2.05] (protocol/player-props.md#npcprop) |
| SCRIPT is applied only while the NPC has no script yet; a second SCRIPT for the same NPC is ignored | 2.05 | [2.05] (protocol/player-props.md#205-coverage-update-2026-10-21-205) |
| NPCPROP 43 is Z, `c (z + 50)` with z from −50 to 170, from 2.22 on; NPCPROP 77 is Z2 in 2.31 | 2.22, 2.31 | [2.22][2.31] (protocol/player-props.md#unknown-prop-ids-205-checked-against-222-and-231) |

## 2.6.5 BDPROP (baddy)

| Id | Name | Encoding and notes | Source |
| ---: | --- | --- | --- |
| 0 | ID | — | [srv] (protocol/player-props.md#bdprop-baddy) |
| 1 / 2 | X / Y | c(tiles × 2) | [srv] (protocol/player-props.md#bdprop-baddy) |
| 3 | TYPE | 0 graysoldier … 9 dragon (see GS1 baddy names) | [srv] (protocol/player-props.md#bdprop-baddy) |
| 4 | POWERIMAGE | c(power) + str(image); an empty image means the default for the type | [srv][2.05] (protocol/player-props.md#bdprop-baddy) |
| 5 | MODE | 0 walk, 1 look, 2 hunt, 3 hurt, 4 bumped, 5 die, 6 swamp-shot, 7 hare-jump, 9 dead; the 2.22 docs add 8 spider-shoot. On mode 5 the server switches to 9 after 2 s | [srv][doc] (protocol/player-props.md#bdprop-baddy) |
| 6 | ANI | c | [srv] (protocol/player-props.md#bdprop-baddy) |
| 7 | DIR | c(a × 4 + b): two directions in one byte, `a = v >> 2`, `b = v & 3` (which one is the head is not traced) | [srv][2.05] (protocol/player-props.md#bdprop-baddy) |
| 8–10 | VERSESIGHT / VERSEHURT / VERSEATTACK | str each | [srv] (protocol/player-props.md#bdprop-baddy) |

The baddy verses come from the backslash-separated verse line of the level file (→ §3) [srv] (protocol/player-props.md#bdprop-baddy).

## 2.6.6 Ids each parser accepts

An id outside a parser's accepted set ends that message's stream (→ §2.6.1).

| Stream | Build | Accepted ids | Stops at | Source |
| --- | --- | --- | --- | --- |
| self (9) | 2.00 | 0–35; disputed → App. E#8 | 36 and up | [bin] (version-profiles/plo-playerprops-layouts.tsv) |
| self (9) | 2.04 | between the 2.00 and 2.05 sets; not re-read | unmeasured | [bin] (version-profiles/plo-playerprops-layouts.tsv) |
| self (9) | 2.05 | 0–42 | 43 and up, including 50 and 51 | [2.05] (protocol/player-props.md#unknown-prop-ids-205-checked-against-222-and-231) |
| self (9) | 2.17.1, 2.22 | through 74 | 50, 51, 53 | [bin] (version-profiles/plo-playerprops-layouts.tsv); [2.22] (protocol/player-props.md#unknown-prop-ids-205-checked-against-222-and-231) |
| self (9) | 2.31 | through 80, with X2, Y2, Z2 at 78–80 | 50, 51, 53, 75–77 | [2.31] (protocol/player-props.md#unknown-prop-ids-205-checked-against-222-and-231) |
| other players (8) | 2.00 | 0–35 | 36 and up | [bin] (version-profiles/plo-otherplprops-layouts.tsv) |
| other players (8) | 2.05 | 0, 2, 8–13, 15–21, 24, 30–42, 50, 51 | 1, 3–7, 14, 22, 23, 25–29, 43–49, 52 and up | [2.05] (protocol/player-props.md#unknown-prop-ids-205-checked-against-222-and-231) |
| other players (8) | 2.22 | highest 76 | 1, 3–7, 14, 22, 25–29 | [2.22] (protocol/player-props.md#unknown-prop-ids-205-checked-against-222-and-231) |
| other players (8) | 2.31 | 0, 2, 8–13, 15–21, 23, 24, 30–76, 78–80 | 1, 3–7, 14, 22, 25–29, 77 | [bin] (version-profiles/plo-otherplprops-layouts.tsv) |
| NPC (3, 33) | 2.00 | 0–36; disputed → App. E#8 | 37 and up | [bin] (version-profiles/plo-npcprops-layouts.tsv) |
| NPC (3, 33) | 2.05 | 0–40 | 41 and up | [2.05] (protocol/player-props.md#unknown-prop-ids-205-checked-against-222-and-231) |
| NPC (3) | 2.17.1 | 0–40, 44–47, 53–73 | 41–43, 48–52 | [bin] (version-profiles/plo-npcprops-layouts.tsv) |
| NPC (3) | 2.22 | highest 73, including 43 | 48–52 | [bin] (version-profiles/plo-npcprops-layouts.tsv); [2.22] (protocol/player-props.md#unknown-prop-ids-205-checked-against-222-and-231) |
| NPC (3) | 2.31 | highest 77 | 48–52 | [2.31] (protocol/player-props.md#unknown-prop-ids-205-checked-against-222-and-231) |
| baddy (2) | 2.05 | 0–10 | 11 and up | [2.05] (protocol/player-props.md#unknown-prop-ids-205-checked-against-222-and-231) |

| Rule | Builds | Source |
| --- | --- | --- |
| A server that sends a 2.05 client another player's MAXPOWER (1), RUPEES (3), ID (14), HORSEBUSHES (22) or a counter (25–29) loses every prop after it in that message; send those to the player only, or last | 2.05 | [2.05] (protocol/player-props.md#unknown-prop-ids-205-checked-against-222-and-231) |
| 2.05 knows PLPROP 0–42, 50 and 51 only; it sends 0–24, 26, 31–33, 35 and 37–42, and only receives 25, 27–30, 34, 36, 50 and 51 | 2.05 | [2.05] (protocol/player-props.md#205-coverage-update-2026-10-21-205) |
| 2.05 sends props 0, 11, 13, 18, 31 and 33 together at session start, and 42, 15, 16 together on attach or a move | 2.05 | [2.05] (protocol/player-props.md#plprop-player) |
| No client checked parses PLPROP 77 or 81, or NPCPROP 48 | 2.05, 2.22, 2.31 | [2.05][2.22][2.31] (protocol/player-props.md#unknown-prop-ids-205-checked-against-222-and-231) |
| The 2.22 send-side prop builder also knows 75 and 76 | 2.22 | [bin] (version-profiles/plo-playerprops-layouts.tsv) |
| From 2.3 GServer-v2 puts X2 and Y2 before X and Y in other-player props | server | [srv] (version-profiles/2.22-2.31.md#wire-protocol) |

Prop ranges for the 1.21 to 1.32 builds are in → App. C.6, and parser growth from 1.33 to the 2.1 tests in → App. C.3. Two notes disagree on the 2.00 ranges → App. E#8.
