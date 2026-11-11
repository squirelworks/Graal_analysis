# Shoot packets in the 5.0.0.7 client, and how SHOOT2 stores gravity (5.0.0.7 to 6.00b1)

Date: 2026-11-11

Source: the Windows 5.0.0.7 engine (July 2007; called "5.00r7" in `v5x-clients.md`), using the unpatched engine file, read statically. The PLI_SHOOT2 sender was read in the 5.12 engine (October 2007), 5.24r4 and 6.00b1 (`v5v6-windows-unpacked.md`). Nothing was run. Tags: **[bin]** read from the client · **[srv]** read from the GServer-v2 fork (`seihai-gserver-v2`, `seihai-gs2lib`) · **[inf]** inferred.

The community called this build "5.007". It's the build whose launcher reports FileVersion `5.0.0.7`.

## Short answer

- **Gravity in SHOOT2 is 2 bytes in 5.0.0.7, not a byte.** It uses the PLPROP X2 / Y2 encoding (`player-props.md`), scaled by 256:
  - encode: `v = (round(|g| × 256) << 1) | (g < 0 ? 1 : 0)`, then write `v` as a GSHORT: `(v >> 7) + 32`, `(v & 127) + 32`
  - decode: `v = ((b0 − 32) << 7) + (b1 − 32)`, `g = (v & 1 ? −1 : +1) × (v >> 1) / 256`
  - step 1/256; range about ±32 (8191/256) with 7-bit digits
  - if fewer than 2 bytes are left, gravity is 0 **[bin]**
- **5.0.0.7 never sends PLI_SHOOT2 (48).** No send of id 48 exists in the engine. GS2 `shoot` sends **PLI_SHOOT (40)**, which has no gravity field. 5.0.0.7 only *receives* the SHOOT2 layout: as PLO_SHOOT2 (191), and as UDP peer id 30. **[bin]**
- **The sender arrives in 5.1x, and it also writes 2 bytes.** 5.12, 5.24r4 and 6.00b1 send PLI_SHOOT2 (48) with the same body the 5.0.0.7 reader takes. Gravity is `floor(g × 256 + 0.0001)`, X2-signed, written as a GSHORT. None of these builds writes gravity as one byte. **[bin]** The one-byte gravity in GServer-v2 (below) matches no client read so far. The 6.00r2 and 6.03r7 builds are laid out differently, and their sender wasn't found.

| Gravity | v | Bytes on the wire |
|---|---|---|
| 2.0 (the default) | 1024 | `0x28 0x20` (`( `) |
| 0.5 | 256 | `0x22 0x20` (`" `) |
| 1.0 | 512 | `0x24 0x20` (`$ `) |
| −1.0 | 513 | `0x24 0x21` (`$!`) |
| 0 | 0 | `0x20 0x20` |

## Field scales (all three shoot layouts)

The angle and power steps match the community's figures: angle 2π/220 and power 1/44. **[bin]**

| Field | Sent as | Client range before encoding |
|---|---|---|
| angle | `round(angle × 220 / 2π)`, GCHAR | first wrapped into [0, 2π) |
| zangle | `round((zangle + π/2) × 220 / π)`, GCHAR; decoded `b × π/220 − π/2` | clamped to [−π/2, π/2] |
| power | `round(power × 44)`, GCHAR; decoded `b / 44` | clamped to [0, 5], so 0–220 |

- "round" is `floor(x + 0.5 + 0.0001)`.
- Power is in tiles per 0.05 s step. That makes the cap of 5 equal to 100 tiles per second. **[bin][inf]**

## PLI_SHOOT2 (48), what 5.12 to 6.00b1 send **[bin]**

The body is the PLO_SHOOT2 body below without the leading player id. One routine builds it, sends it to UDP peers as UDP id 30, then sends it over TCP as 48. Here is how each field is built:

- **Position.** The sender splits the gmap position into a level (offset x, y = `floor(pos / 64 + 0.0001)`) and a position inside that level. x and y become `floor(local × 16 + 0.0001)` pixels; z becomes `floor(z × 16 + 0.0001)`. Each is then X2-signed (`2 × |v|`, plus 1 if negative) and written as a GSHORT. The GSHORT writer caps at 28671.
- **Angle, zangle, power.** `floor(angle × 220/2π + 0.0001)`, `floor((zangle + π/2) × 220/π + 0.0001)`, `floor(power × 44 + 0.0001)`, each a GCHAR. These truncate. The 5.0.0.7 PLI_SHOOT sender rounds instead (+0.5).
- **Gravity.** `floor(g × 256 + 0.0001)`, X2-signed, as a GSHORT: 2 bytes.
- **Gani and shoot params.** First the GCHAR length + `gani[,aniparams]`, then the GCHAR length + shoot params. A string longer than 223 bytes is sent as the byte 0xFF followed by its first 223 bytes. The login password uses the same rule.

## PLI_SHOOT (40), what 5.0.0.7 sends **[bin]**

| Field | Encoding |
|---|---|
| shooter | GINT3. The GS2 `shoot` path always sends 0 (three spaces). |
| x | GCHAR, `round(x × 2)`: half tiles, level-local (the gmap level offset is subtracted first) |
| y | GCHAR, same as x |
| z | GCHAR, `floor(z + 0.0001) + 50`: whole tiles, not rounded |
| angle, zangle, power | GCHAR each, as above |
| gani | GCHAR length, then `gani` or `gani,aniparams` |
| shoot params | GCHAR length, then the current `setshootparams` string |

This matches the GServer-v2 reader (`8 × x` px, `16 × (z − 50)` px). **[srv]** The same body goes to UDP peers as UDP id 28.

## PLO_SHOOT (175), received **[bin]**

This is GSHORT player id + the PLI_SHOOT body above. The decode is: x = `(b − 32) / 2` tiles; z = `b − 32 − 50`; then angle, zangle and power. The body is ignored if it's shorter than 10 bytes. A shooter id above 0 is looked up among the level's NPCs and the shot starts from that NPC. Id 0 uses the shooter player.

## PLO_SHOOT2 (191), received **[bin]**

This is GSHORT player id, then:

| # | Field | Bytes | Decode |
|---|---|---|---|
| 1 | x | 2 | X2-style: `±(v >> 1)` **pixels** |
| 2 | y | 2 | as x |
| 3 | z | 2 | as x |
| 4 | offset x | 1 | GCHAR `b − 32`, signed: a gmap level column. Adds `64 × offset` tiles to x. |
| 5 | offset y | 1 | as offset x, for y |
| 6 | angle | 1 | `(b − 32) × 2π/220` |
| 7 | zangle | 1 | `(b − 32) × π/220 − π/2` |
| 8 | power | 1 | `(b − 32) / 44` |
| 9 | gravity | 2 | X2-style, `/ 256` (above) |
| 10 | gani | 1 + n | GCHAR length (negative read as 0), then `gani[,aniparams]`, split at the first comma |
| 11 | shoot params | 1 + n | GCHAR length, then the string. Optional: skipped when nothing is left. |

- A body shorter than 14 bytes is ignored.
- The client then subtracts its own level's gmap origin from (x + 64·offset x, y + 64·offset y). So the position is gmap-wide.
- The same reader handles UDP peer id 30.
- The 5.24r4 reader has the same 2-byte gravity with the same `/ 16 / 16` scale, followed by a one-byte gani length. **[bin]**

## What the client does with gravity **[bin]**

- Each projectile can carry its own gravity, plus a flag.
- A projectile made from SHOOT2 sets the flag and uses the gravity from the packet.
- A projectile made by GS2 `shoot` or from PLO_SHOOT (175) doesn't set the flag. It uses the global script variable **`gravity`**, which is a double, defaults to 2 and can be set from script.
- On each step, the vertical speed drops by `gravity × 0.05`. The starting speeds are `power × cos(zangle)` horizontally and `power × sin(zangle)` vertically.

## Compared with GServer-v2 **[srv][inf]**

GServer-v2 builds PLO_SHOOT2 for clients of version 5.07 and newer differently from what 5.0.0.7 reads:

| Field | GServer-v2 writes | 5.0.0.7 reads |
|---|---|---|
| x, y, z | plain GSHORT pixels | X2-style (`v >> 1`, low bit = sign) |
| gravity | one GCHAR, `gravity × 16` | 2 bytes, `/ 256` |
| gani length | GSHORT | GCHAR |

The gravity and gani-length fields happen to total 3 bytes either way, so the following fields stay aligned. A static read predicts the following:

- Positions arrive at half their value, and an odd value flips the sign.
- For gani names under 128 characters, the client reads the gravity byte and the high byte of the gani length together as one gravity value. That gives `server byte / 4`, which is 4× the intended gravity.

Neither prediction has been checked in a lab. The GServer reader for PLI_SHOOT2 (48) assumes the same one-byte gravity with a GSHORT gani length. That layout has not been checked against a client that sends 48.

## Not done

- [x] ~~Read the first PLI_SHOOT2 (48) sender~~: 5.12, 5.24r4 and 6.00b1 send 2-byte gravity ×256 (above).
- [ ] Read the 6.00r2, 6.01r1 and 6.03r7 senders.
- [ ] Lab check: send a PLO_SHOOT2 with known gravity to a 5.0.0.7 client and watch the arc.
