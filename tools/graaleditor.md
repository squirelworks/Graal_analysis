# GraalEditor

Version 2.3.1.1, Linux Cyberjoueur. From 2.3 the editor and the online client are separate executables.

## Packing

The copy shipped in the client tree is a Thinstall package (pre-VMware ThinApp). Magic `0x82D0B188`, LoaderFlags reused as an offset. The Delphi image is recovered by running the stub decompressor and the `0xD7` block codec. PE version resource (present even in the stub): CompanyName `Linux Cyberjoueur`, FileVersion `2.3.1.1`, InternalName `Graal editor`, ProductName `GraalEditor`. Linker 2.25.

See also `tools/level-editor/` for the built-in editor of each client (2.22 as the reference). The decimal-`BOARD 0` claim in the next section conflicts with the base64 rows that the 2.05 and 2.22 built-in editors write; it has not been re-checked against a file written by GraalEditor itself.

## Document model

Main form `TAdventure`, document `TAdventureLevel`, unit `UAdventureEditor`.

Sections the editor reads and writes (field order follows the dialogs, not the client loader):

- `BOARD 0` — 64 lines of 64 decimal tile indices (not base64 runs).
- `LINK`, `SIGN`, `CHEST`, `NPC`, `BADDY`, `LEVELNAMES`.
- Heights kept as a `TLevelHeights` overlay, not a second BOARD.

A file of raw decimal indices does not pass the client `GLEVNW01` loader until rewritten as base64 runs. The reverse is also true: a client `.nw` is not a `BOARD 0` grid.

## Collision

The editor does not store type bytes. Collision is decided later by the 4096-byte type table (wall ≥ 20, water == 11).
