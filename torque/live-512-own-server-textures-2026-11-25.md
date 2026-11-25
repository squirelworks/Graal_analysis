# 5.12 on our own 3D server: texture names, formats, client updates (2026-11-25)

Lab: the real 5.12 client against seihai-gserver-v2 in graal3d mode, inside a
lab VM. Run by the renderer lab. Behaviour only. The captures and
screenshots stay in the lab share. Board rows: T3D-023, T3D-032, T3D-033,
T3D-046. **[lab][cap]**

## Texture names (T3D-033, final)

- The client drops any image extension from material and sky texture names:
  `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`, `.tga`, `.dds`.
- It lower-cases the name and asks the server for the bare name. For example,
  `C6CYN.PNG` is requested as `c6cyn`.
- Shape names keep their extension (`.3ds`).
- After a "not found" answer the client does not ask again.
- It saves the received bytes unchanged under the bare name:
  - a name with an underscore goes to a subfolder named after the part before
    the first underscore (`g3dn_c1` goes to `levels3d/images/g3dn/`, `gnsky_fr`
    goes to `images/gnsky/`);
  - other names go to `images/`.

## Texture formats (T3D-032)

The client decodes a texture by its content, not by its name.

| Drawn | Not drawn (white) |
|---|---|
| 8-bit PNG: RGB, RGBA, paletted, grey, interlaced | 16-bit PNG |
| JPEG, baseline and progressive | BMP, 24 and 32 bit |
| GIF | TGA |
| | DDS |

- A missing texture draws white. It does not fall back to the material colour.
- Alpha 0 is cut out. Alpha 128 draws fully opaque, so there is no blending.
- GIF transparency draws white.

## What the client sends for its control object (T3D-023)

Whatever the control object's class, the client sends its position plus an
update in the GameObject layout.

- With a `Camera` control object, the first update carries the transform only.
  After that the client sends an empty update once a second.
- With a `GameObject` control object, the update carries shape, transform and
  flags.

## Sky (T3D-046, partial)

Series 1 on the real 5.12 client, one change per run. **[lab][cap]**

- **Face order.** Sky-line texture entries 0 to 4 map to these directions:
  0 is -y, 1 is +x, 2 is +y, 3 is -x and 4 is up.
- **Mirroring.** The side faces draw mirrored left to right, with up still
  up. The up face has the top of its image toward +y.
- **Entry 5** (the bottom face) is not drawn with the default options.
- **Below the horizon** the sky shows the fog colour under Mesa (llvmpipe),
  even looking straight down. Under the VM's GDI Generic OpenGL 1.1 driver it
  was black, with a fog-coloured band fading up from the horizon. The fog
  colour tints it (checked with red). Face order and mirroring are the same
  on both drivers.
- **Visible distance.** Values of 0, 50, 200 and 1000 gave pixel-identical
  frames. Markers at 100 and 300 always showed and a marker at 800 never
  did, so this field does not drive clipping or fog on the client. What
  does is still open.
- **Flags.** The first flag turns sky textures on; with it off, a solid
  colour fills the sky. The second and third flags showed nothing when
  looking up. Whether either turns on the bottom face is still being run.
- **Scale.** The client's faces look about twice as magnified as a plain
  cube box. Not explained yet.

Still open: cloud layers, what limits the view distance, flags 2 and 3, and
the magnification.

## Client fault

The fault reproduces when `levels3d/` is deleted but `FILENAMECACHE.txt` is
kept:

- the client requests no meshes;
- then it crashes with an access violation inside the 3D engine.

A server cannot cause this; it is a client cache state. When a 3D session
misbehaves after a cleanup, delete `FILENAMECACHE.txt` too.
