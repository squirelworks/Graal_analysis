# Water, splashes and the built-in animation names

Date: 2026-10-28. Read from the 2.05 rev 2 client and checked against its
executable's string table. **[2.05]** These notes contain no addresses,
routine names or decompiler text.

## Built-in animations

The client keeps one table of animation names, which it plays as
`<name>.gani`. In table order:

| # | name | # | name | # | name |
|---|---|---|---|---|---|
| 0 | idle | 11 | carrystill | 22 | hurt |
| 1 | walk | 12 | hiddenstill | 23 | ridehurt |
| 2 | walkslow | 13 | carry | 24 | dead |
| 3 | kick | 14 | hidden | 25 | maps1 |
| 4 | sword | 15 | shoot | 26 | maps2 |
| 5 | ridesword | 16 | ridestill | 27 | maps3 |
| 6 | spin | 17 | ridefire | 28 | swim |
| 7 | push | 18 | rideeat | 29 | lava |
| 8 | grab | 19 | ride | 30 | carried |
| 9 | pull | 20 | sit | | |
| 10 | lift | 21 | sleep | | |

Uses that were seen in the code:

* The sword swing plays `sword`; on a horse, `ridesword`.
* The charged swing plays `spin`.
* The A key's grab plays `grab`, and its lift plays `lift`.
* The item key's "lay item" mode plays `hiddenstill`.
* Firing a weapon on a horse plays `ridefire`.
* A throw sets the player back to `idle`.
* Swimming plays `swim`, or `lava` on a lava tile (type 12).

## Water

The client checks the player's tile on every game tick. It skips the check
while the sword swings, while riding, and when the player is not under
local control.

* **Into a liquid tile.**
  * When not swimming already, the client starts a splash, which is break
    effect 5, at the player's position.
  * When the player was not walking at the time (a warp or a knock), it
    starts two more splashes.
  * It then enters swim mode with `swim`, or `lava` when the tile type
    is 12.
* **Off a liquid tile while swimming.** One splash, then back to standing.
* **Liquid test.** The lava animation is chosen inside the water branch, so
  the client's liquid test is true for lava tiles too. **[inf]** The test
  itself is a jump table that was not followed.

## Break effect sounds

Each break effect plays a sound as it starts, at `(x + 1, y + 1)` from its
anchor:

* `sounds/water.wav` for the splash (effect 5);
* `sounds/crush.wav` for every other effect.
