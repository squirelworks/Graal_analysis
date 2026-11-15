# Version-token map generation

The sole maintained data source is
[the canonical catalogue](../../client-internals/version-token-catalogue.md).
Its tables explicitly carry exact identifier, build/alias, per-association
evidence, public source, platform and socket/service role. Reproduction columns
are historical context and are not exported as current support assertions.

From the repository root:

```
python tools/token-map/generate.py
python tools/token-map/generate.py --check
python -m unittest discover -s tools/token-map -q
```

The generator writes [the human map](../../VERSION-TOKENS.md) and
[the TSV](../../version-profiles/version-token-map.tsv). Never edit those outputs.
`--check` fails for stale outputs or duplicate/malformed canonical associations.
No binaries, private intake, external packages or network are used to generate.

TSV columns: `token` is the exact ASCII identifier (empty for unresolved/no-token
rows); `state` distinguishes those cases. `build`, `platform`, `role` and
`family` retain associations. `evidence` is the complete supporting signature
in W, B, L, S, U, C order; `B+` is one qualified B and `-` is documented
no-token. `confidence` explains every included category. `source` and Markdown links in
`source_details` are repository-root-relative public references. No inferred
date or filename is converted into token bytes.

Canonical Source cells contain named records, for example
`[W@capture] citation<br>[B@static] citation`. The Grade cell must exactly match
their aggregated signature. `[B@mirror~static]` records a dependent citation;
it cannot create a new category or depend on a missing/cyclic/conflicting
source. `[L@legacy!conflict]` retains a disagreement without counting it as
support. IDs are association-local. Multiple sources are not a confidence
score, and the generator never guesses categories from citation prose.

The appended TSV `source_records` column contains JSON objects with `id`,
`category`, `citation`, `depends_on` and `status`. Existing token/build/role
columns retain their meaning; consumers that require an exact column list
must accommodate this added column. U may coexist with positive categories
only when its citation explicitly names `scope:`; `-` cannot mix with them.
Neither a missing capture nor a failed scanner establishes token absence.

The [pinned beta4 comparison](beta4-comparison.md) distinguishes exact values,
raw prefix discrepancies and ambiguous associations. To compare a supplied
copy: `python tools/token-map/compare_beta4.py <versions-text-file>`.
Suggestions do not silently normalize source tokens, and the research TSV is
not a drop-in server allow-list.

The tests preserve consequential shared-token/grade boundaries, all currently
audited mobile associations and role distinctions, and validate public source
links. Adding evidence may require updating the dated coverage assertions; do
not relax them merely to make a lost association pass.

The 2026-11-15 audit compared the fresh core generated token export (83 rows):
every exported value is represented here. The map also includes server-only,
RC/NC and connector identifiers that its schema omits. That is value coverage,
not proof that the core implements every association or behavior. The core
export is a consumer snapshot, not another editable research catalogue.

A bounded token-pattern scan of this repository's Markdown/TSV/TOML sources was
also reconciled. It is an omission check, not token discovery: level magics,
negative search terms, date guesses and stored lowercase intermediates cannot
be promoted to login identities. The 45-client/16-server intake is a separate
research scope; no complete teardown or runtime coverage is implied.
