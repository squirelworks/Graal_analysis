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
`family` retain associations. `evidence` preserves grade qualifiers and
`confidence` explains the leading grade. `source` and Markdown links in
`source_details` are repository-root-relative public references. No inferred
date or filename is converted into token bytes.

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
