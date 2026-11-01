# Save rules

## Whether a file is written
A received file is first held in memory as a cached stream. It is written to disk only when the `saveimages` option is on; the option lives in the client's config file and defaults to on.

## Where
1. If the client already has a file under that name, it is replaced where it is. The lookup tries the name as a path from the game folder, then the client's own file-name index (name to path and time).
2. Otherwise by name, case-insensitive:
   - `.wav`: `sounds`.
   - from 2.17.1 on: `.gmap`, and `.txt`, `.gif`, `.png`, `.mng` with `map` in the name: `maps`.
   - everything else under `levels`, in a folder by name: `bomys` (name starts `bomy` or `b_`), `ganis` (`.gani`), `emoticons`, `hats` (`hat` plus a digit as the fourth character), `heads`, `bodies`, `swords`, `shields` (the name contains `head`, `body`, `sword`, `shield`), else `webgifs`.
3. 2.05 rev 2 has no `maps` rule: its downloads all go under `levels`. 2.1 to 2.16 are inferred to match the later builds (no build in that range was read).

Lab: a downloaded gmap on 2.22 was saved as `maps/<name>`; images and animations went to the `levels` folders above.

## Time of the saved file
From 2.1 the file reply carries a GINT5 last-write time; the client sets it on the saved file. Before 2.1 the reply has no time, so the file's time is the time of the download.

## Names
Compared without regard to case. The fold is plain A–Z only, and the index then compares the folded bytes exactly; see [`04-name-index-case-link.md`](04-name-index-case-link.md). Lookups use the same normalisation as the loaders.
