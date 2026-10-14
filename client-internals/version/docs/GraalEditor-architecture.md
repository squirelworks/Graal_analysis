# Architecture

GraalEditor is a Delphi VCL application. The live document is a `TAdventureLevel` owned by the main form `TAdventure`. Preview goes through DelphiX (`TDXForm`, DirectDraw 5 and 7). Sound goes through BASS. Picture codecs are the same family GraalShop uses (GIF, MNG, PNG/DIB).

```
GraalEditor.exe  (unpacked image, base 0x400000)
├── Delphi RTL          AnsiString, exceptions, file IO
├── VCL                 forms, listviews, richedit, menus, dialogs
├── Graphics            TGIF, TMNG, TJPEGImage, TBitmap, TGraalImage
├── DelphiX / DirectDraw  TDXForm, DirectDraw 5 and DirectDraw 7
├── BASS                music, samples, microphone device names
├── Domain              TAdventureLevel, TEditorLevelCache, TGraalMap,
│                       TEditorLink, TEditorSign, TEditorNPC, TEditorChest,
│                       TEditorObject, TLevelObject, TLevelHeights
├── Animation           TGraalAni and the GraalShop actor/step/sprite set
└── UI                  TAdventure + modal frames (see ui.md)
```

See [diagrams/architecture.svg](diagrams/architecture.svg) and [diagrams/classes.svg](diagrams/classes.svg).

## Layers

### Runtime

Borland RTL banner: `SOFTWARE\Borland\Delphi\RTL`, `Portions Copyright (c) 1983,97 Borland`. Linker version 2.25. Sections are the classic Delphi layout: `CODE`, `DATA`, `BSS`, `.idata`, `.tls`, `.reloc`, `.rsrc`. Unit name recovered from RTTI: `UAdventureEditor`.

### VCL shell

One main form, twenty modal or tool forms stored as `TPF0` DFMs in `.rsrc`. The main form is `TAdventure` / `Adventure`, caption `Graal`, `poScreenCenter`, `KeyPreview` set. It owns the tile canvas, a mode radio group, and the menu that opens the other frames.

There is no plugin ABI. Registry use that shows up is the Delphi locale key and the shell-folders key the Thinstall stub virtualizes, not a Graal account store. Account files the editor knows by name: `buddyaccounts.txt`, `ignoredaccounts.txt`, `mutedaccounts.txt`, `graalconfig.txt`, `headsconfig.txt`, `FILENAMECACHE.txt`.

### Picture, map, sound

- GIF: `TGifAnimation`, `TGifAnimationStep`, failure `Gif loading failed!`
- MNG: `TMNGAnimation`, `TMNGAnimationStep`, failure `MNG loading failed!`
- PNG and ordinary bitmaps via `TGraalImage` / `TBitmap`. Image dialog: `CImage files (*.png, *.mng, *.gif)`
- DirectDraw init can fail for 5 or 7: `Error when loading and initializing DirectDraw5` / `DirectDraw7`. More Options has `Don't use Direct3D (lights)` and `Draw in compatibility mode (very slow)`, plus a vertical-blank wait checkbox.
- BASS loads music and samples. More Options has Audio and Microphone pages.
- World map assets: `graalmap.png`, `map.png`, `map2.png`, `minimap.txt`, `bigmap.txt`, `loadgmaps.txt`. Status strings: `Loaded gmap`, `Loaded minimap`, `Loaded minimap from`.

### Domain

`TAdventureLevel` is the open level. `TEditorLevelCache` keeps recently loaded levels (the link walker and the gmap need neighbours). `TGraalMap` is the stitched world. `TLevelHeights` is a height overlay distinct from the tile board.

Placed entities are separate types, not one tagged union: `TEditorLink`, `TEditorSign`, `TEditorNPC`, `TEditorDefNPC`, `TEditorChest`, `TEditorObject`, plus baddy state edited by `TEditBaddy`. `TEditorUndoInfo` is the undo record. `TGaniObject` / `TImageAnimation` attach a GANI to a placed object.

### Animation subset

The GANI object model is the GraalShop one, compiled into the editor so tile-object scripts and NPC animations can be previewed without launching GraalShop:

`TGraalAni`, `TGraalAniSprite`, `TGraalSpriteAttachment`, `TGraalAniPart`, `TGraalAniSound`, `TGraalAniStep`, `TGraalActor`, `TGraalActorMod`.

`TTilesArrayFrame` is the tile-index / script editor (Courier New edit plus a rich edit). Its sample script is the offline tutorial: `addtiledef picso.png,offlinetutorial,1` and `setplayerprop` / `setcharprop` lines.

## Control flow, one screen

```
WinMain-equivalent (Delphi RTL)
        │
        ▼
TAdventure  caption "Graal"
        │
        ├── F5 Load Level ── open *.graal / *.nw ── TAdventureLevel
        ├── F4 Edit Level ── tile / object / baddy / npc / chest radios
        ├── links ── TLinkList ── TLinkOptions
        ├── signs ── TEditSigns
        ├── NPC ── TEditNPC (image + script rich edit)
        ├── baddy ── TEditBaddy (type + three verses)
        ├── chest ── TChestEdit (item + sign index)
        ├── F6 Debugger, F7 Player List, F8 Server List
        └── save ── write BOARD / LINK / SIGN / CHEST / NPC / BADDY
```

## Binary facts

- Unpacked image base `0x400000`, `SizeOfImage 0x1B1000`, entry RVA `0x155D4C`.
- Version resource (also present, UTF-16, in the packed stub): CompanyName `Linux Cyberjoueur`, FileVersion `2.3.1.1`, InternalName `Graal editor`, ProductName `GraalEditor`.
- On-disk packed file is the Thinstall stub. Do not point IDR or a Delphi decompiler at `graal/GraalEditor.exe`. Point them at `unpacked/GraalEditor.exe`.
