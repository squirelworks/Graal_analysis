# Working plan

Private tree. Evidence for the Mac image stays in `v3-tge-rewrite/used.md` and `v3-python-repro/teardown/`. `STATUS.md` is what this code does.

The finished product is a v3 client that can do what a v2 client can do. The v2 behaviour is the study in [squirelworks/Graal_analysis](https://github.com/squirelworks/Graal_analysis). The v3 method names are the ones a client routine registers. A v2 rule is coded only when that study states it. It is not a claim that the Mac image was re-read for that rule.

## Local play

| Action | v2 source | Here |
| --- | --- | --- |
| Load a `.nw` | `formats/glevnw01.txt` | `Level.load` reads `GLEVNW01` and `GSERVL01`. Tiles use the Mac 62-character alphabet. `+` and `/` are the study's two extra characters so a tile that alphabet cannot spell still reloads. |
| Walk `moveUp/Left/Down/Right` | the four keys | Coded. Plain step is 0.5. Hidden walk is that step times 0.2, which is the 2.05 factor (`carry-hide-and-glove.md`). |
| Pick up a bush or a rock, `doA` | lift table in `board-respawn.md`. Glove 1 lifts bush, sign, pot. The stone is entry 4 and needs glove 2. | Coded. `examples/yard.nw` has the bush. Glove stays 1 unless set. |
| Hide under a bush, `doD` | sprites 261, 263, 239. A pot or a sign does not hide. | Coded. |
| Throw, `doS` | S throws, including from hiding. Landing does not write the board. | Coded. The carried object is cleared. Flight was not read in the study, so there is no arc. |
| Open a chest when facing it | closed tiles 1784 1785 / 1800 1801 become 829 830 / 845 846. A `CHEST` record opens and shows its sign. | Coded. The study did not say whether the chest is tried before the sign. Lift is first, then the chest, then the sign. |
| Read a sign | three lines a page. The map key closes it. A sign at (0, 0) is kept by index. | Coded. `doA` turns the page. `doM` closes it. |

The tile-type reject in a client routine is still unread. Walking does not stop on a wall.

## Online

| Action | v2 / v3 source | Here |
| --- | --- | --- |
| Open the server list | v3 method `openServerList`. Lister id 0 is a client routine. | A list payload fills the rows. Field 5 is a client routine. |
| `connectToSelectedServer` | a client routine reads fields 6 and 7 | Stores `host:port`. `--connect selected` dials that address. |
| Login line | id 5, then id 37. a client routine. | The frame is sent. Account and password are the CLI strings. The Mac fields a client field and a client global are still unread. |
| Receive a board and draw it | game id 0, a client routine | Rectangle runs replace the 64-wide tiles and the grid draws them. |
| Other players | game id 2, a client routine | Field 1 and field 2 are drawn. Field 3 is unnamed. |
| Movement other players can see | the flag path a client routine | Not sent. The step is local. `step_send_not_in_00310b0c`. |
| `setChat` | a client routine id 0x16, then a client routine | The inner bytes are printed. The XOR inputs are unread, so no datagram is sent. |
| Request a missing file | a client routine id 0x17, at most four, skip `.gft` | The names ride the second login flush. Id 0x84 writes a wanted file into `engine/store/`. |

GServer-v2 remains the host this login is aimed at. UDP stays the conditional track in the previous plan: the Mac socket opens only when `noudp` is off, and that server does not read it.

## GUI

| Piece | v2 source | Here |
| --- | --- | --- |
| `GuiCanvas` methods | a client routine | Already the content, dialog stack, cursor, and repaint. |
| Server list | `openServerList` | Text block under the grid. |
| Player list | 2.05 F7. This image has `GuiPlayerView` and no method of that name. | `showPlayerList` is the local window. |
| Chat bar | `setChat`, control name `ChatBar` | The line is the `chat:` row. |
| Level editor | 2.05 F4 (`level-editor-205.md`): place tiles, an NPC, save. Refused while online. | `editorOpen`, `editorPlaceTile`, `editorPlaceNpc`, `editorSave`. One NPC is a stub script line. Undo, stamps, and the link dialog are not in this pass. |
| Options | volumes, nickname, account | `setNickName`, `setAccountName`, `setPassWord`, and the four volume methods store the value. They do not change a sound device. |

The picture is still the text grid. A window toolkit waits until a received board is the thing on that grid.

## Next

1. The three bytes a client routine XORs, then the chat datagram can be sent.
2. The send that should follow a client routine, if one exists outside a client routine.
3. What a client routine is numbering on the id 0x22 file list.
4. The wall test, when a client routine is reduced to tile types.

## Stop rules

- An unread Mac body stays a stub with its function name.
- Do not patch GServer-v2.
- Do not open a Themida image.
- Do not write under `Graal_analysis` or a public repo.
- New code stays in `v3-combined/engine/`.
