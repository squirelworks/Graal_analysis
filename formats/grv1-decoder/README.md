# grv1.py: GR-V1 / Z3-V1 level decoder

Decodes binary `.graal` (`GR-V1.00`–`GR-V1.03`) and `.zelda` (`Z3-V1.03`, `Z3-V1.04`) levels. Python 3, no dependencies. Original code written from `formats/level-binary.md` and `client-internals/level-editor-205.md`.

```
python3 grv1.py level.graal            # summary: links, baddies, NPCs, chests, signs
python3 grv1.py level.graal --board    # plus the 64x64 tile grid
python3 grv1.py level.graal --json     # JSON (add --board for tiles)
```

Behaviour follows the 2.05 client loader:

- Code width is 13 bits for `GR-V1.02`/`GR-V1.03` and 12 bits otherwise.
- NPCs are read from `GR-V1.00` on, chests from `GR-V1.01` on. `.zelda` files have neither.
- The baddy section ends at the first record shorter than 3 bytes or whose x byte is ≥ 0x80. An x byte of 0 is a valid baddy (real levels have them).
- NPC scripts have `0xA7` turned into newlines. Sign text goes through the sign alphabet, and `#K(13)` (CR) is dropped.

Checked against the 13 tutorial levels embedded in the 2.05 client and the 9 in 2.22. All parse with the expected link grid, chest items, and sign text (see `client-internals/offline-tutorial-205.md`).

To get the tutorial levels, extract the `TUTORIAL*` RCDATA resources from your own copy of the client (any PE resource tool works). The levels are not committed here.
