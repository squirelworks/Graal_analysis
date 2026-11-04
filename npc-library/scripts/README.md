# Original NPC library

New GS1 NPC scripts, written from scratch for this repository. **Every line here is original work.** No script was copied, adapted or paraphrased from the GR-V1 level scrape or any other archive. The only inputs were:

- the own-words behaviour summaries in [`../behaviours.md`](../behaviours.md), used as a list of the kinds of NPC worth having;
- the reference manual's scripting part ([`manual/08-scripting/`](../../manual/08-scripting/)), for what the 2.05 client accepts;
- our own design.

The scripts are free for anyone to use on their own server or levels.

## Dialect

The target is GS1 as the **2.05 rev 2** client parses it: the 161-command table of manual §8.2.4. The scripts avoid:

- commands that 2.05 parses but ignores (§8.2.4.9);
- commands that only the 2.22 documentation has (§8.2.7.3);
- `#` codes beyond `#c`, `#s(...)` and `#v(...)` (the full set is open, App. E#203);
- conditions that can be between 0 and 1 (App. E#200), so every test is a comparison or a flag.

They also avoid the commands that the 2.22 documentation drops (the † rows of §8.2.4), so they should run unchanged on the later 2.x clients up to 2.22. That is an inference from the tables; no lab run has confirmed it yet. Clients from 2.3 onwards run NPCs on the NPC server and 4.x onwards use GS2 (§8.3), so these scripts are for classic offline and 2.x-era servers.

`tools/gs1-lint/gs1lint.py` checks every `*.gs1` file here against the manual's table. Its `Library` test runs in CI:

```
python tools/gs1-lint/gs1lint.py npc-library/scripts
```

## Conventions

- Every file starts with a header that gives its name, the category in `behaviours.md` it covers, a suggested image, the events it uses, and any flags it reads or sets.
- Values meant to be changed are marked `// <-`.
- Flags that must be unique per copy (a chest's "opened" flag, for example) are named in the header. Rename them in every place they appear.
- Image and sound names are placeholders. Use whatever your level's art provides.
- Positions are in tiles, and `x`, `y` is the NPC's top-left corner.

## Scripts

### objects/ — signs, chests, doors, blocks

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
