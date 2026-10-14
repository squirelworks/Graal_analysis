# GOBJSET01 — object stamps

Signature `GOBJSET01`. Five sets ship in the client tree (`objectsStandard`, `objectsHouse Inside`, `objectsCastle`, `objectsSnow`, `objectsVolcano`).

```
OBJECT width height name
<height lines of width*2 base64 characters>
OBJECTEND
```

Same 12-bit base64 packing as GLEVNW01. The name may contain spaces. There is no layer, link, NPC, or type byte.

Placing a stamp writes the tile ids onto the board. Collision is decided later by the type table. Example: the first stamp in objectsStandard is 2×2 “Bush”, base64 `ACAD` / `ASAT` → ids 2, 3, 18, 19. Those type bytes are 20/22, so the bush is wall. The stamp file itself does not say so.

288 named multi-tile objects across the five sets. Stamp id 0 is a 4×4 ground fill in the dungeon generator; stamp id 1 is a hole and is not written.
