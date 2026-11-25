<!-- manual: kind=reference status=draft -->
# 2.7 File transfer

The request messages are laid out in → §2.4.7 and the replies in → §2.5.7; the raw-data escape is in → §2.1.3. This chapter gives the sequence and the version rules.

> Status: draft.

## 2.7.1 Requests and replies

A client asks for a file in one of three ways. Each row gives a request, the reply when the server sends the file, the reply when it does not, and the builds that use that request [srv] (protocol/file-transfer.md#requests-client--server).

| Request | Reply when the file is sent | Reply otherwise | Builds | Source |
| --- | --- | --- | --- | --- |
| 23 `PLI_WANTFILE` (name) | 100 `RAWDATA` + 102 `FILE` | 30 `FILESENDFAILED` (name) | 1.21 to 6.x | [srv] (protocol/file-transfer.md#requests-client--server) |
| 34 `PLI_UPDATEFILE` (`i5` cached modtime, name) | 100 + 102 when the modtime differs | below 2.1: 30; 2.1 and later: 45 `FILEUPTODATE` | 1.42 to 6.x | [srv] (protocol/file-transfer.md#requests-client--server) |
| 47 `PLI_VERIFYWANTSEND` (`i5 crc32`, name) | 100 + 102 when the client's copy is stale | unmeasured | 5.00r7, 5.24, 6.x | [srv] (protocol/file-transfer.md#requests-client--server); [cap] (protocol/file-transfer.md#what-5x-asks-for-at-login-cap) |

The rules below cover the edge cases of those replies, which differ either side of 2.1, and say that game clients never upload [srv] (protocol/file-transfer.md#requests-client--server).

| Rule | Builds | Source |
| --- | --- | --- |
| Below 2.1 the server adds `.gif` to a requested name with no extension | server | [srv] (protocol/file-transfer.md#requests-client--server) |
| Below 2.1, 30 also means "already up to date"; 2.05 handles 45, but the server does not send it to 2.05 | server; 2.05 | [srv] (protocol/file-transfer.md#replies-server--client) |
| Game clients cannot upload; RC upload uses the file-browser ids 89 to 98 and 65 to 67 (→ §7). 6.x clients carry the ids for the scripted-RC file browser; on a game connection the GServer-v2 fork treats them as unknown packets (→ §2.7.1) | server | [srv] (protocol/file-transfer.md#upload-rc-only); [lab] (protocol/lab-appe-hostb-2026-11-20.md#upload-ids-from-a-game-connection-e9) |

**Settled question, formerly E#9: uploads from game clients.** Which game-client feature sends the file-browser and upload ids, and whether a server accepts them from a game connection, was open; a lab run and the client's own strings settled it [lab] (protocol/lab-appe-hostb-2026-11-20.md#upload-ids-from-a-game-connection-e9).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: game clients cannot upload; the ids are RC-only. B: 6.01r1 and 6.03r7 send the ids with an upload queue | [srv] (protocol/file-transfer.md#upload-rc-only); [bin] (protocol/v6x-clients.md#client--server-ids-601-603) |
| Settled | 6.03r7 describes its upload calls as working only while the scripted RC has a file browser open: they are the scripted-RC staff feature. On the GServer-v2 fork, those ids on a game connection are unknown packets; after three the player is dropped, and no file is written | [lab] (protocol/lab-appe-hostb-2026-11-20.md#upload-ids-from-a-game-connection-e9) |
| Verdict | Verified for the fork; both claims hold, for different connections. Original servers were not run | [lab] (protocol/lab-appe-hostb-2026-11-20.md#upload-ids-from-a-game-connection-e9) |

## 2.7.2 The `PLO_FILE` body

The following historical rows describe server version branches; the exact original 2.05r2 receiver differs → §2.7.9 [2.05][bin] (protocol/file-205r2-prefix-lf.md#exact-receiver-boundary).

| Client version (by the server's token table) | Layout behind 100 | Source |
| --- | --- | --- |
| historical server branch below 2.1 | `c 102`, `str filename`, then the file bytes; no modtime and no trailing `\n`; the RAWDATA length is 1 + 1 + name + data | [srv] (protocol/file-transfer.md#plo_file-body-srv) |
| 2.1 to 2.13 | `c 102`, `i5 modtime`, `str filename`, the bytes, then `\n`, in one piece | [srv] (protocol/file-transfer.md#plo_file-body-srv) |
| 2.14 and later | as 2.1, split into 32000-byte chunks; a file over 32000 bytes is wrapped in 68 `LARGEFILESTART`, 84 `LARGEFILESIZE` and 69 `LARGEFILEEND` | [srv] (protocol/file-transfer.md#plo_file-body-srv) |

The rules below give the size limit on a single file, and how a large file arrives in chunks and is put back together [srv] (protocol/file-transfer.md#plo_file-body-srv).

| Rule | Builds | Source |
| --- | --- | --- |
| A client before 2.14 cannot receive a file over 64000 bytes; the server answers 30 instead | server | [srv] (protocol/file-transfer.md#plo_file-body-srv) |
| A 541,248-byte file reached 5.00r7 as 68, 84, then 102 chunks each with modtime and name, then 69, and was saved byte for byte | 5.00r7 (lab, stock gs2lib) | [cap][bin] (protocol/file-transfer.md#what-5x-asks-for-at-login-cap) |
| On 69 the client compares the name with the stored one and processes the accumulated stream as one file (→ §2.5.7) | 2.17.1 to 2.31 | [bin] (version-profiles/plo-layouts-217-231.tsv) |

## 2.7.3 The layout follows the server's token table

Which file layout a client gets depends on how the server ranks its token, not on what the client can parse. The rules explain that ranking and what an unranked token causes [srv] (protocol/file-transfer.md#the-layout-follows-the-servers-token-table-not-the-client-2026-10-31).

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

For the focus builds the ladder above gives: 1.39 takes the pre-2.1 path and never sends id 34; 2.22 and later take the ≥ 2.14 path with 32000-byte chunks, and 2.31 adds 84 to its receive set; 4.20r8, 5.00r7, 5.12 and 6.03r7 take the same path when the server's table knows their tokens, and fall back to the pre-2.1 path (large files fail with 30) when it does not. A static read of 4.20r8, 5.00r7, 5.12 and 6.03r7 found handlers for 68, 69 and 84 in all four and no receive-side size limit: 84 only feeds progress, and 69 saves whatever arrived without comparing it to 84. [srv][bin][cap] (protocol/large-file-thresholds-focus.md#receive-handlers-on-4208-to-6037-g262-2026-11-25)

The recorded patched 1.41r1 input is generation 3 (`GNW13110`). Its 45 direct receive cases are 0–41, 43, 75 and 100, so 68/69 are absent from that switch. This does not establish the FILE body behind RAWDATA 100: the exact raw/file subpath remains unread. It is not a pristine-vendor or all-copies claim [bin] (protocol/file-profile-evidence-2026-11-21.md#the-recorded-141r1-input).

The 2.22/2.31 profile's `defaults.gen5` is a local shared block, not literal inheritance from a 2.1 profile. Its `file_modtime` and `image_ext_default` historical ≥2.1 comments describe server gates; `large_files` combines recorded 68/69 receive cases with a server chunk size. Those dimensions do not independently establish native metadata handling, extension selection or size limits. Existing UDP evidence covers `noudp` and `fixedudpport` presence and default-off behavior, not the numeric fixed-port default; `zlib_fix_npc` remains a server workaround with inferred native equivalence [bin][srv][inf] (protocol/file-profile-evidence-2026-11-21.md#shared-222-and-231-defaults).

The profile's combined `compression_src` tag also needs direction: real 2.22 client-originated raw/zlib frames include partial compressed groups, but client-originated bz2 remains unseen. This reconciliation changes comments and provenance, not profile values [cap] (protocol/file-profile-evidence-2026-11-21.md#captures-remain-directional).

## 2.7.4 Requests at login

Each build asks for different files when it enters a server. The table gives the first requests seen per build. The late builds always start with the base package [srv][inf][cap] (protocol/file-transfer.md#typical-flow-for-205-srvinf).

| Build | Requests seen | Source |
| --- | --- | --- |
| 2.05 | for each file a level references (for example `head25.png`, `sword1.png`, `walk.gani`): 34 when cached, else 23; the server answers 100 + 102 or 30 | [srv][inf][cap] (protocol/file-transfer.md#typical-flow-for-205-srvinf) |
| 2.22 | 34 for the default images (sword, shield, body, bomb), then 23 (→ §2.4.11) | [cap] (version-profiles/2.22-2.31.md#wire-protocol) |
| 5.24r4, 5.30r3, 6.03r7 | `basepackage.gupd` first; with an empty cache as 23, twice | [cap] (protocol/file-transfer.md#what-5x-asks-for-at-login-cap) |
| 5.00r7 | `basepackage.gupd` as 47 when that server's copy is cached and as 23 when not; the cache is kept per server name | [cap] (protocol/file-transfer.md#what-5x-asks-for-at-login-cap) |
| 5.x | then 34 for `idle.gani`, `sprites.png`, `body.png`, `head0.png`, `shield1.png` and the `guigames_*` images, and 23 for the fonts (`arial.ttf`, `arialbd.ttf`) and `tiledefs<server>.txt` | [cap] (protocol/file-transfer.md#what-5x-asks-for-at-login-cap) |

Update packages and their messages (105, 106, 187) are in → §2.5.7.

## 2.7.5 The client's request lists

A client does not ask for a file twice. The rules below describe the three lists it keeps, how many requests it allows in flight, and when a name moves from one list to another [bin] (client-internals/decomp-findings-2026-10-25-e/01-request-lists.md#lists).

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

The rules below say when a download is written to disk, where it goes, and which modification time it keeps [bin] (client-internals/decomp-findings-2026-10-25-e/02-save-rules.md#whether-a-file-is-written).

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
| Graal 2002 ver7, ver8 (2.1.0.0, Oct 2001) | as the 2.1 test builds: no `maps` rule, so a downloaded `.gmap` lands in `levels/webgifs` | [bin] (client-internals/graal2002-save-folders-2026-11-20.md#where-a-downloaded-file-is-saved) |
| Graal 2002 ver9 (2.1.0.0, 30 Oct 2001) to v22 (2.1.0.4) | the first builds with the `maps` rule, already in the 2.17.1 form | [bin] (client-internals/graal2002-save-folders-2026-11-20.md#where-a-downloaded-file-is-saved) |
| 2.12 to 2.16 | no binary; very probably the `maps` rule, since every build from ver9 on has it | [inf] (client-internals/graal2002-save-folders-2026-11-20.md#where-a-downloaded-file-is-saved) |

**Settled question, formerly E#10: when the `maps` download folder arrived.** Which build first saved downloads into `maps` was open between the 2.1 test builds and 2.17.1. A static read of the six Graal 2002 images settled it: ver9 (2.1.0.0, shipped 30 Oct 2001) is the first, and ver7 and ver8 still save a `.gmap` into `levels/webgifs` [bin] (client-internals/graal2002-save-folders-2026-11-20.md#where-a-downloaded-file-is-saved). The save rule comes before the gmap loader, which none of 2.1.0.0 to 2.1.0.4 has [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#gmap-code-in-the-21-builds-e10).

In the same builds no folder is made at start-up: each is created just before its first write, by the download save, the web-level cache (`weblevels/<host>/<level>-<port>.code`, `GWEBL001` then `GR-V1.03` text), the PM log, profiles, tiledefs and tile objects. The start-up file index skips folders named in `+pms+profiles+weblevels+`, so those files are never served as game files; `maps` is indexed [bin] (client-internals/graal2002-save-folders-2026-11-20.md#when-folders-are-made).

## 2.7.7 Finding a local file

Before asking the server, a client looks for the file on disk. The rules below give how it matches names and in which order it searches, for 2.05 rev 2 and 2.22 [bin] (client-internals/decomp-findings-2026-10-25-e/04-name-index-case-link.md#case-fold).

| Rule | Builds | Source |
| --- | --- | --- |
| Names are folded A to Z only, then compared byte for byte; accented letters do not match across case | 2.05 rev 2, 2.22 | [bin] (client-internals/decomp-findings-2026-10-25-e/04-name-index-case-link.md#case-fold) |
| A file of that name in the current directory wins first: the game folder in 2.22, the `levels` folder in 2.05 rev 2 (or a world opened from elsewhere) | 2.05 rev 2, 2.22 | [bin] (client-internals/decomp-findings-2026-10-25-e/04-name-index-case-link.md#which-copy-is-used) |
| 2.22 indexes the game folder at startup, files before subdirectories in listing order, skipping top-level `pms`, `profiles` and `weblevels` and `.code` files; for a duplicate name the newer last-write time wins, and an equal time keeps the first found | 2.22 | [bin] (client-internals/decomp-findings-2026-10-25-e/04-name-index-case-link.md#which-copy-is-used) |
| 2.05 rev 2 looks up on demand: the current directory, then a remembered path, then a depth-first search of an opened world's folder and the game folder with the same skips; the first hit wins and is remembered | 2.05 rev 2 | [bin] (client-internals/decomp-findings-2026-10-25-e/04-name-index-case-link.md#which-copy-is-used) |
| For two different files of one name, 2.22 draws the newer and 2.05 rev 2 the first found | 2.05 rev 2, 2.22 | [bin] (client-internals/decomp-findings-2026-10-25-e/name-index-rules.tsv) |

## 2.7.8 Unpacked Windows 6.1.1.3 packages

The unpacked 6.1.1.3 image was searched for package and download names. The two rules record what was found and what was not [bin] (protocol/v6113-files.md#names-in-the-image).

| Rule | Builds | Source |
| --- | --- | --- |
| The only `.gupd` file name in the image is `basepackage.gupd`. `package_mainfiles.gupd` is not in the listing. `game_console.log` is a path the client opens, and the log is not in the repository | 6.1.1.3 | [bin] (protocol/v6113-files.md#names-in-the-image) |
| `onSendUpdatePackage` and `onSendDownloadFile` are present. A numeric request id for `basepackage.gupd` was not recovered | 6.1.1.3 | [bin] (protocol/v6113-files.md#request-ids) |

## 2.7.9 Exact original Windows 2.05r2 receiver

The 2.05 rev 2 file receiver was read exactly. Each row names one property of it and gives the detail. The last rows say how a server was checked against it, and how far that check goes [2.05][bin] (protocol/file-205r2-prefix-lf.md#exact-receiver-boundary).

| Rule | Detail | Source |
| --- | --- | --- |
| counted layout | FILE opcode, five encoded metadata bytes unconditionally, encoded one-byte filename length L, L name bytes, content; for raw count N, content length is N − 7 − L | [2.05][bin] (protocol/file-205r2-prefix-lf.md#exact-receiver-boundary) |
| LF boundary | collector bypasses normal delimiter subtraction; all N bytes reach FILE copy, including a terminal LF inside N; outside-count bytes are not content | [2.05][bin] (protocol/file-205r2-prefix-lf.md#exact-receiver-boundary) |
| baseline mismatch | tested server commit 1b0a6e omitted prefix before 2.1, counted an added LF and emitted no empty FILE; local fixes correct those paths without changing the receiver specification | [srv][lab] (protocol/file-205r2-prefix-lf.md#server-comparison-and-controlled-checks) |
| synthetic checks | two profiles × five fixtures improved 0/10 to 10/10 filename/content checks; not ten original-client runs | [lab] (protocol/file-205r2-prefix-lf.md#server-comparison-and-controlled-checks) |
| original-client evidence | unchanged 2.05r2 entered local world, requested all fixtures, sent movement properties and saved exact no-LF/one-LF/binary-LF files; two-LF valid-GIF persistence required repeating unchanged server record to already-requested name | [2.05][lab] (protocol/file-205r2-prefix-lf.md#server-comparison-and-controlled-checks) |
| residuals | initial two-LF caching and empty persistence unresolved; unsolicited alias not cached; byte-copy does not establish general retry/registration/deduplication | [lab] (protocol/file-205r2-prefix-lf.md#server-comparison-and-controlled-checks) |
| fixture | isolated Wine/display namespaces, loopback only/no routes, unchanged executable and completed cleanup; labeled 2.31 donor resources, not authentic full 2.05 distribution | [lab] (protocol/file-205r2-prefix-lf.md#fixture-and-execution-limits) |
| startup qualification | only copied world greeting emptied to bypass HTML/Wine stall; milestone 6 and equal level objects; default greeting unchanged; native Windows/cause unproved | [lab] (protocol/file-205r2-prefix-lf.md#fixture-and-execution-limits) |
| limits | other clients, large-file continuation and malformed inputs remain unqualified; no server patches published in this increment | [lab] (protocol/file-205r2-prefix-lf.md#fixture-and-execution-limits) |

## 2.7.10 The 2.22 start-up file checks

Windows 2.22 (`GNW03014`) on a loopback lab, listserver port 14922 and the decrypting proxy on 14803. The near-empty folder that reaches the server list is the executable, `bass.dll`, `basswma.dll`, `hvdi.dll`, `arrays.dat`, `arrays2.dat`, `arrays2.sig`, `graal.sig` and `pics1.png`. The login screen itself appears once `graal.sig` is present; its images are inside the executable. Start Online then asks for `arrays.dat` and `pics1.png`. The client writes `graalconfig.txt`, `servermessage.html` and `weblevels` itself. [lab] (live-runs/open-issues-2026-11-14/README.md#4-245-222-login-default-checks-with-a-near-empty-data-folder)

Both the near-empty folder and a full folder sent their file checks in the second client-to-server frame, together with the first player-props line (id 2), one zlib frame, 0.3 s after login. [lab] (live-runs/open-issues-2026-11-14/README.md#4-245-222-login-default-checks-with-a-near-empty-data-folder)

| Folder | In that frame, besides the props line | Source |
| --- | --- | --- |
| near-empty | id 23 for `idle.gani` and for the online, away and do-not-disturb player-list icons | [lab] (live-runs/open-issues-2026-11-14/README.md#4-245-222-login-default-checks-with-a-near-empty-data-folder) |
| full | id 34 for four other player-list icons (eating, hiding, no private messages, role-playing), each with a 5-byte modification time first, then id 23 for `steps.wav` and one gani | [lab] (live-runs/open-issues-2026-11-14/README.md#4-245-222-login-default-checks-with-a-near-empty-data-folder) |

Id 23 asks for a file the client does not have. Id 34 is the update check and carries the local file's modification time. Which player-list icons are named follows the status list in S→C 180. With a full folder the online, away and do-not-disturb icons were not asked for; with a near-empty folder only those three were. [lab] (live-runs/open-issues-2026-11-14/README.md#4-245-222-login-default-checks-with-a-near-empty-data-folder)

This server answered none of those requests: no S→C 102 and no 30. Neither client sent another file check afterwards, so sword, shield, body, bomb, bow and head images were not in this capture even though S→C 9 named some of them. The set above is only what leaves before any answer. An earlier run whose server did answer saw two further frames. A rerun against a server that answers id 23 and id 34 is still needed for the rest of the default set. [lab] (live-runs/open-issues-2026-11-14/README.md#4-245-222-login-default-checks-with-a-near-empty-data-folder)

The shared second-frame bundling and the near-empty against full first wave were settled first [lab] (protocol/222-login-default-files.md). A 2026-11-19 rerun with a GServer-v2 build that answers each check took the client past its first frame and gave the whole set [lab] (live-runs/open-issues-2026-11-19/README.md#4-245-222-login-default-checks-with-a-server-that-answers).

| Data folder | Packet | Files checked | Source |
| --- | --- | ---: | --- |
| full | 34 (modification time, then name) | 13 | [lab] (live-runs/open-issues-2026-11-19/README.md#4-245-222-login-default-checks-with-a-server-that-answers) |
| near-empty (root start-up files only) | 23 (name only) | 17 | [lab] (live-runs/open-issues-2026-11-19/README.md#4-245-222-login-default-checks-with-a-server-that-answers) |

| Rule | Builds | Source |
| --- | --- | --- |
| At most four file packets go in one frame. The first four share a frame with the first flags and props line, and each later batch of up to four waits until the server has answered the batch before it | 2.22 | [lab] (live-runs/open-issues-2026-11-19/README.md#4-245-222-login-default-checks-with-a-server-that-answers) |
| With nothing but the executable, 2.22 stops at start-up because `pics1.png` is missing, so a near-empty folder still needs the root start-up files | 2.22 | [lab] (live-runs/open-issues-2026-11-19/README.md#4-245-222-login-default-checks-with-a-server-that-answers) |

The difference is five files (`idle.gani`, `plisticononline.png`, `plisticonaway.png`, `plisticondnd.png`, `head0.png`) that 2.22 requests when missing and never update-checks when present; a re-run of the near-empty case requested 18 (→ §2.7.10). [lab] (live-runs/open-issues-2026-11-19/README.md#4-245-222-login-default-checks-with-a-server-that-answers); [lab] (protocol/lab-appe-hosta-2026-11-20.md#start-up-file-checks-on-222-e25)

**Settled question, formerly E#25: the 2.22 start-up file checks: 13 against 17.** Why 2.22 checks 13 files with a full data folder and more with a near-empty one was open; the two runs' file lists set side by side settled it [lab] (protocol/lab-appe-hosta-2026-11-20.md#start-up-file-checks-on-222-e25).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | A full folder checks 13 files with id 34; a near-empty folder checks 17 with id 23 | [lab] (live-runs/open-issues-2026-11-19/README.md) |
| Settled | A re-run requested 18 with id 23 and update-checked 13 with id 34. Five files, `idle.gani`, `plisticononline.png`, `plisticonaway.png`, `plisticondnd.png` and `head0.png`, are requested when missing and never update-checked when present; `block.png` is a level file and appears in both | [lab] (protocol/lab-appe-hosta-2026-11-20.md#start-up-file-checks-on-222-e25) |
| Verdict | Verified: the best guess held, with five such files rather than four | [lab] (protocol/lab-appe-hosta-2026-11-20.md#start-up-file-checks-on-222-e25) |
