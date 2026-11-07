<!-- manual: kind=reference status=draft -->
# 8.4 GS2 bytecode

This chapter covers compiled scripts on the wire. 2.05 and earlier clients receive GS1 as text and never see bytecode (→ §8.1.2). The container 4.2.0.8, 5.0.0.7, and unpacked 6.00 parse is → §8.4.2. OpenGS1's layout, a reimplementation, stays in → §8.4.3 for reference. Syntax and the event model stay open (→ App. E#207). Which message carries the container is still disputed (→ App. E#202).

> Status: draft. The container for the builds in §8.4.2 is recorded; syntax, the standard library, and the event model stay open (→ App. E#207). The id that carries the container is disputed (→ App. E#202).

## 8.4.1 Transport

| Item | Rule | Source |
| --- | --- | --- |
| message | `PLO_NPCBYTECODE` (131, wire byte `0xa3`): `i3 code`, then the bytecode | [srv] (protocol/packet-ids.md) |
| version gate | sent only to clients at or above the GServer-v2 version constant `CLVER_4_0211`, and only when the bytecode is non-empty | [srv] (protocol/graphics-movement-bytecode.md#on-wire) |
| framing | wrapped in `PLO_RAWDATA` with a length prefix (→ §2.1.2) | [srv] (protocol/graphics-movement-bytecode.md#on-wire) |
| with NPC props | an NPC is sent as `PLO_NPCPROPS` plus the optional `PLO_NPCBYTECODE` | [srv] (protocol/graphics-movement-bytecode.md#other-level-objects) |
| 2.05 | the 2.05 receive switch does not handle it | [srv][2.05] (protocol/packet-ids.md) |
| other ids | a second reading puts GS2 bytecode on id 197 → App. E#202 | [srv] (protocol/packet-layouts.md; client-internals/feature-specs/02-weapons-combat.md#weapon-lists-server-to-client-srv205) |
| how the client stores it | a 24-byte instruction record and an op-index program counter, for the builds in → §8.4.2 | [bin] (protocol/gs2-client-vm.md#container-the-client-reads) |

## 8.4.2 Format

4.2.0.8, 5.0.0.7, and unpacked 6.00r2 and 6.00r4 parse one container: four big-endian segments (event mask, functions, strings, opcodes) and `F0`–`F6` operands. It does not share OpenGS1's layout (→ §8.4.3). Syntax, the standard library, and the event model stay open → App. E#207.

| Item | Rule | Source |
| --- | --- | --- |
| container | big-endian types 1–4, not GSHORT, not the `0xAC` wrapper | [bin] (protocol/gs2-client-vm.md#container-the-client-reads) |
| later builds | 5.0.0.7 and 6.00 add dispatcher cases; 6.00 adds folds 234–242 | [bin] (protocol/gs2-client-vm.md#opcodes-added-after-4208) |
| still open | GS2 syntax, standard library, event model | [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |

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

## 8.4.4 Unpacked Windows 6.1.1.3

| Rule | Builds | Source |
| --- | --- | --- |
| A `.code` file shorter than eight bytes is rejected. The magic is `GRESCR01`, and the CRC32 covers the bytes after those eight | 6.1.1.3 | [bin] (client-internals/gs2-6113.md#load-path-and-the-code-cache) |
| The dispatcher has 152 cases, from 11 through 242, with no case 48, 49 or 200. Cases 54, 121, 201–242 are present. Unpacked 6.037 has the same set | 6.1.1.3, 6.037 | [bin] (client-internals/gs2-6113.md#opcode-range) |
| Those cases include the opcodes the Preagonal compiler does not emit. A full builtin table was not extracted | 6.1.1.3 | [bin][doc] (client-internals/gs2-6113.md#against-preagonal) |
