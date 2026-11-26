# Our Frankenstein 6.037 vs the stock 6.03r7 RETAIL client: ours is an unpacked from-source 3D-capable hybrid, retail is a QPlay/CyaSSL-packed 2D Quattro binary (T3D-132)

Date: 2026-11-26. Static read (no client/VM run) comparing our own "Frankenstein 6.037" build against the **stock 6.03r7 retail client as a real user runs it** — the packed `Graal 6.0.3.7.exe` upload (`client-internals/skipped-v6-read.md`, `client-internals/packed-6037.md`) — rather than against the unpacked 6.00 engine already covered by [T3D-122](3d-frankenstein-6037-vs-600-2026-11-26.md). Builds on [T3D-121](3d-v6-quattro-vs-512-2026-11-26.md) (the unpacked 6.03r7 client is Quattro 2D) and [T3D-122](3d-frankenstein-6037-vs-600-2026-11-26.md) (our build is a from-source Quattro+proto-24 hybrid). Conceptual only. Board row: [T3D-132](3d-capability-board.tsv).

## Headline

Against **what a real 6.03r7 user actually runs**, our Frankenstein 6.037 differs on two axes at once: **packaging/transport** (new here) and **3D capability** (same verdict as [T3D-122](3d-frankenstein-6037-vs-600-2026-11-26.md)).

- **Packaging:** the retail 6.03r7 ships as a **multi-layer packed binary** — a self-decrypting stub, scrambled section names, and a **QPlay/CyaSSL** TLS+compression export surface — whose version resource calls itself `Graal.exe`. Our build is a **plain unpacked native executable** with ordinary C++ symbols and **no packer markers at all**, naming itself `Frankenstein 6.0` / 6.037, version 0.0.1.
- **Secure transport:** the retail stub embeds a **CyaSSL (wolfSSL) TLS stack** (SSLv3 client, RSA/ARC4/MD5/SHA, zlib inflate/deflate) as its `QPlay.exe` secure-channel layer. Our build carries **none of that** — its 3D half is the 5.12 proto-24 **plaintext UDP+TCP dual link**, its 2D half the Quattro session.
- **3D:** underneath the packer the retail is the **Quattro 2D engine** (no Torque class set, no proto-24 — [T3D-121](3d-v6-quattro-vs-512-2026-11-26.md)); ours **adds the whole proto-24 3D stack** ([T3D-122](3d-frankenstein-6037-vs-600-2026-11-26.md)). So the 3D delta vs retail is the same as vs stock 6.00.

## 1. What "stock 6.03r7 retail" is on disk **[bin]**

The uploaded `Graal 6.0.3.7.exe` is **not the engine** — it is the packed outer shell (`client-internals/skipped-v6-read.md`):

- **Self-decrypting stub.** Entry calls one helper, then a breakpoint; the helper walks ~4 KB a dword at a time, xoring and adding a constant. No second image is exposed to the decompiler past the breakpoint — the real engine is only reconstructed at run time.
- **Scrambled sections.** Section names are not `UPX0`/`.text`; each image has two scrambled section names plus `.rsrc` and `.idata`. The 6.037 file imports only `DebugBreak`.
- **QPlay/CyaSSL export directory.** The export directory is named `QPlay.exe` (while the version resource still says `Graal.exe`). It is a **TLS + compression surface**, not a list of Graal classes: a CyaSSL context, certificates/keys, an SSLv3 client method, connect/read/write/shutdown, plus RSA, ARC4, MD5, SHA, a RNG, and zlib inflate/deflate. The bytes at those exports are not that library in the clear (anti-analysis).
- **Engine absent from the listing.** No OpenGL/Direct3D import, no FMOD, no GS2 control name, no `TSocket`, no Torque class, no protocol id in the packed file — all of that lives in the engine the stub unpacks at run time, which is the Quattro 2D engine ([T3D-121](3d-v6-quattro-vs-512-2026-11-26.md): the unpacked 6.03r7 client, token `G3D0311C`, is byte-identical to the Wine-lab `graal603.exe`).

So a real 6.03r7 user runs a **protected Quattro 2D client behind a CyaSSL/QPlay packer**.

## 2. What our Frankenstein 6.037 is **[bin]**

From [T3D-122](3d-frankenstein-6037-vs-600-2026-11-26.md): a from-source hybrid of two of our repros — a **6.03r7 Quattro 2D host** with the **5.12 Graal3D proto-24 link** linked directly in. **Unpacked**, ordinary C++ symbols for both halves, **no Themida/WinLicense/QPlay/CyaSSL layers**, built for macOS/Linux/Windows, version 0.0.1.

## 3. The deltas vs retail **[bin]**

| axis | stock 6.03r7 retail (packed upload) | our Frankenstein 6.037 |
| --- | --- | --- |
| packing | multi-layer: self-decrypting stub, scrambled sections, QPlay packer | **unpacked**, ordinary C++ symbols, no packer markers |
| identity string | version resource `Graal.exe`; export dir `QPlay.exe` | names itself `Frankenstein 6.0` / 6.037, v0.0.1 |
| secure transport | **CyaSSL/wolfSSL** TLS (SSLv3, RSA/ARC4/MD5/SHA, zlib) as the QPlay surface | **none** — plaintext proto-24 UDP+TCP dual link + Quattro session |
| engine (once unpacked) | Quattro **2D** (no Torque classes, no proto-24) | Quattro 2D host **+ proto-24 3D link** linked in |
| 3D networking | **absent** (gen-5 2D protocol only) | **present**: `"3 "` server entry, dual-link handshake, login steps 2–6, GameObject/Camera ghosts, control object, sky, terrain chunks |
| 3D render | n/a (2D) | stand-in box/grid placeholder only (real Torque renderer is future work) |
| analysis posture | anti-debug / anti-decompile (breakpoint stub, scrambled names, obfuscated exports) | fully readable source + symbols |

**New vs [T3D-122](3d-frankenstein-6037-vs-600-2026-11-26.md):** the packaging and CyaSSL/QPlay **secure-transport** axis. [T3D-122](3d-frankenstein-6037-vs-600-2026-11-26.md) compared our build to the *unpacked* 6.00 engine, so it did not touch the packer or the TLS surface. Our build does **not** reproduce the retail's CyaSSL/QPlay secure channel — a real deployment gap, not just a cosmetic one: the retail client can speak the packer's TLS/compression channel; ours speaks the 5.12 proto-24 plaintext link instead.

**Unchanged vs [T3D-122](3d-frankenstein-6037-vs-600-2026-11-26.md):** the 3D verdict. The packing hides no extra 3D — [T3D-121](3d-v6-quattro-vs-512-2026-11-26.md) read the unpacked 6.03r7 directly and found it Quattro 2D, so the packer is wrapping a 2D engine. Our build still is the only one of the two with proto-24 3D capability, box-view only.

## 4. Verdict

Against the retail client a real user runs, our Frankenstein 6.037 is distinguished **both** by being an **unpacked, symbol-bearing, packer-free developer build without the retail's CyaSSL/QPlay secure-transport layer**, **and** by carrying a **proto-24 3D networking stack the retail 2D Quattro binary lacks** (box-view render only). It is emphatically not the retail 6.03r7 image with a 3D patch: it shares neither the packer, the TLS surface, nor the 2D-only engine.

## For a server

Neither the **stock 6.03r7 retail** client nor its unpacked Quattro engine can be driven as a 5.12-class proto-24 3D client — it speaks the gen-5 2D protocol only. Only our Frankenstein 6.037 can (and only to a stand-in box view). A server also cannot assume a retail-style CyaSSL/QPlay secure channel when talking to our build: our build has no such layer, so its 3D link is the plaintext proto-24 UDP+TCP dual link.

## Method caveat

Static read only. The packed retail listing (`client-internals/skipped-v6-read.md`) is the outer shell; the "retail engine" verdict rests on [T3D-121](3d-v6-quattro-vs-512-2026-11-26.md)'s direct read of the *unpacked* 6.03r7 client (byte-identical to `graal603.exe`), not on dynamically unpacking the upload here. Our build's proto-24 3D stack and the absence of any packer/CyaSSL layer are present as real code and symbols ([T3D-122](3d-frankenstein-6037-vs-600-2026-11-26.md)). The secure-transport delta is a code-presence fact (retail has the CyaSSL/QPlay surface, ours does not), not a live handshake comparison.
