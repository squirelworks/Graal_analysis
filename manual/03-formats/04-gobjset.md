<!-- manual: kind=reference status=complete -->
# 3.4 GOBJSET01 object sets

An object set is a list of named multi-tile stamps that an editor places on a board. It carries tile ids only; what a tile does is decided by the tile type table (→ §3.5).

## 3.4.1 Layout

```
GOBJSET01
OBJECT width height name
<height lines of width*2 base64 characters>
OBJECTEND
…
```

| Rule | Detail | Source |
| --- | --- | --- |
| signature | `GOBJSET01` | [file] (formats/gobjset01.md) |
| tile packing | the same 12-bit base64 packing as GLEVNW01 (→ §3.1.3.2) | [file] (formats/gobjset01.md) |
| name | may contain spaces | [file] (formats/gobjset01.md) |
| no other fields | there is no layer, link, NPC or type byte | [file] (formats/gobjset01.md) |
| placing | placing a stamp writes its tile ids onto the board; collision is decided later by the type table | [file] (formats/gobjset01.md) |

## 3.4.2 Shipped sets

| Item | Detail | Source |
| --- | --- | --- |
| sets in the client tree | `objectsStandard`, `objectsHouse Inside`, `objectsCastle`, `objectsSnow`, `objectsVolcano` | [file] (formats/gobjset01.md) |
| objects | 288 named multi-tile objects across the five sets | [file] (formats/gobjset01.md) |
| first stamp | `objectsStandard` begins with the 2×2 "Bush", base64 `ACAD` / `ASAT` → ids 2, 3, 18, 19 | [file] (formats/gobjset01.md) |
| Bush collision | `disputed → App. E#100` | [file] (formats/gobjset01.md); [src] (formats/tile-walk.md#stamp-vocabulary) |
| generator stamps | in DungeonGenerator, stamp id 0 is a 4×4 ground fill and stamp id 1 is a hole that is not written (→ §3.1.3.4) | [bin] (formats/gobjset01.md) |
