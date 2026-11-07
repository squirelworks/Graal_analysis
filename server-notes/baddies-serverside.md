# Recreating the 2.22 baddies in serverside scripts

Date: 2026-11-04

How to make a serverside NPC behave like a 2.22 built-in baddy, with the rules in `client-internals/baddies-222.md` and a worked gray soldier in `baddies/graysoldier-222.gs1`. Written for the built-in NPC-server of the seihai-gserver-v2 fork; the approach carries over to any server that runs GS1 serverside.

Tags as in the spec: **[2.22]** · **[cap]** · **[srv]** · **[inf]**.

## Two ways to do it

| | Real baddies (`putcomp`, level baddies) | A serverside NPC that acts as a baddy |
| --- | --- | --- |
| Who runs the AI | the level's leader client [2.22] | the server script |
| Who decides a hit | each client, for the swings it sees; the leader applies them [2.22][cap] | the server script |
| Works with nobody in the level | no, nothing moves until a leader is there | yes, if the server keeps running the level's NPCs |
| Cheating | the leader can move, heal or kill baddies at will | only what the script allows |
| Needs on the client | nothing extra: the client draws them with its own code | ganis that draw the baddy (made from `arrays.dat` by `tools/baddy-222/gen_ganis.py`) |
| Fidelity | exact, it is the client's code | as close as the script; see "What differs" |

If the goal is simply to have the classic baddies, the first column already works with any 2.22 client. The rest of this note is about the second column: moving the logic onto the server.

## The step

The client runs one AI step every 100 ms [2.22]. A serverside script does the same with `timeout = 0.1`. All counts in the spec are in these steps, so they carry over unchanged: 44 steps of looking about, a 16-step pause before the chase, 8 steps of knockback, 14 steps of dying, 20 steps for a verse.

## Mapping the client's state to a script

| Client | Script |
| --- | --- |
| x, y (2 × 2 body, top-left) | the NPC's `x`, `y`; the baddy's centre is `x + 1, y + 1` |
| mode, counter `c`, `lost`, power, knock vector, verse flags | `this.` variables |
| body direction | `this.dir`, and the NPC's `dir` so that the gani faces the right way |
| head direction | `this.head`; drawn by choosing between the `look1` / `look3` ganis |
| ani | which gani is set (`setcharani`) |
| the 2 × 2 blocking test | `onwall` at the same probe points |
| the player list (target, touch, sword) | `players[i]`, `playerscount` |
| touch damage | `hitplayer i, power, x + 1, y + 1` |
| verses | `message` for 20 steps |
| mode 9 and the server's respawn timer | `timeout = this.respawn`, then reset |
| `baddyitems` drops | `lay` with the same odds |

The ganis come from `tools/baddy-222/gen_ganis.py`: run it on your own `arrays.dat` with the baddy's image and copy the `.gani` files to the server. Nothing from `arrays.dat` is stored in this repository.

## The worked script: gray soldier (type 0)

`baddies/graysoldier-222.gs1`. Each step, in this order:

1. **Respawn.** When `this.respawning` is set: back to the start position, power 2, mode 0, facing down, counter `Random(20) + 40`, all verses fresh.
2. **Dead (mode 9).** Wait `this.respawn` seconds (60, GServer-v2's `baddyrespawntime` default), then respawn.
3. **Sword.** For every player whose gani is `sword`, the 2.22 shield-block box, then the hit box. A hit takes the player's sword power and starts mode 3 with knock length 2.0; a block starts mode 4 with 0.8. Counter 8, knock vector `−(P − B) × 2` scaled to the length.
4. **Target.** The nearest player by the larger of the two distances; after the first, only players in sight count.
5. **Mode 0 / 1.** Walk and look about exactly as the client does, then the sight check with the head's direction; seeing the target starts the hunt with counter 16 and the sight verse.
6. **Mode 2.** The 1 s pause, then the melee hunt: the 0, 3, 2, 1 cycle, `lost` up to 40, the main and side axis, the 0.5 probe ahead and the 0.1 probe outside, the three ways of moving, and the unstick.
7. **Modes 3 / 4.** Six steps of knockback (undone against walls), then dying or back to the hunt with counter 12 and the hurt verse once.
8. **Mode 5.** 15 steps of dying, then mode 9 and the drop.
9. **Touch.** Any player whose centre is within 1 tile of the baddy's centre takes half a heart. The client's 2 s hurt lock-out spaces the hits out as it does with a real baddy.
10. **Verses and gani.** The verse shows for 20 steps; the gani changes only when the state does, so the clients get one prop per change.

The other types change only a few values and one or two blocks:

| Type | Change |
| --- | --- |
| 1, 2, 7 | power 3, 4, 6; their own image; type 7 touches for a whole heart |
| 3, 9 | no shield; replace the melee step with the archer step (walk to the spot 11 tiles in line, `shoot` or `shootarrow` with a 15-step cool-down); ganis with the bow (`aim`) |
| 4 | no movement: the 43-step swamp cycle, hit only while out of the water (`21 < c < 37`), no knockback |
| 5 | the 46-step jump cycle, hit only while `16 < c < 38`, one hit kills |
| 6 | walk at 0.5, no sight check, the ink stop (mode 8) when the walk counter runs out, no hunt |
| 8 | power 12, walk 0.5, hunt 0.75, no shield |

## What differs from the client

- **Blocking.** In the fork, `onwall` tests wall tiles and blocking NPCs, and players unless the NPC ran `noplayeronwall`. The script runs `noplayeronwall`, so that the target's own body cannot break the line of sight, and `dontblock`, so that `onwall` does not find the baddy itself. The client also stops a baddy at water, chairs and bed bottoms (tile types 11, 3 and 5) and at other players; add tile-type tests if the levels need them [inf].
- **Square root.** The script uses `^ 0.5` to scale the knock vector.
- **The shield push.** In 2.22 a shield block also pushes the player back. The script leaves the player alone, because a serverside script cannot set another player's pushed state the way the client does; a `hitplayer` with power 0 from the baddy's centre is the closest stand-in [inf].
- **Hit timing.** The client tests the sword every 50 ms tick; the script every 100 ms step. A sword swing lasts several steps, so this only shifts a hit by up to 50 ms.
- **Players' positions.** The server knows a player's position only from its props, so the script sees players a little later than a leader client sees its own player.
- **Hiding.** The fork's NPC-server has a hide/show bug, so the script never hides the NPC; a dead baddy shows the empty `gone` gani instead.
- **Arrows and bombs.** The worked script handles the sword only. Hits from arrows, bombs and thrown objects need the server's `wa*hit` events (or a weapon script that calls `hitcompu`-style code) with the spec's hit box `Bx ± 1, By − 2 to By + 1`.

## Status

- `baddies/graysoldier-222.gs1` passes `tools/gs1-lint/gs1lint.py` apart from one expected error: `noplayeronwall` is a serverside command that the 2.05 client table does not have. It has not been run on a live server yet: building the fork needs a newer compiler than the lab image had, and its GS1 grammar embeds C++ code, so it could not be parsed with a Python ANTLR runtime either.
- The fork's serverside `players[i]` members (`x`, `y`, `dir`, `hearts`, `swordpower`), `#m(i)` for a player's gani, and `hitplayer` are used as the fork's command list documents them; they should be the first thing checked on a live run.
