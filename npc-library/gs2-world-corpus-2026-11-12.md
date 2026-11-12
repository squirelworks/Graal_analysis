# GS2 and GS1 in three playerworld script sets (2026-11-12)

A survey of how real playerworld scripts use GS2 and GS1, made by running Seihai's temporary GS2 compiler (`seihai-core`, `scripting::gs2::compile`) over three owner-held exports. It gives aggregate counts only. No script text, world name, file name or path is published, and the evidence is cited by its public ID **GS2-WORLD-CORPUS-20261112** in `docs/evidence-index.tsv`. Short examples below are hand-written to show a shape, not copied. **[lab]**

The sets are:

| Set | Era | Scripts tried | Language |
| --- | --- | --- | --- |
| A | 2008 levels | 2,593 level NPCs | GS2 |
| B | 2007 script export | 1,316 (exports split at `//#CLIENTSIDE`) | almost all GS2 |
| C | 2006 world | 35,739 | GS1 |
| D | a later edit of C | 405 | GS1 |

Exports are key-value headers with the script between a start and an end marker. The harness strips that wrapper and splits server and client parts at a line that is exactly `//#CLIENTSIDE`. **[lab]**

## What GS2 scripts use

Counts are occurrences, with scripts in brackets where they were taken, over sets A and B together. **[lab]**

| Construct | Count |
| --- | --- |
| `@` join | 6,736 (474 scripts) |
| `SPC` join | 2,874 (459) |
| `new Gui…(…)` | 1,282 (101) |
| `.add(` | 1,162 |
| `for (x : list)` | 1,007 (348) |
| `.size()` | 794 |
| `.substring(` | 639 |
| `with (` | 605 |
| `.tokenize(` | 592 |
| `.pos(` | 495 |
| `switch` | 352 |
| `NL` / `TAB` | 148 / 48 |
| `new TStaticVar` | 26 |

- **Code outside functions** appears in 211 scripts. In 124 of them it comes after a function. The first such statement is a `public function` header (87), a GS1-style `if (event)` block (74), a command (15), a call (14) or `enum` (13). **[lab]**
- **Message codes do not appear inside GS2 string literals.** Where GS2-era files use `#v(`, `#t(`, `#c` or `#s(`, it is outside string literals (64, 36, 33 and 27 uses), in GS1-style command arguments. Nothing in this set depends on a GS2 client expanding codes inside strings. **[lab][inf]**
- The first parse errors of the compiler as it was on 2026-11-12 (before the change below) were method calls `obj.f()` (299 scripts), `SPC`/`NL`/`TAB` (155), a member or call after a call (146), `switch` (97), a function body without braces (73), for-each (65), a member after an index (32), `in |a, b|` (28), prefix `++`/`--` (27), `in {…}` (21) and `obj.(expr)` (18). **[lab]**

## What GS1 scripts use that GS2 has no command for

Set C, scripts and occurrences. **[lab]**

| GS1 name | Scripts / uses |
| --- | --- |
| `setstring` | 1,841 / 4,926 |
| `setcharprop` | 449 / 4,508 |
| `seteffectmode` | 396 |
| `strtofloat` | 185 |
| `strcontains` | 158 |
| `tokenize` | 124 |
| `addweapon` | 82 |
| `addstring` | 76 |
| `savelog2` | 57 |
| `hasweapon` | 38 |

- **Statements outside every event test** are in 4,152 scripts. Most are commands that set state: a bare `join` (2,565 statements, 1,134 before the first event test and 1,431 after one), `setshape` (346), `dontblock` (275), `drawunderplayer` (162), `setcoloreffect` (108). GS1 runs them on every event, in source order. **[lab]**
- **Event tests with guards**: 598 scripts. Most are chains of three or more terms with one event, such as `playertouchsme && a && !b` (296) and `action… && x && !y` (86). An event test with an `else` occurs in 48 scripts, and an event flag read as a value (`playerchats` inside an expression) in 56. **[lab]**

## Compiler results

Same harness and sets for each build; no build panicked. Percent is scripts that compiled. **[lab]**

| Set | seihai-core main (d76d2bb) | PR #9 (6c80e51) | PR #10 (c173e82) |
| --- | --- | --- | --- |
| A (GS2) | 93.0% | 93.0% | 95.1% |
| B (GS2) | 15.0% | 15.0% | 61.9% |
| C (GS1 lowered) | 71.6% | 77.7% | 93.1% |
| D (GS1 lowered) | 37.5% | 38.3% | 51.9% |

After PR #10 the largest refusals are: in set C, `seteffectmode` (396), a call or command inside a GS1 `with` body (372), a top-level statement after an event test that is not a command (267), complex event tests (130), `setcharprop` colour codes it does not map (128), an event test with `else` (60), event flags read as values (104), `#I` (47) and `hasweapon` (35); in set B, `;` and name errors from constructs still unparsed (267), `return`/`sleep`/`break` leaving a `with` (69) and `new T(name) { … }` blocks (68).

PR #9 lowers `join` inside event tests and merges repeated event blocks. PR #10 adds the GS2 constructs above, code outside functions in both front ends, guard chains, message codes, and the GS1 string and character-property commands.

## What this does and does not settle

- It settles which constructs a GS2 compiler needs before it can take real 2007–2008 scripts: method calls, the join operators, `switch`, for-each, `new` (including GUI objects), and code outside functions. It ranks the GS1 commands a GS1-to-GS2 port must replace. **[lab]**
- It does not show what an official compiler emits for any of these. Seihai's encodings for six of the eight `gs2-parser` fixtures match that compiler byte for byte; the rest (members and indexes after a call, `new T(name)` with a name, `in {…}`, `@=`, escapes) are Seihai's choice and need a check against official bytecode. The 19 official 6.113 bodies in `protocol/gs2-official-bytecode-6113.md` are the obvious place to look. **[inf]**
- It does not settle whether GS2 runs top-level code before every event. The GS1 lowering relies on the one bounded 4.04r2 result (`client-internals/linux-404r2-events.md`); a script whose GS1 top-level statement comes after an event block, and is not a command, is still refused. **[inf]**
- The GS2 property names that `setcharprop` codes become (`chat`, `nick`, `headimg`, `bodyimg`, `shieldimg`, `swordimg`, `colors[i]`, `attr[i]`) are a reading, not checked against a client. **[inf]**
- The third-party compiler's `control` and `calls` fixtures show two behaviours Seihai does not copy: a `switch` arm that falls off the end runs on into the case tests again, and a call that is the brace-less body of an `if` leaves its value on the stack. Whether the official compiler does either is open. **[src][inf]**

## Still to survey

- [ ] The 2017 and 2019 backups of the GS1-era world (owner-held, Drive only): whether they are GS2, and the same counts.
- [ ] `seteffectmode`, GS1 `with` bodies, `new Gui…(name) { … }` blocks, `enum` and `obj.(expr)`: the largest constructs the compiler still refuses.
- [ ] Compare Seihai's no-fixture encodings with the official 6.113 bodies.
