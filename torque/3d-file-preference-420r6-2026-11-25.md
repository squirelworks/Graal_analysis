# Local files vs the server's copy in 3D mode (T3D-107, Linux 4.20r6)

Date: 2026-11-25. Loopback lab of the Linux 4.20r6 client against our own 3D lab server, with the 2D link decoded by the lab proxy (runs `pref420-a` to `pref420-d2`; no movement input). Linux 4.20r6 is 3D-equal to Windows 4.20r8 ([T3D-004](3d-engines-5007-512-and-403-411-2026-11-25.md#t3d-004-linux-and-mac-against-their-windows-twins)). Board row: [T3D-107](3d-capability-board.tsv). See also [archives](3d-archives-404r2-512-2026-11-25.md) (T3D-012).

## The check on the wire **[lab]**

When the 3D world names a file, the client checks it over the normal 2D TCP link:

| Client has the file | Packet | Body |
| --- | --- | --- |
| yes | `PLI_UPDATEFILE` (34) | GINT5 modtime (the local file's Unix mtime in seconds), then the name |
| no | `PLI_WANTFILE` (23) | the name |

The server decides. If its copy is newer it sends the file (`PLO_RAWDATA` 100 + `PLO_FILE` 102, with the server's modtime in the header). Otherwise it answers `PLO_FILEUPTODATE` (45). The lab server also answers 45 when it has no copy at all. The client compares nothing itself: it keeps what it has unless a file arrives.

## Lab **[lab]**

Each name had two versions that look different on screen. `pshape.3ds` was the textured cube on the client and the plain red cube on the server. `labtex.png` was a four-colour pattern on the client and solid green on the server. Client copies went in the client folder's `levels3d/` (the data folder) or in the user folder's `levels3d/`.

| Run | Set-up | Request → answer | Drawn | Files after |
| --- | --- | --- | --- | --- |
| pref420-a | client copies (data folder) newer than the server's | 34 with the client mtimes → 45 | client's | unchanged |
| pref420-b | client copies older | 34 → both sent | server's | **downloads saved beside the local copies** in the user folder under `levels3d/images/`, carrying the server's modtime; data-folder copies untouched |
| pref420-b2 | next session, same folders | 34 for the shape with the downloaded copy's mtime → 45 | the downloaded copy | unchanged |
| pref420-d1 | server has neither; `labtex.png` in both folders, data folder newer | 34 with the data folder's mtime → 45 | data-folder copy | unchanged |
| pref420-d2 | as d1, user folder newer | 34 with the user folder's mtime → 45 | user-folder copy | unchanged |
| pref420-c | d2's folders with the newer user-folder copy deleted | 34 with the remaining copy's mtime → 45 | the remaining copy | – |

## Answers

- **Same name, different content:** the client uses its own copy unless the server's copy is newer. A download is saved in the user folder under `levels3d/images/` and does not overwrite a data-folder copy.
- **The modtime decides.** Between two local copies, the newest wins whichever folder it is in. A downloaded copy keeps winning in later sessions while it stays the newest.
- **`FILENAMECACHE.txt`:** the binary names it in the user folder, but the client never wrote one in seven lab sessions, so a stale cache could not be tested. After a file was deleted between sessions, the client simply used the remaining copy.
- **Player override:** a player can override server content by giving a local file a newer mtime than the server's copy, in either folder. A server can force its content only by making its copy newer than any local one. Zip members are never checked at all ([T3D-012](3d-archives-404r2-512-2026-11-25.md)), so a zip in `levels3d` overrides the server whatever the mtimes.
