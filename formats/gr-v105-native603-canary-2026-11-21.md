# GR-V1.05 native Linux 6.03r7: parser canary and physical link returns

Date: 2026-11-21. Tags: **[lab]** for the original-client observations below.
Evidence ID: `GR105-NATIVE603-CANARY-LINKS` in [the evidence index](../docs/evidence-index.tsv).
This follows the [initial served-layer result](https://github.com/squirelworks/Graal_analysis/pull/753)
with a separate bounded run. It adds no Windows-client result.

## Setup and scope

The original native Linux 6.03r7 client ran in the Debian lab VM against the same existing
world-server deployment as the first positive run. Its deployment record associates the
world binary with source `01bb0b3f`, descended from the reference fork's reader repair.
That association remains reported provenance, not an independently reproduced build;
no server build or test rerun is claimed here. The controller reports loopback-only traffic
in a private VM network namespace.

Three generated positive fixtures were used: two layers, an explicit empty hole, and RLE.
The client entered each fixture through an injected chat warp. The canary was then applied
and measured before returning to the hub. No malformed fixture was replayed.

## Independent HUD/parser canary

The run first recorded two reference frames after setting the bomb-count HUD property to
1 and 99 respectively. Before each fixture, it reset the property to 1 and recorded a
before frame. After the serve, a separate injected `PLO_PLAYERPROPS` (9), property 5 = 99,
tested subsequent packet parsing and HUD update. This is an independent parser/HUD canary,
not a bomb-use, sword or broader gameplay-action test. **[lab]**

The scorer used the existing [canary.py](../tools/probe/canary.py) distance rule: mean absolute
grayscale difference in the 40 by 22 bomb-count region of the 1024 by 768 frame. A sample
is landed when its distance from the 99 reference is less than half its distance from the
1 reference; the reverse is lost. The controller used a private bitmap-decoding port with
the integer RGB-to-grayscale coefficients. The original Python/Pillow tool did not run
successfully in the guest, so its execution is not claimed.

| Fixture | Before serve | After serve and separate canary | After physical return |
|---|---|---|---|
| two layers | lost | landed | landed |
| explicit empty hole | lost | landed | landed |
| RLE | lost | landed | landed |

All three served-canary regions matched the 99 reference exactly in the scorer's grayscale
comparison. The returned frames remained closer to that reference under the same rule.
The retained served frames show the painted regions and hole; returned frames show the hub.
These observations add a parser/HUD liveness check to the earlier client-alive markers. **[lab]**

## Physical return through advertised links

After each served-canary frame, the plan used a chat warp to an approach position inside
that same positive level. It then held Down for 1.2 seconds and released the key.
After the physical-input marker, each case produced a client `PLI_LEVELWARPMOD` (30)
naming the hub, followed by the server's `PLO_LEVELNAME` (6) response for that hub.
No chat-warp command occurred between that marker and the client request. The returned
screens remained alive and drawn. **[lab]**

This proves the advertised bottom return link in one direction for those three fixtures.
It does not prove walking into the positive levels from the hub; ingress in the
successful run remained chat warp.
The successful follow-up plan had no packet-9 wait timeout.

## Remaining gap

- [x] Add the independent parser/HUD canary after serving each native Linux positive fixture.
- [x] Exercise each advertised bottom return link with physical input and bind the resulting
  client request, server level response and returned frame.
- [ ] Establish correctly served coverage on Windows 5.12 and the separate 5.24r4 repaint case.
- [ ] Establish walking ingress separately; one-direction return is not bidirectional traversal.
- [ ] Measure heights, malformed inputs and a real vendor-original on-disk sample separately.

G226 and the live portion of G227 remain partial. These results do not imply arbitrary
GR-V1.05 compatibility or an actual bomb-use gameplay test.
