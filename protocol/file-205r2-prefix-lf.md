# Original Windows 2.05r2 FILE prefix and counted content

## Input and evidence

The original Windows 2.05 rev 2 executable is researcher-identified by SHA-256 `b0e39a04ca0891d0f02282a113a1cd80ddf7a1880a786c5831f26a452e8cbb08`. Evidence IDs `GRAAL-RAW-FILE-LF-20261109-01`, `SEIHAI-ORIGINAL-NETWORK-20261109-01` and `SEIHAI-ORIGINAL-VALID-GIF-20261109-01` resolve in [the evidence index](../docs/evidence-index.tsv). The editor verified the sanitized publication digest against its supplied manifest. Executable/evidence digests, static checks and lab outcomes remain researcher-supplied; raw code, captures and assets were not inspected.

## Exact receiver boundary

`[2.05][bin]` Behind RAWDATA, the FILE handler consumes the opcode, five encoded metadata bytes, an encoded one-byte filename length L, L filename bytes, then content. The five-byte read is unconditional on this branch. With N announced raw bytes, content length is N − 7 − L. The former server-derived claim of an optional or absent prefix is not this receiver's specification.

`[2.05][bin]` The counted collector bypasses normal line-delimiter subtraction and delivers all N bytes. Neither it nor the FILE-copy boundary drops a final LF inside that count. Bytes outside N are not content. A server-added delimiter inside N therefore becomes a file byte, regardless of ordinary line-message framing.

## Server comparison and controlled checks

`[srv][lab]` The tested Seihai-gserver-v2 seihai-branch baseline commit was `1b0a6e15641aa542168d5fd0878517d15d990adc`. Its pre-2.1 path omitted the prefix, its queue added LF inside the raw count, and a nonempty-only loop emitted no empty FILE record. Three local fixes changed those paths; publication/aggregation of those uncommitted and unpushed patches is separately deferred. This note publishes behavior findings, not patches.

`[lab]` Synthetic probes for 2.00 and 2.05r2 profiles each requested five fixtures: empty, no-LF, one-LF, two-LF and binary-LF. Filename/content checks changed from 0/10 at baseline to 10/10 after fixes. These are protocol probes, not ten original-client runs.

`[2.05][lab]` The unchanged original 2.05r2 client logged into the patched local world, requested all five fixtures and sent movement properties. Exact no-LF, one-LF and binary-LF files were found on disk. In a separate valid-GIF control, two terminal LF bytes persisted after repeating an unchanged server-generated record to an already-requested filename.

`[lab]` Initial two-LF delivery did not persist; empty-file persistence also remains unresolved. An unsolicited filename alias was not cached. Byte-copy evidence does not settle resource registration, deduplication, retry or general persistence rules.

## Fixture and execution limits

`[lab]` Wine and a virtual display ran inside private user/PID/network namespaces with loopback only and no routes. No public service was contacted. The original executable remained byte-identical and final cleanup completed. A labeled 2.31 resource donor completed the earlier package, so the setup was not an authentic complete 2.05 distribution.

`[lab]` The supplied HTML greeting stalled loading under Wine; emptying the copied world's greeting alone allowed milestone 6 with equal current/pending level objects. Repository default greeting was unchanged. The HTML/Wine cause and native Windows behavior are unproved. No new execution occurred during publication packaging.

- [x] ~~Establish the exact receiver prefix and counted-LF copy boundary.~~
- [ ] Resolve empty persistence and initial two-LF caching.
- [ ] Establish general retry/registration behavior, other builds, large-file continuation and malformed-input handling.
- [ ] Separate HTML/Wine and native Windows behavior with an appropriate controlled fixture.
