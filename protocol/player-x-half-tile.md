# Player X/Y on the wire: one-byte half-tiles (props 15/16) and X2/Y2 (78/79)

Sources: static reads of the client binaries **[bin]** (1.21, 2.05 rev2, 2.17.1, 2.22, 2.31, 3.04 Linux, 4.04r2, 5.30r3, 6.03r7) and walking captures **[cap]** (2.00, 2.31). A live injection check is listed under "Open" at the end.

## One-byte X/Y (PLPROP 15 / 16)

The value on the wire is `half-tiles + 32`, one byte.

### Receive (all clients)

Every client read so far decodes the byte with an unsigned load followed by a signed 32-bit subtraction:

    v = (int)(uint8)byte - 32      // zero-extend, then int arithmetic
    x = v / 2.0                    // tiles
    x += gmap segment x offset     // only when the player is on a gmap

No client sign-extends the byte. The result:

| wire byte | half-tiles | tiles |
|---|---|---|
| 0x00 … 0x1F | −32 … −1 | −16 … −0.5 |
| 0x0A | −22 | −11, cannot be sent: it is the message terminator `\n` |
| 0x20 | 0 | 0 |
| 0x21 … 0xFF | 1 … 223 | 0.5 … 111.5 |

So 0xD8 … 0xFF mean +92 … +111.5 tiles to the client. A server that reads them as signed (−20 … −0.5) does not match any client.

Read in: 1.21, 2.05 rev2, 2.17.1, 2.22, 2.31 (Delphi), 3.04 Linux (Torque C++), 4.04r2 GraalEngine.dll, 5.30r3, 6.03r7. **[bin]**
1.21 has no gmap offset. In every client, baddy X/Y bytes are decoded the same way and then clamped to 0 … 63.

### Send

    byte = (round(2 * x) + 32) & 0xFF

- The rounding is round-half-up in 2.05, 4.04 and 6.03 (`floor(2x + 0.5 + 0.0001)`), round-to-nearest in 2.22 and 2.31, and Delphi `Round` in 1.21. **[bin]**
- The client never clamps its own X/Y. Stepping off the west edge sends −0.5 as 0x1F: a 2.00 capture shows exactly that byte while the player was at x = −0.5. **[bin][cap]**
- On a gmap the client sends the x inside the current segment (0 … 64), not the gmap-wide x. **[bin]**
- Values at or above 111.75 tiles wrap through the low 8 bits. This can't happen on a 64×64 level.
- The NPC prop writer (2.05) is different: it clamps an NPC's x/y to 0 … 63 before writing it. **[bin]**

### Range and overflow

- Other players: after decoding, x is stored as a double with no clamp. The usable range is −16 … +111.5. A sender x below −16 wraps through the low 8 bits, for example −16.5 to +111.5, −20 to +108 and −64 to +64. **[bin]**
- The local player in 2.22 and 2.31 stores its own x/y as 24-bit fixed point, `(x + 10) * 65536`, split into four obfuscated 6-bit fields. A PLAYERPROPS X below −10 for your own player therefore wraps to about +246 − |overflow|; for example −16 is read back as +240. **[bin]**

## X2 / Y2 / Z2 (PLPROP 78 / 79 / 80), 2.30 and later

    p   = floor(16 * x)                 // pixels
    v   = 2 * |p| + (p < 0 ? 1 : 0)
    v   = min(v, 0x6FFF)                // 4.x and later; 2.31 has no clamp
    out = chr((v >> 7) + 32) chr((v & 0x7F) + 32)

The receiver computes `v = (b0 − 32) * 128 + (b1 − 32)`, then `x = (v >> 1) / 16`, and negates x when bit 0 is set. **[bin]**

- 2.31 and all 4.x–6.x clients send only X2/Y2 while walking (2.31 capture). **[cap]**
- 2.22 and earlier don't parse props above 74/76, so they never see X2. A server has to send them prop 15/16.
- Neither byte can be `\n`, because each byte is at least 32.

## Server note

GServer-v2's older `TPlayerProps.cpp` reads `readGUChar() / 2`, which matches the clients. It writes `(char)(x * 2) + 32`, which truncates toward zero where the clients round.

## Open

- [ ] Live check: inject the bytes from the tables into real 2.05, 2.22 and 2.31 clients (and 4.x to 6.x for X2), and read back the x each client holds.
