# Real Windows 4.x to 6.x clients on a lab server, 2026-11-18

Lab run for #398 (the 4.x to 6.x rows) and the ping capture moved from
seihai-gserver#44. Real, unchanged Windows clients ran in a Windows 10 lab
VM against seihai-gserver (with its Login lobby) and seihai-listserver on
the lab host. Every run was offline: the VM's firewall let it reach only the
lab ports, and the clients' baked login and list names pointed at the lab.
The only client art was Seihai's own server art pack (seihai#559). **[lab]**

## Setup

| Item | Value |
| --- | --- |
| Clients | 4.20r8 (`G3D20126`), 5.00r7 CRC-patch build (`G3D22067`), 5.12 (`G3D14097`), 5.24r4 (`G3D15010`), 6.03r7 packed Windows exe (`G3D0311C`); also 1.39, 2.22 and 2.31 for the shared-level check |
| Clock | held at the build's era for the whole session: 2007-07-01 (4.20r8), 2007-07-25 (5.00r7), 2007-11-19 (5.12), 2012-11-20 (5.24r4, 6.03r7) |
| Server | seihai-gserver `main` 0afe61d, then squirelworks/seihai-gserver#158 |
| Login path | 4.x to 6.x dial the baked Login name on 14900 (the lobby), get the burst and their first files, then the server warp (178) to the game port |
| Input | VirtualBox keyboard scan codes into the focused client window |

## Results

| Build | Lobby → warp → game port | Draws tiles, player, HUD, NPC text | Walk | Ping (108 → 162) |
| --- | --- | --- | --- | --- |
| 4.20r8 | yes (login form account) | yes | yes | answered, same value (11–37 ms) |
| 5.00r7 | yes (as `guest`) | yes | yes | not sent to 5.x |
| 5.12 | yes (as `guest`) | yes | not driven | not sent to 5.x |
| 5.24r4 | yes (as `guest`) | yes | yes | not sent to 5.x |
| 6.03r7 | yes (as `guest`) | yes | yes | answered, same value (21–176 ms) |
| 6.113 | not run | – | – | – |

The full #398 action list (chests, push and pull, bushes, swim, spin) was
not run for these builds: it needs the harness fixture world, and this run
used a plain grass level. 6.113 cannot log in to a lab server: its token
comes in the connector script, whose reply is signed (see
`protocol/v7-connector-live-20261111.md`).

## Client behaviour seen

- **`LISTPROCESSES` (182) kills real Windows 6.03r7.** With 182 at the end
  of the login burst, the packed 6.03r7 exited with an access violation in
  `ntdll.dll` about 13 s after login, before it opened its
  window, every time and on any port. Without 182 it plays. GServer-v2 does
  not send 182 to it. Earlier Wine runs of a dumped 6.03r7 exe did not
  crash, so this was only visible on real Windows. **[lab]**
- **6.03r7 keeps a "Connecting to <server>…" box** over the level until the
  server has sent `ONLINEMODE` (168) and `SERVERLISTCONNECTED` (190). With
  both in the login burst the box closes as soon as the level is in. On the
  Login port it reads "Connecting to the login server…". **[lab]**
- **5.x and 6.x check `basepackage.gupd` with `PLI_VERIFYWANTSEND` (47)**
  on the game port (GINT5 CRC-32, then the name), after asking for it with
  `WANTFILE` on the Login server. **[lab]**
- **First files go to the Login server.** Every build asked the Login
  server for `pics1.png`, the bow and bomb icons and the player art right
  after the burst (5 to 11 requests within about 0.4 s), then checked them
  again on the game server with `UPDATEFILE` and its cached time. **[lab]**
- **Guests:** 5.x and 6.x log in as `guest` before any account form; only
  4.20r8 shows a login form first. **[lab]**
- **Files asked for** that a world may need besides the tileset and player
  art: `minimap.txt` (6.03r7), `bigmap.txt` (4.20r8 to 5.12), `head26.png`
  (5.00r7, 5.12), `guigames_arcmessage2.png` (5.24r4), and the player-list
  window images `playerlist_open.png`, `plistcat_guilds.png`,
  `plistcat_online.png`, `plistcat_servers.png`, `plisticononline.png`
  (4.20r8 to 5.12). **[lab]**
- **Not answered by the server, sent by the client:** 152 and 154 from
  4.20r8, 5.00r7 and 5.12 right after login on the game port. **[lab]**
- **An NPC with no image** (`NPC - x y` in the level file) sent as image
  `-` made every build from 1.39 to 6.03r7 ask for `-.gif`. **[lab]**

## Five builds in one level

1.39, 2.22, 2.31, 5.24r4 and 6.03r7 were online together in one level, the
5.x/6.x pair through the lobby. Every viewer saw the others arrive, drew them
with body and name, and saw them move. Chat was not re-run: 5.x and 6.x
show no chat bar unless the server sends a chat GUI script. **[lab]**

Server-side write-up: squirelworks/seihai-gserver `docs/lab/stage6-win10-2026-11-18.md`.
