# GR-V1.05 from the stock 5.00r7 web-level cache (lab)

Date: 2026-11-16

Loopback lab only. Synthetic multi-layer text levels; stock Windows **5.00r7**
wrote the ordinary web-level cache entries; the GR-V bodies inside those entries
were decoded against the static layout in [`gr-v105-500r7.md`](gr-v105-500r7.md).
Aggregates and layout only. No cache ciphertext, key material, or decrypt steps.
Tags: **[lab]**.

## Method (short)

| Piece | What was used |
|---|---|
| Client | Stock Windows **5.00r7** (repro label `G3D22067`), staged 2.22-era starter tiles |
| Server | Loopback lab game server that delivers upper board layers on the wire (layer index > 0) |
| Save path | Route B: the client's own web-level cache after guest reconnects into each start level |
| Editor route | Not used this pass |
| Samples | Five synthetic 64×64 `GLEVNW01` levels (L1 control; L2–L5 multi-layer paints) |

Saved cache files stay off-repo. Placeholder path shape only:
`weblevels/<host>/<level>-<port>.code`.

## What the cache bodies held

| Sample | Magic | GCHAR count byte | Layer count | Notes |
|---|---|---|---|---|
| L1 | `GR-V1.03` | — | 1 | Control: layer 0 only; painted cells and runs decoded as expected |
| L2 | `GR-V1.05` | `0x22` | 2 | Layer 1 mostly tile **4095**; distinct painted cells present |
| L3 | `GR-V1.05` | `0x22` | 2 | Same board shape as L2; **no** `HEIGHTS`…`HEIGHTSEND` in the cache body |
| L4 | `GR-V1.05` | `0x23` | 3 | Layer 2 present and all **4095** |
| L5 | `GR-V1.05` | `0x22` | 2 | One layer-1 cell painted explicitly as **4095** (same numeric value as untouched) |

Forcing a four-byte pad after the count on L2 made the board decode fail
(`board ended early`). There is **no** pad between the count byte and board 0,
and no gap between consecutive boards beyond the packed bitstreams. **[lab]**

L1→L2 body delta matches the static expectation: magic change, the count byte,
and one extra board. Links were present; baddy / NPC / chest markers were empty
terminators. Signs authored in the text source did not appear in these cache
bodies (same “links yes, signs sometimes empty” pattern already noted for the
web-level writer). **[lab]**

## Answers (Q1–Q6)

| # | Result | Tag |
|---|---|---|
| Q1 | Matches the static layout: `GR-V1.05` + GCHAR count + N × 13-bit boards + 1.04-style body; **no pad** | **[lab]** |
| Q2 | Untouched upper-layer cells are **4095** (L2 layer 1: thousands of 4095 cells plus the painted patch) | **[lab]** |
| Q3 | **Inconclusive on this Route B path.** The L3 text source carried `HEIGHTS` / `HEIGHTSEND`, but the cached `1.05` body had **no** heights block. That does not prove `1.05` cannot carry heights; it only shows this server→cache path did not round-trip them | **[lab]** |
| Q4 | Writer count is **2** (`0x22`) for two live layers and **3** (`0x23`) when a third all-4095 layer is present | **[lab]** |
| Q5 | Stock **5.00r7** web-level cache **does** write `GR-V1.05` when live layers > 1 | **[lab]** |
| Q6 | Screenshots were not available this pass. From the cache alone, an explicit tile **4095** equals an untouched **4095**, so draw difference is unsettled | **[lab]** |

## Limits

- One client build, one Route B session, synthetic levels only. No claim about
  wild server-shipped binary `1.05` files.
- Heights round-trip and on-screen draw of tile 4095 remain open.
- Outer `.code` wrapper details for this Windows 5.00r7 path are out of scope
  here (separate work; not published in this note).
