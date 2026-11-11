# GS1 message expansion, exact 2.05r2

Evidence ID GS1-MESSAGE-205R2-20261109-01. Researcher-verified executable SHA-256 b0e39a04ca0891d0f02282a113a1cd80ddf7a1880a786c5831f26a452e8cbb08. This contract comes from original-matching recovered functions and fresh original instruction decoding of the complete expander. It is not a cross-version claim or an assertion that a downstream reviewer independently verified the binary. This portion describes static evidence; the separately identified original-client runs below add bounded runtime observations.

## Processing contract

The message command trims leading and trailing bytes below 33, expands in mode zero with the running NPC context, stores the resulting NPC text, and clears its timer-display state. Expansion finds the first hash that has a following byte. It constructs a replacement, recursively expands the remaining suffix, then joins prefix, replacement, and expanded suffix. Replacement text is not automatically rescanned as part of that join. Explicit recursive argument expansion is described below. Text is handled as byte strings, not Unicode code points.

A final hash is retained. An unrecognized code consumes only its hash: A#?B becomes A?B. Recognized codes default to consuming their hash and code letter even when arguments are absent or invalid. Color and image-parameter selectors consume an additional byte. A valid balanced argument extends consumption through its closing delimiter. Failure to find that delimiter leaves the parenthesis and subsequent bytes as suffix; it does not leave the whole recognized code intact. This is a static control-flow conclusion, not a guarantee against arbitrary malicious expressions or unbounded recursive input.

The delimiter helper counts nested matching parentheses using another scanner. Its quote/escape handling is not fully reviewed here. Therefore comma and parenthesis behavior inside quoted arguments remains a helper-level gap.

## Literal and display codes

- `##` returns one literal hash.
- `#.` `#4` `#A` `#B` `#X` `#Y` `#d` `#h` `#i` `#l` `#r` `#u` `#x` `#y` `#z` retain their two-byte spellings for downstream display handling. This expander does not render their glyphs.
- `#b` inserts a linefeed only when expansion mode is nonzero. The ordinary message command passes zero, so it produces an empty replacement there.
- `#E` inserts one byte from shared runtime state. The producer and user-facing meaning of that byte remain untraced.

## Character selectors

The following codes accept an optional numeric character selector immediately after their spelling: `#1`, `#2`, `#3`, `#5`, `#6`, `#7`, `#8`, `#C0` through `#C5`, `#P1` through `#P5`, `#a`, `#c`, `#g`, `#m`, `#n`. Without parentheses they use the local player. A supplied expression is evaluated and converted using the client's biased-floor integer helper, then resolved: zero is the local player; minus one is the running NPC only when it is a character; positive indices enumerate remote players followed by other character NPCs, excluding the caller. An unresolved selector yields an empty replacement. These are character selectors, not persistent NPC identifiers.

- `#1`, `#2`, `#3`, `#5`, `#8` return the selected character's sword, shield, head, horse, and body image names respectively, or empty when the relevant image object is absent. Normalization strips the directory through the final slash or backslash, then lowercases ASCII A–Z. It does not remove the extension.
- `#6` obtains the selected actor’s carried-NPC image, with basename-style slash/backslash stripping and ASCII lowercase normalization, retaining the extension. An absent association yields empty. The later [independent static association checkpoint](#independent-carried-npc-association-checkpoint) establishes this identity for the exact original 2.05r2 input; it does not validate all selector, pickup or lifetime paths.
- `#7` enters the character-selection family but has no output branch, so its replacement remains empty.
- `#C0` through `#C5` read six corresponding 32-bit actor storage slots and use each stored value as an index into the shared color-name table. The sixth accepted storage index has no proven semantic color identity here. This does not establish six clothing colors or six transmitted color bytes; retain the separately established five-byte wire color property. This branch does not itself validate the stored index against the color-name table size. Invalid selector digits yield empty and still consume the third byte.
- `#P1` through `#P5` fetch the corresponding one-based character image parameter. The helper returns stored text; if that text is empty and a stored numeric fallback is nonnegative, it returns integer text instead. Invalid selector digits yield empty.
- `#c` returns the character's message text directly, without recursively expanding that returned text.
- `#n` returns the decoded actor-name field. `#g` obtains that same name, then returns text between its first opening parenthesis and a subsequent closing parenthesis; missing delimiters yield empty. This supports the guild-tag interpretation mechanically, without asserting authentication or membership.
- `#a` returns a direct character string field. `#m` returns the current animation name from the optional animation object used by the setani/setcharani setter. The precise identity of the direct `#a` field remains unresolved here and should not be guessed from historical documentation.

## Expression and string operations

- `#v(expression)` recursively expands its argument in mode zero, evaluates it in numeric expression mode, and formats the resulting double through the shared numeric formatter. This differs from parsing a bare condition as a named flag. Exact decimal precision, exponent thresholds, and nonfinite formatting remain formatter gaps.
- `#s(name)` trims and recursively expands its argument in mode zero, then looks up the string-variable store. It returns the variable's value, not the literal argument. The helper has two store representations; exact name normalization and case rules remain partial.
- `#T(text)` trims its argument, recursively expands it in mode zero, then trims the expanded result again. Trimming removes bytes below 33 at either end.
- `#e(start,length,text)` evaluates the first two top-level comma-separated parts as numbers, converts each with the biased-floor helper, recursively expands the remaining text, and slices by byte position. Start is zero-based, clamped to the range zero through string length. Negative length means the remainder; an overrun is clipped to the remainder. Missing separators produce empty replacement after consuming a balanced argument. Separator parsing inside quotes is not fully established.

## Keys, weapons, and indexed lists

- `#K(number)` evaluates and converts its argument. Integers from zero through 65535 yield a one-byte string containing the low eight bits. Values outside that range yield empty. In particular this is not a Unicode character constructor. Embedded zero can exist in the expanded managed string; downstream display behavior is a separate question.
- `#k(number)` evaluates and converts its argument, then resolves a configured control binding's display name. The called helper accepts control indices zero through ten; other values produce empty. It uses binding variant zero. Keyboard layout and localization details remain downstream gaps.
- `#w` returns the currently selected weapon's decoded name; `#W` returns that weapon's image name. With an explicit parenthesized numeric index they use that zero-based weapon-list entry instead. Explicit out-of-range indices produce empty; the omitted-index path checks only that the selected index is nonnegative before calling the list accessor. Their argument is recursively expanded in mode zero before numeric evaluation. Weapon image output is obtained directly, without the lowercasing/path stripping used for character equipment above.
- `#f` returns the running NPC's image name, normalized by removing directory prefixes and lowercasing ASCII. `#L` applies the same normalization to a local-player-owned string field; the exact field identity is not newly established here.
- `#p(index)` and `#t(index)` recursively expand and numerically evaluate their arguments, convert to integers, bounds-check against separate shared string lists, then return that zero-based entry or empty. The `#t` list is directly linked to tokenize/tokenize2: those commands clear and fill the exact list read here. The [event-parameter follow-up](gs1-event-parameters-205r2.md#producer-and-consumer-linkage) establishes that dispatch clears and fills the `#p`/`paramscount` list from actor pending text, separately from tokenize; queue overwrite and lifetime limits remain explicit.

## Limits and independent tests

Useful independent controls are literal and unknown hashes, a trailing hash, numeric display of 0.5, a byte slice of ABCD, a stored string variable, character code 65 and an out-of-range character code, missing parentheses, and a deliberately absent character or weapon selector. Renderer output and string-buffer inspection answer different questions, especially for zero bytes and preserved glyph codes. Runtime evidence collected separately must retain its own fixture and asset qualifications.

The public contract deliberately leaves unresolved shared-state byte meaning, the direct character string identity, one image association, one local-player string field, numeric formatting details, scanner quoting, and downstream glyph rendering. It does not substitute documentation names for untraced data flow.

## Selector membership and coverage

Supplement GS1-MESSAGE-CATALOG-205R2-20261109-02 adds evidence to GS1-MESSAGE-205R2-20261109-01 without changing it. Exact executable SHA-256: b0e39a04ca0891d0f02282a113a1cd80ddf7a1880a786c5831f26a452e8cbb08. Input/hash verification is researcher-supplied.

The original outer dispatch recognizes exactly **44 byte selectors** following a hash:

`# . 1 2 3 4 5 6 7 8 A B C E K L P T W X Y a b c d e f g h i k l m n p r s t u v w x y z`

These are bytes following the initial hash: the first entry represents `##`. Case is significant. The two multi-byte families accept color digits C0–C5 and image-parameter digits P1–P5. Replacing C and P with those eleven spellings yields 53 recognized spellings. This is a syntax inventory, not 53 distinct operations: it includes display codes preserved for later rendering and the recognized empty-output code #7.

Fresh decoding of the original byte-index lookup and its target table verifies complete outer membership, including the default route for other bytes. This is stronger and more specific than recognizing code names in recovered text. The previously saved linear instruction listing crosses embedded lookup data; those data bytes must not be interpreted as executed instructions. The separate decoded table in this supplement supplies that missing distinction.

Per-code effects in the preceding contract use original-matching recovered helper bodies, selected fresh instruction checks, actual caller argument setup, and independently traced data producers where stated. This does not mean every helper has been completely revalidated from instructions. In particular, complete outer dispatch coverage leaves partial the identities behind #a, #E and #L (the later #6 association checkpoint narrows that one identity only), quoting rules in argument scanners, exact numeric formatting, and downstream glyph rendering. A complete selector catalog therefore does not close Appendix E#203.

The #t producer is directly linked to the list cleared and populated by tokenize/tokenize2. The #m animation object is directly shared with setani/setcharani. These are data-flow links rather than copied documentation labels. Runtime fixtures conducted by the coordinating researcher are separate records; this supplement performs no target execution and makes no additional visual claims.

## New original-client controls

[2.05][lab] GS1-MESSAGE-RUNTIME-205R2-20261109-04 records30 control outputs across three usable scenes. A fourth scene with character/name overlap is retained privately as diagnostic material and was replaced by a more widely spaced layout. Outputs were reviewed directly from the original client, not inferred from expected values. The companion runtime-observations.json records each input, setup, displayed output and qualification. No missing label is treated as an empty expansion.

[lab] Literal and fallback controls give A##B to A#B, A#?B to A?B, a trailing A# unchanged, and A#vB to AB when the recognized numeric code lacks its argument. Uppercase A#VB becomes AVB: case is significant. A#?#v(2)B becomes A?2B, so unknown-code fallback still permits expansion of the remaining suffix.

[lab] A##v(2) remains A#v(2). A stored string containing literal #v(2) is returned unchanged by #s, and the calling character NPC's prior message containing that text is returned unchanged by #c(-1). These controls corroborate the distinction between explicit recursive argument expansion and automatic rescanning of inserted replacement text. Nested #e(1,2,#s(lab.test)) produces BC when that string variable contains ABCD.

[lab] #v(0.5) displays0.5 and #v(2+3) displays5; these are examples, not a complete numeric-formatting specification. #e(1,2,ABCD) gives BC, negative start clamps to give AB, negative length returns the suffix BCD, an oversized start gives empty, and an oversized length clips to BCD. #K(65) gives A and #K(-1) gives empty. #K(0) renders a box glyph; its exact byte is not established by visual output. A#bB gives AB in the ordinary message command's mode zero, rather than a newline.

[lab] For a character NPC given the name Lab(Tag), #n(-1) displays Lab(Tag) and #g(-1) displays Tag. #7(-1) produces empty in a character context. Initializing tokens from alpha,beta gives alpha for #t(0), beta for #t(1), and empty for #t(2). #p(0) is empty in the tested created-event context; that original control alone does not qualify event-parameter delivery. Separate [producer and local-delivery controls](gs1-event-parameters-205r2.md#new-end-to-end-original-client-controls) now supply that bounded evidence.

[lab] All four runs used the exact unchanged Windows2.05r2 executable under Wine with a private virtual display and isolated user/PID/network namespaces. No server was used. Target files were completed with explicitly labeled2.31 donor assets and owned synthetic levels, rather than an authentic complete2.05 distribution. Every run exited with supervisor status0 and completed cleanup. Screenshots, raw functions and exact harness/configuration identities remain private.

The selector catalog is complete for this outer switch, but Appendix E#203 remains partial for the listed field identities, quoting, formatting and downstream renderer semantics. None of these observations extends the wire color property or proves all recognized spellings execute useful operations. Other builds, remote-player selector ordering in a live session, every helper branch and malformed-expression behavior remain unqualified.

Evidence retrieval: the static, catalog and runtime identifiers above are indexed in [docs/evidence-index.tsv](../docs/evidence-index.tsv). Digests and original-client observations are researcher supplied; the editor verified the four sanitized handoff file digests, not the private evidence or executable.

## Event-parameter follow-up

[bin][lab] GS1-EVENT-PARAMS-205R2-20261109-01 and GS1-PARAM-RUNTIME-205R2-20261109-04 establish the exact-build #p producer and local delivery chain. The actor has one pending text field shared by queued event names; dispatch splits it into the shared parameter list. Accepted distinct events can overwrite it, while rejected duplicates/actions preserve it. callnpc/callweapon queue empty parameter text, with callweapon static-only. See [the focused note](gs1-event-parameters-205r2.md) for split/lifetime controls, donor/visual qualifications and remaining scheduling, nested-context and network limits. This closes only the producer gap, not the remaining field/scanner/formatter/renderer questions.

## Independent carried-NPC association checkpoint

[bin] The 2026-11-09 independent Windows check matches identical original executables from two supplied archive variants to the contract input SHA-256 `b0e39a04ca0891d0f02282a113a1cd80ddf7a1880a786c5831f26a452e8cbb08`. Package labels do not authenticate a release. Selected prior instruction records were matched to original bytes and decoded independently, with focused command/selector and direct-branch checks; all 634 checked prior instructions matched. The publisher reviewed the sanitized receipt and its digest, not a fresh executable scan or client run.

[bin] The association read by `#6` is written by the eligible-NPC pickup branch, whose carryable-flag check corresponds to `canbecarried`/`cannotbecarried`. Throw transfers that association to the thrown-object record and clears it; `takeplayercarry` clears it, and NPC removal clears matching actors’ associations. Ordinary tile/auxiliary carrying paths are distinct. These selected producer/consumer links establish carried-NPC image identity without proving complete pickup/input/collision eligibility, every actor selector, or full object lifetime.

[bin] The getter strips slash/backslash directories and lowercases ASCII while retaining the extension. No association leaves an empty replacement. The common expansion path recursively processes the remaining original suffix and does not rescan inserted image text for message codes. Arbitrary multibyte filename behavior and downstream rendering remain unvalidated.

The received ownership-assignment fragment is not used to claim a receiver contract: its earlier helper label was incorrect, and the enclosing function/full protocol-property case remain unresolved. Do not reuse that label or infer complete receive/error-path validation. No runtime success, renderer, animation-label or cross-build conclusion follows from these static checks. Server/commit: none; no client, VM or imported script was launched for this corroboration/publication.

Evidence `W2052-FIELD6-INDEPENDENT-20261109` and `W2052-FIELD6-SEMANTIC-20261109` resolve to the actual sanitized corroboration receipt, SHA-256 `0a74e6b93a6a7646a151551526172a3aa703383e4b126c9921a22bd15d329e2b`. The publisher matched that document; exact original input matching and native observations are researcher-supplied. Raw instructions, addresses, code, carrier retrieval paths and original assets remain private. Appendix E#203 remains partial for other field identities, scanners, formatting, selectors and rendering.
