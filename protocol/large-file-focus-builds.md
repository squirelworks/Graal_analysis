# Large-file path for focus builds 4.208–6.037

Date: 2026-11-16. Research-gaps / research-list rank **#10** (focus 4.208, 5.007, 5.120, 6.037).

**Question:** what is the real size limit and large-file path (`large_files`, `large_file_size`) for each focus build?

**Answer so far:** on the **server token table**, every known token for these builds sits **above** the 2.14 cut, so a correctly recognised client gets the **≥ 2.14** file layout (modtime + `LARGEFILE*` chunking). Exact **per-build client** thresholds in the profile audit remain **inferred / unread** until stock binaries are re-read. The old “5.12 black level” case was a **wrong / unknown token** (pre-2.1 path, 64 KB refusal), not proof that 5.12 lacks large files.

Tags: **[src]** gs2lib version table; **[srv]** GServer file branches; **[cap]** 5.24r4 large `pics1.png` after token fix; **[doc]** cross-links. No new binary session in this pass.

## Era cuts (server behaviour)

From `protocol/file-transfer.md` **[srv]**:

| Client rank (from login token) | File reply |
|---|---|
| Below 2.1 | `PLO_FILE` without modtime; up-to-date often as id 30; no large-file ids |
| 2.1 – 2.13 | modtime + name + bytes; files over **64000** bytes → `FILESENDFAILED` (30) |
| ≥ 2.14 | modtime path; files over **32000** bytes use `LARGEFILESTART` / `LARGEFILESIZE` / `LARGEFILEEND` (68 / 84 / 69) |

Clients before 2.14 cannot receive files over 64000 bytes. **[srv]**

## Focus-build tokens vs that cut

gs2lib’s `clientVersions[]` places these focus tokens **above** `CLVER_2_14` when present (`file-transfer.md` table) **[src]**:

| Focus | Example token(s) | Rank vs 2.14 |
|---|---|---|
| 4.208 | 4.x `G3D…` slots used in labs | Above (when in table) |
| 5.007 | `G3D22067` (`CLVER_5_07`) | Above |
| 5.120 | `G3D14097` (`CLVER_5_12`) | Above |
| 6.037 | `G3D0311C` / `G3D0511C` | Above |

**Rule:** a server that **knows** the token serves the large-file path. A token allowed but **missing** from the table becomes `CLVER_UNKNOWN` (0) and gets the pre-2.1 / sub-2.14 refusal path — including the 5.24 “PNG as file name” / black-level lab case when `pics1.png` (~210 KB) was refused. **[cap][src]**

## What is still open (profile audit)

| Row | Status |
|---|---|
| Server-side cut for recognised 4.x–6.x tokens | **Settled** for “has large-file path” **[src][srv]** |
| Exact `large_files` / `large_file_size` values per focus **client** binary | **Open** (S on stock 4.20r8 / 5.00r7 / 5.12 / 6.03r7 receive handlers) |
| Live 300 KB image receive on each focus build against seihai-gserver | **Open** (L; needs assets + correct token) |

Do not treat “inferred from 2.3 / 2.14” profile cells as false — treat them as **unverified on these exes**. The era rule above is the floor until that S/L lands.
