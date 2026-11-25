# 3D engine static reads: sky functions, name tags, protocol, loaders, input (2026-11-25)

Static reads of the 5.00r7 3D engine, used in place of 5.12's, whose engine
is packed inside its exe. Behaviour only; no addresses or code. Board rows:
T3D-057, T3D-063, T3D-065, T3D-072, T3D-080, T3D-098. **[bin 5.00r7]**

## Sky, fog and view functions (T3D-063)

- `setSunColors`, `setSkyBandColors`, `setFogColors` and `setSkyBandSizes`
  each take one list. They fill a client-side day and night keyframe table.
  They do not touch the ghosted Sky or Sun. This explains why the live 5.12
  probe saw no change (live-512-gs2-3d-probe-2026-11-25.md).
- `syncTimeOfDay` takes two numbers.
- `updateVisibleDistance` takes no argument. It re-reads
  `$pref::Video::visibleDistance` (`visibledistance3D`).
- There is no `updateFogDistance` function.
- `lightScene` does a full relight.

## Name tags (T3D-065)

`GuiShapeNameHud` has `nameMaxDistance` and `nameDistanceFade`. It reads the
GameObject fields `nickname`, `nickcolor`, `movetype` and `liquidtype`.
Whether it skips the control object is still open.

## Protocol check (T3D-072, T3D-080)

- The connect reject has separate texts for a protocol that is too old, a
  protocol that is too new, and a wrong game.
- The 3D protocol numbers in the held builds are 19, 21 and 24.

## Loaders (T3D-098)

- `.3ds`, `.dts` and `.dif` loaders are registered.
- The DIF and ForceField readers check their version numbers.
- 4.03r3 and 4.11 could not be read: each is a single packed client.

## Input (T3D-057)

The engine binds the `moveMap2D` move commands itself. `getAllowCursorOff`
is a callback into the client exe, not a GS2 function. The full list of
default binds is still open.
