# Static reads for Appendix E, thirteenth batch (2026-11-20)

Date: 2026-11-20. Evidence: **[bin]** (a linear disassembly of the x86-64 native engine library of
Android Classic 1.8, the package used in the 2026-11-20 emulator run, read with its exported
symbol names; no client run). Only behaviour is given here. Covers App. E#18.

The package carries one native engine library in four builds (ARM, ARM64, x86 and x86-64). It is
not encrypted, and its symbols are exported, so the connection class and its methods can be read
by name. Only the x86-64 build was read.

## The connection class

The engine has the same connection class as the 6.11 desktop clients. It has the same two framing
modes and the same script-facing calls:

- a classic mode, which is the default after every reset;
- a template mode, chosen by `setprotocol`, whose header template uses the letters `I`, `L`, `T`
  and `E` (→ §2.10.3);
- per-direction ciphers set by name, `RC4` or `AES`, with the parse key and TLS options;
- the connector start-up: `StartScript_Connector`, the fallback `StartScript_Fail`, the connector
  modes of the server list, and script-set outgoing id tables.

So Android Classic 1.8 is on the 6.1x connector line. This agrees with the emulator run, where it
fetched `conf.gs` first.

## The classic mode, sending

- **Messages.** Each message is the id + 32, then the data, then a line feed. They are added to an
  outgoing buffer. The buffer is packed into a frame once it holds 4,096 bytes or more, or when the
  connection is flushed.
- **Raw data.** A message whose data contains a line feed, and every message with id 93 or 163, is
  sent behind a message 50 that carries its length as three 7-bit characters. The length is the
  data length + 2, capped at 3,670,015.
- **The first message.** The first message after connecting gets one extra byte after its id: the
  connection's key + 32. The connector script picks the id and the data of that message; the
  engine does not build a login itself.
- **The key.** On reset, the key is the UTC time AND 127, so 0 to 127. On connect, the same key is
  used for the incoming direction. Both cipher states start at `0x04A80B38`.
- **Frame header.** A two-byte big-endian length, or `FF FF` and a four-byte big-endian length for
  a body over 65,534 bytes. Then comes a compression byte, unless a fixed type is set. The length
  includes the compression byte.
- **The first frame** uses fixed type 3: zlib, no cipher and no compression byte. After that frame
  the type goes back to automatic.
- **Automatic type:**
  - `06` (bzip2) when bzip2 is allowed and the body is at least 4,096 bytes;
  - otherwise `04` (zlib) when the body is at least 48 bytes;
  - otherwise `02` (no compression).
  - A per-connection flag turns compression off, which always gives `02`. What sets it was not
    traced.
- **Partial XOR.** Before each four-byte group the state becomes state × `0x08088405` + key, and the
  group is XORed with the state's bytes, least significant first. A raw body gets
  min(ceil(n / 4), 12) groups. A zlib or bzip2 body gets min(floor(n / 4), 4) groups. The XOR is
  applied after compression.

## The classic mode, receiving

- The receiver reads the two-byte length, or `FF FF` and four bytes, and waits for the whole body.
- Unless a fixed type is set, the first body byte is the type:
  - 1 and 2 are raw;
  - 3 and 4 are zlib;
  - 5 and 6 are bzip2.
  - The even types are XORed with the incoming state first, using the same group counts as sending.
- The plain body is split at line feeds. Each line is one message, with the first byte − 32 as its
  id. After a raw-length message, the next message is taken by length instead of by line feed.
- A zero or negative length, or a body that decodes to nothing, is logged as invalid data. The
  connection is then marked blocked and stops reading and sending.

## What this settles

- Before a connector script switches anything, Android Classic 1.8 frames, compresses and ciphers
  exactly as the desktop generation-5 clients do (→ §2.2.3). That includes the floor/ceil group
  counts of 5.12 and the Mac receivers, and the type-3 first frame with the key byte that iPhone
  Classic+ 1.13 uses.
- After the connector reply, the script can move the connection to template mode, RC4 or AES, or
  TLS, exactly as on 6.11.

## Not covered

- What the official connector script for Android chooses. The emulator run got no reply, so the
  mode, cipher and login id actually used on the live service are not known.
- The other six Android packages (Classic 1.6 to 2.2 and Era 1.7 and 2.0). They report the same
  engine line, but they were not read.
- The template mode's receive path in detail. Only its letters and its call into the ciphers were
  checked.
