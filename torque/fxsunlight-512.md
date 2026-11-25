# Graal 5.12 `fxSunLight` (sun flare) update

Date: 2026-11-25. Client: the real 5.12 `Graal3DEngine.dll` (SHA-256 `04f7a133…`), static read.
Tags as in `README.md`: **[bin]** read from that binary for behaviour, **[inf]** inferred. Nothing
here is decompiled text. Encoding terms as in [terrain-512.md](terrain-512.md) and
[udp-session.md](udp-session.md) §2: "raw" values go through the stream's byte read at the current
bit position, `pstring` as there.

`fxSunLight` is the stock TGE 1.x sun-flare object (a lens flare drawn at a sun direction, with
optional animated colour, brightness, rotation, size, azimuth and elevation). In 5.12 it is a
ghosted object like `WaterBlock`, so a server can send it. Its update keeps the stock field order,
with Graal's own encodings: booleans are single raw bytes, the animation switches are bit flags,
and colours are four raw bytes. **[bin]**

## Update layout

| # | Field | Encoding |
|---|---|---|
| 0 | anything follows | flag; 0 ends the update |
| 1 | object name | `pstring` |
| 2 | transform | 6 × raw 32 floats: a position, then a second 3-vector (rotation **[inf]**) |
| 3 | enable | raw 8 (non-zero = on) |
| 4 | local flare bitmap | `pstring` (texture name) |
| 5 | remote flare bitmap | `pstring` (texture name) |
| 6 | sun azimuth, sun elevation | 2 × raw 32 floats (degrees **[inf]**) |
| 7 | flare TP | raw 8 (non-zero = on) |
| 8 | colour | 4 × raw 8: R, G, B, A (0–255) |
| 9 | brightness, flare size, fade time, blend mode | 4 × raw 32 (blend mode is a number; the client logs `fxSunLight: Invalid Blend Mode Selected!` for a bad one) |
| 10 | animation switches | 14 flags, in order: anim colour, anim brightness, anim rotation, anim size, anim azimuth, anim elevation, lerp colour, lerp brightness, lerp rotation, lerp size, lerp azimuth, lerp elevation, link flare size, single colour keys |
| 11 | min colour, max colour | 2 × (4 × raw 8 RGBA) |
| 12 | min/max brightness, rotation, size, azimuth, elevation | 10 × raw 32 floats, as min then max for each |
| 13 | key strings | 8 × `pstring`: red, green, blue, brightness, rotation, size, azimuth, elevation keys |
| 14 | cycle times | 6 × raw 32 floats: colour, brightness, rotation, size, azimuth, elevation time |

After reading, the client re-applies the settings (textures, animation state). **[bin]** Field
names come from the class's own property names in the same binary, which follow stock TGE's
order. The meanings are stock Torque's **[inf]**: a key string is a run of letters `A`–`Z`, read
as a value from min (`A`) to max (`Z`), stepped through over the matching cycle time.

Not yet tried live. A lab check would ghost one `fxSunLight` beside the terrain world and vary
azimuth, elevation, size and colour.
