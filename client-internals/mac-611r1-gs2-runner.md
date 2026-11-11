# Mac OS X 6.11r1: the GS2 runner, sleep and calls

This is a static reading of the GS2 instruction runner in the Mac OS X 6.11r1 client (`Graal v6.11r1[Mac OS X]`, executable SHA-256 `95c5353c848130a748ace773000b6170f3a033bd4dcaa794b18d4943a7aa043a`). It sits beside the Windows engines in [gs2-vm-from-engines.md](gs2-vm-from-engines.md) and the Linux 6.x dispatch in [linux-cross-version-dispatch.md](linux-cross-version-dispatch.md). It is a separate input, and nothing here is assumed to hold for those builds. Evidence `MAC-V6-OPCODE-20261109`. **[bin]**

No guest was started for this reading. The broad analysis pass timed out, so the function inventory and its references are incomplete. Where the text says "selected", only those handlers were read.

## Decoded records and dispatch

**[bin]** The runner does not execute the serialized bytecode directly. It works on decoded instruction records of 40 bytes each. The first byte is the opcode, and each record also caches the native handler for that opcode. A handler ends by jumping straight to the next record's cached handler, so the runner's own loop is not visited between instructions. The record layout is not the wire layout. Windows 6.1.1.3 stores a decoded instruction in 24 bytes (→ [gs2-unpacked-6113.md](../protocol/gs2-unpacked-6113.md#container)); the two layouts are different.

**[bin]** The first time a program runs, a preparation pass appends opcode 164 as an end marker and fills every record's handler from a table. The instruction index is a signed 32-bit number, and fetching an instruction increments it before the handler runs.

**[bin]** The table was read through a 256-entry window. Entries 243 and 244 are zero, and from 245 on the window runs into neighbouring type data. The true table length is therefore unknown; 243 entries, as on Linux 6.x, fits but was not proved. Zero entries are not safe no-ops.

## The handlers that were read

**[bin]** These handlers were read one by one. This is not a complete opcode map.

| Opcode | What the handler does |
| --- | --- |
| 0 | falls through to the next record |
| 1 | jumps; the target is the operand, a double converted to a signed integer |
| 2 | numeric conditional branch, then pops |
| 6 | call (see below) |
| 8 | sleep |
| 9 | loop check |
| 11 | wait for an event |
| 20 | pushes a numeric literal |
| 21 | pushes a string literal |
| 24 | pushes the number one |
| 27 | pushes pi |
| 164 | the end marker added at preparation; advances to the next function or frame |

Opcodes 1, 2 and 6 agree with the 4.2.0.8 meanings in [gs2-vm-from-engines.md](gs2-vm-from-engines.md#opcodes). The handler for opcode 7 was too large for the bounded walk and is not described here.

## The loop check

**[bin]** The runner loads 10000 as the default loop-check limit, and the owner's context can override it. Opcode 9 keeps a counter on its instruction record, tied to the compiled program's generation, so recompiling resets it. No per-instruction decrement was found. The 4.2.0.8 reading, where opcode 9 stops past 10000 executions, is close, but a general "fuel" limit across all instructions is not supported by this build.

## The value stack

**[bin]** Stack nodes come from a reusable pool that grows by 100 nodes at a time. Each node holds a number, a string or a reference, and links to its neighbours. A pop moves the top pointer and the index. When a node's contents are freed was not fully traced. The 100-step growth matches the 4.2.0.8 value stack; this build's upper limit was not read.

## Sleep and waitfor

**[bin]** Sleep (8) and wait-for (11) both take a snapshot of the running script. The snapshot keeps the current function and instruction index, copies the typed stack values, moves the frame list and the object context into the snapshot, and records the event name. It is then queued. A positive delay is stored as an absolute deadline: the manager's clock plus the delay. Both paths can return status 2 after taking the snapshot.

**[bin]** Restoring a snapshot puts back the stack values, frames and object context, optionally pushes a saved return value, and frees the snapshot. The unit of the clock and the order in which due snapshots run were not checked. Compare the Windows 4.2 rule, where the 2D clock adds 0.05 per pass (→ [gs2-vm-from-engines.md](gs2-vm-from-engines.md#timers)); that rule was not looked for here.

## Calls

**[bin]** A call searches back down the stack for the argument marker (a value with tag 0), so the arguments are everything above it. It resolves the callable from a name or an object, checks that the caller may access it, picks the script-function path or another callable path, and checks the number of parameters. If the classes the call needs are still downloading, the runner can suspend on `classesdownloaded`. It saves the instruction index one step back, so the call is retried when the script resumes. The native call interface and how frames move between objects were not read.

## Runner status

**[bin]** Three return values were seen, each on particular paths: 0 when the program runs out or advances normally, 1 for missing prerequisites and a failed loop check, and 2 on suspension paths. These are observations, not names for a status type.

## Limits

- Static and partial: the handler table extent, the opcode-7 handler, arithmetic and comparison handlers, type conversion and NaN handling are open.
- Nothing was run. No script was executed in the Lion guest for this note, and the language version that produced the bytecode is not identified.
- The bytecode-to-record mapping and the source-to-bytecode mapping are not recovered. These findings narrow E#207 for one Mac build only.
