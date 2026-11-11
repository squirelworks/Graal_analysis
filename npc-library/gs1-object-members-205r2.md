# GS1 object-array member binding in exact 2.05r2

Evidence GS1-OBJECT-MEMBERS-205R2-20261109-01. Researcher-verified original executable SHA-256: b0e39a04ca0891d0f02282a113a1cd80ddf7a1880a786c5831f26a452e8cbb08. This pass uses freshly decoded compiled records and parser instructions, plus original-matching recovered evaluator/helper bodies. The static record performs no target execution; the separate runtime controls below provide additional original-client observations. Numeric expression IDs below are language identifiers, not binary addresses.

## Parser binding

The original table contains both each family name and its explicit member suffix. The parser scans records in order, compares the family name, checks token count against the signature, checks bracket punctuation, and compares the member token against the stored suffix. It parses the bracket index in numeric mode, stores that child expression, and copies the matched record's expression ID into the node. It exits at the first successful record. Consequently these mappings are direct compiled-table and parser evidence, rather than an inference from documentation order.

There are 36 records for the seven requested families. One duplicate spelling leaves 35 distinct ordinary member names:

- compus: x=600, y=601, type=602, dir=603, headdir=604, power=605, mode=606.
- bombs: x=640, y=641, power=642, time=643.
- arrows: x=660, y=661, dir=662, dx=663, a second dx=664, type=665, from=666.
- items: x=680, y=681, type=682, time=683.
- explos: x=700, y=701, power=702, time=703, dir=704.
- horses: x=720, y=721, dir=722, bushes=723, bombs=724, bombpower=725, type=726.
- signs: x=780, y=781.

The arrow records contradict the old documentation-order assumption. The first dx record binds to the horizontal displacement getter. The following record is also spelled dx, although its evaluator reads the other displacement component. The first-success parser shadows that second record. No dy member spelling exists in this exact family's compiled records. This is an exact-build compatibility defect; it is not a recommendation to correct the original parser silently. A runtime negative control using dy is separate from proving what fallback parsing does after no member matches.

## Evaluation and bounds

For each requested family, evaluation recursively computes the index, converts it through the client's biased-floor helper, and checks it against the corresponding list in the local player's current level. Negative indices, absent current level, and indices at or above list length return the evaluator's initialized numeric zero. These are list positions, not persistent object identifiers. Collection mutation can change what a later evaluation at the same index reads. This pass does not establish whether a whole expression or event snapshots lists against intervening updates.

For ordinary finite values within integer range, index conversion is floor(value + 0.0001). Overflow, nonfinite values, and malformed syntax remain outside that bounded rule.

## Getter effects

- compus x and y read double coordinates. Type, direction, head direction, power, and mode read integer state directly. Their field names are supported by the parser binding; construction and update rules for those state values are separate.
- bombs x and y read double coordinates; power reads integer state. Time reads an integer timer converted to floating point and divided by 20. This scale does not measure scheduler frequency.
- arrows x and y read double coordinates. Dir is computed from the displacement vector: horizontal wins ties, nonnegative horizontal yields right, negative horizontal left; otherwise nonnegative vertical yields down and negative vertical up. A zero vector therefore reports right. The first dx getter reads horizontal displacement; the shadowed second dx getter reads vertical displacement. Type and from read integer state directly; their enum meanings and producer provenance remain separate.
- items x and y read double coordinates. Type obtains a decoded item identity, scans a 25-entry identity table, and returns the matching index or minus one. If duplicate identities existed, the loop would retain the last matching index. The identity helper also checks redundant stored values and can take an integrity-failure path; this is not a purely inert memory read. Time reads an integer timer divided by 20.
- explos x and y read double coordinates; power reads integer state; time reads an integer timer divided by 20. Dir converts stored state through a shared mapping table rather than returning the raw stored value. The complete direction-table contents and invalid stored-index behavior are not newly validated here.
- horses x and y read double coordinates; dir and bombpower read integer state. Bushes and bombs use specialized decoded-value getters rather than direct exposed counters. The inspected bushes getter checks redundant stored values and can take an integrity-failure path. Complete bombs getter semantics remain a helper gap. Type maps a stored boolean to zero or one; assigning semantic horse varieties to those values requires separate producer evidence.
- signs x and y read integer positions and convert them to the evaluator's floating numeric result. This differs from the double-coordinate storage used by most moving objects.

## Coverage and limits

The companion MEMBER-BINDINGS.json lists all 36 compiled records. Full spelling-to-ID binding and first-match behavior are supported; all seven family selection/bounds paths and their getter branches have been reviewed. Selected parser and bounds instructions were freshly decoded, while detailed getter effects also rely on recovered original-matching evaluator text and named helper traces. This is not a claim that every downstream helper has been fully validated from instructions.

Assignment/write dispatch is not traced in this record: successful getter binding does not prove that a member is assignable, or establish setter clamps, notifications, packets, or list ownership. Other open points are fallback semantics for unknown suffixes, exact scanner case/quoting behavior, all object enum meanings, the explosion direction map, the horse bombs decoder, integrity-failure consequences, and cross-version changes. Appendix E#204's former documentation-order assumption can be replaced by these exact bindings while those broader questions remain explicit.

## Original-client corroboration

[2.05][lab] GS1-MEMBER-RUNTIME-205R2-20261109-02 adds two owned offline scenes. The level contains signs at numeric coordinates(14,24) and(39,37). The original client displays those four values through signs[0].x/y and signs[1].x/y and reports signscount2. Negative index minus one and index2 return0. Index0.9998 selects the first sign, while0.99995 selects the second. These controls corroborate zero-based bounded lookup and the biased-floor conversion; a host-language truncating cast would differ near this boundary.

[lab] In the first scene, an up arrow followed by a right arrow produces arrowscount2, with up dir0/dx0 and right dir3/dx1. In the second scene one up arrow is observed after a requested sleep0.2: count1,dir0,dx0 and the unassigned arrows[0].dy expression0, while its numeric y has decreased by4 from the saved value. That distinguishes the zero result from absence of vertical movement. The missing builtin dy binding and shadowing proof come from the compiled table/parser, not merely from observing zero. Do not generalize every unknown member to a permanently zero value or call this a syntax rejection.

[lab] A bomb requested with power1 at(20,35) is read back as count1,x20,y35,power1,time3. This agrees with the inspected timer getter's division by20. The test does not measure a scheduler frequency, specify all spawn/update semantics or validate every object family dynamically.

[lab] Both runs use the exact unchanged original Windows2.05r2 executable under Wine with a private virtual display and isolated user/PID/network namespaces. No server is used. Original target files are completed with explicitly labeled2.31 donor assets and owned synthetic levels, not an authentic complete original2.05 distribution. Both supervisors exit0 and cleanup completes. Twelve displayed control outputs are retained with their inputs and qualifications in runtime-observations.json; they are visual observations, not an independently instrumented AST trace. The COUNT prefix approaches the minimap, but its numeric result2 is unobscured.

Appendix E#204's name-to-ID question is answered for these seven families in this exact build. Keep assignment semantics, complete unknown-member fallback behavior, scanner case/quoting, all enum meanings, explosion direction mapping, specialized integrity-check consequences and other builds separate and open. In particular, do not silently add dy or reorder the arrow bindings to match later documentation.

Evidence retrieval: [docs/evidence-index.tsv](../docs/evidence-index.tsv) indexes the static and runtime records. Digests and observations are researcher supplied; the editor matched five sanitized handoff digests, without inspecting the original binary or private evidence.
