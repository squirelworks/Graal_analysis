# 3D audio and particles on 4.04r2: networked classes are 4.04r2-only and unplaceable; GS2 sound runs, script particles need a definition (T3D-061, Linux 4.04r2)

Date: 2026-11-25. Registered-class / GS2 `-listscriptfunctions` reads for 4.04r2 vs the 5.12-class engine plus a single-client protocol-19 lab on native Linux 4.04r2 (g3d404 route). Observation only. Board row: [T3D-061](3d-capability-board.tsv). Companion to [T3D-049](3d-weather-404r2-2026-11-25.md) (weather), [T3D-084](3d-sound-paths-2026-11-25.md) (sound) and [T3D-085](3d-particles-512-vs-404r2-2026-11-25.md) (particles); builds on [T3D-081](3d-object-classes-by-build-2026-11-25.md).

## Headline

The TGE **3D audio** classes (`Sim3DAudioEvent`, `AudioEmitter`, …) and the networked **particle** class (`ParticleEmitterNode`) are **4.04r2-only** and gone from the 5.12-class engine — and, like weather, **our lab server cannot place one** (no scene keyword, no matching datablock in the protocol-19 set). What *is* reachable on protocol 19 is the **GS2 sound path** (`play`/`play2`/`playlooped2` run and resolve the file) and the **script `TParticleEmitter` API** (reachable but draws nothing without a particle-type definition).

## Registered-class evidence **[bin]**

| class | 4.04r2 | 5.12-class (4.20r6) |
| --- | --- | --- |
| `Sim3DAudioEvent` / `Sim2DAudioEvent` | registered | – |
| `AudioEmitter` / `AudioDescription` / `AudioProfile` / `AudioEnvironment` | registered | – |
| `ParticleEmitterNode` / `ParticleEmitterNodeData` / `ParticleEmitterData` / `ParticleData` | registered | – |

- All present on 4.04r2 (binary rep + GS2 dump), absent on the 5.12-class engine. Consistent with [T3D-081](3d-object-classes-by-build-2026-11-25.md)/[T3D-084](3d-sound-paths-2026-11-25.md)/[T3D-085](3d-particles-512-vs-404r2-2026-11-25.md).
- GS2 members on 4.04r2: `AudioEmitter (SceneObject)`; `ParticleEmitterNode (GameBase)` with `datablock`/`emitter` refs — both datablock-backed, needing `AudioDescription`/`ParticleEmitterData`/`ParticleData`.
- **The shared GS2 `TParticleEmitter (TGraalVar)` scripting class is on 4.04r2 too** (`particletypes`, `maxparticles`, `emit()`, `dropemitter`) — the same script particle API as 5.12 ([T3D-085](3d-particles-512-vs-404r2-2026-11-25.md)), distinct from the networked `ParticleEmitterNode`.
- The **4.04r2-only TGE audio funcs** `playaudio`/`stopaudio`/`playthread`/`playthreadext` are in the dump, **but `playaudio` is not callable from a client GS2 weapon** (client reports "not found") — not a usable client path. `play`/`play2`/`playlooped2` are on both builds ([T3D-084](3d-sound-paths-2026-11-25.md)).

## Server emit-path verdict **[srv]**

**No path**, same as weather ([T3D-049](3d-weather-404r2-2026-11-25.md)): no audio/particle/emitter scene keyword; the protocol-19 datablock set is only `CameraData`/`PlayerData` (so the `AudioDescription`/`ParticleEmitterData`/`ParticleData` datablock these objects need is never sent); protocol-19 ghosts are Sky + stock TGE Player/Camera only ([T3D-106](3d-authoring-surface-2026-11-25.md)). The classes exist client-side; the server can't place one.

## Lab: protocol-19 single client **[lab]**

A `weapon3d` GS2 script ran on 4.04r2 (showtext reached "t12").

- **Sound — runs, file resolves.** `play("snd420.wav")`, `play2(...)`, `playlooped2(...)` ran and the client fetched `snd420.wav` (downloaded, ~1.7 KB). Same reachable Graal GS2 sound path as 5.12, now confirmed on **protocol 19**. `playaudio(...)` **errored** ("Function playaudio not found in script"). Audio output **not verifiable headless**.
- **Script particles — reachable, drew nothing.** The weapon set `particletypes`/`maxparticles` on a `showimg`'s `.emitter` and called `emit()` each tick with no error, but **no particles drew** — `particletypes` indexes a **particle-type definition** that was not present/served, so `emit()` had nothing to spawn.
- **Networked particle/audio — not creatable.** `ParticleEmitterNode`/`AudioEmitter` need their datablock, which the server doesn't send; no client-script create binds.
- **Bonus — built-in weather/particle asset set.** The 4.04r2 3D client requests built-in snow/splash assets at startup (`g3d_playersnow1.png`, `g3d_splashsnow1/2.png`, `g3d_hairsnow1.png`, `g3d_splashxmas.jpg`; none served → not found). So the engine carries a **built-in particle/weather effect set** referencing these assets — not exercised here (assets absent, no trigger).

**Verdict:** GS2 sound calls **ran / file resolved** on protocol 19; networked audio/particle classes **[not reachable on this route]**; script `TParticleEmitter` **reachable but drew no particles** (no particle-type definition).

### Headless note

Audio not verifiable headless ([T3D-084](3d-sound-paths-2026-11-25.md)). Script particle sprites would be renderable under llvmpipe (it draws textures fine), so they'd be visually verifiable — but none emitted here, so there was nothing to see.

## For a server

- **Networked** `AudioEmitter`/`Sim3DAudioEvent`/`ParticleEmitterNode` on 4.04r2 would need new server support (a world audio/particle keyword, the matching datablocks in the protocol-19 set, ghost-after-datablock code) — a server gap to scope separately, not built here.
- **Script** sound works on both builds via `play`/`play2`/`playlooped2` (ship the `.wav` on disk with its extension, [T3D-084](3d-sound-paths-2026-11-25.md)). Making the **script** `TParticleEmitter` actually draw needs a particle-type definition supplied to the client.
- None of this applies to 5.12-class clients, where these classes are gone; the built-in snow/splash asset set is a 4.04r2 engine feature.
