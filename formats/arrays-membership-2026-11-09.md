# Bounded arrays.dat membership inspection

## Evidence boundary

`[file]` Evidence record `GRAAL-ARRAYS-20261109-01` describes a static file inspection. The [evidence index](../workingpapers/sources.tsv) registers its researcher-supplied digest. The editor used sanitized research summaries only; private tables, exported membership files and raw evidence were not inspected or published. Input identities, counts and validation outcomes below are researcher-supplied.

`[file]` Package labels describe collection provenance. They do not authenticate vendor releases, historical asset combinations, or which executable loaded a table. Co-packaged Windows executable metadata may identify a package's client more narrowly, but does not establish those relationships. No client ran during this inspection.

## Structure and exact input

`[file]` List 0 and list 1 denote the first two top-level arrays, indexed from zero. They are structural positions, not runtime category names. The parser follows the [documented recursive format](arrays-and-signatures.md#arraysdat): a big-endian 32-bit header gives kind in the upper 16 bits and count in the lower 16 bits. Kind 0 holds count 32-bit values; kind 1 holds count recursively encoded arrays.

`[file]` The exact input is 11,500 bytes with SHA-256 `b65905ad1e1d1e48d2b7841525c749272426e5160d187f05e8d6b37946296927`. It occurs in packages labelled 2.22 and 2.3 and a separately collected loose copy. It parses to 25 top-level arrays with no remaining bytes.

| Property of this exact input | Result |
| --- | --- |
| List 0 entries | 934, internally unique |
| List 1 entries | 116, internally unique |
| Shared values | 15 |
| Union | 1,035 distinct values, all within 0–4095 |
| Values in list 1 only | 101 |
| Values 2, 3, 18 and 19 | absent from both lists |

`[file]` The collection comprises 53 file occurrences and 26 distinct hashes. Twenty-five distinct inputs parsed through end-of-file and re-encoded byte-for-byte. The remaining input, from a 39ster-labelled package, uses an unsupported representation and is excluded from membership/count claims. It is not counted as a failed official-client table. The four values above are absent from the first two arrays of every successfully parsed input. Other inputs vary in shape, lengths and values; one has internal duplicates. The exact-input counts cannot be generalized to them.

## What the counts settle

`[file]` The inspected lists do not support the earlier assertion that the Bush stamp values appear in them. This corrects file membership only; the relevant consumer, active sheet and a placed bush's runtime collision remain untraced by this pass (E#100).

`[file]` The 1,035-value union differs from the earlier exported mask's 3,195 non-blocking count. The producer, coverage, mapping and selected sheet of that mask remain unlinked to this input. Subtraction does not supply a corrected walkability count (E#101).

`[file]` List-0-only membership and two-list-union membership differ on 101 values here. This establishes different set operations, without determining which operation a runtime path uses (E#608). Earlier consumer observations retain their own evidence and build scope.

- [x] ~~Check structure, counts, overlap and Bush-value membership for the bounded inputs.~~
- [ ] Link an exact input to a particular consuming client and active sheet.
- [ ] Determine runtime collision for the distinguishing values and placed bushes.
- [ ] Reconcile the earlier exported mask's provenance and interpretation.
