# Chat, private messages, and staff traffic

Date: 2026-10-21

Sources: GServer-v2 `TPlayer.cpp`, `TPlayerRC.cpp` (GPLv3, summarized); 2.05 tables. Tags as elsewhere.

## Chat bubble

How the line is drawn and how long it stays, per build: `client-internals/chat-text.md`.

Local chat is not a message id. It is the `PLPROP_CURCHAT` (12) string inside `PLI_PLAYERPROPS`. The server forwards it to the level as `PLO_OTHERPLPROPS`. Server commands typed in chat (`setnick`, `/sethead`, …) are parsed from the same prop. **[srv]** The one exception is toall: when the chat-bar text (lower-cased and trimmed) starts with `toall:`, 2.05 sends the rest as `PLI_TOALL` (6) instead of as CURCHAT. **[2.05]**

## Toall

| Dir | Id | Layout |
|-----|---:|--------|
| C→S | 6 TOALL | `GSTRING message` (2.05: text after `toall:`, trimmed, max 200 bytes) |
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

The staff tools run their own logins: RC `GSERV023`–`025`, NC `NCL11012`, RC2 type 6 on gen 5. NC packet layouts: `protocol/npc-control.md`. RC details: `tools/remotecontrol.md`.

## Profiles

| Dir | Id | Layout | 2.05 |
|-----|---:|--------|:----:|
| C→S | 80 PROFILEGET | rest = account | ✔ |
| C→S | 81 PROFILESET | 10 fields, each `c len` + text (see below) [2.05] | ✔ |
| S→C | 75 PROFILE | the same field list, relayed from the listserver [2.05] | ✔ |

### Profile field list (2.05) **[2.05]**
Both PROFILESET and PROFILE are a run of length-prefixed strings, `c(len) + text` each, read until the message ends. The fields come from the profile window, in this order:

| # | Field | Notes |
|--:|-------|-------|
| 0 | account | the profile's owner |
| 1 | real name | |
| 2 | age | |
| 3 | sex | `-` (unknown), `male`, or `female` |
| 4 | country | |
| 5 | ICQ number | |
| 6 | e-mail | |
| 7 | homepage | |
| 8 | favourite Graal hangout | |
| 9 | favourite quote | the quote box's lines joined with spaces, trimmed, cut to 220 characters |

Each text field is trimmed before sending. 2.05 sends PROFILESET from the profile window's Send button. Close on your own profile only keeps the edits locally. The Send button also works in another player's profile window (while that player is online), and then field 0 is **that player's** account, so a server must not take field 0 as proof of who is editing.

On PROFILE, 2.05 needs at least 10 fields (fewer and the packet is ignored). It drops field 0 and saves fields 1–9 to a local per-account profile file. The in-game stats in the same window (online time, kills, deaths, rating, alignment, max power, gralats, sword power, spin, level) are not in this packet; they most likely come from the player's props [inf].

## Open
- Whether 2.05 shows `PLO_STAFFGUILDS` anywhere.
