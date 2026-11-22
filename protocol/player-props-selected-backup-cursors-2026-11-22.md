# Own/shared cursor census for one selected backup

Date: 2026-11-22. Evidence `W500-PLAYER-CURSOR-CENSUS-20261122`. Static reads of one archive-labelled 5.00r7 backup input; the label does not authenticate its distribution or runtime identity. This is not a genuine 5.12 table. No target code or new stream experiment was executed. **[bin]**

The [numeric table](player-props-selected-backup-cursors-2026-11-22.tsv) covers every logical ID from 0 through 82 and the two outside-range groups possible after subtracting 32 from an unsigned ID byte. Both dispatch translations and their required jump slots were read as data. The own reader has 76 explicit IDs and seven defaults; the shared reader has 69 explicit IDs and fourteen defaults. Extent flow was checked across all 38 own target groups, including its default, and all forty nondefault shared groups plus its default. This is a complete nominal cursor census for these two selected functions, not a complete semantic property specification or cross-version result. **[bin]**

## Reading the table

N is the current available length, including the property ID. The letters a and b denote the indexing helper's unsigned results at the first and second value positions. When present, these are the corresponding stream bytes. Missing-position fallback is not established as a constant zero, so a formula using b does not prove that b was present. W is a nominal value extent, excluding the ID. **[bin]**

The table describes dispatch reached with N at least two. A local or delegated case that reaches common advancement requests removal of W plus one. The removal helper caps a positive request at the available tail; that does not prove all declared bytes existed, that every callback returns normally, or that the whole parser is safe for malformed input. A default shared entry instead exits without removing the current record. **[bin]**

The own-route column classifies local handling, a bounded prefix copied into shared application, or the default/common path. It is not a guarantee of a setter or observable effect. Application details and downstream callbacks are not completely reconstructed by the extent-flow audit. **[bin][inf]**

## Entry and default behavior

- With no bytes, both readers stop. With a lone final ID, the own reader does not enter its record loop. **[bin]**
- With one byte, the shared reader normally skips dispatch: a nonnegative decoded ID requests removal of two, clamped to the one available byte; a negative decoded ID exits. Logical 51 is the exception: it executes its ID-only branch, reads no value byte and still requests removal of two. This short-input path precedes the table, including entries that would be defaults with N at least two. **[bin]**
- Own defaults retain W equal to one and continue through common processing and advancement. They are not universally no-op records: common cache work remains separate. Shared defaults end this reader invocation without current-record removal; previously selected post-loop effects may still occur. Neither behavior establishes a disconnect or an error response. **[bin]**

## Lengths, guards and delegated copies

Length-prefixed families clamp the decoded length at zero, then add one for the length byte. The compact/extended cases, conditional long case and guard-dependent fixed cases are recorded separately in the table rather than assigned a single unconditional width. **[bin]**

In particular, shared 24, 31 and 36 use three value bytes only when N is at least four; shared 30 uses five only when N is at least six; shared 42 uses four only when N is at least five. Their short paths retain W equal to one. Shared 76 retains W equal to three even when its four-byte presence guard prevents application. Shared 13 similarly sets W equal to five before its full-record update guard. Equality or value-range suppression must not be mistaken for cursor suppression. **[bin]**

Own delegation passes a bounded copy of its selected W-plus-one prefix to shared application. After that call, the original own-reader stream advances according to its own W, not the shared copy's cursor or return behavior. The copy can be shorter than the declared prefix. Matching application routes therefore do not justify substituting shared widths for own widths. **[bin]**

The coordinate conversion/storage and selected logical177 dispatcher findings remain separately qualified in [the status note](player-props-5x-status.md). This table adds neither tile/pixel units nor receiver-type guarantees. It also does not resolve the broader color-selector, ordering or power-bias questions. **[bin][inf]**

## Remaining boundaries

- [x] Enumerate dispatch membership and nominal extent flow for these selected own/shared readers.
- [ ] Establish authenticated build coverage, including genuine 5.12, rather than transfer the archive label to another specimen.
- [ ] Complete semantic field and downstream helper behavior; cursor accounting is not a valid-input grammar or rendering result.
- [ ] Establish controlled runtime and truncated-stream behavior without treating nominal requests or bounded copies as safety proofs.

G290 remains partial. The original multi-build width-table checklist and P4–P6 remain open beyond these selected static results. **[inf]**
