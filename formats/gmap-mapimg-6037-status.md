# 6.037 gmap reader: `MAPIMG` vs `MINIMAPIMG` — status

Date: 2026-11-16. Research-list rank **#57** (focus 6.037 Win). Inventory of published reader key lists; **no Win 6.03r7 binary session** this pass (Share not mounted).

Tags: **[bin]** older clients’ key tables; **[srv]/[doc]** format keys; **[inf]** 6.037 claim unconfirmed.

## Question

Does the **client** gmap (`GRMAP001`) parser on Windows **6.03r7** omit `MAPIMG` and only honour `MINIMAPIMG`, while format / GServer notes still list `MAPIMG` as the overview image?

## Settled elsewhere (not 6.037)

| Claim | Status | Evidence |
|---|---|---|
| Format / server key table includes both `MAPIMG` and `MINIMAPIMG` | **Settled** | [`gmap.md`](gmap.md); manual §3.2 **[srv][doc]** |
| 2.05 dormant reader knows `MAPIMG` (among generator keys); no caller found | **Settled** | `gmap.md` **[2.05]** |
| 2.22 / 2.31 / **3.x** client reader key lists name **`MINIMAPIMG`** and do **not** list `MAPIMG` | **Settled** for those eras | [`v3x-clients.md`](../protocol/v3x-clients.md) (“same keys as the 2.22/2.31 Windows clients”) **[bin]** |
| 5.x / 6.x notes say `GRMAP001` “as in 3.x” without re-walking the key table | **Documented, not a 6.037 proof** | [`v5x-clients.md`](../protocol/v5x-clients.md); [`v6x-clients.md`](../protocol/v6x-clients.md) **[bin]** summary only |

So: a **3.x-era omission of `MAPIMG` on the client** is already in our notes. That is **lead** for #57, not confirmation that Win 6.03r7 matches it.

## Still open for #57

| Question | Next |
|---|---|
| Win **6.03r7** (`G3D0311C`) gmap key table / string compare: `MAPIMG` present? | **S** on Share/Claude Win unpack |
| Linux 6.03r7 (`G3D0511C`) same or different | Optional **S** sibling |
| Live: gmap with only `MAPIMG` vs only `MINIMAPIMG` | **L** after #1 assets |

Until that **S** lands, do **not** edit `formats/gmap.md` to drop `MAPIMG` — it remains correct for servers / writers / older dormant readers.

## Checklist

- [ ] Static key table on Win 6.03r7 (and optionally Linux twin).
- [ ] One-sentence update in `gmap.md` **only if** the client omit is confirmed.
- [ ] Fixture lab with assets if static is ambiguous.
