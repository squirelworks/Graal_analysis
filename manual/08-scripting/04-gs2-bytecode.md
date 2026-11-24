<!-- manual: kind=reference status=draft -->
# 8.4 GS2 bytecode

This chapter covers compiled scripts on the wire. 2.05 and earlier clients receive GS1 as text and never see bytecode (→ §8.1.2). The container 4.2.0.8, 5.0.0.7, and unpacked 6.00 parse is → §8.4.2; the per-build dispatch ranges are → §8.4.4, and the load-time fusion stages → §8.4.6. The runner, including the value-stack cap and opcodes 9 and 10, is → §8.3.3. OpenGS1's layout, a reimplementation, stays in → §8.4.3 for reference. Syntax, the standard library, and the event model stay open (→ App. E#207). Which message carries it is settled in → §8.4.1.

> Status: draft. The container for the builds in §8.4.2 is recorded. The runner is in §8.3.3. Syntax, the standard library, and the event model stay open (→ App. E#207). Which id carries the container is settled in → §8.4.1.

## 8.4.1 Transport

GS2 reaches the client as compiled bytecode. The rules below give the message that carries it, the version gate and the framing [srv] (protocol/packet-ids.md).

| Item | Rule | Source |
| --- | --- | --- |
| message | `PLO_NPCBYTECODE` (131, wire byte `0xa3`): `i3 code`, then the bytecode | [srv] (protocol/packet-ids.md) |
| version gate | sent only to clients at or above the GServer-v2 version constant `CLVER_4_0211`, and only when the bytecode is non-empty | [srv] (protocol/graphics-movement-bytecode.md#on-wire) |
| framing | wrapped in `PLO_RAWDATA` with a length prefix (→ §2.1.2) | [srv] (protocol/graphics-movement-bytecode.md#on-wire) |
| with NPC props | an NPC is sent as `PLO_NPCPROPS` plus the optional `PLO_NPCBYTECODE` | [srv] (protocol/graphics-movement-bytecode.md#other-level-objects) |
| 2.05 | the 2.05 receive switch does not handle it | [srv][2.05] (protocol/packet-ids.md) |
| other ids | a second reading puts GS2 bytecode on id 197 → §8.4.1 | [srv] (protocol/packet-layouts.md; client-internals/feature-specs/02-weapons-combat.md#weapon-lists-server-to-client-srv205) |
| how the client stores it | a 24-byte instruction record and an op-index program counter (→ §8.4.2). 4.2.0.8 attaches those instructions to the `TGraalVar` (→ §8.3.3) | [bin] (protocol/gs2-client-vm.md#container-the-client-reads); [bin] (client-internals/gs2-vm-from-engines.md#bytecode-and-source) |

**Settled question, formerly E#202: Which message carries GS2 bytecode.** Which message carries a GS2 script body on 4.x and 5.x clients was open: three sources named 131, 197 and 140 [srv] (protocol/packet-ids.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: NPC bytecode is `PLO_NPCBYTECODE` (131) behind `PLO_RAWDATA`. B: 197 "GS2 bytecode" replaces the script prop. C: 197 is `PLO_LOADSCRIPT`, a descriptor list | [srv] (protocol/packet-ids.md); [srv] (protocol/packet-layouts.md) |
| Settled (NPCs) | 131 behind 100 carries a runnable NPC body on 4.20r8, 5.24r4 and 6.03r7: the script fuzz delivered every case that way and the scripts ran | [lab] (protocol/script-fuzz-2026-11-19.md) |
| Settled (classes and weapons) | On 6.x, 197 is the descriptor `type,name,1,key,crc` and 140 carries the body, from the cache or the wire, never inside 197 | [cap] (protocol/gs2-official-bytecode-6113.md#what-this-settles); [bin] (formats/linux-6x-class-cache.md); [lab][cap] (protocol/linux-603-network-gs2.md) |
| Verdict | Verified: two messages for two kinds of object, not three rival claims. Claim B names the class exchange by its first message | [lab] (protocol/script-fuzz-2026-11-19.md) |
| Also measured | 4.20r8 does not honour the 6.x class path as sent: ten 197 and 140 variants with a valid compiled body ran no script and drew no request, while 131 behind 100 runs NPC bodies on the same build | [lab] (protocol/lab-appe-hosta-2026-11-20.md#gs2-class-path-on-420r8-e202-leftover) |
| Left over | How 4.20r8 delivers weapon and class scripts, and 4.0x before 4.20r8 | [lab] (protocol/lab-appe-hosta-2026-11-20.md#gs2-class-path-on-420r8-e202-leftover) |

[bin] In the selected Linux 6.03r7 class-cache caller, a pending-name lookup can suppress a new request after false helper status. Positive status can still skip a fresh reader call, while named class-loaded notification call paths follow; neither a notification nor no second request establishes a cache hit or parse. The future acceptance plan keeps status, reader entries, requests and actual event delivery separate. This is static caller evidence, not another network result. [bin] (formats/linux-6x-class-cache.md#caller-gates-and-the-next-cache-observation)

## 8.4.2 Format

4.2.0.8, 5.0.0.7, and unpacked 6.00r2 and 6.00r4 parse one container: four big-endian segments (event mask, functions, strings, opcodes) and `F0`–`F6` operands. It does not share OpenGS1's layout (→ §8.4.3). The runner is → §8.3.3. Syntax, the standard library, and the event model stay open → App. E#207.

| Item | Rule | Source |
| --- | --- | --- |
| container | big-endian types 1–4, not GSHORT, not the `0xAC` wrapper | [bin] (protocol/gs2-client-vm.md#container-the-client-reads) |
| later builds | 5.0.0.7 and 6.00 add dispatcher cases; 6.00 adds folds 234–242 | [bin] (protocol/gs2-client-vm.md#opcodes-added-after-4208) |
| unpacked 6.1.1.3 | same four segments, 24-byte instructions, cases 54 and 121 and folds 234–242; 48 and 49 stay absent (→ §8.4.4) | [bin] (protocol/gs2-unpacked-6113.md#what-the-dispatcher-adds-past-600) |
| still open | GS2 syntax, standard library, event model | [inf] (protocol/graphics-movement-bytecode.md#what-still-needs-capture-or-confirmation) |

#### What the clients run

The bytecode these clients run is a big-endian four-segment container. Segment lengths are raw 32-bit counts, so they are not GSHORT (→ §2.1.1). The container is not OpenGS1's layout (→ §8.4.3). Packet 140 and packet 197 stay the envelopes in → §8.3.2. The script object parses the segments, not the `0xAC` file wrapper in → §8.3.6. The runner that executes it is → §8.3.3.

| Item | Rule | Source |
| --- | --- | --- |
| segments | types 1–4: event mask, functions, strings, opcodes; markers `F0`–`F6` | [bin] (protocol/gs2-client-vm.md#container-the-client-reads) |
| 4.2.0.8 weapons | `weblevels` `.code` by CRC32; no `GRESCR01`; 195 is a gani | [bin] (protocol/gs2-client-vm.md#how-4208-loads-a-weapon-or-a-class) |
| 5.x and 6.00 | `GRESCR01` cache; the wire header is unchanged from → §8.3.2 | [bin] (protocol/gs2-client-vm.md#script-cache) |
| 6.113 | no container and no opcode switch in the Windows listing. It adds nothing past 6.00's cases 54 and 121 and folds 234–242, and it cannot show whether 48 and 49 returned | [bin] (protocol/gs2-6113.md#what-6113-cannot-show) |
| unpacked 6.1.1.3 | the switch is present and adds no case past that 6.00 set; 48 and 49 stay absent (→ §8.4.4) | [bin] (protocol/gs2-unpacked-6113.md#what-the-dispatcher-adds-past-600) |
| compiler lead | the MPL-2.0 checklist in → §8.3.6, compared with these clients | [doc] (protocol/gs2-client-vm.md#compiler-and-builtins) |

The opcode names, the peephole, and the bytes the client runs which that compiler does not emit stay in the note [bin] (protocol/gs2-client-vm.md#what-differs). The effect of each of those bytes is [bin] (protocol/gs2-client-only-opcodes.md).

#### Linux 4.20r6: the container reader

[bin] The r6 reader uses big-endian four-byte framing/directory numbers and NUL-terminated names. Removing a leading `public.` marker and forwarding a flag does not define runtime visibility. Markers 240–242 select string entries (one/two-byte unsigned indexes; four-byte form checks nonnegative representation); 243–245 supply signed integers; 246 uses the selected numeric-text wrapper described below. Other bytes append tagged records; marker branches modify the latest record. Corpus controls do not cover multiple-marker overwrite, and strict validator rejection is not native bounds/default behavior. [bin] (client-internals/linux-420r6-reader-fusion.md)

[bin] The marker-246 wrapper has separate empty/lowercase `true`/`false` branches, exact lowercase `0x` unsigned-32-bit base-16 conversion, and general library floating conversion. No end-pointer/consumed-length or range-error check establishes full-text validity. Ordered nonzero results pass; zero/unordered results enter fallback, preserving only exact `0`/`0x0` and otherwise yielding minus one, assuming normal floating comparison completion. Text extraction advances past its NUL independently of numeric parsing; a prior record receives the numeric result when present. Loaded-library/environment grammar, floating exception state, buffer/sentinel safety, malformed inputs and public-call runtime behavior remain open. [bin] (client-internals/linux-420r6-reader-fusion.md#selected-numeric-text-wrapper-2026-11-22)

#### Windows 5.00r7: segment words and four authored vectors

[bin] The 5.00r7 backup engine's script setter reads the segment type and length as ordinary big-endian 32-bit words, not the printable packet integers. A `public.` prefix in the function table sets visibility 1 and `publicsoap.` sets visibility 2; the default is 0. Visibility 2 is stored metadata and does not show a callable SOAP service. [bin] (client-internals/windows-404r2-500r7-static-2026-11-09.md#500r7-script-container-and-cache)

[inf] Four hand-written vectors make the layers testable without an original payload. A weapon request is logical 158 with the name; a class request is logical 161 with the stored-body CRC as five offset-integer bytes and then the name; `00 00 00 01 00 00 00 04 00 00 00 01` is a container with only an event mask, so nothing in it can run; and a 4.04r2 GS1 `setstring client.` flag should leave as logical 18. These are predictions from the static reading, before outer framing and encryption. None was captured or sent to a client. [inf] (client-internals/windows-404r2-500r7-static-2026-11-09.md#four-authored-vectors-for-these-boundaries)

## 8.4.3 OpenGS1 bytecode (reference reimplementation)

OpenGS1 defines a stack-based bytecode VM for GS1 [src] (protocol/graphics-movement-bytecode.md#scripting--gs1-bytecode). It is an independent reimplementation: 2.05 does not share its opcode set and does not run bytecode at all [2.05] (npc-library/gs1-reference-205.md#execution-model-205). No official client reads it, 3.153 included (see the settled question below).

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


**Settled question, formerly E#208: What the OpenGS1 opcode set describes.** Whether OpenGS1's layout describes any official bytecode was open; 4.2.0.8 and later were known to use the four-segment container, but 3.153, the first client that handles 131, had not been read. A read of the 3.153 Mac client settled it [bin] (client-internals/static-reads-appendix-e-2026-11-20-h.md#the-3153-script-container-e208).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | 3.153 reads the four-segment container of → §8.4.2: big-endian 32-bit type and length per segment, stop outside 1 to 4; 1 the event mask, 2 the function table (code position, zero-terminated name, `public.` stripped and flagged), 3 the string table, 4 the instructions with operand markers `F0`–`F2` (string index), `F3`–`F5` (signed number) and `F6` (number as text) | [bin] (client-internals/static-reads-appendix-e-2026-11-20-h.md#the-reader) |
| Settled | 3.153 also writes the same container from a script in memory, choosing the smallest operand form that fits; whether it compiles source was not traced | [bin] (client-internals/static-reads-appendix-e-2026-11-20-h.md#the-writer) |
| Verdict | Verified by read on 3.153; the best guess holds: OpenGS1 describes only itself, and the container dates from the first bytecode client | [bin] (client-internals/static-reads-appendix-e-2026-11-20-h.md#what-this-settles) |
| Left over | 3.153's opcode switch and whether it folds | [inf] (client-internals/static-reads-appendix-e-2026-11-20-h.md#not-covered) |

## 8.4.4 Dispatch by build

Each build guards its opcode dispatch over its own range, and the range grows with the engine: Linux 4.04r2 ends at 190, both Linux 4.20 revisions guard through 233, and the three Linux 6.x inputs map a prefix through 242. [bin] (client-internals/linux-404r2-vm-dispatch.md#earlier-dispatch-boundary); [bin] (client-internals/linux-cross-version-dispatch.md) The selectors above the serialized range are fused internal tags made after loading (→ §8.4.6), so they are not wire bytes. [bin] (client-internals/linux-420r6-reader-fusion.md)

#### Linux 4.04r2

The Linux 4.04r2 bytecode dispatch table was read exactly. Each row gives one observation and its limit [bin] (client-internals/linux-404r2-vm-dispatch.md#earlier-dispatch-boundary).

| Item | Exact-build observation | Limit | Source |
| --- | --- | --- | --- |
| Dispatch table | Range ends at 190; 191 indexed slots, of which 119 select a non-skip path; slot 11 selects the common skip path | Later fused-opcode range is outside this table; helper semantics not all recovered | [bin] (client-internals/linux-404r2-vm-dispatch.md#earlier-dispatch-boundary) |
| Extracted stream coverage | Every opcode in fourteen recovered streams selects a non-skip slot | Does not establish execution of every stream | [bin] (client-internals/linux-404r2-vm-dispatch.md#earlier-dispatch-boundary) |
| Slot-11 insertion control | Tested event order and completion are unchanged | One context; later Windows wait behavior is not assigned to this value | [cap] (client-internals/linux-404r2-vm-dispatch.md#earlier-dispatch-boundary) |
| Static frame helper | Depth guard, overrun path, frame-like allocation, prior-position save, push and active-state change | Field meanings remain inferred; no successful new live stop confirms this helper | [bin] (client-internals/linux-404r2-vm-dispatch.md#guarded-frame-transition) |

Later-build opcode and frame descriptions retain their own identities. Unrecovered helpers and correspondence remain open → App. E#207. [bin] (client-internals/linux-404r2-vm-dispatch.md#version-and-semantic-limits)

#### Linux 4.20 and 6.x

[bin] Both 4.20 revisions guard selectors through 233 (234 positions: 80 common fallback and 154 other targets), compared with 4.04's range through 190. The three 6.x inputs share executable-target sets and cache native destinations per decoded instruction. Their inspected prefix through 242 has 167 executable-mapping pointers and 76 zeros; a 243-entry extent is inferred. Adjacent non-code data/zeros are not safe no-ops, and internal selectors are not automatically wire bytes. [bin] (client-internals/linux-cross-version-dispatch.md)


[cap] Five unchanged startups reach executor entry, without hitting the new frame candidates. Three separate 6.x captures each single-step one selector-23 cached jump after its cached/static/register destinations agree. Termination follows the jump; handler completion and event scheduling are unmeasured. Eight untruncated captures retain identity and verify owned cleanup, with no server. E#207 remains partial. [cap] (client-internals/linux-cross-version-dispatch.md)

#### Unpacked Windows 6.1.1.3

The unpacked Windows 6.1.1.3 image walks the same four segment types and stores a decoded instruction in 24 bytes. Operand markers `F0`–`F6` keep the 6.00 widths. The dispatcher adds no case past 242. Cases 54, 121 and folds 234–242 are present. Cases 48 and 49 are not. A `.code` file of at least eight bytes is accepted when the magic is `GRESCR01`, the cache flag is 1, and the CRC32 of the bytes after the magic matches. [bin] (protocol/gs2-unpacked-6113.md#container); [bin] (protocol/gs2-unpacked-6113.md#what-the-dispatcher-adds-past-600); [bin] (protocol/gs2-unpacked-6113.md#script-cache)

| Rule | Builds | Source |
| --- | --- | --- |
| A `.code` file shorter than eight bytes is rejected. The magic is `GRESCR01`, and the CRC32 covers the bytes after those eight | 6.1.1.3 | [bin] (client-internals/gs2-6113.md#load-path-and-the-code-cache) |
| The dispatcher has 152 cases, from 11 through 242, with no case 48, 49 or 200. Cases 54, 121, 201–242 are present. Unpacked 6.037 has the same set | 6.1.1.3, 6.037 | [bin] (client-internals/gs2-6113.md#opcode-range) |
| Those cases include the opcodes the Preagonal compiler does not emit. A full builtin table was not extracted | 6.1.1.3 | [bin][doc] (client-internals/gs2-6113.md#against-preagonal) |

#### Mac OS X 6.11r1

The Mac 6.11r1 runner was read on its own, so the paragraph and table below describe that one input. It runs decoded 40-byte records rather than the serialized bytes, and each record caches its native handler, so a handler jumps straight to the next one. A preparation pass appends opcode 164 as an end marker. The table was read through a 256-entry window whose entries 243 and 244 are zero; its true length is unknown. [bin] (client-internals/mac-611r1-gs2-runner.md#decoded-records-and-dispatch)

The table lists only the behaviours that were read handler by handler; it is not an opcode map, and the opcode-7 handler is still unread. [bin] (client-internals/mac-611r1-gs2-runner.md#the-handlers-that-were-read)

| Item | Mac 6.11r1 observation | Source |
| --- | --- | --- |
| read handlers | 0 fall through, 1 jump, 2 numeric branch and pop, 6 call, 8 sleep, 9 loop check, 11 wait for, 20 number, 21 string, 24 one, 27 pi, 164 end marker | [bin] (client-internals/mac-611r1-gs2-runner.md#the-handlers-that-were-read) |
| loop check | default limit 10000, overridable from the owner's context; the counter lives on the opcode-9 record and resets with recompilation; no general per-instruction fuel was found | [bin] (client-internals/mac-611r1-gs2-runner.md#the-loop-check) |
| sleep and waitfor | snapshot of function, index, stack, frames and object context; the deadline is the manager's clock plus the delay; status 2 after the snapshot | [bin] (client-internals/mac-611r1-gs2-runner.md#sleep-and-waitfor) |
| call | arguments run down to the tag-0 marker; access and parameter count are checked; can suspend on `classesdownloaded` and retry the call | [bin] (client-internals/mac-611r1-gs2-runner.md#calls) |
| status | 0 normal end, 1 missing prerequisites or failed loop check, 2 suspension | [bin] (client-internals/mac-611r1-gs2-runner.md#runner-status) |

Nothing was run in a guest, so the clock's unit, the order of due snapshots and the native call interface are open (→ App. E#207). [bin] (client-internals/mac-611r1-gs2-runner.md#limits)

#### Case sets across the readable builds

One static pass read the dispatcher of every readable client VM, Windows 4.03r3 to 7.12.43, Linux 6.x x64 and Android Classic 1.8 and 2.2, and lists the opcodes each one runs [bin] (protocol/gs2-opcode-table.md#case-sets).

| Builds | Cases | Change from the row above | Source |
| --- | ---: | --- | --- |
| 4.03r3, 4.04r2, 4.11 | 119 | base set: 1–10, 20–27, 30–47, 50–53, 60–104, 110–120, 130–142, 150, 151, 163, 180–184, 189, 190 | [bin] (protocol/gs2-opcode-table.md#case-sets) |
| 4.20r8 | 154 | adds 11 (`waitfor`) and the folds 200–233 | [bin] (protocol/gs2-opcode-table.md#case-sets) |
| 5.00r7, 5.12 | 158 | adds 48, 49, 54 and 121 (from the earlier export reading; the shipped DLLs were not re-read) | [bin] (protocol/gs2-opcode-table.md#case-sets) |
| 5.30r3 to 6.1.1.3, 7.12.43, Android 1.8 and 2.2 | 165 | drops 48 and 49; adds the folds 234–242, which are already in 5.30r3 | [bin] (protocol/gs2-opcode-table.md#case-sets) |
| Linux 6.x x64 (June 2011 beta, November 2011, 6.03r7) | 167 | the 165 above, plus 0 (a plain step to the next instruction) and 164 | [bin] (protocol/gs2-opcode-table.md#case-sets) |

| Rule | Builds | Source |
| --- | --- | --- |
| 4.03r3 to 4.20r8 fill a table of opcode names, one ordinary word per byte (`add`, `sin`, `less`), at start-up; 5.x and later images carry no names. The table also names seven bytes no dispatcher runs: 160–162 and 185–188 | 4.03r3–4.20r8 | [bin] (protocol/gs2-opcode-table.md#the-clients-own-names) |
| The Linux x64 builds resolve each decoded instruction to a handler address at load time and jump from handler to handler; an opcode with no handler stores a null address with no guard found, so an unknown byte is unsafe there rather than a skip | Linux 6.x x64 | [bin][inf] (protocol/gs2-opcode-table.md#linux-uses-threaded-dispatch) |
| Opcode 164 switches to the next joined script that has instructions, or backs up and leaves the run loop; read as "continue in the next joined script"; no compiler is known to emit it | Linux 6.x x64 | [bin][inf] (protocol/gs2-opcode-table.md#opcode-164-on-linux) |
| The decoded instruction is 24 bytes on Windows 4.2.0.8 to 6.1.1.3, 40 bytes on Linux x64, 7.12.43 and Android 2.2, and 20 or 32 bytes on Android 1.8 x86 or x86_64; none of this is in the byte stream | per build | [bin] (protocol/gs2-opcode-table.md#linux-uses-threaded-dispatch) |

A compiler that must run on every client from 4.03r3 follows four rules [bin][cap] (protocol/gs2-opcode-table.md#for-a-compiler-and-a-vm).

| Rule | Source |
| --- | --- |
| Do not emit 11 (`waitfor`); it is not dispatched before 4.20r8 | [bin] (protocol/gs2-opcode-table.md#for-a-compiler-and-a-vm) |
| 48 and 49 run only on 5.00r7 and 5.12, and 54 and 121 only from 5.00r7; emitting any of them breaks 4.x | [bin] (protocol/gs2-opcode-table.md#for-a-compiler-and-a-vm) |
| on 5.00r7, 54 consumes object, member name and value (pushed in that order); 49 builds its list in reverse push order; 48 takes name/value pairs (name pushed first) but keeps taking them until two or fewer values remain, whatever its count (→ App. E#209) | [bin] (client-internals/static-reads-appendix-e-2026-11-20-b.md#gs2-opcodes-48-49-and-54-on-500r7-e209) |
| 0, 160–162, 164 and 185–188 are never portable | [bin] (protocol/gs2-opcode-table.md#for-a-compiler-and-a-vm) |
| The folds 200–242 are made by each client after decode; a compiler never writes them | [bin][cap] (protocol/gs2-opcode-table.md#for-a-compiler-and-a-vm) |

Mapped onto the GS2 features a 2016–2019 server backup uses, only `waitfor` needs a VM newer than 4.03r3; the rest compile to the 119-case base set, so what limits such scripts on old clients is the command library behind opcode 6, not the opcode set [bin][inf] (protocol/gs2-opcode-table.md#delteria-2019-features-by-opcode). The Linux 6.x x86 dispatcher, the ARM-only Android builds and each handler's effect on 5.30r3 and 7.12.43 are still unread → App. E#207 [bin] (protocol/gs2-opcode-table.md#still-open).

## 8.4.5 Built-in names in unpacked 6.1.1.3 and 6.0.3.7

Both unpacked images store the eighteen math names `abs`, `atan`, `atan2`, `ceil`, `cos`, `floor`, `log`, `max`, `min`, `pi`, `pow`, `random`, `round`, `sin`, `sqrt`, `sqrt1_2`, `sqrt2` and `tan`. [bin] (client-internals/gs2-builtins-6113.md)

Of the names Preagonal's compiler turns into opcodes, these images contain `abs`, `cos`, `log`, `max`, `min`, `pow`, `random`, `sin`, `format` and `sleep`. They do not contain `arctan`, `exp`, `vecx`, `vecy`, `arraylen` or `tokenize`. [bin][doc] (client-internals/gs2-builtins-6113.md)

`putcomp` and `putnewcomp` are in 6.0.3.7 and not in 6.1.1.3. `setprotocol`, `sendraw` and `senddata` are in 6.1.1.3 and not in 6.0.3.7, and so are the cipher names the connector script calls: `aes_encrypt`, `aes_decrypt`, `des_encrypt`, `des_decrypt`, `rc4_cipher`, `rsa_encrypt`, `rsa_decrypt`, `rsa_sign`, `rsa_verify` and `sha256` (→ §2.10). 6.1.1.3 also stores the movie-clip names `gotoandplay`, `gotoandstop`, `attachmovie` and `stop`; 6.0.3.7 has `gotoandplay`. [bin] (client-internals/gs2-builtins-6113.md)

#### The 6.01 registration tables

The 6.x client fills its script library at start-up from static tables, one row per built-in. A function row gives the name, a return-type letter and one letter per parameter (`i` integer, `u` unsigned, `d` and `f` numbers, `b` boolean, `s` string, `o` object, `X` any further arguments); a property row gives the name, a type letter, and whether it can be written. Each table goes either into the global registry or onto a class. Read from Linux 6.01r1, the full lists are in the source note [bin] (client-internals/gs2-builtins-601-registry.md#counts).

| Group | Tables | Entries | Source |
| --- | ---: | ---: | --- |
| Global functions | 32 | 314 | [bin] (client-internals/gs2-builtins-601-registry.md#global-functions-314) |
| Global properties | 16 | 123 | [bin] (client-internals/gs2-builtins-601-registry.md#global-properties-123) |
| Class members | 146 (141 on 91 named classes, 5 unnamed) | 1,284 | [bin][inf] (client-internals/gs2-builtins-601-registry.md#members-by-class) |

The class of each table is inferred from the class name used next to its registration call. What each built-in does is not read; only names and types are (→ App. E#207) [inf] (client-internals/gs2-builtins-601-registry.md#not-covered).

## 8.4.6 Load-time stages and fusion

#### Linux 4.20r6: post-load fusion


[bin] A jump-index pass and adjacent-pattern fusion rewrite selected records to internal tags 200–233 while retaining collection positions and advancing past matches; a current first tag 11 stays unchanged. This explains a corpus maximum of 189 alongside a larger internal range, without asserting transmitted fused values or a recovered compiler. Offline review runs no client/server. Malformed-input behavior, numeric grammar and public/joined semantics remain open in E#207. [bin] (client-internals/linux-420r6-reader-fusion.md)

#### The folds by build, and fold 241

The folds are made by the client after decoding, so a compiler never writes them (→ §8.4.4). A checklist of folds 200 to 242 against stock 4.20r8, 5.00r7 and 6.00, and against the published open reimplementation's fuse table, found one difference [bin][doc] (protocol/gs2-fold-241-2026-11-16.md#version-gate).

| Build | Folds the stock client makes | Source |
| --- | --- | --- |
| 4.20r8 | 200 to 233: all 34 arithmetic, boolean, compare and register-load folds | [bin] (protocol/gs2-fold-241-2026-11-16.md#200233) |
| 5.00r7 | 200 to 233; none of 234 to 242 | [bin] (protocol/gs2-fold-241-2026-11-16.md#version-gate) |
| 6.00r2, 6.00r4 | 200 to 242 | [bin] (protocol/gs2-fold-241-2026-11-16.md#version-gate) |

Fold 241 is the one the open reimplementation leaves out. Stock 6.00 makes it when a name load is followed by a call, `setreg` or `makeprop` and the name is a flagged entry of the global builtin registry; the entry is then kept on the instruction. A VM that runs the same sequence unfused gets the same result, so the gap affects speed, not behaviour, as far as is known. [bin][inf] (protocol/gs2-fold-241-2026-11-16.md#234242-600)

**Settled question, formerly E#211: Which objects make 6.00 fuse fold 241.** Which registry entries carry the flag was not read, so a clean-room VM could not decide when to fuse. A read of the registration tables in 6.00r2, 6.00r4, 6.01r1 Linux and 6.03r7 Windows settled it [bin] (client-internals/static-reads-appendix-e-2026-11-20-i.md#which-names-make-fold-241-e211).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | The flag is set only through the second of the two registration routines, from a per-row field. Seventeen global built-ins carry it: `disabledefmovement`, `disablemap`, `disablepause`, `disableselectweapons`, `disableweapons`, `enabledefmovement`, `enablefeatures`, `enablemap`, `enablepause`, `enableselectweapons`, `enableweapons`, `freezeplayer`, `noplayerkilling`, `onwall`, `onwall2`, `onwater` and `onwater2` | [bin] (client-internals/static-reads-appendix-e-2026-11-20-i.md#where-the-flag-comes-from) |
| Settled | The set is the same in 6.00r2, 6.00r4, 6.01r1 and 6.03r7. Script objects (weapons, NPCs, the player, controls) are not in the registry and never make 241 | [bin] (client-internals/static-reads-appendix-e-2026-11-20-i.md#by-build) |
| Verdict | Verified by read; the best guess (weapons and other globals that resolve once) was wrong. A clean-room VM can fuse 241 from a fixed list of these 17 names | [bin] (client-internals/static-reads-appendix-e-2026-11-20-i.md#what-this-settles) |
| Left over | Why these 17 are marked, and whether a script function of the same name would resolve differently unfused | [inf] (client-internals/static-reads-appendix-e-2026-11-20-i.md#not-covered) |

#### Linux 6.01 x86: decoded program and saved state

[bin] In the exact Linux 6.01r1 x86 review, the reader creates decoded records with initially empty native targets. A postpass constructs fused internal tags and caches a registry pointer on one selected path; the executor separately prepares jump targets and adds a termination record. These stages do not define new source-language or serialized opcodes. [bin] (client-internals/linux-601-x86-program-state.md).

[bin] Selected saved-state handling mixes copy, transfer and selective cloning, forms a deadline from a scripting clock plus positive input, and shows registration, first-match removal and replacement calls. Fresh typed holders may share string backing or copy pointer payloads; only selected references receive wrappers. The collection helper replaces destination storage with a shallow pointer-array copy on success; callers separately clear source containers. Destructive restore distinguishes holder, temporary-element and context-container cleanup. Selected frame retention uses exact pointer membership before attempting to append an absent frame. Dynamic reference/object ownership and allocation behavior remain open. The call-frame layout differs from 4.20; this is not a uniform deep-copy or portable snapshot contract. [bin] (client-internals/linux-601-x86-program-state.md).

[bin] Reload frees and rebuilds decoded records, discarding their embedded caches. Registry-reference rewriting, executor native-jump preparation and indexed numeric-payload reset have distinct fields and flag/lifetime paths; one must not be called the other's invalidation. The selected cached handler transports a registry pointer into a typed value before the next dispatch, without dereferencing it or invoking a callback in that block. Later consumers, registry ownership/removal and complete update contracts remain unbound. Trigger/restore execution, subscription lifetime, cancellation order, clock cadence and public results remain unproved; complete export delivery did not reconstruct the full indirect handler table. No new runtime result or cross-architecture equivalence follows. [bin] (client-internals/linux-601-x86-program-state.md#selected-ownership-and-cache-lifecycles-2026-11-22).

## 8.4.7 Scripts embedded in the Linux clients

#### Linux 4.04r2: embedded scripts and live linkage

Linux 4.04r2 carries scripts inside its executable. Each row gives one piece of evidence about them, what it showed and the limit of that reading [bin] (client-internals/linux-404r2-embedded-scripts.md#recovered-corpus-and-structural-checks).

| Evidence | Observation | Limit | Source |
| --- | --- | --- | --- |
| Bounded embedded-zlib extraction | Fourteen valid four-segment candidates, 129 named entries and 15,799 decoded instructions; instruction bytes round-trip and indexes are in range | Structural validation is not corpus-wide execution | [bin] (client-internals/linux-404r2-embedded-scripts.md#recovered-corpus-and-structural-checks) |
| Profile-script input | A corrected read of 9,530 live bytes matches the recovered payload digest; the same run enters the native executor | One loader/executor linkage, not all streams or complete profile execution | [cap] (client-internals/linux-404r2-embedded-scripts.md#one-payload-linked-to-execution) |
| Native reader/writer recovery | Operations available for focused review | Does not itself supply a full format specification | [bin] (client-internals/linux-404r2-embedded-scripts.md#recovered-corpus-and-structural-checks) |

The wrong-representation hash attempt remains superseded; only the corrected read supplies the match. Historical server-delivered content, cross-platform equivalence and 3D gameplay are not established. Remaining container/execution questions → App. E#207. [cap] (client-internals/linux-404r2-embedded-scripts.md#one-payload-linked-to-execution); [bin] (client-internals/linux-404r2-embedded-scripts.md#boundary)

#### Across Linux builds

[bin] Bounded extraction finds 14 containers in 4.04r2, 13 in each 4.20 revision and each 6.01 architecture, and 12 in 6.03r7 x64. The 4.20 pair and 6.01 architecture pair each agree on all 13 inflated payloads; 6.03 is an exact subset of 6.01. Its missing scanned payload has nine entries and 247 instructions, without proving feature removal. Five payloads match between 4.04 and 4.20. [bin] (client-internals/linux-cross-version-embedded-controls.md)


[bin] Entry/instruction totals are 119/15,208 for each 4.20 corpus, 55/5,053 for each 6.01 corpus and 46/4,806 for 6.03. All 78 occurrences validate four unique segments numbered 1–4, candidate entry/string bounds and exact instruction-byte reconstruction; maximum observed tag is 189. Neither 3.04 duplicate yields an accepted bounded zlib stream. Roster alignment remains a candidate comparison. Extraction runs no client/server and proves neither execution nor native semantic equivalence; E#207 remains partial. [bin] (client-internals/linux-cross-version-embedded-controls.md)

## 8.4.8 Network GS2 on Linux 6.03

[lab][cap] Three exact Linux 6.03r7 x64 probes establish class parsing, explicitly registered weapon instruction execution and later continuation at the saved next position. The proxy-origin bodies and corrected descriptor-length boundary are independently reviewed. This is not normal server compiler/writer validation, a script return-value oracle, exact sleep timing, cache-hit proof or rendered gameplay. [lab][cap] (protocol/linux-603-network-gs2.md).

## 8.4.9 The VM by client version, 3.153 to 6.03r7

Six VMs were read side by side: 3.153 and 4.20r6 (Mac PowerPC), 4.20r8 and 5.00r7 (Windows), 6.01r1 and 6.03r7 (Linux). Unread builds borrow the nearest read VM [bin][inf] (client-internals/gs2-vm-by-version.md). The per-build matrix is App. C.8. A later table adds the loader, the slots, event-name matching and the clock, and retires the loans for the builds that were read after this chapter: [bin][doc] (client-internals/gs2-vm-loader-diff.md). A compact quirks table restates those rows for era scripts and adds the Linux 6.03r7 timer ceil lab: [bin][lab][doc] (client-internals/gs2-vm-quirks-by-version.md).

A selected archive-labelled backup follow-up distinguishes counted-call adapters and formal binding from source evaluation order. Explicit WITH-end removes a context entry and recomputes outer context; frame destruction can instead invalidate matching references in place, while terminal cleanup clears the list. The label does not authenticate a distribution or establish runtime identity. A separate re-walk of nineteen official 6.113-era bodies found 524 normal closures but no early-exit discriminator; neither input establishes that the clean-room VM's unwind behavior matches native execution. G242/G303 remain partial. [bin][cap][inf] (client-internals/gs2-vm-from-engines.md#selected-backup-call-binding-and-context-cleanup-2026-11-22).

The same selected backup's native callback bridge uses twenty 32-bit cells, with an optional receiver consuming a cell and string-object returns adding a separate hidden result pointer. Numeric input pointers differ from by-value floating arguments; selected boolean/integer packing uses the epsilon-adjusted conversion. Floating/string return routes precede the word-result dispatch. The trailing-string forward helper doubles backslashes and double quotes, drops low control bytes and conditionally wraps the result; inverse parsing, callback reentry and ownership remain unestablished. Separately, the nineteen official bodies contain 1,786 operandless calls and 474 marker/formal-bind/save-stack prologues, including 34 temporary-member forms; their 484 function-table rows share those prologues. Neither observation establishes source evaluation order, complete argument semantics or a portable ABI. [bin][cap] (client-internals/gs2-vm-from-engines.md#selected-backup-call-binding-and-context-cleanup-2026-11-22).

The selected backup's cross-object scripted call uses a separate machine. Normal results are copied to the caller's marker; suspension additionally depends on a last-saved-state timestamp check, then snapshots and links a continuation. A later selected state execution can transfer that link through another suspension or prepare a result for restoration with the caller's saved context, subject to readiness and stack capacity. Null alone is not suspension, and the observed final caller-event callback does not establish its scheduling policy or event ordering. [bin] (client-internals/gs2-vm-from-engines.md#selected-backup-call-binding-and-context-cleanup-2026-11-22).

| Item | Rule | Source |
| --- | --- | --- |
| opcodes added | 104 object compare (4.20r6); 11 `waitfor` and the optimiser's 200–233 (4.20r8); 48, 49, 54, 121 (5.00r7); 0, 164 and 234–242, without 48 and 49 (6.x) | [bin] (client-internals/gs2-vm-by-version.md#opcodes-each-vm-handles) |
| unnamed opcodes | 45/46 store and load a local slot; 47 resolves a variable reference; 66/67 `&&`/`\|\|` as 1 or 0 with both sides evaluated; 121 adds or joins | [bin] (client-internals/gs2-vm-by-version.md#opcodes-the-open-compilers-do-not-name) |
| load-time optimiser | from 4.20r8, common sequences are fused into internal opcodes above 200 when a script loads; never in a file | [bin] (client-internals/gs2-vm-by-version.md#the-load-time-optimiser-420r8-on) |
| limits | value stack 256 (3.153), 10000 (4.x, 5.x), none (6.x); 10000 loop passes and call depth; `maxlooplimit` from 5.00r7 | [bin] (client-internals/gs2-vm-by-version.md#limits) |
| integer conversion | `floor(x + 0.0001)` in every VM | [bin] (client-internals/gs2-vm-by-version.md#maths-and-text) |
| `%`, `^`, shifts | the tolerance in `%` only in 4.20r6/4.20r8; `^ 0.5` is a square root in 4.x/5.x, `^ 2` is `a*a` from 5.24r4; positive `^ 0.5` is single precision on 6.03r7/6.01r1 and double on unpacked 6.1.1.3 and Mac 6.11r1; shift counts modulo 64 on PowerPC, 32 on x86 | [bin] (client-internals/gs2-vm-by-version.md#maths-and-text; client-internals/static-reads-appendix-e-2026-11-24-g082.md) |
| number to text | `"0"` under 0.0001; up to 9 truncated decimals, trailing zeros dropped, a trailing 999 carried up | [bin] (client-internals/gs2-vm-by-version.md#maths-and-text) |
| 6.03r7 timer | with Seihai-compiled GS2 bytecode on loopback, periods **ceil** to 50 ms; sub-0.05 fires at ~20/s (not the classic GS1 floor) | [lab] (client-internals/gs2-vm-quirks-by-version.md#linux-603r7-timer-lab) |
| event casing | schedule / cancel fold case; on 6.03r7 the function-table lookup for a fired event folds `A`–`Z` in both the hash and the comparison, so `onTimeout` and `onTimeOut` are one function; other builds not proven | [bin][lab][inf] (client-internals/gs2-vm-quirks-by-version.md#5-event-name-matching-ontimeout-vs-ontimeout); [bin] (client-internals/static-reads-appendix-e-2026-11-20-j.md#event-names-and-the-function-table-603r7) |
| loop-limit name | 6.00r2 to 6.03r7 keep the property name scrambled; it unscrambles to `maxlooplimit` | [bin] (client-internals/static-reads-appendix-e-2026-11-20-j.md#the-6x-loop-limit-name) |

Open: → App. E#209.

## 8.4.10 What official compiled bodies look like

Nineteen official GS2 bodies of the 6.113 era were walked offline, and a larger sample of 660 for one check. The bodies, keys and names stay private; only counts are published. These describe what the official compiler wrote, which a clean-room compiler can aim for; they do not show which compiler passes produced it [cap] (protocol/gs2-official-jump-narrow-returns-2026-11-16.md#on-the-19-official-6113-era-bodies).

| Check | Result on the official bodies | Source |
| --- | --- | --- |
| jumps whose target is an unconditional jump | 0 of 2239 | [cap] (protocol/gs2-official-jump-narrow-returns-2026-11-16.md#on-the-19-official-6113-era-bodies) |
| jumps whose target is any jump | 69, nearly all conditional to conditional; no Or to Or chains | [cap] (protocol/gs2-official-jump-narrow-returns-2026-11-16.md#on-the-19-official-6113-era-bodies) |
| integer markers | `F3` 5113, `F4` 3128, `F5` 19; none wider than its value needs, and all 19 `F5` loads need the width | [cap] (protocol/gs2-official-jump-narrow-returns-2026-11-16.md#on-the-19-official-6113-era-bodies) |
| string markers | `F0` 11251, `F1` 3045, `F2` none; none wider than needed | [cap] (protocol/gs2-official-jump-narrow-returns-2026-11-16.md#on-the-19-official-6113-era-bodies) |
| how a body ends | 18 of 660 bodies do not end in a return instruction (→ App. E#214) | [cap] (protocol/gs2-official-jump-narrow-returns-2026-11-16.md#enlarged-residual-bodies-that-do-not-end-in-a-return) |
| how a body begins | all 19 start with an unconditional jump to the end of the stream: a function-only image, with no top-level statements, whose named functions start at their function-table indices | [cap][inf] (protocol/gs2-official-function-only-shape-2026-11-16.md#observation) |
| non-ASCII strings | one body of 19 has a high byte in its string segment: *Français* stored with the single byte `0xE7` for ç, which is Latin-1 or Windows-1252, not UTF-8 | [cap] (protocol/gs2-official-strings-latin1-2026-11-16.md#official-segment-3-bytes) |

The rules below say what follows for a client and a compiler, and where the evidence stops [cap][inf] (protocol/gs2-official-jump-narrow-returns-2026-11-16.md#enlarged-residual-bodies-that-do-not-end-in-a-return).

| Rule | Source |
| --- | --- |
| Clean output is consistent with a jump-threading and marker-narrowing pass, but careful emitting alone gives the same stream, so the official compiler's passes are not known. Open compilers' test baselines do leave jump-to-jump chains and wide `F4` markers | [cap][inf] (protocol/gs2-official-jump-narrow-returns-2026-11-16.md#enlarged-residual-bodies-that-do-not-end-in-a-return) |
| On 4.20r8 and 5.12 a function-only image (leading jump to the end) never runs a top level, and an image with top-level code runs it before `onCreated` and again before every later event; 6.03r7 was not run (→ §8.3.4, §8.4.10) | [lab] (protocol/lab-appe-hosta-2026-11-20.md#gs2-top-level-pass-e212) |
| The 5.00r7 and 6.03r7 clients draw text through the Windows ANSI path, with no UTF-8 literal in the scanned 5.00r7 engine, so on a Western European Windows the Latin-1 bytes above draw as the expected letters. The classic French language packs use the same single-byte letters. On another code page the same bytes draw differently; 5.00r7 is measured below | [bin][file][inf] (protocol/gs2-official-strings-latin1-2026-11-16.md#focus-client-text-path-500r7--603r7) |

**Settled question, formerly E#213: How GS2 text bytes draw on screen.** Whether the clients draw official bytecode's single Latin-1 bytes as the intended letters was open. Lab runs on 5.00r7 under a Western code page settled it for that build [lab] (protocol/lab-appe-hostb-2026-11-20c.md#latin-1-text-on-500r7-e213); [lab] (protocol/lab-appe-hostb-2026-11-20d.md#latin-1-byte-231-in-showtext-and-a-sign-on-500r7-e213).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | 5.00r7 draws bytes 231, 233, 252 and 241 as ç, é, ü and ñ in chat, nicknames and GS2 `showtext`, including text built with `char(231)` on the client | [lab] (protocol/lab-appe-hostb-2026-11-20c.md#latin-1-text-on-500r7-e213); [lab] (protocol/lab-appe-hostb-2026-11-20d.md#latin-1-byte-231-in-showtext-and-a-sign-on-500r7-e213) |
| Verdict | Verified for 5.00r7 on a Western code page; the best guess (bytes pass through the Windows code page) holds | [lab] (protocol/lab-appe-hostb-2026-11-20d.md#latin-1-byte-231-in-showtext-and-a-sign-on-500r7-e213) |
| Left over | A 6.x build, a sign on screen, and another code page; the lab server's GS1 translator and sign encoder garble non-ASCII bytes on their own, so use GS2 | [lab] (protocol/lab-appe-hostb-2026-11-20d.md#latin-1-byte-231-in-showtext-and-a-sign-on-500r7-e213) |

**Settled question, formerly E#212: Whether a function-only image skips the top-level pass.** Whether stock clients treat a leading jump to the end as "no top level", and re-run top-level code before every event when an image has some, was open; loopback fixtures settled it [lab] (protocol/lab-appe-hosta-2026-11-20.md#gs2-top-level-pass-e212).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | The 19 official bodies are all function-only; a Linux 4.04r2 experiment suggested a top-level re-run | [cap][lab] (protocol/gs2-official-function-only-shape-2026-11-16.md#what-this-does-and-does-not-settle) |
| Settled | On 4.20r8 and 5.12, with bytecode in 131: a script with a top level runs it before `onCreated` and again before every later `onTimeout`; its function-only twin never runs a top level | [lab] (protocol/lab-appe-hosta-2026-11-20.md#gs2-top-level-pass-e212) |
| Verdict | Verified on two builds; the best guess held on both counts | [lab] (protocol/lab-appe-hosta-2026-11-20.md#gs2-top-level-pass-e212) |
| Left over | 6.03r7, and a handler at instruction 0 | [lab] (protocol/lab-appe-hosta-2026-11-20.md#gs2-top-level-pass-e212) |


## 8.4.11 Undispatched bytes, raw folds and damaged containers (lab)

The script fuzz of → §8.3.10 also sent every byte that no compiler emits, the fold bytes written raw, and damaged containers. The tables give what each client did [lab] (protocol/script-fuzz-2026-11-19.md#gs2-what-each-undispatched-byte-does).

The separate 5.00r7 static study already describes 48's object construction and incrementing counter and 49's list construction. The retained backup-engine reread (`W500-OP48-49-REREAD-20261122`) corroborates those broad effects without independently rebinding the conversion constant or insertion target. These are static findings, not a completed runtime test or genuine 5.12 contract [bin] (protocol/gs2-client-only-opcodes.md#48-and-49-retained-500r7-backup-engine); [bin] (client-internals/static-reads-appendix-e-2026-11-20-b.md#gs2-opcodes-48-49-and-54-on-500r7-e209).

| Rule | 6.03r7 Linux | 5.24r4, 4.20r8 | Source |
| --- | --- | --- | --- |
| a byte with no handler | crashes the client about 0.2 s after the script starts: bytes 12–19, 28, 29, 48, 49, 55–59, 105–109, 122–129, 143–149, 152–162, 165–179, 185–188 and 191–199; the threaded dispatch has no guard in front of an empty handler slot | runs as a no-op through the switch default; a value pushed before it survives | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-what-each-undispatched-byte-does) |
| byte 0 | a no-op, even with an operand | as 6.03r7 | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-what-each-undispatched-byte-does) |
| byte 164 | halts the script, as "continue in the next script" would with no next script | as 6.03r7 | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-what-each-undispatched-byte-does) |
| after a lone push (5.24r4 / 4.20r8) | — | 46 (slot load) gives an empty value, 47 gives 0, 200–207, 224–230, 233–235 and 241 run with an empty value, 208–223, 231, 232, 240 and 242 halt; 236–239 halt on 5.24r4 and give an empty value on 4.20r8 | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-what-each-undispatched-byte-does) |

Compilers never write the fold bytes 200–242; each client creates them after decoding. Written raw after pushes of 3 and 4 with an operand of 2, they behave as below [lab] (protocol/script-fuzz-2026-11-19.md#gs2-the-fold-bytes-written-raw).

| Bytes | 6.03r7 | 5.24r4 | 4.20r8 | Source |
| --- | --- | --- | --- | --- |
| 200–207, 224–230, 233–235, 241 | run, empty value | same | same | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-the-fold-bytes-written-raw) |
| 208–215 | plain binary operations on the two values: 7 (add), −1 (sub), 12 (mul), 0.75 (div), 3 (mod), 81 (pow), 1, 1 | same | same | [lab][inf] (protocol/script-fuzz-2026-11-19.md#gs2-the-fold-bytes-written-raw) |
| 216–223 | halt | halt | halt | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-the-fold-bytes-written-raw) |
| 231, 242 | crash | the engine stops for good | halt (4.20r8 has folds only up to 233) | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-the-fold-bytes-written-raw) |
| 232 | halts; crashed once on a re-check | halts | halts | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-the-fold-bytes-written-raw) |
| 236–240 | halt | halt | 236–239 empty value, 240 halts | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-the-fold-bytes-written-raw) |

The rules below give the other crashes, stopped engines and container damage [lab] (protocol/script-fuzz-2026-11-19.md#gs2-crashes-and-dead-engines-outside-the-opcode-sweep).

| Rule | 6.03r7 | 5.24r4 | 4.20r8 | Source |
| --- | --- | --- | --- | --- |
| an operand marker `0xf7` to `0xff` where a second operand would be | crash | empty value | empty value | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-crashes-and-dead-engines-outside-the-opcode-sweep) |
| a marker `0xf3` to `0xf5` there | empty value | empty value | empty value | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-crashes-and-dead-engines-outside-the-opcode-sweep) |
| slot store (45) into slot 1024, 4000 or −1, then a load (46) | crash | the engine stops for good | 0 | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-crashes-and-dead-engines-outside-the-opcode-sweep) |
| object literal (48) with n = 1, value before name | crash | the engine stops for good | empty value | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-crashes-and-dead-engines-outside-the-opcode-sweep) |
| the code segment twice | the engine stops for good | silent | the engine stops for good | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-crashes-and-dead-engines-outside-the-opcode-sweep) |
| an unknown segment type first, or the segments in reverse order | silent | silent | silent | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-crashes-and-dead-engines-outside-the-opcode-sweep) |
| six single-byte flips in the code segment | crash | — | — | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-crashes-and-dead-engines-outside-the-opcode-sweep) |
| 1 or 5 bytes cut off a segment | runs | runs | runs | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-damaged-containers) |
| a jump target of 9999 or −1 | runs on | runs on | runs on | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-damaged-containers) |
| a string index past the string table | empty value | empty value | empty value | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-damaged-containers) |
| decimal text (F6) | read like C `atof`/`strtol`: `"0x10"` 16, `"12abc"` 12, `"1,5"` 1, `"  3"` 3, `""` 0; `-0`, `nan` and `1e-400` load as −1; NaN prints as `0.-000000000` | as 6.03r7, and `inf` loads as −1 | as 6.03r7, and big numbers clamp to 4294967295 (`"1e400"`, a long run of 9s, `99999999999`); `-2147483649` stays | [lab] (protocol/script-fuzz-2026-11-19.md#gs2-damaged-containers) |

Opcode by opcode, against the value a straightforward VM would give: 66 and 67 treat any text operand as true; 104 (object compare) on texts returns a byte difference like `strcmp` on 6.03r7 (`""` against `"x"` −120), mostly the plain result on 5.24r4, and 0.05 for any text on 4.20r8; 121 is a numeric add on 6.03r7 and 5.24r4, with a non-number counted as −1 (`"x"+2` is 1), and is not dispatched by 4.20r8; with 54 every push order leaves `this.k` at 0 on 6.03r7 and 5.24r4, and 4.20r8 does not dispatch it; a slot store of 9, a pop, then a slot load reads back 0 for slots 0, 1, 5 and 1023, likely because a function's slots exist only once its own code sets them up [lab][inf] (protocol/script-fuzz-2026-11-19.md#gs2-value-rules-that-differ-from-seihais-vm).

## 8.4.12 Opcode names by byte

The table gives every opcode byte that any client names or dispatches, with the client's own name for it, and whether each build has a case for it (→ §8.4.4). "yes" means the build has a case, or a handler on Linux, and "·" means it does not. Note ¹: 11 is unnamed and not dispatched on 4.03r3 to 4.11. Note ²: the folds are named in 4.20r8 only; they are made after decode and never appear in a byte stream, and 234 to 242 have no name in any table. In the compiler column, **yes** means a recorded emitter in the MPL-2.0 compiler, **no** a recorded absence, and **?** that neither is recorded [bin] (protocol/gs2-opcode-table.md#the-table).

| Byte | Client name | 4.03r3–4.11 | 4.20r8 | 5.00r7, 5.12 | 5.30r3–6.113, 7.12.43, Android | Linux 6.x x64 | Preagonal compiler | Source |
| ---: | --- | :---: | :---: | :---: | :---: | :---: | :---: | --- |
| 0 | `noop` | · | · | · | · | yes | ? | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 1 | `jump` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 2 | `jumptrue` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 3 | `sjumptrue` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 4 | `jumpfalse` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 5 | `sjumpfalse` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 6 | `call` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 7 | `return` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 8 | `sleep` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 9 | `loopcheck` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 10 | `savestackpos` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 11 | `waitfor` ¹ | · | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 20 | `loadfloat` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 21 | `loadstring` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 22 | `loadmember` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 23 | `stackmark` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 24 | `loadtrue` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 25 | `loadfalse` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 26 | `loadnull` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 27 | `loadpi` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 30 | `dupe` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 31 | `swap` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 32 | `pop` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 33 | `makefloat` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 34 | `makestring` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 35 | `makemember` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 36 | `makeobject` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 37 | `makearray` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 38 | `initarray` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 39 | `setarray` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 40 | `setmember` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 41 | `makevar` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 42 | `createobject` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 43 | `makeoldscriptvar` | yes | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 44 | `convertbool` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 45 | `setreg` | yes | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 46 | `getreg` | yes | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 47 | `makeprop` | yes | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 48 | (none) | · | · | yes | · | · | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 49 | (none) | · | · | yes | · | · | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 50 | `assign` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 51 | `massassign` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 52 | `inc` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 53 | `dec` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 54 | (none) | · | · | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 60 | `add` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 61 | `sub` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 62 | `mul` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 63 | `div` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 64 | `mod` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 65 | `pow` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 66 | `and` | yes | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 67 | `or` | yes | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 68 | `not` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 69 | `negative` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 70 | `equal` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 71 | `nequal` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 72 | `less` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 73 | `greater` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 74 | `lessequal` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 75 | `greaterequal` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 76 | `bitor` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 77 | `bitand` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 78 | `bitxor` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 79 | `bitinvert` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 80 | `inrange` | yes | yes | yes | yes | yes | ? | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 81 | `inarray` | yes | yes | yes | yes | yes | ? | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 82 | `indexof` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 83 | `type` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 84 | `format` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 85 | `int` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 86 | `abs` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 87 | `random` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 88 | `sin` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 89 | `cos` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 90 | `arctan` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 91 | `exp` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 92 | `log` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 93 | `min` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 94 | `max` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 95 | `getangle` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 96 | `getdir` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 97 | `vecx` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 98 | `vecy` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 99 | `indicesof` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 100 | `link` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 101 | `shl` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 102 | `shr` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 103 | `char` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 104 | `compare` | yes | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 110 | `trim` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 111 | `length` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 112 | `pos` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 113 | `app` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 114 | `charat` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 115 | `substring` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 116 | `beginswith` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 117 | `endson` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 118 | `tokenize` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 119 | `translate` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 120 | `positions` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 121 | (none) | · | · | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 130 | `arraysize` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 131 | `getarraycell` | yes | yes | yes | yes | yes | ? | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 132 | `setarraycell` | yes | yes | yes | yes | yes | ? | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 133 | `getarraycell2` | yes | yes | yes | yes | yes | ? | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 134 | `setarraycell2` | yes | yes | yes | yes | yes | ? | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 135 | `subarray` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 136 | `arrayadd` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 137 | `arraydelete` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 138 | `arrayremove` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 139 | `arrayreplace` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 140 | `arrayinsert` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 141 | `arrayclear` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 142 | `expandarray` | yes | yes | yes | yes | yes | ? | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 150 | `with` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 151 | `popwith` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 160 | `goto` | · | · | · | · | · | ? | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 161 | `break` | · | · | · | · | · | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 162 | `continue` | · | · | · | · | · | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 163 | `foreach` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 164 | (none) | · | · | · | · | yes | ? | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 180 | `loadthis` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 181 | `loadthiso` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 182 | `loadplayer` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 183 | `loadplayero` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 184 | `loadlevel` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 185 | `loadserver` | · | · | · | · | · | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 186 | `loadserverr` | · | · | · | · | · | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 187 | `loadclient` | · | · | · | · | · | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 188 | `loadclientr` | · | · | · | · | · | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 189 | `loadtemp` | yes | yes | yes | yes | yes | yes | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 190 | `loadparams` | yes | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 200 | `addfloat` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 201 | `subfloat` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 202 | `mulfloat` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 203 | `divfloat` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 204 | `modfloat` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 205 | `powfloat` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 206 | `andfloat` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 207 | `orfloat` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 208 | `addassign` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 209 | `subassign` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 210 | `mulassign` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 211 | `divassign` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 212 | `modassign` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 213 | `powassign` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 214 | `andassign` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 215 | `orassign` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 216 | `addfloatassign` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 217 | `subfloatassign` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 218 | `mulfloatassign` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 219 | `divfloatassign` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 220 | `modfloatassign` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 221 | `powfloatassign` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 222 | `andfloatassign` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 223 | `orfloatassign` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 224 | `lessfloat` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 225 | `greatorfloat` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 226 | `lessequalfloat` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 227 | `greaterequalfloat` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 228 | `getregfloat` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 229 | `getregstring` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 230 | `getregobject` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 231 | `getregincpop` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 232 | `getregdecpop` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 233 | `getregdupe` ² | · | yes | yes | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 234 | (none) | · | · | · | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 235 | (none) | · | · | · | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 236 | (none) | · | · | · | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 237 | (none) | · | · | · | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 238 | (none) | · | · | · | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 239 | (none) | · | · | · | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 240 | (none) | · | · | · | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 241 | (none) | · | · | · | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
| 242 | (none) | · | · | · | yes | yes | no | [bin] (protocol/gs2-opcode-table.md#the-table) |
