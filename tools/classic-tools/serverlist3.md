# Classic listserver (`serverlist3`)

Date: 2026-11-01

The ELF in the Server Lister package. One process, two listen ports, MySQL for accounts and the public directory. It is not the Win32 `ListServer.exe` in `../server-tools-2001.md`. **[bin]**

`tools/classic-tools/listframe.py` packs and unpacks the frame and the login lines. It does not open a socket.

## Start and config

The only argument is the full path of a config file. If it is missing, the process prints `Configuraton not found.` and `Pleace specify the full path of the configuration file as parameter.` and exits. Those spellings are in the image. **[bin]**

Each config line is `key=value`. The keys it reads are:

| Key | Role |
| --- | --- |
| `clientsport` | Port for game clients |
| `serversport` | Port for game servers |
| `playerlimit` | Cap used by the free-player check |
| `databaseserver` | MySQL server name |
| `showmore` | URL sent to a client on the trial and free-server replies |

A sample file in the same package sets the two ports to the lab client ports 14922 and 14923 and a player limit. The show-more value is whatever URL the operator wrote. **[file]**

On the console it prints `Server lister started` with the two ports. Beside the process it writes `playercount.txt`, `maxplayers.txt`, `accountcount.txt` and `playerstats.txt`. The stats file has `Servers:` and `Players:` sections, marks a player `upgraded`, `ghost` or `trial`, and a summary line for waiting ghosts, ghosts, free players and the limit. **[bin]**

## Frame

Both listeners use one framing. A frame is a big-endian 16-bit length and then that many zlib bytes. The inflated body is newline-separated lines. The first byte of a line is `id + 32`. A length-prefixed string is `count + 32` and then that many bytes. An uncompressed buffer past 16383 bytes, or an outgoing buffer past 4095 bytes, is treated as a broken link (the outgoing buffer is flushed first). **[bin]**

## What a client sends

| Id | Rest of the line |
| --- | --- |
| 0 | Edition text. Stored and used to filter the directory. |
| 1 | Account, then password, each a length-prefixed string. |
| other | Ignored. |

There is no gen-5 key, no version token of the later list, and no second cipher. **[bin]**

Id 0 selects directory rows whose edition contains that text and whose `lastwrite` is under 10 minutes. The row columns are name, language, description, homepage, version, player count, address and port. **[bin]**

Id 1 loads the account by name. The password is not placed in the query. The stored value is a `crypt` hash of the first 8 characters, with a two-character salt taken from the usual 64-character alphabet. The check is local. **[bin]**

## What the client is shown

A hard failure (unknown account, wrong password, ban) is message id 4, the error text, and the link closes. The texts include `The password is wrong`, `Your account is currently banned.`, and `The account … doesn't exist yet, please sign up for it first.` **[bin]**

A success is message id 0 (the directory line) and id 2 (the status text), and then the link closes. Status text can be `Welcome to Graal!`, a staff sentence (global, or limited to named servers), a remaining-time sentence (years, days, hours), the trial sentence, or the free-server sentence (`Thanks for buying Graal! You will have no limitations on the` / `free servers…`). **[bin]**

The trial sentence and the free-server sentence also send id 3 first, carrying the `showmore` URL. That is a URL the operator configured. The process does not open a browser and does not read a saved login. **[bin]**

## What a game server sends

The first line is the login. Its first byte is kind 0 or 1 (`byte - 32`). The next 8 bytes must be `GLSER001` or `GLSER002`. The rest of the line is the world name. Any other kind or token closes the link. Kind 1 suppresses the ghost queue message below. The world name is looked up, and the socket address must match the address stored for that world, or the console says the server is not allowed to connect from its address. **[bin]**

After login, only two ids are acted on:

| Id | Meaning |
| --- | --- |
| 4 | Player add or update. Two 7-bit bytes of player id, a flag byte, a length byte, then the name. Bit 0 and bit 1 of the flag are stored. If bit 1 is set and the login kind was 0, the listserver replies to the game server with id 7: the coded player id and, when the player is queued, `N ghost(s) before you`. |
| 5 | Player leave. Two 7-bit bytes of player id. The player is removed and the limit is checked again. |
| other | Ignored. |

The public directory is not built from these messages. It is the MySQL `serverlist` table. The game-server link is presence, the ghost queue, and the address check. **[bin]**

Account columns read for a client login: account name, encrypted password, email, blocked, only-load, admin level, admin worlds, ban time, ban reason, registration end. **[bin]**

## What it never sends

No registry walk, no saved-login harvest, no browser, no plaintext password in the account query, no gen-5 list handshake. **[bin]**
