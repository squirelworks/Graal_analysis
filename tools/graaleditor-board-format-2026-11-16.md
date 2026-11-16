# GraalEditor 2.3.1.1 BOARD text shape

Date: 2026-11-16. Tracker: [#619](https://github.com/squirelworks/Graal_analysis/issues/619) (c). Tags: **[bin][GE]**.

Settles App. E#600 for the **text writer** in GraalEditor 2.3.1.1: it emits GLEVNW01-style **base64** `BOARD` runs, not 64 decimal indices per row. A file written by Save As was not captured in this pass; the encoding comes from a static read of the live Delphi writer recovered from the Thinstall process image.

## Verdict

| Claim | Result |
| --- | --- |
| A — `BOARD 0` as 64 lines of 64 decimal tile indices | **false** for this binary’s text writer |
| B — same base64 rows as the 2.05 / 2.22 built-in writers | **holds** for the writer |

## Emitted shape

- File starts with `GLEVNW01` and a newline.
- Each painted row is `BOARD 0 <y> 64 0 <128 characters>` plus a newline. `<y>` is the decimal row index. The 128 characters are 64 tiles × two base64 alphabet characters (high 6 bits, then low 6 bits), the same packing as `formats/glevnw01.txt`. **[bin]**
- Rows whose 64 tiles are all zero are **omitted**. A brand-new blank level therefore has the header and no `BOARD` lines until a nonzero tile is placed. **[bin]**

Example of a single nonzero tile (id 1 at column 0 of row 0): the run begins `AB` then sixty-three `AA` pairs (128 characters total). **[bin]**

Other section keywords the writer still knows (`LINK`, `SIGN`/`SIGNEND`, `CHEST`, `BADDY`/`BADDYEND`, `NPC`/`NPCEND`, `HEIGHTS`/`HEIGHTSEND`) match the earlier GraalEditor notes; this pass only re-checked the tile layer encoding. **[bin][GE]**

## Relation to older notes

`tools/graaleditor.md` and `formats/glevnw01.txt` recorded Claim A from an earlier document-model read that was never checked against a saved file. The 2.05 / 2.22 built-in editors already write base64 (`tools/level-editor/222-reference.md`). The standalone editor is the same `TAdventure` lineage with the online client removed (`tools/graaleditor-vs-205.md`); its text writer matches that lineage. **[GE][2.22][bin]**

## Open

- A Save As `.nw` on a working desktop (VM or owner-approved GUI) as a file-level confirmation. Writer static already chooses Claim B. **[lab]**
