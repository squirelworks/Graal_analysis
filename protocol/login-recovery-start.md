# Protocol recovery — initial notes

Date: 2026-10-14

## Starting point
Newest binary: Graal_231.exe (post IDR + Dhrake).

## Observed in EntryPoint (231)
- Auto-connect path when two controls (likely username + password) have non-empty text.
- Calls a handler equivalent to `TConnectFrame_Button1Click`.
- This is the highest-value next trace target for the login packet.

## Immediate next trace
1. Locate the connect button handler in the 231 Ghidra database.
2. Follow the call chain that builds and sends the initial login / handshake packet.
3. Record:
   - Packet ID / first byte(s)
   - Field order and encoding (length-prefixed strings, etc.)
   - Any version or client-identification bytes
4. Add the corresponding Rust type + serializer in `seihai/client/src/protocol`.

## Provisional implementation (2026-10-14)
A working (but unconfirmed) encoding is now in `seihai/client`:
- `LoginRequest` — id 0x01, length-prefixed username/password/version
- `LevelRequest` — id 0x10, length-prefixed name
- `PlayerUpdate` — id 0x20, f32 x/y + u8 dir

These exist so the client can attempt a connection. Replace the layouts as soon as the real packet formats are recovered from the 231 binary.

## Other high-value flows (later)
- Level request / level data
- Player movement / position updates
- NPC / script-related messages
