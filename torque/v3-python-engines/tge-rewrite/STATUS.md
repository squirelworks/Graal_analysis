# Status

Surface list: `used.md`. Code: `engine/`. The Mac image is `MacGraal_v304`. This is a terminal canvas, not a windowed OpenGL view.

## What runs today

- `SimObject` / `SimSet` with the methods read from a client routine.
- A console that evals `echo`, `set`, `createCanvas`, `start2D`, `resetCanvas`, `Canvas.setContent`, `Canvas.pushDialog`, `Canvas.popDialog`, and the `GuiGraalCtrl` move and `loadLevel` methods.
- One object per `Gui*` control string. `GuiCanvas` and `GuiGraalCtrl` have the methods from a client routine and a client routine. The rest render nothing.
- A 9×9 text grid of the 64×64 `BOARD`, player marked `@`.
- `NetConnection.connect` / `getAddress`, with the Torque stat methods as empty returns.
- `engine/main.py --listen PORT` accepts the other science task’s client, prints id 5 and id 37, and replies with inbound id 0.

Checked: `engine/main.py --steps right,up` loads `engine/examples/tiny.nw`, steps to 1,0, and blocks the next `up` on the 64-bound. `--listen` against `v3-python-repro/python/client.py --host localhost` completed the login exchange.

## What is still a stub

- `GuiTSCtrl`, `GuiGraal3DCtrl`, profiles, huds, PM controls, `ShapeBase`, `Camera`, `Interior`, and `Terrain*` have names and no behavior.
- `GameConnection` ghosting, demo record, and 3D audio are not implemented.
- Move distance is one board cell. The binary does not say that. `walk` / `walkslow` are not frames.
- Tile art is the hex of the stored `uint16`. No png blit.
- The outer flush (length header, mode byte, LCG, a client routine, a client routine) is not on the socket. The host speaks the inner newline records the Python client sends by default.
- `echo` is implemented. The registrar body that binds the real `echo` builtin was not fully listed.

## What would make it host the Python v3 client

The listen path already accepts that client’s id 5 (`G3D28015` plus two strings) and id 37, and the client’s parser accepts the id 0 reply.

To play a level through that socket, the host would have to send the inbound ids a client routine understands (0–10) as the level and the player, and the client would have to apply them. Today the client only prints the reply. It does not load the host’s board. The host also does not wrap writes in a client routine, so a build that set the codec mode would not match.
