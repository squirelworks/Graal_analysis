# Public 2.1.0.0 level open, and the ver7 and v22 neighbours

Date: 2026-11-15.

Static read of the public 2.1.0.0 image (2001-11-13), Graal 2002 ver7, and Graal 2002 v22. Nothing was run. These paths are local file reads. No client-to-server send of a level, a baddy, a chest or a weapon was read.

## Open gate

The public image's open function returns without reading when the level object is absent.

Otherwise it reads eight bytes and accepts them in this order: `Z3-V1.03`, `Z3-V1.04`, `GR-V1.00`, `GR-V1.01`, `GR-V1.02`, `GR-V1.03`, `GLEVNW01`.

Any other eight bytes open a dialog. The caption is `Warning`. The text is `Unsupported file type!`. The level is not loaded, and the status text is not set to `Level loaded`.

A match clears a 64 by 64 area, rewinds the stream to the start, parses it, and then sets the status text `Level loaded`. **[bin]**

The 2.05 editor accepts the same seven magics and uses the same rejection text (`client-internals/level-editor-205.md`). The 2.22 and 2.31 string tables contain `Unsupported file type!`, and the exported 2.22 code still has no caller for it (`tools/level-editor/222-reference.md`). This read is the caller in the public 2.1.0.0 image.

Ver7 and v22 both contain `Unsupported file type!`. The follow-up below identifies the ver7 caller. The v22 caller remains open. **[bin]**

## Local enter

The public function logs `Player enters local level ` plus the level name, then tests a supplied stream against the same seven magics. A mismatch stores a flag byte and the constant 40, and does not swap the level. A match, or a call with no stream, continues into the swap. **[bin]**

The swap compares the level name with three literals: `level1.graal`, `YoshiClanR2.zelda` and `YoshiClanFields.zelda`. On the public 2.1.0.0 image and on v22, a match calls a helper with the level and two floating-point values, each 31. The [selected helper comparison](v21-local-enter.md#name-matched-helper-selected-static-comparison) now traces record construction and append, including the conditional v22 path. This is not a player-position or rendering test. **[bin]**

Linux 3.04 uses the same seven magics and the same constant 40. Its note says the enter line is logged when there is no game connection, and a rejected magic does not log (`torque/304-adventure.md`). In the public function, the log is emitted and the magic test follows it. A connection test around this call was not read. A strings pass over ver7 did not find `Player enters local level `. **[bin]**

## What the parser stores

In both the public image and ver7, `GLEVNW01` goes to a text loader and that function returns. `GR-V1.02` and `GR-V1.03` pass 13 to the board decoder. Any other magic that reaches the decoder, including `Z3-V1.03` and `Z3-V1.04`, passes 12. That is the split the 2.05 reader uses (`formats/level-binary-client.md`). **[bin]**

The public image then stores five sections, in order:

1. Lines until a one-character marker. Each other line is passed to a helper before the resulting record is inserted.
2. Records read up to a newline after at least three bytes. The section ends on a record shorter than three bytes, or on a record whose first byte is at least 128. The first two bytes are raw coordinates. The third byte is the type. A longer tail is split on `\` into at most three fields. That is the baddy record in manual §3.1.2.4.
3. When the magic is `GR-V1.00`, `GR-V1.01`, `GR-V1.02` or `GR-V1.03`: lines until a one-character marker. The x and y are the first two bytes minus 32, stored as floats. The text from the third character is split on `#` into two fields.
4. Reached from the `GR-V1.01`, `GR-V1.02` and `GR-V1.03` tests: lines until a one-character marker, four values of byte-minus-32 (two coordinates, an item, and a sign index), then a zero flag. That is the chest record in manual §3.1.2.5. `GR-V1.00` also enters the link loop in step 3. A [follow-up comparison](v21-level-record-gate.md) confirms that a fresh header check skips this chest section for `GR-V1.00`.
5. Remaining lines. The x and y are byte-minus-32 integers, and the text from the third character is a string. That is the sign record in manual §3.1.2.6.

**[bin]**

ver7's traced body stores the whole lines of step 1, the link records of step 3, and the sign records of step 5. Its scan of the baddy end condition does not construct a baddy object. It does not construct the four-field chest records. The receive ids for baddies and chests on ver7 remain the lab question in [`graal2002-and-140-builds.md`](graal2002-and-140-builds.md). This paragraph is the file reader only. **[bin]**

A follow-up static read binds the marker to the entire one-character line `#` in the selected text-record, link-record and chest loops of the public 2.1.0.0, ver7 and v22 binary readers. The equality branch exits the section. This matches the delimiter documented for 2.05 rev 2 ([binary level format](../formats/level-binary-client.md)). Baddies use a separate binary termination rule. Section order, record support and NW behavior are outside this comparison. **[bin]**

## v22 when the file is missing

v22's open path loads by handle when a lookup by name returns one. When that lookup is empty and a second opener returns a stream, it loads that stream and releases it. When both are empty and a mode field equals 2, it creates a stream, writes the eight bytes `GLEVNW01`, and loads that stream. When both are empty and the mode field is some other value, this function does not load. **[bin]**

That mode field is a stored integer. Receive id 177, which stores a New-World flag with an empty payload on v22, was not the body read here. What writes the mode field was not read. This path sends no packet.

## Text writer on the public image

The public image's writer starts with `GLEVNW01`, then 64 lines of 64 tiles. Each tile is two base64 characters from a 12-bit index, high six bits first. It then writes `LINK ` lines, `CHEST ` lines, and a `BADDYEND` terminator. Those shapes are the text format in `formats/glevnw01.txt`. This pass did not re-measure every field of the `LINK` and `CHEST` lines. **[bin]**

## Gani direction count

The public image's gani reader starts a step at four direction rows. `SINGLEDIRECTION` changes that count to one. At `ANIEND`, a group with fewer rows than the count is dropped, and a group with at least that many rows is kept. The grammar (`formats/gani.txt`) and the shared Mac v5 executable (`client-internals/macos-v5-animation-group-lifecycle.md`) already state that rule. This read shows it in the public 2.1.0.0 image. `SPRITE`, `COLOREFFECT` and `ZOOMEFFECT` are recognised. Their minimum field counts were not separated from the keyword token, so they are not restated. **[bin]**

## Weapon name on v22

v22 contains the literal `Control-NPC`. It does not contain `controlnpc.txt`. The one reference compares a list item's name with `Control-NPC`. When the names match and a flag byte on that object is clear, it calls a helper. The initial read stopped at that call; the selected follow-up below traces the helper. **[bin]**

A strings pass over the public image found neither literal. ver7's inventory has both, next to each other. The body that installs a weapon from `controlnpc.txt` on ver10 is a different read and is not repeated here. **[bin]**

### v22 event helper: selected follow-up

The examined caller requires its stored mode to equal 2 and a current level object. It walks that level's list, compares each non-null item's decoded name with `Control-NPC`, and calls the helper only while the item's initialization byte is clear. The arguments include the literal `playerenters` and the current level. The mode's writer and meaning are not identified by this call. **[bin]**

The helper copies the pending string-list contents and saves an auxiliary string and integer. It clears the working list and string, sets the integer to -1, adds `playerenters`, and calls the shared script executor. On normal return it copies back the saved list contents and restores the string and integer. The executor's initialization path adds `created` through a separate working-list reference and sets the initialization byte before command execution; identity with the wrapper's pending list is not established. These steps do not establish an ordering of executed event handlers, a complete object rollback or restoration after an exception. **[bin]**

The selected wrapper does not assemble a fixed outgoing packet. It invokes script dispatch; effects of the executed commands, including possible network output, were not followed through the full interpreter. No packet format or runtime result is established for this `Control-NPC` path. G079 therefore remains partial. The retained static receipt is owner-held under `V2104-CONTROLNPC-EVENT-20261128` in the [evidence index](../docs/evidence-index.tsv). **[bin]**

## Selected ver8, ver9, ver10 and ver13 readers

The four examined readers match ver7 in the selected normal top-level paths. `GLEVNW01` goes to a separate reader. The binary board call selects 13 bits for `GR-V1.02` and `GR-V1.03`, and 12 bits on its other path. The opening record section passes each complete line to a helper that tokenizes it before the reader inserts the resulting object. **[bin]**

For `GR-V1.00` through `GR-V1.03`, the link section converts the first two bytes minus 32 to floating-point coordinates and splits the remaining text on `#`. The final sign loop inserts records with integer coordinates decoded by subtracting 32 and a processed text tail. The [previous record-gate comparison](v21-level-record-gate.md) covers the baddy and chest loops. This comparison covers selected normal branches and helper prefixes. The separate NW reader, complete helper equivalence and runtime behavior remain open. **[bin]**

## Open points

- [x] Read the one-character marker as text and compare it with the 2.05 rev 2 delimiter. See the comparison above.
- [x] Find the ver7 `Unsupported file type!` caller. See the follow-up below.
- [ ] Identify a v22 caller for the same warning.
- [x] Compare the selected level readers in ver8, ver9, ver10 and ver13. See the static comparison above.
- [x] ~~Read the effect of the helper called for `level1.graal`, `YoshiClanR2.zelda` or `YoshiClanFields.zelda`.~~ Selected record construction/field stores/list append and the v22 guard are traced in the [helper comparison](v21-local-enter.md#name-matched-helper-selected-static-comparison); runtime meaning remains separate.
- [ ] Follow the v22 helper after a `Control-NPC` name match, including any packet it sends.
- [ ] Finish identifying v22's mode field. The [selected writer follow-up](v21-local-enter.md#selected-v22-integer-field-writers) traces two stores of 2 and three zero stores, distinct from receive 177's global-byte write; full writer coverage and value meanings remain open.

## Selected invalid-header paths

Ver7's local-file entry uses `Unsupported file type!` with a `Warning` caption after all recognized headers fail. The selected v22 rejection path sets a failure flag and stores 40 before returning. The same warning text is present in v22. Its observed assignment and cleanup do not identify a dialog caller. **[bin]**
