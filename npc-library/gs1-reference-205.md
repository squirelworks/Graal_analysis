# GS1 reference — client 2.05 rev 2

Date: 2026-10-21

Sources: the 2.05 command and expression tables (names and argument signatures only; no code); Graal Reborn 2.22 `commands.rtf` and `npcprogramming.doc` (user's Drive); OpenGS1 (MIT) for comparison. Tags: **[2.05]** read from the 2.05 tables · **[doc]** 2.22 docs · **[inf]**.

## Execution model **[2.05]**

- 2.05 does **not** compile GS1 to bytecode. NPC and weapon scripts arrive as source text (`NPCPROP_SCRIPT`), are parsed into a tree, and are interpreted recursively.
- Command ids are `600 + table index`. `if` is 605. A condition counts as true when it evaluates to ≥ 1.0.
- Expressions resolve through a second table of functions and variables with numeric ids (100–825, below) and a small operator table.
- OpenGS1's stack bytecode (Push/Assign/Jmp/…) is an independent reimplementation. Its opcode set is not something 2.05 shares. Keep Seihai's VM, but load scripts from text.
- Command names that end in a space in the table (`say `, `set `, `setlevel `, `setimg `, `move `, …) require an argument. The others are matched as whole words. **[inf]**

## Argument signature letters

One letter per argument in the table's signature column:

| Letter | Meaning | Tag |
|:------:|---------|-----|
| R | numeric expression | [2.05][inf] |
| S | string expression (`#s`, quoted text, string vars) | [inf] |
| M | message / free text up to `;` (flag names, level names) | [inf] |
| F / Q | filename | [inf] |
| I | item name (`greenrupee` … `spinattack`) | [doc] |
| B | baddy name (`graysoldier` … `dragon`) | [doc] |
| C | color name (`white` … `transparent`) | [doc] |
| D | direction: `up`/`left`/`down`/`right` or 0–3 | [doc] |
| L | carry object (`bush`, `sign`, `vase`, `stone`, `blackstone`, `bomb`, …) | [doc] |
| O | tile object (from `tileobjects/`) | [inf] |

This replaces the "R = literal `real`" reading in `gs1-commands.md`.

## Commands (159) **[2.05]**

| Op | Command | Args | Op | Command | Args | Op | Command | Args |
|---:|---------|------|---:|---------|------|---:|---------|------|
| 600 | `say` | R | 601 | `lay` | I | 602 | `take` | I |
| 603 | `hurt` | R | 604 | `set` | M | 605 | `if` | — |
| 606 | `play` | F | 607 | `unset` | M | 608 | `setgif`† | F |
| 609 | `removecompus` | — | 610 | `setlevel` | M | 611 | `setskincolor` | C |
| 612 | `setcoatcolor` | C | 613 | `setsleevecolor` | C | 614 | `setshoecolor` | C |
| 615 | `setbeltcolor` | C | 616 | `setplayerdir` | D | 617 | `putcomp` | BRR |
| 618 | `takeplayercarry` | — | 619 | `dontblocklocal` | — | 620 | `drawoverplayer` | — |
| 621 | `enableweapons` | — | 622 | `disableweapons` | — | 623 | `shootarrow` | D |
| 624 | `shootfireball` | D | 625 | `shootfireblast` | D | 626 | `shootnuke` | D |
| 627 | `putbomb` | RRR | 628 | `putexplosion` | RRR | 629 | `putleaps` | RRR |
| 630 | `shootball` | — | 631 | `timershow` | — | 632 | `toinventory` | S |
| 633 | `followplayer` | — | 634 | `else` | — | 635 | `openurl` | M |
| 636 | `seturllevel` | M | 637 | `stopmidi` | — | 638 | `blockagainlocal` | — |
| 639 | `drawunderplayer` | — | 640 | `puthorse` | MRR | 641 | `canbecarried` | — |
| 642 | `cannotbecarried` | — | 643 | `noplayerkilling` | — | 644 | `canbepushed` | — |
| 645 | `cannotbepushed` | — | 646 | `canbepulled` | — | 647 | `cannotbepulled` | — |
| 648 | `message` | S | 649 | `setsword` | MR | 650 | `setshield` | MR |
| 651 | `putnewcomp` | BRRMR | 652 | `putnpc` | QQRR | 653 | `destroy` | — |
| 654 | `freezeplayer` | R | 655 | `sethead` | F | 656 | `toweapons` | M |
| 657 | `showimg` | RMRR | 658 | `hideimg` | R | 659 | `hidesword` | R |
| 660 | `for` | — | 661 | `hitcompu` | RRRR | 662 | `hitplayer` | RRRR |
| 663 | `setbow`† | S | 664 | `updateboard` | RRRR | 665 | `putobject` | ORR |
| 666 | `setarray` | RR | 667 | `sleep` | R | 668 | `while` | — |
| 669 | `hideplayer` | R | 670 | `timereverywhere` | — | 671 | `setminimap` | FFRR |
| 672 | `setmap` | FFRR | 673 | `showcharacter` | — | 674 | `setplayerprop` | MM |
| 675 | `setcharprop` | MM | 676 | `showfile` | F | 677 | `setstring` | SS |
| 678 | `setbackpal` | F | 679 | `setletters` | F | 680 | `setgifpart`† | FRRRR |
| 681 | `setfocus` | RR | 682 | `resetfocus` | — | 683 | `setbody` | F |
| 684 | `carryobject` | L | 685 | `throwcarry` | — | 686 | `showlocal` | — |
| 687 | `hidelocal` | — | 688 | `dontblock` | — | 689 | `blockagain` | — |
| 690 | `setbacktile`† | R | 691 | `takeplayerhorse` | — | 692 | `removebomb` | R |
| 693 | `removearrow` | R | 694 | `removeitem` | R | 695 | `removeexplo` | R |
| 696 | `removehorse` | R | 697 | `explodebomb` | R | 698 | `reflectarrow` | R |
| 699 | `lay2` | IRR | 700 | `take2` | R | 701 | `takehorse` | R |
| 702 | `playlooped` | F | 703 | `stopsound` | F | 704 | `changeimgpart` | RRRRR |
| 705 | `setlevel2` | MRR | 706 | `hitnpc` | RRRR | 707 | `canwarp2`† | — |
| 708 | `setani` | SS | 709 | `setcharani` | SS | 710 | `callnpc` | RS |
| 711 | `say2` | S | 712 | `break` | — | 713 | `continue` | — |
| 714 | `callweapon` | RS | 715 | `spyfire` | RR | 716 | `function` | — |
| 717 | `return` | — | 718 | `changeimgvis` | RR | 719 | `setimg` | F |
| 720 | `setimgpart` | FRRRR | 721 | `drawovertrees`† | — | 722 | `putexplosion2` | RRRR |
| 723 | `showstats` | R | 724 | `canwarp`† | — | 725 | `setshape` | RRR |
| 726 | `seteffect` | RRRR | 727 | `setcoloreffect` | RRRR | 728 | `setzoomeffect` | R |
| 729 | `drawaslight` | — | 730 | `changeimgcolors` | RRRRR | 731 | `changeimgzoom` | RR |
| 732 | `setgender` | S | 733 | `setchargender` | S | 734 | `join`† | S |
| 735 | `freezeplayer2`† | — | 736 | `unfreezeplayer` | — | 737 | `enabledefmovement` | — |
| 738 | `disabledefmovement` | — | 739 | `setmusicvolume` | RR | 740 | `openurl2` | MRR |
| 741 | `hitobjects` | RRR | 742 | `tokenize` | S | 743 | `tokenize2` | SS |
| 744 | `triggeraction` | RRSS | 745 | `move` | RRRR | 746 | `addtiledef` | SSR |
| 747 | `addtiledef2` | SSRR | 748 | `removetiledefs` | S | 749 | `replaceani` | MM |
| 750 | `attachplayertoobj` | RR | 751 | `setshape2` | RRR | 752 | `detachplayer` | — |
| 753 | `enableselectweapons` | — | 754 | `disableselectweapons` | — | 755 | `setbacktile2`† | RRRRR |
| 756 | `setz`† | RRRRRRRR | 757 | `updateterrain` | — | 758 | `loadmap` | F |

† = not in the 2.22 `commands.rtf`: either removed or renamed by 2.22 (`setgif`→`setimg`, `setgifpart`→`setimgpart`), or undocumented (`setz`, `drawovertrees`, `setbacktile*`, `canwarp*`, `join`, `freezeplayer2`, `setbow`).

**Missing from the table:** `hide` and `show`, the two most common commands in the scraped library, are not table entries. `showlocal`, `hidelocal`, `hideimg`, `hideplayer`, and `hidesword` are. Either the parser special-cases them or the table extraction missed entries. **Open.** Commands documented for 2.22 but absent in 2.05 include `addstring`/`insertstring`/`replacestring`/`removestring`/`deletestring`, `putnpc2`, `showtext`/`showtext2`, `showpoly`, `showani`, `play2`, `setshootparams`, `shoot`, `enablefeatures`, `seteffectmode`, `changeimgmode`, and the mouse/keypressed family.

## Functions and variables **[2.05]**

| Id range | Group | Names |
|---------:|-------|-------|
| 100–102 | board / conversion | `board[R]`, `strtofloat(S)`, `timevar` |
| 200–218 | object counts and globals | `compuscount`, `playerscount`, `bombscount`, `arrowscount`, `itemscount`, `exploscount`, `horsescount`, `npcscount`, `signscount`, `selectedweapon`, `screenwidth`, `screenheight`, `tokenscount`, `paramscount`, `actionplayer`, `weaponscount`, `levelorgx`, `levelorgy` |
| 400–455 | math, tests, string tests | `random(R,R)`, `sin(R)`, `cos(R)`, `arctan(R)`, `int(R)`, `abs(R)`, `arraylen(R)`, `testcompu(R,R)`, `testplayer(R,R)`, `testbomb(R,R)`, `testitem(R,R)`, `testexplo(R,R)`, `testhorse(R,R)`, `testnpc(R,R)`, `testsign(R,R)`, `tiletype(R,R)`, `onwall(R,R)`, `playersays(S)`, `playersays(R,S)`, `playersays2(S)`, `playersays2(R,S)`, `strequals(S,S)`, `strcontains(S,S)`, `hasweapon(S)`, `onwater(R,R)`, `keydown(R)`, `startswith(S,S)`, `indexof(S,S)`, `strlen(S)`, `onmapx(S)`, `onmapy(S)`, `vecx(R)`, `vecy(R)`, `getz(R,R)` |
| 600–606 | compus[i].* | 7 members; the 2.22 docs list the same count: x, y, type, dir, headdir, power, mode [doc] |
| 640–643 | bombs[i].* | 4 members; the 2.22 docs list the same count: x, y, power, time [doc] |
| 660–666 | arrows[i].* | 7 members; the 2.22 docs list the same count: x, y, dx, dy, dir, type, from [doc] |
| 680–683 | items[i].* | 4 members; the 2.22 docs list the same count: x, y, type, time [doc] |
| 700–704 | explos[i].* | 5 members; the 2.22 docs list the same count: x, y, power, time, dir [doc] |
| 720–726 | horses[i].* | 7 members; the 2.22 docs list the same count: x, y, dir, bushes, bombs, bombpower, type [doc] |
| 740–758 | this.* / npcs[i].* | `x`, `y`, `width`, `height`, `rupees`, `darts`, `bombs`, `hearts`, `timeout`, `glovepower`, `swordpower`, `shieldpower`, `hurtdx`, `hurtdy`, `id`, `save[2]`, `dir`, `sprite`, `ap` (the same ids reached through `npcs[i].`; `save` takes an index) |
| 780–781 | signs[i].* | 2 members; the 2.22 docs list the same count: x, y [doc] |
| 800–819 | player* / players[i].* | `playerx`, `playery`, `playerrupees`, `playerdarts`, `playerbombs`, `playerhearts`, `playerfullhearts`, `playerdir`, `playerglovepower`, `playerbombpower`, `playershootpower`, `playerswordpower`, `playershieldpower`, `playerheadset`, `playersprite`, `playerid`, `playersaysnumber`, `playermp`, `playerap`, `playerhurtdx` (the same ids reached through `players[i].`) |
| 820–825 | player* / players[i].* | `playerhurtdy`, `playerfreezetime`, `playerhurtpower`, `playerattachid`, `playerattachtype`, `playerz` (the same ids reached through `players[i].`) |

Member names for `compus[i]`, `bombs[i]`, and similar objects are not in the expression table. Each group's member count matches the 2.22 doc list exactly. The names in the table are the doc names in doc order, and the mapping of names to ids is **[inf]** until the member parser is traced.

## Built-in flags and events **[2.05]**

These are flags tested with `if (name)`, not functions. The engine sets them before running a script.

**Event flags:** `created`, `playerenters`, `timeout`, `playertouchsme`, `playertouchsother`, `playerendsreading`, `playerchats`, `playersays(…)`/`playersays2(…)` (functions), `wasshot`, `wasshooted`, `washit`, `wasthrown`, `waspelt`, `peltwith…`, `exploded`, `compusdied`, `compsdead`, `playerdies`, `playerhurt`, `playerhurted`, `playerlaysitem`, `weaponfired`, `action…` (any `triggeraction` name), `shotbyplayer`, `shotbybaddy`.

**State flags:** `visible`, `carrying`, `carries…`, `carriesnpc`, `weaponsenabled`, `followsplayer`, `isweapon`, `playeronhorse`, `canspin`, `playerswimming`, `issparringzone`, `sparringzone`, `nopkzone`, `isleader`, `playerismale`, `playerisfemale`, `playerreading`, `isonmap`, `lighteffectsenabled`, `playerattached`, `firedonhorse`.

`main` sits in the same string cluster. It is probably the weapon's main event or entry. **[inf]**

Absent in 2.05 but documented for 2.22: `actionleftmouse`/`actionrightmouse`/`actiondoublemouse`, `actionprojectile`, `keypressed`, `mousedown`, `playeronline`, `playerpaused`.

## Constants **[doc]**

- **Items** (`lay`, `take`, chest item index): 0 greenrupee, 1 bluerupee, 2 redrupee, 3 bombs, 4 darts, 5 heart, 6 glove1, 7 bow, 8 bomb, 9 shield, 10 sword, 11 fullheart, 12 superbomb, 13 battleaxe, 14 goldensword, 15 mirrorshield, 16 glove2, 17 lizardshield, 18 lizardsword, 19 goldrupee, 20 fireball, 21 fireblast, 22 nukeshot, 23 joltbomb, 24 spinattack. GServer's `LevelItemType` agrees. **[srv]**
- **Baddies:** 0 graysoldier, 1 bluesoldier, 2 redsoldier, 3 shootingsoldier, 4 swampsoldier, 5 frog, 6 octopus, 7 goldenwarrior, 8 lizardon, 9 dragon. 2.05 also has `baddyhare.gif`, so a hare type exists. Its index is open.
- **Baddy modes:** 0 walking, 1 looking, 2 hunting, 3 hurt, 4 bumped, 5 dying, 6 shooting (swamp), 7 jumping (frog), 8 shooting (spider), 9 dead.
- **Directions:** 0 up, 1 left, 2 down, 3 right.
- **Player sprites:** 0 idle; 1–8 walk; 9–13 sword; 14–18 push; 19–22 pull; 23 lift; 24 carry idle; 25–32 carry walk; 33 shoot; 34–36 ride; 37 sit; 38 sleep; 39 hurt; 40 dead (39 and 40 only on `showcharacter` NPCs).
- **Tile types** (`tiletype(x,y)`): 0 nonblocking, 2 hurting underground, 3 chair, 4 bed top, 5 bed bottom, 6 swamp, 7 lava swamp, 8 near water, 9 near lava, 11 water, 12 lava, 20 throw-through, 21 jumping stone, 22 blocking.
- **Colors:** white, yellow, orange, pink, red, darkred, lightgreen, green, darkgreen, lightblue, blue, darkblue, brown, cynober, purple, darkpurple, lightgray, gray, black, transparent. The same list is used for `PLPROP_COLORS` indexes. **[srv]**
- **`move` options:** cachetype 0–2, +4 block check, +8 event when done, +16 apply direction.
- **`seteffectmode`** (2.22): 0 light, 1 transparency, 2 holes.

## Operators and syntax **[doc]**

`=`, `+=`, `-=`, `*=`, `/=`, `++`, `--`; arithmetic `+ - * / %`, `^` power; comparison `== != < > <= >=`; logic `&& || !`; `in` for ranges and sets (`x in |0,64|`, `2 in {1,2,3}`); `this.` for NPC-local variables; `#` string codes (`#s(var)`, `#v(expr)`, …, 2.x). Control flow: `if`/`else`, `for`, `while`, `break`, `continue`, `function name() {}` + `name();`, `return`, `sleep`, `timeout = n`.

The full `#` string-code set for 2.05 is not yet extracted. **Open.**
