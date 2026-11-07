# What a 5.x/6.x Login server is already known to send

Date: 2026-11-01. No socket was opened. This collects the protocol notes and the client reads that already describe a server the client names `Login`. It leaves matrix unknown #3 open: the screens a public Login server paints are still unobserved.

Tags follow the notes they come from. A lab line is a loopback GServer-v2 standing in under that name. It is a record of what these clients accept.

## Handlers the client ties to that session

The 5.x and 6.01/6.03 clients open an ordinary game connection and name the server `Login`. There is no separate list protocol. The server list and the account screens are scripted GUI from that session. **[bin]** `protocol/v5x-clients.md`, `protocol/v6x-clients.md`.

| Message the notes tie to this session | What the client does with it | Tag |
|---|---|---|
| S→C 190 `PLO_SERVERLISTCONNECTED` | Raises `onServerListerConnect`. 4.20r8 treats this as the Login server accepting the session. 5.00r7 ties it to the server-list screen. `packet-ids.md` leaves the payload cell empty. | **[bin]** |
| S→C 178 `PLO_SERVERWARP` | Comma text of at least four fields. Field 0 is unused, field 1 is the new server name, field 2 the host, field 3 the port. The client closes the session and logs in again under that name. Seen when a lab proxy injected it, and when GServer-v2's listserver forwards a server-info request. | **[bin]** `packet-ids.md`; **[live]** `client-internals/live-behaviour-404.md`; **[cap]** `version-profiles/lab-v5-2026-10-30.md`, `protocol/v5v6-lab-play.md` |
| Level-load ids (name, board, chests, NPCs), on the lab stand-in | While the server name starts with `login`, the draw-layer mask is 0. 4.04r2 draws no players and no HUD. 5.x/6.x draw no characters and no default HUD. 5.24 and 5.30 draw tiles; 5.31r4 and 6.03r7 draw chests and image NPCs and no tiles until after the warp. | **[bin]** 4.04 mask; **[cap]** `lab-v5-2026-10-30.md`, `v5v6-lab-play.md` |
| Script and gani handlers (S→C 140, 197, 195) | The same handlers a game server uses. The notes call the server list, the account screens and the chat bar scripted GUI. The engine looks up a GUI control named `ChatBar` before keyboard input becomes chat. A bare lab server creates no such control, and typing sends nothing. The script text itself is in the unobserved list below. | **[bin]** `v5x-clients.md`, `v4x-clients.md`; **[cap]** `lab-v5-2026-10-30.md` |
| File reply to the client's `basepackage.gupd` request (C→S 23, or 47 when that server's copy is cached) | File ids carry the body (100/102), 45 answers "not modified", 105/106 mark package size and completion. A minimal `GRPKG001` with `NAME`, `VERSION`, `PLATFORM` and `MODE` satisfies the lab client. The client stores the Login copy under `updatepackages/`. | **[bin]** `v4x-clients.md`; **[cap]** `file-transfer.md`, `v5v6-lab-play.md`, `live-behaviour-404.md` |

6.01 and 6.03 use the same named session and the same 190 event. Their extra receive ids (109, 111 `creationtime.dat`, 198) are general handlers. No note says a Login server is the one that sends them. **[bin]** `v6x-clients.md`.

6.11 asks for a connector script before the game socket. The reply is loaded as `StartScript_Connector` and its `onCreated` runs. That script calls `connecttogameserver` and can replace the framing, the cipher and both id tables, and it builds the login itself. The gen-5 path remains the default until the script calls `setprotocol`. **[bin]** `v6x-clients.md`.

## The lab burst these clients accepted

`v5v6-lab-play.md` records GServer-v2's first burst after the login frame, on every 5.x/6.x build that lab played. The server side is GServer-v2. Ids in that burst include 190, then the level load (14, 6, 100, 101, chests, 156, 3), the staff and status lists (47, 180), the start and HTML messages (179, 41) and 182 (the client answers with its window titles on 44). 178 is absent from that burst. The lab proxy sends 178 afterwards. GServer-v2 itself sends 178 when its listserver forwards a server-info request. **[wire]**

4.04r2 on the same kind of stand-in asks for `basepackage.gupd` and `bigmap.txt` on the Login session. `bigmap.txt` is asked once per run of the program, on that session, and is not asked again after the warp. **[live]** `live-behaviour-404.md`.

## Still unobserved

A public Login session was not captured.

- The bytes a public 5.x or 6.x Login server sends, including the payload of S→C 190.
- The GUI script text for the server list, the account screens and the `ChatBar` control.
- The `FILE` list inside that server's `basepackage.gupd`, and any later update package.
- The backdrop level that server chooses (name, tiles, chests, image NPCs).
- The 6.11 connector script body, and with it the framing, cipher and login token a 6.11 client actually uses.
- The resulting look (matrix unknown #3). The lab screens are the lab world's ganis and a server named by the injected 178.
