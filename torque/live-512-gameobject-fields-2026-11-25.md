# 5.12 GameObject fields on the wire, tested live (2026-11-25)

Lab: the real 5.12 client on Mesa, a server sending one GameObject field at a
time (series 2). Behaviour only; captures in the lab share. Board rows:
T3D-015, T3D-046. **[lab][cap]**

## Section 2 is scale, not velocity

The second GameObject update section is the shape's **scale** about its
origin, not velocity as the static read guessed:

- `(2,2,2)` doubles the shape, `(1,1,3)` makes it three times taller,
  `0.5` halves it, all about the object's origin.
- `(0,0,0)` draws it at normal size, so that value means unset.

This corrects udp-session.md section 8 and wire-by-build.md section 2.

## Rotation and visibility flags

- Rotations about x, y and z all apply.
- Of the boolean flags (section 13), only `0x0004` hides the object
  (`0xffff` hides it too, since it includes that bit). `0x01`, `0x02`,
  `0x08`, `0x10`, `0x40`, `0x80` and `0x100` each drew a pixel-identical
  frame; `0x20` is being rerun.

## Fields accepted but not drawn on a static GameObject

skin (with or without `.png`), chat, attr1 to attr3, and nickname with
colour are all accepted but show nothing on a static GameObject: no pixels,
no file request, no name tag and no chat bubble. These probably need a
player or a control object, not a plain scenery GameObject.

## Sky bottom face and `.ft`

From the GDI runs:

- With sky flags `1 1 1`, sky entry 5 draws as a floor below the horizon.
  So the bottom face is drawn when the flags turn it on.
- A skin is never requested for a `.3ds` shape.
- A live `.ft` text shape downloads with its texture but draws nothing; this
  is being rechecked.
