# Ranged baddy kills on 1.21 and 2.17.1, and sword against sword on 2.22 (2026-11-20)

Lab run for #652 (the 1.21 drop or reward, the 2.17.1 drop check, the sword spark) and
App. E#324. Every run was offline (1.21, 2.17.1) or on a loopback GServer-v2 lab world (2.22),
in the Debian lab VM, under Wine + Xvfb, inside a private network namespace with no route out.
Raw screenshots and logs are kept privately; this page has the derived results. **[lab]**

## Setup

| Item | Value |
| --- | --- |
| Clients | 1.21 (One Player, start level replaced), 2.17.1 Training (`Graal_2171.exe`, Wine virtual desktop, level loaded with F5), 2.22 (`GNW03014`) twice for the sword scene |
| Kill method | No player weapon. An NPC in the level calls `putexplosion 1,x,y` on the centre of each baddy every 1.5 s, starting 12 s after entry |
| Level | The 2026-11-19 rock corridor board, plus four archers (type 3), each shut in a ring of rocks at (14,16), (44,16), (14,32) and (44,32). The player stands in the corridor at about x 30, 14 to 16 tiles from every archer, and never moves |
| Evidence | Screenshots every 0.3 to 0.4 s from entry, about 30 s per run; the gralat, dart and bomb counters on the HUD (1.21) |

Because the player is far from every archer and does not move, a gralat that reaches the
counter can only be a direct kill reward, and anything drawn at the archer's spot is a drop.
The rock ring stops the archers' arrows and stops them walking, and the explosion does not
need a line to the archer.

## 1. 1.21: the archer drops an item; the counter does not change

Two runs, four archers each; two archers per run are in view.

| Run | What was drawn where each archer died | Gralats on the HUD |
| --- | --- | --- |
| 1 (first shot about 10 s in, archers already dead) | a heart at one spot, a dart bundle at the other | 0 before and after |
| 2 (shots from entry) | archers alive for 8 frames; after the explosions, a **green gralat** drawn at each spot | 0 before and after |

- 1.21 rolls a real ground drop when an archer dies, and the drop can be a heart, darts or a
  green gralat, as the 0–99 roll in the static read says.
- No kill gave a gralat to the counter. So the "+1 gralat in the frame of death" seen in the
  12 sword kills of 2026-11-19 was a dropped green gralat landing on the player and being
  picked up at once, not a direct kill reward.
- The drawn items were gone about 1 to 5 s later (the next explosions hit the same spots, so
  their normal lifetime was not measured here).

## 2. 2.17.1: no drop

One run, all four archers in view (2.17.1 shows the whole lab area).

- Each archer took two explosions: the first put it into its hurt pose, the second killed it.
  All four died within about 1 s of each other.
- Nothing was drawn at any of the four spots in the 20 s after the deaths: **0 drops in 4
  kills**.

With the 2.05 rev 2 result (0 drops in 25 sword kills) this fits "no client-side drop roll from
2.0". The 2.17.1 Training player has no visible gralat counter, so a direct reward could not be
read on this build.

## 3. 2.22: sword against sword, still not caught

Two real 2.22 clients on the lab world were placed face to face, 2 and then 3.5 tiles apart, and
both swung at the same moment, 6 times per run, with screenshots of both views about every 60 ms
during the swing.

- The swing arcs and the hurt knockback show, and both clients took hits, so the swords did
  reach. No separate small spark sprite could be told apart from the two swing arcs in any frame.
- The lab level's gray soldier walked into several of the frames, so this is not a clean
  sword-on-sword scene either. The sword spark stays open.

## Still open after this run

- The sword spark (array 21, 5 ticks): it needs a cleaner sword-against-sword or sword-against-
  shield scene, with frame-exact capture (the client's own frame, not a screenshot every 60 ms).
- The 2.17.1 direct-reward question, on a 2.17.1 mode that shows the gralat counter.
