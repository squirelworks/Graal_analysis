# Real 2.22 client on Graal the Adventure (2026-10-30)

A short live run of the real client, `Graal_222.exe` from the Graal 2.2.2.0 install, on the public server Graal the Adventure (`2gta.home.eevul.net:14913`), signed in as the user's own account (Seji) from the client's saved login. The run was driven by a script on the user's PC: about 2 minutes of walking, one door and one sword swing in the first pass, then about 6 minutes at one bush in the second. Screenshots are in this folder, captured from the window at 2.5x scale (one 16 px tile is 40 px).

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
## Second pass: bushes, hiding, chat (20:22 to 20:28 local)

Done next to the bush east of Cat's Pub. Crops are 600 x 450 physical pixels around the player.

### Lift, hide under it, throw

| Step | Screenshot | What the screen showed |
|---|---|---|
| A facing the bush | [lift-b](lift-b.png) | The bush goes over the head and the 2 x 2 stump is left on the board at once. The carried bush is drawn green, while the bush on the board was the bluish-grey variety: the carried image is the plain bush sprite, not the board's tiles. |
| D while carrying | [duck-b](duck-b.png) | The player disappears under the bush; only the bush is drawn, at ground level, on the player's spot. |
| Left arrow while hidden | [hidemove](hidemove.png) | The bush moves with the player (one tile in 250 ms), still with nothing of the player showing. |
| D again | [unhide](unhide.png) | Back to the normal carry pose. D toggles. |
| A | [throw-a](throw-a.png) | The bush is thrown in the facing direction (left) and leaves the view. |

### Bush respawn on this server

Lifted at 20:26:34.7 and thrown away, then the bush's spot was captured every 2.5 s for 100 s ([resp-montage](resp-montage.png)). The stump shows at 3, 6, 8, 11 and 13 s; the bush is back at 16 s and stays. So the server puts a lifted bush back about **14 to 16 s** after the lift. That fits the GServer-v2 rule in `client-internals/board-respawn.md` (exactly `respawntime`, default 15 s), not the 1.3-era 6 to 12 s random timer. A first, untimed lift on the same bush (20:22) had also come back within a minute.

### Sword on a bush

| Screenshot | What it shows |
|---|---|
| [cut-a](cut-a.png), about 100 ms after S | The sword arc to the right and four green leaf pieces flying out from the bush's spot; the stump is already on the board. |
| [cut-b](cut-b.png), 700 ms later | Leaves gone, stump left. |

The leaf pieces are green although this bush is the bluish-grey kind.

### Pushing

Holding right into the bush ([face2](face2.png)) shows the push pose: arms forward, body leaning into the bush. Nothing moves.

### Chat

- Tab opens the chat line at the bottom; the typed text shows there in the system font ([chat-typing](chat-typing.png)).
- Enter sends it ("hi"). The text then shows above the player's head as small white text with a dark outline, with **no bubble or box around it** ([chat-a](chat-a.png)). On this server, with the 2.22 client, "chat bubble" is just outlined text.
- The line was still over the head about 45 s later, while the player had not moved. That matches Seihai's note that your own line is held until a direction key (`chat-lists.md`).
- After Enter the chat line keeps the keyboard: the arrows did not move or turn the player until Tab was pressed again. A Seihai profile for 2.22 should do the same.

## Against Seihai's laundry list

| Seihai item | What the real 2.22 client showed |
|---|---|
| First-load warps land at the link's arrival (laundry 2026-10-29-b, priority 1) | The interior was not cached and the player came in inside it, in the water. Whether that spot is the link's new-x/new-y was not checked against the level file. |
| Big map neighbours (priority 7) | Crossing north from the start level into the sparring complex showed no blank board or pause in the screenshot taken right after. |
| Sign input (priority 4) | Not tested: the one sign approached was not opened. |
| Duck while carrying (priority 4) | D hides the player under the carried bush, the bush moves with the player while hidden, and D again brings the player back. Seihai commit 0ddbc35 ("Hide under a carried bush or stone with D") matches this. |
| Bush respawn | About 15 s on this server (see above). Seihai shows the server's own restore through `PLO_BOARDMODIFY`, so nothing to change. |
| Chat repeat, chat bubble look | Chat over the head is plain outlined text with no bubble. Key repeat while typing was not tested. |
| Pots, signs, appearance commands | Not tested on this run. |
| HUD counters | Counters start at their defaults and update in place a few seconds after the level is drawn. |

## Not done

- One public chat line ("hi"), with the user's go-ahead. No PMs, no items used or dropped, no sparring.
- The client was left running and logged in at the end of the run.
