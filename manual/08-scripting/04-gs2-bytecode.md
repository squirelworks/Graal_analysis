<!-- manual: kind=reference status=draft -->
# 8.4 GS2 bytecode

This chapter covers compiled scripts on the wire. 2.05 and earlier clients receive GS1 as text and never see bytecode (→ §8.1.2). The container 4.2.0.8, 5.0.0.7, and unpacked 6.00 parse is → §8.4.2 and → §8.3.6. The runner, including the value-stack cap and opcodes 9 and 10, is → §8.3.7. OpenGS1's layout, a reimplementation, stays in → §8.4.3 for reference. Syntax, the standard library, and the event model stay open (→ App. E#207). Which message carries the container is still disputed (→ App. E#202).

> Status: draft. The container for the builds in §8.4.2 is recorded. The runner is in §8.3.7. Syntax, the standard library, and the event model stay open (→ App. E#207). The id that carries the container is disputed (→ App. E#202).

## 8.4.1 Transport

| Item | Rule | Source |
| --- | --- | --- |
| message | `PLO_NPCBYTECODE` (131, wire byte `0xa3`): `i3 code`, then the bytecode | [srv] (protocol/packet-ids.md) |
| version gate | sent only to clients at or above the GServer-v2 version constant `CLVER_4_0211`, and only when the bytecode is non-empty | [srv] (protocol/graphics-movement-bytecode.md#on-wire) |
| framing | wrapped in `PLO_RAWDATA` with a length prefix (→ §2.1.2) | [srv] (protocol/graphics-movement-bytecode.md#on-wire) |
| with NPC props | an NPC is sent as `PLO_NPCPROPS` plus the optional `PLO_NPCBYTECODE` | [srv] (protocol/graphics-movement-bytecode.md#other-level-objects) |
| 2.05 | the 2.05 receive switch does not handle it | [srv][2.05] (protocol/packet-ids.md) |
| other ids | a second reading puts GS2 bytecode on id 197 → App. E#202 | [srv] (protocol/packet-layouts.md; client-internals/feature-specs/02-weapons-combat.md#weapon-lists-server-to-client-srv205) |
| how the client stores it | a 24-byte instruction record and an op-index program counter (→ §8.4.2). 4.2.0.8 attaches those instructions to the `TGraalVar` (→ §8.3.7) | [bin] (protocol/gs2-client-vm.md#container-the-client-reads); [bin] (client-internals/gs2-vm-from-engines.md#bytecode-and-source) |

## 8.4.2 Format

4.2.0.8, 5.0.0.7, and unpacked 6.00r2 and 6.00r4 parse one container: four big-endian segments (event mask, functions, strings, opcodes) and `F0`–`F6` operands. It does not share OpenGS1's layout (→ §8.4.3). The runner is → §8.3.7. Syntax, the standard library, and the event model stay open → App. E#207.

| Item | Rule | Source |
| --- | --- | --- |
| container | big-endian types 1–4, not GSHORT, not the `0xAC` wrapper | [bin] (protocol/gs2-client-vm.md#container-the-client-reads) |
| later builds | 5.0.0.7 and 6.00 add dispatcher cases; 6.00 adds folds 234–242 | [bin] (protocol/gs2-client-vm.md#opcodes-added-after-4208) |
| unpacked 6.1.1.3 | same four segments, 24-byte instructions, cases 54 and 121 and folds 234–242; 48 and 49 stay absent (→ §8.4.4) | [bin] (protocol/gs2-unpacked-6113.md#what-the-dispatcher-adds-past-600) |
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

The unpacked Windows 6.1.1.3 image walks the same four segment types and stores a decoded instruction in 24 bytes. Operand markers `F0`–`F6` keep the 6.00 widths. The dispatcher adds no case past 242. Cases 54, 121 and folds 234–242 are present. Cases 48 and 49 are not. A `.code` file of at least eight bytes is accepted when the magic is `GRESCR01`, the cache flag is 1, and the CRC32 of the bytes after the magic matches. [bin] (protocol/gs2-unpacked-6113.md#container); [bin] (protocol/gs2-unpacked-6113.md#what-the-dispatcher-adds-past-600); [bin] (protocol/gs2-unpacked-6113.md#script-cache)

| Rule | Builds | Source |
| --- | --- | --- |
| A `.code` file shorter than eight bytes is rejected. The magic is `GRESCR01`, and the CRC32 covers the bytes after those eight | 6.1.1.3 | [bin] (client-internals/gs2-6113.md#load-path-and-the-code-cache) |
| The dispatcher has 152 cases, from 11 through 242, with no case 48, 49 or 200. Cases 54, 121, 201–242 are present. Unpacked 6.037 has the same set | 6.1.1.3, 6.037 | [bin] (client-internals/gs2-6113.md#opcode-range) |
| Those cases include the opcodes the Preagonal compiler does not emit. A full builtin table was not extracted | 6.1.1.3 | [bin][doc] (client-internals/gs2-6113.md#against-preagonal) |

## 8.4.5 Built-in names in unpacked 6.1.1.3 and 6.0.3.7

Both unpacked images store the eighteen math names `abs`, `atan`, `atan2`, `ceil`, `cos`, `floor`, `log`, `max`, `min`, `pi`, `pow`, `random`, `round`, `sin`, `sqrt`, `sqrt1_2`, `sqrt2` and `tan`. [bin] (client-internals/gs2-builtins-6113.md)

Of the names Preagonal's compiler turns into opcodes, these images contain `abs`, `cos`, `log`, `max`, `min`, `pow`, `random`, `sin`, `format` and `sleep`. They do not contain `arctan`, `exp`, `vecx`, `vecy`, `arraylen` or `tokenize`. [bin][doc] (client-internals/gs2-builtins-6113.md)

`putcomp` and `putnewcomp` are in 6.0.3.7 and not in 6.1.1.3. `setprotocol`, `sendraw` and `senddata` are in 6.1.1.3 and not in 6.0.3.7. [bin] (client-internals/gs2-builtins-6113.md)

## 8.4.6 Earlier Linux 4.04r2 dispatch and frame scope

| Item | Exact-build observation | Limit | Source |
| --- | --- | --- | --- |
| Dispatch table | Range ends at 190; 191 indexed slots, of which 119 select a non-skip path; slot 11 selects the common skip path | Later fused-opcode range is outside this table; helper semantics not all recovered | [bin] (client-internals/linux-404r2-vm-dispatch.md#earlier-dispatch-boundary) |
| Extracted stream coverage | Every opcode in fourteen recovered streams selects a non-skip slot | Does not establish execution of every stream | [bin] (client-internals/linux-404r2-vm-dispatch.md#earlier-dispatch-boundary) |
| Slot-11 insertion control | Tested event order and completion are unchanged | One context; later Windows wait behavior is not assigned to this value | [cap] (client-internals/linux-404r2-vm-dispatch.md#earlier-dispatch-boundary) |
| Static frame helper | Depth guard, overrun path, frame-like allocation, prior-position save, push and active-state change | Field meanings remain inferred; no successful new live stop confirms this helper | [bin] (client-internals/linux-404r2-vm-dispatch.md#guarded-frame-transition) |

Later-build opcode and frame descriptions retain their own identities. Unrecovered helpers and correspondence remain open → App. E#207. [bin] (client-internals/linux-404r2-vm-dispatch.md#version-and-semantic-limits)

## 8.4.7 Linux 4.04r2 embedded scripts and live linkage

| Evidence | Observation | Limit | Source |
| --- | --- | --- | --- |
| Bounded embedded-zlib extraction | Fourteen valid four-segment candidates, 129 named entries and 15,799 decoded instructions; instruction bytes round-trip and indexes are in range | Structural validation is not corpus-wide execution | [bin] (client-internals/linux-404r2-embedded-scripts.md#recovered-corpus-and-structural-checks) |
| Profile-script input | A corrected read of 9,530 live bytes matches the recovered payload digest; the same run enters the native executor | One loader/executor linkage, not all streams or complete profile execution | [cap] (client-internals/linux-404r2-embedded-scripts.md#one-payload-linked-to-execution) |
| Native reader/writer recovery | Operations available for focused review | Does not itself supply a full format specification | [bin] (client-internals/linux-404r2-embedded-scripts.md#recovered-corpus-and-structural-checks) |

The wrong-representation hash attempt remains superseded; only the corrected read supplies the match. Historical server-delivered content, cross-platform equivalence and 3D gameplay are not established. Remaining container/execution questions → App. E#207. [cap] (client-internals/linux-404r2-embedded-scripts.md#one-payload-linked-to-execution); [bin] (client-internals/linux-404r2-embedded-scripts.md#boundary)

## 8.4.8 Compare bounded Linux embedded-script corpora across builds

[bin] Bounded extraction finds 14 containers in 4.04r2, 13 in each 4.20 revision and each 6.01 architecture, and 12 in 6.03r7 x64. The 4.20 pair and 6.01 architecture pair each agree on all 13 inflated payloads; 6.03 is an exact subset of 6.01. Its missing scanned payload has nine entries and 247 instructions, without proving feature removal. Five payloads match between 4.04 and 4.20. [bin] (client-internals/linux-cross-version-embedded-controls.md)


[bin] Entry/instruction totals are 119/15,208 for each 4.20 corpus, 55/5,053 for each 6.01 corpus and 46/4,806 for 6.03. All 78 occurrences validate four unique segments numbered 1–4, candidate entry/string bounds and exact instruction-byte reconstruction; maximum observed tag is 189. Neither 3.04 duplicate yields an accepted bounded zlib stream. Roster alignment remains a candidate comparison. Extraction runs no client/server and proves neither execution nor native semantic equivalence; E#207 remains partial. [bin] (client-internals/linux-cross-version-embedded-controls.md)
