# The GS2 VM by client version, 3.153 to 6.03r7

Date: 2026-11-13. Sources: static reads of six client VMs, published as behaviour in
squirelworks/seihai-core `documentation/gs2-vm-versions.md` (PR #27, release 0.0.23) **[doc]**,
which this note restates for the reference. The reads themselves are **[bin]**. No addresses or
decompiled code are reproduced.

Earlier notes read one engine at a time: the 4.2.0.8 executor and the 5.0.0.7 additions in
[gs2-vm-from-engines.md](gs2-vm-from-engines.md), the 6.1.1.3 runner in [gs2-6113.md](gs2-6113.md),
and the client-side opcode list in [../protocol/gs2-client-vm.md](../protocol/gs2-client-vm.md).
This note puts the builds side by side: which opcodes each VM handles, what the load-time
optimiser fuses, the limits, and the maths and text rules that change between builds.

## What was read

| Build | Platform | How the VM was found | Tag |
| --- | --- | --- | --- |
| 3.153 | Mac OS X PowerPC | the dispatcher as one switch | [bin] |
| 4.20r6 | Mac OS X PowerPC | the dispatcher as one switch | [bin] |
| 4.20r8 | Windows x86 | the dispatcher switch, plus the load-time optimiser | [bin] |
| 5.00r7 | Windows x86 | the dispatcher switch | [bin] |
| 6.01r1 | Linux | a computed-goto handler table, one function per handler | [bin] |
| 6.03r7 | Linux | a computed-goto handler table, one function per handler | [bin] |

Builds that were not read take the nearest earlier VM that was **[inf]**: 4.04r2 (Windows
and Mac) and 4.20r6 take 4.20r6's; 5.12 to 5.31r4 take 5.00r7's (the Mac 5.12 with the
PowerPC shift rule, assumed); 6.00r2, 6.00r4, 6.015, 6.034 and 6.03r7 take 6.03r7's, and
6.01r1 has the same handler set. The 7.x (Unity) VM was not read.

## Opcodes each VM handles

| Build | Opcodes handled | Change from the build before | Tag |
| --- | --- | --- | --- |
| 3.153 | 1–10, 20–27, 30–47, 50–53, 60–103, 110–120, 130–142, 150, 151, 163, 180–184, 189, 190 | — | [bin] |
| 4.20r6 | as 3.153, plus 104 | object compare (104) | [bin] |
| 4.20r8 | as 4.20r6, plus 11 and 200–233 | `waitfor` (11); the optimiser's own opcodes | [bin] |
| 5.00r7 | as 4.20r8, plus 48, 49, 54, 121 | object and number-list literals, a three-operand member store, add-or-join | [bin] |
| 6.01r1, 6.03r7 | as 5.00r7 without 48 and 49, plus 0, 164, 234–242 | an end-of-script sentinel (164) and more fused opcodes | [bin] |

### Opcodes the open compilers do not name

| Op | Builds | Behaviour | Tag |
| --- | --- | --- | --- |
| 45 | all | copies the top into local slot *n* (operand, *n* < 1024) of the running function without popping it | [bin] |
| 46 | all | pushes a copy of local slot *n* | [bin] |
| 47 | all | turns the top into a resolved variable reference, creating the variable; with 45 and 46 this caches a variable for repeated use | [bin] |
| 48 | 5.00r7 only | object literal from *n* name/value pairs | [bin] |
| 49 | 5.00r7 only | list of *n* numbers, *n* clamped to 0–10000 | [bin] |
| 54 | 5.00r7 on | a member store with three operands; what it stores is not understood | [bin] |
| 66 | all | `a && b` as a value: 1 or 0, both sides evaluated | [bin] |
| 67 | all | `a \|\| b` as a value: 1 or 0, both sides evaluated | [bin] |
| 121 | 5.00r7 on | `+` that joins as text when either operand on the stack is a string, else adds | [bin] |
| 164 | 6.x | appended when a script loads: ends the script and goes on to the next; never in a file | [bin] |

### Named opcodes with version notes

- **11, `waitfor`** (4.20r8 on) pops the timeout, the event and the object. With a non-empty
  event and a timeout above 0 the VM registers the event, saves the run and returns; the run
  resumes with 1 when the event comes. Otherwise it pushes 0 **[bin]**. That a timeout that runs
  out gives 0 is assumed; that path was not followed **[inf]**.
- **104, object compare** (4.20r6 on) compares the two values and leaves -1, 0 or 1 **[bin]**.

### The load-time optimiser (4.20r8 on)

When a script loads, 4.20r8 and later rewrite common sequences into single internal opcodes.
Compilers never write these; a reimplementation does not need them to run bytecode, but they
explain the handlers above 200 **[bin]**.

| Internal | Fuses |
| --- | --- |
| 200–207 | number literal + arithmetic 60–67 |
| 208–215 | arithmetic 60–67 + assign |
| 216–223 | number literal + arithmetic + assign |
| 224–227 | number literal + compare 72–75 |
| 228–233 | slot load 46 + 30, 33, 34, 36, or 52/53 with a pop |
| 234–242 (6.x) | variable + member access, variable + call (241), 47 + 45 (242), number + array index (240) |

## Limits

| Limit | 3.153 | 4.20r6 | 4.20r8 | 5.00r7 | 6.x | Tag |
| --- | --- | --- | --- | --- | --- | --- |
| value stack | 256 | 10000 | 10000 | 10000 | none | [bin] |
| loop passes, per loop | 10000 | 10000 | 10000 | 10000, `maxlooplimit` | 10000, settable | [bin] |
| call depth | 10000 | 10000 | 10000 | 10000 | 10000 | [bin] |

5.00r7 adds `this.maxlooplimit`, clamped to 100–1000000. 6.x keeps the limit in a field of the
script object (default 10000); its property name is scrambled in the binary and was not
recovered **[bin]**.

## Maths and text

| Rule | Behaviour | Tag |
| --- | --- | --- |
| integer conversion (`int()`, bitwise operators, indices) | every VM computes `floor(x + 0.0001)`, not `floor(x)` | [bin] |
| `a % b` | 0 when `b` is 0. 4.20r6 and 4.20r8 compute `a - floor(a/b + 0.0001) * b`; 3.153, 5.00r7 and 6.x drop the tolerance | [bin] |
| `a ^ b` | a positive base goes to `pow`; a zero base gives 0; a negative base gives 1 for `b == 0`, `±pow(-a, b)` by parity for an integer `b`, `1/pow(a, -b)` for a negative `b`, else 0. 4.x and 5.x add `b == 0.5` → square root. 6.x checks `b == 2` first (`a * a`) and takes a positive base's square root in single precision | [bin] |
| shifts | the PowerPC builds (3.153, 4.20r6) take the count modulo 64 and give 0 or -1 past 31; the x86 builds (4.20r8 on) take it modulo 32 | [bin] |
| comparisons | two numbers are equal within 0.0001 in every VM; a string against a number compares as the number it reads as; two strings compare by bytes | [bin] |
| number to text (3.153 and 6.x alike) | `\|x\| < 0.0001` is `"0"`; otherwise the sign, the integer part (truncated, at most 2147483647) and up to 9 decimals, truncated with trailing zeros dropped, where a fraction ending in 999 is carried up | [bin] |

The number-to-text rule is what a `+` join, `format("%f")` and `format("%s")` produce.

## Not known

- What opcode 54 stores, and the operand order of 48 and 49.
- The value `waitfor` gives when its timeout runs out.
- The 6.x name of the loop-limit property.
- 4.04r2 (both builds), 5.12 to 5.31r4 (both 5.12 builds), 6.00r2 and 6.00r4 were not read;
  their rows above are inferred from the nearest read build.
- The 7.x VM, and the builds that borrow a VM from another build.
