# Android Classic and Era: the socket layer

Date: 2026-11-20. Tracker: [#648](https://github.com/squirelworks/Graal_analysis/issues/648); App. E#18. Tags: **[bin]** (static read of the held Android packages' native engine libraries, no run) and **[lab]** (the 2026-11-20 Android-x86 emulator run on loopback, `lab-appe-gwentea2-2026-11-20d.md`).

The GraalOnline Classic 1.8 x86_64 engine library keeps its C++ symbols, so it was read first. The other held packages and ABIs were checked against it.

## What the native engine is

The Android native engine is the desktop 6.x code base. Its connection class carries both desktop stream parsers: the classic one and the 6.1x connector one. **[bin]**

## The classic stream (generation 5)

This is the desktop generation-5 frame, the same as on 2.22, 5.x and 6.x (→ manual §2.2.3). **[bin]**

- Each frame is a two-byte big-endian length, then a compression byte: 2 raw, 4 zlib, 6 bzip2.
- The body is XORed with the `0x08088405` LCG keystream, seeded `0x04A80B38`.
- Steps are capped at 12 four-byte groups for a raw body and 4 for a compressed one. A compressed body's step count rounds down, as in 4.x, 5.12 and the Mac builds.
- The seed and multiplier are constants in every held package and every ABI, so every Android library carries this codec.

## The connector stream

The second parser is the 6.1x connector framer. It follows the protocol template the connector script sets (→ manual §2.10). Its zlib threshold is 48 bytes and its bzip2 threshold 4096, both stored as data. **[bin]**

The crypto present is the full 6.1x connector set:
- RC4, AES-CBC, DES-ECB and RSA verify and decrypt;
- base64, MD5 and SHA-256;
- the set-encryption key and parse routines the connector script calls (`protocol/connector-script.md`).

**[bin]**

## Login and token

There is **no compiled-in version token** in the library: no `G3D…` or `GNP…` string. The only version string is the HTTP user agent. The login is built from the connector script the server supplies (`StartScript_Connector`), so its bytes are whatever that signed script sends. **[bin]**

Android Classic 1.8 is therefore a connector client with no client-side token. That closes the token item of `../client-internals/android-login-token-boundary.md` as a documented no-token family.

## On the wire (lab)

Classic 1.8 starts with a TLS ClientHello without SNI to `<connector-host>` on 443. When that fails, it sends a plain `GET /conf.gs?p=<base64> HTTP/1.0` with `Host: <connector-host>` and `User-Agent: Graal/6.15401`. With no signed `conf.gs` reply it stays on "connecting" and never opens a game socket, the same connector wall as desktop 6.113. So the generation-5 game framing above was read but not seen on the wire. **[lab]**

## For the probe proxy

No new codec is needed. Once a game socket is open, `tools/probe/gen5probe.py` already decodes this framing, including the 12 and 4 caps and the rounded-down compressed count. What is missing is a way past the signed connector: a reply signed with the operator key, which is not held, or the patched-client key swap used for desktop 6.113. Until then no Android game session can be swept. **[inf]**

The `p=` value uses the same unrecovered DES key as the 6.11 and v7 work.
