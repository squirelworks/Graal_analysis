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

- Stock gs2lib has no `G3D15010` (5.24r3, 5.24r4, 6.00 beta2) and no `G3D03048` (6.00 beta1), so GServer serves those builds every pre-2.1 path (`server-notes/lab-servers-2026-10-30.md`). **[srv]**
- The client always reads `PLO_FILE` as `i5 modtime` + `str filename` + data. Given the old layout, it takes the length byte and the first 4 characters of the name as the modtime, and the 5th character as the name length. **[srv][inf]**
- For `sword1.png` that is `*swor` as the modtime and `d` (68) as the length, so the "name" is `1.png` followed by 63 bytes of PNG data. That is the lab message "Couldn't open …1.png‰PNG… for writing". **[cap]** for the message, the byte walk is worked from the server code.
- With a gs2lib copy that knows `G3D15010`, the same server sent 5.24r4 `&w1vH)state.png‰PNG…` (GINT5 modtime, then the name) and the client saved the files normally (v5x lab proxy log 2026-10-30b, connection c6). **[cap]**

**Rule.** A server for 5.x and 6.x clients must know every token it allows, and must put each at or above `CLVER_2_14`, so that files carry the modtime and large files come in chunks. The lab got there by renaming one entry of the table to `G3D15010` (`G3D26090` in the v5 lab, `G3D14097` in the "Play v5 and v6 clients" lab, see `version-profiles/lab-v5-2026-10-30.md` and `v5v6-lab-play.md`). Either works for 5.24 because both slots are far above 2.14, but it takes the renamed build off the table (5.30–6.00r4 or 5.12). Adding the token as a new entry is the clean fix. **[srv][inf]**

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
