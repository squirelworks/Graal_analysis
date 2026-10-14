# GraalShop

Delphi GANI editor. Name is a Photoshop pun, not a store.

## Modes

- Sprite mode (`GANI0001`): four direction rows, placements on a sheet.
- Movie mode (`GANI0002`): actors of kinds CHAR, SPRITE, SOUND, TEXT.

Domain objects recovered from RTTI: `TGraalAni`, `TGraalAniSprite`, `TGraalAniStep`, `TGraalActor`, `TEditFrame`.

## Contract

A GANI file is line-oriented. `SPRITE` / `ANI` / `ANIEND` / `PLAYSOUND` / `DEFAULTATTR` blocks. The stepper advances the frame index. The shop copies the script and does not run it.

Offline tiledef used by the client tree: `picso.png,offlinetutorial,1,0,0`.
