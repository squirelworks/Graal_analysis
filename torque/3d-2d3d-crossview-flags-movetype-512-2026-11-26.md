# The 2D↔3D cross-view, server flags, and movetype as a 2D observer sees it (T3D-069, T3D-133, T3D-054)

Date: 2026-11-26. Lab: a real 5.12 (3D) in a Windows 10 VM and a real 2.22 (2D,
Wine, headless Xvfb) on the same server, same world, loopback, `graal3d_trace` on,
against seihai-gserver #209 (c7ee7e9 → bbf165d). The 2.22 reaches the server
through the lab listserver (which lists the G3D server untagged; the `3 ` tag left
2.22's list empty). This is the stable second client the earlier movetype and
look-prop notes said they needed. Behaviour only. **[lab]**

Builds on [the look-prop note](3d-look-props-512-2026-11-26.md) (the first,
single-direction cross-view) and [the movetype note](3d-movetype-rigid-list-512-2026-11-26.md)
(the on-wire glide-vs-jump), which it completes.

## T3D-133 — server flags: a 2D client reads them, the 3D script does not

`serverflags.txt` with `server.labflag=on`, same world:

- **2D: yes.** A GS1 level NPC (`if (server.labflag) setplayerprop #c,labflag=#s(server.labflag)`)
  shows "labflag=on" over the 2.22 player.
- **3D: no.** The 5.12 weapon3d's `showtext` reads `server.labflag` **empty** for the
  whole run.

So the **same world** hands the flag to the 2D client but not to the 3D script.
This confirms the earlier seihai-gserver narrowing: the server sends the flag
correctly (the 2D side proves it on the same world), and the gap is the **5.12 3D
plug-in not exposing server flags to GS2** — a client-side receive/exposure
limit, not a server send gap.

## T3D-069 — the full cross-view matrix (2.22 ↔ 5.12)

Each row is what the *other* client shows for a player on the near client. **[lab]**

| property | 3D player → on the 2D screen | 2D player → on the 3D screen |
|---|---|---|
| presence | yes — a default 2D sprite, labelled with the account (`pc:1`) | yes — drawn as the world's playershape (a red cube) beside the viewer's own |
| position | yes — `g3dpos` moves show on 2D | **yes** — a ~16-tile 2.22 walk stepped the 3D `G2DPlayer` cube across the screen, trace `at=` updating ~every 200 ms |
| chat | yes — `player.chat` drew over the sprite | **no on screen** — the server carries it (`G2DPlayer … chat=…` in the trace; a weapon3d reads `.chat`) but 5.12 draws no text over the `G2DPlayer` |
| nick | no — `player.nick` never showed; the 2D screen kept the account | **no on screen** — the server carries it (`nick=` in the trace; a weapon3d reads `.nickname`) but 5.12 draws no nick over the `G2DPlayer` |
| head/body/colours | no way to set these from 3D; the 2D client shows the default look | none appear in 3D — always the world playershape |

So presence and **position cross both ways**. Chat and nick are **server-complete**
for the 2D→3D direction — the roster carries them and a 5.12 script can read
`G2DPlayer_<acct>.nickname` / `.chat` — but 5.12 **draws neither by default**;
rendering them over a `G2DPlayer` is a client/script matter. Head/body/colours
never cross: a 3D player is a default sprite on 2D, a 2D player is the world
playershape in 3D. **[lab]**

Two scripting notes: `findobject("G2DPlayer_<acct>")` returns 0, but the **direct
name reference** (`G2DPlayer_<acct>.nickname`) resolves — the object is reachable
by name, not via `findobject`. And with the 5.12 3D player in the level, the
2.22's **level-NPC timeouts did not run** on #209 (standalone they did): old Graal
runs level timeouts only on the **level leader**, which here was the 3D player.
This turned out to be a **server gap, fixed in seihai-gserver #211** (a 2D player
now gets `PLO_ISLEADER` when the leader links 3D, when it enters a level a 3D
player leads, and on any hand-off); re-verified on #211 the 2.22's timeouts run
with a 5.12 in the level in both join orders (see
[the multi-client coexistence note](3d-multiclient-coexistence-066-072-211-512-2026-11-26.md)).
**[lab]**

## T3D-054 — movetype, as the 2D observer sees it

Watching a 3D `g3dpos` move (6 tiles out and back) from the 2.22 screen
(snapshots ~every 0.34 s): **both `rigid` and `list` appear as jumps** — the
sprite snaps to the target with no in-between frames, indistinguishable between
the two. So the `rigid` glide seen on the wire (a move-list stream, the control
transform unchanged) is a property of the **moving client's own render**, not of
what the position stream carries to an observer: a 2D observer sees the same snap
either way. (`interpolate` was not re-run from this side.) This completes the
other-screen view the movetype note had left open. **[lab]**

## Summary

| row | verdict |
| --- | --- |
| T3D-133 | server flags reach a 2D client but not the 3D GS2 script on the same world — client-side exposure limit, not a server gap |
| T3D-069 | cross-view is presence + position both ways; chat/nick are server-complete for 2D→3D but 5.12 doesn't draw them (script-readable); head/body/colours never cross |
| T3D-054 | a 2D observer sees both `rigid` and `list` as jumps — the glide is the moving client's own render, not transmitted |
