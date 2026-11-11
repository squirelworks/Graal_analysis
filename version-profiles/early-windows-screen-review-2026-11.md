# What the early Windows clients show when started: v0, v1 and v2

The research owner started each early Windows client in an isolated Wine lab, offline, and reviewed screenshots and run summaries. This note records what each build showed. It is a look at the screen, not a measurement: there are no frame-rate, timing or movement-distance claims, and none of the runs is authenticated release media. Evidence `EARLY-VISUAL-V0-20261109` and `EARLY-VISUAL-V1V2-20261109`. **[lab][cap]**

Each build was tried with its own data first, and then with assets added where its own were missing. Where a run needed borrowed assets, that is said below.

## v0: 1st Graal to 15th Graal (18 builds)

**[lab][cap]**

- All 18 builds show their start screen. 16 reach an offline scene with an options panel.
- The bedroom, HUD and player are visible in 1st, 2nd, 3rd, 4th, 7th, 8th and 10th to 15th Graal. 5th Graal alpha and 6th Graal draw the outdoor scene.
- After the Right-arrow trial the player's placement changes. In 14th and 15th Graal the player goes from lying in bed to standing.
- 4th Graal alpha and 5th Graal draw only part of the scene, with black areas and wrong strips of tiles.
- 9th Graal stays at the start screen; the Start request timed out. 9th Graal alpha stops on a "heads.gif cannot be opened" message.
- Only 12 run summaries record a successful Start, while the screenshots show 16 scenes. The screenshots are the better count of what was drawn; the summaries undercount.

Limits: 5th Graal alpha used a world borrowed from 5th Graal. 3rd Graal and 4th Graal alpha had sound files filled in from their own packages. The S, A and D key trials do not isolate one mechanic each.

## v1: 1.19 to 1.41 (18 builds)

**[lab][cap]**

- 17 of 18 builds show an offline scene, and the placement changes after the Right-arrow trial. Earlier builds start in a bedroom; 1.32 and later start in the welcome cave with named NPCs. 1.19 stays at the start screen.
- 1.21, 1.25 and 1.27 were put together from their own installers.

## v2: 2.00 to 2.22 (23 builds)

**[lab][cap]**

- 2.04 and the three 2.05 revisions draw the tutorial terrain, the HUD, the parchment and the options.
- NewWorld beta 1 draws an interior with NPCs.
- 2.00, 2.01 rev 1 and 2.03 stop on a "missing objects.dat" message. That matches the data-file caveat in [client-internals/decomp-findings-2026-10-24-b/04-v2.00-client.md](../client-internals/decomp-findings-2026-10-24-b/04-v2.00-client.md).
- 2.02 and its two revisions show an all-black window.
- One 2.22 image shows an "execution file corrupted" warning. The modified 2.22 reaches the authored truth-test scene; the stock 2.22 still warns.
- The editor retries for NewWorld betas 1 and 2 show only a blank canvas.
- Retries with legacy assets borrowed from 1.41 rev 1 reach the tutorial. That does not make the first runs successful.

Limits: the parchment changes by itself, so movement is not isolated in v2.

## How to use this

These rows say which builds reach a scene in this lab and which need help, so a later test can pick a build that draws. They do not establish timing, input handling or gameplay, and they do not replace the per-build notes. Scene and mechanic validation stays open in App. E#610.
