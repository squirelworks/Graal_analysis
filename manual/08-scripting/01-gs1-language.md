<!-- manual: kind=reference status=draft -->
# 8.1 GS1 language

This chapter describes GS1, the NPC and weapon script language of the 1.x and 2.x clients, as the 2.05 rev 2 client parses and runs it. The command-by-command reference, the expression tables and the per-build changes are in → §8.2. The later language is in → §8.3.

> Status: draft. The full `#` message-code set, object-array writes and fallback details and the `move` option bits are still open (→ App. E#203, App. E#204, App. E#206).

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
| `if` | evaluates its condition and jumps past its block when the condition is false; the threshold for "true" is disputed → App. E#200 | [2.05] (npc-library/gs1-reference-205.md#execution-model-205; npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
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
| `callnpc i, event` | runs NPC *i*'s script with the given event flag set; the documentation says parameters after the event arrive as `#p(n)` | [2.05][doc] (npc-library/gs1-command-reference-205.md#control-flow) |
| `callweapon i, event` | moves weapon *i* to the player's centre, then runs its script with the event flag set | [2.05] (npc-library/gs1-command-reference-205.md#control-flow) |
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
| string codes | `#` codes such as `#s(var)` and `#v(expr)`; the full 2.05 set is open → App. E#203 | [doc] (npc-library/gs1-reference-205.md#operators-and-syntax-doc) |
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
