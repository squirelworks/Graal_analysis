# Save-folder layouts by build, and the empty-stream guard

Each build's save routine for a downloaded file was read (static). The table is `save-folders-by-build.tsv`.

## Layouts
- **1.33 to 1.41** (1.33, 1.34, 1.35, 1.36, 1.37, 1.38, 1.39, 1.41 read): one folder for everything that is saved, `levels/webgifs`. The 1.39 routine is entered only for names ending `.gif`, `.png` or `.mng`, so no sound is saved. It deletes an existing file with the same path first, writes the stream, and sets no modification time.
- **1.42 NewMain**: the two builds differ. The earlier one adds `ganis`, `heads`, `swords`, `shields`; the later one adds `sounds` (for `.wav`) and `bomys`. Not read further.
- **2.00 (all four revisions) and 2.01 (both)**: `sounds` for `.wav`. Under `levels`: `bomys` for names starting `bomy` or `b_`, `ganis` for `.gani`, `emoticons` for names starting `emoticon`, `heads`, `bodies`, `swords`, `shields` for names containing those words, else `webgifs`. There is no `hats` folder: a `hat0.png` goes to `webgifs`. There is no `maps` folder.
- **2.02 (all three revisions), 2.03, 2.04, 2.05 rev 1 and 2, both 2.1 test builds**: the same list plus `hats` (name starts `hat`, fourth character a digit, in the builds that test it). Still no `maps`.
- **2.17.1, 2.22, 2.31**: the same, plus `maps` for `.gmap` and for `.txt`, `.gif`, `.png`, `.mng` names containing `map`.
- 2.1 to 2.16 have no binary: when `maps` arrived between the 2.1 test builds and 2.17.1 is unknown.

## The guard
Every build read (1.39, 2.00, 2.05 rev 2, 2.17.1, 2.22, 2.31) begins the save routine with: the stream exists and its size is above zero. Otherwise the routine returns: nothing is written, an existing copy is not deleted, the modification time is not touched and the file is not announced to the loaders. A stream left empty by a failed send is therefore never saved.

## Login request set (compared with traces)
In the 2.22 and 2.31 lab traces (real client against a real server, and Seihai in place of the client, same server) the login requests of the two clients match for the body-part images, icons and the gmap. The remaining difference is the second default-weapon image, which the real clients ask for and Seihai did not: the real order is the bomb image, then the bow image.

Evidence about the default weapons (not used to wire anything): the open server source numbers the default items with bow 7 and bomb 8; the 2.22 client's table of item names follows the same order; the real login asks the bomb image before the bow image, as a walk over default weapons 8 then 7 would. Which wire id names which image was not seen directly.
