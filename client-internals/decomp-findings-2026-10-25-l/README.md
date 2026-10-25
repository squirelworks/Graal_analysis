# Decomp findings 2026-10-25 (l): walking body box, arrays.dat, cut/lift, a public-server run

Derived facts from reading the 2.05 client (walking, lifting, sword cut, chest
open) and from one login to a public GServer-RS with a 2.22 profile. No
addresses, no function names, no decompiler output, no code. Numbers are
tile units unless stated.

- `01-walking-body-box.md` — the wall test of the walking routine: a box with
  four probe points per facing, keys applied one at a time, corner nudge.
  Corrects `../foot-test.md`'s "official ~2.05 used a different body-block mask":
  that mask is this box.
- `02-arrays-dat.md` — the full layout of `arrays.dat` (25 arrays, nested
  kinds) and what each array is for.
- `03-cut-lift-chest.md` — sword cut, lift by glove power, chest open by tile
  and by record, the A-key order, probe offsets.
- `04-public-server-run.md` — what a public server sent on login (counts and
  layouts), why no chests were drawn, the weapon-script line-break byte, the
  capture link type.
- `open-questions.tsv` — what was not read.

Checked against: Seihai PRs 60 to 64 (tests listed there).
