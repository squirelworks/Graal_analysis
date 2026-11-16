# GS2 value-semantics: stock answers vs third-party claims

Date: 2026-11-16. Tags: **[bin]** for stock VM reads (5.00r7 / 6.x, with 4.20r8 where noted); **[inf]** where a Windows helper remains unopened.

Leads-only confirm against a third-party engine claim. No third-party code. Extends existing rows in [`gs2-vm-by-version.md`](gs2-vm-by-version.md) and related VM notes — this note only records which claimed defaults match stock and which do not.

## Match stock

| Rule | Stock |
| --- | --- |
| Number equality / order | Within **0.0001**; integer coerce is `floor(x + 0.0001)` **[bin]** |
| `/` and `%` by zero | Push **0** **[bin]** |
| Floored `%` | Yes on **5.00r7** / **6.x**; **4.20r8** adds `+0.0001` inside the quotient **[bin]** |
| `charat` out of range | Empty string **[bin]** |

IEEE-754 **0.0001** appears in the 5.00r7 engine, 4.20r8 engine, and Linux 6.03r7 images checked for this pass. **[bin]**

## Same outcome, different mechanism

A third-party claim that `pow` clamps NaN to 0 after a bare library call is **not** how stock writes the power opcode. Stock uses a **branched** `a^b` (positive → library pow; zero base → 0; negative base → parity / reciprocal / else **0**). Scripts that would NaN under a raw `pow` still see **0** on stock, but not via a post-`pow` `isnan` check. Keep the branched writer. **[bin]**

## Mismatch stock

| Claim | Stock |
| --- | --- |
| Fixed **100 000** back-edge budget; `ontimeout` exempt | Default budget is **10 000** on 5.00r7 / 6.03r7; 5.00r7 exposes `this.maxlooplimit` (clamped); no `ontimeout` exemption string found; float64 **100 000** absent from those engines while **10 000** is present **[bin]** |
| `waitfor` is a no-op that always pushes 0 | From **4.20r8** on, opcode 11 registers a real wait; resume pushes **1** on catch and **0** on timeout **[bin]** |

## Still open

- Whether Windows `beginswith` / `endson` (opcodes 116/117) ignore case — a third-party claim says yes; Android classic string compare ignores case, but that is not a substitute for opening the Windows helpers. **[bin][inf]**
- Tiny live fixtures for `starts`/`ends` case on **5.12** / **6.03r7**. **[lab]**
