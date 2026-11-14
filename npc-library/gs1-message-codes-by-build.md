# GS1 message codes and one loop reading, by build

Date: 2026-11-13. The per-build summary in
[gs1-per-build-2026-11-13.md](gs1-per-build-2026-11-13.md) names when codes arrive.
This note is the registration list and the offline scenes that summary left out,
plus two argument letters it had wrong. No addresses.

Sources: the command and message-code registries of the original 1.41r1, 2.05r2,
2.17.1, 2.22, 2.31 and Linux 3.04 clients **[bin]**; offline scenes on the real
1.41r1, 2.05r2, 2.17.1, 2.22 and 2.31 Windows clients under Wine, with no network
**[lab]**. 3.04 was not run. Screenshots stay owner-held.

The populated `#F` `#S` `#D` `#I` `#R` `#P6`–`#P9` `#C6` `#C7` readings, and `##`
as a one-pass escape, are the later run in
[the 2026-11-14 lab](../live-runs/open-issues-2026-11-14/README.md#1-442-gs1-per-version).
They are not repeated here.

## Two engines

1.41r1 and 2.05r2 keep commands in a static table and expand `#` codes through one
dispatch **[bin]**. 2.17.1, 2.22, 2.31 and Linux 3.04 register each code by name at
start-up, and each code brings its own argument letters **[bin]**. 2.05r2 used one
shared rule for every code.

An unknown code loses only its `#` on the old engine (`A#?B` shows `A?B`) and stays
as written on the new one (`A#?B` shows `A#?B`) **[lab]**.

## Registered names

Letters below are the ones the registry stores: `R`, `S`, `F` and `M` **[bin]**.
What `M` means at run time is not read here. A code written `bare or (R)` accepts the
name alone or with one number.

| Build | Codes the registry names | Tag |
| --- | --- | --- |
| 2.17.1 | 46 names: `v(R)`, `s(S)`, `I(S,R)`, `e(R,R,S)`, `t(R)`, `p(R)`, `T(S)`, `L`, `F`, `S`, `D`, `E`, `k(R)`, `K(R)`, `f` bare or `(R)`, `w` bare or `(R)`, `W` bare or `(R)`, `P1`–`P9` each bare or `(R)`, `P(R)` or `P(R,R)`, `a` `n` `g` `c` `m` each bare or `(R)`, `1` `2` `3` `5` `6` `8` each bare or `(R)`, `C0`–`C7` each bare or `(R)` | [bin] |
| 2.22, 2.31 | the 2.17.1 set plus `R(S)` | [bin] |
| 3.04 Linux | the 2.22 set without `C5`, `C6` and `C7` (`C0`–`C4` only) | [bin] |

Against the 2.05r2 set, the new registry adds `I(S,R)`, `F`, `S`, `D`, `P6`–`P9`,
a bare `P` with one or two numbers, and `C6` and `C7` **[bin]**. `R(S)` is 2.22
and 2.31 only **[bin]**. It does not register `##`, `#b`, `#7`, or the display
codes `#.` `#4` `#A` `#B` `#X` `#Y` `#d` `#h` `#i` `#l` `#r` `#u` `#x` `#y` `#z`
**[bin]**. `##` still becomes `#` in the scenes, so that escape is outside this
registry **[lab]**.

`#K`, `#L` and `#E` stay registered **[bin]**. `#b` is not, and `A#bB` stays
`A#bB` from 2.17.1 **[lab]**. On 2.05r2 the same text shows `AB` **[lab]**.

### Letters the summary had wrong

The registration read and the summary disagree on two commands. This note keeps
the registration read. Both are the same letters on 2.17.1, 2.22, 2.31 and 3.04
**[bin]**.

| Command | Registration | What the summary said |
| --- | --- | --- |
| `showimg2` | `RMRRR` | `RFRRR` |
| `savelog2` | `MS` | `SS` |

`setspritesimage` and `setstatusimage` are not registered through 3.04. 5.00r7
registers both with `F` **[bin]**.

## What the empty scenes showed

Each NPC ran `message` with one code and no sword, horse or carried object.
Offline, so there is no account. Equipment codes show the default image **[lab]**.

| Code | 1.41r1 | 2.05r2 | 2.17.1, 2.22, 2.31 | Tag |
| --- | --- | --- | --- | --- |
| `##` | `#` | `#` | `#` | [lab] |
| `A#?B` | `A?B` | `A?B` | `A#?B` | [lab] |
| `#e(1,2,ABCD)` | `e(1,2,ABCD)` (no `#e`) | `BC` | `BC` | [lab] |
| `#K(65)` | `K(65)` (no `#K`) | `A` | `A` | [lab] |
| `A#bB` | `AB` | `AB` | `A#bB` | [lab] |
| `#v(0.5)`, `#v(2+3)` | `0.5`, `5` | `0.5`, `5` | `0.5`, `5` | [lab] |
| `#F` | not a code (`F`) | not a code | the level file name | [lab] |
| `#S`, `#D` | not codes | not codes | empty in this scene | [lab] |
| `#a` | `guest` | empty | empty | [lab] |
| `#1`, `#2`, `#8` | `sword1.gif`, `shield1.gif`, `body.png` | the same gif names, and `body.png` | the same names with `.png` | [lab] |

1.41r1's recognised set, read from one scene that tried every letter and digit, is
`#`, `1`, `2`, `3`, `5`, `6`, `7`, `8`, `C`, `L`, `a`, `b`, `c`, `f`, `g`, `m`,
`n`, `s`, `v` and `w` **[lab]**. It has no `#e`, `#K`, `#t`, `#T`, `#p`, `#k`,
`#W`, `#P`, `#E` and no display codes. An unknown code still drops only the `#`.

`#7` shows empty on 2.05r2 and 1.41r1 and is not registered from 2.17.1, so
`A#7B` stays `A#7B` there **[lab]**.

### Bare `#5` and `#6`

On 2.17.1, 2.22 and 2.31, bare `#5` and `#6` did not come out empty. Each was
replaced by the label text that stood in front of it in the same message, so a
label `07:[A` followed by `#5` showed `07:[A07:[AB]` **[lab]**. The cause was
not traced. This is not the 2.05r2 reading, where argument-less `#5` and `#6`
are empty **[lab]**.

## v of a doubled hash

On 1.41r1, 2.05r2, 2.17.1, 2.22 and 2.31, `message` of `##` shows `#`,
`setstring` of `##` then `#s` shows `#`, and `#v(##)` shows `0` **[lab]**.
Inside `#v` the escaped hash is not a number. 1.33 is different: `##` gives an
empty string there, already recorded in the 2026-11-14 run.

## A flag named `1`

A bare number in `while` or `for` is false on these five builds, the same
flag-name path as `if` **[lab]**. After `set 1;`, `while(1)` runs **[lab]**.
`while(0.5)` was not retried with a flag of that name.

| Head | 1.41r1, 2.05r2, 2.17.1, 2.22, 2.31 |
| --- | --- |
| `while(1)`, `while(0.5)`, `for` with a bare `1` | body never runs |
| `while((0+1))`, `while(this.i<5)` | body runs (counted to 5) |
| `set 1;` then `while(1)` | body runs (counted to 5) |

1.33 was not readable in this pass: `#v` cannot see a `this.` counter there.
The later `.graal` run found a bare number false on 1.33 as well, and did not
repeat `set 1`.

## Not in this note

- What bare `#5` and `#6` echo, beyond the label text they showed.
- A static trace of the 2.17 condition and flag path. The outcomes above are
  the scenes.
- Events, flags, variables and functions per 1.x build.
- GANI frame timing with `WAIT` on 2.17.1 and 2.31. That session is not this note.
