# Ids sent by 5.12; 2.31 id-44 disagreement — status

Date: 2026-11-16. Research-list rank **#17**. Consolidates E#4 / profile rows; **no new send-wrapper walk or throw capture**.

Reconciled 2026-11-22 against the already published November 20 throw lab; no new execution.

Tags: **[bin]** send floors; **[cap]** partial 5.12 / 2.31 labs; **[inf]** open disagreements.

## 5.12 client→server send floor

| Source | What it lists | Limits |
|---|---|---|
| Genuine 5.12 **S→C** handled set | Identical to 5.00r7 (100 ids incl. 132/133/193/197) | [`v5v6-windows-unpacked.md`](v5v6-windows-unpacked.md) **[bin]** — receive side |
| Original 5.00r7 send-wrapper scan (connection) | Scan omitted **11**; combined floor now includes the separately traced throw path. Includes **44** as process-list reply | [`v5x-clients.md`](v5x-clients.md#client--server-ids-500r7) **[bin]** |
| 5.00r7 throw path (backup engine) | **Does** send **11** (`PLI_THROWCARRIED`) empty body — wrapper list missed it | E#4 static resolution; [`windows-404r2-500r7-static-2026-11-09.md`](../client-internals/windows-404r2-500r7-static-2026-11-09.md) **[bin]** |
| Unchanged 5.00r7 throw lab | Empty-body **11** on both completed throws; separate from the backup-engine static input | [`November 20 lab`](lab-appe-hostb-2026-11-20.md#throw-id-on-500r7-e4) **[lab]** |
| Profile `5.00-6.03.toml` 5.12 row | Cap-only sample: `1, 2, 11, 23, 24, 34, 37, 38, 44, 47, 157` — **send code not read** | `pli_sent_src = "cap only"` **[cap]** |

**Status for #17 (5.12 half):** treat the **5.00r7 floor + id 11** as the best proxy until a genuine **5.12 `Graal3DEngine.dll` send-wrapper pass** lands. Cap sample proves 5.12 can emit 11 and 44 on the wire; it is not a complete set. Do not use the “5.12 untouched” tree (it is 5.00r7 — F01 / #53).

## 2.31 “id 44” — two different messages

| Direction | Id 44 | 2.22 | 2.31 | Verdict |
|---|---|---|---|---|
| **S→C** | `HASNPCSERVER` | handled | **dropped** (adds 84, 189) | **Settled** [`2.22-2.31.md`](../version-profiles/2.22-2.31.md) **[bin]** |
| **C→S** | process-list reply to S→C 182 | sent | still sent (lab answered process-list) | **Settled** as still present **[bin][cap]** |

There is no remaining “does 2.31 send 44?” disagreement once S→C vs C→S are separated. Profile `pli_sent` for 2.31 still lists C→S 44.

## Still open

- [ ] Full **5.12** send-wrapper / variable-send floor on genuine engine (**S**).
- [x] ~~Wire-confirm id 11 on a 5.00r7 throw.~~ The published November 20 lab records two throws; this does not supply a controlled 5.12 throw comparison.
- [ ] A controlled **5.12 throw capture** tying id 11 to the throw action; its existing partial capture sample is not that comparison.
- [x] ~~Align `v5x-clients.md` wrapper-list text with the separately traced throw path.~~ The original scan and combined floor are now distinguished, with the later lab cited separately.
