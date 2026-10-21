# Graal3D protocol

Date: 2026-10-21

The Graal3D client and server use TCP port 14901, plus UDP from client to client. Static reads only; not yet checked on the wire.

## Encoding

The same text codec as 2D Graal (see `protocol/PROTOCOL-CHEATSHEET.md`):

- `c(v)` is one byte, `v + 32`.
- `sN(v)` is an N-byte unsigned integer, 7 bits per byte, most significant first, each byte `+ 32`.
- `str(s)` is `c(len)` then the bytes.

## TCP frames

```
[u16 BE length] [zlib block]
```

The zlib block holds one or more messages, each `c(id)` + payload + `\n`. Both sides queue messages and compress when the queue passes 4096 bytes or on the frame-tick flush. A client drops the link if more than 256 KiB of compressed output is pending. The client sends in 256-byte slices. The receive side inflates into a buffer of up to 256,000 bytes.

There is no key byte or scramble. A message must not contain `\n`; text with line breaks (level files, admin messages) replaces each `\n` with `§` (0xA7).

## Login

The first line from the client:

```
c(0)  "GR3DV002"  str(account)  str(password)
```

The server reads the version at bytes 2 to 9. `GR3DV001` gets packet 5 "You need at least Graal3D beta2…". If an account is missing, in use or disabled, the server sends 5 with the matching text. A line with id 1 and the same layout is an admin login. It needs an account with admin level ≥ 1, puts the session on the admin list, and gets the account list (50) and player list (55).

On TCP accept, before login, the server sends `6` with `c(0)`.

On a player login the server:
1. Links the account and applies the props saved in the account record (see `formats.md`).
2. Sends `3` (own props: id, x, y, z, angle, animation).
3. For each other player, sends `2` (their props) to the new player and the new player's props to them.
4. Sends the player to their level (below).
5. Tells admin sessions with `55`.

## Server → client

| Id | Name used here | Payload | Client action |
|---|---|---|---|
| 0 | LEVEL | level file text, `\n` as `§`, or empty | Saves the text under the current level name and loads it as a `.x` mesh. Empty means "you already have it". |
| 1 | LEVELNAME | rest = file name | Stored as the current level name. |
| 2 | OTHERPLPROPS | `c(player id)` + props | Creates the player on first sight, then applies the props. |
| 3 | PLAYERPROPS | props | Applies to the local player. |
| 4 | (leader) | empty | Sent to the first player in a level, and to the next one when the first leaves. The client sets a flag that packet 0 clears. |
| 5 | DISCMESSAGE | rest = text | Stored. Shown when the socket closes ("You have been disconnected from the server." if empty). |
| 6 | (session) | `c(v)` | Stores `v` in a global. The server sends 0 on accept. |
| 7 | FILESENDFAILED | rest = file name | Not handled by the client. |
| 8 | ADMINMESSAGE | rest, `§` = line break | Shown in an "Administrator message" box. |
| 16 | (2D discmessage) | text | Not handled. Sent only by the server's player-list kick button. |
| 50–59 | admin replies | see below | Admin sessions only. |
| 100 | RAWDATA | `s3(len)` | The client flags the next line as raw and then discards it. |
| 101 | FILE | `str(name)` + bytes | Server answer to request 2. Unused by this client. |

## Client → server

| Id | Payload | Server action |
|---|---|---|
| 0 | login (above) | |
| 1 | props | Applies, then relays (below). |
| 2 | file name | Looks in `levels\`. Sends 100 + 101 if the file is under 64,500 bytes, else 7. Never sent by the shipped client. |

Admin commands (51–64) are listed at the end.

## Player properties

The same prop ids are used in both directions and inside UDP. A props payload is a run of `c(prop id)` + value with no separators.

| Id | Value | Field | Default | Client sends |
|---|---|---|---|---|
| 0 | `c` | player id (1–200) | – | no |
| 1 | `s2` | x: `(v − 8000) / 2` | 0 | yes |
| 2 | `s2` | y, same scale | 0 | yes |
| 3 | `s2` | z, same scale | 0 | yes |
| 4 | `c` | angle: `v × 2` degrees | 0 | yes |
| 5 | `s2` | animation frame (likely) | 0 | yes |
| 6 | `str` | body model | `body.x` | yes |
| 7 | `str` | head model | `head.x` | yes |
| 8 | `str` | body texture (reloads on change) | `body.bmp` | yes |
| 9 | `str` | head texture | `man.bmp` | yes |
| 10 | 4 bytes, 6 bits each | arm colour, 24-bit RGB | `FF0000` | yes |
| 11 | 4 × 6 bits | shoe colour | `800000` | yes |
| 12 | `str` (≤ 200) | nickname, optional ` (guild)` | – | yes |
| 13 | `str` (≤ 200) | chat text | – | yes |
| 14 | `str` | level file | `level1.x` (client), `startlevel.x` (server) | no |
| 15 | `s3` | UDP port, 0 = none | 0 | yes (its own bound port) |
| 16 | 5 bytes: 4 bits then 4 × 7 | IPv4 address, packed in 32 bits | – | no (the server fills in the TCP peer address) |
| 17 | 4 × 6 bits | hand colour | `FDCC47` | yes |
| 50 | `c` | 1 = this player is in your level (add as UDP peer), 0 = not | – | server only |
| 51 | none | player left: remove | – | server only |

The colour props map to mesh pairs: 10 to the two arms, 17 to the two hands, 11 to the two feet. The pairing comes from the mesh slots each prop recolours plus the config key names.

Each tick the client re-encodes all props it sends, compares them with the last tick, and sends the changed ones as one `1` message. Props 1–5 are also compared separately for UDP (below). The first send after connecting carries the full look (6–12 and 15).

### Server relay rules

- On prop 12, the server splits `nick (guild)`. It keeps the tag only if `guilds\guild<guild>.txt` lists the account, and echoes the result back with `3`. The nickname then goes to every player (2) and every admin session (59).
- On prop 15, the server broadcasts to every player.
- On prop 14, the player changes level (below).
- Prop 16 from a client is ignored while the player has a live socket.
- Other changes go to players in the same level with `2`. **Props 1–5 and 13 are left out when both players have a UDP port**, because those go peer to peer. Each observer has its own dirty set, so a player who was skipped gets the missing props later.

### Level change

1. The server finds the level in its cache, or loads it from `levels\<name>`.
2. It sends `1` (name), then `0` with the file text, or `0` empty if this player was already sent that level.
3. For each player already in the level, it sends both sides `2` with `50 = 1` and the props that player has not yet seen.
4. If the player is alone in the level, it sends `4`.
5. It tells admin sessions with `59`.

On leaving a level the others get `50 = 0`. On disconnect every player gets `c(id)` + prop 51.

## UDP (client to client)

The client binds one UDP socket (port 0, or the fixed port from the config) unless `noudp` is set. It tells the server the bound port in prop 15. The server adds the peer's IP as prop 16. The client keeps a peer list of players flagged with `50 = 1` that have both a UDP port and an address.

Datagrams have no length prefix and no compression:

| First byte | Body | Meaning |
|---|---|---|
| `c(0)` | the values of props 1–5 back to back, without prop ids (9 bytes) | position update; ignored if 8 bytes or fewer |
| `c(1)` | chat text, up to 200 bytes (longer is cut and given `...`) | chat line |

A receiver accepts a datagram only if its source address and port match a known player, and applies it to that player. The sender sends one copy to each peer: position only when props 1–5 changed since the last tick, and chat right after Enter. The chat also goes to the server as prop 13 in the next props diff.

## Admin commands

The server keeps these from the 2D GServer. Each needs a minimum admin level (0 none, 1 and 2 staff, 3 full). An admin can only act on accounts at or below their own level, unless they are level 3.

Account ids are a 28-bit number sent as 4 bytes, 7 bits each.

| Id in | Payload | Effect / reply |
|---|---|---|
| 51 | account id | Reply 54: account record. |
| 52 | account id, `str` name, `str` password, `str` props, `c` flags | Edit account. → 51 (changed) and 52 (renamed) to admins. |
| 53 | account record | Add account. → 50 to admins. |
| 54 | account id | Delete account. → 53 to admins. |
| 59 | `c(player id)` | Reply 57: that player's account. |
| 60 | `c(player id)` + account record | Edit an online player's account. |
| 61 | `c(player id)` | Kick: the player gets 5 "The server administrator has disconnected you." |
| 62 | `s2(count)` + `str` names | Reload these levels from disk. |
| 63 | text | Message to all players (8), signed with the sender's account. |
| 64 | `c(player id)` + text | Message to one player (8). |

Server → admin: 50 account added, 51 account changed, 52 account renamed, 53 account deleted, 54 account record, 55 player joined, 56 player left, 57 player's account, 58 player's account renamed, 59 player props (level, nickname). The 55/56 ids match the 2D add/remove-player ids. Names for the others are descriptive, not recovered.

Account flags byte (also in `accounts.txt`): bit 0 = a shared account (the session is not tied to the record, so props are not saved back), bits 1–3 = admin level, bit 4 = disabled. The meaning of bit 0 is inferred from where it is checked.
