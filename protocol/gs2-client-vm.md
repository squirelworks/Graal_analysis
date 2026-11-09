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

## The 4.2.0.8 VM

Read from the Windows 4.2.0.8 `GraalEngine.dll` export. Nothing was run. The script object is `TGraalScript`. The machine that steps it is `TScriptExecutionSpace`, holding a `TGraalVar` stack. **[bin]**

### Container the client reads

`setScript` walks the bytes as big-endian 32-bit words. A type outside 1–4, or a short read, ends the walk. The four types may arrive in any order. The compiler's order (1, then 2, then 3, then 4) is what it writes, not what the reader requires. A trailing `0x0A` is not a segment, so it ends the walk the same way a missing byte does. The `0xAC` wrapper is not stripped. A file that starts with that byte has a type word other than 1–4, and the reader stops with no instructions. **[bin]**

| Type | What 4.2.0.8 stores |
| --- | --- |
| 1 | one 32-bit word, kept as the script's event bit mask |
| 2 | function table: 32-bit op index, then a NUL-terminated name. A name that starts with `public.` loses those seven characters and is marked public |
| 3 | NUL-terminated strings |
| 4 | instructions |

Operands on a segment-4 opcode, big-endian, signed where the width is an integer: **[bin]**

| Marker | Payload | Stored as |
| --- | --- | --- |
| `F0` | unsigned 8-bit index | string from segment 3, type tag string |
| `F1` | unsigned 16-bit index | string, type tag string |
| `F2` | unsigned 32-bit index | string, type tag string |
| `F3` | signed 8-bit | number (a double) |
| `F4` | signed 16-bit | number |
| `F5` | signed 32-bit | number |
| `F6` | NUL-terminated decimal | number, via the float parser |

This is not GSHORT. A GSHORT reader will not recover a segment length or an operand. It is also not OpenGS1's layout (a body offset, then constant tables, then 4-byte packed values) in → §8.4.3. **[bin]** (`manual/08-scripting/04-gs2-bytecode.md`)

Each decoded instruction is a 24-byte record: the opcode, a type tag, a string, and a double. The record is not a 40-byte slot. **[bin]**

### Names the client gives the opcodes

4.2.0.8 fills a table, one string per opcode from 0, used as the instruction's own name. Empty slots are unnamed. A slot whose symbol is only a character or two is the operator spelling (`+`, `==`, and the rest) and is not given a long name. The long names that are present: **[bin]**

| Bytes | Client name | What the dispatcher does |
| --- | --- | --- |
| 2 | `jumptrue` | if the top number is not 0, set the program counter to the operand plus the current script piece's base, then pop |
| 3 | `sjumptrue` | if the top number is not 0, jump the same way and leave the value; if it is 0, pop and continue |
| 4 | `jumpfalse` | if the top number is 0, jump and pop; if it is not 0, pop and continue |
| 5 | `sjumpfalse` | if the top number is 0, jump and leave the value; if it is not 0, pop and continue |
| 7 | `return` | pop the call frame. A returned object that is the current object, or one of its sub-values, is cloned before the frame goes away |
| 8 | `sleep` | a positive number sets a timeout and saves the machine under the name `timeout`; anything else clears the show-timer |
| 9 | `loopcheck` | add 1 to a counter on the frame. Above 10000, record `Loop limit exceeded` and stop |
| 10 | `savestackpos` | store the current stack height on the frame. This is not a jump |
| 11 | `waitfor` | pop a number and two strings. When the first string is non-empty and the number is positive, register a catch for that event |
| 20–27 | `loadfloat`, `loadstring`, `loadmember`, `stackmark`, `loadtrue`, `loadfalse`, `loadnull`, `loadpi` | push that constant or name |
| 33–42 | `makefloat`, `makestring`, `makemember`, `makeobject`, `makearray`, `initarray`, `setarray`, `setmember`, `makevar`, `createobject` | convert, build, or store, matching those names |
| 43 | `makeoldscriptvar` | present. The compiler does not emit 43 |
| 44 | `convertbool` | the compiler's inline-conditional opcode, same number |
| 45–47 | `setreg`, `getreg`, `makeprop` | present. The compiler does not emit 45, 46, or 47 |
| 50–51 | `assign`, `massassign` | 50 is assignment. 51 is the compiler's end-of-parameters opcode; the client's name for that byte is `massassign` |
| 69 | `negative` | unary minus |
| 70–75 | `equal`, `nequal`, then the four comparisons | the less-than slot is a short symbol, not a long name |
| 76–79 | `bitor`, `bitand`, `bitxor`, `bitinvert` | bitwise |
| 80–82 | `inrange`, `inarray`, `indexof` | membership and index |
| 84 | `format` | format |
| 87, 90, 95, 96 | `random`, `arctan`, `getangle`, `getdir` | those functions. `sin`, `cos`, `exp`, `log`, `min`, `max`, `abs`, `vecx`, and `vecy` are the surrounding slots and are short symbols |
| 99 | `indicesof` | indices |
| 104 | `compare` | present. The compiler does not emit 104 |
| 111, 114–120 | `length`, `charat`, `substring`, `beginswith`, `endson`, `tokenize`, `translate`, `positions` | string operations. `beginswith` and `endson` are the client's names for the compiler's `starts` and `ends` |
| 130–142 | `arraysize`, `getarraycell`, `setarraycell`, `getarraycell2`, `setarraycell2`, `subarray`, `arrayadd`, `arraydelete`, `arrayremove`, `arrayreplace`, `arrayinsert`, `arrayclear`, `expandarray` | arrays, including the two-index forms |
| 151 | `popwith` | end of `with` |
| 163 | `foreach` | `for`-each |
| 180–184 | `loadthis`, `loadthiso`, `loadplayer`, `loadplayero`, `loadlevel` | those objects |
| 189–190 | `loadtemp`, `loadparams` | `temp` and `params`. The compiler does not emit 190 |

The same table names bytes the dispatcher does not implement: `break` (161), `continue` (162), `loadserver` (185), `loadserverr` (186), `loadclient` (187), `loadclientr` (188). A byte with no case falls out of the switch, calls one helper, and skips two further instruction slots. It is not run as that named operation. **[bin]**

Opcode 6 is the call. The name is the string on the stack. A failed call with a non-empty name is recorded as a script error. There is no second table of game-command opcodes. `showimg`, `hideimg`, `trigger`, and `settimer` are ordinary strings the engine compares elsewhere; they are not a complete command list. **[bin]**

Jumps add the base of the current script piece. Joined classes are one program counter over several instruction lists, and the script object keeps a child named `joinedclasses`. Inside a single script the base is 0, so the compiler's op index is the program counter. **[bin]**

An event list longer than 9999 records `Events number overrun` and drops the event. **[bin]**

### Peephole, after decode

The fold runs on the instruction list, not in the compiler. It rewrites the first opcode and skips the following one or two. **[bin]**

| First | Next | Becomes | Client name of the result |
| --- | --- | --- | --- |
| 20 `loadfloat` | 60–67, and the opcode after that is not 50 | 200–207 | `addfloat` `subfloat` `mulfloat` `divfloat` `modfloat` `powfloat` `andfloat` `orfloat` |
| 20 | 60–67 followed by 50 `assign` | 216–223 | `addfloatassign` through `orfloatassign` |
| 20 | 72–75 | 224–227 | `lessfloat` `greatorfloat` `lessequalfloat` `greaterequalfloat` |
| 46 `getreg` | 30, 33, 34, or 36 | 233, 228, 229, 230 | `getregdupe` `getregfloat` `getregstring` `getregobject` |
| 46 | 52 or 53, then 32 | 231 or 232 | `getregincpop` `getregdecpop` |
| 60–67 | 50 `assign` | 208–215 | `addassign` through `orassign` |

Bytes 66 and 67 sit in the arithmetic group. The folded names are `andfloat` and `orfloat`, so those two bytes are the value forms of and/or. The compiler does not emit them. The jump forms stay at 3 and 5. **[bin]**

### How 4.2.0.8 loads a weapon or a class

There is no `GRESCR01` magic in this engine. A weapon cache file is `weblevels`, then `weapons`, then the escaped name, then `.code`, under the user folder. If that file exists, its zlib CRC32 is compared with the value passed in. On a match the file bytes are handed to `setScript`. On a miss the client asks again. That is the id 193 path already described for this build: a CRC32 and a weapon name, not a mod-time. **[bin]** (`protocol/v4x-clients.md`)

`addClassScript` stores the class by name and runs the same container parser on the bytes. **[bin]**

Id 195 is a gani name and gani text. Id 196 has the same layout as 193, and this build's handler reads it and does nothing else. Neither id is the script container. **[bin]** (`protocol/v4x-clients.md`)

Id 140 is still the weapon-script message in the packet table. Its body is not the `0xAC` wrapper, and it is not GSHORT inside the container. **[srv]** (`protocol/packet-ids.md`)

## 5.0.0.7 and unpacked 6.00

Read from the 5.0.0.7 `GraalEngine.dll` export and from the unpacked Windows 6.00r2 and 6.00r4 executables. Nothing was run. 6.00r4's dispatcher cases are the same set as 6.00r2. **[bin]**

`torque/5007-engine.md` describes `setScript`, `runScript`, and `executeFunction` for this DLL and leaves the opcode loop unread. The cases in this section are that loop. **[bin]** (`torque/5007-engine.md#how-a-script-runs`)

### Same container

Both generations walk segment types 1–4 and stop on any other type. Segment 1 is still one 32-bit event mask. Segment 2 still strips a leading `public.` (seven characters) and records the function as public. Segment 4 still uses markers `F0`–`F6` with the same widths and the same string-versus-number split. The 4.2.0.8 peephole is still there, with the same results (200–233). 6.00 walks the decoded instructions at a stride of 24 bytes, the same record size as 4.2.0.8. **[bin]**

5.0.0.7's jumps, in the cases read, store the operand as the index into the one instruction list being stepped. They do not add a second base. A single script still matches the compiler's op index. **[bin]**

### Opcodes added after 4.2.0.8

The 4.2.0.8 switch is the base. Later dispatchers only add cases. **[bin]**

| Build | Added cases | What was read |
| --- | --- | --- |
| 5.0.0.7 | 48, 49, 54, 121 | 48 and 49 require a non-empty stack and then call a helper; the helper was not read, so it is not named. 54 builds a value with type tag 4 from the top of the stack, copying a string onto it when one is present. 121 adds the two numbers, unless either value has the string type tag, in which case both go through the string helper |
| 6.00r2 and 6.00r4 | 54, 121, and 234–242 | 54 and 121 match the 5.0.0.7 cases. 48 and 49 are not in this switch. 234–242 are the extra folds below |

The compiler emits none of these. **[doc]** (`npc-library/preagonal-gs2.md`)

6.00 folds more pairs after decode. The byte stream still uses `F0`–`F6` as operands, so a folded opcode in that range exists only on the decoded list. **[bin]**

| First | Next | Result |
| --- | --- | --- |
| 20 `loadfloat` | 131 `getarraycell` | 240 |
| 22 `loadmember` | 6 `call`, or 45 `setreg`, or 47 `makeprop`, when the name resolves and that object is flagged | 241, and the resolved object is stored on the instruction |
| 22 | 35 `makemember`, then 33, 34, 36, or 47 | 236, 237, 238, or 239. 47 is skipped when the opcode after it is 45 |
| 22 | 35, and none of those four follow | 234 |
| 22 | 36 | 235 |
| 47 `makeprop` | 45 `setreg` | 242, the next instruction's number is copied, and the type tag is set to number |

### Script cache

5.0.0.7 knows `GRESCR01`. The reader accepts a file only when it is longer than the magic, the magic matches, and the CRC32 of the bytes after the magic matches the value passed in. It then runs the key over that body and returns the plaintext to the script loader. A cache flag other than 1 returns an empty script. **[bin]**

The on-wire header around that body is already recorded: id 140 is a GSHORT length, then `type,name,cache flag`, then two GINT5 words that are the DES key, then the plain body; id 197 is the cache-hit form with the same key and a CRC32; id 195 is still a gani. **[bin]** (`protocol/v5x-clients.md`, `formats/gwebl001-cache.md`)

Unpacked 6.00r2 and 6.00r4 compare the same `GRESCR01` magic on a `.code` file of at least eight bytes. The class and weapon paths and the DES step are the cache note's, not a second format. **[bin]** (`formats/gwebl001-cache.md`)

## What differs

Tags: **[bin]** the clients above. **[doc]** the Preagonal compiler at `7878bc5` (`npc-library/preagonal-gs2.md`).

The client accepts every opcode the compiler emits. The compiler does not emit bytes the client still runs. The effect of each of those bytes is in `protocol/gs2-client-only-opcodes.md`.

| Bytes | Client | Compiler |
| --- | --- | --- |
| 43, 45, 46, 47, 104, 190 | `makeoldscriptvar`, `setreg`, `getreg`, `makeprop`, `compare`, `loadparams` | not in the `Op` enum |
| 66, 67 | value and/or, folded onward to `andfloat` / `orfloat` | not emitted; jumps stay at 3 and 5 |
| 48, 49 | 5.0.0.7 only | not emitted |
| 54, 121 | 5.0.0.7 and 6.00 | not emitted |
| 161, 162, 185–188 | named `break`, `continue`, `loadserver`, `loadserverr`, `loadclient`, `loadclientr`, and not dispatched | not emitted |
| 200–233, and 234–242 on 6.00 | folded by the client after decode | not emitted |

The other way, names for the same byte:

| Byte | Client name | Compiler name |
| --- | --- | --- |
| 9 | `loopcheck`, and it does stop past 10000 | `CmdCall` |
| 10 | `savestackpos` | `Jmp`, described on the engine side as a byte-offset jump. 4.2.0.8 stores the stack height and does not jump |
| 51 | `massassign` | end of a parameter list |
| 116, 117 | `beginswith`, `endson` | `starts`, `ends` |

The compiler's default file header (byte `0xAC`, raw 16-bit length, `type,name,0,`) is not a segment stream, not GSHORT, and not packet 140's body. `setScript` on these clients will not run a file that starts with that wrapper. The bytes they run are the four segments. Packet 140 and packet 197 are the envelopes in `protocol/v5x-clients.md`. **[bin][doc]**

## For graal-client-repro issues

Issues #151–#155 were read with `gh issue view`. The repro repo was not edited. `gh issue comment` on #151 returned "Resource not accessible by integration" and was not retried. The comments below are what would have been posted.

**#151** (TGE 1.2 surface). 3.04 stays TorqueScript plus GS1. Do not add this opcode table to that surface. GS2 starts with the 4.2.0.8 dispatcher in this note.

**#152** (Torque scaffold). No GS2 opcode or load path goes into `common/torque`. Unchanged.

**#153** (login, historical source left untouched). Unchanged. A later script VM reads the four segments, not packet 140's GSHORT header and not the compiler's `0xAC` wrapper.

**#154** (7.x research). Do not take a 40-byte instruction slot, or ids 195 and 196 as the script body, from the 7.x properties note. These clients decode a 24-byte instruction. 195 is a gani in 4.20r8 and in 5.x. Script bytes are the four-segment container, cached as `.code` (4.2.0.8, CRC32) or `GRESCR01` (5.0.0.7 and unpacked 6.00).

**#155** (parked Torque module pointed at 3.04). Do not point that module at this VM. 3.04 is not the GS2 dispatcher.

### Unpacked Windows 6.03 weapon-cache follow-up

[bin] The exact [Windows 6.03 weapon caller](../formats/windows-603-weapon-cache.md) distinguishes returned bytes from success and checks stored-body CRC before transformation. An eight-byte magic-only file does not satisfy that caller for zero or nonzero expected CRC. This narrows cache acceptance only; it does not change the separately studied 5.00/6.00 input contracts or demonstrate script execution.
