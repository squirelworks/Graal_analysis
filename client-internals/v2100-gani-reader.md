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

Any other line in the block is split on commas. A piece is kept only when it has exactly three fields. The second and third fields are integers. The first field is an integer sprite id, or `PARAM` followed by an integer, or `ATTR` followed by an integer. A prefix value of 0 or below does not by itself keep the piece. The prefix spellings are now recovered by the bounded follow-up below. **[bin]**

### Placement prefixes: static follow-up (2026-11-23)

The examined archive-labelled public image is 1,771,008 bytes with embedded FileVersion 2.1.0.0, matching the public-image descriptors in the [build inventory](graal2002-and-140-builds.md#form-resources). Version and size are not vendor authentication or a claim about every image with that version. Only the client executable was extracted for static analysis; no installer, client or script was run. Evidence: V2100-GANI-PREFIXES-20261123. **[file][bin]**

In the placement branch of the same reader identified by its `ANIEND` and `PLAYSOUND` references, the first test uses the five-byte literal `PARAM`; the next uses the four-byte literal `ATTR`. Both raw string objects and the instructions that pass them to the prefix helper were read. The helper compares the beginning of the candidate with the literal's bytes; it is not a search for that text anywhere in the token, or a whole-token equality test. This does not establish a case-normalization policy for the complete file grammar. **[bin]**

For `PARAM`, the reader takes the tail starting at character 6 (one-based); for `ATTR`, at character 5. The tail goes through the same integer-conversion helper used for the placement coordinates, and the two prefix results go into separate fields. If neither prefix matches, the first field instead goes through integer conversion and sprite lookup. The normal keep branch requires a found sprite or a positive prefix index; zero or a negative prefix index alone does not retain the placement. **[bin]**

This closes G144's literal-spelling question for the examined image. It does not prove parameter/attribute value resolution at rendering, malformed-number recovery, index upper bounds, acceptance of arbitrary suffixes, or the grammar of ver7/v22. The decompiler's exception-handler and value-flow coverage is incomplete; the literal bytes, suffix positions and normal keep/discard branch were checked against instructions rather than inferred from a high-level return type. The other open questions below remain separate. **[bin]**

## `SPRITE`, `COLOREFFECT`, `ZOOMEFFECT`

The first field is the keyword. A call with no arguments sits between taking that field and reading the field count. The call was not identified, so it is not a traced removal of the keyword. The counts of fields remaining after the keyword are an inference from the next read being an integer. They are not a measured count. **[inf]**

| Keyword | Fields remaining after the keyword | Fields this body reads |
| --- | --- | --- |
| `SPRITE` | more than five, inferred | an integer, a text name, and four integers. A further field is not stored |
| `COLOREFFECT` | more than four, inferred | that integer and four floating-point values, when the integer finds a sprite already stored. A miss stores nothing |
| `ZOOMEFFECT` | more than one, inferred | that integer and one floating-point value, with the same sprite test |
| `SETBACKTO` | at least one, inferred | that field as text |

The last column is what this body reads after the call. **[bin]**

`CONTINUOUS` and `SINGLEDIRECTION` each set a flag byte. One more flag byte, beside those two, is set by a header word this read did not recover. `SCRIPT` collects the following lines until `SCRIPTEND`. The separator between those lines was not recovered, and this body does not run the text. A line that matches none of these words is not stored. This body does not test `ATTACHSPRITE` or the movie-mode words. **[bin]**

The word that opens the block `ANIEND` closes was not recovered as text in this read.

## Open

- [x] ~~Recover the five-character and four-character prefix spellings.~~ `PARAM` and `ATTR`, bound to the selected public image's actual placement branch; see [the static follow-up](#placement-prefixes-static-follow-up-2026-11-23).
- [ ] Recover the block opener and the third flag word.
- [ ] Identify the no-argument call between the keyword and the field count. Until that call is a traced removal, the post-keyword counts stay an inference.
- [ ] Compare this reader with ver7 and with v22.
