# Appendix E lab runs on lab host B, second batch (2026-11-20)

Date: 2026-11-20. Evidence: **[lab]**. Real Windows clients and the original 1999 server under Wine,
in the lab host B the Linux lab VM. Each run used its own network namespace with loopback only.
Login hosts the clients dial resolve to lab listeners there. The lab servers sat behind the `gen5probe`
proxy, so both directions were logged. Captures and screenshots stay in the lab. Probe rows are appended
to [`probe-results.tsv`](probe-results.tsv). The first batch is in
[`lab-appe-hostb-2026-11-20.md`](lab-appe-hostb-2026-11-20.md).

## Login of the 1.40 build (E#15)

Build: 1.40 (`GNW23090`, FileVersion 1.3.9.1, shipped 2000-09-24). World: the npcdemo lab world on
the GServer-v2 fork, with `GNW23090` added to its allowed versions.

- The start form has a language list, a mode list (One Player, One Player Online, Two, Three and
  Four Players), a head list, and one text field for the account. The labels beside them do not line
  up under Wine. There is no host or port field.
- One Player Online + Start opens a "Server List" window. It asks for the list on port **14910** of
  its built-in list host. 1.41 rev 1 asks on 14923. The client sends nothing on that connection; it
  waits for the list.
- Picking the server and Connect logs in with type 0, generation 3, token `GNW23090`, the account
  and the password.
- The server answers the classic way: a level name and one full board. The client draws the level
  and walks.
- First client messages: four file requests (23: `wbomb1.png`, then `block.png` three times), its own
  props (2), then three NPC-prop messages (3).
- The nickname in the client's first props is its own stored default, not the account name.

### Graal 2002 v22 (`GNW31101`): not completed

- It asks its built-in list host on port 14922 for the list. It sends list name `graal2002` and
  the account, then shows the list.
- Connect never opened a game connection. That held with a double-click on the server, Return, and a
  Wine virtual desktop. So no game login was captured. The likely cause is that this list protocol
  expects an answer the lab listserver does not give.

## Where a binary sign list ends, on 2.31 (E#604)

Build: 2.31 (`GNW28015`), offline: Training, then the F5 level loader. The files and the method are
the ones used for 2.05 in the first batch: a real GR-V1.03 level (the 1.21 `level40.graal`) with its
three sign slots rewritten as `ONE`, `TWO` and `THREE`.

| File | Sign 1 | Sign 2 | Sign 3 |
| --- | --- | --- | --- |
| no gap | ONE | TWO | THREE |
| empty line after sign 1 | ONE | not shown | not shown |
| empty line, a `HEIGHTS` line, then signs 2 and 3 | — | not shown | — |

- 2.31 stops the sign list at the first empty line, as 2.05 does in the first batch. The two readers
  agree, and both keep 1 sign of 3.
- Lab notes:
  - 2.31's F5 loader finds a new level file only after its `FILENAMECACHE.txt` has been deleted.
  - It needs a Wine virtual desktop.
  - Keys need an explicit focus on the game window.

## The original GServer 1.3 with the 1.3 test client (E#423)

Server: `GServer13.exe`, the original 1999 server shipped with the 1.3 test client. It ran under
Wine on its own options dialog (port changed), behind the probe. Clients: two real 1.3 test clients
(`GSERV014`, A and B), then a 1.28 beta 2 client (`GSERV013`).

### Accounts and login

- The server refuses an unknown account with "An account with the name and password you typed in
  doesn't exist."
- Its `accounts.txt` takes the same record shape as GServer 1.28 beta 2's file: account, password,
  then the stored props. Records copied from a 1.28 beta 2 file worked unchanged.
- 1.3 logs in with type 0, generation 2. The start level is drawn and played.

### An older build

- 1.28 beta 2 logs in, and the server closes the connection at once. The client shows "You need at
  least Graal version 1.3 to play on this server."
- The players already online (A and B) each receive an other-player message for the rejected player's
  id with prop 51 (disconnected).
- So a build older than 1.3 never stays online here. That means it can never be the target of the
  private-message "cannot answer" reply on this server.

### Other players in the same level

- When B joins, A receives other-player messages (8) for B with a **one-byte** player id. First comes
  an empty head (11), then position, level and the other props.
- When B sends its own props, A receives B's nickname (0) and head as B sent them.

### Server prop limits (props sent by A)

| Prop sent by A | Server's reply to A (9) | What B receives for A (8) |
| --- | --- | --- |
| max hearts 30 | max hearts 20 | — |
| hearts 30 (60 half hearts) | 40 half hearts (twice the max) | the raw 60 |
| gralats 20,000,000 | nothing | nothing |
| arrows 150 | 99 | — |
| bombs 150 | 99 | — |
| alignment 120 | nothing | 120 |
| sword power 5 | nothing | 5 |
| shield power 4 | nothing | 4 |
| glove power 9 | nothing | nothing |
| bomb power 9 | nothing | nothing |

- Hearts, max hearts, arrows and bombs are corrected back to the sender.
- Alignment, sword and shield go on to the other player as sent, with no correction on the wire.
- Gralats, glove and bomb power are neither answered nor passed on.

### Not settled

- How nickname and head are sent for a player in **another** level. A warp injected into B (PLO 14,
  in the later layout) left B on "loading" without a level request, so B never changed level.

## The player-list folder that prop 81 picks (E#23)

Build: 5.00r7 (`G3D22067`), unchanged, with its own licence. Its LAN login host is redirected to the
lab inside the namespace, and the clock is 2007-07-25. 5.00r7 opens its built-in player-list window by
itself. The window has folders Staff, Buddies, Guild, Normal, Ignore and Offline, and three tabs.
Other players were injected (8) with an account (34), a nickname (0), a level (20) and prop 81.

Each value was tested on its own: one injected player per fresh login. Then every row of the list
was hovered, each folder header was clicked twice, and all three tabs were shown. Under Wine the list
redraws rows only on mouse events.

| Prop 81 | Counted in "Players: N online" | Shown |
| --- | --- | --- |
| none, 0, 8, 16, 32, 64 | yes | under Normal |
| 2, 4, 6, 10, 12 | yes | in no folder, on none of the three tabs (players, Global Guilds, Servers) |
| 3 (and 1, 5, 7, 9 in the earlier mixed runs) | no | nowhere |

- Bit 0 takes the player out of the online count and out of the list.
- Bit 1 or bit 2 keeps the player counted but shows them in no folder.
- Bits 3 to 6 alone change nothing visible: the player is listed under Normal, as with 0 or no prop 81.
- No value put a player under Staff, Buddies, Guild, Ignore or Offline. Those folders probably come
  from the client's own lists, not from prop 81: the server's staff list (47), the client's buddy and
  ignore lists, and the guild tag. **[inf]**
- So in this build prop 81 does not pick a folder. Its low three bits decide whether and how the player
  is counted and listed.
