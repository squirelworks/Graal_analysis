# GS2 opcodes the clients run and the compiler does not emit

Date: 2026-11-07. Tags as in `README.md`. Nothing was executed.

The checklist of names and the container stay in `protocol/gs2-client-vm.md`. This note is the effect of the opcodes that checklist leaves unread: the ones Graal's client VM dispatches and the MPL-2.0 Preagonal compiler does not emit. **[bin][doc]**

Images: Windows 4.2.0.8 `GraalEngine.dll`, 5.0.0.7 `GraalEngine.dll`, and the unpacked Windows 6.00r2 and 6.00r4 executables. 6.00r4's cases for these opcodes have the same shape as 6.00r2. **[bin]**

The compiler is [Preagonal.Scripting.GS2Compiler](https://github.com/Preagonal/Preagonal.Scripting.GS2Compiler) at `7878bc5`. Its private `Op` enum is `GS2Compiler.cs` lines 2160–2275. That enum has no member for any opcode below, so the compiler has no emitter for them. Opcodes 200 and above are also absent from the enum. **[doc]**

A fused opcode exists only on the decoded instruction list. The byte stream still uses the unfused opcode. The fold rewrites the first opcode and the executor skips the one or two that were swallowed. **[bin]**

## Which image dispatches it

| Opcode | Name | 4.2.0.8 | 5.0.0.7 | 6.00r2 and 6.00r4 |
| --- | --- | --- | --- | --- |
| 43 | `makeoldscriptvar` | yes | yes | yes |
| 45 | `setreg` | yes | yes | yes |
| 46 | `getreg` | yes | yes | yes |
| 47 | `makeprop` | yes | yes | yes |
| 66, 67 | value and, value or | yes | yes | yes |
| 104 | `compare` | yes | yes | yes |
| 190 | `loadparams` | yes | yes | yes |
| 200–233 | folds of the rows above | yes | yes | yes |
| 48, 49 | no long name read | no | yes | no |
| 54, 121 | no long name read | no | yes | yes |
| 234–242 | further folds | no | no | yes |

5.0.0.7's script switch stops at 233 apart from 48, 49, 54, and 121. The 6.00 script switch has 54, 121, and 234–242, and has no case 48 or 49. **[bin]**

## 43 `makeoldscriptvar`

The top value stays on the stack. Its string is split on `.`. The slot's tag becomes object, and the object pointer is the path that was found. An empty string, or an empty piece between dots, stores a null object. **[bin]**

The first piece:

| First piece | Object |
| --- | --- |
| `this` | the current non-player from the `with` stack |
| `thiso` | the variable that owns the running script |
| `player` | the current player |
| `playero` | the player object kept beside the machine |
| `client`, `clientr`, `serverr` | a child of that player object, created when missing, using this same name |
| any other name | a child of the current player, created when missing, using this same name |

Each later piece is a child of the object so far. A missing child is created. `this`, `thiso`, `player`, and `playero` are the objects themselves. The three `client` / `server` spellings are not: they are children of the player object. **[bin]**

## 45 `setreg` and 46 `getreg`

Both take the instruction's number, truncated toward zero. An index in 0..1023 selects a slot on the current call frame. The frame's list grows up to that index. An empty stack or a missing frame stops the script. **[bin]**

`setreg` copies the top value into that slot and leaves the value on the stack. An index outside 0..1023 does not write. `getreg` pushes a copy of the slot. An index outside 0..1023 pushes the number 0. **[bin]**

## 47 `makeprop`

The top value is rewritten in place as a resolved variable (tag 5). A number becomes an empty resolved value. An object keeps its object pointer. A string or a variable name is resolved, and a missing name is created. The resolver tries a property of the object before a child variable. **[bin]**

## 66 and 67

Both need two values. The right-hand value is popped. The left-hand number field becomes 0 or 1. The tag is left as it was. Only the number field is tested, so a zero number is zero whatever the tag says. **[bin]**

| Opcode | Result |
| --- | --- |
| 66 | 1 when both numbers are not 0, otherwise 0 |
| 67 | 1 when either number is not 0, otherwise 0 |

The jump forms stay at 3 and 5. **[bin]**

## 104 `compare`

The same helper as equality. It needs two values, materialises both, and pops the right-hand one. The result is a three-way code: −1 when the left is less, 0 when they match, 1 when the left is greater. **[bin]**

| Tags | Comparison |
| --- | --- |
| two numbers | numeric, and two numbers within 0.0001 count as equal |
| a number and a string | the string is parsed as a number, then the same numeric test |
| two strings | byte by byte, with A–Z folded to a–z |
| a number and an object | the number against the object pointer, read as an unsigned integer |
| two objects | the object pointers, ordered numerically |
| an object and a string | a string kept on the object against the other string, when the object pointer is not null |
| any other pair | 0 |

The three-way code is written into the number field of the popped right-hand slot. The left-hand slot, which remains on the stack, is marked as a number and its number field is not replaced. Equality (opcode 70) uses the same helper and does write 0 or 1 onto the remaining slot. **[bin]**

## 190 `loadparams`

Pushes one object. The pointer is the parameter object installed for this call, the same object the name `params` resolves to. A missing parameter object is pushed as a null object. The opcode does not look a name up. **[bin]**

## Folds 200–233

The peephole pairs two or three decoded opcodes. The first is rewritten. The number on a `loadfloat` stays on that instruction and is the right-hand operand. The left-hand value is already on the stack. **[bin]**

| First | Next | Result | What the executor does |
| --- | --- | --- | --- |
| 20 `loadfloat` | 60–67, and the one after that is not 50 | 200–207 | the top number is combined with the immediate, and the following opcode is skipped |
| 20 | 60–67, then 50 `assign` | 216–223 | the destination under the left value is assigned that value combined with the immediate, both stack values are consumed, and the next two opcodes are skipped |
| 60–67 | 50 `assign` | 208–215 | three stack values, destination under left under right; the destination variable is assigned left combined with right, and the assign opcode is skipped |
| 20 | 72–75 | 224–227 | the top value compared with the immediate, replaced by 0 or 1, and the compare opcode is skipped |
| 46 `getreg` | 33, 34, or 36 | 228–230 | push that register, then convert to number, string, or object, and skip the conversion |
| 46 | 52 or 53, then 32 | 231 or 232 | increment or decrement the register in place, push nothing, and skip the increment and the pop |
| 46 | 30 | 233 | push that register twice, and skip the copy |

The combinations, read one by one: **[bin]**

| Result | Combination |
| --- | --- |
| 200, 208, 216 | add |
| 201, 209, 217 | subtract |
| 202, 210, 218 | multiply |
| 203, 211, 219 | divide, and a zero divisor stores 0 |
| 204, 212, 220 | remainder, and a zero divisor stores 0. A negative dividend uses the same toward-negative truncation as opcode 64 |
| 205, 213, 221 | power, the same branches as opcode 65 |
| 206, 214, 222 | 1 only when both sides are not 0 |
| 207, 215, 223 | 1 when either side is not 0 |

224 is less-than, 225 greater-than, 226 less-or-equal, 227 greater-or-equal. The compare is the numeric three-way test above, including the 0.0001 band. A string is parsed as a number first. An object is compared as its pointer. The immediate is the right-hand side. **[bin]**

228 converts with the number conversion and does not create a name. 229 uses the string conversion. 230 uses the object conversion and does create a missing name. **[bin]**

The assign forms call the same store as opcode 50: the value is resolved, a property setter is used when the slot has a property, and otherwise the variable's number is written. **[bin]**

## 48 and 49, in 5.0.0.7 only

Both require a non-empty stack. 4.2.0.8 and the two 6.00 images have no case. **[bin]**

Opcode 48 allocates a new variable with an empty name and registers it on the universe. The top number is increased by 0.0001 and then truncated toward zero, and a negative non-integral result is moved one further down. When that count is positive, and at least three values are on the stack, the loop takes pairs from under the count: the upper of the pair is the value, the lower is converted to a string and used as a child name, and a missing child is created. The count is discarded by the first pop. The loop repeats until fewer than three values remain, so the original number is not a pair count. The new variable then replaces the slot left on top. A count that is not positive, or a positive count with fewer than three values on the stack, stores the new variable on the current top and takes no pairs. **[bin]**

Opcode 49 truncates the top number the same way, without the 0.0001 bias, and clamps it to 0..10000. It builds an array and appends that many numbers from under the count, converting each to a number. The count itself is not an element. If the stack runs out, the loop stops. The array object replaces the slot the loop landed on. A count of 0 replaces the top with an empty array. **[bin]**

## 54 and 121

Present in 5.0.0.7 and in both 6.00 images. Absent in 4.2.0.8. **[bin]**

Opcode 54 needs three values in 5.0.0.7 (the stack index is at least 2) and a stack count above 1 in 6.00. It drops two values, converts the value now on top to an object, and will create a missing name. If that value has an object pointer, the string from the slot above is copied onto it. Otherwise the string is cleared. The tag becomes a variable name. A value is then copied and the assign helper runs, the same store as opcode 50. **[bin]**

Opcode 121 needs two values. If either tag is string, both values are converted to strings and the right-hand string is appended to the left, the same append as opcode 113. Otherwise both are converted to numbers and the numbers are added, the same add as opcode 60. **[bin]**

## Folds 234–242, in 6.00 only

The pairing, from the 6.00 fold: **[bin]** (`protocol/gs2-client-vm.md#opcodes-added-after-4208`)

| First | Next | Result |
| --- | --- | --- |
| 22 `loadmember` | 35, and none of 33, 34, 36, 47 follow | 234 |
| 22 | 36 | 235 |
| 22 | 35, then 33, 34, 36, or 47 | 236, 237, 238, or 239. 47 is not folded when 45 follows it |
| 20 `loadfloat` | 131 | 240 |
| 22 | 6, or 45, or 47, when the name resolves and that object is flagged | 241, and the resolved object is stored on the instruction |
| 47 | 45 | 242, and the next instruction's number is copied onto this one |

The executor, read case by case: **[bin]**

| Result | Effect |
| --- | --- |
| 234 | the member-access step: a top value with no object has its string cleared, and one with an object has a string copied onto it. The tag becomes a variable name. The next opcode is skipped |
| 235 | a new variable-name is pushed, with a copied string and no object, then converted to an object. The next opcode is skipped |
| 236 | the 234 step, then the number conversion, and the next two opcodes are skipped |
| 237 | the 234 step, then the string conversion, and the next two opcodes are skipped |
| 238 | the 234 step, then the object conversion with creation, and the next two opcodes are skipped |
| 239 | the 234 step, then `makeprop`, and the next two opcodes are skipped |
| 240 | the instruction's number is pushed, then the array-read runs: that number, truncated like the other integer sites, indexes the object underneath. The next opcode is skipped |
| 241 | a resolved value is pushed. Its variable pointer is null and its property pointer is the object the fold stored. This case does not skip a further opcode |
| 242 | the same register store as `setreg`, using the number the fold copied, and the next opcode is skipped. This case does not itself run `makeprop` |

The source of the string copied in 234's object branch was not visible in this read. **[bin]**

## Names with no case

The 4.2.0.8 name table reserves these. The script switch in 4.2.0.8, in 5.0.0.7, and in both 6.00 images has no case for the number. **[bin]**

`break` (161) is a reserved name and has no case. `continue` (162) is a reserved name and has no case. `loadserver` (185) is a reserved name and has no case. `loadserverr` (186) is a reserved name and has no case. `loadclient` (187) is a reserved name and has no case. `loadclientr` (188) is a reserved name and has no case.
