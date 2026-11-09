<!-- manual: kind=reference status=draft -->
# 8.2 GS1 reference by version

This chapter is the GS1 reference: argument types, name tables, every command of the 2.05 rev 2 table with what 2.05 does, the expression tables, constants, and how the command table grew from 1.33 to the NewWorld betas. How scripts are compiled and run is in → §8.1.

> Status: draft. Command behaviour was read from 2.05 rev 2 only; other builds are covered by table membership, not by executor reads (→ §8.2.7). Four stored signatures have an exact-input static correction; argument conversion and semantic equivalence remain open (→ App. E#201).

## 8.2.1 Argument signature letters

Each command in the table carries one letter per argument. The compiler uses the letters to parse and to label its usage messages [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works).

| Letter | Compiler's label | Accepts | Source |
| --- | --- | --- | --- |
| `R` | number | any numeric expression | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works; npc-library/gs1-reference-205.md#argument-signature-letters) |
| `S` | string | a string expression: `#s` codes, quoted text, string variables; message codes are expanded at run time | [2.05][inf] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works; npc-library/gs1-reference-205.md#argument-signature-letters) |
| `M` | string | raw text up to `;`, such as flag and level names; message codes are expanded at run time | [2.05][inf] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works; npc-library/gs1-reference-205.md#argument-signature-letters) |
| `F` | filename | a file name | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| `Q` | filename | a file name that names a script file | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works) |
| `I` | itemname | one of the 25 item names (→ §8.2.2) | [2.05][doc] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works; npc-library/gs1-reference-205.md#argument-signature-letters) |
| `B` | baddyname | one of the 10 baddy names | [2.05][doc] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works; npc-library/gs1-reference-205.md#argument-signature-letters) |
| `C` | colorname | one of the 20 colour names, or a number | [2.05][doc] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works; npc-library/gs1-reference-205.md#argument-signature-letters) |
| `D` | direction | `up` `left` `down` `right` (0..3), or a numeric expression | [2.05][doc] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works; npc-library/gs1-reference-205.md#argument-signature-letters) |
| `L` | carry objectname | one of the 11 carry objects | [2.05][doc] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works; npc-library/gs1-reference-205.md#argument-signature-letters) |
| `O` | objectname | an entry from the editor's predefined tile-objects list (`tileobjects/`) | [2.05][inf] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works; npc-library/gs1-reference-205.md#argument-signature-letters) |

The four corrected entries give stored letters only; argument conversion and equivalence of the older descriptions remain unmeasured → App. E#201 [bin] (npc-library/gs1-signatures-205-followup.md#checks-and-limits).

## 8.2.2 Name tables

| Table | Index: name | Source |
| --- | --- | --- |
| items (`I`) | 0 greenrupee, 1 bluerupee, 2 redrupee, 3 bombs, 4 darts, 5 heart, 6 glove1, 7 bow, 8 bomb, 9 shield, 10 sword, 11 fullheart, 12 superbomb, 13 battleaxe, 14 goldensword, 15 mirrorshield, 16 glove2, 17 lizardshield, 18 lizardsword, 19 goldrupee, 20 fireball, 21 fireblast, 22 nukeshot, 23 joltbomb, 24 spinattack | [2.05][doc][srv] (npc-library/gs1-command-reference-205.md#name-tables; npc-library/gs1-reference-205.md#constants-doc) |
| baddies (`B`) | 0 graysoldier, 1 bluesoldier, 2 redsoldier, 3 shootingsoldier, 4 swampsoldier, 5 frog, 6 octopus, 7 goldenwarrior, 8 lizardon, 9 dragon | [2.05][doc] (npc-library/gs1-command-reference-205.md#name-tables; npc-library/gs1-reference-205.md#constants-doc) |
| hare baddy | 2.05 ships `baddyhare.gif`; it is type 5, `frog`, which 2.22 draws with the hare image (→ App. E#205) | [file] (npc-library/gs1-reference-205.md#constants-doc); [2.22] (client-internals/baddies-222.md#types-222) |
| colours (`C`) | 0 white, 1 yellow, 2 orange, 3 pink, 4 red, 5 darkred, 6 lightgreen, 7 green, 8 darkgreen, 9 lightblue, 10 blue, 11 darkblue, 12 brown, 13 cynober, 14 purple, 15 darkpurple, 16 lightgray, 17 gray, 18 black, 19 transparent; the same list indexes `PLPROP_COLORS` | [2.05][srv] (npc-library/gs1-command-reference-205.md#name-tables; npc-library/gs1-reference-205.md#constants-doc) |
| carry objects (`L`) | 0 bush, 1 sign, 2 vase, 3 stone, 4 blackstone, 5 bomb, 6 hotbomb, 7 superbomb, 8 joltbomb, 9 hotjoltbomb, 10 none | [2.05] (npc-library/gs1-command-reference-205.md#name-tables) |
| directions (`D`) | 0 up, 1 left, 2 down, 3 right; numeric values are reduced mod 4, negative values too | [2.05] (npc-library/gs1-command-reference-205.md#name-tables) |
| direction table | the four names follow the command table directly; a dump that reads two records past `hide` finds `up` and `right` and wrongly counts 163 commands | [2.05] (npc-library/gs1-command-reference-205.md#how-the-interpreter-works; client-internals/newworld-betas.md#corrections-to-other-notes) |

## 8.2.3 Online side effects

When the client is connected, some commands also tell the server (TCP, PLI ids → App. A) or nearby peers (UDP ids → §2.9) [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects). A level-local action goes over UDP only when every other player in the level has a UDP port, otherwise over both [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects).

| Command | TCP (PLI) | UDP | Source |
| --- | --- | --- | --- |
| `take`, `take2`, `removeitem` | 13 ITEMDEL | 20 item del | [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects) |
| `putcomp`, `putnewcomp` | 17 BADDYADD, instead of spawning locally | n/a | [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects) |
| `putnpc` | 21 PUTNPC, instead of creating locally | n/a | [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects) |
| `destroy` | 29 NPCWEAPONDEL if the NPC is also a weapon, then 22 NPCDEL | n/a | [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects) |
| `toweapons` | 33 WEAPONADD | n/a | [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects) |
| `hitcompu` | 16 BADDYHURT | n/a | [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects) |
| `hitplayer` on a remote player | n/a | 21 remote hit, to the victim only | [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects) |
| `putexplosion`, `putexplosion2` | 27 EXPLOSION | 14 explosion | [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects) |
| `spyfire` | 10 FIRESPY | 13 fire spy | [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects) |
| `hitobjects` | 36 HITOBJECTS | 25 hit objects | [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects) |
| `triggeraction` | 38 TRIGGERACTION | 26 trigger action | [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects) |
| `removebomb` | n/a | 11 bomb del | [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects) |
| `removehorse`, `takehorse` | n/a | 17 horse del | [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects) |
| `reflectarrow` | n/a | 12 arrow, re-sent with the new direction | [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects) |
| `setplayerprop #c,...` | chat prop | 22 chat | [2.05] (npc-library/gs1-command-reference-205.md#online-side-effects) |

## 8.2.4 Commands of 2.05 rev 2

The 2.05 table holds 161 commands, ops 600 to 760 (op = 600 + table index); `show` (759) and `hide` (760), the two most common commands in the scraped library, are its last two entries [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-commands.md#update-2026-10-21). The table is the same in 2.05 rev 1 and rev 2 [bin] (client-internals/build-diff-204-205.md#205-rev1--rev2).

How to read the tables below:

- *Op* is the 2.05 command number. Commands are inserted in the middle of the table in later builds, so the index of a command changes between builds and an op is valid only for 2.05 [bin] (client-internals/cross-version-timeline.md#gs1-commands).
- *In the table from* is the first build whose table has the command; 1.33 is the earliest build read, so "1.33" means "1.33 or earlier" [bin] (client-internals/cross-version-timeline.md#gs1-commands).
- A † marks a command that is not in the 2.22 `commands.rtf`: removed, renamed (`setgif` → `setimg`, `setgifpart` → `setimgpart`) or undocumented [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205).
- Positions are in tiles unless the row says otherwise; "doc" means the 2000 `npcprogramming.doc` or the `newfeatures` logs, and where the client and the documentation disagree the row gives the client's behaviour [2.05][doc] (npc-library/gs1-command-reference-205.md#commands).

### 8.2.4.1 Messages, signs, sound, files

| Op | Command | Args | In the table from | What 2.05 does | Source |
| ---: | --- | --- | --- | --- | --- |
| 600 | `say` | `R` | 1.33 | Shows sign *n* of the current level (index into the level's sign list). Skipped if the index is out of range or the player is already in the sign-reading state. Puts the player into the reading state. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#messages-signs-sound-files) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 606 | `play` | `F` | 1.33 | Plays a sound positioned at the NPC's centre. Online, a file that is not found locally is requested by its raw name. Doc: midis loop. | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#messages-signs-sound-files) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 635 | `openurl` | `M` | 1.33; takes arguments from 2.01 | Opens the URL in the system browser (doc: with a confirm dialog, no `http://` needed). | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#messages-signs-sound-files) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 637 | `stopmidi` | — | 1.33 | Stops the current midi. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#messages-signs-sound-files) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 648 | `message` | `S` | 1.33 | Sets the text drawn above the NPC. An empty string clears it. Also turns off `timershow`. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#messages-signs-sound-files) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 676 | `showfile` | `F` | 1.33 | Opens the file with its associated program, like a double-click. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#messages-signs-sound-files) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 678 | `setbackpal` | `F` | 1.33 | Copies the 256-colour palette of the given image into the tileset and into every loaded level's tile image, then repaints. Remembers the file so the same palette is not reloaded. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#messages-signs-sound-files) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 679 | `setletters` | `F` | 1.33 | Replaces the sign font image (default `letters.png`) if the file exists. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#messages-signs-sound-files) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 702 | `playlooped` | `F` | 1.37 | Same, but the file is queued as a looped sound (internally the name gets a `+` prefix). Stops on level exit or `stopsound`. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#messages-signs-sound-files) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 703 | `stopsound` | `F` | 1.37 | Stops that (looped) sound. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#messages-signs-sound-files) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 711 | `say2` | `S` | 1.41 rev1 | Same as `say`, but shows the given text directly instead of a level sign. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#messages-signs-sound-files) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 739 | `setmusicvolume` | `RR` | 2.0 | Sets music volume, left and right (doc: 0..1). | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#messages-signs-sound-files) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 740 | `openurl2` | `MRR` | 2.01 | Opens the URL in the client's own HTML window of the given width and height. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#messages-signs-sound-files) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |

### 8.2.4.2 Flags and variables

| Op | Command | Args | In the table from | What 2.05 does | Source |
| ---: | --- | --- | --- | --- | --- |
| 604 | `set` | `M` | 1.33 | Sets a flag (doc: `server.` prefix makes it server-wide). | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#flags-and-variables) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 607 | `unset` | `M` | 1.33 | Clears a flag. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#flags-and-variables) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 666 | `setarray` | `RR` | 1.33 | Resizes the array variable named by the first argument to *n* elements. Ignored unless the first argument is a plain or `this.` variable. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#flags-and-variables) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 677 | `setstring` | `SS` | 1.33 | Sets string variable *name* = *value* (stored as the flag `name=value`). Empty value deletes it. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#flags-and-variables) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 742 | `tokenize` | `S` | 2.02 rev2 | Splits the expanded string into the global token list on spaces and commas (quotes group). | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#flags-and-variables) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 743 | `tokenize2` | `SS` | 2.02 rev2 | Same, with extra delimiter characters added to the space/comma set. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#flags-and-variables) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |

### 8.2.4.3 Control flow

| Op | Command | Args | In the table from | What 2.05 does | Source |
| ---: | --- | --- | --- | --- | --- |
| 605 | `if` | — | 1.33 | Evaluates the condition; jumps past the block when it is 0. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#control-flow) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 634 | `else` | — | 1.33 | Compiled away into a jump. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#control-flow) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 660 | `for` | — | 1.33 | Loop; condition checked each pass; stops after 10,000 passes. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#control-flow) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 667 | `sleep` | `R` | 1.33 | Sets the NPC's timeout to the value and remembers the next statement; the next `timeout` event resumes there. `sleep 0` just clears the timer display. Ends the current run. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#control-flow) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 668 | `while` | — | 1.33 | Same loop node as `for`. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#control-flow) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 710 | `callnpc` | `RS` | 1.41 rev1 | Runs NPC *index*'s script with the given event flag set. Doc: params after the event are passed as `#p(n)`. | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#control-flow) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 712 | `break` | — | 1.41 rev1 | Jumps to the end of the enclosing loop. Outside a loop it ends the script. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#control-flow) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 713 | `continue` | — | 1.41 rev1 | Jumps to the loop's next pass. Outside a loop it ends the script. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#control-flow) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 714 | `callweapon` | `RS` | 1.41 rev1 | Moves weapon *index* to the player's centre, then runs its script with the given event flag set. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#control-flow) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 716 | `function` | — | 1.41 rev1 | Compiled away. Calls to a named function become a call node (max depth 10,000). | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#control-flow) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 717 | `return` | — | 1.41 rev1 | Pops the call stack and resumes after the call. With an empty stack it ends the script. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#control-flow) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 744 | `triggeraction` | `RRSS` | 2.03 | Fires *action* with *params* at the object on (x, y) locally, and sends it online. From a weapon, the sender is the player. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#control-flow) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |

### 8.2.4.4 NPC appearance and behaviour

| Op | Command | Args | In the table from | What 2.05 does | Source |
| ---: | --- | --- | --- | --- | --- |
| 608 | `setgif` † | `F` | 1.33 | Sets the NPC image, shows the NPC, and resets the visible part to the whole image. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 619 | `dontblocklocal` | — | 1.34 | Same, local only. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 620 | `drawoverplayer` | — | 1.33 | Draw layer +1. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 631 | `timershow` | — | 1.33 | Draws the NPC's timeout counter over it. Cleared by `message` and `sleep 0`. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 638 | `blockagainlocal` | — | 1.34 | Same, local only. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 639 | `drawunderplayer` | — | 1.33 | Draw layer −1. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 641 | `canbecarried` | — | 1.33 | Player can / cannot lift the NPC. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 642 | `cannotbecarried` | — | 1.33 | Player can / cannot lift the NPC. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 644 | `canbepushed` | — | 1.33 | Player can / cannot push it. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 645 | `cannotbepushed` | — | 1.33 | Player can / cannot push it. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 646 | `canbepulled` | — | 1.33 | Player can / cannot pull it. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 647 | `cannotbepulled` | — | 1.33 | Player can / cannot pull it. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 652 | `putnpc` | `QQRR` | 1.33 | Offline: creates a new NPC with that image and script file at (x, y) and runs its `playerenters`. Online: asks the server instead. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 653 | `destroy` | — | 1.33 | Removes the NPC from the level (and from the weapon list), sends the deletes online, ends the run. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 670 | `timereverywhere` | — | 1.33 | This client gets the NPC's timeout events even when it is not the level leader. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 680 | `setgifpart` † | `FRRRR` | 1.33 | Same, then shows only (x, y, w, h) of the image in pixels. x, y are clamped to 0..16000 and w, h to 0..220, then trimmed to the image size. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 686 | `showlocal` | — | 1.34 | Same, but marked local (not synced). | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 687 | `hidelocal` | — | 1.34 | Same, marked local. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 688 | `dontblock` | — | 1.33 | Player can walk through the NPC. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 689 | `blockagain` | — | 1.33 | Blocks again and also resets the draw layer to normal (undoes `drawoverplayer`/`drawunderplayer`). | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 719 | `setimg` | `F` | 1.41 rev1 | Sets the NPC image, shows the NPC, and resets the visible part to the whole image. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 720 | `setimgpart` | `FRRRR` | 1.41 rev1 | Same, then shows only (x, y, w, h) of the image in pixels. x, y are clamped to 0..16000 and w, h to 0..220, then trimmed to the image size. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 725 | `setshape` | `RRR` | NewMain 1.42; takes arguments from 2.04 | Type 0 or 1 (1 = fixed rectangle), width and height in pixels. Other types are ignored. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 726 | `seteffect` | `RRRR` | 1.33; out 1.34–1.41; back NewMain 1.42 | Global screen tint r, g, b, a (day/night). Online gate applies. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 727 | `setcoloreffect` | `RRRR` | NewMain 1.42 | Per-NPC colour multiply r, g, b, a. Online gate applies. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 728 | `setzoomeffect` | `R` | NewMain 1.42 | Per-NPC zoom factor. Online gate applies. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 729 | `drawaslight` | — | NewMain 1.42 | Draw layer 9: above the day/night effect, below the status bar. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 745 | `move` | `RRRR` | 2.03 | Smoothly moves the NPC by dx, dy over *time* seconds with option bits. (option bits not decoded) | [2.05][inf] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 751 | `setshape2` | `RRR` | 2.04 | Makes the NPC block like a small level: width and height in tiles, plus a tile-type array (literal or array variable) of w×h entries. A short or missing array clears the shape. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 759 | `show` | — | 1.33 | Shows the NPC (re-applies its image). | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 760 | `hide` | — | 1.33 | Hides the NPC (only if it is in the current level). If it was following the player, it stops following and the run ends. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |

### 8.2.4.5 Character NPCs (`showcharacter`)

| Op | Command | Args | In the table from | What 2.05 does | Source |
| ---: | --- | --- | --- | --- | --- |
| 633 | `followplayer` | — | 1.33 | Offline only: NPC follows the player and stops blocking. Ignored online (matches the doc). | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#character-npcs-showcharacter) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 673 | `showcharacter` | — | 1.33 | Draws the NPC as a player character (once; later calls do nothing). | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#character-npcs-showcharacter) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 675 | `setcharprop` | `MM` | 1.33 | Sets a character property from a message code: `#1` sword image, `#2` shield image, `#3` head image, `#5` horse image (creates the horse if needed), `#8` body image, `#C0`..`#C5` colours (name or number), `#P1`..`#P5` attributes, `#c` chat text (not in preview mode), `#n` nickname. Other codes are ignored. The first word is the property code (not expanded as a message). Codes inside the value are expanded first; on script-running servers `#n` in that value is the triggering player's nickname, while property code `#n` writes the NPC's nickname — see `server-notes/setcharprop-hash-n.md`. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#character-npcs-showcharacter) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 684 | `carryobject` | `L` | 1.34 | Character carries the object (0..10; `none` = 10). Only for `showcharacter` NPCs; switches to the carry gani. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#character-npcs-showcharacter) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 685 | `throwcarry` | — | 1.34 | Throws the carried object if the character is in a carry sprite; bombs become live bombs. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#character-npcs-showcharacter) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 701 | `takehorse` | `R` | 1.36 | Character mounts horse *index* (removes it from the level). Only for `showcharacter` NPCs. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#character-npcs-showcharacter) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 709 | `setcharani` | `SS` | 1.39 | Sets the character's gani and its parameter string. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#character-npcs-showcharacter) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 733 | `setchargender` | `S` | 2.0 | `male` sets male; anything else sets female. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#character-npcs-showcharacter) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |

### 8.2.4.6 The player

| Op | Command | Args | In the table from | What 2.05 does | Source |
| ---: | --- | --- | --- | --- | --- |
| 603 | `hurt` | `R` | 1.33 | Hurts the player by half-hearts and knocks them away from the NPC's centre. Skipped when the player cannot be hurt right now (dead, in a protected state, or flagged unhittable on an NPC-server). 0 or negative heals (doc). | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 610 | `setlevel` | `M` | 1.33; takes arguments from 1.38 | Warps the player to that level at the current x, y. Ends the run. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 611 | `setskincolor` | `C` | 1.33 | Player colour slots 0..4. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 612 | `setcoatcolor` | `C` | 1.33 | Player colour slots 0..4. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 613 | `setsleevecolor` | `C` | 1.33 | Player colour slots 0..4. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 614 | `setshoecolor` | `C` | 1.33 | Player colour slots 0..4. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 615 | `setbeltcolor` | `C` | 1.33 | Player colour slots 0..4. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 616 | `setplayerdir` | `D` | 1.33 | Player direction, reduced mod 4. Accepts a name or an expression (doc says names only). | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 618 | `takeplayercarry` | — | 1.33 | Removes what the player carries and resets the gani. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 621 | `enableweapons` | — | 1.33 | Turns player weapons on / off. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 622 | `disableweapons` | — | 1.33 | Turns player weapons on / off. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 632 | `toinventory` | `S` | 1.33 | Sets the flag and moves the NPC into the inventory. Offline it leaves the level and the run ends; online a copy goes to the inventory and the NPC stays. Only for NPCs of the current level. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (npc-library/gs1-signatures-205-followup.md#stored-letters) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 649 | `setsword` | `MR` | 1.33 | Sword image and power. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 650 | `setshield` | `MR` | 1.33 | Shield image and power. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 654 | `freezeplayer` | `R` | 1.33 | Freezes the player for 0..30 seconds (clamped) and drops what they carry. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 655 | `sethead` | `F` | 1.33 | Player head image. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 656 | `toweapons` | `M` | 1.33 | Adds a copy of the NPC as weapon *name* (replacing one with the same name, in the same slot), runs its `playerenters`, selects it, and sends it online. A `/` in the name keeps only the part after it. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 659 | `hidesword` | `R` | 1.33 | Hides the sword for 0..30 seconds. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 663 | `setbow` † | `S` | 1.33 | Sets the bow image on the running NPC's character, not on the player. (differs from doc, which says the player's bow) | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 669 | `hideplayer` | `R` | 1.33 | Hides the player for 0..30 seconds. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 674 | `setplayerprop` | `MM` | 1.33 | Same codes as `setcharprop` but on the player: `#1 #2 #3 #5 #8 #C0..#C5 #P1..#P5 #c`. `#c` sets the chat text with a 60-tick timeout and sends it online. `#7` is not handled (doc lists it). | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 683 | `setbody` | `F` | 1.33 | Player body image (skipped if it is the same file). | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 691 | `takeplayerhorse` | — | 1.36 | Removes the player's horse. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 705 | `setlevel2` | `MRR` | 1.38 | Warps to that level at (x, y). Ends the run. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 708 | `setani` | `SS` | 1.39 | Player gani and parameter string. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 723 | `showstats` | `R` | 1.41 rev1 | Bitmask of status-bar parts to show (doc: 1 ASD, 2 icons, 4 rupees, 8 bombs, ...). | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 732 | `setgender` | `S` | 2.0 | `male` sets male; anything else sets female. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 737 | `enabledefmovement` | — | 2.0 | Turns the built-in movement and controls on / off. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 738 | `disabledefmovement` | — | 2.0 | Turns the built-in movement and controls on / off. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 749 | `replaceani` | `MM` | 2.04 | Replaces one of the 31 default gani names (walk, idle, sword, ...) with another gani file. Online gate applies. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (npc-library/gs1-signatures-205-followup.md#stored-letters) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 750 | `attachplayertoobj` | `RR` | 2.04 | Type 0 only (NPC): attaches the player to the NPC with that id. Online gate applies. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 752 | `detachplayer` | — | 2.04 | Detaches the player if attached. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 753 | `enableselectweapons` | — | 2.04 | Allows / blocks opening the weapon selection. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 754 | `disableselectweapons` | — | 2.04 | Allows / blocks opening the weapon selection. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#the-player) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |

### 8.2.4.7 Combat, items, level objects

| Op | Command | Args | In the table from | What 2.05 does | Source |
| ---: | --- | --- | --- | --- | --- |
| 601 | `lay` | `I` | 1.33; takes arguments from 1.36 | Drops the item next to the NPC, to the right or below depending on where the player stands (doc). | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 602 | `take` | `I` | 1.33 | Picks up the first item of that type lying within the NPC's radius (half its diagonal) and gives it to the NPC. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 609 | `removecompus` | — | 1.33 | Deletes every baddy (doc: causes `compusdied`). | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 617 | `putcomp` | `BRR` | 1.33 | Offline: spawns that baddy at (x, y). Online: asks the server. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 623 | `shootarrow` | `D` | 1.33 | Fires that projectile from the NPC's edge in the given direction (reduced mod 4). Drawn on the NPC's layer, or the player's for weapons. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 624 | `shootfireball` | `D` | 1.33 | Fires that projectile from the NPC's edge in the given direction (reduced mod 4). Drawn on the NPC's layer, or the player's for weapons. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 625 | `shootfireblast` | `D` | 1.33 | Fires that projectile from the NPC's edge in the given direction (reduced mod 4). Drawn on the NPC's layer, or the player's for weapons. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 626 | `shootnuke` | `D` | 1.33 | Fires that projectile from the NPC's edge in the given direction (reduced mod 4). Drawn on the NPC's layer, or the player's for weapons. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 627 | `putbomb` | `RRR` | 1.33 | Bomb of power 0..2 at (x, y). | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 628 | `putexplosion` | `RRR` | 1.33; takes arguments from 1.41 rev1 | Explosion of radius *r* at (x, y), with sound. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 629 | `putleaps` | `RRR` | 1.33 | Leaps of type 0..5 at (x, y) (bush, swamp, stone, sign, ball, water). | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 630 | `shootball` | — | 1.33 | Fires a ball from the NPC's centre toward the player. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 640 | `puthorse` | `MRR` | 1.33 | Horse with that image at (x, y). | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (npc-library/gs1-signatures-205-followup.md#stored-letters) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 643 | `noplayerkilling` | — | 1.33 | Turns off player-vs-player damage in this level. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 651 | `putnewcomp` | `BRRMR` | 1.33 | Same, plus image and power. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 661 | `hitcompu` | `RRRR` | 1.33 | index, power, fromx, fromy: damages and knocks back the baddy, and sends it online. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 662 | `hitplayer` | `RRRR` | 1.33 | index, half-hearts, fromx, fromy. Local player: hurt with knockback. Another player: UDP 21 to that player only (skipped if they are dead or protected). An NPC: treated like `hitnpc`. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 692 | `removebomb` | `R` | 1.36 | Deletes bomb *index*. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 693 | `removearrow` | `R` | 1.36 | Deletes arrow *index* (local only, doc). | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 694 | `removeitem` | `R` | 1.36 | Deletes item *index*. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 695 | `removeexplo` | `R` | 1.36 | Deletes explosion *index*. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 696 | `removehorse` | `R` | 1.36 | Deletes horse *index*. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 697 | `explodebomb` | `R` | 1.36 | Detonates bomb *index* now. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 698 | `reflectarrow` | `R` | 1.36 | Reverses arrow *index*. Against a character NPC it bounces off the side it hits; otherwise both directions flip. The arrow's sprite turns to its new direction and the shooter becomes the player when called from a weapon. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 699 | `lay2` | `IRR` | 1.36 | Drops the item at (x, y). | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 700 | `take2` | `R` | 1.36 | Picks up item *index*. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 706 | `hitnpc` | `RRRR` | 1.38 | NPC *index* gets the damage; its script gets `washit` style handling (no automatic push, doc). | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 715 | `spyfire` | `RR` | 1.41 rev1 | Spawns a fire-spy effect just in front of the player (player position plus their facing direction) and sends it online. (role of the two arguments) In 1.41 rev1 and NewMain 1.42 it parses but does nothing; it works from 2.0. | [2.05][inf] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands; client-internals/spyfire-by-version.md#result) |
| 722 | `putexplosion2` | `RRRR` | 1.41 rev1 | Power, radius, x, y; power 3 is a jolt-bomb explosion. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 741 | `hitobjects` | `RRR` | 2.01 | Hits everything at (x, y) with *power*, like a sword, and sends it online. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#combat-items-level-objects) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |

### 8.2.4.8 Board, map, images

| Op | Command | Args | In the table from | What 2.05 does | Source |
| ---: | --- | --- | --- | --- | --- |
| 657 | `showimg` | `RMRR` | 1.33 | Image *index* at (x, y), on the NPC's layer +1 (player's for weapons). Re-using an index replaces it; the same file only moves. A name starting with `@` is a text image. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#board-map-images) [bin] (npc-library/gs1-signatures-205-followup.md#stored-letters) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 658 | `hideimg` | `R` | 1.33 | Deletes image *index*. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#board-map-images) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 664 | `updateboard` | `RRRR` | 1.33 | Redraws the board rectangle (x, y, w, h) after `board[]` writes (doc: also syncs online). | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#board-map-images) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 665 | `putobject` | `ORR` | 1.33 | Offline only: stamps a predefined tile object on the 64×64 board at (x, y), clipped to the board, then redraws. Ignored online (doc: security). | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#board-map-images) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 671 | `setminimap` | `FFRR` | 1.33 | Same for the minimap. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#board-map-images) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 672 | `setmap` | `FFRR` | 1.33 | Loads the big map image and its level-names file, sets the player's head-icon position, and recomputes "is on map" for every player. Both files must exist. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#board-map-images) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 704 | `changeimgpart` | `RRRRR` | 1.38 | Visible part of image *index*; x, y clamped to 0..16000, w, h to 0..220. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#board-map-images) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 718 | `changeimgvis` | `RR` | 1.41 rev1 | Layer of image *index*: 0, 1, 2 = under / level with / over the NPC; 3 = light layer (like `drawaslight`); 4 = screen (over the status bar). | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#board-map-images) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 730 | `changeimgcolors` | `RRRRR` | NewMain 1.42 | Colour multiply for image *index*. Online gate applies. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#board-map-images) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 731 | `changeimgzoom` | `RR` | NewMain 1.42 | Zoom for image *index*. Online gate applies. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#board-map-images) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 746 | `addtiledef` | `SSR` | 2.04 | Use image *file* instead of `pics1.png` for levels starting with *prefix*. Online gate applies. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#board-map-images) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 747 | `addtiledef2` | `SSRR` | 2.04 | Same, but pastes the image at (x, y) of the tileset. Online gate applies. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#board-map-images) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 748 | `removetiledefs` | `S` | 2.04 | Removes tile definitions for *prefix*. Online gate applies. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#board-map-images) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 758 | `loadmap` | `F` | 2.05 rev1 | Loads a gmap file; if the current level belongs to it (and the editor is closed), rebuilds the level view. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#board-map-images) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |

### 8.2.4.9 Parsed but ignored by the 2.05 client

| Op | Command | Args | In the table from | What 2.05 does | Source |
| ---: | --- | --- | --- | --- | --- |
| 636 | `seturllevel` | `M` | 1.33 | parsed, no executor case; doc describes it as an offline URL warp; not implemented here. | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#parsed-but-ignored-by-the-205-client) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 681 | `setfocus` | `RR` | 1.33 | parsed, no executor case; later logs mention a camera focus at (x, y). | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#parsed-but-ignored-by-the-205-client) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 682 | `resetfocus` | — | 1.33 | parsed, no executor case | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#parsed-but-ignored-by-the-205-client) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 690 | `setbacktile` † | `R` | 1.34; takes arguments from 2.05 rev1 | parsed, no executor case; allowed in preview mode but still a no-op. | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#parsed-but-ignored-by-the-205-client) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 707 | `canwarp2` † | — | NewMain 1.42 | parsed, no executor case; warp permission is handled by the server in this era (inf). | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#parsed-but-ignored-by-the-205-client) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 721 | `drawovertrees` † | — | 1.41 rev1 | parsed, no executor case | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#parsed-but-ignored-by-the-205-client) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 724 | `canwarp` † | — | 1.41 rev1 | parsed, no executor case | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#parsed-but-ignored-by-the-205-client) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 734 | `join` † | `S` | 2.0 | parsed, no executor case; server-side class join in later versions (inf). | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#parsed-but-ignored-by-the-205-client) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 735 | `freezeplayer2` † | — | 2.0 | parsed, no executor case | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#parsed-but-ignored-by-the-205-client) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 736 | `unfreezeplayer` | — | 2.0 | parsed, no executor case | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#parsed-but-ignored-by-the-205-client) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 755 | `setbacktile2` † | `RRRRR` | 2.05 rev1 | parsed, no executor case | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#parsed-but-ignored-by-the-205-client) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 756 | `setz` † | `RRRRRRRR` | 2.05 rev1 | parsed, no executor case | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#parsed-but-ignored-by-the-205-client) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 757 | `updateterrain` | — | 2.05 rev1 | parsed, no executor case | [2.05] (npc-library/gs1-reference-205.md#commands-161-205; npc-library/gs1-command-reference-205.md#parsed-but-ignored-by-the-205-client) [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
## 8.2.5 Functions and variables

Expressions resolve names through a table of functions and variables with numeric ids [2.05] (npc-library/gs1-reference-205.md#functions-and-variables-205).

| Ids | Group | Names | Source |
| --- | --- | --- | --- |
| 100–102 | board and conversion | `board[R]`, `strtofloat(S)`, `timevar` | [2.05] (npc-library/gs1-reference-205.md#functions-and-variables-205) |
| 200–218 | object counts and globals | `compuscount`, `playerscount`, `bombscount`, `arrowscount`, `itemscount`, `exploscount`, `horsescount`, `npcscount`, `signscount`, `selectedweapon`, `screenwidth`, `screenheight`, `tokenscount`, `paramscount`, `actionplayer`, `weaponscount`, `levelorgx`, `levelorgy` | [2.05] (npc-library/gs1-reference-205.md#functions-and-variables-205) |
| 400–455 | maths, tests, string tests | `random(R,R)`, `sin(R)`, `cos(R)`, `arctan(R)`, `int(R)`, `abs(R)`, `arraylen(R)`, `testcompu(R,R)`, `testplayer(R,R)`, `testbomb(R,R)`, `testitem(R,R)`, `testexplo(R,R)`, `testhorse(R,R)`, `testnpc(R,R)`, `testsign(R,R)`, `tiletype(R,R)`, `onwall(R,R)`, `playersays(S)`, `playersays(R,S)`, `playersays2(S)`, `playersays2(R,S)`, `strequals(S,S)`, `strcontains(S,S)`, `hasweapon(S)`, `onwater(R,R)`, `keydown(R)`, `startswith(S,S)`, `indexof(S,S)`, `strlen(S)`, `onmapx(S)`, `onmapy(S)`, `vecx(R)`, `vecy(R)`, `getz(R,R)` | [2.05] (npc-library/gs1-reference-205.md#functions-and-variables-205) |
| 600–606 | `compus[i].*` | x=600, y=601, type=602, dir=603, headdir=604, power=605, mode=606 | [bin] (npc-library/gs1-object-members-205r2.md#parser-binding) |
| 640–643 | `bombs[i].*` | x=640, y=641, power=642, time=643 | [bin] (npc-library/gs1-object-members-205r2.md#parser-binding) |
| 660–666 | `arrows[i].*` | x=660, y=661, dir=662, dx=663, dx=664 (shadowed), type=665, from=666 | [bin] (npc-library/gs1-object-members-205r2.md#parser-binding) |
| 680–683 | `items[i].*` | x=680, y=681, type=682, time=683 | [bin] (npc-library/gs1-object-members-205r2.md#parser-binding) |
| 700–704 | `explos[i].*` | x=700, y=701, power=702, time=703, dir=704 | [bin] (npc-library/gs1-object-members-205r2.md#parser-binding) |
| 720–726 | `horses[i].*` | x=720, y=721, dir=722, bushes=723, bombs=724, bombpower=725, type=726 | [bin] (npc-library/gs1-object-members-205r2.md#parser-binding) |
| 740–758 | `this.*` and `npcs[i].*` | `x`, `y`, `width`, `height`, `rupees`, `darts`, `bombs`, `hearts`, `timeout`, `glovepower`, `swordpower`, `shieldpower`, `hurtdx`, `hurtdy`, `id`, `save[2]`, `dir`, `sprite`, `ap`; `save` takes an index | [2.05] (npc-library/gs1-reference-205.md#functions-and-variables-205) |
| 780–781 | `signs[i].*` | x=780, y=781 | [bin] (npc-library/gs1-object-members-205r2.md#parser-binding) |
| 800–819 | `player*` and `players[i].*` | `playerx`, `playery`, `playerrupees`, `playerdarts`, `playerbombs`, `playerhearts`, `playerfullhearts`, `playerdir`, `playerglovepower`, `playerbombpower`, `playershootpower`, `playerswordpower`, `playershieldpower`, `playerheadset`, `playersprite`, `playerid`, `playersaysnumber`, `playermp`, `playerap`, `playerhurtdx` | [2.05] (npc-library/gs1-reference-205.md#functions-and-variables-205) |
| 820–825 | `player*` and `players[i].*` | `playerhurtdy`, `playerfreezetime`, `playerhurtpower`, `playerattachid`, `playerattachtype`, `playerz` | [2.05] (npc-library/gs1-reference-205.md#functions-and-variables-205) |

The seven families above have 36 exact compiled records / 35 distinct family/member spellings. The parser matches stored suffixes and exits on its first successful record: arrow `dx=663` shadows the duplicate `dx=664` vertical getter, with no builtin `dy` spelling. This replaces the documentation-order inference for the exact checked build → App. E#204. Expression IDs are language identifiers, not binary addresses or serialized bytecode [bin] (npc-library/gs1-object-members-205r2.md#parser-binding).

The NewWorld betas add eight time variables after the direction list. They are variables (also usable as `#v(name)` codes), not commands; the server sends the time in packet 42 [bin][doc] (client-internals/newworld-betas.md#gs1-changes):

| Variable | Range | Source |
| --- | --- | --- |
| `nwday` | 1…28 | [doc] (client-internals/newworld-betas.md#gs1-changes) |
| `nwweek` | 1…40 | [doc] (client-internals/newworld-betas.md#gs1-changes) |
| `nwyear` | 1000… | [doc] (client-internals/newworld-betas.md#gs1-changes) |
| `nwweekday` | 1…7 | [doc] (client-internals/newworld-betas.md#gs1-changes) |
| `nwmonth` | 1…10 | [doc] (client-internals/newworld-betas.md#gs1-changes) |
| `nwtime` | 0…1439 minutes | [doc] (client-internals/newworld-betas.md#gs1-changes) |
| `nwhour` | 0…23 | [doc] (client-internals/newworld-betas.md#gs1-changes) |
| `nwmin` | 0…59 | [doc] (client-internals/newworld-betas.md#gs1-changes) |

## 8.2.6 Constants

| Constant set | Values | Source |
| --- | --- | --- |
| baddy modes | 0 walking, 1 looking, 2 hunting, 3 hurt, 4 bumped, 5 dying, 6 shooting (swamp), 7 jumping (frog), 8 shooting (spider), 9 dead | [doc] (npc-library/gs1-reference-205.md#constants-doc) |
| player sprites | 0 idle; 1–8 walk; 9–13 sword; 14–18 push; 19–22 pull; 23 lift; 24 carry idle; 25–32 carry walk; 33 shoot; 34–36 ride; 37 sit; 38 sleep; 39 hurt; 40 dead; 39 and 40 only on `showcharacter` NPCs | [doc] (npc-library/gs1-reference-205.md#constants-doc) |
| tile types (`tiletype(x,y)`) | 0 nonblocking, 2 hurting underground, 3 chair, 4 bed top, 5 bed bottom, 6 swamp, 7 lava swamp, 8 near water, 9 near lava, 11 water, 12 lava, 20 throw-through, 21 jumping stone, 22 blocking | [doc] (npc-library/gs1-reference-205.md#constants-doc) |
| `move` options | cachetype 0–2; +4 block check; +8 event when done; +16 apply direction; 2.05's handling of the bits is not decoded → App. E#206 | [doc] (npc-library/gs1-reference-205.md#constants-doc); [2.05][inf] (npc-library/gs1-command-reference-205.md#npc-appearance-and-behaviour) |
| `showstats` mask | 1 ASD, 2 icons, 4 rupees, 8 bombs, and further bits the notes do not list | [doc] (npc-library/gs1-command-reference-205.md#the-player) |
| `changeimgvis` layers | 0, 1, 2 under, level with, over the NPC; 3 light layer, as `drawaslight`; 4 screen, over the status bar | [2.05] (npc-library/gs1-command-reference-205.md#board-map-images) |
| `putleaps` types | 0 bush, 1 swamp, 2 stone, 3 sign, 4 ball, 5 water | [2.05] (npc-library/gs1-command-reference-205.md#combat-items-level-objects) |
| `seteffectmode` (2.22) | 0 light, 1 transparency, 2 holes | [doc] (npc-library/gs1-reference-205.md#constants-doc) |

## 8.2.7 The command table by build

The executor matches commands against one table of fixed-size records [bin] (client-internals/cross-version-timeline.md#gs1-commands). In 2.05 and the NewWorld betas a record is 12 bytes: name, a flags word and an argument-signature string [bin] (client-internals/newworld-betas.md#gs1-changes). Other keyword lists that follow the table in some builds (`*=`, `:=`, the 1.33 soldier names, the NewWorld time variables) are not counted [bin] (client-internals/cross-version-timeline.md#gs1-commands).

| Build | Commands | Added over the previous row | Source |
| --- | ---: | --- | --- |
| 1.33 | 88 | n/a; earliest build read | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 1.34 | 93 | `dontblocklocal`, `blockagainlocal`, `showlocal`, `hidelocal`, `carryobject`, `throwcarry`, `setbacktile`; `seteffect` and `unseteffect` leave the table | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 1.35 | 93 | none; same table as 1.34 | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 1.36 | 104 | `lay2`, `take2`, `takehorse`, `takeplayerhorse`, `removebomb`, `removearrow`, `removeitem`, `removeexplo`, `removehorse`, `explodebomb`, `reflectarrow`; `lay` now takes arguments | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 1.37 | 106 | `playlooped`, `stopsound` | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 1.38 | 109 | `setlevel2`, `changeimgpart`, `hitnpc`; `setlevel` now takes arguments | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 1.39 | 111 | `setani`, `setcharani` | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 1.41 rev 1 | 126 | `canwarp`, `callnpc`, `say2`, `break`, `continue`, `callweapon`, `spyfire`, `function`, `return`, `changeimgvis`, `setimg`, `setimgpart`, `drawovertrees`, `putexplosion2`, `showstats`; `putexplosion` now takes arguments | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| NewMain 1.42 | 134 | `canwarp2`, `setshape`, `seteffect` (back), `setcoloreffect`, `setzoomeffect`, `drawaslight`, `changeimgcolors`, `changeimgzoom` | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 2.0 | 142 | `setgender`, `setchargender`, `join`, `freezeplayer2`, `unfreezeplayer`, `enabledefmovement`, `disabledefmovement`, `setmusicvolume` | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 2.01 | 144 | `openurl2`, `hitobjects`; `openurl` now takes arguments | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 2.02 rev 2 | 146 | `tokenize`, `tokenize2` | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 2.03 | 148 | `triggeraction`, `move` | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 2.04 | 157 | `addtiledef`, `addtiledef2`, `removetiledefs`, `replaceani`, `attachplayertoobj`, `detachplayer`, `setshape2`, `enableselectweapons`, `disableselectweapons`; `setshape` now takes arguments | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| 2.05 rev 1, rev 2 | 161 | `setbacktile2`, `setz`, `updateterrain`, `loadmap`; `setbacktile` now takes arguments | [bin] (client-internals/cross-version-timeline.md#gs1-commands; client-internals/build-diff-204-205.md#204--205) |
| 2.1 tests | 161 | none; same table as 2.05 | [bin] (client-internals/cross-version-timeline.md#gs1-commands) |
| NewWorld beta 1 | 161 | none; same table as 2.05 | [bin] (client-internals/cross-version-timeline.md#gs1-commands; client-internals/newworld-betas.md#gs1-changes) |
| NewWorld beta 2 | 165 | `addstring`, `insertstring`, `removestring`, `deletestring`, inserted after `loadmap` | [bin] (client-internals/cross-version-timeline.md#gs1-commands; client-internals/newworld-betas.md#gs1-changes) |

Every command or variable the 2.01 to 2.05 change logs name appears in that build's string table; the only undocumented additions are `actionplayer`, `lighteffectsenabled` (2.03) and the `bomy_*` animation names [bin][doc] (client-internals/decomp-findings-2026-10-24-c/09-features-classes-vocabulary.md#vocabulary-scriptidentifier-strings-resources-excluded); [bin] (client-internals/decomp-findings-2026-10-24-c/script_vocab_deltas.tsv). The 2.1 tests add the strings `ascii`, `defnpc`, `playeronline`, `startinfullscreen` and `tiles` (test 2) and `groundheights`, `waterheight`, `playerhp` and `playermaxhp` (test 3) outside the command table [bin] (client-internals/decomp-findings-2026-10-24-c/08-test-builds-newworld-newmain.md#21-test2-and-test3).

Being in the table does not mean a command does anything. Executor cases were read for 2.05 (→ §8.2.4.9) and for the NewWorld betas against their bases; other builds have not been checked [bin] (client-internals/cross-version-timeline.md#gs1-commands).

### 8.2.7.1 NewWorld betas

| Item | Rule | Source |
| --- | --- | --- |
| string lists (beta 2 only) | `addstring list,text` (S,S), `insertstring list,index,text` (S,R,S), `removestring list,text` (S,S), `deletestring list,index` (S,R), with `sarraylen(list)`, `lindexof(list,text)` and `#I(list,i)` | [bin] (client-internals/newworld-betas.md#gs1-changes) |
| list storage | a list is a normal string flag in comma form: `numbers="12 34",567,"8,9"` | [doc] (client-internals/newworld-betas.md#gs1-changes) |
| live in the betas, ignored in 2.05 | `setfocus`, `resetfocus`, `setbacktile`, `drawovertrees`, `setbacktile2`, `setz`, `updateterrain` | [bin] (client-internals/newworld-betas.md#gs1-changes) |
| parsed but ignored in the betas, live in 2.05 | `removecompus`, `putcomp`, `putnewcomp`, `hitcompu`; `puthorse`, `takehorse`, `takeplayerhorse`, `removehorse`; `carryobject`, `throwcarry`, `takeplayercarry`; `setsword`, `hidesword`, `setbow`; `freezeplayer`; `enabledefmovement`, `disabledefmovement`; `toinventory`; `followplayer` | [bin] (client-internals/newworld-betas.md#gs1-changes) |
| why | the control NPC script (`controlnpc.txt`) takes over movement, swords, carrying and horses | [bin][doc] (client-internals/newworld-betas.md#gs1-changes) |

### 8.2.7.2 Scripting changes from 2.1 to 2.31

From the release notes; the binaries have not been read for the command tables of these builds [doc] (client-internals/feature-timeline.md).

| Version | Scripting change | Source |
| --- | --- | --- |
| 2.02 | string parsing | [doc] (client-internals/feature-timeline.md) |
| 2.04 | gani `PLAYSOUND PARAM1`, `replacegani` | [doc] (client-internals/feature-timeline.md) |
| 2.1 | gani scripts (`SCRIPT … SCRIPTEND`), string arrays, `play2`, `graalversion` | [doc] (client-internals/feature-timeline.md) |
| 2.12 | `wraptext`, `wraptext2` | [doc] (client-internals/feature-timeline.md) |
| 2.15 | `showimg2` | [doc] (client-internals/feature-timeline.md) |
| 2.16 | `seteffectmode` (real transparency); gani attributes `#P10`–`#P30` | [doc] (client-internals/feature-timeline.md) |
| 2.17 | sound through BASS, with the same GS1 sound commands plus `musicpos` and `musiclen` | [2.17][2.22] (client-internals/feature-specs/01-sound.md) |
| 2.19 | `this.` strings on the client; on NPC-server servers only `client.` strings are sent | [doc] (client-internals/feature-timeline.md) |
| 2.2 | `updateboard2` for server-side tile changes on gmaps | [doc] (client-internals/feature-timeline.md) |
| 2.21 | `triggeraction 0,0,clientside,…` reaches a weapon's client-side part | [doc] (client-internals/feature-timeline.md) |
| 2.22 | `gravity`, `downloadsize` | [doc] (client-internals/feature-timeline.md) |
| 2.3 | classic client-side NPC mode removed; `timevar2` | [doc] (client-internals/feature-timeline.md) |
| 2.22 (symbol table, against 2.17) | added `gravity`, `textwidth(zoom,font,style,text)`, `textheight(zoom,font,style)`, `isthisflagset`, `isplayerflagset`, and a `#R` message code with a string argument; removed `isflagset`, which the two new tests replace | [bin] (version-profiles/2.22-2.31.md#gs1-script-differences-from-the-clients-symbol-table-bin) |
| 2.31 (symbol table, against 2.22) | added `timevar2`, `downloadsize`, `onwall2(x,y,w,h)`, `onwater2(x,y,w,h)`; nothing removed | [bin] (version-profiles/2.22-2.31.md#gs1-script-differences-from-the-clients-symbol-table-bin) |
| 2.22 `downloadsize` | announced in the 2.22 notes but absent from the 2.22 symbol table; a 2.22 script sees it as undefined (0) | [bin][doc][inf] (version-profiles/2.22-2.31.md#gs1-script-differences-from-the-clients-symbol-table-bin) |

### 8.2.7.3 2.05 against the 2.22 documentation

| Item | Names | Source |
| --- | --- | --- |
| documented for 2.22, absent in 2.05 | `addstring`, `insertstring`, `replacestring`, `removestring`, `deletestring`, `putnpc2`, `showtext`, `showtext2`, `showpoly`, `showani`, `play2`, `setshootparams`, `shoot`, `enablefeatures`, `seteffectmode`, `changeimgmode`, and the mouse and `keypressed` family | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205) |
| in 2.05, not in the 2.22 `commands.rtf` | the † rows of §8.2.4 | [2.05][doc] (npc-library/gs1-reference-205.md#commands-161-205) |

## 8.2.8 Superseded readings

An earlier catalogue of GS1 commands, built from public tables and the scrape before 2.05 was read, is corrected by the 2.05 reading [2.05] (npc-library/gs1-command-reference-205.md#corrections-to-gs1-commandsmd). The corrected values are the ones in this chapter.

| Earlier reading | Corrected | Source |
| --- | --- | --- |
| `R` is the literal string "real" | `R` is a numeric expression | [2.05] (npc-library/gs1-command-reference-205.md#corrections-to-gs1-commandsmd); [file] (npc-library/gs1-commands.md#pattern-letters) |
| `D` is 0 south, 1 west, 2 east, 3 north | `D` is 0 up, 1 left, 2 down, 3 right, or a number | [2.05] (npc-library/gs1-command-reference-205.md#corrections-to-gs1-commandsmd); [file] (npc-library/gs1-commands.md#pattern-letters) |
| `warp` and `jump` are commands | neither is a GS1 command in 2.05 (→ §8.1.8) | [2.05] (npc-library/gs1-command-reference-205.md#corrections-to-gs1-commandsmd) |
| `canwarp`, `canwarp2`, `join`, `setfocus`, `resetfocus`, `unfreezeplayer` act | they compile but do nothing in 2.05 | [2.05] (npc-library/gs1-command-reference-205.md#corrections-to-gs1-commandsmd) |
| `spyfire` is a debug hook | `spyfire` is a game effect with a network message (PLI 10) | [2.05] (npc-library/gs1-command-reference-205.md#corrections-to-gs1-commandsmd) |
| the 2.05 table has 163 commands, or ends at 758 | 161 commands, 600–760, ending with `show` and `hide` | [2.05] (npc-library/gs1-commands.md#update-2026-10-21; npc-library/gs1-reference-205.md#commands-161-205) |
| 2.05 runs OpenGS1-style bytecode | 2.05 interprets a parse tree built from script text (→ §8.1.2) | [2.05] (npc-library/gs1-commands.md#update-2026-10-21) |

## 8.2.9 Exact-build object getter semantics

For these seven families, evaluation computes the numeric index and, for ordinary finite in-range values, uses `floor(value + 0.0001)`. It bounds-checks the local player's current-level list; absent level, negative or end/out-of-range index yields initialized numeric zero. Indices are mutable list positions, not persistent IDs; event/expression snapshot guarantees are unproved [bin] (npc-library/gs1-object-members-205r2.md#evaluation-and-bounds).

Compus, bombs, arrows, items, explos and horses expose double x/y coordinates; signs expose integer coordinates converted to floating results. Compus state and bomb power are direct integers. Bomb/item/explosion time divides an integer timer by 20, without measuring scheduler cadence. Arrow direction uses displacement, horizontal winning ties: nonnegative horizontal is right, negative left, otherwise nonnegative vertical down and negative up; zero vector reports right. Its first dx is horizontal and the shadowed duplicate vertical. Arrow type/from are raw integer state with enum/producer meanings separate [bin] (npc-library/gs1-object-members-205r2.md#getter-effects).

Item type decodes an identity, searches 25 entries and returns the matching index or minus one (last match if duplicated); its helper checks redundant values and may take an integrity-failure path. Explosion direction maps stored state through a shared table whose full contents/invalid-index behavior remain unvalidated. Horse dir/bombpower are direct integers; bushes/bombs use specialized decoded getters, with redundant-value checks in bushes and incomplete bombs-helper semantics. Horse type maps a stored boolean to zero/one without establishing semantic varieties. These getters are not all inert reads [bin] (npc-library/gs1-object-members-205r2.md#getter-effects).

Two original-client offline runs contribute twelve displayed controls. Signs at (14,24)/(39,37) read correctly, negative/end indices yield zero, and 0.9998/0.99995 choose first/second sign. Up/right arrows show direction0/dx0 and direction3/dx1. A separate up-arrow snapshot after requested sleep0.2 has count1, direction0, dx0 and unassigned dy0 while y decreased4; zero dy does not prove no vertical motion or a general fallback rule. A requested power1 bomb at (20,35) reads count1/x20/y35/power1/time3. No writes, live AST or timing cadence were measured [lab] (npc-library/gs1-object-members-205r2.md#original-client-corroboration).

The exact unchanged original Windows2.05r2 ran under Wine/private display in isolated namespaces without a server, using explicit 2.31 donor assets and owned fixtures. Both supervisors exited zero and cleanup completed; the count2 result is unobscured despite a nearby minimap. Identity/static/visual observations are researcher supplied. Fresh parser/table/bounds instructions and recovered matching getter/helper text support the mapping; this is not full instruction validation of every helper. Writes, setter clamps/notifications, unknown-member fallback, scanner case/quoting, enum meanings, explosion mapping, horse decoder/integrity consequences and other builds remain open [bin][lab] (npc-library/gs1-object-members-205r2.md#coverage-and-limits; npc-library/gs1-object-members-205r2.md#original-client-corroboration).
