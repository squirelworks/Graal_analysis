# v7 Graal3DEngine: chat, movement, world, UDP

Date: 2026-11-08

Target: WorldsSetup64-614. Tags: **[bin]** · **[doc]** classic layouts where v7 only names the event.

No addresses. Wire ids are remapped — use event / `tclient_*` names, not classic numeric ids, unless a live remapper dump says otherwise.

---

## 1. Chat **[bin]**

| Direction | Name | Payload (one line) |
|---|---|---|
| C→S | `onSendToAllChat` (logical PLI slot 3, shares remapper cell 2) | to-all chat text |
| C→S | `onSendPrivateMessage` (slot 50) | PM envelope (count / ids / text — classic shape **[doc]**) |
| C→S | `onSendRCChat` (slot 26) | RC chat |
| S→C | `tclient_settoallmsg` | to-all text |
| S→C | `tclient_setprivatemessage` | PM envelope |
| S→C | `tclient_setadminmessage` / `setrpgmessage` / `setghostmessage` | message variants |
| S→C | `tclient_receivetext` | generic text / dialog |

---

## 2. Board / level / warp **[bin]**

| Direction | Name | Payload |
|---|---|---|
| C→S | `onSendBoardModify` / `BoardModify2` | board modify delta / v2 |
| C→S | `onSendLevelWarp` / `LevelWarpModtime` | level warp (± modtime) |
| C→S | `onSendEnterLevel` | enter level |
| C→S | `onSendPreloadLevel` | preload |
| C→S | `onSendServerWarp` | server warp request |
| S→C | `tclient_setboardmodify` / `setboardmodify2` | board deltas |
| S→C | `tclient_setlevelboard` / `setrawboard` / `setrawboard2` | full/raw board |
| S→C | `tclient_setserverwarp` / `playerwarped2` | warp |
| S→C | `tclient_setlevelmodtime` / `setserverlevel` / `setlevelheights` / `setlevelfailed` | level meta |

Movement props still ride the **player prop stream** (`X`/`Y`/`Z` / `X2`… and `onServerSetPlayerX/Y/Z` cleartext setters). **[bin]**

---

## 3. UDP / peer path **[bin][inf]**

| Evidence | Reading |
|---|---|
| PLPROP still has **UDPPORT** / **IPADDR** encodings in the player encode switch | classic peer fields remain in the prop codec |
| No clear `udpsocket` / bind-to-14900 style Graal-P2P strings recovered in this pass | |
| Exports include **LiteNetLib** / **MLAPI** native-invoke stubs | Unity multiplayer plugins, separate from classic Graal UDP peer |

**Verdict:** classic UDP peer **codec fields** still exist on the player object; a dedicated Graal UDP socket path was **not** confirmed as live in v7-614. Treat peer UDP as **legacy-capable / unused unless a session proves otherwise**. Unity LiteNetLib is a different channel. **[inf]**

---

## 4. vs 6.x

Event names match the 6.11 `onSend*` / `tclient_*` set. Framing may be classic or `setprotocol` (default classic until connector). Chat/board/warp semantics unchanged at the name layer.
