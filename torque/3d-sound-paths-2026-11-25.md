# 3D sound on 5.12 is the GS2 play2/play3d path; the Torque audio classes are 4.04r2-only (T3D-084)

Date: 2026-11-25. Registered-class and GS2 `-listscriptfunctions` reads for 4.04r2/4.20r8/5.00r7/5.12, plus a light lab invocation on native Linux 4.20r6 (5.12-class, protocol 24). Linux 4.20r6 is 3D-equal to 4.20r8 ([T3D-004](3d-engines-5007-512-and-403-411-2026-11-25.md)). Board row: [T3D-084](3d-capability-board.tsv). Builds on [T3D-081](3d-object-classes-by-build-2026-11-25.md)/[T3D-085](3d-particles-512-vs-404r2-2026-11-25.md) (datablock classes dropped from 5.12).

**Audio output is not verifiable headless** (no real audio device) — the deliverable is which sound paths exist and are reachable, and whether a GS2 sound call runs and resolves its file, not an audio recording.

## Torque audio classes — all 4.04r2-only **[bin]**

| class | 4.20r6 (5.12-class) | 4.04r2 |
| --- | --- | --- |
| `Sim3DAudioEvent` | no (not registered, no string) | registered |
| `Sim2DAudioEvent` | no | registered |
| `AudioEmitter` | no | registered |
| `AudioDescription` | no | registered |
| `AudioProfile` | no | registered |
| `AudioEnvironment` | no | registered |

The **entire Torque datablock audio family — `Sim3DAudioEvent`, `AudioEmitter`, `AudioDescription`, `AudioProfile`, `AudioEnvironment` — is 4.04r2-only and gone from the 5.12-class engine**, class rep and name string both ([T3D-081](3d-object-classes-by-build-2026-11-25.md): `AudioEmitter` is one of the eleven). The GS2 dumps agree: those classes appear only in the 4.04r2 dump.

## GS2 sound functions **[bin]**

| function | signature | 4.04r2 | 4.20r8 | 5.00r7 | 5.12 | what it is |
| --- | --- | --- | --- | --- | --- | --- |
| `play` | `play(str)` | Y | Y | Y | Y | play a 2D sound |
| `play2` | `play2(str, float, float, float)` | Y | Y | Y | Y | positional (x,y,z) sound — 3D |
| `playlooped` | `playlooped(str)` | Y | Y | Y | Y | looped 2D |
| `playlooped2` | `playlooped2(str, float, float, float)` | Y | Y | Y | Y | looped positional (x,y,z) — 3D |
| `play3d` | `play3d(str, bool, str, str)` | – | Y | Y | Y | a named 3D-sound call — new in the protocol-24 family |
| `stopsound` | `stopsound(str)` | Y | Y | Y | Y | stop |
| `setmusic`, `setmusicvolume(float,float)` | | Y | Y | Y | Y | music/volume |
| `playaudio`, `stopaudio`, `playthread`, `playthreadext` | | Y | – | – | – | 4.04r2-only (the TGE/datablock audio functions) |

- **3D positional sound** is `play2(str, x, y, z)` and `playlooped2(str, x, y, z)` — present on all builds, 4.04r2 included. The position args make it 3D; the engine attenuates by distance from the listener.
- **`play3d(str, bool, str, str)`** is new in the 5.x / protocol-24 family (absent on 4.04r2).
- **Falloff/distance:** no script-settable 3D-sound radius/falloff/rolloff appears — distance attenuation is implicit from the position arg vs the listener, handled by the engine (FMOD), not an authored radius. `play2`/`playlooped2` carry only position, not a radius.

### How 5.12 3D sound is done

**Via the GS2 client functions `play2` / `play3d` / `playlooped2`, not via the Torque `AudioEmitter` / `Sim3DAudioEvent` networked datablock path** — that whole class family is dropped from 5.12 (like the other datablock game classes). On 4.04r2 **both** paths exist (the Torque datablock audio and the Graal `play2`/`playlooped2`); on 5.12 only the Graal GS2 path remains, with `play3d` added.

## Lab: invoke a GS2 3D-sound call (4.20r6) **[lab]**

A `weapon3d` GS2 script ([T3D-018](3d-client-events-420r6-2026-11-25.md)) on `onCreated` called `play`, `play2(…,10,0,1)`, `play3d(…,false,"","")` and `playlooped2(…,0,0,1)` on a pre-placed 8-bit PCM `.wav` (on disk with its extension, [T3D-077](3d-texture-formats-420r6-2026-11-25.md)), then `play2` at a moving position every 3 s.

- **The call ran** — the client reached the sound calls, no disconnect or error.
- **The client resolved the sound file** — a `PLI_UPDATEFILE` for the `.wav` went out and the server answered "up to date", i.e. the `play*` calls triggered the sound-file lookup. This is the observable proof the path is reachable.
- **The audio engine initialised** — the console logged FMOD coming up on the ALSA backend; no sound/audio error.
- **Audio output itself is not verifiable headless** — nothing is audible, so this confirms the GS2 3D-sound call ran, FMOD initialised and the file resolved, not that the sound played or that attenuation was applied.

## For a server

- On a 5.12-class client, do 3D sound with the GS2 `play2`/`playlooped2` (position args) or `play3d` — **not** the Torque `AudioEmitter`/`Sim3DAudioEvent` datablock path, which is gone. Distance attenuation is automatic from the position vs the listener; there is no authored falloff radius.
- Ship the sound file on disk with its extension before the call, as for textures ([T3D-077](3d-texture-formats-420r6-2026-11-25.md)).
