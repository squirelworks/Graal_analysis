# Receive-dispatch revision boundaries in Windows 2.02 and 2.05

## Scope and provenance

`[bin]` The six inputs below are Windows PE32 GUI executables for 32-bit x86 (IA-32), as verified by the researcher. Exact input identities and observations are researcher-supplied. The editor reviewed the sanitized prose handoff only; executables, raw routing records and private capsule contents were not independently inspected.

Evidence ID `GRAAL-E7-STATIC-ROUTING-20261109-5c65913ec464` resolves through [the evidence index](../workingpapers/sources.tsv). Its researcher-supplied capsule digest binds the input identities, platform and static routing observations. Private code and locations remain outside the repository.

## Distinct receive routes

`[bin]` A distinct branch for server-to-client logical message 47 exists in each checked 2.02 revision, including revision 0. Message 168 likewise has a distinct branch in all three checked 2.05 revisions. Each questioned entry selects a destination different from that dispatcher's default route.

| Exact input | Questioned logical message | Logical IDs with distinct branches | Researcher-supplied executable SHA-256 |
| --- | --- | --- | --- |
| 2.02 rev 0 | 47 | 56 | 86809c03eda63071c7538eb5e924ea972916329c12e77434da68d5ea8a97ba0f |
| 2.02 rev 1 | 47 | 56 | b6894c917c5769fbadea1b7d2f07e0290c315108c45c69983949fb99838a1109 |
| 2.02 rev 2 | 47 | 56 | 83d1aed3cf57f4fa6812917837691fce246b157f9f1960396e2a513061ce5aae |
| 2.05 rev 0 | 168 | 59 | 04d11effcbc7cd5a9cb14a9fbdc1fc8ee7fcd5cdb89d718a9d5fefa0ad931680 |
| 2.05 rev 1 | 168 | 59 | abf081f73b049de2c849d3202bb881eff773c0d287102f9019feeb6128b6651c |
| 2.05 rev 2 | 168 | 59 | b0e39a04ca0891d0f02282a113a1cd80ddf7a1880a786c5831f26a452e8cbb08 |

`[bin]` This corroborates the existing [per-build receive table](../version-profiles/plo-handled-ids-by-build.tsv) and corrects the narrower revision labels formerly used in [the timeline](cross-version-timeline.md#server--client-packets). A revision-0 dispatch inventory must include the questioned message for its checked family; postponing it until 2.02 rev 2 or 2.05 rev 1 is unsupported by these inputs.

## Validation and limits

`[bin]` The researcher identified the receive dispatcher through client class metadata, inspected the logical-message range check, index lookup and destination table, and compared each questioned entry with the default route. All six comparisons found a distinct destination. No client or server was executed.

`[bin]` Branch presence does not establish runtime reachability, successful packet handling, payload layouts or complete handler effects. Those need separate evidence. These observations settle the revision discrepancy for the six identified inputs, without establishing the first occurrence across every historical branch.

- [x] ~~Check receive branches for message 47 in 2.02 revisions 0–2 and message 168 in 2.05 revisions 0–2.~~
- [ ] Establish runtime handling and payload semantics separately.
