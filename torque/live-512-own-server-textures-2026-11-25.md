# 5.12 on our own 3D server: texture names, formats, client updates (2026-11-25)

Lab: the real 5.12 client against seihai-gserver-v2 in graal3d mode, inside the
GwenTea2 VM. Run by the renderer lab. Behaviour only. The captures and
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

- When the camera looks along +y, the client shows the third sky entry.
- It draws a fog horizon.

Open: the full face order, the cloud layers and the fog bands.

## Client fault

The fault reproduces when `levels3d/` is deleted but `FILENAMECACHE.txt` is
kept:

- the client requests no meshes;
- then it crashes with an access violation inside the 3D engine.

A server cannot cause this; it is a client cache state. When a 3D session
misbehaves after a cleanup, delete `FILENAMECACHE.txt` too.
