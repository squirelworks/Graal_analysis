# fxSunLight has exactly 14 animation-switch flags, not 16 — settled from the 5.12 engine's own field registration plus the live-accept check (T3D-047)

Date: 2026-11-26. Static read of the 5.12 `Graal3DEngine` (the same binary as [fxsunlight-512](fxsunlight-512.md)), cross-checked against the live-accept behaviour already captured. Conceptual only; nothing decompiled is reproduced here. Board row: [T3D-047](3d-capability-board.tsv). Settles the 14-vs-16 dispute left open between two earlier static reads; the live draw/crash behaviour is in [fxsunlight-512](fxsunlight-512.md) and [live-512-sun-replicators](live-512-sun-replicators-2026-11-25.md).

## Headline

**The fxSunLight animation-switch group is 14 flags, not 16.** The 5.12 engine's own fxSunLight class registers **exactly 14 boolean animation-switch fields**, in this order, and nothing resembling a 15th or 16th flag follows them (the next fields are key strings and cycle times, which are `pstring`/float, not flags). The live 5.12 client unpacks the **14**-flag layout cleanly, and a one-bit slip crashes the ghost unpack — a behavioural confirmation that the field group is 14 wide. The earlier "16" read was an overcount.

## The 14 flags, in field order **[bin]**

As registered by the class in the 5.12 engine (the same names the GS2 surface exposes, [gs2-3d-objects-404r2-512](gs2-3d-objects-404r2-512.md)):

1. anim colour
2. anim brightness
3. anim rotation
4. anim size
5. anim azimuth
6. anim elevation
7. lerp colour
8. lerp brightness
9. lerp rotation
10. lerp size
11. lerp azimuth
12. lerp elevation
13. link flare size
14. single colour keys

Immediately after these come the **key strings** (red/green/blue/brightness/rotation/size/azimuth/elevation keys — 8 `pstring`) and the **cycle times** (colour/brightness/rotation/size/azimuth/elevation time — 6 floats). Those are separate typed fields, not part of the flag group, which is why counting them as flags inflates the total. The booleans that precede the group — `enable` and `flaretp` — are separate raw-8 fields (layout fields 3 and 7 in [fxsunlight-512](fxsunlight-512.md)), not part of the animation-switch bits either.

## Why 14 is right, not 16

- **Field registration:** the class registers 14 — and only 14 — boolean animation-switch fields (anim ×6, lerp ×6, link-flare-size, single-colour-keys), matching the enumerated layout field 10 of [fxsunlight-512](fxsunlight-512.md) one-for-one. There is no 15th/16th boolean in that run; the sequence moves straight on to the key-string fields.
- **Live-accept check:** the real 5.12 client accepts a ghost built with the **14**-flag layout, and a one-bit misalignment crashes it during unpack ([fxsunlight-512](fxsunlight-512.md)). A 16-bit group would desync the 14-flag layout and crash every time; it does not.

So the two lines of evidence — the engine's own field set and the live client's clean unpack — both give **14**.

## "Which bit crashes" **[lab]**

From [live-512-sun-replicators](live-512-sun-replicators-2026-11-25.md): the client crashes on **all flags set together with animation key strings**, i.e. the animation/key-string processing path when every anim+lerp flag is on and keys are supplied — not a single identifiable flag bit that is unsafe on its own. Individual flags (and blend modes 0/1/2/9) unpack without a crash ([fxsunlight-512](fxsunlight-512.md)); the crash is in driving the full animation machinery at once, not in one bit of the 14.

## For a server

Treat the fxSunLight animation-switch group as **14 flags** (anim ×6, lerp ×6, link-flare-size, single-colour-keys), then the 8 key strings and 6 cycle times. Don't send all 14 anim/lerp flags on together with populated key strings — that combination crashes the 5.12 client. The networked sun still draws no flare regardless ([fxsunlight-512](fxsunlight-512.md)), so this governs ghost safety, not a visible light.

## Method caveat

Static read of the 5.12 engine's fxSunLight field registration (names and order only — no decompiled text, addresses or symbols reproduced, per the repo rules), combined with the already-captured live-accept/crash behaviour. The count rests on the field set (14 booleans) and the live client accepting the 14-flag layout; the exact wire bit-packing of the group was not re-traced instruction-by-instruction, but a 16-wide group is excluded by the clean 14-flag unpack.
