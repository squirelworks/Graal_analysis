# v7 vs 6.11 connector script: settled outside vs blocked inside (G246)

Date: 2026-11-24. Tags: **[doc][lab]** prior connector notes 뿯½ **[bin]** held
Worlds engine method/string surface already published 뿯½ **[inf]** what a decrypted
reply would still need to settle.

This is the next Crypto board item (**G246** / `connector-script.md` Open /
section **7a**): whether the production **7.x connector script** differs from the
**6.11** one in **token**, **template**, and **cipher**. No hosts, keys, `?p=`
blobs, reply bodies, addresses or digests appear here. No public-service fetch and
no conf.gs fuzz were run.

## Short answer (honest partial)

**Outside the script** the 7.x vs 6.11 differences are already settled in
`connector-script.md` 뿯½7a (and the linked live/trust-anchor notes). **Inside the
script** — the exact token literal, `setProtocol` template string, and the cipher
type/key path the production reply chooses — stays **uncompared**. Decrypting a
7.x reply for its own launch remains **blocked** by the stock trust-anchor
**NO-GO** (**G156**) plus the open G028 residuals (payload cipher / plaintext /
`?p=` DES key). Those residuals were **not** re-chased here. **[inf]**

## Settled without a decrypted 7.x script

| Question | Settled finding | Evidence |
| --- | --- | --- |
| Same connector **design**? | Yes: HTTPS 뿯↽ `conf.gs?p=`, same reply container, script-driven login | `v7-connector-live-20261111.md` 뿯½2–뿯½3; `connector-script.md` 뿯½1–뿯½2 **[lab]** |
| Compiled-in eight-char token? | **No** on 7.x (same pattern as 6.11): token is expected from the connector script, not a baked `GNP…` / `G3D…` literal | `v7-graal3d-identity-and-builds.md` 뿯½2; `v7-connector-live-20261111.md` 뿯½1 **[bin][lab]** |
| Engine can run the 6.11-family steps? | Yes: `StartScript_Connector` / `_Fail`, `scriptip` / SSL field names, `setprotocol` path, cleartext `RC4`/`AES` selectors, `I`/`L`/`T`/`E` framing cluster; default before script is classic mode 0 | `v7-graal3d-framing-and-packet-tables.md` 뿯½2 **[bin]** |
| Outside-script diffs vs 6.11? | Ship form (Unity+Themida), `User-Agent` 6.76/6.77, VERSIONINFO 6.114, **per-launch** `?p=`, encrypted `onSend…` names, cross-launch reply reject | `connector-script.md` 뿯½7a **[bin][lab]** |
| Stock decrypt avenue? | **Closed:** trust-anchor swap is a **NO-GO**; payload key unrecovered | `v7-connector-trust-anchor.md` (G156); `v7-connector-payload-cipher.md` (G028) **[bin][lab][inf]** |

The moderate best guess from App. E#616 still stands as a **guess only**: once
decrypted, the script likely still follows the 6.11 structure (set protocol, set
ciphers, id tables, connect, login). That is **not** a comparison of the three
named fields. **[inf]**

## Still open (needs a decrypt the stock path cannot provide)

| Field | 6.11 known | 7.x production script |
| --- | --- | --- |
| **Token** (`sendRaw` literal) | `GNP1905C` on Mac 6.111 and Windows 6.113 **[lab][cap]** | **Uncompared.** Upstream gs2lib labels Worlds as `G3D2204D`; whether production replies use that, `GNP1905C`, or another string is **not** established (`v7-connector-live-20261111.md` 뿯½1) |
| **Template** (`setProtocol`) | `EILLLT` **[lab]** | **Uncompared.** Engine has the letter cluster; the string the reply passes is unread |
| **Cipher** (type + key path the script installs) | RC4 via `generate16ByteKey` / `setEncryptionParseKey` / `setEncryptionOut` on 6.11 **[lab]** | **Uncompared.** Engine exports RC4 and AES-CBC; which one the production script picks, and with what key/IV source, is unread |

What would settle the three fields (unchanged from 뿯½7a, with G156 applied):

1. An **authorised genuine** reply for one live launch's exact `?p=`, then a
   post-decrypt read the anti-tamper layer tolerates (hardware BP / read-only scan
   — not inline hooks), **or**
2. A **clean-room / repro** client that owns its own connector key and serves its
   own script.

Stock patched-client / lab-signed accept is ruled out (**G156**). G028's payload /
plaintext / `?p=` opens stay open and were left untouched. **[inf]**

## Out of scope

Does not start **G332**, **G334**, or **G335**. Does not reopen **G028** residual
opens, **G156** trust-anchor residuals, **G248** Phase B, **G155** / G3D2504D, or
**E#618** live frame. **G273** stays **DROPPED**.
