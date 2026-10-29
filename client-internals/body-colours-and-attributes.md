# Body colours, looks commands and GANI attributes (2.05)

How 2.05 colours a player's body, what the looks commands change, and how a
GANI's attribute sprites (the hat) pick their picture. Derived from the 2.05
client unless marked otherwise.

## Body colours

| Fact | Status |
|---|---|
| A body picture is a palette image. Before it is drawn, palette entry 5 takes the skin colour, 6 the coat, 4 the sleeves, 3 the shoes and 1 the belt. Entry 0 always takes colour 18 (black, the outline) | derived |
| The five colours are prop 13 (COLORS), in the order skin, coat, sleeves, shoes, belt. This settles the order `protocol/player-props.md` marks as inferred | derived |
| The colour list, by index: 0 white 255,255,255; 1 yellow 255,255,0; 2 orange 255,173,107; 3 pink 255,132,132; 4 red 255,0,0; 5 darkred 206,24,41; 6 lightgreen 132,255,132; 7 green 0,255,0; 8 darkgreen 0,198,0; 9 lightblue 132,132,255; 10 blue 0,0,255; 11 darkblue 0,0,198; 12 brown 132,0,0; 13 cynober 0,255,255; 14 purple 255,0,255; 15 darkpurple 132,0,132; 16 lightgray 206,206,206; 17 gray 132,132,132; 18 black 0,0,8; 19 transparent 0,0,0 | derived |
| A new player is orange, darkred, black, darkred, black (2, 5, 18, 5, 18), with `body.png` and `head0.gif` | derived |
| The stock bodies follow that palette layout, and entry 2 is the clear colour | checked on the 2.22 `body.png` and `body13.png` |
| Graal Reborn's GServer gives a new account 2, 0, 10, 4, 18 instead | read from GServer-v2 beta4 source |

## Looks commands

| Fact | Status |
|---|---|
| `sethead`, `setbody`, `setskincolor`, `setcoatcolor`, `setsleevecolor`, `setshoecolor` and `setbeltcolor` change the local player, whichever NPC or weapon runs them. The NPC is not changed; an NPC's own look is `setcharprop` | derived |
| A colour command takes a colour name from the list above or a number, rounded, into its slot | derived |
| `sethead`, `setbody`, `setskin`, `setcoat`, `setsleeves`, `setshoes` and `setbelt` typed in chat are run by the GServer, which sends the new props back. They are not client commands | read from GServer-v2 beta4 source |

## GANI attributes

| Fact | Status |
|---|---|
| A GANI sprite whose picture is `ATTR1` … `ATTR5` draws the player's attribute 1 to 5 | derived |
| Attributes 1 to 5 are props 37 to 41 (GATTRIB1 to GATTRIB5). 2.05 reads them for other players as well as its own | derived |
| A player with no attribute of their own draws the GANI's `DEFAULTATTR1` … `DEFAULTATTR5`. The stock `idle.gani` names `hat0.png` as attribute 1, the hat | checked on the 2.22 GANIs |
| `setplayerprop #P1,<image>` … `#P5` set attributes 1 to 5; `#3`, `#8` and `#C0` … `#C5` set head, body and colours the same way (`npc-library/gs1-command-reference-205.md`). What a sixth colour slot `#C5` is for is not known | derived |

## Not checked

- Which folder 2.05 looks in for an attribute picture. The stock hats are
  in `hats/`, so the hat is inferred to be looked for there.
- What 2.05 draws for an attribute set to an empty name.
- None of this has been checked against a running 2.05 client.
