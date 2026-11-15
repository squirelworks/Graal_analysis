# Update packages after login (gap #28)

Date: 2026-11-16. Research-gaps / research-list rank **#28** (focus 4.208, 5.x, 6.037). Overlap: `[ASSIGNED: GPAKE .enc loader]` — same package code path.

**Question:** What does `PLI_UPDATEPACKAGEREQUESTFILE` (159) send, what does the client do with a `.gupd` beyond `basepackage`, and what is the `PLI_VERIFYWANTSEND` (47) contract?

**Answer so far:**

| Piece | Status | Evidence |
|---|---|---|
| Cold start asks for `basepackage.gupd` with **WANTFILE 23** (often twice) | **Settled** | 4.04/4.20 live **[live]**; 5.x/6.x login captures **[cap]** |
| After a local copy exists, next run sends **47** with CRC-32 of the file | **Settled** (4.x lab) | `live-behaviour-404.md` **[live]** |
| Within one run, client keeps asking with 23 rather than switching to 47 | **Settled** (4.x lab) | same |
| Saves under `updatepackages/` (and per-server subfolder) | **Settled** (4.x) | same |
| Login `basepackage` / `login.gupd` contents on one observed Login server | **Settled for that capture** | `login-session-observed.md` **[cap]** — not a general contract |
| GServer-v2 `master` 159 layout: `c` name len, name, `c` install type (1/2), then one `i5` CRC per package file | **Settled as [srv]** | `gserver-v2-master-handlers.md` |
| Older manual 159 layout (“order, name, modtime”) | **Disputed** | both **[srv]**; client send site unread |
| Reply chain: `PLO_UPDATEPACKAGESIZE` (105) → differing files → `PLO_UPDATEPACKAGEDONE` (106) | **Settled as [srv]** (GServer-v2) | same |
| `PLO_UPDATEPACKAGEISUPDATED` (187) on RC file replace | **Settled as [srv]** | same |
| seihai-gserver: packages load; **159 not handled**; **47 = no** | **Settled as [doc]** | `PARITY.md` |
| Client-side 159 / 47 builders on 5.007 / 5.120 / 6.037 | **Open** | need S |
| Behaviour for non-`basepackage` `.gupd` on focus builds | **Open** | need L |

Tags: **[live][cap][srv][doc]**. No new binary session in this pass.

## Ids (hygiene)

| Id | Direction | Name | Layout known so far |
|---|---|---|---|
| 23 | C→S | WANTFILE | used for cold `basepackage.gupd` |
| 47 | C→S | `PLI_VERIFYWANTSEND` | `i5` CRC-32, `str` filename — “send if stale” **[srv]** packet-ids; 4.x lab confirms CRC use **[live]** |
| 159 | C→S | `PLI_UPDATEPACKAGEREQUESTFILE` | two **[srv]** readings disagree; client unread |
| 105 | S→C | `PLO_UPDATEPACKAGESIZE` | package name + total size of files to send **[srv]** |
| 106 | S→C | `PLO_UPDATEPACKAGEDONE` | package name **[srv]** |
| 187 | S→C | `PLO_UPDATEPACKAGEISUPDATED` | filename + `\n` **[srv]** |

## Still open (focus)

| Item | Status |
|---|---|
| S of 47 and 159 builders on 4.20r8 / 5.00r7 / 5.12 / 6.03r7 | **Open** |
| Settle which 159 layout the **client** writes | **Open** |
| L: non-base `.gupd` install / reinstall on a focus Windows build | **Open** |
| seihai-gserver handlers for 47 and 159 | **Open** (after layout) |

## Next steps

1. S: focus send wrappers for 47 and 159 (fold with GPAKE lead if the same module).
2. L: loopback Login + game with a second `.gupd` listed from `basepackage`.
3. Then implement seihai-gserver 47/159 beyond “no” / “partial”.
