<!-- manual: kind=reference status=draft -->
# 2.8 Chat and private messages

The message layouts are in → §2.4.8 (client to server) and → §2.5.8 (server to client). How the client draws chat and nicknames is behaviour, in → §4.

> Status: draft.

## 2.8.1 Local chat

| Rule | Builds | Source |
| --- | --- | --- |
| Local chat is not a message: it is the CURCHAT prop (12) inside `PLI_PLAYERPROPS`; the server forwards it to the level as `PLO_OTHERPLPROPS` | server; 2.05 | [srv] (protocol/chat-pm-rc.md#chat-bubble) |
| Server commands typed in chat (`setnick`, `/sethead` and the like) are parsed by the server from the same prop | server | [srv] (protocol/chat-pm-rc.md#chat-bubble) |
| When the chat-bar text, lower-cased and trimmed, starts with `toall:`, 2.05 sends the rest as `PLI_TOALL` (6) instead | 2.05 | [2.05] (protocol/chat-pm-rc.md#chat-bubble) |
| A line longer than 256 characters is cut to its first 253 characters plus `...` when sent; the receiver draws whatever arrives | 2.05 | [2.05] (client-internals/chat-text.md#length) |
| When the player's own line times out (3 s after the first move), the client sends an empty CURCHAT | 2.05 | [2.05][cap] (client-internals/chat-text.md#how-long-it-stays-live-205-rev-2-2026-10-30) |
| A typed `showname` is not sent to the server | 2.05 | [2.05][cap] (client-internals/chat-text.md#nickname-131-to-231) |
| Chat also goes peer to peer as UDP id 22 (→ §2.9) | 2.00 to 2.05, 3.04 | [2.05] (protocol/udp-p2p.md#udp-ids-own-dispatcher-not-plipl-numbering) |

## 2.8.2 Private messages

| Rule | Builds | Source |
| --- | --- | --- |
| A PM names its recipients by player id (`s count`, then the ids), so one message can go to several players | server; 2.05 | [srv][2.05] (protocol/chat-pm-rc.md#private-messages) |
| Mass PMs and guild PMs use the same message with different type labels, such as `"Server Message:"` or `"Guild message:"` | server | [srv] (protocol/chat-pm-rc.md#private-messages) |
| Players in jail can PM only RCs | server | [srv] (protocol/chat-pm-rc.md#private-messages) |
| ADDITFLAGS bit `0x01` blocks mass messages and `0x04` blocks toall (→ §2.6.2.2) | server | [srv] (protocol/player-props.md#additflags-srv) |

## 2.8.3 Staff messages

| Rule | Builds | Source |
| --- | --- | --- |
| An admin message reaches a game client as `PLO_RC_ADMINMESSAGE` (35), `Admin <account>:` followed by `0xA7` and the text | server; 2.05 | [srv][2.05] (protocol/chat-pm-rc.md#admin-and-staff) |
| The staff-guild list is sent at login as `PLO_STAFFGUILDS` (47) | server; 2.05 | [srv][2.05] (protocol/chat-pm-rc.md#admin-and-staff) |
| The staff tools run their own logins: RC `GSERV023` to `GSERV025`, NC `NCL11012`, RC2 as type 6 on generation 5 (→ §7) | server | [srv] (protocol/chat-pm-rc.md#admin-and-staff) |

## 2.8.4 Buddy and list text requests

| Rule | Builds | Source |
| --- | --- | --- |
| Buddy requests go in `PLI_SENDTEXT` as the tokens `GraalEngine`, `lister`, then `verifybuddies`, `addbuddy` or `deletebuddy`, then the account list | 2.17+; server | [srv] (client-internals/feature-specs/14-friends-ignore.md#server-behaviour-srv) |
| The server forwards those three options to the listserver, never for guest accounts, and stores nothing itself | server | [srv] (client-internals/feature-specs/14-friends-ignore.md#server-behaviour-srv) |
| The listserver answers with `PLO_SERVERTEXT` (82) carrying `weapon`, `lister`, `buddylist`, then a comma list of accounts | listserver | [srv] (client-internals/feature-specs/14-friends-ignore.md#server-behaviour-srv) |
| `PLI_REQUESTTEXT` types `pmservers`, `pmserverplayers <server>`, `pmunmapserver` and `pmguilds` go to the listserver for the cross-server and guild tabs | server | [srv] (client-internals/feature-specs/14-friends-ignore.md#server-behaviour-srv) |
| A real 2.22 client sent no buddy request on add or delete; it only wrote `buddyaccounts.txt`, so the token layout on the wire is unmeasured (→ §4.10.5.2) | 2.22 | [cap] (client-internals/feature-specs/14-friends-ignore.md#lab-findings-from-a-real-222-client-2026-10-24-cap) |
| `PLI_MUTEPLAYER` (43) is `s playerId, c 1/0`; GServer-v2 registers no handler, so it counts as an invalid packet, and more than 5 invalid packets disconnect the client; two sends from a 2.22 client did not | 2.17+; server | [srv][cap] (client-internals/feature-specs/14-friends-ignore.md#server-behaviour-srv) |

## 2.8.5 Profiles

| Rule | Builds | Source |
| --- | --- | --- |
| `PLI_PROFILESET` and `PLO_PROFILE` are a run of `c length` + text fields, read until the message ends | 2.05 | [2.05] (protocol/chat-pm-rc.md#profile-field-list-205-205) |
| The profile is relayed from the listserver (→ §6) | 2.05 | [2.05] (protocol/chat-pm-rc.md#profiles) |
| 2.05 sends PROFILESET from the profile window's Send button, which also works in another online player's window; Close on your own profile only keeps the edits locally | 2.05 | [2.05] (protocol/chat-pm-rc.md#profile-field-list-205-205) |
| On PROFILE, 2.05 needs at least 10 fields, drops field 0 and saves fields 1 to 9 to a local per-account profile file | 2.05 | [2.05] (protocol/chat-pm-rc.md#profile-field-list-205-205) |
| The in-game stats in the same window (online time, kills, deaths, rating and so on) are not in this message; they most likely come from the player's props | 2.05 | [inf] (protocol/chat-pm-rc.md#profile-field-list-205-205) |

| Field | Content | Source |
| ---: | --- | --- |
| 0 | account, the profile's owner | [2.05] (protocol/chat-pm-rc.md#profile-field-list-205-205) |
| 1 | real name | [2.05] (protocol/chat-pm-rc.md#profile-field-list-205-205) |
| 2 | age | [2.05] (protocol/chat-pm-rc.md#profile-field-list-205-205) |
| 3 | sex: `-` (unknown), `male` or `female` | [2.05] (protocol/chat-pm-rc.md#profile-field-list-205-205) |
| 4 | country | [2.05] (protocol/chat-pm-rc.md#profile-field-list-205-205) |
| 5 | ICQ number | [2.05] (protocol/chat-pm-rc.md#profile-field-list-205-205) |
| 6 | e-mail | [2.05] (protocol/chat-pm-rc.md#profile-field-list-205-205) |
| 7 | homepage | [2.05] (protocol/chat-pm-rc.md#profile-field-list-205-205) |
| 8 | favourite Graal hangout | [2.05] (protocol/chat-pm-rc.md#profile-field-list-205-205) |
| 9 | favourite quote: the quote box's lines joined with spaces, trimmed, cut to 220 characters | [2.05] (protocol/chat-pm-rc.md#profile-field-list-205-205) |

Each text field is trimmed before sending [2.05] (protocol/chat-pm-rc.md#profile-field-list-205-205).

## 2.8.6 Unpacked Windows 6.1.1.3

| Rule | Builds | Source |
| --- | --- | --- |
| Another player's line arrives as the script event `onToall`, raised by `tclient_settoallmsg` on the TCP incoming path. The UDP callback does not raise it | 6.1.1.3 | [bin] (protocol/v6113-chat.md#the-arrival-path) |
| No compiled PLO id is assigned to that event. The wire id is the script pair, which is not in the image | 6.1.1.3 | [bin] (protocol/v6113-chat.md#which-plo) |
