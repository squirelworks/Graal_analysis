# Damage from bombs, arrows, thrown objects and baddies (2.05)

How many hearts each non-sword source takes from the local player, and when it hits. Read from the 2.05 program. The sword rule is in `decomp-findings-2026-10-24-d/01-sword-damage.md`.

Each source below calls the same hurt routine with a power in hearts and a knockback direction. That routine takes the hearts off, starts hurt mode (40 ticks), and runs `playerhurt`. It does nothing while the player cannot be hurt: already in hurt mode, dead, swimming, or in the editor or paused, as in the sword notes. So overlapping pieces of one blast take hearts only once.

## Powers

| source | hearts taken |
|---|---|
| explosion piece of type 1 (`putbomb 1`, `putexplosion`, the blast of a fireblast or nukeshot) | 0.5 |
| explosion piece of type 2 (`putbomb 2`, the super bomb) | 0.5 |
| explosion piece of type 3 (`putbomb 3`, the jolt bomb) | 1 |
| arrow (`shootarrow`) | 0.5 |
| fireball (`shootfireball`) | 1 |
| fireblast (`shootfireblast`) | 0.5, then a blast |
| nuke (`shootnuke`) | 1, then a blast |
| thrown object (`waspelt`) | 1, or 0.5 when the player has exactly 1 heart left |
| baddy touching the player | 0.5, or 1 for the golden warrior (type 7) |

## Bombs and explosions

- `putbomb power,x,y` makes a bomb with that power. Powers 1 to 3 are the bomb, super bomb and jolt bomb of the built-in weapons.
- When it goes off:
  - Power 3 plays `thunder.wav`, and any other power plays `bomb.wav`.
  - Power 2 makes five blasts: four of reach 2 at the four diagonal corners, 2 tiles out, and one of reach 4 in the middle. All five are type 2.
  - Any other power makes one blast of reach 2, with the bomb's power as its type.
- A blast of reach `n` (at most 15) is a cross: a centre piece, then `n` pieces in each of the four directions. The last piece of each arm uses the end picture.
- `putexplosion radius,x,y` makes one blast of type 1 with the given reach.
- A piece hurts the player when its centre, offset by one tile, is less than one tile from the player's centre (x + 1.5, y + 2) on both axes. The knockback is the piece's direction.

## Projectiles

- The four shoot commands make a flying object of type 0 (arrow), 1 (fireball), 2 (fireblast) or 3 (nuke), at speed 1, and play `arrow.wav`.
- Types 1 and 3 take 1 heart and the others take 0.5.
- After hitting, types 2 and 3 make a blast of reach 2 and type 1 at the hit.

## Thrown objects

- A thrown object hurts the player when it lands within 2 tiles of the player's point (x + 0.5, y + 1) on both axes.
- It takes 1 heart, except when the player has exactly 1 heart left, when it takes half a heart.

## Baddies

- A baddy that touches the player takes half a heart. The golden warrior takes 1.
- Touching means the player's centre is within one tile of the baddy's point on both axes.
- On a hit, the baddy may say its "when it hurts the player" verse.

## Who can hurt whom

- A bomb, blast, arrow or thrown object can belong to another player. If it does, and the level has run `noplayerkilling`, it does not hurt.
- A source that belongs to no player, such as a baddy's or the level's own, always hurts.
- When a player-owned source leaves the player at 0 hearts or fewer, the client reports the owner as the killer.

## Confirmed, inferred, not tested

- Confirmed from the program: the powers in the table, the bomb split, the blast shape, the projectile types, the hit boxes and the ownership rule.
- Inferred:
  - that bomb powers 1 to 3 are the bomb, super bomb and jolt bomb (from the built-in weapon scripts);
  - that the noplayerkilling check is the level flag the sword gate uses.
- Not tested in the lab or on a wire.
