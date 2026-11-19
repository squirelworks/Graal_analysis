# Fuzzing the 6.113 `conf.gs` connector reply, and the key patch that unlocks it

Date: 2026-11-19. Tags: **[bin]** the unpacked-image and connector notes cited below · **[lab]** the loopback method and prior lab runs cited below · **[inf]** inference / design. No hosts, addresses, keys, offsets, `?p=` blobs or reply bodies appear here (AGENTS.md).

This note is a method and design, not a run. It ties together the two halves of a single question: **how to make a stock Windows 6.113 client accept a `conf.gs` reply we built (the "key patch"), and how to fuzz that reply once it will.** It builds on [`connector-script.md`](connector-script.md) (the reply container and the script's steps), [`v6113-login-lab-method.md`](v6113-login-lab-method.md) (the two gates and the trust-anchor swap), [`v6113-status.md`](v6113-status.md) (what is settled), and the from-outside debug method in [`../client-internals/hypervisor-live-debug.md`](../client-internals/hypervisor-live-debug.md). The harness skeleton it describes lives in [`../tools/connfuzz/`](../tools/connfuzz/).

Everything here is loopback-only against our own lab responder. The patched binary, any offset, and any key are lab artifacts that stay off git (AGENTS.md); only the plain-behaviour method is published.

## What is being fuzzed, and why it needs the key patch

The connector reply is a signed container (`connector-script.md` §2): a 4-byte marker, a 256-byte RSA-2048 signature over the **bare** SHA-256 of the payload (no DigestInfo), a 4-byte inner length, then the encrypted script payload. The client verifies the signature against a public key compiled into the client **before** it decrypts, and never runs a reply that fails. **[bin][cap]**

That pre-decrypt gate splits the attack surface into two layers, which must be fuzzed differently:

| Layer | What the client does with it | Needs the key patch? |
| --- | --- | --- |
| **Container framing** — marker, signature field, inner length, the payload buffer sizing | Read and sized **before** the verify decides. A short read, an over-long declared length, or a truncated body is handled by the container reader regardless of whether the signature will pass. | **No.** Runnable against a stock client as soon as a loopback connector exists. |
| **Decrypted script content** — the GS2 body, the id-table pairs, the token, the RSA key material and cipher params the script carries | Reached **only after** the verify passes and the payload is decrypted and run as `StartScript_Connector`. | **Yes.** A stock client discards any payload we did not sign with the operator key, so the deep parser is never reached until the client trusts a key we hold. |

So the key patch is not a side quest; it is the enabler for the deep (script-content) fuzzing. Container fuzzing can start first and needs nothing patched.

## The key patch: trust-anchor swap (and the skip variant)

The gate is an RSA-2048 public modulus the client checks the signature against. For 6.113 that anchor is **not a static constant in the file**: a static scan of the unpacked image found no stored RSA-2048 modulus (no DER, no CryptoAPI blob, no PEM), the general CyaSSL RSA-verify paths take their key from a server-signing-key property that arrives on the wire at runtime, and the connector-reply signature check itself is **virtualized inside the Themida VM**. The anchor materializes in memory only at verify time. **[lab]** (concurrent unpack/runtime capture; exact routine and bytes go to the Share write-up, off git)

That rules out a static file-offset patch. Both lab patches below are therefore **runtime, in-memory, at-verify-time** operations on a **lab copy only**, never the original (AGENTS.md), done from the host with the from-outside method (QEMU/KVM gdbstub, patch after Themida's VM has materialized the value; `hypervisor-live-debug.md`), so no in-guest debugger meets Themida's anti-debug:

1. **Trust-anchor swap (preferred).** At verify time, replace the materialized public modulus the check consumes with the public half of a lab key pair we hold. The client then verifies, and runs, any `conf.gs` we sign with the matching lab private key. This keeps the whole signed-container path live, so it also exercises the real (virtualized) verify with valid input — what phase-B fuzzing needs. The clean-room repro reaches the same end a different way: it bakes in its **own** modulus and runs its **own** signed script, and a stock reply does not verify against it (`v6113-login-lab-method.md`; `graal-client-repro`, `Connector6113.pas`). **[bin][inf]**
2. **Signature-skip (coarser).** Force the virtualized verify's verdict to success at runtime. The client then accepts an **unsigned or arbitrarily-signed** reply. Simpler, and it lets the fuzzer vary the signature field freely, but it removes the real verify from the path and changes control flow more than the swap. Use it only to reach the payload parser quickly. **[inf]**

### Locating the anchor

The modulus and the verify do not exist in the packed stub listing (`engine-6113.md`, `decompile-6113.md`); the engine body (with a CyaSSL surface and `StartScript_Connector`) is present once Themida has unpacked it (`unpacked-6113.md`), but — per the finding above — the connector-reply check is virtualized and the modulus is runtime-only, so the landmark is a **run-time site**, not a file offset. At plain-behaviour level:

- The reply is verified against a **bare 32-byte SHA-256** digest (PKCS#1 v1.5 **type 1** over a raw digest, not the type-2 session-key padding — `gen6-s2c-pkcs-padding-2026-11-16.md`), on the path that turns the reply into `StartScript_Connector`, gated before the payload decrypt.
- The swap/skip site is the routine that **consumes** the materialized modulus / produces the verify verdict, caught at verify time by the host watcher. The unpack thread is capturing the decrypted modulus and pinning that consuming routine, and pulling the earlier GwenTea2 MODULUS-SWAP notes for their offsets.

The captured modulus bytes, the exact site and any patchable in-memory address are recorded **in the Share labs write-up, off git**.

**Dependency:** the runtime capture (decrypted modulus + consuming routine) and the runnable lab copy come from the Themida-unpack thread. This note's design and the offline harness do not wait on it; only the live patch and run do.

## The conf.gs payload cipher is the open piece for phase B

The container payload is "the encrypted script; different on every request" (`connector-script.md` §2). How the client **decrypts** that payload into runnable `StartScript_Connector` bytes is not yet pinned in our notes (it is distinct from the `GRESCR01` weak-DES script *cache*, which is settled — `gs2-client-vm.md`, `gs2-official-bytecode-6113.md`). Phase-B content fuzzing that expects the client to *run* a mutated script needs that cipher pinned first, so the fuzzer can hand the client a payload it can decrypt. Until then, phase B can still fuzz at the **decrypt boundary**: a validly-signed container whose payload is structurally mutated (wrong declared length, truncated body, random body) exercises the decrypt-and-load path's error handling, which is the first thing reached after the verify passes. Pinning the payload cipher is called out in Still open.

## Fuzzing design

### Phase A — container framing (stock client, no patch)

Mutate the container around a fixed, inert payload and serve it from the loopback connector. Watch the client. Because these fields are consumed before the verify's verdict matters, a defect here is a pre-authentication defect — the most valuable kind.

| Field | Mutations |
| --- | --- |
| Marker (4) | flipped bytes, wrong marker, all-zero, all-0xFF |
| Signature (256) | all-zero, all-0xFF, one byte short, one byte long, truncated mid-field (forces a short read on the length that follows) |
| Inner length (4) | declared length far larger than the body sent; declared length 0 with a body present; declared length at the 16-bit ceiling; the high two bytes non-zero (the field is documented as `00 00` + 16-bit) |
| Payload (N) | body shorter than declared; body longer than declared; empty; a few bytes then EOF (connection closed early) |
| Transport | HTTP reply truncated mid-container; `Content-Length` larger than the bytes sent; chunked vs plain; a 443 reset to force the plain-HTTP `conf.gs` fallback (`v6113-login-lab-method.md`) |

### Phase B — decrypted script content (patched client)

With the trust anchor swapped, sign each mutated payload with the lab key so it verifies, then feed the decrypt-and-run path. Mutation targets, from the script's known surface (`connector-script.md` §4, §4a, §4c; `v611-id-tables.md`):

| Target | Mutations | Why |
| --- | --- | --- |
| Payload length vs body | mismatch, truncation, oversize (as phase A but now **past** the verify) | the decrypt/load error path |
| GS2 bytecode body | truncated segments, bad segment lengths, unknown opcodes, a body that is not valid GS2 | the script loader / VM on connector-supplied code |
| `setProtocol` framer bytes (`EILLLT`) | wrong letters, short header, over-long length field | the framer setup |
| Incoming id-table pairs | out-of-range handler values, the reserved values (255 clear, 254 do-not-call, 253/252 special), duplicate and sparse tables | `setindatahandlers` (`connector-script.md` §5) |
| The `0xfc` key-frame the script makes the client accept | cipher type out of {1,2}; the Graal **value+32** length bytes **below 32** (underflow); key/IV lengths that disagree with the bytes that follow; a 256-byte block that is not a valid RSA block | the parse-key path (`connector-script.md` §4c, `gen6-s2c-pkcs-padding-2026-11-16.md`) |
| Token / `sendRaw` literal | wrong length, embedded NUL, oversize | the clear hello builder |
| Login settings the script reads | out-of-range `logintype`/`ciphertype`, malformed `cipherkey`/`initvector`/`keydata` | `connector-script.md` §4a |

### Mutation engine

A small library of deterministic mutators (bit flips, field-boundary values, length over/underflow, truncation, duplication, injected NULs, size extremes) over a template container. Deterministic and seeded, so any crash reproduces from its seed. One mutation per reply by default; an escalation mode combines two. The known gen-2.x "a NUL byte drops the rest of the frame" behaviour (`probe-targets-2026-11-18.md`) is a reminder that length/terminator edge cases are where Graal parsers break, so those are weighted first.

## The harness

A distinct piece from the game-wire probe harness, because it sits one gate earlier. `tools/probe/gen5probe.py` proxies the **game** stream (after the connector gate). `tools/connfuzz/` stands in for the **HTTP connector** that precedes it. They share the lab discipline (loopback only, VM/`bwrap`, redaction) and compose: connfuzz gets the client past (or into) the connector gate; gen5probe then fuzzes the game wire behind it.

Parts (skeleton in `tools/connfuzz/`, see its README):

- **`connfuzz.py`** — builds the container from its four fields; the mutator library; a stdlib `http.server` responder that serves a chosen (optionally mutated) reply for `GET /conf.gs?p=...` with `User-Agent: Graal/<version>`; a note on the 443-reset helper that forces the plain-HTTP fallback. Signing is pluggable and **done by an external command with a lab key at runtime** (e.g. `openssl` or a `cryptography`-backed signer) so **no key is committed** and the shipped code stays stdlib-only.
- **`selftest.py`** — offline: asserts the container layout (field sizes and offsets of a built reply), that each mutator changes exactly what it claims, and that the responder serves the bytes it was given. No client, no keys, no network beyond loopback — runnable in CI the way `tools/probe/selftest.py` is.
- **`README.md`** — how to run it in the lab against a patched client, and the hard rule that it is loopback-only and never pointed at any real connector host.

### Observation and triage

The client runs in the lab VM; the from-outside watcher reads it (`hypervisor-live-debug.md`): host-side memory snapshots and hardware breakpoints, no in-guest debugger. Per reply, classify the outcome:

| Outcome | Signal |
| --- | --- |
| **Crash** | process gone / fault caught by the host watcher; record the seed |
| **Hang** | still up but no progress past the connector fetch within a timeout |
| **Silent reject** | falls to `StartScript_Fail` / "Problem setting up the networking" (`connector-script.md` §6) and retries — the expected path for a bad container |
| **Accept-and-diverge** | the reply was accepted and the client did something new on the wire (a different hello, framing, or id set) — the interesting phase-B result; hand off to `gen5probe.py` to read it |
| **No effect** | accepted/rejected with identical behaviour to the baseline |

Each reply logs its seed, the mutated field, the container bytes' length, and the outcome, so every finding reproduces. Keys, hosts and reply bodies stay out of the logs and off git.

## Still open

- **Pin the `conf.gs` payload cipher** (how the client decrypts the container payload into `StartScript_Connector`). Phase-B *run-the-script* fuzzing depends on it; phase-B *decrypt-boundary* fuzzing does not. **[lab]**
- **The live run.** It needs the runtime capture of the materialized modulus and its consuming (virtualized) verify site (Themida-unpack thread), the trust-anchor swap or skip applied in memory on a lab copy, and the harness wired to the from-outside watcher. Each half is understood; they have not been run as one chain. **[lab]**
- **Wire into the two-gate chain.** A full malformed-reply pass that reaches the game wire also needs the classic login/list gate served by the `seihai` stack (`v6113-login-lab-method.md`), so connfuzz and gen5probe run back to back. **[lab]**
