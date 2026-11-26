# What the official GS2 compiler emits: a behavioural spec (2026-11-26)

This note says which bytecode the official server-side GS2 compiler writes for a script,
as a list of rules. Seihai's compiler (`seihai-core` `scripting::gs2::compile`) is being
brought to these rules; this note is the spec it is written from, kept apart from the
code.

## Provenance

- **[cap]** The 151 official captures with sources in Preagonal.Scripting.GS2Compiler
  `dev` `3568f38` (`tests/official-baselines`), described in
  [preagonal-gs2-dev-compare-2026-11-26.md](preagonal-gs2-dev-compare-2026-11-26.md), and
  our own official 6.113 bodies
  ([gs2-official-bytecode-6113.md](../protocol/gs2-official-bytecode-6113.md),
  [gs2-official-functable-order-2026-11-16.md](../protocol/gs2-official-functable-order-2026-11-16.md),
  [gs2-official-jump-narrow-returns-2026-11-16.md](../protocol/gs2-official-jump-narrow-returns-2026-11-16.md),
  [gs2-official-varcache-functable-partial-2026-11-16.md](../protocol/gs2-official-varcache-functable-partial-2026-11-16.md)).
  Every rule below was checked against the captures; the counts are at the end.
- **[read]** Where the captures alone did not make a rule clear, Preagonal `dev`'s source
  (MPL-2.0) was read to learn what it does, and its output was used as a black box. This
  note states behaviour in our own words. It quotes no code, and nothing in it is a
  translation of their files. Implementations in MIT/Apache trees must be written from
  this note and the captures, not from their source.
- Their `Preagonal.Scripting.GSAst` package (no stated licence, private source) was not
  used, vendored or read beyond what the build needed.
- No capture, bytecode file or raw log is published here. Counts only.

Rules marked **[read]** were seen in `dev`'s output but not yet in a capture.

## File layout

- Integers, jump targets included, use the smallest marker that holds them (`F3`, then
  `F4`, then `F5`). There is no fixed 16-bit placeholder for forward jumps.
- The code segment does not end with an extra `OP_RET`. A script with no top-level code
  ends with the last function's own `OP_RET`; top-level code ends the way a function body
  does.
- Strings are stored in the order they are first used.
- Function table: functions not on an object come first, in the order the engine's name
  hash list walks them, keyed by the name without `public.`. Functions on an object
  (`obj.f`, the `universe` entries) follow in source order.
  - The hash: start at 0x1505; for each byte, multiply by 17 and xor the byte, where `A`–`Z`
    count as lower case and other bytes as signed.
  - The list starts with 32 buckets and grows eight times when its count reaches the
    bucket count. A new entry goes to the front of its bucket, and the walk goes bucket by
    bucket from the first.
- Jump threading: an `OP_SET_INDEX`, `OP_SET_INDEX_TRUE`, `OP_OR`, `OP_IF` or `OP_AND`
  whose target is itself an `OP_SET_INDEX` jumps straight to the end of that chain.

## The variable cache (opcodes 45, 46, 47)

Each function (not a lambda, not top-level code) may keep often-used names in numbered
slots.

- **What counts as a reference:** a plain name (`x`, `player`, `client`, `level`); `this.x`,
  `thiso.x` and `temp.x`; the name of a script or host call; `this.f(...)` and
  `thiso.f(...)` as `this.f`. `this`, `thiso`, `temp`, `playero`, `pi`, `true`, `false`,
  `null` and `NULL` on their own are not.
- **What is not searched:** `with` bodies, `new … { }` blocks, `@` texts, the arguments of
  opcode built-ins (all but `pow`, whose arguments do count), and the inline methods
  `size type indices link index length substring pos charat starts ends trim tokenize
  positions subarray clear add delete insert remove replace lower upper`.
- **Which names get a slot:** a name referenced five times or more in the function, or at
  least once inside a loop. Inside a loop means a `while` test or body, a `for`
  initialiser, test, step or body, or a `for (… : …)` list or body.
- **Slot numbers:** all referenced names are put through the hash-list order above, and
  the names that get a slot are numbered in that order from 0.
- **Prologue:** after `OP_JMP`, and after `OP_CMD_CALL` when the function has one, each
  slot in order: the name's push (`OP_TYPE_VAR name`; or the owner opcode, `OP_TYPE_VAR
  member`, `OP_MEMBER_ACCESS`; or `OP_PARAMS`), then 47, then 45 with the slot number,
  then `OP_INDEX_DEC`.
- **Uses:** every later push of that name is 46 with the slot number.
- A bare name first seen as `temp.x` uses the `temp.x` slot. `for (temp.x : …)` makes the
  bare name `x` mean `temp.x` from there on.
- The cache is not used inside `with` bodies, `new` blocks, opcode built-in arguments,
  inline method operands, or a dynamic member name.

## Instructions

- `OP_CMD_CALL` comes after `OP_JMP` only when the body contains a call. `format`, the
  inline methods and `new T` without call arguments are not calls.
- A member owner gets `OP_CONV_TO_OBJECT`, unless it is a root pushed by its own opcode
  (`this`, `thiso`, `player`, `playero`, `level`, `temp`) and not loaded from a slot. An
  indexed read always gets `OP_CONV_TO_OBJECT` before a further index or member.
- A dynamic member name `obj.(expr)` gets no `OP_CONV_TO_STRING`; a `this` owner is
  converted.
- `sin cos arctan vecx vecy abs int exp log random min max char` push their arguments in
  source order.
- `makevar("text")` pushes the text with no `OP_CONV_TO_STRING`. A string method converts
  its receiver only when it is not text. `s.substring(a)` pushes -1 as the length.
  `"text".length()` is the byte count as a number.
- `OP_IN_RANGE` carries an integer operand. All 26 seen are 0. **[read]** The other values
  mark open bounds (2 for the lower, 1 for the upper).
- `switch`: a jump to the tests, the bodies, a jump out after the last body, then the
  tests in label order; `default` puts `OP_SET_INDEX` at its place among them.
- `params` is `OP_PARAMS` (190); `NULL` is `OP_TYPE_NULL`.
- `for (… : …)` drops three values at its end.
- A function ends with `return 0` (`OP_TYPE_NUMBER 0`, `OP_RET`) unless its last statement
  is a `return`.

Seen in the captures and not yet written into Seihai: folding numeric constants
(`1 + 2` to one number), joining string literals, folding enum members `A.B` to their
value, `OP_AND` for some `&&` chains where an `OP_IF` chain is expected, a cached bare
`this` in some functions, and some `OP_CONV_TO_FLOAT` choices.

## GS1 input

No official GS1-to-GS2 body has been seen by us (Preagonal's GS1 fixtures are private).
**[read]** GS1 differs from GS2 in two ways: `format` counts as a call, and the built-ins
above push their arguments in reverse. Seihai keeps its earlier GS1 output elsewhere until
there is a capture to check against.

## Checked against the captures

Seihai's compiler after the change, on the 151 official captures **[cap][test]**:

| | Before | After |
| --- | ---: | ---: |
| Byte-for-byte equal (legacy mode) | 0 | 54 |
| Same instructions; only operand widths, string order or a final `OP_RET` differ | 21 | 16 |
| Different | 116 | 74 |
| Rejected by the compiler | 7 | 7 |
| Byte-for-byte equal (strict mode) | 0 | 53 |

The variable-cache rules give the same slot list as the official body in 1113 of 1136
functions in the 144 readable captures. 82 of those captures use the cache. Seihai's reader
now reads all 151 (it refused 8 before, all on `OP_IN_RANGE`'s operand).
