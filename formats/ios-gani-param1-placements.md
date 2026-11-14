# PARAM1 placement structure in two iOS builds

Date: 2026-11-15. Execution-free resource inspection for Classic+ 1.13 and Era+ 1.0. Evidence `IOS-GANI-PARAM1-20261115-04` ([index](../docs/evidence-index.tsv)). No native parser, renderer or device was run. **[file]**

## Field context

The inspected resources contain uppercase `PARAM1` as the first token of an ANI placement group, followed by two positive decimal integer coordinate spellings. This is a placement reference, not merely a symbolic sheet name in a SPRITE declaration. The two field positions were counted separately; SCRIPT bodies were excluded from the placement search. **[file]**

Each selected resource declares `SINGLEDIRECTION` and contains one ANI placement row with two comma-separated groups. In one resource form, the `PARAM1` group is first; in the other it is second. Whitespace separates the three fields within each group. Only slot 1 and uppercase spelling are established by these observations. **[file]**

Two distinct resource contents occur in both inspected builds, giving four package occurrences of the direct symbolic placement. These are shared copies of two forms, not four independent syntax examples. A wider bounded survey of 437 GANI members across 27 preserved packages found no other direct `ATTR`/`PARAM` plus decimal-slot first tokens in ANI groups under this exact search. That search does not exclude other spellings, formats or code-generated content. **[file]**

## Useful preservation contract

A parser preserving these declarations needs to distinguish the symbolic `PARAM1` reference from numeric sprite `0`. Converting a failed numeric parse to zero loses the observed identifier; a serializer can then save a different declaration. A representation can retain the symbolic token without claiming to resolve it to artwork. This is a file-preservation requirement, not a recovered native drawing algorithm. **[file]**

Independent synthetic regressions can distinguish numeric zero from a symbolic reference in either comma-group position, retain their coordinates through serialization, and ensure unresolved symbolic input does not accidentally select numeric sprite zero. Such tests establish the implementation's preservation and fallback behavior; they are not native rendering observations. **[doc]**

## Limits and next questions

The observed coordinate examples are positive integers. Negative or fractional native-coordinate acceptance, other slots, case-insensitive acceptance, default direction behavior without `SINGLEDIRECTION`, native slot resolution, rendering and timing remain unverified. Sprite-sheet references are a separate context and do not establish direct-placement behavior. No original resource text, artwork, member names or artifact hashes are reproduced here. **[file]**

This is separate from the [movie sample's boolean spellings](../tools/graalshop.md#shipped-movie-sample-and-remaining-limits). That earlier study does not supply evidence for these direct ANI placements. **[doc]**

- [x] ~~Distinguish direct ANI symbolic references from SPRITE sheet references in the inspected resources.~~ Bounded structure above.
- [ ] Establish the exact native resolver and coordinate/slot acceptance before claiming playback compatibility.
- [ ] Verify each consuming parser/serializer preserves the symbolic identifier; test renderer fallback separately from native resolution.
