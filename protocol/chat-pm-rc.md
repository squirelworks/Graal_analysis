# Chat, private messages, and staff traffic

Date: 2026-10-21

Sources: GServer-v2 `TPlayer.cpp`, `TPlayerRC.cpp` (GPLv3, summarized); 2.05 tables. Tags as elsewhere.

## Chat bubble

Local chat is not a message id. It is the `PLPROP_CURCHAT` (12) string inside `PLI_PLAYERPROPS`. The server forwards it to the level as `PLO_OTHERPLPROPS`. Server commands typed in chat (`setnick`, `/sethead`, …) are parsed from the same prop. **[srv]** 2.05 has no sender for `PLI_TOALL` (6), so 2.05 probably has no toall chat. **[2.05][inf]**

## Toall

| Dir | Id | Layout |
|-----|---:|--------|
| C→S | 6 TOALL | `str message` |
| S→C | 13 TOALL | `s player id`, `str message` (2.05 handles it) |

## Private messages

| Dir | Id | Layout | 2.05 |
|-----|---:|--------|:----:|
| C→S | 28 PRIVATEMESSAGE | `s count`, `count × s player id`, rest = message (gtokenized) | ✔ |
| S→C | 37 PRIVATEMESSAGE | `s from id`, rest = `"type","message"` as a quoted, comma-separated list. The type is a label such as `"Server Message:"`, `"Guild message:"`, or empty | ✔ |

Mass PMs and guild PMs use the same packet with different type labels. Players in jail can PM only RCs. **[srv]**

## Admin and staff

| Dir | Id | Name | Notes | 2.05 |
|-----|---:|------|-------|:----:|
| S→C | 35 | RC_ADMINMESSAGE | rest = `Admin <account>:\xa7<text>` | ✔ |
| S→C | 47 | STAFFGUILDS | `"guild",` repeated (quoted, comma-terminated), sent at login | ✔ |
| S→C | 74 | RC_CHAT | RC console line | · |
| C→S | 51–98 | RC_* | server options, folder config, player props get/set, accounts, bans, rights, comments, file browser | · (RC client only) |
| C→S | 103–119 | NC_* | NPC-control: NPC get/set/warp, classes, weapons | · |

The staff tools run their own logins: RC `GSERV023`–`025`, NC `NCL11012`, RC2 type 6 on gen 5. Their packet details live in `tools/remotecontrol.md`.

## Profiles

| Dir | Id | Layout | 2.05 |
|-----|---:|--------|:----:|
| C→S | 80 PROFILEGET | rest = account | ✔ |
| C→S | 81 PROFILESET | account + field list (exact layout not yet traced) [inf] | ✔ |
| S→C | 75 PROFILE | rest = profile blob relayed from the listserver | ✔ |

## Open
- The field order of a 2.05 profile (2.05 predates the listserver profile fields in `SVO_GETPROF`).
- Whether 2.05 shows `PLO_STAFFGUILDS` anywhere.
