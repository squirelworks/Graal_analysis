# GraalShop

Delphi GANI editor. Name is a Photoshop pun, not a store.

## Modes

- Sprite mode (`GANI0001`): four direction rows, placements on a sheet.
- Movie mode (`GANI0002`): actors of kinds CHAR, SPRITE, SOUND, TEXT.

Domain objects recovered from RTTI: `TGraalAni`, `TGraalAniSprite`, `TGraalAniStep`, `TGraalActor`, `TEditFrame`.

## Contract

A GANI file is line-oriented. `SPRITE` / `ANI` / `ANIEND` / `PLAYSOUND` / `DEFAULTATTR` blocks. The stepper advances the frame index. The shop copies the script and does not run it.

Offline tiledef used by the client tree: `picso.png,offlinetutorial,1,0,0`.

## Movie mode file grammar

Read from the save and load routines of the 2002-05-01 `GraalShop.exe`
(the build also shipped as `GraalShop1.1.exe`). Static read, 2026-11-14.

```
GANI0002
SPRITE …                      ; sprite table as in sprite mode
FRAMES <count>                ; written only in movie mode
LOOP / CONTINUOUS / BACKCOLOR #rrggbb / SETBACKTO / DEFAULT* / COLOREFFECT / ZOOMEFFECT
                              ; SINGLEDIRECTION is never written in movie mode
SCRIPT … SCRIPTEND            ; optional
MOVIE
  ACTOR <kind> <name>         ; kind: CHAR, SPRITE, SOUND or TEXT
    FRAME <n> <key>=<value>,<key>=<value>,…
    …
  ACTOREND
                              ; a blank line between actors
MOVIEEND
```

- Indents are two spaces for `ACTOR`/`ACTOREND` and four for `FRAME`. The
  loader splits each line into words, so the indent does not matter.
- `FRAME n` is a keyframe at timeline frame `n`. After the number, the rest of
  the line is split on `,`, each piece trimmed, and empty pieces dropped. So
  values cannot contain a comma.
- Each piece is `key=value`. On edit, a piece with only a key deletes that key
  from the keyframe, and a keyframe left with no keys is removed.
- The actor's state at frame `t` is the last keyframe at or before `t` for each
  key, except `dx` and `dy`, which move linearly between keyframes.
- The timeline runs `FRAMES` frames; `LOOP` wraps it.

Keys by actor kind (the key strings the player looks up):

| Kinds | Keys |
|---|---|
| all | `dx`, `dy` (position, interpolated), `layer`, `visible` |
| CHAR | `playerlook`, `dir`, `ani`, `chat`, `head`, `body`, `sword`, `shield`, `horse`, three `attr`, three `param` and five `color` keys with an index |
| SPRITE | `sprite #` (sprite id from the table), `PARAM`/`ATTR` image sources |
| SOUND | `file` |
| TEXT | `text`, `font`, `fontsize`, `color` (hex), `zoom`, `bold`, `italic`, `underline`, `strikeout`, `centered`, `rightaligned`, `wordwrap`, `shaded` |

Not pinned down statically: how booleans and the indexed keys (`param1` or
`param 1`) are spelled in the file, and the unit of `dx`/`dy`. A saved
`GANI0002` file would settle all three; we hold none. The 2.05 client does not
play `GANI0002` (see `graaleditor-vs-205.md`).
