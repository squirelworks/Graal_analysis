# Reference reimplementations: what to trust

Date: 2026-10-30. Read-only study of two xtjoeytx repositories, weighed against
the real-client notes in this repository and Seihai's own documentation. The
code is summarized and cited, not copied. Nothing was sent to xtjoeytx (no
issue, PR or fork).

| repo | commit read | what it really is |
|---|---|---|
| `xtjoeytx/2dadventureclient` | `78040b7` (2020-02-29) | GServer-v2 (2020) with an SDL window and one local player bolted on. It hosts a server; it never connects to one. See `2dadventureclient.md`. |
| `xtjoeytx/LevelScriptEditor` | `2a81976` (2021-02-25) | A C# tool for bulk-editing NPC scripts in a folder of `.nw` levels, with "mark complete" tracking. Not a tile editor. See `levelscripteditor.md`. |

Tags used in these notes: **[2dac]** 2dadventureclient source, **[lse]**
LevelScriptEditor source, **[srv]** GServer-v2 source, **[2.05]**/**[2.22]**
real-client notes already in this repository, **[cap]** lab captures, **[inf]**
inferred.

## Verdict in one table

| behaviour | reference does | real clients | verdict for Seihai |
|---|---|---|---|
| wall test | one point at (x+2, y+2.75) | six-probe box, corner nudge, flush snap | **invented**, keep Seihai's box |
| walk speed | 4 px per rendered frame (about 15 tiles/s at 60 fps) | 0.5 tile per 50 ms (10 tiles/s) | **invented**, keep 50 ms steps |
| diagonal walking | both axes, one test, last key wins the facing | up, left, down, right as separate tested steps | **invented** |
| position on the wire | pixel props 78/79 for every client | 2.05/2.22 send half-tile props 15/16; pixels from 2.3 | **2.3+ only**, keep per-version |
| `gr.x` / `gr.y` flags | sent by a **server-supplied weapon** `-gr_movement` | — | **correction** to Seihai's `gr-flags.md`, see below |
| tile id to sheet pixel | 512-id blocks of 16 x 32 | same | **matches** |
| chest picture | tiles 1784 (closed) and 829 (open) | same ids in 2.22 `arrays.dat` | **matches** |
| draw order | all players and NPCs sorted by y | height layers (under, player, over, light) | **invented** |
| GANI timing | one shared timer per file, `WAIT` and `PLAYSOUND` skipped | per-object counter, `WAIT` holds | **incomplete**, don't copy |
| level links, gmap crossing, water, lava | not done for the local player | done | **missing**, nothing to learn |
| `.nw` read/write (LSE) | GLEVNW01 only, BADDY dropped on save | 2.05/2.22 write BADDY | **lossy**, don't copy the writer |
| NPC metadata headers (LSE) | `//#[KEY:value]` comment lines | not a client feature | **invented**, harmless comments |
| multi-layer boards (LSE) | keeps each `BOARD` layer apart | 2.22 ignores the layer field | **later era**, keep Seihai's merge |

## The correction: `gr.x` and `gr.y` come from the server

Seihai's `documentation/gr-flags.md` says "real clients keep the player's
position in two client flags, `gr.x` and `gr.y`" and models it as a client
behaviour per version (`LoginOnly` for 2.17, `Tracking` for 2.22). The source
of those flags is the server:

* GServer-v2 ships a weapon `-gr_movement` (`bin/servers/default/weapons/weapon-gr_movement.txt`)
  and puts `WEAPON -gr_movement` in `defaultaccount.txt`, so every new account
  on a stock server gets it **[srv]**. The 2dadventureclient fork carries the
  same files **[2dac]**.
* The weapon is a clientside GS1 script. On `playerenters` or `timeout` it does
  `setstring gr.x,#v(int((playerx+0.25)*2)/2)` (and the same for `gr.y`), then
  `timeout=0.05`. Unless the flag `gr.off`, `gr.x.off` or `gr.y.off` is set
  **[srv]**.
* The server's flag handler swallows `gr.x`/`gr.y`/`gr.z` from clients below
  2.3 and turns them into props 15/16/(z) for the other players, but only on
  ticks where no real movement prop arrived. The readme says this is to
  "simulate the smooth movement as found in the Graal clients 2.3 and up"
  **[srv]**. The setting is `flaghack_movement` (default on).
* The lab runs stock GServer-v2 (`tools/lab-setup.md`), and the public
  GServer-RS run also sent `-gr_movement` in the login burst
  (`client-internals/decomp-findings-2026-10-25-l/04-public-server-run.md`).

So what the captures show fits a script running in the client:

* the value is the position rounded to half a tile, written without decimals
  for whole numbers (`#v` formatting) **[cap]**;
* a 50 ms cadence in 2.22 is the `timeout=0.05` loop;
* 2.17 sending once at login fits `playerenters` firing and the timeout loop
  not running there **[inf]**;
* 2.31 never sending is not explained by the script; the cause was not
  checked **[inf]**.

**For Seihai:** a client should not send `gr.x`/`gr.y` on its own. It should
send them when, and only when, it runs a weapon script that sets them. On an
official 2001-era server there is no such weapon, so a real 2.05 or 2.22
client would send nothing. Seihai's script engine already runs weapon scripts
(the `§` line-break fix in Seihai's `public-gserver-run.md`), so the hard-coded
`protocol.gr_flags` profile switch is at best a duplicate of that, and at worst
a double send on a GServer-v2 server. Worth a lab run with the weapon removed
from the lab account to confirm the real 2.22 then sends no `gr` flags.

## What Seihai could adopt

Little of the client code, because the real-client notes here are already
more precise. The useful parts:

1. **The `-gr_movement` explanation** above (a fix, not an adoption).
2. **GServer's version workarounds as a checklist of server quirks** a
   Seihai client will meet on GServer-v2: the server deletes `Bomb` and `Bow`
   right after login because "the client adds them", sends `-gr_zlib_fix` to
   2.21 to 2.31, and pushes every big-map file to 2.31 because that client
   does not request it after `setmap` **[srv]**. These are server behaviours,
   not client ones, so a nostalgic Seihai should tolerate them, not imitate
   them.
3. **LevelScriptEditor's find-identical-scripts idea** for Seihai tooling:
   group NPCs across a level folder by exact script text (optionally the same
   image), edit once, apply to all. This fits the `npc-library` work. Take the
   idea, not the writer (see `levelscripteditor.md`).

## Small thing found in passing (Seihai)

`client/src/assets/level.rs` still has `tile_src_rect`, which maps a tile id
row-major on a 128-wide sheet (`col = id % 128`). That is the mapping
`client-assets.md` corrected on 2026-10-25. Nothing calls it (the renderer in
`render/tiles.rs` uses the right block mapping), so it is dead code that could
mislead.
