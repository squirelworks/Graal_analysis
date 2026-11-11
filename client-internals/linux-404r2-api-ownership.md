# Correct Linux 4.04r2 script API declaration ownership

Subject: the owner-labelled Linux 4.04r2 x86 ELF, researcher-supplied
executable SHA-256 `50f2057117cfafd5a1151d6e6fdd1413095fa71445ff274bf923ce7dc04198aa`. This identity does not establish equivalence with
a Windows component or another release bearing a similar label.

The publication editor reviewed the sanitized 2026-11-09 research handoff and
recorded its digest. Underlying evidence digests and observations are supplied by
the researcher; raw code, captures and client assets were not opened to fill gaps.
Source IDs resolve through [the evidence index](../docs/evidence-index.tsv).

## Declaration ownership correction

`[test]` The prior structured catalog parser failed to recognize an unindented
root script-object heading. It consequently assigned that object's 38 declarations
to the global list. Correct grouping gives 176 published types and 332 globals
for this exact input, without changing the total declaration count. Source:
`L404-API-CORRECTION`.

`[test]` Raw client CLI output and the earlier bundle are preserved unchanged.
This is a correction of derived metadata, not changed client behavior. Other
catalog versions have their own correction records; these counts do not apply
automatically to them.

## What membership does not establish

Published scripting declarations identify a script-facing surface. They are not
proof of execution, native C++ layout, binding effects, conversion rules or inherited
member behavior. No declaration or native type dump is reproduced here.

The [Linux teardown summary](../version-profiles/linux-teardown.md) remains the
collection-level index. Its complete-catalog coverage is distinct from correct
semantic grouping and from tested implementation behavior.

- [x] ~~Restore root-object declarations to their owning catalog group.~~ The corrected counts above retain the total.
- [ ] Validate binding effects, conversions and inherited members separately.
- [ ] Review each other build's correction record before using its counts.
