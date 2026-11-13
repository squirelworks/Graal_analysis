# v3 — properties

Date: 2026-11-08 · Tags: **[bin]**

## Wire codec · **high**

Player fields are a numeric id switch (about 0–76, with gaps). On the wire each small value is a byte `n + 0x20`. Strings are length-prefixed the same way (length byte, then text; id 0 caps around 200 characters). Multi-byte values use several 7-bit GCHAR chunks.

| id | Meaning (from the codec) |
|---|---|
| 0 | length-prefixed string (nick / account-style) |
| 1–7 | small numeric / flag fields |
| 8 | sword image (`sword1.` … `sword4.`) |
| 9 | shield image (`shield1.` … `shield3.`) |
| 10+ | further body fields (no friendly names in the image) |

No `account,alpha,ani,…` comma registry.

## Script-facing names · **high**

The GS1 surface includes `setplayerprop` / `setcharprop` and reads such as `playerhp`, `playerhearts`, `playerrupees`, `playerbombs`, `playerdir` (as `.dir` on lists), sword/shield/glove/bomb/shoot power, `playerid`, `playermp`, `playerap`, gender and attach flags. NPC and baddy objects exist (`TServerNPC`, `TBaddy`) with list accessors (`getnpc`, `npcs`, `.timeout`, `.save`). Those names are the script API, not a second wire id space.

## showimg · **high**

Builtins `showimg` / `showimg2` and type `TShowImg` (`graal/showimgs.cpp`).

## Diff vs v4

Same GCHAR property idea and the same sword/shield normalization. v4’s other-player path also names head and chat; v3’s codec shows sword and shield explicitly and leaves most other ids unnamed.
