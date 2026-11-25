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
| Events | partial | Both event receivers refuse an event when 1000 or more are already queued, log `Events number overrun for <name>` and return 0; the 4.x engine read beside it uses 10000 in the same two routines ("longer than 9999"). The cap is the engine's own value, not a patch: the unpatched engine and both patched engines carry the same comparison, and their patches touch only the licence-file check and the auto-update gates, far from the event code ([G084, 2026-11-24](#500r7-event-queue-cap-g084-2026-11-24)). `istimeout`, `created` and `initialized` are inserted at the front; the note says those literals are not automatically the source spellings. A null argument suppresses a duplicate of the same route and name. On 5.12 the `waitfor` timeout path was followed: the wait is saved with result 1, and the timer resumes it with 0 once the clock plus 0.0001 is past the deadline **[bin]** **[doc]** |
| Names and clock | partial | The 5.00r7 script pass uses the same 0.05 step as 4.20r8. The backup-image note found clock logic on the universe service and did not recover the caller's cadence, so the 0.05 rule and that gap are both kept. The reserved-name walk was not re-opened; nothing in the 5.00r7 read says it changed **[bin]** |

## 5.24r4, 5.30r3, 5.31r4, 6.00r2 and 6.00r4 (Windows)

The profile reads these five as one VM, and reads 6.00r2 and 6.00r4's dispatchers as identical to each other. The 2026-11-13 side-by-side had not read them and lent 5.24–5.31 the 5.00r7 VM and 6.00 the 6.03r7 VM. Both loans are retired: this VM has already dropped opcodes 48 and 49, and it has not yet dropped the 10000 stack cap or switched the square root to single precision **[doc]**.

| Dimension | Grade | What this build does |
| --- | --- | --- |
| Parse | partial | 6.00r2 and 6.00r4 walk types 1–4, strip `public.`, and use the same `F0`–`F6` widths. A decoded instruction is still 24 bytes. The cache magic and the checksum-after-magic rule match 5.00r7. `publicsoap.` was not re-checked. 5.24r4's own reader was not written up separately **[bin]** |
| Slots | settled | 45–47 remain. Folds 234–242 add variable-plus-member, variable-plus-call, a resolved-variable store into a slot, and a number plus an array index. The executor skips one or two following instructions, except the call fold, which does not skip **[bin]** **[doc]** |
| Opcodes | settled | 5.00r7's set without 48 and 49, plus 234–242. 54 and 121 stay. 6.00r2 and 6.00r4 do not have 48 or 49. No end-of-script opcode 164 in this profile; that opcode is recorded on the Linux 6.x and Mac 6.11r1 runners, not here **[bin]** **[doc]** |
| Maths | settled | Stack stays 10000. `maxlooplimit` is still a plain name on 5.24r4 through 5.31r4. 6.00r2 and 6.00r4 keep the field and do not keep the plain name. Remainder is the plain floor. Power checks `b == 2` first and uses `a * a`, and a positive square root stays double precision. Shifts stay modulo 32 **[doc]** |
| Events | partial | On 6.00r2 the `waitfor` timeout path matches 5.12: saved with result 1, resumed with 0 after the deadline. The 4.20r8 queued names (`created`, `timeout`, `istimeout`) were seen as strings in the 6.00 images; the method that matches them to `onTimeout` was not recovered, and case variants were not tested **[bin]** **[doc]** |
| Names and clock | partial | 6.00r2 has the performance-counter seconds function and the names `timeout` and `istimeout`. The 0.05 step was not found in that image, so the 4.20r8 step does not carry forward. The reserved-name walk was not re-opened **[bin]** |

## 6.01r1 and 6.03r7

Linux 6.01r1 and Linux 6.03r7 share a handler set, found as one function per opcode behind a computed goto. Windows 6.03r7 was read as a switch, with the same stack rule and the same power helper, and without opcodes 0 and 164. 6.015 and 6.034 have no binary; they take this profile because the builds on either side share it **[inf]**.

| Dimension | Grade | What this build does |
| --- | --- | --- |
| Parse | partial | Linux 6.01r1 decodes records with empty native targets, then a post-pass builds the fused tags and one path caches a handler pointer. The executor adds a termination record. That does not add a new serialized opcode. The four-segment walk is the 6.00 one; it was not re-specified for these two ELFs **[bin]** |
| Slots | partial | The 6.00 folds 234–242, including the slot store, are in the handler set. Linux 6.01r1's saved call-frame layout differs from 4.20r8. Which fields moved was not listed, so the 1024-slot rule is carried, not re-proved **[bin]** **[doc]** |
| Opcodes | settled | The 5.24r4–6.00r4 set. Linux adds opcode 0, which falls through, and opcode 164, appended at load as an end marker that continues into the next script and is never stored in a file. Windows 6.03r7's switch does not add those two. 48 and 49 stay absent. The loop-limit property's name is scrambled on 6.x and was not recovered; the profile keeps calling it `maxlooplimit` **[bin]** **[doc]** |
| Maths | settled | No value-stack cap. Loop default remains 10000 and is settable. Call depth 10000. Remainder is the plain floor. A positive square root is single precision, and `b == 2` is `a * a` before that. Shifts stay modulo 32. Integer conversion, equality within 0.0001, and the nine-decimal number-to-text rule match 3.153 **[bin]** **[doc]** |
| Events | partial | The 6.00 names `timeout` and `istimeout` are present. Linux 6.01r1 saves a deadline as the script clock plus a positive input, and replaces the first matching pending record. Trigger, restore, cancellation order and the public result values were not proved. Case of `onTimeout` against `onTimeOut` was not tested **[bin]** |
| Names and clock | partial | The clock's cadence on Linux 6.01r1 was not proved. Windows 6.03r7's profile uses the single-precision power rule and does not restate the 0.05 step. The reserved-name list was not re-opened **[bin]** **[doc]** |

## Unpacked Windows 6.1.1.3

The packed listing of this version has no opcode switch. The row is the unpacked image. It adds no case past the 6.00 set **[bin]**.

| Dimension | Grade | What this build does |
| --- | --- | --- |
| Parse | settled | The walker stops when the segment type is outside 1–4. Segment 1 stores one integer, the event mask. Segment 2 drops a leading `public.` and marks the function public. Segment 3 is the string table. Segment 4 uses the 6.00 marker widths, and a decoded instruction is 24 bytes. A cache file shorter than eight bytes is rejected. The magic must match, the flag must be 1, and the checksum covers the bytes after the magic. `publicsoap.` was not mentioned **[bin]** |
| Slots | partial | Fold 242 still requires a call frame, stores a register, and skips the next opcode. The 0–1023 range was not re-measured. Official bodies from this era use dense slot indices per function, and the highest index in the seven-body slice is 10; every opcode 47 is immediately followed by 45 **[bin]** **[cap]** |
| Opcodes | settled | Cases through 242, including 54, 121 and 200–242. No 48, no 49, no case above 242, and the 4.2 names that were never implemented stay unimplemented. An opcode with no case pops one value and continues. 54 on this image rejects a stack shorter than two (the 6.00 guard, not 5.00r7's three-value guard), drops two values, converts what is then on top to an object, and stores as opcode 50 does. 121 joins when either tag is a string, otherwise adds. The pair recogniser that produces 234–242 was not separated; the executor still accepts those results **[bin]** |
| Maths | partial | Power checks `b == 2` first (`a * a`). A positive `b == 0.5` takes a double-precision square root — not the 6.03r7 single-precision path ([note](static-reads-appendix-e-2026-11-24-g082.md#unpacked-windows-6113)). Remainder, shifts, stack caps and number-to-text were not re-opened **[bin]** |
| Events | open | Not read on this image |
| Names and clock | open | Not read on this image |

### What the 6.113-era compiler writes

Nineteen decrypted bodies, six classes and thirteen weapons, all walk as segments 1–4 in that order, segment 1 a zero word, no trailing newline, no file wrapper, markers only `F0`–`F6`, and no opcode at 200 or above. Twelve of the nineteen use a `public.` prefix. Opcode 190 (`loadparams`) occurs. Opcodes 48, 49, 54 and 121 do not occur in this set. A seven-body slice of the same family confirms the container checks and shows segment 2 is not sorted by a case-insensitive name hash, nor by instruction index. That is the compiler's output, not a proof of how the VM looks a name up **[cap]**.

The checksum on those cache files covers the stored bytes after the magic, before decryption. An older sentence that put the checksum on the plaintext does not hold for this capture **[cap]**.

## Mac 6.11r1

A partial handler read. The table was walked through a 256-entry window whose entries 243 and 244 are zero; the true length was not proved. Nothing was run.

| Dimension | Grade | What this build does |
| --- | --- | --- |
| Parse | partial | The runner executes decoded 40-byte records, not the serialized bytes. The first byte is the opcode, and each record caches its handler. The bytecode-to-record mapping was not recovered, so the segment walk is not shown **[bin]** |
| Slots | open | Not among the handlers that were read. The value stack is a pool that grows by 100; the upper limit was not read **[bin]** |
| Opcodes | partial | Handlers read: 0 falls through, 1 jumps, 2 branches and pops, 6 calls, 8 sleeps, 9 checks the loop, 11 waits, 20 pushes a number, 21 pushes a string, 24 pushes 1, 27 pushes pi, 164 is the end marker added at preparation. Opcode 7 was not read. 1, 2 and 6 agree with 4.20r8. The loop check defaults to 10000, can be overridden from the owner's context, and the counter lives on the opcode-9 record and resets when the program is rebuilt **[bin]** |
| Maths | partial | The power helper checks `b == 2` first (`a * a`). A positive `b == 0.5` uses a double-precision square root (`sqrtsd`), not a single-precision convert-and-root ([note](static-reads-appendix-e-2026-11-24-g082.md#mac-os-x-611r1)). Other exponents call `pow`. Remainder, shifts, NaN beyond those paths and the stack cap stay unread **[bin]** |
| Events | partial | Sleep and waitfor snapshot the function, the index, the stack, the frames and the object context, and store the event name. A positive delay is the manager's clock plus the delay. Status 2 means suspended. The unit of the clock and the order of due snapshots were not checked **[bin]** |
| Names and clock | partial | A call walks the stack down to the tag-0 marker, checks access and the parameter count, and can suspend on `classesdownloaded` and retry the call. The reserved-name walk was not read. The clock unit is open **[bin]** |

## Android

Only Classic 1.8's x86 engine was read as a GS2 machine. Classic 1.7 was read for the Java host, not for opcodes. Era 1.7, Era 2.0, Classic 2.0 and Classic 2.2 have native libraries and were not opened as VMs. Those four rows are open on every dimension. Do not project the 1.8 rules onto them, or back onto the Windows and Linux builds **[bin]**.

**Update (2026-11-20).** Classic 2.2 and Era 2.0 were matched function by function to Classic 1.8 in [static-reads-appendix-e-2026-11-20-n.md](static-reads-appendix-e-2026-11-20-n.md). Era 2.0 is the same engine as Classic 2.2. Classic 2.2 dispatches the same 165 opcode numbers as 1.8; 54 and 121 have handlers and 48, 49 and 164 do not. The event-function lookup ignores case in all three, so `onTimeout` and `onTimeOut` are one function. The limits listed under 1.8 are in identical functions in 2.2. Era 1.7 is stripped and ARM only, and Classic 1.6, 1.7 and 2.0 were not read **[bin]**.

### Classic 1.8

| Dimension | Grade | What this build does |
| --- | --- | --- |
| Parse | settled | The same four segments: event mask, function table with a `public.` strip, NUL-terminated strings, opcodes with the same marker widths. Jumps and functions are instruction indices. Fused opcodes are made while decoding and are not file bytes. A decoded instruction is 20 bytes here and 24 on the Windows notes; neither size is part of the file format **[bin]** |
| Slots | partial | Assignment uses separate setters for locals, references and properties, and leaves nothing on the stack. The desktop 0–1023 slot opcodes were not named in this reading **[bin]** |
| Opcodes | partial | 165 dispatch cases, 243 function selectors and 43 fusions, counted rather than listed. An opcode with no handler continues without popping. Four conditional branches: two always pop, and the short-circuit pair keeps the value when the branch is taken. The fold pass rewrites the first instruction of a group and skips the rest, so indices do not move. 54 and 121 have handlers; 48, 49 and 164 do not, so they continue without popping (read 2026-11-20 from the dispatch table, [note n](static-reads-appendix-e-2026-11-20-n.md#classic-22-against-classic-18)) **[bin]** |
| Maths | settled | Integer conversion truncates toward zero, which is not the desktop `floor(x + 0.0001)`. Remainder is `a − b·floor(a/b)`, so the sign follows the divisor, and a zero divisor yields 0. Division by zero yields 0. The machine's own boolean is non-zero; the boolean passed to a native call is `floor(v + 0.0001) ≠ 0`, so 0.5 is true inside the machine and false at a native call. Numbers compare equal within 0.0001. String comparison ignores case; the desktop VMs compare strings by bytes. The loop budget is 10000 with a generation counter that resets when the generation changes. The call stack refuses a new frame at 10000. The value stack grows by 100 and this helper has no 10000 cap. Which pass, the 10000th or the 10001st, stops the loop was not run **[bin]** |
| Events | partial | The queue refuses a new event at 1000. At that limit `onAllRCChat` is dropped silently and other events take the error path. `istimeout`, `created` and `initialized` go to the front. A scheduled event refuses a negative delay, lowercases the name, and is due within 0.0001 of its deadline. Event functions are found by putting `on` in front of the name and looking it up ignoring case, then in each joined class, so `onTimeout` and `onTimeOut` are one function (read 2026-11-20, [note n](static-reads-appendix-e-2026-11-20-n.md#event-names-ignore-case-18-22-and-era-20)). How `onActionServerSide` is spelled was not read **[bin]** |
| Names and clock | partial | A positive sleep saves a continuation; zero or less does not suspend. The clock either samples real time or steps by a configured interval. It is not always 0.05. The frame gate in front of timers starts at 50 ms and can be changed, and a late frame does not catch up. The desktop reserved-name walk was not read. Joining a class ignores one already joined, otherwise appends it and installs its event catchers **[bin]** |

## Reference implementations

These are ours. They are not a client reading. Where they disagree with a settled client cell, the client cell wins.

### seihai-core

The executor is profiled per client version. `Machine::new` is the 3.153 profile. Builds before 4.04r2 are given that profile. Mac 4.04r2 is given the September 2006 Mac profile. Mac 5.12 is given 5.00r7 with the PowerPC shift. 6.015 and 6.034 are given the 6.03r7 profile. There is no 6.1.1.3 or Android profile; an unknown version falls through to 3.153 **[src]** **[doc]**.

| Dimension | Grade | What it does |
| --- | --- | --- |
| Parse | partial | The GS2 path used here is a compiler into an in-memory script, not a four-segment file reader. The compiler keeps a `public.` prefix on the function name. Lookup accepts the plain name or that prefixed name, and the compare is case-sensitive. Clients strip the prefix at load **[src]** |
| Slots | settled | Store into a slot ignores an index outside 0–1023. A load of a slot that was never stored pushes 0 **[src]** |
| Opcodes | settled | The profile refuses 11, 104, 48, 49, 54 and 121 on the builds whose VM lacks them, and logs a skip. Other opcodes are attempted on every profile. Fused opcodes are not required; a bytecode file that never contains them still runs. 48 drops the pairs and pushes null, because there is no object value. 164 is not appended at load **[src]** **[doc]** |
| Maths | partial | Integer conversion, the 0.0001 equality, number-to-text, the two remainder rules and the two shift rules follow the profile. `b == 2` shortened to `a * a`, and the single-precision square root, run only on the 6.03r7 profile. The profile note also records that short-circuit from 5.24r4; the executor does not apply it on the 5.24r4 profile **[src]** **[doc]** |
| Events | settled | A timer expiry looks up the exact name `onTimeout`. `scheduleevent` drops a leading `on` without regard to case, keeps the rest of the spelling, and later looks up `on` plus that rest, so `onTimeOut` stays `onTimeOut`. `cancelevents` compares without case. `call_event` itself is case-sensitive. A function written `onTimeOut` does not run for the timer **[src]** |
| Names and clock | settled | Commands and the `timeout` property match without case. The clock is GServer-v2's frame clock: one frame is 0.05 s, and a duration becomes `(int)(t * 20)` frames. A scheduled event of less than one frame runs on the next frame. GServer-v2 never fires that event. While a script is sleeping, a due event waits. This is not the client's double clock **[src]** |

### GServer-v2

No GS2 bytecode VM. Server scripts are JavaScript. The wrappers are the event-name rule for that host **[src]**.

| Dimension | Grade | What it does |
| --- | --- | --- |
| Parse | settled | No segment reader. A weapon or NPC script is wrapped as a JavaScript function. There is nothing to say about `F0`–`F6` |
| Slots | settled | No GS2 slots |
| Opcodes | settled | No GS2 opcodes. `settimer` and `scheduleevent` are methods on the NPC object |
| Maths | open | Not a GS2 maths VM. Do not copy a client remainder rule onto it |
| Events | settled | The NPC wrapper declares `onTimeout` and copies it onto the NPC only when the script defined that exact identifier. The weapon wrapper declares `onActionServerSide` and assigns it even when the script did not define it. JavaScript identifiers are case-sensitive, so `onTimeOut` is a different function and is not copied to `onTimeout`. The weapon corpus's client event `onActionClientSide` is not one of these bindings **[src]** **[lab]** |
| Names and clock | settled | `timeout` and a scheduled event count down in frames of one twentieth of a second. Each frame subtracts one. At 0 the NPC's `onTimeout` is queued once. A count that starts at 0 is off, and a scheduled count that starts below one never runs **[src]** |

### gs2lib

The C++ support library under the server: sockets, packet ciphers, packet queues, packet ids and the client-version table. It is not a script machine **[src]**.

| Dimension | Grade | What it does |
| --- | --- | --- |
| Parse, slots, opcodes, maths, events | settled | None of these exist here. A script difference cannot be fixed in this library |
| Names and clock | settled | The timeout helper is an integer countdown used by socket waits. It does not name `onTimeout`, and it does not step a script clock |

### Client-shaped loader beside the notes

The C++ loader in the client reproduction parses the four segments, strips an exact `public.` prefix, and looks functions up without case, so `ONCREATED` matches `onCreated`. It fuses 200–233 on every profile, and fuses 234–242 only on the 6.00 profile. Its "4.2" opcode set includes both `waitfor` and object compare, so it does not represent 3.153, Windows 4.04r2, or the September 2006 Mac image. Slot stores and loads outside 0–1023 do nothing and read as 0. An action is started by looking up `on` plus the queued name **[src]**.

## Summary

Grades only. The evidence is in the section for that build. "Open" on a whole row means the image was not read; a profile may still lend it a neighbour.

| Build | Parse | Slots | Opcodes and fusion | Maths and limits | Event names | Names and clock |
| --- | --- | --- | --- | --- | --- | --- |
| 3.153 | partial | settled | settled | settled | partial | partial |
| Windows 4.04r2 | partial | open | settled | settled | partial | partial |
| Linux 4.04r2 | partial | open | settled | open | partial | open |
| Mac 4.04r2 | open | open | open | open | open | open |
| Mac, 2006-09-19 (4.20r6 label) | partial | settled | settled | settled | open | open |
| Linux 4.20r6 | partial | open | partial | partial | partial | open |
| Windows 4.20r8 | settled | settled | settled | settled | partial | settled |
| Linux 4.20r8 | open | open | partial | open | open | open |
| 5.00r7 and Windows 5.12 | settled | settled | partial | settled | partial | partial |
| Mac 5.12 | open | open | open | open | open | open |
| 5.24r4 through 6.00r4 | partial | settled | settled | settled | partial | partial |
| Linux 6.01r1 and 6.03r7 | partial | partial | settled | settled | partial | partial |
| Windows 6.03r7 | partial | partial | settled | settled | partial | partial |
| 6.015 and 6.034 | open | open | open | open | open | open |
| Unpacked Windows 6.1.1.3 | settled | partial | settled | partial | open | open |
| Mac 6.11r1 | partial | open | partial | partial | partial | partial |
| Android Classic 1.8 | settled | partial | partial | settled | partial | partial |
| Android Classic 2.2 and Era 2.0 | open | open | partial | partial | partial | open |
| Android Era 1.7, and Classic 1.6, 1.7 and 2.0 | open | open | open | open | open | open |
| seihai-core | partial | settled | settled | partial | settled | settled |
| GServer-v2 | settled | settled | settled | open | settled | settled |
| gs2lib | settled | settled | settled | settled | settled | settled |

gs2lib's settled cells mean the library has no script machine, not that a client rule was confirmed.

### Loans the 2026-11-13 side-by-side should no longer make

- Windows 4.04r2 was read. It is not an unread copy of the Mac image: the handler set matches, the shift rule is the x86 one, and the clock section above is its own **[doc]** **[bin]**.
- Windows 5.12's dispatcher matches 5.00r7. It is not an inference **[doc]**.
- 5.24r4, 5.30r3, 5.31r4, 6.00r2 and 6.00r4 are one VM. They are not 5.00r7 (48 and 49 are gone) and they are not 6.03r7 (the stack cap and the double-precision square root remain) **[doc]**.
- Unpacked Windows 6.1.1.3 and Mac 6.11r1 keep the double-precision positive square root. They are not 6.03r7's single-precision power rule **[bin]**.
- Linux 4.20r6 is not the September 2006 Mac image. The Linux notes give it opcode 11 and folds 200–233; the Mac image has neither **[bin]**.

### What the script corpora do not settle

The weapon survey and the world survey grade a compiler: which source it accepts, and which event names the weapons spell (`onCreated`, `onTimeout`, `onActionClientSide`, and the server binding `onActionServerSide`). They were compiled in the compiler's legacy mode. A strict mode, a legacy mode and an automatic choice between them change how much source is accepted. They do not change a client's opcode, a slot rule or a clock. Mode-split counts stay out of this page; the working tally names the exports. The published aggregates are [gs2-weapon-corpus-2026-11-14.md](../npc-library/gs2-weapon-corpus-2026-11-14.md) and [gs2-world-corpus-2026-11-12.md](../npc-library/gs2-world-corpus-2026-11-12.md) **[lab]**.

## Focus-build close-out of E#209 (G187, G088, 2026-11-25)

Static read of the stock 4.20r8 engine and the 5.12 engine image; nothing run. **[bin]** unless marked.

**`waitfor` on stock 4.20r8.** `waitfor(object, event, timeout)` returns 0 at once when the event is empty, the timeout is not above 0, or there is no owning script. Otherwise it saves the script state with result 1, the event name (lower-cased, a leading `on` removed) and a deadline of now + timeout, and pauses. If the deadline passes first, the timer clears it, sets the saved result to 0 and re-queues the event, so the script resumes with **0**; if the event arrives first, it resumes with the saved **1**. This matches the [retained 4.20r8-labelled input](gs2-wait-results-2026-11-22.md#separately-retained-420r8-labelled-input) point for point. Of the three 4.20r8 engines held, one differs from stock by a single patched byte and the packet-logger build by 290 bytes; the earlier export matches stock at every byte where the other two differ, so that retained input was very likely the stock file. **[bin][inf]**

**`sleep` on stock 4.20r8.** `sleep(t)` with t > 0 re-arms the object's own timeout timer (the one `settimer` uses) and resumes on `onTimeout` with no value, so a sleep replaces any pending `settimer`. `sleep(t)` with t ≤ 0 does not pause.

**5.12.** Opcodes 48, 49 and 54 are instruction-for-instruction the same as 5.00r7's, so the [5.00r7 results](static-reads-appendix-e-2026-11-20-b.md#gs2-opcodes-48-49-and-54-on-500r7-e209) hold: 54 takes object, member name and value and stores like 50; 49 lists in pop order with its count clamped to 0–10000; 48 takes name-then-value pairs with the upward-counting loop. The `waitfor` path and timer check also match 5.00r7: saved with 1, resumed with 0 on timeout and 1 if the event comes first. This promotes the earlier [doc] claim for 5.12 to [bin].

**48, 49 and 54 on stock 4.20r8.** None is handled; each is skipped with nothing popped, pushed or logged. For 48 and 49 the count and items stay on the stack, so the expression's value is whatever is on top (normally the count) and the following code runs on a misaligned stack. The 2026-11-19 fuzz recorded an empty value for 48/49 on 4.20r8; the static reading suggests that observation depended on the surrounding expression, not on a handler. **[bin][inf]**

## Still open

- [x] ~~Function-table case.~~ Read on 6.03r7 in [static-reads-appendix-e-2026-11-20-j.md](static-reads-appendix-e-2026-11-20-j.md#event-names-and-the-function-table-603r7): the lookup for a fired event ignores case. Other builds not read. Earlier text: No client reading shows whether `onTimeout` and `onTimeOut` are one function. seihai-core treats them as different; the C++ loader treats them as the same; GServer-v2's JavaScript bindings are the exact identifiers.
- [x] ~~`onActionServerSide` / `onActionClientSide` on a client VM.~~ Read on 6.03r7: 48 `clientside,<weapon>,…` becomes the weapon event `actionclientside`; `triggeraction` to `serverside`/`servernpc` goes to the server ([static-reads-appendix-e-2026-11-20-j.md](static-reads-appendix-e-2026-11-20-j.md#how-a-server-trigger-reaches-a-weapon-603r7)). The server wrapper and the weapon survey use those spellings. No client matcher was read.
- [x] ~~Operand order of opcodes 48 and 49, and a single description of how many values opcode 54 pops on 5.00r7.~~ Settled in [static-reads-appendix-e-2026-11-20-b.md](static-reads-appendix-e-2026-11-20-b.md#gs2-opcodes-48-49-and-54-on-500r7-e209): 54 takes three values, 49 lists in reverse push order, 48 takes name-then-value pairs with an upward-counting loop.
- [x] ~~The 6.x name of the loop-limit property.~~ `maxlooplimit`, scrambled ([static-reads-appendix-e-2026-11-20-j.md](static-reads-appendix-e-2026-11-20-j.md#the-6x-loop-limit-name)). 6.00r2 and 6.00r4 have the field without the plain name `maxlooplimit`.
- [ ] Mac 4.04r2, Mac 5.12, the December 2006 Mac 4.20r6, 6.015, 6.034, Android Era 1.7, and Classic 1.6, 1.7 and 2.0. Classic 2.2 and Era 2.0 are matched to 1.8 in [static-reads-appendix-e-2026-11-20-n.md](static-reads-appendix-e-2026-11-20-n.md); their execution loop was not read case by case.
- [x] ~~Maths on unpacked 6.1.1.3 and on Mac 6.11r1. The 6.03r7 single-precision square root does not transfer.~~ Both keep `b == 2` → `a * a` and take a positive `b == 0.5` in **double** precision ([note](static-reads-appendix-e-2026-11-24-g082.md)).
- [ ] Whether Linux 4.20r6's fusion and opcode 11, published from a handoff the editor did not re-run, match a fresh read of that ELF.
- [x] ~~The 5.00r7 event-queue cap of 1000, read on a backup from a patched install, against a stock image. 4.20r8's cap is 9999.~~ The 1000 cap is the engine's own ([below](#500r7-event-queue-cap-g084-2026-11-24)).
- [ ] Unity 7.x, left out of scope.

## 5.00r7 event-queue cap (G084, 2026-11-24)

Static read, nothing run **[bin]**.

- **The value.** Both event receivers compare the queued-event count with 1000. Below 1000 the event is queued. At 1000 or more the engine logs `Events number overrun for <name>` and returns 0, so the 1000th queued event is the last one accepted. The first receiver is the one that puts `istimeout`, `created` and `initialized` at the front of the queue; the second only appends. The overrun text is used by these two routines only.
- **Not a patch.** The unpatched 5.00r7 engine and the two patched engines held (the licence-check patch, and the same patch plus two auto-update gates) carry identical instructions in both receivers. Every patched byte sits in the licence-file check or the auto-update gates, nowhere near the event code.
- **Earlier 4.x.** A January 2007 4.x engine has the same two receivers with 10000 in place of 1000, which is the "longer than 9999" figure in the 4.20r8 row. That engine was not matched byte for byte to 4.20r8. The routine is unchanged between the two builds; only the compiled limit dropped.
- **Provenance limit.** No first-party 5.00r7 installer is held. Every 5.00r7 copy found comes from one unpacked release lineage, which ships the unpatched engine as its backup file. The unpatched image is therefore the best stock reference available, not an installer-verified one.

