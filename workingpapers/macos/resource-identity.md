# macOS extracted-resource identity, revision 1

`[test]` Source `MAC-PPC-RESOURCE-IDENTITY-20261109-R1` records a read-only
comparison of extracted release directories. The publication editor verified
the sanitized record against its supplied digest; underlying per-file manifests
and original client containers were not independently inspected.

| Archive-labelled group | Copies | Regular files per copy | Observed comparison |
| --- | ---: | ---: | --- |
| v3.04 and v3.15r2 | 2 | 718 | Regular-file contents and relative names match |
| v5.12 and four additional v5 copies | 5 | 73 | Regular-file contents and relative names match |

`[test]` Every regular file was hashed, relative names were compared, and symbolic
link targets were recorded without following links. This extends the earlier
main-executable comparison to regular extracted content within these groups.
No original DMG/installer identity, historical release label, timestamp,
permission or empty-directory equivalence is established.

`[test]` No renderer or gameplay observation follows from this comparison. Earlier
dated evidence records and digests remain unchanged. It does not provide the
missing full identity of the earlier published 3.153 study's input, so that
cross-collection linkage remains unverified.

- [x] ~~Compare extracted regular-file resources where main executables match.~~
  Revision 1 supplies the bounded result above.
- [ ] Obtain authenticated historical input identities before resolving the
  earlier 3.153 attribution across collections.

See the [compatibility note](client-compatibility.md) for architecture and label
scope, and [the source index](../sources.tsv) for the sanitized record digest.
Original containers, per-file manifests and private retrieval paths remain private.
