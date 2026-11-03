<!-- manual: kind=reference status=draft -->
# 2.3 Login and handshake by generation

Tokens are listed in → §1.2.2, frames in → §2.1.4 and ciphers in → §2.2. The listserver exchange that comes before a game login is in → §6; RC and NC logins are in → §7.

## 2.3.1 1998 relay (generation 1)

### 2.3.1.1 Connections

| Rule | Builds | Source |
| --- | --- | --- |
| The client connects over TCP to a lobby and relay server that knows nothing about the game; it groups connections into named games, gives each an 8-character id, and forwards `D` lines between partners | 1st Graal to 1.1.9 | [bin] (protocol/relay-1998.md#summary) |
| A client opens two connections to the same port: one in the fixed game name and one in a room named after the current level; both pair with the other player | 1.1.9 (captured); 1st, 3rd, 4th alpha, 5th Graal (live) | [cap][live] (protocol/relay-1998.md#game-names) |
| Every message is a text line ending in `\n`; the first character is the command | 1st Graal to 1.1.9 | [bin] (protocol/relay-1998.md#summary) |
| There is no login token and no peer-to-peer mode | 1st Graal to 1.1.9 | [bin] (protocol/relay-1998.md#summary) |
| Levels are not sent over the relay; web levels are fetched over plain HTTP/1.0 by a separate small client | 1st Graal to 1.1.9 | [bin] (protocol/relay-1998.md#transport-by-build) |
| Default server: the loopback address on 14801; from 3rd Graal the connect dialog is pre-filled with a relay on 14802; 4th and 5th alpha have no pre-filled relay host | 1st Graal to 1.1.9 | [bin] (protocol/relay-1998.md#summary) |

| Builds | Socket layer | Source |
| --- | --- | --- |
| 1st, 2nd Graal | ICS `TWSocket`, event driven | [bin] (protocol/relay-1998.md#transport-by-build) |
| 3rd Graal to 1.1.9 | plain WinSock 1.1: blocking `connect`, then `FIONBIO`, then polled `recv`; host tried with `inet_addr`, then `gethostbyname` | [bin] (protocol/relay-1998.md#transport-by-build) |
| 15th Graal on | as above, plus a hostname-to-address cache in front of the resolver | [bin] (protocol/relay-1998.md#transport-by-build) |

### 2.3.1.2 Lobby lines

| Direction | Line | Meaning | Source |
| --- | --- | --- | --- |
| C→S | `N<game>#<name>` | join `<game>` as a player; the clients always send the name `def` and send the nickname later inside `D` | [bin] (protocol/relay-1998.md#lobby-lines) |
| C→S | `P<id>` | ask to play with player `<id>`, or accept a request | [bin] (protocol/relay-1998.md#lobby-lines) |
| C→S | `C` | leave the current party | [bin] (protocol/relay-1998.md#lobby-lines) |
| C→S | `-` | leave the available list; sent on a deliberate disconnect | [bin] (protocol/relay-1998.md#lobby-lines) |
| C→S | `D<data>` | relay `<data>` to the party (→ §2.3.1.4) | [bin] (protocol/relay-1998.md#lobby-lines) |
| S→C | `I<id8>` | your id: `0000` plus a 4-digit counter | [bin] (protocol/relay-1998.md#lobby-lines) |
| S→C | `+<id8>` | player in the same game; if it is the only known peer the client answers `P<id8>` at once | [bin] (protocol/relay-1998.md#lobby-lines) |
| S→C | `-<id8>` | player left | [bin] (protocol/relay-1998.md#lobby-lines) |
| S→C | `P<id8>` | partnership confirmed; the client then pushes its whole state to the peer | [bin] (protocol/relay-1998.md#lobby-lines) |
| S→C | `C<id8>` | the partner left the party | [bin] (protocol/relay-1998.md#lobby-lines) |
| S→C | `D<data>` | relayed data | [bin] (protocol/relay-1998.md#lobby-lines) |
| S→C | `NR`, `NL` | sent right after `N` by the 1.1.9 server: `NR` = relay levels, `NL` = local levels (the client then starts in `onlinestartlocal.graal`); a server with local levels sends `NR` then `NL` | [bin][cap] (protocol/relay-1998.md#lobby-lines) |
| C→S | `O`, `S`, `V<id>` | observer, super user, observe a player; accepted by the 1.1.9 server | [bin] (protocol/relay-1998.md#lobby-lines) |

### 2.3.1.3 Game names

| Builds | Name sent with `N` | Source |
| --- | --- | --- |
| 1st, 2nd Graal | `Zelda2` | [bin] (protocol/relay-1998.md#game-names) |
| 3rd, 4th Graal | `Graal` | [bin] (protocol/relay-1998.md#game-names) |
| 4thgraalalpha | `Graal2` (room prefix `G2`) | [bin] (protocol/relay-1998.md#game-names) |
| 5th Graal, 5thgraalalpha | `Graal3` | [bin] (protocol/relay-1998.md#game-names) |
| 6th Graal | `Graal4` | [bin] (protocol/relay-1998.md#game-names) |
| 7th to 9th Graal | `Graal5` | [bin] (protocol/relay-1998.md#game-names) |
| 10th to 12th Graal | `Graal6` | [bin] (protocol/relay-1998.md#game-names) |
| 13th Graal | `Graal7` | [bin] (protocol/relay-1998.md#game-names) |
| 14th, 15th Graal, 1.1, 1.1.9 | `Graal8` | [bin] (protocol/relay-1998.md#game-names) |

The constant is the fallback. On a level the client sends `G<n>` plus the level's location (a web level's URL without `http://`), so each level is its own room and players meet only on the same level and a compatible build [bin][live] (protocol/relay-1998.md#game-names).

### 2.3.1.4 `D` payloads

```
D <sid:2> <type:1> <payload>
```

| Field | Encoding | Source |
| --- | --- | --- |
| `sid` | sender id as two base-128 characters, `(c0 - 32) * 128 + (c1 - 32)`; the receiver writes it back as `0000` plus 4 zero-padded digits; the server does not stamp the sender | [bin] (protocol/relay-1998.md#d-payloads) |
| coordinates | half tiles, `(c - 32) / 2` | [bin] (protocol/relay-1998.md#d-payloads) |
| knock-back and fine offsets | `(c - 96) / 16` | [bin] (protocol/relay-1998.md#d-payloads) |

| Builds | Types sent | Source |
| --- | --- | --- |
| 1st Graal | `A B C E F G H L M N O P R S T W` (can also receive `D`) | [bin] (protocol/relay-1998.md#d-payloads) |
| 2nd to 4th Graal | adds `Q` | [bin] (protocol/relay-1998.md#d-payloads) |
| 4thgraalalpha to 5thgraalalpha | adds `I U X Y Z` | [bin] (protocol/relay-1998.md#d-payloads) |
| 6th Graal | adds sending `D` | [bin] (protocol/relay-1998.md#d-payloads) |
| 7th Graal | adds `0` to `4` | [bin] (protocol/relay-1998.md#d-payloads) |
| 8th Graal, 9thgraalalpha | adds `5` | [bin] (protocol/relay-1998.md#d-payloads) |
| 9th to 14th Graal | adds `6`, `7` | [bin] (protocol/relay-1998.md#d-payloads) |
| 15th Graal, 1.1, 1.1.9 | adds `8` | [bin] (protocol/relay-1998.md#d-payloads) |

| Type | Payload | Meaning | Source |
| --- | --- | --- | --- |
| `A` | x, y, dir/flags, kind, one more byte | arrow fired; in a 1.1.9 capture, level NPCs firing every 0.5 s produced steady `A` lines from both clients, because each client runs the level NPCs itself | [bin][cap] (protocol/relay-1998.md#d-payloads) |
| `B` | x, y, w·8+h, then w·h tiles as two base-128 characters each | board modify | [bin] (protocol/relay-1998.md#d-payloads) |
| `C` | text | chat line | [bin] (protocol/relay-1998.md#d-payloads) |
| `D` | one character per object id | listed baddies or NPCs are dead | [bin] (protocol/relay-1998.md#d-payloads) |
| `E` | x, y, item index | item laid down | [bin] (protocol/relay-1998.md#d-payloads) |
| `F` | x, y, a, b | bomb laid | [bin] (protocol/relay-1998.md#d-payloads) |
| `G` | x, y, item index | item picked up | [bin] (protocol/relay-1998.md#d-payloads) |
| `H` | object id, dx, dy, damage (dx, dy in the `/16` encoding) | baddy hurt | [bin] (protocol/relay-1998.md#d-payloads) |
| `I` | none | player left the level or went to a link; cleared by the next `P` | [bin] (protocol/relay-1998.md#d-payloads) |
| `L` | level name | current level | [bin] (protocol/relay-1998.md#d-payloads) |
| `M` | repeated 6-byte records: id, x, y, sprite, dir·4+mode, state | baddy movement batch | [bin] (protocol/relay-1998.md#d-payloads) |
| `N` | text | nickname | [bin] (protocol/relay-1998.md#d-payloads) |
| `O` | carried object id (space = none) | carry object | [bin] (protocol/relay-1998.md#d-payloads) |
| `P` | x, y, sprite (animation frame·4 + direction, 0 up, 1 left, 2 down, 3 right) | position and animation, sent every 100 ms while moving | [bin][cap] (protocol/relay-1998.md#d-payloads) |
| `Q` | NPC id | `playertouchsme` for an NPC on the receiver's side | [bin] (protocol/relay-1998.md#d-payloads) |
| `R` | x, y | object at x, y removed | [inf] (protocol/relay-1998.md#d-payloads) |
| `S` | count, then that many colour indices (4 in 1st Graal, 5 from 4th alpha) | sprite colours | [bin] (protocol/relay-1998.md#d-payloads) |
| `T` | 10 characters, base 128, little end first | login time; the peer with the earliest time is level leader and runs baddies and NPCs | [bin] (protocol/relay-1998.md#d-payloads) |
| `U` | x, y, kind, id | baddy spawned | [bin] (protocol/relay-1998.md#d-payloads) |
| `W` | sprite | throws the carried object | [bin] (protocol/relay-1998.md#d-payloads) |
| `X` | target id | hit or kill aimed at one player; only the named player applies it | [inf] (protocol/relay-1998.md#d-payloads) |
| `Y` | sword power, shield power, power | sword and shield change | [bin] (protocol/relay-1998.md#d-payloads) |
| `Z` | none | state flag | [inf] (protocol/relay-1998.md#d-payloads) |
| `0` | horse image, or empty | horse on or off | [bin] (protocol/relay-1998.md#d-payloads) |
| `1`, `4` | x, y | horse and bush actions | [inf] (protocol/relay-1998.md#d-payloads) |
| `2` | dx, dy | fireball | [bin] (protocol/relay-1998.md#d-payloads) |
| `3` | len, image, script | carrying an NPC; the image can be an `http://` path | [bin] (protocol/relay-1998.md#d-payloads) |
| `5`, `6`, `7` | none | pose flags (sitting, sleeping) | [inf] (protocol/relay-1998.md#d-payloads) |
| `8` | registration-key string | duplicate key check; a peer with the same key disconnects the client with a message | [bin] (protocol/relay-1998.md#d-payloads) |

Several `D` types live on in 1.21 as numbered messages with the same meaning and similar payloads: board modify, bomb, item, horse and throw [bin] (protocol/relay-1998.md#what-changed-in-121).

## 2.3.2 1999 GSERV login (generation 2)

The first message after `connect` is an id-0 line [bin] (protocol/gserv-1999.md#login):

| Offset | Field | Type | Value | Source |
| ---: | --- | --- | --- | --- |
| 0 | type | `c` | 0 = player; the server treats 1 as RemoteControl | [bin] (protocol/gserv-1999.md#login) |
| 1 | token | 8 bytes | `GSERVnnn` (→ §1.2.2) | [bin] (protocol/gserv-1999.md#login) |
| 9 | account | `str` | the connect dialog defaults to the built-in guest login | [bin] (protocol/gserv-1999.md#login) |
| — | password | `str` | | [bin] (protocol/gserv-1999.md#login) |
| — | terminator | `\n` | | [bin] (protocol/gserv-1999.md#login) |

| GServer | Accepts | Minimum for a player connection | Source |
| --- | --- | --- | --- |
| 1.21 (May 1999) | `GSERV007` | 7 | [bin] (protocol/gserv-1999.md#what-the-gservers-accept) |
| 1.28 (Nov 1999) | `GSERV007` to `GSERV013` | 13 | [bin] (protocol/gserv-1999.md#what-the-gservers-accept) |
| GServer13 (Nov 1999) | `GSERV007` to `GSERV014` | 14 | [bin] (protocol/gserv-1999.md#what-the-gservers-accept) |

| Rule | Source |
| --- | --- |
| The server matches the token against a fixed list, stores its number (7 to 14) on the connection, then checks the minimum for the connection type; old tokens stay on the list so that RemoteControl (`GSERV011`) can log in | [bin] (protocol/gserv-1999.md#what-the-gservers-accept) |
| Refusals and login errors (version too old, account disabled, account in use, no such account) are sent as id 16 (DISCMESSAGE) | [bin] (protocol/gserv-1999.md#what-the-gservers-accept) |
| A token newer than the server's list is refused like an old one: GServer13 answers `GSERV016` and `GSERV018` with id 16 | [cap] (protocol/gserv-1999.md#what-the-gservers-accept) |
| The 1.33 to 1.39 clients use the same generation with `GNW` tokens and default to the built-in guest login; their login field layout beyond the token is unmeasured | [bin] (protocol/gserv-1999.md); [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |

Message ids and props handled per build in this generation are in → App. C.

## 2.3.3 2.x login (generation 3, type 0)

| Offset | Field | Type | Value | Source |
| ---: | --- | --- | --- | --- |
| 0 | client type | `c` | 0 (wire `0x20`) | [2.05][srv] (protocol/login-and-walk.md#login-line-first-message-sent-clean) |
| 1 | key | `c` | `rand & 0x7F`, the gen-3 key (→ §2.2.2) | [2.05] (protocol/login-and-walk.md#login-line-first-message-sent-clean); [bin] (version-profiles/gen3-insertion-200-205.tsv) |
| 2 | token | 8 bytes | e.g. `GNW03081` (2.05), `GNW22122` (2.17) | [2.05] (protocol/login-and-walk.md#login-line-first-message-sent-clean); [bin] (protocol/client-versions.md#game-server-login) |
| 10 | account | `str` | | [2.05] (protocol/login-and-walk.md#login-line-first-message-sent-clean) |
| — | password | `str` | | [2.05] (protocol/login-and-walk.md#login-line-first-message-sent-clean) |
| — | terminator | `\n` | no identity string follows the password | [2.05][bin] (protocol/login-and-walk.md#how-the-server-parses-it-srv) |

| Rule | Builds | Source |
| --- | --- | --- |
| The login message is sent without the gen-3 insertion; the messages after it carry it | 2.00 to 2.17 | [2.05][cap] (protocol/codec-and-framing.md#gen-3-205); [bin] (version-profiles/gen3-insertion-200-205.tsv) |
| The token is built one character at a time in code, so no string literal exists | 1.38 to 2.31 | [2.05] (protocol/login-and-walk.md#login-line-first-message-sent-clean); [bin] (protocol/client-versions.md#game-server-login) |
| `PLI_LANGUAGE` (37) follows the login, with a language name (`English` observed) | 2.02 rev2 and later | [2.05][cap] (protocol/login-and-walk.md#login-line-first-message-sent-clean); [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
| `PLI_TAMPERCHECK` (39) follows 37 (→ §2.4, → §4.10) | 2.17 and later Delphi clients | [bin] (protocol/client-versions.md#game-server-login) |
| The account name is kept obfuscated in memory and decoded only to build the login message; the map is `dec(b) = (~b - 10) & 0xFF` | 2.17, 2.22, 2.31 | [bin] (protocol/client-versions.md#game-server-login) |
| The password is obfuscated the same way | 2.31 | [bin] (protocol/client-versions.md#game-server-login) |
| A lab GServer-v2 admits 2.00 once `GNW24011` is in its allowed-versions list | 2.00 | [lab] (client-internals/version-tokens.md) |

## 2.3.4 2.22, 2.31 and 3.x login (generation 5, type 5)

The fields are those of → §2.3.3 with client type 5. The message travels in the fixed mode-3 login frame (→ §2.2.4) [bin] (protocol/client-versions.md#game-server-login); [bin] (protocol/v3x-clients.md#game-server-login-and-cipher).

| Builds | Type | Token | After the login | Credentials in memory | Source |
| --- | ---: | --- | --- | --- | --- |
| 2.22 | 5 | `GNW03014` | 37, then 39 | obfuscated (→ §2.3.3) | [bin] (protocol/client-versions.md#game-server-login) |
| 2.31 | 5 | `GNW28015` | 37, then 39 | obfuscated | [bin] (protocol/client-versions.md#game-server-login) |
| 3.04 Linux | 5 | `G3D03014` | 37 only; no 39 (confirmed on the wire) | plain | [bin] (protocol/v3x-clients.md#game-server-login-and-cipher) |
| 3.153 Mac | 5 | `G3D28015` | 37 only; no 39 | plain | [bin] (protocol/v3x-clients.md#game-server-login-and-cipher) |

## 2.3.5 4.x to 6.03 login (generation 5, type 5, machine ids)

| Order | Field | Type | Source |
| ---: | --- | --- | --- |
| 1 | client type 5 | `c` | [bin] (protocol/v4x-clients.md#login-packet); [bin] (protocol/v5x-clients.md#login) |
| 2 | key | `c`, `rand & 0x7F`; wire bytes above `0x7F` occur because the key goes up to `0x7F` | [bin] (protocol/v5x-clients.md#login); [cap] (protocol/v5v6-windows-unpacked.md#login-message) |
| 3 | token | 8 bytes | [bin] (protocol/v4x-clients.md#login-packet) |
| 4 | account | `str`; 224 bytes or more → `0xFF` + first 223 bytes | [bin] (protocol/v4x-clients.md#login-packet) |
| 5 | password | `str`; same long-string rule | [bin] (protocol/v4x-clients.md#login-packet) |
| 6 | machine list | comma-separated text, below | [bin] (protocol/v4x-clients.md#login-packet) |

| Builds | Field 1 | Field 2 | Field 3 | Field 4 | Field 5 | Source |
| --- | --- | --- | --- | --- | --- | --- |
| Windows 4.20r8, 5.00r7 | `win` | MD5 hex of the Windows `DigitalProductId` | MD5 hex of the network adapter MAC (fallback: node part of `UuidCreateSequential`, or `UuidCreate`) | MD5 hex of the `C:\` volume serial | none | [bin] (protocol/v4x-clients.md#login-packet); [bin] (protocol/v5x-clients.md#login) |
| Mac 4.20r6 | `mac` | hash of the primary Ethernet MAC | hash of 4 bytes of `stat("/etc")` | empty | none | [bin] (protocol/v4x-clients.md#login-packet) |
| Windows 5.12, 5.24r3 to 6.03r7 | `win` | MD5 hex of the product id (5.24 and later also read `DigitalProductId4`, so the hash differs from 5.12) | MD5 hex of the adapter MAC | MD5 hex of the `C:\` serial | quoted Windows version `"<major>.<minor> <build> <service pack>"` | [cap][bin] (protocol/v5v6-windows-unpacked.md#login-message) |
| Linux 6.01r1, 6.03r7 | `linux` | MD5 hex of the `eth0` MAC | MD5 hex of the inode number of `/etc` | empty | kernel release and version string | [bin] (protocol/v6x-clients.md#login-message-601-and-603) |

| Rule | Builds | Source |
| --- | --- | --- |
| The machine fields let a server ban per machine; 2.x and 3.x send no machine id | 4.x and later | [bin][inf] (protocol/v5x-clients.md#login); [bin] (protocol/v4x-clients.md#login-packet) |
| `PLI_LANGUAGE` (37) follows, then the socket switches to dynamic mode | 4.x to 6.03 | [bin] (protocol/v5x-clients.md#login); [bin] (protocol/v6x-clients.md#login-message-601-and-603) |
| After 37 the client requests `basepackage.gupd` (23, twice), then `arial.ttf`, `bigmap.txt` or `minimap.txt` by build, then 34 for a GUI image (→ §2.7) | 5.12 to 6.03r7 Windows | [cap] (protocol/v5v6-windows-unpacked.md#login-message) |
| Each build logs in by itself as the built-in guest once it reaches the login screen; the guest password is fixed per build family and is decrypted at run time on Linux 6.x | 5.12 to 6.03r7 | [cap][inf] (protocol/v5v6-windows-unpacked.md#login-message); [bin][inf] (protocol/v6x-clients.md#login-message-601-and-603) |
| The first connection goes to a game server named `Login`, not to a separate listserver; the client reaches a game only after S→C 178 (`PLO_SERVERWARP`) and logs in again to that host (→ §6) | 4.x to 6.03 | [bin] (protocol/v4x-clients.md#login-server-and-licensegraal); [bin][cap] (protocol/v5x-clients.md#login); [bin] (protocol/v6x-clients.md#login-server) |
| 6.11 asks for a connector script before the game socket; the script builds the login itself, so its token and layout are unmeasured (→ §2.10) | 6.11 Mac | [bin] (protocol/login-session-known.md) |

## 2.3.6 Server parse and reply sequence

### 2.3.6.1 How a GServer-v2 parses the login

| Step | Rule | Source |
| ---: | --- | --- |
| 1 | read the type GCHAR; `type = 1 << value` | [srv] (protocol/login-and-walk.md#how-the-server-parses-it-srv) |
| 2 | for type 0, read 8 bytes as a token; if they are not a known token (the gen-3 key comes first), rewind one byte, switch to generation 3, read the key, then the real token | [srv] (protocol/login-and-walk.md#how-the-server-parses-it-srv) |
| 3 | read the account and password `str`; an optional identity string read exists for later clients | [srv] (protocol/login-and-walk.md#how-the-server-parses-it-srv) |
| 4 | map the token to a version id (→ §1.3); `GNW03081` sorts below 2.1, so 2.05 gets every pre-2.1 code path (no file modification times, `PLPROP_GANI` sent as the bow slot, the 1.41 level sequence) | [srv] (protocol/login-and-walk.md#how-the-server-parses-it-srv) |

| Type value | Connection | Source |
| ---: | --- | --- |
| 0 | client (type 0: generation 2 or 3) | [srv] (protocol/login-and-walk.md#how-the-server-parses-it-srv) |
| 1 | RC | [srv] (protocol/login-and-walk.md#how-the-server-parses-it-srv) |
| 2 | NPC-server | [srv] (protocol/login-and-walk.md#how-the-server-parses-it-srv) |
| 3 | NC | [srv] (protocol/login-and-walk.md#how-the-server-parses-it-srv) |
| 4 | client 2.19 to 2.21 | [srv] (protocol/login-and-walk.md#how-the-server-parses-it-srv) |
| 5 | client 2.22 and later | [srv] (protocol/login-and-walk.md#how-the-server-parses-it-srv) |
| 6 | RC2 | [srv] (protocol/login-and-walk.md#how-the-server-parses-it-srv) |
| 8 | web | [srv] (protocol/login-and-walk.md#how-the-server-parses-it-srv) |

Other login tokens the server knows: NC `NCL11012` and `NCL21075`, RC `GSERV023` to `GSERV025`, NPC-server `GRNS0000` and `LNX00001` [srv] (protocol/login-and-walk.md#how-the-server-parses-it-srv).

### 2.3.6.2 Reply sequences

| Server | Messages after a good player login, in order | Source |
| --- | --- | --- |
| GServer13 | 9 (own props), 28 (flags, only if the account has any), 14 (warp), 100 then a separate frame with 101 and the board, 6 (level name), 1 (links), 5 (signs), 39 (level modification time), 3 (NPC props with scripts), 10 | [cap] (protocol/gserv-1999.md#what-the-gservers-accept) |
| GServer 1.28 | as GServer13 without 39 | [cap] (protocol/gserv-1999.md#what-the-gservers-accept) |
| GServer 1.21 | 9, 14, 100, 101 with the board, 6, 1, 10, all in one zlib frame; no 39 | [cap] (protocol/gserv-1999.md#what-the-gservers-accept) |
| any of the above, another player already on the level | 8 (other player's props) right after 9 | [cap] (protocol/gserv-1999.md#what-the-gservers-accept) |
| GServer-v2 as a `Login` stand-in, to 5.x and 6.x clients | 190, the level load (14, 6, 100, 101, chests, 156, 3), staff and status lists (47, 180), start and HTML messages (179, 41), 182 (the client answers with its window titles on 44); 178 is not in this burst | [wire] (protocol/login-session-known.md#the-lab-burst-these-clients-accepted) |

The bytes a public 5.x or 6.x `Login` server sends are unobserved (→ App. E#3).
