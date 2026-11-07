# Decomp findings 2026-10-25 (m): the whole walking rule

Derived facts from reading the walking routine of the 2.05, 2.17.1, 2.22 and
2.31 clients. It is the same routine in all four: the same probe table, nudge
table, branches and constants. No addresses, no function names, no decompiler
output, no code. Numbers are tile units.

- `01-walking-rule.md` — step order, the six probe points and how a point is
  turned into a tile, the corner nudge, the snap flush to a wall after a
  refused step, the 0.0625 line snap, what a point can be blocked by. Completes
  `../decomp-findings-2026-10-25-l/01-walking-body-box.md`, which had the probe
  table and the nudge conditions but not the snaps or the tile rounding.
- `open-questions.tsv` — what was not read.

Why this matters: a port that implements only "refuse the step if the first
four points are blocked" stops half a tile short of any wall on its right or
below (the right and bottom probes sit on the tile line one tile beyond the
body) and sticks on corners. Seihai had exactly that; see its
`documentation/walking-collision.md`.

Checked against: Seihai's tests of the rule (stopping positions from both
half-tile alignments, the slide round a wall's end, the line snap). No lab run
of the real client yet.
