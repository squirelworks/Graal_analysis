# PARAM1 placement structure in two iOS builds

Date: 2026-11-15. Execution-free resource inspection for Classic+ 1.13 and Era+ 1.0. Evidence `IOS-GANI-PARAM1-20261115-04` ([index](../docs/evidence-index.tsv)). No native parser, renderer or device was run. **[file]**

## Field context

The inspected resources contain uppercase `PARAM1` as the first token of an ANI placement group, followed by two positive decimal integer coordinate spellings. This is a placement reference, not merely a symbolic sheet name in a SPRITE declaration. The two field positions were counted separately; SCRIPT bodies were excluded from the placement search. **[file]**

Each selected resource declares `SINGLEDIRECTION` and contains one ANI placement row with two comma-separated groups. In one resource form, the `PARAM1` group is first; in the other it is second. Whitespace separates the three fields within each group. Only slot 1 and uppercase spelling are established by these observations. **[file]**

Two distinct resource contents occur in both inspected builds, giving four package occurrences of the direct symbolic placement. These are shared copies of two forms, not four independent syntax examples. A wider bounded survey of 437 GANI members across 27 preserved packages found no other direct `ATTR`/`PARAM` plus decimal-slot first tokens in ANI groups under this exact search. That search does not exclude other spellings, formats or code-generated content. **[file]**

## Useful preservation contract

A parser preserving these declarations needs to distinguish the symbolic `PARAM1` reference from numeric sprite `0`. Converting a failed numeric parse to zero loses the observed identifier; a serializer can then save a different declaration. A representation can retain the symbolic token without claiming to resolve it to artwork. This is a file-preservation requirement, not a recovered native drawing algorithm. **[file]**

Independent synthetic regressions can distinguish numeric zero from a symbolic reference in either comma-group position, retain their coordinates through serialization, and ensure unresolved symbolic input does not accidentally select numeric sprite zero. Such tests establish the implementation's preservation and fallback behavior; they are not native rendering observations. **[doc]**

## Consumer reconciliation (2026-11-21)

This is a bounded source audit of the following current consumers, not a new
native parser or drawing run. Their implementation already separates uppercase
`PARAM1` from numeric sprite zero; no duplicate parser migration is needed.

- **Core**, revision `89cf379fda9b037012d2406a2eb910683c000bb1`:
  [`GaniPlacementReference`](https://github.com/squirelworks/seihai-core/blob/89cf379fda9b037012d2406a2eb910683c000bb1/crates/seihai-core/src/assets/gani.rs#L19)
  stores `Sprite` and `Param1` separately. Its display form preserves the token,
  and `param1_is_distinct_from_numeric_zero_in_either_group` tests both comma
  positions and coordinates. The shared
  [drawing helper](https://github.com/squirelworks/seihai-core/blob/89cf379fda9b037012d2406a2eb910683c000bb1/crates/seihai-draw/src/sprite.rs#L71)
  matches only `Sprite` before lookup; its `unresolved_param1_never_draws_numeric_zero`
  test distinguishes a visible numeric control from transparent unresolved input.
- **Seihai**, revision `58d3fbabc7539163d5fd82cbe56fcf6baa24947d`:
  [drawing and bounds](https://github.com/squirelworks/seihai/blob/58d3fbabc7539163d5fd82cbe56fcf6baa24947d/crates/seihai-mae/src/render/tiles.rs#L700)
  explicitly match `Sprite` before lookup. The test
  `numeric_zero_draws_and_unresolved_param1_does_not_draw_or_expand_bounds`
  checks pixels and bounds separately. The current manifest follows core main;
  no committed lockfile was found in this tree, so this is not an exact resolved
  dependency assertion for an arbitrary local build.
- **Servertools**, revision `ca8b640d946e98d760071c43efb0d106954e81a4`:
  the [LAT encoder](https://github.com/squirelworks/seihai-servertools/blob/ca8b640d946e98d760071c43efb0d106954e81a4/crates/lat-core/src/gani.rs#L217)
  serializes the reference rather than converting it to a numeric id.
  `symbolic_placement_survives_encode_without_becoming_zero` reparses both group
  orders and checks the symbolic coordinates and numeric-zero control. Its
  manifest and lockfile select core/draw `v0.7.2`, revision
  `81ba7e24df32ff5f937d0c09e7d5f75da6aa6913`; the typed reference and parser test
  are present in that selected core, not merely in newer main.
- **GCR**, main revision `926cf3aa17828b3903eee77551d372ffae57a423`:
  the [Pascal parser](https://github.com/squirelworks/graal-client-repro/blob/926cf3aa17828b3903eee77551d372ffae57a423/common/GAni.pas#L142)
  and [C++ parser](https://github.com/squirelworks/graal-client-repro/blob/926cf3aa17828b3903eee77551d372ffae57a423/common/cpp/quattro/files/gani.cpp#L42)
  preserve `PARAM1` as a negative sentinel, distinct from zero. Pascal
  `FindSprite` rejects negative ids before indexing. The C++ world renderer
  handles symbolic parts and continues before ordinary sprite lookup; its
  carry/image fallback is an implementation policy, not native iOS evidence.
  These two reader APIs have no ANI serializer; this is not a round-trip claim.

The Rust parser, drawing and editor regression **definitions** above were read;
they were not rerun for this reconciliation. An additional independent synthetic
Pascal parser/lookup control ran against the unchanged GCR reader: 14 assertions
passed, with zero unfreed memory blocks. It checked both group positions,
retained positive coordinates, distinct numeric-zero resolution and rejection of
the unresolved sentinel before indexing. It did not run a renderer or serializer.
Evidence `G231-CONSUMER-CONTROL-20261121` identifies that offline control. Existing
GCR carry tests are separate from this zero-versus-symbol control. **[doc]**

This settles preservation and fallback for the named readers, renderers and
actual editor serializer. It does not establish arbitrary symbolic tokens,
other slots/case variants, native coordinate acceptance or native playback.

## Limits and next questions

The observed coordinate examples are positive integers. Negative or fractional native-coordinate acceptance, other slots, case-insensitive acceptance, default direction behavior without `SINGLEDIRECTION`, native slot resolution, rendering and timing remain unverified. Sprite-sheet references are a separate context and do not establish direct-placement behavior. No original resource text, artwork, member names or artifact hashes are reproduced here. **[file]**

This is separate from the [movie sample's boolean spellings](../tools/graalshop.md#shipped-movie-sample-and-remaining-limits). That earlier study does not supply evidence for these direct ANI placements. **[doc]**

- [x] ~~Distinguish direct ANI symbolic references from SPRITE sheet references in the inspected resources.~~ Bounded structure above.
- [ ] Establish the exact native resolver and coordinate/slot acceptance before claiming playback compatibility.
- [x] ~~Verify uppercase `PARAM1` preservation and fallback in the named current consumers.~~ [Consumer reconciliation](#consumer-reconciliation-2026-11-21); actual serializer and reader-only APIs distinguished.
