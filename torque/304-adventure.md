# The 3.04 2D session

Date: 2026-11-07. Static read of the Linux `graalexe` 3.04 decompile. Nothing was run. Tags as in [README.md](README.md).

This binary has no C++ type named `TAdventure`. The on-screen game is the Torque control `GuiGraalCtrl`. The first time that control wakes it logs `Graal activated!`, allocates the session from `gui/guiGraalCtrl.cc`, and `graal/adventure.cpp` fills it in. A later wake reuses the same session. **[bin]**

## Session start

`adventure.cpp` opens `license/license.graal`, `license/sig.license` and `license/sig.graal` before it builds the world objects. The public-key check on those files is the one in [protocol/v3x-clients.md](../protocol/v3x-clients.md). **[bin]**

The constructor then:

- passes the status list `Online,Away,DND` into the player-list setup
- creates the local player (`graal/graalplayer.cpp`) and, when graphics are ready, loads its images
- builds five surfaces (`graal/surfaceowner.cpp`): one unnamed, then `sprites.png`, `state.png`, `bomb1.png` and `bomb2.png`
- loads the tile definitions (`graal/tiles.cpp`)

**[bin]**

An empty screenshot name is prefixed with `graal_` and the actual grab is Torque's console call `screenShot`. **[bin]**

Leaving a dead connection raises Torque `MessageBoxOK` with the disconnect text. A counter on that connection past 1199 raises the same box and the counter is cleared. **[bin]**

## Mouse, keys and chat

`GuiGraalCtrl` owns the child named `ChatBar`. A key-down whose modifier mask 48 is clear toggles a chat-focus flag, shows or hides `ChatBar`, and makes it the responder while the flag is on. Other keys go to `adventure.cpp`. While chat focus is off, key codes 33 through 58 are handed to the local player as the letters A through Z (the code plus 32). A key whose code is 25, with mask 48 set, calls the screenshot path. **[bin]**

Mouse buttons are named `left`, `middle` and `right`. A press tells the local player that name, and fires a script event `leftmouse`, `middlemouse` or `rightmouse`. A repeat click also fires `double` and `doublemouse`. When a game connection exists, the same names are sent there. A release sends the button name without the `mouse` event. **[bin]**

Three local-player states change a click before that:

- One state treats the click as a probe and then leaves the state.
- The map state, when modifier mask 12 is set, is a warp. The mouse is scaled from the big-map image onto the gmap, in 64-pixel tiles. With a game connection the line sent starts with `warpto `; with none, the local player moves.
- The map state, or a flag on the player, picks a message target under the cursor. A named body whose flag is set wins, then text that starts with `Guild message:`, then any other named body, then `Mass message:`, then an unnamed body that has a script. If nothing matches, the click keeps the player's own chat target.

**[bin]**

`setChat` lands in the same chat routine and then runs `ChatBar.setText("")`. A line that starts with `toall:` is stripped of that prefix and sent on the game connection. The exact line `showname` stores 60 on the local player and does not send. The exact line `showap` stores 60 and sends an empty body. Any other line stores 61 and sends the text. **[bin]**

## Levels and the local player

`graalplayer.cpp` only logs `Player enters local level %s.` when there is no game connection. The first eight bytes of the file must be `Z3-V1.03`, `Z3-V1.04`, `GR-V1.00`, `GR-V1.01`, `GR-V1.02`, `GR-V1.03` or `GLEVNW01`. Anything else sets a failure flag and the value 40, and does not log the enter line. `GR-V1.04` and `GSERVL01` are not accepted by this gate. **[bin]**

`Player enters server level %s.` is the other path. It looks the level up by name and, if it has to create one, uses the web-level reader. **[bin]**

`levels.cpp` is the parser behind both. It logs `Loaded minimap from %s` and `Scanning folder structure of %s...`. A gmap is recognised by `GRMAP001` and the keys `WIDTH`, `HEIGHT`, `GENERATED`, `LEVELNAMES`, `GENSEED`, `LEVHEIGHT`, `LEVCHAOS`, `MINIMAPIMG`, `NOAUTOMAPPING`, `HEIGHTMAP`, `RANDOMSEEDS` and `HEIGHTS` (each with the matching `END` marker where the file has one). A level body is `GLEVNW01` or `GSERVL01`, with sections `BOARD`, `CHEST` (image `chest.png`), `NPC`, `BADDY`, `SIGN`, `HEIGHTS` and `REPLACENPCS`. `GR-V1.00` through `GR-V1.04` are all named. A cached download is `GWEBL001` under `weblevels`, beside `.code` files. Emoticon files are prefixed `emoticon_`. **[bin]**

The cache read and write call `descipher.cpp`. That unit pads with byte value 10 out to a multiple of 8, writes a 4-byte length, runs each 8-byte block through an encrypt or decrypt step, and keeps a bytewise running sum. The reader drops the buffer when the stored sum does not match. Those two steps sit in the same part of the binary as the Crypto++ type names `DESEncryption` and `DESDecryption`. The layout is the web-level cache in [protocol/v3x-clients.md](../protocol/v3x-clients.md). **[bin]**

The local player loads `bigmap.txt`, `map.png`, `minimap.txt`, `map2.png` and `letters.png`, and starts on the animation `idle`. It writes the console line `$pref::Graal::nickname = "%s";` when the nick changes. Wrapping a line splits on space and the characters `.,;+-?!`. Sword and shield stems are `sword1.` through `sword4.` and `shield1.` through `shield3.`. Sounds named here include `lift.wav` and `lift2.wav`. The offline tutorial level `offlinetutorial_b-2.graal` is named in this unit. Entering a level fires the trigger `playerenters`; a touch fires `playertouchsme`. **[bin]**

`startOfflineMode` shows `AdventureGui` and loads `offlinetutorial.gmap` for the local player, and only when no game connection is open. **[bin]**

## What the control exposes

The console methods on `GuiGraalCtrl`, in order, are `moveUp`, `moveLeft`, `moveDown`, `moveRight`, `doA`, `doS`, `doD`, `doQ`, `doP`, `doM`, `doMicro`, `setChat`, `setPassWord`, `openServerList`, `selectServer`, `selectServerCategory`, `startOfflineMode`, `connectToSelectedServer`, `serverDirectConnect`, `privateMessageSend`, `playerListOpenPlayer`, `playerListProfile`, `updateLoadLevelFields`, `loadLevel`, `updatePlayerProfile`, `updatePlayerMuted`, `updateMidiVolume`, `updateMp3Volume`, `updateRadioVolume`, `updateMicroActivationLevel`, `updateGraalOptions`. Counts include the command name and the object: `loadLevel` is 5, `updatePlayerProfile` is 12. The table does not register `setNickName`, `setAccountName`, `setLanguage` or `retrieveAccountFields`. **[bin]**

The same control file registers `$pref::Graal::` variables: `nickname`, `accountname`, `language` (the default literal is `English`), `automapping`, `notoalls`, `dontloadlistheads`, `fixedport`, `fixedudpport`, `noudp`, `dontconnectlevels`, `limitnicknames`, `nicknamelimit`, `defaultfontsize`. Movement methods pass the script argument through to the local player. `openServerList`, `connectToSelectedServer`, `startOfflineMode` and `serverDirectConnect` call the server-list unit. Volume methods call the sound unit ([304-audio-ui.md](304-audio-ui.md)). **[bin]**
