# GS1 command reference (client 2.05 rev 2)

Date: 2026-10-21

What each GS1 command does in the 2.05 rev 2 client, read from the client's script compiler and command executor. Cross-checked against
`npcprogramming.doc` (2000) and the `newfeatures*.txt` change logs shipped with Graal Reborn 2.22. Where the client and the docs disagree,
the client wins and the row says so. **[inf]** marks a reading that is not fully pinned down.

This replaces the guesses in [gs1-commands.md](gs1-commands.md) for 2.05. That file's pattern-letter list and its `warp` / `jump` rows
were wrong; see "Corrections" at the end.

## How the interpreter works

- Scripts are compiled once, on level load, into a flat list of statement nodes. Each node holds a command number, up to two string
  arguments, up to eight numeric expression arguments, a jump target, and a pre-resolved name index (item, baddy, colour, etc.).
- Command numbers are **600 + table index** in the GS1 numbering. The 2.05 table has **161** commands (index 0..160, opcodes 600..760).
  Earlier dumps listed 163 because they ran into the next table in memory, the direction names `up`, `left`, `down`, `right`.
- Each command has an argument signature. The compiler uses it to parse and to build the "usage" text in error messages:

  | Letter | Compiler's label | Accepts |
  |---|---|---|
  | `R` | number | any numeric expression |
  | `M`, `S` | string | raw text, message codes expanded at run time |
  | `F`, `Q` | filename | file name; offline, the compiler rejects a missing file unless it starts with `http://`. `Q` names a script file |
  | `I` | itemname | one of 25 item names (table below) |
  | `B` | baddyname | one of 10 baddy names |
  | `C` | colorname | one of 20 colour names, or a number |
  | `D` | direction | `up` `left` `down` `right` (0..3), or a numeric expression |
  | `L` | carry objectname | one of 11 carry objects |
  | `O` | objectname | an entry from the editor's predefined tile-objects list |

- Every event runs the whole node list from the top. `if` evaluates its expression and jumps past its block when it is 0. `else`,
  `function` and the closing braces never reach the executor: the compiler turns them into four internal node kinds:
  assignment / expression statement, unconditional jump, function call, and end of function body.
- Loops (`for`, `while`) count passes and stop after **10,000**, as the doc says. Function calls push a return point and stop
  nesting at **10,000** deep. A `return` (or the end of a function body) with an empty call stack ends the script.
- Several commands **end the current script run** after they execute: `setlevel`, `setlevel2`, `destroy`, `sleep` (non-zero),
  `toinventory` (offline), `hide` on an NPC that is following the player, and `break` / `continue` outside a loop.
- String arguments are trimmed and message codes (`#c`, `#v(...)`, ...) are expanded before use, for almost every command.
- **Weapon NPCs act as the player.** When the running NPC is one of the player's weapons, commands that spawn things (bombs,
  explosions, horses, projectiles, `showimg` layers, `hitobjects`, `triggeraction`, `reflectarrow`) use the player's level and count
  the player as the source, not the NPC.
- **Online gates.** Several visual commands run only offline, or online when the server announced that it has an NPC server
  (server packet 44): `seteffect`, `setcoloreffect`, `setzoomeffect`, `changeimgcolors`, `changeimgzoom`, `addtiledef`,
  `addtiledef2`, `removetiledefs`, `replaceani`, `attachplayertoobj`. Online without an NPC server they do nothing.
- **Editor preview mode.** When the in-game editor builds a preview copy of a `showcharacter` NPC, it runs that NPC's
  `playerenters` in a restricted mode. Only `if`, `else`, `for`, `while`, `setgif`, `setgifpart`, `setimg`, `setimgpart`,
  `setmap`, `showcharacter`, `setcharprop`, `setcharani`, `setbackpal`, `setbacktile`, `setbacktile2`, `addtiledef`,
  `addtiledef2`, `setz`, `loadmap`, function calls, and `++`/`--` style assignments run. Everything else is skipped. **[inf: the
  trigger is the editor-copy path; exact UI action not traced]**

## Name tables

- **Items** (`I`, index 0..24): greenrupee, bluerupee, redrupee, bombs, darts, heart, glove1, bow, bomb, shield, sword,
  fullheart, superbomb, battleaxe, goldensword, mirrorshield, glove2, lizardshield, lizardsword, goldrupee, fireball,
  fireblast, nukeshot, joltbomb, spinattack.
- **Baddies** (`B`, 0..9): graysoldier, bluesoldier, redsoldier, shootingsoldier, swampsoldier, frog, octopus, goldenwarrior,
  lizardon, dragon.
- **Colours** (`C`, 0..19): white, yellow, orange, pink, red, darkred, lightgreen, green, darkgreen, lightblue, blue, darkblue,
  brown, cynober, purple, darkpurple, lightgray, gray, black, transparent.
- **Carry objects** (`L`, 0..10): bush, sign, vase, stone, blackstone, bomb, hotbomb, superbomb, joltbomb, hotjoltbomb, none.
- **Directions** (`D`): up 0, left 1, down 2, right 3. Numeric values are reduced mod 4 (negative values too).

## Online side effects

When connected, some commands also tell the server or nearby peers. TCP ids are PLI numbers from
[protocol/packet-ids.md](../protocol/packet-ids.md); UDP ids are the peer-to-peer ids from [protocol/udp-p2p.md](../protocol/udp-p2p.md).

| Command | TCP (PLI) | UDP |
|---|---|---|
| `take`, `take2`, `removeitem` | 13 ITEMDEL | 20 item del |
| `putcomp`, `putnewcomp` | 17 BADDYADD (instead of spawning locally) | |
| `putnpc` | 21 PUTNPC (instead of creating locally) | |
| `destroy` | 29 NPCWEAPONDEL if the NPC is also a weapon, then 22 NPCDEL | |
| `toweapons` | 33 WEAPONADD | |
| `hitcompu` | 16 BADDYHURT | |
| `hitplayer` (remote player) | | 21 remote hit, to the victim only |
| `putexplosion`, `putexplosion2` | 27 EXPLOSION | 14 explosion |
| `spyfire` | 10 FIRESPY | 13 fire spy |
| `hitobjects` | 36 HITOBJECTS | 25 hit objects |
| `triggeraction` | 38 TRIGGERACTION | 26 trigger action |
| `removebomb` | | 11 bomb del |
| `removehorse`, `takehorse` | | 17 horse del |
| `reflectarrow` | | 12 arrow (re-sent with the new direction) |
| `setplayerprop #c,...` | chat prop | 22 chat |

Plain TCP routing also applies: a level-local action goes over UDP only when every other player in the level has a UDP port,
otherwise over both (see udp-p2p.md).

## Commands

"Doc" means npcprogramming.doc or the newfeatures logs. Positions are in tiles unless noted.

### Messages, signs, sound, files

| Op | Command | Args | What 2.05 does |
|---|---|---|---|
| 600 | `say` | R | Shows sign *n* of the current level (index into the level's sign list). Skipped if the index is out of range or the player is already in the sign-reading state. Puts the player into the reading state. |
| 711 | `say2` | S | Same as `say`, but shows the given text directly instead of a level sign. |
| 648 | `message` | S | Sets the text drawn above the NPC. An empty string clears it. Also turns off `timershow`. |
| 606 | `play` | F | Plays a sound positioned at the NPC's centre. Online, a file that is not found locally is requested by its raw name. Doc: midis loop. |
| 702 | `playlooped` | F | Same, but the file is queued as a looped sound (internally the name gets a `+` prefix). Stops on level exit or `stopsound`. |
| 703 | `stopsound` | F | Stops that (looped) sound. |
| 637 | `stopmidi` | – | Stops the current midi. |
| 739 | `setmusicvolume` | R,R | Sets music volume, left and right (doc: 0..1). |
| 635 | `openurl` | M | Opens the URL in the system browser (doc: with a confirm dialog, no `http://` needed). |
| 740 | `openurl2` | M,R,R | Opens the URL in the client's own HTML window of the given width and height. |
| 676 | `showfile` | F | Opens the file with its associated program, like a double-click. |
| 678 | `setbackpal` | F | Copies the 256-colour palette of the given image into the tileset and into every loaded level's tile image, then repaints. Remembers the file so the same palette is not reloaded. |
| 679 | `setletters` | F | Replaces the sign font image (default `letters.png`) if the file exists. |

### Flags and variables

| Op | Command | Args | What 2.05 does |
|---|---|---|---|
| 604 | `set` | M | Sets a flag (doc: `server.` prefix makes it server-wide). |
| 607 | `unset` | M | Clears a flag. |
| 677 | `setstring` | S,S | Sets string variable *name* = *value* (stored as the flag `name=value`). Empty value deletes it. |
| 666 | `setarray` | R,R | Resizes the array variable named by the first argument to *n* elements. Ignored unless the first argument is a plain or `this.` variable. |
| 742 | `tokenize` | S | Splits the expanded string into the global token list on spaces and commas (quotes group). |
| 743 | `tokenize2` | S,S | Same, with extra delimiter characters added to the space/comma set. |

### Control flow

| Op | Command | Args | What 2.05 does |
|---|---|---|---|
| 605 | `if` | – | Evaluates the condition; jumps past the block when it is 0. |
| 634 | `else` | – | Compiled away into a jump. |
| 660 | `for` | – | Loop; condition checked each pass; stops after 10,000 passes. |
| 668 | `while` | – | Same loop node as `for`. |
| 667 | `sleep` | R | Sets the NPC's timeout to the value and remembers the next statement; the next `timeout` event resumes there. `sleep 0` just clears the timer display. Ends the current run. |
| 712 | `break` | – | Jumps to the end of the enclosing loop. Outside a loop it ends the script. |
| 713 | `continue` | – | Jumps to the loop's next pass. Outside a loop it ends the script. |
| 716 | `function` | – | Compiled away. Calls to a named function become a call node (max depth 10,000). |
| 717 | `return` | – | Pops the call stack and resumes after the call. With an empty stack it ends the script. |
| 710 | `callnpc` | R,S | Runs NPC *index*'s script with the given event flag set. Doc: params after the event are passed as `#p(n)`. |
| 714 | `callweapon` | R,S | Moves weapon *index* to the player's centre, then runs its script with the given event flag set. |
| 744 | `triggeraction` | R,R,S,S | Fires *action* with *params* at the object on (x, y) locally, and sends it online. From a weapon, the sender is the player. |

### NPC appearance and behaviour

| Op | Command | Args | What 2.05 does |
|---|---|---|---|
| 608 / 719 | `setgif` / `setimg` | F | Sets the NPC image, shows the NPC, and resets the visible part to the whole image. |
| 680 / 720 | `setgifpart` / `setimgpart` | F,R,R,R,R | Same, then shows only (x, y, w, h) of the image in pixels. x, y are clamped to 0..16000 and w, h to 0..220, then trimmed to the image size. |
| 759 | `show` | – | Shows the NPC (re-applies its image). |
| 686 | `showlocal` | – | Same, but marked local (not synced). |
| 760 | `hide` | – | Hides the NPC (only if it is in the current level). If it was following the player, it stops following and the run ends. |
| 687 | `hidelocal` | – | Same, marked local. |
| 688 | `dontblock` | – | Player can walk through the NPC. |
| 619 | `dontblocklocal` | – | Same, local only. |
| 689 | `blockagain` | – | Blocks again and also resets the draw layer to normal (undoes `drawoverplayer`/`drawunderplayer`). |
| 638 | `blockagainlocal` | – | Same, local only. |
| 620 | `drawoverplayer` | – | Draw layer +1. |
| 639 | `drawunderplayer` | – | Draw layer −1. |
| 729 | `drawaslight` | – | Draw layer 9: above the day/night effect, below the status bar. |
| 641 / 642 | `canbecarried` / `cannotbecarried` | – | Player can / cannot lift the NPC. |
| 644 / 645 | `canbepushed` / `cannotbepushed` | – | Player can / cannot push it. |
| 646 / 647 | `canbepulled` / `cannotbepulled` | – | Player can / cannot pull it. |
| 631 | `timershow` | – | Draws the NPC's timeout counter over it. Cleared by `message` and `sleep 0`. |
| 670 | `timereverywhere` | – | This client gets the NPC's timeout events even when it is not the level leader. |
| 725 | `setshape` | R,R,R | Type 0 or 1 (1 = fixed rectangle), width and height in pixels. Other types are ignored. |
| 751 | `setshape2` | R,R,R | Makes the NPC block like a small level: width and height in tiles, plus a tile-type array (literal or array variable) of w×h entries. A short or missing array clears the shape. |
| 726 | `seteffect` | R,R,R,R | Global screen tint r, g, b, a (day/night). Online gate applies. |
| 727 | `setcoloreffect` | R,R,R,R | Per-NPC colour multiply r, g, b, a. Online gate applies. |
| 728 | `setzoomeffect` | R | Per-NPC zoom factor. Online gate applies. |
| 745 | `move` | R,R,R,R | Smoothly moves the NPC by dx, dy over *time* seconds with option bits. **[inf: option bits not decoded]** |
| 653 | `destroy` | – | Removes the NPC from the level (and from the weapon list), sends the deletes online, ends the run. |
| 652 | `putnpc` | Q,Q,R,R | Offline: creates a new NPC with that image and script file at (x, y) and runs its `playerenters`. Online: asks the server instead. |

### Character NPCs (`showcharacter`)

| Op | Command | Args | What 2.05 does |
|---|---|---|---|
| 673 | `showcharacter` | – | Draws the NPC as a player character (once; later calls do nothing). |
| 675 | `setcharprop` | M,M | Sets a character property from a message code: `#1` sword image, `#2` shield image, `#3` head image, `#5` horse image (creates the horse if needed), `#8` body image, `#C0`..`#C5` colours (name or number), `#P1`..`#P5` attributes, `#c` chat text (not in preview mode), `#n` nickname. Other codes are ignored. |
| 709 | `setcharani` | S,S | Sets the character's gani and its parameter string. |
| 733 | `setchargender` | S | `male` sets male; anything else sets female. |
| 684 | `carryobject` | L | Character carries the object (0..10; `none` = 10). Only for `showcharacter` NPCs; switches to the carry gani. |
| 685 | `throwcarry` | – | Throws the carried object if the character is in a carry sprite; bombs become live bombs. |
| 701 | `takehorse` | R | Character mounts horse *index* (removes it from the level). Only for `showcharacter` NPCs. |
| 633 | `followplayer` | – | Offline only: NPC follows the player and stops blocking. Ignored online (matches the doc). |

### The player

| Op | Command | Args | What 2.05 does |
|---|---|---|---|
| 610 | `setlevel` | M | Warps the player to that level at the current x, y. Ends the run. |
| 705 | `setlevel2` | M,R,R | Warps to that level at (x, y). Ends the run. |
| 655 | `sethead` | F | Player head image. |
| 683 | `setbody` | F | Player body image (skipped if it is the same file). |
| 649 | `setsword` | M,R | Sword image and power. |
| 650 | `setshield` | M,R | Shield image and power. |
| 663 | `setbow` | S | Sets the bow image on the running NPC's character, not on the player. **[differs from doc, which says the player's bow]** |
| 616 | `setplayerdir` | D | Player direction, reduced mod 4. Accepts a name or an expression (doc says names only). |
| 611..615 | `setskincolor`, `setcoatcolor`, `setsleevecolor`, `setshoecolor`, `setbeltcolor` | C | Player colour slots 0..4. |
| 674 | `setplayerprop` | M,M | Same codes as `setcharprop` but on the player: `#1 #2 #3 #5 #8 #C0..#C5 #P1..#P5 #c`. `#c` sets the chat text with a 60-tick timeout and sends it online. `#7` is **not** handled (doc lists it). |
| 708 | `setani` | S,S | Player gani and parameter string. |
| 749 | `replaceani` | S,S | Replaces one of the 31 default gani names (walk, idle, sword, ...) with another gani file. Online gate applies. |
| 732 | `setgender` | S | `male` sets male; anything else sets female. |
| 603 | `hurt` | R | Hurts the player by half-hearts and knocks them away from the NPC's centre. Skipped when the player cannot be hurt right now (dead, in a protected state, or flagged unhittable on an NPC-server). 0 or negative heals (doc). |
| 654 | `freezeplayer` | R | Freezes the player for 0..30 seconds (clamped) and drops what they carry. |
| 669 | `hideplayer` | R | Hides the player for 0..30 seconds. |
| 659 | `hidesword` | R | Hides the sword for 0..30 seconds. |
| 618 | `takeplayercarry` | – | Removes what the player carries and resets the gani. |
| 691 | `takeplayerhorse` | – | Removes the player's horse. |
| 621 / 622 | `enableweapons` / `disableweapons` | – | Turns player weapons on / off. |
| 737 / 738 | `enabledefmovement` / `disabledefmovement` | – | Turns the built-in movement and controls on / off. |
| 753 / 754 | `enableselectweapons` / `disableselectweapons` | – | Allows / blocks opening the weapon selection. |
| 723 | `showstats` | R | Bitmask of status-bar parts to show (doc: 1 ASD, 2 icons, 4 rupees, 8 bombs, ...). |
| 750 | `attachplayertoobj` | R,R | Type 0 only (NPC): attaches the player to the NPC with that id. Online gate applies. |
| 752 | `detachplayer` | – | Detaches the player if attached. |
| 632 | `toinventory` | M | Sets the flag and moves the NPC into the inventory. Offline it leaves the level and the run ends; online a copy goes to the inventory and the NPC stays. Only for NPCs of the current level. |
| 656 | `toweapons` | M | Adds a copy of the NPC as weapon *name* (replacing one with the same name, in the same slot), runs its `playerenters`, selects it, and sends it online. A `/` in the name keeps only the part after it. |

### Combat, items, level objects

| Op | Command | Args | What 2.05 does |
|---|---|---|---|
| 601 | `lay` | I | Drops the item next to the NPC, to the right or below depending on where the player stands (doc). |
| 699 | `lay2` | I,R,R | Drops the item at (x, y). |
| 602 | `take` | I | Picks up the first item of that type lying within the NPC's radius (half its diagonal) and gives it to the NPC. |
| 700 | `take2` | R | Picks up item *index*. |
| 694 | `removeitem` | R | Deletes item *index*. |
| 627 | `putbomb` | R,R,R | Bomb of power 0..2 at (x, y). |
| 628 | `putexplosion` | R,R,R | Explosion of radius *r* at (x, y), with sound. |
| 722 | `putexplosion2` | R,R,R,R | Power, radius, x, y; power 3 is a jolt-bomb explosion. |
| 629 | `putleaps` | R,R,R | Leaps of type 0..5 at (x, y) (bush, swamp, stone, sign, ball, water). |
| 640 | `puthorse` | F,R,R | Horse with that image at (x, y). |
| 692 | `removebomb` | R | Deletes bomb *index*. |
| 697 | `explodebomb` | R | Detonates bomb *index* now. |
| 693 | `removearrow` | R | Deletes arrow *index* (local only, doc). |
| 698 | `reflectarrow` | R | Reverses arrow *index*. Against a character NPC it bounces off the side it hits; otherwise both directions flip. The arrow's sprite turns to its new direction and the shooter becomes the player when called from a weapon. |
| 695 | `removeexplo` | R | Deletes explosion *index*. |
| 696 | `removehorse` | R | Deletes horse *index*. |
| 623..626 | `shootarrow`, `shootfireball`, `shootfireblast`, `shootnuke` | D | Fires that projectile from the NPC's edge in the given direction (reduced mod 4). Drawn on the NPC's layer, or the player's for weapons. |
| 630 | `shootball` | – | Fires a ball from the NPC's centre toward the player. |
| 715 | `spyfire` | R,R | Spawns a fire-spy effect just in front of the player (player position plus their facing direction) and sends it online. **[inf: role of the two arguments]** |
| 662 | `hitplayer` | R,R,R,R | index, half-hearts, fromx, fromy. Local player: hurt with knockback. Another player: UDP 21 to that player only (skipped if they are dead or protected). An NPC: treated like `hitnpc`. |
| 706 | `hitnpc` | R,R,R,R | NPC *index* gets the damage; its script gets `washit` style handling (no automatic push, doc). |
| 741 | `hitobjects` | R,R,R | Hits everything at (x, y) with *power*, like a sword, and sends it online. |
| 617 | `putcomp` | B,R,R | Offline: spawns that baddy at (x, y). Online: asks the server. |
| 651 | `putnewcomp` | B,R,R,M,R | Same, plus image and power. |
| 661 | `hitcompu` | R,R,R,R | index, power, fromx, fromy: damages and knocks back the baddy, and sends it online. |
| 609 | `removecompus` | – | Deletes every baddy (doc: causes `compusdied`). |
| 643 | `noplayerkilling` | – | Turns off player-vs-player damage in this level. |

### Board, map, images

| Op | Command | Args | What 2.05 does |
|---|---|---|---|
| 664 | `updateboard` | R,R,R,R | Redraws the board rectangle (x, y, w, h) after `board[]` writes (doc: also syncs online). |
| 665 | `putobject` | O,R,R | Offline only: stamps a predefined tile object on the 64×64 board at (x, y), clipped to the board, then redraws. Ignored online (doc: security). |
| 672 | `setmap` | F,F,R,R | Loads the big map image and its level-names file, sets the player's head-icon position, and recomputes "is on map" for every player. Both files must exist. |
| 671 | `setminimap` | F,F,R,R | Same for the minimap. |
| 758 | `loadmap` | F | Loads a gmap file; if the current level belongs to it (and the editor is closed), rebuilds the level view. |
| 746 | `addtiledef` | S,S,R | Use image *file* instead of `pics1.png` for levels starting with *prefix*. Online gate applies. |
| 747 | `addtiledef2` | S,S,R,R | Same, but pastes the image at (x, y) of the tileset. Online gate applies. |
| 748 | `removetiledefs` | S | Removes tile definitions for *prefix*. Online gate applies. |
| 657 | `showimg` | R,F,R,R | Image *index* at (x, y), on the NPC's layer +1 (player's for weapons). Re-using an index replaces it; the same file only moves. A name starting with `@` is a text image. |
| 704 | `changeimgpart` | R,R,R,R,R | Visible part of image *index*; x, y clamped to 0..16000, w, h to 0..220. |
| 718 | `changeimgvis` | R,R | Layer of image *index*: 0, 1, 2 = under / level with / over the NPC; 3 = light layer (like `drawaslight`); 4 = screen (over the status bar). |
| 730 | `changeimgcolors` | R,R,R,R,R | Colour multiply for image *index*. Online gate applies. |
| 731 | `changeimgzoom` | R,R | Zoom for image *index*. Online gate applies. |
| 658 | `hideimg` | R | Deletes image *index*. |

### Parsed but ignored by the 2.05 client

These are in the table, so scripts using them compile, but the executor has no handler. They do nothing in 2.05.

| Op | Command | Args | Notes |
|---|---|---|---|
| 636 | `seturllevel` | M | Doc describes it as an offline URL warp; not implemented here. |
| 681 | `setfocus` | R,R | Later logs mention a camera focus at (x, y). |
| 682 | `resetfocus` | – | |
| 690 | `setbacktile` | R | Allowed in preview mode but still a no-op. |
| 707 | `canwarp2` | – | Warp permission is handled by the server in this era **[inf]**. |
| 721 | `drawovertrees` | – | |
| 724 | `canwarp` | – | |
| 734 | `join` | S | Server-side class join in later versions **[inf]**. |
| 735 | `freezeplayer2` | – | |
| 736 | `unfreezeplayer` | – | |
| 755 | `setbacktile2` | R,R,R,R,R | |
| 756 | `setz` | R×8 | |
| 757 | `updateterrain` | – | |

## Corrections to gs1-commands.md

- Pattern letters: `R` is a numeric expression, not the literal string "real". `D` is up 0, left 1, down 2, right 3 (or a number),
  not "0 south, 1 west, 2 east, 3 north".
- `warp` and `jump` are not GS1 commands in 2.05. Warping is `setlevel` / `setlevel2`, or assigning `playerx` / `playery`.
- `canwarp`, `canwarp2`, `join`, `setfocus`, `resetfocus`, `unfreezeplayer` compile but do nothing in 2.05.
- `spyfire` is a game effect with a network packet (PLI 10), not a debug hook.
