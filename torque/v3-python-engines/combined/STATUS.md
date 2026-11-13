# Combined v3 path

Code is `engine/`. The lists it follows are still `v3-tge-rewrite/used.md` and `v3-python-repro/teardown/`. Those files were not rewritten.

## What main does today

`engine/main.py` builds a `GuiCanvas`, evals `createCanvas`, `start2D`, and `Canvas.setContent(GraalCtrl)`, and loads a local `GLEVNW01`. `--steps right,up` moves by the recovered plain step, to `0.5,-0.5`. The same position is copied onto `GuiTSCtrl`, `GuiGraal3DCtrl`, and `Camera`.

`--listen` accepts the inner newline records (id 5 with `G3D28015`, then id 37) and answers with id 0. `--inner` sends those same records. `v3-python-repro/python/client.py` can talk to this `--listen` as well.

`--connect` / `--framed-listen` follow a client routine: the id 5 record is flushed, then the id 37 record is flushed. The first frame is mode 3 (zlib, 2-byte length, no XOR). The second is mode 2 and is XORed with the session key. A local listener recovers `G3D28015` and `E\n`.

## Torque classes

Methods that are real, from the registrar that listed them:

| class | registrar | what runs |
| --- | --- | --- |
| `GuiCanvas` | a client routine | content, dialog stack, cursor, filters, repaint |
| `GuiGraalCtrl` | a client routine | the four moves, `loadLevel`, account, server, and the volume and option methods |
| `SimObject` / `SimSet` | a client routine | name, id, set membership |
| `NetConnection` | a client routine | address and the stat calls, which only record |
| `GameConnection` | a client routine | ghosting, demo, and camera calls, which only record |
| `Camera` | a client routine | `getPosition` returns the cell; `setOrbitMode` and `setFlyMode` record |
| `AdvancedCamera` | a client routine | the 25 listed methods record their arguments |
| console | a client routine, a client routine, a client routine | `echo`, `eval` of a semicolon script, `exec` of a file or a string, the string helpers, `isObject`, `nameToID`, `schedule`, `cancel`, `isEventPending` |

`GuiTSCtrl` and `GuiGraal3DCtrl` still have no methods in those functions. They hold the level and the cell that `GuiGraalCtrl` writes. `GuiGraal3DCtrl.activated` stays false. The string `Graal3D activated!` belongs to a client routine, a client routine, and a client routine, and no opened function sets the flag.

`ShapeBase` still has no method list. `GuiBitmapCtrl` holds the tile words. The remaining `Gui*` names in `used.md` are still empty subclasses.

A move stores a 0 or 1 in the direction slot and, when the flag is 1, adds the plain step from a client routine: the unit vector `(0,-1)`, `(-1,0)`, `(0,1)`, `(1,0)` times `0.5`. The destination is not rejected in this engine. a client routine undoes that step when six samples from a client routine are not all zero, and those return values were not mapped to tile types.

`getVersionString` still returns the stand-in `G3D28015`. a client routine registers the command and its return text was not read.

## Outer flush

Both transforms are real. a client routine is zlib 1.1.3 `compress` (a client routine, `deflateInit_` level -1, version `1.1.3`). Modes 3 and 4 use it. a client routine is bzip2 1.0.2 `BZ2_bzBuffToBuffCompress` with block size 5, verbosity 0, and work factor 30. Modes 5 and 6 use it. The engine's zlib is the 1.1.3 library in `engine/libz113.so`. The bzip2 call uses the host libbz2 1.0.8.

a client routine writes the session key before the first flush. `+0x8` is the constant an address. `+0x10` is `time()` masked with `0x7f`. `+0x14` starts at 3, so the first flush is zlib with a 2-byte length and no XOR, and the flush then stores 0 back into `+0x14`. The id 37 record is the second flush. It is short, so it is mode 2 and the LCG uses that key.

## Step

`GuiGraalCtrl.move*` does not add a coordinate itself. a client routine and the three neighbors store the a client routine flag. a client routine adds the direction unit times `0.5` for the plain scale (`DOUBLE_006481e8`). Up is `(0,-1)`, left is `(-1,0)`, down is `(0,1)`, right is `(1,0)`, from the doubles at the pointer in a client global.

The coded rule does not reject the destination. The binary undoes the step in a client routine when the six a client routine samples are not all zero. That function was not reduced to a list of blocking tile types.

## Local actions from the v2 study

`engine/play.py` is the 2.05 lift, hide, throw, chest, and sign, cited in `ROADMAP.md`. `examples/yard.nw` holds a bush, a closed chest, a sign, and an NPC stub. `doA` on the bush leaves tiles 677 678 / 693 694 and carries it. `doD` hides. The next step is 0.1. `doS` clears the carry and does not write the board. Glove 1 does not lift the stone. Glove 2 does. A chest facing the player becomes tiles 829 830 / 845 846. A sign shows three lines, and the next `doA` closes a two-line sign. `editorSave` writes a `GLEVNW01` this loader reads back. `requestFile` queues a missing name and reports a file already in `engine/store/`.

## Packets read from the Mac image

The list connection and the game connection are different switches.

The lister's id 0 is a client routine. A gchar count, then each row's gchar field count, then short fields. The dialog shows field 0 and field 5. a client routine reads the name prefix: `3 ` category 1, `P ` category 0, `U ` hidden, `H ` category 2, and no prefix category 3. Category 2 keeps the prefix. The others drop two characters. Fields 6 and 7 are the host and the port. a client routine parses field 5 and the port: empty is an address, `true` is 1, `false` is 0, `0x` is hex, and the rest is atoi. `connectToSelectedServer` stores `host:port`. Ids 1, 2, and 4 on that connection are an ignored copy, `AccountInfo.setText`, and `ServerLister` / `MessageBoxOK`. They are not the row parser.

Game id 0 is a client routine into a client routine. Each run is x, y, width, height as `byte-0x20`, then `width*height` tiles of two bytes, `(first-0x20)*0x80 + (second-0x20)`, written on the 64-wide board at `(y*64+x)`. A short run stops the packet. a client routine looks the level up in a 3 by 3 table and returns -1, -1 when this client has no table. a client routine blits the rectangle against the camera. The camera window at player+0x388 is unread. The tiles are already stored before that blit.

Game id 2 is a client routine. The first byte minus 0x20 selects the player. a client routine then reads the same bytes. Field 1 is x and field 2 is y, each `(byte-0x20)*0.5` clamped to 0..63. Field 0 replaces the stored id. Field 3 is the unnamed byte at player+0x3a (`player_field_3_unnamed`). Field 7 is `(byte-0x20)>>2` and `(byte-0x20)&3`. Nothing in that function is named direction. A player with no x and y is not drawn.

`setChat` reaches a client routine, which truncates to 0xdc and calls a client routine with id 0x16. The inner bytes are `gchar(0x16)` plus the text. a client routine prepends the byte at player+0x1cf and XORs every byte with the low byte of player+0x1ec and the low byte of the object at a client global field +0x1ec. Those three values are unread, so `setChat` does not build the datagram. a client routine is `sendto` of that buffer to the four address bytes at player+0x314 and the port at +0x31a. `--chat` prints the inner bytes and does not write them on the TCP socket.

`move*` stores a flag in the eleven-word array a client routine writes. a client routine copies it onto the player. a client routine calls a client routine, which calls a client routine for a direction. That path does not send. The stub is `step_send_not_in_00310b0c`.

`requestFile` skips a name whose tail from the last `.` is `.gft` (a client routine walks backward, a client routine). Other names, at most four, go out as id 0x17 with the raw filename on the second login flush. The five-gchar prefix a client routine builds for id 0x22 is unread (`file_prefix_00330c34`). Game id 0x84 is a short name and then the bytes. a client routine delivers them only when that name is already wanted, and this client writes those bytes under `engine/store/`.

## Next gap

The two login strings are still unread in the Mac image. String A is the field at a client field and string B is a client global. The 3.x study names them account and password. This client still sends the account and second string it was given. The open stubs are `player_field_3_unnamed`, the three a client routine inputs, `file_prefix_00330c34`, the camera window in a client routine, and `step_send_not_in_00310b0c`.
