<!-- manual: kind=reference status=draft -->
# 8.1 GS1 language

This chapter describes GS1, the NPC and weapon script language of the 1.x and 2.x clients, as the 2.05 rev 2 client parses and runs it. The command-by-command reference, the expression tables and the per-build changes are in → §8.2. The later language is in → §8.3.

> Status: draft. The `#` message-code helper/field semantics and object-array writes and fallback details remain open; the bounded `move` consumer is described in §8.2.9, with scheduling and collision residuals (→ App. E#203, App. E#204, App. E#206).

## 8.1.1 Where scripts run

| Item | Rule | Source |
| --- | --- | --- |
| host | Classic NPCs are pure client-side; the archived script corpus shows no separate server VM | [doc] (npc-library/archival-scripting-notes.md#runtime-model-highlights-classic-client) |
| corpus | the archived level scripts sort into genres; baddies (452 scripts) and hazards (192) lead, and most baddy NPCs are event skeletons that react to the player entering or touching them, an item drop, or all baddies dying | [doc] (npc-library/behaviours.md#combat--baddies-452-scripts); [doc] (npc-library/behaviours.md#combat--hazards-192-scripts) |
| kinds of script | a level NPC, a weapon NPC (made by `toweapons -Name`), and a child NPC made by `putnpc` | [doc] (npc-library/archival-scripting-notes.md#runtime-model-highlights-classic-client) |
| delivery to 2.05 | NPC and weapon scripts arrive as source text in the NPC script prop (`NPCPROP_SCRIPT`) | [2.05] (npc-library/gs1-reference-205.md#execution-model-205) |
| weapon delivery | PLO 33 NPCWEAPONADD carries `str name` and an NPC prop stream with image and script; a name the player already has is ignored; 2.05 fires `playerenters` on the new weapon | [srv][2.05] (client-internals/feature-specs/02-weapons-combat.md#weapon-lists-server-to-client-srv205) |
| pre-v4 clients | the server sends the weapon script as plain GS1 text | [srv] (client-internals/feature-specs/02-weapons-combat.md#weapon-lists-server-to-client-srv205) |
| level editor | each level NPC has an image (or none) and a GS1 script; the 2.05 editor's script window has *Test* (a syntax check) and *Style* | [2.05] (client-internals/level-editor-205.md) |
| NPC server present | when the server sends PLO 44 (`PLO_HASNPCSERVER`), several visual commands are allowed online (→ §8.1.9) and the client stops applying NPC props itself | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works); [bin] (protocol/packet-ids.md) |
| 2.3 and later | the classic client-side NPC mode is removed; Classic moves to the NPC server | [doc] (client-internals/feature-timeline.md) |
| 4.04 rev 2 | still runs GS1 weapon scripts, but sends only `client.` string flags to the server; `set`, `setstring gr.*` and `setplayerprop #c` from a weapon send nothing | [live] (client-internals/live-behaviour-404.md) |

## 8.1.2 Compilation

2.05 does not compile GS1 to bytecode. It parses the script text once, on level load, and interprets the result [2.05] (npc-library/gs1-reference-205.md#execution-model-205; npc-library/gs1-command-reference-205.md#how-the-interpreter-works).

| Item | Rule | Source |
| --- | --- | --- |
| compiled form | a flat list of statement nodes | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| statement node | a command number, up to two string arguments, up to eight numeric expression arguments, a jump target and a pre-resolved name index (item, baddy, colour and the like) | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| command number | 600 + the command's index in the command table; `if` is 605 (→ §8.2.4) | [2.05] (npc-library/gs1-reference-205.md#execution-model-205) |
| expressions | resolved through a second table of functions and variables with numeric ids 100–825 (→ §8.2.5) and a small operator table | [2.05] (npc-library/gs1-reference-205.md#execution-model-205) |
| argument parsing | each command has an argument signature (→ §8.2.1); the compiler uses it to parse the arguments and to build the usage text of its error messages | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| compiled-away keywords | `else`, `function` and closing braces never reach the executor; they become four internal node kinds: assignment or expression statement, unconditional jump, function call, and end of function body | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| name matching | command names that end in a space in the table (`say `, `set `, `setlevel `, `setimg `, `move ` and others) require an argument; the others are matched as whole words | [inf] (npc-library/gs1-reference-205.md#execution-model-205) |
| missing files | offline, the compiler rejects a filename argument naming a missing file unless it starts with `http://` | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| OpenGS1 | OpenGS1's stack bytecode is an independent reimplementation; 2.05 does not share its opcode set (→ §8.4.3) | [2.05] (npc-library/gs1-reference-205.md#execution-model-205) |

## 8.1.3 Execution

| Item | Rule | Source |
| --- | --- | --- |
| run | every event runs the whole node list from the top | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| event test | events are flags tested with `if (name)`; the engine sets the flag before it runs the script (→ §8.1.5) | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205) |
| `if` | exact checked 2.05 revision 2 skips its block on zero; ordinary finite nonzero computed results are true. Condition-name parsing is separate from numeric message expansion → App. E#200 | [2.05][bin][lab] (npc-library/gs1-condition-truth-205r2.md#condition-execution-and-parsing) |
| loops | `for` and `while` are the same loop node; the condition is checked on each pass and the loop stops after 10,000 passes, as the 2000 documentation says | [2.05][doc] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| function calls | a call pushes a return point; nesting stops at 10,000 deep | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| `return` | pops the call stack and resumes after the call; with an empty stack (or at the end of a function body) it ends the script | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| string arguments | trimmed, and message codes (`#c`, `#v(...)` and others) are expanded before use, for almost every command | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |

These commands end the current script run after they execute:

| Command | Condition | Source |
| --- | --- | --- |
| `setlevel`, `setlevel2` | always | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| `destroy` | always | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| `sleep` | non-zero argument | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| `toinventory` | offline | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| `hide` | on an NPC that is following the player | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| `break`, `continue` | outside a loop | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |

## 8.1.4 Timeouts and sleep

| Item | Rule | Source |
| --- | --- | --- |
| timer | a script sets `timeout = N` (seconds); when it expires the script runs with the `timeout` flag set | [doc] (npc-library/archival-scripting-notes.md#runtime-model-highlights-classic-client) |
| common rates | 0.05 s for AI and HUDs, 0.1–0.2 s for menus, 0.5–1.0 s for idle NPCs, in the archived corpus | [doc] (npc-library/archival-scripting-notes.md#runtime-model-highlights-classic-client) |
| `sleep n` | sets the NPC's timeout to *n*, remembers the next statement, and ends the run; the next `timeout` event resumes there | [2.05] (npc-library/gs1-command-reference-205.md#control-flow) |
| `sleep 0` | only clears the timer display | [2.05] (npc-library/gs1-command-reference-205.md#control-flow) |
| `timershow` | draws the NPC's timeout counter over it; cleared by `message` and by `sleep 0` | [2.05] (npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) |
| who gets timeouts | only the level leader receives an NPC's timeout events, unless the NPC runs `timereverywhere` | [2.05] (npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) |

## 8.1.5 Events

The engine sets one of these flags and runs the script [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205). The scrape count is the number of the 3,172 scraped level scripts that test the event, where the notes counted it.

| Event | Scrape count | Source |
| --- | ---: | --- |
| `created` | unmeasured | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205) |
| `playerenters` | 2,268 | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205); [file] (npc-library/gs1-commands.md#event-frequency-reminder) |
| `timeout` | 1,456 | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205); [file] (npc-library/gs1-commands.md#event-frequency-reminder) |
| `playertouchsme` | 1,986 | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205); [file] (npc-library/gs1-commands.md#event-frequency-reminder) |
| `playertouchsother` | 1,074 | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205); [file] (npc-library/gs1-commands.md#event-frequency-reminder) |
| `playerendsreading` | 1,123 | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205); [file] (npc-library/gs1-commands.md#event-frequency-reminder) |
| `playerchats` | unmeasured | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205) |
| `playersays(…)`, `playersays2(…)` | unmeasured; these are functions, not flags | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205) |
| `wasshot` | 728 | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205); [file] (npc-library/gs1-commands.md#event-frequency-reminder) |
| `wasshooted`, `washit`, `wasthrown`, `waspelt`, `peltwith…` | unmeasured | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205) |
| `exploded` | unmeasured | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205) |
| `compusdied` | 1,122 | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205); [file] (npc-library/gs1-commands.md#event-frequency-reminder) |
| `compsdead` | unmeasured | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205) |
| `playerdies`, `playerhurt`, `playerhurted` | unmeasured | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205) |
| `playerlaysitem`, `weaponfired` | unmeasured | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205) |
| `action…` | unmeasured; any action name sent by `triggeraction` | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205) |
| `shotbyplayer`, `shotbybaddy` | unmeasured | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205) |
| `main` | unmeasured; sits in the same string cluster, probably a weapon's main event or entry | [inf] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205) |

Events documented for 2.22 but absent in 2.05: `actionleftmouse`, `actionrightmouse`, `actiondoublemouse`, `actionprojectile`, `keypressed`, `mousedown`, `playeronline`, `playerpaused` [2.05][doc] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205).

How an event reaches another script:

| Mechanism | Rule | Source |
| --- | --- | --- |
| `callnpc i, event` | exact 2.05r2 queues the expanded event name with empty parameter text; comma suffixes are not split into `#p` values | [bin][lab] (npc-library/gs1-event-parameters-205r2.md#commands-and-local-delivery) |
| `callweapon i, event` | moves weapon *i* to the player's centre, then queues its event name with empty parameters; static-only in this follow-up | [bin] (npc-library/gs1-event-parameters-205r2.md#commands-and-local-delivery) |
| `triggeraction x, y, action, params` | fires `action` with its parameters at the object on (x, y) locally, and sends it online (→ §8.2.3) | [2.05] (npc-library/gs1-command-reference-205.md#control-flow) |
| `triggeraction 0,0,clientside,…` | from 2.21, reaches a weapon's client-side part | [doc] (client-internals/feature-timeline.md) |

## 8.1.6 State flags

The engine keeps these flags current; a script tests them with `if` [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205).

| Group | Flags | Source |
| --- | --- | --- |
| NPC | `visible`, `isweapon`, `followsplayer`, `isleader`, `isonmap` | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205) |
| carrying | `carrying`, `carries…`, `carriesnpc` | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205) |
| player | `weaponsenabled`, `playeronhorse`, `canspin`, `playerswimming`, `playerismale`, `playerisfemale`, `playerreading`, `playerattached`, `firedonhorse` | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205) |
| level | `issparringzone`, `sparringzone`, `nopkzone`, `lighteffectsenabled` | [2.05] (npc-library/gs1-reference-205.md#built-in-flags-and-events-205) |

## 8.1.7 Flags, variables and persistence

| Item | Rule | Source |
| --- | --- | --- |
| flags | `set name` sets a flag, `unset name` clears it; the documentation says a `server.` prefix makes it server-wide | [2.05][doc] (npc-library/gs1-command-reference-205.md#flags-and-variables) |
| string variables | `setstring name,value` stores the flag `name=value`; an empty value deletes it | [2.05] (npc-library/gs1-command-reference-205.md#flags-and-variables) |
| arrays | `setarray var,n` resizes an array variable to *n* elements; ignored unless the variable is plain or `this.` | [2.05] (npc-library/gs1-command-reference-205.md#flags-and-variables) |
| NPC-local variables | `this.` prefix | [doc] (npc-library/gs1-reference-205.md#operators-and-syntax-doc) |
| NPC save slots | `save[n]`, reached as `this.save[i]` or `npcs[i].save[i]` (→ §8.2.5) | [2.05] (npc-library/gs1-reference-205.md#functions-and-variables-205); [doc] (npc-library/archival-scripting-notes.md#runtime-model-highlights-classic-client) |
| persistence | scripts persist state through `toweapons`, `save[n]` and `client.*` flags | [doc] (npc-library/archival-scripting-notes.md#runtime-model-highlights-classic-client) |
| tokens | `tokenize` splits a string into the global token list on spaces and commas (quotes group); `tokenize2` adds delimiter characters; `tokenscount` gives the count | [2.05] (npc-library/gs1-command-reference-205.md#flags-and-variables; npc-library/gs1-reference-205.md#functions-and-variables-205) |
| 2.19 | `this.` strings on the client; on NPC-server servers the client stops sending strings that are not `client.` | [doc] (client-internals/feature-timeline.md) |
| 4.04 rev 2 | only `client.` string flags are sent to the server | [live] (client-internals/live-behaviour-404.md) |
| image ids | HUD and shop scripts in the archived corpus collide often in the `showimg` index band around 300 and above | [doc] (npc-library/archival-scripting-notes.md#runtime-model-highlights-classic-client) |

## 8.1.8 Syntax and operators

| Item | Forms | Source |
| --- | --- | --- |
| assignment | `=`, `+=`, `-=`, `*=`, `/=`, `++`, `--` | [doc] (npc-library/gs1-reference-205.md#operators-and-syntax-doc) |
| arithmetic | `+ - * / %`, `^` for power | [doc] (npc-library/gs1-reference-205.md#operators-and-syntax-doc) |
| comparison | `== != < > <= >=` | [doc] (npc-library/gs1-reference-205.md#operators-and-syntax-doc) |
| logic | `&&`, `\|\|`, `!` | [doc] (npc-library/gs1-reference-205.md#operators-and-syntax-doc) |
| membership | `in` for ranges and sets: `x in \|0,64\|`, `2 in {1,2,3}` | [doc] (npc-library/gs1-reference-205.md#operators-and-syntax-doc) |
| control flow | `if`/`else`, `for`, `while`, `break`, `continue`, `function name() {}` with `name();`, `return`, `sleep`, `timeout = n` | [doc] (npc-library/gs1-reference-205.md#operators-and-syntax-doc) |
| string codes | exact 2.05r2 outer catalog has 44 selectors / 53 family-expanded spellings; helper/field and display meanings remain partial → App. E#203 | [bin] (npc-library/gs1-message-codes-205r2.md#selector-membership-and-coverage) |
| character props | `setcharprop` and `setplayerprop` take a property code (`#1`, `#2`, `#3`, `#5`, `#8`, `#C0`..`#C5`, `#P1`..`#P5`, `#c`, `#n`) as their first word (→ §8.2.4.5) | [2.05] (npc-library/gs1-command-reference-205.md#character-npcs-showcharacter) |
| not commands | `warp` and `jump` are not GS1 commands in 2.05; warping is `setlevel` / `setlevel2` or an assignment to `playerx` / `playery` | [2.05] (npc-library/gs1-command-reference-205.md#corrections-to-gs1-commandsmd) |

## 8.1.9 Execution contexts

| Context | Rule | Source |
| --- | --- | --- |
| weapon NPCs act as the player | when the running NPC is one of the player's weapons, commands that spawn things (bombs, explosions, horses, projectiles, `showimg` layers, `hitobjects`, `triggeraction`, `reflectarrow`) use the player's level and count the player as the source | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| online gate | `seteffect`, `setcoloreffect`, `setzoomeffect`, `changeimgcolors`, `changeimgzoom`, `addtiledef`, `addtiledef2`, `removetiledefs`, `replaceani` and `attachplayertoobj` run only offline, or online when the server announced an NPC server (PLO 44); online without an NPC server they do nothing | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| editor preview | when the in-game editor builds a preview copy of a `showcharacter` NPC, it runs that NPC's `playerenters` in a restricted mode | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| preview whitelist | only `if`, `else`, `for`, `while`, `setgif`, `setgifpart`, `setimg`, `setimgpart`, `setmap`, `showcharacter`, `setcharprop`, `setcharani`, `setbackpal`, `setbacktile`, `setbacktile2`, `addtiledef`, `addtiledef2`, `setz`, `loadmap`, function calls and `++`/`--` style assignments run; everything else is skipped | [2.05][inf] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| online side effects | some commands also send a TCP or UDP message when connected (→ §8.2.3) | [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects) |

## 8.1.10 The script corpus

The notes hold two collections of real GS1 scripts, the evidence for the frequency counts in this part:

| Collection | Content | Source |
| --- | --- | --- |
| level scrape | 3,172 unique scripts from GR-V1 `.graal` levels; the scrape reported 3,187, and 15 records were lost to truncated source pages | [file] (npc-library/README.md) |
| level scrape by genre | combat 1,400; interaction 602; dialogue 373; spawn 328; misc 257; object 168; transport 59 | [file] (npc-library/README.md#counts) |
| archived catalogue | 1,520 unique script bodies from 6,275 placements, with a body-hash catalogue; held off-repository | [doc] (npc-library/archival-scripting-notes.md#source-archive) |

The archived catalogue classifies about 1,519 documented scripts [doc] (npc-library/archival-scripting-notes.md#classification-summary-from-ash):

| Class | Approx. count | Source |
| --- | ---: | --- |
| quest / dialogue | 516 | [doc] (npc-library/archival-scripting-notes.md#classification-summary-from-ash) |
| level prop / trigger | 390 | [doc] (npc-library/archival-scripting-notes.md#classification-summary-from-ash) |
| farm / planting | 136 | [doc] (npc-library/archival-scripting-notes.md#classification-summary-from-ash) |
| player weapon / projectile | 135 | [doc] (npc-library/archival-scripting-notes.md#classification-summary-from-ash) |
| shop / merchant | 111 | [doc] (npc-library/archival-scripting-notes.md#classification-summary-from-ash) |
| minigame | 59 | [doc] (npc-library/archival-scripting-notes.md#classification-summary-from-ash) |
| enemy / baddy AI | 44 | [doc] (npc-library/archival-scripting-notes.md#classification-summary-from-ash) |
| inventory / equipment UI | 37 | [doc] (npc-library/archival-scripting-notes.md#classification-summary-from-ash) |
| HUD / stats overlay | 20 | [doc] (npc-library/archival-scripting-notes.md#classification-summary-from-ash) |

The commands most used in the level scrape are `hide` and `show` (in most `playertouchsme` scripts), then the level-change commands, `hurt`, `say`, and `set` / `unset` [file] (npc-library/gs1-commands.md#offline-wiring-priority).

## 8.1.10 Exact-build condition truth and comparison folding

In the checked original Windows 2.05 revision 2, computed `(0.5+0)` and `(-0.5)` display their nonzero values and take the true branch; `(0+0)` displays zero and is false. Bare `0.5` displays 0.5 but is false in condition context, while `created` displays zero numerically and is true. Unrecognized bare condition tokens can become named-flag tests; numeric message expansion is a separate parsing context. These observations do not establish a threshold of one or rounding [2.05][bin][lab] (npc-library/gs1-condition-truth-205r2.md#condition-execution-and-parsing).

A separate compiler defect folds comparisons of constant numeric leaves to zero: observed `1==1`, `1!=0`, `1<2`, `2>1`, `1=1` and `(1+0)==1` all display zero and are false. The comparison parent becomes a zero-initialized numeric leaf before evaluation; arithmetic folding evaluates before changing the parent. Dynamic self-equality and ordering controls and `this.a==1` after assigning one work, while dynamic self-inequality is false. This is not absence of comparison support or a complete operator/precedence contract [2.05][bin][lab] (npc-library/gs1-condition-truth-205r2.md#constant-comparison-folding).

The researcher ran sixteen owned cases in two offline Wine/virtual-display fixtures, with unchanged original executable bytes, no server or external network, explicit 2.31 donor assets and completed cleanup. Fifteen labels were fully readable in the second layout; its actor-obscured greater-than control was read from the identical script in the first. No absent label counted as false. Ten fresh selected instruction reads corroborate the mechanism, without live expression-node inspection. Evidence and target identity are researcher supplied. Other builds, nonfinite/malformed values, full aliases/precedence and flag-name collisions remain open [lab] (npc-library/gs1-condition-truth-205r2.md#verification-and-limits).

## 8.1.11 Exact 2.05r2 message expansion

The checked outer dispatch recognizes 44 selector bytes, or 53 spellings after replacing C/P family prefixes with C0–C5/P1–P5. This includes preserved display codes and empty-output `#7`; it is not a count of implemented operations. Case matters. The byte selector inventory is `# . 1 2 3 4 5 6 7 8 A B C E K L P T W X Y a b c d e f g h i k l m n p r s t u v w x y z` [bin] (npc-library/gs1-message-codes-205r2.md#selector-membership-and-coverage).

Message trims end bytes below 33, expands in mode zero with the caller, stores its text and clears timer-display state. Expansion joins prefix, replacement and recursively expanded suffix without automatically rescanning inserted text. A trailing hash survives; unknown codes drop only their hash. Recognized codes consume their prefix even without valid arguments; a balanced argument extends consumption through its close. Parenthesis nesting is traced but quote/escape scanning remains partial. Strings and slicing use bytes [bin] (npc-library/gs1-message-codes-205r2.md#processing-contract).

`##` yields a hash. `#.` `#4` `#A` `#B` `#X` `#Y` `#d` `#h` `#i` `#l` `#r` `#u` `#x` `#y` `#z` preserve their two-byte display spellings. `#b` adds LF only in nonzero expansion mode; ordinary message mode zero removes it. `#E` inserts a runtime-state byte of unresolved meaning [bin] (npc-library/gs1-message-codes-205r2.md#literal-and-display-codes).

Character-family codes accept an optional numeric selector: omitted/zero selects the local player, minus one selects the caller only if a character, positive indices enumerate remote players then other character NPCs excluding the caller; unresolved selectors yield empty. Conversion uses the biased-floor helper. `#1/#2/#3/#5/#8` return sword/shield/head/horse/body images, stripping directories and lowercasing ASCII, retaining extensions; absent objects yield empty. `#6` is another unproved image association. `#7` selects but outputs empty. `#C0`–`#C5` index color names through six actor storage slots; the sixth slot has unproved meaning and does not extend the five-byte wire color property. Invalid C/P digits consume the extra byte and yield empty; C storage values lack a local table-size check. `#P1`–`#P5` return stored image-parameter text or a nonnegative integer fallback. `#c` returns unexpanded character text; `#n` returns the name and `#g` extracts its parenthesized tag without proving membership. `#a` is an unresolved direct string field; `#m` shares the animation object with setani/setcharani [bin] (npc-library/gs1-message-codes-205r2.md#character-selectors).

`#v(expr)` recursively expands its argument in mode zero, numerically evaluates and formats a double; exact formatting remains open. `#s(name)` trims/expands the name and returns its stored string, with store normalization/case still partial. `#T(text)` trims, expands and trims again. `#e(start,length,text)` numerically evaluates the first two top-level comma parts, biased-floor converts them, expands text and slices bytes: zero-based start clamps to string bounds, negative length means remainder, overruns clip. Missing separators yield empty after consuming balanced arguments; quoted separators remain unqualified [bin] (npc-library/gs1-message-codes-205r2.md#expression-and-string-operations).

`#K(number)` returns the low byte for converted integers zero through 65535, otherwise empty; this is not Unicode. Embedded zero and display behavior are distinct. `#k(number)` asks for configured binding variant zero at indices zero through ten; layout/localization remain open. `#w/#W` return selected weapon name/image or an explicitly indexed zero-based entry after argument expansion/evaluation. Explicit out-of-range indices yield empty; omitted index checks nonnegative before list access. Weapon image names are not normalized like character equipment. `#f` normalizes the caller image; `#L` normalizes a local-player string of unresolved identity. `#p/#t` expand/evaluate/convert indices and bounds-check distinct string lists; tokenize/tokenize2 produce the #t list; the separate dispatch producer for #p is established in §8.1.12 [bin] (npc-library/gs1-message-codes-205r2.md#keys-weapons-and-indexed-lists).

Thirty qualified outputs in three usable scenes corroborate hash escaping/fallback, trailing hashes, recognized missing arguments, case sensitivity, non-rescanning of inserted text and explicit nested argument expansion. Substring bounds, numeric examples, `#K(65)`/negative input, mode-zero `#b`, name/tag extraction, empty `#7` and token indices were observed. `#K(0)` is only a box-glyph observation; empty `#p(0)` does not identify event parameters. Four original-client Wine/private-display runs used unchanged executable bytes, isolated namespaces, no server, explicit 2.31 donor assets and owned fixtures; all exited zero and cleaned up. One overlapping layout is diagnostic only and replaced, not counted among controls. Identity, static and visual evidence are researcher supplied; complete selector decoding does not fully revalidate every helper. Other builds, live remote-player ordering, malformed input, quoted scanners, exact formatting, #6/#a/#E/#L meanings and downstream rendering remain open [bin][lab] (npc-library/gs1-message-codes-205r2.md#new-original-client-controls).

## 8.1.12 Exact 2.05r2 event parameters

Event dispatch clears and fills the shared list read by `#p(index)`/`paramscount` from an actor's pending parameter text, using a literal comma separator. Numeric indices are expanded/evaluated/converted and bounds-checked; negative/out-of-range yields empty. This list is separate from the tokenize/tokenize2 list used by `#t`/`tokenscount` [bin] (npc-library/gs1-event-parameters-205r2.md#producer-and-consumer-linkage).

An actor has multiple pending event names but one parameter-text field. Each accepted distinct event adds its name and replaces that field; duplicate pending names are rejected without changing it. Any pending action-prefixed name rejects another action-prefixed request. Newly accepted actions also record source context; exact name-case rules remain untraced. Thus later accepted calls can overwrite earlier pending parameters, depending on batching; rejected requests preserve them [bin] (npc-library/gs1-event-parameters-205r2.md#queue-ownership-and-overwrite-rules).

`callnpc` resolves its caller-relative selector; `callweapon` resolves a zero-based weapon index and centers its actor on the player. Both queue expanded event names through an empty-parameter wrapper, rather than executing receivers synchronously or splitting comma suffixes into #p. Local `triggeraction` supplies separate parameter text, prefixes the action name and checks eligible receiver bodies; weapon delivery has an additional local-player proximity/source gate. Connected sending is separate from this offline chain [bin] (npc-library/gs1-event-parameters-205r2.md#commands-and-local-delivery).

The byte splitter ends unquoted tokens at the first comma. A quote at the start removes that quote and takes text through the next quote, retaining internal commas. Tokens and remainders trim end bytes below33. Unquoted empty fields and trailing commas are skipped; quoted empty remains. Missing closing quote consumes the rest; there is no escape/backslash-aware quote search. Text after a closing quote need not start with comma. These mechanics are separate from script-level construction/quoting [bin] (npc-library/gs1-event-parameters-205r2.md#splitting-grammar).

A nonnull player context rebuilds the shared list at dispatch entry; null-player early exit does not. Conditional normal cleanup clears pending actor fields but not the shared list, which may retain the current/last context until another dispatch. The nested wrapper saves/restores actor fields without a visible corresponding shared-list snapshot; this does not establish complete reentrant semantics or immutable per-event payloads. The cleanup condition's global meaning remains open [bin] (npc-library/gs1-event-parameters-205r2.md#lifetime-and-nested-context).

Four original-client offline runs provide ten qualified result groups. Local alpha,beta delivery gives count2; unquoted empties/trailing comma are skipped, quoted empty retained, quoted beta,gamma stays one entry, and a mid-token quote does not protect its comma. A queued action followed by a distinct callnpc probe produces both handler markers with count0; two rejected-action controls retain the first value. A saved pre-sleep count2/alpha/beta resumes as count0/empty after requested sleep0.2, without isolating cleanup versus later overwrite or measuring elapsed timing. Long labels use a readable repeat; ordinary-empty uses the earlier clear scene, with no obscured label counted empty [lab] (npc-library/gs1-event-parameters-205r2.md#new-end-to-end-original-client-controls).

Runs used unchanged original Windows2.05r2 under Wine/private displays and isolated namespaces, no server, owned levels and explicit 2.31 donor assets; all supervisors exited zero and cleanup completed. Evidence is researcher supplied, using selected fresh instructions and recovered matching bodies; no live AST/pending-field snapshots. Callweapon remains static-only. Network acceptance, every event/source category, full nested-context restoration, case/escaping, precise scheduling and other profiles remain open. Only the #p producer gap is closed; broader E#203 field/scanner/formatter/renderer questions remain [bin][lab] (npc-library/gs1-event-parameters-205r2.md#new-end-to-end-original-client-controls).

## 8.1.13 Bound Linux 3.04 GS1 source-weapon events and predicates

[lab][cap] An independently authored source weapon on original Linux3.04 produces created/playerenters flag messages and fresh-account persistence. Numeric readbacks and explicit positive comparisons work while tested bare predicates do not activate. This is a separate build scope from the Windows2.05r2 resolution; no universal numeric threshold or complete predicate/name-lookup rule is established. [lab][cap] (npc-library/linux-304-gs1-runtime.md).
