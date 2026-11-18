# Assimilator batch ops on levels and scripts

Date: 2026-11-16. Tracker: [#619](https://github.com/squirelworks/Graal_analysis/issues/619) (a). Tags: **[bin]**.

Extends the salvage summary in `recovered-drive-tools/ghidra-analysis/Assimilator/SUMMARY.md` with the batch contract Seihai’s offline editor still needs: what the classic “GIF to PNG Assimilator” accepts, what it rewrites, and how empty runs fail.

## Product

Delphi GUI branded **Graal GIF to PNG Assimilator**. Offline only. PE32, not Themida-packed in the copy examined here. **[bin]**

## Two checklists

| List | Add actions | File filter |
| --- | --- | --- |
| Scripts | Add Script; Add All Scripts in Folder; Check / Uncheck All | Combined: `.graal`, `.nw`, `.txt`, `.gscript`, `.gani`. Separate “Graal Level File” filter: `.graal`, `.nw`. Separate script filter: `.txt`, `.gscript`. Separate GANI filter: `.gani` |
| MNG Files | Add MNG; Add All MNGs in Folder; Check / Uncheck All | `.mng` |

Levels sit on the **Scripts** list as text files, not on a dedicated board transcoder. **[bin]**

## What a run does

- Walks the **checked** rows and rewrites GIF references inside those texts: counts of `*.gif` and of `setgif` replacements are reported when a file is processed. **[bin]**
- Reports “Total PNG and MNGs placed” and a progress line of the form “Progress *n* of *m* files”. **[bin]**
- Shows “Graal Version: N/A” until a client version is configured; the version field does not gate the rewrite strings above. **[bin]**

This is **not** a GR↔NW / magic-based level re-saver. Format normalize for levels remains the built-in editor’s Ctrl+Q batch re-save (read by magic, write by extension) in `tools/level-editor/222-reference.md`. **[bin][2.22]**

## Empty and failed runs

| Condition | Message |
| --- | --- |
| Nothing in the list | `[ERROR] There are no files in the list.` |
| Nothing left unchecked when the action expects unchecked rows | `[ERROR] There are no unchecked files.` |
| Per-file failure | `[ERROR] [` … `] The file` … |

Successful per-file lines use a `[FILE]` prefix with the same bracketed index style. **[bin]**

## Seihai takeaway

An Assimilator-style batch op on levels is: **text rewrite of GIF / `setgif` references across a checked checklist that may include `.graal` / `.nw`**, with hard errors when the checklist is empty. It does not settle board encoding. **[bin]**

## Open

- Exact PNG path spelling written when a `*.gif` token is replaced (extension-only vs folder policy). **[bin]**
- Whether unchecked rows are skipped or require an explicit “check” before convert (UI has both Check and Uncheck All; the “no unchecked files” error implies at least one action consumes unchecked rows). **[bin]**
