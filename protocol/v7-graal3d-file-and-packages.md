# v7 Graal3DEngine: file and package transfer

Date: 2026-11-08

Target: WorldsSetup64-614 `unpacked_Graal3DEngine.dll`. Tags: **[bin]** · **[doc]** 5.x/6.x lab sequences where v7 only has the same filenames/APIs.

No addresses in this file.

---

## 1. Magics and paths **[bin]**

| Magic / path | Role |
|---|---|
| `GRPKG001` | update package container |
| `.gupd` | package manifest suffix |
| `basepackage.gupd` | first/base package name (cleartext) |
| `updatepackages/` | on-disk package tree |
| `SUBPACKAGE` | nested package key inside manifests |
| `webfiles/` | HTTP/web file tree |
| `levels3d/` | 3D level assets (listed with translations/offline/tileobjects/profiles/maps/…) |
| `TUpdatePackage` | native update-package type |
| `TFileDownload_*` | download object API (exported) |

Script API still exposes `requestbasefiles` on the connection object (same family as 6.11). **[doc][bin]**

---

## 2. Package request sequence **[doc][bin]**

v7 keeps the **filename vocabulary** of earlier clients (`basepackage.gupd`, `updatepackages/`, `SUBPACKAGE`). A full ordered list of `package_mainfiles` / `package_sounds` / `package_images` as separate cleartext tokens was **not** recovered in this image — treat those names as **script-/server-driven** `.gupd` contents, not baked C strings.

What a Worlds client still does in practice (aligned with 5.x/6.x labs + v7 symbols):

1. Connector / login path can call **`requestbasefiles`**.
2. First package name seen in binary: **`basepackage.gupd`**.
3. Cache under `updatepackages/` (per-server directories in older labs).
4. Manifest keys include **`SUBPACKAGE`** for nesting.
5. Progress / completion raises script events such as **`onAssetBundleDownloaded`**, **`onClassesDownloaded`**, **`classesdownloaded`** (Unity-side naming mixed with Graal package flow).

PLI side: remapper slots **UpdatePackage**, **DownloadFile**, **UploadStart** / **SaveFile** / **UploadEnd** (see PLI table).  
PLO side: `tclient_setpackagestart` / `setpackageend`, `tclient_download*` family. **[bin]**

---

## 3. Caps, errors, HTTP **[bin]**

| Signal | Meaning |
|---|---|
| Download progress / error log lines | written to the console log on file fetch |
| Oversized web-file skip | download aborted when the web file exceeds an internal size limit |
| Upload size-cap message | upload rejected when the file exceeds a maximum (exact limit not decoded) |
| Upload file-picker hook | native entry that opens a file dialog for upload |
| Asset-bundle download path | Unity AssetBundle name passed to the download path |
| Exports `TFileDownload_CanDownload` / `_Download` / `_Update`, `SendFileToHttpRequest` | concurrent native download object + HTTP send |

**Concurrent request window / exact byte caps / retry counters:** not recovered as clear constants this pass — only the error strings and download object API. Note the gap; do not invent numbers.

---

## 4. `game_console.log` **[bin]**

Cleartext log name **`game_console.log`** is present. Download lines above are the matchable patterns for package/file failures in that log.

---

## 5. vs 6.x **[doc][bin]**

Same `basepackage.gupd` / `updatepackages/` / `GRPKG001` story as 5–6.x. Worlds adds Unity **AssetBundle** download strings beside the classic `.gupd` path. Wire ids for want-file vs verify remain **script-remapped** (do not hard-code classic 23/47 without a live remapper dump).
