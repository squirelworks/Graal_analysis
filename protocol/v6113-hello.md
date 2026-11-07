# How unpacked Windows 6.1.1.3 sends GNP1905C

Date: 2026-11-07. Static read of the unpacked 6.1.1.3 listing and the unpacked 6.0.3.7 listing, set against the port 14900 capture. Nothing was run. Tags: **[bin]** the two listings · **[cap]** `protocol/v6113-list-capture.md`.

## The eight characters

The capture's first eight bytes are `GNP1905C`, the same on both answered sessions, written before the client has read any server byte. **[cap]** (`protocol/v6113-list-capture.md#the-clear-hello`)

Those eight characters are not a literal in the 6.1.1.3 image. The length-and-position string decoder is in this image: the same pass recovers `sendraw`, `senddata` and `setprotocol`. No stored string decodes to `GNP1905C` or `gnp1905c`, and no instruction writes those eight characters one by one. The number `graalversion` returns is 6.113. No builder in this image turns 6.113 into the digits `1905`. How those four digits and the final letter are chosen: not found. **[bin]**

`sendraw` is the native path that can put those eight bytes on the socket. After `setprotocol` has switched the connection, a send whose id is −1 appends the caller's bytes and adds neither a packet id nor a header. A numbered send, while the template has not yet supplied both a length field and a packet-id field, is refused with "Cannot send data, socket is not in a state where data can be sent". The caller that supplies `GNP1905C` is not in this image. **[bin]**

## Against unpacked 6.0.3.7

Unpacked 6.0.3.7 stores one scrambled eight-byte string. The same decoder yields `g3d0311c`. The login constructor decodes that string, upper-cases the buffer, and sends the result as packet id 5. All eight characters are constants in the stored string. The prefix `g3d`, the digits `0311` and the final `c` are not computed from the version words. Unpacked 6.1.1.3 has no string that decodes to a `G3D` or `GNP` token, and it has no id-5 constructor of that shape. **[bin]**

## The six bytes after the token

The capture's next bytes are the six-byte header `01 02 00 01 17 fd`, then a zlib member `78 9c` of 273 bytes that inflates to 262. The inflated bytes start `00 01 00 01 06 fc` and then 256 bytes that differ between the two sessions. **[cap]** (`protocol/v6113-list-capture.md#the-clear-hello`)

`setprotocol` switches the connection off the generation-5 framer. The header is as long as the template the caller passes. Each of `I`, `L`, `T` and `E` is one big-endian field, one to four bytes wide, the width being how many times the letter is repeated:

| Letter | What is written |
| --- | --- |
| `I` | A packet counter. It starts at 1 and increases by one on each numbered send |
| `L` | The header length plus the body length |
| `T` | The packet id |
| `E` | 0, 1 or 2 |

`E` is 1 when the body is at least 48 bytes and the packet id equals one id stored on the connection. `E` is 2 when that same id matches, a global flag is set, a second flag on the connection is set, and the body is at least 4096 bytes. Otherwise `E` is 0. `E` 1 compresses the body with zlib `compress`. `E` 2 compresses it with bzip2 at block size 5. The linked zlib text is 1.2.5. **[bin]**

The template string is not in the image, so this listing does not assign the six captured bytes to `I`, `L`, `T` and `E`. The length rule is consistent with the capture: a 6-byte header plus the 273-byte zlib member is 279, and 279 is `01 17`, which sits in that header. That is a size check, not a recovered template. **[bin][cap]**

The bytes `78 9c` are a zlib header. They match what zlib `compress` writes, and they also match a zlib member that was already the body of an `E` 0 send. Which of those two produced this member: not found. What builds the inflated 262 bytes, the six-byte prefix and the 256 bytes after it: not found. **[bin][cap]**

## What the cipher is

A new connection starts on the generation-5 framer. Both directions take the shared seed, the step is that state times the Borland multiplier plus the key, and the key is a random value kept to 7 bits. The mode field starts at 3, the login frame the 6.01 and 6.03 notes describe (a length and a zlib member, no cipher). In the later mode, a short frame is XORed for at most 12 dwords and a zlib or bzip2 frame for at most 4. A packet is the id plus 32, the body, and a newline. **[bin]** (`protocol/v6x-clients.md#cipher-and-framing-classic-mode`)

`setencryptionout` selects the cipher for the new-protocol mode by a name the caller passes. The names in this image are `AES` and `RC4`. Any other name clears it. The key and the initial value come from the caller. Nothing in the connect path shows which name, key or initial value the 6.113 session used. **[bin]**

The capture already shows that the bytes after the hello are not the generation-5 partial XOR. The listing agrees: that XOR belongs to the framer `setprotocol` replaces, and the six-byte header belongs to the replacement. The cipher on the bytes after the zlib member: not found. **[bin][cap]** (`protocol/v6113-list-capture.md#what-stays-ciphertext`)
