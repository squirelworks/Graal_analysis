<!-- manual: kind=reference status=draft -->
# 3.3 GANI animations

A GANI file is the text animation format that GraalShop reads and writes and that clients load from `levels/ganis/`. This chapter gives its grammar as the editor reads it; how a client plays a GANI is in → §4.

> Status: draft. The grammar is from the GraalShop reader and writer and checked against client sample files; the separate exact-input Mac v5 loader result is scoped in §3.3.7.

## 3.3.1 File

A gani is a text file of keyword lines. The rules below give the general form and the samples it was checked against [bin] (formats/gani.txt).

| Rule | Detail | Source |
| --- | --- | --- |
| form | line-oriented text; the first line is the discriminator | [bin] (formats/gani.txt) |
| case | the parser lowercases each line before comparing keywords; the writer emits uppercase keywords and space-padded columns | [bin] (formats/gani.txt) |
| samples | client samples under `levels/ganis/` and `levels/bomys/` match the sprite dialect, including files that omit the signature | [file] (formats/gani.txt) |

The first line tells sprite mode from movie mode. Each row gives one signature, the mode value it sets and the body that follows [bin] (formats/gani.txt).

| First line | Mode value | Body | Source |
| --- | --- | --- | --- |
| `GANI0001` | 0 | sprite table, header, `ANI` … `ANIEND` (sprite mode) | [bin] (formats/gani.txt) |
| `GANI0002` | 1 | sprite table, header, `MOVIE` … `MOVIEEND` (movie mode) | [bin] (formats/gani.txt) |

## 3.3.2 Grammar

The grammar as the editor accepts it [bin] (formats/gani.txt):

```
file        := signature? sprite* header* body
signature   := "GANI0001" | "GANI0002"
sprite      := "SPRITE" id sheet x y w h description
             | "ATTACHSPRITE"  id parent dx dy
             | "ATTACHSPRITE2" id parent dx dy
header      := "LOOP" | "CONTINUOUS" | "SINGLEDIRECTION"
             | "SETBACKTO" name
             | "BACKCOLOR" "#" hex6
             | "FRAMES" count
             | "DEFAULTHEAD" file | "DEFAULTBODY" file
             | "DEFAULTPARAM"n value | "DEFAULTATTR"n value
             | "COLOREFFECT" id args | "ZOOMEFFECT" id args
             | "ROTATEEFFECT" id args
             | "STRETCHXEFFECT" id args | "STRETCHYEFFECT" id args
             | "EFFECTMODE" id args
body        := ani | movie
ani         := "ANI" step* "ANIEND"
movie       := "MOVIE" actor* "MOVIEEND"
actor       := "ACTOR" name frame* "ACTOREND"
frame       := "FRAME" index token ("," token)*
step        := placement ("," placement)* | "WAIT" n | "PLAYSOUND" name x y
placement   := spriteId x y | "PARAM"n x y | "ATTR"n x y
script      := "SCRIPT" rawlines "SCRIPTEND"
```

In `DEFAULTPARAM`, `DEFAULTATTR`, `PARAM` and `ATTR` the slot number is glued to the keyword, as in `DEFAULTATTR1 hat0.png` and `PARAM1 0 0`; every GANI in the NewWorld beta and NewMain folders is written this way [file][doc] (client-internals/graal-wiki-crosscheck-2026-11-11.md#where-the-wiki-corrects-or-extends-this-repo).

## 3.3.3 Sprite rows

Sprite rows cut images out of sheets. The rules below give their fields, the column widths the writer uses, and how attached sprites work [bin] (formats/gani.txt).

| Rule | Detail | Source |
| --- | --- | --- |
| `SPRITE` | id, sheet, x, y, w, h, description | [bin] (formats/gani.txt) |
| columns | the writer pads the id to 4, the sheet name to 14, and x, y, w and h to 4, then writes the description | [bin] (formats/gani.txt) |
| `ATTACHSPRITE`, `ATTACHSPRITE2` | hang a sprite on a parent sprite with a pixel offset; they are not a second sheet | [bin] (formats/gani.txt) |

Client files therefore look like this [file] (formats/gani.txt):

```
SPRITE    0         SPRITES    0    0   24   12 shadow
SPRITE  200            HEAD    0    0   32   32 head up
SPRITE   20           SWORD   62    0   28   28 sword
```

## 3.3.4 Header

The header keywords set how an animation plays. Each row gives a keyword and its meaning; some are written in only one mode [bin] (formats/gani.txt).

| Keyword | Meaning | Source |
| --- | --- | --- |
| `LOOP`, `CONTINUOUS` | playback flags | [bin] (formats/gani.txt) |
| `SINGLEDIRECTION` | each step holds one row instead of four; written only in sprite mode | [bin] (formats/gani.txt) |
| `FRAMES` | frame count; written only in movie mode | [bin] (formats/gani.txt) |
| `SETBACKTO` | names the GANI to return to | [bin] (formats/gani.txt) |
| `BACKCOLOR` | a `#rrggbb` fill behind the editor preview | [bin] (formats/gani.txt) |
| `DEFAULTHEAD`, `DEFAULTBODY` | reload the head and body images | [bin] (formats/gani.txt) |
| `DEFAULTPARAM`, `DEFAULTATTR` | seed the 30-row attribute grid | [bin] (formats/gani.txt) |
| `COLOREFFECT`, `ZOOMEFFECT`, `ROTATEEFFECT`, `STRETCHXEFFECT`, `STRETCHYEFFECT`, `EFFECTMODE` | stored as an id plus arguments and applied at blit time | [bin] (formats/gani.txt) |
| `SCRIPT` … `SCRIPTEND` | copied through as text; the editor does not execute it | [bin] (formats/gani.txt) |
| `ROTATEPROJECTILE` | from 6.036: a projectile drawn with this GANI is turned to its flight path; the GANI must also be `SINGLEDIRECTION` and drawn facing right; not yet seen in a binary | [doc] (client-internals/graal-wiki-crosscheck-2026-11-11.md#where-the-wiki-corrects-or-extends-this-repo) |

## 3.3.5 Sprite mode body

In sprite mode the body is a list of steps. The rules below say what a step can hold and how directions are laid out [bin] (formats/gani.txt).

| Rule | Detail | Source |
| --- | --- | --- |
| bounds | `ANI` opens the step list and `ANIEND` closes it | [bin] (formats/gani.txt) |
| step | a comma-separated placement row, a `WAIT` hold, or a `PLAYSOUND name x y` cue | [bin] (formats/gani.txt) |
| placement | a sprite id plus x and y, or a `PARAM` or `ATTR` slot plus x and y | [bin] (formats/gani.txt) |
| directions | a step holds four direction rows, or one row when `SINGLEDIRECTION` is set | [bin] (formats/gani.txt) |
| wait | the wait counter starts at 1; each `WAIT` adds to it | [bin] (formats/gani.txt) |

## 3.3.6 Movie mode body

In movie mode the body is a list of actors, each with its own frames. The rules below give that structure [bin] (formats/gani.txt).

| Rule | Detail | Source |
| --- | --- | --- |
| bounds | `MOVIE` opens the actor list and `MOVIEEND` closes it | [bin] (formats/gani.txt) |
| actor | `ACTOR name`, a run of `FRAME` lines, `ACTOREND` | [bin] (formats/gani.txt) |
| actor kind | not a keyword in the frame line but an integer on the actor: 0 CHAR, 1 SPRITE, 2 SOUND, 3 TEXT | [bin] (formats/gani.txt) |
| frame | an index and a comma-separated token list; the tokens become `key=value` strings on the actor's frame record | [bin] (formats/gani.txt) |

## 3.3.7 Shared Mac v5 loader boundary

The shared PowerPC v5 main executable, including an archive copy labelled 5.12, was inspected statically; matching bytes do not authenticate release labels. ANI collects comma-delimited placement records into a group requiring four records, or one with SINGLEDIRECTION. ANIEND accepts a sufficient group and discards an incomplete one. End of input destroys a still-current group rather than establishing its commitment. [bin] (client-internals/macos-v5-animation-group-lifecycle.md)

WAIT adds duration to an existing group. PLAYSOUND stores a resource reference, the current duration and two default fields; both optional numeric arguments must exist to replace those defaults. These storage observations do not prove units, scheduling, audible playback or rendering. SCRIPT collects text through SCRIPTEND or end of input; this loader body does not run an interpreter. Native runtime acceptance, full placement grammar, numeric/tokenizer helpers and GS1/GS2 execution remain untested here. [bin] (client-internals/macos-v5-animation-group-lifecycle.md)
