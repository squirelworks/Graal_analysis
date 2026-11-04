# Hazards: spikes, fire, traps, turrets

Part of the [original NPC library](../README.md). Covers `combat / hazards` in [`behaviours.md`](../../behaviours.md): things that hurt on contact, push the player back, hide behind a password, can be thrown, remove themselves after triggering, or fire on a timer.

Damage uses `hurt n` (half-hearts, with knockback away from the NPC). A negative value heals, as the 2000 documentation says (manual §8.2.4.6). Turrets fire with `shootarrow` and `shootfireball` from the NPC's edge (§8.2.4.7).

| File | What it does |
| --- | --- |
| `spikes.gs1` | Hurts on contact. Non-blocking, drawn under the player. |
| `spikes-timed.gs1` | Up 1 s, down 2 s. Catches a player standing on it as it rises. Staggered with an offset. |
| `fire-pushback.gs1` | Burns and throws the player one tile back the way they came, if that tile is free. |
| `healing-spring.gs1` | Heals half a heart a second while the player stands in it (negative `hurt`). |
| `password-trap.gs1` | Explodes under anyone until a nearby player says the word. Then it stays safe for them. |
| `throwable-hazard.gs1` | Spiked ball that hurts to bump but can be lifted, thrown and shattered (`hitobjects`). |
| `one-shot-trap.gs1` | Falling rock: a warning, then a hit if the player is still under it. Then `destroy`, so it never fires again. |
| `turret.gs1` | Fires an arrow in a fixed direction on a steady beat, with an offset for staggered volleys. |
| `fire-spitter.gs1` | Every 2 s, spits a fireball toward a player within 8 tiles. |
| `bomb-timed.gs1` | Barrel lit by touch or hit. A 3 s visible countdown (`timershow`), then a big explosion. |
