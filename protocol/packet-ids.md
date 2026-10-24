# Packet id tables

Date: 2026-10-21

Names: gs2lib `IEnums.h` (2026-10 bitbucket head, GPLv3). The names are as in gs2lib; the notes are restated in this repo's field notation (`c`, `s`, `i3`, `str`, …), not copied. The 2.05 column is taken from the 2.05 rev 2 server→client jump table and the client→server sender functions.

Wire byte = id + 0x20 (GCHAR). Ids above 223 cannot be sent as a single GCHAR.

Legend, 2.05 column: **✔** handled or sent by 2.05 · **·** not present in 2.05.

## Server → client (PLO_*)

| Id | Wire | Name | 2.05 | Notes (restated from server source) |
|---:|:----:|------|:----:|------|
| 0 | 0x20 | `PLO_LEVELBOARD` | ✔ |   |
| 1 | 0x21 | `PLO_LEVELLINK` | ✔ |   |
| 2 | 0x22 | `PLO_BADDYPROPS` | ✔ |   |
| 3 | 0x23 | `PLO_NPCPROPS` | ✔ |   |
| 4 | 0x24 | `PLO_LEVELCHEST` | ✔ |   |
| 5 | 0x25 | `PLO_LEVELSIGN` | ✔ |   |
| 6 | 0x26 | `PLO_LEVELNAME` | ✔ |   |
| 7 | 0x27 | `PLO_BOARDMODIFY` | ✔ |   |
| 8 | 0x28 | `PLO_OTHERPLPROPS` | ✔ |   |
| 9 | 0x29 | `PLO_PLAYERPROPS` | ✔ |   |
| 10 | 0x2a | `PLO_ISLEADER` | ✔ |   |
| 11 | 0x2b | `PLO_BOMBADD` | ✔ |   |
| 12 | 0x2c | `PLO_BOMBDEL` | ✔ |   |
| 13 | 0x2d | `PLO_TOALL` | ✔ |   |
| 14 | 0x2e | `PLO_PLAYERWARP` | ✔ |   |
| 15 | 0x2f | `PLO_WARPFAILED` | ✔ |   |
| 16 | 0x30 | `PLO_DISCMESSAGE` | ✔ |   |
| 17 | 0x31 | `PLO_HORSEADD` | ✔ |   |
| 18 | 0x32 | `PLO_HORSEDEL` | ✔ |   |
| 19 | 0x33 | `PLO_ARROWADD` | ✔ |   |
| 20 | 0x34 | `PLO_FIRESPY` | ✔ |   |
| 21 | 0x35 | `PLO_THROWCARRIED` | ✔ |   |
| 22 | 0x36 | `PLO_ITEMADD` | ✔ |   |
| 23 | 0x37 | `PLO_ITEMDEL` | ✔ |   |
| 24 | 0x38 | `PLO_NPCMOVED` | ✔ |   |
| 25 | 0x39 | `PLO_SIGNATURE` | ✔ | `c v`: 1 = the client quits; 0 = quits unless the host is 127.0.0.1; other values ignored (layout read in 2.17–2.31; the id is handled from 2.00) **[bin]** |
| 26 | 0x3a | `PLO_NPCACTION` | · | purpose unknown; client 6.037 ignores it |
| 27 | 0x3b | `PLO_BADDYHURT` | ✔ |   |
| 28 | 0x3c | `PLO_FLAGSET` | ✔ |   |
| 29 | 0x3d | `PLO_NPCDEL` | ✔ |   |
| 30 | 0x3e | `PLO_FILESENDFAILED` | ✔ |   |
| 31 | 0x3f | `PLO_FLAGDEL` | ✔ |   |
| 32 | 0x40 | `PLO_SHOWIMGPLAYER` | ✔ |   |
| 33 | 0x41 | `PLO_NPCWEAPONADD` | ✔ |   |
| 34 | 0x42 | `PLO_NPCWEAPONDEL` | ✔ |   |
| 35 | 0x43 | `PLO_RC_ADMINMESSAGE` | ✔ |   |
| 36 | 0x44 | `PLO_EXPLOSION` | ✔ |   |
| 37 | 0x45 | `PLO_PRIVATEMESSAGE` | ✔ |   |
| 38 | 0x46 | `PLO_PUSHAWAY` | ✔ | `c dx, c dy`; each scales as v/16 − 4 (±2 tiles in 1/16 steps) |
| 39 | 0x47 | `PLO_LEVELMODTIME` | ✔ | 2.17–2.31: the rest is passed unparsed to the active gmap or level object, only if one exists **[bin]** |
| 40 | 0x48 | `PLO_HURTPLAYER` | ✔ |   |
| 41 | 0x49 | `PLO_STARTMESSAGE` | ✔ | client 6.037 ignores it; rest = RTF or HTML text; cached as `servermessage.rtf` / `.html` and shown in the start-message viewer; client 6.037 ignores it **[bin]** |
| 42 | 0x4a | `PLO_NEWWORLDTIME` | ✔ |   |
| 43 | 0x4b | `PLO_DEFAULTWEAPON` | ✔ |   |
| 44 | 0x4c | `PLO_HASNPCSERVER` | ✔ | when present, the client stops applying NPC props itself; client 5.07+ ignores it; no payload; handled by 2.00–2.22, not handled by 2.31 **[bin]** |
| 45 | 0x4d | `PLO_FILEUPTODATE` | ✔ |   |
| 46 | 0x4e | `PLO_HITOBJECTS` | ✔ |   |
| 47 | 0x4f | `PLO_STAFFGUILDS` | ✔ | comma text, stored as the staff-guild list **[bin]** |
| 48 | 0x50 | `PLO_TRIGGERACTION` | ✔ | `s fromPlayer`, `i3 fromNPC`, `c xTile`, `c yTile`, `list action,params` |
| 49 | 0x51 | `PLO_PLAYERWARP2` | · | `c x×2, c y×2, c z` (unused by 2.17–2.31), `c gmapX, c gmapY`, rest = level; x and y are `v/2` tiles; gmapX/Y apply only when the level name ends in `.gmap` (clamped to the grid) **[bin]** |
| 50 | 0x52 | `PLO_RC_ACCOUNTADD` | · |   |
| 51 | 0x53 | `PLO_RC_ACCOUNTSTATUS` | · |   |
| 52 | 0x54 | `PLO_RC_ACCOUNTNAME` | · |   |
| 53 | 0x55 | `PLO_RC_ACCOUNTDEL` | · |   |
| 54 | 0x56 | `PLO_RC_ACCOUNTPROPS` | · |   |
| 55 | 0x57 | `PLO_ADDPLAYER` | · | client 5.07+ ignores it |
| 56 | 0x58 | `PLO_DELPLAYER` | · | client 5.07+ ignores it |
| 57 | 0x59 | `PLO_RC_ACCOUNTPROPSGET` | · |   |
| 58 | 0x5a | `PLO_RC_ACCOUNTCHANGE` | · |   |
| 59 | 0x5b | `PLO_RC_PLAYERPROPSCHANGE` | · |   |
| 60 | 0x5c | `PLO_UNKNOWN60` | · | client 5.07+ ignores it |
| 61 | 0x5d | `PLO_RC_SERVERFLAGSGET` | · |   |
| 62 | 0x5e | `PLO_RC_PLAYERRIGHTSGET` | · |   |
| 63 | 0x5f | `PLO_RC_PLAYERCOMMENTSGET` | · |   |
| 64 | 0x60 | `PLO_RC_PLAYERBANGET` | · |   |
| 65 | 0x61 | `PLO_RC_FILEBROWSER_DIRLIST` | · |   |
| 66 | 0x62 | `PLO_RC_FILEBROWSER_DIR` | · |   |
| 67 | 0x63 | `PLO_RC_FILEBROWSER_MESSAGE` | · |   |
| 68 | 0x64 | `PLO_LARGEFILESTART` | · | rest = file name (2.31 also clears the stored size) **[bin]** |
| 69 | 0x65 | `PLO_LARGEFILEEND` | · | rest = file name; if it equals the stored name the received stream is processed as a file **[bin]** |
| 70 | 0x66 | `PLO_RC_ACCOUNTLISTGET` | · |   |
| 71 | 0x67 | `PLO_RC_PLAYERPROPS` | · |   |
| 72 | 0x68 | `PLO_RC_PLAYERPROPSGET` | · |   |
| 73 | 0x69 | `PLO_RC_ACCOUNTGET` | · |   |
| 74 | 0x6a | `PLO_RC_CHAT` | · |   |
| 75 | 0x6b | `PLO_PROFILE` | ✔ | repeat `c n` + n chars; first field = account, the rest = profile lines **[bin]** |
| 76 | 0x6c | `PLO_RC_SERVEROPTIONSGET` | · |   |
| 77 | 0x6d | `PLO_RC_FOLDERCONFIGGET` | · |   |
| 78 | 0x6e | `PLO_NC_CONTROL` | · | repurposed by Graal Reborn; original purpose unknown; client 5.07+ ignores it |
| 79 | 0x6f | `PLO_NPCSERVERADDR` | · | two bytes (0, 2), then `ip,port` text; client 5. ignores it |
| 80 | 0x70 | `PLO_NC_LEVELLIST` | · | `str levels`; client 5.07+ ignores it |
| 81 | 0x71 | `PLO_UNKNOWN81` | · | client 5.07+ ignores it |
| 82 | 0x72 | `PLO_SERVERTEXT` | · | reply to PLI_REQUESTTEXT / PLI_SENDTEXT |
| 83 | 0x73 | `PLO_UNKNOWN83` | · | client 5.07+ ignores it |
| 84 | 0x74 | `PLO_LARGEFILESIZE` | · | `i5 size` (2.31 only) **[bin]** |
| 100 | 0x84 | `PLO_RAWDATA` | ✔ | `i3 length` |
| 101 | 0x85 | `PLO_BOARDPACKET` | ✔ via RAWDATA |   |
| 102 | 0x86 | `PLO_FILE` | ✔ via RAWDATA |   |
| 103 | 0x87 | `PLO_RC_MAXUPLOADFILESIZE` | · | `i5 bytes`: RC upload limit (default 20 MiB) |
| 104 | 0x88 | `PLO_UNKNOWN104` | · | `str data` holding `c`, `i5`, `i5` (an 8-byte value) |
| 105 | 0x89 | `PLO_UPDATEPACKAGESIZE` | · | package-update message (5.07, 6.037) |
| 106 | 0x8a | `PLO_UPDATEPACKAGEDONE` | · | package-update message (5.07, 6.037) |
| 107 | 0x8b | `PLO_BOARDLAYER` | · | like LEVELBOARD, for extra layers |
| 108 | 0x8c | `PLO_UNKNOWN108` | · |   |
| 109 | 0x8d | `PLO_UNKNOWN109` | · | `i5 modtime`, `str url`: fetch a file over HTTP (connector?) |
| 110 | 0x8e | `PLO_UNKNOWN110` | · | ignored by clients |
| 111 | 0x8f | `PLO_SETNETCOOKIE` | · | `rest cookie` |
| 124 | 0x9c | `PLO_UNKNOWN124` | · | seen by RC3; possibly player flags (untested) |
| 131 | 0xa3 | `PLO_NPCBYTECODE` | · | `i3 code`, `bytecode` |
| 132 | 0xa4 | `PLO_UNKNOWN132` | · | 5.07 only; client 6.037 ignores it |
| 133 | 0xa5 | `PLO_UNKNOWN133` | · | rest = text; maybe registers a class script |
| 134 | 0xa6 | `PLO_GANISCRIPT` | · | gani scripts, maybe for package downloads |
| 140 | 0xac | `PLO_NPCWEAPONSCRIPT` | · | `s info_length`, `script` |
| 150 | 0xb6 | `PLO_NPCDEL2` | ✔ | `c n`, n-char level name, `i3 npc id` **[bin]** |
| 151 | 0xb7 | `PLO_HIDENPCS` | ✔ | no payload; removes NPCs with ids 1 to 999 of the active level (id 0 excluded) **[bin]** |
| 153 | 0xb9 | `PLO_SAY2` | ✔ | rest = text; signs use it too |
| 154 | 0xba | `PLO_FREEZEPLAYER2` | ✔ |  |
| 155 | 0xbb | `PLO_UNFREEZEPLAYER` | ✔ |  |
| 156 | 0xbc | `PLO_SETACTIVELEVEL` | ✔ | rest = level or `.gmap` name; a `.gmap` is loaded and made active. 2.31 adds an extra follow-up step (purpose unknown) **[bin]** |
| 157 | 0xbd | `PLO_NC_NPCATTRIBUTES` | · | `str attributes`; client 5.07+ ignores it |
| 158 | 0xbe | `PLO_NC_NPCADD` | · | `i3 id`, `c 50`, `str name`, `c 51`, `str type`, `c 52`, `str level` |
| 159 | 0xbf | `PLO_NC_NPCDELETE` | · | `i3 id`; client 5.07+ ignores it |
| 160 | 0xc0 | `PLO_NC_NPCSCRIPT` | · | `i3 id`, `str script`; client 5.07+ ignores it |
| 161 | 0xc1 | `PLO_NC_NPCFLAGS` | · | `i3 id`, `str flags`; client 5.07+ ignores it |
| 162 | 0xc2 | `PLO_NC_CLASSGET` | · | `str name`, `str script`; client 5.07+ ignores it |
| 163 | 0xc3 | `PLO_NC_CLASSADD` | · | `class`; client 5.07+ ignores it |
| 164 | 0xc4 | `PLO_NC_LEVELDUMP` | · | client 5.07+ ignores it |
| 165 | 0xc5 | `PLO_MOVE` | ✔ | client 6.037 ignores it; `i3 npc id` (> 0) + move data **[bin]** |
| 166 | 0xc6 | `PLO_SHOWIMGNPC` | ✔ | `i3 npc id` + prop list **[bin]** |
| 167 | 0xc7 | `PLO_NC_WEAPONLISTGET` | · | `c name1 length`, `name1`, `c name2 length`, `name2`; client 5.07+ ignores it |
| 168 | 0xc8 | `PLO_UNKNOWN168` | ✔ | sent by the login server; payload ignored; local-player reset (2.17–2.31) **[bin]** |
| 169 | 0xc9 | `PLO_UPGRADEURL` | · | with DISCONNECT: the reconnect button becomes "Upgrade" and opens this URL; rest = URL text **[bin]** |
| 170 | 0xca | `PLO_GHOSTMODE` | · | `c flag` (> 0 = ghost on) **[bin]** |
| 171 | 0xcb | `PLO_BIGMAP` | · | client 6.037 ignores it; comma text `txt,png,x,y` (≥ 4 fields used); x, y parsed as floats **[bin]** |
| 172 | 0xcc | `PLO_MINIMAP` | · | same layout as 171, goes to the minimap **[bin]** |
| 173 | 0xcd | `PLO_GHOSTTEXT` | · | rest = text **[bin]** |
| 174 | 0xce | `PLO_GHOSTICON` | · | `c flag` (> 0 = show icon) **[bin]** |
| 175 | 0xcf | `PLO_SHOOT` | · | client 6.037 ignores it; `s player id` + shot data; only when the player is in the active level **[bin]** |
| 176 | 0xd0 | `PLO_KINGDOMSMODE` | · | client switches to Kingdoms mode; no payload **[bin]** |
| 177 | 0xd1 | `PLO_NEWWORLDMODE` | · | client switches to New World mode; no payload **[bin]** |
| 178 | 0xd2 | `PLO_SERVERWARP` | · | comma text, ≥ 4 fields, fields 1–3 used (meaning unresolved) **[bin]** |
| 179 | 0xd3 | `PLO_RPGWINDOW` | · | rest = text **[bin]** |
| 180 | 0xd4 | `PLO_STATUSLIST` | · | rest = text **[bin]** |
| 181 | 0xd5 | `PLO_UNKNOWN181` | · | `s player id`, `c toggle` (length ≥ 3) **[bin]** |
| 182 | 0xd6 | `PLO_LISTPROCESSES` | · | no payload; client answers `PLI_PROCESSLIST` (44) **[bin]** |
| 183 | 0xd7 | `PLO_HASPROCESSRUNNING` | · | rest = names; client answers `PLI_PROCESSRUNNING` (45) with `c 0/1` **[bin]** |
| 184 | 0xd8 | `PLO_TAKESCREENSHOT` | · | rest = file name, only `.png` accepted; saved under a screenshots folder **[bin]** |
| 185 | 0xd9 | `PLO_BOARDHEIGHTS` | · | `c mapX, c mapY, c blockX, c blockY, c w-1, c h-1`, then w×h cells of 2 raw bytes; height = (b0−0x20−50) + (b1−0x20)/128 **[bin]** |
| 186 | 0xda | `PLO_BOARDMODIFY2` | · | `c mapX, c mapY, c x, c y, c w, c h`, then w×h `s tile` row-major, then ignored padding: bytes after the tiles are not read, a payload one byte short of 6+2*w*h is dropped silently, a block past column 63 is clipped (2.22+; client reaction lab-tested with injected frames, no server seen sending it) **[bin][cap]** |
| 187 | 0xdb | `PLO_UPDATEPACKAGEISUPDATED` | · | package-update message (5.07, 6.037) |
| 188 | 0xdc | `PLO_NC_CLASSDELETE` | · | `class`; client 5.07+ ignores it |
| 189 | 0xdd | `PLO_MOVE2` | · | `i3 id`; as 165 with an extra flag (2.31 only) **[bin]** |
| 190 | 0xde | `PLO_SERVERLISTCONNECTED` | · |  |
| 191 | 0xdf | `PLO_SHOOT2` | · | 5.07 / 6.037 |
| 192 | 0xe0 | `PLO_NC_WEAPONGET` | · | `str name`, `str image`, `script`; client 5.07+ ignores it |
| 193 | 0xe1 | `PLO_UNKNOWN193` | · | `i5 ?`, `?` |
| 194 | 0xe2 | `PLO_CLEARWEAPONS` | · | empty; precedes the weapon list |
| 195 | 0xe3 | `PLO_LOADGANI` | · | `str gani`, `list` (SETBACKTO and others) |
| 197 | 0xe5 | `PLO_LOADSCRIPT` | · | `list type,name,saveToDisk,desKey,crc32` (type weapon/npc/class/gani; key = two i5) |
| 198 | 0xe6 | `PLO_SERVEROPTIONS` | · | `i5 serverOptions` |
| 252 | — | `PLO_SET_ENC_KEY` | · | sets AES/RC4 key and IV |
| 253 | — | `PLO_BUNDLE` | · | several packets in one |

**Layouts of ids 25, 39, 41, 44, 47, 49, 68–84, 150–156, 165–189 [bin]** were read from the 2.17.1, 2.22 and 2.31 receive handlers (decompile pass of 2026-10-24); the full table with version gates and confidence is `version-profiles/plo-layouts-217-231.tsv`, and the handled-id set of every build from 2.00 to 2.31 is `version-profiles/plo-handled-ids-by-build.tsv`. Dispatch bounds: 2.17.1 id 185, 2.22 id 186, 2.31 id 189. Ids 152 and 167 are not handled by any of them. Id 26 (`PLO_NPCACTION`) is handled by 2.00–2.03 and dropped in 2.04. Still undecoded: the `PLO_SERVERWARP` (178) field meanings and the extra step 2.31 adds after `PLO_SETACTIVELEVEL` (156); see `client-internals/decomp-findings-2026-10-24-b/05-open-items.md`.

No jump-table entry in 2.05: 26 (`PLO_NPCACTION`), 49–74, 76–99, and everything ≥ 101 except 150, 151, 153–156, 165, 166, 168. Ids 101 and 102 are read behind `PLO_RAWDATA` (see `codec-and-framing.md`). The dispatcher bound is 0xA8 (id 168). Unused slots fall to one shared default arm. **[2.05]**

## Client → server (PLI_*)

| Id | Wire | Name | 2.05 | Notes (restated from server source) |
|---:|:----:|------|:----:|------|
| 0 | 0x20 | `PLI_LEVELWARP` | ✔ |   |
| 1 | 0x21 | `PLI_BOARDMODIFY` | ✔ |   |
| 2 | 0x22 | `PLI_PLAYERPROPS` | ✔ |   |
| 3 | 0x23 | `PLI_NPCPROPS` | ✔ |   |
| 4 | 0x24 | `PLI_BOMBADD` | ✔ |   |
| 5 | 0x25 | `PLI_BOMBDEL` | ✔ | v6+ also sends it around login |
| 6 | 0x26 | `PLI_TOALL` | ✔ | 2.05: chat text with a `toall:` prefix |
| 7 | 0x27 | `PLI_HORSEADD` | ✔ |   |
| 8 | 0x28 | `PLI_HORSEDEL` | ✔ |   |
| 9 | 0x29 | `PLI_ARROWADD` | ✔ |   |
| 10 | 0x2a | `PLI_FIRESPY` | ✔ |   |
| 11 | 0x2b | `PLI_THROWCARRIED` | ✔ |   |
| 12 | 0x2c | `PLI_ITEMADD` | ✔ |   |
| 13 | 0x2d | `PLI_ITEMDEL` | ✔ |   |
| 14 | 0x2e | `PLI_CLAIMPKER` | ✔ |   |
| 15 | 0x2f | `PLI_BADDYPROPS` | ✔ |   |
| 16 | 0x30 | `PLI_BADDYHURT` | ✔ |   |
| 17 | 0x31 | `PLI_BADDYADD` | ✔ |   |
| 18 | 0x32 | `PLI_FLAGSET` | ✔ |   |
| 19 | 0x33 | `PLI_FLAGDEL` | ✔ |   |
| 20 | 0x34 | `PLI_OPENCHEST` | ✔ |   |
| 21 | 0x35 | `PLI_PUTNPC` | ✔ |   |
| 22 | 0x36 | `PLI_NPCDEL` | ✔ |   |
| 23 | 0x37 | `PLI_WANTFILE` | ✔ |   |
| 24 | 0x38 | `PLI_SHOWIMGPLAYER` | ✔ | 2.31 also sends it by itself about every 5.1 s with a 1-byte payload (value 9 seen); meaning unknown **[cap]** |
| 25 | 0x39 | `PLI_UNKNOWN25` | · |   |
| 26 | 0x3a | `PLI_HURTPLAYER` | ✔ |   |
| 27 | 0x3b | `PLI_EXPLOSION` | ✔ |   |
| 28 | 0x3c | `PLI_PRIVATEMESSAGE` | ✔ |   |
| 29 | 0x3d | `PLI_NPCWEAPONDEL` | ✔ |   |
| 30 | 0x3e | `PLI_LEVELWARPMOD` | ✔ |   |
| 31 | 0x3f | `PLI_PACKETCOUNT` | · |   |
| 32 | 0x40 | `PLI_ITEMTAKE` | ✔ |   |
| 33 | 0x41 | `PLI_WEAPONADD` | ✔ |   |
| 34 | 0x42 | `PLI_UPDATEFILE` | ✔ |   |
| 35 | 0x43 | `PLI_ADJACENTLEVEL` | ✔ |   |
| 36 | 0x44 | `PLI_HITOBJECTS` | ✔ |   |
| 37 | 0x45 | `PLI_LANGUAGE` | ✔ |   |
| 38 | 0x46 | `PLI_TRIGGERACTION` | ✔ | `i3 fromNPC`, `c x`, `c y`, `list actionAndParams`; 2.05 sends x and y in half-tiles (see `packet-layouts.md`) |
| 39 | 0x47 | `PLI_TAMPERCHECK` | · | 10 raw bytes, a constant per client build (not two `i5`); sent right after `PLI_LANGUAGE` at login. 2.22 also re-sends it on every gmap edge crossing, 2.31 about every 3.2 s. Values in `version-profiles/tampercheck-values.tsv`; how the bytes are built is in `client-internals/decomp-findings-2026-10-24-b/01-tamper-check-id39.md` **[cap][bin]** |
| 40 | 0x48 | `PLI_SHOOT` | · |   |
| 41 | 0x49 | `PLI_SERVERWARP` | · |   |
| 43 | 0x4b | `PLI_MUTEPLAYER` | · | player-list mute: `s player id`, `c on/off` (1 = mute, 0 = unmute); one message per click, confirmed from a real 2.22 client **[cap]** |
| 44 | 0x4c | `PLI_PROCESSLIST` | · | the client's reply to `PLO_LISTPROCESSES` (182) **[bin][cap]** |
| 45 | 0x4d | `PLI_PROCESSRUNNING` | · | `c flag`: reply to HASPROCESSRUNNING; 1 if the server's string occurs in the client's own process list **[bin]** |
| 46 | 0x4e | `PLI_ENTERLEVEL` | · | `c 1` on every level entry (login and each gmap edge crossing in the lab), sent just before the props message that carries cell prop 43/44 and the wrapped coordinate; 2.31 only, and 2.31 does not re-send id 39 at a crossing **[cap]** |
| 47 | 0x4f | `PLI_VERIFYWANTSEND` | · | `i5 crc32`, `str filename`: send the file if stale |
| 48 | 0x50 | `PLI_SHOOT2` | · |   |
| 50 | 0x52 | `PLI_RAWDATA` | · |   |
| 51 | 0x53 | `PLI_RC_SERVEROPTIONSGET` | · |   |
| 52 | 0x54 | `PLI_RC_SERVEROPTIONSSET` | · |   |
| 53 | 0x55 | `PLI_RC_FOLDERCONFIGGET` | · |   |
| 54 | 0x56 | `PLI_RC_FOLDERCONFIGSET` | · |   |
| 55 | 0x57 | `PLI_RC_RESPAWNSET` | · |   |
| 56 | 0x58 | `PLI_RC_HORSELIFESET` | · |   |
| 57 | 0x59 | `PLI_RC_APINCREMENTSET` | · |   |
| 58 | 0x5a | `PLI_RC_BADDYRESPAWNSET` | · |   |
| 59 | 0x5b | `PLI_RC_PLAYERPROPSGET` | · |   |
| 60 | 0x5c | `PLI_RC_PLAYERPROPSSET` | · |   |
| 61 | 0x5d | `PLI_RC_DISCONNECTPLAYER` | · |   |
| 62 | 0x5e | `PLI_RC_UPDATELEVELS` | · |   |
| 63 | 0x5f | `PLI_RC_ADMINMESSAGE` | · |   |
| 64 | 0x60 | `PLI_RC_PRIVADMINMESSAGE` | · |   |
| 65 | 0x61 | `PLI_RC_LISTRCS` | · |   |
| 66 | 0x62 | `PLI_RC_DISCONNECTRC` | · |   |
| 67 | 0x63 | `PLI_RC_APPLYREASON` | · |   |
| 68 | 0x64 | `PLI_RC_SERVERFLAGSGET` | · |   |
| 69 | 0x65 | `PLI_RC_SERVERFLAGSSET` | · |   |
| 70 | 0x66 | `PLI_RC_ACCOUNTADD` | · |   |
| 71 | 0x67 | `PLI_RC_ACCOUNTDEL` | · |   |
| 72 | 0x68 | `PLI_RC_ACCOUNTLISTGET` | · |   |
| 73 | 0x69 | `PLI_RC_PLAYERPROPSGET2` | · | by player id |
| 74 | 0x6a | `PLI_RC_PLAYERPROPSGET3` | · | by account name |
| 75 | 0x6b | `PLI_RC_PLAYERPROPSRESET` | · |   |
| 76 | 0x6c | `PLI_RC_PLAYERPROPSSET2` | · |   |
| 77 | 0x6d | `PLI_RC_ACCOUNTGET` | · |   |
| 78 | 0x6e | `PLI_RC_ACCOUNTSET` | · |   |
| 79 | 0x6f | `PLI_RC_CHAT` | · |   |
| 80 | 0x70 | `PLI_PROFILEGET` | ✔ |   |
| 81 | 0x71 | `PLI_PROFILESET` | ✔ |   |
| 82 | 0x72 | `PLI_RC_WARPPLAYER` | · |   |
| 83 | 0x73 | `PLI_RC_PLAYERRIGHTSGET` | · |   |
| 84 | 0x74 | `PLI_RC_PLAYERRIGHTSSET` | · |   |
| 85 | 0x75 | `PLI_RC_PLAYERCOMMENTSGET` | · |   |
| 86 | 0x76 | `PLI_RC_PLAYERCOMMENTSSET` | · |   |
| 87 | 0x77 | `PLI_RC_PLAYERBANGET` | · |   |
| 88 | 0x78 | `PLI_RC_PLAYERBANSET` | · |   |
| 89 | 0x79 | `PLI_RC_FILEBROWSER_START` | · |   |
| 90 | 0x7a | `PLI_RC_FILEBROWSER_CD` | · |   |
| 91 | 0x7b | `PLI_RC_FILEBROWSER_END` | · |   |
| 92 | 0x7c | `PLI_RC_FILEBROWSER_DOWN` | · |   |
| 93 | 0x7d | `PLI_RC_FILEBROWSER_UP` | · |   |
| 94 | 0x7e | `PLI_NPCSERVERQUERY` | · |   |
| 96 | 0x80 | `PLI_RC_FILEBROWSER_MOVE` | · |   |
| 97 | 0x81 | `PLI_RC_FILEBROWSER_DELETE` | · |   |
| 98 | 0x82 | `PLI_RC_FILEBROWSER_RENAME` | · |   |
| 103 | 0x87 | `PLI_NC_NPCGET` | · | `i3 id` |
| 104 | 0x88 | `PLI_NC_NPCDELETE` | · | `i3 id` |
| 105 | 0x89 | `PLI_NC_NPCRESET` | · | `i3 id` |
| 106 | 0x8a | `PLI_NC_NPCSCRIPTGET` | · | `i3 id` |
| 107 | 0x8b | `PLI_NC_NPCWARP` | · | `i3 id`, `c x*2`, `c y*2`, `level` |
| 108 | 0x8c | `PLI_NC_NPCFLAGSGET` | · | `i3 id` |
| 109 | 0x8d | `PLI_NC_NPCSCRIPTSET` | · | `i3 id`, `str script` |
| 110 | 0x8e | `PLI_NC_NPCFLAGSSET` | · | `i3 id`, `str flags` |
| 111 | 0x8f | `PLI_NC_NPCADD` | · | `str info` = name,id,type,scripter,level,x,y |
| 112 | 0x90 | `PLI_NC_CLASSEDIT` | · | `class` |
| 113 | 0x91 | `PLI_NC_CLASSADD` | · | `c name length`, `name`, `str script` |
| 114 | 0x92 | `PLI_NC_LOCALNPCSGET` | · | `level` |
| 115 | 0x93 | `PLI_NC_WEAPONLISTGET` | · |  |
| 116 | 0x94 | `PLI_NC_WEAPONGET` | · | `weapon` |
| 117 | 0x95 | `PLI_NC_WEAPONADD` | · | `c weapon length`, `weapon`, `c image length`, `image`, `code` |
| 118 | 0x96 | `PLI_NC_WEAPONDELETE` | · | `weapon` |
| 119 | 0x97 | `PLI_NC_CLASSDELETE` | · | `class` |
| 130 | 0xa2 | `PLI_REQUESTUPDATEBOARD` | · | `c level length`, `level`, `i5 modtime`, `s x`, `s y`, `s width`, `s height` |
| 150 | 0xb6 | `PLI_NC_LEVELLISTGET` | · |  |
| 151 | 0xb7 | `PLI_NC_LEVELLISTSET` | · | `str levels` |
| 152 | 0xb8 | `PLI_REQUESTTEXT` | · | read a server value |
| 154 | 0xba | `PLI_SENDTEXT` | · | write a server value |
| 155 | 0xbb | `PLI_RC_LARGEFILESTART` | · |   |
| 156 | 0xbc | `PLI_RC_LARGEFILEEND` | · |   |
| 157 | 0xbd | `PLI_UPDATEGANI` | · | gani update request (like UPDATECLASS) |
| 158 | 0xbe | `PLI_UPDATESCRIPT` | · | rest = script name to fetch |
| 159 | 0xbf | `PLI_UPDATEPACKAGEREQUESTFILE` | · | order?, package file name, modtime |
| 160 | 0xc0 | `PLI_RC_FOLDERDELETE` | · |   |
| 161 | 0xc1 | `PLI_UPDATECLASS` | · | `i5 modtime` + rest = class name |
| 162 | 0xc2 | `PLI_RC_UNKNOWN162` | · | empty; RC3 beta |
| 252 | — | `PLI_SET_ENC_KEY` | · | sets AES/RC4 key and IV |
| 253 | — | `PLI_BUNDLE` | · | several packets in one |

2.05 senders were found for 0–5, 7–24, 26–30, 32–38, 80, and 81 **[2.05]**. A sender for 6 (`PLI_TOALL`) was also found: chat-bar text starting with `toall:` is sent as id 6 (see `chat-pm-rc.md`). No sender was found for 25 or 31 (`PLI_PACKETCOUNT`).

Id 0 is overloaded. The login line starts with GCHAR 0 because that byte is the client type, and later `PLI_LEVELWARP` messages also use id 0. The server tells them apart by connection state. **[srv][2.05]**

## Renames between gs2lib versions

The GServer-v2 submodule copy (2025-01) uses older names for several ids: `PLI_SHOWIMG`→`PLI_SHOWIMGPLAYER` (24), `PLI_MAPINFO`→`PLI_TAMPERCHECK` (39), `PLI_UNKNOWN46`→`PLI_ENTERLEVEL` (46), `PLO_SHOWIMG`→`PLO_SHOWIMGPLAYER` (32), `PLO_FULLSTOP`/`2`→`PLO_KINGDOMSMODE`/`PLO_NEWWORLDMODE` (176/177), `PLO_UNKNOWN183–186`→`HASPROCESSRUNNING`/`TAKESCREENSHOT`/`BOARDHEIGHTS`/`BOARDMODIFY2`, `PLO_UNKNOWN190`→`PLO_SERVERLISTCONNECTED`. The newer copy also adds `PLI_PROCESSRUNNING` 45, `PLI_SET_ENC_KEY` 252, `PLI_BUNDLE` 253, `PLO_SETNETCOOKIE` 111, and `PLO_UPGRADEURL` 169.

## Conflicts with older notes

- `OPCODE-SUMMARY.md` (39ster 2.1 source) names 100/101/102 FILELEN/TILES/FILEBLOB. gs2lib calls them RAWDATA/BOARDPACKET/FILE. The roles are the same. Its other server→client ids agree with gs2lib.
- `session-opcodes-cleaned.md` lists 0x22 as "Computer / NPC-like object". 0x22 is `PLO_BADDYPROPS` (baddies are "compus" in GS1). NPCs are 0x23.
- The same table's 0x85 "level load (raw path)" and 0x86 "stream data" are 101 `PLO_BOARDPACKET` and 102 `PLO_FILE`, both read behind `PLO_RAWDATA` (0x84).
- `packet-id-diff.md` provisional ids (`Login 0x01`, `LevelRequest 0x10`, `PlayerUpdate 0x20`) are retired. The real ids are login type 0, `PLI_LEVELWARP` 0, and `PLI_PLAYERPROPS` 2.

**2.05 receive count [2.05]:** 59 handled PLO ids plus a silent default arm. Every id marked · above is ignored without error, including 26 and 49–59. UDP peer messages use a separate id space; see `udp-p2p.md`.
