# Large-file thresholds on the focus builds

Date: 2026-11-16. Research-list rank **#10** (focus 1.39, 1.411, 2.220, 2.310, 4.208, 5.007, 5.120, 6.037). Consolidates existing notes; no new binary session or ~300 KB push in this pass.

Tags: **[bin]** client handlers; **[srv]** GServer-v2 / gs2lib version table; **[cap]** lab file saves; **[doc]** release notes; **[inf]** unread clients.

## Settled ladder (server reply shape)

The **reply layout and whether LARGEFILE\* are used** follow the **server's token → `versionID` table**, not a client-declared capability. An allowed but unknown token gets `CLVER_UNKNOWN` and the pre-2.1 path. **[srv]** (`file-transfer.md`)

| Era (server `versionID`) | Small `PLO_FILE` (102) | Files larger than ~64 KB | Chunk size |
|---|---|---|---|
| Before 2.1 | name + bytes, **no** modtime, no trailing `\n` | Server answers **30** `FILESENDFAILED` (no LARGEFILE\*) | n/a |
| 2.1 – 2.13 | `i5` modtime + name + bytes + `\n`, one piece | Still **no** LARGEFILE\*; over 64000 → 30 | n/a |
| ≥ 2.14 | same layout, split | **68** `LARGEFILESTART` / **84** `LARGEFILESIZE` / 102 chunks / **69** `LARGEFILEEND` | **32000** bytes |

Clients before 2.14 cannot receive files over 64000 bytes on a correct server table. **[srv]**

## Focus builds

| Focus | Token (typical) | On a correct gs2lib / Seihai table | Evidence |
|---|---|---|---|
| **1.39** | `GNW07080` | Pre-2.1 path: no modtime FILE; **no** large-file ids handled; client only asks **23** `WANTFILE` (never 34). | `versions-133-139.md` **[bin][lab]** |
| **1.41r1** | (gen-2 list era) | Still before 2.14: expect modtime/era rules of its server slot; **no** LARGEFILE\* on that client generation. Exact 1.41r1 FILE handler not re-read this pass. | **[inf]** from era ladder + `file-transfer.md` |
| **2.22** | `GNW03014` | ≥ 2.14: large_files true; 68/69 known; 32000-byte chunks. | `2.22-2.31.toml` **[bin]**; release note “files bigger than 64k” from 2.14 **[doc]** |
| **2.31** | `GNW28015` | Same as 2.22 plus **84** `LARGEFILESIZE` in the receive set. | `2.22-2.31.toml` **[bin]** |
| **4.208** | `G3D20126` | Above 2.14 on any current table that knows the token; Login also uses 23/47 for packages. | `v4x-clients.md`; `live-behaviour-404.md` **[bin][live]** |
| **5.007** | `G3D22067` | Stock gs2lib knows it (`CLVER_5_07`). Lab: 541 248-byte file as 68 → 84 → 102 chunks → 69; client saved byte-for-byte. | `file-transfer.md`; Seihai `v5v6-profiles.md` **[cap][bin]** |
| **5.120** | `G3D14097` | Known as `CLVER_5_12`. Same ≥2.14 large-file path when the table matches. | `file-transfer.md` **[src]** |
| **6.037** Win / Linux | `G3D0311C` / `G3D0511C` | Known as `CLVER_6_037` / `_LINUX`. Same ≥2.14 path; v5/v6 labs pulled large `pics1.png` once assets + table were correct. | `file-transfer.md`; `v5v6-lab-play.md` **[src][cap]** |

### Token-table trap (not a client threshold)

If the server **does not** know the login token, every focus 4.x–6.x build is treated as pre-2.1: no modtime, no LARGEFILE\*, and big files fail with 30. That is how stock gs2lib broke **5.24** (`G3D15010` missing) — fixed for labs by `gs2lib-CLVER_5_24.patch`. Focus **5.007 / 5.120 / 6.037** are already in the stock table; **4.208** must be listed the same way on any Seihai / fork table used in labs. **[srv][cap]**

## Client ask side (related, not the threshold)

| Pattern | Builds | Note |
|---|---|---|
| 23 `WANTFILE` when uncached | all focus eras | Per-server cache folders on 4.x+ (`updatepackages/<server>/`). |
| 47 `VERIFYWANTSEND` when that server's copy is cached | 4.x+, 5.00r7 lab | CRC + name; 5.00r7: 47 on Login, 23 after 178 when world cache empty. **[cap]** |
| 34 `UPDATEFILE` | from ~2.1 | 1.39 never sends it. **[bin]** |

## Open

- [ ] Exact per-exe `large_files` / `large_file_size` (or equivalent receive constants) on stock **4.208 / 5.007 / 5.12 / 6.037** — profile-audit cells that still say “inferred from 2.14” are **unverified on these binaries**, not false. **[inf]**
- [ ] Discriminating **~300 KB** image push on each focus build against seihai-gserver (confirm chunk boundaries and 84 handling on 2.22 vs 2.31).
- [ ] Static 1.41r1 FILE / LARGEFILE receive set (confirm no 68/69).
- [ ] Whether any focus client enforces a **stricter** on-disk limit than the server's 32000-byte chunks (none claimed today).
