# Public 2.1.0.0 gani field counts

Date: 2026-11-15. Static read of the gani line reader in the public 2.1.0.0 image (FileVersion 2.1.0.0, shipped 2001-11-13). Nothing was run. ver7, ver8, ver9, ver10, ver13 and v22 were not compared. This is a file reader. No packet was read.

The direction-row minimum, four or one after `SINGLEDIRECTION`, and `ANIEND` dropping a short group, are already stated for the shared Mac v5 loader (`macos-v5-animation-group-lifecycle.md`) and for the editor grammar (`formats/gani.txt`). This image uses that same minimum. The counts below are the part that note does not give.

## `PLAYSOUND`

Inside the block that `ANIEND` closes, a line whose text starts with `PLAYSOUND` is stored when it has more than one field and a frame is open.

| Field | What is stored |
| --- | --- |
| 1, the field after the keyword | the sound name |
| two floating-point slots | `1.5` and `2.0` |
| 2 and 3, only when the line has more than three fields | those two numbers replace `1.5` and `2.0` |

The sound is also stamped with the frame's counter at that moment. The counter's unit, and whether the sound is played, were not read. **[bin]**

The Mac v5 loader stores two default fields and replaces them only when both optional numbers are present. It does not give the two values. **[bin]**

## `WAIT` and a placement

A line whose text starts with `WAIT`, with more than one field and an open frame, adds field 1 as an integer to that counter. The counter's starting value was not read in this function. **[bin]**

Any other line in the block is split on commas. A piece is kept only when it has exactly three fields. The second and third fields are integers. The first field is an integer sprite id, or a five-character prefix whose tail is an integer, or a four-character prefix whose tail is an integer. A prefix value of 0 or below does not by itself keep the piece. The two prefix spellings were not recovered. **[bin]**

## `SPRITE`, `COLOREFFECT`, `ZOOMEFFECT`

The first field is the keyword. A call with no arguments sits between taking that field and reading the field count. This note treats the call as removing the keyword, because the next read of the first remaining field is an integer.

| Keyword | Kept when | Stored fields |
| --- | --- | --- |
| `SPRITE` | more than five fields remain | an integer, a text name, and four integers. A further field is not stored |
| `COLOREFFECT` | more than four fields remain, and the first integer finds a sprite already stored | that integer and four floating-point values. A miss stores nothing |
| `ZOOMEFFECT` | more than one field remains, with the same sprite test | that integer and one floating-point value |
| `SETBACKTO` | at least one field remains | that field as text |

`CONTINUOUS` and `SINGLEDIRECTION` each set a flag byte. One more flag byte, beside those two, is set by a header word this read did not recover. `SCRIPT` collects the following lines until `SCRIPTEND`. The separator between those lines was not recovered, and this body does not run the text. A line that matches none of these words is not stored. This body does not test `ATTACHSPRITE` or the movie-mode words. **[bin]**

The word that opens the block `ANIEND` closes was not recovered as text in this read.

## Open

- [ ] Recover the five-character and four-character prefix spellings.
- [ ] Recover the block opener and the third flag word.
- [ ] Compare this reader with ver7 and with v22.
