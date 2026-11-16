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
