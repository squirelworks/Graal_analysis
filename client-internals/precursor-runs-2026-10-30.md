# Precursor runs and behaviour constants (2026-10-30)

This note follows `precursors-and-fan-builds.md`. That note was a static read. This time the Java precursors and the Game Boy Color demo were **run** in a sandbox, and the game-feel numbers were read out of the Zelda Online 2 and Java Graal sources.
The aim is to give Seihai's per-version profiles exact numbers for the oldest builds: tick rate, walking, pushing against walls, lifting, bush drops, respawn, and how chat is drawn.

Tags: **[src]** read from the Java source, **[live]** seen in a running client or on the wire.
No code is quoted. Screenshots are in the project's shared folder under `graal-decompile/precursors/runs-2026-10-30/`, not in this repo.

## How it was run

- **Zelda Online 2.** The bundled GServ Standalone server ran on port 14801, with two copies of the applet in an applet harness under Xvfb. Both clients joined, saw each other, walked, cut bushes, pushed against walls and chatted. The traffic was captured with tcpdump. **[live]**
- **Java Graal (July 2000).** Two copies of the applet ran in the same harness. The applet only connects to its own codebase host on 14802, so a plain TCP forwarder from 14802 to the GServ server on 14801 stood in for the old relay. Both players saw each other. **[live]**
- **Game Boy Color demo.** Run in PyBoy with scripted input. **[live]**

## Behaviour constants (Zelda Online 2 and Java Graal)

Every number below is the same in both games. The Java Graal applet is the Zelda Online 2 engine, re-skinned with Graal art and given new levels.

| What | Value | Tag |
|---|---|---|
| Main loop | 50 ms per tick (20 Hz) | [src] |
| Walk step | half a tile per tick while a key is held | [src] |
| Corner slide (walking into the edge of a block) | a quarter of the walk step, sideways around the corner | [src] |
| Sword | 5 ticks; hits are tested on ticks 1 to 3 only | [src] |
| Being hurt | 40 ticks of hurt state, half a heart of damage | [src] |
| Shield bump | 4 ticks | [src] |
| Lifting | 5 ticks | [src] |
| Baddy moves | sent by the level leader every 2 ticks (100 ms) | [src] |

### Walking into a wall

The player keeps a push counter that counts ticks spent walking into something solid. **[src]**, and the pose was seen in the running client. **[live]**

- **Ticks 0 to 17 (0.9 s):** nothing visible. The player stands in the walk pose against the wall.
- **Tick 18:** the push pose starts. The push frames advance one step every 4 ticks. The ledge-jump check also runs from tick 18, so a jump down a ledge needs 0.9 s of pushing.
- **Tick 28 (1.4 s):** a push stone in front of the player moves.
- **Tick 38:** the counter goes back to 18, so the push animation loops without restarting the 0.9 s wait.
- Letting go of the key, or turning, resets the counter to 0.

Compare `ledges-push-pull.md` for the Delphi clients.

### Bushes, stones and pots

- **Cutting a bush** rolls one number from 0 to 99. **[src]**
  - 0 to 24: one green rupee (25%).
  - 25 to 29: a heart (5%), worth one heart of power.
  - 30 and 31: a five-rupee item (2%).
  - 32 to 99: nothing (68%).
- **Lifting.** There are four liftable object kinds. Kinds 0 to 2 can always be lifted. Kind 3 (the heavy stone) needs the stronger glove. A lifted bush (kind 0) rolls the same drop as a cut one. Kind 2 always leaves a heart. **[src]**
- **While carrying**, the player is drawn with a separate set of four carry sprites, one per direction, with the object drawn above the head. The player is not hidden under the object in these games. Hiding under a carried bush came later; see `carry-hide-and-glove.md`. **[src]**
- **Respawn: there is no timer.** Cut bushes, lifted stones and broken pots stay gone only for the visit. Every board change is cleared when a level loads, so everything is back when the player leaves and comes back. Nothing grows back while the player stays on the level. **[src]** Re-entry was not tested live.
- **Sharing board changes.** Each change is relayed as a `B` line. The level leader (earliest login time) sends all of the current changes to every newcomer, so a player who joins sees the bushes already cut. **[src]** The captured sessions had no board changes on the wire, because nothing was cut while both clients were in the same room. **[live]**

### Chat

**There is no chat bubble.** **[src]**, **[live]**

- Chat text is drawn in TimesRoman bold, 20 points, in black, over a white copy of the same text shifted one pixel right and one pixel down. The result reads as black text with a thin white edge.
- The text is centred on the player (the player's x plus 12 pixels, times the zoom), just above the head.
- The nickname is drawn in the same style three tiles lower, under the feet.
- There is no box, no background and no tail. The bubble seen in later Graal belongs to the Delphi clients, not to these.

## What the wire showed

- **Room names.** Zelda Online 2 joined as `NZlevel11.6#def`, and Java Graal joined as `NG2level13.graal#def`. These match what the sources say. **[live]**
- **Join order.** The server answers `I<id8>`, then sends `+<id8><name>` for each available player. The client answers the first `+` with `P<id8>` and then pushes its whole state: login time, position, chat, nickname, colours and carried object. **[live]**
- **Doubled relay.** When two clients see each other at the same moment, they both send `P` for the other. GServ then links the pair twice, and every `D` line after that is delivered twice. One capture had 1144 relayed lines for 572 sent. Nothing visibly broke, because most `D` lines are state updates such as position (550 of 578 sent lines in the Zelda Online 2 capture were `M` moves). A doubled one-off event, such as a board change, would simply be applied twice. It happened with both Zelda Online 2 and Java Graal. A server that emulates GServ for these clients does not need to reproduce it. **[live]**

## Game Boy Color demo in an emulator

This adds a run to the static read in `gameboy-demo.md`. Everything it says about the screens held up. **[live]**

- There is no title screen. The ROM goes straight from the Nintendo logo to room 0, the outdoor start with palm trees, bushes and flowers.
- **Select** opens the character carousel in the window. It shows three heads with the middle one's name in the font, and the item slots labelled "Button B" and "Button A" under it. Turning it left and right went through Vincent, Fung Si Yun, Pach Soldier, Ninji, Lunar and Squall in that order, and each step changed the player's look straight away. This confirms the static finding that the carousel is a free picker over all character types.
- The item icons under the slots change with the character. For example Fung Si Yun shows a green item in slot A, and Pach Soldier shows a blue sword in slot B.
- Walking around room 0 and the next rooms showed the NPCs and log walls where the room table in `gameboy-demo.md` puts them.
- Start (music) was not checked by ear here. A later, longer run (see "Seen in an emulator" in `gameboy-demo.md`) found that Start mutes the game.

## What this means for Seihai profiles

For a "Zelda Online 2" or "Java Graal" profile:

- Run game logic at 20 Hz and move half a tile per tick.
- Show the push pose after 0.9 s against a wall, and move push stones at 1.4 s.
- Use the bush drop table above.
- Never regrow anything during a visit, and restore everything on level load.
- Draw chat as bold serif black text with a white one-pixel offset and no bubble.
- Do not hide the player under a carried object.

For the Delphi Graal builds these numbers are a starting point only. Their wall push, hiding and respawn timers have their own notes and are not covered here.

## Open

- Whether the 1st to 4th Delphi betas still used the 0.9 s / 1.4 s push timings. The Delphi code has not been compared yet.
- The GB demo's music format, which depends on cartridge RAM that the ROM never writes. In the emulator, Start only muted the game (see `gameboy-demo.md`).
