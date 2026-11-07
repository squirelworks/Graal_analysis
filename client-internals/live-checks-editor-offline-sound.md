# Live checks: editor, offline mode and sound (2.05, 2.22, 2.31, GraalEditor)

Date: 2026-10-30

These results come from running the real clients in the Wine lab described in `live-trace-205.md`: Wine 9 with a 32-bit prefix, Xvfb, a network namespace with only loopback, and an ALSA `null` device so that DirectSound starts. File access was logged with Wine's `+file` channel, and which file each action used was read from that log. The code paths named below come from the 2.05 rev 2 decompile. Names only, no code.

Tags: **[live]** seen in a running client · **[2.05]** read from the 2.05 binary · **[inf]** inferred.

Corrections to earlier notes are collected at the end.

## Offline mode

### The Training button

All three clients tested have a **Training** button on the start screen. 2.05 rev 2's welcome text says: "press 'Training' for some offline training levels, and 'Start' for the online mode." Pressing it starts offline play on the embedded tutorial and makes no network connection. **[live]**

| Client | Start screen buttons | Training starts on | Big map / minimap |
|--------|----------------------|--------------------|-------------------|
| 2.05 rev 2 | Training, Options, Start | `tutorial_b-4.graal`: the welcome sign, Stefan, the two coloured lights | `tutorialmap.txt` set by the level's `setmap` NPC |
| 2.22 | Training, Options, Get an account!, Start | `offlinetutorial_b-2.graal`, the centre of the 3×3 grid: wizard, cauldron, two torches | the client's `bigmap.txt` / `minimap.txt`, plus `maps/parts/offlinetutorial/offlinetutorial_*.graal.png` |
| 2.31 | Training, **Editor**, Options, Get an account!, Start | `offlinetutorial_b-2.graal`, the same as 2.22 | the same as 2.22 |

The 2.22 and 2.31 start level plays `cauldron_bubbles.wav` and `fire_torch0..2.wav` as soon as it loads. Those sounds come from its NPCs. **[live]**

### The embedded level always wins

A file on disk with the same name does not replace the embedded level. **[live]**

- **2.05**: with `tutorial_b-4.graal` (a different level's contents) in the game folder, Training still loads the embedded b-4. The client does not even look for the name on disk.
- **2.22**: with `offlinetutorial_b-2.graal` in the game folder, the client looks the name up once but still loads the embedded copy.

### Tile definitions when offline

Every client tested reads `levels/tiledefs/tiledefsOffline.txt` when Training starts. That includes 2.05, which builds the file name as `tiledefs` + the server name + `.txt`, and the server name offline is `Offline`. The shipped file has one line, `picso.png,offlinetutorial,1,0,0`, which applies to the `offlinetutorial*` levels only. So in 2.05 the read happens but has no effect on the old `tutorial_*` levels. **[live][2.05]**

### The reconnect dialog and *Play offline*

Pressing *Start* in 2.05 with no listserver shows "The connection couldn't be established!" and stays on the server list. That screen has no *Play offline* button. **[live]**

The reconnect dialog has three buttons: *Reconnect*, *Open serverlist* and *Play offline*. It was reached two ways in the lab. **[live]**

| How the connection ended | Dialog text | *Play offline* goes to |
|--------------------------|-------------|------------------------|
| The listserver listed a server, but its game port refused the connection (TCP reset) | "The connection couldn't be established!" | `tutorial_b-4.graal` with the welcome sign, the same as Training. No level file was read from disk. |
| Logged in, then the game socket was destroyed from outside (`ss -K`) | "You have been disconnected from the game server." | The same level, reloaded from the game folder (`onlinestartlocal.nw`), with the player where they stood. |

Two lab notes:

- Closing the server side normally (a FIN) was not enough. The client left the socket half-closed and showed no dialog. The dialog came up only after a reset or a socket error.
- For the second row, a copy of the online level was in the game folder. The case where the level is not on disk was not repeated after a drop. The code says it falls back to the tutorial (see `offline-tutorial-205.md`).

## Built-in editor (2.05)

### Generate map (M)

After the "Generating the map may take some minutes. Proceed?" prompt, the editor works through the level list of the **currently loaded big map**. That is the list from `bigmap.txt`, or whichever list a `setmap` NPC loaded (for the tutorial, `tutorialmap.txt`). **[live][2.05]**

- It reads each listed level from disk in list order, row by row, and loads it as a level. Then it runs the level's NPCs into a 1024×1024 view and shrinks that to **56×56 px** in the output image. Missing or unreadable entries become blank squares.
- It does not follow links. Levels that are not in the list are skipped, for example `tutorial_b-2_house.graal`.
- The result is offered in a save dialog as `graalmap.png`, defaulting to the level's folder. With the 3×4 tutorial list it produced a 168×224 PNG.
- Afterwards, the level that was open in the editor is restored.

### Play saves first

Pressing *Play* on a named, modified level writes the level to disk ("Level saved" in the status bar) before the *Level options* dialog asks for the start position. **[live]** This matches the 2.22 behaviour in `tools/level-editor/222-reference.md`.

### Edit flags

*Edit flags* edits the client's in-memory flag list. Flags typed into it are still there after Play and a return to the editor. Nothing is written when the dialog closes or when the client exits: the test flag was not in any file in the game folder or the Wine prefix, nor in the registry. The list does not survive a restart. **[live]**

## 2.31 and GraalEditor

- The 2.31 start screen's **Editor** button starts `GraalEditor.exe` from the game folder as a separate process. The 2.31 client still has no editor forms of its own. **[live]**
- GraalEditor 2.3.1.1 runs under Wine. It opens on a new `new2.nw` tab with the four palette modes, including *Predefined NPCs*. **[live]**
- At startup it looks for `arrays2.sig`, `arrays2.dat`, `graaleditor.sig`, and `arrays.dat`. The shipped folder has no `GraalEditor.sig`, and the editor starts normally anyway. With one byte of `arrays2.sig` flipped, it also starts normally, with the same file reads and no message. Whatever the RSA check controls, it does not stop the editor from starting. **[live]**

## Sound (2.05)

With an audio device present, DirectSound starts and the client plays effects. Each effect shows up as a lookup of its file under `sounds\`, and that is how the rows below were matched to actions. Most rows were triggered in a test level: water, a pushable stone block, a bush, ledge rows, and chests. GS1 NPCs fired the remaining effects on staggered timers (`putbomb`, `putexplosion2`, `shoot*`, `putleaps`, `spyfire`, `lay`, `puthorse`, `putcomp`, `hurt`, `setgender`). **[live]** marks a sound heard in the running client. **[2.05]** marks a sound known only from the call sites of the sound routine.

| Action | Sound | Source |
|--------|-------|--------|
| Walking on ground | `steps2.wav` about every 0.2 s; `steps.wav` when a move starts | [live] |
| Swimming | `water.wav` about every 0.8 s | [live] |
| Riding a horse | `horse.wav` and `horse2.wav`, alternating about every 0.4 s | [live] |
| Sword swing | `sword.wav`; with the battle axe, `axe.wav` | [live] |
| Lifting a bush | `lift.wav` for a male player, `lift2.wav` for a female one (`setgender female`) | [live] |
| **Getting hurt** | the same `lift.wav` / `lift2.wav`: `hurt`, an explosion, a thrown ball or a baddy hit all play it | [live] |
| Dying | `dead.wav` | [live] |
| Laying a bomb | `put.wav` | [live] |
| Bomb or explosion | `bomb.wav` (`putbomb` of any power, `putexplosion`, `putexplosion2` power 2, the end of a fireblast or nuke) | [live] |
| Jolt explosion | `thunder.wav` (`putexplosion2` power 3) | [live] |
| Launching any projectile | `arrow.wav` for arrows, fireballs, fireblasts, nukes and `shootball`, and for arrows from shooting baddies and the dragon | [live] |
| Fire spy | `fire.wav` (`spyfire`) | [live] |
| A thrown object or leap landing | `crush.wav`; `water.wav` for the water leap (type 5) | [live] |
| Picking up a laid item (rupees, battle axe) | `extra.wav` | [live] |
| Opening a chest | `chest.wav`, also when the chest has a sign. No item sound follows. | [live] |
| Sign pages | `nextpage.wav` on every page turn | [live] |
| Pushing a stone block | `stonemove.wav` about once a second while it moves | [live] |
| Ledge jump | `jump.wav` | [live] |
| Frog | `frog.wav` when it hops | [live] |
| Baddy walking | `steps.wav` | [live] |
| Baddy dies | `compudead.wav` | [live] |
| Baddy draws its sword | `swordon.wav`. Six baddy types were tried; none played it. | [2.05] |
| An arrow hitting the player | `arrowon.wav`. Not reached: no test arrow hit the player. | [2.05] |
| `item.wav`, `item2.wav` | Only used in the sign-reading routine and in a server-message handler. The chest and laid-item tests didn't play them. | [2.05] |
| Another player's bomb or item (online) | `bomb.wav` / `thunder.wav`, `item.wav`, `extra.wav`, from server messages | [2.05][inf] |
| GANI `PLAYSOUND`, GS1 `play` / `playlooped` | the named file | [2.05] |

The lift/hurt sound is picked by a single byte on the player object: `lift.wav` when it is set, `lift2.wav` when clear. New players start with it set. That `setgender female` clears it is inferred from the sound changing. **[2.05][inf]**

## Corrections to earlier notes

- `offline-tutorial-205.md` said there is no offline item on the start screen. There is: **Training**. It is the usual way in, and *Play offline* on the reconnect dialog is the other.
- `offline-tutorial-205.md` and `tools/graaleditor-vs-205.md` said only 2.22 reads `tiledefsOffline.txt`. 2.05 and 2.31 read it too (see above).
- `tools/graaleditor-vs-205.md` said 2.31 has no editor. It has no editor *forms*, but its start screen launches GraalEditor.
- `level-editor-205.md` listed Generate map and Edit flags as open. Both are answered above.
- The first version of the sound table in this note guessed that `lift2.wav` is for heavy objects and that `fire.wav` is the fireball. Both were wrong. `lift2.wav` is the female lift and hurt sound, every projectile launches with `arrow.wav`, and `fire.wav` belongs to `spyfire`.
