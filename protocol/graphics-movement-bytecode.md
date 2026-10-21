# Graphics, movement, and bytecode research notes

Date: 2026-10-14  
Sources: GServer-v2 `TLevel.cpp` / `TPlayer.cpp` / `TNPC.cpp`, OpenGS1 VM.

## Graphics pushes

### Board data
- `PLO_BOARDPACKET`: raw 64×64 `short` tile array (layer 0), 8192 bytes + newline.
- `PLO_BOARDLAYER`: `(layer:u8)(0)(0)(64)(64)` + raw `short[4096]` for that layer.
- `PLO_LEVELBOARD` / `PLO_BOARDMODIFY`: concatenated `getBoardStr()` results from `TLevelBoardChange`.
  - Change holds `x, y, width, height, tiles, oldTiles, modTime`.
  - Byte layout confirmed on the wire for 2.05: `c x, c y, c w, c h` + w × h GSHORT tiles, one change per message. See `packet-layouts.md`, "Board change on the wire". **[cap]**

### Other level objects
- `PLO_NPCPROPS` + optional `PLO_NPCBYTECODE` (wrapped in `PLO_RAWDATA` for clients ≥ 4.0211).
- `PLO_LEVELLINK`, `PLO_LEVELSIGN`, `PLO_LEVELCHEST`, `PLO_HORSEADD`, `PLO_BADDYPROPS`, `PLO_ITEMDEL`.

### GANI
- Client maintains a fixed list of standard GANIs (`walk.gani`, `sword.gani`, `idle.gani`, etc.).
- Animation state is part of player/NPC props, not a separate board packet.

## Player movement

- Pre-2.3 clients: server watches `gr.x` / `gr.y` flags and emits `PLPROP_X` / `PLPROP_Y` (position × 2) via a queued `-gr_movement` path.
- ≥ 2.3 clients: different (direct) path; the `gr.*` workaround is skipped.
- Positions are floats internally; on-wire often scaled by 2 and sent as chars/shorts.
- Client is expected to send local movement; server is authoritative for other players.

**Still needed:** exact packet ID and field layout the *client* emits for its own movement (direction, position, GANI).

## Scripting — GS1 bytecode

OpenGS1 defines a stack-based bytecode VM.

### Bytecode file layout (`Bytecode.cpp`)
1. `u32` body offset
2. `u32` string-constant count + length-prefixed strings
3. `u32` number-constant count + `f32`s
4. Bytecode body (starts at body offset)

### PackedValue (4 bytes)
- `valueType:4` (`PACKVALUE_CONST_NUMBER`, `CONST_STRING`, `CONST_ARRAY`, `NAMED`)
- `value:16` (index into constant table or name table)
- `unused:12`

### Opcodes (from `Operation.hpp`)
| Opcode | Meaning |
|--------|---------|
| `OP_PUSH` | Push PackedValue |
| `OP_ASSIGN` | S(1) = S(0) |
| `OP_ARR_SET` / `OP_ARR_GET` | Array access |
| `OP_ADD` … `OP_POW` | Arithmetic |
| `OP_INC` / `OP_INCPUSH` / `OP_DEC` / `OP_DECPUSH` | Inc/dec |
| `OP_CALL` / `OP_CMD_CALL` | Function / command call |
| `OP_JMP` / `OP_JAL` / `OP_RET` | Control flow |
| `OP_EQ` / `OP_LT` / `OP_GT` / `OP_LTE` / `OP_GTE` | Comparisons |
| `OP_NOT` / `OP_AND` / `OP_OR` | Logic |
| `OP_JEZ` / `OP_JNZ` | Conditional jumps |
| `OP_STOP` | Halt |
| `OP_DBG_OUT` | Debug |

### On-wire
- `PLO_NPCBYTECODE` carries the raw bytecode blob for an NPC.
- Sent only to clients ≥ `CLVER_4_0211` and only when bytecode is non-empty.
- Wrapped in `PLO_RAWDATA` with a length prefix.

## What is already usable for Seihai
- Board packet sizes and IDs are known.
- Full GS1 opcode set and constant-table layout are known.
- Movement scaling (×2) and the pre-2.3 `gr.x`/`gr.y` path are known.

## What still needs capture or confirmation
1. ~~Exact byte layout of `TLevelBoardChange::getBoardStr()`.~~ Done: see `packet-layouts.md`.
2. Client→server movement packet (ID + fields) for both <2.3 and ≥2.3.
3. How the original Delphi client stores/receives `PLO_NPCBYTECODE` (Ghidra trace).
4. Mapping from GS1 command names (`setcharprop`, `showcharacter`, etc.) to host functions the VM calls.
5. Whether later clients ever use a different bytecode format (GS2) or only V8.
