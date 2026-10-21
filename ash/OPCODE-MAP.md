# Opcode map

Date: 2026-10-21

Full session-opcode table that `protocol/OPCODE-SUMMARY.md` points to. One row per packet id, using the gs2lib names from `protocol/packet-ids.md` (same ids and 2.05 coverage). The 39ster 2.1 column lists the older names that OPCODE-SUMMARY uses, where they differ. This file covers session packets only; GS1 script opcodes are in `npc-library/gs1-reference-205.md`.

Encoding: wire byte = id + 0x20. Each message is GCHAR id + payload + `\n`. Field types: `c` = GCHAR, `s` = GSHORT, `i3`/`i4`/`i5` = 3/4/5-byte G-ints, `str` = GCHAR length + bytes, "rest" = the remainder of the line. ×2 means half-tile units. See `protocol/codec-and-framing.md`.

2.05 column: **yes** = handled (S→C) or sent (C→S) by client 2.05 rev 2; **via 100** = only reachable behind `PLO_RAWDATA`; **—** = not present in 2.05. Payloads are from GServer-v2 / gs2lib source [srv] unless marked [inf]. Empty payload cells mean the layout is not documented in these notes yet.

## Client → server (PLI)

| Id | Wire | Name | 39ster 2.1 | Dir | Payload | 2.05 |
|---:|:----:|------|------------|:---:|---------|:----:|
| 0 | 0x20 | `PLI_LEVELWARP` |  | C→S | `c x×2, c y×2` + rest = level (byte 0 of the first line is the client type) | yes |
| 1 | 0x21 | `PLI_BOARDMODIFY` |  | C→S | `c x, c y, c w, c h` + w×h `s tile` | yes |
| 2 | 0x22 | `PLI_PLAYERPROPS` |  | C→S | PLPROP stream | yes |
| 3 | 0x23 | `PLI_NPCPROPS` |  | C→S | `i3 id` + NPCPROP stream | yes |
| 4 | 0x24 | `PLI_BOMBADD` | `ADDBOMB` | C→S | `c x×2, c y×2, c power, c fuse` | yes |
| 5 | 0x25 | `PLI_BOMBDEL` |  | C→S | as 4 | yes |
| 6 | 0x26 | `PLI_TOALL` |  | C→S | `str message` | — |
| 7 | 0x27 | `PLI_HORSEADD` |  | C→S | `c x×2, c y×2, c dir+4×bushes` + rest = image | yes |
| 8 | 0x28 | `PLI_HORSEDEL` |  | C→S | `c x×2, c y×2` | yes |
| 9 | 0x29 | `PLI_ARROWADD` |  | C→S | arrow: x, y, dir | yes |
| 10 | 0x2a | `PLI_FIRESPY` |  | C→S | fire spy | yes |
| 11 | 0x2b | `PLI_THROWCARRIED` |  | C→S | throw carried | yes |
| 12 | 0x2c | `PLI_ITEMADD` |  | C→S | `c x×2, c y×2, c item` | yes |
| 13 | 0x2d | `PLI_ITEMDEL` |  | C→S | `c x×2, c y×2, c item` | yes |
| 14 | 0x2e | `PLI_CLAIMPKER` |  | C→S | `s killer id` | yes |
| 15 | 0x2f | `PLI_BADDYPROPS` |  | C→S | `c id` + BDPROP stream | yes |
| 16 | 0x30 | `PLI_BADDYHURT` |  | C→S | `c id` + BDPROP stream | yes |
| 17 | 0x31 | `PLI_BADDYADD` |  | C→S | `c id` + BDPROP stream | yes |
| 18 | 0x32 | `PLI_FLAGSET` |  | C→S | rest = `name` or `name=value` | yes |
| 19 | 0x33 | `PLI_FLAGDEL` |  | C→S | rest = flag name | yes |
| 20 | 0x34 | `PLI_OPENCHEST` |  | C→S | `c x, c y` | yes |
| 21 | 0x35 | `PLI_PUTNPC` |  | C→S | `str image`, `str code`, `c x×2, c y×2` | yes |
| 22 | 0x36 | `PLI_NPCDEL` |  | C→S |  | yes |
| 23 | 0x37 | `PLI_WANTFILE` | `WANTGIF` | C→S | rest = filename | yes |
| 24 | 0x38 | `PLI_SHOWIMGPLAYER` |  | C→S |  | yes |
| 25 | 0x39 | `PLI_UNKNOWN25` |  | C→S |  | — |
| 26 | 0x3a | `PLI_HURTPLAYER` |  | C→S | `s victim, c dx, c dy, c power, i3 npc` | yes |
| 27 | 0x3b | `PLI_EXPLOSION` |  | C→S | `c radius, c x×2, c y×2, c power` | yes |
| 28 | 0x3c | `PLI_PRIVATEMESSAGE` |  | C→S | `s count`, count × `s id`, rest = message | yes |
| 29 | 0x3d | `PLI_NPCWEAPONDEL` |  | C→S | rest = weapon name | yes |
| 30 | 0x3e | `PLI_LEVELWARPMOD` | `MODLEVELWARP` | C→S | `i5 modtime, c x×2, c y×2` + rest = level | yes |
| 31 | 0x3f | `PLI_PACKETCOUNT` |  | C→S |  | — |
| 32 | 0x40 | `PLI_ITEMTAKE` |  | C→S |  | yes |
| 33 | 0x41 | `PLI_WEAPONADD` |  | C→S | `c type` + (`c item` | `i3 npc id`) | yes |
| 34 | 0x42 | `PLI_UPDATEFILE` |  | C→S | `i5 modtime` + rest = filename | yes |
| 35 | 0x43 | `PLI_ADJACENTLEVEL` |  | C→S | `i5 modtime` + rest = level | yes |
| 36 | 0x44 | `PLI_HITOBJECTS` |  | C→S | power, x, y [, npc] | yes |
| 37 | 0x45 | `PLI_LANGUAGE` |  | C→S | rest = language name | yes |
| 38 | 0x46 | `PLI_TRIGGERACTION` |  | C→S | `i3 npc, c x×2, c y×2` + rest = `action,params` | yes |
| 39 | 0x47 | `PLI_TAMPERCHECK` |  | C→S |  | — |
| 40 | 0x48 | `PLI_SHOOT` |  | C→S |  | — |
| 41 | 0x49 | `PLI_SERVERWARP` |  | C→S |  | — |
| 43 | 0x4b | `PLI_MUTEPLAYER` |  | C→S |  | — |
| 44 | 0x4c | `PLI_PROCESSLIST` |  | C→S |  | — |
| 45 | 0x4d | `PLI_PROCESSRUNNING` |  | C→S |  | — |
| 46 | 0x4e | `PLI_ENTERLEVEL` |  | C→S |  | — |
| 47 | 0x4f | `PLI_VERIFYWANTSEND` |  | C→S | `i5 crc32` + rest = filename | — |
| 48 | 0x50 | `PLI_SHOOT2` |  | C→S |  | — |
| 50 | 0x52 | `PLI_RAWDATA` |  | C→S |  | — |
| 51 | 0x53 | `PLI_RC_SERVEROPTIONSGET` |  | C→S |  | — |
| 52 | 0x54 | `PLI_RC_SERVEROPTIONSSET` |  | C→S |  | — |
| 53 | 0x55 | `PLI_RC_FOLDERCONFIGGET` |  | C→S |  | — |
| 54 | 0x56 | `PLI_RC_FOLDERCONFIGSET` |  | C→S |  | — |
| 55 | 0x57 | `PLI_RC_RESPAWNSET` |  | C→S |  | — |
| 56 | 0x58 | `PLI_RC_HORSELIFESET` |  | C→S |  | — |
| 57 | 0x59 | `PLI_RC_APINCREMENTSET` |  | C→S |  | — |
| 58 | 0x5a | `PLI_RC_BADDYRESPAWNSET` |  | C→S |  | — |
| 59 | 0x5b | `PLI_RC_PLAYERPROPSGET` |  | C→S |  | — |
| 60 | 0x5c | `PLI_RC_PLAYERPROPSSET` |  | C→S |  | — |
| 61 | 0x5d | `PLI_RC_DISCONNECTPLAYER` |  | C→S |  | — |
| 62 | 0x5e | `PLI_RC_UPDATELEVELS` |  | C→S |  | — |
| 63 | 0x5f | `PLI_RC_ADMINMESSAGE` |  | C→S |  | — |
| 64 | 0x60 | `PLI_RC_PRIVADMINMESSAGE` |  | C→S |  | — |
| 65 | 0x61 | `PLI_RC_LISTRCS` |  | C→S |  | — |
| 66 | 0x62 | `PLI_RC_DISCONNECTRC` |  | C→S |  | — |
| 67 | 0x63 | `PLI_RC_APPLYREASON` |  | C→S |  | — |
| 68 | 0x64 | `PLI_RC_SERVERFLAGSGET` |  | C→S |  | — |
| 69 | 0x65 | `PLI_RC_SERVERFLAGSSET` |  | C→S |  | — |
| 70 | 0x66 | `PLI_RC_ACCOUNTADD` |  | C→S |  | — |
| 71 | 0x67 | `PLI_RC_ACCOUNTDEL` |  | C→S |  | — |
| 72 | 0x68 | `PLI_RC_ACCOUNTLISTGET` |  | C→S |  | — |
| 73 | 0x69 | `PLI_RC_PLAYERPROPSGET2` |  | C→S |  | — |
| 74 | 0x6a | `PLI_RC_PLAYERPROPSGET3` |  | C→S |  | — |
| 75 | 0x6b | `PLI_RC_PLAYERPROPSRESET` |  | C→S |  | — |
| 76 | 0x6c | `PLI_RC_PLAYERPROPSSET2` |  | C→S |  | — |
| 77 | 0x6d | `PLI_RC_ACCOUNTGET` |  | C→S |  | — |
| 78 | 0x6e | `PLI_RC_ACCOUNTSET` |  | C→S |  | — |
| 79 | 0x6f | `PLI_RC_CHAT` |  | C→S |  | — |
| 80 | 0x70 | `PLI_PROFILEGET` |  | C→S | rest = account | yes |
| 81 | 0x71 | `PLI_PROFILESET` |  | C→S | account + profile fields [inf] | yes |
| 82 | 0x72 | `PLI_RC_WARPPLAYER` |  | C→S |  | — |
| 83 | 0x73 | `PLI_RC_PLAYERRIGHTSGET` |  | C→S |  | — |
| 84 | 0x74 | `PLI_RC_PLAYERRIGHTSSET` |  | C→S |  | — |
| 85 | 0x75 | `PLI_RC_PLAYERCOMMENTSGET` |  | C→S |  | — |
| 86 | 0x76 | `PLI_RC_PLAYERCOMMENTSSET` |  | C→S |  | — |
| 87 | 0x77 | `PLI_RC_PLAYERBANGET` |  | C→S |  | — |
| 88 | 0x78 | `PLI_RC_PLAYERBANSET` |  | C→S |  | — |
| 89 | 0x79 | `PLI_RC_FILEBROWSER_START` |  | C→S |  | — |
| 90 | 0x7a | `PLI_RC_FILEBROWSER_CD` |  | C→S |  | — |
| 91 | 0x7b | `PLI_RC_FILEBROWSER_END` |  | C→S |  | — |
| 92 | 0x7c | `PLI_RC_FILEBROWSER_DOWN` |  | C→S |  | — |
| 93 | 0x7d | `PLI_RC_FILEBROWSER_UP` |  | C→S |  | — |
| 94 | 0x7e | `PLI_NPCSERVERQUERY` |  | C→S |  | — |
| 96 | 0x80 | `PLI_RC_FILEBROWSER_MOVE` |  | C→S |  | — |
| 97 | 0x81 | `PLI_RC_FILEBROWSER_DELETE` |  | C→S |  | — |
| 98 | 0x82 | `PLI_RC_FILEBROWSER_RENAME` |  | C→S |  | — |
| 103 | 0x87 | `PLI_NC_NPCGET` |  | C→S |  | — |
| 104 | 0x88 | `PLI_NC_NPCDELETE` |  | C→S |  | — |
| 105 | 0x89 | `PLI_NC_NPCRESET` |  | C→S |  | — |
| 106 | 0x8a | `PLI_NC_NPCSCRIPTGET` |  | C→S |  | — |
| 107 | 0x8b | `PLI_NC_NPCWARP` |  | C→S |  | — |
| 108 | 0x8c | `PLI_NC_NPCFLAGSGET` |  | C→S |  | — |
| 109 | 0x8d | `PLI_NC_NPCSCRIPTSET` |  | C→S |  | — |
| 110 | 0x8e | `PLI_NC_NPCFLAGSSET` |  | C→S |  | — |
| 111 | 0x8f | `PLI_NC_NPCADD` |  | C→S |  | — |
| 112 | 0x90 | `PLI_NC_CLASSEDIT` |  | C→S |  | — |
| 113 | 0x91 | `PLI_NC_CLASSADD` |  | C→S |  | — |
| 114 | 0x92 | `PLI_NC_LOCALNPCSGET` |  | C→S |  | — |
| 115 | 0x93 | `PLI_NC_WEAPONLISTGET` |  | C→S |  | — |
| 116 | 0x94 | `PLI_NC_WEAPONGET` |  | C→S |  | — |
| 117 | 0x95 | `PLI_NC_WEAPONADD` |  | C→S |  | — |
| 118 | 0x96 | `PLI_NC_WEAPONDELETE` |  | C→S |  | — |
| 119 | 0x97 | `PLI_NC_CLASSDELETE` |  | C→S |  | — |
| 130 | 0xa2 | `PLI_REQUESTUPDATEBOARD` |  | C→S |  | — |
| 150 | 0xb6 | `PLI_NC_LEVELLISTGET` |  | C→S |  | — |
| 151 | 0xb7 | `PLI_NC_LEVELLISTSET` |  | C→S |  | — |
| 152 | 0xb8 | `PLI_REQUESTTEXT` |  | C→S |  | — |
| 154 | 0xba | `PLI_SENDTEXT` |  | C→S |  | — |
| 155 | 0xbb | `PLI_RC_LARGEFILESTART` |  | C→S |  | — |
| 156 | 0xbc | `PLI_RC_LARGEFILEEND` |  | C→S |  | — |
| 157 | 0xbd | `PLI_UPDATEGANI` |  | C→S |  | — |
| 158 | 0xbe | `PLI_UPDATESCRIPT` |  | C→S |  | — |
| 159 | 0xbf | `PLI_UPDATEPACKAGEREQUESTFILE` |  | C→S |  | — |
| 160 | 0xc0 | `PLI_RC_FOLDERDELETE` |  | C→S |  | — |
| 161 | 0xc1 | `PLI_UPDATECLASS` |  | C→S |  | — |
| 162 | 0xc2 | `PLI_RC_UNKNOWN162` |  | C→S |  | — |
| 252 | — | `PLI_SET_ENC_KEY` |  | C→S |  | — |
| 253 | — | `PLI_BUNDLE` |  | C→S |  | — |

## Server → client (PLO)

| Id | Wire | Name | 39ster 2.1 | Dir | Payload | 2.05 |
|---:|:----:|------|------------|:---:|---------|:----:|
| 0 | 0x20 | `PLO_LEVELBOARD` |  | S→C | empty = use cached board; else board changes (as 7) | yes |
| 1 | 0x21 | `PLO_LEVELLINK` |  | S→C | rest = `dest x y w h newx newy` | yes |
| 2 | 0x22 | `PLO_BADDYPROPS` | `SBADDYPROPS` | S→C | `c id` + BDPROP stream | yes |
| 3 | 0x23 | `PLO_NPCPROPS` | `SNPCPROPS` | S→C | `i3 id` + NPCPROP stream | yes |
| 4 | 0x24 | `PLO_LEVELCHEST` |  | S→C | `c opened, c x, c y` [+ `c item, c signindex`] | yes |
| 5 | 0x25 | `PLO_LEVELSIGN` |  | S→C | `c x, c y` + sign-alphabet text | yes |
| 6 | 0x26 | `PLO_LEVELNAME` |  | S→C | rest = level filename | yes |
| 7 | 0x27 | `PLO_BOARDMODIFY` | `SBOARDMODIFY` | S→C | `c x, c y, c w, c h` + w×h `s tile` | yes |
| 8 | 0x28 | `PLO_OTHERPLPROPS` |  | S→C | `s id` + PLPROP stream | yes |
| 9 | 0x29 | `PLO_PLAYERPROPS` | `SPLAYERPROPS` | S→C | PLPROP stream (self) | yes |
| 10 | 0x2a | `PLO_ISLEADER` |  | S→C | empty: you lead this level | yes |
| 11 | 0x2b | `PLO_BOMBADD` |  | S→C | `c x×2, c y×2, c power, c fuse` | yes |
| 12 | 0x2c | `PLO_BOMBDEL` |  | S→C | as 11 | yes |
| 13 | 0x2d | `PLO_TOALL` |  | S→C | `s player id`, `str message` | yes |
| 14 | 0x2e | `PLO_PLAYERWARP` |  | S→C | `c x×2, c y×2` + rest = level | yes |
| 15 | 0x2f | `PLO_WARPFAILED` |  | S→C | rest = level | yes |
| 16 | 0x30 | `PLO_DISCMESSAGE` |  | S→C | rest = text; connection closes | yes |
| 17 | 0x31 | `PLO_HORSEADD` |  | S→C | relayed PLI 7 body: `c x×2, c y×2, c dir+4×bushes` + image | yes |
| 18 | 0x32 | `PLO_HORSEDEL` |  | S→C | `c x×2, c y×2` | yes |
| 19 | 0x33 | `PLO_ARROWADD` |  | S→C | arrow: x, y, dir | yes |
| 20 | 0x34 | `PLO_FIRESPY` |  | S→C | fire spy (relayed) | yes |
| 21 | 0x35 | `PLO_THROWCARRIED` |  | S→C | throw carried (relayed) | yes |
| 22 | 0x36 | `PLO_ITEMADD` |  | S→C | `c x×2, c y×2, c item` | yes |
| 23 | 0x37 | `PLO_ITEMDEL` |  | S→C | `c x×2, c y×2, c item` | yes |
| 24 | 0x38 | `PLO_NPCMOVED` |  | S→C |  | yes |
| 25 | 0x39 | `PLO_SIGNATURE` |  | S→C |  | yes |
| 26 | 0x3a | `PLO_NPCACTION` |  | S→C |  | — |
| 27 | 0x3b | `PLO_BADDYHURT` |  | S→C | baddy hurt: `c id` + BDPROP stream | yes |
| 28 | 0x3c | `PLO_FLAGSET` |  | S→C | rest = `name` or `name=value` | yes |
| 29 | 0x3d | `PLO_NPCDEL` |  | S→C |  | yes |
| 30 | 0x3e | `PLO_FILESENDFAILED` |  | S→C | rest = filename (pre-2.1: also "up to date") | yes |
| 31 | 0x3f | `PLO_FLAGDEL` |  | S→C | rest = flag name | yes |
| 32 | 0x40 | `PLO_SHOWIMGPLAYER` |  | S→C |  | yes |
| 33 | 0x41 | `PLO_NPCWEAPONADD` |  | S→C | `str name`, NPCPROP image + script | yes |
| 34 | 0x42 | `PLO_NPCWEAPONDEL` |  | S→C | rest = weapon name | yes |
| 35 | 0x43 | `PLO_RC_ADMINMESSAGE` |  | S→C | rest = `Admin <account>:\xa7<text>` | yes |
| 36 | 0x44 | `PLO_EXPLOSION` |  | S→C | `c radius, c x×2, c y×2, c power` | yes |
| 37 | 0x45 | `PLO_PRIVATEMESSAGE` |  | S→C | `s from id`, rest = quoted `"type","message"` | yes |
| 38 | 0x46 | `PLO_PUSHAWAY` |  | S→C | `c dx, c dy` | yes |
| 39 | 0x47 | `PLO_LEVELMODTIME` |  | S→C | `i5 modtime` | yes |
| 40 | 0x48 | `PLO_HURTPLAYER` |  | S→C | `s attacker, c dx, c dy, c power, i3 npc` | yes |
| 41 | 0x49 | `PLO_STARTMESSAGE` |  | S→C |  | yes |
| 42 | 0x4a | `PLO_NEWWORLDTIME` |  | S→C | `i4 time` | yes |
| 43 | 0x4b | `PLO_DEFAULTWEAPON` |  | S→C | `c item index` | yes |
| 44 | 0x4c | `PLO_HASNPCSERVER` |  | S→C |  | yes |
| 45 | 0x4d | `PLO_FILEUPTODATE` |  | S→C | rest = filename | yes |
| 46 | 0x4e | `PLO_HITOBJECTS` |  | S→C | hit objects: power, x, y [, npc] | yes |
| 47 | 0x4f | `PLO_STAFFGUILDS` |  | S→C | `"guild",` repeated | yes |
| 48 | 0x50 | `PLO_TRIGGERACTION` |  | S→C | `i3 npc, c x×2, c y×2` + rest = `action,params` | yes |
| 49 | 0x51 | `PLO_PLAYERWARP2` |  | S→C |  | — |
| 50 | 0x52 | `PLO_RC_ACCOUNTADD` |  | S→C |  | — |
| 51 | 0x53 | `PLO_RC_ACCOUNTSTATUS` |  | S→C |  | — |
| 52 | 0x54 | `PLO_RC_ACCOUNTNAME` |  | S→C |  | — |
| 53 | 0x55 | `PLO_RC_ACCOUNTDEL` |  | S→C |  | — |
| 54 | 0x56 | `PLO_RC_ACCOUNTPROPS` |  | S→C |  | — |
| 55 | 0x57 | `PLO_ADDPLAYER` |  | S→C |  | — |
| 56 | 0x58 | `PLO_DELPLAYER` |  | S→C |  | — |
| 57 | 0x59 | `PLO_RC_ACCOUNTPROPSGET` |  | S→C |  | — |
| 58 | 0x5a | `PLO_RC_ACCOUNTCHANGE` |  | S→C |  | — |
| 59 | 0x5b | `PLO_RC_PLAYERPROPSCHANGE` |  | S→C |  | — |
| 60 | 0x5c | `PLO_UNKNOWN60` |  | S→C |  | — |
| 61 | 0x5d | `PLO_RC_SERVERFLAGSGET` |  | S→C |  | — |
| 62 | 0x5e | `PLO_RC_PLAYERRIGHTSGET` |  | S→C |  | — |
| 63 | 0x5f | `PLO_RC_PLAYERCOMMENTSGET` |  | S→C |  | — |
| 64 | 0x60 | `PLO_RC_PLAYERBANGET` |  | S→C |  | — |
| 65 | 0x61 | `PLO_RC_FILEBROWSER_DIRLIST` |  | S→C |  | — |
| 66 | 0x62 | `PLO_RC_FILEBROWSER_DIR` |  | S→C |  | — |
| 67 | 0x63 | `PLO_RC_FILEBROWSER_MESSAGE` |  | S→C |  | — |
| 68 | 0x64 | `PLO_LARGEFILESTART` |  | S→C | rest = filename | — |
| 69 | 0x65 | `PLO_LARGEFILEEND` |  | S→C | rest = filename | — |
| 70 | 0x66 | `PLO_RC_ACCOUNTLISTGET` |  | S→C |  | — |
| 71 | 0x67 | `PLO_RC_PLAYERPROPS` |  | S→C |  | — |
| 72 | 0x68 | `PLO_RC_PLAYERPROPSGET` |  | S→C |  | — |
| 73 | 0x69 | `PLO_RC_ACCOUNTGET` |  | S→C |  | — |
| 74 | 0x6a | `PLO_RC_CHAT` |  | S→C | RC console line | — |
| 75 | 0x6b | `PLO_PROFILE` |  | S→C | rest = profile blob | yes |
| 76 | 0x6c | `PLO_RC_SERVEROPTIONSGET` |  | S→C |  | — |
| 77 | 0x6d | `PLO_RC_FOLDERCONFIGGET` |  | S→C |  | — |
| 78 | 0x6e | `PLO_NC_CONTROL` |  | S→C |  | — |
| 79 | 0x6f | `PLO_NPCSERVERADDR` |  | S→C |  | — |
| 80 | 0x70 | `PLO_NC_LEVELLIST` |  | S→C |  | — |
| 81 | 0x71 | `PLO_UNKNOWN81` |  | S→C |  | — |
| 82 | 0x72 | `PLO_SERVERTEXT` |  | S→C |  | — |
| 83 | 0x73 | `PLO_UNKNOWN83` |  | S→C |  | — |
| 84 | 0x74 | `PLO_LARGEFILESIZE` |  | S→C | `i5 size` | — |
| 100 | 0x84 | `PLO_RAWDATA` | `FILELEN` | S→C | `i3 length` of the next raw message | yes |
| 101 | 0x85 | `PLO_BOARDPACKET` | `TILES` | S→C | 4096 × u16 LE tiles (behind 100) | via 100 |
| 102 | 0x86 | `PLO_FILE` | `FILEBLOB` | S→C | file: `str name` [+ `i5 modtime` ≥ 2.1] + bytes (behind 100) | via 100 |
| 103 | 0x87 | `PLO_RC_MAXUPLOADFILESIZE` |  | S→C |  | — |
| 104 | 0x88 | `PLO_UNKNOWN104` |  | S→C |  | — |
| 105 | 0x89 | `PLO_UPDATEPACKAGESIZE` |  | S→C |  | — |
| 106 | 0x8a | `PLO_UPDATEPACKAGEDONE` |  | S→C |  | — |
| 107 | 0x8b | `PLO_BOARDLAYER` |  | S→C |  | — |
| 108 | 0x8c | `PLO_UNKNOWN108` |  | S→C |  | — |
| 109 | 0x8d | `PLO_UNKNOWN109` |  | S→C |  | — |
| 110 | 0x8e | `PLO_UNKNOWN110` |  | S→C |  | — |
| 111 | 0x8f | `PLO_SETNETCOOKIE` |  | S→C |  | — |
| 124 | 0x9c | `PLO_UNKNOWN124` |  | S→C |  | — |
| 131 | 0xa3 | `PLO_NPCBYTECODE` |  | S→C |  | — |
| 132 | 0xa4 | `PLO_UNKNOWN132` |  | S→C |  | — |
| 133 | 0xa5 | `PLO_UNKNOWN133` |  | S→C |  | — |
| 134 | 0xa6 | `PLO_GANISCRIPT` |  | S→C |  | — |
| 140 | 0xac | `PLO_NPCWEAPONSCRIPT` |  | S→C |  | — |
| 150 | 0xb6 | `PLO_NPCDEL2` |  | S→C |  | yes |
| 151 | 0xb7 | `PLO_HIDENPCS` |  | S→C |  | yes |
| 153 | 0xb9 | `PLO_SAY2` |  | S→C | rest = text, `\xa7` = newline | yes |
| 154 | 0xba | `PLO_FREEZEPLAYER2` |  | S→C | empty | yes |
| 155 | 0xbb | `PLO_UNFREEZEPLAYER` |  | S→C | empty | yes |
| 156 | 0xbc | `PLO_SETACTIVELEVEL` |  | S→C | rest = level for following object packets | yes |
| 157 | 0xbd | `PLO_NC_NPCATTRIBUTES` |  | S→C |  | — |
| 158 | 0xbe | `PLO_NC_NPCADD` |  | S→C |  | — |
| 159 | 0xbf | `PLO_NC_NPCDELETE` |  | S→C |  | — |
| 160 | 0xc0 | `PLO_NC_NPCSCRIPT` |  | S→C |  | — |
| 161 | 0xc1 | `PLO_NC_NPCFLAGS` |  | S→C |  | — |
| 162 | 0xc2 | `PLO_NC_CLASSGET` |  | S→C |  | — |
| 163 | 0xc3 | `PLO_NC_CLASSADD` |  | S→C |  | — |
| 164 | 0xc4 | `PLO_NC_LEVELDUMP` |  | S→C |  | — |
| 165 | 0xc5 | `PLO_MOVE` |  | S→C |  | yes |
| 166 | 0xc6 | `PLO_SHOWIMGNPC` |  | S→C |  | yes |
| 167 | 0xc7 | `PLO_NC_WEAPONLISTGET` |  | S→C |  | — |
| 168 | 0xc8 | `PLO_UNKNOWN168` |  | S→C |  | yes |
| 169 | 0xc9 | `PLO_UPGRADEURL` |  | S→C |  | — |
| 170 | 0xca | `PLO_GHOSTMODE` |  | S→C |  | — |
| 171 | 0xcb | `PLO_BIGMAP` |  | S→C |  | — |
| 172 | 0xcc | `PLO_MINIMAP` |  | S→C |  | — |
| 173 | 0xcd | `PLO_GHOSTTEXT` |  | S→C |  | — |
| 174 | 0xce | `PLO_GHOSTICON` |  | S→C |  | — |
| 175 | 0xcf | `PLO_SHOOT` |  | S→C |  | — |
| 176 | 0xd0 | `PLO_KINGDOMSMODE` |  | S→C |  | — |
| 177 | 0xd1 | `PLO_NEWWORLDMODE` |  | S→C |  | — |
| 178 | 0xd2 | `PLO_SERVERWARP` |  | S→C |  | — |
| 179 | 0xd3 | `PLO_RPGWINDOW` |  | S→C |  | — |
| 180 | 0xd4 | `PLO_STATUSLIST` |  | S→C |  | — |
| 181 | 0xd5 | `PLO_UNKNOWN181` |  | S→C |  | — |
| 182 | 0xd6 | `PLO_LISTPROCESSES` |  | S→C |  | — |
| 183 | 0xd7 | `PLO_HASPROCESSRUNNING` |  | S→C |  | — |
| 184 | 0xd8 | `PLO_TAKESCREENSHOT` |  | S→C |  | — |
| 185 | 0xd9 | `PLO_BOARDHEIGHTS` |  | S→C |  | — |
| 186 | 0xda | `PLO_BOARDMODIFY2` |  | S→C |  | — |
| 187 | 0xdb | `PLO_UPDATEPACKAGEISUPDATED` |  | S→C |  | — |
| 188 | 0xdc | `PLO_NC_CLASSDELETE` |  | S→C |  | — |
| 189 | 0xdd | `PLO_MOVE2` |  | S→C |  | — |
| 190 | 0xde | `PLO_SERVERLISTCONNECTED` |  | S→C |  | — |
| 191 | 0xdf | `PLO_SHOOT2` |  | S→C |  | — |
| 192 | 0xe0 | `PLO_NC_WEAPONGET` |  | S→C |  | — |
| 193 | 0xe1 | `PLO_UNKNOWN193` |  | S→C |  | — |
| 194 | 0xe2 | `PLO_CLEARWEAPONS` |  | S→C |  | — |
| 195 | 0xe3 | `PLO_LOADGANI` |  | S→C |  | — |
| 197 | 0xe5 | `PLO_LOADSCRIPT` |  | S→C |  | — |
| 198 | 0xe6 | `PLO_SERVEROPTIONS` |  | S→C |  | — |
| 252 | — | `PLO_SET_ENC_KEY` |  | S→C |  | — |
| 253 | — | `PLO_BUNDLE` |  | S→C |  | — |

Counts: 128 PLI ids, 38 sent by 2.05; 152 PLO ids, 59 handled by 2.05 (plus 101/102 behind 100).

Notes:
- 39ster 2.1 numbered RC ops 51–87 as mostly empty stubs. In gs2lib these are `PLI_RC_*` (51–98) and `PLI_NC_*` (103–119). 2.05 sends none of them.
- The 2.05 peer-to-peer UDP channel has its own id space; see `protocol/udp-p2p.md`.
- The first client line is not PLI 0: byte 0 is the client type (0 = classic client). See `protocol/login-and-walk.md`.
