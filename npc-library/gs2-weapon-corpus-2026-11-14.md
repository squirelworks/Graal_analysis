# What GS2 weapon scripts ask of a 4.x to 6.x client (2026-11-14)

A survey of the client half of real GS2 weapon scripts: which events they handle, which
commands, opcodes and `player` members they use, what `onWeaponFired` does, and how much of
that the graal-client-repro GS2 core and Quattro program already provide. It ends with an
implementation order. Aggregate counts only: no script text, world, weapon, class or file name
is published, and world-specific function names are counted but not named. The evidence is
cited as **GS2-WEAPON-CORPUS-20261114** in `docs/evidence-index.tsv`. **[lab]**

The 3.x Torque clients (3.04, 3.153) are out of scope: their game scripts are GS1. The 3.153
image does carry a GS2 dispatcher ([gs2-vm-by-version.md](../client-internals/gs2-vm-by-version.md)),
but nothing here depends on it.

## The sets

| Set | What | Weapons | Classes | With a client side |
| --- | --- | --- | --- | --- |
| B | the 2007 export of [gs2-world-corpus-2026-11-12.md](gs2-world-corpus-2026-11-12.md), weapons only | 554 | 246 | 522 |
| E | a 2018 playerworld export (weapons, classes and NPCs) | 854 | 720 | 811 |

Set B was written for the clients of mid-2007 (4.20r8, 5.00r7); set E for the 5.x and 6.x
clients of its time **[inf]**. The two worlds script weapons differently. In set E, 453
weapons handle `onWeaponFired`. Set B uses it in only 20 weapons: its spells are fired by a
world key handler that calls a world event on the weapon (211 weapons), so `findweapon` and
calls into another weapon's public functions matter more there.

## Method

1. Each weapon file was unwrapped (header lines, `SCRIPT` … `SCRIPTEND`) and split at the line
   `//#CLIENTSIDE`; only the client part goes to the client.
2. The client parts were compiled with Seihai's GS2 compiler in legacy mode (seihai-core
   8118ede, `scripting::gs2::compile`). Of the weapons with a `//#CLIENTSIDE` line, 784 of 828
   (set E) and 518 of 532 (set B) compiled. The rest stop on parse gaps (47) or on GS1 message
   codes such as `#I` and `#w` (11), and are left out of the bytecode counts. The bytecode
   is that compiler's, not the official one's; opcode choice for these constructs matches the
   official encoder on the fixtures where that has been checked
   ([gs2-world-corpus-2026-11-12.md](gs2-world-corpus-2026-11-12.md#what-this-does-and-does-not-settle)) **[inf]**.
3. The bytecode was read for the opcodes used, global calls (a name pushed with opcode 22 just
   before a call, 6), method calls (22, 35, 6), `player` members (182, 22, 35) and the function
   table. A call to a function the script itself defines, or that any class in the same set
   defines, is not counted as a command.
4. A text pass over all weapons (including those that did not compile) gave the event counts
   and the `onWeaponFired` body categories. Counts are weapons, not occurrences.

## Which clients run these, and how they get them

| Clients | Engine | Weapon delivery from GServer-v2 | VM profile |
| --- | --- | --- | --- |
| 4.04r2, 4.11 Mac, 4.20r6, 4.20r8 | Delphi launcher + `GraalEngine` | 33 with the image, then 193 with a CRC, or 132 with the bytecode **[srv]** | 4.2: no 48, 49, 54, 121; `waitfor` (11) only from 4.20r8; 104 from 4.20r6 |
| 5.00r7, 5.12 | the same split | 33, then 197 (`GRESCR01` header), or 140 with the bytecode **[srv]** | 5.0 |
| 5.24r3 on, every 6.x | Quattro | as 5.00r7 | 6.00 |

Delivery is read from `seihai-gserver-v2` `Weapon::sendWeaponToPlayer` and
`sendByteCodeToPlayer` **[srv]**. The VM profiles are from
[gs2-vm-by-version.md](../client-internals/gs2-vm-by-version.md) **[bin]**.

## Events

Weapons that define each event in their client part (text pass).

| Event | E | B | What fires it in the client |
| --- | --- | --- | --- |
| `onCreated` | 539 | 460 | the script loading |
| `onWeaponFired` | 445 | 18 | the player using the selected weapon |
| `onTimeout` | 342 | 264 | `setTimer` running out |
| `onPlayerEnters` | 208 | 79 | the player arriving in a level |
| `onPlayerChats` | 200 | 98 | the player's own chat line (`player.chat` holds it) |
| `onActionClientSide` | 194 | 58 | the server's 48 with `clientside,<weapon>,…` **[srv]** |
| `onKeyPressed` | 180 | 41 | a key; the scripts read `params` as key code and key |
| `onMouseDown` | 76 | 14 | a mouse press on the play area |
| `onPlayerHurt` | 38 | 0 | the player taking damage |
| `onPlayerDies` | 15 | 0 | the player dying |
| world-defined events (any other `on…` function) | 255 | 258 | `scheduleevent`, `trigger`, or another script's call |

GS1-style event tests (`if (weaponfired)`) are rare in both sets (10 or fewer weapons each).

## What `onWeaponFired` does (set E, 445 handlers)

The median handler is 10 lines, the 90th percentile 25. A handler can fall in several rows.

| Body does | Handlers |
| --- | --- |
| writes or tests `player.chat` (mostly a refusal message such as "not here") | 187 |
| plays a gani on the player (`setani`, `replaceani`) | 168 |
| sends to the server (`triggerserver`, `triggeraction`) | 125 |
| holds the player (`freezeplayer`, `disabledefmovement`) | 108 |
| starts a timer or a scheduled event | 90 |
| none of the rows here (world calls, flags) | 81 |
| opens a `say2` box | 45 |
| calls the weapon's own equip or unequip function | 29 |
| sets `player.dir` or `player.ani` | 25 |
| shows or changes screen images | 22 |
| fires a projectile, lays a bomb or an explosion | 22 |
| toggles an on/off flag | 15 |
| builds a GUI | 9 |
| plays a sound | 7 |

The commands inside the handlers, in order: `setani` 164, `freezeplayer` 98, `triggerserver`
93, `setTimer` 59, `vecx`/`vecy` 48, `say2` 45, `triggeraction` 38, `scheduleevent` 32,
`replaceani` 30, `setshootparams`/`shoot` 14, `hideimg` 12, `showimg` 11,
`disabledefmovement` 10, `play` 8, `disableweapons` 7, `putbomb` 3, `shootarrow` 2.

So a typical fired weapon is: check a cooldown or level rule (and say so in `player.chat`),
play an attack gani with the player held for its length, tell the server, and release on a
timer. That path needs no drawing beyond the gani.

## Commands

Weapons whose compiled client part calls each name (8 or more weapons over both sets).
"GS1 table" means the name is in the command list of 3.04, 4.04r2, 4.20r8 and 5.00r7
([gs1-commands-by-version.tsv](gs1-commands-by-version.tsv)) **[bin]**; "—" means it is not a
GS1 command (a GS2 name, or an expression function), and which 4.x build first has it is not
read. Every name below is used in set B, a 2007 world, except where its B count is 0, so it
existed in the mid-2007 clients **[inf]**. "Repro" is graal-client-repro's GS2 host as of
PR #359 (`common/cpp/gs2/engine_commands.cpp`, `gui.cpp`, `quattro/shell`) **[doc]**.

| Name | E | B | Repro | GS1 table |
| --- | --- | --- | --- | --- |
| `setTimer` | 323 | 269 | registered | — |
| `triggerserver` | 388 | 75 | missing | — |
| `setani` | 355 | 83 | missing | yes |
| `triggeraction` | 102 | 270 | missing | yes |
| `join` | 8 | 358 | registered | yes |
| `freezeplayer` | 265 | 60 | missing | yes |
| `findweapon` | 28 | 224 | missing | — |
| `addcontrol` | 140 | 84 | registered | — |
| `keydown` | 181 | 26 | registered | — |
| `hideimg` | 128 | 53 | missing | yes |
| `scheduleevent` | 161 | 8 | missing | — |
| `findimg` | 101 | 61 | missing | — |
| `hideimgs` | 91 | 52 | missing | yes |
| `replaceani` | 122 | 7 | missing | yes |
| `showimg` | 91 | 32 | missing | yes |
| `destroy` | 63 | 38 | missing | yes |
| `setshootparams` | 67 | 29 | missing | yes |
| `shoot` | 67 | 25 | missing | yes |
| `md5` | 1 | 81 | missing | — |
| `say2` | 67 | 8 | missing | yes |
| `keydown2` | 62 | 10 | missing | — |
| `onwall2` | 61 | 9 | missing | — |
| `enabledefmovement` | 64 | 6 | missing | yes |
| `disabledefmovement` | 56 | 8 | missing | yes |
| `changeimgcolors` | 57 | 13 | missing | yes |
| `changeimgvis` | 57 | 12 | missing | yes |
| `clearrows`, `addrow`, `setselectedrow` | 50, 51, 38 | 18, 14, 10 | registered | — |
| `echo` | 27 | 36 | registered | — |
| `enableweapons` | 59 | 3 | missing | yes |
| `disableweapons` | 52 | 3 | missing | yes |
| `play` | 59 | 3 | missing | yes |
| `showtext` | 43 | 14 | missing | yes |
| `getimgwidth`, `getimgheight` | 33, 32 | 12, 11 | missing | — |
| `cancelevents` | 43 | 0 | missing | — |
| `showpoly` | 23 | 20 | missing | yes |
| `changeimgzoom` | 36 | 5 | missing | yes |
| `changeimgpart` | 23 | 16 | missing | yes |
| `showani` | 13 | 20 | missing | yes |
| `setfocus`, `resetfocus` | 26, 29 | 3, 3 | missing | yes |
| `seticonsize` | 23 | 9 | missing | — |
| `keycode`, `getkeycode` | 32, 21 | 0, 8 | missing | — |
| `onwall` | 21 | 6 | missing | — |
| `findplayer` | 11 | 15 | missing | — |
| `testnpc` | 16 | 6 | missing | — |
| `seteffect` | 16 | 4 | missing | yes |
| `serverwarp` | 6 | 14 | missing | yes |
| `showstats` | 15 | 4 | missing | yes |
| `lowercase` | 8 | 11 | registered | — |
| `onwater`, `onwater2` | 14, 14 | 4, 0 | missing | — |
| `getstringkeys` | 2 | 15 | missing | — |
| `gettextwidth` | 6 | 11 | missing | — |
| `putleaps` | 14 | 1 | missing | yes |
| `hideplayer` | 15 | 0 | missing | yes |
| `enablepause`, `disablepause` | 10, 13 | 0, 2 | missing | yes |
| `changeimgmode` | 13 | 2 | missing | yes |
| `addlocalmodifier` | 14 | 0 | registered (emitter) | — |
| `disableselectweapons`, `enableselectweapons` | 13, 9 | 1, 0 | missing | yes |
| `enablefeatures` | 11 | 3 | missing | yes |
| `isobject` | 12 | 0 | missing | — |
| `playlooped`, `play2` | 11, 9 | 0, 0 | missing | yes |
| `noplayerkilling` | 8 | 3 | missing | yes |
| `requesttext` | 2 | 9 | missing | — |
| `putbomb`, `shootarrow`, `shootfireball`, `shootnuke` | 5, 4, 5, 5 | 0 | registered (#359) | yes |

World class functions (defined in the set's own classes and delivered with 133/134) are left
out: in set E the most-called one is a level rule check (70 weapons); in set B, a cooldown
and a damage helper (114 and 51).

Methods called on objects, beyond the GUI row methods #359 already has: `destroy` (151 E,
82 B), `show` and `hide` on controls (32, 31), `lower` (21), `isinclass` (18), `drawimage`
and `drawimagerectangle` on drawing panels (18, 11), `showtop` (15), `objecttype` (10),
`scrolltobottom` (9), `scheduleevent` on an object (9), `trigger` (7 E, 15 B). Set B
also calls four world-defined functions as methods on other objects, in 41 to 147 weapons
each; with its 224 `findweapon` calls, calling another weapon's `public function` is the main
thing set B needs from `findweapon` **[inf]**.

## Opcodes the repro machine still refuses

Opcodes the repro's `common/cpp/gs2/machine.cpp` has no case for (PR #359), by weapons whose
compiled client part contains them **[doc][lab]**:

| Opcode | E | B | Notes |
| --- | --- | --- | --- |
| 81 `in` (value in a list) | 175 | 33 | |
| 95 `getangle` | 113 | 40 | |
| 136 list `add` | 108 | 72 | |
| 80 `in` range (`in <a, b>`) | 101 | 51 | |
| 118 `tokenize` | 88 | 173 | |
| 96 `getdir` | 48 | 86 | |
| 137 list `delete` | 39 | 25 | |
| 38 new array | 25 | 40 | |
| 133, 134, 142 two-dimensional arrays | 22, 5, 6 | 2, 1, 4 | |
| 138 list `remove` | 22 | 5 | |
| 141 list `clear` | 16 | 3 | |
| 41 `makevar` | 14 | 32 | |
| 140 list `insert` | 10 | 3 | |
| 39 `setarray` | 7 | 0 | |
| 120 `positions` | 6 | 3 | |
| 11 `waitfor` | 5 | 0 | 4.20r8 on only |
| 135 `subarray`, 139 `replace`, 99, 83, 92 | ≤ 4 | ≤ 3 | |

Everything else the weapons use (calls, `with`, `foreach`, `format`, `sleep`, string methods
`starts`, `substring`, `pos`, `length`, `trim`, `ends`, arrays 131/132, the maths opcodes) the
machine already runs.

## `player` members read or written

Set E, weapons: `chat` 413, `y` 327, `x` 325, `level` 287, `dir` 264, `account` 234, `ani` 136,
`z` 76, `mp` 71, `gmap` 66, `attr[]` 58, `guild` 51, `weapons` 51, `freezetime` 47, `hearts`
46, `client`/`clientr` 38/18, `weapon` 35, `ap` 25, `paused` 22, `communityname` 22, `colors`
16, `darts` 16, `nick` 16, `fullhearts`, `rupees` 14, `head`/`body`/image members ≤ 12. Set B
adds `target` (102) and many world-defined members. The repro's Quattro `player` object
(PR #359) keeps `x`, `y`, `dir`, `bombs`, `darts`, `rupees`, `hearts`, `fullhearts`, `id`,
`account`, `nick`, `ani` and `level` in step; it does not yet carry `chat`, `z`, `mp`, `ap`,
`gmap`, `attr[]`, `guild`, `weapons`, `weapon`, `freezetime` or `client`/`clientr` **[doc]**.

## Implementation order

"Runs" below means the weapon's compiled client part has no opcode the repro machine refuses
and calls no name that is neither registered nor defined in the script or its set's classes.
It says nothing about whether the commands behave correctly. With #359, 119 of 784 set-E
weapons and 99 of 518 set-B weapons pass that bar **[lab]**.

Adding the names in the order below raises that count step by step (a greedy order: each step
adds the name that lets the most further weapons pass).

| Step | Adds | Set E passing (of 784) | Set B passing (of 518) |
| --- | --- | --- | --- |
| — | PR #359 as it is | 119 | 99 |
| 1 | `triggerserver`, `triggeraction` (and `onActionClientSide` from 48) | 168 | 128 |
| 2 | `setani`, `replaceani`, `freezeplayer` | 247 | 135 |
| 3 | `say2`, `scheduleevent`, `cancelevents`, `destroy` | 279 | 145 |
| 4 | every opcode in the table above | 349 | 183 |
| 5 | the show-image commands: `showimg`, `showimg2`, `hideimg`, `hideimgs`, `findimg`, `changeimg*`, `showtext`, `showtext2`, `showpoly`, `showani`, `getimgwidth`, `getimgheight` | 400 | 217 |
| 6 | `findweapon`, `onwall`, `onwall2`, `onwater`, `onwater2`, `testnpc`, `play`, `play2`, `playlooped`, `keydown2`, `keycode`, `getkeycode`, `seticonsize`, `hideplayer`, `md5`, `enabledefmovement`, `disabledefmovement`, `enableweapons`, `disableweapons`, `setfocus`, `resetfocus` | 533 | 406 |
| 7 | `setshootparams`, `shoot` | 586 | 431 |

Counts are cumulative **[lab]**. The order follows what the fired-weapon path needs first, not
the greedy best: a greedy run (each step the single name that lets the most further weapons
pass) puts the same names in nearly the same order, with `tokenize` and `in` inside the first
eight. After step 7, what blocks the remaining 198 (E) and 87 (B) weapons is a long tail: no
name blocks more than 16 of them (`seteffect`, `showstats`, `putleaps`, `findplayer`,
`getstringkeys`, `serverwarp`, `isobject`, `enablefeatures`, the weapon-select switches).

What each step needs from the client, in the repro's terms:

1. **Server messages.** `triggerserver(kind, name, params…)` and
   `triggeraction(0, 0, "serverside", name, params…)` both end as client 38 TRIGGERACTION with
   `serverside,<weapon>,<params>`; GServer-v2 turns that into the weapon's
   `onActionServerSide` **[srv]**. That `triggerserver` sends exactly this text is read from the
   scripts and the server, not from a client **[inf]**. The reverse path, server 48 with
   `clientside,<weapon>,<params>`, has to queue `onActionClientSide` on that weapon with
   `params` set.
2. **Gani and hold.** `setani(gani, params)` and `replaceani(old, new)` set what the player
   draws (the repro already draws ganis); `freezeplayer(seconds)` and
   `disabledefmovement`/`enabledefmovement` stop the walk keys; `player.freezetime`,
   `player.ani` and `player.dir` read and write the same state. These, with `player.chat`
   (written to the chat bubble and sent as the chat prop) and the `onPlayerChats` and
   `onKeyPressed` events, cover the common fired-weapon path in the section above.
3. **Events and boxes.** `scheduleevent(seconds, event, params…)` queues a named event on the
   object, `cancelevents(name)` drops them; `say2` opens the sign box with the text; `destroy`
   removes an object (a control, a show-image, the script's own object).
4. **Machine.** The opcodes in the table above, all in `common/cpp/gs2`. Their behaviour is in
   [../client-internals/gs2-vm-from-engines.md](../client-internals/gs2-vm-from-engines.md) and
   [../protocol/gs2-client-vm.md](../protocol/gs2-client-vm.md); `in` with a range and a list,
   `tokenize` and the list methods are the ones the corpus leans on.
5. **Show-images.** The numbered show-image layer (`showimg`, `showimg2`, `showtext`,
   `showpoly`, `showani`, `changeimg*`, `findimg` returning the object, `hideimg`, `hideimgs`,
   `getimgwidth`/`getimgheight`). The repro's `GuiShowImgCtrl` already draws an ani or an image
   through the painter; the world-layer show-images are the same object type drawn over the
   level.
6. **Lookups and the rest.** `findweapon(name)` returning the weapon's script object so that a
   call on it runs that script's public function (the machine already calls "another object's
   script"); wall and water tests against the board; sound as a logged no-op until the sound
   layer exists.

7. **Projectiles.** `setshootparams` and `shoot` (67 and 25 weapons) need the shot packet
   and the `onActionProjectile` event on the receiving side.

## Not settled

- Which 4.x build first has each GS2-only name (`triggerserver`, `scheduleevent`, `findimg`,
  `findweapon`, `md5`, `cancelevents`, `keydown2`, `onwall2`). The GS1 command table does not
  list them; the engines' command tables would. Set B shows most existed by mid-2007.
- What a 4.x to 6.x client does when a script calls a name it does not have. The repro raises
  the engines' "not found" error; whether the original then stops the script or goes on is not
  read.
- The argument forms. This survey counts names, not signatures; the GS1 table gives argument
  letters for the GS1 names only.
- Whether the official compiler emits the same opcodes for these scripts as Seihai's (for the
  opcode table above). The official 6.113 bodies in
  [../protocol/gs2-official-bytecode-6113.md](../protocol/gs2-official-bytecode-6113.md) are the
  check.
