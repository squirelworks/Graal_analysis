# GS2 segment-1 GS1 event mask (producer / consumer)

Date: 2026-11-16. Tags: **[cap]** for official bodies; **[bin]** for stock VM / engine strings.

Leads-only. Bodies, keys and names stay private — structure and counts only. Extends [`gs2-vm-from-engines.md`](../client-internals/gs2-vm-from-engines.md) and the nineteen-body container note.

## What segment 1 is

On 4.20r8 / 5.00r7 / 6.00, segment type **1** is one big-endian **32-bit** GS1 event mask on the script. A second mask word sits beside it. Joined classes **OR** their masks in. `needEvent(index)` is true when that bit is set, and also when the script is **not yet initialized**. The named `script_event` list through `playanimation` is already published. **[bin]**

## Official output — always zero so far

| Corpus | Segment-1 value | Tag |
| --- | --- | --- |
| Official 6.113-era GS2 bodies | **0 / 19** nonzero | [cap] |
| Additional held decrypted GS2 bodies this pass | **0 / 26** nonzero | [cap] |
| Enlarged offline GS2 container hunt | **0** nonzero seg1 in **208+175** containers | [cap] |

So every official / captured GS2-shaped body held here leaves the GS1 mask empty. That fits pure GS2 / function-only server scripts. It does **not** yet show what an official compiler writes for a classic top-level `if (playerenters)` style body — no such compiled body was found. **[cap]**

## Bit 27 `pkzonechanges`

A third-party compiler/engine pair names bit **27** as `pkzonechanges`. Stock **4.20r8** and **5.00r7** engines carry the classic event names through `playanimation` / `shapetrigger` / `washit` / `playerleaves` and the `needEvent` surface, but **`pkzonechanges` is absent** as an event name (nearby `pkzone` / `nopkzone` strings are property-side). Do **not** require bit 27 for 4.x/5.x fidelity. **[bin]**

## Consumer rule (stock)

Stock VMs **do** filter GS1-indexed events with the mask (plus the not-yet-initialized bypass). Joined masks count. Whether a clear bit is bypassed solely because an `on…` handler exists is **not** settled in the published `needEvent` wording and still needs a dispatch re-read or a live mask set/clear fixture. **[bin][inf]**

## Still open

- An official (or stock-server) GS1-compiled body with a **nonzero** segment 1. **[cap]/[lab]**
- Exact skip rule when the bit is clear but an `on…` handler exists. **[bin]/[lab]**
- Live mask set vs clear on **4.20r8**, **5.12**, **6.03r7**. **[lab]**
