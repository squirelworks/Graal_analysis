# Cross-version anchor search — 2171 / 222 / 231 vs v2.05

Date: 2026-10-14

## Method
Searched the three versioned C exports for anchors known from format notes and the v2.05 corpus (`DispatchGs1.txt`, plate map, CRC/PNG/level strings).

## Hits

| Anchor | 2171 | 222 | 231 | Notes |
|--------|------|-----|-----|-------|
| `GLEVNW01` | 4 | 3 | 0 | Text level magic. 231 may use a different path or string form. |
| `GR-V1` | 33 | 33 | 17 | Binary level magic. 231 also checks `GR-V1.04`. |
| `IHDR` | 1 | 1 | 1 | PNG writer present in all three. |
| `BOARD ` | 1 | 1 | 0 | Text board line. |
| `0xEDB88320` | 0 | 0 | 0 | Constant is lowercase `0xedb88320` in the export. |

## Identified clusters (2171)

### Level load
- Level load-from-stream path — reads 8-byte magic, compares `"GLEVNW01"`, calls loader.
- Nearby stream-handling helpers sit beside that path.
- Earlier site — magic check chain for `GR-V1.00`–`03` and `GLEVNW01` (version/capability path).
- Writer site — emits `"GLEVNW01\n"`.

### PNG
- `IHDR` compare inside the export path. Matches the earlier note that PNG writers still lack recovered names in the export.

### CRC-32
- CRC-32 table builder — contains the `>> 1 ^ 0xedb88320` polynomial step.
- Nearby helpers are likely init / update.

## Version notes
- 2171 and 222 are nearly identical in magic-check structure.
- 231 drops the plain `GLEVNW01` / `BOARD ` string hits in this export and adds `GR-V1.04`. Level load may have been refactored or the string is built differently.
- CRC and PNG anchors are stable across all three.

## Suggested names (2171, confirm in the local decompile project)
- Level load-from-stream → `Level_LoadFromStream` (or `TLevel_Load`)
- CRC table builder → `Crc32_BuildTable`
- PNG path containing `IHDR` → `Png_WriteChunk` / `Png_Export`

## Next
Repeat the same enclosing-function lookup for 222 and 231, then rename inside the Ghidra projects. The v2.05 `DispatchGs1.txt` is opcode-oriented and does not share these level/CRC strings; use it for the script-dispatcher pass separately.
