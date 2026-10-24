# Classic Graal level editor: notes by version

Date: 2026-10-25. Derived facts only: class and form inventories, string tables, file-format behaviour, and the behaviour of the editor code paths. No code, addresses or symbol names.

**Reading order**

1. `222-reference.md`: the primary reference. The editor built into the 2.22 client, described feature by feature.
2. `version-deltas.md`: every other build as a delta from 2.22 (1st Graal through 2.31, the New World betas, and the standalone GraalEditor).
3. `formats-crossref.md`: how the editor's loaders and writers relate to `formats/level-binary.md`, the GR-V1 notes, and the 2026-10-25 batch f findings.
4. `seihai-tracking.md`: the 2.22 feature list in implementation order, then per-version deltas, written as a checklist for a future version-selectable Seihai level editor. It is a tracking note only; nothing here implies an implementation.

## Where the material was

- The built-in editor is the `TAdventure` main form in a second, editor mode of the client. It is present in the 2.22 client and in every earlier client the notes cover; the 2.31 client has lost the editor forms.
- Primary source: the 2.22 client's built-in editor, read from a decompile plus a second decompiler pass over handlers the first export had left out.
- Version differences: the 2.17.1, 2.31 and 2.05 rev 2 clients (decompiles), the 1.39 and 2.00–2.04 clients (decompiles and string/class inventories), 1st Graal and every build in the drive-clients inventory (string and class inventories only), and the two New World beta clients.
- Shipped documents in the 2.22 install tree, which are not decompiles and are the best evidence for *when* a feature appeared: the `newfeatures` change logs (1.41, 2.12, 2.17, 2.21, 2.22, 2.31), the stamp sets, the tile-definition files, the editor cursor GANI, and the editor-NPC example scripts.
- The standalone editor: `GraalEditor.exe` 2.3.1.1 is a Thinstall package (see `tools/graaleditor.md`). It was only checked for packing. It was **not** unpacked in this pass. Earlier notes already describe an unpacked image, and those are used as they stand. `Greaditor.exe` (2001, New World beta folders) is UPX-packed and looks like a separate editor; not unpacked either.

## Tags

- **[2.22]** read from the 2.22 code or strings this pass.
- **[prev]** carried from an existing note (`client-internals/level-editor-205.md`, `tools/graaleditor-vs-205.md`, `tools/graaleditor.md`) and not re-read in 2.22. The dialog or class exists in 2.22; its contents are assumed unchanged.
- **[log]** from a shipped change log. The change log says it, the code was not traced.
- **[struct]** structure only. The decompile of that routine is dominated by obfuscated accessors or is missing, so only its shape (what it calls, what it tests) is known.
- **[inf]** inferred.

## Decompiles are lossy

Every statement tagged [2.22] comes from decompiled Delphi code. The decompiles lose type information, merge branches, and show the program's own obfuscated field accessors as arithmetic noise. Where a handler could not be read cleanly it is tagged [struct]. Handlers that the first export did not contain were recovered with a second decompiler pass; the three that could not be recovered are listed in `222-reference.md` under *Open*.

## What is new compared with the existing notes

The 2.05 note and the GraalEditor notes already cover the dialogs, the palette, undo, the GOBJSET01 sets, and the GR-V1.03 writer. This folder adds:

- 2.22 as the reference, with a per-feature table that says which parts were re-read in 2.22.
- A **correction** to `client-internals/client-assets.md`: the tile id → sheet mapping was wrong (see `222-reference.md`).
- A **correction** to the baddy section ending in `client-internals/level-editor-205.md` (x = 0 does not end the section).
- The 9×9 `HEIGHTS` block in the editor's text format, and where the editor writes it.
- The `BOARD` row rules of the text reader, including that the layer field is not read.
- Defaults and edge rules of *Turn selection into a warp field*, including the `playerx` / `playery` arrival defaults and the edge cases that write `0` and `61`.
- Save format chosen by the file extension, and the fact that none of the editors checked (1.39, 2.05, 2.22) writes `Z3-V1`, `GR-V1.00`–`GR-V1.02` or `GR-V1.04` levels.
- `Ctrl+Q` (batch re-save) and `F10` (border toggle) in the key map.
- Flood fill with the right mouse button, multi-level editing on maps, editor control-NPCs, predefined NPCs, and the other change-log dated features.
- A class and format timeline across every build in the inventory, including that the New World betas have no chest or baddy editor.
- Chest position clamp (0–62) in loaders up to 2.04, removed in 2.05.
- One line on the standalone editors' packing.
- A Seihai tracking checklist.

## Not changed

- No existing note was removed. Three were corrected in place (see above and the README entry).
- `formats/level-binary.md` and the batch f findings are cited, not edited.

## Caveats

- The mouse state machine (drag, drop, select, double-click dispatch) is **structure-only**.
- The two obfuscated session-mode flags that gate chest and baddy load/save are **structure-only**; their meaning is only inferred.
- The standalone GraalEditor was not unpacked. Its behaviour comes from earlier notes.
- Class inventories use exact class-name strings in each exe. A class missing from the table may only have been renamed.
- Whether the stock client evaluates arrival offsets such as `playery+10` at warp time was **not traced**. The editor only stores the text.
