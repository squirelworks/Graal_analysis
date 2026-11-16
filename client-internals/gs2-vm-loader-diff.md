# GS2 loader and VM, cross-version

Date: 2026-11-16. A difference table for the bytecode loader and the script machine, from 3.153 through 6.1.1.3, the Android line where a machine was read, and the three reference implementations (seihai-core, GServer-v2, gs2lib). Unity 7.x is out of scope and was not opened.

This pass did not disassemble anything new. Each cell restates a reading already published in this repository or in seihai-core's VM profile note, in plain behaviour. Where those two disagree, the cell stays partial. No image was executed.

The earlier side-by-side, [gs2-vm-by-version.md](gs2-vm-by-version.md), covers opcodes, fusion, limits and maths for six VMs and treats several neighbours as unread. The profile note written after that read fills some of those neighbours in. This page does not replace the opcode lists; it adds the loader, the slots, event-name matching, and name and clock rules, and it records which later reads retire an inference.

## How a cell is graded

| Grade | Meaning |
| --- | --- |
| settled | One reading of that build states the behaviour, and no later note of the same build contradicts it |
| partial | A reading exists, and it is incomplete, limited to one input, or contradicted by another note of a build that shares the label |
| open | Not read. A borrowed profile is not a reading |

Tags are the repository's: **[bin]** a client image, **[cap]** a capture or a decrypted body walked offline, **[src]** our own source, **[doc]** a published profile note, **[lab]** a corpus or a loopback run, **[inf]** a conclusion past the reading. A **[doc]** cell is the profile note's account of a binary it says was read. This pass did not open that binary again.

## What this pass could not open

- The vendored compiler tree beside GServer-v2 is empty, so there is no second compiler source to compare with the clients. gs2lib, which is present, is not a script machine (see the reference section).
- Android Era, Classic other than 1.8's x86 engine, the December 2006 Mac build that actually sends the 4.20r6 token, Mac 4.04r2 and Mac 5.12 were not read as VMs. Their rows stay open or partial on purpose.
- No new disassembly session was started. Gaps below are unread behaviour, not a missing tool.

## 3.153 (Mac PowerPC)

The machine the later profiles treat as the base. Desktop clients before 4.04r2 have no GS2 VM of their own and are given this one only as a stand-in **[inf]**.

| Dimension | Grade | What this build does |
| --- | --- | --- |
| Parse | partial | The 4.2 loader agrees with the 3.153 file layout on big-endian segment words, types 1–4, instruction indices, a `public.` prefix, and operand markers `F0`–`F6`. The 3.153 account's required trailing newline is what a compiler writes; the 4.2 loader does not require it, and this pass did not re-open 3.153's own reader **[bin]** |
| Slots | settled | Opcodes 45 and 46 copy a local slot, index below 1024, and 47 turns the top into a resolved variable. Present from this build on **[bin]** **[doc]** |
| Opcodes | settled | Handles 1–10, 20–27, 30–47, 50–53, 60–103, 110–120, 130–142, 150, 151, 163, 180–184, 189, 190. No 11, no 104, no opcodes at 200 or above **[bin]** **[doc]** |
| Maths | settled | Value stack 256. Loop passes and call depth 10000. Integer conversion is `floor(x + 0.0001)`. Remainder drops the 0.0001 tolerance and is 0 when the divisor is 0. Shifts take the count modulo 64 and yield 0 or −1 past 31. Two numbers compare equal within 0.0001. Number-to-text is the shared nine-decimal rule **[bin]** **[doc]** |
| Events | partial | The names this build's notes use as examples are `onCreated` and `onTimeout`. The 4.2 runner queues `created` and `timeout` instead, and that note does not re-read how 3.153 matches the two spellings. Whether `onTimeOut` is the same function as `onTimeout` was not read **[bin]** |
| Names and clock | partial | An unqualified name walks `with`, locals, this script, the level, then globals. A leading `$` is special in the 3.153 account and is not special in the 4.2 resolver, which also adds `serverr` as a third name for the player object. Sleep is described as yielding for the given number of seconds, which matches the 4.2 3D clock and not the 2D 0.05 step **[bin]** |

## 4.04r2

Three images, not one profile. Windows and Linux were read separately. The Mac image was not.

### Windows 4.04r2

| Dimension | Grade | What this build does |
| --- | --- | --- |
| Parse | partial | The core has a GS2 segment-and-dispatcher interface beside a GS1 source parser. The segment walk itself was not opened on this image. The GS1 path normalizes source, splits on semicolons, and runs statement handlers **[bin]** |
| Slots | open | The 45/46/47 rules are not stated for this image. The profile gives it the shared slot opcodes only because its handler set matches the Mac image below **[doc]** |
| Opcodes | settled | The dispatcher matches the Mac image's set: 3.153's handlers plus 104, and not 11 and not the 200–233 folds. Linux 4.04r2, read on its own, also ends at 190 and sends opcode 11 down the skip path **[doc]** **[bin]** |
| Maths | settled | The profile's rules are the Mac image's, on x86: stack 10000, tolerant remainder, shift count modulo 32 **[doc]** |
| Events | partial | On the GS1 path, `created` is added to the active list on first run and is not queued through the later named-event helper. The legacy countdown queues the name `timeout` when it reaches 0. The GS2-style pass queues `istimeout` when the remaining time falls below 0.0001. How a source function `onTimeout` is chosen from those names was not read **[bin]** |
| Names and clock | partial | Three clocks. Tick count scaled by 0.001, and that helper does not use the performance counter. The legacy `timeout` property stores passes: negatives clamp to 0, then the value is multiplied by 20, 0.0001 is added, and the result is floored; the getter multiplies by 0.05; each service call subtracts one and queues `timeout` at 0. A separate GS2-style clock starts from the scaled tick count and then adds 0.05 per pass. The save and restore of a sleeping script is open, and none of this measures the real update rate **[bin]** |

### Linux 4.04r2

| Dimension | Grade | What this build does |
| --- | --- | --- |
| Parse | partial | Embedded scripts recover as the four-segment container, with instruction indices in range. The reader was not given a full format write-up. A trailing newline and a `publicsoap.` prefix were not tested **[bin]** |
| Slots | open | Not read |
| Opcodes | settled | The dispatch table ends at 190. Opcode 11 selects the common skip path. Inserting opcode 11 into one event fixture did not change that fixture's event order. Folds at 200 and above are outside the table **[bin]** **[cap]** |
| Maths | open | Limits and arithmetic helpers were not recovered. Do not copy the Windows row onto this executable |
| Events | partial | One profile-script payload was linked into the native executor. That is one linkage, not an event-name rule **[cap]** |
| Names and clock | open | Not read. The Windows clock section does not transfer |

### Mac 4.04r2

| Dimension | Grade | What this build does |
| --- | --- | --- |
| Parse, slots, opcodes, maths, events, names and clock | open | Not read. The profile lends it the Mac image's rules, including the PowerPC shift, because that image is PowerPC too **[inf]** |

## 4.20r6

The label covers two different images. The Mac VM row is the 2006-09-19 build that carries a 4.20r6 label and the token of the 4.10r2/4.11 era. The Mac build dated 2006-12-21, which sends the real 4.20r6 token, was not the machine that was read **[bin]**. The Linux ELF is a third input.

### Mac image dated 2006-09-19

| Dimension | Grade | What this build does |
| --- | --- | --- |
| Parse | partial | Not opened on its own. The shared desktop layout is assumed from the 4.2 Windows reader **[inf]** |
| Slots | settled | Same 45/46/47 slot opcodes as 3.153 **[bin]** **[doc]** |
| Opcodes | settled | 3.153's set plus 104 (object compare, leaving −1, 0 or 1). No `waitfor` (11). No load-time folds **[bin]** **[doc]** |
| Maths | settled | Stack 10000. Remainder uses `floor(a/b + 0.0001)`. Shifts stay on the PowerPC rule (count modulo 64). `b == 0.5` on a positive base is a square root, as on the other 4.x and 5.x VMs **[bin]** **[doc]** |
| Events | open | The 4.2 Windows event names were not re-read on this image |
| Names and clock | open | Not read on this image. The profile does not record a clock |

### Linux 4.20r6

The publication of this ELF says the editor matched a sanitized handoff and did not re-open the executable. Treat the rows as partial even where the note tags them **[bin]**.

| Dimension | Grade | What this build does |
| --- | --- | --- |
| Parse | partial | Big-endian 32-bit segment words and NUL-terminated names. A leading `public.` is removed and a flag is forwarded; that flag is not a proof of call visibility. Markers for string indices and signed integers match the `F0`–`F5` widths. The numeric-text marker's grammar was not shown to be decimal-only. A second marker on the same instruction is not covered by the recovered corpus **[bin]** |
| Slots | open | The fusion pass rewrites some records into 200–233 and leaves a record tagged 11 unchanged. It does not describe opcodes 45–47 |
| Opcodes | partial | Fusion rewrites adjacent pairs into internal tags 200–233 and keeps the instruction positions, so a file whose highest opcode is 189 can still feed those tags. Opcode 11 has a real handler here, unlike Linux 4.04r2. That contradicts the Mac image's row, which has neither 11 nor the folds. The two images do not share a VM **[bin]** |
| Maths | partial | The value stack grows by 100 and refuses to pass 10000, read on the opcode-11 path. Remainder, power and shifts were not read **[bin]** |
| Events | partial | Opcode 11 takes a number and two strings. A saved wait needs a non-empty name and a positive number; zero is not an indefinite wait on the path that was read. Registration lowercases with the C library and, when the name starts with `on`, drops those two bytes. The saved key is normalized on insert, and an empty target may be compared with the current owner's name. Only the first matching pending record is replaced. Resume, cancellation and the value the opcode leaves were not run **[bin]** |
| Names and clock | open | The empty-target comparison above is not a full resolver. The clock step was not read |

## 4.20r8 (Windows)

The engine whose script object and loader were read in full. Linux 4.20r8 is only known to have a real opcode-11 handler, in the same survey as Linux 4.20r6; its other cells are open **[bin]**.

| Dimension | Grade | What this build does |
| --- | --- | --- |
| Parse | settled | Big-endian type and length. Types outside 1–4, or a short read, end the walk. The four types may arrive in any order. A trailing newline is not required. A compiler file wrapper in front of the segments is not stripped, so a file that starts with that wrapper yields no instructions. Segment 1 is one event-mask word. Segment 2 is an instruction index and a NUL-terminated name; a leading `public.` (seven characters) is removed and the function is marked public. Segment 3 is NUL-terminated strings. Segment 4 uses `F0`–`F2` string indices and `F3`–`F6` numbers; `F6` is a NUL-terminated decimal parsed as a float. A decoded instruction is 24 bytes. There is no cache magic in this engine: a weapon file is accepted when its checksum matches, and the bytes go straight to the loader **[bin]** |
| Slots | settled | 45 copies the top into frame slot 0–1023 without popping. 46 pushes that slot. 47 resolves the top into a variable reference. The client's names are `setreg`, `getreg` and `makeprop`. Folds 228–233 are slot-load plus a conversion, or a slot increment or decrement followed by a pop **[bin]** |
| Opcodes | settled | The 4.20r6 set, plus 11 (`waitfor`) and the load-time folds 200–233. Folds rewrite the first instruction and the executor skips the next one, or the next two when an increment and a pop are swallowed. Compilers do not emit 200 or above. 66 and 67 are value forms of and/or: both sides run, and the result is 1 or 0. An opcode with no case is not run as the name in the opcode-name table (`break`, `continue`, `loadserver` and the client/server names sit in that table and have no case) **[bin]** |
| Maths | settled | Stack grows by 100 and stops at 10000. Call depth fails when more than 9999 frames are already stacked, leaving 0, with the text `Callstack overrun`. Loop opcode 9 stops past 10000 with `Loop limit exceeded`. Remainder keeps the 0.0001 tolerance. Shifts take the count modulo 32. Integer conversion and numeric equality match 3.153. Fused divide yields 0 when the divisor is 0 **[bin]** |
| Events | partial | The runner queues `created` after a non-empty script is attached, `initialized` from the init call, `timeout` from opcode 8, and `istimeout` when the sleep duration has elapsed. Those are not the source names `onCreated` and `onTimeout`. `waitfor` deletes a leading `on` before it stores the event, and a queued name that starts with `on` is treated as aimed at an object. `scheduleEvent` lowercases the name. `cancelEvents` matches without case. A queue longer than 9999 drops the event. Which function-table spelling (`onTimeout` or `onTimeOut`) that queue selects was not read. The weapon corpus's `onActionClientSide` / `onActionServerSide` names are source spellings; this runner's match against them was not read **[bin]** **[lab]** |
| Names and clock | settled | Reserved names, before the search: `temp` (the frame, or the universe at top level), `params`, `this`, `thiso`, `player`, `playero`, `level`, and `client` / `clientr` / `serverr` (one object). `join` and `leave` are looked up on `thiso`. Then: `with` objects newest first, the newest active frame, a property of `thiso`, the level, the universe, and on a miss `playero`. A leading `$` is not special. In 2D, once the clock is non-zero each script pass adds 0.05, so a sleep of 1 lasts 20 passes. In 3D, or while the clock is still zero, the clock is seconds from the performance counter, or tick count times 0.001 if that counter is missing. A timeout is due when the remaining time is below 0.0001. The value `waitfor` pushes when the timeout expires was not followed on this build; later builds that were followed push 0 **[bin]** **[doc]** |

## 5.00r7 and 5.12

Windows 5.12's dispatcher matches Windows 5.00r7 instruction for instruction **[doc]**. The cells below are the 5.00r7 readings unless a sentence names 5.12. Mac 5.12 was not read; the profile only changes its shift rule to the PowerPC one **[inf]**.

| Dimension | Grade | What this build does |
| --- | --- | --- |
| Parse | settled | Same four big-endian segments as 4.20r8, same `F0`–`F6` widths, same `public.` strip. A `publicsoap.` prefix (eleven characters) is a second visibility value, stored and not a callable service. The cache file must start with the eight-byte magic, the flag must be 1, and the checksum is taken over the bytes after the magic before they are decoded **[bin]** |
| Slots | settled | 45–47 unchanged. No new slot opcode **[bin]** **[doc]** |
| Opcodes | partial | Adds 48, 49, 54 and 121, and keeps 11 and 200–233. 121 adds, or joins as text when either value is a string. 54 is a member store: the 5.00r7 note pops two values and marks a variable, the profile pops the value, the member name and the object, and the later 6.1.1.3 note says this build's guard requires three values. Operand order for 48 and 49 is still unread. 48 builds an object from name/value pairs; 49 builds a list of numbers, the count clamped to 0–10000 **[bin]** **[doc]** |
| Maths | settled | Stack still 10000. Remainder drops the 0.0001 tolerance again. Shifts stay modulo 32. `this.maxlooplimit` appears, clamped to 100–1000000. Integer conversion, equality and number-to-text are unchanged. `b == 0.5` is still a square root **[bin]** **[doc]** |
| Events | partial | On the backup 5.00r7 image, both event receivers reject a queue of 1000 or more, which is not the 4.20r8 limit of 9999. That image is a backup from a folder that had been patched, so the 1000 cap is that file's, not a proof it shipped that way. `istimeout`, `created` and `initialized` are inserted at the front; the note says those literals are not automatically the source spellings. A null argument suppresses a duplicate of the same route and name. On 5.12 the `waitfor` timeout path was followed: the wait is saved with result 1, and the timer resumes it with 0 once the clock plus 0.0001 is past the deadline **[bin]** **[doc]** |
| Names and clock | partial | The 5.00r7 script pass uses the same 0.05 step as 4.20r8. The backup-image note found clock logic on the universe service and did not recover the caller's cadence, so the 0.05 rule and that gap are both kept. The reserved-name walk was not re-opened; nothing in the 5.00r7 read says it changed **[bin]** |
