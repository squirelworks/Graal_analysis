# Knockback and the packet hits

## Knockback of a hit
The routine that hurts the player takes a power in hearts and a knockback vector (dx, dy). It sets hurt mode (mode 3, counter 40) and stores the vector scaled to length one tile. A zero vector is replaced by one tile east.

For the first five ticks of hurt mode (the counter reads 39 down to 35 after its decrement) the player moves one tile along the stored vector each tick, then the body box is tested at twelve points; if any is blocked the step is undone and the push is tried again the next tick. On open ground the player ends five tiles away after 250 ms. The test uses the same ground rules as an ordinary walk (blocking tiles, and chests).

The twelve points lie on the edges of a box 0.6 to 2.4 tiles across and 1.1 to 2.9 tiles down from (X, Y) (the position properties): three points per edge, the four corners counted twice; see `knockback-probes.tsv`. The box is centred on (X+1.5, Y+2.0). The routine and the table are the same in 2.05 rev 2, 2.17.1, 2.22 and 2.31.

Where the vector comes from:
- sword hit: from the attacker's position to the victim's;
- packet 40: its two bytes (the byte minus 0x60, over 16, tiles);
- packet 46: the victim's centre minus the hit point.

## Gates shared by the sword and the packets
Read in 2.05 rev 2 and 2.22. In this order:
1. the attacker's player id is known;
2. the victim is hurtable (not already hurt, not dead, not swimming);
3. the victim's AP is not 100;
4. the level has not run no-player-killing;
5. the attacker's once-a-second stamp: the second of the day is compared with the one stored for that attacker and stored; the table is shared by the sword and both packets, and the store happens before the guild test;
6. the guild test: the first bracket pair in the attacker's nickname must not occur in the victim's nickname;
7. for the packets, the per-player field test (below);
8. packet 40: the squared distance between the two X/Y positions is at most 100 (ten tiles). Packet 46: the box test below.

The sword path adds the reach box and an attacker status test; the packet path has **no** attacker status test.

Power: packet power is capped at one heart; a power of 0 is accepted (hurt mode and knockback, no hearts taken).

## Packet 46 box
The hit point is (b1/2, b2/2) in tiles, from the two bytes after the power. The player's centre is (X+1.5, Y+2.0). A hit lands when the absolute difference is strictly under 2 on each axis.

## The per-player field of packet 40
Packet 40 is dropped unless a field of the attacker's player record equals the same field of the victim's. In 2.05 and in 2.22 the field is the one that holds a parent or owner record; ordinary players have none, so both sides read zero and the test passes. This is an inference from the other readers of the field; no wire was seen.

## What stays unknown
- Which object kinds (bomb, arrow, baddy) call the hurt routine with which power: the callers use half a heart by default and one heart for a few object kinds, and the kind mapping was not traced.
- Whether the respawn routine's second entry save lands on the death spot online (needs a capture).
- Whether the real client sends CURPOWER after damage (needs a capture).
