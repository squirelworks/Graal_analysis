# Login and walk frames

Date: 2026-10-14

## Login (locked)
```
Chr((rand & 0x7F) + 0x20) + GNW##### + length-biased account + length-biased password
```
Length bias: `nbytes + 0x20`. Token is exactly 8 characters.

Implemented in `seihai/client/src/protocol/mod.rs` as `LoginRequest::write_classic`.
Unit test covers the fixed-prefix case.

## Walk (provisional field split)
Wire type `"` (0x22 = logical 0x02 + 0x20), newline-terminated.
Provisional payload: biased classic-x, biased classic-y, biased dir.

`write_walk` / `decode_walk` round-trip in tests. Exact x/y/dir split still needs a known-position capture to confirm.

## Offline wiring
`OfflineSession::try_move` now returns `Option<PlayerUpdate>` on success.
