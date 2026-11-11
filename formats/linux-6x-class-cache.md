# Linux 6.x class cache: packet 197, the 161 request and the stored-body CRC

This note carries the class side of the Linux 6.x script cache. The local-file helper itself is in [linux-603-local-cache-helper.md](linux-603-local-cache-helper.md); this note covers what the class path does around it. Everything here is a static reading of retained native code. No client, server or debugger was started for it.

Inputs: Linux 6.03r7 x64, executable SHA-256 `ceeaefeb2df0668c9de921d4b967c511f85b235b25a18563534eb2f09b619c50` (the same input as the local-file helper note and [the network GS2 probes](../protocol/linux-603-network-gs2.md)), and Linux 6.01r1 x86 for the delivery split below. Evidence `LNX603-CLASS-CACHE-20261109` and `LNX601-X86-DELIVERY-20261109`.

## How the writer and reader order the work

[bin] On Linux 6.03r7 x64 the cache writer transforms the class body first and then puts the eight-byte `GRESCR01` prefix in front of the transformed bytes. The reader checks the CRC before it calls its inverse-side block helper. So the CRC covers the **stored, transformed body**, not the plaintext. Older notes that say this build checks the plaintext after decryption are wrong for this input. The block transform itself was not identified, and no cipher name is assigned to it from its block size alone.

## Packet 197 and the zero CRC

[bin] Packet 197 parses its whole body as one metadata list, and the expected CRC is one of its fields. Unlike packet 140 (→ [the descriptor-length note](../protocol/linux-603-network-gs2.md)), it has no separate script-body split. The list parser handles commas and selected quote and escape characters, so the list is not a plain split on commas. Its full escaping grammar was not recovered.

[bin] When the expected CRC in packet 197 is zero, the class path does not call the validator at all. It goes to a path that deletes the cache entry, may load an empty program, and raises the class-loaded notification. When the expected CRC is non-zero, it has to equal the CRC of the stored body. A file that is only the eight-byte prefix has an empty body, whose CRC is zero, so it can never match a non-zero value. **On this path a header-only cache file can never be a class cache hit**, whichever CRC the server sends. This is a static conclusion; no file rejection or successful parse was observed.

## The class request on a cache miss

[bin] On a class cache miss the client sends logical id **161**. The body is the stored-body CRC of the cached file, written as five offset-integer bytes, then the class name. The generic packet table calls that field a modification time; on this path it is the CRC, and nothing here shows it to be a time. The class request number must not be applied to weapons, which use 158 on the Windows path studied in [windows-404r2-500r7-static-2026-11-09.md](../client-internals/windows-404r2-500r7-static-2026-11-09.md#500r7-script-container-and-cache).

## Linux 6.01 x86: two delivery shapes, one class store

[bin] In Linux 6.01r1 x86, packet 140 splits a descriptor from the remaining body (the descriptor length counts only the descriptor's own bytes, so the body starts two bytes later). Packet 197 parses its whole input into a larger metadata collection. The class branches of both packets lead to class lookup, storage, loading and a named class-loaded notification. So body delivery (140) and metadata and status (197) are two formats and should not be merged into one payload description.

[bin] The class store uses the modern class-code namespace. It is not the older web-level body cache in [gwebl001-cache.md](gwebl001-cache.md), and the two should not be equated. The named notification calls are static paths; their delivery to a script was not observed.

## Limits

- These are exact-input static readings. Cache fixtures, request and response completion, malformed files and script execution were not tested.
- Bytes that come out of the reader are compiled segment records. Removing the transport and cache layers does not turn them into source text.
- The 6.01 x86 threaded executor still does not reconstruct every indirect handler, so E#207 stays partial.
- These findings narrow E#202: on Linux 6.x, 197 is a metadata and status message with an expected CRC, and 140 carries the body. Whether other builds or server generations use 197 differently stays open.
