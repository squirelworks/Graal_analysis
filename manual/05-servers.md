<!-- manual: kind=reference status=draft -->
# 5 Game servers

This part describes the game servers that Graal clients talk to: the original 1999 GServer13, the 2006 39ster 2.1 remake, and GServer-v2 as the reference for later behaviour. Login frames are in → §2.3, ciphers in → §2.2, and the reply sequence after a good login in → §2.3.6. The listserver is in → §6, RC and NC in → §7.

> Status: draft. The newest server of the original line in the archive is the 1.39 family (a 2002 Windows build and 2003–2005 rebuilds of the 1.39 tree, → §5.1.7). No official 2.x GServer binary is in the archive, so the 2.x-era server rules here come from GServer-v2 and the 39ster remake, not from an original server. The two 1999 servers were read in full in 2026-11 (→ §5.1.6).

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

GServer 1.28 beta 2 (`GServerv.exe`) and the October 1999 GServer have `respawntime`, `horselifetime` and `baddyrespawntime`, but `pktimeout` ("Playerkiller flag timeout in sec") in place of `apincrementtime`: player-killer flags came before alignment points [bin] (server-notes/original-server-builds-1999-2007.md#the-timer-options-bin). An RC of 2000 can set the same four timers over the wire (→ §7.1.4).

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

### 5.1.6 Game rules of GServer 1.28 beta 2 and 1.3

A 2026-11 static read of both 1999 servers gives their handling of each client message, their timers and their baddy and kill rules [bin] (server-notes/gserver-1999-rules.md). Where GServer-v2 differs, the 1999 rule is the original.

| Item | Rule | Source |
| --- | --- | --- |
| version gate | 1.3 knows `GSERV007` to `GSERV014` but refuses every build before 1.3; 1.28 beta 2 refuses builds before itself | [bin] (server-notes/gserver-1999-rules.md#the-two-builds) |
| board changes | only a 2×2 change grows back, after a random whole number of seconds from 0.75 to 1.25 × the respawn time (7.5 to 12.5 s by default); larger changes stay | [bin] (server-notes/gserver-1999-rules.md#client-messages) |
| horses | `PLI_HORSEADD` is kept for the horse lifetime and sent only to arrivals; then `PLO_HORSEDEL` to the level (9.5 to 9.8 s in a lab run) | [bin][lab] (server-notes/gserver-1999-rules.md#timers-once-a-second) |
| `PLI_TOALL` | to every other player online as `PLO_TOALL`, sender id first | [bin] (server-notes/gserver-1999-rules.md#client-messages) |
| baddy props | accepted only from the level's leader; a dead leader hands leadership to the next player | [bin] (server-notes/gserver-1999-rules.md#own-props) |
| not handled | bombs, arrows, thrown objects and floor items (4, 5, 9, 11, 12, 13), 24, 27 | [bin] (server-notes/gserver-1999-rules.md#client-messages) |
| prop limits | max hearts 20, gralats 9,999,999, arrows and bombs 99, alignment 0 to 100; sword 1–4 and shield 1–3 become stock images | [bin] (server-notes/gserver-1999-rules.md#own-props) |
| deaths | counted when status prop 18 gets the dead bit 8 | [bin] (server-notes/gserver-1999-rules.md#own-props) |
| alignment | +1 every 20 minutes online, up to 100 | [bin] (server-notes/gserver-1999-rules.md#timers-once-a-second) |
| baddy start modes | swamp soldier (4) mode 6, hare (5) mode 7; powers 2, 3, 4, 3, 2, 1, 1, 6, 12, 8 for types 0–9 | [bin] (server-notes/gserver-1999-rules.md#baddies) |
| kills (1.3) | count only when the victim has 10 AP or more; the killer loses (victim AP + 10) / 20, rounded half to even | [bin] (server-notes/gserver-1999-rules.md#kills-13) |
| private messages | a build too old to answer gets the sender "The player cannot answer because he/she has an older version." | [bin] (server-notes/gserver-1999-rules.md#client-messages) |

A lab run of the original `GServer13.exe` with real 1.3 test clients: 1.28 beta 2 is dropped at login with "You need at least Graal version 1.3 to play on this server."; on the wire, max hearts, hearts, arrows and bombs are corrected back to the sender (20, twice the max, 99, 99), alignment 120, sword 5 and shield 4 pass to the other player unchanged, and gralats over the limit, glove and bomb power get no reply and are not passed on [lab] (protocol/lab-appe-hostb-2026-11-20b.md#server-prop-limits-props-sent-by-a).


**Settled question, formerly E#423: The 1999 servers: what the static read left open.** How the original 1999 server sends players in other levels, which builds get the "cannot answer" reply, and its prop limits beyond the counted props were open after the static read. Lab runs of the original `GServer13.exe` with real 1.3 test clients settled them [lab] (protocol/lab-appe-hostb-2026-11-20c.md#level-change-and-other-level-props-on-gserver-13-e423).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | A level change is `PLI_LEVELWARP` (0), or `PLI_LEVELWARPMOD` (30) when the level is cached; the players left behind get prop 50 = 0 and the new level and position (props 20, 15, 16), with no nickname or head | [lab] (protocol/lab-appe-hostb-2026-11-20c.md#level-change-and-other-level-props-on-gserver-13-e423) |
| Settled | The nickname (0) and head (11) go to every player online, in every level; 1.3 sends the head as one byte, the head number. Colours, sword, chat and the UDP port go only to the same level. A player logging in gets, for a player in another level, only the nickname, head, position, level name, prop 30 and the UDP port | [lab] (protocol/lab-appe-hostb-2026-11-20c.md#level-change-and-other-level-props-on-gserver-13-e423) |
| Settled | 1.28 beta 2 is dropped right after login ("You need at least Graal version 1.3 to play on this server.") and the others get prop 51 for it, so no older build stays online to receive the "cannot answer" reply on this server | [lab] (protocol/lab-appe-hostb-2026-11-20b.md#an-older-build) |
| Settled | Prop limits: max hearts 20, power twice the max, arrows and bombs 99 are echoed to the sender; alignment is shown to others as at most 100, shield as at most 3, and sword 9 is kept; gralats, glove and bomb power over the limit get no reply | [lab] (protocol/lab-appe-hostb-2026-11-20c.md#level-change-and-other-level-props-on-gserver-13-e423); [lab] (protocol/lab-appe-hostb-2026-11-20b.md#server-prop-limits-props-sent-by-a) |
| Verdict | Verified on GServer13 with 1.3 test clients. The best guess (other-level players sent like same-level ones) is refuted: only the nickname and head cross levels | [lab] (protocol/lab-appe-hostb-2026-11-20c.md#level-change-and-other-level-props-on-gserver-13-e423) |
| Left over | The "cannot answer" reply has no reachable target on GServer13; GServer 1.28 beta 2 was not run in this way | [inf] (server-notes/gserver-1999-rules.md#not-known) |

### 5.1.7 Other servers of the original line

Besides GServer13 and GServer 1.28 beta 2, the archive holds an October 1999 GServer, a December 1999 Linux GServer with its source tree, a 2003 Windows port of GServer 1.34 rev 1, and the 1.39 family. Each row gives one rule that differs from GServer13 [bin][src] (server-notes/original-server-builds-1999-2007.md).

| Server | Rule | Source |
| --- | --- | --- |
| October 1999 | lets in 1.27 (`GSERV011`) and later; relays bombs, arrows, fire, thrown carry, items, NPC weapon images and explosions to the level, which 1.28 beta 2 and GServer13 drop | [bin] (server-notes/original-server-builds-1999-2007.md#bombs-arrows-and-items-relayed-dropped-relayed-again-binsrc) |
| December 1999 (Linux) | lets in `GSERV015` and later; relays the same effects again, but only to a peer that cannot get them over UDP; PMs over 1,024 bytes are refused; a non-admin in the levels `police2`, `police4` or `police5` (jail) cannot send to-all (6) or PMs (28) | [src] (server-notes/original-server-builds-1999-2007.md#the-december-1999-linux-server-src) |
| 1.34 rev 1 port | lets in `GNW27030` (1.34 rev 1) only; its token table also names the RC tokens `GSERV012` to `GSERV018` and the clients `GNW20020` (1.33), `GNW28020` (between 1.33 and 1.34, by its date a 1.33 revision [inf]) and `GNW22030` (1.34) | [bin] (server-notes/original-server-builds-1999-2007.md#what-the-server-token-tables-settle-binsrc) |
| 1.39 | lets in 1.38 rev 1, 1.39 and 1.39 rev 1 (`GNW02070`, `GNW07080`, `GNW12080`); accepts only 2 × 2 board changes from a fixed list of tile replacements; checks a client message count (31) and drops a client whose count is wrong | [src][bin] (server-notes/original-server-builds-1999-2007.md#the-139-server-family-srcbin) |
| 1.39 builds | none runs NPC scripts on the server: the NPC engine in the 1.39 tree is a build option that no surviving binary has on. The tree's NewWorld build option expects the client token `G2N29070` (Graal NewWorld 1.39) | [src][bin] (server-notes/original-server-builds-1999-2007.md#the-139-server-family-srcbin) |

Six community servers of 2007 to 2010 are not originals, but their token tables are binary evidence for client tokens. The gs2emu table pairs each token with a name, checked slot by slot: `G3D16053` 3.0, `G3D27063` 3.01, `G3D03014` 3.041, `G3D28095` 4.0211, `G3D09125` 4.034, `G3D17026` 4.042, `G3D26076` 4.110, `G3D20126` 4.208, `G3D22067` 5.07 and `G3D14097` 5.12; `G3D04048` and `G3D18010` (iPhone 1.1 and 1.5, in 2.3.1 only); `GSERV023` to `GSERV025` (RC 1.010, 1.1 and 2.0). It confirms the public-list names of every 2.x token (→ §2.3) [bin] (server-notes/original-server-builds-1999-2007.md).

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

The pinned newer fork consumes `newtilesets` (false by default) and `newtilesetlevels` (an empty list by default) in server tile-category selection. Terrain takes precedence; otherwise the fork's case-sensitive matcher or a literal level-name prefix selects the new-format category map, followed by the global Boolean, then classic fallback. These options select server categories; original-server equivalence and client rendering remain unverified [srv] (server-notes/tile-category-options-2026-11-21.md#settings-and-selection).

Coordinates at or above the level's upper dimensions and unavailable tiles return blocking before category lookup. The registered GS1 `tiletype` function reads that level category, with blocking fallback when no level exists. Its wall predicate recognizes throw-through, jump-stone and blocking categories; GS1 `onwall` and `onwall2` also have object/player checks. `playerswimming` samples the water/lava categories. Terrain category lookup returns nonblocking before the tile-id range check; other selections reject ids at or above 4096. No live setting-change or new runtime result is established [srv] (server-notes/tile-category-options-2026-11-21.md#concrete-consumers).

The pinned newer fork tracks `syncdistancex`/`syncdistancey` at 192 tiles each and `syncbydistanceinside` at false. Its numeric synchronization query uses inclusive independent axes, returns all members when both distances cover the dimensions, delegates bigmaps to data routing and bypasses numeric tests inside ordinary levels unless enabled. Entry/departure and ghost-refresh callers use this query; ordinary level-scoped property buffers instead use current-level or bounded 3-by-3 map-cell routing [srv] (server-notes/sync-distance-routing-2026-11-21.md#defaults-and-the-numeric-query).

`sendtonearbybigmaplevels` defaults true and gates cross-level sends in one nearby-send method, alongside the pre-2.01 client gate and temporary active-level wrapper. The ordinary-property helper does not apply that option gate. These are separate paths, not universal visibility controls. Advice to avoid distances below 64 is not an enforced predicate minimum; malformed-value defaults, live reannouncement and original/client agreement are not established here [srv] (server-notes/sync-distance-routing-2026-11-21.md#ordinary-data-routing-and-send-gates).

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

**Settled question, formerly E#400: Two projects called Ash.** Whether the two things the notes call Ash were one project or two was open. The repository owner settled it [doc] (server-notes/ash-identity-2026-11-20.md#statement).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: Ash is a Python rewrite of the gs2emu protocol (default port 14812). B: Ash is the blueprint pack of the 2006 39ster 2.1 GServer (default port 14822) | [src] (server-notes/01-lineage.md#what-is-binary--world-only); [src] (ash/INDEX.md); [src] (ash/ARCHIVAL-NOTE.md) |
| Settled | The repository owner states that Ash was an early attempt at working out how to reproduce Graal, and is not Graal. Both bodies of notes come from that one effort | [doc] (server-notes/ash-identity-2026-11-20.md#statement) |
| Verdict | Both claims describe parts of the same reproduction effort; the best guess of two unrelated projects is refuted. Neither is evidence of an original Graal program | [doc] (server-notes/ash-identity-2026-11-20.md#what-this-means-for-the-notes) |

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

#### Every client-to-server id at a GServer-v2 build

Our GServer-v2 lab build was sent every id 0–223 with an empty body from a live 6.03r7 session, then one baddy of each type [lab][srv] (protocol/probe-targets-2026-11-18.md#server-side-every-clientserver-id-at-our-gserver-v2-build).

| Rule | Source |
| --- | --- |
| It handles 0–41, 44, 46–48, 50, 80, 81, 130, 152, 154, 157–159, 161 and 223; every other id from 18 to 223 (168 ids) is unknown to it | [lab][srv] (protocol/probe-targets-2026-11-18.md#server-side-every-clientserver-id-at-our-gserver-v2-build) |
| Each unknown id is logged and counted; after three it sends `PLO_DISCMESSAGE` and drops the client, and 6.03r7 then logs in again by itself | [lab][srv] (protocol/probe-targets-2026-11-18.md#server-side-every-clientserver-id-at-our-gserver-v2-build) |
| Some handled ids do not check an empty body: 17 (`PLI_BADDYADD`) made a type-224 baddy that ended the 6.03r7 session; 31, 41 and 130 logged junk values | [lab][srv] (protocol/probe-targets-2026-11-18.md#server-side-every-clientserver-id-at-our-gserver-v2-build) |
| 39 (`PLI_TAMPERCHECK`) gets no reply and no log line (→ App. E#320) | [lab][srv] (protocol/probe-targets-2026-11-18.md#server-side-every-clientserver-id-at-our-gserver-v2-build) |
| 6.03r7 survives baddy types 0–24 and quits on 25 and 31; 4.20r8 and 2.22 survive every type up to 223. A server should keep to the named types 0–9 and never send a 6.x client a type above 24 | [lab] (protocol/probe-targets-2026-11-18.md#server-side-every-clientserver-id-at-our-gserver-v2-build) |

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

### 5.3.8 Refused logins, disconnects and clipped props

GServer-v2 checks a login in a fixed order and stops at the first check that fails. Each refusal has its own text. The tables below give the checks, the reasons it drops a player later, and how it clips the props a client sets [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv).

| Order | Check | Text the client gets | Source |
| ---: | --- | --- | --- |
| 1 | player limit (`maxplayers`) | "This server has reached its player limit." | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |
| 2 | IP ban: wildcard match against `config/ipbans.txt`, skipped for staff with the modify-staff right | "You have been banned from this server." | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |
| 3 | client version not in `allowedversions.txt` (ranges `a:b` allowed, → §5.4.2) | "Your client version is not allowed on this server." and a line with the allowed list | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |
| 4 | listserver down, or the listserver refused the login | "The login server is offline.  Try again later.", or the listserver's own text | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |
| 5 | account banned (`BANNED 1`, not for staff) | "You have been banned.  Reason: <BANREASON>" | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |
| 6 | `onlystaff` on, or the IP outside the account's `IPRANGE` | "This server is currently restricted to staff only." or "Your IP doesn't match one of the allowed IPs for this account." | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |
| 7 | account already online | if the old session has been idle 30 s or more, it gets "Someone else has logged into your account." and is dropped; otherwise the new login gets "Account is already in use." (compared without case) | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |
| 8 | no start level | "No level available." | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |

| Later disconnect | Text | Source |
| --- | --- | --- |
| idle, with `disconnectifnotmoved` and `maxnomovement` seconds | "You have been disconnected due to inactivity." | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |
| more than five unknown packet ids, or garbled props | "Disconnected for sending invalid packets." | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |
| RC kick | "One of the server administrators, <name>, has disconnected you", plus " for the following reason: <reason>" when one is given | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |
| RC ban by account | "<name> has banned you.  Reason: <reason>"; `BANNED` and `BANREASON` are saved to the account | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |
| RC account reset | "Your account was reset by <name>" | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |
| any, on 2.14 and later | `PLO_UPGRADEURL` (169) can go with the disconnect and turns Reconnect into an Upgrade button | [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv) |

The word filter's `ban` action is not implemented (→ §5.3.6) [srv] (client-internals/feature-specs/13-ban-kick.md#exact-server-behaviour-messages-in-the-order-they-can-happen-srv).

| Prop a client sets | Server clip | Source |
| --- | --- | --- |
| arrows, bombs | 0 to 99 | [srv] (client-internals/feature-specs/03-inventory.md#props-involved-self-stream-plprop-ids-srv) |
| rupees | at most 9,999,999 | [srv] (client-internals/feature-specs/03-inventory.md#props-involved-self-stream-plprop-ids-srv) |
| sword and shield power | `swordlimit` and `shieldlimit` (3 in the lab) | [srv] (client-internals/feature-specs/03-inventory.md#props-involved-self-stream-plprop-ids-srv) |
| bomb power, glove power | 0 to 3; at most 3 | [srv] (client-internals/feature-specs/03-inventory.md#props-involved-self-stream-plprop-ids-srv) |
| CURPOWER | cannot rise for a player under 40 AP | [srv] (client-internals/feature-specs/03-inventory.md#props-involved-self-stream-plprop-ids-srv) |

Built with the NPC-server option, some of these props become server-only; the lab server is built without it [srv] (client-internals/feature-specs/03-inventory.md#props-involved-self-stream-plprop-ids-srv).

### 5.3.9 Reference-fork ghost-mode configuration

The older documentation lead's unread-key count is a historical snapshot. At reference-fork source `0cf8f83d`, `ghostmodeenabled` and `ghostmodefornotstaff` are tracked Boolean keys with false defaults and concrete consumers. Disabled selects nobody; enabled with the non-staff restriction selects only non-staff; enabled without it selects everybody. Staff membership is checked against the server's staff list case-insensitively [srv] (server-notes/ghost-mode-options-2026-11-21.md#selection-policy).

Selected clients receive empty `PLO_GHOSTMODE` and `PLO_GHOSTTEXT` with the corner label "Ghost Mode" during login. Other-player properties append the `ghostani` GANI override without changing the stored own gani in that helper. Level entry sends `PLO_GHOSTICON` from the supplied level's eligible-client collection, with nearby refresh on entry and departure. The source routine returns without a disabling mode packet when the player is unselected. Existing test definitions cover tracked defaults, changed values, the eight policy combinations and the extension-free gani name; they were read, not executed in this audit. Original-server equivalence, client rendering/collision and live toggling remain separate questions, and G067's wider option inventory stays open [srv] (server-notes/ghost-mode-options-2026-11-21.md#concrete-consumers); [srv] (server-notes/ghost-mode-options-2026-11-21.md#validation-and-limits).

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
| object attributes | as in the client, plus `playerlastdead` (the last death or login time; Graal2001 only) | — | [doc] (tools/npcserver-2001.md#4-variables-and-flags) |
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

## 5.6 GServer-v2 under malformed and unusual input

The lab runs that fuzzed clients and staff tools through the open-source server also showed how that server handles levels and accounts it was not written for. The rules below are its behaviour as of the fork the labs used; they describe the reference server, not any original Graal server [srv][lab] (formats/gr-v105-fuzz-2026-11-19.md#the-lab-gserver-misreads-every-gr-v105-file-srvlab). The layer-count and malformed-link source defects were subsequently repaired in fork PR #118, commit `eea7a0b2`, retained at `4d1fb2f9`: width guards `C >= 2` through `C >= 5` now consume the requested byte count, `noexcept` filesystem lookups treat an uncheckable path as absent, and short NPC, chest and sign records are skipped. Existing generated regressions check cursor positions, a two-layer board, empty upper cells, an overlong link and short records. This source audit does not measure a new live serve; G226 and the live portion of G227 remain open [srv] (formats/gr-v105-fuzz-2026-11-19.md#source-repair-reconciled-on-2026-11-21-srv).

| Rule | Detail | Source |
| --- | --- | --- |
| `GR-V1.05` layer count | the loader reads the one-byte layer count with a packed-integer template whose width guards are written the wrong way round, so a one-byte read consumes five bytes and every board starts four bytes late; re-decoding with that skew reproduces every cell the server sent. Layer 1 then reaches the client as run-code garbage, an 8-layer level sends only 2 layers, and painted cells never arrive. The same call is used elsewhere in the file reader | [srv][lab] (formats/gr-v105-fuzz-2026-11-19.md#the-lab-gserver-misreads-every-gr-v105-file-srvlab) |
| `GR-V1.05` empty cells | the loader already turns an on-disk 4095 on layers above 0 into the wire's empty value (→ §3.1.2.11), for literal codes and both run kinds | [lab][srv] (formats/gr-v105-fuzz-2026-11-19.md#what-this-settles) |
| `GR-V1.05` heights | the binary loader reads the block only for 1.05; standalone loading does not establish a send. The fork has a conditional packet-185 gmap sender: seeded terrain, a map position and nonempty 81-value overrides are required; the entry path can skip board data for a current cache. Six GCHAR fields identify map cell, zero block start and dimensions-minus-one (8,8), then 81 row-major pairs encode whole height plus 50 and fraction times 128. Byte fields use the pinned GCHAR helper, not little-endian tile words. This is reference-fork source behavior, not original 5.12/6.03r7 acceptance | [srv] (formats/height-transport-scope-2026-11-21.md#reference-fork-storage-to-sender); [srv] (formats/height-transport-scope-2026-11-21.md#reference-fork-serialization) |
| server crash on a level | two synthetic levels (a layer count of 0, and 4095 on layer 0) end the server with an uncaught file-system exception, "File name too long": board bytes are read as a link line, and the existence check on that huge level name throws. A cut board, many short boards and a count byte of 255 do not crash it | [lab] (formats/gr-v105-fuzz-2026-11-19.md#two-levels-crash-the-lab-gserver-lab) |
| `PLI_LEVELWARP` (0) from a client | an injected 0 does not move the client, because the server sends no `PLO_PLAYERWARP` back; the lab moved players with a chat `warpto` and `warptoforall` on instead | [lab] (formats/gr-v105-fuzz-2026-11-19.md#method) |
| RC rights | an RC login needs the account's rights bitmask and an open IP range, not just a place on the staff list, or the server answers `You do not have RC rights.`; the flat-file account loader reads the bitmask from the `LOCALRIGHTS` key (there is no `ADMINRIGHTS` key) | [lab] (protocol/rc-fuzz-2026-11-19.md#setup); [lab] (protocol/rc-fuzz-2026-11-19.md#the-nc-socket-embedded-in-a-2002-rc) |
| NC address | the server answers `PLI_NPCSERVERQUERY` (94) with `PLO_NPCSERVERADDR` (79), about 9 ms later, only when the RC also holds the NPC-control right; builds from before a later change always check it, and a newer build with `npcrights=false` skips it | [lab] (protocol/rc-fuzz-2026-11-19.md#the-nc-socket-embedded-in-a-2002-rc) |
| 6.1.1.3 token | `GNP1905C` is not in the server's version catalogue (→ §2.10.8) | [lab][srv] (protocol/v6113-login-lab-2026-11-19.md#3-server-side-version-catalogue-gap-labsrv) |

The later positive native Linux 6.03r7 run used a world binary associated by its deployment record with source `01bb0b3f`, descended from repair PR #118. This is reported deployment provenance, not a reproduced build. A full 64 by 64 upper board delivered 64 cells of tile 332 and 4032 all-ones empty cells; an explicit hole delivered 63 and 4033, and RLE added 16 cells of tile 333 on layer 2. The patch, hole and additional RLE region are visible. Injected chat warps returned to the hub; walking a link was not measured. The packet-9 wait timed out after 60 seconds before the plan continued. Client-alive checks were positive, but no independent gameplay canary, 5.12 serve or malformed-file run was performed. G226 and the live portion of G227 remain open [lab] (formats/gr-v105-native603-2026-11-21.md#method-and-provenance); [lab] (formats/gr-v105-native603-2026-11-21.md#delivered-layers); [lab] (formats/gr-v105-native603-2026-11-21.md#limits-and-remaining-work).

The separate native Linux 6.03r7 follow-up tested a PLO_PLAYERPROPS (9) property-5 parser/HUD canary after each of three generated positive serves, with reset 1 and landed 99 references. All served canary regions matched the 99 reference; this is not an actual bomb-use test. The scorer used a bitmap-decoding port of the existing canary.py rule, not a successful original Python/Pillow invocation. Each advertised bottom return was then exercised by physical Down input, paired client PLI_LEVELWARPMOD (30) and server PLO_LEVELNAME (6) hub messages, and a drawn return frame. Ingress stayed chat warp and the last plan had no packet-9 wait timeout. Native-Windows behavior, the 5.24r4 Wine ambiguity and walking ingress remain open; G226/G227 are still partial [lab] (formats/gr-v105-served-canary-links-2026-11-21.md#independent-hudparser-canary); [lab] (formats/gr-v105-served-canary-links-2026-11-21.md#physical-return-through-advertised-links).

The separate Windows 5.12 run under Wine inside Debian used the same reported world deployment and positive fixtures. All three served parser/HUD canaries and physical bottom returns passed the retained scoring and request/response checks. The scorer region followed the game viewport rather than the desktop origin. No fresh full-board histogram, native-Windows run or rebuilt-binary proof is added [lab] (formats/gr-v105-served-canary-links-2026-11-21.md#windows-512-under-wine).

The 5.24r4-labelled Windows client under Wine remained able to return physically to the hub, but all three served-frame HUD/parser scores were unclear amid partial black repaint; the returned hub scores landed. Visible HUD digits alone are not a scorer pass, and repaint ambiguity does not establish parser failure [lab] (formats/gr-v105-served-canary-links-2026-11-21.md#retained-524r4-labelled-build-under-wine).
