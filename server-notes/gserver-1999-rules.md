# What the original 1999 servers do: GServer 1.28 beta 2 and 1.3

Date: 2026-11-13. Static reads of the two original servers in the archive, both written by the
original author: **GServer 1.28 beta 2** (23 November 1999, shipped with the 1.28 beta 2 client)
and **GServer 1.3** (29 November 1999, shipped with the 1.3 test client) **[bin]**. Their wire
protocol is in [../protocol/gserv-1999.md](../protocol/gserv-1999.md); this note is their game
rules. The rules are implemented, as plain behaviour, in squirelworks/seihai-gserver PR #109
(`docs/ORIGINAL-SERVERS.md`, `rules = 1999`) **[doc]**. No addresses or decompiled code.

Until now these servers had only been run in a loopback lab for a login and the start dialog
(→ [setcharprop-hash-n.md](setcharprop-hash-n.md)). Everything else the notes say about server
rules comes from GServer-v2, a later reimplementation.

## The two builds

Both are the same Delphi 4 tray program. 1.3 adds kill claims and alignment points; 1.28 beta 2
has neither. 1.3 knows the tokens `GSERV007` to `GSERV014` but turns every build before 1.3
away with "You need at least Graal version 1.3 to play on this server."; 1.28 beta 2 does the
same for builds before 1.28 beta 2 **[bin]**.

The start dialog (also `serverconfig.txt`) has five settings: the port (14804), the bush
respawn time (10 s), the horse lifetime (10 s), the alignment increment time (1200 s) and the
baddy respawn time (60 s). That is GServer13's set; 1.28 beta 2 has a player-killer flag timeout (`pktimeout`) in place of the alignment increment (`original-server-builds-1999-2007.md#the-timer-options-bin`). A one-second timer runs the game clock; each socket is read on a
second, faster timer **[bin]**.

## Client messages

| Message | What the 1999 servers do | Tag |
| --- | --- | --- |
| `PLI_LEVELWARP` (0), `PLI_LEVELWARPMOD` (30, 1.3 only) | leave the level, move, enter the new one | [bin] |
| `PLI_BOARDMODIFY` (1) | the tiles go into the server's copy of the board and to the others in the level (`PLO_BOARDMODIFY` 7). Only a 2×2 change grows back, after a random whole number of seconds from 0.75 to 1.25 times the respawn time (7.5 to 12.5 s by default); the old tiles then go to the level. Larger changes stay. A later arrival gets the board with the changes in it | [bin] |
| `PLI_PLAYERPROPS` (2) | applied with limits (below) | [bin] |
| `PLI_NPCPROPS` (3) | passed to the others in the level, then kept | [bin] |
| `PLI_TOALL` (6) | to every other player online as `PLO_TOALL` (13), the sender's id first | [bin] |
| `PLI_HORSEADD` (7) | `x*2, y*2, dir, image`; kept for the horse lifetime, replacing a horse on the same spot; **not** passed on at once, only to arrivals | [bin] |
| `PLI_HORSEDEL` (8) | the horse on that spot is removed; nobody is told | [bin] |
| `PLI_FIRESPY` (10) | read and dropped | [bin] |
| `PLI_CLAIMPKER` (14, 1.3 only) | one `GCHAR`, the killer's id (→ Kills) | [bin] |
| `PLI_BADDYPROPS` (15) | **only from the level's leader**; passed to the others in the level, then kept | [bin] |
| `PLI_BADDYHURT` (16) | to the leader as `PLO_BADDYHURT` (27) | [bin] |
| `PLI_BADDYADD` (17) | a baddy that does not come back | [bin] |
| `PLI_FLAGSET`, `PLI_FLAGDEL` (18, 19) | the account's flags | [bin] |
| `PLI_OPENCHEST` (20) | kept on the account | [bin] |
| `PLI_PUTNPC` (21), `PLI_NPCDEL` (22) | an NPC from a script file, sent to the level; removed | [bin] |
| `PLI_WANTFILE` (23) | the name with `.gif` added, from the server folder, if under 64,500 bytes; else "failed" (30) | [bin] |
| `PLI_WEAPONADD` (25), 29 | weapons on the account | [bin] |
| `PLI_PRIVATEMESSAGE` (28) | one `GCHAR` count, one `GCHAR` per id. A build too old to answer gets the sender "The player cannot answer because he/she has an older version." | [bin] |
| 51 to 64 | the RemoteControl's messages: accounts, disconnect, admin messages, player props | [bin] |

**Not handled at all:** `PLI_BOMBADD` (4), `PLI_BOMBDEL` (5), `PLI_ARROWADD` (9),
`PLI_THROWCARRIED` (11), `PLI_ITEMADD` (12), `PLI_ITEMDEL` (13), 24 and 27. These servers pass
on no bombs, arrows, thrown objects or floor items; later servers do **[bin]**.

## Own props

The server keeps every prop, limits some, and tells the client the value it kept
(`PLO_PLAYERPROPS` 9): max hearts 20, hearts up to the max (none taken while dead), gralats
9,999,999, arrows and bombs 99, alignment 0 to 100. Sword 1 to 4 and shield 1 to 3 become the
stock images **[bin]**.

- **Deaths.** When the status (prop 18) gets its dead bit (8), the death count rises by one.
- **A dead leader.** If the player who died leads the level (runs its baddies) and others are
  there, the next player becomes leader (`PLO_ISLEADER` 10) and the dead one goes to the back.
- **Carrying an NPC.** A second player claiming an NPC that someone already carries is refused.

The nickname and head go to every player online, in every level. Hearts, sword, shield,
colours, the carried NPC and alignment go to the level at once; position and sprite go out
batched **[bin]**.

## Timers, once a second

1. Cut bushes count down and grow back.
2. Horses count down the horse lifetime; the level then gets `PLO_HORSEDEL` (18) with the spot.
   A 1.3 lab run saw this at 9.5 to 9.8 s **[lab]**.
3. A baddy the leader set dead (mode 9) counts down the baddy respawn time and comes back at
   its spawn point with its type's power and start mode. There is no server step from dying
   (mode 5) to dead: the leader's client says mode 9.
4. Each player's time online rises, and every alignment increment time (20 minutes) their
   alignment rises by one, up to 100.

## Baddies

| Type | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Power | 2 | 3 | 4 | 3 | 2 | 1 | 1 | 6 | 12 | 8 |
| Start mode | 0 | 0 | 0 | 0 | 6 | 7 | 0 | 0 | 0 | 0 |
| Image | gray | blue | red | blue | gray | hare | octopus | gold | lizardon | dragon |

Powers and images match GServer-v2. The start modes do not: a swamp soldier (4) starts in mode 6
and a hare (5) in mode 7, for level baddies and when they come back; GServer-v2 starts every
type in mode 0 **[bin]**. Compare [baddies-serverside.md](baddies-serverside.md) and the client
side in [../client-internals/combat-baddy-tile-by-version.md](../client-internals/combat-baddy-tile-by-version.md).

## Kills (1.3)

A kill claim counts only when the **victim** has 10 alignment points or more. The killer then
loses `(victim's AP + 10) / 20`, rounded half to even (1 to 6 points), never below 0, and the
killer's kill count rises. A victim under 10 AP costs nothing and is not counted. GServer-v2
instead takes `2 * (1 + killer's AP / 20)` from every killer **[bin]**.

## Entering a level

The board (or nothing, when the client's copy is current), links, signs and the mod time; then
each chest, opened or not for this account; each horse (`PLO_HORSEADD` 17); each baddy; each
NPC; and the players there, both ways. The first player in leads. Players in other levels hear
the new level and position **[bin]**.

## Where GServer-v2 differs

| | 1999 servers | GServer-v2 |
| --- | --- | --- |
| horses | kept per level, sent to arrivals, removed after the lifetime | not handled |
| `PLI_TOALL` | to everyone else online | dropped |
| kill claims from 1.21 to 1.35 | one `GCHAR` id | read as a `GSHORT`, so dropped |
| deaths | counted from the dead bit | not counted |
| alignment | +1 per 20 minutes online, up to 100 | never rises |
| a leader's own mode 9 | starts the baddy respawn | stopped the baddy from coming back |
| bush regrowth | 0.75 to 1.25 × 10 s | 15 s |
| kill cost | the rule above | `2 * (1 + killer's AP / 20)` |
| a dead leader | hands off | stays leader |
| baddy props from a follower | dropped | kept |
| swamp soldier and hare start modes | 6 and 7 | 0 |

## Not known

- Which older builds get the private-message "cannot answer" reply.
- How the nickname and head of players in other levels are sent.
- The server-side prop limits beyond the counted ones.
- A real-client lab run of these rules (1.3 test client against a server running them) has not
  been done; it is tracked in squirelworks/seihai-gserver #110.
- No 2.x-era original server is in the archive.
