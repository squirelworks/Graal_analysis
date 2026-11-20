# Static reads for Appendix E, fourth batch (2026-11-20)

Date: 2026-11-20. Evidence: **[bin]** (a disassembler read of the real client executables on the
Mirae lab, with no client run). Only behaviour is given here. Covers App. E#203, E#206, E#311,
E#312 and E#507.

Builds read: 2.05 rev 2 `Graal.exe`, 2.17.1, the real Windows 2.22 `Graal_222.exe`, 2.31 and the
3.04 client.

## The `#E` message code in 2.05 (E#203)

- In 2.05 rev 2, `#E` always expands to a single space. No feature fills the field behind it, so it
  is a placeholder.
- The same expander shape was not found in 2.17.1, 2.22 or 2.31, so the bare `#5` and `#6`
  scanner change in 2.17 was not reached by this read.

## The `move` queue in 2.05 (E#206)

- The `move` command has two callers: the GS1 command, and a move received from the network, which
  brings its own start position.
- Option bits 0 and 1 (the value and 3): 0 replaces the queue. 1 appends, but replaces when the end
  of the queue is more than 5 tiles away (the sum of the x and y distances).
- The queue holds at most 100 records, and the hundredth forces a replace.
- One consumer loops over every NPC in the local player's level and advances each queue once per
  call. It does not catch up for elapsed time.
- This fits "once per 50 ms step, with no catch-up", but that the consumer runs once per step was
  not shown.

## Explosions on 2.22 (E#311)

- An explosion is one centre piece and four arms. Each arm has a piece every 2 tiles, out to twice
  the power in tiles (the power is capped at 15). Each piece lives 12 ticks.
- Each tick, a piece hurts the local player when the piece's x + 1 is less than 1 tile from the
  player's x + 1.5, and the piece's y + 1 is less than 1 tile from the player's y + 2. The
  level-cell, can-be-hurt and `noplayerkilling` rules of shots (below) apply too.
- The damage is half a heart, or a full heart when the explosion was made with kind 3. Shots make
  kind 1. The knockback follows the piece's arm.
- So the measured hit pattern comes from the 2-tile spacing and the strict "less than 1" windows:
  the piece rows sit at the bomb's y, y ± 2 and so on. A full heart comes from a kind-3 explosion,
  not from two pieces overlapping.
- Not traced: which bomb sources make kind 3 on 2.22, and whether the hurt routine's cooldown lets a
  second piece in the same tick add damage.
- Each piece also breaks the bush, pot and rock patterns under its four corner probes, and fires
  `exploded` on an NPC it touches.

## The shot message on 2.22 (E#312)

The receiver of server message 19 (a shot):

- reads x and y as half tiles, then a flags byte, then a power or gani byte (less 32), then the last
  byte less 33 as the shot type;
- in the flags byte, the low 2 bits are the direction; bit 4 makes a second effect call; bit 8 links
  the shot to the sending player and copies one of that player's fields onto the shot;
- ignores a message of 5 bytes or fewer, and any shot that arrives while the player has no current
  level.

When it makes the shot it stores the level's `noplayerkilling` flag on it. The level keeps that
flag twice, scrambled, and checks the two copies against each other.

Each tick, the shot hurts the local player only when all of these hold:

- it is in the player's own level cell, the centre of the 3 × 3 update;
- it was not made on a `noplayerkilling` level and is not bouncing;
- the usual can-be-hurt check passes;
- the shot's box overlaps the player's box, x + 0.5 to x + 2.5 and y + 1 to y + 3;
- one field copied from the shot's owner equals the same field on the local player (0 when no owner
  is linked). That field is not identified.

On a hit, types 0 and 1 can be stopped by a shield held facing the shot (shield level above 0).
Otherwise the damage is half a heart for types 0 and 2, and a full heart for types 1 and 3. A
`noplayerkilling` level blocks the damage when the owner is a known player. Type 2 and up also make
an explosion at the impact point (power 2), on an NPC, a wall or a baddy too.

So shot types 0 and 1 (last byte 33 and 34) can hurt a receiving client directly. The earlier lab
results fit a blocked direct hit: the owner-field match or a level flag.

## Sheet type 5 on 3.04 (E#507)

- Type 5 comes from a per-level tile-type table and is a walk rule, not only a drawing variant.
- It sets a byte flag on the level object, takes its own path in the walk classifier, and the
  height and ground query returns 0 for it.
- What fills the per-level table (server tile definitions or a script) was not traced.
