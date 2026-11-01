# Tools

Cleaned notes on the classic Graal tool chain. Derived from observed behavior and format output. No raw decompile material.

| Tool | Role | Notes |
|------|------|-------|
| GraalEditor | Level editor (2.3.1.1) | Separate exe from 2.3 onward. Writes decimal BOARD 0 grids plus LINK/SIGN/CHEST/NPC/BADDY. |
| Built-in level editor | Editor inside each client (2.22 is the reference) | `level-editor/`: 2.22 reference, per-version deltas, format cross-reference, Seihai tracking checklist. |
| GraalShop | GANI editor | Sprite mode (GANI0001) and movie mode (GANI0002). |
| TerrainGenerator | Height-field world | Plasma midpoint displacement → GRMAP001 + GLEVNW01 with HEIGHTS. The 2.22 reference is `generators-222/terrain.py`. |
| DungeonGenerator | Stamp dungeon | 8×11 layout → GLEVNW01 boards and GRMAP001. The 2.22 reference is `generators-222/dungeon.py`. |
| GraalLevelGen | Image-to-levels | December 2000 contract in `classic-tools/graal-level-gen.md`. The 2.22 nw-gmap reference is `generators-222/levelgen.py`. |
| gif2mng | GIF converter | PNG for one frame, MNG for more. `-b` snaps to body palette. |
| RemoteControl | Staff client | Classic text codec on two sockets. Predecessor of RC2. |
| RemoteControl 2000–2002 | Staff client lineage | `GSERV014`→`GSERV023`, option packets, id changes. See `remotecontrol-lineage.md`. |
| NPC Control (RC 1.41) | NPC-server client | `NCL11012` login, NPC-server discovery, NC packet ids. Tool history in `npc-control.md`; wire layouts for `seihai-rc` in `../protocol/npc-control.md`. |
| Fan server tools | ListServer, serverlist, 1.39 scripts, Guildmaker | See `server-tools-2001.md`. Warns about a password stealer in the win32 ListServer. |
| Classic listserver ELF | Client and game-server directory | `classic-tools/serverlist3.md`. Frame and login lines in `classic-tools/listframe.py`. |
| gserverstat | HTML leaderboards | `classic-tools/gserverstat.md`. Account blob in `classic-tools/account13.py`. |
| Character Designer / GChar | Offline looks | `classic-tools/character-designer.md`. `CHR:1.00` line in `classic-tools/chrfile.py`. |
| TextConvert | Graal to New World levels | `classic-tools/text-convert.md`. |
| NPC server (2001) | Server-side NPC host | Logs into GServer as a player, 0.1 s tick, PM admin commands, `join` classes. See `npcserver-2001.md`. |

See the individual files for the measured contracts. `graaleditor-vs-205.md` compares GraalEditor and GraalShop with the editor built into the 2.05 client.
- `lab-setup.md` — the offline Wine + GServer + listserver-stub lab used for the [cap] captures.
- `relay-bridge/` — `room_bridge.py` (logging proxy for the 1998 GServ relay that can rename join rooms), `AppletRun.java` (runs the Java Graal / Zelda Online applets in a frame), `pcap_lines.py` (prints the relay lines in a capture). See `../client-internals/relay-room-bridge.md`.
- `lab-servers/` — our lab listserver (version 2, with tests), `run-lab.sh` and the gs2lib patch our GServer build carries. See `../server-notes/lab-servers-2026-10-30.md` for what our servers are and how they compare with GServer-v2 beta4.
- `ghidra/` — headless salvage scripts for recovered binaries (`analyze_tool.sh`, `ghidra_scripts/ExportSalvageArtifacts.java`). Counts and decompiler text stay in gitignored `local-out/`. The prose summaries of those tools are in seihai-servertools (`recovered-drive-tools/`, `recovered-hacks/`).

## File-format helpers (`file-formats/`)

Pure-Python helpers written for the notes in `formats/` and `client-internals/`. No client code.

| Script | Does |
|--------|------|
| `graaldes.py` | The client's DES variant (bit-reversed key bytes) and its 48-character string cipher. Decrypts saved passwords. See `client-internals/saved-passwords.md`. |
| `gwebl.py` | Decrypts and parses `weblevels/*.code` (GWEBL001). Also a GR-V board reader and writer and a GR-V level parser. See `formats/gwebl001-cache.md`. |
| `extract_tutorials.py` | Pulls the 13 embedded tutorial levels out of a 2.0x exe (needs `pefile`). See `formats/level-binary-client.md`. |
