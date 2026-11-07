# LevelScriptEditor

Source: `xtjoeytx/LevelScriptEditor` at `2a81976` (2021-02-25), read-only,
C# WinForms (`src/Levels/*.cs`, `src/Forms/*.cs`, `src/State/GlobalState.cs`).
Tags as in `README.md`.

## What it is

Not a level editor. It opens a folder, loads every `*.nw` file, lists each
level's NPCs in a tree, and lets you edit one NPC's script, image and a
description. Its main feature is "replace similar scripts": find every NPC in
the folder whose script text is identical (optionally with the same image),
and replace them all in one go, with a "mark complete" flag and a
"N / M completed" counter **[lse]**. It reads like a tool for a script port
(GS1 to GS2 on a big world), not for building levels.

## The `.nw` reader

| point | reference **[lse]** | real clients / existing notes | verdict |
|---|---|---|---|
| formats | `.nw` with first line `GLEVNW01` only | 2.05 also opens `Z3-V1.03/1.04`, `GR-V1.00–1.03` (`level-editor-205.md`) | narrower |
| `BOARD x y w layer data` | skips runs outside 0..64 or with `x + w > 64`; keeps one board per layer index | 2.22 does not read the layer field: every row goes on the one board (Seihai `level-editor.md`, from the 2.22 notes) | layers are a later-era idea |
| tile code | `index(c1) << 6 + index(c2)` on `A–Z a–z 0–9 + / =` | same, without `=` (`formats/glevnw01.txt`) | matches; an invalid character gives a bad id instead of ending the row |
| `LINK` | level name may contain spaces (everything before the last six tokens) | GServer and the notes say the name has no spaces | lenient, fine |
| `NPC image x y` | image may contain spaces; x and y as doubles | same; `-` for no image | matches |
| `SIGN`, `CHEST` | read | read | matches |
| `BADDY … BADDYEND` | **not read** | written by 2.05 and 2.22 | see the writer |
| anything else (`HEIGHTS` …) | ignored | 2.22 has `HEIGHTS` (Seihai `level-editor.md`) | see the writer |

## The `.nw` writer: lossy

On save the whole file is rebuilt from what was parsed **[lse]**:

* `GLEVNW01`, then 64 `BOARD 0 y 64 layer` rows per layer, then links, signs,
  chests, NPCs, each with `\n` line ends.
* **Baddies, heights and every unknown line are dropped.** Saving one NPC
  change deletes every baddy in that level.
* The order is LINK, SIGN, CHEST, NPC. 2.05 writes LINK, SIGN, CHEST, BADDY,
  NPC (`level-editor-205.md`).
* NPC x and y are written with .NET's default number format, which follows
  the machine's culture, so on a German or French Windows `30.5` is saved as
  `30,5`.
* NPC scripts are trimmed of leading and trailing blank space.

Seihai's level tool already went the other way on purpose: its `save` keeps
the file's own lines and writes byte-identical output when nothing changed
(Seihai `level-editor.md`). Do not take this writer.

## NPC header comments

The tool stores its own metadata as comment lines at the top of a script:
`//#[MARKED]`, `//#[DESC:text]` **[lse]**. A line starting `// NPC made by `
right after them is kept separately and written back. Real clients treat these
as plain `//` comments, so they are harmless in a level, but they are this
tool's invention, not a Graal convention. If Seihai ever shows them, treat them
as comments.

## What is worth taking

The workflow, not the code: an index of identical scripts across a level
folder, with one edit applied to every copy and a completion count. The
`npc-library` already has 3,172 unique scripts; the same grouping would tell a
Seihai level author which scripts repeat across GR-V1 levels and which ones
are one-offs.
