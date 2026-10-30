# 02 Weapons and combat

Snapshots read: Graal_analysis `8da6800`, Seihai `06aacfd`, GServer-v2 (local checkout).

## Weapon lists (server to client) **[srv][2.05]**
| PLO | Name | Layout |
|---:|---|---|
| 33 | NPCWEAPONADD | `str name` + NPC prop stream (image, script). A name the player already has is ignored. 2.05 fires `playerenters` on it. |
| 34 | NPCWEAPONDEL | rest = name |
| 43 | DEFAULTWEAPON | `c item index` (0-24, see 03). A built-in weapon: bow, bomb, sword, etc. |
| 197 | (bytecode) | v4+ only; replaces the script for GS2. 2.05 never sees it. |
Client to server: `PLI_WEAPONADD` (33) type 0 = `c item index`; type 1 = `i3 npc id`. 2.05 only sends type 0. `PLI_NPCWEAPONDEL` (29) = name.

GServer builds the list at login (`sendLogin`): clear (`PLO_CLEARWEAPONS`), the account's weapons, protected weapons, then default weapons if the `defaultweapons` option is on. The weapon script text comes from `TWeapon`; for pre-v4 clients the script is sent as plain GS1 text.

## Combat packets **[srv][2.05][cap]**
The client is authoritative. It sends its own action and the server re-emits it to the rest of the level with `s player id` in front. In 2.05 most of these also go over UDP (see 07); the TCP copy is sent only when some player in the level has no UDP port, or an NPC server exists.

| PLI | PLO | Name | Client layout | Notes |
|---:|---:|---|---|---|
| 4 | 11 | BOMBADD | `c x*2, c y*2, c power(+8 = mine), c fuse` | fuse seen: 55 (about 2.75 s) |
| 5 | 12 | BOMBDEL | `c x*2, c y*2` | PLO has no player id |
| 9 | 19 | ARROWADD | `c x*2, c y*2, c flags, c type`, last byte offset 33 | flags: dir&3, +4 effect, +8 owned |
| 10 | 20 | FIRESPY | `c (a*8+b)` | |
| 11 | 21 | THROWCARRIED | empty | |
| 26 | 40 | HURTPLAYER | `s victim, c (dx+4)*16, c (dy+4)*16, c power` [+ `i3 npc`] | receiver: power = (v-32)/2 hearts, cap 1.0 |
| 27 | 36 | EXPLOSION | `c radius, c x*2, c y*2, c power(+8 mine)` | power & 7 clamped 1-3 |
| 36 | 46 | HITOBJECTS | `c power*2, c x*2, c y*2` [+ `i3 npc`] | sword-swing "hit" broadcast |
| 16 | 27 | BADDYHURT | `c id, c dx, c dy, c power` | applied only by the level leader |
| 15 | 2 | BADDYPROPS | `c id` + baddy prop stream | server forwards to everyone except the leader |
| 17 | - | BADDYADD | `c x*2, c y*2, c type, c power` + image | server creates the baddy and answers with props |
| 38 | 48 | TRIGGERACTION | `i3 npc, c x*2, c y*2` + action text | half-tiles in 2.05 |
Server behaviour (`TPlayer.cpp`):
- `msgPLI_HURTPLAYER`: victim lookup; if the victim has the paused status bit, nothing happens; otherwise forwards to the victim with the attacker id.
- `msgPLI_BADDYHURT`: sent only to the level leader (first player in the level's list), who owns baddy AI. `msgPLI_BADDYPROPS` stores the props and forwards to non-leaders. `msgPLI_BADDYADD` caps power at 12 half-hearts and marks it non-respawning.
- `TLevelBaddy::setProps`: mode die starts a 2 s timer to dead; mode dead starts the `baddyrespawntime` timer (60 s lab default) or removes the baddy; with `baddyitems` it drops an item on death.
- Level objects (`TLevel::doTimedEvents`) respawn cut bushes after `respawntime` (15 s) by re-sending BOARDMODIFY.
- `msgPLI_CLAIMPKER` (14): the dead player names the killer; the server adjusts kills/AP (and a rating update in sparring zones).
- `PLO_ISLEADER` (10): "you run this level's baddies". Seihai counts it as unhandled. It matters only if Seihai wants to simulate baddies.
- Spin attack (2.1+ only, `PLPROP_GANI` = `spin`, handled in `TPlayerProps.cpp`): the server itself broadcasts four `HITOBJECTS` packets around the player (4 half-tiles above, below, left, right of the centre) so other clients register the spin. 2.05 has its own sender for HITOBJECTS (36); the exact trigger in a normal swing is not traced.
How 2.05 receives hits is in `protocol/packet-layouts.md` "Hits": HURTPLAYER applies only if the attacker is within 10 tiles and the local player is hurtable; HITOBJECTS only if the player's centre is within 2 tiles of (x, y).

## 2.05 sword swing and hit box **[2.05][dec]**
From the 2.05 rev2 decompile (2026-10-24); details in `../decomp-findings-2026-10-24/04-sword-hitbox.md`.
- **Start of a swing.** Needs weapons allowed by the level or server, sword power not 0, not swimming without a horse, and not already in the charged-spin mode. A normal swing is mode 6. A spin is mode 13: it needs the has-spin flag (STATUS bit 0x40) and starts when S is pressed again while mode 6 is still running. It is not a hold-to-charge; see `../player-mannerisms-live.md`. The client plays the sword, ridesword or spin gani and a sound, then checks for a cuttable bush at the sword tip. The sprite sent to others follows animation steps 9 to 13 (S 6 to 10, see 11).
- **The victim's client decides a hit**; the attacker only broadcasts position, direction and sprite. A hit counts when **all** of these hold:
  - the attacker is on step 9 to 13 (S 6 to 10);
  - the victim is **0 to 4 tiles ahead** of the attacker in the facing direction;
  - the sideways offset is **under 2 tiles**;
  - the victim's **AP is not exactly 100** (such players cannot be hit);
  - the victim is hurtable (not in mode 3, mode 10, dead or editor/pause).
- **Damage** is inferred to be sword power divided by 2 hearts. Not confirmed from a capture; treat it as a Seihai default.
- **Explosions:** a bomb hit needs the victim within 1 tile on both axes of the blast, with knockback of 0.5 or 1.0 tile.
- **After a hit** the victim goes to hurt mode 3 for 40 ticks (cannot be hurt again), and if hearts reach 0 or below the victim client sends `PLI_CLAIMPKER` (14) naming the attacker (see 04).
- Open: how this relates to the `HURTPLAYER` (26) packet in 2.05 (the decompile findings do not say whether the attacker also sends it for a sword hit); frame timing in milliseconds (comes from the gani files, not the client); 1.39 sword and hit box (not read).

## Seihai today
- `SessionState` keeps `weapons` (names and scripts) and `default_weapons`; it does **not** show or select them, send any combat packet, or decode 11/12/19/20/21/36/40/46/48 (they count as unhandled).
- Offline mode has a sword model in the web-Seihai design notes (`formats/seihai-systems.md`). Those numbers are Seihai's own, not 2.05 values.
- No HURTPLAYER handling: Seihai never loses hearts from another player.

## Steps for Claude
1. Parse server packets 11, 12, 19, 20, 21, 36, 40, 46, 48 into events on `SessionState` (list of timed objects: bombs, arrows, hits). Decode per the table. Ignore silently if the level is not the named level.
2. Render bombs and arrows with the existing sprite sheet; remove on BOMBDEL, on explosion or timeout.
3. HURTPLAYER receive: subtract power from `CURPOWER` locally, apply knockback `(v-0x60)/16`, start an invulnerability window, then send the new `PLPROP_CURPOWER` (the server accepts hearts from the client, and refuses to raise them for AP under 40).
3a. Seihai as a **victim** should evaluate sword hits itself with the 2.05 rule above (reach 0 to 4 tiles ahead, lateral under 2, attacker on S 6 to 10, own AP not 100, not already hurt or swimming), and send CLAIMPKER when hearts reach zero.
4. Send side, in this order: BOMBADD (4) with the owner flag, explosion (27) when the fuse ends, BOARDMODIFY (1) for any tile the blast changes, HITOBJECTS (36) when your sword or bomb effect lands (trigger not traced, see NEEDS), HURTPLAYER (26) when your sword box hits another player in the level.
5. Weapons UI: list `weapons` and default weapons; pick with the item key; for GS1 weapons run the script through the existing `scripting` module.
6. Baddies: parse BADDYPROPS (2); only simulate if `ISLEADER` (10) has been received. First pass: draw them from props only.
7. Track an invalid-packet budget: GServer disconnects a client after the 6th unknown id (`msgPLI_NULL`), so never send ids absent from the profile's `pli` set.

## How to test
- Two Seihai or Seihai plus one Wine 2.05 client in the lab level, `bushitems = true`. Drop a bomb next to bushes: expect BOMBADD, then eight BOARDMODIFY runs, ITEMADD drops, then a respawn BOARDMODIFY 15 s later (matches the existing capture in `packet-layouts.md`).
- Replay the existing decoded two-player captures through `SessionState` (examples `lab_replay`) and assert the new event lists.
- GServer rebroadcast can be checked with a second raw client from `examples/session_probe.rs`.

## NEEDS
Nothing for the protocol. The 2.05 hit-box geometry and the frames that can hit are now known (above). Still open, for feel only: when exactly 2.05 sends `HITOBJECTS` (36) in a normal swing, the real damage formula (inferred power / 2), and the 1.39 sword. The server does not check any of it, so any plausible box interoperates.
