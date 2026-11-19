# Getting the real 6.113 client past login in the lab: the two gates, and what can be replayed

Date: 2026-11-19. Tags: **[lab]** a loopback-only run of the real Themida-packed Windows 6.113 client in a QEMU/KVM VM with a restricted NIC (no public network, no captures against anyone's servers) · **[cap]** prior owner-held 6.113 captures cited by the notes below · **[bin]** the unpacked-image and connector notes · **[inf]** inference. No hosts, addresses, keys, `?p=` blobs or cache bodies appear here (AGENTS.md).

This note answers a practical question: can the stock 6.113 client be driven through login in a lab, and can its connector reply or token be replayed or forged? It is the loopback counterpart to the capture notes ([`v6113-status.md`](v6113-status.md), [`connector-script.md`](connector-script.md), [`v611-outgoing-cipher.md`](v611-outgoing-cipher.md)) and uses the from-outside method in [`client-internals/hypervisor-live-debug.md`](../client-internals/hypervisor-live-debug.md).

## There are two gates, not one

The RC4 handshake the earlier notes describe (`GNP1905C`, one clear `EILLLT`/`0xfd` frame, RC4 from offset 287) is the **game-server** connection. It is not the first thing the client does. A stock launch has two separate gates, and they fail independently:

1. **The login/list gate — classic protocol.** On start the client drives a classic login-and-list host family (a `<login-host>` / `<list-host>` set, distinct from the connector host). This is the account-and-serverlist step, and it is the one the UI means by "Connecting to the login server…". **[lab]** With that host unreachable the client never leaves this screen, and the connector/game step below is never reached in a restricted lab env. **[lab]**
2. **The connector gate — signed script, then RC4.** The game-server connection is the one that fetches a signed `conf.gs` reply from the connector host family (`<connector-host>`, first label `con`, falling back to `con2`), verifies it, decrypts it, and runs it as `StartScript_Connector`. That script supplies the token and sets up RC4 (`connector-script.md` §4). **[bin][cap]**

So "get past its login" is really two problems. The first is a classic login/list server, which the clean-room `seihai-listserver` / `seihai-gserver` family already speaks for the 2.x–6.0x tokens; whether 6.113's login-step token is classic or connector-supplied on that first hop is still open (see Open). The second is the connector signature, below.

## The connector request is deterministic across launches

**[lab]** The client builds its connector request — `GET /conf.gs?p=<opaque>` with `User-Agent: Graal/<version>` — in memory before it connects. Read from two **separate fresh launches** of the same build, the `?p=` value was **byte-for-byte identical** (a ~56-character string in the client's own base64 alphabet, i.e. DES-ECB ciphertext of the fixed `g=…,p=…,v=…,b=…` descriptor). It carries no per-launch nonce or timestamp.

This sharpens open item "what `?p=` binds": for 6.113 the **request** side binds nothing per launch. It is a pure function of the build (game, platform, version, build-date). That differs from the v7 observation that a reply "verifies only for the per-launch request it was signed for" (`v7-connector-live-20261111.md`); whatever per-launch binding exists for 7.x is **not** present in the 6.113 request. **[lab]**

## The token and framing are not in the client at all — shown from the other side

Earlier notes established this from the capture and the unpacked image (the eight token bytes are a `sendRaw` literal in the server's script, not a compiled-in client string: `v6113-hello.md`, `v6-login-token-explained.md`). The lab run confirms it from the negative direction: in a launch where **no connector reply was ever accepted**, a full scan of the running client's memory found **zero** occurrences of the token, of `setprotocol`, or of the `EILLLT` template. **[lab]** Until a signed script arrives and runs, the client simply does not hold the words it would put on the wire. The connector gate is therefore total: no reply, no token, no framing, no RC4.

## Replay, forge, and the only lab bypass

- **Forge a reply for a stock client — not possible.** The reply is a 4-byte marker, a 256-byte RSA-2048 signature over the **bare** SHA-256 of the payload (no DigestInfo), a length, and the encrypted script. The client checks the signature against a **public key compiled into the client** *before* it decrypts, and never runs a reply that fails (`connector-script.md` §2, `v6-login-token-explained.md`). Without the operator's private key you cannot make a payload a stock client will accept. **[bin][cap]**
- **Replay a genuine captured reply — not blocked at the request level for 6.113.** Because the request is deterministic (above), a genuine reply's signed payload stays valid on every later launch of the same build; the signature is over the payload, which does not change. This is unlike 7.x. The open caveat is whether the decrypted **script** itself carries a short-lived element the client re-checks (a clock or sequence value); that cannot be decided without a genuine reply in hand, which is owner-held and off-git. **[inf]**
- **Replacing the trust anchor — the clean-room repro, not the stock client.** Since the gate is the compiled-in public key, the clean-room repro drives its own client by trusting a lab key: it bakes in its **own** modulus and runs its **own** signed script (`graal-client-repro`, `Connector6113.pas`: "a stock connector reply does not verify against it, and a reply signed for this key is never accepted by a stock client"). The equivalent for the real packed client would have been an in-memory swap of the public modulus once Themida unpacked it. **That swap was tried on loopback and does not work** — the packer virtualizes verify and consumes the modulus inline, so the in-memory patch does not flip the verdict ([`v6113-login-lab-2026-11-19.md`](v6113-login-lab-2026-11-19.md)). So the anchor swap is a clean-room-repro technique only; a stock client still needs a genuine signed reply. **[bin][lab][inf]**

## Method (loopback only)

**[lab]** The real client is Themida/WinLicense-packed and 32-bit (WOW64 on a 64-bit guest). The run used the method in [`hypervisor-live-debug.md`](../client-internals/hypervisor-live-debug.md): a copy-on-write overlay of the lab Windows image (base read-only), a **restricted** user-mode NIC so the guest can reach only loopback forwards and never the public network, the connector/login host families redirected to a lab address via the guest hosts file, and the client's state read from host-side memory snapshots (no debugger inside the guest, so Themida's anti-debug is moot). A lab HTTP responder stands in for the connector; a 443 reset makes the client fall back to plain-HTTP `conf.gs`. All captures, keys and hosts stay off git.

## Still open (carried, not closed)

> **Update (2026-11-19, #510):** a loopback attempt at the trust-anchor swap below came back a
> decisive negative — the packer virtualizes the signature check and consumes the modulus
> inline, so an in-memory public-key swap does not flip the stock client's verdict. The
> stock-client anchor-swap path is therefore ruled out; see
> [`v6113-login-lab-2026-11-19.md`](v6113-login-lab-2026-11-19.md). The clean-room login
> handshake did run end to end there.

- A full end-to-end **logged-in** session of the *real* client in the lab. It needs the login/list gate served (the clean-room `seihai` stack) **and** the connector gate passed. The anchor-swap route is now ruled out for a stock client (see the 2026-11-19 update above), so this needs a genuine signed reply, which stays owner-held. **[lab]**
- The **post-RC4 login packet** of the real client (account/password framing, login-step argument order). It is runtime-only and still unread; the clean way to get it is to drive the real client with a connector script whose RC4 key the lab chose, then read the first encrypted send. Needs the bypass above. **[lab]**
- Whether 6.113's **first-hop login/list token** is classic or connector-supplied. **[lab]**
