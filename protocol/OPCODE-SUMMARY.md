# Opcode Summary — 39ster 2.1

Authoritative source: `msgFuncs` table + enums in original `player.h`.  
Full details and emission points: `ash/OPCODE-MAP.md`.

## Client → Server (selected)

| Op | Name              | Notes |
|----|-------------------|-------|
| 0  | LEVELWARP         | |
| 1  | BOARDMODIFY       | |
| 2  | PLAYERPROPS       | |
| 3  | NPCPROPS          | |
| 4  | ADDBOMB           | |
| 20 | OPENCHEST         | remembers coords |
| 23 | WANTGIF           | file request |
| 30 | MODLEVELWARP      | |
| 37 | LANGUAGE          | |
| 51–87 | RC ops         | mostly empty stubs |

## Server → Client (selected)

| Op | Name              | Notes |
|----|-------------------|-------|
| 1  | LEVELLINK         | |
| 2  | SBADDYPROPS       | |
| 3  | SNPCPROPS         | |
| 6  | LEVELNAME         | |
| 7  | SBOARDMODIFY      | |
| 8  | OTHERPLPROPS      | |
| 9  | SPLAYERPROPS      | |
| 100| FILELEN           | |
| 101| TILES             | GR-V1 board |
| 102| FILEBLOB          | |

See Ash OPCODE-MAP.md for the complete 0–88 client table and all server ops.

## Note (2026-10-21)

This table follows 39ster 2.1. Current gs2lib names: 23 = `PLI_WANTFILE`; 30 = `PLI_LEVELWARPMOD`; server 100/101/102 = `PLO_RAWDATA`/`PLO_BOARDPACKET`/`PLO_FILE`, with the same roles as FILELEN/TILES/FILEBLOB. 2.05 coverage and the full id list are in `packet-ids.md`.
