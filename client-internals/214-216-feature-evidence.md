# 2.14–2.16 feature attribution: release notes, token reports and server gates

Date: 2026-11-21. This is a bounded G190 documentary reconciliation, not a
native client read or lab run. The selected retained 2002 release-note sections
are registered as `RELEASE-NOTES-214216` in the
[evidence index](../docs/evidence-index.tsv). Entries below mean documented
under that release heading, not independently measured introduction dates.

## Keep three kinds of evidence separate

- **[doc]** Release-note headings identify which release is credited with a
  feature or fix. A later explanatory section can describe an older feature.
- **[doc]** The [canonical token catalogue](version-token-catalogue.md#21231-gen-3-to-gen-5)
  associates 2.14–2.16 names with documentary token reports. These rows are
  list-grade associations, not exact-build binary or runtime confirmation.
- **[srv]** A server's version gate describes that implementation's policy.
  It can corroborate a compatibility boundary without proving the original
  client parser, a complete send set or behavior of every revision.

The [inferred profiles](version-profiles/141-217.toml) combine these sources.
Nothing here promotes their inferred packet sets or authorizes a consumer
feature/profile change.

## Selected feature families by documentary heading

The token column joins a release heading to the catalogue's reported family.
It does not identify an exact executable or independently date every revision.
No calendar release date is derived from the token's digits.

| Release heading | Selected documentary feature attribution | Catalogue association and limit |
| --- | --- | --- |
| 2.14 | split server-list tabs; voice activation/muting; expanded music formats and separate volume controls; player-list status icons | `GNW30042`, documentary 2.14 family |
| 2.14 | keyboard script event and lookup helpers; in-game mouse variables/events and click actions; GANI movie mode | same reported family; not a measured callback ABI or event-delivery contract |
| 2.14 | `serverwarp`; downloads above the old 64K boundary and download-progress reporting | same reported family; no packet layout or full outgoing set is established by the feature description |
| 2.14 rev4–rev6 | voice configuration/playback fixes, sound-volume correction, version-variable correction and focus/voice-key fixes | do not assign a separate token to each revision from the family report |
| 2.14 rev7 | pause/map enable/disable commands and related flags; inactive-window keyboard handling | the notes refer to a `graalversion` threshold of 2.147, not a separately authenticated login token |
| 2.15 | `showimg2` with a height coordinate; suppression of keyboard script events while typing chat; volume-relative music adjustment and looping fixes | 2.15.0 is reported as `GNW19052`; this is documentary feature dating |
| 2.15 rev2 | selected crash, map-baddy and personal-message formatting fixes | 2.15.1/2.15.2 are reported with `GNW20052`; the release-note heading alone does not bind a particular executable to either alias |
| 2.16 | effect modes for lights/transparency/subtraction; extension from nine to thirty GANI attributes and GANIs used as attributes | `GNW12102`, documentary 2.16 family; no per-revision parser proof |
| 2.16 | `showani`/`showpoly`/`showtext` families and height variants; `enablefeatures`; additional coordinate/math helpers | same reported family; advertised command semantics remain documentary evidence |
| 2.16 | UDP-reception warning and Enter/Space leaving pause | same reported family; no measured warning cadence or native key path |
| 2.16 rev1–rev7 | follow-up fixes to GANI attributes, UDP checking, rendering, arithmetic and map behavior | do not infer one feature-complete implementation or separate token dates for all revisions |

**[doc]** The 2.14 section explicitly introduces a further group as features
added earlier but previously undocumented, including animation-step variables
and projectile shooting. Its placement is therefore not evidence that `shoot`
or those variables first appeared in 2.14. The earlier introduction remains
unresolved by this document. Likewise a fix heading does not prove the feature
was absent before that revision.

## What the reference server actually gates

**[srv]** The reference fork's `seihai` branch was read at
[`0cf8f83d0ac658299abb4a9c93dab99cca805f37`](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/Player.cpp#L746-L787).
Its file sender selects large-file framing above 32,000 bytes, but clients
classified before 2.14 use a whole-file body and are rejected above 64,000
bytes. At or after the 2.14 gate it permits the chunked path. This agrees
with the documentary large-download boundary; the numbers describe this
server implementation, not a measured original-client capacity.

The gate operates on the server's resolved version id. It neither authenticates
the version of an arbitrary executable presenting a shared token nor dates
voice, keyboard, GANI or script features. No GPL source is copied into a
clean-room consumer; this note is an original-prose summary in the research
repository.

## Remaining G190 work

- [x] Attribute the selected 2.14–2.16 feature families to their documentary
  headings and reported token families, retaining revision ambiguity.
- [x] Compare the documentary large-download boundary with a pinned current
  reference-server version gate.
- [ ] Reconcile the earlier 2.1–2.13 feature families and other unlisted
  release-note details; this is not the whole G190 catalogue.
- [ ] Independently establish exact client implementations, feature-introduction
  boundaries and revision/token bindings before promoting inferred profiles.

The [manual's outgoing-id sets](../manual/02-protocol/04-pli.md) are a separate
claim: documentary feature attribution does not settle inferred packet sets.
