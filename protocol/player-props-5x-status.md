# Player-prop parsers on 5.00r7 / 5.12 — status

Date: 2026-11-16. Research-list rank **#6** (focus 5.007, 5.120). Points at the completed case-set read; **no new jump-table pass or two-client prop lab** this pass.

Tags: **[bin]** case sets and the selected reader extent below; **[inf]** complete value-width and pyreborn leads still open.

## Settled (case sets)

Canonical note: [`v5-props.md`](v5-props.md) (2026-11-13 static).

| Stream | 5.00r7 / 5.12 (same as 5.30r3 / 5.31r4) | vs 4.x |
|---|---|---|
| self (PLO 9) | 0–32, 34–49, 52, 54–74, 78–**82**; skip-unknown as one byte | **+82** only |
| other (PLO 8) | 0, 2, 8–13, 15–21, 23, 24, 30–76, 78–**82**; unknown ends stream | **+82** only |
| NPC (PLO 3) | 0–47, 53–77 | unchanged from late 4.x set in that note |
| baddy (PLO 2) | 0–10 | unchanged |

- **82** on other players: one length byte (−32) then that many bytes → string on the player; self hands 82 to the other-player parser. Server name `COMMUNITYNAME` is **[srv]**; the string read is **[bin]**.
- **77** still not parsed in 5.x (ends other-player stream; one-byte skip in self).
- 6.x native parsers and the 6.1.1.3 `tclient_set*props` bridge are in the same note / [`v6-props.md`](v6-props.md) — out of #6’s focus but adjacent.

Identity reminder: a folder labelled “5.12 untouched” is **5.00r7** re-versioned ([`launchers-420r8-500r7-512.md`](../client-internals/launchers-420r8-500r7-512.md)). Genuine 5.12 engine is `Graal3DEngine.dll`. **[bin]**

## Selected appearance-reader extents (2026-11-22)

A retained archive-labelled 5.00r7 backup input gives a bounded sword/shield consumption result (evidence `W500-APPEARANCE-READERS-20261122`). The label is not authenticated stock/vendor provenance or runtime identity, and this input does not establish the genuine 5.12 reader. **[bin]**

For these two properties, the selected shared reader uses one value byte when its unsigned byte minus 32 is below 10. Otherwise its nominal value extent is two bytes plus the nonnegative declared image length: the first value byte, a length byte and the image bytes. The length is the unsigned length byte minus 32, clamped at zero for this cursor calculation. These extents exclude the property ID. The own-player parser independently calculates the same nominal extent before forwarding the selected property prefix to shared application; the top-level self and other parsers are not identical. **[bin]**

The image substring helper bounds the selected image slice by available text. This is distinct from the declared cursor advancement: the selected outer guards do not prove that the entire extended value is present, strict truncation rejection or safe arbitrary-byte consumption. Compact preset-image cases cover sword 1–4 and shield 1–3, but being below the reader discriminator alone does not establish semantic power. That discriminator is not interchangeable with a historical sender's bias. **[bin]**

This is a selected static extent, not the complete self/other width table, P6 semantic resolution, rendering/healing behavior or a runtime alignment result. Other properties, other specimens and genuine 5.12 remain open. **[bin][inf]**

## Still open for #6

| Question | Why | Next |
|---|---|---|
| Per-id **value widths** beyond the ids named in `v5-props.md` | Needed for safe encode / fuzz-free lab fixtures | **S** width table on 5.00r7 + 5.12 engines |
| Two-client prop **diff** on the wire | Confirms other-player accept set live | **L** after #1 assets |
| Pyreborn leads **P4** COLORS 5↔8 via PLO 177; **P5** ascending-id stop; **P6** sword/shield bias | Leads only until our **S** | Same static pass as widths |

## Open checklist

- [ ] Publish a 5.00r7 / 5.12 per-id width table (self + other).
- [ ] Confirm or reject P4–P6 against that table / two-client capture.
- [ ] Optional: unknown own-id long-value desync lab (called out in `v5-props.md`).
