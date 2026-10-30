# Graal3D (February 2000)

Date: 2026-10-21

Graal3D is a separate 3D side project shipped as `graal3d.7z`: a client, `Graal3D.exe`, and its own server, `GServer.exe`.
Both carry resource stamps from 2000-02-05, between the 2D releases V1.32 (`GSERV018`) and V1.33 (the first `GNW` token).
These notes come from static reads of both binaries (RTTI, form resources, strings), a decompiler pass, and a live lab on 2026-10-30.
No decompiler output is reproduced here.

**Does it use a gserver?** Yes, its own: `GServer.exe` from the same archive (TCP 14901). It does not talk to the 2D GServer or the list server. Players also exchange position and chat directly over UDP once the server has told each client the others' addresses.

- [protocol.md](protocol.md): framing, login, packet ids, the player property table, peer-to-peer UDP, admin commands.
- [formats.md](formats.md): config files, the registry password, `accounts.txt`, levels and models.
- [client-behaviour.md](client-behaviour.md): controls, walking, running, jumping, camera and the chat log, for a per-version profile.
- [lab-2026-10-30.md](lab-2026-10-30.md): the live run of both programs under Wine, what it confirmed and its limits.
- [reference-server/](reference-server/): a small Python server written from these notes. The real client logs into it, and it matches the original server's messages on the lab session.
- [torque-engine-4x.md](torque-engine-4x.md): the **other** Graal 3D, the Torque-based `Graal3DEngine.dll` of the 4.x clients (2006), and how a 4.x client connects to a 3D server.

## What ships

| File | Notes |
|---|---|
| `Graal3D.exe` | Delphi client. DelphiX `TDXDraw` in Direct3D retained mode (`do3D`, `doRetainedMode`, `doZBuffer`, `doTexture`), 50 ms `TDXTimer`. zlib 1.1.2 linked. |
| `GServer.exe` | Delphi server, default TCP port 14901, `levels\` folder, `accounts.txt`. |
| `graal3dconfig.txt` | Client config (server address, port, UDP options, look). |
| `serverconfig.txt` | `serverport=14901`. |
| `level1.x`, `startlevel.x` | Levels as DirectX `.x` text files. |
| `head.x`, `body.x`, `armleft/right.x`, `handleft/right.x`, `footleft/right.x` | The player model, one mesh per body part. |
| `*.bmp` | Textures (`body.bmp`, `body1.bmp`, `man.bmp` for the head, and the level textures). `logo.bmp` is the connect-window image. |

There are no `.graal`/`.nw` loaders, no GANI, no tiles and no NPC scripting in either binary.

## Client windows

| Class | Purpose |
|---|---|
| `TAdventure` | Main window: the 3D view, a chat edit line, the frame timer. Ctrl+Enter toggles fullscreen, Esc quits, F1 and F2 open the two option windows. Enter in the chat line sets the chat text. |
| `TConnectFrame` | Start window: nickname (default `Stefan`), host (default `127.0.0.1`), port `14901`, account and password (both `guest`). |
| `TMoreOptions` | "Hardware options": fixed UDP port (default 14898) and "Don't use UDP". |
| `TEditLook` | "Player look": `bodyx`, `headx`, `bodytex`, arm, shoe and hand colours. |

Each frame tick the client reads the TCP socket, reads the UDP socket, diffs its own player properties and queues the changes, then flushes the TCP send buffer.

## Server windows

| Class | Purpose |
|---|---|
| `TStartFrame` | Start dialog. |
| `TServerFrame` | Main window: player count, "Edit accounts", "Update levels", tray menu with Show / Shutdown. Caption starts as `Graal3D: 0 player(s)`. |
| `TAccountList`, `TEditAccount` | Account list and editor (name, password, admin level, disabled flag). |
| `TPlayerStats` | Online player list with message, disconnect and account buttons. |
| `TSendFrame` | Message to one player or to all. |
| `TUpdateLevels` | Names of cached levels to reload from disk. |

The server holds at most 200 players. Player ids are the lowest free slot from 1 to 200.

## How it relates to the 2D Graal of the same time

**The server is the 2D GServer with the game removed.** Every Delphi class in the Graal3D `GServer.exe` also exists in `GServer13.exe` (graal13b, 1999-11-29). The 2D server has 23 more: `TServerNPC`, `TServerBaddy`, `TServerChest`, `TServerHorse`, `TServerLevelLink`, `TBoardModify`, their `*Modify` delta classes, and the rich-edit/printer VCL units. The shared classes keep their names and roles:

- `TServerAccount` is 44 bytes in both servers, and accounts live in `accounts.txt` in both.
- `TServerLevel` shrinks from 8,244 bytes (it held a 64×64 board) to 24 bytes (name, file text, the list of players in it, and the list of players already sent the file).
- `TServerPlayerModify` keeps its job of tracking, per observer, which properties are still unsent.
- The admin forms (`TAccountList`, `TEditAccount`, `TPlayerStats`, `TSendFrame`, `TUpdateLevels`) are carried over.
- The guild tag check (`guilds\guild<name>.txt`) is carried over.

**The wire codec is the 2D codec.** Frames are a 2-byte big-endian length plus a zlib block, one message per line, `id + 32` packet ids, `+32` length-prefixed strings and 7-bit big-endian integers, with a 4096-byte flush. The differences:

- The version string is `GR3DV002` (the server also recognises `GR3DV001` and rejects it with "You need at least Graal3D beta2 to play on this server.").
- There is no key byte and no per-packet scramble.
- Packet ids and the property table are renumbered from scratch: positions are 3D floats, the angle is one byte, and colours are 24-bit.
- Player positions and chat go **peer to peer over UDP**. The server hands each client the other players' UDP endpoints and only relays position and chat over TCP for players that have no UDP. The 2D clients of the time also had `noudp` and `fixedudpport`, but there UDP went to the server.

**The client reuses the 2D client's skeleton.** It has the same class names: `TAdventure` (main form with `DXDraw`/`DXTimer1`), `TAdventureClient` (the socket object), `TAdventureServer` (here a small host-name → address cache entry), `TConnectFrame`, `TMoreOptions`, `TProgramCheck` (the "Graal execution file is corrupted" self-check) and `DesCipher`. The 2D-only parts (level, NPC, weapon and script classes) are gone, and `TPlayer` now holds Direct3D RM frames and meshes.

**Leftovers that show the port.** The server's player-list "disconnect" button sends packet 16, which is the 2D client's disconnect-message id. The Graal3D client ignores 16, so that kick arrives silently. The admin command path (61) sends 5, which the 3D client does show. The server still answers a file request (2) with the 2D raw-data pair 100/101, but the 3D client never sends 2 and drops raw data.

## Open points

- Packets 4 and 6 set client values that nothing reads (checked 2026-10-30). Packet 4 follows 2D "leader" semantics on the server side.
- Movement and camera maths: see [client-behaviour.md](client-behaviour.md).
- No admin client for Graal3D is in the archives. The admin protocol below comes from the server alone.
- The live run (see [lab-2026-10-30.md](lab-2026-10-30.md)) confirmed the TCP side. UDP between two real clients still needs Microsoft's `d3drm.dll`, which Wine does not provide.
