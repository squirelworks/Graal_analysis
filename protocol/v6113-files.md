# File transfer names in unpacked 6.1.1.3

Date: 2026-11-07. Static read of the unpacked 6.1.1.3 listing. Nothing was run. `game_console.log` is not a file in this repository. Tags: **[bin]**.

## Names in the image

| Name | Where it is used |
| --- | --- |
| `basepackage.gupd` | Compared with a name being opened, and passed into the package helpers that run when packages are collected |
| `.gupd` | The suffix those helpers match |
| `all update packages (.gupd files) ha` | The start of a status string. The rest of the sentence is truncated in the listing |
| `some update packages (.gupd files) h` | The start of a second status string |
| `downloaded an update package (.gupd)` | The start of a third status string |
| `game_console.log` | Joined onto a directory path and opened. The log text is not in the repository, so no request id was read from it |

`package_mainfiles.gupd`: not found. No other `.gupd` file name was found. **[bin]**

## Request ids

The script events `onSendUpdatePackage` and `onSendDownloadFile` are present. A numeric packet id for `basepackage.gupd`, or for any other package name, was not recovered. The wire id is the one the script's outgoing table assigns, and that table is not in the image. **[bin]** (`protocol/v6x-clients.md#client--server-ids-601-603` records id 23 for `basepackage.gupd` on earlier Windows captures; this listing does not show that id.)
