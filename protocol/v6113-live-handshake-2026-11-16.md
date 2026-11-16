# Windows 6.113 live handshake confirm (2026-11-16)

Date: 2026-11-16. Derived wire behaviour from an owner-held official Windows
6.1.1.3 live capture after Login. Captures, keys, cache bodies, digests, hosts
and machine paths stay off git. Tags: **[cap]** this run · **[cap]** prior
Windows 6.113 captures · **[lab]** Mac 6.111 offline cipher work · **[bin]**
existing connector / hello notes · **[inf]** where length rules out AES.

Companion status hub: [`v6113-status.md`](v6113-status.md). Clear-prefix /
RC4 boundary: [`v611-outgoing-cipher.md`](v611-outgoing-cipher.md). Earlier
14900 capture shape: [`v6113-list-capture.md`](v6113-list-capture.md). Live
connector-before-Login check (same day, different claim):
[`v6113-live-connector-2026-11-16.md`](v6113-live-connector-2026-11-16.md).

## What this settles

| Claim | Status |
| --- | --- |
| Official Windows 6.113 on `HOST:14900` still opens with clear `GNP1905C`, then one clear zlib-wrapped outer `EILLLT` (`E=1`, `T=0xfd`, `LLL=279`) | Settled again **[cap]** (2026-11-16) |
| Client→server RC4 begins at stream offset **287**; the second TCP write may carry the clear 279-byte wrapper plus a short ciphertext tail | Settled again **[cap]** |
| One capture held three answered `HOST:14900` sessions and one unanswered SYN | Settled **[cap]** |
| After owner Login the session stayed on `HOST:14900` (no `HOST:14911` / `HOST:14912` in that file) while server→client volume grew | Settled for this file **[cap]** |
| Server’s first clear reply is also `EILLLT` with `T=0xfd`; later bytes are opaque | Settled again **[cap]** |
| Early sessions show post-hello client writes of length 7, which does not fit AES block padding on this path | Settled again **[cap][inf]** (plain RC4, not TLS/AES framing) |
| This pass does **not** recover session keys and does **not** decrypt post-287 traffic | Explicit non-result **[cap]** |

This does **not** close the loopback `conf.gs` harness, login-step argument
order, `?p=` binding, connector plaintext, or the post-decrypt Login / play
reply contract. Those stay open in `v6113-status.md`.

## Live path (structure only)

1. Stock official Windows 6.113 client spoke first on `HOST:14900`.
2. Every answered session used the same clear hello shape already recorded for
   6.11: eight-byte token, then one outer framed packet, then ciphertext.
3. After Login, the largest answered session stayed on that same port while
   server→client bytes grew into the in-world / asset range. No separate game
   port appeared in this file. **[cap]**

Nothing in this note names a host, prints a key, dumps a payload, or cites a
private capture file.

## Clear hello shape (all answered sessions)

Client always speaks first, in **two** TCP writes:

1. Length 8 — clear token `GNP1905C` (no header). Same literal the connector
   script’s `sendRaw` is already known to supply (`v6113-hello.md`,
   `v6-login-token-explained.md`). **[cap][bin]**
2. A second write that begins as outer `EILLLT`:
   - `E=1` (zlib)
   - `I=2`
   - `LLL=279` (six-byte header + 273-byte zlib member)
   - `T=0xfd` (bundle)
   - First **279** bytes = clear wrapper
   - Remainder in the same TCP write = ciphertext tail → stream offset
     **287** is the RC4 boundary (same cut as `v611-outgoing-cipher.md`)

No second clear `GNP*` / `G3D*` token appears later in any answered stream.
**[cap]**

That matches the 2026-11-07 Windows 6.113 port-14900 note and the Mac 6.111
lab cipher boundary. This run is a live reconfirm on official 6.113 after
Login, not a new framing. **[cap][lab]**

## Server first clear reply

The server’s first payload is still clear `EILLLT` with `T=0xfd`. Observed
first-write lengths on this pass:

| Role (inferred) | First S→C clear length | Outer shape |
| --- | ---: | --- |
| Early Login-server session | 291 | `EILLLT`, `T=0xfd`, entire first write clear |
| Second Login-server session | 291 | same |
| Post-Login / bulk session | 279 | same outer form as the client’s clear wrapper |

After that first clear server frame, subsequent head bytes are opaque in both
directions — consistent with RC4 after the connector’s `setEncryptionOut`
switch, headers included. **[cap][lab]**

## Session layout on `HOST:14900`

| Item | Count / value |
| --- | --- |
| Answered data-bearing TCP sessions | **3** |
| Unanswered SYN-only attempt | **1** |
| Post-Login port jump to `HOST:14911` / `HOST:14912` | **none** in this file |

Rough payload roles (byte counts are structure only; no bodies):

| Session | Approximate role |
| --- | --- |
| First answered | early Login-server exchange |
| Second answered | second Login-server exchange |
| Third answered | post-Login / in-world bulk (largest server→client volume) |

The unanswered SYN is a connect attempt with no payload and no answer in the
file. It does not change the hello shape on the three answered sessions.
**[cap]**

Earlier same-day detours that touched other service ports are **not** this
official path and are not used as evidence here.

## Cipher markers (no key recovery)

- Post-hello **client→server length-7** writes appear on the early answered
  sessions and not on the post-Login bulk window scanned here. A 7-byte write
  is incompatible with AES block padding; it agrees with the held finding that
  the 6.11 login path uses **plain RC4**, not AES/TLS, on this socket.
  **[cap][bin][inf]**
- No TLS record on `HOST:14900`. **[cap]**
- zlib magic appears inside the clear hello segment(s), not as a recurring
  clear framing after the switch. **[cap]**
- Wire bytes never show plaintext `setEncryptionOut` / `setProtocol` /
  `sendRaw` strings after the hello (those live in the connector script;
  order already documented in `connector-script.md` / `v611-outgoing-cipher.md`).
  **[cap][lab]**

This pass does **not** newly identify the RC4 key, does **not** decrypt
post-287 traffic, and does **not** expose a clear connector `conf.gs` body.
**[cap]**

## Against prior notes

| Prior claim | This live confirm |
| --- | --- |
| `v6113-list-capture.md`: clear `GNP1905C` + six-byte header + zlib, then opaque bytes on `HOST:14900` | Same clear hello; RC4 cut named at offset **287**; three answered sessions + one unanswered SYN again |
| `v611-outgoing-cipher.md`: clear prefix ends at 287; plain RC4; 7-byte writes rule out AES | Reconfirmed on official Windows 6.113 after Login **[cap]** |
| `v6113-status.md`: cipher/hello settled; live harness still open | Hello/cipher reconfirm only; loopback harness and post-decrypt Login replies stay open |
| `v6113-live-connector-2026-11-16.md`: connector still served before Login UI | Complementary: that note is cache/UI; this note is the `HOST:14900` handshake after connect |

## Still open (unchanged)

1. Session RC4 key material / decrypted post-287 stream / clear `tclient_set*`
   wire ids and bodies. **[lab]**
2. Cleartext `conf.gs` / decrypted connector start-script for a loopback
   responder seed. **[lab]**
3. Whether some other official path ever hands off to a separate game port
   after Login (this file stayed on `HOST:14900`). **[cap][inf]**
4. First Login / play replies a 6.113 client needs after decrypt, versus
   6.037 — still the open half of #510. **[lab]**

## Non-goals / scrub

- No hosts, IPs, digests, key bytes, account names, raw cache bodies, private
  capture filenames or machine paths in this note.
- No decompile text, no binary addresses, no third-party REA copy.
- No claim that Gen5 `G3D0311C` labs stand in for this path
  (`v6113-status.md`).
- No publication of decrypts; the explicit result is that none were recovered
  here.
