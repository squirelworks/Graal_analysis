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

See the individual files for the measured contracts.

## File-format helpers (`file-formats/`)

Pure-Python helpers written for the notes in `formats/` and `client-internals/`. No client code.

| Script | Does |
|--------|------|
| `graaldes.py` | The client's DES variant (bit-reversed key bytes) and its 48-character string cipher. Decrypts saved passwords. See `client-internals/saved-passwords.md`. |
| `gwebl.py` | Decrypts and parses `weblevels/*.code` (GWEBL001). Also a GR-V board reader and writer and a GR-V level parser. See `formats/gwebl001-cache.md`. |
| `extract_tutorials.py` | Pulls the 13 embedded tutorial levels out of a 2.0x exe (needs `pefile`). See `formats/level-binary-client.md`. |
