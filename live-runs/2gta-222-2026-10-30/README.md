# Real 2.22 client on Graal the Adventure (2026-10-30)

A short live run of the real client, `Graal_222.exe` from the Graal 2.2.2.0 install, on the public server Graal the Adventure (`2gta.home.eevul.net:14913`), signed in as the user's own account (Seji) from the client's saved login. The run was driven by a script on the user's PC: about 2 minutes of walking, one door, one sword swing, no chat. Screenshots are in this folder, captured from the window at 2.5x scale (one 16 px tile is 40 px).

What follows is what the screen showed. Nothing here was read from packets.

## Server list

![server list](222-serverlist.png)

- Window title "Graal Reborn Server list". The footer greets the account ("Welcome to Graal Reborn, Seji. There are 10 server(s) online.").
- Gold tab: Graal the Adventure (0 players) and GServer-RS (0 players). Silver and Bronze were not opened.
- Graal the Adventure's row: language English, version "Beta Version: 4.0.0", description "Occupied by Kalzor.", homepage `https://graal.in/c/playerworlds…`.
- GServer-RS's row: version "Version: 0.1.262", description "Rust gserver testing", homepage on github.com (vinvicta's gserver).

## First screen after Connect

![start](gta-start.png)

- The client opens a separate window titled with the server name, "Graal the Adventure". The empty strip at the bottom is the chat line.
- HUD: the A, S and D slots top left (S shows the sword with a "1", D a ring), the magic bar under them, the rupee/bomb/arrow counters in the middle, three hearts and the `00/01` counter on the right.
- Right after the level appears the counters read 0 rupees, 00 bombs, 03 arrows. A few seconds later (first screenshot after walking, [walk1](walk1.png)) they read 6, 05, 03, and later 7, 10, 03. The real client shows the counts as they arrive, after the level is already drawn; the start screen is not held back for them.
- A server-side minimap is drawn at the bottom left, with the player's head as the marker. It is a weapon/NPC image, not a built-in client panel.
- An NPC message ("Come one come all! The house of bananas is open…") scrolls across the bottom of the view in an outlined font.

## Camera

Walking right or up moves the view, not the player: the player stays at the same place on screen (about the window's middle) while the board scrolls under them, until the level edge. Compare [gta-start](gta-start.png) with [walk1](walk1.png).

## Level-name banner

![banner](walk2.png)

Walking up the stairs north of the start crosses into the next level. The client then shows a parchment panel, "US Sparring Complex", in the lower half of the view, over the board, for a few seconds. It is drawn in the same panel style as a sign. It is most likely a server script (the level's or a weapon's); this run did not check whether the client itself names levels on entry.

## Door, water and other NPCs

![inside](inside.png)

- Walking up into the complex's door loads the interior. The player arrives in the deep water on the left and is drawn with the swim sprite (head and shoulders only).
- NPCs carry name labels under them in the outlined font ("Marge", "Gemetzel Haus' Fighter"). The fighter shows a green "?!" above it.
- Walking down out of the interior puts the player outside on the path south of the building ([down1](down1.png)), facing down with the shield in front.

## Sword

![sword](sword-a.png)

One S press, captured about 90 ms in: the sword frame facing down with the blade tip below the player.
## Against Seihai's laundry list

| Seihai item | What the real 2.22 client showed |
|---|---|
| First-load warps land at the link's arrival (laundry 2026-10-29-b, priority 1) | The interior was not cached and the player came in inside it, in the water. Whether that spot is the link's new-x/new-y was not checked against the level file. |
| Big map neighbours (priority 7) | Crossing north from the start level into the sparring complex showed no blank board or pause in the screenshot taken right after. |
| Sign input (priority 4) | Not tested: the one sign approached was not opened. |
| Duck while carrying, pots, appearance commands | Not tested on this run. |
| HUD counters | Counters start at their defaults and update in place a few seconds after the level is drawn. |

## Not done

- No chat, no PMs, no items used or dropped, no sparring.
- The client was left running and logged in at the end of the run.
