# 5.12 movetype: rigid glides, list jumps (2026-11-26)

Lab: a real 5.12 client under Wine on Mesa llvmpipe, against our own gserver
(main at the #206 merge) on loopback. Question: how does the server's
`movetype` world setting change the way a 5.12 client renders a
position update driven by a `g3dpos` move? Behaviour only; trace stays in
the lab kit. **[lab][cap]**

This is the live counterpart to the static T3D-054 finding (5.12 reports its
own position and is sent no Torque Move): it shows how a *server-driven*
position lands on the client depending on `movetype`.

## `movetype rigid` → glide (move-list driven, transform unchanged)

With `movetype rigid` in `graal3dworld.txt`, a `g3dpos` move goes out as a
**stream of events** (~112 event/control lines for the move vs ~54 for
list), and the control object's own transform **stays at the old position** —
the control-object line keeps `at=30,-26,1` (its own move-data section, not
the transform). The move is
carried in the move data, not the object transform, so the client **glides**
to the target with a small lag. No object section is echoed for the move.

## `movetype list` → jump (transform carries the position)

With `movetype list`, the control object line goes **straight to the target**
— `control object: at 70.00,-26.00,1.00` in its transform section — i.e. the object is
sent with the new transform carrying the position, so the client **jumps**
exactly to the target (x 30 → 70 with no intermediate glide). Fewer events
than rigid.

## Summary

| movetype | how position is sent | client result |
| --- | --- | --- |
| `rigid` | move-list events; control transform unchanged | glides to target, small lag |
| `list` | control-object transform carries the new position | jumps exactly to target |

Both held the link with no desync and no drop (0 panics). So on 5.12 the
`movetype` setting selects between a move-list-driven glide and a
transform-carried jump — the same position arrives either way, but rigid
animates toward it and list snaps to it. (`interpolate`, seen earlier, glides
smoothly in step with the move — the same family as rigid.)

The other-screen view of the glide-vs-jump (how a second client sees the
moving player) is now captured with a stable 2D client (a real 2.22 under
Wine/Xvfb watching the 3D player's `g3dpos` moves): on the **2D** screen both
`rigid` and `list` appear as **jumps** — the sprite snaps to the target with no
in-between frames, indistinguishable between the two. So the rigid glide is a
property of the *moving* client's own render, not of what the position stream
carries to an observer: a 2D observer sees the same snap either way. (Captured
in [the 2D↔3D cross-view note](3d-2d3d-crossview-flags-movetype-512-2026-11-26.md),
T3D-054/069/133.) The `interpolate` other-screen view was not re-run.
