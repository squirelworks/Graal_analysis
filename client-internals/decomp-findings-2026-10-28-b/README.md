# Decomp findings 2026-10-28 (b): tile types in 2.05

Derived facts from reading the 2.05 rev 2 client: how a tile's type is
decided, and the script functions `tiletype`, `onwall` and `onwater`. No
addresses, no function names, no decompiler output, no code.

- `01-tile-type-tests.md`: there is no type table for the default tileset.
  Each type test asks one `arrays.dat` list. Also covered: the fixed
  position rule for tilesets of the new kind, `tiletype()` returning -1 on
  the default tileset, and lava counting as water.
- `tile-type-lists.tsv`: which array or rule answers each type number.

Checked against: Seihai PR 108 (tests listed there). Static read only.
Nothing was run against a server.
