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

**Follow-up run (5.12, Mesa) [lab].** The client does fetch the flare texture: on the first visit it requests exactly the name in the object (tried as `.png`, `.jpg` and a bare name), caches it in its images folder, and loads it from there on later visits. Nothing about the flare is logged. Even so, no flare drew in any case: 64 × 64 and 256 × 256 PNGs with transparency, a 256 × 256 JPG and a bare name, freshly pushed or cached, with 0 flare-coloured pixels in 8 shots toward the sun direction. So the texture loading works, and the draw is still never reached. A side effect appeared: with a yellow colour set, the sky behind and to the left of the camera, toward −y and −x, turns solid yellow, while the +x and +y sides stay normal. This happens with the flare switched off and at flare size 20 as well as 300. A blue colour changes nothing, and with no `fxSunLight` there is no tint. The tinted sides match the fixed −x/−y light direction the terrain shows (see `terrain-512.md`). Either our field layout is a few bytes off, so the colour bytes land in another field, or the client tints the sky on the sun's side. That isn't settled yet **[inf]**.

**The yellow "sky tint" is the flare (5.12, Mesa) [lab].** Shot with one camera looking straight up
at a 150° field of view, so each frame shows every side of the sky. The tint follows the flare's
colour channel by channel. Yellow adds about +127 to +250 to red and green on every side and
leaves blue alone. Red alone adds only red, green alone adds only green, and blue alone changes
nothing, because the flare texture used has no blue. So it is the flare texture multiplied by the
colour. Blend mode 1 turns the whole screen opaque yellow, and mode 2 is additive like mode 0.
Alpha, enable, azimuth (0, 90, 180, 270) and elevation (5, 45, 85) change nothing. So the client
draws the flare as a screen-filling quad and does not place it with the azimuth and elevation we
send. With a level camera it shows when looking toward −x or −y and is gone toward +x or +y, the
same side as the fixed terrain light in `terrain-512.md`. That suggests the client positions it
from the `Sun` object's direction (here (0, −0.71, −0.71)) or from a fixed direction
**[inf]**. Adding or removing one or eight bits right after the colour fields keeps the ghost
loading but removes the tint. So the fields after the colour gate the draw, and our layout is
aligned as sent. With all animation flags on, with or without "AZ" key strings, the client stays
up (no crash) and draws no tint. Under GDI nothing from `fxSunLight` draws at all.

**What turns the flare on: a fixed direction in the sky (5.12, Mesa) [lab].** In 179 runs, the
flare was on exactly when the camera faced toward one fixed point, at azimuth about 227° (toward
−x/−y; 0° is +y, 90° is +x) and elevation about 76°. It was off otherwise, with a clean split
over 107 sweep shots. Turning a level camera, it is fully off from 0° to 136° and switches fully
on within one 2° step at about 137°. It stays on to about 316° and switches off by 318°, so the
edges sit 180° apart and centred on 227°. It doesn't fade. In pitch it stays on while looking up
or level, and goes off once the camera looks down far enough, by about 14° at a yaw of 225°. That
is a hemisphere test against that fixed direction. It draws as part of the sky, behind the
terrain. Nothing sent moves or resizes it:

- the `Sun` object's direction (five tried), colour, or whether there is a `Sun` at all;
- the flare's azimuth, elevation, size (20 to 1000 gave pixel-identical shots), alpha or enable.

Only the colour × texture and the blend mode change how it looks. The `Sun` ghost was decoded from
packet captures and matches its documented layout: a flag, the name, then direction, colour and
ambient as plain floats. So the client receives the `Sun` direction correctly and doesn't use it
here. A renderer matching 5.12 should draw the flare texture × colour as a screen-filling quad
in the sky layer, with the sent blend mode, whenever the camera's forward vector points into the
hemisphere around azimuth 227°, elevation 76°.
