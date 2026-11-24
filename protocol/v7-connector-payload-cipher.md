# v7 connector reply: signature vs payload cipher (E#616)

Date: 2026-11-24. Tags: **[bin]** unpacked Worlds engine export inventory on a held
build-614 image · **[lab][doc]** prior connector notes cited below · **[inf]** what still
needs a patched client or a post-decrypt memory read.

This is the first Crypto board item (**G028** / Appendix **E#616**): what the decrypted
v7 connector script says (game host, framing/cipher, login). Container layout and the
per-launch signature were already known
([v7-connector-live-20261111.md](v7-connector-live-20261111.md) §3;
[connector-script.md](connector-script.md) §2). No hosts, keys, `?p=` blobs, reply bodies,
addresses or digests appear here.

## Settled: the 256-byte RSA block does not wrap an AES key

The E#616 best guess said the RSA block wraps an AES key for the payload. That conflates
two different RSA uses:

| Stage | What the 256-byte RSA material is | Evidence |
| --- | --- | --- |
| **Connector reply container** | RSA-2048 **signature** over the bare SHA-256 of the encrypted payload (no DigestInfo). Verified **before** any payload decrypt. | Same container as 6.11 **[lab]** (`v7-connector-live-20261111.md` §3; `v6-login-token-explained.md`); engine exports a **verify** API (`RsaSSL_Verify` / inline twin) separate from private-decrypt **[bin]** |
| **Game session `0xfc` key frame** | RSA **wrap** of a cipher type + length-prefixed key/IV, after the script runs | `connector-script.md` §4c **[lab][bin]** — later stage, not the container field |

So for the connector container, the RSA block is signature-only. It does **not** carry the
payload's symmetric key. The payload uses a **separate** compiled-in symmetric key
(`connector-script.md` §7a). **[bin][inf]**

## v7 engine crypto surface (readable exports)

On the held unpacked Worlds engine image (build 614), the exported crypto names are:

- **AES-CBC:** set-key / set-IV / encrypt / decrypt
- **RC4 (Arc4):** set-key / process
- **RSA:** public encrypt, private decrypt, SSL sign, SSL **verify** (and key init/free)
- **Hashes / RNG:** MD5, SHA, SHA-256, HMAC, RNG

There is **no DES export** on that engine image. The readable house DES-ECB inventory that
`conf-gs-fuzzing.md` names for 6.113 therefore does not appear as an exported symbol here;
`?p=` is still described as DES-ECB under a compiled-in key (`v6x-clients.md`), but that
key is not recovered and is not sitting behind a DES export on this image. **[bin]**

AES-CBC and RC4 remain the stream primitives the game path can select after the script runs
(`v7-graal3d-framing-and-packet-tables.md`). That does **not** by itself name the
connector-**payload** cipher. **[bin][inf]**

## Still open (honest partial)

| Open | Status after this pass |
| --- | --- |
| Exact **payload cipher** (AES-CBC vs RC4 vs something else) and its key/IV source | **Not pinned.** Parallel to 6.113: connector-reply decrypt is not a readable house-cipher entry point (`conf-gs-fuzzing.md`); v7 Themida ends inline hooks on verify / AES decrypt / RC4 set-key (`v7-connector-live-20261111.md` §3). |
| **Plaintext** script (host/port, framing, login it builds) | **Blocked** on stock: lab replies fail the per-launch signature; cross-launch replay rejected; trust-anchor swap is a NO-GO on packed clients (`conf-gs-fuzzing.md`, `connector-script.md` §7a). |
| **`?p=` DES key** | **Unrecovered** (shared with 6.11 work). No DES export on the v7 engine image above. |

## What settles the rest

1. ~~A client whose baked connector public key is replaced with a lab key, then a lab-signed
   reply for that launch's exact `?p=`~~ — **ruled out on stock v7** (G156 /
   [v7-connector-trust-anchor.md](v7-connector-trust-anchor.md): packed Themida verify;
   analysis dumps not runnable).
2. A post-decrypt read of the live script buffers by a method the anti-tamper layer tolerates
   (hardware breakpoint / read-only scan after a genuine accepted reply), not inline hooks —
   still needs a reply the stock client already accepts (authorised genuine launch), or a
   clean-room client that owns its own key.

Until one of those remaining routes runs, production plaintext stays **Maybe never**;
structure work stays on the clean-room repro track. **[inf]**

## Out of scope

Does not start **G246**, **G332**, **G334**, or **G335**. Does not reopen
**G248** Phase B, **G155** / G3D2504D, or **E#618** live frame. **G273** stays **DROPPED**.
**G156** is answered separately in `v7-connector-trust-anchor.md`.
