# Section shapes as seen in real GR-V1.03 files

After the board bit stream (padded to a whole byte) the file is, in order:

1. Links: one text line each, ended by a line holding only `#`. In every file the link section is `n` link lines plus `#\n`; a level with no links is just `#\n`.
2. Baddies: records of three raw bytes (`x`, `y`, type) plus a verse line ending in `\n`; the section ends with `FF FF FF` plus `\n` (the terminator is an empty verse line). Verses are separators only (`\\` seen as two backslashes for empty verses).
3. NPCs: one line each (`x+32`, `y+32`, `image#script`, script line breaks as `0xA7`), ended by a line `#`.
4. Chests: four bytes each (`x+32`, `y+32`, `item+32`, `signindex+32`) plus `\n`, ended by a line `#`. A level without chests still has the bare `#\n`.
5. Signs: records until end of file. **When a level has no signs the file simply ends after the chest `#\n`:** no sign record and no empty line. 2305 of 3113 files have no signs; 2308 files end with `#\n`.

Nothing follows the signs in any file: no `HEIGHTS`, no unknown trailing bytes (0 bytes left over in all 3113).

All counts of whole-tile coordinates check out against the board: in one supplied level a link's two tiles hold the same tile id (a door), and in the other the chest sits on its own tile id. NPC and baddy bytes are single bytes and may lie outside 0..63 (165 NPCs: x from -32 to 223, y from -11 to 223; 3 baddies with y = 255).

NPC image field: 10735 `.gif`, 1164 `.png`, 46 `.mng`, 1 `.mid`, 1 `.mp3`, and 2913 empty (script-only NPCs).
