# Movement

## Keys · high

a client routine at an address fills two name tables at startup (`param_2 == 0xFFFF` and `param_1 == 1`).

| slot string | neighbor string |
| --- | --- |
| `up` `left` `down` `right` | `item` `attack` `action` `map` `switchtochat` `itemlist` `pause` |
| `moveUp` `moveLeft` `moveDown` `moveRight` | `doD` `doS` `doA` `doM` `doTab` `doQ` `doP` |

a client routine stores the animation names `walk`, `bomywalk`, and `walkslow`. It also stores `TProjectile`. It does not add a step to a coordinate.

## Board bounds · high

The level board is 64 by 64. a client routine accepts a tile x only when `x < 0x40`, a tile y only when `0 <= y < 0x40`, and a run width only when `x + width <= 0x40`. The cell index is `(y * 0x40 + x) * 2`.

That is the only spatial test recovered. It is the board writer, not a per-step walker.

## Not recovered

| topic | result |
| --- | --- |
| one-tile step on a key | no function adds 1 to a player x or y next to `moveUp` |
| blocking tile test | not found |
| water | the string `water` occurs 15 times. The referenced function a client routine registers Torque vehicle fields (`splashFreqMod`, `bodyFriction`, `collisionTol`). No Graal water tile |
| ledge | the string is absent |
| inbound “direction” | packet id 7 stores the low 2 bits of one byte at `player+0x38` and the upper bits at `+0x37`. That split is real. Calling the low bits a facing is a guess, so it stays unnamed |
