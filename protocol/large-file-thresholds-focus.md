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
| **1.41r1** | `GNW13110`, generation 3 | The recorded patched input's direct switch has 45 cases (0–41, 43, 75, 100), without 68/69. The exact raw/file subpath remains unread here; direct-case absence does not establish FILE absence or its body. | [Exact-input scope](file-profile-evidence-2026-11-21.md#the-recorded-141r1-input) **[bin]** |
| **2.22** | `GNW03014` | 68/69 receive cases are recorded; 32000-byte chunks describe the server sender. | `2.22-2.31.toml` **[bin]** for cases; `file-transfer.md` **[srv]** for chunks; 2.14 release note **[doc]** |
| **2.31** | `GNW28015` | Same as 2.22 plus **84** `LARGEFILESIZE` in the receive set. | `2.22-2.31.toml` **[bin]** |
| **4.208** | `G3D20126` | Above 2.14 on any current table that knows the token; Login also uses 23/47 for packages. | `v4x-clients.md`; `live-behaviour-404.md` **[bin][live]** |
| **5.007** | `G3D22067` | Stock gs2lib knows it (`CLVER_5_07`). Lab: 541 248-byte file as 68 → 84 → 102 chunks → 69; client saved byte-for-byte. | `file-transfer.md`; Seihai `v5v6-profiles.md` **[cap][bin]** |
| **5.120** | `G3D14097` | Known as `CLVER_5_12`. Same ≥2.14 large-file path when the table matches. | `file-transfer.md` **[src]** |
| **6.037** Win / Linux | `G3D0311C` / `G3D0511C` | Known as `CLVER_6_037` / `_LINUX`. Same ≥2.14 path; v5/v6 labs pulled large `pics1.png` once assets + table were correct. | `file-transfer.md`; `v5v6-lab-play.md` **[src][cap]** |

### Token-table trap (not a client threshold)

If the server **does not** know the login token, every focus 4.x–6.x build is treated as pre-2.1: no modtime, no LARGEFILE\*, and big files fail with 30. That is how stock gs2lib broke **5.24** (`G3D15010` missing) — fixed for labs by `gs2lib-CLVER_5_24.patch`. Focus **5.007 / 5.120 / 6.037** are already in the stock table; **4.208** must be listed the same way on any Seihai / fork table used in labs. **[srv][cap]**

## Receive handlers on 4.208 to 6.037 (G262, 2026-11-25)

Static read of the stock engines (capstone/pefile, nothing run). Files: 4.20r8 unhooked `GraalEngine.dll` from the unpacked set (sha256 `828e9311…`); 5.00r7 stock engine (`dde0fc85…`); 5.12 memory image of the engine (`ac01cd79…`; the shipped `04f7a133` engine was not on hand); 6.03r7 third-party unpack of `Graal 6.0.3.7.exe` (`2be6bf4b…`). **[bin]**

| Build | 68 `LARGEFILESTART` | 84 `LARGEFILESIZE` | 69 `LARGEFILEEND` | Receive-side size limit |
|---|---|---|---|---|
| 4.208 | handled | handled | handled | none |
| 5.007 | handled | handled | handled | none |
| 5.12 | handled | handled | handled | none |
| 6.037 | handled | handled | handled | none |

The switch takes the already-decoded id (no extra bias); 100 (`RAWDATA`) and 108 are tested before it. 30, 45 and 102 are switch cases in all four.

The handlers have the same shape in every build:

- **68** stores the current large-file name, zeroes the expected size and resets any buffer already held under that name.
- **84** reads a 5-byte encoded number into the expected-size global (0 if the payload is shorter than 5 bytes). No bounds check.
- **102** appends each chunk. The expected size is only the total passed to `onFileChunkReceived` and the progress ratio.
- **69** clears the name if it matches, logs `File download: … (size: N) done` using the bytes actually received, fires `onFileDownloaded`, saves the file and frees the buffer. It never compares the received length with the 84 value.

**No receive-side size constant.** Every `32000` (`0x7d00`) in these engines is the RC upload chunker (sending 155), the `GetLogicalDriveStringsA` buffer (5.x/6.x) or FreeType. The only ceilings are the encodings: 32 bits for the 84 value and 2 097 151 bytes per raw (100) packet. Not traced: the string-append growth and the socket raw-data reader, so an allocation cap there is not ruled out.

Consequence for profiles: `large_files = true` and `large_file_size = true` on 4.208, 5.007, 5.12 and 6.037 are now **[bin]**, not inferred from 2.14. 32000-byte chunks remain a server choice.

## Client ask side (related, not the threshold)

| Pattern | Builds | Note |
|---|---|---|
| 23 `WANTFILE` when uncached | all focus eras | Per-server cache folders on 4.x+ (`updatepackages/<server>/`). |
| 47 `VERIFYWANTSEND` when that server's copy is cached | 4.x+, 5.00r7 lab | CRC + name; 5.00r7: 47 on Login, 23 after 178 when world cache empty. **[cap]** |
| 34 `UPDATEFILE` | from ~2.1 | 1.39 never sends it. **[bin]** |

## Open

- [x] ~~Exact per-exe `large_files` / `large_file_size` on stock 4.208 / 5.007 / 5.12 / 6.037.~~ [Read 2026-11-25](#receive-handlers-on-4208-to-6037-g262-2026-11-25): all four handle 68, 69 and 84; no receive-side size limit. **[bin]**
- [ ] Discriminating **~300 KB** image push on each focus build against seihai-gserver (confirm chunk boundaries and 84 handling on 2.22 vs 2.31).
- [x] ~~Reconcile the recorded 1.41r1 direct receive set: no 68/69.~~ [Exact-input scope](file-profile-evidence-2026-11-21.md#the-recorded-141r1-input).
- [ ] Read the exact 1.41r1 raw/file subpath and FILE body; G264 remains partial.
- [ ] Whether any focus client enforces a **stricter** on-disk limit than the server's 32000-byte chunks (none claimed today).
