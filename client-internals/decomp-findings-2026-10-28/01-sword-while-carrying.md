# Sword key while carrying

Date: 2026-10-28. From the 2.05 client (derived). 2.22 and 2.31 not read.

The game keys reach the player by index: weapon (default D), sword
(default S) and action (default A).

* **Sword key with an object carried:** no swing. The carried object is
  thrown, the same throw the action key does: it leaves from above the head,
  the carry sprite goes back to none (-1) and the idle gani is set. If the
  player's mode was walking, or the lay-down mode below, the mode goes back
  to idle. No swing precondition (sword power, swimming) is checked on this
  path.
* **Sword key with empty hands:** the normal swing.
* **Action key with an object carried:** throws, except in the lay-down
  mode, which has its own action.
* **Weapon key with an object carried:** does not throw. It only matters when
  the carried sprite is 239, 261 or 263; then the player enters a lay-down
  mode with its own gani. What that mode does was not read.

Online, a throw also triggers the client's player-props send (the carry
sprite change); the exact bytes were not captured.

Not confirmed in a lab capture yet.
