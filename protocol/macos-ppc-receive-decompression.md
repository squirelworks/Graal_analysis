# PowerPC receive decompression and workspace policy

[bin] This note is the per-build companion to
[the PowerPC receive framing note](macos-ppc-receive-framing.md). That note gives
the frame boundary, the mode byte and the cipher stepping that all four Mac
PowerPC receivers share. It leaves out what happens after the XOR step, because
the decompression wrappers differ from build to build. This note covers those
wrappers.

The source is a static review dated 2026-11-09. Decompiled bodies were checked
against their assembly. No client was run, no compressed frame was fed to a
receiver, and no wire capture was taken.

## Inputs

| Archive group | What the label covers |
| --- | --- |
| Shared v3 | Two archive copies, labelled 3.04 and 3.15r2, with the same main executable |
| Label 4.04r2 | One copy |
| Label 4.20r6 | One copy |
| Shared v5 | Five copies, one of them labelled 5.12, with the same main executable |

Matching executable bytes do not authenticate a release label. The executable
digests are owner-held.

## What each wrapper accepts

**[bin] Shared v3 and 4.04r2.**
- The receive wrappers decompress into a shared output buffer of fixed capacity.
- A frame is accepted only if decompression produces some output and that output fits within the capacity.
- A zlib member succeeds only when the wrapper returns zero. The lower "finish" route also accepts end-of-stream before cleanup.
- These early wrappers have no loop that grows the buffer and retries.

**[bin] 4.20r6.**
- The zlib wrapper calls the library with the version string `1.2.3`. The shared v3 lower wrapper calls it with `1.1.3`.
- The zlib route still requires a zero return and some output within the shared capacity.
- The bzip2-linked wrapper requires a non-negative return and some output within its bound.
- The bzip2 library body was not reviewed in full.

**[bin] Shared v5.**
- The receive callers pass a null output buffer, so they use a shared workspace.
- The workspace size is a power of two. It starts at the current shared capacity, or at 65536 bytes if that is larger.
- When decompression reports that it needs more room, the requested size doubles. It keeps doubling only while the next request is at most 4194304 bytes (4 MiB).
- A caller that supplies its own non-null output buffer does not use this grow-and-retry route.

[inf] The 4 MiB figure stops the doubling. It is not a limit on decoded output. The shared capacity can already be larger than 4 MiB when the retry starts, and a caller-supplied buffer skips the route entirely.

[bin] In the shared v3 executable, one opened streaming routine checks a header the way a zlib wrapper does:
- the compression method nibble must be 8;
- the window size is checked;
- the two header bytes must be divisible by 31;
- a preset dictionary is handled on its own path;
- a four-byte trailer is checked at the end.

Who calls this routine was not traced. Other compression-labelled hits in that executable are:
- a libbzip2 fatal-error routine that ends the process;
- a JPEG 2000 image decoder.

Neither hit shows a bzip2 path for game frames.

## Limits

- The version strings are the values passed when the library is initialized. They do not prove which vendor package was linked.
- Nothing here shows that a valid compressed member is accepted at run time. The review also does not settle concurrency or every malformed-input case.
- The cipher stepping and the frame boundary are in the framing note and are not repeated here. Send-side symmetry is not claimed.
- A frame tagged as compressed that contains arbitrary bytes is not a valid compressed member. Such a frame tests nothing about these wrappers.

## Remaining work

- [ ] Run a positive control first: an unchanged receiver that accepts one valid raw frame. Then feed it independently generated zlib members at lengths near each capacity boundary. Record the cipher stepping, the decoder's return value, the output bytes and the state that follows, each separately.
- [ ] Open the bzip2 lower body in 4.20r6 and v5.
- [ ] Trace the callers of the shared v3 streaming routine.

## Evidence

These are sanitized static summaries held by the researcher. They are registered in
[the evidence index](../docs/evidence-index.tsv). Raw exports and digests are
owner-held.

- `MAC-PPC-V3-FRAME-STATIC-20261109-R1`, `MAC-PPC-404-FRAME-STATIC-20261109-R1`,
  `MAC-PPC-420-FRAME-STATIC-20261109-R1`, `MAC-PPC-V5-FRAME-STATIC-20261109-R1`.
- `MAC-PPC-V3-BROAD-STATIC-20261109-R1` (zlib-style header check, library hits).
