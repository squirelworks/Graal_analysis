# Fuzzing the 6.113 `conf.gs` connector reply, and the key-patch attempt

Date: 2026-11-19. Tags: **[bin]** the unpacked-image and connector notes cited below · **[lab]** the loopback method and the 2026-11-19 lab runs · **[inf]** inference / design. No hosts, addresses, keys, offsets, `?p=` blobs or reply bodies appear here (AGENTS.md).

This note ties together the two halves of one question: **how to make a stock Windows 6.113 client accept a `conf.gs` reply we built (the "key patch"), and how to fuzz that reply.** It is the design *plus* the 2026-11-19 lab results. The short version: the key-patch **logic** is proven on a faithful clean-room copy of the verify, but patching the **real Themida-packed client's** connector key is a **NO-GO** (Results, below); the phase-A container fuzz has been run against the real stock client and it fails closed on every malformation. It builds on [`connector-script.md`](connector-script.md) (the reply container and the script's steps), [`v6113-login-lab-method.md`](v6113-login-lab-method.md) (the two gates and the trust-anchor idea), [`v6113-status.md`](v6113-status.md), and the from-outside method in [`../client-internals/hypervisor-live-debug.md`](../client-internals/hypervisor-live-debug.md). The harness lives in [`../tools/connfuzz/`](../tools/connfuzz/).

Everything here is loopback-only against our own lab responder, in a headless KVM lab guest. Every patched binary, offset, key and dump is a lab artifact kept off git (AGENTS.md); only the plain-behaviour result is published.

## What is being fuzzed, and why the deep layer needs the key

The connector reply is a signed container (`connector-script.md` §2): a 4-byte marker, a 256-byte RSA-2048 signature over the **bare** SHA-256 of the payload (no DigestInfo), a 4-byte inner length, then the encrypted script payload. The client verifies the signature against a public key it holds **before** it decrypts, and never runs a reply that fails. **[bin][cap][lab]**

That pre-decrypt gate splits the surface into two layers, fuzzed differently:

| Layer | What the client does with it | Needs the key? |
| --- | --- | --- |
| **Container framing** — marker, signature field, inner length, payload buffer sizing | Read and sized **before** the verify decides. A short read, an over-long declared length, or a truncated body is handled by the container reader regardless of whether the signature will pass. | **No.** Runnable against a stock client with only a loopback connector. |
| **Decrypted script content** — the GS2 body, id-table pairs, token, RSA key material, cipher params | Reached **only after** the verify passes and the payload is decrypted and run as `StartScript_Connector`. | **Yes.** A stock client discards any payload it did not verify, so the deep parser is never reached unless it trusts a key we hold. |

So container (phase-A) fuzzing needs nothing patched; script-content (phase-B) fuzzing needs the client to accept our reply — the key patch below, or the clean-room repro.

## The key patch: attempted, and why it is a NO-GO on the real binary

The idea: make the client trust a lab key, then serve a lab-signed `conf.gs`. On a **faithful clean-room copy** of the verify (the repro's own RSA + SHA units, byte-compatible container) this works and was used as the design oracle — a lab-signed reply is **rejected** under the real connector key and **accepted** the moment the anchor is swapped to our lab key (openssl cross-checked). **[lab]** But the stock client's verify is not readable code; it runs inside the protector's VM, and two separate lab attempts to move the real client's trust anchor both failed:

1. **In-memory data-swap — impossible.** The verify is fully virtualized: the protector's own stub is the only reader of the key buffer, it is consumed inline during decrypt, and a full post-verify RAM dump shows **zero** copies of the modulus in any swappable form. There is no external buffer to overwrite. **[lab]**
2. **Ciphertext-precompute — defeated by a decoy.** The at-rest key blob is obfuscated by a **deterministic rolling XOR** (a one-bit-rotating key, no data feedback), which was fully reversed and validated — it reproduces the real modulus and exponent byte-for-byte. From that model a crafted at-rest ciphertext was computed so the client's **own** decrypt stub emits our **lab** key, and in the VM the readable key region then held our lab modulus exactly. **The signature still rejected.** Probing confirmed the readable connector-script handler (which runs only on a valid signature) is never reached: the verify does **not** use that readable region. It is effectively a **decoy**; the modulus the RSA check actually consumes is materialised inside the protector VM and never appears in a patchable form. **[lab]**

**Verdict:** making a real stock 6.113 client accept a lab-signed `conf.gs` by patching the connector key is a **NO-GO**. The reliable route to an end-to-end lab client is the clean-room **`graal-client-repro`** (`graal-6.1.1.3-GNP1905C`), which owns its own key and crypto; the signature + payload + phase-B work belongs there. **[lab][inf]**

A coarser **signature-skip** (forcing the verdict to success) was not pursued: the verdict is produced inside the same VM, so it has the same wall, and it changes control flow more than a swap would.

## The `conf.gs` payload cipher: also behind the VM wall

The container payload is "the encrypted script; different on every request" (`connector-script.md` §2). Static reversing settled the client's **house cipher** — it is **DES-ECB** (the `quattro_lib` DES, same primitive the `GRESCR01` script *cache* uses with a CRC32, `gs2-client-vm.md`) — and enumerated every readable DES entry point (the cache, the `des_encrypt`/`des_decrypt` builtins, a self-test). **None of them is on the connector-reply path.** So, like the verify, the reply **payload-decrypt is virtualized**; its exact cipher and key/IV source cannot be pinned from the readable image. The server→client `0xfc` key-frame is a separate, later, *asymmetric* stage (RSA to the script's parse key, `connector-script.md` §4c) — not this symmetric payload cipher. **[bin][lab]**

Consequence: phase-B *run-the-script* fuzzing of the **stock** client is blocked the same way the key patch is. It is reached instead through the clean-room repro, which owns the payload crypto (and can use the readable DES-ECB as an oracle).

## Fuzzing design

### Phase A — container framing (stock client, no patch)

Mutate the container around a fixed, inert payload and serve it from the loopback connector. These fields are consumed before the verify's verdict matters, so a defect here is pre-authentication — the most valuable kind.

| Field | Mutations |
| --- | --- |
| Marker (4) | flipped bytes, wrong marker, all-zero, all-0xFF |
| Signature (256) | all-zero, all-0xFF, one byte short, one byte long, truncated mid-field |
| Inner length (4) | declared length far larger than the body; declared 0 with a body present; declared at the ceiling; high bytes non-zero |
| Payload (N) | body shorter than declared; body longer than declared; empty; a few bytes then EOF |
| Transport | reply truncated mid-container; `Content-Length` larger than the bytes sent; chunked vs plain; a 443 reset to force the plain-HTTP `conf.gs` fallback |

### Phase B — decrypted script content (repro client)

With a client that owns its key (the repro), sign each mutated payload so it verifies, then feed the decrypt-and-run path. Targets, from the script's known surface (`connector-script.md` §4, §4a, §4c; `v611-id-tables.md`):

| Target | Mutations | Why |
| --- | --- | --- |
| Payload length vs body | mismatch, truncation, oversize (now **past** the verify) | the decrypt/load error path |
| GS2 bytecode body | truncated segments, bad segment lengths, unknown opcodes, non-GS2 body | the script loader / VM on connector-supplied code |
| `setProtocol` framer bytes (`EILLLT`) | wrong letters, short header, over-long length field | the framer setup |
| Incoming id-table pairs | out-of-range handler values, the reserved values (255/254/253/252), duplicate and sparse tables | `setindatahandlers` (`connector-script.md` §5) |
| The `0xfc` key-frame | cipher type out of {1,2}; Graal **value+32** length bytes **below 32** (underflow); key/IV lengths disagreeing with the bytes that follow; a 256-byte block that is not a valid RSA block | the parse-key path (`connector-script.md` §4c) |
| Token / `sendRaw` literal | wrong length, embedded NUL, oversize | the clear hello builder |
| Login settings the script reads | out-of-range `logintype`/`ciphertype`, malformed `cipherkey`/`initvector`/`keydata` | `connector-script.md` §4a |

### Mutation engine

A small library of deterministic mutators (bit flips, field-boundary values, length over/underflow, truncation, duplication, injected NULs, size extremes) over a template container, seeded so any finding reproduces. One mutation per reply by default. The gen-2.x "a NUL byte drops the rest of the frame" behaviour (`probe-targets-2026-11-18.md`) is a reminder that length/terminator edges are where Graal parsers break, so those are weighted first.

## The harness

Distinct from the game-wire probe harness, because it sits one gate earlier. `tools/probe/gen5probe.py` proxies the **game** stream (after the connector gate); `tools/connfuzz/` stands in for the **HTTP connector** before it. They share the lab discipline (loopback only, VM, redaction) and compose. Parts (see the tool README):

- **`connfuzz.py`** — builds the container from its four fields; the mutator library; a stdlib responder for `GET /conf.gs?p=...` with `User-Agent: Graal/<version>`; the 443-reset note. Signing is external with a lab key at runtime, so **no key is committed** and the shipped code stays stdlib-only.
- **`selftest.py`** — offline: container layout, each mutator, the responder's bytes. No client, no keys. CI-runnable like `tools/probe/selftest.py`.

### Observation and triage

The client runs in the lab VM, read from outside (`hypervisor-live-debug.md`). Per reply: **crash** (process gone), **hang** (no progress past the fetch), **silent reject** (connect-error / `StartScript_Fail` then retry — the expected path for a bad container), **accept-and-diverge** (accepted and doing something new on the wire — hand to `gen5probe.py`), or **no effect**. Each reply logs its seed, the mutated field, the container length, and the outcome; keys, hosts and reply bodies stay off git.

## Results (2026-11-19 lab)

All in a headless KVM lab guest, loopback-only, lab copies only; artifacts and write-ups off git.

- **Key-patch logic — proven on faithful code.** Against the repro's clean-room verify (byte-compatible container) and an independent openssl check, a lab-signed reply is rejected under the real connector key and accepted under the swapped lab key. **[lab]**
- **Real-binary key patch — NO-GO.** Both the in-memory data-swap and the ciphertext-precompute were run against the real packed client and failed as described above (fully virtualized verify; the readable key region is a decoy). The at-rest obfuscation (rolling XOR) was fully solved on the way, which is what proves the readable region is not what the verify consumes. **[lab]**
- **Phase-A container fuzz — run against the real stock client, fails closed.** All 18 one-field container mutations (marker / signature / inner length / payload-vs-length variants) were served to the real client over the loopback connector and compared to the clean-room oracle. **Every one fails closed:** the client stays up and shows the connect-error dialog — **no crash, no hang, no accept.** Notably the maximum declared length and the length/body-mismatch cases do **not** over-read or crash, so the container length is validated before use. **No candidate stock-client defect in phase A.** **[lab]**
- **Payload cipher — characterised, behind the VM wall.** House cipher is DES-ECB; the connector-reply decrypt is not a readable DES entry point (virtualized). **[bin][lab]**

## Still open / next

- **Phase-B on the repro.** Script-content fuzzing (the table above) against `graal-client-repro`, which owns its key and payload crypto — the route now that the stock client is a NO-GO for the deep layer. **[lab]**
- **Deeper phase-A variants** (two-field combinations, transport-level truncation timing) against the real client, since single-field phase-A is clean. **[lab]**
- **Wire into the two-gate chain.** A malformed-reply pass that reaches the game wire also needs the classic login/list gate served by the `seihai` stack (`v6113-login-lab-method.md`), so connfuzz and `gen5probe.py` run back to back. **[lab]**
