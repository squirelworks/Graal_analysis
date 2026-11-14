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

The earlier static read (2026-11-14) attributes these save/load routines to
a 2002-05-01 editor also labelled GraalShop 1.1. The separate
[editor comparison](graaleditor-vs-205.md#workflow) describes the old 2002
editor as sprite-only and associates movie support with the 2006 editor.
The exact editor attribution remains unresolved; the grammar below is the
published static description, not a newly authenticated editor identity. **[doc]**

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

## Shipped movie sample and remaining limits

Saved movie existence was already reported in the
[earlier asset survey](../archive/game-assets-worlds-2026-11-01.md): one
archived world's animation set includes a `GANI0002` file. This does not
establish that it is the same sample as the mobile copies below. **[doc]**

A packaged tutorial movie in Classic+ 1.13 and Era+ 1.0 has byte-identical
text in the two inspected copies. Execution-free file parsing observes a
`SPRITE` actor and a `TEXT` actor. The sprite's `visible` value is lowercase
`true`. The text actor uses lowercase `true` for `centered`, `shaded`,
`visible` and `wordwrap`, and lowercase `false` for `bold`, `italic`,
`rightaligned`, `strikeout` and `underline`. Its `sprite #` spelling and
`ACTOR kind name` structure corroborate the grammar already documented
above; they are not newly discovered grammar. **[file]**

Evidence: `IOS-GANI-MOVIE-20261115-01`, registered in the
[evidence index](../docs/evidence-index.tsv). Package inventory and
supplemental text parsing establish shipped declarations only. No native
playback or editor save was tested. The observation establishes these
literal spellings in this sample, not every accepted boolean spelling.
No original asset text or artwork is reproduced here. **[file]**

The sample has no `CHAR` actor. Indexed CHAR-key spelling, the units of
`dx`/`dy`, frame duration, native interpolation/playback and which editor
produced it remain unresolved. A saved declaration alone cannot settle
those runtime or provenance questions. The conflicting editor attributions
above also remain open (manual App. E#612). The separate 2.05 static read
reports no movie-mode support
([comparison](graaleditor-vs-205.md#how-this-compares-with-what-205-can-play)).
**[file][doc]**
