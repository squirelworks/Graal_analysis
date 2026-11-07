# Drawing in Linux 3.04

Date: 2026-11-07. Static read of the Linux `graalexe` 3.04 decompile. Nothing was run. Tags as in [README.md](README.md).

The 2D pictures are Graal types, compiled from `graal/tiles.cpp`, `graal/graphics.cpp`, `graal/ganis.cpp`, `graal/showimgs.cpp` and `graal/surfaceowner.cpp`. They are not Torque scene objects. **[bin]**

## Types

C++ type info in this binary, parent named in the second column:

| Type | Parent |
|---|---|
| `TDrawableObject` | none |
| `TLevelObject` | `TDrawableObject` |
| `TGaniObject` | `TLevelObject` |
| `TServerPlayer` | `TGaniObject` |
| `TDrawableSurface` | `TDrawableObject` |
| `TSurfaceOwner` | `TDrawableSurface` |

`TServerPlayer` is the other people in the level ([304-net.md](304-net.md)). `TSurfaceOwner` is the image holder: the session builds one per HUD sheet and asks it to load a file name ([304-adventure.md](304-adventure.md)). **[bin]**

## Sheets and tiles

`graphics.cpp` loads `.png` files and answers width and height. The map click uses those sizes to scale the mouse onto the gmap. **[bin]**

`tiles.cpp` logs `Loading tile definitions for offline mode.` when the current server name is `Offline`, and `Loading tile definitions for server ` plus the name otherwise. It reads `tiledefs/*.txt`, and the sheet it names is `pics1.png`. **[bin]**

## Ganis

`ganis.cpp` reads a `.gani` as text. The block words it recognises are `ANIEND`, `PLAYSOUND`, `PARAM`, `ATTR`, `ACTOR`, `ACTOREND`, `FRAME`, `SPRITE`, `ATTACHSPRITE`, `ATTACHSPRITE2`, `COLOREFFECT`, `ZOOMEFFECT`, `EFFECTMODE`, `SCRIPT`, `SCRIPTEND`, `MOVIE`, `CONTINUOUS`, `SINGLEDIRECTION`, `SETBACKTO`, `FRAMES`, `DEFAULTHEAD`, `DEFAULTBODY`, `DEFAULTPARAM` and `DEFAULTATTR`. **[bin]**

A new gani starts at zoom 1. The setter names are `dx`, `dy`, `layer`, `visible`, `dir`, `ani`, `chat`, `head`, `sword`, `shield`, `horse`, `param`, `color`, `sprite #`, `file`, `text` and `zoom`, plus the text flags `italic`, `centered`, `rightaligned`, `underline`, `strikeout`, `wordwrap` and `shaded`. A colour value may start with `0x`. Two script names are compiled in this unit, `playerenters` and `playerlook`. The still horse animation is `horsestill`. **[bin]**

The single-direction names, in the order the unit stores them, are `CHAR`, `SPRITE`, `SOUND`, `TEXT`, `idle`, `walk`, `walkslow`, `kick`, `sword`, `ridesword`, `spin`, `push`, `grab`, `pull`, `lift`, `carrystill`, `hiddenstill`, `carry`, `hidden`, `shoot`, `ridestill`, `ridefire`, `rideeat`, `ride`, `sit`, `sleep`, `hurt`, `ridehurt`, `dead`, `maps1`, `maps2`, `maps3`, `swim`, `lava`, `carried`. **[bin]**

## Show images

`showimgs.cpp` treats a line that starts with `ATTR` or `PARAM` as an attribute. A line that starts with `#` builds a point list stored under the name `polygon`. The first number is kept when it is 3; any other first number is stored as 2. **[bin]**

`scriptfunctions.cpp` reaches the same polygon object when a show-image verb asks for one ([304-npcs.md](304-npcs.md)). **[bin]**
