# 5.x and 6.x clients: expiry dates, the clock check, and the black screen

Date: 2026-11-13. Question: real 5.24r4 (Windows, under Wine) and Linux 6.03r7 drew a black screen against the lab server. Are these builds time-bombed, and if not, why do they draw black?

Short answer: **5.24r4 and 6.03r7 are not time-bombed.** The black screen had two server-side causes. The lab world held no client art, and the lab login server warped the client away before `pics1.png` had finished downloading. With both fixed, both clients drew the whole level on the real date, with no fake clock and no renderer change.

Tags: **[bin]** read from the client's memory dump (`v5v6-windows-unpacked.md`); **[lab]** seen in a lab run (loopback only, a Debian VM, Wine for the Windows build); **[inf]** inferred.

## Which builds expire

| Build | Wrapper | Expiry | What happens on today's date |
|---|---|---|---|
| 5.12 | MoleBox | none found | runs |
| 5.24r3, 5.24r4 | MoleBox | **none** **[bin][lab]** | runs; 5.24r4 started and played on the real date **[lab]** |
| 6.00 beta1, beta2 | MoleBox | none found **[bin]** | – |
| 5.30r3, 5.31r4, 6.00r2, 6.00r4 | Themida/WinLicense | **yes** | logs "This is a beta release of Graal. If it's not working on your computer then please download a new version…" and exits within about 1 s, before any window opens (`v5v6-windows-unpacked.md`, `v5v6-lab-play.md`) |
| 6.03r7 (Windows) | Themida/WinLicense | none **[bin]** | – |
| 6.03r7 (Linux) | none | none **[lab]** | runs |

### How the expiry works (5.30r3 to 6.00r4)

- The "beta release" text is in all four dumps, but only in memory that was not part of the program image (a heap or stack region captured with the dump). It is not in the image's own data, and no code in the dumped image points at it. So the text is built at run time and the check runs inside the Themida/WinLicense layer, not in the game's own readable code. **[bin]**
- This fits WinLicense's own expiration-date feature, or a check wrapped in its virtual-machine macros. Which of the two it is was not read. **[inf]**
- The clock has to stay set back for the **whole** session (`v5v6-lab-play.md`): when the clock jumps forward after start, the client disconnects with "You have been disconnected due to inactivity", and on 6.00r2/r4 the check seems to run again after login. **[lab][inf]**
- The result of expiry is an **exit**, not a black screen.
- The cutoff dates were found by a day-level clock binary search (one fresh launch per probed day at 12:00). A day **passes** when the client dials the login host within about 30 s; a day **fails** when it prints only its start / beta banner, opens no connection, and exits. Boundaries were double-checked. **[lab]** ([5.30r3 / 5.31r4](../protocol/lab-appe-hostb-2026-11-20.md#expiry-dates-of-530r3-and-531r4-e14); [6.00r2 / 6.00r4](../protocol/lab-appe-hostb-2026-11-20c.md#expiry-dates-of-600r2-and-600r4-e14))

| Build | Last day it runs | First day it stops | Notes |
|---|---|---|---|
| 5.30r3 | 2010-12-31 | 2011-01-01 | Round year-end; no game-side expiry text in the image **[lab]** |
| 5.31r4 | 2011-03-20 | 2011-03-21 | About 75 days after its link date (2011-01-05) **[lab]** |
| 6.00r2 | 2011-08-26 | 2011-08-27 | 75 days after the archive exe date (2011-06-13) **[lab]** |
| 6.00r4 | 2011-09-08 | 2011-09-09 | 74 days after the archive exe date (2011-06-27) **[lab]** |

Lab sessions that need these builds still set the clock back into the pass window for the **whole** session (for example 2011-06-14 for 6.00r2, 2011-06-28 for 6.00r4) and keep it steady so the timer warning is not set off.

### 5.24r4 in detail (no expiry)

The 5.24r4 dump is MoleBox-wrapped and fully readable, with its import names intact. **[bin]**

- Date and clock calls: `GetLocalTime` and `GetSystemTime` (from the C runtime's `time()` and from one game routine), `GetSystemTimeAsFileTime` (only the runtime's start-up cookie), and `GetTickCount` and `QueryPerformanceCounter` (frame timing).
- The 13 callers of `time()` are random seeds, log time stamps, the GS2 elapsed-time helper, and the login cipher key (`time & 0x7F`). None of them compares the date with a fixed cutoff.
- It has no expiry text. The license file in the 5.12 bundle has no date in it either. It only lists the login hosts and links.

### The "wrong system timer" warning (5.24r3 onwards)

Every build from 5.24r3 to 6.03r7 carries this text. 5.12 does not have it. **[bin]**

> The game detected a wrong system timer. If this problem occurs again the please contact the GraalOnline team! (N ms)

In 5.24r4 the check works like this. **[bin]**

- About once a second, the client takes the wall-clock time of day from `GetSystemTime`, in milliseconds, and the tick counter from `GetTickCount`.
- If the two have moved apart by more than 100 ms since the last check, a strike is counted. After 3 strikes, a box titled "Warning" opens with the text above.
- So it is a speed-hack check, not a date check. A faked clock that drifts or jumps against the tick counter can trigger it. A clock that is merely set back, at a steady offset, does not. **[inf]**
- In the 2026-11-13 run on the real date there was no Warning box. **[lab]**
- In the Themida builds the string is present, but no code in the dump points at it, so the check could not be read there. **[bin]**

## Why the lab drew black (2026-11-13)

Server: GServer-v2 fork `fbd30767` (merge of #73), the `login` and `milestone` lab worlds, and a gen-5 logging proxy. Clients: real 5.24r4 under Wine, and Linux 6.03r7. **[lab]**

1. **No art in the worlds.** The `login` and `milestone` worlds held no `pics1.png`, ganis, bodies, heads, swords, shields, `state.png`, `sprites.png` or `chest.png`. The 5.x/6.x builds bundle no art (the Themida builds bundle nothing at all, and the MoleBox builds only GUI files). Every request was answered with `PLO_FILESENDFAILED` (30), and `game_console.log` listed each one as "not found". The screen was fully black at 20, 35 and 50 s.
2. **The warp came before `pics1.png` finished.** The worlds were copied and the 2.22 art set added: `pics1.png`, `state.png`, `sprites.png`, `chest.png`, 109 ganis, 20 bodies, 60 heads, 15 swords and 26 shields. With that, the HUD (hearts, AP bar, counters) and the player drew, but every tile stayed black.
   - Both clients ask for `pics1.png` **once, early, on the login server**. The login server sent the server warp (S→C 178) right after level entry. The 210,232-byte transfer was cut off: 6.03r7 logged it at 32,000 bytes, and 5.24r4 stopped at 160,000.
   - Neither client asks the target world for the tileset again.
   - With an older lab login server that answers the file requests before it warps, `pics1.png` completed. Then 6.03r7 drew everything: grass, trees, water, the lettering, three chests, the player and the HUD.
   - This held with that older build as the login server and the `fbd30767` build as the world server. So the world side is fine, and the cause is the timing of the login server's warp.
   - That older build refuses 5.24r4 ("Allowed: 4.042 - 6.037"). 5.24r4 was therefore run through the buffering proxy, with `pics1.png` complete before the warp, and it then drew the whole level in its 800×600 window.
3. **Not the cause:**
   - the date: 5.24r4 ran on the real date with no fake clock and showed no Warning or expiry text;
   - the renderer: no change was needed, and both clients log "Initialized OpenGL";
   - the VM's lack of a GPU.

### Lab gotchas

- 5.24r4 trusts its `FILENAMECACHE.txt`. A file deleted from its cache folder is never downloaded again (see also the stale-cache black view in `gs1-on-5x-hud-and-flags.md`).
- The lab NPC's `message` text was not visible in any frame, even in fully drawn ones. That is a separate open point and not a render fault.

## For lab servers

- Give the login world and the game world the full art set, at least `pics1.png`, the ganis, body, head, sword and shield images, `state.png`, `sprites.png` and `chest.png`.
- Do not warp a 5.x/6.x client off the login server until its first file requests have been answered, or have the target world send the tileset after the warp.
- No fake clock is needed for 5.24r3/r4, the 6.00 betas or 6.03r7. 5.30r3, 5.31r4, 6.00r2 and 6.00r4 need the clock set back for the whole session. Keep that clock steady, without jumps or a changed rate, so the timer warning is not set off.

## Wine fidelity policy (2026-11-16)

Owner confirmation (2026-11-16): later Wine runs that called **Windows 6.03r7 black / no input** and **5.24r4 no tiles or players** were installs that lacked the **base asset set from a Graal 2.22 client folder** (`pics1.png` and the other starter files). Those symptoms are **not** a client or gserver protocol gap once the asset tree is complete. **[doc]** (owner); same cause family as the 2026-11-13 lab above **[lab]**.

**Policy for 4.x–6.x loopback labs:**

1. **Wine is acceptable** for wire and draw checks on focus builds **4.208 / 5.007 / 5.120 / 6.037** (and neighbours) **when** the install holds the 2.22-era base assets before the client starts, and the login/world servers can serve them (and finish `pics1.png` before an early 178, as above).
2. Treat remaining Wine-only **black / no-draw** reports as **asset or warp-timing bugs** until a run with staged assets still fails.
3. Prefer a real Windows guest for **input and OpenGL edge cases** (for example 5.24r4 keys landing as game keys instead of chat under Wine in the five-client grid). Wine may still miss those even with art present. **[lab]**

Lab notes that scored 5.24r4 / 6.03r7 as “wire only” under Wine without staging that art set should be read with this cause: the messages arrived; the draw path never had a tileset. Re-run with assets before treating those cells as a Seihai or client defect.

### Re-score with 2.22 base assets (2026-11-16) **[lab]**

Loopback Wine re-run of **5.24r4** and **Windows 6.03r7** after staging the 2.22-era base files (`pics1.png`, `state.png`, `sprites.png`, ganis/bodies/heads/swords/shields/sounds/tileobjects; optional `chest.png`), clearing stale 5.24r4 `FILENAMECACHE.txt` rows for those names, and holding the login-server 178 until first file requests finished:

| Client | Tiles | Local player | HUD | Still black? | Input note |
|---|---|---|---|---|---|
| 5.24r4 (Wine) | yes | yes (after body/head/sword/shield served) | yes | no (letterbox only) | XTest reaches game keys; chat under Wine still prefer real Windows |
| 6.03r7 Windows (Wine) | yes | yes | yes | **no** | frame deltas after arrows/attack; full chat matrix still prefer real Windows |

So the five-client “wire” cells for these two builds were an **asset / warp-timing** miss, not a protocol or permanent Wine draw failure. Screenshots stay private (original art). The seihai-gserver five-clients lab note can cite this cause when next edited.

## Open

- [x] The cutoff dates of 5.30r3, 5.31r4, 6.00r2 and 6.00r4 (inside the protection layer; binary search on the clock would find them). **Done 2026-11-24 [lab]** — folded from the clock sweeps already recorded for E#14; see the cutoff table under [How the expiry works](#how-the-expiry-works-530r3-to-600r4).
- [ ] Whether the Themida builds' timer check matches 5.24r4's thresholds.
- [ ] The lab NPC `message` text not drawing on 5.24r4/6.03r7.
- [x] Re-score the five-client Wine “wire” cells for 5.24r4 / 6.03r7 with the 2.22 base asset set staged (draw and input may still differ from real Windows). **Done 2026-11-16 [lab]** — both draw tiles/HUD/player under Wine with assets + warp hold; see table above.
