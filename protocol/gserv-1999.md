# GSERV-token protocol, 1.21 to 1.32 (May 1999 to January 2000)

Date: 2026-10-21

This covers the clients from 1.21 to 1.32 and the GServer and RemoteControl builds shipped with 1.21, 1.28 beta 2 and 1.3 test.
It is the first central-server protocol: accounts, a login token, and zlib on every frame.
In the GServer-v2 numbering this is encryption generation 2, the same one 1.33 to 1.39 use with GNW tokens.
The notes come from static analysis of the shipped executables. No decompiler output is reproduced.

## Gen 1 to gen 2 in one table

| | Gen 1 (1st Graal to 1.1.9) | Gen 2 (1.21 on) |
|---|---|---|
| Server | Lobby/relay, no game logic | GServer: accounts, levels, NPCs, flags, weapons |
| Port | 14801 local default, 14802 Cyberjoueur | 14804 (`www.graalonline.com`) for 1.21 to 1.3 test, 14900 from 1.31 |
| Framing | Text lines | `u16` big-endian length, then a zlib stream |
| Message ids | One letter (`D` plus a type letter) | `chr(id+32)` as the first byte of each line |
| Identity | Server-given 8-character id, nickname sent as data | Account and password at login |
| Levels | HTTP from the level server | Sent by the GServer |

Nothing in gen 2 is encrypted. The DES code in these clients is only used for local files (see `formats/graalsav.md`).

## Framing

Sending: messages queue in one buffer as `chr(id+32) + data + "\n"`.
On flush the whole buffer is deflated with zlib 1.0.4 and written as:

```
[len_hi][len_lo][zlib stream of len bytes]
```

There is no size threshold. Every flush is compressed.

Receiving: frames are read the same way, inflated, and split on `\n`.
Server id 100 (`chr(132)`) puts the reader into a raw mode that takes a given byte count instead of a line, for file data.
`nodecompressionerror=` in `graalconfig.txt` (from 1.28 beta 2) hides the inflate error message.

## Login

The first message after `connect` is a normal id-0 line:

```
' '                    type: chr(0+32) = player. The GServer treats '!' (type 1) as RemoteControl
"GSERVnnn"             8 bytes
chr(len(account)+32) account
chr(len(password)+32) password
```

The connect dialog's defaults are `guest` / `guest`.
This is the same shape the later gen-3 login uses, minus the key byte and with GSERV instead of GNW.

| Client | Token |
|---|---|
| 1.21, RemoteControl 1.21 | `GSERV007` |
| RemoteControl 1.28, RemoteControl 1.3 | `GSERV011` |
| 1.28 beta 2 | `GSERV013` |
| 1.3 test | `GSERV014` |
| 1.31 | `GSERV016` |
| 1.32 | `GSERV018` |

The tokens are a protocol revision and not a date. GNW tokens, which are dates, start with 1.33.

### What the GServers accept

The server compares the token against a fixed list and stores the matching number (7 to 14) on the connection.
Then it checks the minimum for the connection type.

| GServer | Accepts | Player minimum and refusal text |
|---|---|---|
| 1.21 (May 1999) | `GSERV007` | "You need Graal version 1.2 rev1 to play on this server." |
| 1.28 (Nov 1999) | `GSERV007` to `GSERV013` | 13: "You need at least Graal version 1.28beta2 to play on this server." |
| 1.3 (Nov 1999) | `GSERV007` to `GSERV014` | 14: "You need at least Graal version 1.3 to play on this server." |

The older tokens stay on the list so that RemoteControl (GSERV011) can still log in.
Refusals and login errors ("The account has been disabled by an admin.", "The account is already in use.", "An account with the name and password you typed in doesn't exist.") go out as server id 16, which is DISCMESSAGE in the later numbering.
After a good player login the 1.3 server sends the player's props (9), flags (28), NPC weapons (33) and the other players' props (8), among others.

## Message ids

The server-to-client numbering used through 2.x is already in place in 1.21.
The 1.21 handlers line up with the later names: 1 links (`TEditorLink`), 2 baddy props (`TComputer`), 3 NPC props (`TEditorNPC`), 4 chest, 5 sign (`TAdventureSign`), 7 board modify, 8 other player props (`TOtherClient`), 21 throw carried (`TAdventureCarry`), 22 item add (`fullheart`, `sword`, `shield`), 23 item delete (`extra.wav`).

| Client | Server-to-client ids handled |
|---|---|
| 1.21 | 0 to 34 except 30, plus 100 |
| 1.28 beta 2 | 0 to 38, plus 100 |
| 1.3 test | 0 to 39, plus 100 |
| 1.31 | 0 to 40, plus 100 |
| 1.32 | 0 to 41, plus 100 |

The client-to-server ids visible as constants are 0 and 10 to 26 in 1.21, and 0 and 10 to 30 in 1.32. Other sends pass the id in a register, so these lists are not complete.

## UDP (1.28 beta 2 on)

The 1.28 beta 2 notes call this "direct data packages", and it is the first build that links `bind`, `sendto` and `recvfrom`.
The client binds a UDP socket and sends single, uncompressed, unframed messages (anything without a `\n`) straight to another player's address and port. The address and port are stored on the other player's record, so they most likely come from the server (*inferred*).
The main loop reads TCP and UDP separately ("tcp read", "udp read" in the 1.32 profiler labels).
1.31 adds `noudp=` and `fixedudpport=` to `graalconfig.txt` (the catalogue gives 14899 as the fixed-port default).
The UDP payload ids in this era have not been mapped yet. `protocol/udp-p2p.md` covers the 2.05 UDP ids and is the closest reference.

## Open questions

- The meanings of ids 35 to 41 and the full client-to-server list. A diff against the 1.39 Dhrake names would settle most of them.
- Whether RemoteControl uses the same framing. It probably does, since the server code path is shared, but it hasn't been checked.
