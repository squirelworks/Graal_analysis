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

## Other players' bombs, blasts and shots

How the 2.05 client takes the server's copies of another player's bomb (`PLO_BOMBADD`, 11), explosion (`PLO_EXPLOSION`, 36) and shot (`PLO_ARROWADD`, 19), and when the result hurts the local player. Read from the 2.05 rev 2 program. The bytes follow the sender's player id; every value below is `byte - 32` unless it says otherwise.

### Bomb (11)

- Needs at least 4 bytes: `x×2`, `y×2`, power, fuse.
- Power is `v & 7`; bit 8 marks the bomb as the sender's. The fuse is the byte itself, in ticks.
- The bomb goes through the same routine as a local `putbomb`, so water under `(x + 1, y + 1)` makes a splash and no bomb. Nothing is sent back.
- It is put in the sender's level (the local player's level when the sender is unknown).
- It burns and goes off exactly like a local bomb (60-tick fuse for a local `putbomb`, the sender's copy 5 ticks shorter), with the sender as the owner of every piece.

### Explosion (36)

- Needs at least 4 bytes: reach, `x×2`, `y×2`, power.
- Power is `v & 7`, 0 read as 1 and anything above 3 read as 3; bit 8 marks the explosion as the sender's.
- It makes one cross of that reach (at most 15) and that type at `(x, y)`. The five-cross split of the super bomb belongs to a bomb's bang only, not to this packet.
- It plays one of two sounds, chosen by whether the power is 3. The two names are not visible in this routine; that they are `thunder.wav` and `bomb.wav`, as for a bomb, is an inference.

### Shot (19)

- Needs at least 5 bytes: `x×2`, `y×2`, flags, sprite, type. The type byte is `byte - 33`.
- Flags: `& 3` is the direction, 4 first removes a shot this client already has, 8 marks the shot as the sender's.
- The byte before the type is the sprite id, not the type. Arrows use sprites 107 to 110 (107 + direction).
- The shot flies 1 tile per tick along its direction.
- With flag 4, the client first deletes every shot it holds that flies the opposite way with the same sprite (any arrow sprite matches any other), on the same line. That this is the copy of a shot a shield sent back is an inference.
- In a level that has run `noplayerkilling`, the receiver marks the shot as a player's shot, and such a shot never hits the local player.

### When a piece hurts the local player

Each tick of its 11-tick life, a piece hurts when all of these hold:

1. the piece is in the player's level;
2. the player can be hurt (see the sword notes);
3. the centre test of "Bombs and explosions" above passes.

Then the ownership test: the piece counts as a player's when the client is online, the piece has an owner, and that owner is still in the client's player list. A player's piece in a `noplayerkilling` level does not hurt. A piece whose owner has left counts as nobody's, and it hurts.

A hit takes half a heart, or a whole heart for a piece of type 3, and knocks the player along the piece's arm. When a player's piece leaves the player at 0 hearts or fewer, the client reports the owner as the killer.

### When a shot hurts the local player

Each tick the shot moves first, then:

- **Level edge.** Past -2 or at 64 and beyond in its direction, it moves to the neighbouring level of the loaded gmap block, or it is gone.
- **Hit test.** It is skipped while the shot is bouncing back, when it is a player's shot (the local player's own, or one received in a `noplayerkilling` level), or when the player cannot be hurt.
  - The shot's size comes from the sprite table entry `v` (array 24): width `((v >> 6) & 63) / 16` and height `(v & 63) / 16` tiles.
  - It hits when `x + w > px + 0.5`, `x < px + 2.5`, `y + h > py + 1` and `y < py + 3`, where `(px, py)` is the player's position.
- **Shield.** Before hurting, a shield can stop the shot. This needs all of:
  - the player faces the shot;
  - the player's shield power is above 0;
  - the shot is of type 0 or 1;
  - the player's animation is one of two names from the built-in animation list. That these are `idle` and `walk` is an inference.

  The result depends on the shield power:
  - Power 1: an arrow sprite turns back for 3 ticks with a sound. Any other sprite is gone.
  - Power 2 or more: the shot is sent back the other way, with its sprite turned, and the client sends it again as a new shot.
- **Hurt.** Otherwise the shot hurts. It uses the same ownership and `noplayerkilling` test as a piece, and the same killer report. It takes half a heart, or a whole heart for type 1 or 3. The knockback the shot passes is not visible in this decompile.
- **After a hit.** The shot is gone. A shot of type 2 or 3 leaves a blast of reach 2 and type 1, owned by the shooter, at the hit.

### Open

- **Walls.** In the decompiled flow, types 0 and 1 skip the blocking test that stops types 2 and 3, so arrows and fireballs would fly through walls. The blocking test lost its arguments in the decompile, so this is not settled. Check it in the lab.
- **Baddies.** The baddy touch above was not re-read here.
- **The two shield animation names.** See "Shield" above.

## Confirmed, inferred, not tested

- Confirmed from the program: the powers in the table, the bomb split, the blast shape, the projectile types, the hit boxes and the ownership rule.
- Inferred:
  - that bomb powers 1 to 3 are the bomb, super bomb and jolt bomb (from the built-in weapon scripts);
  - that the noplayerkilling check is the level flag the sword gate uses.
- Also confirmed from the program: the receive side of ids 11, 36 and 19, the owner and `noplayerkilling` test, the killer report, and the shot's hit box. The inferences there are marked in place.
- Not tested in the lab or on a wire.
