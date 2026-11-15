# First-load warp into a non-local level (gap #15)

Date: 2026-11-16. Research-gaps / research-list rank **#15** (focus: all; labs named 2.22 and 6.03r7). Pointers: seihai-core#7 / seihai#224; difftest leftovers.

**Question:** What goes on the wire when a link targets a level the client doesn’t hold?

**Answer so far (adjacent evidence only — dedicated link lab still open):**

| Piece | Status | Evidence |
|---|---|---|
| Gmap warp 49 without `.gmap` on disk → loading hang (no `LEVELNAMES`) | **Settled** | `gmap-file-on-warp.md` **[bin]** |
| Client WANTFILE for missing gmap; seihai-gserver does not push `.gmap` before 49 | **Settled** | same **[srv][bin]** |
| Whether a later WANTFILE answer alone finishes a hung 49 | **Open** | same note **[lab]** |
| Ordinary door/edge link into a **`.nw` level not on disk** (non-gmap) | **Open** | seihai-core#7 — needs L with proxy |
| 6.03r7 same path | **Open** | named in gap method; no capture filed here |

Tags: **[bin][srv][doc]**. No new proxy lab in this pass.

## Expected wire sketch (hypothesis — not lab-proven for plain `.nw`)

1. Client follows the link / receives warp naming a level it lacks.
2. Client requests the level (and any art) via WANTFILE / related ids.
3. Server answers with file bytes or FILESENDFAILED; level framing (`LEVELNAME`, board, …) must arrive in an order the client accepts.
4. Until the level object exists, boards/links may be dropped (named-level rule in `gmap-adjacent-level-target.md`).

Confirm or replace with a 2.22 + 6.03r7 loopback decode of a door into a deliberately absent level.

## Still open

| Item | Status |
|---|---|
| Full C→S / S→C sequence for non-local `.nw` on 2.22 | **Open** L |
| Same on 6.03r7 | **Open** L |
| Difftest gmap-login bundling leftovers vs this path | **Open** (fold after lab) |
