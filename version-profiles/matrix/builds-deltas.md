# Per-build deltas from the static survey, 1998 to 2.31

Date: 2026-10-30. Generated from the survey in `README.md` (method there). Each line lists what a build adds (+) or drops (−) against the build listed before it, in link order. Graal3D is a separate program and is listed on its own. **[bin]** strings and form resources; **[file]** shipped files.

## `graalconfig.txt` keys

Plain `key=` strings. From 1.38 some keys are built one character at a time, so a key can be missing from this list while the build still reads it; garbled three-letter keys (`ekv`, `u5j`, `d4n`, `kxs`, `azg`) are such fragments.

- **6th Graal (beta5)**: + `joystickon=`, `musicon=`, `reversestereo=`, `soundfxon=`, `waitvertical=`
- **8th Graal (beta8)**: + `saveimages=`
- **1.1 (15th)**: + `editnickname=`, `gamemode=`
- **1.21**: + `accountname=`, `loadcolorsfromserver=`, `password=`, `serveraddr=`, `serverport=`
- **1.28 beta2**: + `compabilitydraw=`, `externalchat=`, `language=`, `nodecompressionerror=`
- **1.3 test**: + `font=`, `fontsize=`; − `accountname=`, `password=`
- **1.31**: + `fixedport=`, `fixedudpport=`, `noudp=`; − `editnickname=`
- **1.32**: + `nomassmessages=`
- **Graal3D** (separate program): `bodytex=`, `bodyx=`, `fixedport=`, `fixedudpport=`, `headx=`, `noudp=`, `serveraddr=`, `serverport=`
- **1.33**: + `nodirectinput=`
- **1.35**: + `nohtmlinpms=`, `u5j=`
- **1.36**: + `limitnicknames=`, `nicknamelimit=`; − `serverport=`
- **1.38**: − `externalchat=`
- **1.39**: + `dontconnectlevels=`, `dontloadlistheads=`, `nohtmlimages=`, `notoalls=`, `sortplayersbyname=`
- **1.41 rev1**: + `dontsavepasswords=`, `fullscreenmode=`, `usewinamp=`; − `serveraddr=`
- **NewMain 1.42 (24)**: + `dontsavepms=`, `dontusedirectx7=`, `ekv=`, `head=`, `joyselected=`; − `gamemode=`
- **2.00**: − `loadcolorsfromserver=`
- **NewWorld beta 1**: − `ekv=`
- **2.05 rev2**: + `ekv=`
- **2.1 test 2**: + `startinfullscreen=`; − `ekv=`
- **2.17.1**: + `automapping=`, `d4n=`, `kxs=`, `microactivatebyvolume=`, `microactivatekey=`, `microactivationlevel=`, `microinputdevice=`, `microon=`, `midivolume=`, `mp3volume=`, `quickplayerworlds=`, `radiovolume=`, `sfxvolume=`, `voicecodec=`, `voicevolume=`; − `musicon=`, `soundfxon=`, `usewinamp=`
- **2.22**: + `azg=`; − `d4n=`, `kxs=`
- **2.31**: + `cachefilenames=`

## Sound effect names (`.wav`)

Names the executable refers to. Sounds named only by scripts or ganis are not here.

- **4th Graal alpha**: + `arrow.wav`, `axe.wav`, `bomb.wav`, `chest.wav`, `crush.wav`, `dead.wav`, `extra.wav`, `frog.wav`, `lift.wav`, `put.wav`, `sword.wav`, `swordon.wav`
- **7th Graal (beta7)**: + `water.wav`
- **8th Graal (beta8)**: + `arrowon.wav`, `compudead.wav`, `fire.wav`, `goal.wav`, `horse.wav`, `horse2.wav`, `item.wav`, `item2.wav`, `jump.wav`, `lift2.wav`, `nextpage.wav`, `sign.wav`, `steps.wav`, `steps2.wav`, `stonemove.wav`, `thunder.wav`
- **1.1.9 Gold**: − `horse.wav`, `horse2.wav`, `steps2.wav`
- **Graal3D** (separate program): none
- **1.34**: + `horse2.wav`
- **NewMain 1.42 (24)**: − `dead.wav`, `goal.wav`, `sign.wav`
- **NewWorld beta 1**: − `chest.wav`, `compudead.wav`, `frog.wav`, `item2.wav`, `jump.wav`, `stonemove.wav`, `swordon.wav`
- **2.05 rev2**: + `chest.wav`, `compudead.wav`, `frog.wav`, `item2.wav`, `jump.wav`, `stonemove.wav`, `swordon.wav`
- **NewWorld beta 2**: − `chest.wav`, `compudead.wav`, `frog.wav`, `item2.wav`, `jump.wav`, `stonemove.wav`, `swordon.wav`
- **2.17.1**: + `chest.wav`, `compudead.wav`, `frog.wav`, `item2.wav`, `jump.wav`, `stonemove.wav`, `swordon.wav`

## Image names the executable refers to

- **1st Graal**: + `letters.gif`, `link.gif`, `map.gif`, `opps.gif`, `pics1.gif`, `state.gif`
- **3rd Graal**: + `heads.gif`
- **5th Graal**: + `sprites.gif`; − `link.gif`
- **5th Graal alpha**: + `map2.gif`
- **9th Graal alpha**: + `graal.bmp`, `ride.gif`, `ride2.gif`, `servant1.gif`
- **9th Graal (beta9)**: + `w-warpdoor.gif`
- **1.0 (11th)**: + `warpdoor.gif`; − `w-warpdoor.gif`
- **1.1 (15th)**: + `map3.gif`
- **1.21**: + `baddyblue.gif`, `baddydragon.gif`, `baddygold.gif`, `baddygray.gif`, `baddyhare.gif`, `baddylizardon.gif`, `baddyoctopus.gif`, `baddyred.gif`, `head0.gif`, `head1.gif`, `head2.gif`, `head3.gif`, `shield1.gif`, `shield2.gif`, `shield3.gif`, `sword1.gif`, `sword2.gif`, `sword3.gif`, `sword4.gif`, `wbomb1.gif`, `wbomb2.gif`, `wbomb3.gif`, `wbow1.gif`, `wbow2.gif`, `wbow4.gif`, `wbowi1.gif`, `wbowi2.gif`, `wbowi3.gif`, `wbowi4.gif`; − `heads.gif`, `ride.gif`, `ride2.gif`, `servant1.gif`, `warpdoor.gif`
- **1.28 beta2**: − `map3.gif`
- **1.3 test**: + `ss_arrow.gif`, `ss_bomb.gif`
- **Graal3D** (separate program): `body.bmp`, `logo.bmp`, `man.bmp`
- **1.33**: + `body.png`, `bomb1.png`, `bomb2.png`, `letters.png`, `map.png`, `map2.png`, `opps.png`, `pics1.png`, `sprites.png`, `state.png`; − `letters.gif`, `map.gif`, `map2.gif`, `opps.gif`, `pics1.gif`, `sprites.gif`, `state.gif`
- **1.34**: + `graal.png`
- **1.35**: + `graalmap.bmp`; − `head0.gif`, `head1.gif`, `head2.gif`, `head3.gif`
- **1.41 rev1**: + `graalmap.png`; − `graal.bmp`, `graalmap.bmp`
- **NewMain 1.42 (24)**: + `head0.gif`
- **2.00**: + `1hlight2.png`, `ahlight2.png`, `arrowsbox.gif`, `bluelampani.gif`, `door.gif`, `gate1.gif`, `gate2.gif`, `head19.gif`, `head24.gif`, `head26.gif`, `head27.gif`, `head495.gif`, `light2.png`, `sleepkoji.gif`, `tutorial_housegate.png`, `tutorialmap.png`, `tutorialmap2.png`
- **NewWorld beta 1**: + `bodynw.png`, `headalgo000.gif`, `newsword.png`, `pics1nw.png`, `spritesnw.png`; − `1hlight2.png`, `ahlight2.png`, `arrowsbox.gif`, `bluelampani.gif`, `body.png`, `door.gif`, `gate1.gif`, `gate2.gif`, `head19.gif`, `head24.gif`, `head26.gif`, `head27.gif`, `head495.gif`, `light2.png`, `sleepkoji.gif`, `sprites.png`, `tutorial_housegate.png`, `tutorialmap.png`, `tutorialmap2.png`, `wbow1.gif`, `wbow2.gif`, `wbow4.gif`
- **2.05 rev2**: + `1hlight2.png`, `ahlight2.png`, `arrowsbox.gif`, `bluelampani.gif`, `body.png`, `door.gif`, `gate1.gif`, `gate2.gif`, `head19.gif`, `head24.gif`, `head26.gif`, `head27.gif`, `head495.gif`, `light2.png`, `sleepkoji.gif`, `sprites.png`, `tutorial_housegate.png`, `tutorialmap.png`, `tutorialmap2.png`, `wbow1.gif`, `wbow2.gif`, `wbow4.gif`; − `bodynw.png`, `headalgo000.gif`, `newsword.png`, `pics1nw.png`, `spritesnw.png`
- **NewWorld beta 2**: + `bodynw.png`, `headalgo000.gif`, `newsword.png`, `pics1nw.png`, `spritesnw.png`; − `1hlight2.png`, `ahlight2.png`, `arrowsbox.gif`, `bluelampani.gif`, `body.png`, `door.gif`, `gate1.gif`, `gate2.gif`, `head19.gif`, `head24.gif`, `head26.gif`, `head27.gif`, `head495.gif`, `light2.png`, `sleepkoji.gif`, `sprites.png`, `tutorial_housegate.png`, `tutorialmap.png`, `tutorialmap2.png`, `wbow1.gif`, `wbow2.gif`, `wbow4.gif`
- **2.17.1**: + `baddyblue.png`, `baddydragon.png`, `baddygold.png`, `baddygray.png`, `baddyhare.png`, `baddylizardon.png`, `baddyoctopus.png`, `baddyred.png`, `body.png`, `bshield0.png`, `emoticonmicro.png`, `g2k2pet_squirrelm0.png`, `graal2002letters.png`, `head0.png`, `head26.png`, `khairs0.png`, `khead0.png`, `klegs0.png`, `kmarms100.png`, `kmbody100.png`, `picso.png`, `shield1.png`, `shield2.png`, `shield3.png`, `sprites.png`, `ss_arrow.png`, `ss_bomb.png`, `sword1.png`, `sword2.png`, `sword3.png`, `sword4.png`, `wbomb1.png`, `wbomb2.png`, `wbomb3.png`, `wbow1.png`, `wbow2.png`, `wbow4.png`, `wbowi1.png`, `wbowi2.png`, `wbowi3.png`, `wbowi4.png`; − `baddyblue.gif`, `baddydragon.gif`, `baddygold.gif`, `baddygray.gif`, `baddyhare.gif`, `baddylizardon.gif`, `baddyoctopus.gif`, `baddyred.gif`, `bodynw.png`, `head0.gif`, `headalgo000.gif`, `newsword.png`, `pics1nw.png`, `shield2.gif`, `shield3.gif`, `spritesnw.png`, `ss_arrow.gif`, `ss_bomb.gif`, `sword1.gif`, `sword2.gif`, `sword3.gif`, `sword4.gif`, `wbomb1.gif`, `wbomb2.gif`, `wbomb3.gif`, `wbowi1.gif`, `wbowi2.gif`, `wbowi3.gif`, `wbowi4.gif`
- **2.31**: − `graalmap.png`, `shield1.gif`, `ss_arrow.png`, `ss_bomb.png`

## Delphi forms (windows)

Form class names from the RCDATA resources.

- **1st Graal**: + `TADVENTURE`, `TCONNECTFRAME`, `TEDITBADDY`, `TEDITSIGNS`, `TLINKLIST`, `TLINKOPTIONS`, `TLOADLEVEL`, `TOBJECTNAME`, `TOPTIONS`, `TSHOWCODES`
- **2nd Graal**: + `TCHESTEDIT`, `TEDITPERSON`, `TPERSONACTION`
- **3rd Graal**: + `TEDITFLAGS`
- **5th Graal**: + `TMOREOPTIONS`
- **6th Graal (beta5)**: + `TOPENURL`
- **9th Graal alpha**: + `TRECONNECTFRAME`
- **1.1 (15th)**: + `TCONTROLSFRAME`
- **1.21**: + `TDEBUGGERFRAME`
- **1.28 beta2**: + `TEDITCHARACTER`, `TMESSAGEEDITOR`, `TPLAYERLIST`
- **1.32**: + `TRTFMESSAGE`
- **Graal3D** (separate program): `TADVENTURE`, `TCONNECTFRAME`, `TEDITLOOK`, `TMOREOPTIONS`
- **1.39**: + `TPLAYERLISTOPTIONS`, `TPROFILEEDIT`
- **1.41 rev1**: + `TSERVERLISTFRAME`, `TSERVERMESSAGE`, `TSHORTMESSAGE`, `TWAABOUT`; − `TRTFMESSAGE`
- **2.04**: + `TOBJECTSET`
- **NewWorld beta 1**: − `TCHESTEDIT`, `TEDITBADDY`
- **2.05 rev2**: + `TCHESTEDIT`, `TEDITBADDY`
- **2.1 test 2**: + `TEDITNPC`; − `TEDITPERSON`, `TOBJECTSET`, `TPERSONACTION`, `TSHOWCODES`
- **NewWorld beta 2**: − `TCHESTEDIT`, `TEDITBADDY`
- **2.17.1**: + `TABOUTDLG`, `TCHESTEDIT`, `TEDITBADDY`, `TLOGFRAME`, `TRPGFRAME`, `TTILESARRAYFRAME`; − `TWAABOUT`
- **2.31**: − `TCHESTEDIT`, `TDEBUGGERFRAME`, `TEDITBADDY`, `TEDITCHARACTER`, `TEDITFLAGS`, `TEDITNPC`, `TEDITSIGNS`, `TLINKLIST`, `TLINKOPTIONS`, `TOBJECTNAME`, `TTILESARRAYFRAME`

## Font names in the executable

- **1st Graal**: + `Courier`, `MS Sans Serif`, `System`
- **6th Graal (beta5)**: − `Courier`
- **Graal3D** (separate program): `MS Sans Serif`, `System`
- **1.34**: + `Courier`, `Courier New`
- **2.17.1**: + `Arial`
