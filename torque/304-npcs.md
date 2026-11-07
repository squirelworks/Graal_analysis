# NPCs, baddies, weapons and script in Linux 3.04

Date: 2026-11-07. Static read of the Linux `graalexe` 3.04 decompile. Nothing was run. Tags as in [README.md](README.md).

These units are `graal/npcs.cpp`, `graal/baddies.cpp`, `graal/weapons.cpp`, `graal/scriptfunctions.cpp` and the list helpers in `graal/convertedclasses.cpp`. The level file stores the bodies; this is what the client does with them. **[bin]**

## Triggers

Placing a copy of an NPC onto a level fires the trigger `playerenters` when the caller asks for it and the local player exists. The same name is fired from the local player on a level change ([304-adventure.md](304-adventure.md)). Other trigger names compiled in `npcs.cpp` are `created`, `timeout`, `waspelt`, `sparringzone`, `movementfinished` and `washitnpc`. **[bin]**

A body with no image name is filled from `sword1.png`, `sword2.png`, `sword3.png`, `sword4.png`, `shield1.png`, `shield2.png`, `shield3.png` or `head0.png`, and a head name is completed with `.png`. Player-like animations in this unit are `bomy_idle`, `bomy_walk` and `bomy_kick`, under the prefix `bomy_`. One compiled script signature is `(S;S;S)S`. **[bin]**

## Baddies and weapons

`baddies.cpp` gives baddy types 3 and 4 their own surface and loads `wbow1.png` into it. Other types drop that surface. The death sound named here is `compudead.wav`. **[bin]**

`weapons.cpp` cuts one rectangle out of a list of rectangles: any overlap is split into the pieces that remain, and the original rectangle is removed. Where a computed weapon name would be empty, the unit writes the name `Back`. **[bin]**

## Script helpers

`scriptfunctions.cpp` implements the verbs that touch the world from a script. The name `shapetiletypes` is the grid of tile values: the first two numbers are the width and height in tiles, and the values come from the script list or from an existing buffer. A show-image verb whose case is the polygon case creates the `polygon` object that `showimgs.cpp` also builds ([304-draw.md](304-draw.md)). Sounds played from this unit are `bomb.wav`, `thunder.wav`, `axe.wav` and `sword.wav`. **[bin]**

`convertedclasses.cpp` is the list and string layer the other Graal units call (index, append, compare). Turning a bare name into a file path uses the name's first two characters as the directory when those characters are accepted, and the directory `special` otherwise, then appends `.txt`. **[bin]**
