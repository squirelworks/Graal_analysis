# Objects: signs, chests, doors, blocks

Part of the [original NPC library](../README.md). Covers the `object / signs`, `object / chests`, `object / doors` and `object / blocks` categories of [`behaviours.md`](../../behaviours.md).

| File | What it does |
| --- | --- |
| `sign-basic.gs1` | Shows one line when the player faces it. |
| `sign-quest.gs1` | Notice board whose text follows two quest flags. |
| `sign-read-once.gs1` | A note that vanishes for good once read (`playerendsreading`). |
| `sign-countdown.gs1` | Touch to start a countdown drawn above the post. Says "Time!" at zero. |
| `sign-hush.gs1` | Reading it stops the background music. |
| `chest-rupees.gs1` | Pays rupees once per player and keeps the open frame on later visits. |
| `chest-random.gs1` | Weighted random drop (rupees, bombs, arrows or a heart container) placed in front of the chest. |
| `chest-password.gs1` | Gives a riddle on touch. Saying the answer nearby opens it. |
| `chest-equipment.gs1` | Sword upgrade that refuses if the player's sword is already as good. |
| `chest-mimic.gs1` | First touch springs an explosion and a hit. After that it is an empty box. |
| `door-timed.gs1` | Opens on touch, closes after 2 s, waits while the player stands in the doorway. Runs on every client. |
| `door-key.gs1` | Locked door that uses up a small key and stays open. |
| `key-pickup.gs1` | The small key for `door-key.gs1`. Holds one key at a time. |
| `door-password.gs1` | Gate that opens for 5 s when a nearby player says the word. |
| `door-clear-room.gs1` | Shutter that lifts when the level's last baddy dies (`compusdied`). |
| `block-pushable.gs1` | Block the player can push and pull. |
| `block-night.gs1` | Shown only at night, or only by day, from a `night` flag. |
| `block-chime.gs1` | Plays a sound when bumped, at most once a second. |
| `block-dropper.gs1` | Places up to four crates (`putnpc`) at eight-second intervals. |
| `crate.gs1` | Liftable crate that breaks into splinters when thrown. |
