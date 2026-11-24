# v7 Worlds: connector trust-anchor swap is a NO-GO (E#616 / G156)

Date: 2026-11-24. Tags: **[bin]** held unpacked Worlds engine export/string inventory ·
**[lab][doc]** prior 6.113 trust-anchor and v7 connector notes · **[inf]** what that
blocks for a stock client.

This is the second Crypto board item (**G156** / Appendix **E#616** / `docs/NEXT.md`):
the avenue that said the decrypted connector script (game host/port and the login it
builds) needs a client whose baked connector public key is replaced with a lab key.
No hosts, keys, moduli, digests, `?p=` blobs, reply bodies, addresses or offsets appear
here.

## Settled: stock v7 cannot take a lab trust anchor

The NEXT checkbox and `connector-script.md` §7a name the same prerequisite as 6.113:
swap the compiled-in connector verify key for a lab key, then serve a lab-signed
`conf.gs` for that launch's exact `?p=`. On stock Windows 6.113 that swap is already a
**NO-GO** (`conf-gs-fuzzing.md`: virtualized verify; readable key region is a decoy).
This pass checks whether **v7 Worlds** is any different.

It is not.

| Surface | What is readable | What is runnable / patchable |
| --- | --- | --- |
| **Packed stock Worlds engine** | Crypto **export names** only (verify / private-decrypt / AES-CBC / RC4). Connector field names and the fail-path string are **not** cleartext in the packed image. | Live process under Themida/WinLicense. Inline hooks on verify / AES decrypt / RC4 set-key end the process before networking (`v7-connector-live-20261111.md` §3). Same protector family as the 6.113 NO-GO. |
| **Held unpacked analysis image** | Same export surface as G028 (`RsaSSL_Verify` / `RsaSSL_VerifyInline` separate from `RsaPrivateDecrypt*`; AES-CBC; Arc4; **no DES export**). Built-in connector skeleton strings are present (`StartScript_Connector`, `StartScript_Fail`, `scriptip` / `scriptsslcipher` / `scriptsslsubject` / `scriptsslissuer`, `Problem setting up the networking`, `User-Agent: Graal`). No PEM public-key armor. | **Not a drop-in client.** The unpack notes already treat these dumps as analysis images (tiny relocation directory; base-fixed). Editing an analysis dump does not produce a stock-accepted, anti-tamper-passing Worlds process. **[bin][doc]** |

So the two stock routes that would make a replaced public key useful both fail:

1. **Patch the packed client** — verify stays inside the protector VM; prior live attempts already showed engine-export hooks are fatal; no public-service fuzz and no further attach/memgrab was run here (same stop as G248 Phase B / 6.113 key recovery).
2. **Patch an unpacked image and run it** — the held dumps are not validated runnable replacements; they cannot be used as the "client with a replaced public key" the checkbox asks for.

Clean-room key-swap **logic** remains proven only on a faithful verify copy (`conf-gs-fuzzing.md`); that does not transfer to stock Worlds. **[lab][inf]**

## What this does *not* settle

G028's residual opens stay open and were not re-chased:

- exact connector-**payload** cipher and key/IV source
- production **plaintext** script (host/port, framing, login)
- the `?p=` DES key

Those still need either an authorised genuine reply for one live launch's exact `?p=`
(out of scope here; manual pace; no public-service fetch) or a post-decrypt read after a
reply the client already accepts — which stock v7 will not do for a lab-signed body.
Structure work stays on the clean-room repro track (`connector-script.md` §7a). **[inf]**

## Out of scope

Does not start **G246**, **G332**, **G334**, or **G335**. Does not reopen **G248**
Phase B, **G155** / G3D2504D, or **E#618** live frame. Does not change G028's residual
payload / plaintext / `?p=` opens beyond recording that the replaced-key avenue is closed.
**G273** stays **DROPPED**.