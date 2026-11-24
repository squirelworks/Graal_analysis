# Public 2.1.0.0 gani field counts

Date: 2026-11-15. Static read of the gani line reader in the public 2.1.0.0 image (FileVersion 2.1.0.0, shipped 2001-11-13). Nothing was run. The original study did not compare the other images; the bounded ver7/v22 follow-up below now covers the documented reader features. ver8, ver9, ver10 and ver13 remain outside this comparison. This is a file reader. No packet was read.

The direction-row minimum, four or one after `SINGLEDIRECTION`, and `ANIEND` dropping a short group, are already stated for the shared Mac v5 loader (`macos-v5-animation-group-lifecycle.md`) and for the editor grammar (`formats/gani.txt`). This image uses that same minimum. The counts below are the part that note does not give.

## `PLAYSOUND`

Inside the `ANI` block that `ANIEND` closes, a line whose text starts with `PLAYSOUND` is stored when it has more than one field and a frame is open.

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

The first field is the keyword. The intervening call was previously unidentified because its decompiled presentation omitted the register arguments. The follow-up below resolves it as first-element deletion with index zero before the later count checks. These selected normal-path minima are now statically verified after keyword removal, rather than inferred from the next field's type. No runtime count was measured. **[bin]**

| Keyword | Fields remaining after the keyword | Fields this body reads |
| --- | --- | --- |
| `SPRITE` | at least six, statically verified | an integer, a text name, and four integers. A further field is not stored |
| `COLOREFFECT` | at least five, statically verified | that integer and four floating-point values, when the integer finds a sprite already stored. A miss stores nothing |
| `ZOOMEFFECT` | at least two, statically verified | that integer and one floating-point value, with the same sprite test |
| `SETBACKTO` | at least one, statically verified | that field as text |

The last column is what this body reads after the call. Having enough fields does not by itself prove successful numeric conversion, a matching sprite or rendered output. **[bin]**

`LOOP`, `CONTINUOUS` and `SINGLEDIRECTION` each set a separate flag byte. The `LOOP` spelling and the `ANI` opener are bound by the follow-up below. `SCRIPT` collects the following lines until `SCRIPTEND`. The separator between those lines was not recovered, and this body does not run the text. A line that matches none of these words is not stored. This body does not test `ATTACHSPRITE` or the movie-mode words. **[bin]**

### Block opener and third flag: static follow-up (2026-11-23)

This follow-up uses the same examined image and identity qualification as the [placement-prefix study](#placement-prefixes-static-follow-up-2026-11-23). The selected retained reader instructions were compared with a fresh constant-window read from that unchanged file, mapped through its observed PE section headers. The word lengths and bytes are three characters for `ANI` and four for `LOOP`. No original program or Graal script was executed. Evidence: V2100-GANI-HEADER-WORDS-20261123. **[file][bin]**

A header comparison with `ANI` sets the reader's animation-block mode. The main line loop tests that mode to select the block-reading path. In that path, matching `ANIEND` processes the current direction group using the existing minimum-row check, clears the pending group and clears the mode. This binds the opener to the selected parser transition; it is not a claim about playback or a complete malformed/end-of-file grammar. **[bin]**

Matching `LOOP` sets a stored byte flag to one. The neighboring `CONTINUOUS` and `SINGLEDIRECTION` branches set different bytes. The latter also sets the direction-row minimum to one rather than the reader's initial four. The selected `LOOP` branch changes its flag, not that minimum or the animation-block mode. Its name does not establish how a later renderer or timer consumes it. **[bin]**

G145's two-word recovery is answered for this input. Default/reset behavior, interactions among the flags, rendering/repeat semantics, error recovery and other builds are not established by these selected normal-path observations. The G146 call/count follow-up below is separate; G147's later bounded cross-build comparison is recorded below. **[bin]**

### Keyword removal and field counts: static follow-up (2026-11-23)

This uses the same examined image and [identity qualification](#placement-prefixes-static-follow-up-2026-11-23). The tokenizer constructs a fresh list whose concrete class metadata identifies `TStringList`; the selected construction and return instructions bind that object to the caller. The reader checks that the list is nonempty, reads its element zero as the keyword, then passes the list object and index zero to a virtual method. Thus the apparent argument-free call is a decompiler limitation, not the instruction-level call contract. Evidence: V2100-GANI-KEYWORD-REMOVAL-20261123. **[bin]**

The concrete method-table target identifies the operation by its state changes: on its normal path, it finalizes the indexed entry, decrements the list's count and moves the remaining entries down. The caller's zero index therefore removes the first entry it just read. The selected count getter returns that same decremented count field; the selected element getter reads the indexed string entry. The caller subsequently checks at least six remaining fields for `SPRITE`, five for `COLOREFFECT`, two for `ZOOMEFFECT` and one for `SETBACKTO`. Those count checks concern the list after keyword removal. **[bin]**

This closes G146's call-identification and post-keyword-count question for the selected reader. It is based on register setup, concrete table entries, getter/deletion/copy instructions and the following branch thresholds, not a guessed source-level method name. Decompiler return typing and exception-handler coverage remain incomplete. Error/callback effects, malformed input, numeric domains, allocation safety, playback and other builds were not established; the result describes the normal path, not a runtime acceptance test. No original client or Graal script was run. **[bin]**

### Selected-reader comparison with ver7 and v22 (2026-11-24)

The documented public image was compared statically with two separately retained inputs labelled ver7 and v22. The examined ver7 input is 1,665,536 bytes with embedded FileVersion 2.1.0.0; v22 is 1,805,824 bytes with embedded FileVersion 2.1.0.4. These descriptors match the [build inventory](graal2002-and-140-builds.md#form-resources), but release labels, sizes and version resources do not authenticate a vendor release or identify every build with that version. Evidence: V2100-GANI-READER-COMPARE-20261124. No original program or Graal script was executed. **[file][bin]**

For each input, the reader was located through its actual `ANIEND` reference. The selected instruction paths, literal data, tokenizer, prefix helper, concrete list-method target and count getter were inspected separately. Address-stripped pseudocode similarity was used only to locate corresponding branches; it is not proof that the binaries or their callees are equivalent. **[bin]**

No difference was found in these finite normal-path storage contracts:

- `ANI` selects animation-block mode; `ANIEND` checks the pending direction group and clears that mode. The minimum starts at four and the selected `SINGLEDIRECTION` branch changes it to one. `LOOP`, `CONTINUOUS` and `SINGLEDIRECTION` use separate flag stores.
- `WAIT` adds the integer field to an open frame's counter. `PLAYSOUND` stores the sound name and current counter, initializes the two slots to `1.5` and `2.0`, and reads the optional pair only when both fields exist.
- A placement piece has exactly three fields. The first follows sprite lookup or the byte-prefix tests `PARAM` and `ATTR`, with one-based tail starts six and five and separate index fields. A found sprite or positive prefix index is required by the normal keep branch; the two coordinates use integer conversion.
- The tokenizer returns the concrete string-list object used by the caller. The caller reads its first entry and invokes deletion at index zero; the selected method decrements the same count field returned by the getter. Post-keyword minima are six for `SPRITE`, five for `COLOREFFECT`, two for `ZOOMEFFECT` and one for `SETBACKTO`, with the field reads described above. Color and zoom stores still require a found sprite.
- `SCRIPT` selects text collection and `SCRIPTEND` leaves that mode. The selected normal header dispatch has no `ATTACHSPRITE` or movie-word branch. This is a boundary of the inspected dispatch, not a claim that those features are absent from the entire client. **[bin]**

This answers G147's comparison of the documented reader features for these three inputs. It does not establish whole-reader or whole-client equivalence, complete callee behavior, numeric acceptance/error recovery, callback effects, resource safety, rendered results, sound scheduling, counter units/start, flag reset/interactions, script execution or other builds. In particular, the comparison does not turn an uninspected malformed or exceptional path into an acceptance guarantee. Decompiler return typing and exception-handler coverage remain incomplete; actual register setup, returned-value instructions, data and normal branches were used where the high-level output omitted them. **[bin]**

## Open

- [x] ~~Recover the five-character and four-character prefix spellings.~~ `PARAM` and `ATTR`, bound to the selected public image's actual placement branch; see [the static follow-up](#placement-prefixes-static-follow-up-2026-11-23).
- [x] ~~Recover the block opener and the third flag word.~~ `ANI` and `LOOP`, bound to selected parser-mode and separate flag stores; see [the static follow-up](#block-opener-and-third-flag-static-follow-up-2026-11-23).
- [x] ~~Identify the no-argument call between the keyword and the field count.~~ The instructions pass index zero to the concrete first-entry deletion method; the selected post-removal count thresholds are verified. See [the static follow-up](#keyword-removal-and-field-counts-static-follow-up-2026-11-23).
- [x] ~~Compare this reader with ver7 and with v22.~~ The documented normal-path storage contracts match in the three selected inputs; see [the bounded static comparison](#selected-reader-comparison-with-ver7-and-v22-2026-11-24). Whole-client and runtime equivalence are not established.
