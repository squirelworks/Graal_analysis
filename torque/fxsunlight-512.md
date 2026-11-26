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
| 2 | transform | position 3 × raw 32 floats, then rotation as a quaternion's x, y, z (3 × raw 32 floats) and a flag set when w is negative (w is rebuilt as the positive or negative root); the same encoding as the `WaterBlock` transform |
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

A first live try with the transform's flag left out crashed the client while it unpacked the ghost, as a one-bit slip would. **[lab]** With the corrected layout the real 5.12 client accepts the ghost: nine cases (azimuth, elevation, size, colour, blend modes 0, 1, 2 and 9, enable 0) all stayed up, and the flare texture was fetched once over TCP and cached. No `Invalid Blend Mode` line appeared, even for 9. No flare showed under the GDI renderer with azimuth 0, elevation 30 and flare size 300, looking level toward each of the four headings (0°, 90°, 180°, 270° about z), and nothing about the flare was logged. Eight more views also showed no flare: elevation 30 looking up at two pitches toward headings 0 and 180, and elevation 5 looking level toward all four headings. A pixel scan for the flare's colour found none in any frame. So under GDI the 5.12 client draws no flare at all; under Mesa llvmpipe it drew no flare either, in 16 views (elevations 30 and 5, four headings, level and pitched up), so something beyond the renderer is still missing. **[lab]** Statically, the flare's draw function needs the loaded flare texture, and it logs the
`Invalid Blend Mode` line for any blend mode other than 0, 1 or 2 (0 is additive). That line never
appeared for blend mode 9, so the draw function was never called in these runs: the scene did not
hand the object to the renderer at all **[bin]**. A likely cause is that the object's own
position was out of view **[inf]**; a run with the object 10 units in front of the camera at eye height (enable on, both flare bitmaps
set, size 300, elevation 5) still drew no flare and still logged no `Invalid Blend Mode` line for
blend mode 9, under Mesa. The ghost is created and the texture is cached, but the draw path is
never entered, so our rawobject `fxSunLight` is missing a field or registration the real object
needs beyond the update fields read here; it is not the position, the box or the renderer. **[lab]** Statically, the flare is drawn by a render-image callback in the object's render vtable, which
the scene's render manager calls only for an object it has added to its visible set. The prep that
registers that callback bails unless an internal flag is set; that flag is set by the routine that
loads the flare bitmaps. The ghost's bitmaps were cached, yet neither the draw nor the blend
validator ran, which points at the ghosted object not being added to the client's render set,
rather than a missing update field. Pinning it down needs a debugger on the live client. **[bin][inf]** A lab check would ghost one `fxSunLight` beside the terrain world and vary
azimuth, elevation, size and colour.
