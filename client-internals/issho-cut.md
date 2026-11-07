# What the 6.x C++ core owns

Date: 2026-11-07. Static read of the unpacked 6.0.3.7 and 6.1.1.3 listings. Nothing was run. Tags: **[bin]** those two listings · **[doc]** the Torque-era notes for v3–v5.

Seihai issue 377 splits the client work into issho, the post-Torque C++ core, and Ato, the Torque years. This page is only that cut, from the listings. No Seihai code is written here.

## Issho, from these two images

Both unpacked images are one `quattro_lib` program. The names present in both are `TSocket`, `TServerPlayer`, `TServerNPC`, `TServerLevel`, `GuiGraalCtrl`, `StartScript_GraalGui`, `GRESCR01`, `OpenGL`, `Direct3DCreate9` and `fmod`. `SimObject`, `GameConnection`, `TerrainBlock` and `horizSizing` are absent from both. **[bin]**

The GS2 dispatcher in both images has the same 152 cases, from 11 through 242, with no case 48, 49 or 200. **[bin]**

`GuiWindowCtrl`, `GuiControlProfile` and `GuiTilesCtrl` are strings in both images. They are not a Torque console: the console classes above are absent, and the 6.037 note already records `-printmap` writing Torque 2D datablock text without running a module. **[bin]** (`client-internals/unpacked-6037.md#torque-names-that-remain`)

6.1.1.3 adds the script methods `setprotocol`, `sendraw` and `senddata`, and the `tclient_*` handlers. A decoded-string search of 6.037 finds none of those names. The core they sit on is the same `quattro_lib` program. **[bin]**

## Ato, v3 to v5

Ato is the Torque client those years actually ship. The notes, not these two listings, are the evidence: a Torque console and net layer, `SimObject` and `GameConnection`, and for the 3D servers a UDP channel on the listed port plus one. **[doc]** (`torque/README.md`, `manual/10-torque.md`)

These two listings are the other side of that cut. They keep a few Torque control names as strings, and they do not keep the Torque console or the Torque net classes. The 6.1.1.3 game connect path does not open a datagram socket. **[bin]**
