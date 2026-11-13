<!-- manual: kind=reference status=draft -->
# 9 Graal3D (2000)

Graal3D is a separate 3D side project from February 2000, with its own Delphi client (`Graal3D.exe`) and its own server (`GServer.exe`). It does not talk to the 2D GServer or the list server. The Torque-based 3D of the 4.x clients is a different program (→ §10).

> Status: draft.

## 9.0 What ships and how it relates to 2D Graal

Graal3D is a separate program from 2000 with its own server. The facts below say what the archive holds and where it sits among the 2D releases [file] (graal3d/README.md#what-ships).

| Fact | Source |
| --- | --- |
| The archive `graal3d.7z` holds the client, the server, `graal3dconfig.txt`, `serverconfig.txt`, two levels (`level1.x`, `startlevel.x`), eight player-model meshes and their BMP textures | [file] (graal3d/README.md#what-ships) |
| Both programs carry resource stamps from 2000-02-05, between 2D releases 1.32 (`GSERV018`) and 1.33 (the first `GNW` token) | [bin] (graal3d/README.md#graal3d-february-2000) |
| The client is Delphi with DelphiX `TDXDraw` in Direct3D retained mode (z-buffer, textures), a 50 ms `TDXTimer`, and zlib 1.1.2 linked | [bin] (graal3d/README.md#what-ships) |
| Neither program has `.graal`/`.nw` loaders, GANI, tiles or NPC scripting | [bin] (graal3d/README.md#what-ships) |
| The server's default TCP port is 14901, its levels live in `levels\`, and accounts in `accounts.txt` | [file] (graal3d/README.md#what-ships) |
| The server holds at most 200 players; a player id is the lowest free slot from 1 to 200 | [bin] (graal3d/README.md#server-windows) |
| Every Delphi class in the Graal3D server also exists in the 2D `GServer13.exe` of 1999-11-29; the 2D server has 23 more (NPC, baddy, chest, horse, level-link and board-modify classes, and their deltas) | [bin] (graal3d/README.md#how-it-relates-to-the-2d-graal-of-the-same-time) |
| The account record is 44 bytes in both servers; the level object shrinks from 8,244 bytes (a 64×64 board) to 24 bytes (name, file text, players in it, players already sent the file) | [bin] (graal3d/README.md#how-it-relates-to-the-2d-graal-of-the-same-time) |
| The per-observer "unsent props" tracker, the admin forms and the guild-tag check are carried over from the 2D server | [bin] (graal3d/README.md#how-it-relates-to-the-2d-graal-of-the-same-time) |
| The client keeps the 2D client's class names for the main form, the socket object, the connect window, the options window, the self-check and the DES helper; the level, NPC, weapon and script classes are gone | [bin] (graal3d/README.md#how-it-relates-to-the-2d-graal-of-the-same-time) |
| Each frame tick the client reads TCP, reads UDP, diffs its own player props and queues the changes, then flushes the TCP send buffer | [bin] (graal3d/README.md#client-windows) |
| The client windows are the main 3D view with a chat line, the connect window (nickname, host, port 14901, the built-in guest account), "Hardware options" (fixed UDP port, "Don't use UDP") and "Player look" | [bin] (graal3d/README.md#client-windows) |
| The server windows are a start dialog, the main window (player count, "Edit accounts", "Update levels", a tray menu), an account list and editor, an online player list, a message window and a level-reload window | [bin] (graal3d/README.md#server-windows) |

## 9.1 Protocol

### 9.1.1 Encoding and frames

Graal3D borrows the 2D codec. The rules below give its encodings and how a TCP frame is laid out [bin] (graal3d/protocol.md#encoding).

| Rule | Source |
| --- | --- |
| The text codec is the 2D one: `c` is one byte + 32, `sN` is an N-byte integer with 7 bits per byte, most significant first, each byte + 32, and `str` is `c(len)` then the bytes (→ §2.1) | [bin] (graal3d/protocol.md#encoding) |
| A TCP frame is a 2-byte big-endian length, then one zlib block holding one or more messages, each `c(id)` + payload + `\n` | [bin] (graal3d/protocol.md#tcp-frames) |
| Both sides compress when the queue passes 4096 bytes or on the frame-tick flush; the client sends in 256-byte slices and inflates into a buffer of up to 256,000 bytes | [bin] (graal3d/protocol.md#tcp-frames) |
| A client drops the link when more than 256 KiB of compressed output is pending | [bin] (graal3d/protocol.md#tcp-frames) |
| There is no key byte and no per-packet scramble | [bin][cap] (graal3d/protocol.md#tcp-frames) |
| Text with line breaks (level files, admin messages) writes each `\n` as `§` (0xA7) | [cap] (graal3d/protocol.md#tcp-frames) |
| The client sends its login line and its first props line in one frame; the server answers each event with its own frame, so a server may flush per event | [cap] (graal3d/protocol.md#tcp-frames) |
| Packet ids and the prop table are numbered from scratch, not shared with 2D; positions are 3D, the angle is one byte and colours are 24-bit | [bin] (graal3d/README.md#how-it-relates-to-the-2d-graal-of-the-same-time) |

### 9.1.2 Login

The rules below give the Graal3D login in order, from the server's first message to acceptance or refusal [cap] (graal3d/protocol.md#login).

| Rule | Source |
| --- | --- |
| On TCP accept, before login, the server sends id 6 with `c(0)` | [cap] (graal3d/protocol.md#login) |
| The client's first line is `c(0)`, the version `GR3DV002`, `str(account)`, `str(password)`; the server reads the version at bytes 2 to 9 | [bin][cap] (graal3d/protocol.md#login) |
| `GR3DV001` is recognised and rejected with id 5 and the text "You need at least Graal3D beta2 to play on this server." | [bin] (graal3d/protocol.md#login) |
| A missing, in-use or disabled account gets id 5 with the matching text, then the server closes | [cap] (graal3d/protocol.md#login) |
| The server still parses the rest of a rejected frame and applies the props line to a throwaway player; a server need not copy this | [cap] (graal3d/protocol.md#login) |
| Id 1 with the same layout is an admin login; it needs admin level 1 or more and gets the account list (50) and the player list (55) | [bin][cap] (graal3d/protocol.md#login) |
| A normal account already in use is rejected; a load-only account may log in many times at once | [cap] (graal3d/protocol.md#login) |

Login order on the server [cap] (graal3d/protocol.md#login):

| Step | Server action | Source |
| ---: | --- | --- |
| 1 | Gives the lowest free id, links the account and applies its saved props; a non-empty saved nickname is relayed at once to the others as `2` + prop 12 | [cap] (graal3d/protocol.md#login) |
| 2 | Sends `3` with props 0–5 | [cap] (graal3d/protocol.md#login) |
| 3 | Exchanges `2` with all of props 0–17 between the new player and every other player | [cap] (graal3d/protocol.md#login) |
| 4 | Sends the player to their level (→ §9.3.2) | [cap] (graal3d/protocol.md#login) |
| 5 | Tells admin sessions with 55 | [cap] (graal3d/protocol.md#login) |
| 6 | Handles the client's first props line like any other, so the others see props 12 and 15 again | [cap] (graal3d/protocol.md#login) |

### 9.1.3 Server → client ids

These are the messages the Graal3D server sends. Each row gives the id, its name in the notes, the payload and what the client does [bin][cap] (graal3d/protocol.md#server--client).

| Id | Name in the notes | Payload | Client action | Source |
| ---: | --- | --- | --- | --- |
| 0 | LEVEL | level text with `§` for `\n`, or empty | saves and loads it as a `.x` mesh; empty means "you already have it" (→ §9.3) | [bin][cap] (graal3d/protocol.md#server--client) |
| 1 | LEVELNAME | rest = file name | stored as the current level name | [bin][cap] (graal3d/protocol.md#server--client) |
| 2 | OTHERPLPROPS | `c(player id)` + props | creates the player on first sight, then applies the props | [bin][cap] (graal3d/protocol.md#server--client) |
| 3 | PLAYERPROPS | props | applies to the local player | [bin][cap] (graal3d/protocol.md#server--client) |
| 4 | leader | empty | sent to the first player in a level and to the next when the first leaves; sets a flag nothing reads | [bin][cap] (graal3d/protocol.md#server--client) |
| 5 | DISCMESSAGE | rest = text | shown when the socket closes; empty gives "You have been disconnected from the server." | [bin][cap] (graal3d/protocol.md#server--client) |
| 6 | session | `c(v)` | stores a value nothing reads; the server sends 0 on accept | [bin][cap] (graal3d/protocol.md#server--client) |
| 7 | FILESENDFAILED | rest = file name | not handled | [bin] (graal3d/protocol.md#server--client) |
| 8 | ADMINMESSAGE | rest, `§` = line break | shown in an "Administrator message" box | [bin][cap] (graal3d/protocol.md#server--client) |
| 16 | 2D disconnect message | text | not handled; sent only by the server's player-list kick button, so that kick arrives silently | [bin] (graal3d/README.md#how-it-relates-to-the-2d-graal-of-the-same-time) |
| 50–59 | admin replies | → §9.2.3 | admin sessions only | [bin][cap] (graal3d/protocol.md#admin-commands) |
| 100 | RAWDATA | `s3(len)` | flags the next line as raw, then discards it | [bin] (graal3d/protocol.md#server--client) |
| 101 | FILE | `str(name)` + bytes | the server's answer to request 2; unused by this client | [bin] (graal3d/protocol.md#server--client) |

### 9.1.4 Client → server ids

These are the messages a Graal3D client sends. Each row gives the id, the payload and the server's action [bin][cap] (graal3d/protocol.md#client--server).

| Id | Payload | Server action | Source |
| ---: | --- | --- | --- |
| 0 | login (→ §9.1.2) | | [bin][cap] (graal3d/protocol.md#client--server) |
| 1 | props | applies, then relays (→ §9.2.1) | [bin][cap] (graal3d/protocol.md#client--server) |
| 2 | file name | looks in `levels\`; sends 100 + 101 if the file is under 64,500 bytes, else 7; the shipped client never sends it | [bin] (graal3d/protocol.md#client--server) |
| 51–64 | admin commands | → §9.2.3 | [bin][cap] (graal3d/protocol.md#admin-commands) |

### 9.1.5 UDP between clients

Like 2D Graal, Graal3D sends some traffic between clients over UDP. The rules below give how peers find each other and what goes over the channel [bin] (graal3d/protocol.md#udp-client-to-client).

| Rule | Source |
| --- | --- |
| Unless `noudp` is set, the client binds one UDP socket on port 0 or on the fixed port from its config, and announces the bound port in prop 15 | [bin] (graal3d/protocol.md#udp-client-to-client) |
| The server adds the peer's address as prop 16; a client keeps as peers the players flagged `50 = 1` that have both a port and an address | [bin] (graal3d/protocol.md#udp-client-to-client) |
| Datagrams have no length prefix and no compression | [bin] (graal3d/protocol.md#udp-client-to-client) |
| First byte `c(0)`: the values of props 1–5 back to back without prop ids (9 bytes), a position update; 8 bytes or fewer is ignored | [bin] (graal3d/protocol.md#udp-client-to-client) |
| First byte `c(1)`: chat text, at most 200 bytes; longer text is cut and ends in `...` | [bin] (graal3d/protocol.md#udp-client-to-client) |
| A datagram is accepted only from the address and port of a known player | [bin] (graal3d/protocol.md#udp-client-to-client) |
| Position goes to each peer only when props 1–5 changed since the last tick; chat goes right after Enter, and also to the server as prop 13 in the next props diff | [bin] (graal3d/protocol.md#udp-client-to-client) |
| In 2D clients of the same time UDP went to the server; in Graal3D it goes peer to peer (the 2D peer channel is → §2.9) | [bin] (graal3d/README.md#how-it-relates-to-the-2d-graal-of-the-same-time) |
| UDP between two real clients was not seen in the lab, because Wine has no retained-mode `d3drm.dll` | [lab] (graal3d/lab-2026-10-30.md#not-confirmed) |

## 9.2 Props and accounts

### 9.2.1 Player props

The same ids are used in both directions and inside UDP; a props payload is a run of `c(prop id)` + value with no separators [bin] (graal3d/protocol.md#player-properties).

| Id | Value | Field | Default | Client sends | Source |
| ---: | --- | --- | --- | --- | --- |
| 0 | `c` | player id (1–200) | — | no | [bin] (graal3d/protocol.md#player-properties) |
| 1 | `s2` | x, `(v − 8000) / 2` | 0 | yes | [bin] (graal3d/protocol.md#player-properties) |
| 2 | `s2` | y, same scale | 0 | yes | [bin] (graal3d/protocol.md#player-properties) |
| 3 | `s2` | z, same scale | 0 | yes | [bin] (graal3d/protocol.md#player-properties) |
| 4 | `c` | angle, `v × 2` degrees | 0 | yes | [bin] (graal3d/protocol.md#player-properties) |
| 5 | `s2` | animation tick counter (→ §9.6.3) | 0 | yes | [bin] (graal3d/client-behaviour.md#animation-counter-prop-5) |
| 6 | `str` | body model | `body.x` | yes | [bin] (graal3d/protocol.md#player-properties) |
| 7 | `str` | head model | `head.x` | yes | [bin] (graal3d/protocol.md#player-properties) |
| 8 | `str` | body texture, reloaded on change | `body.bmp` | yes | [bin] (graal3d/protocol.md#player-properties) |
| 9 | `str` | head texture | `man.bmp` | yes | [bin] (graal3d/protocol.md#player-properties) |
| 10 | 4 × 6 bits | arm colour, 24-bit RGB | `FF0000` | yes | [bin] (graal3d/protocol.md#player-properties) |
| 11 | 4 × 6 bits | shoe colour | `800000` | yes | [bin] (graal3d/protocol.md#player-properties) |
| 12 | `str`, at most 200 | nickname, optional ` (guild)` | — | yes | [bin] (graal3d/protocol.md#player-properties) |
| 13 | `str`, at most 200 | chat text | — | yes | [bin] (graal3d/protocol.md#player-properties) |
| 14 | `str` | level file | `level1.x` in the client, `startlevel.x` in the server | no | [bin][cap] (graal3d/protocol.md#player-properties) |
| 15 | `s3` | UDP port, 0 = none | 0 | yes, its bound port | [bin][cap] (graal3d/protocol.md#player-properties) |
| 16 | 5 bytes: 4 bits, then 4 × 7 bits | IPv4 address: the in-memory address word read as a little-endian integer | — | no; the server fills in the TCP peer address | [bin][cap] (graal3d/protocol.md#player-properties) |
| 17 | 4 × 6 bits | hand colour | `FDCC47` | yes | [bin] (graal3d/protocol.md#player-properties) |
| 50 | `c` | 1 = this player is in your level (add as UDP peer), 0 = not | — | server only | [bin][cap] (graal3d/protocol.md#player-properties) |
| 51 | none | player left: remove | — | server only | [bin][cap] (graal3d/protocol.md#player-properties) |

Players are described by props, as in 2D. The rules below give what some props mean and how they are sent each tick [bin] (graal3d/protocol.md#player-properties).

| Rule | Source |
| --- | --- |
| Prop 10 colours the two arms, 17 the two hands and 11 the two feet | [bin] (graal3d/protocol.md#player-properties) |
| Each tick the client re-encodes every prop it sends, compares with the last tick and sends the changed ones as one id-1 message; the first send carries the full look (6–12 and 15) | [bin] (graal3d/protocol.md#player-properties) |
| The wire range of props 1–3 is −4000 to 4095.5 in half-unit steps, which covers the ±4000 world clamp (→ §9.5) | [bin] (graal3d/client-behaviour.md#walking-and-running) |

### 9.2.2 Server relay rules

The server checks and relays props. The rules below give how it treats nicknames and guild tags and who it relays to [cap] (graal3d/protocol.md#server-relay-rules).

| Rule | Source |
| --- | --- |
| On prop 12 the server splits `nick (guild)` and keeps the tag only if `guilds\guild<guild>.txt` lists the account; if the text had a tag, the result is echoed back with `3`; a plain nickname gets no echo | [cap] (graal3d/protocol.md#server-relay-rules) |
| The nickname then goes to every player (2) and every admin session (59) | [cap] (graal3d/protocol.md#server-relay-rules) |
| Prop 15 goes to every player as `2` + prop 15 | [cap] (graal3d/protocol.md#server-relay-rules) |
| Prop 14 from a client is stored and relayed to the level, but does not move the player; only the server moves players, at login and when an admin edits an online player (60) | [cap][bin] (graal3d/protocol.md#server-relay-rules) |
| Prop 16 from a client is ignored while the player has a live socket | [bin] (graal3d/protocol.md#server-relay-rules) |
| All changed props in the line go as one `2` line to the players in the same level, leaving out props 1–5 and 13 when both players have a UDP port; when nothing is left, nothing is sent | [cap] (graal3d/protocol.md#server-relay-rules) |
| Each observer has its own dirty set, so a player who was skipped gets the missing props later | [bin] (graal3d/protocol.md#server-relay-rules) |
| On disconnect every player gets `c(id)` + prop 51 and admin sessions get 56 + `c(id)` | [cap] (graal3d/protocol.md#level-change) |

### 9.2.3 Admin protocol

The admin protocol is read from the server alone; no Graal3D admin client is in the archives [bin] (graal3d/README.md#open-points). Each command needs a minimum admin level (0 none, 1 and 2 staff, 3 full), and an admin can act only on accounts at or below their own level unless they are level 3 [bin] (graal3d/protocol.md#admin-commands). An account id is a 28-bit number sent as 4 bytes of 7 bits [bin] (graal3d/protocol.md#admin-commands).

| Id in | Payload | Effect or reply | Source |
| ---: | --- | --- | --- |
| 51 | account id | reply 54, the account record | [bin] (graal3d/protocol.md#admin-commands) |
| 52 | account id, `str` name, `str` password, `str` props, `c` flags | edit account; 51 (changed) and 52 (renamed) to admins | [bin] (graal3d/protocol.md#admin-commands) |
| 53 | account record | add account; 50 to admins | [bin] (graal3d/protocol.md#admin-commands) |
| 54 | account id | delete account; 53 to admins | [bin] (graal3d/protocol.md#admin-commands) |
| 59 | `c(player id)` | reply 57, that player's account | [bin] (graal3d/protocol.md#admin-commands) |
| 60 | `c(player id)` + account record | edit an online player's account | [bin] (graal3d/protocol.md#admin-commands) |
| 61 | `c(player id)` | kick: the player gets 5 "The server administrator has disconnected you." and the others get prop 51 | [cap] (graal3d/protocol.md#admin-commands) |
| 62 | `s2(count)` + `str` names | reload these levels from disk | [bin] (graal3d/protocol.md#admin-commands) |
| 63 | text | message to all players (8) as `Administrator <account>:§<text>` | [cap] (graal3d/protocol.md#admin-commands) |
| 64 | `c(player id)` + text | message to one player (8) | [bin] (graal3d/protocol.md#admin-commands) |

Admin sessions get their own messages. Each row gives an id the server sends out, its meaning and its layout [cap] (graal3d/protocol.md#admin-commands).

| Id out | Meaning | Layout | Source |
| ---: | --- | --- | --- |
| 50 | account added | account id, `c(folder)`, name to end of line; one per account after an admin login | [cap] (graal3d/protocol.md#admin-commands) |
| 51 | account changed | account id, `c(flags)`; sent when a bound player leaves and the record is saved | [cap] (graal3d/protocol.md#admin-commands) |
| 52 | account renamed | unmeasured | [bin] (graal3d/protocol.md#admin-commands) |
| 53 | account deleted | unmeasured | [bin] (graal3d/protocol.md#admin-commands) |
| 54 | account record | account id, `str(password field)` (came back empty), `str(props)`, `c(flags)` | [cap] (graal3d/protocol.md#admin-commands) |
| 55 | player joined | `c(player id)`, `str(account)`, prop 14 | [cap] (graal3d/protocol.md#admin-commands) |
| 56 | player left | `c(player id)` | [cap] (graal3d/protocol.md#admin-commands) |
| 57 | player's account | unmeasured | [bin] (graal3d/protocol.md#admin-commands) |
| 58 | player's account renamed | unmeasured | [bin] (graal3d/protocol.md#admin-commands) |
| 59 | player props | `c(player id)` + props: the nickname, the full props on login, prop 14 on level entry | [cap] (graal3d/protocol.md#admin-commands) |

The rules below explain the folder byte and how the admin ids line up with the 2D ones [cap][inf] (graal3d/protocol.md#admin-commands).

| Rule | Source |
| --- | --- |
| The folder byte in 50 fits 1 for a normal account plus 4 × the admin level, and 0 for a load-only account; the formula is fitted to three accounts | [cap][inf] (graal3d/protocol.md#admin-commands) |
| 55 and 56 match the 2D add- and remove-player ids; the names of the other admin ids are descriptive, not recovered | [bin] (graal3d/protocol.md#admin-commands) |
| The admin kick path (61) sends 5, which the client shows; the player-list kick button sends the 2D id 16, which it ignores | [bin] (graal3d/README.md#how-it-relates-to-the-2d-graal-of-the-same-time) |
| Commands 51–54, 59, 60 and 62 were not exercised live | [lab] (graal3d/lab-2026-10-30.md#not-confirmed) |

### 9.2.4 Account and config files

The server keeps accounts and settings in text files. The rules below give their layout [cap] (graal3d/formats.md#accountstxt-server).

| Rule | Source |
| --- | --- |
| `accounts.txt` holds one account per `\n`-terminated line in the `+32` codec: `str(name) str(password) str(saved props) c(flags)` and seven `c(0)` bytes; a hand-written file is accepted | [cap] (graal3d/formats.md#accountstxt-server) |
| The saved props are the player's prop run, props 1–14, 16 and 17 (no 0 or 15); empty until the player first leaves, written back when a bound player leaves or is edited, and applied at the next login, nickname and chat text included | [cap] (graal3d/formats.md#accountstxt-server) |
| Flags: bit 0 = load only (the session is not tied to the record, props are not saved back, many logins may share it), bits 1–3 = admin level, bit 4 = blocked | [cap] (graal3d/protocol.md#admin-commands) |
| The server UI names the levels No rights (0), Graalian Police (1), Trusted Admin (2) and Administrator (3) | [bin] (graal3d/formats.md#accountstxt-server) |
| The seven trailing bytes are the empty count-prefixed lists of the 2D account record; nothing in Graal3D fills them | [bin] (graal3d/formats.md#accountstxt-server) |
| The server rewrites `accounts.txt` whenever an account changes | [bin] (graal3d/formats.md#accountstxt-server) |
| `guilds\guild<name>.txt` lists one account per line; a nickname keeps its `(name)` tag only if the file exists and lists the account, as in the 2D server | [bin] (graal3d/formats.md#guildsguildnametxt-server) |
| `serverconfig.txt` holds `serverport=14901` | [file] (graal3d/formats.md#serverconfigtxt-server) |
| The client stores nickname, account and password in the registry under `HKCU\Software\Graal3D`, section `Client`; the password is three DES blocks under a key built into the exe, written as 48 printable characters (obfuscation, not protection; the key is not given here) | [bin] (graal3d/formats.md#registry-client) |

Client config `graal3dconfig.txt`, `key=value` lines read at start and written back on change [file] (graal3d/formats.md#graal3dconfigtxt-client):

| Key | Shipped value | Meaning | Source |
| --- | --- | --- | --- |
| `serveraddr` | `<public-host>` | server host or address; the connect window defaults to the loopback address | [file] (graal3d/formats.md#graal3dconfigtxt-client) |
| `serverport` | 14901 | TCP port | [file] (graal3d/formats.md#graal3dconfigtxt-client) |
| `fixedport` | `false` | bind UDP to `fixedudpport` instead of a random port | [file] (graal3d/formats.md#graal3dconfigtxt-client) |
| `fixedudpport` | 14898 | fixed UDP port | [file] (graal3d/formats.md#graal3dconfigtxt-client) |
| `noudp` | `false` | no UDP socket; position and chat go only through the server | [file] (graal3d/formats.md#graal3dconfigtxt-client) |
| `bodyx`, `headx`, `bodytex` | `body.x`, `head.x`, `body.bmp` | props 6, 7 and 8 | [file] (graal3d/formats.md#graal3dconfigtxt-client) |
| `armcolor`, `shoecolor`, `handcolor` | `FF0000`, `800000`, `FDCC47` | props 10, 11 and 17 | [file] (graal3d/formats.md#graal3dconfigtxt-client) |
| `accountname`, `password` | — | also accepted by the reader | [bin] (graal3d/formats.md#graal3dconfigtxt-client) |

## 9.3 Levels (.x)

### 9.3.1 Level files

A Graal3D level is a DirectX mesh file. The rules below say what it holds and how the two shipped levels differ [file] (graal3d/formats.md#levels-levelsx-on-the-server).

| Rule | Source |
| --- | --- |
| A level is a DirectX retained-mode `.x` text file (`xof 0302txt 0064`); there is no tile layer, NPC or link data | [file] (graal3d/formats.md#levels-levelsx-on-the-server) |
| `startlevel.x` is the server's start level and `level1.x` the client's default; the two hold the same scene and differ only in line ends and trailing spaces | [file] (graal3d/formats.md#levels-levelsx-on-the-server) |
| The shipped scene is one 139-vertex mesh `obj` with nine materials and seven textures (`grass`, `way`, `stones`, `wall`, `tower`, `platform`, `clouds`) | [file] (graal3d/formats.md#levels-levelsx-on-the-server) |
| The server caches each level's text and sends it inline in id 0; the client saves it under the level name in its own folder and loads it with Direct3D RM | [bin][cap] (graal3d/formats.md#levels-levelsx-on-the-server) |
| Textures are not transferred: the BMPs a level names must already be in the client folder | [bin] (graal3d/formats.md#levels-levelsx-on-the-server) |
| The client's saved copy was byte-identical to the server's file in the lab | [cap] (graal3d/protocol.md#level-change) |

### 9.3.2 Level change

Changing level takes a few server steps. The steps below are in order [bin] (graal3d/protocol.md#level-change).

| Step | Server action | Source |
| ---: | --- | --- |
| 1 | Finds the level in its cache or loads `levels\<name>` | [bin] (graal3d/protocol.md#level-change) |
| 2 | Sends 1 (name), then 0 with the text, or 0 empty if this player was already sent that level; the "already sent" list is per player, so a second login gets the full text again | [cap] (graal3d/protocol.md#level-change) |
| 3 | For each player already in the level, sends both sides `2` with `50 = 1` and the props not yet seen | [cap] (graal3d/protocol.md#level-change) |
| 4 | Sends 4 if the player is alone in the level | [cap] (graal3d/protocol.md#level-change) |
| 5 | Tells admin sessions with 59 | [cap] (graal3d/protocol.md#level-change) |
| — | On leaving a level the others get `50 = 0` | [cap] (graal3d/protocol.md#level-change) |

### 9.3.3 Player model and textures

The player is built from eight meshes. The rules below give the meshes and their textures [file] (graal3d/formats.md#player-model-client).

| Rule | Source |
| --- | --- |
| The player is eight `.x` meshes (`xof 0303txt 0032`): body, head, two arms, two hands, two feet, each with normals, texture coordinates and a material | [file] (graal3d/formats.md#player-model-client) |
| `body.x` is textured with `body.bmp` (128×128, 24-bit; `body1.bmp` is an alternative) and `head.x` with `man.bmp` (64×64) | [file] (graal3d/formats.md#player-model-client) |
| Mesh and texture names travel as props 6–9, so they may point at any file present on every client; colours are set as material colours at run time | [bin] (graal3d/formats.md#player-model-client) |
| Textures are plain Windows BMPs, 24-bit or 8-bit RLE, mostly 128×128 (`clouds.bmp` is 256×256) | [file] (graal3d/formats.md#textures) |

## 9.4 Camera

The camera follows the player at fixed offsets. Each row gives one quantity or rule with its value [bin] (graal3d/camera.md#status-for-g3d-2).

| Quantity or rule | Value | Source |
| --- | --- | --- |
| Follow distance | 220 behind the player | [bin] (graal3d/camera.md#status-for-g3d-2) |
| Look height | 80 above the player on Y | [bin] (graal3d/camera.md#status-for-g3d-2) |
| Gap closing per tick | factor `((d − 220) / 220)² / 10` with the sign of `d − 220`, `d` the horizontal distance; skipped if the factor is 0 or 100 or more | [bin] (graal3d/camera.md#follow-rule-numpad-0-toggles-follow-onoff) |
| Y follow per tick | `(player_y + 80 − camera_y) / 10` | [bin] (graal3d/camera.md#follow-rule-numpad-0-toggles-follow-onoff) |
| Turn | up to ±5° per tick toward the player, more when the player is behind the camera | [bin] (graal3d/camera.md#follow-rule-numpad-0-toggles-follow-onoff) |
| Aim | `LookAt` the player, then pitch −0.15 rad about the camera's local X axis | [bin] (graal3d/camera.md#follow-rule-numpad-0-toggles-follow-onoff) |
| Follow toggle | Numpad 0; with follow off the camera stays where it is | [bin] (graal3d/camera.md#follow-rule-numpad-0-toggles-follow-onoff) |
| Facing sent | prop 4 is the angle of the camera-to-player direction, sent as degrees / 2 | [bin] (graal3d/camera.md#follow-rule-numpad-0-toggles-follow-onoff) |
| Surface | 640×456 pixels | [bin] (graal3d/camera.md#display-size-aspect-context-only) |
| Field | the Direct3D RM initial field 0.5, a square window; the exe sets no field | [doc][bin] (graal3d/camera.md#field-of-view) |
| Opening | `2 × atan(0.5)` ≈ 53.13° on either axis of that window | [inf] (graal3d/camera.md#field-of-view) |
| Front plane | 1 (library initial value) | [doc] (graal3d/camera.md#field-of-view) |
| Back plane | 5000, set right after the viewport is created; the front plane stays at the library's 1 (settled → App. E#500) | [bin] (graal3d/camera.md#back-clipping-plane-re-read-2026-11-13) |
| Lab | none of these figures is lab-confirmed; Wine's retained-mode stubs break camera frames | [lab] (graal3d/camera.md#still-needed) |

## 9.5 Collision

Collision uses a small set of numbers. Each row gives one quantity and its value [bin] (graal3d/collision.md#what-the-collider-needs).

| Quantity | Value | Source |
| --- | --- | --- |
| Body radius (horizontal half-extent) | 5 | [bin] (graal3d/collision.md#what-the-collider-needs) |
| Upper probe height | +35 above the feet | [bin] (graal3d/collision.md#what-the-collider-needs) |
| Upper probe lateral offsets | 0, +10 and −10 on the strafe axis only | [bin] (graal3d/collision.md#what-the-collider-needs) |
| Max step height | 30 | [bin] (graal3d/collision.md#what-the-collider-needs) |
| Walkable face | normal Y > 0 | [bin] (graal3d/collision.md#what-the-collider-needs) |
| Feet-mesh attach | normal Y > 0.2; steeper walkable faces snap the point but skip the attach | [bin] (graal3d/collision.md#what-the-collider-needs) |
| Wall already clear | new signed distance ≥ 3 | [bin] (graal3d/collision.md#what-the-collider-needs) |
| Wall started inside | previous signed distance < −5 | [bin] (graal3d/collision.md#what-the-collider-needs) |
| World clamp, x and z | ±4000; a step that would leave is dropped | [bin] (graal3d/collision.md#what-the-collider-needs) |
| Sliding | subtract `distance × normal` from the test point | [bin] (graal3d/collision.md#what-the-collider-needs) |

Order of tests for one attempted step:

| Step | Action | Source |
| ---: | --- | --- |
| 1 | Build the candidate position from the walk, run or jump delta (→ §9.6) | [bin] (graal3d/collision.md#order-of-tests-one-attempted-step) |
| 2 | Load every face of the level mesh, filled at level load, and transform its vertices to world space | [bin] (graal3d/collision.md#order-of-tests-one-attempted-step) |
| 3 | Run the body probes against every face; a blocked probe stops the rest | [bin] (graal3d/collision.md#body-probes) |
| 4 | Reject the step if a probe is blocked, otherwise keep the (possibly slid) position | [bin] (graal3d/collision.md#order-of-tests-one-attempted-step) |
| 5 | Drop the step if x or z leaves ±4000 | [bin] (graal3d/collision.md#order-of-tests-one-attempted-step) |

The rules below give where the collision probes lie and how each set is used [bin] (graal3d/collision.md#body-probes).

| Rule | Source |
| --- | --- |
| Ground probes: four points in the feet plane at ±5 on the facing axis and ±5 on the strafe axis, a plus shape, not a filled disc | [bin] (graal3d/collision.md#body-probes) |
| Upper probes: Y + 35 at lateral 0, +10, −10; they use only the wall and ceiling path | [bin] (graal3d/collision.md#body-probes) |
| A face is used only if the probe's (x, z) lies inside its horizontal projection, by a winding test that tries both edge orders | [bin] (graal3d/collision.md#over-face-test) |
| Walkable face, ground probes only: signed distance > 30 lands on the face; < −30 fails (step too high); otherwise the probe slides onto the plane, with the mesh attach when normal Y > 0.2 | [bin] (graal3d/collision.md#walkable-faces-normal-y--0) |
| Wall or ceiling (normal Y ≤ 0): the face is dropped if the new distance is ≥ 3, the previous distance < −5, or the move has zero length; otherwise the new point slides onto the plane | [bin] (graal3d/collision.md#walls-and-ceilings-normal-y--0) |
| No floor friction, extra ground stickiness or ceiling thickness shows in the routine's constants | [bin] (graal3d/collision.md#what-this-does-not-settle) |
| A disc of radius 5 is an approximation of the plus-shaped probe set, not what the binary runs | [inf] (graal3d/collision.md#what-this-does-not-settle) |
| Collision is not lab-confirmed; Wine's face query is a stub | [lab] (graal3d/collision.md#what-this-does-not-settle) |

## 9.6 Client behaviour

### 9.6.1 Controls

Graal3D is played on the number pad. Each row gives a key and its action [bin] (graal3d/client-behaviour.md#controls).

| Key | Action | Source |
| --- | --- | --- |
| Numpad 8 / 2 | forward / back, relative to the camera's view direction | [bin] (graal3d/client-behaviour.md#controls) |
| Numpad 4 / 6 | strafe left / right | [bin] (graal3d/client-behaviour.md#controls) |
| Numpad 5 | jump | [bin] (graal3d/client-behaviour.md#controls) |
| Numpad 0 | camera follow on or off | [bin] (graal3d/client-behaviour.md#controls) |
| Enter | send the chat line | [bin] (graal3d/client-behaviour.md#controls) |
| Ctrl+Enter | fullscreen on or off | [bin] (graal3d/client-behaviour.md#controls) |
| F1 / F2 | Hardware options / Player look | [bin] (graal3d/client-behaviour.md#controls) |
| Esc | quit | [bin] (graal3d/client-behaviour.md#controls) |
| — | movement keys are polled only while the chat line lacks focus and the window is active | [bin] (graal3d/client-behaviour.md#controls) |

### 9.6.2 Walking, running and jumping

The rules below give walking speed, running and the jump [bin] (graal3d/client-behaviour.md#walking-and-running).

| Rule | Source |
| --- | --- |
| Walking speed is 8 units per 50 ms tick (160 per second) | [bin] (graal3d/client-behaviour.md#walking-and-running) |
| After 25 ticks of walking without stopping the speed becomes ×1.5 (12 per tick); stopping resets the count | [bin] (graal3d/client-behaviour.md#walking-and-running) |
| Holding only "back" walks backwards along the facing at key-down, not following the camera | [bin] (graal3d/client-behaviour.md#walking-and-running) |
| While walking, y gets `abs(sin(3.14 × 2 × (anim − 1) / 40)) × 3` added (the program uses 3.14, not π) | [bin] (graal3d/client-behaviour.md#walking-and-running) |
| The jump climbs by a fixed table of 10, 10, 9, 8, 6, 3, 1 units per tick (47 in 7 ticks), walks the table back down with negative speeds, then falls at −10 per tick until it lands | [bin] (graal3d/client-behaviour.md#jumping) |
| Releasing the key early starts the fall at once from the top of the table, so a tap gives a short hop; a new jump needs the key released and pressed again | [bin] (graal3d/client-behaviour.md#jumping) |

### 9.6.3 Animation counter

Prop 5 drives the walk and jump poses. The rules below say how it counts [bin] (graal3d/client-behaviour.md#animation-counter-prop-5).

| Rule | Source |
| --- | --- |
| Prop 5 is a tick counter for the walk and jump poses, not a pose id | [bin] (graal3d/client-behaviour.md#animation-counter-prop-5) |
| Starting to walk sets it to 0 or 20 at random, so players do not step in time; a jump sets it to 40 | [bin] (graal3d/client-behaviour.md#animation-counter-prop-5) |
| Where it advances each tick was not traced; that standing still freezes it is an inference | [inf] (graal3d/client-behaviour.md#animation-counter-prop-5) |

### 9.6.4 Chat

Chat in Graal3D is a log, not bubbles. The rules below give how lines are added and drawn [bin] (graal3d/client-behaviour.md#chat).

| Rule | Source |
| --- | --- |
| There are no chat bubbles; a chat line (prop 13 or a UDP chat datagram) is added to a chat log as `nickname: text` | [bin] (graal3d/client-behaviour.md#chat) |
| The log is drawn at the bottom left of the view, x = 5, newest line at y ≈ 451, older lines above, in white 14 px "Dialog" | [bin] (graal3d/client-behaviour.md#chat) |
| Each line stays 10 seconds (200 ticks) | [bin] (graal3d/client-behaviour.md#chat) |
| A line over 200 characters is cut and ends in `...` | [bin] (graal3d/client-behaviour.md#chat) |
| The "Player look" window edits props 6–11 and 17 and saves them in `graal3dconfig.txt` | [bin] (graal3d/client-behaviour.md#look) |

### 9.6.5 Lab coverage

Not every part of Graal3D was confirmed in the lab. The facts below say what was and what was not [lab] (graal3d/lab-2026-10-30.md#what-was-confirmed).

| Fact | Source |
| --- | --- |
| Lab-confirmed on 2026-10-30: the accept and reject flow, the login order, the full props exchange, level name, text and leader, prop 50, the UDP relay rule, the guild-tag echo, prop 14 not moving the player, saved props, load-only logins, the disconnect messages, the admin login replies and `accounts.txt` | [lab] (graal3d/lab-2026-10-30.md#what-was-confirmed) |
| Not confirmed: UDP between two real clients, admin commands 51–54, 59, 60 and 62, and the two kick buttons | [lab] (graal3d/lab-2026-10-30.md#not-confirmed) |
| Ids 4 and 6 set client values that nothing reads | [bin][cap] (graal3d/README.md#open-points) |
