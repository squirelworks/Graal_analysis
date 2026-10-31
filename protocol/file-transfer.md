# File transfer

Date: 2026-10-21

Sources: GServer-v2 `TPlayer::sendFile`, `msgPLI_WANTFILE`, `msgPLI_UPDATEFILE` (GPLv3, summarized); 2.05 dispatch and sender tables. Tags as elsewhere.

## Requests (client → server)

| Id | Name | Layout | 2.05 | Notes |
|---:|------|--------|:----:|-------|
| 23 | WANTFILE | rest = filename | ✔ | Pre-2.1: the server appends `.gif` when there is no extension **[srv]** |
| 34 | UPDATEFILE | `i5 cached modtime` + rest = filename | ✔ | The server sends the file if the modtime differs; otherwise it replies "up to date" **[srv]** |
| 47 | VERIFYWANTSEND | `i5 crc32` + rest = filename | · | 2.x later |
| 155/156 | RC_LARGEFILESTART/END | RC upload framing | · | RC only |

## Replies (server → client)

| Id | Name | Layout | 2.05 |
|---:|------|--------|:----:|
| 100 | RAWDATA | `i3 length` of the next message | ✔ |
| 102 | FILE | see below; always behind RAWDATA | ✔ via 100 |
| 30 | FILESENDFAILED | rest = filename. **Pre-2.1 also uses this for "already up to date"** | ✔ |
| 45 | FILEUPTODATE | rest = filename (≥ 2.1) | ✔ (handled, but the server does not send it to 2.05) |
| 68 / 69 | LARGEFILESTART / END | rest = filename | · |
| 84 | LARGEFILESIZE | `i5 size` | · |

### PLO_FILE body **[srv]**

| Client | Layout |
|--------|--------|
| < 2.1 (**2.05**) | `c(102)` `str filename` + file bytes. No modtime, no trailing `\n`. RAWDATA length = 1 + 1 + name + data |
| 2.1 – 2.13 | `c(102)` `i5 modtime` `str filename` + bytes + `\n`, all in one piece |
| ≥ 2.14 | as above, split into 32000-byte chunks; files > 32000 bytes are wrapped in LARGEFILESTART / LARGEFILESIZE / LARGEFILEEND |

Clients before 2.14 cannot receive files over 64000 bytes. The server answers FILESENDFAILED instead. **[srv]**

## The layout follows the server's token table, not the client (2026-10-31)

Every version branch in GServer's file code tests `versionID`, and `versionID` comes only from the login token looked up in gs2lib's table. A token that is allowed (`allowedversions.txt`) but not in the table gets `CLVER_UNKNOWN` (0), which is below every real version. **[srv]**

What such a client gets, from GServer-v2 `efb5b90` (`TPlayer::sendFile`, `msgPLI_WANTFILE`, `msgPLI_UPDATEFILE`, `TPlayerProps`): **[srv]**

| Below | Server behaviour |
|---|---|
| 2.1 | `PLO_FILE` without the GINT5 modtime and without the trailing `\n` |
| 2.1 | an up-to-date `UPDATEFILE` is answered with 30 (`FILESENDFAILED`), not 45 |
| 2.1 | `.gif` is added to a requested name with no extension, and numbered head, body, sword and shield props get `.gif` names |
| 2.1 | the level goes through `sendLevel141`, with no `PLO_SETACTIVELEVEL` (156) |
| 2.14 | no large-file packets: a file over 64000 bytes is answered with 30 |

### The 5.24 "PNG as file name" bug

- Stock gs2lib has no `G3D15010` (5.24r3, 5.24r4, 6.00 beta2) and no `G3D03048` (6.00 beta1), so GServer serves those builds every pre-2.1 path. Read in gs2lib `5c36ab8` (the version GServer beta4 fetches; see the table below). **[src]**
- The client always reads `PLO_FILE` as `i5 modtime` + `str filename` + data. Given the old layout, it takes the length byte and the first 4 characters of the name as the modtime, and the 5th character as the name length. **[srv][inf]**
- For `sword1.png` that is `*swor` as the modtime and `d` (68) as the length, so the "name" is `1.png` followed by 63 bytes of PNG data. That is the lab message "Couldn't open …1.png‰PNG… for writing". **[cap]** for the message, the byte walk is worked from the server code.
- With a gs2lib copy that knows `G3D15010`, the same server sent 5.24r4 `&w1vH)state.png‰PNG…` (GINT5 modtime, then the name) and the client saved the files normally (v5x lab proxy log 2026-10-30b, connection c6). **[cap]**

### gs2lib's version table **[src]**

Read in gs2lib `5c36ab8` (`src/IUtil.cpp` `clientVersions[]`, `include/IUtil.h` `CLVER_*`):

- `getVersionID` walks `clientVersions[]` and returns the **index** of the first exact match, or `CLVER_UNKNOWN` (0). The index is the `CLVER_*` value. So a token's rank is simply its position in the array, and every `versionID < CLVER_x` test in GServer compares positions.
- The 5.x/6.x part of the table, in order:

| Token | Enum | Build |
|---|---|---|
| `G3D22067` | `CLVER_5_07` | 5.00r7 |
| `G3D14097` | `CLVER_5_12` | 5.12 |
| `G3D26090` | `CLVER_5_31x` | 5.30r3, 5.31r4, 6.00r2, 6.00r4 |
| `G3D3007A` | `CLVER_6_015` | 6.01x (no lab build) |
| `G3D2505C` | `CLVER_6_034` | 6.034/6.035 |
| `G3D0311C` | `CLVER_6_037` | 6.03r7 Windows |
| `G3D0511C` | `CLVER_6_037_LINUX` | 6.03r7 Linux |

- `G3D15010` and `G3D03048` appear nowhere in the source. (With `gs2lib-CLVER_5_24.patch`, `G3D15010` becomes `CLVER_5_24`, between `G3D14097` and `G3D26090`.) All 5.x/6.x entries sit far above `CLVER_2_14`.
- The array and the enum must stay in step: an entry added to one without the other shifts every later version id.

**Rule.** A server for 5.x and 6.x clients must know every token it allows. Every 5.x/6.x slot in the table is above `CLVER_2_14`, so any of them gives files with the modtime and large files in chunks. **[src]** The lab got there by renaming one entry to `G3D15010` (`G3D26090` in the v5 lab, `G3D14097` in the "Play v5 and v6 clients" lab, see `version-profiles/lab-v5-2026-10-30.md` and `v5v6-lab-play.md`). Each rename takes the renamed build off the table (5.30 to 6.00r4, or 5.12). The clean fix is a new `CLVER_5_24` between `CLVER_5_12` and `CLVER_5_31x`, added to both the array and the enum. **Done 2026-10-31:** `tools/lab-servers/gs2lib-CLVER_5_24.patch` (and a `b839106` version for the efb5b90 lab build) adds that slot. Real 5.24r4 on GServer efb5b90 with the patched library got every file in the new layout, including `pics1.png` as a large file, and saved them byte for byte. On stock gs2lib it reproduced the bug. **[cap]** Details are in `tools/lab-servers/README.md`. **[src]** for the table, **[inf]** for the placement: it follows the build dates, and no original server's table was seen. Where 5.24 sits matters only for tests against `CLVER_5_*` or `CLVER_6_015`; GServer `efb5b90` has one (`versionID < CLVER_6_015` in `TPlayerLogin.cpp`), and 5.24 is below `CLVER_6_015` in either slot, so it takes the same branch.

**Client side.** A client cannot tell the server which layout to use. Seihai reads with the profile's layout first and, if the name comes out with control bytes, no dot, or longer than the message, reads the other layout and keeps it for the connection (Seihai `documentation/file-cache.md`). **[inf]**

### What 5.x asks for at login **[cap]**

- 5.24r4, 5.30r3 and 6.03r7 open with `basepackage.gupd`. With an empty cache it goes as 23 (`WANTFILE`), twice (v5x lab 2026-10-30b; `v5v6-windows-unpacked.md`).
- In the "Play v5 and v6 clients" runs, 5.24 and 6.03r7 sent it as **47** (`VERIFYWANTSEND`, `i5 crc32` + name), twice, while the `G3D26090` build sent 23 (`lab-v5v6/logs`). That 47 is used when a copy is already cached is **[inf]**: the cache state of those runs was not recorded.
- Then `UPDATEFILE` for `idle.gani`, `sprites.png`, `body.png`, `head0.png`, `shield1.png` and the `guigames_*` images, and `WANTFILE` for the fonts (`arial.ttf`, `arialbd.ttf`) and `tiledefs<server>.txt`.

## Typical flow for 2.05 **[srv][inf]**

1. A level arrives that references `head25.png`, `sword1.png`, or `walk.gani`.
2. The client checks its local cache. For a cached file it sends `UPDATEFILE(modtime, name)`, otherwise `WANTFILE(name)`.
3. The server replies `RAWDATA(len)` + `FILE(name, bytes)`, or `FILESENDFAILED(name)`, which for 2.05 means "missing or unchanged".

The 2026-10-04 clear sessions show this pattern. Server frames there contain `sword1.png`, `head25.png`, `walk.gani`, and `steps.wav` pushes. **[cap]**

## Upload (RC only)

RemoteControl's folder change (0x5a wire) and upload ids are in `tools/remotecontrol.md`. In gs2lib, the RC file browser covers ids 89–98 (`PLI_RC_FILEBROWSER_*`) and `PLO_RC_FILEBROWSER_DIRLIST`/`DIR`/`MESSAGE` (65–67). Game clients cannot upload. **[srv]**

## Open
- How 2.05 picks its local cache folder, and whether it ever sends `UPDATEFILE` for level files or only for images.
- The 2.05 handlers for 30 and 45 were found in the jump table but have not been traced.
