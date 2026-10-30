# Offline mode and the embedded tutorial (client 2.05 rev 2)

Date: 2026-10-21

Derived from the 2.05 rev 2 binary (resources, strings, and the offline and level-load paths) and from decoding the embedded levels with `formats/grv1-decoder/grv1.py`. Names only, no code. Tags: **[2.05]** · **[2.22]** · **[inf]**.

This note refines `offline-play.md` and `offline-training.md`.

## How the client goes offline

Offline play is reached in these ways:

1. **Training on the start screen.** It starts the embedded tutorial at `tutorial_b-4.graal` with no connection (confirmed live, see `live-checks-editor-offline-sound.md`). **[2.05]**
2. **"&Play offline" on the reconnect dialog** (`TReconnectFrame`). The dialog appears when the connection fails or drops ("The connection could not be established!", "You have been disconnected from the game server.", "There are too many players online."). Choosing *Play offline* frees the game socket, so the connection object is nil from then on. **[2.05]**
3. **Command line.** `Graal.exe level.graal` starts with a local player and opens that file in the editor. Play then runs it offline (see `level-editor-205.md`).
4. **F5 Load level** while online. The client warns "When you load a level you will be disconnected from the server. Continue?" and then loads the file locally.

"Offline" in the client simply means *no game connection object*. Every check that refuses the editor, enables the tutorial resources, or sends file requests tests that one condition.

### Where the player lands

When *Play offline* is chosen:

- If the level the player was on exists in the local folder, the player stays on it at the same coordinates.
- Otherwise the player is moved to **`tutorial_b-4.graal` at (32, 60)**. The map overlays are switched to the tutorial set: `tutorialmap.png` / `tutorialmap.txt` for the big map and `tutorialmap2.png` / `tutorialmap.txt` for the minimap. A "first offline start" flag is also set.
- If the level still fails to load, a warning names the level and the client stays at the reconnect dialog.

Both of the first two cases were seen live: after a refused connection the player went to the tutorial, and after a drop on a level that was also on disk the client reloaded that level at the same spot (see `live-checks-editor-offline-sound.md`).

## Where offline levels come from

The level loader checks two sources in order. **[2.05]**

1. **Embedded tutorial.** When offline, and the name starts with `tutorial`, the loader maps the file name to an `RCDATA` resource and reads the level from the executable.
2. **Disk.** Otherwise it looks the name up through the file-name cache and reads the file from disk.

The embedded copy wins: with a `tutorial_b-4.graal` of different content in the game folder, the client still loads the embedded level and does not look for the file (live).

Online, names starting with `tutorial` are not special. They go to the server like any other level.

| Level file | Resource |
|------------|----------|
| `tutorial_a-1.graal` … `tutorial_a-4.graal` | `TUTORIALA1` … `TUTORIALA4` |
| `tutorial_b-1.graal` … `tutorial_b-4.graal` | `TUTORIALB1` … `TUTORIALB4` |
| `tutorial_b-2_house.graal` | `TUTORIALB2H` |
| `tutorial_c-1.graal` … `tutorial_c-4.graal` | `TUTORIALC1` … `TUTORIALC4` |

All 13 are `GR-V1.03` binary levels (see `formats/level-binary.md`).

### Special level names

Three level names trigger an extra setup step when loaded: `level1.graal`, `YoshiClanR2.zelda`, and `YoshiClanFields.zelda`. These are the original single-player start levels. What the step does has not been traced. **[2.05]**

## The tutorial world

The levels form a 3×4 grid: letters are columns from west to east, digits are rows from north to south. Edge links use `playerx` / `playery` to keep the other coordinate, landing at 0 or 61 on the far side.

```
        a        b                     c
  1   a-1  ──  b-1                 ──  c-1
       │        │                       │
  2   a-2  ──  b-2 (+ b-2_house)   ──  c-2
       │        │                       │
  3   a-3  ──  b-3                 ──  c-3
       │        │                       │
  4   a-4  ──  b-4  START (32,60)  ──  c-4
```

| Level | Links | NPCs | Chests | Signs | Content |
|-------|-------|------|--------|-------|---------|
| a-1 … a-4, c-1 … c-4, b-1 | 2–3 | 0 | 0 | 0 | Scenery only |
| **b-4** (start) | 3 | 8 | 1 | 3 | Welcome sign ("In this tutorial you will learn … say the password 'Balibu'"). A gate NPC opens when the player chats `Balibu` and stands in a y range. A `setmap tutorialmap.png …` / `setminimap …` NPC. Two light NPCs (`drawaslight`, `setcoloreffect`). Two character NPCs. The chest holds `glove1` (the red power glove) with sign 0: "Go to the stone, press … to lift it!" |
| b-3 | 4 | 0 | 0 | 1 | Sign at (36, 37): "Use the sword to cut those trees!" |
| b-2 | 5 | 5 | 0 | 2 | An arrow box NPC (`lay darts`). A door NPC that opens on the `opendoors` flag and plays `chest.wav`. Character NPCs. The link into the house is at (22, 26). The signs explain shooting statues to open the door, then "Excellent! You got the treasures! … Press F8!" |
| b-2_house | 1 | 6 | 6 | 7 | A shopkeeper ("give me 5 rupees", how to drop a rupee). A house gate NPC that slides open on the `housegateopen` flag with `stonemove.wav`. Two lamps, two lights. Six chests: battleaxe, lizardshield, spinattack, nukeshot, fullheart, superbomb, each with its own sign. |

The tutorial ends by sending the player to **F8** (server list) to go online.

Signs at (0, 0) are not drawn on the board. Chests and the `say n` command show them by index. Six of the seven house signs are chest signs.

## Later clients

- **2.17, 2.22 and 2.31** keep embedded tutorials but trim them to a 3×3 grid of 9 levels named `offlinetutorial_a-1.graal` … `offlinetutorial_c-3.graal` (resources `TUTORIALA1` … `TUTORIALC3`, still `GR-V1.03`). Training starts on `offlinetutorial_b-2.graal`, the centre of the grid (2.22 and 2.31, live). **[2.17][2.22][2.31]**
- Offline, every client tested (2.05, 2.22, 2.31) reads `levels/tiledefs/tiledefsOffline.txt`, because the tile-definition file name is `tiledefs` + server name + `.txt` and the offline server name is `Offline`. The shipped file only targets `offlinetutorial*` levels, so it has no effect on the 2.05 tutorial. **[live]**
- The standalone GraalEditor 2.3.1.1 carries the same 9 `offlinetutorial_*` names and `tiledefsOffline.txt`. **[inf from strings]**

## Offline implications

- An offline reimplementation that wants the original first-run experience needs the 13 resources and the `tutorial*` resource lookup. Decoded copies can be produced locally with the decoder. The levels are not committed here.
- The resource mapping applies only when the client has no connection, so a server can host its own `tutorial_*.graal` levels without conflict.
