# 3D capabilities by build (3.04 to 5.12)

Date: 2026-11-25. Companion to [`three-d.toml`](three-d.toml), the machine-readable source for the
`three_d` part of Seihai's version profile. This page says what each field controls and why each
build has its value. Every value in the TOML carries an evidence tag: **bin** (static read of that
build), **lab** (real client against our gserver), **cap** (capture of the real client) or
**assumed** (carried from the nearest read build or from stock TGE 1.x). An assumed value is a
default for Seihai, not a fact about the client.

Scope: the Torque 3D side of the 3.x to 5.x clients. The DirectX Graal3D of 2000 is a separate
program and is not covered. 1.x and 2.x (Delphi) and 5.24r4 onwards have no Torque 3D side.
Seihai's profile has no `three_d` for those builds.

## The builds at a glance

| | 3.04 | 3.153 | 4.04r2 | 4.20r6 | 4.20r8 | 5.00r7 | 5.12 | 4.20 Linux |
|---|---|---|---|---|---|---|---|---|
| Torque protocol | 9 | 19 | 19 | 21 | 24 (lab) | 24 | 24 | 24 (lab) |
| Game layer | TGE | TGE | TGE | GameObject | GameObject | GameObject | GameObject | GameObject (lab) |
| Class table | none | 3 types | 3 types | 2 types | 2 types *assumed* | 2 types | 2 types | 2 types *assumed* |
| Client sends moves | yes *assumed* | yes | yes | no, reports position | no *assumed* | no *assumed* | no, reports position | no *assumed* |
| Mission phases | 3 *assumed* | 3 *assumed* | 3 | 2 *assumed* | 2 | 2 | 2, and optional (cap) | 2 (lab) |
| Local `.ter` terrain | yes *assumed* | yes | yes | no *assumed* | no *assumed* | no *assumed* | no | no *assumed* |
| Streamed terrain chunks | no | yes | yes | yes | no: crashes after the TerrainBlock (lab) | yes | yes (lab) | no *assumed as 4.20r8* |
| TorqueScript | compiles | compiles | none | none *assumed* | none | none *assumed* | none | none *assumed* |
| Runs script a server sends | no *assumed* | no | no | no *assumed* | no | no *assumed* | no | no *assumed* |
| Terraformer | full | full | greyscale only | greyscale *assumed* | greyscale *assumed* | greyscale *assumed* | greyscale only | greyscale *assumed* |
| Greyscale import | any *assumed* | any *assumed* | 32-bit RGBA only *assumed* | 32-bit RGBA only *assumed* | 32-bit RGBA only *assumed* | 32-bit RGBA only *assumed* | 32-bit RGBA only (lab) | 32-bit RGBA only *assumed* |
| Texture names | as named *assumed* | as named *assumed* | as named *assumed* | strip `.png` *assumed* | strip `.png` *assumed* | strip `.png` *assumed* | strip `.png` (cap) | strip `.png` *assumed* |
| Download refuses | *not read* | *not read* | `.dso .cs .ter` | *assumed as 5.12* | *assumed as 5.12* | *assumed as 5.12* | `.dso .cs .ter` | *assumed as 5.12* |

The Mac 4.04r2 and Mac 5.12 rows take their Windows twin's values, all assumed (T3D-004).

"4.20 Linux" is the Linux 4.20r6 and 4.20r8 builds (`G3D22126`). They link as protocol 24, not
21, so they take 5.12's row except where the 2026-11-25 lab
([lab-2026-11-25-g3d-worlds.md](../torque/lab-2026-11-25-g3d-worlds.md)) read them. Seihai's
"4.20r6" row is the Mac build the Tiger lab ran (`G3D27076`), which
[login-tokens-3x-7x.md](../protocol/login-tokens-3x-7x.md) dates to the 4.10r2 era.

## What each field controls in Seihai

- **Handshake and framing** (`protocol`, `game`, `class_table`, `class_ids_12bit`,
  `length_prefixes`): what the gserver writes in the connect accept and how it frames events and
  ghosts. The gserver picks this by the protocol number the client sends, so an assumed protocol
  only matters when Seihai presents itself as that build.
- **Game layer** (`game_layer`, `mission_phases`, `phases_optional`, `client_moves`,
  `control_objects`): whether the server sends datablocks and a `Player`, or `GameObject`s; how many
  mission phases to drive; and which class may be the control object. 5.12 accepted a `Camera` as its
  control object and no mission phases at all from a third-party server (cap, 2026-11-24).
- **Terrain** (`ter_file`, `ter_max`, `terrain_chunks`, `chunk_cache`, `terrain_texture`,
  `terrain_chunk_max`): whether a server may offer streamed terrain, where the client caches it
  (`levels3d/heights/<server>/heights<x>-<y>.dat` and `heights.info`, one name per line, in
  [terrain-512.md](../torque/terrain-512.md)), and the 1023-byte limit on one compressed chunk.
  Chunk payloads for 4.20 and 5.00r7 are assumed to be 5.12's; only 5.12's has been read in full.
- **Scripts and tools** (`torque_script`, `server_scripts`, `terraformer`, `greyscale_rgba32_only`, `terrain_editor`): only 3.04 and 3.153 run
  TorqueScript, and no read build has a path for a server to make it run new script (3.153: T3D-009, static). 4.04r2 and 5.12 keep `TerrainEditor` and a Terraformer cut to `loadGreyscale`,
  `saveGreyscale` and `setTerrain`
  ([script-and-terrain-tools-by-build.md](../torque/script-and-terrain-tools-by-build.md)). A server
  must not send `.cs` or `.dso` to a build that does not compile them.
  On 5.12 a GS2 weapon can create the Terraformer; `loadGreyscale` fetches the image over TCP, and
  only a 32-bit RGBA PNG is safe there: a 24-bit RGB or 8-bit grey PNG crashes the client (lab,
  PR #854). `setTerrain` returns 1 only when a TerrainBlock exists.
- **Formats** (`dts_min`, `dts_max`, `dif_version`, `three_ds`, `md3_version`): what shapes a server may name.
  Both 4.04r2 and 5.12 take the DTS version from the low byte of the version word and accept up to
  24. 4.04r2 has no floor: as in stock TGE, versions below 19 go to an old-format reader. 5.12
  rejects anything below 17 and sends 17 and 18 to the old reader. Both require DIF
  InteriorResource version 44 with Interior version 0 (T3D-029, static). Whether every version in range draws is still for the renderer lab.
  On Linux 4.20 a DTS 17 shape froze the client although its loader takes it, so a server should
  serve DTS 24. That build also crashed on a `.3ds` with no materials, a truncated `.3ds`, or a
  chunk length past the end of the file, so a server should check `.3ds` files before it names
  them. 4.04r2 has an MD3 loader and 5.12 has none.
- **Files** (`texture_names`, `download_refused`, `bigdata`, `bigdata_chunk_max`,
  `udp_port_offset`): 5.12 strips `.png` from material texture names and requests and stores the
  bare name, so a server must serve the image under its bare name too. The resource-miss path never
  asks for `.dso`, `.cs` or `.ter`. BigData text chunks carry at most 191 bytes.

## Updating

When a board row in [`torque/3d-capability-board.tsv`](../torque/3d-capability-board.tsv) closes,
change the value and its evidence tag in `three-d.toml`. Seihai mirrors the file with
`seihai/tools/gen_three_d_fixture.py`, and seihai-core's unit tests compare every `three_d` row
with the mirrored fixture.
