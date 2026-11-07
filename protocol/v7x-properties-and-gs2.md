# 7.x properties and GS2

Cleaned observations. No addresses.

## Player properties (PLPROP 0–82)

| ID | Name | Wire format | Notes |
|----|------|-------------|-------|
| 0 | NICKNAME | GCHAR(len) + str | Nickname + guild. Outgoing max 200. |
| 1 | MAXPOWER | GCHAR | Max hearts |
| 2 | CURPOWER | GCHAR(hp * 2) | Current hearts |
| 3 | RUPEESCOUNT | GINT3 | Rupees |
| 4 | ARROWSCOUNT | GCHAR | Arrows |
| 5 | BOMBSCOUNT | GCHAR | Bombs |
| 6 | GLOVEPOWER | GCHAR | Glove power |
| 7 | BOMBPOWER | GCHAR | Bomb power |
| 8 | SWORDPOWER | GCHAR(pow) [+ len + img] | ≤9 standard; >9 = pow−30 + image |
| 9 | SHIELDPOWER | GCHAR(pow) [+ len + img] | ≤9 standard; >9 = pow−10 + image |
| 10 | GANI | GCHAR(len) + gani[,param] | Animation |
| 11 | HEADGIF | GCHAR(id_or_len) [+ str] | <100 = headN; ≥100 = custom |
| 12 | CURCHAT | GCHAR(len) + str | Chat text |
| 13 | COLORS | 5 × GCHAR | Body colors |
| 14 | ID | GSHORT | Player ID |
| 15 | X | GCHAR(x * 2) | Half-tile X |
| 16 | Y | GCHAR(y * 2) | Half-tile Y |
| 17 | SPRITE / DIR | GCHAR | Dir = val & 3; sprite = val >> 2 |
| 18 | STATUS | GCHAR(bitmask) | Paused, hidden, dead, etc. |
| 19 | CARRYSPRITE | GCHAR | Carried object type |
| 20 | CURLEVEL | GCHAR(len) + str | Level filename |
| 21 | HORSEGIF | GCHAR(len) + str | Horse / mount |
| 22 | HORSEBUSHES | GCHAR | Horse counter |
| 23 | EFFECTCOLORS | GCHAR [+ 4B] | Legacy |
| 24 | CARRYNPC | 3 bytes | Skipped |
| 25 | APCOUNTER | GSHORT | Local |
| 26 | MAGICPOINTS | GCHAR | 0–100 |
| 27–29 | KILLS/DEATHS/ONLINESECS | GINT3 | Local |
| 30 | IPADDR | GINT5 | IP / ID |
| 31 | UDPPORT | 3 bytes | Consumed |
| 32 | ALIGNMENT | GCHAR | 0–100 |
| 33 | ADDITFLAGS | GCHAR | Flags |
| 34 | ACCOUNTNAME | GCHAR(len) + str | Account |
| 35 | BODYIMG | GCHAR(len) + str | Body image |
| 36 | RATING | 3 bytes | Rating + deviation |
| 37–41 | GATTRIB1..5 | GCHAR(len) + str | attr[1..5] |
| 42 | ATTACHNPC | GCHAR + GINT3 | Attach |
| 43 | GMAPLEVELX | GCHAR | GMAP X |
| 44 | GMAPLEVELY | GCHAR | GMAP Y |
| 45 | Z | GCHAR(z + 50) | Z height |
| 46–49 | GATTRIB6..9 | GCHAR(len) + str | attr[6..9] |
| 50 | JOINLEAVELVL | GCHAR | 0 left, 1 entered |
| 51 | PCONNECTED | (0 bytes) | Disconnected |
| 52 | PLLANGUAGE | GCHAR(len) + str | Language |
| 53 | PSTATUSMSG | GCHAR | Status icon |
| 54–73 | GATTRIB10..29 | GCHAR(len) + str | attr[10..29] |
| 74 | GATTRIB30 | GCHAR(len) + str | attr[30] |
| 75 | OSTYPE | GCHAR(len) + str | OS / secondary |
| 76 | TEXTCODEPAGE | GINT3 | Default 1250 |
| 77 | UNKNOWN77 | — | Reserved |
| 78 | X2 | GSHORT(x * 16) | High-precision X |
| 79 | Y2 | GSHORT(y * 16) | High-precision Y |
| 80 | Z2 | GSHORT(z * 16) | High-precision Z |
| 81 | GMAPFLAGS | GCHAR | Bit 0 = hide guild |
| 82 | COMMUNITYNAME | GCHAR(len) + str | Display name |

## NPC properties (NPCPROP 0–77)

| ID | Name | Wire format | Notes |
|----|------|-------------|-------|
| 0 | IMAGE | GCHAR(len) + str | `#c#` = character mode |
| 1 | SCRIPT | GSHORT(len) + str | Client script |
| 2 | X | GCHAR(x * 2) | Half-tile |
| 3 | Y | GCHAR(y * 2) | Half-tile |
| 4 | POWER | GCHAR(hp * 2) | Hearts |
| 5 | RUPEES | GINT3 | — |
| 6 | ARROWS | GCHAR | — |
| 7 | BOMBS | GCHAR | — |
| 8 | GLOVEPOWER | GCHAR | — |
| 9 | BOMBPOWER | GCHAR | — |
| 10 | SWORDGIF | GCHAR [+ img] | ≤9 or custom |
| 11 | SHIELDGIF | GCHAR [+ img] | ≤9 or custom |
| 12 | GANI | GCHAR(len) + str | Animation |
| 13 | VISFLAGS | GCHAR | Visible, draw order, block |
| 14 | BLOCKFLAGS | GCHAR | — |
| 15 | MESSAGE | GCHAR(len) + str | Max 200 |
| 16 | HURTDXDY | 2 × GCHAR | Knockback |
| 17 | ID | GINT3 | Skipped |
| 18 | SPRITE / DIR | GCHAR | Dir & sprite |
| 19 | COLORS | 5 × GCHAR | — |
| 20 | NICKNAME | GCHAR(len) + str | — |
| 21 | HORSEGIF | GCHAR(len) + str | — |
| 22 | HEADGIF | GCHAR [+ str] | <100 = headN |
| 23–32 | SAVE0..9 | 10 × GCHAR | — |
| 33 | ALIGNMENT | GCHAR | 0–100 |
| 34 | IMAGEPART | 6 bytes | Crop rect |
| 35 | BODYIMG | GCHAR(len) + str | — |
| 36–40 | GATTRIB1..5 | GCHAR(len) + str | — |
| 41 | GMAPLEVELX | GCHAR | — |
| 42 | GMAPLEVELY | GCHAR | — |
| 43 | Z | GCHAR(z + 50) | — |
| 44–47 | GATTRIB6..9 | GCHAR(len) + str | — |
| 48–52 | (unhandled) | — | Ends loop |
| 53–73 | GATTRIB10..30 | GCHAR(len) + str | — |
| 74 | CLASS | GSHORT(len) + bytes | Compiled script |
| 75 | X2 | GSHORT(x * 16) | High-precision |
| 76 | Y2 | GSHORT(y * 16) | High-precision |
| 77 | Z2 | GSHORT(z * 16) | High-precision |

## Baddy properties (BDPROP 0–10)

| ID | Name | Wire format |
|----|------|-------------|
| 0 | ID | GCHAR |
| 1 | X | GCHAR(x * 2) |
| 2 | Y | GCHAR(y * 2) |
| 3 | TYPE | GCHAR |
| 4 | POWERIMAGE | GCHAR(hp) + len + img |
| 5 | MODE | GCHAR (9 = dead) |
| 6 | ANICOUNT | GCHAR |
| 7 | DIR | GCHAR (body & 3, walk >> 2) |
| 8 | VERSESIGHT | GCHAR(len) + str |
| 9 | VERSEHURT | GCHAR(len) + str |
| 10 | VERSEATTACK | GCHAR(len) + str |

## showimg sub-properties (0–8)

Record starts with index+10 (−1 = full sync). Then:

| Tag | Format |
|-----|--------|
| 0 | len + name (0 deletes) |
| 1 | x |
| 2 | y |
| 3 | layer + 1 |
| 4 | space or `!` + crop |
| 5 | 4 × rgba |
| 6 | zoom |
| 7 | z + 50 |
| 8 | dir |

## GRESCR01 cache

Compiled weapon/class scripts cached with magic `GRESCR01`.

- PLO 195: type, name, modtime, 64-bit DES key, CRC32.
- On mismatch or missing file, client requests the body.
- Body is DES-ECB encrypted in 8-byte blocks.
- PLO 196 delivers the bytecode; client writes the cache and loads the plaintext.

## GS2 container

Big-endian TLV after decryption:

| Section | Content |
|---------|---------|
| 1 | 4-byte event bitmask |
| 2 | Function table (index + name; `public.` / `on*`) |
| 3 | String constant pool |
| 4 | Instruction stream (40-byte slots) |

Operand prefixes 0xF0–0xF6: string-pool index (u8/u16/u32), immediate (s8/s16/s32), or ASCII float.

## GS2 opcodes (ranges)

| Range | Category |
|-------|----------|
| 0x01–0x05 | Jumps |
| 0x06 | Call |
| 0x14, 0x16 | Push number / string |
| 0x1E–0x25 | Stack and type coercion |
| 0x2D–0x2F | Variable resolution |
| 0x32 | Assign |
| 0x34–0x35 | Inc / dec |
| 0x3C–0x41 | Arithmetic |
| 0x42–0x45 | Logic / unary |
| 0x46–0x4B | Compare |
| 0x4C–0x4F | Bitwise |
| 0x50–0x52 | Membership |
| 0x53 | type() |
| 0x55–0x5F | Math builtins |
| 0x61–0x62 | vecx / vecy |
| 0x65–0x66 | Shifts |
| 0x67, 0x6E–0x79 | Strings |
| 0x82–0x8E | Arrays |
| 0x96–0x97 | with |
| 0xA3 | foreach |
| 0xB4–0xBE | Built-in objects |
| 0xC8–0xF2 | Peephole superinstructions |

Limits: event queue 1000, string 64 MB, setarray 10 000, security level check on overwrite.
