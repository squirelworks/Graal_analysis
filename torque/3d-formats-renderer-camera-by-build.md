# 3D file formats, renderer, camera and sound by build (4.04r2, 5.12)

Static read of the two Graal3DEngine.dll builds we hold unpacked. It records
which loaders, settings and classes are present in each build, by their names
and messages. Presence is not proof that a feature works in a session; the
open boxes say what still needs a lab. Board rows: T3D-013, T3D-029, T3D-031, T3D-039, T3D-034,
T3D-035, T3D-051, T3D-055, T3D-062.

## Shape and model formats (T3D-031, T3D-034, T3D-035)

| Format | 4.04r2 | 5.12 |
|---|---|---|
| `.dts` shapes | yes | yes |
| `.dif` interiors | yes | yes |
| `.3ds` | yes | yes |
| `.dsq` sequence files | not in the plug-in; the 2D engine files `.dsq` downloads under `anis` | yes, in the shape extension list next to `.dts`, `.3ds`, `.dif` |
| `TSShapeConstructor` (adds sequences to a shape) | registered class | gone |
| `.md3` (Quake 3 player model) | yes: an MD3 loader that builds a model from `<name>_lower.md3`, `_upper.md3`, `_head.md3` and `<name>_lower_default.skin`, with its own error messages per part | gone |
| `.ifl` animated textures | yes (material list code) | no literal |
| `.dml` material lists | yes | no literal |

Version bounds (T3D-029):

| Check | 4.04r2 | 5.12 |
|---|---|---|
| DTS shape version accepted (low byte of the version word) | up to 24, no floor; below 19 goes to the old-format reader | 17 to 24; below 17 rejected ("not supported anymore"); 17 and 18 go to the old-format reader |
| DIF `InteriorResource` file version | exactly 44 | exactly 44 |
| DIF `Interior` version | exactly 0 | exactly 0 |

If a shape's version is above the maximum, the client logs "can currently only
load version 24 and before". If it is below the minimum, the client logs "not
supported anymore". An interior with any other version fails with
"incompatible file version found". **[bin]**

So MD3 models, IFL textures, DML lists and the shape constructor are 4.04r2
features. 5.12 keeps DTS, DIF and 3DS and adds a `.dsq` entry to its shape
list.

Open: whether 5.12 actually merges a `.dsq` into a shape, and how 4.04r2 picks
the MD3 animation. Both need a lab.

## Where downloaded 3D files are stored (T3D-053, part)

When a download arrives, the client picks a subfolder by extension. The 5.12
mapping for the 3D types:

| Extension | Subfolder |
|---|---|
| `.dts` | `shapes` |
| `.dsq` | `anis` |
| `.dif`, `.ml` | `interior` |
| `.ft` | `trees` |
| `.gpak`, `.gpake` | `gpaks` |
| `.gani` | `ganis` |
| `.ttf` | `fonts` |
| `.wav` | `sounds` |
| `.mp3`, `.mid`, `.ogg`, `.wma` | `music` |
| `.avi`, `.wmv`, `.mov` | `videos` |
| `.gmap` | `maps` |
| `.gupd` | `updatepackages` |

Level text and images go under `levels` or `levels3d`.

`.ml` is Torque's mission-lighting file type. The client files a downloaded
`.ml` with the interiors, but this read found no code that writes one. So
whether a 5.12 lighting pass leaves a cache on disk is still open.

The 4.04r2 sorter is in its 2D engine (GraalEngine.dll). It has the same
folder names except `trees`, `vector` and `guistyles`.

## The `.cs` entry in 5.12's file list (T3D-013)

The 5.12 list `.txt, .rtf, .htm, .html, .xml, .nw, .gani, .gmap, .gupd, .hfl,
.cs, .gs, .arc, .dat, .css, .ini, .uis, .png, .mng, .gif, .jpeg, .jpg, .jp2,
.bmp, .bm8, .tga, .dds` is the file-access gate for the GS2 file functions:
- the file read and write methods,
- getFileModTime,
- requestURL.

Before one of these functions touches a path, the path's extension must be
on the list. If the path has a folder, it must be under one of
`levels/, levels3d/, translations/, offline/, tileobjects/, updatepackages/`;
`scriptfiles/` is the scripts' own folder. A path that fails returns empty.

So `.cs` there means a GS2 script may read or write a `.cs` text file. It does
not mean the client runs TorqueScript: 5.12 has no TorqueScript compiler
(see [script-and-terrain-tools-by-build.md](script-and-terrain-tools-by-build.md)).

## Renderer and video settings (T3D-051)

Both builds carry Torque's OpenGL renderer and its Direct3D wrapper
(`opengl2d3d.dll`, `glu2d3d.dll`, the `D3DDevice` screen-mode messages).

- 4.04r2 exposes the stock settings:
  - `$pref::Video::allowOpenGL` and `$pref::Video::allowD3D`, the video mode prefs;
  - the full `$pref::OpenGL::` set: texture compression, anisotropy, trilinear, mip reduction for interiors and sky, nPatch, maximum hardware lights, gamma correction, and per-extension switches.
- 5.12 keeps only eight `$pref::Video::` names: `resolution`, `fullScreenMode`, `windowMode`, `detailFactor`, `fogDistance`, `visibleDistance`, `screenShotFormat` and `defaultguistyle`. There are no `$pref::OpenGL::` names and no allowD3D or allowOpenGL switch.

Open: whether 5.12 can still be put on the D3D wrapper by any means. This needs a lab.

### GameShape shaders in 5.12 (T3D-039)

5.12's `GameShape` has two script properties, `vertexshader` and
`pixelshader`. 4.04r2 has neither, and no GL shader calls at all.

- The value is GLSL source text, not a file name. On assignment the client
  hands the text straight to the driver as a vertex or fragment shader object
  (the ARB shader-object calls), compiles it, links the two into a program
  and checks the compile status.
- It writes "Compilation of ...: failed" or "...: successful", then
  "Compilation log:" and the driver's info log, to the `graphics` log
  category. That is the shader compile log seen in lab folders.
- Each draw sets three uniforms: `camPos` (the camera position), `tex` and
  `tex2` (two texture units).
- Nothing happens when the driver has no shader support.

Live check on 5.12 (renderer lab, 2026-11-25). A client weapon set both
properties on the player's shape. **[lab]**

- Both strings were stored and read back exactly.
- No file was requested.
- Neither property arrives from the server; only client script sets them.
- The lab VM has a software OpenGL 1.1 driver with no GLSL, so the client wrote
  no compile log.
- Plain text, GLSL source and a file name all drew pixel-identical.

That fits the static read. The compile happens only when the driver supports
shaders and the shape has a program object.

Open: the compile path and its visible effect. These need a VM with a
GLSL-capable GL.

Side finding: 5.12 caches each 3D weapon's compiled script as
`weblevels/weapons/<server>/<weapon>.code`.

## Camera classes (T3D-055)

| Class | 4.04r2 | 5.12 |
|---|---|---|
| `Camera`, `CameraData` | yes | `Camera` only (the control object in a real 5.12 session) |
| `PathCamera`, `PathCameraData` | yes | gone |
| `AdvancedCamera`, `AdvancedCameraData` | yes | gone |
| camera functions | `setCameraPosition`, `getCameraPosition`, `setCameraFov`, `getCameraFov`, `setControlCameraFov`, `getControlCameraFov`, `shakeCamera` | none of these names |

5.12 keeps the names `atCamera`, `atCameraRot` and `belowCamera`.

5.12 gives GS2 no camera functions and no camera properties. The only
camera-named script property is `cameraz` on `GuiPlayerView`, which is the
preview widget. 5.12 has no first-person toggle name either. So in 5.12 the
3D camera is driven only by the server, through the `Camera` ghost when it is
the control object.

Open: which fields of that ghost the client applies. This is the renderer lab's
T3D-023.

## Sound formats (T3D-062)

- 5.12 plays sound through FMOD. Besides `.wav`, it lists `.mp2 .mp3 .ogg .wma .asf` for music and streams. It also has the music-data event and the MP3 and radio volume hooks.
- 4.04r2's plug-in names only `.wav`. Its other sound goes through the 2D engine.

Open: whether the 3D audio classes (`AudioEmitter`, `Sim3DAudioEvent`) play in 4.04r2. This is T3D-061, a lab.
