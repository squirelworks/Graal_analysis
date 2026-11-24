# Static reads appendix E — G082 maths (2026-11-24)

Date: 2026-11-24. Static reads of the power helper on unpacked Windows 6.1.1.3 and on Mac OS X 6.11r1. Nothing was run. Tags: **[bin]**. Closes the open maths line of [gs2-vm-loader-diff.md](gs2-vm-loader-diff.md#still-open).

## Question

Does the 6.03r7 single-precision square root for a positive `a ^ 0.5` transfer to unpacked 6.1.1.3 or to Mac 6.11r1?

On 6.03r7 (Windows and Linux) the power helper checks `b == 2` first (`a * a`), and a positive `b == 0.5` takes the square root in single precision (truncate to float, root, widen back). See [gs2-vm-loader-diff.md](gs2-vm-loader-diff.md#601r1-and-603r7) and [gs2-vm-by-version.md](gs2-vm-by-version.md#maths-and-text).

## Unpacked Windows 6.1.1.3

**[bin]** The power helper on the unpacked image keeps the `b == 2` short path (`a * a`).

**[bin]** When the exponent compares equal to `0.5` and the base is positive, the helper calls the double-precision square-root path. It does **not** truncate the base through a single-precision temporary before the root, and it does not round the result through float afterwards. That is the 5.24r4–6.00r4 double-precision rule, not the 6.03r7 single-precision rule.

**[bin]** Other exponents fall through to the general power library path. Remainder, shifts, stack caps and number-to-text were not re-opened on this image.

## Mac OS X 6.11r1

**[bin]** The named power helper (`PowerX` of two doubles) checks `b == 2` first and returns `a * a`.

**[bin]** When the base is positive and the exponent compares equal to `0.5`, the helper takes a double-precision square root (`sqrtsd`). It does **not** convert through single precision (`cvtsd2ss` / `sqrtss` / `cvtss2sd`). Other exponents call the C `pow` stub.

**[bin]** Negative-base branches, NaN handling beyond those paths, remainder, shifts and the value-stack cap were not re-opened here. The earlier runner note's open maths cell is retired only for this power rule.

## What this closes

| Build | `b == 2` | Positive `b == 0.5` | Grade for that rule |
| --- | --- | --- | --- |
| 6.03r7 (prior) | `a * a` | single-precision root | settled (prior) |
| Unpacked Windows 6.1.1.3 | `a * a` | double-precision root | settled **[bin]** |
| Mac 6.11r1 | `a * a` | double-precision root | settled **[bin]** |

The 6.03r7 single-precision square root does **not** transfer to either of these two builds.

## Limits

- Static only. No script was executed.
- Remainder, shifts, integer conversion, equality, number-to-text and stack/loop caps on these two images stay as in the loader-diff rows unless a later note re-opens them.
- seihai-core's `VmProfile` still applies `float_sqrt` only on the 6.03r7 profile; this note does not change that source.
