# Live runs of the pre-1.33 clients (1.1.9 to 1.32)

Date: 2026-10-30

These are captures of real clients and their bundled servers running under Wine, inside a network namespace that has loopback only.
They check the static notes in `protocol/relay-1998.md`, `protocol/gserv-1999.md` and `client-internals/version-profiles/v121-v132.toml`. Tags: **[cap]** seen on the wire in these runs.
The raw pcaps and decoded dumps are in the project files under `graal-decompile/live-trace/early/`.

## How the runs were made

- Wine 9 (win32 prefix), Xvfb with openbox, Direct3D renderer set to `gdi`. Every pre-1.33 client opens its window under Wine.
- Servers: the 1.1.9 `Gserver.exe` (relay), GServer 1.28 (`GServerv.exe`, from the 1.28 beta 2 zip) and GServer13 (from the 1.3 test zip). Accounts were added in the server's Edit accounts window. The 15th Graal `.graal` levels were copied in, because the later zips don't ship `onlinestartlocal.graal`.
- Clients are pointed at the lab with `graalconfig.txt` (`gamemode=One Player Online`, `serveraddr` set to the loopback address). For 1.1.9 the connect dialog's default host `<list-host-classic>` was mapped to the loopback address.
- **1.21** ships only as an InstallShield 3 package. Its setup was run under Wine, and the installed folder (218 files) is kept in the project files under `graal-decompile/unpacked-installers/graal121/`. The installed `Graal.exe` and `GServer.exe` have the same MD5 as the copies analysed statically.
- **Keyboard under Wine.** These clients give DirectInput a keyboard data format that lists one object over a 256-byte buffer. Wine only fills listed objects, so arrow keys never reach the game, while chat and Alt keys still work because they arrive as window messages. A live patch that widens the format to 256 key objects in memory fixes this in 1.3 test and in 1.21. The exe checks its own checksum, so the file itself can't be edited. With the patch, Wine's dinput trace shows `dwNumObjs 256`. In 1.21 the player then walks. 1.28 beta 2 walks with the same patch, plus `joystickon=false` in `graalconfig.txt`. 1.1.9 walks with the same patch, and both 1.1.9 clients in a two-player run could move.
- **1.28 UDP receive under Wine.** At first only the 1.28 instance started first could move. The second stopped polling its keyboard right after login. The cause is in the game's UDP receive routine. It calls `recvfrom(sock, buf, 0x400, 0, &from, &fromlen)` without ever setting `fromlen`, a local variable that held a stack address (about 3.2 million) in the traced runs. When the first datagram arrives (an arrow from the other client), Wine fills the address buffer out to that length and writes past the top of the main thread's stack. The exception chain on the stack is then overwritten, and the thread loops through nested access violations until the stack overflows. The window stays open and Wine keeps passing it key events, but the game loop is dead. The first instance never got a datagram (the second died before sending one), so it kept running. Windows checks only that `fromlen` is at least 16 and writes 16 bytes, so the bug would not show there (*inferred*). An in-memory patch that sets `fromlen` to 16 before the call fixes it. With the patch on both instances, both players walk and UDP flows both ways. The patch script is `udpfix.py` in the project files.

## GServer 1.21 with 1.21 (GSERV007)

**[cap]**

- The login frame has the same shape, with `GSERV007`. The installed server ships `accounts.txt` with two accounts, `guest`/`guest` and `super`/`super`. Each line holds `chr(len+32)` + name, `chr(len+32)` + password, then the starting props in the same encoding as id 9.
- The reply is **one zlib frame** holding 9 (own props), 14 (warp to `level1.graal`), 100, 101 with the board, 6 (level name), 1 (links) and 10. 1.28 and 1.3 test put 101 in a frame of its own. There is no 39, as in 1.28.
- Walking sends one id 2 message every 100 ms with X/Y and SPRITE, as in 1.3 test.
- The installer pops up "No MCI device open." under Wine (no MIDI device). Pressing OK continues.

## GServer13 with 1.3 test (GSERV014)

Run by the live-trace lab. **[cap]**

- The first client frame is a u16 big-endian length followed by a zlib stream holding `" GSERV014" + chr(5+32) "guest" + chr(5+32) "guest" "\n"`, as in `gserv-1999.md`.
- A bad account gets id 16 with "An account with the name and password you typed in doesn't exist."
- Reply order after a good login: 9 (own props), [28 (flags), only when the account has flags], 14 (level warp: x, y, level), 100 (raw size) and then a separate zlib frame holding 101 and the board, 6 (level name), 1 (links), 5 (signs), **39 (level modification time)**, 3 (NPC props, scripts included), 10.
- The client then asks for NPC images with 23, sets flags with 18, and adds the level's horses with 7. The server answers 30 (file send failed) for the missing images, and deletes the horses with 18 when the horse lifetime runs out (10 s).
- Walking sends one id 2 (props) message per 100 ms with X and SPRITE. Chat is id 2 with prop 12.

## GServer 1.28 with 1.28 beta 2 (GSERV013)

**[cap]**

- The login frame has the same shape, with `GSERV013`.
- The reply order is the same as 1.3 test, except that **there is no id 39**. The level-timestamp cache is new in 1.3 (the 1.3 notes: "levels will be saved on the local hard disk … they contain a timestamp").
- The own-props string (id 9) is one prop shorter than in 1.3 test, which ends with an extra prop (`@R`). That fits a parser that stops at prop 31 in 1.28 beta 2 and 32 in 1.3 test (`v121-v132.toml`).
- A second login with an account that is already online gets id 16 "The account is already in use." The account's first session keeps playing.
- **Second player.** The newcomer gets its own 9 and then, in the same frame, an 8 (other player's props) for the player already in the level, before the 14 warp. The player already there gets 8 messages about the newcomer, starting with the nickname and level. The ids in those 8 messages are the server's player numbers (1 and 2 here). Where the UDP address and port are carried has not been decoded. The other-player props are the obvious place (*inferred*).
- **UDP.** Once both clients are in the same level they send UDP datagrams straight to each other's port, without going through the server. Each datagram is one uncompressed message, `chr(id+32) + data`.
  - **Walking:** the moving client sends **UDP id 0** to the other player every 100 ms. The five bytes are the player props X, Y, SPRITE, STATUS and CARRYSPRITE (15 to 19), each +32. That is the same field list as UDP id 0 in 2.05 (`protocol/udp-p2p.md`).
    - X and Y are in half tiles; Y went up by 2 per step while walking down.
    - SPRITE is animation frame·4 + direction (0 up, 1 left, 2 down, 3 right). Walking down cycled 22, 14, 6, 14 and stopped at 2.
    - STATUS was 16 (`0x10`) and turned 20 (`0x14`) while the player crossed the lake south of the start, then back to 16 past it. At the same moment the client sent prop 18 = 20 over TCP. So `0x04` is the swimming state in this build (*inferred* from where it flipped; later servers name `0x04` "male").
    - The trailing `0x1F` is CARRYSPRITE −1 (nothing carried).
  - At the same time the walking client sends TCP id 2 to the server with only the changed props (16, 17 and, when it flips, 18). **The server forwards nothing to the other player.** The other client sees the walk only through UDP. That is the "player positions & sprite numbers … sent directly to all players that are in the same room" of the 1.28 notes.
  - **Arrows:** id 12 twice every 0.5 s is **arrow add**. The level `onlinestartlocal.graal` has two NPCs whose scripts run `shootarrowleft` and `shootarrowup` on a 0.5 s timeout. The payloads are x, y (half tiles, at each NPC), direction (1 left, 0 up), a type byte, and a last byte sent as `v+33`, the same layout as the later `ARROWADD` (`protocol/packet-layouts.md`). Only one client sends them, to every other player in the level. In a three-client run the first player in the level sent them to the other two. When it quit, the player who had joined second took over within a second and sent them to the third. So 1.28 has one player per level that runs the NPC timeouts for everyone, and the role passes on when that player leaves. **The server picks that player** with id 10 (`ISLEADER`, no payload). The first player's login reply ended with 10, and the second and third players' replies had none. When the first player quit, the server sent 10 to the player who had joined second, and then sent 8 with prop 51 (player gone) about player 1 to both remaining players. The arrows from the new leader started straight after. 1.21 and 1.3 test also end the first player's login reply with 10, so the leader role is older than UDP.
  - A newcomer sends one UDP id 22 with no payload to each player already in the level (seen in the two- and three-client runs). 2.05 uses 22 for chat, so this is most likely the newcomer's empty chat text (*inferred*).

## GServer13 with 1.31 (GSERV016) and 1.32 (GSERV018)

**[cap]**

- Both clients send the same login frame with their own token.
- GServer13 refuses both with id 16 "You need at least Graal version 1.3 to play on this server." A token newer than the server's list is treated as too old. It does not cause a disconnect without a message, or an "unknown version" error.
- **Saved password.** 1.31 and 1.32 (and, by string search, 1.3 test to 1.39) save the login under `HKCU\Software\Graal\Client`: `accountname`, `nickname` and `password`. The password is the 48-character DES string form from `saved-passwords.md`, with the same key that 2.05 uses. `tools/file-formats/graaldes.py` turned the value from this run back into `guest`. So the warning in `saved-passwords.md` applies from 1.3 test on, not only to 2.x. 1.28 beta 2 still reads `accountname=` and `password=` as plain text from `graalconfig.txt`.

## 1.1.9 Gserver with two 1.1.9 clients (relay)

Server started with "Use local levels". **[cap]**

- **Each client opens two TCP connections.** One joins the game `Graal8` and stays in it. The other first joins `G8` with no level, then leaves (`-`, `C`) and re-joins as `G8onlinestart.graal`, then `G8onlinestartlocal.graal`, as the client moves through levels. All lines go to the same server port.
- After every `N` the server answered `NR`, then `NL`, then `I<id8>`. Ids are `0000000n`, numbered across all connections in the order they connect (the three-client run below gave 1 to 6). A connection keeps its id when it changes room.
- **Both connections pair up.** When the second client joined, each connection got `+<id>def` for the other client's connection in the same game. The client answered `P<id>`, and the server confirmed with `P` to both sides. That happened first on `Graal8` and then on `G8onlinestartlocal.graal` once both clients were on that level. The `Graal8` pair carried only the first state push (6 `D` lines each way). The level pair carried the rest (about 120 `D` lines each way in a minute). So the per-level room is where play traffic goes, as `relay-1998.md` says, and the fixed `Graal8` room is an extra channel. What the client uses that channel for beyond the first push was not seen in this short run.
- The state push after `P` is, in order: `L` (level, sent twice as the client moves on), `P` (position), `N` (nickname), `S` (colours), `7` (pose flag), and later `T` (10-character login time), `Y` (sword/shield power) and `C`.
- `D` lines carry the sender id as two base-128 characters (`" "` = 0, `"!"` = 1 …), as in `relay-1998.md`.
- **Type `A` is an arrow shot.** Each client sent `A` about four times a second, alternating two 5-byte payloads. They are the arrows of the two shooting NPCs in `onlinestartlocal.graal` (see the 1.28 UDP id 12 notes above). Unlike 1.28, both 1.1.9 clients sent them, because each client runs the level's NPC scripts itself.
- **Walking.** With the keyboard patch both 1.1.9 clients walk. The moving client sends `D` type `P` on the level connection every 100 ms: x and y in half tiles, then frame·4 + direction, the same encoding as SPRITE in 1.28. Walking right gave `^\3`, `` `\3 ``, `b\+` … (x up by 2 per step, y fixed); stopping sent the idle frame (`#` = 3, facing right).
- **"Use levels from cyberjoueur".** With that option the server sent `NR` alone after each `N`, with no `NL`. The client then joined `G8onlinestart.graal` and stayed there, instead of moving on to `onlinestartlocal.graal`. It opened no other connection (no HTTP).

## 1.1.9 Gserver with three 1.1.9 clients (relay)

Server started with "Use local levels". **[cap]**

- Every connection pairs with every other connection in the same room. When the third client joined `Graal8`, the server sent it `+` for both existing `Graal8` connections, and sent each of them `+` for the newcomer. The same happened in the level room. Each pair then exchanged `P`. So a relay game is a full mesh of pairs, and every `D` line goes to all the sender's partners.
- Each time the newcomer's level connection joined a room, the server first sent it `C<id>` for every other connection id, including ones it was about to pair with, then the `+` lines. This looks like a reset of old partnerships before the new ones (*inferred*).
- When a client quit, the server sent `C<id>` for its level connection to the partners in that room, and `-<id>` for both of its connections to every connection, in all rooms. The other clients carried on, and the remaining ones could still walk.
- **No leader.** All three clients sent the NPC arrows (`A`) all the time, and the two remaining clients went on doing so after the first quit. In the relay each client runs the level's NPC scripts for itself. The leader in 1.21 and later comes from the GSERV server (id 10, above).

## What this changes

- `gserv-1999.md`: the login reply order is now the captured one, plus the 1.28 difference (no 39), the refusal of newer tokens, the second-player 8 messages and the UDP shape.
- `relay-1998.md`: the two connections, `NR` then `NL` (or `NR` alone with Cyberjoueur levels), `A` = arrow shot, and the `P` sprite encoding.
- `gserv-1999.md`: UDP id 0 = X, Y, SPRITE, STATUS, CARRYSPRITE, id 12 = arrow add, and id 10 = level leader.
- `v121-v132.toml`: new `level_leader` feature.
- `v121-v132.toml`: `credentials_in_registry` is now confirmed and names the DES string form.

## Open

Nothing from these runs is left open.
