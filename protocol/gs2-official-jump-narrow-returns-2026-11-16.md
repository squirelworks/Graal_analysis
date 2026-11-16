# Official GS2 bodies: jumps, narrow markers, and missing returns

Date: 2026-11-16. Tags: **[cap]** for offline walks of held bodies; **[inf]** where pass *existence* is unproven.

Leads-only confirm against a third-party claim about post-emit compiler passes. No third-party code. Bodies, keys and names stay private — counts only.

## On the 19 official 6.113-era bodies

| Check | Result | Tag |
| --- | --- | --- |
| Jump whose target is an unconditional jump (opcode 1) | **0 / 2239** jumps | [cap] |
| Jump whose target is any jump op (1–5) | **69** (almost all conditional→conditional chains) | [cap] |
| Or→Or jump chains | **0** | [cap] |
| Integer markers | F3 **5113**, F4 **3128**, F5 **19** | [cap] |
| Oversized integer (F4 value fits F3, or F5 fits F4) | **0** | [cap] |
| String markers | F0 **11251**, F1 **3045**, F2 **0** | [cap] |
| Oversized string (F1 value fits F0) | **0** | [cap] |
| All nineteen F5 sites | Truly need a wide integer load | [cap] |

Official GS2 output is **consistent with** “no live jump→unconditional leftovers” and **strict narrowest** integer/string markers. Consistency does **not** prove a post-emit retarget or shrink pass exists on the official compiler — emit-time discipline alone can produce the same stream. **[cap][inf]**

GS1-mode Or→Or threading is **not testable** on these nineteen (all GS2-shaped; segment 1 always zero). **[cap]**

## Enlarged residual: bodies that do not end in a return

On an enlarged **660**-body sample, **18** bodies do **not** end in a return instruction. That is a real residual shape against a claim that every body is sealed with a final return. It does not by itself prove or refute jump-threading or marker-narrowing passes. **[cap]**

Open-compiler test baselines elsewhere in the held lab tree **do** leave jump→unconditional leftovers and wide F4 markers — a contrast to the captured official/login streams, still not a proof of which passes the official compiler runs. **[cap][inf]**

## Still open

- Pass *existence* on the official compiler (before/after fixture or official binary).
- GS1 Or→Or threading on a real GS1-compiled body.
- Whether the 18 non-return endings are intentional, truncated, or a distinct emitter path.
