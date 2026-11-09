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
- `#` codes beyond `#c`, `#s(...)`, `#v(...)` and mode-dependent `#b` (outer membership is cataloged but helper/renderer semantics remain partial, App. E#203; ordinary message mode zero removes `#b` in the checked original 2.05r2);
- unqualified condition parsing across builds (App. E#200). The exact 2.05r2 follow-up distinguishes computed nonzero truth from bare named flags and identifies a constant-comparison folding defect; comparisons alone are not a universal workaround.

They also avoid the commands that the 2.22 documentation drops (the † rows of §8.2.4), so they should run unchanged on the later 2.x clients up to 2.22. That is an inference from the tables; no lab run has confirmed it yet. Clients from 2.3 onwards run NPCs on the NPC server and 4.x onwards use GS2 (§8.3), so these scripts are for classic offline and 2.x-era servers.

`tools/gs1-lint/gs1lint.py` checks every `*.gs1` file here against the manual's table. Its `Library` test runs in CI:

```
python tools/gs1-lint/gs1lint.py npc-library/scripts
```

## Tested in a real client

All 96 scripts were run in a real 2.05r2 client on a GServer-v2 lab on 2026-11-04. That run found eleven problems, all fixed here, and the lint now checks for the ones it can see:

- Text in function arguments is written bare, spaces included. 2.05 keeps quote marks as part of the text, so `strequals(#c,"buy bombs")` never matches. The lint reports quoted text as an error.
- `say2` does not wrap. Keep each line to about 32 characters and break lines with `#b`. The box shows three lines and pages on. The lint warns about long lines.
- An empty `setcharprop #c,` does not clear a chat bubble. Text that should disappear is shown with `message` and cleared with `message ;`. The lint reports the empty form.
- The word `toweapons` must not appear in a comment, because GServer-v2 names the weapon after the first one in the text. The lint reports it.
- A script placed with `putnpc` must be a file the server serves (`.txt` unless `foldersconfig` serves `.gs1`) and must have no comments, because putnpc joins the lines before comments are removed. `crate.gs1` and `bat-swoop.gs1` are comment-free for that reason, and a test checks every `putnpc` target.
- `playerfullhearts` cannot be written (`playerrupees`, `playerbombs`, `playerdarts` and `playerhearts` can), so heart containers are given as the `fullheart` item.
- An explosion placed by an NPC does not hurt the player, so scripts that should hurt use `hurt`.
- `playertouchsme` only fires while the player moves, so anything that acts on a player standing still checks the position on a timer.
- A thrown NPC keeps the spot where it landed.
- Weapons switched off with `disableweapons` stay off in other levels, and the server saves that to the account. `items/weapons-on.gs1` turns them back on in the levels around a peace zone.

The results, one line per script, are in the lab notes for that run.

## Conventions

- Every file starts with a header that gives its name, the category in `behaviours.md` it covers, a suggested image, the events it uses, and any flags it reads or sets. The two scripts placed with `putnpc` are the exception: they have no comments, and their family README carries the header.
- Values meant to be changed are marked `// <-`.
- Flags that must be unique per copy (a chest's "opened" flag, for example) are named in the header. Rename them in every place they appear.
- Image and sound names are placeholders. Use whatever your level's art provides.
- Positions are in tiles, and `x`, `y` is the NPC's top-left corner.

## Families

Each family folder has its own README with a table of what every script does.

| Folder | Covers (`behaviours.md` categories) |
| --- | --- |
| [`objects/`](objects/README.md) | signs, chests, doors and keys, blocks (object / *) |
| [`transport/`](transport/README.md) | level warps, lifts, teleporter pads (transport / *) |
| [`interaction/`](interaction/README.md) | switches, quest flags, scenery set-up, breakables and liftables, seats, wardrobes (interaction / *, dialogue seats) |
| [`dialogue/`](dialogue/README.md) | talkers, quest givers, keyword NPCs, shopkeepers (dialogue / speech) |
| [`enemies/`](enemies/README.md) | lungers, wanderers, chasers, shooters, guards, bosses, wave controllers (combat / baddies, combat / weapons AI) |
| [`hazards/`](hazards/README.md) | spikes, fire, push-back traps, turrets, timed bombs (combat / hazards) |
| [`spawners/`](spawners/README.md) | respawners, enemy spawners, followers, animation cycles (spawn / timers, misc / other) |
| [`items/`](items/README.md) | weapon pickups, warp ring, digging tool, zone rules (combat / weapons, interaction / flags) |
| [`minigames/`](minigames/README.md) | races, target ranges, games of chance (no single category; built from the same parts) |

A folder appears when its pull request is merged.
