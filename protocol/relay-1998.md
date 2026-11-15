# The 1998 relay protocol (1st Graal to 1.1.9)

Date: 2026-10-21

This covers every client from the first Delphi beta (Sept 1998) to 1.1 / 1.1.9 (Feb 1999), plus the `Gserver.exe` bundled with 1.1.9.
These builds have no login token and no compression. In the GServer-v2 numbering this is encryption generation 1.
The base layouts come from static analysis of the shipped executables; the linked historical runs add qualified original-program and capture evidence. No decompiler output is reproduced.

## Earliest networking capability map

This is the canonical capability summary from the Java precursors through
the GSERV transition. It reconciles existing findings, not a new runtime
survey. **NOTOKEN** below means a documented absence of a version-token
field; it is not an unresolved scan and is never a literal login string.
`[bin]` is static executable/class evidence, `[src]` retained author-source
evidence, `[cap]` captured traffic, `[live]` original-program observation,
and `[inf]` a stated inference. A captured row does not upgrade its siblings.

Sources: [Java/source scope](../client-internals/precursors-and-fan-builds.md),
[Java runs](../client-internals/precursor-runs-2026-10-30.md),
[exact relay rooms and bridge runs](../client-internals/relay-room-bridge.md),
[early native-program captures](../client-internals/live-trace-early.md),
[GSERV contracts](gserv-1999.md), and
[GServer13 run](../client-internals/live-gserver13.md).

### Build-by-build transport and identity

`R` means outgoing TCP to a game-neutral relay: LF lines, pairing and `D`
data, no account login, version token, compression, listserver discovery or
direct peer UDP. The Delphi client has a fixed-game connection and a
level-room connection; observed joins are marked separately from static
siblings. `C` means a central game-server TCP connection with accounts,
token and length-prefixed zlib frames. These are different transports,
even when both use a port called a game-server port. [bin][src][cap]

| Exact build | Transport / token | Level room; fixed game | Evidence boundary |
|---|---|---|---|
| Zelda Online 1 | No multiplayer socket; NOTOKEN | None | Applet assets/levels relative to codebase are file loading, not game networking. [bin] |
| Zelda Online 2 local version | One Java relay TCP; NOTOKEN | `Z` + level basename + `1.6`; no fixed channel | `Zlevel11.6`, pairing, peers and chat observed; board replay remains source-only. [src][live] |
| Java Graal (July 2000) | One Java relay TCP; NOTOKEN | `G2` + level filename; unused `Graal2` mode | Exact `G2level13.graal` observed; do not infer a second selected connection from an unused mode. [bin][live] |
| 1st Graal | R; NOTOKEN | Observed `Zhouse12`; `Zelda2` | Two joins observed. That string alone does not distinguish `Z` + `house12` from `Z` + `house1` + `2`; the latter builder has static support. [bin][live] |
| 2nd Graal | R; NOTOKEN | Per-level form as 1st; `Zelda2` | Static sibling contract; not a separately captured join here. [bin] |
| 3rd Graal | R; NOTOKEN | `G` + level filename; `Graal` | Both `Ghouse1.graal` and fixed join observed. [bin][live] |
| 4th Graal | R; NOTOKEN | `G` + level filename; `Graal` | Static room contract. [bin] |
| 4th Graal alpha | R; NOTOKEN | `G2` + level filename; `Graal2` | Direct shared room with Java Graal observed. [bin][live] |
| 5th Graal | R; NOTOKEN | `G3` + level filename; `Graal3` | Native joins observed; Java cross-build play required a room-renaming proxy. [bin][live] |
| 5th Graal alpha | R; NOTOKEN | `G3` + level; `Graal3` | Static room contract. [bin] |
| 6th Graal | R; NOTOKEN | `G4` + level; `Graal4` | Static room contract. [bin] |
| 7th Graal | R; NOTOKEN | `G5` + level; `Graal5` | Static room contract. [bin] |
| 8th Graal | R; NOTOKEN | `G5` + level; `Graal5` | Static room contract. [bin] |
| 9th Graal alpha | R; NOTOKEN | `G5` + level; `Graal5` | Static room contract; alpha and numbered release stay distinct. [bin] |
| 9th Graal | R; NOTOKEN | `G5` + level; `Graal5` | Static room contract. [bin] |
| 10th Graal | R; NOTOKEN | `G6` + level; `Graal6` | Static room contract. [bin] |
| 11th Graal | R; NOTOKEN | `G6` + level; `Graal6` | Static room contract. [bin] |
| 12th Graal | R; NOTOKEN | `G6` + level; `Graal6` | Static room contract. [bin] |
| 13th Graal | R; NOTOKEN | `G7` + level; `Graal7` | Static room contract. [bin] |
| 14th Graal | R; NOTOKEN | `G8` + level; `Graal8` | Static room contract. [bin] |
| 15th Graal | R; NOTOKEN | `G8` + level; `Graal8` | Static room/level-selection contract. [bin] |
| 1.1 | R; NOTOKEN | `G8` + level; `Graal8` | Static contract; do not relabel the 1.1.9 capture as this build. [bin] |
| 1.1.9 | R; NOTOKEN | `G8` + level; `Graal8` | Two- and three-client captures establish dual connections and full-mesh pairing within each room. [bin][cap] |
| 1.21 | C; `GSERV007` | No relay rooms or listserver discovery | Captured login, single-frame bootstrap and walking; no peer UDP established. [bin][cap] |
| 1.25 | C; `GSERV009` | No relay room | Static exact-build token/server contract; not upgraded by 1.21 captures. [bin] |
| 1.27 | C; `GSERV011` | No relay room | Static exact-build contract; do not transfer 1.28 peer UDP by era. [bin] |
| 1.28 beta 2 | C plus direct peer UDP; `GSERV013` | No relay room | Captured login, peer movement, arrows and server-selected leader; Wine patches qualify the run. Peer endpoint carriage still unresolved. [bin][cap] |
| 1.3 test | C plus peer UDP support; `GSERV014` | No relay room | Original GServer13/client login, files/scripts, movement and chat captured; static UDP support is separate. [bin][cap][live] |
| 1.31 | C plus peer UDP support; `GSERV016` | No relay room | Its login token was captured being refused by GServer13; that is not a successful gameplay session. [bin][cap] |
| 1.32 | C plus peer UDP support; `GSERV018` | No relay room | Same refusal boundary, separately captured token; no sibling gameplay promotion. [bin][cap] |

### What each network can actually carry

**Java precursors.** Zelda Online 1 has no peers or shared board: codebase
file reads are not a relay. Zelda Online 2 local version reads game files
from its working directory and sends position, chat, nickname, colours,
board mutations, baddy state, items and arrows through GServ parties.
Java Graal loads codebase assets/levels, uses the `G2` relay dialect, omits
the colour message and ignores several Delphi-only action types. Actual
peer movement/chat does not demonstrate every source-listed action.
[bin][src][live] See the [Zelda board/replay source boundary](../client-internals/zelda-online-1998.md#board-changes-and-a-joining-players-state).

**Delphi relay.** Positions and chat are `D` data from clients, not a
server world simulation. Board modifications are deltas; whole level files
do not travel through the relay. From 3rd Graal, a separate HTTP client
can fetch web levels; local files and cached levels are different inputs.
The 1.1.9 remote-level-option capture opened no HTTP connection, so that
arm proves `NR` selection, not a successful download. `NR` followed by `NL`
selected the local start level in the local-level arm. All observed 1.1.9
clients ran the NPC arrow scripts themselves: do not generalize Zelda's
timestamp-leader rule into a server-enforced relay NPC scheduler.
[bin][src][cap]

**Central GSERV.** Accounts and tokens replace relay room names. GServer
sends level boards, links, signs, NPC properties/scripts and requested files;
the client still executes its scripts. 1.21's captured bootstrap fits in one
zlib frame; 1.28 and 1.3 test put the raw board in a separate frame, and
only the latter adds level-modification-time message 39 in these runs.
1.28 peer UDP movement carries X/Y, sprite, status and carry sprite; the
TCP copy of changed properties did not make that captured server forward
the walk. Arrow generation passed to the next server-selected leader after
the first left. Peer endpoint fields, other UDP message meanings and
complete exact-build compatibility remain separate questions. [bin][cap]

### Endpoints, servers and observed compatibility

These early clients do not first query a modern listserver. Zelda Online 2
uses a typed relay address; Java Graal uses its codebase host; Delphi relay
clients use their connect-dialog/configured address. 1.21 and 1.28 use a
direct game-server address and accounts. Historical endpoint defaults and
modern rebuild defaults must not be substituted for one another. [bin][src]

Knorr's original GServ carried the Java and bridged Delphi runs; the
bundled 1.1.9 server carried the 1.1.9 relay runs. Central GServers have
version-dependent token lists **and player minima**: knowing an older token
does not imply accepting it as a player. GServer13 refused the separately
captured 1.31/1.32 tokens; its older retained token entries also serve RC.
[src][bin][cap] See [server acceptance](gserv-1999.md#what-the-gservers-accept).

Java Graal and **4th Graal alpha** shared `G2<level>` on stock GServ and
exchanged nicknames/chat without a room rename. Java Graal and **5th Graal**
used different rooms; their observed shared play required the `G2` to `G3`
room-prefix proxy. The proxy retained the level suffix. Movement in both
directions was observed only after the documented Wine input workaround.
Other prefix bridges are proposals, not additional tested pairs, and the
observed subset is not full action/NPC/file compatibility. [bin][live][inf]

### Evidence and implementation boundaries

The historical runs used original programs under Java/Wine harnesses,
not a new Windows-native baseline. The 5th-Graal bridge run disabled
DirectInput loading so the original's keyboard fallback worked, without
changing executable bytes or patching memory. In contrast, 1.21/1.1.9
walking used an in-memory keyboard-format patch; 1.28 additionally disabled
its joystick setting and patched UDP receive address-length initialization
in memory. Their captured behavior is retained with those interventions,
not described as unpatched execution. A room-renaming proxy is a protocol
intervention; a generated rebuild fixture is synthetic. Byte equality of
two retained files binds those bytes, not archive authenticity, origin,
stockness or historical client/server pairing. [live][cap][doc]

Reproduction status (2026-11-15) is separate from all original-behavior rows. GCR
already has relay sockets and two-client relay acceptance tests, Java GServ
multiplayer tests, and direct gen-2 TCP clients. Its [#382](https://github.com/squirelworks/graal-client-repro/pull/382)
is merged; [#384](https://github.com/squirelworks/graal-client-repro/pull/384)
is the open direct-game default correction, not new native evidence.
Seihai's 1.1.9 first-pair relay integration is in progress; it is not counted
here as implemented support or the original's captured full mesh. These dated consumer statements do not establish
original feature equivalence. [doc]

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
Numbers use the same `+32` single-character encoding as the later GCHAR. Captured Delphi position coordinates are half tiles (`(c-32)/2`); board rectangles use whole tile indices. Java position scale must be checked per dialect rather than copied from that Delphi capture. Knock-back and fine offsets use `(c-96)/16`.

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
| `T` | 10 chars, base 128, little end first | Login time; Java source uses local-timestamp comparisons for shared-state leadership/replay, not a global running minimum. This is not proof of exclusive NPC execution on every Delphi relay build: all captured 1.1.9 clients ran the arrow NPCs. |
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
