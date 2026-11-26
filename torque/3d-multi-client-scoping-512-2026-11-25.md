# 5.12 multi-client scoping: ghost count and distance (2026-11-26)

Lab: three real 5.12 clients under Wine on Mesa llvmpipe, against our own
gserver on loopback (never a third-party server). Question (T3D-075): how
does 5.12 scope other players — a ghost limit, and does a far player get
scoped out? One static observer plus two movers driven out to 454 and 630
units and back. Behaviour only; trace and screenshot stay in the lab kit.
**[lab][cap]**

## Ghost count — every player is ghosted to every other

With three players present, **all are ghosted to all**. The observer got a
`G3DPlayer` ghost for both other clients; the third client's log reads "gets
3 world objects and 3 players"; and each move relays "to 2 other 3D
clients". No cap was seen at three. (A higher cap was not probed — this says
there is no cap *at three*, not that the cap is unbounded.)

## Distance scoping — none

**There is no distance scoping.** The server relayed every position all the
way out — mover A to distance 454, mover B to 630 — and every relay line
still read "relay to 2 other 3D clients". The recipient count never dropped,
there was no ghost-out for a far player, and no distance threshold appeared.
A far player stays fully in scope and keeps updating at any distance tried.

Re-scope is therefore moot: nothing is ever scoped out, so the movers simply
went out and came back with continuous relays throughout.

## Server- vs client-decided

Scoping is **not server-decided**. The trace shows the server keeps relaying
every far player's position to everyone (out to 454 / 630). On the observer's
own screen a far mover just walks off the camera's framed area as it recedes,
but its ghost and its position updates are **still being sent and received**.
So any on-screen disappearance is the **camera frame** — the client not
drawing an object outside the view — not server scoping of the ghost.

## Conclusion

5.12 multi-client scoping is **flat**: with three players there is no ghost
cap, no distance-based scope-out, and the server sends every player's
position to every other player regardless of distance. Far players leave the
camera view but are never dropped from the ghost set or the update stream.
Whatever culling a client does is view-frustum drawing, not network scoping.

For a server: because nothing is scoped by distance, per-player relay cost
grows with the full player count, not with who is nearby — a scaling point to
note if a 3D world ever carries many players, though no cap was hit here.
