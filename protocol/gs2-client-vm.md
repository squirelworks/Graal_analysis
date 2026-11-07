# GS2 client VM

Date: 2026-11-07. Tags as in `README.md`.

What a graal-client-repro client and a Seihai script VM can share: the bytecode container, the opcodes the clients dispatch, the names those clients give the opcodes, and how a weapon or class script is loaded. No compiler source is copied. No Rust crate is started here.

Linux 3.04 is TorqueScript plus GS1 on `GuiGraalCtrl`. It is not this VM, and none of its opcodes are listed below. **[bin]** (`torque/engine-304.md`, `manual/08-scripting/03-gs2-language.md`)

`shanalysis` and `gs2-parser` are not checked out under `/agent`. The compiler checklist is the MPL-2.0 Preagonal trees only, plus the study of those trees already on main.

## Compiler and builtins

The compiler and its companion VM are summarised in `npc-library/preagonal-gs2.md`. That note is a third-party reading. It is not a client. This section is only the checklist the client sections are compared with. **[doc]**

Trees, both SPDX `MPL-2.0`: [Preagonal.Scripting.GS2Compiler](https://github.com/Preagonal/Preagonal.Scripting.GS2Compiler) at `7878bc5` and [Preagonal.Scripting.GS2Engine](https://github.com/Preagonal/Preagonal.Scripting.GS2Engine) at `f8b5f13`. There is no type named `GS2Bytecode` or `GS2BuiltInFunctions` in either tree. The container writer is the private `BytecodeWriter` in `GS2Compiler.cs`. The builtin map is two dictionaries and two sets in the same file. The engine's names are `BytecodeSegment` and `Opcode`.

### Container the compiler writes

All multi-byte integers are big-endian. **[doc]** (`GS2Compiler.cs` `ToArray` and `WriteSegment`, lines 1855–1890; `npc-library/preagonal-gs2.md`)

Four segments, each a 32-bit type, a 32-bit byte length, then that many bytes, in this order, then one trailing newline byte (`0x0A`):

| Type | Body |
| --- | --- |
| 1 | one 32-bit word, always zero |
| 2 | function table: 32-bit op index, then a NUL-terminated name |
| 3 | NUL-terminated strings |
| 4 | opcodes |

An op index counts opcodes, not bytes. Operands are not opcodes. Marker `F0` / `F1` / `F2` is a string-table index of 8 / 16 / 32 bits. Marker `F3` / `F4` / `F5` is a signed integer of 8 / 16 / 32 bits. Marker `F6` is a NUL-terminated decimal. After a number-load or after opcode 1 or 2, the writer adds 3 to the marker so a small integer uses `F3`–`F5` rather than `F0`–`F2` (`EmitDynamicNumber`, lines 1841–1846).

With the header flag on (the default), the file starts with byte `0xAC`, a raw big-endian 16-bit length, and the ASCII `type,name,0,`, then the segments (`Header.Wrap`, lines 1914–1922). `0xAC` is 172, which is logical id 140 plus 32, the same bias 4.x uses for a packet id on the wire **[bin]** (`protocol/v4x-clients.md`). The length is not GSHORT. GSHORT is `(v >> 7) + 32` and `(v & 0x7F) + 32` **[srv]** (`protocol/codec-and-framing.md`). Packet 140's own body, once the frame has already carried the id, is a GSHORT header length and then the script **[srv]** (`protocol/packet-ids.md`, `manual/08-scripting/03-gs2-language.md`). The wrapper is a third layout: it puts the wire id in front of a raw 16-bit length and a header that stops at the save-to-disk field.

### Opcodes the compiler emits

The private `Op` enum is `GS2Compiler.cs` lines 2160–2275. The engine enum is `Opcode.cs` lines 3–126. Numbers both sides share, and the four the compiler emits which the engine enum does not name, are already listed in `npc-library/preagonal-gs2.md`. The engine enum's gaps are `waitfor` (11), inline conditional (44), bitwise xor (78), bitwise invert (79), and the two shifts (101, 102). The engine names `params` (190). The compiler's enum has no `params` opcode, so a source name `params` is an ordinary variable. **[doc]**

### Builtins the compiler turns into opcodes

Every other name is a call by opcode 6. Game commands stay in the string table. **[doc]** (`GS2Compiler.cs` lines 1612–1649 and the call emitter at 1239–1487; `npc-library/preagonal-gs2.md`)

| Names | Opcode |
| --- | --- |
| `sleep` | 8 |
| `waitfor` | 11 |
| `setarray` | 39 |
| `makevar` | 41 |
| `format` | 84 |
| `int` cast | 85 |
| `abs` | 86 |
| `random` | 87 |
| `sin`, `cos`, `arctan` | 88, 89, 90 |
| `exp`, `log`, `min`, `max` | 91–94 |
| `getangle`, `getdir` | 95, 96 |
| `vecx`, `vecy` | 97, 98 |
| `pow` | 65 |
| `char` | 103 |
| `arraylen`, `sarraylen`, and `size` | 130 |
| `trim`, `length`, `pos`, `charat`, `substring`, `starts`, `ends`, `tokenize`, `positions` | 110–112, 114–118, 120 |
| `subarray`, `add`, `delete`, `remove`, `replace`, `insert`, `clear` | 135–141 |
| `index`, `type`, `indices`, `link` | 82, 83, 99, 100 |

`_(...)` is opcode 119. `pi`, `this`, `thiso`, `player`, `playero`, `level`, and `temp` are their own opcodes (27, 180–184, 189). `sleep` and `setarray`, and the methods `clear`, `add`, `delete`, `insert`, `remove`, and `replace`, are marked non-returning so the compiler does not drop the result.

The compiler does not emit a peephole or a superinstruction. Opcodes 200 and above are not in its enum.
