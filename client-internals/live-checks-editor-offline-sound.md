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

### Start without a network

Pressing *Start* in 2.05 with no listserver shows "The connection couldn't be established!" and stays on the server list. That screen has no *Play offline* button. The *&Play offline* button belongs to the reconnect dialog, which appears after a game-server connection fails or drops. In the lab, killing the stub game server while logged in left the client with a half-closed socket, and it stopped updating, so the reconnect dialog was not reached live. **[live]**

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

With an audio device present, DirectSound starts and the client plays effects. A play shows up as a lookup of the file in `sounds\`, and that is how the live rows below were matched to actions. **[live]** marks a sound seen in the running client; the rest come from the call sites of the 2.05 sound routine. **[2.05]**

| Action | Sound | Source |
|--------|-------|--------|
| Walking on ground | `steps2.wav` on every 5th movement tick (0.2 s apart in the trace); `steps.wav` at the start of a move | [live] |
| Walking in shallow water | `water.wav` on every 15th movement tick | [2.05] |
| Riding a horse | `horse2.wav` at walking speed, `horse.wav` when faster | [2.05] |
| Sword swing | `sword.wav`; `axe.wav` from the same routine, presumably for the battle axe | [live] (sword), [inf] (axe) |
| Lifting or picking up (bush, pot, own bomb) | `lift.wav`, or `lift2.wav`, chosen by a flag on the lifted object | [live] (lift) |
| Putting down, or laying a bomb | `put.wav` | [live] |
| Bomb explosion | `bomb.wav`; the explosion routine also has `thunder.wav`, presumably for the superbomb | [live] (bomb), [inf] (thunder) |
| A thrown object landing | `crush.wav`, or `water.wav` in water | [live] (crush) |
| Arrow flying, or being shot | `arrow.wav`; `arrowon.wav` when an arrow hits the player | [2.05] |
| Fireball | `fire.wav` | [2.05] |
| Item pickup | `item.wav` (`item2.wav` for some items) | [2.05] |
| Extra item laid or picked up | `extra.wav` | [2.05] |
| Opening a chest | `chest.wav` | [2.05] |
| Sign pages | `nextpage.wav` on every page turn | [live] |
| Pushing, jumping | `stonemove.wav`, `jump.wav` | from the player movement routine; most likely pushing a stone and the ledge jump [2.05][inf] |
| Baddy draws its sword / walks / frog jumps / dies | `swordon.wav`, `steps.wav`, `frog.wav`, `compudead.wav` | [2.05] |
| Another player's bomb or item (online) | `bomb.wav` / `thunder.wav`, `item.wav`, `extra.wav`, played from server messages | [2.05][inf] |
| GANI `PLAYSOUND`, GS1 `play` / `playlooped` | the named file | [2.05] |

## Corrections to earlier notes

- `offline-tutorial-205.md` said there is no offline item on the start screen. There is: **Training**. It is the usual way in, and *Play offline* on the reconnect dialog is the other.
- `offline-tutorial-205.md` and `tools/graaleditor-vs-205.md` said only 2.22 reads `tiledefsOffline.txt`. 2.05 and 2.31 read it too (see above).
- `tools/graaleditor-vs-205.md` said 2.31 has no editor. It has no editor *forms*, but its start screen launches GraalEditor.
- `level-editor-205.md` listed Generate map and Edit flags as open. Both are answered above.
