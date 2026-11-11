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

## Exact show-image wrapper constants (retained static review)

[bin] This addition concerns the archive-labelled Linux 3.04 fixed/obsolete identical x86 analysis ELF, SHA-256 `6e9e35a3ef1320e9705db382ea3184cec07cfce5cac9fb2a550d79fe41931e86`. Its retained original packed executable has a different digest, `7901897411ffcee7b72806d5d021d0b42f5670739ad2ed97467fc86bc75690d0`. The retained findings identify eight named registrations whose thin wrappers pass mode/flag constants into a shared Graal show-image-family helper:

- `showimg`: mode 0, flag 0; `showimg2`: mode 0, flag 1.
- `showani`: mode 4, flag 0; `showani2`: mode 4, flag 1.
- `showpoly`: mode 3, flag 0; `showpoly2`: mode 3, flag 1.
- `showtext`: mode 2, flag 0; `showtext2`: mode 2, flag 1.

[bin] This is an internal wrapper-constant map, not a new command vocabulary or a complete script signature. Existing [version-command records](../npc-library/gs1-commands-by-version.md) already list these names, and the polygon machinery above was already documented. The [machine-readable map](linux-304-showimage-map.static.json) preserves only the eight supported bindings. Mode 1, signature-letter grammar and the semantic meaning of the flag remain unqualified here. No rendering result or behavior of another client is inferred from the constants.

[bin] The selected common helper derives an integer key from a numeric first argument and finds or creates an indexed display object. The retained lookup/insertion pair compares that integer key; insertion rejects an existing equal key and otherwise inserts by position. This supports a sorted integer-key container, not a generic string-name map. It does not specify the numeric conversion's rounding or exceptional values, container corruption handling, all object ownership/lifetimes or the complete helper ABI.

[inf] The equal-key check belongs to this selected display-container insertion helper. It does not establish console/namespace duplicate-registration policy or that repeated script commands with the same key are rejected: the outer path separately performs lookup. The shared helper is a show-image-family dispatcher, not the generic Graal interpreter or the Torque callback adapter.

### Provenance and scope of this addition

[doc] Finding `V3-GRAAL-01` in the retained structured review supplies the eight wrapper constants; `V3-GRAAL-03` supplies the local key comparison/insertion result. The retained baseline comparison explicitly separates this binding precision from already published polygon and native-rendering architecture. Publication preparation reads and hashes those documents; it does not reopen decompiled functions, assembly or executable bytes. Underlying native findings and executable identities remain researcher-supplied.

`LNX304-SHOWIMAGE-FINDINGS-DOC`, `LNX304-SHOWIMAGE-BASELINE-DOC` and `LNX304-SHOWIMAGE-IDENTITIES-DOC` identify the actual owner-held input documents through [the source index](../docs/evidence-index.tsv). Their digests identify documents, not original installers or newly created runtime captures. Raw code, addresses, original assets and private access paths are excluded.

- [x] ~~Map the eight retained exact-build wrapper mode/flag pairs without repeating known command presence.~~
- [ ] Establish unresolved mode, flag/signature semantics and rendered behavior separately before claiming a complete command contract.

No client, server, debugger, provider or implementation build was run for this document-only comparison. Server and server commit: none.
