# Items: weapon pickups and key items

Part of the [original NPC library](../README.md). Covers the pickup half of `combat / weapons`, the warp-ring pickups of `transport / level-warps`, the digging tool and outfit changers of `interaction / flags`, and weapon-free zones, all from [`behaviours.md`](../../behaviours.md).

Each weapon script plays two roles. Lying in a level it is a pickup. On touch it calls `toweapons Name`, which adds a copy of the NPC, script included, as weapon *Name* (manual §8.2.4.6), and then hides. The copy tests `isweapon` and reacts to `weaponfired`. The pickup checks `hasweapon(Name)` so it does not reappear for an owner. Weapon names are one word, because a bare argument with a space does not parse as one name. Do not write the word `toweapons` followed by a space anywhere else in the script, comments included: GServer-v2 names the weapon after the first `toweapons ` it finds in the raw text, so a comment that mentions it renames the weapon (seen with `warp-ring` in a real 2.05r2 client, 2026-11-04). Two scripts (`warp-ring`, `blast-rod`) rely on a weapon's own `timeout`. The manual does not say which client gets a weapon's timeouts, so we infer it is the owner's.

| File | What it does |
| --- | --- |
| `warp-ring.gs1` | Weapon `Warpring`: freezes and spins the player for a second, then warps to one of three towns. |
| `warpstone.gs1` | Weapon `Warpstone`, the key item for `transport/teleporter-keyed.gs1`. |
| `shovel.gs1` | Weapon `Shovel`: turns plain ground in front of the player into a hole tile (`board[]`, `updateboard`) and sometimes finds a rupee. |
| `sword-shrine.gs1` | Sword in the stone. Only a player who finished the shrine quest can draw it (sword power 2). |
| `peace-zone.gs1` | Turns weapons off inside a rectangle and back on outside it. Keep the zone away from links and warps: leaving the level from inside it leaves weapons off, and the server saves that to the account. Pair it with `weapons-on.gs1`. |
| `weapons-on.gs1` | Invisible; turns weapons back on when the player enters. Put one in every level reachable from a peace zone, including where players restart after dying. |
| `blast-rod.gs1` | Weapon `Blastrod`: spends a bomb for an explosion 3 tiles ahead. |
| `mask.gs1` | Weapon `Mask`: swaps the player's head image and sets `guard_pass` while worn. |
| `heart-piece.gs1` | Four pieces make a heart container. The count is kept in the string `heartpieces`. The fourth piece drops a `fullheart` item, because `playerfullhearts` cannot be written on 2.05. |
