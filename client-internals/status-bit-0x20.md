# STATUS bit 0x20: the sword is hidden (2.05)

The player STATUS property (prop 18) carries bit 0x20 while the `hidesword` timer is running. Read from the 2.05 program.

## How the bit is set

- The script command `hidesword n` takes one number. It is clamped to 0..30, multiplied by 20, and stored as a tick count (the game tick is 1/20 s, so `n` is in seconds).
- Each game tick, while the count is 0 or more, it goes down by one. It reaches -1 one tick after it reaches 0.
- When STATUS is built for sending, bit 0x20 is set when the count is 0 or more.
- The count starts at -1 when the player object is made, and is set back to -1 when the player is reset.

`hideplayer n` works the same way, with the same clamp and scale, but on its own counter, which drives bit 0x02 (hidden). In the command table, `hidesword` and `hideplayer` are entries 59 and 69. Both take one number argument (`R`).

## What the bit does

- Another player whose STATUS has 0x20 set (or 0x02) cannot hurt with a sword swing. The hit gate checks the attacker's STATUS (see `decomp-findings-2026-10-24-d/03-hit-gates-and-open-points.md`).
- In the local client, the counter is read only to build STATUS and to count down. Nothing else reads it, so `hidesword` does not stop the local swing itself. The swing is only refused a hit at the victim's end.

## Confirmed, inferred, not tested

- Confirmed: the command, the clamp and scale, the countdown, and the STATUS bit.
- Inferred: that a client also leaves out the sword picture of a player with bit 0x20. The drawing code was not traced.
- Not tested on a wire or in the lab.
