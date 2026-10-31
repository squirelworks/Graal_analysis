# The 1998 relay protocol (1st Graal to 1.1.9)

Date: 2026-10-21

This covers every client from the first Delphi beta (Sept 1998) to 1.1 / 1.1.9 (Feb 1999), plus the `Gserver.exe` bundled with 1.1.9.
These builds have no login token and no compression. In the GServer-v2 numbering this is encryption generation 1.
The notes come from static analysis of the shipped executables. No decompiler output is reproduced.

## Summary

- TCP connections to a lobby/relay server. A captured 1.1.9 client opens two to the same port: one in the fixed game (`Graal8`) and one that follows the current level (`G8<level>`). Both pair with the other player (`client-internals/live-trace-early.md`). The 1998 binaries default to the loopback address on 14801, and the connect dialog (from 3rd Graal on) is pre-filled with the Cyberjoueur server on **14802** (a fixed IPv4 placeholder `<dialog-server-host>` in 3rd, 4th and 5th Graal, `<cyberjoueur-www>` from 6th Graal, `<list-host-classic>` in 1.1.9 and 1.1). The 4th and 5th alpha builds have no pre-filled relay host.
- Every message is a text line ending in `\n`, and the first character is the command. The read buffer is 1 KB.
- The server is a lobby in the style of Stefan Knorr's Java GServ (see `client-internals/zelda-online-1998.md`). It knows nothing about the game. It groups connections into named games, gives each one an 8-character id, and forwards `D` lines between partners.
- All game state travels inside `D` lines. The server does not stamp the sender, so each `D` payload starts with the sender's own id.
- There is no peer-to-peer mode. `TAdventureServer`, which first appears in 15th Graal, is a hostname-to-IP cache record (a name string plus an address, 12-byte instance). It matches the 15th Graal readme line about IP caching. Port 14802 is just the Cyberjoueur relay port.

## Transport by build

| Builds | Socket layer | Notes |
|---|---|---|
| 1st, 2nd Graal | ICS `TWSocket` (François Piette's component), event driven | The first beta creates two client objects for the local two-player mode. |
| 3rd Graal to 1.1.9 | Plain WinSock: blocking `connect`, then `FIONBIO`, then polled `recv` | `WSAStartup(1.1)`. The host is tried with `inet_addr` first and `gethostbyname` second. |
| 15th Graal on | Same, plus the `TAdventureServer` IP cache in front of the resolver | |

Levels are not sent over this connection. Web levels are fetched over plain HTTP/1.0 (`GET <path> HTTP/1.0`) by a separate small client (`TWebClient`). The port comes from the URL: 15th Graal's built-in start level is on `<cyberjoueur-www>:7777`, the others use port 80.

## Lobby lines

Client to server:

| Line | Meaning |
|---|---|
| `N<game>#<name>` | Join `<game>` as a normal player. The clients always send the name `def` and send the real nickname later inside `D`. |
| `P<id>` | Ask to play with player `<id>`, or accept a request. |
| `C` | Leave the current party. |
| `-` | Leave the available list. The client sends it when it disconnects on purpose. |
| `D<data>` | Relay `<data>` to the party. |

Server to client:

| Line | Meaning |
|---|---|
| `I<id8>` | The id the server gives you. Ids are `0000` plus a 4-digit counter. |
| `+<id8>` | Player `<id8>` is in the same game. If it is the only peer the client knows, the client answers `P<id8>` straight away. |
| `-<id8>` | Player left. The client drops it from its peer list. |
| `P<id8>` | Partnership confirmed. The client then pushes its whole state to the peer (login time, position, colours, nickname, sword and shield, and so on). |
| `C<id8>` | The partner left the party. |
| `D<data>` | Relayed data. See below. |
| `NR` / `NL` | 15th Graal on, sent by the 1.1.9 GServer right after `N`. Read statically as `NR` = the server uses Cyberjoueur levels and `NL` = local levels; with `NL` the client starts in `onlinestartlocal.graal`. A server started with local levels sent `NR` and then `NL` after every `N`. Started with "Use levels from cyberjoueur", it sent `NR` alone, and the client stayed in `onlinestart.graal` (`client-internals/live-trace-early.md`). |

The 1.1.9 `Gserver.exe` also accepts `O` (join as observer), `S` (super user) and `V<id>` (observe a player), as the Java server did.
It is a Delphi port of the lobby with a "Start Game Server" dialog: port 14802, and a choice between local levels and levels from Cyberjoueur. Its timer also handles a separate `Chess` game.

### Game names

The game name keeps incompatible betas apart, and from 3rd Graal on it also keeps different levels apart.

| Builds | Game name sent with `N` |
|---|---|
| 1st, 2nd | `Zelda2` (1st Graal also has a branch that builds `Z` + level base + `2`, see `client-internals/early-clients.md`) |
| 3rd, 4th | `Graal` |
| 4th alpha | `Graal2` (room prefix `G2`, the same dialect as Java Graal; see `client-internals/precursors-and-fan-builds.md`) |
| 5th, 5th alpha | `Graal3` |
| 6th | `Graal4` |
| 7th to 9th | `Graal5` |
| 10th to 12th | `Graal6` |
| 13th | `Graal7` |
| 14th, 15th, 1.1, 1.1.9 | `Graal8` |

The constant name is the fallback. When the player is on a level, the client builds the name from `G<n>` plus the level's location (the URL without `http://` for a web level), so each level is effectively its own relay room.
That fits the readmes' "asynchronous multiplayer system". Players only meet when they are on the same level and run a compatible build.
Live runs on 2026-10-31 confirmed the two connections and the level rooms for 1st (`Zhouse12` + `Zelda2`), 3rd (`Ghouse1.graal` + `Graal`), 4th alpha (`G2level13.graal` + `Graal2`) and 5th Graal (`G3level13.graal` + `Graal3`), and put Java Graal in one room with 4th alpha (no help) and with 5th Graal (through a proxy that renames `G2` to `G3`). See `client-internals/relay-room-bridge.md`.

## `D` payloads

```
D <sid:2> <type:1> <payload>
```

`sid` is the sender id as two base-128 characters (`(c0-32)*128 + (c1-32)`). The receiver turns it back into `0000` plus 4 zero-padded digits.
Numbers in the payload use the same `+32` single-character encoding as the later GCHAR. Coordinates are half tiles (`(c-32)/2`). Knock-back and fine offsets use `(c-96)/16`.

Which types each build sends:

| Builds | Types |
|---|---|
| 1st | `A B C E F G H L M N O P R S T W` (it can also receive `D`) |
| 2nd to 4th | adds `Q` |
| 4th alpha to 5th alpha | adds `I U X Y Z` |
| 6th | adds sending `D` |
| 7th | adds `0` to `4` |
| 8th, 9th alpha | adds `5` |
| 9th to 14th | adds `6`, `7` |
| 15th, 1.1, 1.1.9 | adds `8` |

What each type means. Layouts come from the receiving side. Types marked *inferred* are named from the game code they call and the sounds and objects it touches, not from a capture.

| Type | Payload | Meaning |
|---|---|---|
| `A` | x, y, dir/flags, kind, one more byte | Arrow fired (`TAdventureFlying`). In a 1.1.9 capture the steady `A` lines on `onlinestartlocal.graal` came from two level NPCs that run `shootarrowleft` and `shootarrowup` every 0.5 s. The payloads decode as x and y in half tiles at each NPC, direction 1 (left) and 0 (up). Each client runs the level's NPCs itself, so both clients sent them (`client-internals/live-trace-early.md`) |
| `B` | x, y, w·8+h, then w·h tiles as two base-128 chars each | Board modify |
| `C` | text | Chat line (the client also shows its own `showname` text) |
| `D` | one char per object id | Listed baddies or NPCs are dead (`compsdead`) |
| `E` | x, y, item index | Item laid down (`greenrupee`, `bluerupee`, `fullheart` … table) |
| `F` | x, y, a, b | Bomb laid (`put.wav`; the 1st Graal handler creates a `TAdventureBomb`) |
| `G` | x, y, item index | Item picked up (`extra.wav`) |
| `H` | object id, dx, dy, damage | Baddy hurt (dx and dy use the `/16` encoding) |
| `I` | none | The player has left the level or gone to a link. Cleared by the next `P` |
| `L` | level name | Current level (checked against the web-level path) |
| `M` | repeated 6-byte records: id, x, y, sprite, dir·4+mode, state | Baddy movement batch |
| `N` | text | Nickname |
| `O` | carried object id (`' '` = none) | Carry object |
| `P` | x, y, sprite | Position and animation. Also plays step sounds and the horse sound. Captured walking: x and y in half tiles, and the third byte is animation frame·4 + direction (0 up, 1 left, 2 down, 3 right), sent every 100 ms while moving |
| `Q` | NPC id | `playertouchsme` for an NPC on the receiver's side |
| `R` | x, y | Object at x,y removed (*inferred*) |
| `S` | count, then that many colour indices | Sprite colours (4 in 1st Graal, 5 from 4th alpha) |
| `T` | 10 chars, base 128, little end first | Login time. The peer with the earliest time becomes the level leader and runs the baddies and NPCs |
| `U` | x, y, kind, id | Baddy spawned (`TComputer`) |
| `W` | sprite | Throws the carried object (`TAdventureCarry`) |
| `X` | target id | Hit or kill aimed at one player. Only the named player applies it (*inferred*) |
| `Y` | sword power, shield power, power | Sword and shield change (`chest.wav` path) |
| `Z` | none | State flag (*inferred*) |
| `0` | horse image, or empty | Horse on or off (`TAdventureHorse`) |
| `1`, `4` | x, y | Horse and bush actions (*inferred*) |
| `2` | dx, dy | Fireball (`fire.wav`) |
| `3` | len, image, script | Carrying an NPC (`TEditorPerson`). The image can be an `http://` path |
| `5`, `6`, `7` | none | Pose flags. The readme dates sitting and sleeping to 13th Graal (*inferred*) |
| `8` | registration-key string | Duplicate key check. If a peer shows the same `reg.code` key, the client says "Another player uses the same registration key like you. You will be disconnected." |

## The Java lobby this comes from

The lobby itself is Knorr's "GServ Standalone" (1997), shipped with source in Zelda Online 2. Its full line set (observer, super user, watch, the `+<id><name>` form, the ignored `H` score line) and the Zelda Online 2 and Java Graal room names (`Z<level>1.6`, `G2<level>`) are in `client-internals/precursors-and-fan-builds.md`.

## What changed in 1.21

The relay is gone in 1.21. It is replaced by a central GServer with accounts, a version token and zlib. See `gserv-1999.md`.
Several `D` types live on as numbered packets with the same meaning and similar payloads, such as board modify, bomb, item, horse and throw.
