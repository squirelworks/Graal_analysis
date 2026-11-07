# TextConvert

Date: 2026-11-01

Delphi window, about 300 KB, no socket import. The readme is three lines: on start it converts every level in the current folder and in subfolders into New World levels, including links. **[doc][bin]**

The image imports `FindFirstFileA` / `FindNextFileA`, so the walk is a directory walk, which matches the readme. It contains the level signatures `GR-V1.00`, `GR-V1.01`, `GR-V1.02`, `GR-V1.03` and `GLEVNW01`, and the section words `BOARD`, `LINK`, `SIGN` and `NPC`. Failure strings include `Wrong link data!`, `Wrong chest data!`, `Decompression error!` and `File does not exist`. **[bin]**

A few strings (`Server error`, `Do you really want to quit Graal?`, `start1.graal`) come from the shared editor unit compiled into the tool. The import table has no socket library, so those strings are not a connection. **[bin]**

It does not log in, does not ask a listserver for anything, and does not send a level anywhere. Output stays on disk as the converted levels. **[bin][doc]**

`../level-convert/` is a later converter for the whole level chain (Z3-V1, GR-V1, GLEVNW01, a gmap, and a future package). TextConvert itself, as read above, takes GR-V1 levels from a folder and writes GLEVNW01. **[bin][doc]**
