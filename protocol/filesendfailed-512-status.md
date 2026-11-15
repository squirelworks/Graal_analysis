# Missing-file replies on 5.12 (`PLO_FILESENDFAILED` 30) — gap #37

Date: 2026-11-16. Research-gaps / research-list rank **#37** (focus 5.120). Gap pointer: graal-client-repro#304 / seihai-gserver-v2 #61.

**Question:** Does each missing image get exactly one `PLO_FILESENDFAILED` (30), and how does the client react?

**Answer so far:**

| Claim | Status | Evidence |
|---|---|---|
| Layout of 30 is `rest` = filename | **Settled** | packet-ids / file-transfer **[srv][bin]** |
| 2.05r2: 30 installs an **empty** in-memory file, releases request lists, settles the name | **Settled** | `plo-24-29-30-45-205r2.md` **[bin]** |
| 5.x/6.x black-screen lab: every missing art request got a **30**, and `game_console.log` listed each as “not found” | **Settled for that session** | `v5v6-expiry-and-black-screen.md` **[lab]** — not a per-image uniqueness proof |
| Exactly **one** 30 per missing image (no duplicates / no retries after settle) | **Open for 5.12** | need L with a counting decode |
| 5.12-specific empty-file / image reaction after 30 | **Open** | only 2.05r2 file-received path was traced; 5.12 S unread |

Tags: **[bin][lab][doc]**. No new 5.12 session in this pass.

## What is settled enough for Seihai

- Answering WANTFILE / UPDATEFILE with **30 + name** is the right “missing” path for classic and modern clients that handle 30.
- After 30, 2.05r2 will **not re-ask** that name in the same session (settled list). Treat that as the working hypothesis for 5.12 until L proves otherwise.
- A world that answers 30 for `pics1.png` (and other base art) yields a black screen on 5.x/6.x — serve the files (or LARGEFILE) instead.

## Still open

| Item | Status |
|---|---|
| Count: one 30 per distinct missing name on 5.12 | **Open** L |
| Whether 5.12 re-asks after 30 if the name leaves the settled list | **Open** L |
| Empty PNG/gani behaviour on 5.12 after 30 | **Open** S then L |
| seihai-gserver-v2 #61 acceptance | **Open** until the count lab |

## Lab next

1. Loopback 5.12, cold cache, world missing a fixed set of images; decode every 23/34 and every 30.
2. Confirm no second 30 for the same name after settle; note console lines.
3. Optional: S of 5.12 engine “file received” for empty bodies.
