# Player, NPC, and baddy properties

Date: 2026-10-21

Sources: GServer-v2 `TAccount.h`, `TPlayerProps.cpp`, `TNPC.h`/`TNPC.cpp`, `TLevelBaddy.h`/`.cpp` (GPLv3, summarized). Tags: **[srv]** server source · **[2.05]** confirmed in 2.05 · **[2.22]** / **[2.31]** read from that client's prop parser · **[inf]** inferred.

A prop stream is `(GCHAR id, value)*` running to the end of the message. It appears in `PLI_PLAYERPROPS` (2), `PLO_PLAYERPROPS` (9, self), `PLO_OTHERPLPROPS` (8, `GSHORT player id` + stream), `PLO_NPCPROPS` (3, `GINT3 npc id` + stream), and `PLO_BADDYPROPS` (2, `GCHAR baddy id` + stream). There is no length per prop, so a reader must know every id's encoding up to the highest id it expects. **[srv]**

Encodings: `c` = GCHAR, `s` = GSHORT, `i3` = GINT3, `i5` = GINT5, `str` = GSTRING.

## PLPROP (player)

| Id | Name | Encoding | Notes |
|---:|------|----------|-------|
| 0 | NICKNAME | str | |
| 1 | MAXPOWER | c | heart containers |
| 2 | CURPOWER | c | hearts × 2 |
| 3 | RUPEESCOUNT | i3 | gralats |
| 4 | ARROWSCOUNT | c | |
| 5 | BOMBSCOUNT | c | |
| 6 | GLOVEPOWER | c | |
| 7 | BOMBPOWER | c | |
| 8 | SWORDPOWER | c(power + 30) + str(image) | |
| 9 | SHIELDPOWER | c(power + 10) + str(image) | |
| 10 | GANI / BOWGIF | str (≥ 2.1) · pre-2.1: c(10 + len) + image, or c(bowpower) if no image | **2.05 uses the pre-2.1 form** [srv][inf] |
| 11 | HEADGIF | c(len + 100) + image | |
| 12 | CURCHAT | str | chat bubble text |
| 13 | COLORS | 5 × c | color-name indexes; order probably skin, coat, sleeves, shoes, belt (matches the GS1 `set*color` commands) [inf] |
| 14 | ID | s | |
| 15 | X | c(x × 2) | half-tile |
| 16 | Y | c(y × 2) | |
| 17 | SPRITE | c | `% 4` = direction |
| 18 | STATUS | c | bit flags, see below |
| 19 | CARRYSPRITE | c | |
| 20 | CURLEVEL | str | gmap name when on a gmap |
| 21 | HORSEGIF | str | |
| 22 | HORSEBUSHES | c | |
| 23 | EFFECTCOLORS | c | server always sends 0 |
| 24 | CARRYNPC | i3 | npc id |
| 25 | APCOUNTER | s(+1) | |
| 26 | MAGICPOINTS | c | |
| 27 | KILLSCOUNT | i3 | |
| 28 | DEATHSCOUNT | i3 | |
| 29 | ONLINESECS | i3 | |
| 30 | IPADDR | i5 | |
| 31 | UDPPORT | i3 | |
| 32 | ALIGNMENT | c | AP 0–100 |
| 33 | ADDITFLAGS | c | |
| 34 | ACCOUNTNAME | str | |
| 35 | BODYIMG | str | |
| 36 | RATING | i3 | `(rating & 0xFFF) << 9 \| (deviation & 0x1FF)` |
| 37–41 | GATTRIB1–5 | str (≤ 223) | |
| 42 | ATTACHNPC | c(type, 0 = npc) + i3(id) | |
| 43 / 44 | GMAPLEVELX / Y | c | |
| 45 | Z | c(z + 0.5 + 50) | |
| 46–49 | GATTRIB6–9 | str | |
| 50 | JOINLEAVELVL | c | 1 join, 0 leave |
| 51 | PCONNECTED | — | no payload; marks disconnect |
| 52 | PLANGUAGE | str | |
| 53 | PSTATUSMSG | c | index into the server's status list |
| 54–74 | GATTRIB10–30 | str | |
| 75 | OSTYPE | str | 2.19+ (`wind`) |
| 76 | TEXTCODEPAGE | i3 | 2.19+ |
| 77 | UNKNOWN77 | ? | no client checked parses it (2.05, 2.22, 2.31); sending it aborts the rest of the stream [2.05][2.22][2.31] |
| 78–80 | X2 / Y2 / Z2 | s: `abs(v × 16) << 1`, low bit = sign | pixel precision, newer clients only |
| 81 | UNKNOWN81 | c | player-list tab flag (unconfirmed). Above the highest id that 2.31 parses (80), so 2.31 and older stop reading at it [2.31] |
| 82 | COMMUNITYNAME | str | |

2.05 sends props 0, 11, 13, 18, 31, and 33 together at session start, and 42, 15, 16 together on attach or move. **[2.05]** Which ids 2.05 parses depends on the stream (see "Unknown prop ids" below). **[2.05]**

### STATUS bits (prop 18) **[srv]**
`0x01` paused · `0x02` hidden · `0x04` male · `0x08` dead · `0x10` allow weapons · `0x20` hide sword · `0x40` has spin attack.

### ADDITFLAGS **[srv]**
`0x01` no mass message · `0x02` only show one level · `0x04` no toall · `0x08` voice disabled.

## NPCPROP

| Id | Name | Encoding | Id | Name | Encoding |
|---:|------|----------|---:|------|----------|
| 0 | IMAGE | str | 18 | SPRITE | c (pre-2.x clients get `% 4`) |
| 1 | SCRIPT | s(len ≤ 0x3FFF) + text | 19 | COLORS | 5 × c |
| 2 | X | c(px / 8) = half-tiles | 20 | NICKNAME | str |
| 3 | Y | c(px / 8) | 21 | HORSEIMAGE | str |
| 4 | POWER | c | 22 | HEADIMAGE | c(len + 100) + image |
| 5 | RUPEES | i3 | 23–32 | SAVE0–9 | c each |
| 6 | ARROWS | c | 33 | ALIGNMENT | c |
| 7 | BOMBS | c | 34 | IMAGEPART | `s x, s y, c w, c h` (x, y clamped to 0–16000, w, h to 0–220) [2.05] |
| 8 | GLOVEPOWER | c | 35 | BODYIMAGE | str |
| 9 | BOMBPOWER | c | 36–40 | GATTRIB1–5 | str |
| 10 | SWORDIMAGE | c(power + 30) + str, or c(0) | 41 / 42 | GMAPLEVELX / Y | c |
| 11 | SHIELDIMAGE | c(power + 10) + str, or c(0) | 43 | Z | c(z + 50), z −50..170 (2.22, 2.31) [2.22] |
| 12 | GANI / BOWGIF | str | 44–47 | GATTRIB6–9 | str |
| 13 | VISFLAGS | c | 48 | UNKNOWN48 | not parsed by 2.05, 2.22 or 2.31; aborts the stream [2.22][2.31] |
| 14 | BLOCKFLAGS | c | 49–52 | SCRIPTER, NAME, TYPE, CURLEVEL | str |
| 15 | MESSAGE | str | 53–73 | GATTRIB10–30 | str |
| 16 | HURTDXDY | c(dx × 32 + 32), c(dy × 32 + 32) | 74 | CLASS | NPC-server class |
| 17 | ID | i3 | 75 / 76 | X2 / Y2 | as PLPROP X2/Y2 |
| | | | 77 | Z2 | 2 bytes, decoded like X2/Y2; sets the same Z (2.31) [2.31] |

The SCRIPT prop carries the GS1 source text, not bytecode, for pre-4.0 clients. 2.05 parses GS1 from text (see `npc-library/gs1-reference-205.md`). **[srv][2.05]**

## BDPROP (baddy)

| Id | Name | Notes |
|---:|------|-------|
| 0 | ID | |
| 1 / 2 | X / Y | c(tiles × 2) |
| 3 | TYPE | 0 graysoldier … 9 dragon (see GS1 baddy names) |
| 4 | POWERIMAGE | c(power) + str(image); an empty image means the default for the type [2.05] |
| 5 | MODE | 0 walk, 1 look, 2 hunt, 3 hurt, 4 bumped, 5 die, 6 swamp-shot, 7 hare-jump, 9 dead; the 2.22 docs add 8 spider-shoot. On mode 5 the server switches to 9 after 2 s |
| 6 | ANI | c |
| 7 | DIR | c(a × 4 + b): two directions in one byte, `a = v >> 2`, `b = v & 3` (which one is the head is not traced) [2.05] |
| 8–10 | VERSESIGHT / VERSEHURT / VERSEATTACK | str each |

The baddy verses come from the `\`-separated verse line in `.graal`/`.zelda` level files (see `formats/level-binary.md`). **[srv]**

## 2.05 coverage (update 2026-10-21) **[2.05]**

- 2.05 knows PLPROP **0–42, 50, 51** only, and not all of them in every stream (see below).
- **Sent by the client:** 0–24 (7 and 23 are constants: bomb power `*` = 10, effect colors 0), 26, 31, 32, 33, 35, 37–42. **Received only:** 25, 27–30, 34, 36, 50, 51.
- 10 = bow image / weapon (pre-2.1 BOWGIF), not GANI.
- 11 head: GCHAR n<100 → `head<n>.gif`; otherwise GCHAR(len+100) + name (≤100).
- 8 sword: 0–4 = default `sword<n>.gif`; otherwise power+30 then GSTRING image.
- 9 shield: 0–3 = defaults; otherwise power+10 then GSTRING image.
- 17 SPRITE = dir + 4 × animation index (GCHAR); 0x80 in one special state.
- 15/16 X/Y = one GCHAR each, half-tiles.
- 19 CARRYSPRITE: -1 none, 0, 200, 201, or tile-based values.
- 30 IPADDR (GINT5) and 31 UDPPORT (GINT3) feed the UDP peer channel (`udp-p2p.md`).
- 36 RATING (3 bytes) = rating `b0*32 + ((b1&0x7F)>>2)`, deviation `(b1&3)*128 + b2`.
- 37–41 GATTRIB1–5 (`#P1`–`#P5`) exist in 2.05.
- 51 PCONNECTED takes no payload, but 2.05 skips one byte after it. That is harmless because the player is removed straight after, but a server should not put other props behind it.
- NPCPROP 1 (SCRIPT) is applied only while the NPC has no script yet; a second SCRIPT for the same NPC is ignored.

## Unknown prop ids (2.05, checked against 2.22 and 2.31)

Every prop parser in 2.05 is a loop over `(id, value)` with a `switch` on the id. An id the switch does not know ends the loop: **the rest of the message is ignored**, and the props already applied stay applied. **[2.05]** 2.22 and 2.31 do the same. **[2.22][2.31]**

So an unknown id cannot crash these clients. The multi-byte props in the other-player stream check the remaining length first, and string props are copied with clamped lengths. The self stream does not length-check fixed-size props (3, 13, 14, 24), so a truncated one reads a few bytes of garbage, but the loop then ends. **[2.05]** The practical risk for a server is silent loss: one prop the client does not know, placed early, hides every prop after it.

Ids each 2.05 parser accepts **[2.05]**:

| Stream | Accepted ids | Stops at |
|--------|--------------|----------|
| PLAYERPROPS (9, self) | 0–42 | 43 and up, including 50/51. Needs at least 2 bytes left, so a lone trailing id byte is dropped |
| OTHERPLPROPS (8) | 0, 2, 8–13, 15–21, 24, 30–42, 50, 51 | **1, 3–7, 14, 22, 23, 25–29**, 43–49, 52 and up |
| NPCPROPS (3) and NPCWEAPONADD (33) | 0–40 | 41 and up (GMAPLEVELX/Y, Z, …) |
| BADDYPROPS (2) | 0–10 | 11 and up |

The OTHERPLPROPS row matters most: a server that sends a 2.05 client another player's MAXPOWER (1), RUPEES (3), ID (14), HORSEBUSHES (22) or a counter (25–29) loses every prop after it in that message. Send those to the player themself only, or put them last.

Highest ids parsed by later clients (from their switch tables): **[2.22][2.31]**

| Client | Self | Other players | NPC |
|--------|-----:|--------------:|----:|
| 2.22 | 74 (stops at 50, 51, 53) | 76 (stops at 1, 3–7, 14, 22, 25–29) | 73 (stops at 48–52) |
| 2.31 | 80 (stops at 50, 51, 53, 75–77) | 80 (stops at 1, 3–7, 14, 22, 25–29, 77) | 77 (stops at 48–52) |

No client checked knows PLPROP 77 or 81, or NPCPROP 48. NPCPROP 43 is Z (`c(z + 50)`, range −50..170) from 2.22 on, and NPCPROP 77 is Z2 in 2.31.

