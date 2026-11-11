<!-- manual: kind=reference status=draft -->
# 5 Game servers

This part describes the game servers that Graal clients talk to: the original 1999 GServer13, the 2006 39ster 2.1 remake, and GServer-v2 as the reference for later behaviour. Login frames are in → §2.3, ciphers in → §2.2, and the reply sequence after a good login in → §2.3.6. The listserver is in → §6, RC and NC in → §7.

> Status: draft. No official 2000–2002 GServer binary is in the archive, so the 2.x-era server rules here come from GServer-v2 and the 39ster remake, not from an original server.

## 5.1 GServer13 (1999)

GServer13 is the server shipped with the 1.3 test client in the `graal13b` archive; it was run with its own client under Wine on the loopback address [live][cap] (client-internals/live-gserver13.md).

### 5.1.1 Options and defaults

GServer13 opens a start dialog before it listens, and saves the values to `serverconfig.txt` [live] (client-internals/live-gserver13.md#server-settings-and-the-default-account-live):

| Key | Dialog label | Default | Source |
| --- | --- | --- | --- |
| `serverport` | port | 14804 | [live] (client-internals/live-gserver13.md#server-settings-and-the-default-account-live) |
| `respawntime` | Respawn time (bushes etc.) in sec | 10 | [bin][live] (client-internals/board-respawn.md#options) |
| `horselifetime` | Horse lifetime in sec | 10 | [bin][live] (client-internals/board-respawn.md#options) |
| `apincrementtime` | Alignment increment time in sec | 1200 | [bin][live] (client-internals/board-respawn.md#options) |
| `baddyrespawntime` | Baddies respawn time in sec | 60 | [bin][live] (client-internals/board-respawn.md#options) |

GServer 1.28 beta 2 (`GServerv.exe`) has the same four timer keys [bin] (client-internals/board-respawn.md#options). An RC of 2000 can set the same four timers over the wire (→ §7.1.4).

### 5.1.2 Accounts

GServer13 creates every new account from the same template. Each row gives one field of a new account and its default, read from a live run [live] (client-internals/live-gserver13.md#server-settings-and-the-default-account-live).

| Field of a new account (Edit accounts) | Default | Source |
| --- | --- | --- |
| level and position | `onlinestartlocal.graal` at x 30.5, y 30 | [live] (client-internals/live-gserver13.md#server-settings-and-the-default-account-live) |
| AP, MP | 50, 0 | [live] (client-internals/live-gserver13.md#server-settings-and-the-default-account-live) |
| hearts | 3 of 3 | [live] (client-internals/live-gserver13.md#server-settings-and-the-default-account-live) |
| rupees, bombs, arrows | 0, 10, 5 | [live] (client-internals/live-gserver13.md#server-settings-and-the-default-account-live) |
| glove, bomb, bow power | 1, 1, 1 | [live] (client-internals/live-gserver13.md#server-settings-and-the-default-account-live) |
| sword, shield | 1 `sword1.gif`, 1 `shield1.gif` | [live] (client-internals/live-gserver13.md#server-settings-and-the-default-account-live) |
| head, colours | `head0.gif`; orange, white, blue, red, black | [live] (client-internals/live-gserver13.md#server-settings-and-the-default-account-live) |
| weapons, spin attack | weapons enabled, no spin attack | [live] (client-internals/live-gserver13.md#server-settings-and-the-default-account-live) |

The rights levels are no rights, Graalian Police, Trusted Admin and Administrator [live] (client-internals/live-gserver13.md#server-settings-and-the-default-account-live). The 1.3 archive does not ship `onlinestartlocal.graal`; the lab copied it from the 15th Graal build, which uses the same `GR-V1.03` format [live] (client-internals/live-gserver13.md#server-settings-and-the-default-account-live). The account files of this server family are in → §5.4.1.

### 5.1.3 Login and play

The rules below follow a client through a GServer13 session: the first frame, a refused login, and what arrives after a good one [cap] (client-internals/live-gserver13.md#login-cap).

| Rule | Source |
| --- | --- |
| The client's first frame is a `u16be` length and zlib of the id-0 login line with `GSERV014`, account and password (→ §2.3.2) | [cap] (client-internals/live-gserver13.md#login-cap) |
| A wrong account is answered with id 16 and the text "An account with the name and password you typed in doesn't exist."; the client offers Reconnect or Play offline | [cap] (client-internals/live-gserver13.md#login-cap) |
| After a good login the board goes in a separate zlib frame (100, then a frame with 101 and 8192 bytes); the full reply order is in → §2.3.6.2 | [cap] (client-internals/live-gserver13.md#login-cap) |
| The client then asks for each NPC image with id 23; the server answers id 30 (file not sent) for images it lacks | [cap] (client-internals/live-gserver13.md#login-cap) |
| The client sets flags from NPC scripts with id 18 and adds horses with id 7 (from `puthorse`); the server deletes each horse with id 18 about 9.5 to 9.8 s later, matching the 10 s horse lifetime on a 1 s tick | [cap] (client-internals/live-gserver13.md#login-cap) |
| The level leader (the player who sends level NPCs' arrows to the others over UDP) is picked by the server with id 10, sent at the end of the first player's login reply and to the next player when the leader leaves | [cap] (protocol/gserv-1999.md#udp-128-beta-2-on) |
| While a key is held the client sends id 2 with X (prop 15) and SPRITE (17) every 100 ms | [live][cap] (client-internals/live-gserver13.md#in-play-live-cap) |
| Chat is id 2 prop 12; the server relays it; 1.3 draws it with no bubble | [live][cap] (client-internals/live-gserver13.md#in-play-live-cap) |
| Horse deletes and bush regrowth land on the same fractional second, so the server checks its timers once a second | [cap] (client-internals/live-gserver13.md#login-cap) |

### 5.1.4 Board changes and respawn

A board change goes through a fixed set of steps on GServer13. The steps below are in order. Step 3 is the one a client author must know, because the sender gets no echo [bin] (client-internals/board-respawn.md#pli_boardmodify-1-handling-bin).

| Step of `PLI_BOARDMODIFY` (1) | Rule | Source |
| ---: | --- | --- |
| 1 | needs at least 4 bytes, a current level, and `len ≥ 4 + 2·w·h` | [bin] (client-internals/board-respawn.md#pli_boardmodify-1-handling-bin) |
| 2 | writes the new tiles into the server's 64 × 64 board and keeps the old tiles | [bin] (client-internals/board-respawn.md#pli_boardmodify-1-handling-bin) |
| 3 | if a tile changed, relays `PLO_BOARDMODIFY` (7) with the client's bytes to every other player in the level; **the sender is not echoed** | [bin][live] (client-internals/board-respawn.md#pli_boardmodify-1-handling-bin) |
| 4 | a change of exactly 2 × 2 gets a countdown `Trunc(Random · R/2 + 3R/4)` with R = `respawntime`; any other size never respawns (1 × 1, 2 × 1, 3 × 3, the 4 × 4 push/pull block) | [bin][live] (client-internals/board-respawn.md#pli_boardmodify-1-handling-bin) |
| 5 | there is no tile check: any 2 × 2 change respawns, whatever the tiles | [bin] (client-internals/board-respawn.md#pli_boardmodify-1-handling-bin) |
| 6 | the record joins the "changed since you left" list of every player who left the level since loading it; an earlier record with the same `x, y, w, h` is replaced | [bin] (client-internals/board-respawn.md#pli_boardmodify-1-handling-bin) |

Respawn runs from a one-second timer. The rules below give the timer, what a restore sends and when it lands [bin] (client-internals/board-respawn.md#respawn-tick-bin).

| Respawn tick | Rule | Source |
| --- | --- | --- |
| timer | a 1000 ms timer walks every loaded level, empty or not, and decrements each countdown | [bin] (client-internals/board-respawn.md#respawn-tick-bin) |
| restore | at < 1 the server removes the record, sends `PLO_BOARDMODIFY` (7) with the **old** tiles to everyone in the level, the original sender included, and writes them back into its board | [bin][live] (client-internals/board-respawn.md#respawn-tick-bin) |
| timing | for R = 10 the countdown starts at 7..12 and the first tick comes 0 to 1 s after the change, so the restore lands 6 to 12 s later; 7 and 12 are half as likely as 8 to 11 | [bin] (client-internals/board-respawn.md#respawn-tick-bin) |
| measured | 60 of 60 2 × 2 changes respawned after 6.21 to 11.98 s, mean 9.21 s; other sizes never respawned; restored tiles were the level's own tiles | [live] (client-internals/board-respawn.md#measured-live); [live] (version-profiles/lab-gs13-respawn.tsv) |
| re-entry | a player with no change list gets the level as on a first visit; otherwise only the queued changes go out and the list is dropped; the exact packet is hard to read | [bin][inf] (client-internals/board-respawn.md#level-re-entry-bin) |
| disconnect | the player's change lists are freed | [bin] (client-internals/board-respawn.md#level-re-entry-bin) |

Item drops from cut bushes and pots are rolled by the 1.3 client, not by GServer13 [bin][cap] (client-internals/board-respawn.md#summary); the client side is in → §4.5.

### 5.1.5 Scripts

GServer13 has player and NPC props, including an NPC nickname field, but no GS1 command table and no `setcharprop` or `showcharacter` strings; NPC scripts of this era are carried to clients and run there [bin] (server-notes/setcharprop-hash-n.md#1-gserver13-1999-cannot-settle-the-value-question-by-lab). GServer 1.34's Windows binary lists `showcharacter` but not `setcharprop` [bin] (server-notes/setcharprop-hash-n.md#2-server-side-gs1-gserversource-archive). Server-side scripting is in → §5.5.

## 5.2 39ster 2.1 GServer

An open remake of the 1.39 server from December 2006, targeting 2.x clients; one Windows/POSIX C++ process with no script VM [src] (ash/ARCHITECTURE.md). The `ash/` notes describe this tree as written [src] (ash/INDEX.md).

### 5.2.1 Process and data

The 39ster server is a small threaded program. Each row gives one part of its process or data, with the rule that governs it [src] (ash/INDEX.md).

| Item | Rule | Source |
| --- | --- | --- |
| listen port | 14822 by default | [src] (ash/INDEX.md) |
| threads | a main thread (accept loop with a 1 s `select`, `gameTime` + 1 each second, idle kick after 300 s) and one thread per connection; shared heaps, no locks | [src] (ash/ARCHITECTURE.md#2-process-and-thread-model) |
| player cap | `maxPlayers` 100, never enforced; player ids come from a free list | [src] (ash/ARCHITECTURE.md#2-process-and-thread-model) |
| data files | `data/` is walked once at boot; a file is found by basename, first match wins | [src] (ash/BLUEPRINT.md#source-tree) |
| accounts | `accounts/<name>`, plain text; loading is a stub that spawns every player on `level13.graal` | [src] (ash/ARCHITECTURE.md#4-data-stores) |
| weapons | `Weapons.txt`, INI style | [src] (ash/ARCHITECTURE.md#4-data-stores) |
| level formats | GR-V1.01 (12-bit codes), GR-V1.02 and 1.03 (13-bit codes) (→ §3.1); no `.nw` loader | [src] (ash/ALGORITHMS.md#a8--gr-v1-tile-bitstream); [src] (ash/ARCHITECTURE.md) |

### 5.2.2 Connections and login

Each row gives how the 39ster server frames and reads one kind of connection. The RC row shows how much of the RC side is only a stub [src] (ash/BLUEPRINT.md#wire-frame-blueprint).

| Item | Rule | Source |
| --- | --- | --- |
| frame | `u16be` length (raw, not a G-integer) + zlib; the inflated body is `\n`-separated messages | [src] (ash/BLUEPRINT.md#wire-frame-blueprint) |
| player (type 0) | the login line carries a key; every later line drops one byte chosen by the LCG (→ §2.2.2) | [src] (ash/ARCHITECTURE.md#1-system-context); [src] (ash/ALGORITHMS.md#a4--player-descramble-drop-one-lcg) |
| RC (type 1) | same framing, no descramble; RC ids 51 to 87 are in the table but their bodies are empty stubs | [src] (ash/ARCHITECTURE.md#1-system-context) |
| login line | `c type`, `c key` (player only), version (7 bytes for a player, 8 for RC), 1 byte skipped, `str account`, `str password`; the login line itself is not scrambled | [src] (ash/BLUEPRINT.md#wire-frame-blueprint) |
| descramble | iterator starts at `0x04A80B38`; per line `iterator = iterator · 0x8088405 + key`, then the byte at `(iterator & 0xFFFF) mod count` is dropped | [src] (ash/ALGORITHMS.md#a4--player-descramble-drop-one-lcg) |
| G-integers | 1 to 5 bytes, 7-bit groups high first, each + 32 (→ §2.1.1); widths used: 2 for player id and script length, 3 for rupees, kills, deaths and NPC id, 5 for file time | [src] (ash/ALGORITHMS.md#a1--gchar-numeric-codec) |
| head image | `c (100 + n)` then n bytes; an inbound length below 100 is a classic head index, `head{n}.gif` | [src] (ash/ALGORITHMS.md#a1--gchar-numeric-codec) |

Besides the named messages, the server sends three special ids. Each row gives one, its role and its payload [src] (ash/BLUEPRINT.md#server--client-special-ops-not-in-the-named-enum).

| Server id | Role | Payload | Source |
| ---: | --- | --- | --- |
| 100 | announced length | G-integer size of the next packet | [src] (ash/BLUEPRINT.md#server--client-special-ops-not-in-the-named-enum) |
| 101 | raw board | 4096 native `short` tiles | [src] (ash/BLUEPRINT.md#server--client-special-ops-not-in-the-named-enum) |
| 102 | file | 5-byte G-integer modification time, `c` name length, name, raw bytes | [src] (ash/BLUEPRINT.md#server--client-special-ops-not-in-the-named-enum) |

The header comments of the 2006 tree give wrong opcode numbers after 83; the `msgFuncs[89]` table and the C enums are the reliable source [src] (ash/INDEX.md).

## 5.3 GServer-v2 reference behaviour

GServer-v2 is an open reimplementation, not an original server [src] (client-internals/board-respawn.md#gserver-v2-lab-server-src). Where this part says "GServer-v2", it means the behaviour read in its source or seen in the lab; it is the reference for what 2.x and later clients accept, not a record of the official servers.

### 5.3.1 Server source lineage

Several server source trees survive. Each row gives one tree, the era it belongs to and how its code is laid out [src] (server-notes/01-lineage.md#what-is-actually-source).

| Tree | Era | Shape | Source |
| --- | --- | --- | --- |
| `linuxgserver131` | 1.31 | one `gserver.cpp` monolith, about 9k lines with zlib headers | [src] (server-notes/01-lineage.md#what-is-actually-source) |
| `sidrax-v1.4-srv-src-1.3.9` | 1.3.9 | `gserver.cpp`, `levels.cpp`, `npcs.cpp`, MySQL accounts | [src] (server-notes/01-lineage.md#what-is-actually-source) |
| `oldwin32-gserver1.39source` | 1.39 | same family, Win32 | [src] (server-notes/01-lineage.md#what-is-actually-source) |
| `gservernwsrc` | NW, about 1.4 | objects and Pascal strings | [src] (server-notes/01-lineage.md#what-is-actually-source) |
| gs2emu (`d3ecab4`) | Reborn 2.x | typed classes, about 18k lines | [src] (server-notes/01-lineage.md#what-is-actually-source) |
| Reborn binaries 2.1.0 to 2.4.0, GServer revisions 29, 31, 51 | 2.x, 2.17 line | binaries and default worlds only | [src] (server-notes/01-lineage.md#what-is-binary--world-only) |

The trees group into three eras. Each row gives what an era changed in how a server is built [src] (server-notes/01-lineage.md#what-changed-between-eras).

| Era | What changed | Source |
| --- | --- | --- |
| 1.3.x monolith | one listen socket and one world; login, movement and chat in one file; Pascal strings (`c` length + bytes); MySQL or flat-file accounts; generation 3 at most | [src] (server-notes/01-lineage.md#what-changed-between-eras) |
| gs2emu / Reborn 2.x | `servers.txt` runs several worlds in one process; typed players (client, RC, NPC-server); generations 3, 4 and 5 chosen by the login type; `GRACC001` account files and `GLEVNW01` levels; RC file browser; listserver link (→ §6.5); optional NPC-server process | [src] (server-notes/01-lineage.md#what-changed-between-eras) |
| a Python rewrite of gs2emu, also called Ash | same on-disk layout and wire protocol; generations 3 to 5, client, RC and NPC-server logins, listserver link, accounts, levels with baddies, RC file browser, gmaps, baddies, NPC-server relay; no horses, no weapon bytecode; default port 14812 | [src] (server-notes/01-lineage.md#what-changed-between-eras); [src] (server-notes/ash-overview.md#what-ash-implements) |

Two different projects carry the name Ash (→ App. E#400).

### 5.3.2 Login and receive path

The rules below give how GServer-v2 reads a frame and a login, and how the login type picks the generation [src] (server-notes/03-protocol.md#protocol).

| Rule | Source |
| --- | --- |
| Every multi-byte integer on the player socket is big-endian; frames are `u16be` length + payload | [src] (server-notes/03-protocol.md#protocol) |
| The login line is `c type`, `c key` (clients, and RC when the generation is above 3), 8 version bytes, `str account`, `str password`; an NPC-server adds a `s` listen port | [src] (server-notes/03-protocol.md#login-blob-first-line-after-zlib) |
| `type = 1 << value`; the type chooses the generation (client type 0 → 3, type 4 → 4, type 5 and RC2 → 5) and the full type table is in → §2.3.6.1 | [src] (server-notes/04-algorithms.md#5-login) |
| The key resets both iterators; the start value per generation is `0, 0, 0x04A80B38, 0x04A80B38, 0x04A80B38, 0` and the limit is −1 (→ §2.2) | [src] (server-notes/04-algorithms.md#1-lcg-step) |
| Inbound generation 1 is plain, 2 and 3 are zlib, 4 and 5 are XOR then decompress; a generation-3 client line has its inserted byte removed before the id is read; the server's outbound generation 3 inserts nothing | [src] (server-notes/04-algorithms.md#4-inbound-frame); [src] (server-notes/04-algorithms.md#2-gen-3-dummy-byte-client--server-packets-only) |
| Login checks, in order: version in `allowedversions` (→ §5.4.2), IP ban, RC account on the staff list, NPC-server password; then the server asks the listserver with `SVO_VERIACC2` and continues when the answer comes (→ §6.5) | [src] (server-notes/04-algorithms.md#5-login) |
| An NPC-server login is answered with the NC maps, levels and weapons | [src] (server-notes/04-algorithms.md#5-login) |
| A trailing identity string (`win`, hardware ids, OS) is read and forwarded to the listserver | [src] (server-notes/lab-servers-2026-10-30.md#what-our-gserver-does-with-each-client-generation-src) |

### 5.3.3 What real clients require of a server

These rules come from running real clients against GServer-v2 builds and fixing what they refused; each is a client requirement, not a server choice [lab] (tools/lab-servers/README.md#our-beta4-gserver-2026-10-30).

| Requirement | Clients | Source |
| --- | --- | --- |
| Send `PLO_SETACTIVELEVEL` (156) during the level load; without it the client waits on the loading screen | 2.05 (and every Original-type client from 2.01 in the lab fix) | [src][lab] (server-notes/lab-servers-2026-10-30.md#2-gserver-v2-beta4-against-our-build); [lab] (tools/lab-servers/README.md#our-beta4-gserver-2026-10-30) |
| Send the first `PLO_LEVELNAME` before the board; after it, the client stays on the loading screen | 2.05 | [lab] (tools/lab-servers/README.md#our-beta4-gserver-2026-10-30) |
| Read the rest of the login frame: the client sends `PLI_LANGUAGE` in the same frame as the login line, and dropping it leaves the generation-3 iterator one step behind for the whole session ("Invalid PlayerProp" on 2.17.1) | 2.05, 2.17.1 | [lab] (tools/lab-servers/README.md#our-beta4-gserver-2026-10-30) |
| Treat a lone `PLI_PACKETCOUNT` (31) as an ordinary message: these clients send one every 10 s, and a server that reads the next frame as a login kicks them | 1.33 to 1.39, and any 2.x client that sends 31 alone | [lab] (tools/lab-servers/README.md#133-to-139-on-beta4-2026-10-30) |
| Accept id 25 (the client's weapon upload) | 1.33 to 1.37 | [lab] (tools/lab-servers/README.md#133-to-139-on-beta4-2026-10-30) |
| Send prop 10 in the bow form, not as a gani | 1.33 to 1.39 | [lab] (tools/lab-servers/README.md#133-to-139-on-beta4-2026-10-30) |
| Do not save the hidden status bit (`STATUS` 0x02) into the account; a client that quit hidden logs in invisible | 2.x (v4 lab) | [lab] (tools/lab-servers/README.md#our-beta4-gserver-2026-10-30) |
| Answer a 2.x client's zlib data error: 2.21 to 2.31 have a zlib bug on some chat; GServer-v2 either pads chat with a hidden clientside weapon (`-gr_zlib_fix`) or retries the frame as raw DEFLATE and rolls the generation-5 iterator back one step | 2.21 to 2.31 | [src] (server-notes/lab-servers-2026-10-30.md#2-gserver-v2-beta4-against-our-build) |
| A 5.24 client given the pre-2.1 file path saves PNG data as a file name and never gets files over 64000 bytes; with its own version slot it gets the modification time and the large-file messages | 5.24r4 | [cap] (tools/lab-servers/README.md#524-in-gs2libs-version-table-2026-10-31) |

Real 2.05 rev 2, 2.17.1 and 2.22 reach the game and walk on a GServer-v2 build with these fixes, and real 1.33 to 1.39 play on its classic server [lab] (tools/lab-servers/README.md#tests-run-2026-10-30).

### 5.3.4 Version-dependent paths

GServer-v2 serves clients differently by version. Each row gives a path that depends on the version id and the rule behind it [src] (tools/lab-servers/README.md#524-in-gs2libs-version-table-2026-10-31).

| Path | Rule | Source |
| --- | --- | --- |
| version id | the token is looked up in a table; the position in the table is the version id, and comparisons are by id | [src] (tools/lab-servers/README.md#524-in-gs2libs-version-table-2026-10-31) |
| unknown token | an unknown token allowed by config gets id 0, sorts below everything, and is served every pre-2.1 path | [src] (server-notes/lab-servers-2026-10-30.md#what-our-gserver-does-with-each-client-generation-src) |
| level send below 2.1 | the older GServer-v2 master sends a separate 1.41 level sequence with no 156; the newer branch has one level path for every version | [src] (server-notes/lab-servers-2026-10-30.md#2-gserver-v2-beta4-against-our-build) |
| default files | `PLI_UPDATEFILE` for a hard-coded list (`idle.gani`, `walk.gani`, `sword?.png`, `body.png`, the stock sounds, `pics1.png` and others) is answered "up to date" without checking times; `PLI_WANTFILE` has no such shortcut | [src] (server-notes/lab-servers-2026-10-30.md#what-our-gserver-does-with-each-client-generation-src) |
| default file to a pre-2.1 client | one build answers `PLO_FILEUPTODATE` (45), the other `PLO_FILESENDFAILED` (30); 2.05 accepts either | [lab] (server-notes/lab-servers-2026-10-30.md#beta4-built-and-run-against-real-clients-lab) |
| player class | chosen from the login type byte (type 0 is the Original class that 2.05 and 2.17 use), not from version config | [src] (server-notes/lab-servers-2026-10-30.md#beta4-built-and-run-against-real-clients-lab) |
| `generation` setting | server-wide; changes props, baddies, items and NPC details; 1.x clients need `classic`, and 2.x clients on a `classic` server get mangled packets | [src][lab] (server-notes/lab-servers-2026-10-30.md#beta4-built-and-run-against-real-clients-lab); [lab] (tools/lab-servers/README.md#133-to-139-on-beta4-2026-10-30) |

### 5.3.5 Wire encodings the server writes

Each row gives one encoding the server writes and its limits. A client author can check a decoder against these [src] (server-notes/03-protocol.md#g-integers-cstring-writeg).

| Item | Rule | Source |
| --- | --- | --- |
| G-integers | `c` up to 223, `s` up to 12255, `i3` up to 1 568 735, `i4`, and `i5` for file size and time (→ §2.1.1) | [src] (server-notes/03-protocol.md#g-integers-cstring-writeg) |
| Pascal string | `c` length + raw bytes (the text is not offset) | [src] (server-notes/03-protocol.md#g-integers-cstring-writeg) |
| board | `PLO_RAWDATA` with `i3` 8194, then `PLO_BOARDPACKET` and 8192 raw tile bytes (64 × 64 `u16`) | [src] (server-notes/03-protocol.md#level-board) |
| file (2.1+) | `PLO_RAWDATA` with the total, then `PLO_FILE`: `i5` time, `c` name length, name, bytes (→ §2.7) | [src] (server-notes/03-protocol.md#file-send-21) |
| props | the prop encodings are in → §2.6 | [src] (server-notes/03-protocol.md#player-props) |

### 5.3.6 Word filter

`rules.txt` is a word filter. The table gives its file, its header and the fields of a rule [srv] (client-internals/feature-specs/12-motd-rules.md#rules-in-gserver).

| Item | Rule | Source |
| --- | --- | --- |
| file | `config/rules.txt` is the word filter, not a rules text players see | [srv] (client-internals/feature-specs/12-motd-rules.md#rules-in-gserver) |
| header | optional `WARNMESSAGE` and `SHOWWORDSTORC`, then `RULE` … `RULEEND` blocks | [srv] (client-internals/feature-specs/12-motd-rules.md#rules-in-gserver) |
| rule fields | `CHECK` (pm, chat, nick, toall), `MATCH` (`?` is a wildcard), `PRECISION` (number or percent), `WORDPOSITION` (full, start, part), `ACTION` (log, tellrc, replace, warn, jail, ban), optional per-rule `WARNMESSAGE` | [srv] (client-internals/feature-specs/12-motd-rules.md#rules-in-gserver) |
| applied to | chat (prop 12), PMs, toall and nickname changes | [srv] (client-internals/feature-specs/12-motd-rules.md#rules-in-gserver) |
| actions | `replace` swaps the matched letters for `*`; `warn` replaces the whole message with the warn text; `log` and `tellrc` go to the server log and RCs; `jail` and `ban` are stubs and do nothing | [srv] (client-internals/feature-specs/12-motd-rules.md#rules-in-gserver) |
| chat echo | when a chat line was changed, the server sends the new CURCHAT back to the sender so its own bubble shows the filtered text | [srv] (client-internals/feature-specs/12-motd-rules.md#rules-in-gserver) |

### 5.3.7 Board respawn

GServer-v2 respawns board changes on its own terms. The rules below give which changes respawn, after how long, and how a new change clears old ones [src] (client-internals/board-respawn.md#gserver-v2-lab-server-src).

| Rule | Source |
| --- | --- |
| A change respawns only when its top-left tile before the change is one of 11 listed ids (bush, tall grass, pot, sign, stone, black stone and five others); otherwise it is kept with no timeout | [src] (client-internals/board-respawn.md#gserver-v2-lab-server-src) |
| A change of any size can respawn, after exactly `respawntime` (default 15 s) | [src][cap] (client-internals/board-respawn.md#summary) |
| A new change deletes stored changes it fully covers | [src] (client-internals/board-respawn.md#gserver-v2-lab-server-src) |
| The change is relayed to the whole level, sender included | [cap] (client-internals/board-respawn.md#summary) |
| Restore swaps old and new tiles and keeps the record, so late joiners get the restored state | [src] (client-internals/board-respawn.md#gserver-v2-lab-server-src) |
| Drops, for clients at the 2.1 slot or above: bush, grass or swamp tiles with `bushitems` drop item `rand() % 6` `tiledroprate` % of the time (default 50); a pot with `vasesdrop` drops a heart | [src] (client-internals/board-respawn.md#gserver-v2-lab-server-src) |
| With `clientsidepushpull` on, a 4 × 4 change of a push-pull stone is refused and the board is sent back | [src] (client-internals/board-respawn.md#gserver-v2-lab-server-src) |
| The real 2.x GServer's timer, tile list and drop rates are unknown; no 2000–2002 official server binary has been found | [doc] (client-internals/board-respawn.md#open) |

The 1.42 release moved bush and pot drops to the server [doc][bin] (client-internals/board-respawn.md#item-drops-from-142-on-server-side).

## 5.4 Accounts and allowed versions

### 5.4.1 Account stores

Servers keep accounts in different files. Each row gives a server, a file or field, and its layout [src] (tools/classic-tools/gserverstat.md#what-it-reads).

| Server | Store | Layout | Source |
| --- | --- | --- | --- |
| 1999 gserver tree | `accountslist.txt`, one account per line | `str` name, `str` password, a flag byte, a 3-byte file number | [src] (tools/classic-tools/gserverstat.md#what-it-reads) |
| 1999 gserver tree | flag byte | bit 0 only-load, bits 1–3 admin level, bit 4 blocked | [src] (tools/classic-tools/gserverstat.md#what-it-reads) |
| 1999 gserver tree | `accounts/accN.txt` | name, password, a prop list (`id + 32` and a value), the flag byte, two zero counts, weapons, action flags, opened chests | [src] (tools/classic-tools/gserverstat.md#what-it-reads) |
| 1999 gserver tree | `accounts.txt` | read if present, imported, then removed | [src][bin] (tools/classic-tools/gserverstat.md#what-it-reads) |
| GServer 1.39 with MySQL | `accounts` table | `accname`, `encrpass` (traditional DES `crypt`), `email`, `blocked`, `onlyload`, `adminlevel`, `adminworlds`, `lastused` | [src][bin] (tools/server-tools-2001.md#gserver-139-web-scripts-2001) |
| gs2emu / GServer-v2 | `GRACC001` files | text account files | [src] (server-notes/01-lineage.md#what-changed-between-eras) |

The rules below record what the 1999 and 1.39 servers did with account data: stat pages, count files and the chat commands players could use [src][bin] (tools/classic-tools/gserverstat.md#what-it-reads).

| Account rule | Source |
| --- | --- |
| The 1999 stat pages rank accounts by props 0 (nickname), 1 (max hearts), 3 (rupees, three 7-bit bytes), 27 (kills), 28 (deaths), 29 (online seconds) and 32 (alignment), and skip only-load accounts | [src][bin] (tools/classic-tools/gserverstat.md#what-it-reads) |
| GServer 1.39 servers wrote `playercount.txt`, `accountcount.txt`, `serveruptime.txt` and top lists as `nickname:value` lines for web pages | [src] (tools/server-tools-2001.md#gserver-139-web-scripts-2001) |
| The 1.39 chat commands listed for players: `sethead`, `setsword`, `setshield`, `setnick`, `showname`, `showap`, `showdeaths`, `showkills`, `showonlinetime`, `showguild`, `showadmins`, `unstuck me`, `toguild:`, `toall:` | [src] (tools/server-tools-2001.md#gserver-139-web-scripts-2001) |
| GServer-v2's stock default account has `MAXHP 3.00`, which its loader reads as 0 hearts | [lab] (tools/lab-servers/README.md#133-to-139-on-beta4-2026-10-30) |

### 5.4.2 Allowed versions

The 1999 servers accept a fixed list of `GSERV` tokens with a minimum per connection type (→ §2.3.2). GServer-v2 reads the list from a file:

| Rule | Source |
| --- | --- |
| Each line of `config/allowedversions.txt` is a token or a range `A:B`; a range allows every token whose position in the version table lies between A's and B's, both included | [src] (server-notes/public-allowed-versions.md#how-the-server-builds-the-list-src) |
| A token not in the table gets id 0 and lies in no range; a bare unknown token on its own line also resolves to 0, and so admits every unknown token | [src] (server-notes/public-allowed-versions.md#how-the-server-builds-the-list-src); [src] (tools/lab-servers/README.md#524-in-gs2libs-version-table-2026-10-31) |
| The refusal is "Your client version is not allowed on this server." followed by "Allowed:" and the list, each token printed by its table name and a range as `A - B` | [cap][src] (server-notes/public-allowed-versions.md#the-refusals-on-record) |
| A server prints its list only to a client it refuses | [inf] (server-notes/public-allowed-versions.md#open) |
| The stock file of the older master enables only `GNW03014` (2.22) | [src] (server-notes/public-allowed-versions.md#how-the-server-builds-the-list-src) |
| The newer branch groups ranges by `generation`: `classic` = 1.41r1 only, `newmain` = 2.22 to 2.31, `modern` = 5.12 to 6.037; stock, it refuses 2.05 and 2.17 | [src] (server-notes/lab-servers-2026-10-30.md#beta4-built-and-run-against-real-clients-lab); [src] (tools/lab-servers/README.md#524-in-gs2libs-version-table-2026-10-31) |
| The listserver does not check the version; whether a build gets in is up to each game server's list | [cap] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x) |

A server lets a client in only if its token is on the allowed list. The table maps each late token to its build and the name the version table gives it [src] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x).

| Token | Build | Name in the version table | Source |
| --- | --- | --- | --- |
| `G3D22067` | 5.00r7 | 5.07 | [src] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x) |
| `G3D14097` | 5.12 | 5.12 | [src] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x) |
| `G3D26090` | 5.30r3, 5.31r4, 6.00r2, 6.00r4 | 5.31x | [src] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x) |
| `G3D3007A` | 6.01x | 6.015 | [src] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x) |
| `G3D2505C` | 6.034, 6.035 | 6.034/6.035 | [src] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x) |
| `G3D0311C`, `G3D0511C` | 6.03r7 Windows, Linux | 6.037, 6.037 (Linux) | [src] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x) |
| `G3D15010` | 5.24r3, 5.24r4, 6.00 beta2 | not in the table | [src] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x) |
| `G3D03048` | 6.00 beta1 | not in the table | [src] (server-notes/public-allowed-versions.md#what-that-means-for-5x-and-6x) |
| `GNW03081` | 2.05 rev 2 | 2.05r2 (newer branch only) | [src] (server-notes/lab-servers-2026-10-30.md#2-gserver-v2-beta4-against-our-build) |

Public servers print their allowed list when they refuse a client. Each row gives one refusal, the token that was sent and the list printed back [cap] (server-notes/public-allowed-versions.md#the-refusals-on-record).

| Refusal seen from a public server | Client token sent | Allowed list printed | Source |
| --- | --- | --- | --- |
| a GServer-v2 server reporting 4.0.0 | `GNW14015` (2.3) | 2.22, 5.07 | [cap] (server-notes/public-allowed-versions.md#the-refusals-on-record) |
| a second server (signature 73) | `GNW03081` (2.05) | 2.22, and the range 1.41r1 to iPhone Belote 1.5 | [cap] (server-notes/public-allowed-versions.md#the-refusals-on-record) |

The second server refused 2.05 although `GNW03081` lies inside its printed range in the current version table (→ App. E#404). No 5.x or 6.x client has logged in to a public server [cap] (server-notes/public-allowed-versions.md#which-client-versions-public-reborn-game-servers-allow).

## 5.5 NPC server

### 5.5.1 The 2001 NPC server

The 2001 NPC server runs NPC scripts away from the game server. The rules below give how it connects, how its main loop runs and how it starts [doc] (tools/npcserver-2001.md#1-what-the-npc-server-is).

| Rule | Source |
| --- | --- |
| The NPC server is a separate program that logs into the GServer like a player and owns the NPCs of a configured set of levels | [doc] (tools/npcserver-2001.md#1-what-the-npc-server-is) |
| Its main loop runs every 0.1 s: read from the GServer, run all NPC scripts, push changed NPC and player attributes, then sleep; 0.1 s is the smallest useful server-side `sleep` | [doc] (tools/npcserver-2001.md#1-what-the-npc-server-is) |
| Startup: load options, connect to the GServer, then (if connected) load the level list, then load NPCs from its database | [doc] (tools/npcserver-2001.md#1-what-the-npc-server-is) |
| From the GServer it receives player attributes, temporary level state (bombs, explosions, bush removal, dropped items), PMs, game time, levels to reload, and `server.` flag changes; the GServer decides what reaches clients | [doc] (tools/npcserver-2001.md#1-what-the-npc-server-is) |
| To the GServer it sends NPC props, player props changed by scripts, PM replies, weapon grants and warps | [inf][doc] (tools/npcserver-2001.md#implied-gserver-link-inference-needs-a-capture-to-confirm) |
| The packet ids and port of the GServer–NPC-server link are unmeasured | [doc] (tools/npcserver-2001.md#open-questions) |
| Scripts run on the server by default; `//#CLIENTSIDE` splits a script, and the part after it is sent to clients | [doc] (tools/npcserver-2001.md#2-server-side-scripting-model) |
| Server-only events: `created`, `initialized`, `playerenters`, `playerleaves` (not on disconnect), `playertouchsme` (needs `setshape`), `playerchats`, `npcwarped`, `exploded` | [doc] (tools/npcserver-2001.md#2-server-side-scripting-model) |
| The server never loads images, so `setshape 1,w,h` gives an NPC its touch rectangle | [doc] (tools/npcserver-2001.md#3-commands) |

Variable names carry their scope in a prefix. Each row gives one prefix, what it is scoped to and whether it is saved [doc] (tools/npcserver-2001.md#4-variables-and-flags).

| Variable | Scope | Persisted | Source |
| --- | --- | --- | --- |
| `name` | current script or class | no | [doc] (tools/npcserver-2001.md#4-variables-and-flags) |
| `this.name` | current NPC | yes, for database NPCs | [doc] (tools/npcserver-2001.md#4-variables-and-flags) |
| `level.name` | the NPC's level | no | [doc] (tools/npcserver-2001.md#4-variables-and-flags) |
| `server.name` (number) | this NPC server only | no | [doc] (tools/npcserver-2001.md#4-variables-and-flags) |
| flags | current player | yes, in the account | [doc] (tools/npcserver-2001.md#4-variables-and-flags) |
| `client.` flags | current player, also sent to the client, which can change them | yes | [doc] (tools/npcserver-2001.md#4-variables-and-flags) |
| `this.` flags | current NPC | yes, for database NPCs | [doc] (tools/npcserver-2001.md#4-variables-and-flags) |
| `server.` flags | world-wide, shared with other NPC servers of the world, never sent to players | yes | [doc] (tools/npcserver-2001.md#4-variables-and-flags) |

The NPC server's commands fall into groups. Each row gives a group and its commands [doc] (tools/npcserver-2001.md#3-commands).

| Command group | Commands | Source |
| --- | --- | --- |
| flow and core | `destroy`, `if`, `while`, `for`, `break`, `continue`, `sleep`, `set`, `unset`, `setstring`, `message` | [doc] (tools/npcserver-2001.md#3-commands) |
| NPC appearance and state | `setgif`/`setimg`, `setgifpart`/`setimgpart`, `setshape`, `drawoverplayer`, `drawunderplayer`, `dontblock`, `blockagain`, `show`, `hide`, `noplayeronwall`, `showcharacter`, `setcharprop`, `setcharani`, `setchargender`, `putbomb`, `putexplosion`, `putexplosion2`, `setarray` | [doc] (tools/npcserver-2001.md#3-commands) |
| server-side additions | `canwarp`, `canwarp2`, `cannotwarp`, `callnpc`, `with (players[i])`, `with (getplayer(acct))`, `with (npcs[i])`, `with (getnpcs(name))`, `join`, `warpto`, `tokenize`, `tokenize2` | [doc] (tools/npcserver-2001.md#3-commands) |
| acting on the current player | `setplayerprop`, `setani`, `setgender`, `say`, `enableweapons`, `disableweapons`, `toweapons`, `addweapon`, `removeweapon`, `setlevel2`, `freezeplayer2`, `unfreezeplayer` | [doc] (tools/npcserver-2001.md#3-commands) |
| string helpers | `strlen`, `startswith(part,str)`, `indexof(part,str)` (−1 if absent), `#e(start,len,str)`, `#T(str)` (trim), `tokenscount`, `#t(i)` | [doc] (tools/npcserver-2001.md#3-commands) |

Some commands exist only on the NPC server. Each row gives one and its rule [doc] (tools/npcserver-2001.md#3-commands).

| Command | Rule | Source |
| --- | --- | --- |
| `noplayeronwall` | `onwall` and `onwall2` stop counting players on this NPC | [doc] (tools/npcserver-2001.md#3-commands) |
| `canwarp` | database NPCs only; the NPC warps through links exactly as a player would | [doc] (tools/npcserver-2001.md#3-commands) |
| `canwarp2` | database NPCs only; for wandering overworld NPCs: normal links, checks `onwall` at the destination, refuses small links such as house doors | [doc] (tools/npcserver-2001.md#3-commands) |
| `with` | swaps the current player or NPC for the block; commands are skipped if the target does not exist; local variables still resolve to the caller; `sleep`, `break` and `continue` inside the block leave the swapped context in place | [doc] (tools/npcserver-2001.md#3-commands) |
| `join class` | loads `class.txt` from the scripts folder; an NPC holds its own script then each joined class; a class loaded by another NPC is shared, so updating it updates every member; later scripts can override functions | [doc] (tools/npcserver-2001.md#3-commands) |
| `warpto` | moves the NPC to another level; database NPCs only | [doc] (tools/npcserver-2001.md#3-commands) |
| `addweapon` | like `toweapons`, but the weapon script comes from the database and the weapon must already exist | [doc] (tools/npcserver-2001.md#3-commands) |
| `tokenize`, `tokenize2` | `tokenize` splits on spaces and commas; `tokenize2` adds extra delimiters | [doc] (tools/npcserver-2001.md#3-commands) |

Client support for these commands per build is in → §8.1 and → §8.2; the PM admin interface and the NC socket that replaced it are in → §7.3.

### 5.5.2 Message codes on a script-running server

On a server that runs scripts, message codes are expanded before use. The rules below give how `#n` is expanded in `setcharprop` and what it changes [srv] (server-notes/setcharprop-hash-n.md#answer).

| Rule | Source |
| --- | --- |
| In a `setcharprop` value, `#n` expands to the nickname of the player who triggered the script; `#n(id)` picks another player by id | [srv] (server-notes/setcharprop-hash-n.md#answer) |
| `setcharprop` always expands its second argument before applying it | [srv] (server-notes/setcharprop-hash-n.md#2-server-side-gs1-gserversource-archive) |
| When the first argument is `#n`, the expanded text becomes the NPC's nickname and its `showcharacter` nickname, and the NPC nickname prop is marked for sending | [srv] (server-notes/setcharprop-hash-n.md#2-server-side-gs1-gserversource-archive) |
| `#F` is the current player's level name, which can differ from `#L` (the NPC's level) | [doc] (tools/npcserver-2001.md#6-message-codes) |
| A capture that proves the server-side `#n` expansion on a script-running server is still open | [inf] (server-notes/setcharprop-hash-n.md#still-open) |

### 5.5.3 Later NPC servers

Later servers handle NPCs in their own ways. Each row gives one server and how it runs NPC scripts [src] (server-notes/lab-servers-2026-10-30.md#2-gserver-v2-beta4-against-our-build).

| Server | Rule | Source |
| --- | --- | --- |
| GServer-v2, newer branch | adds a GS1 NPC server, tested on the 2.x generation; the V8 GS2 NPC server stays optional | [src] (server-notes/lab-servers-2026-10-30.md#2-gserver-v2-beta4-against-our-build) |
| GServer-v2, newer branch, own notes | 1.38 to 1.411 and the 2.x/3.x generation are supported client-authoritative; clientside GS1 works up to 5.007; server-side GS2 is not supported | [src] (server-notes/lab-servers-2026-10-30.md#2-gserver-v2-beta4-against-our-build) |
| the Python gs2emu rewrite | announces the NPC server to clients and relays the address query (→ §7.2) | [src] (server-notes/ash-overview.md#what-ash-implements) |
| any GS1 NPC server | the 2.22 built-in baddies can run as server-owned NPCs: one AI step per 0.1 s `timeout`, the client's probe points tested with `onwall`, touch damage with `hitplayer`, and ganis built from `arrays.dat`; a worked gray soldier is not yet tested live | [inf] (server-notes/baddies-serverside.md#the-step); [2.22] (client-internals/baddies-222.md#the-ai-step-222) |
