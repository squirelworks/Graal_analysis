# v7 vs 6.11 connector id tables: settled model vs unread pair lists (G332)

Date: 2026-11-24. Tags: **[doc][lab]** prior connector and 6.111 live-table notes ·
**[bin]** held Worlds engine remapper / method surface already published ·
**[inf]** what a decrypted 7.x reply would still need to settle.

This is the next Crypto board item (**G332** / `v611-id-tables.md` Open): whether
the production **7.x connector scripts** load the **same** packet-id tables the
Mac 6.111 lab run published. No hosts, keys, `?p=` blobs, reply bodies, addresses
or digests appear here. No public-service fetch, no conf.gs fuzz, and no
decompiler dumps were run.

## Short answer (honest partial)

**The install model matches.** 7.x still fills the remappers through
`setoutdatahandlers` / `setindatahandlers` with the same sentinels and the same
PLI `onSend*` slot names (0…56) as 6.11. **The production pair lists are not
read.** Comparing those lists to the 6.111 tables in `v611-id-tables.md` still
needs a 7.x reply decrypted for its own launch. Stock decrypt stays **blocked**
by the trust-anchor **NO-GO** (**G156**) plus the open G028 residuals (payload
cipher / plaintext / `?p=` DES key). Those residuals were **not** re-chased here.
**[inf]**

## Settled without a decrypted 7.x script

| Question | Settled finding | Evidence |
| --- | --- | --- |
| Same remapper **API**? | Yes: script loads outgoing 256-dword table and incoming `(wire id, handler)` pairs | `connector-script.md` section 5; `v7-graal3d-pli-plo-tables.md` Model **[bin][doc]** |
| Same inbound **sentinels**? | Yes: `< 0x5F` native (95 slots), `0xFC` / `0xFD` specials, `0xFE` script, `0xFF` ignore | `v7-graal3d-framing-and-packet-tables.md` section 3; `v7-graal3d-pli-plo-tables.md` **[bin]** |
| Same PLI **slot names**? | Yes: decrypted 7.x `onSend*` names match the 6.11 slot table 0…56 one for one | `v7-graal3d-pli-plo-tables.md` section 1; `connector-script.md` section 7a **[bin][doc]** |
| Same inbound **name family**? | Yes: 7.x recovers the `tclient_*` set (same family as 6.11); wire id → slot still script-only | `v7-graal3d-pli-plo-tables.md` sections 2–3 **[bin]** |
| 6.11 live tables known? | Yes: Mac 6.111 lab run published both 256-entry tables (new-protocol incoming set in use) | `v611-id-tables.md` **[lab]** |
| Can 7.x reuse capture-replay? | **No.** Per-launch `?p=` makes a captured reply fail on the next launch | `connector-script.md` section 7a; `v7-connector-live-20261111.md` **[lab]** |
| Stock decrypt avenue? | **Closed:** trust-anchor swap is a **NO-GO**; payload key unrecovered | `v7-connector-trust-anchor.md` (G156); `v7-connector-payload-cipher.md` (G028) **[bin][lab][inf]** |

The moderate best guess from App. E#616 still stands as a **guess only**: once
decrypted, the script likely still installs id tables in the 6.11 structure. That
is **not** a byte-for-byte (or pair-for-pair) comparison to the published 6.111
lists. **[inf]**

## Still open (needs a decrypt the stock path cannot provide)

| Artifact | 6.11 known | 7.x production script |
| --- | --- | --- |
| **Outgoing** internal-slot → wire id list | Full 58 mapped slots (+ −1 empties) from Mac 6.111 **[lab]** | **Uncompared.** Engine has the loader; the list the reply passes is unread |
| **Incoming** wire id → handler pairs (new-protocol set) | 96 pairs, including 252/253 and dropping wire 100 **[lab]** | **Uncompared.** Same |
| Old- vs new-protocol choice | Two installs; live table matches new-protocol set **[lab]** | **Uncompared.** Whether 7.x still installs both, or which set wins, is unread |

What would settle the pair-list compare (unchanged from `v611-id-tables.md` Open,
with G156 applied):

1. An **authorised genuine** reply for one live launch's exact `?p=`, then a
   post-decrypt read the anti-tamper layer tolerates (hardware BP / read-only scan
   — not inline hooks), **or**
2. A **clean-room / repro** client that owns its own connector key and serves its
   own script (then the tables are whatever that script chooses).

Stock patched-client / lab-signed accept is ruled out (**G156**). G028's payload /
plaintext / `?p=` opens stay open and were left untouched. G246's token / template /
cipher opens stay open and were left untouched. **[inf]**

## Out of scope

Does not start **G334** or **G335**. Does not reopen **G028** residual opens,
**G156** trust-anchor residuals, **G246** token/template/cipher comparison,
**G248** Phase B, **G155** / G3D2504D, or **E#618** live frame. **G273** stays
**DROPPED**.