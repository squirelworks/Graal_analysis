# What GServer-v2 `master` does with some ids the manual left unmeasured

Date: 2026-11-12. Tags: **[srv]** reading of the public GPL GServer-v2 source, branch `master` at commit `efb5b90` (pinned 2026-11-12). Sources are cited by file under `server/src/TPlayer/`. The note summarises the code; it does not copy it. This is what one modern server reimplementation does. It is not proof of what the original server did, and the original client's reading of the same bytes is tagged separately in the manual rows.

The manual's §2.4 and §2.5 had `unmeasured` in the server-action or layout cells for the ids below.

## Client → server

| Id | Name | Layout the server reads | What the server does | Where |
| ---: | --- | --- | --- | --- |
| 14 | `PLI_CLAIMPKER` | `s killer id` | Ignored if the killer is unknown or is the sender. In a **sparring level**, it runs a Glicko-style rating update for both players: ratings are capped at 0–4000 and deviations at 50–350, it skips the update when both players share an IP address, and it sends the new `PLPROP_RATING` to the level and to the player. Elsewhere it adds one kill to the killer (unless `dontchangekills`), and with `apsystem` on it lowers the killer's AP when the victim had 20 or more, resetting the killer's AP timer from `aptime0`–`aptime4`. | `TPlayer.cpp`, `msgPLI_CLAIMPKER` |
| 21 | `PLI_PUTNPC` | `str image`, `str script file`, `c x×2`, `c y×2` | Only when `putnpcenabled` is set, and never with the NPC-server build. It loads the script file from the server's files, turns line breaks into `§`, and adds an NPC with that image and script at (x, y) in the sender's level. | `TPlayer.cpp`, `msgPLI_PUTNPC` |
| 22 | `PLI_NPCDEL` | `i3 npc id` | Deletes that NPC if it exists. Off with the NPC-server build. | `TPlayer.cpp`, `msgPLI_NPCDEL` |
| 31 | `PLI_PACKETCOUNT` | `s count` | Compares the count with the server's own count of packets received since the last 31. If they differ, or the count is above 10000, it logs a warning. Either way it resets its counter. It does not disconnect. | `TPlayer.cpp`, `msgPLI_PACKETCOUNT` |
| 32 | `PLI_ITEMTAKE` | `c x×2`, `c y×2`, … | Shares the handler with 13 `PLI_ITEMDEL`. It relays `PLO_ITEMDEL` (23) with the same body to the other players in the level, and removes the item at (x, y). For 32 only, it also gives the item to the sender as a player property, which is sent to the level and to the sender. | `TPlayer.cpp`, `msgPLI_ITEMDEL` |
| 40 | `PLI_SHOOT` | `i3 shot id` (the source notes it was always 0 in its tests), `c x`, `c y`, `c z+50` (each read as tiles ×16 to pixels), `c angle` (0–220 = 0–π), `c z angle`, `c speed` (pixels per tick), `str gani`, `c params length` (not enforced), `rest` = shoot params | Re-sent to the players in the level area: as `PLO_SHOOT` to clients older than 5.07, and as `PLO_SHOOT2` (gravity 8) to 5.07 and later. | `TPlayer.cpp`, `msgPLI_SHOOT` |
| 48 | `PLI_SHOOT2` | (the layout already in the manual) | Re-sent the same way as 40, in both forms. | `TPlayer.cpp`, `msgPLI_SHOOT2` |
| 130 | `PLI_REQUESTUPDATEBOARD` | (the layout already in the manual) | Logs it and **sends nothing back**. The source marks the reply as unknown. | `TPlayer.cpp`, `msgPLI_REQUESTUPDATEBOARD` |
| 152 | `PLI_REQUESTTEXT` | `rest` = a gtokenized list: weapon, type, option, … | It switches on type and option. `lister` options go to the listserver (`simplelist`, `rebornlist`, `serverinfo`) or are answered locally with fixed lists (`subscriptions`, `bantypes`, `getglobalitems`). `pmservers` and `pmguilds` go to the listserver. `pmserverplayers` and `pmunmapserver` add or remove a PM server. `packageinfo` answers with a package's file count and total size. Local answers are `PLO_SERVERTEXT` (82), which echoes weapon, type and option first. | `TPlayerRequestText.cpp` |
| 154 | `PLI_SENDTEXT` | same gtokenized list | The same dispatch for actions, such as the `irc` login, which answers an RC with `PLO_ADDPLAYER` for the channel. | `TPlayerRequestText.cpp` |
| 157 | `PLI_UPDATEGANI` | `i5` CRC-32 of the client's gani bytecode, `rest` = gani name without `.gani` | If the gani exists, it sends the compiled gani when the CRC differs. It then always sends `PLO_UNKNOWN195` with the name and `"SETBACKTO <gani>"` (the source says 4.x and later need it). An unknown gani gets no reply. | `TPlayerScripts.cpp`, `msgPLI_UPDATEGANI` |
| 159 | `PLI_UPDATEPACKAGEREQUESTFILE` | `c name length`, package name, `c install type` (1 install, 2 reinstall), `rest` = one `i5` CRC-32 per package file, in the package's order | Reinstall ignores the CRCs. It sends `PLO_UPDATEPACKAGESIZE` (package name and total size of the files whose CRC differs), then each such file, then `PLO_UPDATEPACKAGEDONE` (106). | `TPlayerUpdatePackages.cpp` |

The 159 layout here differs from the one in the manual ("an order value, package file name, modtime"), which came from an older server reading. The client side has not been read, so both readings stay tagged **[srv]**.

## Server → client

| Id | Name | Layout the server writes | When | Where |
| ---: | --- | --- | --- | --- |
| 55 | `PLO_ADDPLAYER` | `s id`, `str account`, then player-property pairs (`PLPROP_NICKNAME` + string, `PLPROP_UNKNOWN81` + one byte for the player type) | To RCs, for each player at login and for external (PM-server) players. Game clients get it only on the external-player path. | `TPlayerLogin.cpp`, `TPlayerExternalPlayers.cpp` |
| 56 | `PLO_DELPLAYER` | `s id` | To RCs when a player leaves, and for external players. | `TPlayer.cpp`, `TPlayerExternalPlayers.cpp` |
| 82 | `PLO_SERVERTEXT` | `rest` = gtokenized list, starting with the request's weapon, type and option | Answers 152 and 154 | `TPlayerRequestText.cpp` |
| 106 | `PLO_UPDATEPACKAGEDONE` | `rest` = package name | After the files of a 159 request | `TPlayerUpdatePackages.cpp` |
| 187 | `PLO_UPDATEPACKAGEISUPDATED` | `rest` = file name + `\n` | To players when an RC uploads a new version of a game file that already existed. A `.gani` is recompiled and its bytecode is re-sent. | `TPlayerRC.cpp` |
