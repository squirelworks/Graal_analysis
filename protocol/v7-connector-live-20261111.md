# v7 Worlds: live connector capture and online-play reach

Date: 2026-11-11

Target: `WorldsSetup64-614` (`Worlds.exe` + `Graal3DEngine.dll`), run in the Windows 10 RE Lab VM
with every DNS answer forced to loopback and lab HTTP/TLS listeners in front of it. Tags:
**[live]** this run · **[bin]** the unpacked `Graal3DEngine.dll` export/string inventory ·
**[doc]** prior 6.11 connector reading (`protocol/v6x-clients.md`, `protocol/v6113-hello.md`).

The real connector host names, the `?p=` request blob and the captured reply bodies are **not**
in this repository. They are kept in the private lab workspace. No client ever reached the
internet; the one real fetch was a user-authorised, one-off host-side `curl`-style replay of the
captured request, recorded privately.

No addresses in this file.

---

## 1. Self-identification **[live][bin]**

The v7 Worlds clients do **not** send a baked eight-character `G3D…`/`GNP…` login token of the
kind 2.x–6.03 use. On the wire to the connector they identify only by an HTTP `User-Agent`:

| Build | `User-Agent` | VERSIONINFO |
|---|---|---|
| 548, 610, 612 | `Graal/6.76` | `Graal` 6.114 |
| 613, 614, 71243 | `Graal/6.77` | `Graal` 6.114 |

The `User-Agent` version is a double formatted after the literal `User-Agent: Graal/`; the six
builds split 6.76 / 6.77 at build 613. Build 614 was confirmed `Graal/6.77` live. The VERSIONINFO
`6.114` is a separate product-version string and is the same across all six. **[bin]** for the
split, **[live]** for 614.

Because the client carries no token, there is nothing to add to `allowedversions.txt` for a v7
*client*: the login identity is built by the connector script at run time (`setloginaccount` /
`getpassword` / `senddata`, same surface as 6.11). `gs2lib` already carries upstream's
`G3D2204D` = `CLVER_WORLDS` ("Graal Worlds"); whether the production connector makes these Unity
builds send that exact token is **not** established. **[bin][doc]**

---

## 2. Connector request order **[live]**

On start-up build 614 did, in order:

1. a TCP connection and a 9-byte write to a non-connector address, then a 1-byte write (an
   unrelated local/update probe);
2. **TLS to the Worlds connector host on 443** (ClientHello carried that host as SNI);
3. on TLS failure, a **plain-HTTP `GET /conf.gs?p=<blob> HTTP/1.0`** to the same host, with
   `User-Agent: Graal/6.77` and `Connection: Keep-Alive`;
4. the same `GET` to a **second host** whose first label differs (the `…ios` → `…ios2` fallback).

This is the 6.11 connector design exactly: HTTPS first, plain-HTTP `/conf.gs` fallback, a second
host on failure, `User-Agent: Graal/<version>`. **[live]**, matching **[doc]**
`protocol/v6x-clients.md#connector-request`.

The `?p=` query is the 6.11 shape: a DES-ECB-then-client-base64-then-URL-encoded blob of
`g=…,p=…,v=…,b=…`. The compiled-in key was not recovered, so the blob is not decoded here. **[doc]**

---

## 3. The real reply container **[live]**

A single user-authorised host-side replay of the captured request returned, from
`Server: Graal-HTTP-Server 20130907`, `Content-Type: application/octet-stream`:

| Field | Value |
|---|---|
| Marker | 4 bytes `00 00 01 00` |
| RSA block | 256 bytes (RSA-2048) |
| Inner length | 4 bytes `00 00 <len16>` |
| Payload | `<len16>` bytes, high-entropy (~7.99 bits/byte), **not** ECB (no aligned block repeats within or across replies), different on every request |

`conf.gs` and `con.gs`/`con.png` returned the same container with different payload lengths.
This is byte-for-byte the container the 6.11 Mac client's connector reply uses (same `Server`
banner, same `00 00 01 00` marker, same per-response randomisation). **So one connector design
covers 6.11 and v7.** **[live]**, cross-referenced to the 6.11 capture.

The 256-byte block is an RSA-2048 **signature** the client verifies against a public key baked
into the client (the client exports `RsaSSL_Verify` and holds the key; the recovered private key
in the image is an unrelated pair). The payload is separately encrypted (AES-CBC or RC4; the
engine exports `AesCbcEncrypt`/`AesCbcDecrypt`/`Arc4Process` and selects between them). **[bin]**
for the primitive inventory; the exact payload cipher and whether the RSA block also wraps the
payload key is pending a client-side decrypt trace.

**Anti-tamper blocks an in-process inline-hook decrypt trace.** `Worlds.exe` ran for minutes and
reached the connector fetch under a Frida agent that hooked only `ws2_32.dll`. The instant that
agent placed inline hooks on the **engine's own** exports (`RsaSSL_Verify`, `AesCbcDecrypt`,
`Arc4SetKey`), the process exited ~15 s into start-up, before any networking, on three separate
runs. `Graal3DEngine.dll` carries Themida/WinLicense packer strings, so the shipped engine
self-checks its own code and terminates when its exported functions are inline-patched. A
**read-only memory scan** (no code patch) is tolerated and ran for the full session. **[live]**

**A replayed reply does not verify; the client falls to `StartScript_Fail`.** Serving the
genuine captured reply back to a fresh client instance on loopback, then scanning process memory,
found only the client's **built-in** connector skeleton and the fail path: the baked field names
`scriptip` / `scriptsslcipher` / `scriptsslsubject` / `scriptsslissuer`, the string
`Problem setting up the networking`, and GUI `onCreated` scripts. None of `connecttogameserver`,
`setprotocol`, `setoutdatahandlers`, a game host/port or any server-supplied `StartScript_Connector`
body ever appeared, across six scans over two minutes. So the client **rejected** the replayed
reply: the RSA signature is bound to the specific request (its per-request `?p=` nonce/time), not
to the body alone, so a reply captured for one request cannot be replayed to another. This both
reconfirms the sign-with-server-private-key verdict and means a captured genuine reply is **not**
a shortcut to the decrypted connector script. **[live][inf]**

---

## 4. Online-play reach **[live][inf]**

A **stock, unmodified v7 Worlds client cannot be brought online against a lab server.** The
client verifies the connector reply's RSA signature against GraalOnline's public key; producing a
reply the client accepts needs the matching **private** signing key, which is held only by the
official server. A lab `/conf.gs` responder therefore cannot satisfy the check. The only routes to
a working client are:

1. **patch the client** — replace the baked signing public key with one whose private half we
   generate, and sign our own connector replies; or
2. **build a reproduction client** (`graal-client-repro`) that speaks the post-connector game
   protocol directly, skipping the connector/verify gate.

Route 2 is the realistic v7 target. The post-connector game protocol itself (framing, remapper,
PLO/PLI, GS2/GRESCR, ciphers) is already mapped from the binary in the sibling v7 notes; what the
reproduction client additionally needs is the decrypted connector script's own output — the game
host/port and the login the script builds — which a client-side decrypt trace of the genuine
reply can supply without any patch and without network access.

---

## 5. Open

1. Client-side decrypt trace, by a method the engine's Themida anti-tamper tolerates
   (hardware breakpoint, or a targeted post-decrypt memory scan of the live network/script
   buffers, not inline hooks and not a reply replay): dump the plaintext connector script, the
   game server host/port it names, and the login it builds. This requires driving the client
   against a lab that completes the connector handshake the client accepts, i.e. a patched client
   (route 1 in §4), since an unpatched client rejects any reply we can serve.
2. Confirm whether the production connector makes these builds send `G3D2204D` or another token.
3. The `?p=` compiled-in DES key (shared with the 6.11 work).
