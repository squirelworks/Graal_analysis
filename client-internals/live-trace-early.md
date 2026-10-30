# Live runs of the pre-1.33 clients (1.1.9 to 1.32)

Date: 2026-10-30

These are captures of real clients and their bundled servers running under Wine, inside a network namespace that has loopback only.
They check the static notes in `protocol/relay-1998.md`, `protocol/gserv-1999.md` and `client-internals/version-profiles/v121-v132.toml`. Tags: **[cap]** seen on the wire in these runs.
The raw pcaps and decoded dumps are in the project files under `graal-decompile/live-trace/early/`.

## How the runs were made

- Wine 9 (win32 prefix), Xvfb with openbox, Direct3D renderer set to `gdi`. Every pre-1.33 client opens its window under Wine.
- Servers: the 1.1.9 `Gserver.exe` (relay), GServer 1.28 (`GServerv.exe`, from the 1.28 beta 2 zip) and GServer13 (from the 1.3 test zip). Accounts were added in the server's Edit accounts window. The 15th Graal `.graal` levels were copied in, because the later zips don't ship `onlinestartlocal.graal`.
- Clients are pointed at the lab with `graalconfig.txt` (`gamemode=One Player Online`, `serveraddr=127.0.0.1`). For 1.1.9 the connect dialog's default host `www.graalonline.com` was mapped to 127.0.0.1.
- **1.21** ships only as an InstallShield 3 package. Its setup was run under Wine, and the installed folder (218 files) is kept in the project files under `graal-decompile/unpacked-installers/graal121/`. The installed `Graal.exe` and `GServer.exe` have the same MD5 as the copies analysed statically.
- **Keyboard under Wine.** These clients give DirectInput a keyboard data format that lists one object over a 256-byte buffer. Wine only fills listed objects, so arrow keys never reach the game, while chat and Alt keys still work because they arrive as window messages. A live patch that widens the format to 256 key objects in memory fixes this in 1.3 test and in 1.21. The exe checks its own checksum, so the file itself can't be edited. With the patch, Wine's dinput trace shows `dwNumObjs 256`. In 1.21 the player then walks. 1.28 beta 2 still doesn't walk with the patch in place: it creates four keyboard devices (one per local player), calls GetDeviceState once on each and then stops polling. Wine releases the devices again right after each Acquire, and no key event ever reaches dinput. 1.21 polled about a thousand times in the same span. The cause is not found, so no movement was captured for 1.28 beta 2.

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
- **UDP.** Once both clients are in the same level they send UDP datagrams straight to each other's port, without going through the server. Each datagram is one uncompressed message, `chr(id+32) + data`. With both players standing still, each client sent id 12 twice every 0.5 s with two fixed 5-byte payloads. The same two payloads appear in the 1.1.9 relay as `D` type `A` on the same level (below), so this is the "direct data packages" path from the 1.28 notes, carrying something periodic on that level. What it carries is still open.

## GServer13 with 1.31 (GSERV016) and 1.32 (GSERV018)

**[cap]**

- Both clients send the same login frame with their own token.
- GServer13 refuses both with id 16 "You need at least Graal version 1.3 to play on this server." A token newer than the server's list is treated as too old. It does not cause a disconnect without a message, or an "unknown version" error.
- **Saved password.** 1.31 and 1.32 (and, by string search, 1.3 test to 1.39) save the login under `HKCU\Software\Graal\Client`: `accountname`, `nickname` and `password`. The password is the 48-character DES string form from `saved-passwords.md`, with the same key that 2.05 uses. `tools/file-formats/graaldes.py` turned the value from this run back into `guest`. So the warning in `saved-passwords.md` applies from 1.3 test on, not only to 2.x. 1.28 beta 2 still reads `accountname=` and `password=` as plain text from `graalconfig.txt`.

## 1.1.9 Gserver with two 1.1.9 clients (relay)

Server started with "Use local levels". **[cap]**

- **Each client opens two TCP connections.** One joins the game `Graal8` and stays in it. The other first joins `G8` with no level, then leaves (`-`, `C`) and re-joins as `G8onlinestart.graal`, then `G8onlinestartlocal.graal`, as the client moves through levels. All lines go to the same server port.
- After every `N` the server answered `NR`, then `NL`, then `I<id8>`. Ids are `0000000n`, counted per connection.
- **Both connections pair up.** When the second client joined, each connection got `+<id>def` for the other client's connection in the same game. The client answered `P<id>`, and the server confirmed with `P` to both sides. That happened first on `Graal8` and then on `G8onlinestartlocal.graal` once both clients were on that level. The `Graal8` pair carried only the first state push (6 `D` lines each way). The level pair carried the rest (about 120 `D` lines each way in a minute). So the per-level room is where play traffic goes, as `relay-1998.md` says, and the fixed `Graal8` room is an extra channel. What the client uses that channel for beyond the first push was not seen in this short run.
- The state push after `P` is, in order: `L` (level, sent twice as the client moves on), `P` (position), `N` (nickname), `S` (colours), `7` (pose flag), and later `T` (10-character login time), `Y` (sword/shield power) and `C`.
- `D` lines carry the sender id as two base-128 characters (`" "` = 0, `"!"` = 1 …), as in `relay-1998.md`.
- **Type `A` is not only "shot fired".** With no one shooting, each client sent `A` about four times a second, alternating the same two 5-byte payloads that 1.28 beta 2 sends as UDP id 12. The row in `relay-1998.md` is marked accordingly.

## What this changes

- `gserv-1999.md`: the login reply order is now the captured one, plus the 1.28 difference (no 39), the refusal of newer tokens, the second-player 8 messages and the UDP shape.
- `relay-1998.md`: the two connections, `NR` then `NL`, and the caveat on `A`.
- `v121-v132.toml`: `credentials_in_registry` is now confirmed and names the DES string form.

## Open

- Movement in the relay builds (1.1.9 and earlier). The patch should carry over, but it hasn't been tried.
- The meaning of relay `A` / UDP id 12 on `onlinestartlocal.graal`.
- The 1.1.9 server with "Use levels from cyberjoueur": whether it then sends `NR` alone.
- Why 1.28 beta 2 stops polling its keyboards under Wine.
