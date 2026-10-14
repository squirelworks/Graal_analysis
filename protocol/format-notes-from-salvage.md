# Format notes from salvage (2026-10-14)

Promoted from `/recycler/salvage/seihai-original-data/docs/` and dropin formats.

## Level formats

### GLEVNW01 (.nw)
- First line: `GLEVNW01`
- `BOARD x y width layer tilesdata` — horizontal run, 12-bit tile indices packed as two base64 chars
- Alphabet: `A-Za-z0-9+/` (AA = 0, // = 4095)
- Stored at `levelTiles[x + y*64]`; layer ignored
- Other records: LINK, SIGN/SIGNEND, NPC/NPCEND, BADDY/BADDYEND, CHEST
- Loader also accepts GR-V1.01–03 (binary .graal) and Z3-V1.03/04 (Zelda)

### Board model
- 64×64 cells, 16 px each, world = 1024×1024 px
- File pairs: `.seihai`/`.graal`, `.as`/`.nw`
- Headers: SH-V1.00–03, GR-V1.00–03, GLEVAS01, GLEVNW01, Z3-V1.03/04

### GRMAP001 (.gmap)
- Level list with HEIGHTS blocks, not a board itself

## Collision (tiletypes)
- Client does not inspect the tileset image
- Board stores tile id (0–4095); collision is a separate 4096-byte table
- `isOnWall`: type ≥ 20
- `isOnWater`: type == 11
- Table lives in `tiletypes.h` / `tiledefs.txt` (128 values per line)

## Sign text
- Binary sign record: `byte0 = x+0x20`, `byte1 = y+0x20`, rest = sign alphabet
- Do not apply binary decoder to GLEVNW01 signs (already text) or NPC scripts (Latin-1, 0xA7 = newline)
- Drop-in decoder: `formats/sign-decoder/signText.js`

## Files promoted
- `/shworkingpapers/assets/formats/` — glevnw01, grmap001, gani, tiletypes, boards, systems
- `/shworkingpapers/assets/tiledef/tiledefs.txt`
- `/shworkingpapers/scripting/sign-decoder.md`
- `/shdecompiling/graal-v205/` — Graal.exe.c, .gzf, DispatchGs1.txt, PlateGs1.java (do not release)
