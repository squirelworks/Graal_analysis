# Tools

Cleaned notes on the classic Graal tool chain. Derived from observed behavior and format output. No raw decompile material.

| Tool | Role | Notes |
|------|------|-------|
| GraalEditor | Level editor (2.3.1.1) | Separate exe from 2.3 onward. Writes decimal BOARD 0 grids plus LINK/SIGN/CHEST/NPC/BADDY. |
| GraalShop | GANI editor | Sprite mode (GANI0001) and movie mode (GANI0002). |
| TerrainGenerator | Height-field world | Plasma midpoint displacement → GRMAP001 + GLEVNW01 with HEIGHTS. |
| DungeonGenerator | Stamp dungeon | 8×11 layout → GLEVNW01 boards and GRMAP001. |
| GraalLevelGen | Image-to-levels | Converts an image into linked levels. |
| gif2mng | GIF converter | PNG for one frame, MNG for more. `-b` snaps to body palette. |
| RemoteControl | Staff client | Classic text codec on two sockets. Predecessor of RC2. |
| RemoteControl 2000–2002 | Staff client lineage | `GSERV014`→`GSERV023`, option packets, id changes. See `remotecontrol-lineage.md`. |
| NPC Control (RC 1.41) | NPC-server client | `NCL11012` login, NPC-server discovery, NC packet ids. See `npc-control.md`. |
| Fan server tools | ListServer, serverlist, 1.39 scripts, Guildmaker | See `server-tools-2001.md`. Warns about a password stealer in the win32 ListServer. |
| NPC server (2001) | Server-side NPC host | Logs into GServer as a player, 0.1 s tick, PM admin commands, `join` classes. See `npcserver-2001.md`. |

See the individual files for the measured contracts. `graaleditor-vs-205.md` compares GraalEditor and GraalShop with the editor built into the 2.05 client.
- `lab-setup.md` — the offline Wine + GServer + listserver-stub lab used for the [cap] captures.

## File-format helpers (`file-formats/`)

Pure-Python helpers written for the notes in `formats/` and `client-internals/`. No client code.

| Script | Does |
|--------|------|
| `graaldes.py` | The client's DES variant (bit-reversed key bytes) and its 48-character string cipher. Decrypts saved passwords. See `client-internals/saved-passwords.md`. |
| `gwebl.py` | Decrypts and parses `weblevels/*.code` (GWEBL001). Also a GR-V board reader and writer and a GR-V level parser. See `formats/gwebl001-cache.md`. |
| `extract_tutorials.py` | Pulls the 13 embedded tutorial levels out of a 2.0x exe (needs `pefile`). See `formats/level-binary-client.md`. |
