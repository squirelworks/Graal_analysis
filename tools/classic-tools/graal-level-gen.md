# GraalLevelGen (December 2000)

Date: 2026-11-01

The Delphi generator shipped as `GraalLevelGen.exe` with `levelgendoc.html` and `levelgen.png`. The one-line note in `../generators.md` calls it an image-to-levels writer. This is the operator contract from that HTML, checked against the image. The image imports no socket library. **[doc][bin]**

The package readme says the levels are New World format and that the tool does not apply to 1.3.9 or older. **[doc]**

## What the operator does

Draw a map whose width is 64 times the number of levels across and whose height is 64 times the number of levels down. Save it as a gif, or as an 8-bit png. Start the tool, pick the image, an output folder and a world name, and press Generate World. **[doc]**

| Colour | RGB | Becomes |
| --- | --- | --- |
| Green | 24, 140, 24 | Grass, not drawn |
| Light green | 181, 239, 189 | Forest |
| Blue | 0, 0, 255 | Water |
| Maroon | 128, 0, 0 | Mountains |
| Red | 255, 0, 0 | Flowers |
| Light brown | 150, 110, 0 | Sand |
| Brown | 113, 82, 0 | Small sand stones |
| Dark gold | 83, 61, 0 | Big sand stone |
| Dark green | 0, 106, 0 | Swamp |
| Very dark green | 0, 66, 0 | Bushes |
| Cyan | 0, 255, 255 | Puddle |
| Dark cyan | 0, 179, 179 | Puddle stone |

The mapping from a pixel to a tile is a grid, not one tile per pixel, so the levels are not a 1:1 copy of the picture. **[doc]**

## What it writes

Files named `worldname_a-01.graal` through, at the largest, `worldname_z-99.graal`, plus `bigmap.txt` for the editor's map (the M key). The HTML says not to drop that `bigmap.txt` on top of the main world's copy. **[doc]**

A second run on levels that already exist reads them and adds the new objects. It does not replace the previous board. That is how the doc stacks trees on mountains: generate the mountains, generate again for the trees. **[doc]**

The image contains the signatures `GLEVNW01` and `GR-V1.00` through `GR-V1.03`, and the words `BOARD`, `LINK`, `SIGN` and `NPC`. Those strings sit in the same editor unit as level names such as `start1.graal`. Which signature a given save writes was not separated from that unit. The HTML is clear about the file names. **[bin][doc]**

## What it never sends

No socket import, no login, no server list. The world stays in the output folder. **[bin]**
