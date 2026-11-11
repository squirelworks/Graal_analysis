<!-- manual: kind=reference status=draft -->
# 4.8 Offline and training mode

This chapter gives how the client plays without a game server: the ways in, where the player lands, where offline levels come from and what the embedded tutorial holds. The tutorial's level resources are in → §3.1.2.8; the level formats in → §3.1.

> Status: draft. Read from 2.05 rev 2 and checked live on 2.05 rev 2, 2.22 and 2.31; the special single-player level names are open (→ App. E#319).

## 4.8.1 What offline means

| Rule | Detail | Source |
| --- | --- | --- |
| condition | offline means the client has no game connection object; every check that refuses the editor, enables the tutorial resources or sends file requests tests that one condition | [2.05] (client-internals/offline-tutorial-205.md#how-the-client-goes-offline) |
| current level name | the global that holds the current level name is set only by the server's set-level message, so it stays empty in offline training; the level is still drawn and walked | [live] (client-internals/offline-training.md#difference-from-session-levels) |
| same rules | entering an offline level stores the level name and arrival point on the player; collision, signs, links and scripts run the same paths as for a disk level online | [live] (client-internals/offline-training.md#enter-path) |

## 4.8.2 Ways in (2.05)

| Way | Detail | Source |
| --- | --- | --- |
| Training | a button on the start screen; starts the embedded tutorial at `tutorial_b-4.graal` and makes no connection | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#the-training-button) |
| Play offline | a button of the reconnect dialog, beside Reconnect and Open serverlist; choosing it frees the game socket | [2.05][live] (client-internals/offline-tutorial-205.md#how-the-client-goes-offline); [live] (client-internals/live-checks-editor-offline-sound.md#the-reconnect-dialog-and-play-offline) |
| command line | `Graal.exe level.graal` starts with a local player and opens the file in the editor; Play then runs it offline (→ §4.9) | [2.05] (client-internals/offline-tutorial-205.md#how-the-client-goes-offline) |
| F5 Load level | while online the client warns that loading a level disconnects from the server, then loads the file locally | [2.05] (client-internals/offline-tutorial-205.md#how-the-client-goes-offline) |

### 4.8.2.1 The reconnect dialog

| Rule | Detail | Source |
| --- | --- | --- |
| texts | shown when the connection cannot be established, is dropped, or the server is full | [2.05] (client-internals/offline-tutorial-205.md#how-the-client-goes-offline) |
| no listserver | pressing Start with no listserver shows the connection error and stays on the server list, which has no Play offline button | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#the-reconnect-dialog-and-play-offline) |
| refused game port | the dialog appears; Play offline goes to the tutorial start, reading no level file from disk | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#the-reconnect-dialog-and-play-offline) |
| dropped after login | the dialog appears; Play offline reloads the current level from the game folder with the player where they stood | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#the-reconnect-dialog-and-play-offline) |
| half-closed socket | a normal close from the server side left the socket half-closed and showed no dialog; only a reset or socket error brought it up | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#the-reconnect-dialog-and-play-offline) |

### 4.8.2.2 Where the player lands on Play offline

| Case | Result | Source |
| --- | --- | --- |
| the current level exists in the local folder | the player stays on it at the same coordinates | [2.05][live] (client-internals/offline-tutorial-205.md#where-the-player-lands) |
| it does not | the player goes to `tutorial_b-4.graal` at (32, 60); the big map switches to `tutorialmap.png` and the minimap to `tutorialmap2.png`, both with `tutorialmap.txt`; a first-offline-start flag is set | [2.05][live] (client-internals/offline-tutorial-205.md#where-the-player-lands) |
| the level still fails to load | a warning names the level and the client stays at the reconnect dialog | [2.05] (client-internals/offline-tutorial-205.md#where-the-player-lands) |
| dropped on a level not on disk | not repeated live; the code falls back to the tutorial | [2.05] (client-internals/live-checks-editor-offline-sound.md#the-reconnect-dialog-and-play-offline) |

## 4.8.3 Where offline levels come from

| Rule | Detail | Source |
| --- | --- | --- |
| order | offline, a name starting with `tutorial` is read from the executable's resource (→ §3.1.2.8); any other name goes through the file-name cache to disk | [2.05] (client-internals/offline-tutorial-205.md#where-offline-levels-come-from) |
| embedded wins, 2.05 | with a different `tutorial_b-4.graal` in the game folder, Training still loads the embedded level and does not look on disk | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#the-embedded-level-always-wins) |
| embedded wins, 2.22 | with `offlinetutorial_b-2.graal` in the game folder, the client looks the name up once but still loads the embedded copy | [live][2.22] (client-internals/live-checks-editor-offline-sound.md#the-embedded-level-always-wins) |
| online | names starting with `tutorial` are not special and go to the server like any level, so a server can host its own | [2.05] (client-internals/offline-tutorial-205.md#where-offline-levels-come-from) |
| tile definitions | every client tested reads `levels/tiledefs/tiledefsOffline.txt` on Training, since the file is `tiledefs` + server name + `.txt` and the offline server name is `Offline`; the shipped file targets only `offlinetutorial*` levels, so it changes nothing in 2.05's tutorial | [live][2.05][2.22] (client-internals/live-checks-editor-offline-sound.md#tile-definitions-when-offline) |
| special names | `level1.graal`, `YoshiClanR2.zelda` and `YoshiClanFields.zelda`, the old single-player start levels, run an extra setup step on load; what it does is unmeasured (→ App. E#319) | [2.05] (client-internals/offline-tutorial-205.md#special-level-names) |

## 4.8.4 The tutorial world

### 4.8.4.1 2.05

| Rule | Detail | Source |
| --- | --- | --- |
| grid | 3 columns (a to c, west to east) by 4 rows (1 to 4, north to south), plus `tutorial_b-2_house.graal` linked from b-2 at (22, 26); edge links keep the other coordinate and land at 0 or 61 | [test] (client-internals/offline-tutorial-205.md#the-tutorial-world) |
| scenery levels | a-1 to a-4, c-1 to c-4 and b-1: 2 or 3 links, no NPCs, chests or signs | [test] (client-internals/offline-tutorial-205.md#the-tutorial-world) |
| b-4, the start | 8 NPCs, 1 chest, 3 signs: a welcome sign, a gate NPC that opens when the player says the word the sign gives while standing in a band of rows, a `setmap` and `setminimap` NPC, two light NPCs and two character NPCs; the chest holds `glove1` | [test] (client-internals/offline-tutorial-205.md#the-tutorial-world) |
| b-3 | a sign telling the player to cut the trees with the sword | [test] (client-internals/offline-tutorial-205.md#the-tutorial-world) |
| b-2 | 5 NPCs, 2 signs: an arrow box, a door that opens on the `opendoors` flag with `chest.wav`, character NPCs | [test] (client-internals/offline-tutorial-205.md#the-tutorial-world) |
| b-2 house | 6 NPCs, 6 chests, 7 signs: a shopkeeper, a gate that slides open on `housegateopen` with `stonemove.wav`, lamps and lights; the chests hold battleaxe, lizardshield, spinattack, nukeshot, fullheart and superbomb | [test] (client-internals/offline-tutorial-205.md#the-tutorial-world) |
| signs at (0, 0) | not drawn on the board; chests and `say n` show them by index | [test] (client-internals/offline-tutorial-205.md#the-tutorial-world) |
| end | the last sign sends the player to F8, the server list, to go online | [test] (client-internals/offline-tutorial-205.md#the-tutorial-world) |
| map | `tutorialmap.txt`, set by the start level's `setmap` NPC | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#the-training-button) |

### 4.8.4.2 Later builds

| Builds | Detail | Source |
| --- | --- | --- |
| 2.17, 2.22, 2.31 | 9 embedded `GR-V1.03` levels, `offlinetutorial_a-1.graal` to `offlinetutorial_c-3.graal` | [2.17][2.22][2.31] (client-internals/offline-tutorial-205.md#later-clients) |
| 2.22, 2.31 | Training starts on `offlinetutorial_b-2.graal`, the centre of the grid; its NPCs play `cauldron_bubbles.wav` and `fire_torch0` to `fire_torch2` as soon as it loads; the maps are the client's own `bigmap.txt` and `minimap.txt` plus per-level map parts | [live] (client-internals/live-checks-editor-offline-sound.md#the-training-button) |
| start screens | 2.05: Training, Options, Start; 2.22 adds Get an account!; 2.31 adds Editor, which launches the separate GraalEditor (→ §11.6) | [live] (client-internals/live-checks-editor-offline-sound.md#the-training-button) |
| GraalEditor 2.3.1.1 | carries the same 9 names and `tiledefsOffline.txt` | [inf] (client-internals/offline-tutorial-205.md#later-clients) |

## 4.8.5 Windows 4.04r2: bounded initialization evidence

| Condition | Before | After or observed result | Limit | Source |
| --- | --- | --- | --- | --- |
| Controlled startup, no server or login | Client initialization | Native game/UI window construction, successful DirectDraw initialization call, and opens of configuration, cache, GUI assets and four supplied animations | Window visibility, successful decoding and a rendered gameplay scene are unmeasured by these hooks | [cap] (version-profiles/windows-404r2-teardown.md#startup-capture) |
| Harness invokes an internal offline transition on the UI thread | No adventure object | Offline-mode flag set; adventure object allocated; observed message-loop callbacks continue for 20.031 seconds after the call returns | Instrumented invocation, not a normal user action or documented API; a playable level, movement and bush interactions remain unmeasured by this capture | [cap] (version-profiles/windows-404r2-teardown.md#controlled-offline-transition) |

These observations do not establish that 4.04r2 uses the 2.05 entry conditions or arrival rules in → §4.8.1–4.8.2. Earlier unsuccessful harness attempts are not successful offline sessions. [cap] (version-profiles/windows-404r2-teardown.md#controlled-offline-transition)

Remaining scene and mechanic validation: → App. E#610.
