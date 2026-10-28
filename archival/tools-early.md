# Tools (early measurements)

Date: 2026-10-14 (archived 2026-10-28)

Short notes on the classic tool chain as first measured from format output. Later work in `tools/` and the level-editor notes supersedes these where they conflict.

## GraalEditor

Version 2.3.1.1, Linux Cyberjoueur. From 2.3 the editor and the online client are separate executables. The copy shipped in the client tree is a Thinstall package. Main form `TAdventure`, document `TAdventureLevel`. Writes decimal `BOARD 0` grids (64 lines of 64 indices) plus LINK/SIGN/CHEST/NPC/BADDY. A file of raw decimal indices does not pass the client `GLEVNW01` loader until rewritten as base64 runs.

## GraalShop

Delphi GANI editor. Sprite mode (`GANI0001`) and movie mode (`GANI0002`). Actor kinds CHAR, SPRITE, SOUND, TEXT.

## Generators

Three writers emit `GLEVNW01` / `GRMAP001`. They do not emit the same file.

- TerrainGenerator: plasma midpoint displacement → `GRMAP001` with `HEIGHTS` blocks (9×9) and `GLEVNW01` levels that are 64 rows of tile 0 plus a `HEIGHTS` overlay.
- DungeonGenerator: 8×11 stamp layout → one base64 `BOARD` of 64×64, edge `LINK`s, and `NPC` blocks. Stamp id 0 is a 4×4 ground fill; stamp id 1 is a hole and is not written.
- GraalLevelGen: image-to-linked-levels pipeline.

## gif2mng

GIF to PNG or MNG. Banner date 2004-06-03. `-b` snaps the palette to the seven Graal body slots and forces transparent index 2.

## RemoteControl

Delphi staff client, predecessor of the GTK `RC2_2.05`. Two sockets (RC at console +0x38c, NPC at +0x390). Classic text codec (id + 0x20). NPC login is type 3 starting with the literal `NCL11012`. Player list packet 0x37 carries a property stream.
