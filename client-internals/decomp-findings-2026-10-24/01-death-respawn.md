# 2.05 rev2: death and respawn (derived)

Source: static analysis of the 2.05 rev2 client, 2026-10-24. Behaviour only; no code is reproduced.
Tick is 50 ms. See `player-modes.tsv`, `life-states.tsv` and `constants-205.tsv`.

## Trigger
- Any change that leaves hearts at 0 or below starts the death sequence once.
- A per-frame safety net also forces the dead life-state whenever hearts are 0 or below.

## Sequence on the dying client
1. A death timer starts at 0 and counts up each tick. It stops at 30 (1.5 s).
2. Life-state becomes "dead", mode goes back to 0 (normal) and the player faces down.
3. The "dead" gani plays for the local player and the script event `playerdies` fires.
4. Controls are ignored until the timer passes 27 (1.35 s).
5. Status prop (18) gets the dead bit (0x08) only when life-state is dead and the timer is at least 28. So other players see the player as dead only after about 1.4 s.
6. No sprite for "dead" goes on the wire. The sprite prop shows plain idle plus direction. The dead state is carried by the status bit only.

## Respawn
- After the timer passes 27, any movement or action key triggers the respawn. There is no dedicated respawn packet and no server permission step on this path.
- **Hearts after respawn** (AP = alignment points):

| AP | Hearts |
|---|---|
| below 20 | 3 |
| 20 to 39 | min(5, max hearts) |
| 40 or more | max hearts |

- **Destination** is the last saved level-entry point (level, x, y, direction). It is updated on every level entry, unless the old and new levels share the same name group (see the gap list), and also at login.
  - If nothing was saved and the client is online: x 30.5, y 30.0, facing down, in the current level.
  - Offline: the default start level `tutorial_b-4.graal`.
  - When the online flag is set, the client re-sends the current level at the current x/y, so the server sees an ordinary level warp (the PLI_LEVELWARP route) rather than a "died" message.
- After respawn the status bit 0x08 clears when life-state returns to playing.

## Damage rules that feed this
- Healing only happens at AP 40 or above.
- No damage in swim mode (10) or in the editor/pause state unless forced.
- Hurt state: mode 3 for 40 ticks, "hurt" gani, knockback, script event `playerhurt`. A player already in mode 3, mode 10 or dead cannot be hurt.
- The victim's client decides hits (see `04-sword-hitbox.md`). When hearts reach 0 or below after a sword hit, an explosion hit or a UDP hurt, the victim client sends PLI_CLAIMPKER (14) carrying the attacker's player id.

## Anti-cheat note
Hearts, AP and max-power sit in an attribute array that the client stores obfuscated twice and cross-checks. A mismatch raises "memory problems error 1/2". Editing hearts from outside the client is therefore detected by the client itself.

## Gaps
- The exact "same name group" rule for not updating the saved entry point was only partly traced.
- The server-side reaction to CLAIMPKER is not in the client binary.
