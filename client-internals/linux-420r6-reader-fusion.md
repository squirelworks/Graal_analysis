# Bound Linux 4.20r6 container operands and post-load fusion

The original publication reviewed only the sanitized 2026-11-09 Linux cross-version handoff and matched its supplied SHA-256; no raw code, capture text, script body or client asset was inspected for that publication. Its observations and private-carrier digests were researcher-supplied, not independently re-run or authenticated by the editor. The dated follow-up below additionally reads selected retained source, instructions and identity-bound referenced bytes for the same executable. It runs no client, script, conversion library or server. Evidence keys resolve via [the source index](../docs/evidence-index.tsv), not proposed JSON aliases.

Runtime observations use owned isolated Linux guest/process workflows with no server or server commit, no online login/gameplay and ordinary debugger breakpoints. New probes patch neither executable/signature checks nor script input. Bounded termination and owned-group cleanup do not assert that every system process was inspectable; separately identified unreadable kernel workers are outside the owned client/debugger group.

[bin] The new selected 4.20r6 native package is researcher-reported host-verified: 316 unique selected C-export entries and 2,929 manifest files, five repaired retained-dossier deliveries and zero unresolved requested facets. This is selected recovery coverage, not complete source/semantics. At the cited handoff revision, five expanded native jobs were pending; their completion is not asserted here.

## Exact executable inputs

[bin] Source `LNX-INPUT-IDENTITIES-20261109` is a materialized sanitized identity record whose digest the editor matched. Its executable identities were rechecked by the researcher. Release names remain owner-held labels; executable-byte hashes are not installer-container hashes. Later analysis copies are byte-identical to their original executables. For 3.04, original packed and UPX-decompressed analysis bytes are separate identities.

- 4.20r6-x86 (i386, ELF32): original executable SHA-256 `a994afd24f5ebdcf73647ffe8b6752274a6c874058cb0db05c525bab060224d0`; analysis ELF has the same hash.

## Native reader boundaries

[bin] The reviewed r6 reader uses big-endian four-byte framing/directory numbers and NUL-terminated directory names. It removes a leading `public.` declaration marker and forwards a flag. Format recognition does not establish runtime public-call visibility.

[bin] Operand markers 240–242 select string-table entries using one-byte and two-byte unsigned indexes and a four-byte form with an explicit nonnegative-representation check. Markers 243–245 read progressively wider signed integers into numeric payloads. Marker 246 passes text to the selected conversion wrapper traced below; its loaded-library grammar remains unmeasured. Other bytes append numeric-tagged instruction records; marker branches modify the most recent record.

[bin] The recovered r6 corpus does not cover multiple-marker overwrite edges. Native local bounds/default behavior is not equivalent to the stricter whole-input rejection rules used for corpus validation.

## Selected numeric-text wrapper (2026-11-22)

[bin] Evidence: LNX420-NUMERIC-TEXT-20261122 in the [source index](../docs/evidence-index.tsv). The selected marker dispatch reaches text extraction and the conversion wrapper; when a prior instruction record exists, the result is stored as its numeric operand. This is not a whole marker-placement validity rule.

[bin] Empty input returns zero. Exact lowercase `true` and `false` take separate one/zero branches. An exact lowercase `0x` prefix selects unsigned base-16 library conversion of the suffix; the returned unsigned 32-bit value is widened to floating point. Other text uses the loaded C-library floating converter. Both calls pass no end-pointer destination, and the wrapper does not check consumed length or range-error state. Library/environment-dependent decimal, exponent, hexadecimal-floating, nonfinite and locale grammar are not established by naming those callees.

[bin] After either library conversion, the selected floating comparison returns an ordered nonzero value. Zero and unordered results instead enter a spelling-sensitive fallback, assuming the comparison completes normally: exact `0` or `0x0` is preserved as zero; other nonempty fallback text yields numeric minus one. The early empty/keyword branches remain separate. Instructions, rather than a recovered C inequality, establish this unordered-result distinction. Floating exception state and actual parsing of any spelling were not tested; this is neither a general finite-only filter nor full-text validation.

[bin] Text extraction checks its initial cursor against logical length, then scans to a NUL and advances past that terminator independently of numeric parsing. Its selected failed gate substitutes an empty string and a sentinel cursor. The scan does not receive a remaining-length bound here; buffer construction and sentinels remain untraced. This read establishes neither safe truncation, whole-input rejection nor an out-of-bounds defect. Malformed/truncated input, multiple-marker overwrites and source/public-call runtime behavior remain open.

## Post-load transforms

[bin] One native pass rebuilds a jump-index collection. Another recognizes adjacent instruction patterns and rewrites selected records to fused internal tags in the 200–233 range. Collection positions are retained while the scan advances over matched patterns. A current first record tagged 11 takes the unchanged path. These native transforms explain how a serialized corpus with maximum observed tag 189 can feed a wider internal executor.

[bin] This is not source-compiler recovery or proof that fused tags were transmitted on the wire. Complete native bodies and raw corroboration were compared with the exact-roundtrip corpus offline. No client/server ran; cleanup is not applicable. Numeric-text grammar, malformed-input recovery, public/joined calls and source-language semantics remain open in E#207.

- [x] ~~Review r6 operand handling and native jump-index/fusion passes.~~
- [x] ~~Trace the selected marker-246 text wrapper, numeric fallback and independent cursor advance.~~ See the dated follow-up.
- [ ] Test loaded-library/environment grammar, malformed/truncated input, multiple-marker overwrites and source/public-call semantics.

## Evidence provenance

- `LNX420-R6-READER-MARKERS` — researcher-supplied original private-carrier SHA-256 `eeae38810ac8f04fc80b4fa49e8d66ba7b298c3480cdc6ffaa91846e22f7e1a6`.
- `LNX420-R6-JUMP-INDEX-PASS` — researcher-supplied original private-carrier SHA-256 `3ff0446953d5be88d670c6b020bfcfee7821665b3fa32836869d37c39bc38cf9`.
- `LNX420-R6-FUSION-PASS` — researcher-supplied original private-carrier SHA-256 `913db09f4a817efd402c4c83a6f69baf6ec4e81fa433431ebca58e5e24b3be6a`.
- `LNX420-R6-INTERNAL-TRANSFORMS` — researcher-supplied original private-carrier SHA-256 `4a78abade7dcb58ee9096dd3a356243e08d0fdff797c643a562d6be21a32889b`.
- `LNX420-R6-NATIVE-REVIEW` — researcher-supplied original private-carrier SHA-256 `731e164826a858d1593c0146a634b6ef207add67a3cf6628086d970f03d24852`.
- `LNX420-R6-NATIVE-BUNDLE` — researcher-supplied original private-carrier SHA-256 `6c3c5ee9e6af833de92a35f8587f2b05225a73915c5fe770b2c2e0334eac0737`.
- `LNX420-R6-NATIVE-VERIFICATION` — researcher-supplied original private-carrier SHA-256 `cbe17bddafcca4999b35d9813b105133e96cb9dbdf3512b35daa9420765d1f0c`.
- `LNX420-R6-NATIVE-VALIDATION` — researcher-supplied original private-carrier SHA-256 `47c6c4025b054ff9fbbe5449ee155c0b4ab6f3d427d87d12fd81548bfd2d347a`.
- `LNX420-R6-NATIVE-RECOVERY` — researcher-supplied original private-carrier SHA-256 `e97acd04552728f6b1cf9a38f67da78bec800f7793c86476fe98bbe512743804`.

- `LNX-INPUT-IDENTITIES-20261109` — materialized sanitized identity-record SHA-256 `7ce8a1cf7fb492f7a263b3c02c3cadb2c2ce25b9b2bc6135dff7335481504318`; executable hashes remain researcher-supplied.
