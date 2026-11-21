# GR-V1.05: empty / transparent tiles on upper layers

Date: 2026-11-16. Tags: **[bin]** for stock 5.00r7 level I/O; **[inf]** where draw behaviour is unproven.

Extends [`gr-v105-500r7.md`](gr-v105-500r7.md) (intro build, GCHAR layer count, no pad after the count, writer rule). No on-disk multi-layer sample was decoded in this pass.

## Stock empty markers (5.00r7)

| Stage | Stock behaviour | Tag |
| --- | --- | --- |
| Fresh upper-layer construction | Layer 0 cells start at **0**; layers above 0 start at the all-ones 16-bit value (reads as **−1** when taken as signed) | [bin] |
| Save to disk | Values masked to 12 bits (`& 0xFFF`); an all-ones upper cell becomes on-disk **4095** | [bin] |
| Load from disk | Buffer receives **4095** (`0x0FFF`), not the fresh all-ones RAM value | [bin] |
| Tile get with a missing layer | Returns **−1** | [bin] |
| Equality skip `if (tile == 4095)` in the scanned text | **Not found** | [bin] |

So stock’s honest empty markers are **all-ones / −1 in fresh RAM** and **4095 on disk** after a round-trip. Treating 4095 as a special “map to an internal −2 sentinel on read” is **not** shown for stock. Visual blank may still come from tileset cell 4095 and/or a render loop not yet pinned. **[bin][inf]**

## Layout reminder (unchanged)

`GR-V1.05` = magic + GCHAR layer count + one 13-bit board per layer + the usual post-board body. There is **no** pad between the layer-count byte and the first board on the stock path. Optional `HEIGHTS` may still follow signs as in `1.04`. **[bin]** ([gr-v105-500r7.md](gr-v105-500r7.md))

## Sample hunt limits

Held corpus hunts for files that **start** with `GR-V1.05` remain empty so far. A start-only search is **not** a real negative once encrypted caches are in play: a level can sit deeper in a blob. Separately, held `GRESCR01` objects in a weblevels-style zip are **weapon / class scripts**, not level boards — do not treat them as encrypted levels awaiting packet-197 keys. **[file][inf]**

2026-11-18: the two Delteria backups (2002 and 2019) hold no `GR-V1.05` file either; the 2019 set has three multi-layer `GLEVNW01` levels instead. See [`hubserver-037-and-delteria-2026-11-18.md`](../server-notes/hubserver-037-and-delteria-2026-11-18.md#level-formats-no-gr-v105-sample). **[file]**

## Still open

- [x] ~~Pin any render-loop skip (or tileset blank) for disk value 4095 on layers above 0.~~ On the wire 4095 draws as tileset cell 4095 and `0xFFFF` draws as empty; see [`gr-v105-fuzz-2026-11-19.md`](gr-v105-fuzz-2026-11-19.md). **[lab]**
- [ ] Decode one real on-disk `GR-V1.05` sample when held. **[file]**
- [ ] Live serve of a multi-layer file to **5.12** / **6.03r7**. The 2026-11-19 attempt used a lab build with a four-byte skew. The source repair has since landed, but a correctly served level remains unmeasured here; see the [source reconciliation](gr-v105-fuzz-2026-11-19.md#source-repair-reconciled-on-2026-11-21-srv). **[lab][srv]**
