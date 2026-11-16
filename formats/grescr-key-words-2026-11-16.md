# GRESCR01 key words: unpack, top digit, and weak-DES sample

Date: 2026-11-16. Tags: **[cap]** for held cache descriptors; **[bin]** for stock client accept path.

Leads-only. **No live script keys in this note.** Counts and structure only.

## Unpack (closed for GRESCR01 / 197)

On the held 6.113-era login-weapon capture family (CRC-matched caches; same family as [gs2-official-bytecode-6113.md](../protocol/gs2-official-bytecode-6113.md)):

- Packet **197** / `GRESCR01` carries two **GINT5** key words.
- Those words unpack little-endian into eight raw key bytes.
- Stock / lab DES then **bit-reverses each byte** (same family as classic gpak / 2.05 password DES) before ECB decrypt.
- CRC32 covers the **encrypted** body after the magic.

Decrypt matched the held cached weapons under that rule. **[cap]** ([gs2-official-bytecode-6113.md](../protocol/gs2-official-bytecode-6113.md); [gwebl001-cache.md](gwebl001-cache.md))

## Top digit

Both GINT5 words stay within a **32-bit** value: the top digit is masked to four bits (≤ 15). Re-check on the held non-placeholder key words found **0** violations. **[cap]**

## Weak / semi-weak DES — sample, not a mint proof

| Check | Result | Tag |
| --- | --- | --- |
| Keys per script (enlarged private pass) | **One** | [cap] |
| Distinct keys in that pass | **756** | [cap] |
| Match published weak or semi-weak 8-byte patterns (raw or after per-byte bit-reverse) | **0** | [cap] |

Absence of weak keys in a clean sample is **expected** even without a reject loop (only a handful of published weak/semi-weak patterns; random 8-byte collision chance is tiny). It does **not** prove the official server re-rolls weak keys when minting. **[cap][inf]**

## Stock client receive path

Stock **5.00r7** engine strings/imports show **no** weak-key / semi-weak-key reject helpers on the GRESCR accept/decrypt path. Clients decrypt with the key they are given; they do not advertise a mint-style reject loop on receive. **[bin]**

Whether the **official server** avoids weak keys when generating the two GINT5 words remains open (needs a static mint read or a controlled probe — not done; no keys stored here). **[inf]**

## PLO 104

File-key unpack for packet **104** was not seen in the held capture for this pass. **[cap]**

## Still open

- Official server key mint: reject/re-roll of weak or semi-weak keys. **[bin]**
- Confirm the same unpack for PLO **104** once a frame is held. **[cap]**
