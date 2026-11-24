# Mac PowerPC machine-identity property read and hash (G129)

Date: 2026-11-24. Tags: **[bin]** opened bodies on 4.04r2, 4.20r6 and shared v5 ·
**[lab]** empty primary-interface field already explained · **[inf]** login-string
assembly still open.

This closes the surface remaining-work item in
[mac-ppc-runtime-surface-2026-11-09.md](mac-ppc-runtime-surface-2026-11-09.md)
(line 262): open the routines that **read** and **hash** the machine-identity
property. The earlier match helper (I/O Kit master port + `IOEthernetInterface`
with an `IOPrimaryInterface` property match) stays as documented there. Field
meanings for the login comma-list are already in [pcid.md](../protocol/pcid.md)
(Mac 4.20r6). No hosts, accounts, digests, RVAs, function names or raw decompiler
dumps appear here. No public-service fetch, no conf.gs fuzz, and no live attach.

## Short answer (honest partial)

**The property-read and the hash of the six-byte MAC are settled on 4.04r2,
4.20r6 and shared v5.** The match helper feeds an iterator; a second helper walks
that iterator, climbs each entry to its `IOService` parent, reads the
`IOMACAddress` CFData property and copies **exactly six** raw bytes into a
caller buffer (zeroed first). A third helper, when those six bytes are present,
runs a plain **MD5** over them (classic initial values) and appends the sixteen
digest bytes as lowercase hex into a string object. If the match/read path fails,
the string helper is left empty instead. That matches the empty network field on
an emulated card that is not marked built-in / primary. **[bin][lab]**

What is **not** closed: the full call graph from login framing through the
comma-list assembler into these helpers, and the other machine fields (the
`/etc` inode hash and the empty third slot) were not reopened on this pass.
**G285+** (listserver PCID rule, Win10 product-id slot, 5.12 product id,
connector machine fields) is **not** started. **[inf]**

## Settled

| Step | What the opened body does | Builds |
| --- | --- | --- |
| Match (already known) | Master port → matching dictionary for `IOEthernetInterface` with `IOPrimaryInterface` under `IOPropertyMatch` → matching services iterator | 4.04r2, 4.20r6, v5 **[bin]** |
| Property read | For each iterator entry: parent under `IOService`; `IOMACAddress` via `IORegistryEntryCreateCFProperty`; `CFDataGetBytes` of length **6** into a zeroed buffer; release objects | same three **[bin]** |
| Copy | On success, copy the six bytes into a small fixed buffer used by the hasher | same three **[bin]** |
| Hash | MD5 init (`0x67452301` / `0xefcdab89` / `0x98badcfe` / `0x10325476`), update over the six raw bytes, finalise, hex-encode all 16 digest bytes into a string | same three **[bin]** |
| Empty path | If match/read fails, the string path clears instead of hashing | same three **[bin]** |
| Emulated empty field | QEMU/OpenBIOS without device-tree `built-in` → no `IOPrimaryInterface` → empty network hash on login | already in the Tiger lab note; fits the empty path above **[lab][inf]** |

So the network field on Mac PowerPC is: **MD5(raw 6-byte `IOMACAddress` of the
primary Ethernet interface), hex-encoded**. Not hex text of the MAC, and not a
LibTomCrypt/`md5` script binding (that string is a separate script API
registration). **[bin][lab]**

## Still open

| Avenue | Status | Why |
| --- | --- | --- |
| Login comma-list assembler → these helpers (full call graph) | **Open** | Wrappers that call match/read/hash were opened; the path that joins `mac,<hash>,…` into the first login frame was not traced end-to-end this pass **[inf]** |
| Second field (`/etc` inode) and empty third slot | **Out of this item** | Already summarised in `pcid.md`; not the `IOMACAddress` property **[inf]** |
| Side path that mixes the six MAC bytes into another buffer with fixed XOR constants | **Observed, not explained** | Present next to the hash wrappers; not required to settle property-read + MD5 hex **[inf]** |
| G285 / G286 / G287 / G289 | **Not started** | Separate Machine-identity board rows **[inf]** |

## Out of scope

Does not start **G285+**. Leaves all **Crypto** residuals (**G028** / **G156** /
**G246** / **G332** / **G334** / **G335**), **G248** Phase B, **G155** /
G3D2504D, and **E#618** live frame untouched. **G273** stays **DROPPED**.

## Evidence

Sanitized static summaries, registered in
[the evidence index](../docs/evidence-index.tsv). Raw exports stay owner-held.

- `MAC-PPC-404-IDENTITY-PROPERTY-20261124-R1`
- `MAC-PPC-420-IDENTITY-PROPERTY-20261124-R1`
- `MAC-PPC-V5-IDENTITY-PROPERTY-20261124-R1`