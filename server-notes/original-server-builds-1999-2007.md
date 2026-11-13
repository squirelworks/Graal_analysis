# Original and early-port GServer builds, 1999 to 2007

Date: 2026-11-13

This note covers nine server folders from the November 2026 disk hunt. They hold
the October 1999 Delphi GServer, the December 1999 Linux GServer and its C++ source tree, a
Windows port of GServer 1.34 rev 1, the 1.39 server family (Windows, Linux,
Matriark's rebuild and JustBurn's 1.39p1), the 39ster win32 GServer, and the
2001–2002 NPC Control and RemoteControl builds.

The binaries were read statically (pefile, capstone; strings, imports, PE resources and jump
tables); nothing was run. Where a source tree ships beside a binary, the source was read for
behaviour, and the binary was checked against it (token tables, messages, the message switch).
No code, addresses or file hashes are given here. Tags: **[bin]** read from the binary,
**[src]** read from the surviving source tree that matches a binary, **[inf]** inferred.

The two November 1999 servers (GServer 1.28 beta 2 and GServer13) are covered in
`seihai-gserver` `docs/ORIGINAL-SERVERS.md` and in `client-internals/board-respawn.md`. They
are used here as the baseline.

## The builds

| Build | Date | Toolchain | Tokens accepted | Players let in | Source |
|---|---|---|---|---|---|
| GServer2, October 1999 (with RemoteControl) | 1999-10-20 | Delphi | `GSERV007`–`GSERV011` | 1.27 and later ("You need at least Graal version 1.27 to play on this server.") | [bin] |
| GServer 1.28 beta 2 (baseline) | 1999-11-23 | Delphi | `GSERV007`–`GSERV013` | 1.28 beta 2 | [bin] |
| GServer13 (baseline) | 1999-11-29 | Delphi | `GSERV007`–`GSERV014` | 1.3 test | [bin] |
| Linux GServer, December 1999 | 1999-12 | g++ (Linux, not stripped) with a C++ source tree | `GSERV007`–`GSERV016` | `GSERV015` and later; RC from `GSERV011` | [src][bin] |
| GServer 1.34 rev 1, Windows port ("Ported by TTH") | built 2003-07-25 | MinGW g++ | `GSERV012`–`GSERV018`, `GNW20020`, `GNW28020`, `GNW22030`, `GNW27030` | 1.34 rev 1 only ("You need Graal version 1.34 rev1 to play on this server.") | [bin] |
| GServer 1.39, Windows (Matriark's MinGW cross-build of the 1.39 tree) | 2002-06-13 | MinGW g++ 2.95, MySQL client | `GSERV019`, `GNW02070`, `GNW07080`, `GNW12080` | 1.38 rev 1 to 1.39 rev 1; RC 2000/7/7 or later | [src][bin] |
| GServer 1.39, Linux (TTH) | 2003-07-30 | static g++, SQLite | as 1.39, plus `GSERV014` in the string table | as 1.39 | [bin] |
| Matriark GServer 1.3.9, Windows (two builds) | 2003-07-26, 2003-07-29 | MinGW g++, SQLite | as 1.39 Linux | "You need at least Graal version 1.28 beta 2 to play on this server." is also present | [bin] |
| JustBurn GServer 1.39p1 v1.1 (Windows, two Linux) | 2004-07 (Linux), 2005-07-19 (Windows) | Cygwin g++ / g++ | as 1.39 | as 1.39 | [src][bin] |
| 39ster win32 GServer | 2007-01-01 | Visual C++ 2005, `zlib1.dll` | none checked; the player record defaults its version field to the placeholder `GNW2005` | any | [src][bin] |

The Linux 1.39 binary of 2003 is the same file in the Linux package and in Matriark's folder
**[bin]**.

### What the server token tables settle **[bin][src]**

The servers' own token tables and refusal texts name builds whose tokens were known only from
public lists, or not at all:

| Token | Build, as the server names it | Evidence |
|---|---|---|
| `GSERV009`, `GSERV011` | 1.25 and 1.27 tokens exist in an original server's table; the October 1999 server lets in 1.27 (`GSERV011`) and later | October 1999 GServer **[bin]** |
| `GSERV019` | RemoteControl 2000/7/7 (the oldest RC the 1.39 server lets in) | 1.39 refusal text **[src][bin]** |
| `GNW28020` | between 1.33 (`GNW20020`, index 19) and 1.34 (`GNW22030`, index 21); by its date (28 Feb 2000) a 1.33 revision **[inf]** | 1.34 rev 1 port: index 20 **[bin]** |
| `GNW27030` | 1.34 rev 1 (27 Mar 2000): the only player token the 1.34 rev 1 port admits | 1.34 rev 1 port: index 22, refusal text **[bin]** |
| `GNW02070` | 1.38 rev 1 | 1.39 server: index 27, refusal text "1.38 rev1 - 1.39 rev 1" **[src][bin]** |
| `GNW07080` | 1.39 | 1.39 server: index 28 **[src][bin]** |
| `GNW12080` | 1.39 rev 1 (the build public lists call "1.391") | 1.39 server: index 29 **[src][bin]** |
| `G2N29070` | Graal NewWorld 1.39 | the 1.39 tree's NewWorld build option **[src]** |
| `G2NRC004` | NewWorld RC 2000/8/19 | the 1.39 tree's NewWorld build option **[src]** |

Version indexes 17 to 26 are not used by the 1.39 tree: it admits only 27 to 29 for players and
19 or later for RCs **[src]**.

## Client messages handled

Each row lists the client message ids that reach a handler, read from each server's message
switch. The baseline rows match `ORIGINAL-SERVERS.md`.

| Server | Ids handled | Source |
|---|---|---|
| October 1999 | 0–13, 15–29, 51–64 | [bin] |
| 1.28 beta 2 | 0–3, 6–8, 10, 15–23, 25, 26, 28, 29, 51–64 | [bin] |
| GServer13 | 0–3, 6–8, 10, 14–23, 25, 26, 28–30, 51–64 | [bin] |
| Linux, December 1999 | 0–30, 51–64 | [src] |
| 1.39 (Windows and Linux) | 0–24, 26–33, 55–58, 61–64, 67–82 | [src][bin] |

An id outside the switch disconnects the player on the 1.39 server, with id 16 "The server got
illegal data from your connection." **[src]**

### Bombs, arrows and items: relayed, dropped, relayed again **[bin][src]**

- **October 1999** relays the effects to every other player in the level. Bomb add 4 goes out as 11,
  bomb delete 5 as 12, arrow 9 as 19, fire 10 as 20, thrown carry 11 as 21 (sender id first),
  item add 12 as 22, item delete 13 as 23, NPC weapon image 24 as 32 (sender id first) and
  explosion 27 as 36. For item add, when the item is a sword or shield and the sender still
  has the starting sword 1 or shield 1, the sender's id is appended **[bin]**.
- **1.28 beta 2 and GServer13** drop all of these. The 1.28 beta 2 client sends them to the other
  players in the level over UDP, so the server does not relay them (`protocol/gserv-1999.md`) **[bin]**.
- **December 1999 and 1.39** relay them again, but only to a peer that cannot get them over UDP:
  the server skips the relay when both the sender and that peer have a UDP port set **[src]**.
  The 1.34 rev 1 port has a "Response socket" on port 14899 for the UDP side **[bin]**.

### The timer options **[bin]**

The October 1999 server and 1.28 beta 2 have **"Playerkiller flag timeout in sec"**
(`pktimeout`) where GServer13 has the alignment increment time (`apincrementtime`).
`client-internals/board-respawn.md` and manual §5.1.1 said 1.28 beta 2 has the same four keys
as GServer13. It does not: it has `respawntime`, `horselifetime`, `pktimeout` and
`baddyrespawntime`. The October 1999 package's `serverconfig.txt` sets `pktimeout=300` and
`baddyrespawntime=30`. Player-killer flags came before alignment points, and GServer13 replaced
them.

## The December 1999 Linux server **[src]**

This is a C++ port of the Delphi server, with the same class names and the same 1-second timer.
It is the server for the 1.31 era (it admits `GSERV015` and `GSERV016`). Compared with GServer13:

- **Login.** A player needs version index 15 or more ("You need at least Graal version 1.3 to
  play on this server."). An RC needs 11 or more. Refusals: "An account with the name and
  password you typed in does not exist.", "The account is already in use.", "The account has
  been disabled by an admin.", "Couldn't find the account file." The account named `Stefan` is
  always admin level 3.
- **Jail.** A non-admin in `police2`, `police4` or `police5` cannot send to-all (6) or PMs (28).
- **PMs (28).** One GCHAR count, that many GCHAR ids, then the text. If the sender's id plus the
  text is over 1,024 bytes, the sender gets 35 "Server message:" + `0xA7` + " Your message was
  too long." and nothing is sent. Otherwise each listed player online gets 37 with the sender's
  id and the text. A target with version index below 9 is not sent the message; instead the
  sender gets 37 with the target's id and `"Server message:","The player cannot read the
  message because he/she has an older Graal version."`. Login refuses those versions, so in
  practice this never happens.
- **Kill claim (14).** Sent by the player who was killed, with one GCHAR: the killer's id.
  Nothing happens unless the sender's AP is 10 or more. The killer, if their AP is above 0, loses
  `trunc((senderAP + 10) / 20)` (floor 0) and is told with 9, and their kill count goes up by
  one. This is GServer13's rule, with truncation where the Delphi build rounds.
- **Horses (7, 8).** Relayed to the level at once as 17 and 18, as well as kept. GServer13 relays
  neither.
- **Hurt player (26).** Sent only to the target, as 40 with the attacker's id first.
- **NPC weapon add (25).** Needs version index 15 or more and a weapon the server knows. It
  appends the weapon name to the player's list unless it is already there.
- **Props.** The clamps are the same as GServer13's (max hearts 20, rupees 9,999,999, arrows
  and bombs 99, MP 100, AP 0–100), and each corrected value is sent back as 9. Sword
  power above 4 is quietly set to 4. Colours are clamped to 0–18. X and Y are ignored while
  hearts are at 0 or below. A sprite of 132 or more becomes 0. An unknown prop index disconnects
  the player.
- **Idle.** A player who hasn't moved for 1,200 s is dropped with 16 "You have been
  disconnected because you didn't move."
- **Who hears a prop.** Nickname (0), head (11), colours (13) and the UDP port go as 8 to
  **every** player online. The nickname also goes to RCs as 59. A nickname written
  `Nick (Guild)` keeps the guild only if the guild list confirms it; otherwise the corrected
  nickname is sent back as 9. A head below 100 is `head<n>.gif`, and 100 + n is a named image.
  Either way it falls back to `head0.gif` when the server's `heads` folder lacks it.
- **Timers.** `baddyrespawntime` defaults to 120 s (GServer13: 60 s).

## The 1.39 server family **[src][bin]**

The 1.39 tree has a `gserver.cpp`, `levels.cpp`, `npcs.cpp` and a MySQL account store. It
reads and writes both `GLEVNW01` and `GSERVL01` level files. The Windows binary was linked
without `npcs` (it has none of the GS1 command names), and so were the 2003 Linux, Matriark and
JustBurn builds. **None of these binaries runs NPC scripts on the server.** Server-side NPCs are
a compile-time option (`SERVERSIDENPCS`) that no surviving build has switched on **[src][bin]**.
`server-notes/setcharprop-hash-n.md` therefore still lacks a pre-2.x Windows server that runs
`setcharprop`.

Rules that differ from GServer13:

| Area | 1.39 rule | Source |
|---|---|---|
| Board change (1) | Ignored unless it is in the level, at most 64 × 64, and **exactly 2 × 2**; each new tile must be a listed replacement of the tile underneath (a fixed list of 44 pairs, 11 objects × 4 tiles). Relayed as 7 to the rest of the level. At most 100 pending changes per level. Respawn after `trunc(0.75R + 0.5R·rand)` seconds, R = `respawntime` | [src] |
| Items on the floor (12, 13, 32) | An item add is stored for 20 s, at most 200 per level, and relayed as 22. Take item (32, new) checks a stored item of that kind at that spot and gives it to the taker. Green, blue and red rupees give +1, +5 and +30; 19 gives +100. Bombs (+5) and arrows (+5) are refused at 99, a heart at full hearts, and item 24 when status bit 64 is already set. The result is sent back as 9, and 23 goes to the rest of the level | [src] |
| Kill claim (14) | A **GSHORT** killer id (two bytes, not one GCHAR as in 1.3). Ignored when the killer has the same last IP as the sender or is not logged in. Otherwise as December 1999 | [src] |
| Message count (31, new) | The client reports how many messages it sent since the last report. A mismatch logs both counts and disconnects with 16 "The server got uncertified data packages from your connection."; a count over 10,000 is logged | [src] |
| Weapon add (33, new) | Type 0 adds a default weapon by item index (0–24). Type 1 adds the weapon of an NPC in the level (by its 3-byte id) that called `toweapons`, once per name | [src] |
| Jail warp | An RC warp (82) needs admin level 2 or more, rights in the target's world, and a lower level than the target (level 5 can warp anyone). It is the only way out of a jail level | [src] |
| Server flags (68, 69) | The RC reads and sets `server.` flags. Setting needs admin level 4 | [src] |
| Same account twice | If the old session has been idle for over 30 s it is saved and dropped with "Another client logged in using your account."; otherwise the new login gets "The account is already in use." | [src] |
| Idle | 1,200 s without action drops the player | [src] |
| Server messages | 41 start message, 42 NewWorld time, 43 default weapon. The RC set grows to 70–82 (direct account and profile edits, RC chat, warp) | [src] |

The 1.34 rev 1 port already has several 1.39 strings: the message-count check, "Another client
logged in using your account.", the idle drop ("You have been disconnected because you didn't
move."), guild messages, a 512 KB output cap and a 128 KB input cap **[bin]**. Its message
switch is compiled as compare chains, so its id set was not read; this is still open.

### Later rebuilds of 1.39

- **TTH's Linux 1.39 (2003) and Matriark's 1.3.9 (2003).** These use an SQLite account store with
  a `dbsetup` repair tool. They add top-10 stats queries (AP, deaths, online time, killers), and
  a staff `warpto x y level` chat command. `startmessage.rtf` is sent at login. The game port
  is 14900, and the response (UDP) socket is on the port below it. Matriark's notes list five
  known bugs. Heads, shields and swords are checked in their own folders but sent from `levels`.
  A guild member whose account name equals a nickname in the guild file needs a `*` prefix.
  An unexplained overflow of server flags and accounts is also listed **[doc][bin]**.
- **JustBurn 1.39p1 v1.1 (2004–05).** Same protocol and token table as 1.39. Accounts can be in
  MySQL or a text-file store (the default admin is `admin`/`admin`). Levels and images are found
  in any subfolder of `levels`, with a cached folder list. The idle drop is turned off.
  New RC chat commands: `/me`, `help->`, `subdirs->`, and `server->uptime`, `version`, `msg`
  and `shutdown` (off by default). New player chat commands: `setskin`, `setcoat`,
  `setsleeve`, `setshoe` and `setbelt`, with 20 named colours **[doc][src]**.

## The 39ster win32 GServer (2007) **[src][bin]**

The source in this folder is the tree that `ash/` describes: an 89-entry message table, port
14822, start level `level13.graal`, and the same descramble iterator start. The binary is the
Visual C++ 2005 build of that tree, so the `ash/` [src] rows now have a matching binary. Nothing
in it changes those notes.

## NPC Control and RemoteControl, 2001–2002 **[bin]**

| Build | Title date | Login token | Forms | What is new |
|---|---|---|---:|---|
| NPC Control | 2001/03/19 | `NCL15031` | 10 | the oldest NC: NPC list, add NPC, local NPCs, classes, add class, **server flag list**, warp |
| NPC Control | 2001/05/21 | `NCL15031` | 10 | same forms |
| NPC Control | 2001/07/13 | `NCL15031` | 10 | flag list replaced by a **weapons list** (the build already known; a second copy differs only in its PE header) |
| RemoteControl (NewWorld) | 2001/05/21 | `G2NRC006` | 15 | the 2001/01/27 main-server RC's forms, for NewWorld |
| RemoteControl (NewWorld) | 2001/08/20 | `G2NRC006` | 18 | rights, comments, local ban, as in the main-server 2001/08/20 RC |
| RemoteControl | 2002/01/11 | `GSERV023`, NC `NCL11012` | 27 | NPC Control, server list, file browser and short-message popup already built in |

So NPC Control was a separate program from March 2001. `tools/npc-control.md` names RC 1.41
(2002/05/02) as the first build with NC inside it. The 2002/01/11 RC already has NC, `GSERV023`
and the 1.41 forms, four months earlier.

## Open

- The 1.34 rev 1 port's message-id set (compare chains, not a jump table).
- What `GNW28020` is (a 1.33 revision, by its date) needs a 1.33 rev 1 client.
- The RC 2002/01/11 send ids, against RC 1.41's.
- A lab login of 1.38 rev 1 / 1.39 / 1.39 rev 1 against the 1.39 Linux server (in a lab VM)
  would turn the token rows above into [cap].
