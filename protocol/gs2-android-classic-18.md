# GS2 on Android Classic 1.8: the container, the machine and its rules

A static reading of the GS2 machine in the Android Classic 1.8 (build 6158) x86 engine, the same input as [client-internals/android-classic.md](../client-internals/android-classic.md). It adds one exact build to [gs2-client-vm.md](gs2-client-vm.md), which covers Windows 4.20 and the Preagonal compiler, and to [client-internals/gs2-vm-from-engines.md](../client-internals/gs2-vm-from-engines.md). The original machine was never run. Where this build differs from the Windows notes, that is a difference between two inputs, not a contradiction, unless the same script is tested on both. Evidence `ANDROID-GS2-20261109`. **[bin]**

## The container

**[bin]** The container is the same four-segment format as the Windows engines. A script is a run of segments, each a big-endian 32-bit type, a big-endian 32-bit length, and the body:

- **1** is the event mask.
- **2** is the function table: a big-endian 32-bit instruction index and a NUL-terminated name for each function. A leading `public.` is removed from the name and kept as visibility.
- **3** is the string table, NUL-terminated strings.
- **4** is the opcodes and their operands.

**[bin]** Functions and jumps point at instruction indices, not byte offsets. An operand marker belongs to the instruction before it: `F0`, `F1` and `F2` are string indices of 8, 16 and 32 bits (big-endian; the 32-bit form refuses negative values); `F3`, `F4` and `F5` are signed integers of those widths; `F6` is a number written as NUL-terminated text. Fused opcodes are made while decoding and never appear as raw bytes. A network envelope or an encrypted cache has to be removed before this parse.

**[bin]** In memory a decoded instruction is 20 bytes on this build; the Windows engine notes give 24. The native binding record is a different structure of 24 bytes. Neither size is part of the portable format. The dispatcher has 165 case labels. The catalogue counts 165 dispatch cases, 243 function selectors and 43 fusions; these counts are not a complete account of what each opcode does.

**[inf]** A strict decoder written for this study passed nine tests on four synthetic files. That checks the decoder, not the client.

## Control flow and the stack

**[bin]** The machine advances the instruction index before it dispatches. An opcode with no handler, or one that falls to the default, continues without popping anything.

**[bin]** There are four conditional branches. Two always pop the tested value. The short-circuit pair keeps the value when the branch is taken and pops it when it is not. A branch tests the number against zero; that is not the same as the explicit integer and boolean conversion helpers.

**[bin]** Converting to an integer truncates toward zero. Assignment pops both the target and the value, including the fused numeric forms, uses separate setters for locals, references and properties, and leaves nothing on the stack.

**[bin]** The loop check tracks a generation. In the same generation it checks the limit and then counts up; when the generation changes, the counter goes back to 0. The budget is 10,000, but whether the 10,000th or 10,001st pass stops needs a runtime test. The call stack refuses a new frame at 10,000. The value stack grows by 100 at a time, and this helper has no 10,000 cap, unlike the Windows 4.2 value stack.

## Numbers and truth

**[bin]**

- Division by zero gives 0. The remainder uses floor, `a − b·floor(a/b)`, so −5 mod 3 is positive and 5 mod −3 is negative. A remainder by zero gives 0.
- The machine's own boolean maps any non-zero number to 1. The boolean passed to native calls instead tests `floor(v + 0.0001) ≠ 0`. So 0.5 is true inside the machine but false when passed to a native call; −0.5 is true in both.
- Numbers compare as equal within 0.0001; only outside that are they less or greater.
- `abs` goes through a 32-bit float and can lose precision. Power has partly read special cases.
- The direction vectors are in the order up, left, down, right; an index out of range gives 0.

## Strings

**[bin]** String comparison ignores case. Mixed types have their own coercions. Searching returns a 0-based byte index and returns −1 for a missing or empty needle. A substring applies `floor(v + 0.0001)` to the start and length, clamps the start, treats a negative length as "to the end", and counts bytes, not Unicode characters.

## Arrays

**[bin]** Reading out of bounds gives 0. Writing does not grow the array. Creating or resizing an array clamps the size to 0 to 10,000. Insert and delete check protection and send a change notice. Cells are typed as number, string or object. Reading a plain variable at index 0 has a compatibility path.

## Events, time and classes

**[bin]** The event queue refuses new events at 1,000. At the limit `onAllRCChat` is dropped silently and other events take the error path. `istimeout`, `created` and `initialized` go to the front of the queue. There is a path that merges duplicates, only partly read.

**[bin]** A scheduled event refuses a negative delay, lowercases the event name, and is due within 0.0001 of its deadline. Its arguments are kept by copying. A positive sleep saves a continuation; a sleep of zero or less does not suspend. The clock either samples real time or steps by a configured interval; it is not always 0.05.

**[bin]** Joining a class ignores a class already joined; otherwise it appends the class, raises its reference count, bumps the generation and installs the class's event catchers. Leaving lowers the count.

## Native bindings

**[bin]** Four registration calls supply 173 native bindings; 172 names are recovered and one is not. Bindings use typed signature codes. Access metadata on a binding does not make the client the authority for anything, and "server-only" marks an authority boundary, not an opcode. The method that compiles zipped scripts is not a recovered compiler.

**[bin]** One binding has its "already encoded" flag set, so its readable name is looked up as encoded bytes. It shares its target with a key-event binding that forwards keys and text to the main window, if there is one. Why is not known.

## A model built from this reading

**[inf]** An independent model with 17 tests covers 144 base-versus-fused combinations and all 43 fusions. It shows that the optimizer keeps every instruction slot: it rewrites the first instruction of a fused group and the machine skips the rest, so indices do not move. Binding a call early does not skip the call. A guard on member stores still allows a later fused register store. This model is not a test of the original client.

## Still open

21 delegated and 13 complex cases are incomplete. Also open: mixed-type coercion, power and unsigned conversions, ownership and freeing, formatting and tokenizing, changing a collection inside `foreach`, native privileges, the order of re-entrant events, the grammar, runtime tests, and the server-side machine.
