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

See the individual files for the measured contracts. `graaleditor-vs-205.md` compares GraalEditor and GraalShop with the editor built into the 2.05 client.
