# The 6.11 connector script's packet-id tables, read live

Date: 2026-11-13. This note covers the id-table item of #397. **[lab]**: an offline run of the unmodified Mac 6.111 client in a Lion lab VM. The VM had no internet. The client fetched a previously captured connector reply from a loopback responder and connected to a loopback game sink. After the connector script's `onCreated` had run, the client was paused and both resolved 256-entry dispatch tables were read from its connection object. No key, capture, host or dump is published.

The gs2lib column is joined from `packet-ids.md` by wire id. It is a name match by number. That the 6.11 handler does what the gs2lib name says is shown only where the `tclient_*` name or the handler's shape agrees (most rows do).

## How the script loads them

- `setoutdatahandlers` ran twice with the same list. **[lab]**
- `setindatahandlers` ran twice with two different lists **[lab]**:
  - **Set 1: 95 pairs.** It includes wire 100 → slot 93 and has no 252 or 253 pairs.
  - **Set 2: 96 pairs.** It drops wire 100 and adds 252 → 252 and 253 → 253.
- The live incoming table matches **set 2** exactly. The script has both `setDataHandlersOldProtocol` and `setDataHandlersNewProtocol` (`connector-script.md` §4a). Set 1 is read as the old-protocol set and set 2 as the new-protocol set, the one in use. **[inf]** The names were not seen at run time.
- No outgoing slot holds `0xFE`, so the live script routes no message to a script event. No incoming wire id uses 254 ("do not call"). **[lab]**
- The incoming slot names come from the 6.1.1.3 native index table (`v6113-handlers.md`). That table applies to this Mac build: the one empty native is slot 90 in both, and the handlers' length checks agree at slots 11, 24, 26 and 52. **[bin][lab]** "By shape" means the slot has no `tclient_*` string, but what it parses matches the name given.

## Outgoing: internal message → wire id

The event names are the 6.11 send slots in `v6x-clients.md`. Slots 58 to 255 hold −1, which means "not sent". **[lab]**

| Internal slot | Wire id | 6.11 send event | gs2lib name for that wire id |
| ---: | ---: | --- | --- |
| 0 | 158 | `onSendWantWeaponScript` | `PLI_UPDATESCRIPT` |
| 1 | 161 | `onSendWantClassScript` | `PLI_UPDATECLASS` |
| 2 | 157 | `onSendWantGaniScript` | `PLI_UPDATEGANI` |
| 3 | 6 | `onSendToAllChat` | `PLI_TOALL` |
| 4 | 14 | `onSendIsPKer` | `PLI_CLAIMPKER` |
| 5 | 11 | `onSendCarryThrown` | `PLI_THROWCARRIED` |
| 6 | 7 | `onSendAddHorse` | `PLI_HORSEADD` |
| 7 | 8 | `onSendDelHorse` | `PLI_HORSEDEL` |
| 8 | 4 | `onSendAddBomb` | `PLI_BOMBADD` |
| 9 | 5 | `onSendDelBomb` | `PLI_BOMBDEL` |
| 10 | 41 | `onSendServerWarp` | `PLI_SERVERWARP` |
| 11 | 38 | `onSendTriggerAction` | `PLI_TRIGGERACTION` |
| 12 | 10 | `onSendFireSpying` | `PLI_FIRESPY` |
| 13 | 27 | `onSendExplosion` | `PLI_EXPLOSION` |
| 14 | 36 | `onSendWeaponHit` | `PLI_HITOBJECTS` |
| 15 | 26 | `onSendPlayerHurt` | `PLI_HURTPLAYER` |
| 16 | 22 | `onSendDeleteNPC` | `PLI_NPCDEL` |
| 17 | 29 | `onSendDeleteWeapon` | `PLI_NPCWEAPONDEL` |
| 18 | 12 | `onSendExtra` | `PLI_ITEMADD` |
| 19 | 32 | `onSendTakeExtra` | `PLI_ITEMTAKE` |
| 20 | 13 | `onSendRemoveExtra` | `PLI_ITEMDEL` |
| 21 | 20 | `onSendOpenChest` | `PLI_OPENCHEST` |
| 22 | 9 | `onSendShot` | `PLI_ARROWADD` |
| 23 | 15 | `onSendBaddyProperties` | `PLI_BADDYPROPS` |
| 24 | 16 | `onSendBaddyHurt` | `PLI_BADDYHURT` |
| 25 | 24 | `onSendWeaponImage` | `PLI_SHOWIMGPLAYER` |
| 26 | 79 | `onSendRCChat` | `PLI_RC_CHAT` |
| 27 | 152 | `onSendRequestText` | `PLI_REQUESTTEXT` |
| 28 | 154 | `onSendSetText` | `PLI_SENDTEXT` |
| 29 | 97 | `onSendFileDeletion` | `PLI_RC_FILEBROWSER_DELETE` |
| 30 | 160 | `onSendFolderDeletion` | `PLI_RC_FOLDERDELETE` |
| 31 | 98 | `onSendFileRename` | `PLI_RC_FILEBROWSER_RENAME` |
| 32 | 96 | `onSendFilesMove` | `PLI_RC_FILEBROWSER_MOVE` |
| 33 | 45 | `onSendHaveWindow` | `PLI_PROCESSRUNNING` |
| 34 | 46 | `onSendEnterLevel` | `PLI_ENTERLEVEL` |
| 35 | 23 | `onSendWantImage` | `PLI_WANTFILE` |
| 36 | 34 | `onSendImageUpdate` | `PLI_UPDATEFILE` |
| 37 | 47 | `onSendImageUpdateCRC` | `PLI_VERIFYWANTSEND` |
| 38 | 0 | `onSendLevelWarp` | `PLI_LEVELWARP` |
| 39 | 30 | `onSendLevelWarpModtime` | `PLI_LEVELWARPMOD` |
| 40 | 92 | `onSendDownloadFile` | `PLI_RC_FILEBROWSER_DOWN` |
| 41 | 1 | `onSendBoardModify` | `PLI_BOARDMODIFY` |
| 42 | 130 | `onSendBoardModify2` | `PLI_REQUESTUPDATEBOARD` |
| 43 | 35 | `onSendPreloadLevel` | `PLI_ADJACENTLEVEL` |
| 44 | 2 | `onSendPlayerProperties` | `PLI_PLAYERPROPS` |
| 45 | 3 | `onSendNPCProperties` | `PLI_NPCPROPS` |
| 46 | 18 | `onSendFlag` | `PLI_FLAGSET` |
| 47 | 19 | `onSendUnsetFlag` | `PLI_FLAGDEL` |
| 48 | 48 | `onSendProjectile` | `PLI_SHOOT2` |
| 49 | 159 | `onSendUpdatePackage` | `PLI_UPDATEPACKAGEREQUESTFILE` |
| 50 | 28 | `onSendPrivateMessage` | `PLI_PRIVATEMESSAGE` |
| 51 | 155 | `onSendUploadStart` | `PLI_RC_LARGEFILESTART` |
| 52 | 93 | `onSendSaveFile` | `PLI_RC_FILEBROWSER_UP` |
| 53 | 156 | `onSendUploadEnd` | `PLI_RC_LARGEFILEEND` |
| 54 | 37 | — | `PLI_LANGUAGE` |
| 55 | 162 | `onSendPingAnswer` | `PLI_PONG` |
| 56 | 44 | `onSendWindowList` | `PLI_PROCESSLIST` |
| 57 | 163 | — | — |


Wire 163 has no gs2lib name. Slot 54 (wire 37, `PLI_LANGUAGE`) and slot 57 have no named send event in the 6.11 slot list.

## Incoming: wire id → native slot

Every wire id not listed here is cleared. Two more pairs are special **[lab]**:

- **252 (`0xfc`):** goes to a fixed routine that reads the server's key frame (`connector-script.md` §4c).
- **253 (`0xfd`):** the bundle id. It is stored and its slot is cleared, so a bundle is unpacked, never dispatched as a message.

| ---: | ---: | --- | --- |
| 0 | 48 | `setlevelboard` | `PLO_LEVELBOARD` |
| 1 | 55 | `addlevellink` | `PLO_LEVELLINK` |
| 2 | 88 | — | `PLO_BADDYPROPS` |
| 3 | 57 | — | `PLO_NPCPROPS` |
| 4 | 75 | — (by shape: `addlevelchest`) | `PLO_LEVELCHEST` |
| 5 | 76 | — | `PLO_LEVELSIGN` |
| 6 | 33 | `setserverlevel` | `PLO_LEVELNAME` |
| 7 | 51 | `setboardmodify` | `PLO_BOARDMODIFY` |
| 8 | 35 | — | `PLO_OTHERPLPROPS` |
| 9 | 1 | `setplayerprops` | `PLO_PLAYERPROPS` |
| 10 | 54 | `setisleader` | `PLO_ISLEADER` |
| 11 | 79 | — | `PLO_BOMBADD` |
| 12 | 80 | — (by shape: `removebomb`) | `PLO_BOMBDEL` |
| 13 | 73 | — | `PLO_TOALL` |
| 14 | 31 | — | `PLO_PLAYERWARP` |
| 15 | 34 | `setlevelfailed` | `PLO_WARPFAILED` |
| 16 | 9 | `setdisconnectmessage` (name not certain) | `PLO_DISCMESSAGE` |
| 17 | 86 | — | `PLO_HORSEADD` |
| 18 | 87 | — (by shape: `removehorse`) | `PLO_HORSEDEL` |
| 19 | 78 | — | `PLO_ARROWADD` |
| 20 | 82 | — | `PLO_FIRESPY` |
| 21 | 83 | — | `PLO_THROWCARRIED` |
| 22 | 84 | — | `PLO_ITEMADD` |
| 23 | 85 | — (by shape: `removeextra`) | `PLO_ITEMDEL` |
| 24 | 59 | — | `PLO_NPCMOVED` |
| 25 | 10 | `setserversignature` | `PLO_SIGNATURE` |
| 27 | 89 | — (by shape: `hurtbaddy`) | `PLO_BADDYHURT` |
| 28 | 6 | `setflagdata` | `PLO_FLAGSET` |
| 29 | 46 | — | `PLO_NPCDEL` |
| 30 | 19 | `downloadimagefailed` | `PLO_FILESENDFAILED` |
| 31 | 7 | `unsetflagdata` | `PLO_FLAGDEL` |
| 32 | 70 | — | `PLO_SHOWIMGPLAYER` |
| 33 | 2 | — | `PLO_NPCWEAPONADD` |
| 34 | 5 | `deleteweapon` | `PLO_NPCWEAPONDEL` |
| 35 | 12 | `setadminmessage` | `PLO_RC_ADMINMESSAGE` |
| 36 | 81 | — | `PLO_EXPLOSION` |
| 37 | 74 | — | `PLO_PRIVATEMESSAGE` |
| 38 | 65 | — (by shape: `pushaway`) | `PLO_PUSHAWAY` |
| 39 | 69 | `setlevelmodtime` | `PLO_LEVELMODTIME` |
| 40 | 63 | — | `PLO_HURTPLAYER` |
| 42 | 18 | `settimevar` | `PLO_NEWWORLDTIME` |
| 43 | 77 | `adddefaultweapon` | `PLO_DEFAULTWEAPON` |
| 45 | 20 | `downloadimagewasok` | `PLO_FILEUPTODATE` |
| 46 | 64 | — | `PLO_HITOBJECTS` |
| 47 | 42 | `setstaffguilds` | `PLO_STAFFGUILDS` |
| 48 | 8 | — | `PLO_TRIGGERACTION` |
| 49 | 32 | — | `PLO_PLAYERWARP2` |
| 67 | 29 | `setfolderlog` | `PLO_RC_FILEBROWSER_MESSAGE` |
| 68 | 21 | `downloadstart` | `PLO_LARGEFILESTART` |
| 69 | 23 | `downloadend` | `PLO_LARGEFILEEND` |
| 74 | 28 | — | `PLO_RC_CHAT` |
| 82 | 30 | — | `PLO_SERVERTEXT` |
| 84 | 22 | `downloadsetsize` | `PLO_LARGEFILESIZE` |
| 101 | 49 | `setrawboard` | `PLO_BOARDPACKET` |
| 102 | 24 | — | `PLO_FILE` |
| 104 | 26 | — (by shape: `setfilekey`) | `PLO_FILEDECRYPTKEY` |
| 105 | 91 | — | `PLO_UPDATEPACKAGESIZE` |
| 106 | 92 | `setpackageend` | `PLO_UPDATEPACKAGEDONE` |
| 107 | 50 | `setrawboard2` | `PLO_BOARDLAYER` |
| 108 | 94 | — | `PLO_PING` |
| 109 | 27 | — | `PLO_HTTPDOWNLOAD` |
| 110 | 90 | none: the empty slot, so this pair does nothing | `PLO_UNKNOWN110` |
| 111 | 17 | `setcookie` | `PLO_SETNETCOOKIE` |
| 131 | 56 | — (by shape: `setnpcscript`) | `PLO_NPCBYTECODE` |
| 134 | 36 | — | `PLO_GANISCRIPT` |
| 140 | 4 | — | `PLO_NPCWEAPONSCRIPT` |
| 150 | 60 | — | `PLO_NPCDEL2` |
| 151 | 61 | `deletelocalnpcs` | `PLO_HIDENPCS` |
| 153 | 45 | `readsign` | `PLO_SAY2` |
| 154 | 66 | `freezeplayer` | `PLO_FREEZEPLAYER2` |
| 155 | 67 | `unfreezeplayer` | `PLO_UNFREEZEPLAYER` |
| 156 | 53 | `setnpclevel` | `PLO_SETACTIVELEVEL` |
| 166 | 71 | — | `PLO_SHOWIMGNPC` |
| 168 | 38 | `setregged` | `PLO_ONLINEMODE` |
| 170 | 39 | `setisghost` | `PLO_GHOSTMODE` |
| 172 | 72 | — | `PLO_MINIMAP` |
| 173 | 40 | `setghostmessage` | `PLO_GHOSTTEXT` |
| 174 | 41 | `setghostsnear` | `PLO_GHOSTICON` |
| 176 | 13 | `setgraal2002server` | `PLO_KINGDOMSMODE` |
| 178 | 0 | `setserverwarp` | `PLO_SERVERWARP` |
| 179 | 44 | `setrpgmessage` | `PLO_RPGWINDOW` |
| 180 | 43 | `setstatusicons` | `PLO_STATUSLIST` |
| 182 | 15 | `getwindowlist` | `PLO_LISTPROCESSES` |
| 183 | 16 | `gethavewindow` | `PLO_HASPROCESSRUNNING` |
| 185 | 68 | — | `PLO_BOARDHEIGHTS` |
| 186 | 52 | `setboardmodify2` | `PLO_BOARDMODIFY2` |
| 187 | 25 | `setfileupdate` | `PLO_UPDATEPACKAGEISUPDATED` |
| 189 | 58 | — | `PLO_MOVE2` |
| 190 | 14 | `setserverlisterconnect` | `PLO_SERVERLISTCONNECTED` |
| 191 | 62 | — | `PLO_SHOOT2` |
| 194 | 47 | `deleteallnpcs` | `PLO_RESETCLIENT` |
| 195 | 37 | — | `PLO_LOADGANI` |
| 197 | 3 | — | `PLO_LOADSCRIPT` |
| 198 | 11 | `setserveroptions` | `PLO_SERVEROPTIONS` |

Notes on single rows:

- **110 → slot 90** is a dead pair, because slot 90 is the one empty native. So a 6.11 client given this script ignores PLO 110, as every older client does (`unknown-ids-2026-11-06.md`). **[lab]**
- **108 → slot 94:** 6.11 takes the ping through the ordinary table, not ahead of the main switch as 4.20 to 6.03 do **[lab]**. The answer would go out through send slot 55 (wire 162) **[inf]**.
- **Wire 100**, the raw-data length in older clients, is in the old-protocol set only. **[lab]**
- **Slot 16's** `tclient_*` string in 6.1.1.3 holds a zero byte, so the name `setdisconnectmessage` is a guess. Wire 16 is `PLO_DISCMESSAGE`, which fits it. **[bin][inf]**

## What this means for a server

A lab server that serves its own connector script chooses these tables. The live set is still worth matching, because it keeps the classic gs2lib wire ids for almost every message, both ways. A server that already speaks the gs2lib ids needs only the framing, the handshake and the cipher from `connector-script.md`. **[lab][inf]**

## Open

- [ ] Whether the 7.x scripts load the same tables. This needs a 7.x reply decrypted for its own launch.
- [ ] The handlers of the "—" slots that no `tclient_*` name or parse shape pins down.
