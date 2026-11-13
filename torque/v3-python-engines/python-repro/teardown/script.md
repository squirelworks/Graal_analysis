# Script

GS2 is absent. `GRESCR01` is absent. `descipher` is absent. The extension `.code` is in the suffix list in a client routine, which does not show the 8-byte cipher.

## GS1 words · high on the words, medium on the letters beside them

a client routine at an address (about 60 KB) holds the verb table. `showimg` is also a small function at an address. `setplayerprop` and `playerhp` are referenced from a client routine, which did not decompile.

Words in a client routine, in table order, with the format literal when one sits on the next string:

| word | format literal beside it |
| --- | --- |
| `blockagain` `blockagainlocal` `canbecarried` `cannotbecarried` `canbepushed` `cannotbepushed` `canbepulled` `cannotbepulled` `carryobject` | |
| `changeimgcolors` | `idddd` |
| `changeimgmode` | `ii` |
| `changeimgpart` | `iiiii` |
| `changeimgvis` `changeimgzoom` | `id` on `changeimgzoom` |
| `destroy` `dontblock` `dontblocklocal` `drawaslight` `drawoverplayer` `drawunderplayer` `findimg` `hide` `hidelocal` `hideimg` `hideimgs` `hurt` `lay` `message` | |
| `move` | `dddi` |
| `setbow` `setcharani` | `ss` |
| `setchargender` `setcoloreffect` | `dddd` |
| `seteffectmode` `setimg` `setimgpart` | `siiii` |
| `setshape` | `iii` |
| `setshape2` | `iio` |
| `setzoomeffect` `shootarrow` `shootball` `shootfireball` `shootfireblast` `shootnuke` `show` `showani` | `iddis` |
| `showani2` | `idddis` |
| `showcharacter` `showimg` | `isdd` |
| `showimg2` | `isddd` |
| `showlocal` `showpoly` | `io` |
| `showpoly2` `showtext` | `iddsss` |
| `showtext2` | `idddsss` |
| `take` `take2` `takehorse` `throwcarry` `timereverywhere` `toweapons` | |

Field names in the same function, before the verbs: `actionplayer`, `hearts`, `height`, `horseimg`, `hp`, `hurtdx`, `hurtdy`, `layer`, `peltwithnpc`, `peltwithbush`, `peltwithsign`, `peltwithvase`, `peltwithstone`, `peltwithblackstone`, `shieldpower`, `sprite`, `swordpower`, `visible`, `width`.

`setplayerprop` itself is not in this list. It lives in the function that failed to decompile.

## Gani · high

a client routine references `SCRIPTEND` together with `ANIEND`, `WAIT`, `PLAYSOUND`, `ACTOR`, `FRAME`. That is the gani text script, not GS2.
