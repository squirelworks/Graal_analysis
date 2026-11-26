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
  `thiso.f(...)` as `this.f`; the variable of a `for (x : …)` loop, as a use inside the
  loop; the list of `x in this.list`; and a bare `this` that owns a run-time member
  (`this.(name)`, `this.(name)(…)`). `this`, `thiso`, `temp`, `playero`, `pi`, `true`,
  `false`, `null` and `NULL` on their own are not otherwise.
- **What is not searched:** `with` bodies, `new … { }` blocks, `@` texts, the arguments of
  opcode built-ins (all but `pow`, whose arguments do count) and of `float(…)` and
  `_(…)`, statements left out as unused values (below), and the inline methods
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
  bare name `x` mean `temp.x` from there on, slot included, even where `x` had a slot of
  its own before the loop.
- The cache is not used inside `with` bodies, `new` blocks, opcode built-in arguments,
  inline method operands, or a dynamic member name.

## Instructions

- `OP_CMD_CALL` comes after `OP_JMP` only when the body contains a call. `format`, the
  inline methods, `float(…)`, `_(…)` and `new T` without call arguments are not calls. A
  `function () { … }` value whose body calls something counts as a call of the function
  it stands in.
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
  is a `return`. An `if`/`else` whose branches all return still gets one.
- Every copy of a function on an object (`obj.f` written twice) is kept, each with its own
  table entry.

## Logic chains

- A run of one operator (`a && b && c`, `a || b || c`) jumps to the end of the run. In
  `a && b || c` the `OP_AND` jumps to the `OP_OR`.
- As the test of an `if`, `while` or `for`, a top-level `&&` is one `OP_IF` per part.
- An `||` pushes all its parts but the last as values, each followed by `OP_OR`. Each
  `OP_OR` jumps to the final `OP_IF` of the last part.
- `!(chain)` is the chain, then `OP_NOT`, then `OP_IF`. As a value it has no
  `OP_INLINE_CONDITIONAL`.
- A ternary whose test is a chain is the chain, then `OP_IF`.
- An `if` whose bodies are both empty keeps only its test, as a dropped value (the chain or
  value, then `OP_INDEX_DEC`). A constant test emits nothing.

## Constants

- `+ - * / % ^ << >> & |` between non-negative number literals and `pi` fold to one
  number. `-(a op b)` folds; `2 + -1` does not.
- `@` between two text literals joins them. For `SPC`, `NL` and `TAB`, only the left
  literal and the separator join.
- **GS2:** `!true`, `!false`, `false && …` and `true || …` fold to `OP_TYPE_TRUE` or
  `OP_TYPE_FALSE`. A folded constant is not a call for `OP_CMD_CALL`.
- **Number text:**
  - A number within 0.0001 of an integer in the 32-bit signed range is written as that
    integer.
  - Larger numbers are written as the text `2147483647`, with its sign.
  - Any other number is written as its integer part and nine decimals, cut off rather
    than rounded. A fraction ending in `999` carries up, and trailing zeros are dropped.
  - The source spelling is not kept: `3.0` and `3` give the same bytes.

## Conversions

- Calls (`int`, `arraylen` and `strlen` included) count as untyped values, so a numeric use
  converts them with `OP_CONV_TO_FLOAT`.
- These need no conversion: comparisons, `==` and `!=`, `!`, `&&` and `||`, `++x`, `pi`,
  `true` and `false`.
- `!x` converts `x` unless it is a comparison, a range test or another `!`.
- **GS2:** the arguments of `substring` and `charat` are numbers. The arguments of `pos`,
  `starts`, `ends` and `positions` are text.
- **GS2:** the list methods `delete` and `subarray` take numbers. `insert` and `replace`
  take a number as the index. `subarray(i)` pushes -1 as the length.
- **GS2:** `@x` is text.
- `a @= b` is: the place, `OP_COPY_LAST_OP`, `OP_CONV_TO_STRING`, `b` as text, `OP_JOIN`,
  `OP_ASSIGN`.
- **GS2:** `obj.(@x)` converts `x`. When the name in brackets starts with text but goes on
  (`obj.(@n - 1)`), the whole expression is converted to text instead.
- **GS2:** the value of `x++` (the old value) is converted again where it is used.

## Other shapes

- **GS2:** bare `this`, `thiso`, `playero` and `temp` used as values are
  `OP_TYPE_VAR "name"`. As owners they keep their own opcodes. `player` and `level` keep
  their opcodes in both cases.
- **`new`:**
  - `new T()` pushes the text `unknown_object`, then the type.
  - `new T(x)` pushes `x`, then `OP_INLINE_NEW`, then the type.
  - With two or more arguments it pushes `unknown_object`.
- **GS2:** `pow(a, b)` is a script call by name and counts as a call. `OP_POW` is used
  only for `^`.
- **GS2:** `_(…)` is not a call.
- **Segment 1** is a bit mask of the script events whose names appear as plain names in
  top-level code (matched in any case; not when followed by a member or a call). The bits,
  from 0:
  - `playerenters`, `playertouchsme`, `playertouchsother`, `playerchats`, `playerhurt`,
    `playerdies`, `playerlaysitem`, `playerendsreading`;
  - `compusdied`, `emoticon`, `mousedown`, `mouseup`, `mousewheel`, `exploded`,
    `wasshot`, `waspelt`;
  - `keypressed`, `actionprojectile2`, three unused bits, `playerleaves`, `washit`;
  - two unused bits, `shapetrigger`, `playanimation`.

  The bit order is from our client notes.
- **Function table:**
  - Functions on `universe` drop `public.`.
  - A plain `onServerListerConnect` also gets a `universe.onServerListerConnect` entry at
    the same start, placed among the entries on an object in source order.

## Old names and short forms (GS2)

- `playerx`, `playery`, `playerreading` (and **[read]** `playerz`, `playerdir`) are
  `player.x` and so on.
- `imgwidth(…)` and `imgheight(…)` take the text between their brackets as it is written
  (leading blanks dropped, quotes kept) and call `getimgwidth` / `getimgheight` with it.
- `sarraylen(a)` pushes the text `a`, then `OP_OBJ_FROM_STR`, `OP_CONV_TO_OBJECT`,
  `OP_OBJ_SIZE`.
- `Enum.MEMBER` is the member's value. `VK_LEFT` is 37 (**[read]** `VK_UP` 38, `VK_RIGHT`
  39, `VK_DOWN` 40, `VK_DELETE` 46).
- `s.lower()` and `s.upper()` are calls of `lowercase` and `uppercase` on `s` as text.
- `float(x)` is `x` with `OP_CONV_TO_FLOAT` (unless it is a number already), and its
  result is converted again where a number is needed. `_(x)` converts `x` to text before
  `OP_TRANSLATE`.
- `obj.link()` is `OP_CONV_TO_OBJECT`, `OP_OBJ_LINK`. `a.indices(v)` pushes `a` as an
  object, then `v`.
- `x in |a, b|` converts both bounds to numbers; `x` is left as it is. `!(x in list)` is
  not converted before `OP_NOT`. A `?:` whose two branches are text is still converted.
- `new T() { … }` with no name pushes `OP_TYPE_VAR unknown_object` where the name goes,
  with no `OP_INLINE_NEW`.
- `xor` is `OP_BWX`, `~` is `OP_BWI`; `^=`, `<<=` and `>>=` work like `+=`. `f(x += 1)`
  passes the new value; on an element it stores, then reads the element again.
- Labeled loops: `outer: for …` and `outer: while …`, with `break outer;` (to the end of
  that loop) and `continue outer;` (to its step).

## Values that are left out (GS2)

- A statement that is only a built-in giving a value (`sin(…)`, `int(…)`, `float(…)`,
  `s.trim()`, `s.size()` and the like, not `waitfor`, `sleep` or `setarray`) emits
  nothing, arguments included, so a call inside it does not add `OP_CMD_CALL`.
- A statement that is only a name or `a.b` emits nothing. `destroy`, `hide`, `show` and
  `enableweapons` on their own are calls.

## Lambda names

A lambda is named `function_<id>_<n>`. Every lambda in one compile has the same `id`, and
`n` counts up from 1 in source order **[cap]**. The `id` is not taken from the source: the
same source captured twice got 1038 and then 1044, and the other captures got 1164, 1183
and 1184. It rises from one compile to the next, so it is a running count of the
server's compiles **[cap]**. No compiler can predict it from the script alone. Seihai
takes it as an input (`compile::Options::lambda_id`); a server passes its own count.

## `=` in tests (GS2, legacy)

- **`for` tests:** a test with `&&` or `||` is pushed as a value chain, then
  `OP_INLINE_CONDITIONAL`, then `OP_IF` (both captured cases, for example
  `temp.i > -1 && !temp.sel`). A test that is `x = v` stores, then `OP_CONV_TO_FLOAT`,
  then `OP_IF`.
- **`if` and `while` tests:** `=` compares, like `==`, also inside brackets:
  `(a = 1) == 2`. A second `=` to the right of it stores, and binds loosely: `a = 1 && b = 2`
  is `a == ((1 && b) = 2)`.
- **Storing into a value that is not a place** (a result, not a name, member or element):
  push the value, `OP_COPY_LAST_OP`, push what is stored, `OP_ASSIGN`.
- **Conditionals:** the branch after `?` may store (`c ? b = 2 : …`). An `=` after the
  branch after `:` stores into the whole conditional: `c ? b = 2 : d = 3` is
  `(c ? b = 2 : d) = 3`.

## GS1 input

No official GS1-to-GS2 body has been seen by us (Preagonal's GS1 fixtures are private).
**[read]** GS1 differs from GS2 in two ways: `format` counts as a call, and the built-ins
above push their arguments in reverse. Seihai keeps its earlier GS1 output elsewhere until
there is a capture to check against.

## Checked against the captures

Seihai's compiler on the 151 official captures **[cap][test]**. The first column is before
this work, then after the cache and layout rules (seihai-core #163), the rules on logic
chains, constants and conversions (#164), and the old names, left-out values, cache uses
and labeled loops (#165), and the lambda number and the `=` rules above (#166, with
each capture's lambda number given to the compiler).

| | Before | #163 | #164 | #165 | #166 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Byte-for-byte equal (legacy mode) | 0 | 54 | 113 | 144 | 151 |
| Different | 137 | 90 | 31 | 6 | 0 |
| Rejected by the compiler | 7 | 7 | 7 | 1 | 0 |
| Byte-for-byte equal (strict mode) | 0 | 53 | 112 | 138 | 144 |

The "Different" column for #163 counts 16 bodies with the same instructions as the
official one, which differ only in operand widths, string order or a final `OP_RET`. Of
the 6 different after #165, 5 differ only in a lambda's name. Without the lambda number,
#166 matches 146 in legacy mode; the other 5 differ only in that number. Strict mode
rejects the 7 captures that rely on the legacy `=` readings.

The variable-cache rules give the same slot list as the official body in all 1233
functions of the 150 captures Seihai compiles (1113 of 1136 before #165). 85 of those
captures use the cache. Seihai's reader reads all 151.
