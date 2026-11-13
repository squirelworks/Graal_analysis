# GS1 commands by client version, 1998 to 5.00r7

Date: 2026-11-04

Which GS1 script commands each Graal client knows, read from the command list inside every client binary we have, from the
1998 betas to 5.00r7 (the "5.007" build, July 2007). It answers "when was this command added or removed" from the clients
themselves rather than from release notes. All rows are **[bin]**: static reads, no client was run.

- The full matrix (208 commands × 61 builds) is [gs1-commands-by-version.tsv](gs1-commands-by-version.tsv).
- The scanner and the build list are in [tools/gs1-table-scan/](../tools/gs1-table-scan/README.md). Re-running it on the same
  binaries gives the same lists.
- What each command does in 2.05 is in [gs1-command-reference-205.md](gs1-command-reference-205.md). The argument-form changes
  for 1.33 to the NewWorld betas are in [cross-version-timeline.md](../client-internals/cross-version-timeline.md#gs1-commands).

## What "has the command" means here

A build has a command when the name is in the list its script compiler matches against. A name that is missing is not a command
in that build. The reverse does not hold: being in the list does not mean the command does anything. 2.05, for example, parses
`setz`, `updateterrain` and `setbacktile2` and then ignores them (see the 2.05 reference). This note does not check executors.

Commands are compared without the trailing space some tables use to mark "takes arguments" (`say ` and `say` are the same
command). Four node kinds the compiler registers next to the commands (`assign`, `endif`, `callfunction`, `jump`) are internal
and are left out. `if`, `else`, `for`, `while`, `function`, `return`, `break`, `continue` and `with` are words a script writes,
so they are kept. Expression functions (`strequals`, `random`, …), flags (`playeronhorse`, …) and variables are not commands and
are not in this list.

## How each family stores the list

| Builds | Where the names live | Scanner mode |
|---|---|---|
| 1st Graal (Sept 1998) | Nowhere. This build has no NPC script interpreter: none of the command names, and no NPC or script strings. | – |
| 2nd Graal to 1.1 (Sept 1998 to Feb 1999) | One static array of pointers to the names, followed by the direction words and, from 3rd Graal, by condition words such as `gotrupees`. | `table` |
| 1.21 to 1.33 | Static array of 16-byte records, the first field pointing at the name. The baddy names follow it. | `table` |
| 1.34 to the 2.1 tests and NewWorld betas | Static array of 12-byte records (name, flags, argument signature), followed by `up` and `right`. | `table` |
| 2.17.1, 2.22, 2.31 | No static table. One start-up routine creates a command object per name, then goes on to register the internal nodes, flags, functions and object members. The commands are the names before the first internal node. | `init` |
| 3.04 Linux to 5.00r7 (the C++ engine) | Also built at start-up, in the engine's script-functions source file. Every keyword is registered with its argument signature: letters such as `RRS` for commands, `(S,S)` for functions. The commands are the names before the first function. | `x86`, `ppc` |

The 1.33 to NewWorld beta 2 counts agree with the earlier count in `cross-version-timeline.md` (88 to 165), which read the same
tables a different way.

## Change by build

Builds are in link-date order within each line. "Added" and "Removed" compare with the row above. The engine row 3.04 is compared
with 2.31: the engine is a separate code base that started from the 2.x command set, so that row shows what it did not take over,
not a removal in time. 3.04 and 2.22 carry the same build date.

| Build | Line | Date | Commands | Added | Removed |
|---|---|---|---:|---|---|
| 2nd Graal | delphi | 1998-09-16 | 13 | `say`, `setx`, `sety`, `lay`, `take`, `hide`, `hurt`, `set`, `if`, `play`, `show`, `unset`, `setgif` | — |
| 3rd Graal | delphi | 1998-09-30 | 26 | `setplayerx`, `setplayery`, `removecompus`, `setlevel`, `setskincolor`, `setcoatcolor`, `setsleevecolor`, `setshoecolor`, `setbeltcolor`, `reducerupees`, `reducebombs`, `reducedarts`, `setplayerdir` | — |
| 4th Graal | delphi | 1998-10-05 | 26 | same as previous |  |
| 4th Graal alpha | delphi | 1998-10-12 | 28 | `putcomp`, `takeplayercarry` | — |
| 5th Graal | delphi | 1998-10-19 | 28 | same as previous |  |
| 5th Graal alpha | delphi | 1998-10-29 | 33 | `dontblock`, `drawoverplayer`, `enableweapons`, `disableweapons`, `shootarrow`, `putbomb`, `putexplosion`, `putleaps`, `shootball`, `timershow`, `toinventory`, `else` | `setx`, `sety`, `setplayerx`, `setplayery`, `reducerupees`, `reducebombs`, `reducedarts` |
| 6th Graal | delphi | 1998-11-09 | 39 | `followplayer`, `openurl`, `seturllevel`, `stopmidi`, `blockagain`, `drawunderplayer` | — |
| 7th Graal | delphi | 1998-12-04 | 45 | `shootfireball`, `shootfireblast`, `shootnuke`, `puthorse`, `canbecarried`, `cannotbecarried` | — |
| 8th Graal | delphi | 1998-12-08 | 45 | same as previous |  |
| 9th Graal alpha | delphi | 1998-12-16 | 45 | same as previous |  |
| 9th Graal | delphi | 1998-12-18 | 46 | `noplayerkilling` | — |
| 10th Graal 1.0 | delphi | 1998-12-22 | 46 | same as previous |  |
| 11th Graal | delphi | 1998-12-23 | 46 | same as previous |  |
| 12th Graal | delphi | 1999-01-05 | 46 | same as previous |  |
| 13th Graal 1.1b1 | delphi | 1999-01-12 | 50 | `canbepushed`, `cannotbepushed`, `canbepulled`, `cannotbepulled` | — |
| 14th Graal 1.1 | delphi | 1999-01-15 | 51 | `message` | — |
| 15th Graal | delphi | 1999-01-25 | 51 | same as previous |  |
| 1.1.9 | delphi | 1999-02-11 | 51 | same as previous |  |
| 1.1 | delphi | 1999-02-14 | 51 | same as previous |  |
| 1.21 | delphi | 1999-05-10 | 71 | `setsword`, `setshield`, `putnewcomp`, `seteffect`, `unseteffect`, `putnpc`, `destroy`, `freezeplayer`, `sethead`, `toweapons`, `showimg`, `hideimg`, `hidesword`, `for`, `hitcompu`, `hitplayer`, `setbow`, `updateboard`, `putobject`, `setarray` | — |
| 1.25 | delphi | 1999-08-07 | 80 | `sleep`, `while`, `hideplayer`, `timereverywhere`, `setminimap`, `setmap`, `showcharacter`, `setplayerprop`, `setcharprop` | — |
| 1.27 | delphi | 1999-10-23 | 84 | `showfile`, `setstring`, `setbackpal`, `setletters` | — |
| 1.28b2 | delphi | 1999-11-23 | 84 | same as previous |  |
| 1.3 test | delphi | 1999-11-29 | 85 | `setgifpart` | — |
| 1.31 | delphi | 1999-12-07 | 85 | same as previous |  |
| 1.32 | delphi | 2000-01-12 | 85 | same as previous |  |
| 1.33 | delphi | 2000-02-21 | 88 | `setfocus`, `resetfocus`, `setbody` | — |
| 1.34 | delphi | 2000-03-23 | 93 | `dontblocklocal`, `blockagainlocal`, `carryobject`, `throwcarry`, `showlocal`, `hidelocal`, `setbacktile` | `seteffect`, `unseteffect` |
| 1.35 | delphi | 2000-04-13 | 93 | same as previous |  |
| 1.36 | delphi | 2000-05-12 | 104 | `takeplayerhorse`, `removebomb`, `removearrow`, `removeitem`, `removeexplo`, `removehorse`, `explodebomb`, `reflectarrow`, `lay2`, `take2`, `takehorse` | — |
| 1.37 | delphi | 2000-05-23 | 106 | `playlooped`, `stopsound` | — |
| 1.38 | delphi | 2000-06-23 | 109 | `changeimgpart`, `setlevel2`, `hitnpc` | — |
| 1.39 | delphi | 2000-08-07 | 111 | `setani`, `setcharani` | — |
| 1.41r1 | delphi | 2000-11 (token) | 126 | `canwarp`, `callnpc`, `say2`, `break`, `continue`, `callweapon`, `spyfire`, `function`, `return`, `changeimgvis`, `setimg`, `setimgpart`, `drawovertrees`, `putexplosion2`, `showstats` | — |
| NM24 | delphi | 2001-01-10 | 134 | `canwarp2`, `setshape`, `seteffect`, `setcoloreffect`, `setzoomeffect`, `drawaslight`, `changeimgcolors`, `changeimgzoom` | — |
| NM26 | delphi | 2001-01-12 | 134 | same as previous |  |
| 2.0 | delphi | 2001-02-01 | 142 | `setgender`, `setchargender`, `join`, `freezeplayer2`, `unfreezeplayer`, `enabledefmovement`, `disabledefmovement`, `setmusicvolume` | — |
| 2.0r1 | delphi | 2001-02-02 | 142 | same as previous |  |
| 2.0r2 | delphi | 2001-02-05 | 142 | same as previous |  |
| 2.0r3 | delphi | 2001-02-07 | 142 | same as previous |  |
| 2.01 | delphi | 2001-03-08 | 144 | `openurl2`, `hitobjects` | — |
| 2.01r1 | delphi | 2001-03-15 | 144 | same as previous |  |
| 2.02 | delphi | 2001-04-15 | 146 | `tokenize`, `tokenize2` | — |
| 2.02r1 | delphi | 2001-04-15 | 146 | same as previous |  |
| 2.02r2 | delphi | 2001-04-20 | 146 | same as previous |  |
| 2.03 | delphi | 2001-05-07 | 148 | `triggeraction`, `move` | — |
| 2.04 | delphi | 2001-06-25 | 157 | `addtiledef`, `addtiledef2`, `removetiledefs`, `replaceani`, `attachplayertoobj`, `setshape2`, `detachplayer`, `enableselectweapons`, `disableselectweapons` | — |
| 2.05 | delphi | 2001-08-03 | 161 | `setbacktile2`, `setz`, `updateterrain`, `loadmap` | — |
| 2.05r1 | delphi | 2001-08-04 | 161 | same as previous |  |
| NWb1 | delphi | 2001-08-06 | 161 | same as previous |  |
| 2.05r2 | delphi | 2001-08-16 | 161 | same as previous |  |
| 2.1t2 | delphi | 2001-09-21 | 161 | same as previous |  |
| 2.1t3 | delphi | 2001-09-27 | 161 | same as previous |  |
| NWb2 | delphi | 2001-10-03 | 165 | `addstring`, `insertstring`, `removestring`, `deletestring` | — |
| 2.17.1 | delphi | 2002-12 (token) | 198 | `putnpc2`, `showimg2`, `hideimgs`, `play2`, `shoot`, `replacestring`, `savelog2`, `setcursor`, `setcursor2`, `wraptext`, `setshootparams`, `wraptext2`, `serverwarp`, `disablepause`, `enablepause`, `disablemap`, `enablemap`, `seteffectmode`, `changeimgmode`, `with`, `showpoly2`, `showani2`, `showtext2`, `sendtonc`, `sendtorc`, `setpm`, `sendpm`, `sendrpgmessage`, `savelog`, `showpoly`, `showani`, `showtext`, `enablefeatures` | — |
| 2.22 | delphi | 2004-01 (token) | 198 | same as previous |  |
| 2.31 | delphi | 2005-01 (token) | 198 | same as previous |  |
| 3.04 Linux | engine | 2004-01 | 191 | — | `putobject`, `setbackpal`, `setbody`, `setbacktile`, `drawovertrees`, `setbacktile2`, `savelog` |
| 3.153 Mac | engine | 2005-02 | 191 | `savelog` | `with` |
| 4.04r2 Win | engine | 2006-03 | 191 | same as previous |  |
| 4.20r6 Mac | engine | 2006-09 | 191 | same as previous |  |
| 4.20r8 Win | engine | 2007-01 | 191 | same as previous |  |
| 5.00r7 Win | engine | 2007-07 | 193 | `setspritesimage`, `setstatusimage` | — |

What stands out:

- **2nd to 5th Graal (Sept–Oct 1998)** had test commands that move the NPC or the player and take items away: `setx`, `sety`,
  `setplayerx`, `setplayery`, `reducerupees`, `reducebombs`, `reducedarts`. The 5th Graal alpha (29 Oct 1998) drops all seven at
  once and adds the first combat and object commands (`putbomb`, `shootarrow`, `putexplosion`, …) and `else`. None of the seven
  comes back.
- **The 1.0 release (10th Graal, Dec 1998) has 46 commands**, 1.1 has 51. The big steps are 1.21 (+20: `putnpc`, `showimg`, `for`,
  `destroy`, `setarray`, …), 1.25 and 1.27 (+9 and +4: `sleep`, `while`, `showcharacter`, … then `setstring`, `showfile`, …; once credited to 1.28 beta 2, see [`gserv-125-127-builds.md`](../client-internals/gserv-125-127-builds.md)), 1.41 rev1 (+15: `function`,
  `return`, `break`, `continue`, `callnpc`, `say2`, …) and 2.17.1 (+33).
- **`seteffect` and `unseteffect`** are in 1.21 to 1.33 and gone in 1.34 to 1.41 rev1. `seteffect` alone returns in NewMain 1.42;
  `unseteffect` never returns.
- **2.17.1 adds 33**: `putnpc2`, `showimg2`, `hideimgs`, `showpoly`, `showpoly2`, `showani`, `showani2`, `showtext`, `showtext2`,
  `changeimgmode`, `seteffectmode`, `play2`, `shoot`, `setshootparams`, `replacestring`, `savelog`, `savelog2`, `setcursor`,
  `setcursor2`, `wraptext`, `wraptext2`, `serverwarp`, `enablepause`, `disablepause`, `enablemap`, `disablemap`, `sendtonc`,
  `sendtorc`, `setpm`, `sendpm`, `sendrpgmessage`, `enablefeatures`, `with`. No client between the 2.1 tests (Sept 2001) and
  2.17.1 (Dec 2002) is in the set, so these can only be dated to "after 2.1 test 3, by 2.17.1". The 2.1x release notes are the
  only finer source.
- **2.17.1, 2.22 and 2.31 have the same 198 commands.** The Windows 2.x command list did not change from Dec 2002 to Jan 2005.
- **The C++ engine (3.04, Jan 2004) does not have** `putobject`, `setbackpal`, `setbody`, `setbacktile`, `setbacktile2` or
  `drawovertrees`. None of them appears in any engine build up to 5.00r7, not even as a string.
- **`savelog` is missing in 3.04** because 3.04 registers `savelog2` twice, the second time where 3.153 and later register
  `savelog`. It looks like a copy-and-paste slip that 3.153 fixed. **[inf]**
- **`with`** is registered by 3.04 and by no later engine. In 4.04r2 the only `with` string belongs to the GS2 compiler (next to
  `popwith`), not to GS1.
- **3.153 Mac to 4.20r8 Win have the same 191 commands**, on PowerPC and on x86, which also cross-checks the two scanner modes.
- **5.00r7 adds `setspritesimage` and `setstatusimage`** (193 commands).

## Every command

"from X" means present from X to the last build of that line; "all" means every build of the line. Both lines are listed because
the engine is a separate code base.

| Command | Windows 2.x line (2nd Graal → 2.31) | C++ engine (3.04 → 5.00r7) |
|---|---|---|
| `addstring` | from NWb2 | all |
| `addtiledef` | from 2.04 | all |
| `addtiledef2` | from 2.04 | all |
| `attachplayertoobj` | from 2.04 | all |
| `blockagain` | from 6th Graal | all |
| `blockagainlocal` | from 1.34 | all |
| `break` | from 1.41r1 | all |
| `callnpc` | from 1.41r1 | all |
| `callweapon` | from 1.41r1 | all |
| `canbecarried` | from 7th Graal | all |
| `canbepulled` | from 13th Graal 1.1b1 | all |
| `canbepushed` | from 13th Graal 1.1b1 | all |
| `cannotbecarried` | from 7th Graal | all |
| `cannotbepulled` | from 13th Graal 1.1b1 | all |
| `cannotbepushed` | from 13th Graal 1.1b1 | all |
| `canwarp` | from 1.41r1 | all |
| `canwarp2` | from NM24 | all |
| `carryobject` | from 1.34 | all |
| `changeimgcolors` | from NM24 | all |
| `changeimgmode` | from 2.17.1 | all |
| `changeimgpart` | from 1.38 | all |
| `changeimgvis` | from 1.41r1 | all |
| `changeimgzoom` | from NM24 | all |
| `continue` | from 1.41r1 | all |
| `deletestring` | from NWb2 | all |
| `destroy` | from 1.21 | all |
| `detachplayer` | from 2.04 | all |
| `disabledefmovement` | from 2.0 | all |
| `disablemap` | from 2.17.1 | all |
| `disablepause` | from 2.17.1 | all |
| `disableselectweapons` | from 2.04 | all |
| `disableweapons` | from 5th Graal alpha | all |
| `dontblock` | from 5th Graal alpha | all |
| `dontblocklocal` | from 1.34 | all |
| `drawaslight` | from NM24 | all |
| `drawoverplayer` | from 5th Graal alpha | all |
| `drawovertrees` | from 1.41r1 | — |
| `drawunderplayer` | from 6th Graal | all |
| `else` | from 5th Graal alpha | all |
| `enabledefmovement` | from 2.0 | all |
| `enablefeatures` | from 2.17.1 | all |
| `enablemap` | from 2.17.1 | all |
| `enablepause` | from 2.17.1 | all |
| `enableselectweapons` | from 2.04 | all |
| `enableweapons` | from 5th Graal alpha | all |
| `explodebomb` | from 1.36 | all |
| `followplayer` | from 6th Graal | all |
| `for` | from 1.21 | all |
| `freezeplayer` | from 1.21 | all |
| `freezeplayer2` | from 2.0 | all |
| `function` | from 1.41r1 | all |
| `hide` | all | all |
| `hideimg` | from 1.21 | all |
| `hideimgs` | from 2.17.1 | all |
| `hidelocal` | from 1.34 | all |
| `hideplayer` | from 1.25 | all |
| `hidesword` | from 1.21 | all |
| `hitcompu` | from 1.21 | all |
| `hitnpc` | from 1.38 | all |
| `hitobjects` | from 2.01 | all |
| `hitplayer` | from 1.21 | all |
| `hurt` | all | all |
| `if` | all | all |
| `insertstring` | from NWb2 | all |
| `join` | from 2.0 | all |
| `lay` | all | all |
| `lay2` | from 1.36 | all |
| `loadmap` | from 2.05 | all |
| `message` | from 14th Graal 1.1 | all |
| `move` | from 2.03 | all |
| `noplayerkilling` | from 9th Graal | all |
| `openurl` | from 6th Graal | all |
| `openurl2` | from 2.01 | all |
| `play` | all | all |
| `play2` | from 2.17.1 | all |
| `playlooped` | from 1.37 | all |
| `putbomb` | from 5th Graal alpha | all |
| `putcomp` | from 4th Graal alpha | all |
| `putexplosion` | from 5th Graal alpha | all |
| `putexplosion2` | from 1.41r1 | all |
| `puthorse` | from 7th Graal | all |
| `putleaps` | from 5th Graal alpha | all |
| `putnewcomp` | from 1.21 | all |
| `putnpc` | from 1.21 | all |
| `putnpc2` | from 2.17.1 | all |
| `putobject` | from 1.21 | — |
| `reducebombs` | 3rd Graal to 5th Graal | — |
| `reducedarts` | 3rd Graal to 5th Graal | — |
| `reducerupees` | 3rd Graal to 5th Graal | — |
| `reflectarrow` | from 1.36 | all |
| `removearrow` | from 1.36 | all |
| `removebomb` | from 1.36 | all |
| `removecompus` | from 3rd Graal | all |
| `removeexplo` | from 1.36 | all |
| `removehorse` | from 1.36 | all |
| `removeitem` | from 1.36 | all |
| `removestring` | from NWb2 | all |
| `removetiledefs` | from 2.04 | all |
| `replaceani` | from 2.04 | all |
| `replacestring` | from 2.17.1 | all |
| `resetfocus` | from 1.33 | all |
| `return` | from 1.41r1 | all |
| `savelog` | from 2.17.1 | from 3.153 Mac |
| `savelog2` | from 2.17.1 | all |
| `say` | all | all |
| `say2` | from 1.41r1 | all |
| `sendpm` | from 2.17.1 | all |
| `sendrpgmessage` | from 2.17.1 | all |
| `sendtonc` | from 2.17.1 | all |
| `sendtorc` | from 2.17.1 | all |
| `serverwarp` | from 2.17.1 | all |
| `set` | all | all |
| `setani` | from 1.39 | all |
| `setarray` | from 1.21 | all |
| `setbackpal` | from 1.27 | — |
| `setbacktile` | from 1.34 | — |
| `setbacktile2` | from 2.05 | — |
| `setbeltcolor` | from 3rd Graal | all |
| `setbody` | from 1.33 | — |
| `setbow` | from 1.21 | all |
| `setcharani` | from 1.39 | all |
| `setchargender` | from 2.0 | all |
| `setcharprop` | from 1.25 | all |
| `setcoatcolor` | from 3rd Graal | all |
| `setcoloreffect` | from NM24 | all |
| `setcursor` | from 2.17.1 | all |
| `setcursor2` | from 2.17.1 | all |
| `seteffect` | 1.21 to 1.33; from NM24 | all |
| `seteffectmode` | from 2.17.1 | all |
| `setfocus` | from 1.33 | all |
| `setgender` | from 2.0 | all |
| `setgif` | all | all |
| `setgifpart` | from 1.3 test | all |
| `sethead` | from 1.21 | all |
| `setimg` | from 1.41r1 | all |
| `setimgpart` | from 1.41r1 | all |
| `setletters` | from 1.27 | all |
| `setlevel` | from 3rd Graal | all |
| `setlevel2` | from 1.38 | all |
| `setmap` | from 1.25 | all |
| `setminimap` | from 1.25 | all |
| `setmusicvolume` | from 2.0 | all |
| `setplayerdir` | from 3rd Graal | all |
| `setplayerprop` | from 1.25 | all |
| `setplayerx` | 3rd Graal to 5th Graal | — |
| `setplayery` | 3rd Graal to 5th Graal | — |
| `setpm` | from 2.17.1 | all |
| `setshape` | from NM24 | all |
| `setshape2` | from 2.04 | all |
| `setshield` | from 1.21 | all |
| `setshoecolor` | from 3rd Graal | all |
| `setshootparams` | from 2.17.1 | all |
| `setskincolor` | from 3rd Graal | all |
| `setsleevecolor` | from 3rd Graal | all |
| `setspritesimage` | — | from 5.00r7 Win |
| `setstatusimage` | — | from 5.00r7 Win |
| `setstring` | from 1.27 | all |
| `setsword` | from 1.21 | all |
| `seturllevel` | from 6th Graal | all |
| `setx` | 2nd Graal to 5th Graal | — |
| `sety` | 2nd Graal to 5th Graal | — |
| `setz` | from 2.05 | all |
| `setzoomeffect` | from NM24 | all |
| `shoot` | from 2.17.1 | all |
| `shootarrow` | from 5th Graal alpha | all |
| `shootball` | from 5th Graal alpha | all |
| `shootfireball` | from 7th Graal | all |
| `shootfireblast` | from 7th Graal | all |
| `shootnuke` | from 7th Graal | all |
| `show` | all | all |
| `showani` | from 2.17.1 | all |
| `showani2` | from 2.17.1 | all |
| `showcharacter` | from 1.25 | all |
| `showfile` | from 1.27 | all |
| `showimg` | from 1.21 | all |
| `showimg2` | from 2.17.1 | all |
| `showlocal` | from 1.34 | all |
| `showpoly` | from 2.17.1 | all |
| `showpoly2` | from 2.17.1 | all |
| `showstats` | from 1.41r1 | all |
| `showtext` | from 2.17.1 | all |
| `showtext2` | from 2.17.1 | all |
| `sleep` | from 1.25 | all |
| `spyfire` | from 1.41r1 | all |
| `stopmidi` | from 6th Graal | all |
| `stopsound` | from 1.37 | all |
| `take` | all | all |
| `take2` | from 1.36 | all |
| `takehorse` | from 1.36 | all |
| `takeplayercarry` | from 4th Graal alpha | all |
| `takeplayerhorse` | from 1.36 | all |
| `throwcarry` | from 1.34 | all |
| `timereverywhere` | from 1.25 | all |
| `timershow` | from 5th Graal alpha | all |
| `toinventory` | from 5th Graal alpha | all |
| `tokenize` | from 2.02 | all |
| `tokenize2` | from 2.02 | all |
| `toweapons` | from 1.21 | all |
| `triggeraction` | from 2.03 | all |
| `unfreezeplayer` | from 2.0 | all |
| `unset` | all | all |
| `unseteffect` | 1.21 to 1.33 | — |
| `updateboard` | from 1.21 | all |
| `updateterrain` | from 2.05 | all |
| `while` | from 1.25 | all |
| `with` | from 2.17.1 | 3.04 Linux only |
| `wraptext` | from 2.17.1 | all |
| `wraptext2` | from 2.17.1 | all |

## Sources

Every build was scanned from the binary below. The MD5 is of the scanned file; for the Delphi builds it matches
`client-internals/build-catalogue.md`. Upload names are as given when they were uploaded to the project.

| Build | Scanned binary | MD5 | Mode |
|---|---|---|---|
| 2nd Graal | "graal clients.zip" / 2ndgraal.7z: the client exe | `f74b35fc7975a4873087f7fd2aa1d79b` | table |
| 3rd Graal | "graal clients.zip" / 3rdgraal.7z: the client exe | `fc78fbc96bdbc6ca22ae56d3ed8635ab` | table |
| 4th Graal | "graal clients.zip" / 4thgraal.7z: the client exe | `e040af2e19912419ab80aa6dd202b4ea` | table |
| 4th Graal alpha | "graal clients.zip" / 4thgraalalpha.7z: the client exe | `8cae23a58e1b1b10f3149bdbe53d0431` | table |
| 5th Graal | "graal clients.zip" / 5thgraal.7z: the client exe | `0e7c3573f0a916f8b2376060e768fe96` | table |
| 5th Graal alpha | "graal clients.zip" / 5thgraalalpha.7z: the client exe | `e54397e7d4f59d30b77d5cf0475335a1` | table |
| 6th Graal | "graal clients.zip" / 6thgraal.7z: the client exe | `53c3caf3d930534db3f44f346f5d651a` | table |
| 7th Graal | "graal clients.zip" / 7thgraal.7z: the client exe | `deb40c31268e499fc4436b8d0687f05d` | table |
| 8th Graal | "graal clients.zip" / 8thgraal.7z: the client exe | `a49aa1b773e41741f211867fd5ea55d7` | table |
| 9th Graal alpha | "graal clients.zip" / 9thgraalalpha.7z: the client exe | `e226e1b83fd437b0aede968fb395b911` | table |
| 9th Graal | "graal clients.zip" / 9thgraal.7z: the client exe | `f0185ff8525a13f2f4e5997f649bc250` | table |
| 10th Graal 1.0 | "graal clients.zip" / 10thgraal.7z: the client exe | `f1f34b4479a8ad7614bd8f7ce56112c6` | table |
| 11th Graal | "graal clients.zip" / 11thgraal.7z: the client exe | `a255212621907affc94a4483c6dfc8e3` | table |
| 12th Graal | "graal clients.zip" / 12thgraal.7z: the client exe | `788ae59e9419806024d14d3e5b611971` | table |
| 13th Graal 1.1b1 | "graal clients.zip" / 13thgraal.7z: the client exe | `a211a0ecf3b58daa2f46759444e18bd3` | table |
| 14th Graal 1.1 | "graal clients.zip" / 14thgraal.7z: the client exe | `d0999d44fcd9c226f350fcf204618885` | table |
| 15th Graal | "graal clients.zip" / 15thgraal.7z: the client exe | `9a7d66dd5c8c506ad4d3e63ee4a9a1f1` | table |
| 1.1.9 | "graal clients.zip" / graal1.1.9.7z: the client exe | `0a6eef88acb4c0fce6e84eee3e76c04a` | table |
| 1.1 | "graal clients.zip" / graal1.1.7z: the client exe | `1a9580655cce686c602c01daa251c453` | table |
| 1.21 | graal121.7z: Graal.exe from the InstallShield package (archive-survey/graal121-unpacked) | `8da2e8284dd8b315a28e2d4fccae79ac` | table |
| 1.28b2 | "graal clients.zip" / graal128b2.7z: the client exe | `8e3c1a7233864da994a0db26f1811212` | table |
| 1.3 test | "graal clients.zip" / graal13b.7z: the client exe | `b62aaa4d606a519e7f4689b33983429b` | table |
| 1.31 | "graal clients.zip" / graal131.7z: the client exe | `bff87a95a34399b2d35b243f281169a7` | table |
| 1.32 | "graal clients.zip" / graal132.7z: the client exe | `42b2596af4b75bcf82db03e0fc274f7d` | table |
| 1.33 | "graal clients.zip" / graal133.7z: the client exe | `a3667ce55a5c67cf025882014b9540b0` | table |
| 1.34 | "graal clients.zip" / graal134.7z: the client exe | `9e403616e73a6079ac37d65d475c81cd` | table |
| 1.35 | "graal clients.zip" / graal135.7z: the client exe | `fe9d99c4bf6e6bc9b1b127823f39646f` | table |
| 1.36 | "graal clients.zip" / graal136.7z: the client exe | `018f51662c7c8862cafb9bfbd14dea41` | table |
| 1.37 | "graal clients.zip" / graal137.7z: the client exe | `5e966a9d1a079af6d682b2618674edb1` | table |
| 1.38 | "graal clients.zip" / graal138.7z: the client exe | `4401f7d02966af709c2df662cebe34a1` | table |
| 1.39 | "graal clients.zip" / graal139.7z: the client exe | `62513ab884f1802a0bcd8114abe349b9` | table |
| 1.41r1 | "graal clients.zip" / graal_gr1411.7z: the client exe | `a97740e711ffe9b698ec03712d4c06af` | table |
| NM24 | "graal clients.zip" / graalnm24.7z: the client exe | `229f05de7a43b98e223d8e1b58bffc63` | table |
| NM26 | "graal clients.zip" / graalnm26.7z: the client exe | `22a08ed154f67948e01b969b68cdb05e` | table |
| 2.0 | "graal clients.zip" / Graal-v2.0.7z: the client exe | `c93e659e2cda36379aaea4706db20b38` | table |
| 2.0r1 | "graal clients.zip" / Graal-v2.0-rev1.7z: the client exe | `30bd230e578d3a347866a87060efec20` | table |
| 2.0r2 | "graal clients.zip" / Graal-v2.0-rev2.7z: the client exe | `fc4bb7e3b7ca9cd8ea6693a033635534` | table |
| 2.0r3 | "graal clients.zip" / Graal-v2.0-rev3.7z: the client exe | `1ce5c1662b65246ae1c6559af5ff71f0` | table |
| 2.01 | "graal clients.zip" / Graal-v2.01.7z: the client exe | `08340a8868f1d11e0285cc70e51200fe` | table |
| 2.01r1 | "graal clients.zip" / Graal-v2.01-rev1.7z: the client exe | `010a32afce66729b838258809a97c0d9` | table |
| 2.02 | "graal clients.zip" / Graal-v2.02.7z: the client exe | `60018a19ef671c506743826728c49718` | table |
| 2.02r1 | "graal clients.zip" / Graal-v2.02-rev1.7z: the client exe | `e06ff79aded885a223b933617d456577` | table |
| 2.02r2 | "graal clients.zip" / Graal-v2.02-rev2.7z: the client exe | `993a1829dbb6acaa2b46063f5efe636c` | table |
| 2.03 | "graal clients.zip" / Graal-v2.03.7z: the client exe | `36972c74baad09ceb33dad94b0eb1e33` | table |
| 2.04 | "graal clients.zip" / Graal-v2.04.7z: the client exe | `a40608308d4f890cb5e4efdd45b38ba4` | table |
| 2.05 | "graal clients.zip" / Graal-v2.05.7z: the client exe | `9abce477945a1307bb2be9ed47d2f170` | table |
| 2.05r1 | "graal clients.zip" / Graal-v2.05-rev1.7z: the client exe | `2780f2f370396c580e1648696698c871` | table |
| NWb1 | "graal clients.zip" / graalnwb1.7z: the client exe | `88d1f84c96da1dcc3942b139fbd741c9` | table |
| 2.05r2 | "graal clients.zip" / Graal-v2.05-rev2.7z: the client exe | `f3fdf54d943fa91c89acba5bb695db99` | table |
| 2.1t2 | "graal clients.zip" / graal21test2.7z: the client exe | `d15d877822ad4145578107857c90fb3c` | table |
| 2.1t3 | "graal clients.zip" / graal21test3.7z: the client exe | `2116a7ba03648dcc004035534ec94de8` | table |
| NWb2 | "graal clients.zip" / graalnwb2.7z: the client exe | `af2d21066659bed6af6c77e52b2cc0e1` | table |
| 2.17.1 | Drive "Graal Reborn 2.22.0" folder: Graal_2171.exe | `0fbef4078da9be6e7fb3969a08c93c5a` | init |
| 2.22 | Drive "Graal Reborn 2.22.0" folder: Graal_222.exe | `bc341f16a17202320b2d5990b6c19bdc` | init |
| 2.31 | Drive "Graal Reborn 2.22.0" folder: Graal_231.exe | `c6a0fad0593462758c2426dee2ae1391` | init |
| 3.04 Linux | upload "Graal v3.04 Linux Fixed.tgz": graalexe after upx -d | `ded1bf1b7d6502f51576b7736c62a814` | x86 |
| 3.153 Mac | upload "Graal v3.15r2 Mac OS X.dmg.gz": Graal.app/Contents/MacOS/Graal | `3930f6630c335c976f6fd032f7a7db4e` | ppc |
| 4.04r2 Win | upload "Graal4Setup.exe" 4.04r2, Thinstall-unpacked: GraalEngine.dll | `fb7d4147723efae1957757b90bca5c80` | x86 |
| 4.20r6 Mac | upload Mac OS X 4.20r6 disk image: Graal.app/Contents/MacOS/Graal | `7028bfd614db7cb0eabdd09f5a9b4b81` | ppc |
| 4.20r8 Win | upload 4.20r8 "Packet Logger v2": GraalEngine.dll (third-party hook, see protocol/v4x-clients.md) | `f7212a4f3b0f0fc271e3e636b7036ffc` | x86 |
| 5.00r7 Win | upload 5.00r7 "Unpacked CRC Patch": GraalEngine.dll.bak (the unpatched original) | `3f8fca95e1c1ab1c060aaf618038886d` | x86 |

The 4.20r8 engine was modified by a third party (a packet-logger hook, see `protocol/v4x-clients.md`). Its command list is the
same as the stock 4.20r6 Mac build. For 5.00r7 the scan used `GraalEngine.dll.bak`, the original before the CRC patch; the patched
DLL differs only in the licence check (`protocol/v5x-clients.md`).

## Not covered

- Builds that are not in the project files: 1.4 (only the patched 1.41 rev1 copy exists), 2.1 to 2.16, 2.3, Windows 3.x, other 4.0x
  builds, and anything between 4.20r8 and 5.00r7.
- Builds after 5.00r7 (5.12 onwards). The question stopped at 5.007. The 5.1 release notes (17 September 2007) say GS1 was removed from the client and GS2 is always used, so 5.12 and later should have no GS1 command table; this is an expectation from the notes, not a read (`client-internals/graal-wiki-crosscheck-2026-11-11.md`). **[doc]**
- Executors: whether each listed command does something in that build. Only 2.05 has that, in
  [gs1-command-reference-205.md](gs1-command-reference-205.md).
- Functions, flags and variables by version. The `init`, `x86` and `ppc` registration runs contain them right after the commands,
  so the same scanner can chart them with a different cut.
