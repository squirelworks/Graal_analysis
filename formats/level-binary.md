# Binary level formats: GR-V1 (.graal) and Z3-V1 (.zelda)

Date: 2026-10-21

Source: GServer-v2 `TLevel::loadGraal`, `TLevel::loadZelda` (GPLv3, summarized). Tags: **[srv]** server source · **[2.05]** · **[inf]** inferred.

The 2.05 string table holds exactly these level magics: `Z3-V1.03`, `Z3-V1.04`, `GR-V1.00`–`GR-V1.03`, and `GLEVNW01`, each set appearing three times in the string table (one copy sits next to the GWEBL001 web-level cache code). **[2.05]** The 2.05 loader itself has not been traced, so the bit-stream rules below come from server source.

## Correction

CONSOLIDATED.md calls GR-V1 a "64×64 board of 2-byte tiles". It is not. The board is a **packed bit stream with run-length codes**. Only `.nw` text and the `PLO_BOARDPACKET` wire form store one 16-bit value per tile.

## Layout

```
char[8] magic        GR-V1.00 | GR-V1.01 | GR-V1.02 | GR-V1.03 | Z3-V1.03 | Z3-V1.04
bitstream board      until 4096 tiles are produced
text   links         lines until "#" or an empty line
binary baddies       3-byte records until FF FF FF, each followed by a verse line
text   npcs          lines until "#" or an empty line  (not in .zelda)
text   chests        lines until "#"   (GR-V1.01+ only, not in .zelda)
text   signs         lines until an empty line or EOF
```

## Board bit stream

- Code width: **12 bits** for `GR-V1.00` and all `Z3-V1.*`; **13 bits** for `GR-V1.01`–`.03`.
- Codes are read least-significant-bit first: bytes are appended to a little-endian bit buffer and `width` bits are taken from the bottom.
- Flag bit = the top bit of the code (`0x800` at 12 bits, `0x1000` at 13 bits).
  - **Flag set:** a control code. `count = code & 0xFF`. If `code & 0x100` is set, the next run is a **double** run.
  - **Flag clear:** a tile id.
- When `count == 1` (the default), write the tile once.
- Single run: write the next tile `count` times, then reset `count = 1`.
- Double run: read two tiles A and B and write `A B` `count` times (`{double 4} 5 6` → `5 6 5 6 5 6 5 6`), then reset.
- Tiles fill `board[x + 64*y]` row by row, layer 0 only.

12-bit files cannot address tiles ≥ 2048 (the flag bit takes the top bit). That is why 1.01 widened the code to 13 bits for the 4096-tile `pics1`. **[inf]**

## Records

| Section | Shape | Notes |
|---------|-------|-------|
| Link | `dest x y w h newx newy` | Spaces in the level name are allowed. Tokens before the last 6 are rejoined. Links to missing levels are dropped. |
| Baddy | `i8 x, i8 y, i8 type` + `\n`-terminated verse line | Verses separated by `\`: sight, hurt, attack. Z3-V1.03 has no verse line. Terminator is `FF FF FF` followed by an empty line. |
| NPC | `GCHAR x, GCHAR y, image#script` | The script uses `0xA7` for newline. An empty image means a script-only NPC. |
| Chest | `GCHAR x, GCHAR y, GCHAR item, GCHAR signindex` | The item index is in `npc-library/gs1-reference-205.md`. |
| Sign | `GCHAR x, GCHAR y` + sign-alphabet text | Decoder in `sign-text.md`. |

Coordinates in these records are whole tiles (GCHAR), not half-tiles. **[srv]**

## Z3-V1 differences
- Sections: board, links, baddies, signs. **No NPC and no chest section.**
- Baddy verse line only in `Z3-V1.04`.
- Board coding is the same as GR-V1.00 (12-bit).

## Open
- GR-V1.04 appears only in the 2.31 binary (`cross-version-anchors.md`). Its changes are unknown.
- Whether the 2.05 writer emits double runs or only single runs.
