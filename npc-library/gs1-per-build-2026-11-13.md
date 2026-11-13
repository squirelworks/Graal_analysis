# GS1 per client build: command tables, statements, conditions and message codes

Date: 2026-11-13. Extends [gs1-commands-by-version.md](gs1-commands-by-version.md) (the 208 × 61 command
matrix), [gs1-condition-truth-205r2.md](gs1-condition-truth-205r2.md) and
[gs1-message-codes-205r2.md](gs1-message-codes-205r2.md) from 2.05r2 to the other builds.
Sources: the command matrix **[bin]**; real 1.41r1, 2.05r2, 2.17.1, 2.22 and 2.31 clients run
offline with authored test scenes **[lab]**; the result as implemented in squirelworks/seihai-core
PR #35 (release 0.0.21) **[doc]**. No addresses or decompiled code.

## Distinct command tables

The 61 builds in the matrix fall into 25 distinct command tables from 1.21 to 5.00r7. A
reimplementation that scripts "as build X" needs X's table, not the newest one: a build
rejects a command it does not have **[bin]**.

| Build | Commands | Change from the row before | Tag |
| --- | ---: | --- | --- |
| 1.21 | 71 | first gen-2 table; `unseteffect` exists only in 1.21 to 1.33 | [bin] |
| 1.28 beta 2 | 84 | `while`, `sleep`, `setcharprop`, `setplayerprop`, `setstring`, `showcharacter`, `showfile`, `hideplayer`, `setbackpal`, `setletters`, `setmap`, `setminimap`, `timereverywhere` | [bin] |
| 1.3 test to 1.32 | 85 | `setgifpart` | [bin] |
| 1.33 to NewWorld beta 2 | 88 to 165 | as App. C.5 | [bin] |
| 2.1 (no binary) | 166 (inferred) | NewWorld beta 2's table plus `play2`, from the release notes | [doc][inf] |
| 2.17.1, 2.22, 2.31 | 198 | 33 commands (below); the Windows 2.x table did not change from December 2002 to January 2005 | [bin] |
| 3.04 Linux | 191 | the C++ engine drops `drawovertrees`, `putobject`, `savelog`, `setbackpal`, `setbacktile`, `setbacktile2`, `setbody` | [bin] |
| 3.153 Mac to 4.20r8 | 191 | `savelog` back, `with` gone | [bin] |
| 5.00r7 | 193 | `setspritesimage`, `setstatusimage` | [bin] |

The 2.12 to 2.16 builds have no binary; `wraptext`/`wraptext2` (2.12) and `showimg2` (2.15) are
dated by the release notes only **[doc]**.

### Argument letters of the 2.17.1 additions

2.17.1, 2.22 and 2.31 register these with the same letters as 3.04 (`R` number, `S` string,
`F` file name) **[bin]**.

| Command | Letters | Command | Letters |
| --- | --- | --- | --- |
| `putnpc2` | RRS | `showtext` | RRRSSS |
| `showtext2` | RRRRSSS | `showani` | RRRRS |
| `showani2` | RRRRRS | `showpoly`, `showpoly2` | RR |
| `changeimgmode` | RR | `shoot` | RRRRRRSS |
| `setshootparams` | S | `serverwarp` | S |
| `sendpm`, `setpm` | S | `sendtonc`, `sendtorc` | S |
| `savelog` | S | `savelog2` | SS |
| `setcursor` | R | `setcursor2` | F |
| `wraptext` | RSS | `wraptext2` | RRSS |
| `showimg2` | RFRRR | `enablemap`, `disablemap`, `enablepause`, `disablepause` | none |
| `setspritesimage`, `setstatusimage` (5.00r7) | F | | |

`putnpc2`, `savelog2`, `sendpm`, `sendtonc`, `sendtorc` and `setpm` have no client-side executor
in 2.17.1 to 3.04: they act on a server **[bin]**.

### Corrected first builds

Read from the tables, against dates that had come from release notes **[bin]**: `showtext` and
`hideimgs` first in 2.17.1; `openurl2` in 2.01; `move` in 2.03; `setz` in 2.05; `addstring` in
NewWorld beta 2 (before 2.1 it is not a command, so an "appends text" rule for older builds has
no source). `seteffect` is absent from 1.34 to 1.41r1 and returns in NewMain 1.42.

## Statement words by build

| Word | Builds | Tag |
| --- | --- | --- |
| `while` | from 1.28 beta 2 | [bin] |
| `function`, `return`, `break`, `continue` | from 1.41r1 | [bin] |
| `with` | 2.17.1 to 3.04 only | [bin] |

A build without the word does not run the statement.

## Conditions: bare numbers are flag names

`if (1)` and `if (0.5)` are false in every build tested: 1.41r1, 2.05r2, 2.17.1, 2.22 and 2.31
**[lab]**. A bare number in a condition is read as a flag name, so it is true only if a flag of
that name is set. This extends the 2.05r2 reading in
[gs1-condition-truth-205r2.md](gs1-condition-truth-205r2.md) to the other builds.

## Constant comparisons before 2.17

Before 2.17, a comparison of two constants is 0: `1==1` and `(1+0)==1` are false in 1.41r1 and
2.05r2, the folding defect described for 2.05r2 **[lab]**. 2.17.1, 2.22 and 2.31 compare
normally **[lab]**.

## Message codes before and after 2.17

| Rule | Before 2.17 (1.41r1, 2.05r2) | 2.17.1 on | Tag |
| --- | --- | --- | --- |
| `##` | becomes `#` | not checked in the 2.17 engine | [lab] |
| `#b` | empty | — | [lab] |
| `#v`, `#s` with no argument | empty | — | [lab] |
| an unknown code | its `#` is dropped: `A#?B` is `A?B`; 1.41's `#e(1,2,x)` is `e(1,2,x)` | stays as written | [lab] |
| `#K(n)` | from 2.00 | yes | [bin] |
| `#F` | — | from 2.17 | [bin] |

## Events, flags, variables and functions

These are not yet tabled per 1.x build; only the 2.00-on string tables have been diffed
([../client-internals/decomp-findings-2026-10-24-c/script_vocab_deltas.tsv](../client-internals/decomp-findings-2026-10-24-c/script_vocab_deltas.tsv)).
Two fixes from those tables: `onmapx`/`onmapy` from 2.03, `getnpc`/`getplayer` from 2.17 **[bin]**.

## Not measured

- `while (1)` on a real client.
- `##` in the 2.17 engine.
- What `#F`, `#S`, `#D`, `#I`, `#R`, `#P6`–`#P9`, `#C6` and `#C7` return in a populated context.
- A static trace of the 2.17 engine's condition and flag path.
- 1.33 cannot load `.nw` levels, so its scenes need a `.graal` level.
- Events, flags, variables and functions per 1.x build.
