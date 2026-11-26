# Static reads closing five partial 3D rows: GS2 events, GameObject sync and draw-gating, keybinds, MD3 animation (T3D-021, T3D-016, T3D-015, T3D-057, T3D-031)

Date: 2026-11-26. Static reads of `Graal3DEngine.dll` (5.00r7 = 5.12, [T3D-104](3d-engine-dll-interface-and-events-2026-11-26.md)) and the 4.04r2 engine. Behaviour only; no addresses, no decompiled text. Board rows:
[T3D-021, T3D-016, T3D-015, T3D-057, T3D-031](3d-capability-board.tsv). **[bin]**

These five rows were each "partial" from a live lab run; this pins the static side so a server or renderer knows the mechanism, not just the observed effect. T3D-014 and T3D-096 are already closed by the typed GS2 surface ([gs2-3d-typed-surface-512-2026-11-26.md](gs2-3d-typed-surface-512-2026-11-26.md)); T3D-014's open piece (the 5.12 `Sky`/`Sun` names) is covered there — `Sky` (30 members), `Sun` (3), `fxSunLight` (52).

## T3D-021 — the GS2 script events the 3D engine fires (5.12)

The full `on*` callback set the engine dispatches into the client's GS2, by area:

- **Session:** `onGraal3DConnectionEstablished`, `onGraal3DLoginStep` (the live lab saw steps 4, 5, 6), plus `setGraal3DConnectionError` and the `isGraal3DMode` predicate (`isgraal3d` true in 3D; `isGraal3DMode` is the engine's own name and was *absent* from the weapon surface in the live run, matching this split).
- **Frame / GUI:** `onGraalVideoFrameDrawn`, `onGuiUpdate`.
- **Input:** `onInputEvent`, `onClick`, `onDblClick`, `onRightClick`.
- **Shape / physics:** `onEndAnimation`, `onImpact`, `onCollision`, `onEnterLiquid`, `onLeaveLiquid`.
- **Mounting:** `onMount`, `onUnmount`.
- **Object lifecycle:** `onAdd`, `onRemove`.
- **Ghosting:** `onGhostAlwaysStarted`, `onGhostAlwaysObjectReceived`.
- **Chat / RPG:** `onRCChat`, `onRPGMessage`.

The engine also exposes `runGraal3DScripts` (the script-run entry). This is the static completion of the live partial (which had confirmed only `onGraal3DLoginStep` and `onRPGMessage`): servers and weapons can rely on this set, and on the collision/liquid/mount events firing client-side.

## T3D-016 — why a client-script-made GameObject never draws (5.12)

A GameObject in 3D is a **server-ghosted scene object**. The decisive tell is the engine's own log line when a non-ghosted object's state is pushed: *"failed to send TGameObjectVar … object not ghosted yet."* The rendered scene is the ghost set downloaded in **"Phase 1: Download Ghost Objects"** (`GhostAlwaysSet` / `GhostAlwaysObjectEvent`), and per-object state syncs as named object-vars only once the object is ghosted.

So a GS2-created GameObject (via the `graal_setCreateGraal3DGameObject` host callback) builds the object record and fetches its shape, but — with no server ghost assignment — it is **never entered into the ghosted scene set the renderer iterates**, and so never draws. That is the static root of the live finding (a script-made GameObject is created and its shape fetched but nothing appears). Creating, moving and deleting it locally operate on the record; drawing requires the object to be ghosted from the server. A 2D gserver driving a weapon therefore cannot make visible 3D content by client-side create alone; the object has to come down the ghost channel.

## T3D-015 — how GameObject properties reach the wire (5.12, static transport)

The GameObject visual/physical properties are GS2 object properties: `shape`/`shapefiles`/`shapebox`/`scaledshapebox`/`shapeobject`, `skin`, `attr`/`attrobjects`, `solid`, `collision`, `shadow`, `alpha`, `movetype`, `liquidtype`/`liquidheight`, `scale`/`scaleVal`/`scaleHeight`, `rotation`/`position`/`direction`/`yaw`, `texture`, the `light*` set (`lightcolor`, `lightdirection`, `lightmap(s)`, `lightFalloffMono`, `lightScene`, `lightSelection`), the `anim*` set (`animelevation`, `animazimuth`, `animsize`, `animrotation`, `animbrightness`, `animcolour`), and `shaperotatemin/max`, `shapescalemin/max`, `rotationtime`/`rotationkeys`/`rotationsnap`.

On the wire these are **not a fixed-offset packed struct**. Each syncs as a **named `TGameObjectVar`** — keyed `class::property` with its value — over the per-object ghost channel, and the send is gated on the object being ghosted (the same "object not ghosted yet" path as T3D-016). So "what each property maps to on the wire" is: a named object-var update (name + value) per property, not a bitfield at a fixed offset. The per-property *client visual effect* (what `solid`/`shadow`/`alpha`/`liquid*` do on screen) stays the renderer lab's probe, which owns this row; this note pins the transport underneath it.

## T3D-057 — the keys the 5.12 client handles itself

The engine owns a GS2 `bind`/`unbind` + `moveMap2D` system and routes raw keys through `graalkeypressed`. The client-handled move/action vocabulary:

- **3D moves:** `moveforward`/`moveforward2`, `movebackward`/`movebackward2`, `moveleft`/`moveleft2`, `moveright`/`moveright2`, `moveup`, `movedown`, `turnleft`, `turnright`, `jump`, `mousefire`.
- **2D moves (moveMap2D):** `moveleft2d`, `moveright2d`, `moveup2d`, `movedown2d`.

Recognized key names include `space`, `enter`, `tab`, `escape`, `shift`, `ctrl`, `alt`, `backspace`, `backslash`, `home`, `end`, `pageup`, and the arrow directions. `getAllowCursorOff` is a client callback (the mouse-lock gate). The specific default key→action pairing is assembled by `bind` calls (scriptable), so the input contract is "these actions and these keys are client-handled," not a single fixed built-in table. (Raw-key routing to `graalkeypressed`/mouse-look is [T3D-102](3d-engine-dll-interface-and-events-2026-11-26.md).)

## T3D-031 — how 4.04r2's MD3 loader picks an animation

4.04r2's MD3 player model is the **Quake-3 player-model convention**: `_lower.md3` + `_upper.md3` + `_head.md3`, joined at `tag_torso`/`tag_head`, with `_lower_default.skin`/`_upper_default.skin` and an `_animation.cfg` that gives each animation its first frame, frame count, looping and `framesPerSec`.

The animation is picked by a **numeric player-animation id** mapped through `_animation.cfg`'s ranges, with the lower and upper bodies animated independently:

- **Lower body (`LEGS_*`):** `LEGS_IDLE`, `LEGS_WALK`, `LEGS_RUN`, `LEGS_BACK`, `LEGS_JUMP`, `LEGS_JUMPB`, `LEGS_LAND`.
- **Upper body (`TORSO_*`):** `TORSO_STAND`, `TORSO_STAND2`, `TORSO_RAISE`, `TORSO_DROP`.

An out-of-range id is rejected with *"MD3: unknown player animation %d."* So a server picks the pose by setting the player-animation id; the loader resolves it to a frame range per `_animation.cfg`. (MD3 is a 4.04r2-only format, gone in 5.12 — [T3D-013/T3D-055](3d-formats-renderer-camera-by-build.md).)

## Summary for the server

| Row | Answer (static) |
| --- | --- |
| T3D-021 | 22 GS2 `on*` callbacks fire client-side: session, frame/GUI, input, collision/liquid/impact, mount, add/remove, ghosting, RC/RPG chat |
| T3D-016 | a script-made GameObject never draws because the rendered scene is the server **ghost set**; a non-ghosted object is created and shape-fetched but never entered into it |
| T3D-015 | GameObject properties sync as **named `TGameObjectVar`** updates (name+value) over the ghost channel, gated on ghosting — not a fixed-offset struct |
| T3D-057 | the client handles its own `moveMap2D` binds; action + key vocabulary enumerated; default key→action pairing is set by scriptable `bind` calls |
| T3D-031 | 4.04r2 MD3 is the Quake-3 lower/upper/head triple + `_animation.cfg`; animation chosen by a numeric `LEGS_*`/`TORSO_*` id, out-of-range rejected |

The common thread across T3D-015/016: 3D GameObjects are **server-ghosted** objects whose state travels as named object-vars; the 2D gserver's weapons can read and script them, but visible 3D content must be ghosted from the server, not created purely client-side.
