# 2.22 login default-file checks (full vs near-empty)

Date: 2026-11-16. Research-gaps / research-list rank **#32** (focus 2.220). Closes the *status* half of Graal_analysis#245’s login-default row; the remaining “full set after answers” lab is still open.

**Question:** which files are checked with a full versus an empty data folder?

**Answer so far (lab 2026-11-14, #245 §4):**

Tags: **[lab]** Wine 2.22 loopback; **[doc]** cross-link. No new session in this pass.

## Minimum folder to reach the server list

Near-empty install, files added until Online worked:

`Graal.exe`, `bass.dll`, `basswma.dll`, `hvdi.dll`, `arrays2.sig`, `arrays2.dat`, `graal.sig`, `arrays.dat`, `pics1.png`.

The client then writes `graalconfig.txt`, `servermessage.html`, and `weblevels\` itself. Login-screen art is inside the exe.

## Wire checks in the second C→S frame

Both folder states put **all first file checks in the client’s second C→S frame**, with the first player-props line (id 2), ~0.3 s after login (one zlib type-4 frame):

| Folder | Besides props |
|---|---|
| Near-empty | id **23** `WANTFILE`: `idle.gani`, `plisticononline.png`, `plisticonaway.png`, `plisticondnd.png` |
| Full | id **34** `UPDATEFILE` (with 5-byte modtime): `plisticoneating.png`, `plisticonhiding.png`, `plisticonno pms.png`, `plisticonrping.png`; plus id **23** `steps.wav`, `lab_u7_time.gani` |

- **23** = missing locally; **34** = has a local copy (modtime check).
- Player-list icons follow the server’s status list (S→C **180**). Near-empty asked for Online/Away/DND; full skipped those (already present) and checked later statuses.
- That lab’s gserver **answered none** of the 23/34 requests, so the client never asked for sword/shield/body/etc. A prior harness whose server *did* answer saw further frames (sword, shield, body, bomb, bow, then `head25`, `steps.wav`). So the table above is **“what goes out before any answer”**, not the complete post-answer set.

## Still open

| Item | Status |
|---|---|
| Shared second-frame bundling with props | **Settled** **[lab]** |
| Near-empty vs full first-wave difference | **Settled** **[lab]** |
| Full set after the server answers 23/34 | **Open** — rerun on seihai-gserver / answering harness |
| Truly empty folder (no DLLs) | N/A — Wine cannot load the exe without the bass/hvdi imports |

Detail and log names: `live-runs/open-issues-2026-11-14/README.md` §4.
