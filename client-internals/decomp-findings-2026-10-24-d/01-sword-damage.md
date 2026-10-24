# Sword damage (victim's client)

Builds read: 2.05 rev 2, 2.17.1, 2.22, 2.31. The rule is the same in all four.

## Who computes it
The victim's client. The attacker's swing reaches others only as props (position, direction, sprite); the hit's size comes from the attacker's SWORDPOWER prop as the victim last received it.

## The sword-power byte (prop 8)
- Sender: the power is limited to -20..20. Power 0 sends byte 0 (no image). A power of 1..4 with the matching default image (sword1..sword4) sends the power itself, 1..4. Anything else sends power + 30 (10..50) followed by the image name.
- Receiver: bytes below 10 are the power; from 10 the power is the byte minus 30.
- The victim stores the power for each other player (a signed value) and uses it when a swing is judged.

## The formula
Half hearts taken = the attacker's sword power, limited to -20..20. In hearts: power / 2. So a power-3 sword takes 1.5 hearts.

Not read: the victim's shield power, item levels, the attacker's AP, the hurt-power field of the hurt packet (that packet carries its own power; see below).

## What happens to the hearts
The shared hurt routine takes a power in hearts and a knockback vector. It asks the heart-change routine for minus the power, then puts the player into hurt mode (mode 3, 40 ticks of 50 ms).
- The heart-change routine ignores a positive change (heal) when the player's AP is below 40. So a negative sword power heals only at AP 40 or more, and hearts stop at the maximum.
- It is also where the swim, editor/pause and death checks live: hearts reaching 0 start the death.
- Hurt mode starts regardless of the sign or size of the power, including 0 and a heal that was ignored.

## The hurt packet (id 40) and its power
`PLO_HURTPLAYER` carries the attacker, a knockback and a power byte (half hearts). The client limits the power to one heart (2 half hearts) before calling the same hurt routine; the attacker must be within 10 tiles. The 2.05 to 2.31 handlers differ only in small decode churn (the earlier batch c tables).
The client's own id 26 send is the mirror image; its power is the attacker's choice, limited the same way.

## Open
See 03.
