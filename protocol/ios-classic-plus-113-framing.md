# iPhone Classic+ 1.13: framing, compression and cipher

Date: 2026-11-19. Static read of the iPhone GraalOnline Classic+ 1.13 app (`G3D0208A`,
32-bit ARM, not FairPlay-encrypted). No device, emulator or capture. Issue #648, App. E#16
and E#18. Evidence `IOS-CLASSIC113-FRAMING-STATIC-20261119` ([index](../docs/evidence-index.tsv)).

## Summary

Classic+ 1.13 uses the **desktop generation-5 stream unchanged**: a two-byte big-endian
length, a compression byte (`0x02` none, `0x04` zlib, `0x06` bzip2), and the gen-5 partial
XOR with the Borland multiplier. The login is client type 5 with a key byte, sent as one
zlib frame with no compression byte and no XOR, exactly like 2.22 and later desktop
clients. One detail matches 5.12 and the Mac PowerPC builds rather than 2.22 and 6.x: a
compressed body steps the cipher once per **whole** 4-byte group (round down). **[bin]**

So the probe proxy (`tools/probe/gen5probe.py`) and a gen-5 lab server can already speak
to this client, and the open part of mobile research is now "get the app running", not
"learn the codec". **[bin][inf]**

## Connection object

The engine's connection object keeps two cipher states, one per direction. **[bin]**

| Field | Initial value | Changed by |
|---|---|---|
| receive iterator | `0x04A80B38` | each received frame |
| send iterator | `0x04A80B38` | each sent frame |
| send key | the current time in seconds, low 7 bits | — |
| receive key | 0 | set equal to the send key when the game connection opens |
| fixed frame type | 3 (login: zlib, no type byte, no XOR) | reset to 0 after the first flush |
| "first message" flag | set when the game connection opens | cleared after the first message |

The socket itself is a plain BSD socket wrapped in a CoreFoundation stream pair. The
engine also has a UDP `sendto` path in the same socket class. **[bin]**

## Messages

Every outgoing message is `GCHAR id` + body + `\n`, appended to an out buffer. **[bin]**

- A body containing `\n` is refused with "Illegal characters in the outgoing data",
  except for ids 93 and 163. Those two are preceded by id 50 (`PLI_RAWDATA`) with a
  three-byte length (7-bit groups, capped at 0x37FFFF), the same rule as 4.x and 6.x
  desktop clients (`v4x-clients.md`, `v6x-clients.md`). **[bin]**
- The out buffer is flushed when it reaches 0x1000 bytes or on an explicit flush.
- The **first** message after the connection opens gets one extra byte after its id:
  the send key + 32. That message is the login. **[bin]**

### Login

```
'%' (5 + 32)   key + 32   "G3D0208A"   GSTRING   GSTRING   identity trailer   '\n'
```

- 5 is the client type for generation-5 clients (gs2lib `PLTYPE_CLIENT3`). **[bin][srv]**
- The token's eight characters are appended one by one after the "Done." status line,
  as the [token study](../client-internals/iphone-version-tokens.md) found. **[bin]**
- The two GSTRINGs are the two getter values in
  [the login-construction note](../client-internals/classic-113-login-construction.md);
  by position in the gen-5 layout they are the account and the password. Their sources
  were not traced, so that naming is **[inf]**.
- The identity trailer is the serialized four-entry list from the same note. Its format
  is still open.
- The client then sends `PLI_LANGUAGE` (37) with its language name, as desktop clients
  do. **[bin]**

## Frames

### Header

| Bytes | Meaning |
|---|---|
| 2, big-endian | length of the rest of the frame; it counts the compression byte |
| `FF FF` + 4, big-endian | the same, for a frame whose length is above 0xFFFE |
| 1 | compression byte (absent while the fixed frame type is set, which is only the login) |

Both directions use the same header. The 4-byte form is the one desktop 6.x clients
added (`v6x-clients.md`). **[bin]**

### Compression choice when sending

| Body length (before compression) | Type |
|---|---|
| 47 bytes or less | `0x02`, uncompressed |
| 48 bytes up to 0xFFF | `0x04`, zlib |
| 0x1000 or more, when a global bzip2 switch and a per-connection flag are both on | `0x06`, bzip2 |
| 0x1000 or more otherwise | `0x04`, zlib |
| any, when the connection's "never compress" flag is set | `0x02` |

Unlike 2.22, a short body is never zlib-compressed to save bytes; 47 bytes is a hard
cut-off. zlib comes from the system library; bzip2 1.0.4 is linked into the app. **[bin]**

### Cipher

`it = it * 0x08088405 + key` (32-bit), then XOR four body bytes with the little-endian
bytes of `it`, for each group, after compression on send and before decompression on
receive. **[bin]**

| Type | Groups stepped and XORed |
|---|---|
| `0x02` | `min(ceil(len / 4), 12)`; a short last group is XORed byte by byte |
| `0x04`, `0x06` | `min(floor(len / 4), 4)`; a short last group is left as it is and does not step the iterator |

Both directions follow this rule. It is the 5.12 rule
([`gen5-cipher-step-5x.md`](gen5-cipher-step-5x.md)) and the Mac PowerPC rule
([`macos-ppc-receive-framing.md`](macos-ppc-receive-framing.md)), not the 2.22 rule in
[`codec-and-framing.md`](codec-and-framing.md#gen-45-partial-xor). The two differ only
for compressed bodies shorter than 16 bytes whose length is not a multiple of 4. A server
that compresses only bodies of 48 bytes or more never sends one, and this client never
sends one either, since it only compresses from 48 bytes up. **[bin][inf]**

### Receive

The receiver reads the header, removes the XOR, decompresses, and splits the body on
`\n`. The first byte of each line minus 32 is the packet id, passed to the engine's
dispatcher. A pending raw-data length (`PLO_RAWDATA`) makes the next message a counted
block instead of a line. **[bin]**

## What this settles

- App. E#18 for iPhone: the outer framing, compression and cipher are the desktop gen-5
  ones. Android is still unread (no Android package on the lab hosts).
- App. E#16: the lower sender and the login frame are traced; the account/password
  naming and the trailer format stay open.
- The proxy's existing gen-5 codec already uses round-down for compressed bodies, so it
  matches this client without a change.

## Open

- [ ] Run the app. The binary is 32-bit ARMv6 for iOS 3–5; there is no iOS emulator for
  it on the lab hosts, so a jailbroken 32-bit device or a full iOS emulator would be needed.
- [ ] Android Classic / Era: read the native engine's socket layer the same way, once a
  package is on a lab host.
- [ ] The identity trailer's four fields, and where the two GSTRINGs come from.
