# GS2 in unpacked Windows 6.1.1.3

Date: 2026-11-07. Static read of the listing in `client-internals/unpacked-6113.md`. Nothing was run. Tags: **[bin]**.

The 6.00 container, opcode effects and folds are `protocol/gs2-client-vm.md` and `protocol/gs2-client-only-opcodes.md`. The packed 6.113 listing added nothing because it had no switch (`protocol/gs2-6113.md`). This page is the switch in the unpacked image.

## Container

The walker reads a segment type and stops when the type is outside 1–4. **[bin]**

| Type | What this image does |
| --- | --- |
| 1 | Stores one integer. That is the event mask |
| 2 | Reads names. A name that starts with `public.` drops those seven characters and is recorded as public |
| 3 | Reads the string table |
| 4 | Reads opcodes. A decoded instruction is stored in a 24-byte record |

On a segment-4 opcode the operand markers are the same widths as 6.00. `F0`, `F1` and `F2` are a string-table index of 8, 16 and 32 bits. `F3`, `F4` and `F5` are a signed integer of 8, 16 and 32 bits, stored as a number. `F6` is a decimal string parsed to a number. **[bin]** (`protocol/gs2-client-vm.md#same-container`)

## What the dispatcher adds past 6.00

Nothing in the case list. The switch runs cases through 242 and has no case above 242. It includes 54, 121 and 200–242. It does not include 48 or 49. It does not include 161, 162 or 185–188, the names 4.2.0.8 reserves and does not run. **[bin]** (`protocol/gs2-client-only-opcodes.md#which-image-dispatches-it`)

An opcode with no case pops one value and joins the ordinary step. **[bin]**

## Cases 54 and 121

Case 54 rejects a stack count below 2, which is the 6.00 guard (a count above 1), not the 5.0.0.7 guard of three values. It drops two values, converts the value now on top to an object, copies a string onto it when an object pointer is present and clears the string otherwise, sets the tag to 4, and then calls the same store as opcode 50. **[bin]** (`protocol/gs2-client-only-opcodes.md#54-and-121`)

Case 121 rejects an empty stack. If either value's tag is 2, both go through the string helper. Otherwise the two numbers are added. **[bin]**

## Folds 234–242

The executor matches the 6.00 effects. The program counter moves one extra step for 234, 235, 240 and 242, two extra steps for 236, 237, 238 and 239, and 241 does not add a step. **[bin]** (`protocol/gs2-client-only-opcodes.md#folds-234242-in-600-only`)

| Case | What this image does |
| --- | --- |
| 234 | Clears the string when there is no object, copies it when there is, sets the tag to 4, skips the next opcode |
| 235 | Pushes a value with tag 4, no object and a copied string, then converts it to an object. Skips the next opcode |
| 236 | The 234 string step, then the number conversion. Skips the next two opcodes |
| 237 | The 234 string step, then the string helper used by case 121. Skips the next two |
| 238 | The 234 string step, then the object conversion used by case 54. Skips the next two |
| 239 | The 234 string step, then one further conversion. Skips the next two |
| 240 | Pushes the instruction's number and runs the same array read as opcode 131. Skips the next opcode |
| 241 | Pushes a value with tag 5, a null variable pointer and a property pointer taken from the instruction. Does not skip |
| 242 | Requires a call frame, runs a register store, and skips the next opcode |

The pair recogniser that rewrites 20, 22 and 47 into these cases was not separated in this read. The pairs stay the 6.00 table. This image shows that the executor still accepts the results. **[bin]**

## Script cache

A `.code` file shorter than eight bytes is rejected. The reader then compares the `GRESCR01` magic. A cache flag other than 1 returns an empty script. The CRC32 is taken over the bytes after the magic. On a match the container walker above runs. On a miss the class-script sender runs: slot `0xFE` calls `onSendWantClassScript`, and any other slot sends that id. **[bin]** (`protocol/gs2-client-vm.md#script-cache`)
