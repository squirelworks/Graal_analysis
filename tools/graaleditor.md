# GraalEditor

Version 2.3.1.1, Linux Cyberjoueur. From 2.3 the editor and the online client are separate executables.

## Packing

The copy shipped in the client tree is a Thinstall package (pre-VMware ThinApp). Magic `0x82D0B188`, LoaderFlags reused as an offset. The Delphi image is recovered by running the stub decompressor and the `0xD7` block codec. PE version resource (present even in the stub): CompanyName `Linux Cyberjoueur`, FileVersion `2.3.1.1`, InternalName `Graal editor`, ProductName `GraalEditor`. Linker 2.25.

See also `tools/level-editor/` for the built-in editor of each client (2.22 as the reference). The text writer's `BOARD` encoding is settled in `tools/graaleditor-board-format-2026-11-16.md` (base64 runs, same packing as GLEVNW01).

## Document model

Main form `TAdventure`, document `TAdventureLevel`, unit `UAdventureEditor`.

Sections the editor reads and writes (field order follows the dialogs, not the client loader):

- `BOARD 0` — GLEVNW01-style rows `BOARD 0 <y> 64 0 <128 base64 characters>`; all-zero rows omitted. **[bin]** (`tools/graaleditor-board-format-2026-11-16.md`)
- `LINK`, `SIGN`, `CHEST`, `NPC`, `BADDY`, `LEVELNAMES`.
- Heights kept as a `TLevelHeights` overlay, not a second BOARD.

An earlier note that claimed decimal tile indices for `BOARD 0` is wrong for this writer. The client loader already expects the base64 form.

## Collision

The editor does not store type bytes. Collision is decided later by the 4096-byte type table (wall ≥ 20, water == 11).
