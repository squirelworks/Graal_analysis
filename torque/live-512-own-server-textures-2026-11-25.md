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
- **Visible distance and fog.** Values of 0, 50, 200 and 1000 gave
  pixel-identical frames. A dedicated fog run (Mesa) drew every 1x1 cube
  along +y out to 800 m, untinted, even behind a visible distance of 100.
  Only the sky takes the fog: a band of the fog colour fades up from the
  horizon with solid fog colour below. So the client does not fog or
  distance-clip GameObjects, and the Sky's visible-distance field changes
  nothing visible. This is not a driver limit (confirmed on Mesa, not just
  GDI).
- **Flags (resolved).** The sky line's three flag bits (`skyoptions b1 b2
  b3`), run across all 8 combinations with the camera pitched down into the
  box:
  - **b1 = use-sky-textures** (known): on → faces textured; off → faces are
    the solid `skysolidcolor`.
  - **b2 = render-bottom-texture.** b2 alone draws the skybox **bottom**
    face: whenever b2=1 the bottom is drawn (textured if b1=1, else solid
    grey); whenever b2=0 the bottom is absent (sides only). The earlier "1 1
    1 draws the bottom" was just a case of b2=1 — `0 1 0` draws it too.
  - **b3 = no-render-bans.** **No visible effect** in any test: every b3=0
    vs b3=1 pair (111/110, 011/010, 101/100, 001/000) rendered identically.
    Likely a banding/dither toggle that doesn't show at these settings.
- **"Scale" is the world visible-distance, not a skybox scale (resolved).**
  The value on the sky line was tried at 50 / 500 / 50000 and the skybox
  renders **identically** at every value — it does not resize the box, tile
  the texture, or move the horizon. The skybox is at infinity; this field is
  the world fog / visible distance (how far terrain and objects fade), the
  same field discussed under "Visible distance and fog" above. (The earlier
  "about twice magnified" impression was the fixed box projection, not a
  scale control.)
- **Clouds — not supported (resolved).** Adding a 7th texture entry
  (`cloud1`) to the sky line makes the client **download** it ("File
  download: cloud1 (size 31040) done") but **no cloud layer draws** — looking
  up shows only the top face and nothing moves. The gserver leaves the Sky's
  storm/cloud/wind sections clear (no cloud count/height/speed sent) and
  there is no world-file field for cloud layers, so the extra texture is
  fetched but unused. Clouds are not a supported feature on this path.

## Client fault

The fault reproduces when `levels3d/` is deleted but `FILENAMECACHE.txt` is
kept:

- the client requests no meshes;
- then it crashes with an access violation inside the 3D engine.

A server cannot cause this; it is a client cache state. When a 3D session
misbehaves after a cleanup, delete `FILENAMECACHE.txt` too.
