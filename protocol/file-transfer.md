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
