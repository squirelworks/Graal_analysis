# Local-enter arguments on the public 2.1.0.0 image and on v22

Date: 2026-11-15. Static read of the local-level enter path in the public 2.1.0.0 image and in Graal 2002 v22. Nothing was run. No packet was read. The initial read did not include ver7. The follow-up below traces its local entry. The literal `Player enters local level ` is absent from ver7's string table. That absence is not a reading of ver7's enter body.

## Two values of 31

When the level name is `level1.graal`, `YoshiClanR2.zelda` or `YoshiClanFields.zelda`, both images call a helper. The call passes the level and two 31s. The selected helper state changes are now traced in the follow-up below; the argument values alone do not establish a player move. **[bin]**

The 2.05 revision-2 caller is included in the follow-up below. Its actual stack arguments also contain two doubles equal to 31; this was not established by the original read.

## Name-matched helper: selected static comparison

Follow-up: 2026-11-28. The selected public 2.1.0.0 image and v22 were compared with a separately retained 2.05 revision-2 input (embedded FileVersion 2.0.5.2), the revision used by the [offline tutorial note](offline-tutorial-205.md#special-level-names). The executable identities were bound before analysis; labels and version resources alone do not authenticate a release. This does not independently bind that input to the earlier lab run. No original program, script or lab was executed. Evidence: LOCAL-ENTRY-HELPER-20261128. **[file][bin]**

In all three selected callers, the name table contains `level1.graal`, `YoshiClanR2.zelda` and `YoshiClanFields.zelda`. A match on the caller's string-comparison path passes the level object and two doubles equal to 31 to the helper. In revision 2 the decompiler omitted those stack arguments, but the actual pushes and the callee's stack reads establish them. Exact filename-case acceptance is not established by this comparison. **[bin]**

On the selected normal construction path, each helper allocates an object whose concrete class metadata names `TAdventureBall`, stores the supplied doubles in two fields of that record, stores 68 in another integer field, clears two further fields, and appends the record to a collection owned by the level. The constructor retains the level context, and the examined append routine stores the object pointer and increments the collection count. Object layouts differ between revisions; this is a comparison of those selected operations, not an assertion that the classes or all their methods are identical. **[bin]**

The public-image and revision-2 helpers perform that construction without the two checks found in the selected v22 helper. V22 first requires two global flag bytes to be clear. If either is set, it returns minus one without taking the construction/append path. The meanings and writers of those flags are outside this helper study; the [level-record note](v21-level-record-gate.md) tracks that separate question. **[bin]**

The two 31s therefore reach fields on a newly appended record. This is not evidence that the helper moves the player to (31, 31), nor does the stored integer 68 establish a rendered item, a collision effect or a named gameplay action. Those consumers, callback and exceptional effects, resource limits, repeated-entry behavior and other builds were not established. The [earlier revision-2 lab observations](../manual/04-behaviour/08-offline.md#483-the-single-player-start-levels) still describe visible outcomes; they did not measure this internal collection. G078/G141's selected caller/helper state changes are answered, while these wider behavioral questions remain separate. **[bin]**

## v22 shifts a 3 by 3 table by 64

The public enter body has no 3 by 3 walk.

v22, after the level is swapped, walks a 3 by 3 table of earlier level pointers when an integer field equals 2 and further object tests pass. The integer field equal to 2 is the test in this body. It is not receive id 177. Rows and columns are 0, 1 and 2. A matching slot adds `(row - 1) * 64` and `(column - 1) * 64` to coordinate pairs, so the shifts are -64, 0 and +64. A table with no match clears the coordinate list those shifts would have updated. The initial read did not follow the field's writers; selected stores are traced below. **[bin]**

Receipt. The public 2.1.0.0 image and v22 were the bodies read. The 3 by 3 loop and the shifts of -64, 0 and +64 are that read. The writer follow-up below is limited to the selected v22 input. **[bin]**

### Selected v22 integer-field writers

Follow-up: 2026-11-28. In the same identity-bound v22 input, two examined setup paths store 2 in the integer field used by the local-entry tests. One installs a newly allocated level object before the store. The other resets fields on the current level, stores 2, and clears its 3 by 3 table. Three selected reset paths store zero in the same field; one also clears the current-level pointer. These are direct four-byte field stores, not inferred names for a mode enumeration. Evidence: V22-ENTRY-MODE-WRITERS-20261128. No original program was run. **[bin]**

The [separately traced receive-177 handler](v21-level-record-gate.md#v22-storage-modes) sets the New World global byte. That is different storage and width from this object's integer field, so it is not the direct writer under comparison. This does not rule out later indirect effects of receiving the message. **[bin]**

G080/G142 remain partial: the selected setup/reset stores are identified, but this is not an exhaustive writer or alias census. The complete meanings of the integer values, caller/UI attribution, exceptional paths and runtime transitions remain unproved. **[bin]**

## Widths beside that call

A header that is not one of `Z3-V1.03`, `Z3-V1.04`, `GR-V1.00`, `GR-V1.01`, `GR-V1.02`, `GR-V1.03` or `GLEVNW01` stores a flag byte and the integer 40, and does not swap the level. Linux 3.04 already stores 40 for that rejection (`torque/304-adventure.md`). On these two images the enter line is logged before the test. No send of 40 was read. **[bin]**

On v22, when the name is not already resident, a second lookup is empty, and the same integer field equals 2, the client writes a stream of exactly eight bytes, `GLEVNW01`, and enters with that stream. Another value of the field does not write the stream. The field equaling 2 is the same test as above, and it is not receive id 177. This path sends no packet. **[bin]**

## Ver7 local entry

The local-file wrapper loads the named file into a memory stream and installs a level object before validating the header. The entry body accepts the seven headers listed above. On acceptance, it rewinds the stream, calls the level reader and reports `Level loaded`. A rejected header takes the warning path before the reader. The earlier assignment leaves rollback unverified. **[bin]**

## Open

- [x] ~~Read the helper that receives the two 31 values, on these images and on 2.05.~~ Selected public/v22/2.05 revision-2 construction, field stores, append and v22 guard paths are compared [above](#name-matched-helper-selected-static-comparison); rendering and wider behavior remain unproved.
- [ ] Finish identifying v22's integer field. The selected two stores of 2, three zero stores and distinction from receive 177 are traced above; full writer coverage and value meanings remain open.
- [x] Read ver7's enter body. See the static entry sequence above.
