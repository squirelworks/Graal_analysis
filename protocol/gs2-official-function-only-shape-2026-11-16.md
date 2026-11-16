# Official GS2 bodies: function-only image shape (full 19)

Date: 2026-11-16. Tags: **[cap]** for the offline walk; **[lab]** / **[inf]** for the open live question (PG1).

Leads-only. No third-party code. Bodies, keys and names stay private — structure only.

## Observation

Every one of the **19** official 6.113-era GS2 bodies in [gs2-official-bytecode-6113.md](gs2-official-bytecode-6113.md) begins with an unconditional jump (opcode **1**) whose target equals the body’s instruction count — a jump from the first instruction to the end of the stream. **[cap]**

Under the usual reading of a “functions-only” image (no executable top-level statements; the leading jump skips past the whole top level to the end, and named functions live at their segment-2 indices), **all 19** match that shape. **[cap][inf]**

## What this does and does not settle

| Question | Status |
| --- | --- |
| Do held official server caches look function-only? | **Yes** on these 19 **[cap]** |
| Does a stock client re-run top-level code before every event when the image is **not** jump-past-end? | Still open (PG1) — needs **[lab]** |
| Do stock **4.20r8**, **5.12**, **6.03r7** treat jump-past-end as “skip the top-level pass”? | Still open **[lab]** |
| If a named handler starts at op 0, is it skipped after a whole-script pass? | Still open **[lab]** |

A bounded Linux **4.04r2** event experiment elsewhere already suggests a top-level re-run on a non–function-only fixture; fold that result, do not replace it. **[lab]**

These nineteen bodies alone cannot settle PG1: they never exercise a script with real top-level statements. **[cap]**

## Still open

- Three loopback fixtures on stock **4.20r8**, **5.12**, and **6.03r7**: top-level + `onCreated`; function-only twin; handler at op 0.
- Static dispatch entry on **4.20r8** and **6.00** for the same shortcut.
