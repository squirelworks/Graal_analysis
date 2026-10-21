# GraalEditor and GraalShop compared with the 2.05 built-in editor

Date: 2026-10-21

Sources: forms, RTTI class lists, version resources, and strings of `GraalEditor.exe` 2.3.1.1 (from a memory image of the unpacked Thinstall package), `GraalShop.exe` 1.1.1.0, and `GraalShop_old.exe`, all from the Graal 2.2.2.0 folder. The 2.05 side is in `client-internals/level-editor-205.md`. For GraalEditor on its own (menus, options, file types), see `tools/graaleditor.md`; this note only covers what changed relative to 2.05. Names only, no code. Tags: **[GE]** GraalEditor · **[GS]** GraalShop · **[2.05]** · **[inf]**.

## Lineage

| Build | Editor |
|-------|--------|
| 2.05 (2001) | Built into `Graal.exe`. F4 switches the game window into editor mode. Refused while online. |
| 2.17 / 2.22 | Still built in, with the newer forms (`TEditNPC`, `TTilesArrayFrame`; 2.22 also `TLogFrame`). |
| 2.31 | No editor forms left in the client (only the 9 tutorial levels remain), so editing moved to GraalEditor. |
| GraalEditor 2.3.1.1 (2005) | The same `TAdventure` program with the online client removed, shipped as its own exe in a Thinstall package. |

GraalEditor is not a rewrite. It keeps the 2.05 main form (`TAdventure`, caption `Graal`), the same tool forms, the same toolbar hints ("Undo board copy", "Turn selection into a warp field"), and even game-only strings ("You cannot open the editor in the online mode.", F7 Player List and F8 Server List buttons in the help form). It also keeps the whole game model (`TPlayer`, `TComputer`, `TAdventureCommand` … the GS1 interpreter), so *Play* still runs a level locally. **[GE]**

It does not have the network client. There is no `TGraalClient`, `TAdventureClient`, or `TServerListClient`, no listserver host, and no login token. **[GE]**

## What GraalEditor adds over 2.05

| Area | 2.05 built-in | GraalEditor 2.3.1.1 |
|------|---------------|---------------------|
| Open | GR-V1.00–1.03, Z3-V1.03/1.04, GLEVNW01 | Same set (`Graal levels (*.graal, *.nw)` filter) |
| Save | `.nw` → GLEVNW01, otherwise GR-V1.03 | GLEVNW01 with a new `HEIGHTS` section. GR-V1 writer strings are still present. **[inf]** "Level(s) saved" means several levels can be saved at once. |
| World | single level plus *Generate map* image. 2.05 already contains a `GRMAP001` reader (`WIDTH`, `HEIGHT`, `GENERATED`, `GENSEED`, …, `HEIGHTMAP`), but no caller was found, so it looks dormant. **[2.05][inf]** | **gmaps** wired into the editor: the same `GRMAP001` reader plus `LEVELNAMES`, `MAPIMG`, `MINIMAPIMG`, `NOAUTOMAPPING`, and the generated-map keys (`GENSEED`, `GENBASE`, `GENEVENBORDERS`, `GENHEIGHT`, `GENCHAOS`, `LEVHEIGHT`, `LEVCHAOS`, `HEIGHTMAP`…`HEIGHTMAPEND`, `RANDOMSEEDS`…`RANDOMSEEDSEND`). A level cache (`TEditorLevelCache`) holds neighbours. |
| Terrain | tile overlays in the editor. The dormant gmap parser knows `HEIGHTMAP`, and `HEIGHTS` appears in the binary, but the editor has no height tools. | `TLevelHeights` height overlay per level (`HEIGHTS`, `.height`, "Terrain Height Spot", "Show terrain grid") |
| Palette modes | predefined object, tile, baddies/NPCs/chests | the same three plus **Predefined NPCs** (`TEditorDefNPC`, "Editor Control-NPC" with a parameter grid) |
| NPC editing | `TEditPerson` (image + *Action*) → `TPersonAction` (script) | one `TEditNPC` window with image, script, Test, Style, and **Find**. Scripts may carry editor markers `//#EDIT` and `//#COMMENTS`. |
| Character NPC | one-page form | the same fields split over four tabs (Look, Movement, Attack, General) |
| Tiles | — | *Export Tiles Array* (`TTilesArrayFrame`): the selection as one line of tile indices and as a script array |
| View | blocking/foreground/terrain overlays | plus *Hide npcs* and *Show terrain grid* |
| Log | — | `TLogFrame` (memo log) |
| Offline data | 13 embedded `tutorial_*` levels | `offlinetutorial_*` (3×3) and `tiledefsOffline.txt` |
| Sound | DelphiX + MCI/Winamp | BASS, with the same function set the 2.22 client imports |
| Integrity | `TProgramCheck` self-check ("The Graal execution file is corrupted…") | the same, plus RSA/SHA-1 signature checks of `GraalEditor.sig` and `arrays2.sig` (`TAS_RSACryptography`, `TAS_DigestSHA1`; "Not ready to verify signature, must have valid public key"). What happens when a check fails has not been traced. |

Unchanged from 2.05: the tile undo model (rectangle snapshots, "Undo board copy"), the link, sign, chest, and baddy dialogs, GOBJSET01 stamp sets with `objects<set>.txt`, right-click to copy objects, and *Generate map* → `graalmap.png`.

## GraalShop (the GANI editor)

`GraalShop.exe` 1.1.1.0 (version resource: "Gani Editor", 2006) and `GraalShop_old.exe` (2002) are separate Delphi programs with one main form, `TEditFrame` ("Graal Shop - The Graal Animation Editor"), and an *Add sprite* dialog. They edit `.gani` files only. Levels are out of scope. **[GS]**

### Model

`TGraalAni` holds sprites (`TGraalAniSprite`, plus `TGraalSpriteAttachment` for `ATTACHSPRITE`/`ATTACHSPRITE2`), frames (`TGraalAniStep` → `TGraalAniPart` placements and `TGraalAniSound`), and, in movie mode, actors (`TGraalActor`, `TGraalActorMod`, `TActorSingleMod`). Undo and redo are a list of `TEditOperation` records.

### Workflow

- **Sprite mode** (`GANI0001`): a direction selector (up/left/down/right), a sprite-definition grid, a frame strip, and a canvas. Toolbar actions: play/stop, add/delete/copy frame, insert step before/after, add sound, add/import/remove-unused sprite definitions, reverse animation, undo/redo, new/load/save/save as. Selected sprites can be moved, brought to front, or sent to back, and keyed with x/y.
- **Movie mode** (`GANI0002`, *-> Movie Mode*): a timeline of actors of kind CHAR, SPRITE, SOUND, or TEXT. TEXT actors have font, zoom, size, alignment, wordwrap, and shading. CHAR actors have ani, dir, head, body, sword, shield, horse, colours, attr, and param. Options: *Automatic Gani Setting* (switch idle/walk when an actor is moved) and *Graal2002 ganis*.
- **Header fields** edited in a grid: Length, Loop, Back. color, Setbackto, Def. head, Def. body, Def. param1–3. These are written as `LOOP`, `BACKCOLOR`, `SETBACKTO`, `DEFAULTHEAD`, `DEFAULTBODY`, `DEFAULTPARAM`, `DEFAULTATTR`, plus `COLOREFFECT` / `ROTATEEFFECT` / `STRETCHXEFFECT` / `STRETCHYEFFECT` / `ZOOMEFFECT` and `SCRIPT`…`SCRIPTEND` (copied, not run). The grammar is in `formats/gani.txt`.
- **Preview** uses DelphiX DirectDraw 7 and plays `PLAYSOUND` steps through DirectSound. Default art: `sprites.png`, `body.png`, `head0.png`, `shield1.png`, `ride.png`, `soundicon.png`. The program finds the Graal folder through `Graal.exe` and `FILENAMECACHE.txt` and searches `pms`, `profiles`, and `weblevels`.

`GraalShop_old` has sprite mode only. It has no `GANI0002`, `MOVIE`, `ACTOR`, `ATTACHSPRITE2`, or `ROTATEEFFECT`. **[GS]**

### How this compares with what 2.05 can play

The 2.05 client reads only the sprite-mode subset: `SPRITE`, `ANI`…`ANIEND`, `WAIT`, `PLAYSOUND`, `LOOP`, `CONTINUOUS`, `SETBACKTO`, `SINGLEDIRECTION`, `COLOREFFECT`, `ZOOMEFFECT`. It has no `GANI0001`/`GANI0002` signatures, no movie mode, no `DEFAULT*`, and no `ATTACHSPRITE*`. **[2.05]** Ganis saved by the 2006 GraalShop with movie mode or attachments do not play in 2.05. A sprite-mode gani with only the fields above does.
