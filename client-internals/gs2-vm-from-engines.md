# GS2 script machine in the 4.2, 5.0 and 6.00 engines

Date: 2026-11-07. Static read of the script runner in three engines. Nothing was executed. Tags: **[bin]**.

The engines are GraalEngine.dll whose version resource is 4.2.0.8, GraalEngine.dll whose version resource is 5.0.0.7, and the unpacked GraalSetup programs whose version resources are 6.00r2 and 6.00r4 (`quattro_lib`). The 3.04 Linux client is not this machine: it is TorqueScript menus plus the native GS1 runner, and this note does not read its opcodes.

An MPL-2.0 compiler and virtual machine exist as a public lead only. They are not evidence of these clients. The comparisons below are with the 2026-10-30 reading in squirelworks/seihai `documentation/gs2-opcodes.md`, `documentation/gs2-executor.md` and `documentation/gs2-grammar.md` (3.153 plus an open compiler). Where this note says the binary agrees, that is the 4.2.0.8 executor unless a version is named.

## Which binaries contain the machine

| Build | What the image contains | Tag |
| --- | --- | --- |
| 4.2.0.8 GraalEngine.dll | The runner is the named type `TScriptExecutionSpace`, owned by a `TGraalVar`. It loads bytecode into a `TGraalScript`, queues events, and dispatches numeric opcodes. `TGraalClientVar` is a `TGraalVar` whose number, string and array writes can be sent; it is not the runner. | [bin] |
| 5.0.0.7 GraalEngine.dll | The same named types and the same opcode switch, plus four opcodes listed under versions. `TGraalUniverse::runScripts` is the clock pass. | [bin] |
| 6.00r2 and 6.00r4 | The opcode switch is in the executable, and so are `thiso`, the `playerenters` name table, `Callstack overrun`, `timeout` and `istimeout`. The two images have the same case numbers. The 4.2 method names were not recovered on these two images. | [bin] |

`Graal3DEngine.dll` in the 4.2.0.8 set is not this runner.

## Script objects

A script object is a `TGraalVar`. Creating the runner (`createScriptSpace`) allocates one `TScriptExecutionSpace` on that variable if it does not already have one, and the runner points back at the variable. **[bin]**

The variable's name is the name it was constructed with. Giving the runner a byte string parses that string as bytecode (below), attaches the resulting `TGraalScript`, and, when the script or a joined class has any instructions, queues the event `created`. Giving it an existing `TGraalScript` does the same attach without parsing. An empty parse clears the runner's initialized flag. **[bin]**

| Kind | How it is tied to a script | Tag |
| --- | --- | --- |
| Player, NPC, level | `TServerPlayer`, `TServerNPC` and `TServerLevel` are `TGraalVar` subclasses. The current player and the current non-player are taken from the `with` stack. | [bin] |
| Class | `addClassScript(name, bytes)` stores a `TGraalScript` in a global table (`getClass` reads it). `joinClass` links that script onto the runner. The instruction walk concatenates the object's own script and the joined classes. Event masks are OR-ed across them. | [bin] |
| Weapon | A named `TGraalVar` receives `setScript` from command 132. A weapons directory stores an encrypted `.code` file; command 193 carries a five-byte Graal integer and a name and calls `setScript` only when that integer matches the file's hash. | [bin] |
| Gani | Command 134 stores the bytecode as a class whose name is `gani.` plus the gani name. | [bin] |
| GUI shell | Named variables, including `StartScript_Profiles` and `StartScript_MainMenu`, are created under the universe and given decompressed embedded bytecode. A name that starts with `login` sets the flag that allows `adventure.` calls. | [bin] |

`TShowImg` is constructed with a `TServerLevel`. Particle emitters and show-images also receive script events. The full property list of each world type was not read. **[bin]**

## How a call finds a function

`OP_CALL` (opcode 6) expects the callee name on top of the stack and a type-0 marker under the arguments. The name is a string (type 2), a variable (type 4) or a resolved value (type 5). **[bin]**

1. A name with no object, or whose object is the running script's own variable, is looked up in the current script's function table.
2. A name on some other object is looked up in that object's script, when it has one, and the call runs there.
3. Otherwise the name is resolved and matched against the built-in command table. Each command has a signature string; the number of arguments must be at least the length of that string, or the error is `Not enough parameters for` plus the name, the number needed and the number given.
4. A command whose name starts with `adventure.` is refused with `Unauthorized call of` unless the running variable's name starts with `login`.
5. If nothing matched, and the variable is set to log missing functions, the error is `Function` plus the script name plus the missing name plus `not found`. The call's slot becomes the number 0.

The error recorder prefixes `GraalScript:` and suffixes `in script of` plus the variable's log name. It keeps at most 20 distinct texts. **[bin]**

A call is refused when the call-stack list already holds more than 9999 frames. The text is `Callstack overrun`, and the slot becomes the number 0. **[bin]** agrees with the 3.153 note that the failure text is `Callstack overrun` and that the slot is 0. The binary's test is "more than 9999 frames already stacked", which the 3.153 note had not read (it used 10000 from the open compiler's comment).

Inside a called function, opcode 10 stores the stack height on the frame, and opcode 51 binds parameters. Opcode 7 writes the top value into the caller's saved slot, drops the frame and continues. With no frame, opcode 7 stops the script. A returned object that belongs to the frame is cloned first. **[bin]** agrees with the 3.153 note on opcode 10 (record stack height) and on opcode 7 (return into the caller's slot, or stop at top level).

## How an unqualified name is resolved

Reserved names are handled before the search. **[bin]**

| Name | Resolves to |
| --- | --- |
| `temp` | the current frame, or the universe object when there is no frame |
| `params` | the parameter object installed for this call |
| `this` | the current non-player from the `with` stack (empty when there is none) |
| `thiso` | the variable that owns the running script |
| `player` | the current player from the `with` stack |
| `playero` | the player object kept beside the machine |
| `level` | that player's level, or the NPC's level when there is no player level |
| `client`, `clientr`, `serverr` | the same object as `playero` |
| `join`, `leave` | looked up on `thiso` rather than by the search below |

`temp` as "the frame, or the global object at top level" agrees with the 3.153 note. `client` and `clientr` agree. `serverr` as a third spelling of that same object is not in that note. A leading `$` is not a special case in this resolver; the 3.153 note says names starting with `$` are handled before the search.

After those names, an unqualified lookup walks: **[bin]**

1. The `with` objects, newest first: a property, then a child variable.
2. The newest call frame that is marked active: a child variable.
3. `thiso`: a property only.
4. The level from the `level` rule: a property, then a child variable.
5. The universe object: a property, then a child variable. If the caller asked to create a missing name, the child is created here. If it is still missing, the same name is tried on `playero`.

That is the 3.153 order (with, locals, this script, level, globals) with two differences: step 3 reads a property of `thiso` and does not itself call the child-variable lookup, and a failed global lookup continues to `playero`.

## Events

Events are functions, queued as actions and run by `runScript`. A queue longer than 9999 actions is refused with `Events number overrun for` plus the event name. **[bin]**

The runner itself queues these names:

| Name | When |
| --- | --- |
| `created` | after a non-empty script is attached |
| `initialized` | `invokeInitializedEvent`, which also sets the initialized flag and drops actions marked as created |
| `timeout` | the saved state written by opcode 8 (`sleep`) |
| `istimeout` | the scheduler, when the sleep duration has elapsed |

The 3.153 note's examples `onCreated` and `onTimeout` are not the names this runner queues. A leading `on` is recognized: `waitfor` deletes those two characters before it stores the event it is waiting for, and dispatch treats an event name that starts with `on` as directed at an object. **[bin]**

`scheduleEvent(delay, name, argument)` lowercases the name, stores the absolute deadline, and later queues that name. `cancelEvents` drops queued names that match, case-insensitively. **[bin]**

A separate `script_event` index is a bit in two masks on the script (one from bytecode segment 1, one kept beside it). Joined classes OR their masks in. `needEvent` is true when that bit is set, and also true when the script is not yet initialized. The names, in index order, are: **[bin]**

`playerenters`, `playertouchsme`, `playertouchsother`, `playerchats`, `playerhurt`, `playerdies`, `playerlaysitem`, `playerendsreading`, `compusdied`, `emoticon`, `mousedown`, `mouseup`, `mousewheel`, `exploded`, `wasshot`, `waspelt`, `keypressed`, `actionprojectile2`, three empty slots, `playerleaves`, `washit`, two empty slots, `shapetrigger`, `playanimation`.

Which gameplay site calls each of those names was not followed. `catchEvent` registers a name on an object (`universe` is the universe object; any other name is a child of it) so that a later event can resume a waiting script.

## Timers

Sleep, `waitfor` and `scheduleEvent` use one double clock. **[bin]**

- In 2D, once the clock is non-zero, each `runScripts` pass adds 0.05. A sleep of 1 therefore lasts 20 of those passes.
- In 3D, or while the clock is still zero, the clock is set from the performance counter as seconds since the first sample. If that counter is missing, the value is the tick count times 0.001.
- A timeout is due when the remaining time is below 0.0001. `waitfor` stores deadline = clock + timeout. `scheduleEvent` stores the same kind of absolute deadline.
- 5.0.0.7 uses the same 0.05 rule in `TGraalUniverse::runScripts`.
- 6.00r2 has the performance-counter seconds function and the names `timeout` and `istimeout`. The 0.05 step was not found in that image.

The 3.153 note's "sleep yields for `t` seconds" agrees with the 3D clock. The 2D 0.05 step is additional.

Opcode 9 adds one to a counter stored in the instruction itself (the same double slot as a numeric operand) and stops the script when the result is greater than 10000, with the text `Loop limit exceeded`. Starting from 0, the 10001st execution of that instruction is the one that stops. **[bin]** agrees that the counter lives in the instruction and that the limit is 10000. The comparison is "greater than 10000 after the increment", which the 3.153 note had not read off the binary.

## Bytecode and source

`setScript` on a byte string runs a loader, not a source parser. The engine also contains a source compiler: a large parse that requires `(` after built-in names and records a signature string. Its grammar was not recovered. Built-in GUI scripts are decompressed, then passed to `setScript`. **[bin]**

The loader reads big-endian 32-bit words. **[bin]** agrees with the open-compiler file layout on byte order. A segment is a type word, a length word and that many bytes. Types outside 1..4, or a truncated header, end the read. A trailing `0x0A` is not checked; the 3.153 note's "one trailing 0x0A" is what that compiler writes, not a byte this loader requires. **[bin]**

| Type | Body |
| --- | --- |
| 1 | one big-endian 32-bit mask, stored as the script's GS1 event mask |
| 2 | repeated: a big-endian 32-bit entry index, then a NUL-terminated name. A name that starts with `public.` loses those seven characters and is stored as public |
| 3 | NUL-terminated strings, the string table |
| 4 | opcode bytes and operands. Each instruction is allocated, then a peephole rewrites some pairs (below) |

The entry index is what `executeFunction` starts at, and the executor's instruction counter steps by one per instruction, so the index counts instructions. **[bin]** agrees with the open-compiler note that the function table's integer is an instruction index and that `public.` is a prefix on public functions.

Operands use a marker byte. **[bin]** agrees with the open-compiler widths, and the multi-byte markers are big-endian:

| Marker | Payload |
| --- | --- |
| `F0` | unsigned 8-bit string-table index |
| `F1` | unsigned 16-bit string-table index |
| `F2` | signed 32-bit string-table index (a negative index is rejected) |
| `F3` | signed 8-bit integer, stored as a double |
| `F4` | signed 16-bit integer, stored as a double |
| `F5` | signed 32-bit integer, stored as a double |
| `F6` | NUL-terminated decimal text, parsed as a float |

Any other byte is an opcode and starts a new instruction. The instruction holds the opcode, a kind (number or string), the string, and a double. That double is the numeric operand and the loop counter. **[bin]**

After the load, pairs are rewritten in place and the following opcode is left in the list. The executor skips it by advancing the instruction index an extra step (two steps for the forms that swallow an increment and a pop). The rewritten opcodes are 200..233. They are not in the open compiler's enum. **[bin]**

| First opcode | Following opcode | Becomes | Effect read in the executor |
| --- | --- | --- | --- |
| push number (20) | add..the boolean pair (60..67), and the next is not assign | 200..207 | operate with the immediate number, skip the following opcode |
| push number (20) | those opcodes, and the next is assign (50) | 216..223 | the same, and the assign is skipped too |
| add..the boolean pair (60..67) | assign (50) | 208..215 | compute and store, skip the assign. Fused divide yields 0 when the divisor is 0 |
| push number (20) | the four ordered compares (72..75) | 224..227 | compare the top value with the immediate, skip the compare opcode |
| opcode 46 | copy, to-string, to-float, or to-object | 228, 229, 230, 233 | frame-slot plus that conversion, skip one |
| opcode 46 | increment or decrement, then pop (32) | 231, 232 | increment or decrement the frame slot, skip two |

Opcode 206 (immediate form of 66) is "both non-zero". Opcode 207 (immediate form of 67) is "either non-zero". So 66 and 67, which the open compiler's enum leaves unnamed, are boolean operations in this executor. **[bin]**

### How the bytes arrive

The engine's control dispatch (the same numbers as the server-to-client message ids) feeds the loader. Packet id 140 is not a case in that dispatch. **[bin]**

| Id | Body, then where it goes |
| --- | --- |
| 131 | a three-byte Graal integer, then the bytecode. The integer selects the object (below 1000 in the level table, 1000 and above in a second table) and `setScript` takes the remainder. This agrees with the manual's `i3` plus bytecode for id 131. |
| 132 | one length byte in the usual biased form (the name is that many bytes, the count being the byte minus 32), then the name, then the bytecode. `setScript` runs on the object of that name. |
| 133 | the same split, into `addClassScript`. |
| 134 | the same split; the class name is `gani.` plus the name. |
| 193 | a five-byte Graal integer and a name. The cached weapon `.code` file is loaded only when the integer matches its hash. |

## Opcodes

The executor switches on the instruction's opcode integer. The binary does not store the `OP_` names. The names in the first column are the ones in the Seihai opcode note, used only where the effect read here is that operation. A stack value's tag is 0 (the argument marker), 1 (number), 2 (string), 3 (object), 4 (variable name) or 5 (resolved variable). **[bin]** agrees with the 3.153 note's tags.

The value stack grows 100 slots at a time and refuses to grow when the size plus 100 would pass 10000, so the cap is 10000. The 3.153 note's cap of 256 is not what 4.2.0.8 does. An underflow sets the stack index to -1 and stops the script. **[bin]**

Jumps add the operand, truncated toward zero, to the base of the current instruction list (the script, or one joined class). In a script with no joined class the base is 0, so the operand is an instruction index, which agrees with the open-compiler note. **[bin]**

| Opcode | Name in the existing note | Effect in 4.2.0.8 |
| --- | --- | --- |
| 1 | unconditional jump | jump, as above |
| 2 | jump if true | jump when the top number is not 0; then pop |
| 3 | or | not 0: jump and keep the value. 0: pop and continue |
| 4 | if | 0: pop and jump. Otherwise pop and continue |
| 5 | and | 0: jump and keep the value. Otherwise pop and continue |
| 6 | call | the call rules above |
| 7 | return | the return rules above |
| 8 | sleep | the timer rules above |
| 9 | loop count | the counter rules above |
| 10 | mark stack | store the stack height on the frame |
| 11 | waitfor | the timer rules above |
| 20 | push number | push the instruction's double, tag 1 |
| 44 | inline conditional | a non-zero top number becomes 1 |
| 45 | (enum: unused) | copy the top value into frame slot 0..1023 |
| 46 | (enum: unused) | push the frame slot selected by the operand |
| 47 | (enum: unused) | present; the helper was not opened |
| 50 | assign | requires two values, then the assign helper |
| 51 | end of parameters | the parameter-binding helper |
| 52 | increment | increment the top variable and leave it there |
| 53 | decrement | decrement the top variable and leave it there |
| 66, 67 | (enum: unused) | present; their immediate fusions are nonzero-and and nonzero-or |
| 97, 98 | vecx, vecy | replace the top value using a four-entry table; the index conversion floors toward negative infinity, so the same conversion that yields -2 for -1.5 |
| 150 | with | present at this number; the push of the with-object was not opened |
| 151 | end with | pop the `with` stack; a player or NPC refreshes the current player and the current non-player |
| 163 | foreach | when the object is an array and the index is in range, bind the element; otherwise jump to the exit |
| 180 | this | push the current `this` object, tag 3 |
| 200..233 | (not in the enum) | the fusions in the bytecode section |

These numbers are also cases in the 4.2.0.8 switch. Their helpers were not opened one by one, so this note does not restate each effect: 21, 22, 23, 24, 25, 26, 27, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 60, 61, 62, 63, 64, 65, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 99, 100, 101, 102, 103, 104, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 181, 182, 183, 184, 189, 190. **[bin]**

Fused divide (opcode 211, the assign form) yields 0 when the divisor is 0. That agrees with the 3.153 note for division. The plain divide case (63) was not opened. The floor-toward-negative conversion agrees with the 3.153 note's `int(-1.5)` rule for the sites that use it (opcodes 97 and 98, and the fused remainder). **[bin]**

## Differences between the three engines

| Item | 4.2.0.8 | 5.0.0.7 | 6.00r2 and 6.00r4 |
| --- | --- | --- | --- |
| Opcode cases | the set above (154 values, 1 through 233 with gaps) | those, plus 48, 49, 54 and 121 | the 4.2 set, plus 54, 121 and 234..242. Not 48 or 49. r2 and r4 match each other |
| 48 and 49 | absent | present; each calls a helper when the stack is non-empty. The helper was not opened | absent |
| 54 | absent | pops two values, copies a string onto the lower value or clears it, marks it as a variable, then assigns | present at this number; the body was not compared line for line with 5.0 |
| 121 | absent | if either of the top two values is a string, both are converted and a string path runs; otherwise the two numbers are added | present at this number; the body was not compared line for line |
| 234..242 | absent | absent | each rewrites the top stack value (tags 4, 1 or 5 appear) and skips one or two following instructions. The helpers are unnamed in the decompile, so the game effect is not known |
| Clock step 0.05 | yes, in the script pass | yes, in `runScripts` | not found |
| Runner type names | `TScriptExecutionSpace` and the methods below | the same, plus `preDestroy`, `leaveAllClasses`, `transferFunctionObjects`. `executeFunction` takes a function object rather than an integer. `joinClass` takes an extra flag. The catching-function lookup returns a function object | method names not recovered |

4.2.0.8 `TScriptExecutionSpace` methods, as behaviour: construct on a `TGraalVar`; free the script, suspended states, actions and errors; record an error; queue `created` and `initialized`; catch, find, ignore and test events; get and set the timeout; set the script from bytes or from a `TGraalScript`; join, leave and list classes; save and restore a machine state; run an action; run a function by index; schedule and cancel events; `runScript`. **[bin]**

## what is still missing before a Seihai VM can be written

Each item is a behaviour this read did not see.

- The effect of each opcode whose helper was not opened (the long list in the opcode section), including compare equality, string case, substring indexes and plain division by zero.
- What opcodes 48, 49, 54 and 121 do in full, and what 234..242 do in 6.00 beyond the stack-tag change.
- The four components of the direction table used by opcodes 97 and 98.
- The source compiler's grammar, and which built-in names it accepts.
- The built-in command table: each name, what its signature letters mean, and what the command changes in the game.
- Which gameplay site fires each `script_event` name (`playerenters` and the rest of that list).
- How the second event-mask word is filled from function names. Segment 1 supplies only the first mask.
- What the public flag changes when a function is called.
- How a saved `timeout` or `waitfor` state is restored onto the stack, instruction by instruction.
- Whether 6.00 steps its script clock by 0.05, or only by the performance-counter seconds.
- The property set of `TServerPlayer`, `TServerNPC`, `TServerLevel` and a weapon (the fields a script reads and writes).
- Packet id 140's own framing. It is not a case in the dispatch that feeds `setScript`.
- Whether a joined class's functions are visible to an unqualified call, or only its event mask and its instructions. The call lookup that was opened searches the current script's function table.
