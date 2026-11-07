# v7 Graal3DEngine: PLI / PLO tables (start)

Date: 2026-11-08

Target: Worlds `WorldsSetup64-614` `unpacked_Graal3DEngine.dll`. Tags: **[bin]** this build · **[doc]** 6.11 slot lexicon for continuity.

No addresses in this file. Machine JSON: `Graal_analysis/_work/ghidra_v7_614/pli_plo_tables.json`.

---

## Model (short)

| Direction | Script API | Remapper |
|---|---|---|
| Client → server (PLI-side) | `onSend*` events when remapper cell is `0xFE` | `setoutdatahandlers` 256 dwords: internal message → wire id **or** `0xFE` |
| Server → client (PLO-side) | `tclient_*` natives + script | `setindatahandlers` pairs: wire id → handler byte |

**Sentinels on inbound install** **[bin]**

| Value | Meaning |
|---|---|
| `< 0x5F` | native handler index (95-entry table) |
| `0xFE` | deliver to script |
| `0xFF` | ignore |
| `0xFC` | stash special id / fixed stub |
| `0xFD` | stash special id / null handler |

Classic dispatch still uses `id = byte - 0x20`. Special length wrap: internal ids `0x5D` / `0xA3` → length as 3-byte GCHAR, resent as id `0x32`. **[bin]**

**Do not** read `logical_slot` or `remapper_cell` as on-wire ids. Wire ids are whatever the connector script writes into the remapper at runtime.

---

## 1. PLI — finished slot table **[bin][doc]**

### How to read the columns

| Column | Meaning |
|---|---|
| **Logical slot** | 6.11 numbering (kept so docs/scripts line up) |
| **Remapper cell** | Dword the FE bridge actually reads in v7 |
| **Event** | Decrypted `onSend*` name (`onsend` + suffix below) |
| **Cell note** | `own` = exclusive cell; `shared←N` = odd logical slot shares remapper cell N |

**v7 layout fact:** several historically adjacent 6.11 slots **share one remapper cell** (the even index). Both bridges fire against that same cell. Gaps 1, 3, 5, 7, 9, 13, 15, 19, 21, 23, 25, 27, 29, 31 are filled as events; they are not missing from the client — they do not own a separate remapper dword. **[bin]**

**Resolved:** `onsendi?pker` → **`onsendispker`** / `onSendIsPKer`. **[bin]**

**Slot 54:** unused (no event), same as 6.11. **[bin][doc]**

**Slot 45 (`onsendnpcproperties`):** vacant remapper cell between playerproperties and flag; **no FE bridge recovered** in this image. Name kept from 6.11 for continuity. **[bin][doc]**

### Table

| Logical | Cell | Cell note | Event (`onSend…`) | Payload (one line) |
|---:|---:|---|---|---|
| 0 | 0 | own | WantWeaponScript | request weapon script by name |
| 1 | 0 | shared←0 | WantClassScript | request class script by name |
| 2 | 2 | own | WantGaniScript | request gani script by name |
| 3 | 2 | shared←2 | ToAllChat | to-all chat text |
| 4 | 4 | own | IsPKer | PKer / hostile flag |
| 5 | 4 | shared←4 | CarryThrown | carry / thrown sprite |
| 6 | 6 | own | AddHorse | add horse |
| 7 | 6 | shared←6 | DelHorse | delete horse |
| 8 | 8 | own | AddBomb | add bomb |
| 9 | 8 | shared←8 | DelBomb | delete bomb |
| 10 | 10 | own | ServerWarp | request server warp |
| 11 | 11 | own | TriggerAction | trigger-action |
| 12 | 12 | own | FireSpying | fire-spy state |
| 13 | 12 | shared←12 | Explosion | explosion |
| 14 | 14 | own | WeaponHit | weapon hit |
| 15 | 14 | shared←14 | PlayerHurt | player hurt |
| 16 | 16 | own | DeleteNPC | delete NPC |
| 17 | 17 | own | DeleteWeapon | delete weapon |
| 18 | 18 | own | Extra | extra / item put |
| 19 | 18 | shared←18 | TakeExtra | take extra / item |
| 20 | 20 | own | RemoveExtra | remove extra / item |
| 21 | 20 | shared←20 | OpenChest | open chest |
| 22 | 22 | own | Shot | shot / projectile fire |
| 23 | 22 | shared←22 | BaddyProperties | baddy prop stream (C→S) |
| 24 | 24 | own | BaddyHurt | baddy hurt |
| 25 | 24 | shared←24 | WeaponImage | weapon image |
| 26 | 26 | own | RCChat | RC chat |
| 27 | 26 | shared←26 | RequestText | request text file |
| 28 | 28 | own | SetText | set text file |
| 29 | 28 | shared←28 | FileDeletion | delete file |
| 30 | 30 | own | FolderDeletion | delete folder |
| 31 | 30 | shared←30 | FileRename | rename file |
| 32 | 32 | own | FilesMove | move files |
| 33 | 33 | own | HaveWindow | have-window report |
| 34 | 34 | own | EnterLevel | enter level |
| 35 | 35 | own | WantImage | request image |
| 36 | 36 | own | ImageUpdate | image update |
| 37 | 37 | own | ImageUpdateCRC | image update with CRC |
| 38 | 38 | own | LevelWarp | level warp |
| 39 | 39 | own | LevelWarpModtime | level warp + modtime |
| 40 | 40 | own | DownloadFile | download / want file |
| 41 | 41 | own | BoardModify | board modify |
| 42 | 42 | own | BoardModify2 | board modify v2 |
| 43 | 43 | own | PreloadLevel | preload level |
| 44 | 44 | own | PlayerProperties | `(GCHAR id,value)*` player props |
| 45 | 45 | **no FE bridge** | NPCProperties | NPC prop stream (C→S) — **[doc]** name only |
| 46 | 46 | own | Flag | set flag |
| 47 | 47 | own | UnsetFlag | unset flag |
| 48 | 48 | own | Projectile | projectile |
| 49 | 49 | own | UpdatePackage | update package |
| 50 | 50 | own | PrivateMessage | private message |
| 51 | 51 | own | UploadStart | upload start |
| 52 | 52 | own | SaveFile | save-file upload body |
| 53 | 53 | own | UploadEnd | upload end |
| 54 | — | unused | — | — |
| 55 | 55 | own | PingAnswer | ping answer |
| 56 | 56 | own | WindowList | window list |

Payload shapes beyond the one-liners (exact field order for board modify, PM envelope, etc.) continue in later topic notes.

---

## 2. PLO — inbound handler table (start) **[bin]**

Inbound natives are exposed to script as **`tclient_*`** names (decrypted in v7). The 95-entry native table is indexed by the low handler byte from `setindatahandlers`. **Wire id → slot is not published here** (runtime script table only).

### Prop / board / chat (high confidence payloads)

| `tclient_*` | Payload (one line) | Notes |
|---|---|---|
| `setplayerprops` | `(GCHAR id,value)*` self | encode/decode switches match classic PLPROP **[bin]** |
| `setotherplayerprops` | `GSHORT` player id + prop stream | classic OTHERPLPROPS shape **[doc][bin]** |
| `setnpcprops` | `GINT3` npc id + prop stream | NPCPROP switch present **[bin]** |
| `setbaddyprops` | `GCHAR` baddy id + prop stream | **[doc][bin]** |
| `setlevelboard` | level board / tiles | |
| `setboardmodify` | board modify delta | pairs with PLI BoardModify |
| `setboardmodify2` | board modify v2 | |
| `setrawboard` / `setrawboard2` | raw board blob | |
| `settoallmsg` | to-all chat text | |
| `setprivatemessage` | PM envelope | |
| `setflagdata` / `unsetflagdata` | flag name (+ value) | |
| `setplayerhurt` | hurt / hearts update | |
| `receivetext` / `readsign` | text / sign | |
| `setadminmessage` / `setrpgmessage` / `setghostmessage` | message variants | |

### Script / package / file

| `tclient_*` | Payload (one line) |
|---|---|
| `setscript` | weapon/class script body |
| `setscriptchecksum` | script id + CRC (+ key fields on cache path) |
| `setnpcscript` | NPC script body |
| `setganiscript` / `setganidata` | gani script / data |
| `setpackagestart` / `setpackageend` | package transfer bookends |
| `downloadstart` / `downloadadddata` / `downloadsetsize` / `downloadend` | file download |
| `downloadimagewasok` / `downloadimagefailed` | image download result |
| `setfilekey` / `setfileupdate` / `setfileredirect` / `setfolderlog` | file helpers |

### World / actors / misc (name-level; field order TBD)

| Group | Names |
|---|---|
| Warp / level | `setserverwarp`, `playerwarped2`, `setlevelmodtime`, `setserverlevel`, `setlevelheights`, `setlevelfailed` |
| NPC lifecycle | `setnpcmove`, `setnpclevel`, `setnpcremoved`, `deletenpc`, `deletelocalnpc(s)`, `deleteallnpcs` |
| Combat props | `addbomb`/`removebomb`, `addhorse`/`removehorse`, `addexplosion`, `addextra`/`removeextra`, `setnewproj`, `hurtbaddy`, `setweapon`, `adddefaultweapon`, `addarrow` |
| Level objects | `addlevelchest`, `addlevellink`, `addlevelsign` |
| Ghost / social | `setghostsnear`, `setisghost`, `setisleader`, `setstaffguilds`, `setstatusicons` |
| Session | `setencryptionin`, `setconnectionattributes`, `setserverlisterconnect`, `setserveroptions`, `setserversignature`, `setping`, `setcookie`, `setregged`, `setgraal2002server`, `settimevar` |
| UI | `getwindowlist`, `gethavewindow`, `freezeplayer`, `unfreezeplayer`, `pushaway`, `setcarrythrown`, `setfirespy` |
| Object mgmt | `createtclient`, `deletetclient` |
| Truncated decrypt | `setdisconne…` (disconnect-related; full spelling not recovered) |

Full alphabetical dump: `pli_plo_tables.json` → `plo_tclient` (92 names).

### Native slot correlation **[bin]**

| Result | Detail |
|---|---|
| Native table | 95 slots (`< 0x5F`); many bodies present |
| Static name↔slot array | **not recovered** (no pointer table of `tclient_*` blobs in slot order; encrypted names lack direct xrefs) |
| Codec anchors | player-prop decode and NPC-prop decode bodies identified inside the native set |
| Practical label | use **`tclient_*` name** as the stable inbound API; remapper pairs wire id → slot at runtime |

Claiming a full 0…94 name list would be guessing — left open on purpose.

---

## 3. vs 6.11 **[doc][bin]**

| Topic | 6.11 | v7-614 |
|---|---|---|
| `onSend*` cleartext | yes | encrypted; recovered above |
| Slot 0…56 event set | yes | same names; shared remapper cells for early pairs |
| `tclient_*` inbound | ~90 named | 92 decrypted; same family |
| Wire-id tables | script-loaded | script-loaded (unchanged model) |

---

## 4. Next

1. Finish native-slot ↔ `tclient_*` for the 95-entry table + payload field orders.  
2. Property stream note (PLPROP / NPCPROP / BDPROP full id ranges).  
3. GS2 / GRESCR VM note.
