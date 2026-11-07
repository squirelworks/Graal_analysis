<!-- manual: kind=reference status=draft -->
# 2.7 File transfer

The request messages are laid out in → §2.4.7 and the replies in → §2.5.7; the raw-data escape is in → §2.1.3. This chapter gives the sequence and the version rules.

> Status: draft.

## 2.7.1 Requests and replies

| Request | Reply when the file is sent | Reply otherwise | Builds | Source |
| --- | --- | --- | --- | --- |
| 23 `PLI_WANTFILE` (name) | 100 `RAWDATA` + 102 `FILE` | 30 `FILESENDFAILED` (name) | 1.21 to 6.x | [srv] (protocol/file-transfer.md#requests-client--server) |
| 34 `PLI_UPDATEFILE` (`i5` cached modtime, name) | 100 + 102 when the modtime differs | below 2.1: 30; 2.1 and later: 45 `FILEUPTODATE` | 1.42 to 6.x | [srv] (protocol/file-transfer.md#requests-client--server) |
| 47 `PLI_VERIFYWANTSEND` (`i5 crc32`, name) | 100 + 102 when the client's copy is stale | unmeasured | 5.00r7, 5.24, 6.x | [srv] (protocol/file-transfer.md#requests-client--server); [cap] (protocol/file-transfer.md#what-5x-asks-for-at-login-cap) |

| Rule | Builds | Source |
| --- | --- | --- |
| Below 2.1 the server adds `.gif` to a requested name with no extension | server | [srv] (protocol/file-transfer.md#requests-client--server) |
| Below 2.1, 30 also means "already up to date"; 2.05 handles 45, but the server does not send it to 2.05 | server; 2.05 | [srv] (protocol/file-transfer.md#replies-server--client) |
| Game clients cannot upload; RC upload uses the file-browser ids 89 to 98 and 65 to 67 (→ §7); disputed for 6.x → App. E#9 | server | [srv] (protocol/file-transfer.md#upload-rc-only) |

## 2.7.2 The `PLO_FILE` body

| Client version (by the server's token table) | Layout behind 100 | Source |
| --- | --- | --- |
| below 2.1 (2.05) | `c 102`, `str filename`, then the file bytes; no modtime and no trailing `\n`; the RAWDATA length is 1 + 1 + name + data | [srv] (protocol/file-transfer.md#plo_file-body-srv) |
| 2.1 to 2.13 | `c 102`, `i5 modtime`, `str filename`, the bytes, then `\n`, in one piece | [srv] (protocol/file-transfer.md#plo_file-body-srv) |
| 2.14 and later | as 2.1, split into 32000-byte chunks; a file over 32000 bytes is wrapped in 68 `LARGEFILESTART`, 84 `LARGEFILESIZE` and 69 `LARGEFILEEND` | [srv] (protocol/file-transfer.md#plo_file-body-srv) |

| Rule | Builds | Source |
| --- | --- | --- |
| A client before 2.14 cannot receive a file over 64000 bytes; the server answers 30 instead | server | [srv] (protocol/file-transfer.md#plo_file-body-srv) |
| A 541,248-byte file reached 5.00r7 as 68, 84, then 102 chunks each with modtime and name, then 69, and was saved byte for byte | 5.00r7 (lab, stock gs2lib) | [cap][bin] (protocol/file-transfer.md#what-5x-asks-for-at-login-cap) |
| On 69 the client compares the name with the stored one and processes the accumulated stream as one file (→ §2.5.7) | 2.17.1 to 2.31 | [bin] (version-profiles/plo-layouts-217-231.tsv) |

## 2.7.3 The layout follows the server's token table

| Rule | Builds | Source |
| --- | --- | --- |
| Every version branch in the server's file code tests the version id, which comes only from the login token looked up in the server library's table; a token that is allowed but not in the table gets version 0, below every real version | server | [srv] (protocol/file-transfer.md#the-layout-follows-the-servers-token-table-not-the-client-2026-10-31) |
| Such a client gets every pre-2.1 path: `PLO_FILE` without modtime or `\n`, 30 for up to date, `.gif` added to names, the pre-2.1 level sequence with no 156, and no large-file messages | server | [srv] (protocol/file-transfer.md#the-layout-follows-the-servers-token-table-not-the-client-2026-10-31) |
| A version's rank is its position in the table; the server compares positions | server library | [src] (protocol/file-transfer.md#gs2libs-version-table-src) |
| The table holds, in order: `G3D22067` (5.00r7), `G3D14097` (5.12), `G3D26090` (5.30r3, 5.31r4, 6.00r2, 6.00r4), `G3D3007A` (6.01x), `G3D2505C` (6.034, 6.035), `G3D0311C` (6.03r7 Windows), `G3D0511C` (6.03r7 Linux); all sit above the 2.14 slot | server library | [src] (protocol/file-transfer.md#gs2libs-version-table-src) |
| `G3D15010` (5.24r3, 5.24r4, 6.00 beta2) and `G3D03048` (6.00 beta1) are not in the stock table | server library | [src] (protocol/file-transfer.md#gs2libs-version-table-src) |
| The client always reads `PLO_FILE` as `i5 modtime` + `str filename` + data; given the old layout it takes the name's length byte and first 4 characters as the modtime, and the 5th character as the length | 5.24 | [srv][inf] (protocol/file-transfer.md#the-524-png-as-file-name-bug) |
| For `sword1.png` that gives the error "Couldn't open …1.png‰PNG… for writing"; with a table that knows `G3D15010` the same server's files were saved normally | 5.24r4 (lab) | [cap] (protocol/file-transfer.md#the-524-png-as-file-name-bug) |
| A server for 5.x and 6.x clients must know every token it allows | server | [src] (protocol/file-transfer.md#gs2libs-version-table-src) |
| A client cannot tell the server which layout to use | all | [inf] (protocol/file-transfer.md#gs2libs-version-table-src) |

## 2.7.4 Requests at login

| Build | Requests seen | Source |
| --- | --- | --- |
| 2.05 | for each file a level references (for example `head25.png`, `sword1.png`, `walk.gani`): 34 when cached, else 23; the server answers 100 + 102 or 30 | [srv][inf][cap] (protocol/file-transfer.md#typical-flow-for-205-srvinf) |
| 2.22 | 34 for the default images (sword, shield, body, bomb), then 23 (→ §2.4.11) | [cap] (version-profiles/2.22-2.31.md#wire-protocol) |
| 5.24r4, 5.30r3, 6.03r7 | `basepackage.gupd` first; with an empty cache as 23, twice | [cap] (protocol/file-transfer.md#what-5x-asks-for-at-login-cap) |
| 5.00r7 | `basepackage.gupd` as 47 when that server's copy is cached and as 23 when not; the cache is kept per server name | [cap] (protocol/file-transfer.md#what-5x-asks-for-at-login-cap) |
| 5.x | then 34 for `idle.gani`, `sprites.png`, `body.png`, `head0.png`, `shield1.png` and the `guigames_*` images, and 23 for the fonts (`arial.ttf`, `arialbd.ttf`) and `tiledefs<server>.txt` | [cap] (protocol/file-transfer.md#what-5x-asks-for-at-login-cap) |

Update packages and their messages (105, 106, 187) are in → §2.5.7.

## 2.7.5 The client's request lists

| Rule | Builds | Source |
| --- | --- | --- |
| The client keeps three name lists: wanted (asked with 23), update-asked (asked with 34) and settled (a reply came back) | 2.00, 2.05 rev 2, 2.17.1, 2.22, 2.31 | [bin] (client-internals/decomp-findings-2026-10-25-e/01-request-lists.md#lists) |
| No local copy: the name is appended to the wanted list unless already there, and sent while that list holds at most four names | same | [bin] (client-internals/decomp-findings-2026-10-25-e/01-request-lists.md#asking) |
| A local copy: the name is appended to the update-asked list unless it is there or settled, and sent while that list holds at most four; so each local file is checked at most once per connection | same | [bin] (client-internals/decomp-findings-2026-10-25-e/01-request-lists.md#asking) |
| The time in 34 is the local file's last-write time in Unix seconds; at login it matched the files' times for the sword, shield and body images | same; 2.22 (lab) | [bin][cap] (client-internals/decomp-findings-2026-10-25-e/01-request-lists.md#asking) |
| Builds with no id 34 never check a local copy | 1.33 to 1.41 | [bin] (client-internals/decomp-findings-2026-10-25-e/01-request-lists.md#asking) |
| Any reply (the file, up to date, send failed, or the end of a large file) removes the name from both lists and adds it to the settled list; if the name was among the first four, the name now fourth goes out; the two lists release independently | same | [bin] (client-internals/decomp-findings-2026-10-25-e/01-request-lists.md#replies) |
| Four of each kind were on the wire before the first reply | 2.22 (lab) | [cap] (client-internals/decomp-findings-2026-10-25-e/README.md#top-facts) |
| The client never compares times; the server decides | same | [bin] (client-internals/decomp-findings-2026-10-25-e/README.md#top-facts) |
| A name answered with 30 is not asked for again on that connection: a missing step sound was asked for once however often the player walked | 2.22 (lab) | [cap] (client-internals/decomp-findings-2026-10-25-e/01-request-lists.md#failed-names) |
| Images and ganis: a local file is used and checked, a missing one asked for; sounds: asked for only when missing, never checked; levels: no file transfer (board messages and the level modtime instead, → §3.8); a gmap: checked when present, asked for when missing | 2.05 rev 2, 2.22; gmap 2.22 (lab) | [bin][cap] (client-internals/decomp-findings-2026-10-25-e/01-request-lists.md#who-asks) |
| In 2.05 rev 2 and 2.22 the request side was read from the matching reply-side code and the lab | 2.05 rev 2, 2.22 | [inf] (client-internals/decomp-findings-2026-10-25-e/request-rules.tsv) |

## 2.7.6 Saving a download

| Rule | Builds | Source |
| --- | --- | --- |
| A received file is held in memory and written to disk only when `saveimages` is on (default on, → §3.9.3) | 2.05 rev 2 to 2.31 | [bin] (client-internals/decomp-findings-2026-10-25-e/02-save-rules.md#whether-a-file-is-written) |
| An empty or missing stream is never saved: nothing is written or deleted and the loaders are not told | 1.39, 2.00, 2.05 rev 2, 2.17.1, 2.22, 2.31 | [bin] (client-internals/decomp-findings-2026-10-25-k/02-save-folders-by-build.md#the-guard) |
| A file the client already has is replaced where it is; a new one is placed by name, compared without case | 2.00 and later | [bin] (client-internals/decomp-findings-2026-10-25-e/02-save-rules.md#where) |
| From 2.1 the saved file gets the time from the reply, so the next check carries the server's time; before 2.1 it keeps the download time | 2.1 and later; earlier | [bin] (client-internals/decomp-findings-2026-10-25-e/02-save-rules.md#time-of-the-saved-file) |

Where a new download is saved, by build:

| Builds | Folders | Source |
| --- | --- | --- |
| 1.33 to 1.41 | everything in `levels/webgifs`; 1.39 saves only `.gif`, `.png` and `.mng`, deletes an old copy first and sets no time | [bin] (client-internals/decomp-findings-2026-10-25-k/02-save-folders-by-build.md#layouts) |
| 1.42 NewMain | the earlier build adds `ganis`, `heads`, `swords`, `shields`; the later adds `sounds` for `.wav` and `bomys` | [bin] (client-internals/decomp-findings-2026-10-25-k/02-save-folders-by-build.md#layouts) |
| 2.00, 2.01 | `sounds` for `.wav`; under `levels`: `bomys` (names starting `bomy` or `b_`), `ganis` (`.gani`), `emoticons` (names starting `emoticon`), `heads`, `bodies`, `swords`, `shields` (names containing those words), else `webgifs` | [bin] (client-internals/decomp-findings-2026-10-25-k/02-save-folders-by-build.md#layouts) |
| 2.02 to 2.05 rev 2, both 2.1 test builds | as 2.00, plus `hats` (`hat` then a digit as the fourth character) | [bin] (client-internals/decomp-findings-2026-10-25-k/02-save-folders-by-build.md#layouts) |
| 2.17.1, 2.22, 2.31 | as 2.05, plus `maps` for `.gmap` and for `.txt`, `.gif`, `.png`, `.mng` names containing `map`; a 2.22 gmap download was saved as `maps/<name>` | [bin][cap] (client-internals/decomp-findings-2026-10-25-k/save-folders-by-build.tsv); [cap] (client-internals/decomp-findings-2026-10-25-e/02-save-rules.md#where) |
| 2.1 to 2.16 | no binary; when `maps` arrived is unknown (→ App. E#10) | [doc] (client-internals/decomp-findings-2026-10-25-k/02-save-folders-by-build.md#layouts) |

## 2.7.7 Finding a local file

| Rule | Builds | Source |
| --- | --- | --- |
| Names are folded A to Z only, then compared byte for byte; accented letters do not match across case | 2.05 rev 2, 2.22 | [bin] (client-internals/decomp-findings-2026-10-25-e/04-name-index-case-link.md#case-fold) |
| A file of that name in the current directory wins first: the game folder in 2.22, the `levels` folder in 2.05 rev 2 (or a world opened from elsewhere) | 2.05 rev 2, 2.22 | [bin] (client-internals/decomp-findings-2026-10-25-e/04-name-index-case-link.md#which-copy-is-used) |
| 2.22 indexes the game folder at startup, files before subdirectories in listing order, skipping top-level `pms`, `profiles` and `weblevels` and `.code` files; for a duplicate name the newer last-write time wins, and an equal time keeps the first found | 2.22 | [bin] (client-internals/decomp-findings-2026-10-25-e/04-name-index-case-link.md#which-copy-is-used) |
| 2.05 rev 2 looks up on demand: the current directory, then a remembered path, then a depth-first search of an opened world's folder and the game folder with the same skips; the first hit wins and is remembered | 2.05 rev 2 | [bin] (client-internals/decomp-findings-2026-10-25-e/04-name-index-case-link.md#which-copy-is-used) |
| For two different files of one name, 2.22 draws the newer and 2.05 rev 2 the first found | 2.05 rev 2, 2.22 | [bin] (client-internals/decomp-findings-2026-10-25-e/name-index-rules.tsv) |
