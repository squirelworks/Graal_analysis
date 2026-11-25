# Lab 2026-11-25: one-change 3D worlds on the real Linux 4.206 client

Date: 2026-11-25. Tags as in [README.md](README.md): **[run]** seen while running the real
client, **[inf]** inferred. Board rows: T3D-026 (the GameObject level on this build; the 5.12
side of the comparison is in a separate lab) and T3D-022 (login steps on the mission route).

## Setup

- **Client:** the real Linux 4.206 client, run in a headless lab VM. It identifies itself as
  `G3D22126` and links as **protocol 24**, not the 21 of the Mac 4.20r6 build in
  [wire-by-build.md](wire-by-build.md). So everything here is the protocol-24 path. **[run]**
- **Server:** the Seihai gserver-v2 (`graal3d = true`), on its mission route (two mission phases,
  then the control object). Everything ran on loopback inside the VM.
- **Worlds:** built by gserver-v2's `tools/lab/g3dlabworlds.py`. Each world changes one thing
  from a control scene (the Kokiri scene of the 2026-11-24 Graal3D pack, as `.3ds` models and PNG
  textures).
- **Method:** before each variant the client's download cache was cleared. Each variant was run
  once; crashes and hangs were run twice.

## Results **[run]**

| Change from the control | Client |
|---|---|
| none (control) | drawn in 3 of 3 runs; login completes (both mission phases, control object). `.3ds` models and the sky box draw plain white although every texture downloaded, also with the textures already cached. Fog shows at the horizon. |
| textures only extension-less, or only `.png` | same as the control |
| no `Sky` object | the background clears to flat dark red (128, 0, 0) |
| fog colour red | red horizon fog |
| Sky visible distance 2000; a Sky with one more texture name | same as the control |
| 64 or 512 more copies of one model | all drawn; the link held |
| `GameObject` section 2 = (1, 1, 1) / (2, 2, 2) / (0.5, 0.5, 0.5) | the object at normal, about double and about half size: **section 2 is the object's scale** |
| `.3ds` with materials and face-material groups removed | crash (segfault) just after "Graal3D has been activated!" (2 of 2) |
| `.3ds` cut at half its length | crash during mission phase 1 (2 of 2) |
| `.3ds` main chunk length 1000 bytes past the end | crash during mission phase 1 (2 of 2) |
| `.3ds` with about 0.5% of bits flipped, three seeds | two crashed, one drew |
| `.3ds` first point list claiming more points than it holds | drawn |
| `.3ds` first face's first point index 65535 | drawn |
| `.dts` version 24 (Marble Blast Gold shapes) | drawn |
| `.dts` version field 16 / 25 | rejected with a console error ("not supported anymore" / "only version 24 and before"); the client stays up |
| `.dts` version field 17 | the client froze on a dark-red screen; the server's 3D link timed out after about 30 s (2 of 2) |
| `.dif` version 44 (Marble Blast Gold interiors) | drawn. One interior out of view still changed the whole scene's lighting. |
| `.dif` version field 43 / 45 | rejected: "InteriorResource::read: incompatible file version found"; the client stays up |

No variant stopped at a login step, and the server dropped none.

## What follows for a server

- **Scale:** send section 2 of the `GameObject` update as the object's scale, (1, 1, 1) by
  default. The gserver now does.
- **Shape files:** this client does not survive a structurally broken `.3ds`. That covers a
  missing material, a truncated file and a chunk length past the end. A server should check
  `.3ds` files before it names them.
- **Version bounds:** `.dts` 17 is not a safe "oldest accepted" version on this build, even
  though the version-17 read path exists. Serve version 24. For `.dif`, only 44 is accepted.
- **Still open:** why textures draw white. It is either this build's `.3ds` texture path or the
  VM's software OpenGL. A Windows 5.12 run of the same control world settles it. **[inf]**
