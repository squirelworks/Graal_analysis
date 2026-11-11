# Where the 6.11 client's outgoing cipher starts

Date: 2026-11-11. Tags: **[cap]** the Windows 6.113 port 14900 capture (`v6113-list-capture.md`) · **[lab]** an offline replay of a captured connector reply to a lab Mac client (6.111, unmodified), owner-held record · **[bin]** the client notes cited below · **[inf]** inference.

Short answer: the client sends the token and one framed packet in the clear. Every byte after that packet is RC4 ciphertext, headers included. On the wire that is stream offset **287**. The RC4 key is 16 bytes, made fresh for each session.

## The clear prefix

The same 287 bytes open every 6.11 client stream we have: two answered Windows 6.113 sessions **[cap]** and six Mac 6.111 sessions **[lab]**.

| Stream offset | Bytes | What it is |
| --- | --- | --- |
| 0–7 | `GNP1905C` | The token, written by `sendRaw`: no header, no id |
| 8–13 | `01 02 00 01 17 fd` | `EILLLT` header: `E` 1 (zlib), `I` 2, `LLL` 279, `T` 0xfd |
| 14–286 | 273 bytes, `78 9c …` | The zlib body of that packet |
| 287 on | everything else | RC4 ciphertext |

The `EILLLT` template is the one the connector script passes to `setProtocol` (`v6-login-token-explained.md`). Each letter is one byte. `E` is the compression byte, `I` the packet counter, `LLL` the big-endian length of header plus body, and `T` the packet id. The prefix confirms that assignment twice over. The outer header's `LLL` is 279, which is 6 + 273. The inflated body is itself a packet whose header has the same shape **[cap][lab]**.

## A packet inside a packet

The zlib body inflates to 262 bytes: `00 01 00 01 06 fc`, then 256 bytes. That is an inner `EILLLT` packet: `E` 0, `I` 1, `LLL` 262, `T` 0xfc, and a 256-byte body. The body changes in every session **[cap][lab]**.

Outer and inner packets draw from **one counter**. The inner 0xfc packet takes 1 and the clear outer 0xfd wrapper takes 2. After the switch, in the decrypted Mac stream, an outer 0xfd takes 4 and wraps an inner packet numbered 3 (id 0x05). A later outer 0xfd takes 8 and wraps inner packets 5 (id 0x25), 6 and 7 (id 0x17). Every outer packet the client sent was id 0xfd with `E` 1, and the packets inside were `E` 0. So a reader that walks only the outer packets sees counters 2, 4, 8, not 2, 3, 4 **[lab]**.

Each outer packet left the client in its own TCP write **[lab]**.

## The switch

The connector script runs, in this order: `setProtocol("EILLLT")`, `sendRaw("GNP1905C")`, `flush`, `setEncryptionParseKey` with cipher type `"RC4"` and a key from `generate16ByteKey()`, `rsa_encrypt`, `sendData`, `setEncryptionOut`. The argument order was not read from the bytecode. The order above comes from the script's string table **[lab]**.

That order explains the boundary. The 0xfc/0xfd packet goes out before `setEncryptionOut`, so it is clear. Everything queued after it is encrypted **[lab][inf]**.

## The cipher

- **RC4.** In one live Mac session the client called its RC4 set-key routine and never called its AES set-key routine. The 16-byte key it set decrypts that session's client stream from offset 287 to the last byte. The keystream starts fresh at 287, and the plaintext is a complete chain of `EILLLT` packets **[lab]**.
- **Plain RC4.** The standard key schedule, no bytes dropped. **[lab]**
- **No IV.** `setEncryptionOut(type, key, iv)` passes only the key to RC4. The IV is used only for `AES`, which this script did not choose **[lab][bin]**.
- **Headers are encrypted.** After 287 the six-byte headers are ciphertext like the bodies **[lab][cap]**.
- **One key per session.** The same key decrypts none of eight other recorded sessions **[lab]**.
- The 6.113 capture agrees without a key. Its later client segments include 7-byte writes, and 6.11's `AES` pads to 16-byte blocks (`v6x-clients.md`, "What the script controls"). A 7-byte write cannot be one **[cap][bin][inf]**.

## The ids 0xfc and 0xfd have gs2lib names **[srv][inf]**

The `T` byte of an `EILLLT` header is the raw id, with no +32. gs2lib's client-to-server enum has the same two ids: 252 = `PLI_SET_ENC_KEY` ("Set AES / RC4 encryption key and init vector") and 253 = `PLI_BUNDLE` ("Bundled packets contain multiple packets"). Neither has a handler in GServer-v2 `master` or `beta4` (also noted in the Reborn protocol docs, `versions-encryption.md`). They match what this note sees: 0xfc carries the 256-byte wrapped RC4 session key, and every outer packet is 0xfd wrapping inner packets. So the enum names look like the 6.11 handshake as the original server knew it. That is an inference from the names and the shapes. No original server code has been seen.

## The 256-byte body

The script makes the RC4 key with `generate16ByteKey`, and calls `rsa_encrypt` with a 2048-bit public key (exponent 65537) that the script carries. The 0xfc body is 256 bytes, the size of one RSA-2048 block, and is not the raw RSA of the key, so a padding scheme is used. The reading that fits is that the 0xfc body carries the session key encrypted to the operator's public key. That could not be proved without the matching private key **[lab][inf]**.

What follows for a server **[inf]**: a server that answers a stock 6.11 client must recover the session key from the 0xfc body. That needs the private key matching the public key in the signed connector script. A lab server does not have it, so it cannot read a stock client's encrypted stream.

## Open points

- [ ] Decrypt the Windows 6.113 capture itself. That needs the session key of that exact session, read from the running client.
- [ ] The incoming direction. The script table holds no `setencryptionin` or `tclient_setencryptionin` name, and the lab server never answered in the 6.11 framing. The server's first packet in the 6.113 capture has the same clear shape (`01 02 00 01 21 fd`), but whether the server's stream after it is RC4 with the same key, or another key, is not known.
- [ ] The padding scheme inside the 0xfc body.

## Method notes

The lab Mac run was offline. The client loaded a previously captured connector reply from a loopback responder, and its game connection went to a sink that sent nothing. The session key was read when the client set it, with hardware breakpoints on the client's RC4 and AES set-key routines through the VM's debugger stub. A memory dump taken during the session alone did not show the key or the RC4 state. No key, capture, host or dump is published.
