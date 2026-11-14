<!-- manual: kind=reference status=draft -->
# Appendix A. Message index

Every client-to-server (PLI) and server-to-client (PLO) id with its wire byte and the section that documents it. Names follow → §0.7; the wire byte is the id + `0x20` (→ §2.1.2). The *2.05* column says whether 2.05 rev 2 sends (PLI) or handles (PLO) the id. UDP peer ids are a separate id space (→ §2.9).

## A.1 Client to server

This is the index of every client-to-server id. Each row gives the logical id, its wire byte, its name, whether 2.05 sends it, and the section that describes it [srv][2.05] (protocol/packet-ids.md#client--server-pli_).

| Id | Wire | Name | 2.05 | Section | Source |
| ---: | --- | --- | --- | --- | --- |
| 0 | `0x20` | `PLI_LEVELWARP` | sent | → §2.4.3 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 1 | `0x21` | `PLI_BOARDMODIFY` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 2 | `0x22` | `PLI_PLAYERPROPS` | sent | → §2.4.4 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 3 | `0x23` | `PLI_NPCPROPS` | sent | → §2.4.4 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 4 | `0x24` | `PLI_BOMBADD` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 5 | `0x25` | `PLI_BOMBDEL` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 6 | `0x26` | `PLI_TOALL` | sent | → §2.4.8 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 7 | `0x27` | `PLI_HORSEADD` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 8 | `0x28` | `PLI_HORSEDEL` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 9 | `0x29` | `PLI_ARROWADD` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 10 | `0x2a` | `PLI_FIRESPY` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 11 | `0x2b` | `PLI_THROWCARRIED` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 12 | `0x2c` | `PLI_ITEMADD` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 13 | `0x2d` | `PLI_ITEMDEL` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 14 | `0x2e` | `PLI_CLAIMPKER` | sent | → §2.4.9 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 15 | `0x2f` | `PLI_BADDYPROPS` | sent | → §2.4.4 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 16 | `0x30` | `PLI_BADDYHURT` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 17 | `0x31` | `PLI_BADDYADD` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 18 | `0x32` | `PLI_FLAGSET` | sent | → §2.4.6 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 19 | `0x33` | `PLI_FLAGDEL` | sent | → §2.4.6 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 20 | `0x34` | `PLI_OPENCHEST` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 21 | `0x35` | `PLI_PUTNPC` | sent | → §2.4.6 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 22 | `0x36` | `PLI_NPCDEL` | sent | → §2.4.6 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 23 | `0x37` | `PLI_WANTFILE` | sent | → §2.4.7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 24 | `0x38` | `PLI_SHOWIMGPLAYER` | sent | → §2.4.9 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 25 | `0x39` | `PLI_TOWEAPON` (was `PLI_UNKNOWN25`; proposed `PLI_WEAPONUPLOAD`) | no | → §2.4.9 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 26 | `0x3a` | `PLI_HURTPLAYER` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 27 | `0x3b` | `PLI_EXPLOSION` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 28 | `0x3c` | `PLI_PRIVATEMESSAGE` | sent | → §2.4.8 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 29 | `0x3d` | `PLI_NPCWEAPONDEL` | sent | → §2.4.6 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 30 | `0x3e` | `PLI_LEVELWARPMOD` | sent | → §2.4.3 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 31 | `0x3f` | `PLI_PACKETCOUNT` | no | → §2.4.9 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 32 | `0x40` | `PLI_ITEMTAKE` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 33 | `0x41` | `PLI_WEAPONADD` | sent | → §2.4.6 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 34 | `0x42` | `PLI_UPDATEFILE` | sent | → §2.4.7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 35 | `0x43` | `PLI_ADJACENTLEVEL` | sent | → §2.4.3 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 36 | `0x44` | `PLI_HITOBJECTS` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 37 | `0x45` | `PLI_LANGUAGE` | sent | → §2.4.9 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 38 | `0x46` | `PLI_TRIGGERACTION` | sent | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 39 | `0x47` | `PLI_TAMPERCHECK` | no | → §2.4.9 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 40 | `0x48` | `PLI_SHOOT` | no | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 41 | `0x49` | `PLI_SERVERWARP` | no | → §2.4.3 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 43 | `0x4b` | `PLI_MUTEPLAYER` | no | → §2.4.9 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 44 | `0x4c` | `PLI_PROCESSLIST` | no | → §2.4.9 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 45 | `0x4d` | `PLI_PROCESSRUNNING` | no | → §2.4.9 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 46 | `0x4e` | `PLI_ENTERLEVEL` | no | → §2.4.3 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 47 | `0x4f` | `PLI_VERIFYWANTSEND` | no | → §2.4.7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 48 | `0x50` | `PLI_SHOOT2` | no | → §2.4.5 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 50 | `0x52` | `PLI_RAWDATA` | no | → §2.4.7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 51 | `0x53` | `PLI_RC_SERVEROPTIONSGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 52 | `0x54` | `PLI_RC_SERVEROPTIONSSET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 53 | `0x55` | `PLI_RC_FOLDERCONFIGGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 54 | `0x56` | `PLI_RC_FOLDERCONFIGSET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 55 | `0x57` | `PLI_RC_RESPAWNSET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 56 | `0x58` | `PLI_RC_HORSELIFESET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 57 | `0x59` | `PLI_RC_APINCREMENTSET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 58 | `0x5a` | `PLI_RC_BADDYRESPAWNSET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 59 | `0x5b` | `PLI_RC_PLAYERPROPSGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 60 | `0x5c` | `PLI_RC_PLAYERPROPSSET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 61 | `0x5d` | `PLI_RC_DISCONNECTPLAYER` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 62 | `0x5e` | `PLI_RC_UPDATELEVELS` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 63 | `0x5f` | `PLI_RC_ADMINMESSAGE` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 64 | `0x60` | `PLI_RC_PRIVADMINMESSAGE` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 65 | `0x61` | `PLI_RC_LISTRCS` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 66 | `0x62` | `PLI_RC_DISCONNECTRC` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 67 | `0x63` | `PLI_RC_APPLYREASON` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 68 | `0x64` | `PLI_RC_SERVERFLAGSGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 69 | `0x65` | `PLI_RC_SERVERFLAGSSET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 70 | `0x66` | `PLI_RC_ACCOUNTADD` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 71 | `0x67` | `PLI_RC_ACCOUNTDEL` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 72 | `0x68` | `PLI_RC_ACCOUNTLISTGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 73 | `0x69` | `PLI_RC_PLAYERPROPSGET2` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 74 | `0x6a` | `PLI_RC_PLAYERPROPSGET3` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 75 | `0x6b` | `PLI_RC_PLAYERPROPSRESET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 76 | `0x6c` | `PLI_RC_PLAYERPROPSSET2` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 77 | `0x6d` | `PLI_RC_ACCOUNTGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 78 | `0x6e` | `PLI_RC_ACCOUNTSET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 79 | `0x6f` | `PLI_RC_CHAT` | no | → §2.4.10 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 80 | `0x70` | `PLI_PROFILEGET` | sent | → §2.4.8 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 81 | `0x71` | `PLI_PROFILESET` | sent | → §2.4.8 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 82 | `0x72` | `PLI_RC_WARPPLAYER` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 83 | `0x73` | `PLI_RC_PLAYERRIGHTSGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 84 | `0x74` | `PLI_RC_PLAYERRIGHTSSET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 85 | `0x75` | `PLI_RC_PLAYERCOMMENTSGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 86 | `0x76` | `PLI_RC_PLAYERCOMMENTSSET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 87 | `0x77` | `PLI_RC_PLAYERBANGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 88 | `0x78` | `PLI_RC_PLAYERBANSET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 89 | `0x79` | `PLI_RC_FILEBROWSER_START` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 90 | `0x7a` | `PLI_RC_FILEBROWSER_CD` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 91 | `0x7b` | `PLI_RC_FILEBROWSER_END` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 92 | `0x7c` | `PLI_RC_FILEBROWSER_DOWN` | no | → §2.4.10 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 93 | `0x7d` | `PLI_RC_FILEBROWSER_UP` | no | → §2.4.10 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 94 | `0x7e` | `PLI_NPCSERVERQUERY` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 96 | `0x80` | `PLI_RC_FILEBROWSER_MOVE` | no | → §2.4.10 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 97 | `0x81` | `PLI_RC_FILEBROWSER_DELETE` | no | → §2.4.10 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 98 | `0x82` | `PLI_RC_FILEBROWSER_RENAME` | no | → §2.4.10 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 103 | `0x87` | `PLI_NC_NPCGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 104 | `0x88` | `PLI_NC_NPCDELETE` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 105 | `0x89` | `PLI_NC_NPCRESET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 106 | `0x8a` | `PLI_NC_NPCSCRIPTGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 107 | `0x8b` | `PLI_NC_NPCWARP` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 108 | `0x8c` | `PLI_NC_NPCFLAGSGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 109 | `0x8d` | `PLI_NC_NPCSCRIPTSET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 110 | `0x8e` | `PLI_NC_NPCFLAGSSET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 111 | `0x8f` | `PLI_NC_NPCADD` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 112 | `0x90` | `PLI_NC_CLASSEDIT` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 113 | `0x91` | `PLI_NC_CLASSADD` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 114 | `0x92` | `PLI_NC_LOCALNPCSGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 115 | `0x93` | `PLI_NC_WEAPONLISTGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 116 | `0x94` | `PLI_NC_WEAPONGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 117 | `0x95` | `PLI_NC_WEAPONADD` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 118 | `0x96` | `PLI_NC_WEAPONDELETE` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 119 | `0x97` | `PLI_NC_CLASSDELETE` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 130 | `0xa2` | `PLI_REQUESTUPDATEBOARD` | no | → §2.4.7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 150 | `0xb6` | `PLI_NC_LEVELLISTGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 151 | `0xb7` | `PLI_NC_LEVELLISTSET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 152 | `0xb8` | `PLI_REQUESTTEXT` | no | → §2.4.7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 154 | `0xba` | `PLI_SENDTEXT` | no | → §2.4.7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 155 | `0xbb` | `PLI_RC_LARGEFILESTART` | no | → §2.4.10 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 156 | `0xbc` | `PLI_RC_LARGEFILEEND` | no | → §2.4.10 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 157 | `0xbd` | `PLI_UPDATEGANI` | no | → §2.4.7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 158 | `0xbe` | `PLI_UPDATESCRIPT` | no | → §2.4.7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 159 | `0xbf` | `PLI_UPDATEPACKAGEREQUESTFILE` | no | → §2.4.7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 160 | `0xc0` | `PLI_RC_FOLDERDELETE` | no | → §2.4.10 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 161 | `0xc1` | `PLI_UPDATECLASS` | no | → §2.4.7 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 162 | `0xc2` | `PLI_PONG` (was `PLI_RC_UNKNOWN162`; proposed `PLI_PING`) | no | → §2.4.9 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 252 | n/a (above 223) | `PLI_SET_ENC_KEY` | no | → §2.4.9 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| 253 | n/a (above 223) | `PLI_BUNDLE` | no | → §2.4.9 | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |

## A.2 Server to client

This is the index of every server-to-client id. The 2.05 column says whether 2.05 handles the id [srv][2.05] (protocol/packet-ids.md#server--client-plo_).

| Id | Wire | Name | 2.05 | Section | Source |
| ---: | --- | --- | --- | --- | --- |
| 0 | `0x20` | `PLO_LEVELBOARD` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 1 | `0x21` | `PLO_LEVELLINK` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 2 | `0x22` | `PLO_BADDYPROPS` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 3 | `0x23` | `PLO_NPCPROPS` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 4 | `0x24` | `PLO_LEVELCHEST` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 5 | `0x25` | `PLO_LEVELSIGN` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 6 | `0x26` | `PLO_LEVELNAME` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 7 | `0x27` | `PLO_BOARDMODIFY` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 8 | `0x28` | `PLO_OTHERPLPROPS` | handled | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 9 | `0x29` | `PLO_PLAYERPROPS` | handled | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 10 | `0x2a` | `PLO_ISLEADER` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 11 | `0x2b` | `PLO_BOMBADD` | handled | → §2.5.5 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 12 | `0x2c` | `PLO_BOMBDEL` | handled | → §2.5.5 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 13 | `0x2d` | `PLO_TOALL` | handled | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 14 | `0x2e` | `PLO_PLAYERWARP` | handled | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 15 | `0x2f` | `PLO_WARPFAILED` | handled | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 16 | `0x30` | `PLO_DISCMESSAGE` | handled | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 17 | `0x31` | `PLO_HORSEADD` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 18 | `0x32` | `PLO_HORSEDEL` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 19 | `0x33` | `PLO_ARROWADD` | handled | → §2.5.5 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 20 | `0x34` | `PLO_FIRESPY` | handled | → §2.5.5 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 21 | `0x35` | `PLO_THROWCARRIED` | handled | → §2.5.5 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 22 | `0x36` | `PLO_ITEMADD` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 23 | `0x37` | `PLO_ITEMDEL` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 24 | `0x38` | `PLO_NPCMOVED` | handled | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 25 | `0x39` | `PLO_SIGNATURE` | handled | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 26 | `0x3a` | `PLO_NPCACTION` | no | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 27 | `0x3b` | `PLO_BADDYHURT` | handled | → §2.5.5 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 28 | `0x3c` | `PLO_FLAGSET` | handled | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 29 | `0x3d` | `PLO_NPCDEL` | handled | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 30 | `0x3e` | `PLO_FILESENDFAILED` | handled | → §2.5.7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 31 | `0x3f` | `PLO_FLAGDEL` | handled | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 32 | `0x40` | `PLO_SHOWIMGPLAYER` | handled | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 33 | `0x41` | `PLO_NPCWEAPONADD` | handled | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 34 | `0x42` | `PLO_NPCWEAPONDEL` | handled | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 35 | `0x43` | `PLO_RC_ADMINMESSAGE` | handled | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 36 | `0x44` | `PLO_EXPLOSION` | handled | → §2.5.5 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 37 | `0x45` | `PLO_PRIVATEMESSAGE` | handled | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 38 | `0x46` | `PLO_PUSHAWAY` | handled | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 39 | `0x47` | `PLO_LEVELMODTIME` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 40 | `0x48` | `PLO_HURTPLAYER` | handled | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 41 | `0x49` | `PLO_STARTMESSAGE` | handled | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 42 | `0x4a` | `PLO_NEWWORLDTIME` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 43 | `0x4b` | `PLO_DEFAULTWEAPON` | handled | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 44 | `0x4c` | `PLO_HASNPCSERVER` | handled | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 45 | `0x4d` | `PLO_FILEUPTODATE` | handled | → §2.5.7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 46 | `0x4e` | `PLO_HITOBJECTS` | handled | → §2.5.5 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 47 | `0x4f` | `PLO_STAFFGUILDS` | handled | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 48 | `0x50` | `PLO_TRIGGERACTION` | handled | → §2.5.5 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 49 | `0x51` | `PLO_PLAYERWARP2` | no | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 50 | `0x52` | `PLO_RC_ACCOUNTADD` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 51 | `0x53` | `PLO_RC_ACCOUNTSTATUS` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 52 | `0x54` | `PLO_RC_ACCOUNTNAME` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 53 | `0x55` | `PLO_RC_ACCOUNTDEL` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 54 | `0x56` | `PLO_RC_ACCOUNTPROPS` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 55 | `0x57` | `PLO_ADDPLAYER` | no | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 56 | `0x58` | `PLO_DELPLAYER` | no | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 57 | `0x59` | `PLO_RC_ACCOUNTPROPSGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 58 | `0x5a` | `PLO_RC_ACCOUNTCHANGE` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 59 | `0x5b` | `PLO_RC_PLAYERPROPSCHANGE` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 60 | `0x5c` | `PLO_UNKNOWN60` | no | → §2.5.10 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 61 | `0x5d` | `PLO_RC_SERVERFLAGSGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 62 | `0x5e` | `PLO_RC_PLAYERRIGHTSGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 63 | `0x5f` | `PLO_RC_PLAYERCOMMENTSGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 64 | `0x60` | `PLO_RC_PLAYERBANGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 65 | `0x61` | `PLO_RC_FILEBROWSER_DIRLIST` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 66 | `0x62` | `PLO_RC_FILEBROWSER_DIR` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 67 | `0x63` | `PLO_RC_FILEBROWSER_MESSAGE` | no | → §2.5.9 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 68 | `0x64` | `PLO_LARGEFILESTART` | no | → §2.5.7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 69 | `0x65` | `PLO_LARGEFILEEND` | no | → §2.5.7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 70 | `0x66` | `PLO_RC_ACCOUNTLISTGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 71 | `0x67` | `PLO_RC_PLAYERPROPS` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 72 | `0x68` | `PLO_RC_PLAYERPROPSGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 73 | `0x69` | `PLO_RC_ACCOUNTGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 74 | `0x6a` | `PLO_RC_CHAT` | no | → §2.5.9 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 75 | `0x6b` | `PLO_PROFILE` | handled | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 76 | `0x6c` | `PLO_RC_SERVEROPTIONSGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 77 | `0x6d` | `PLO_RC_FOLDERCONFIGGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 78 | `0x6e` | `PLO_NC_CONTROL` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 79 | `0x6f` | `PLO_NPCSERVERADDR` | no | → §2.5.9 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 80 | `0x70` | `PLO_NC_LEVELLIST` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 81 | `0x71` | `PLO_UNKNOWN81` | no | → §2.5.10 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 82 | `0x72` | `PLO_SERVERTEXT` | no | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 83 | `0x73` | `PLO_UNKNOWN83` | no | → §2.5.10 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 84 | `0x74` | `PLO_LARGEFILESIZE` | no | → §2.5.7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 100 | `0x84` | `PLO_RAWDATA` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 101 | `0x85` | `PLO_BOARDPACKET` | no | → §2.5.3 | [bin] (version-profiles/plo-handled-ids-by-build.tsv); [srv] (protocol/packet-layouts.md#level-data-server--client) |
| 102 | `0x86` | `PLO_FILE` | no | → §2.5.7 | [bin] (version-profiles/plo-handled-ids-by-build.tsv); [srv] (protocol/codec-and-framing.md#raw-data-escape) |
| 103 | `0x87` | `PLO_RC_MAXUPLOADFILESIZE` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 104 | `0x88` | `PLO_FILEDECRYPTKEY` (was `PLO_UNKNOWN104`; proposed `PLO_FILEKEY`) | no | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 105 | `0x89` | `PLO_UPDATEPACKAGESIZE` | no | → §2.5.7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 106 | `0x8a` | `PLO_UPDATEPACKAGEDONE` | no | → §2.5.7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 107 | `0x8b` | `PLO_BOARDLAYER` | no | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 108 | `0x8c` | `PLO_PING` (was `PLO_UNKNOWN108`) | no | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 109 | `0x8d` | `PLO_HTTPDOWNLOAD` (was `PLO_UNKNOWN109`; proposed `PLO_DOWNLOADURL`) | no | → §2.5.7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 110 | `0x8e` | `PLO_UNKNOWN110` | no | → §2.5.10 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 111 | `0x8f` | `PLO_SETNETCOOKIE` | no | → §2.5.7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 124 | `0x9c` | `PLO_RC_UNKNOWN124` (was `PLO_UNKNOWN124`; proposed `PLO_RC_PLAYERFLAGS`) | no | → §2.5.10 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 131 | `0xa3` | `PLO_NPCBYTECODE` | no | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 132 | `0xa4` | `PLO_UNKNOWN132` (beta4 gserver: `PLO_WEAPONBYTECODE`) | no | → §2.5.10 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 133 | `0xa5` | `PLO_UNKNOWN133` (beta4 gserver: `PLO_CLASSBYTECODE`) | no | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 134 | `0xa6` | `PLO_GANISCRIPT` | no | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 140 | `0xac` | `PLO_NPCWEAPONSCRIPT` | no | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 150 | `0xb6` | `PLO_NPCDEL2` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 151 | `0xb7` | `PLO_HIDENPCS` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 153 | `0xb9` | `PLO_SAY2` | handled | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 154 | `0xba` | `PLO_FREEZEPLAYER2` | handled | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 155 | `0xbb` | `PLO_UNFREEZEPLAYER` | handled | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 156 | `0xbc` | `PLO_SETACTIVELEVEL` | handled | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 157 | `0xbd` | `PLO_NC_NPCATTRIBUTES` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 158 | `0xbe` | `PLO_NC_NPCADD` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 159 | `0xbf` | `PLO_NC_NPCDELETE` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 160 | `0xc0` | `PLO_NC_NPCSCRIPT` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 161 | `0xc1` | `PLO_NC_NPCFLAGS` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 162 | `0xc2` | `PLO_NC_CLASSGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 163 | `0xc3` | `PLO_NC_CLASSADD` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 164 | `0xc4` | `PLO_NC_LEVELDUMP` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 165 | `0xc5` | `PLO_MOVE` | handled | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 166 | `0xc6` | `PLO_SHOWIMGNPC` | handled | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 167 | `0xc7` | `PLO_NC_WEAPONLISTGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 168 | `0xc8` | `PLO_ONLINEMODE` (was `PLO_UNKNOWN168`; proposed `PLO_LOGGEDIN`) | handled | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 169 | `0xc9` | `PLO_UPGRADEURL` | no | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 170 | `0xca` | `PLO_GHOSTMODE` | no | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 171 | `0xcb` | `PLO_BIGMAP` | no | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 172 | `0xcc` | `PLO_MINIMAP` | no | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 173 | `0xcd` | `PLO_GHOSTTEXT` | no | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 174 | `0xce` | `PLO_GHOSTICON` | no | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 175 | `0xcf` | `PLO_SHOOT` | no | → §2.5.5 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 176 | `0xd0` | `PLO_KINGDOMSMODE` | no | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 177 | `0xd1` | `PLO_NEWWORLDMODE` | no | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 178 | `0xd2` | `PLO_SERVERWARP` | no | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 179 | `0xd3` | `PLO_RPGWINDOW` | no | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 180 | `0xd4` | `PLO_STATUSLIST` | no | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 181 | `0xd5` | `PLO_UNKNOWN181` (beta4 gserver: `PLO_PLAYERNOUDP`) | no | → §2.5.4 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 182 | `0xd6` | `PLO_LISTPROCESSES` | no | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 183 | `0xd7` | `PLO_HASPROCESSRUNNING` | no | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 184 | `0xd8` | `PLO_TAKESCREENSHOT` | no | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 185 | `0xd9` | `PLO_BOARDHEIGHTS` | no | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 186 | `0xda` | `PLO_BOARDMODIFY2` | no | → §2.5.3 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 187 | `0xdb` | `PLO_UPDATEPACKAGEISUPDATED` | no | → §2.5.7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 188 | `0xdc` | `PLO_NC_CLASSDELETE` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 189 | `0xdd` | `PLO_MOVE2` | no | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 190 | `0xde` | `PLO_SERVERLISTCONNECTED` | no | → §2.5.8 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 191 | `0xdf` | `PLO_SHOOT2` | no | → §2.5.5 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 192 | `0xe0` | `PLO_NC_WEAPONGET` | no | → §7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 193 | `0xe1` | `PLO_WEAPONHASH` (was `PLO_UNKNOWN193`; proposed `PLO_WEAPONCRC`) | no | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 194 | `0xe2` | `PLO_RESETCLIENT` (was `PLO_CLEARWEAPONS`) | no | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 195 | `0xe3` | `PLO_LOADGANI` | no | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 196 | `0xe4` | (no gs2lib name) | no | → §2.5.6 | [bin] (version-profiles/plo-handled-ids-by-build.tsv); [bin] (protocol/v4x-clients.md#server--client-ids) |
| 197 | `0xe5` | `PLO_LOADSCRIPT` | no | → §2.5.6 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 198 | `0xe6` | `PLO_SERVEROPTIONS` | no | → §2.5.7 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 252 | n/a (above 223) | `PLO_SET_ENC_KEY` | no | → §2.5.10 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |
| 253 | n/a (above 223) | `PLO_BUNDLE` | no | → §2.5.10 | [srv][2.05] (protocol/packet-ids.md#server--client-plo_) |

## A.3 Former names

An older gs2lib copy (the GServer-v2 submodule of 2025-01) uses these names for the same ids:

| Former name | Id | Current name | Source |
| --- | ---: | --- | --- |
| `PLI_SHOWIMG` | 24 | `PLI_SHOWIMGPLAYER` | [srv] (protocol/packet-ids.md#renames-between-gs2lib-versions) |
| `PLI_MAPINFO` | 39 | `PLI_TAMPERCHECK` | [srv] (protocol/packet-ids.md#renames-between-gs2lib-versions) |
| `PLI_UNKNOWN46` | 46 | `PLI_ENTERLEVEL` | [srv] (protocol/packet-ids.md#renames-between-gs2lib-versions) |
| `PLO_SHOWIMG` | 32 | `PLO_SHOWIMGPLAYER` | [srv] (protocol/packet-ids.md#renames-between-gs2lib-versions) |
| `PLO_FULLSTOP` | 176 | `PLO_KINGDOMSMODE` | [srv] (protocol/packet-ids.md#renames-between-gs2lib-versions) |
| `PLO_FULLSTOP2` | 177 | `PLO_NEWWORLDMODE` | [srv] (protocol/packet-ids.md#renames-between-gs2lib-versions) |
| `PLO_UNKNOWN183` | 183 | `PLO_HASPROCESSRUNNING` | [srv] (protocol/packet-ids.md#renames-between-gs2lib-versions) |
| `PLO_UNKNOWN184` | 184 | `PLO_TAKESCREENSHOT` | [srv] (protocol/packet-ids.md#renames-between-gs2lib-versions) |
| `PLO_UNKNOWN185` | 185 | `PLO_BOARDHEIGHTS` | [srv] (protocol/packet-ids.md#renames-between-gs2lib-versions) |
| `PLO_UNKNOWN186` | 186 | `PLO_BOARDMODIFY2` | [srv] (protocol/packet-ids.md#renames-between-gs2lib-versions) |
| `PLO_UNKNOWN190` | 190 | `PLO_SERVERLISTCONNECTED` | [srv] (protocol/packet-ids.md#renames-between-gs2lib-versions) |

Some ids have had more than one name. The rules below record the name changes between copies of the server library [srv] (protocol/packet-ids.md#renames-between-gs2lib-versions).

| Rule | Source |
| --- | --- |
| The newer gs2lib copy adds `PLI_PROCESSRUNNING` (45), `PLI_SET_ENC_KEY` (252), `PLI_BUNDLE` (253), `PLO_SETNETCOOKIE` (111) and `PLO_UPGRADEURL` (169) | [srv] (protocol/packet-ids.md#renames-between-gs2lib-versions) |
| An older note names 100, 101 and 102 FILELEN, TILES and FILEBLOB; the roles are those of `PLO_RAWDATA`, `PLO_BOARDPACKET` and `PLO_FILE` | [doc] (protocol/packet-ids.md#conflicts-with-older-notes) |
| Provisional ids from early notes (login 0x01, level request 0x10, player update 0x20) are retired: the login is type 0, `PLI_LEVELWARP` is 0 and `PLI_PLAYERPROPS` is 2 | [doc] (protocol/packet-ids.md#conflicts-with-older-notes) |
