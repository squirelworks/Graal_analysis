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
