# Do 2D level packets arrive or draw in a 3D session? (T3D-060, Linux 4.20r6)

Date: 2026-11-25. Loopback lab of the Linux 4.20r6 client against our own 3D lab server, with the 2D TCP link decoded and able to inject chosen server-to-client packets (runs `lvl420-a`, `lvl420-b`; no movement input). Linux 4.20r6 is 3D-equal to Windows 4.20r8 ([T3D-004](3d-engines-5007-512-and-403-411-2026-11-25.md#t3d-004-linux-and-mac-against-their-windows-twins)). Board row: [T3D-060](3d-capability-board.tsv).

Once the 3D world was up (one reference GameObject cube), the server sent normal 2D level content the way a 2D client would get it, and the 3D view was shot after each.

| Sent | id | Body |
| --- | --- | --- |
| `PLO_LEVELNAME` | 6 | a level name |
| `PLO_BOARDPACKET` | 101 | a full 64×64 board |
| `PLO_NPCPROPS` | 3 | two NPCs with served images and positions |
| `PLO_LEVELSIGN` | 5 | a sign with text |
| `PLO_LEVELLINK` | 1 | a warp link |
| `PLO_LEVELCHEST` | 4 | a chest |
| `PLO_BADDYPROPS` | 2 | a baddy with a position and image |

The gserver also sends a real 2D level at login on its own (`PLO_LEVELNAME`, a `PLO_BOARDPACKET` and chests for the world's start level), so 2D level content reaches a 3D session even with no injection.

## Results **[lab]**

- **All of it arrived** and the client accepted it without disconnecting: the heartbeats continued and the server logged no drop.
- **Nothing from it was drawn.** All ten screenshots are byte-identical to the plain 3D view (the cube, sky and ground). No board tiles, NPC or baddy billboard, sign or overlay.
- **The client acted on none of it.** After the shape's own file requests it sent no further TCP packets except heartbeats, and notably never requested the 2D NPC or baddy images, which a 2D client always does. So it does not even turn the 2D NPC props into a drawable object.
- Repeats had no effect, and there is no 2D view to switch to on this route (the session is in 3D mode throughout).

The 4.20r6 client draws the scene through its 3D view control while a 3D session is active; the 2D level renderer is a different control and is not on screen. The drop is inferred from the lack of any draw or image request; a deeper static trace was not done.

## Answer

2D level packets do arrive in a 3D session — the login level and anything sent later — but the client accepts them silently and ignores them: nothing is drawn and no request or move follows. The 3D engine owns the screen, so a server driving a 3D session cannot show anything through 2D level packets; it must use the 3D channel (GameObjects, and the `events`/weapon text channel from [T3D-018](3d-client-events-420r6-2026-11-25.md)).
