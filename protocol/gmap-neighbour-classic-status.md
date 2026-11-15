# Gmap neighbour framing on classic-login 2.x (gap #14)

Date: 2026-11-16. Research-gaps / research-list rank **#14** (focus 2.220, 2.310; classic path also hits 2.17). Overlap: `[ASSIGNED: 2.22 gmap re-send on warp]` — run the open lab in the same session.

**Question:** Does GServer-v2’s classic path make 2.x copy neighbour boards onto the player’s own level? Does ending a neighbour reply with the cell’s level name keep `BOARDMODIFY` and chests working?

**Answer so far (static + one gen-5 capture):**

| Claim | Status | Evidence |
|---|---|---|
| Level data always lands on the level named by the **last `PLO_LEVELNAME` (6)** | **Settled** | `gmap-adjacent-level-target.md` **[bin]** 2.17.1 / 2.22 / 2.31 |
| Classic login → `PlayerClientOriginal` omits `LEVELNAME` on neighbour replies | **Settled** | same note **[srv]** |
| That omission overwrites the player’s own tiles with each neighbour | **Predicted** | **[srv][inf]** — not yet reproduced in a classic-login lab |
| Gen-5 login → `PlayerClient` frames every reply with the neighbour name | **Settled** | **[srv]**; 2.22 lab 2026-10-24 **[cap]** |
| Trailing `LEVELNAME` should be the **cell** level, not the `.gmap` name, on 2.17.1/2.22 | **Settled statically** | **[bin][inf]**; keeps named level for later `BOARDMODIFY` / chests |
| Stock overwrite + fixed framing on a 2×2 gmap | **Open** | E#13 “Settles it”; needs L |

Tags: **[bin][srv][cap][doc]** from the existing neighbour note and E#13. No new binary or lab in this pass.

## Sequence that works (static)

For each `PLI_ADJACENTLEVEL` (35):

```
PLO_LEVELNAME  <neighbour name as the client sent it>
… board / links / signs / chests / LEVELMODTIME when stale …
PLO_LEVELNAME  <player’s current cell level name>
```

Use `PLO_PLAYERWARP2` (49) for gmap entry on every client that handles it. Detail: [`gmap-adjacent-level-target.md`](gmap-adjacent-level-target.md).

## Still open

| Item | Status |
|---|---|
| 2.17.1 on stock classic path (expect overwrite) | **Open** L |
| 2.17.1 / 2.22 with cell-name trailing frame (expect correct neighbours + live `BOARDMODIFY`) | **Open** L |
| Seihai gserver-v2 / MIT gserver classic framing fix | **Open** after lab confirms |

## Lab next (same run as gmap re-send)

1. Loopback 2×2 gmap; 2.17.1 against stock `PlayerClientOriginal`, then against cell-name framing.
2. Same gmap with 2.22: confirm trailing cell name keeps chests/`BOARDMODIFY` on the standing level.
3. Fold any warp re-send observations into the assigned gmap-on-warp lead.
