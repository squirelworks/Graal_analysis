# Offline expansion

Date: 2026-10-14

## Offline session
- `in_water` tracks type-11 tiles. Does not block.
- `walk_gani` is an optional `GaniPlayer`. Stepped on every successful move.
- `set_walk_gani` / `walk_frame` expose it.

## GS1 command stubs
Registered no-ops / pass-throughs:
- `message`, `say` — return the first argument
- `setimg`, `showimg` — return the first argument
- `move`, `hideimg`, `setlevel`, `warp` — return None

`CmdCall` dispatches into the registry. Movement and level changes stay with the session, not the VM.

## Scope
Offline only. No listserver, no new decompile work.
