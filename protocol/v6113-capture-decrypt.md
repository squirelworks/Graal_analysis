# Windows 6.113 capture decrypt: settled cut vs blocked key (G334)

Date: 2026-11-24. Tags: **[cap]** owner-held Windows 6.113 port-14900 capture
(`v6113-list-capture.md`) · **[lab]** prior Mac 6.111 key-grab method ·
**[bin]** cipher notes already published · **[inf]** what would still unlock the
ciphertext.

This is the next Crypto board item (**G334** / `v611-outgoing-cipher.md` Open
line 65): decrypt the **Windows 6.113 capture itself**. No hosts, addresses,
accounts, session keys, RSA blocks, digests or wire bytes appear here. No
public-service fetch, no conf.gs fuzz, and no decompiler dumps were run.

## Short answer (honest partial)

**The clear prefix and the RC4 cut are settled on the capture.** Three client
streams in the held Windows 6.113 file open with the same clear hello the Mac
lab already named (`GNP1905C`, outer `EILLLT`/`0xfd` with `LLL=279`, zlib body
inflating to an inner `0xfc` + 256-byte block), then ciphertext from stream
offset **287**. **The post-287 bytes stay unread.** The session key of that
exact capture was never recorded from the running client, and every offline
avenue that would recover it without that key stays blocked. **[cap][inf]**

## Settled without a session key

| Question | Settled finding | Evidence |
| --- | --- | --- |
| Clear hello shape on the capture? | Yes: token + outer `01 02 00 01 17 fd` + zlib `78 9c` member | `v6113-list-capture.md`; reconfirmed on three reassembled client streams **[cap]** |
| RC4 cut? | Stream offset **287**; keystream starts fresh there | `v611-outgoing-cipher.md`; live 6.113 confirm `v6113-live-handshake-2026-11-16.md` **[lab][cap]** |
| Cipher family on this path? | Plain RC4 (no IV); early post-hello client writes of length 7 rule out AES block padding | `v611-outgoing-cipher.md`; live handshake **[lab][cap][inf]** |
| One key per session? | Yes: the three capture streams carry **distinct** post-287 ciphertext and distinct 256-byte inner blocks | capture reassembly **[cap]**; matches Mac lab "one key decrypts none of eight other sessions" **[lab]** |
| Where the key would have lived? | Made by `generate16ByteKey`, sent RSA-wrapped in the clear inner `0xfc`, then installed at `setEncryptionOut` | `v611-outgoing-cipher.md`; `connector-script.md` §4 **[lab][bin]** |
| Can a memory dump alone recover it? | **No.** Mac lab: dump mid-session did not show the key or RC4 state; only the set-key breakpoint did | `v611-outgoing-cipher.md` Method notes **[lab]** |

## Still open (key recovery blocked)

| Avenue | Status for **this** capture | Why |
| --- | --- | --- |
| Read the key from **that exact** running client | **Blocked** | The capture sessions are historical; the process is gone. No owner-held key file for those streams was found for this pass **[inf]** |
| Offline RSA unwrap of the clear `0xfc` body | **Blocked** (out of scope here) | Needs the operator private key matching the script's public key; **unheld**. That padding/private-key question is **G335** and was **not** started **[inf]** |
| Reuse a Mac / lab OUT key from another session | **Blocked** | Keys are per-session; a key from one stream decrypts none of the others **[lab][cap]** |
| Drive stock Windows 6.113 with a lab-chosen key, then grab | Does not decrypt **this** capture | Would only unlock a **new** session. Stock connector trust-anchor reject already pinned for 6.113 lab (`v6113-login-lab-2026-11-19.md`); G248 Phase B left untouched **[lab]** |
| Live 2026-11-16 official handshake | Did not recover keys | Explicit non-result in `v6113-live-handshake-2026-11-16.md` **[cap]** |

What would settle a full decrypt of the held capture (unchanged in nature from the
Open line, with the blockers named):

1. An owner-held record of the **16-byte OUT key** for one of those exact
   streams (read at `setEncryptionOut` / RC4 set-key while that session ran),
   **or**
2. The operator **private** key that unwraps the clear client→server `0xfc`
   body (**G335** — not chased here).

A later live Windows key-grab (hardware BP on a **new** session) would decrypt
that new session only; it does not reopen the historical file. **[inf]**

## Out of scope

Does not start **G335**. Does not reopen **G028** residual opens, **G156**
trust-anchor residuals, **G246** token/template/cipher comparison, **G332**
pair-list comparison, **G248** Phase B, **G155** / G3D2504D, or **E#618** live
frame. **G273** stays **DROPPED**.