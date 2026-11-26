# 5.12-class sound formats are FMOD 3.70's set: WAV/OGG/MP3/MP2 play, WMA/ASF are Windows-gated, FLAC/AAC are silently dropped (T3D-123, Linux 4.20r6)

Date: 2026-11-26. Single-client lab on native Linux 4.20r6 (5.12-class, protocol 24, g3d420 route), software GL. Observation only; only valid files of each format. Board row: [T3D-123](3d-capability-board.tsv). Lab-confirms the partial-static [T3D-062](3d-capability-board.tsv) list; builds on [T3D-084](3d-sound-paths-2026-11-25.md) (sound paths) and [T3D-119](3d-file-loader-errors-420r6-2026-11-26.md) (sound robustness). **Audio output is not verifiable headless** — judged by file-resolve + FMOD accept/no-error/no-crash.

## Headline

The audio backend is **FMOD 3.70** (`libfmod-3.70.so` — FMOD 3.x, **not** FMOD Ex 4.x). FMOD 3.x's native decodable set is exactly **WAV, MP2, MP3, OGG, WMA, ASF** (+ tracker/raw) — precisely the [T3D-062](3d-capability-board.tsv) static list — with **no FLAC or AAC**. So: **ship WAV/OGG/MP3/MP2**; WMA/ASF are the Windows-only Media codec (undependable on the Linux client); FLAC/AAC are not FMOD 3.x formats and are **silently dropped**.

## Format → (resolved? accepted?) **[lab + bin]**

| format | in T3D-062 list | resolved | FMOD 3.70 accepts? | error/crash |
| --- | --- | --- | --- | --- |
| `.wav` (8-bit PCM) | yes | yes | **yes** (core; [T3D-084](3d-sound-paths-2026-11-25.md) baseline) | none |
| `.ogg` (Vorbis) | yes | yes | **yes** (core) | none |
| `.mp3` | yes | yes | **yes** (core) | none |
| `.mp2` | yes | yes | **yes** (core) | none |
| `.wma` | yes | yes | named, but **Windows-codec** — FMOD 3.x WMA decode is Windows-only; unlikely to decode on Linux | none logged |
| `.asf` | yes | yes | same as `.wma` (ASF = WMA container) | none logged |
| `.flac` | **no** | yes | **no** (not an FMOD 3.x format) | none logged (silent) |
| `.aac` | **no** | yes | **no** (not an FMOD 3.x format) | none logged (silent) |

All 8 **resolved** (a `PLI_UPDATEFILE` per file; pre-placed so the gserver reports "not sent"). The weapon ran to completion (end HUD line drew), FMOD initialised (`FMod Sounds: using alsa`), and the client stayed up for every format. **No format — supported or not — logged an FMOD/codec error or crashed.**

## Accept vs reject (reconciled with T3D-062)

- **Accepted (decoded):** WAV, OGG, MP3, MP2 — the core cross-platform FMOD 3.x formats, all in the [T3D-062](3d-capability-board.tsv) list, all resolved with no error.
- **Named but platform-gated:** WMA/ASF appear in the build strings, but FMOD 3.x WMA/ASF is the Windows-only Media codec; they resolve and log no error but almost certainly don't decode on this Linux client (the one uncertain row, not positively confirmable headless).
- **Rejected (not an FMOD 3.x format):** FLAC, AAC — absent from [T3D-062](3d-capability-board.tsv), not decodable by FMOD 3.70; they still resolve, but FMOD can't play them.

## Unsupported-format behaviour

**Graceful — silent, no crash.** flac/aac (and the platform-gated wma/asf) each resolved, the `play2` ran, and the client stayed up with no error and no crash — a no-op for a format FMOD can't decode. Matches [T3D-119](3d-file-loader-errors-420r6-2026-11-26.md)'s sound-loader robustness.

## Headless caveat

Confirmed: each format's file resolve, and that FMOD initialises, logs no error and never crashes. Not confirmed: actual audio / that FMOD truly decoded a file — the client logs no per-sound FMOD result (even known-good WAV logs nothing), so the accept/reject split rests on the identified **FMOD 3.70** codec set + the [T3D-062](3d-capability-board.tsv) strings, not heard audio. WMA/ASF are the only genuinely uncertain rows.

## For a server

Ship 5.12-class sounds as **WAV, OGG, MP3, or MP2** (FMOD 3.70's reliable set). Avoid **WMA/ASF** (Windows-codec, undependable on Linux) and **FLAC/AAC** (not FMOD 3.x formats). An unsupported sound is **silently dropped** — no error, no crash — so a wrong format fails quietly rather than loudly; test playback on a real client to be sure.
