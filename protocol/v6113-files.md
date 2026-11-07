# File transfer names in unpacked 6.1.1.3

Date: 2026-11-07. Static read of the unpacked 6.1.1.3 listing. Nothing was run. `game_console.log` is not a file in this repository. Tags: **[bin]**.

## Names in the image

| Name | Where it is used |
| --- | --- |
| `basepackage.gupd` | Compared with a name being opened, and passed into the package helpers that run when packages are collected |
| `.gupd` | The suffix those helpers match |
| `game_console.log` | Joined onto a directory path and opened. The log text is not in the repository, so no request id was read from it |

Three status texts sit beside those names. One says every update package is done, one says only some of them are, and one says an update package was downloaded. Each sentence is cut off in the listing, so only that complete, partial, or downloaded outcome is recovered. **[bin]**

`package_mainfiles.gupd`: not found. No other `.gupd` file name was found. **[bin]**

## Request ids

The script events `onSendUpdatePackage` and `onSendDownloadFile` are present. A numeric packet id for `basepackage.gupd`, or for any other package name, was not recovered. The wire id is the one the script's outgoing table assigns, and that table is not in the image. **[bin]** (`protocol/v6x-clients.md#client--server-ids-601-603` records id 23 for `basepackage.gupd` on earlier Windows captures; this listing does not show that id.)
