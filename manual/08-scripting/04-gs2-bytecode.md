<!-- manual: kind=reference status=draft -->
# 8.4 GS2 bytecode

This chapter covers compiled scripts on the wire. 2.05 and earlier clients receive GS1 as text and never see bytecode (→ §8.1.2). The format of the bytecode that 4.x and later clients receive is not in the notes (→ App. E#207). The only bytecode format the notes describe is OpenGS1's, a reimplementation, given in → §8.4.3 for reference.

> Status: draft. The GS2 bytecode format itself is open (→ App. E#207); the id that carries it is disputed (→ App. E#202).

## 8.4.1 Transport

| Item | Rule | Source |
| --- | --- | --- |
| message | `PLO_NPCBYTECODE` (131, wire byte `0xa3`): `i3 code`, then the bytecode | [srv] (protocol/packet-ids.md) |
| version gate | sent only to clients at or above the GServer-v2 version constant `CLVER_4_0211`, and only when the bytecode is non-empty | [srv] (protocol/graphics-movement-bytecode.md#on-wire) |
| framing | wrapped in `PLO_RAWDATA` with a length prefix (→ §2.1.2) | [srv] (protocol/graphics-movement-bytecode.md#on-wire) |
| with NPC props | an NPC is sent as `PLO_NPCPROPS` plus the optional `PLO_NPCBYTECODE` | [srv] (protocol/graphics-movement-bytecode.md#other-level-objects) |
| 2.05 | the 2.05 receive switch does not handle it | [srv][2.05] (protocol/packet-ids.md) |
| other ids | a second reading puts GS2 bytecode on id 197 → App. E#202 | [srv] (protocol/packet-layouts.md; client-internals/feature-specs/02-weapons-combat.md#weapon-lists-server-to-client-srv205) |
| how the client stores it | not traced | [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |

## 8.4.2 Format

The notes do not decode the bytecode a 4.x or later client receives, and do not say whether it shares anything with OpenGS1's format → App. E#207 [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation).

## 8.4.3 OpenGS1 bytecode (reference reimplementation)

OpenGS1 defines a stack-based bytecode VM for GS1 [src] (protocol/graphics-movement-bytecode.md#scripting--gs1-bytecode). It is an independent reimplementation: 2.05 does not share its opcode set and does not run bytecode at all [2.05] (npc-library/gs1-reference-205.md#execution-model-205). How the notes first read this format is → App. E#208.

File layout, in order:

| Part | Content | Source |
| --- | --- | --- |
| 1 | `u32` body offset | [src] (protocol/graphics-movement-bytecode.md#bytecode-file-layout-bytecodecpp) |
| 2 | `u32` string-constant count, then length-prefixed strings | [src] (protocol/graphics-movement-bytecode.md#bytecode-file-layout-bytecodecpp) |
| 3 | `u32` number-constant count, then `f32` values | [src] (protocol/graphics-movement-bytecode.md#bytecode-file-layout-bytecodecpp) |
| 4 | the bytecode body, starting at the body offset | [src] (protocol/graphics-movement-bytecode.md#bytecode-file-layout-bytecodecpp) |

A packed value is 4 bytes:

| Field | Bits | Content | Source |
| --- | ---: | --- | --- |
| `valueType` | 4 | constant number, constant string, constant array, or named | [src] (protocol/graphics-movement-bytecode.md#packedvalue-4-bytes) |
| `value` | 16 | an index into the constant table or the name table | [src] (protocol/graphics-movement-bytecode.md#packedvalue-4-bytes) |
| unused | 12 | n/a | [src] (protocol/graphics-movement-bytecode.md#packedvalue-4-bytes) |

Opcodes, by name; the notes give no numeric values:

| Opcode | Meaning | Source |
| --- | --- | --- |
| `OP_PUSH` | push a packed value | [src] (protocol/graphics-movement-bytecode.md#opcodes-from-operationhpp) |
| `OP_ASSIGN` | S(1) = S(0) | [src] (protocol/graphics-movement-bytecode.md#opcodes-from-operationhpp) |
| `OP_ARR_SET`, `OP_ARR_GET` | array access | [src] (protocol/graphics-movement-bytecode.md#opcodes-from-operationhpp) |
| `OP_ADD` … `OP_POW` | arithmetic | [src] (protocol/graphics-movement-bytecode.md#opcodes-from-operationhpp) |
| `OP_INC`, `OP_INCPUSH`, `OP_DEC`, `OP_DECPUSH` | increment and decrement | [src] (protocol/graphics-movement-bytecode.md#opcodes-from-operationhpp) |
| `OP_CALL`, `OP_CMD_CALL` | function call, command call | [src] (protocol/graphics-movement-bytecode.md#opcodes-from-operationhpp) |
| `OP_JMP`, `OP_JAL`, `OP_RET` | control flow | [src] (protocol/graphics-movement-bytecode.md#opcodes-from-operationhpp) |
| `OP_EQ`, `OP_LT`, `OP_GT`, `OP_LTE`, `OP_GTE` | comparisons | [src] (protocol/graphics-movement-bytecode.md#opcodes-from-operationhpp) |
| `OP_NOT`, `OP_AND`, `OP_OR` | logic | [src] (protocol/graphics-movement-bytecode.md#opcodes-from-operationhpp) |
| `OP_JEZ`, `OP_JNZ` | conditional jumps | [src] (protocol/graphics-movement-bytecode.md#opcodes-from-operationhpp) |
| `OP_STOP` | halt | [src] (protocol/graphics-movement-bytecode.md#opcodes-from-operationhpp) |
| `OP_DBG_OUT` | debug output | [src] (protocol/graphics-movement-bytecode.md#opcodes-from-operationhpp) |
