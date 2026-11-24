# Gen-6 client→server `0xfc` padding: settled envelope vs blocked EM (G335)

Date: 2026-11-24. Tags: **[lab]** Mac 6.111 / connector-script facts · **[cap]**
held stock clear `0xfc` bodies · **[bin]** script / method surface · **[inf]**
what the unheld operator private key would still unlock.

This is the last Crypto board item (**G335** / `v611-outgoing-cipher.md` Open
line 68): the padding scheme inside the **client→server** `0xfc` body. No hosts,
addresses, accounts, session keys, RSA blocks, digests or wire bytes appear
here. No public-service fetch, no conf.gs fuzz, and no decompiler dumps were
run. The operator private key was **not** found in lab this pass and stays
**unheld**.

## Short answer (honest partial)

**The envelope around the client→server block is settled. The exact padding
bytes inside that RSA block are not.** The clear client `0xfc` carries one
256-byte RSA-2048 ciphertext wrapped to the **operator** public key (not the
client parse key). Server→client padding is already closed as PKCS#1 v1.5
type-2. Server→client **plaintext** after unwrap is already known (cipher type
+ length-prefixed key/IV). Proving the same (or any other) encoding-message
layout for **client→server** still needs the matching operator **private** key,
which remains unheld. **[lab][cap][inf]**

## Settled (no operator private key required)

| Question | Settled finding | Evidence |
| --- | --- | --- |
| Wire shape of the client key frame? | Clear outer `0xfd` (zlib) wraps inner `0xfc` with a **256-byte** high-entropy body; cut at stream offset **287**, then RC4 | `v611-outgoing-cipher.md`; `connector-script.md` §4 / §4b **[lab][cap]** |
| What the script puts in that body? | `generate16ByteKey` → `rsa_encrypt` under a 2048-bit public key carried in the connector script (exponent 65537) → `sendData` | `v611-outgoing-cipher.md`; `connector-script.md` §4 **[lab][bin]** |
| Which public key wraps C→S? | The **operator** key in the script — **not** the parse-key pair used for S→C | Decrypting stock C→S bodies with the held **parse** private key yields garbage; S→C bodies unwrap cleanly with that same parse key (`gen6-s2c-pkcs-padding-2026-11-16.md`) **[lab][cap]** |
| Server→client padding? | PKCS#1 v1.5 type-2 (`00 02` … nonzero PS … `00` … payload) on held stock S→C blocks | `gen6-s2c-pkcs-padding-2026-11-16.md` **[cap][lab]** |
| Server→client plaintext after unwrap? | Cipher type (1 = RC4, 2 = AES), then length-prefixed key, then length-prefixed IV; Graal **value+32** length bytes. Stock sessions observed: type **1**, keylen **16**, ivlen **16** | `connector-script.md` §4c; S→C padding note **[lab]** |
| Are the two directions the same key? | **No.** Client makes the OUT key; server makes a separate IN key and sends it in its own `0xfc` | `connector-script.md` §4c **[lab]** |
| Signatures vs session-key encrypt? | Connector reply signatures use PKCS#1 v1.5 **type 1** over a bare digest — same family name, different object | `gen6-s2c-pkcs-padding-2026-11-16.md`; `connector-script.md` §2 **[bin][lab]** |

So everything a lab server needs to **emit** its own S→C key frame (and to
document the C→S wire envelope) is settled. Reading a **stock** client's C→S
`0xfc` still is not. **[lab][inf]**

## Still open (operator private key unheld)

| Avenue | Status | Why |
| --- | --- | --- |
| Raw RSA decrypt of held stock **client→server** `0xfc` bodies → read EM leading bytes | **Blocked** | Needs the operator private key matching the script's operator public key; **unheld** this pass (no lab file found; parse-key half does not apply) **[inf]** |
| Confirm PKCS#1 v1.5 type-2 (or any other scheme) on C→S | **Open** | Working inference only: same `rsa_encrypt` family and 256-byte block size as the closed S→C path. Not a proof without a successful unwrap **[inf]** |
| Confirm C→S plaintext field order matches §4c | **Open** | Expected by symmetry (cipher type + length-prefixed key/IV), but the EM has not been opened on stock C→S blocks **[inf]** |
| Lab-minted C→S under a self-owned operator key | Does not prove stock | Circular for the production operator key; useful only for a clean-room server that serves its own connector **[inf]** |

What would close the remaining padding question (never publish the key):

1. An owner-held **operator private** key that matches the public key inside a
   stock connector script, used offline against held clear client→server
   `0xfc` bodies, **or**
2. A lab session where the client is driven by a connector the lab signed under
   a known operator key (stock trust-anchor / Phase B avenues stay out of
   scope here).

Until one of those exists, G335 stays an **honest partial**: envelope and
cross-direction facts settled; encoding-message padding on C→S unread. **[inf]**

## Out of scope

Does not start **Machine-identity** (G129 / G285 / G286 / G287) or any other
group. Does not reopen **G028** residual opens, **G156** trust-anchor
residuals, **G246** token/template/cipher comparison, **G332** pair-list
comparison, **G334** key recovery, **G248** Phase B, **G155** / G3D2504D, or
**E#618** live frame. **G273** stays **DROPPED**.
