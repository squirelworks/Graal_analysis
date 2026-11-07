# A 6.113 session on port 14900

Date: 2026-11-07. One capture the owner supplied, about 84.5 seconds, 1086 frames. Nothing was run from this repo. Tags: **[cap]** this capture · **[bin]** the client notes cited below · **[doc]** the listserver note · **[srv]** the generation table.

The packed listing still has no login builder (`protocol/v6113-wire.md`). This page is what a running 6.113 client sent on port 14900 the same day. Hosts, addresses, accounts and the session bytes are left out.

## What the capture shows

TCP only. No UDP. No TLS record. The first client bytes are the eight-character token `GNP1905C`, not a TLS handshake.

Three connections, all opened by the client:

| Order | What happened | Payloads |
| --- | --- | --- |
| 1 | SYN to one host on port 14900. No SYN-ACK, no payload and no reset in the capture. The next SYN is 1.063 s later | none |
| 2 | Full session to a second host, also port 14900. Round trip about 0.23 s. The client sends FIN 7.5 s after its SYN, then RST; the server's FIN follows. A new SYN starts 4 ms after that FIN | client 2005 bytes, server 669937 bytes |
| 3 | Second full session to that same second host. Same hello. Lasts 75.9 s. The client sends FIN, then RST. No server FIN in the capture | client 3459 bytes, server 1114913 bytes |

The client speaks first on both completed sessions. The server's first payload is 289 bytes on the first of those sessions and 290 bytes on the second, 0.32 s and 0.27 s after the client's first byte.

## The clear hello

Both completed sessions use the same clear prefix. The client sends it before reading any server byte, in two TCP segments: the eight-byte token, then the header, the zlib block and the start of the ciphertext (176 bytes on the first answered session, 198 on the second).

```
47 4e 50 31 39 30 35 43   01 02 00 01 17 fd   78 9c …
G N  P  1  9  0  5  C
```

- Eight ASCII bytes, `GNP1905C`, the same both times. Not a `G3D` token.
- Six header bytes, `01 02 00 01 17 fd`, the same both times. The four-byte sequence `01 02 00 01` occurs once per direction and nowhere else in either session.
- One zlib stream, header `78 9c`, 273 bytes on the wire, inflating to 262 bytes. The stream is self-delimited. Both sessions use those same sizes.

The inflated 262 bytes start with six constant bytes, `00 01 00 01 06 fc`, then 256 bytes. Those 256 bytes differ between the two sessions at 253 positions, and the zlib step does not shrink them. They are not an account, a password, a nickname or a printable platform list. This note does not record them.

The server does not send the token. Its first six bytes are `01 02 00 01 21 fd` on the first answered session and `01 02 00 01 22 fd` on the second. Every header, client and server, ends in `fd`. The byte before that is `17` from the client, `21` from the server the first time and `22` the second time.

## What stays ciphertext

After that prefix the bytes are opaque.

- The client's remaining 1718 and 3172 bytes are not a second zlib stream and do not break into length-prefixed clear frames.
- The server's remaining bytes, about 670 KB and then about 1.1 MB, contain no eight-zero run and no repeated 16-byte block. A generation-5 partial XOR leaves a zlib header or clear text after a few dwords. Neither is present.
- A search of both directions finds no second `GNP1905C`, no `G3D` token, no `GNW30123`, no `newmain`, and none of the level, web-cache, package or script-cache magics named in the 6.x notes.

No PLO id, no PLI id, no property stream and no file-transfer frame is visible. On the longer session the client's later segments are often 7 or 28 bytes, and the server sends segments of tens of kilobytes. Those are ciphertext lengths, not packet ids.

The cipher is not identified. It is not the generation-5 compression byte plus partial XOR, and it is not TLS. Generation 6 is the name the server table leaves unknown (`protocol/codec-and-framing.md`). These bytes do not supply that scheme.

## Against the 6.0x notes

`protocol/v6x-clients.md` and `protocol/v5v6-windows-unpacked.md` describe 6.01, 6.03 and the Windows captures through 6.03r7. They do not describe this session.

| What those notes say | What this capture shows |
| --- | --- |
| Login is id 5 in one clear zlib frame: a key byte, an eight-character `G3D` token (`G3D0108A`, `G3D0511C`, `G3D0311C`, `G3D26090`), then account and password lengths. Id 37 follows. **[bin][cap]** | The clear text is `GNP1905C`, a six-byte header and 256 session bytes. No id byte, no key byte, no `G3D` token, no account field |
| The Linux note calls the key a 7-bit random value. The Windows captures send it as a GCHAR, the wire byte minus 32. **[bin][cap]** | Neither form is in the clear prefix. That disagreement is unchanged. The 6.113 listing also has no key byte (`protocol/v6113-wire.md#contradictions`) |
| After login, generation 5: a compression byte, a short XOR, then packets as id plus 32 and a newline. **[bin][cap]** | Not this framing. The only clear zlib is the hello, and its header is `78 9c` rather than the best-level `78 da` of the older list frames |
| 6.03 stores three login hosts and walks them on failure, port 14900. **[bin]** | Two hosts appear. The first does not answer. The second accepts both sessions. A third host is not in the file |
| 6.11 may wrap the game socket in TLS, RC4 or AES after an HTTPS connector. **[bin]** | This file is a single TCP port, and the first bytes are not TLS. The connector exchange is not in the capture. The packed stub's export names are still not a cipher (`protocol/v6113-wire.md#server-defined-protocol`) |

The static read stands. The 6.113 listing contains no token. The running client sends `GNP1905C` anyway. A 6.03 `G3D` token is the wrong label for this session, and `GNP1905C` is not a string to copy back into the stub.

## Against the listserver note

`protocol/listserver.md` describes a different socket. The classic client list uses ids 0, 1 and 7, the names `newmain` and `GNW30123`, and ports 14921 to 14923. **[doc]** From 4.x, port 14900 is a game server the client treats as Login, and the server list arrives inside that session. **[bin]**

This capture is that port. Both completed sessions start with the same `GNP1905C` hello. There is no clear id 0 list, no id 2 status and no id 1 account frame. The client opens the second session as it closes the first, so the two sessions are not a list handshake followed by a different clear game protocol. Anything that distinguishes them sits in the ciphertext.
