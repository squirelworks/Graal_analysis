# `.dif` interiors: our own generator and a reader

Torque interiors in the form the 5.12 client loads: **InteriorResource 44,
Interior 0, ForceField 0**, the TGE surface record. These are our own files,
built from nothing, so 5.12 interior questions (T3D-030, T3D-087) no longer
wait on someone else's interior.

| File | What |
|---|---|
| [`difgen.py`](difgen.py) | builds a `.dif` from axis-aligned box brushes plus portal rectangles; holds the lab scenes |
| [`difdump.py`](difdump.py) | reads any v44 / v0 file back (ours or a held map2dif one), prints counts, zones and portals, and checks every index |
| [`test_difgen.py`](test_difgen.py) | round trips, zones at points, portal sides, emit strings, coordinate bins; `DIF_SAMPLES=<folder>` also reads held files |

```
python3 tools/dif/difgen.py list
python3 tools/dif/difgen.py scene house out.dif [lightmaps=none]
python3 tools/dif/difdump.py out.dif --zone 0,3,1
python3 -m pytest tools/dif -q
```

The conformance content generator (`tools/conformance/gen_content.py`) makes
every scene as `conf_dif_<scene>.dif` (and `_nolm` with no lightmap) with
solid-colour textures `conf_dif_out/floor/a/b.png`. Nothing generated is
committed.

## What a generated file holds

- **BSP**: axis-aligned split planes over a grid made from every brush face;
  each empty leaf names its zone, each solid leaf lists the surfaces on it.
- **Zones**: zone 0 is the outside (everything reachable from the edge of the
  grid). Every enclosed region is its own zone; a portal rectangle across a
  doorway splits two regions. A portal that would join a zone to itself is
  refused (the zones leak). Inside zones carry flags 1, the outside 0, as
  map2dif writes them.
- **Portals**: a plane, a one-fan polygon, and the zones in front and behind.
- **Surfaces**: every brush face touching empty space, merged into
  rectangles per brush, material and zone; 4-point triangle strips; texture
  generators at 4 units per repeat; a place in a white 256 x 256 lightmap
  (one lumel per unit) or no lightmap.
- **Collision**: one convex hull per brush with its 8 corners, 6 planes,
  emit strings (the whole box for every support point) and poly list (the
  hull's surfaces as fans, one plane group per plane), and the 16 x 16
  coordinate bins over the hulls.
- **Tail**: five empty object lists, an empty vehicle-collision block and no
  game entities: the 88 bytes map2dif ends every file with.

## The lab scenes

`house()`: an enclosed two-room house 16 x 12 x 4.5 on a floor slab. Room A
(zone 1, hot pink) behind a front door, room B (zone 2, teal) behind a middle
door, a portal in each doorway, near-white outside walls, brown floor and roof.

| Scene | Difference | Question |
|---|---|---|
| `house` | consistent: zones 0/1/2, two portals | does it load and draw? |
| `single` | the same geometry, all in zone 0, no portals | baseline |
| `noportal` | the A-B doorway splits the zones but no portal is written | from inside A, is B culled? |
| `window` | no front door; the front wall is solid but has no surfaces | from outside, is room A culled? |
| `window1` | `window` with everything in zone 0 | baseline for `window` |

Cases C049 to C056 in [`torque/conformance`](../../torque/conformance/README.md)
play them on the real clients.

## Sources for the format

- Field order and widths: the MIT-licensed Torque 3D 1.1 interior source
  (`Engine/source/interior/interiorIO.cpp`, `interiorRes.cpp`,
  `interior.cpp` `processHullPolyLists`, `interiorCollision.cpp`
  `getFeatures`), read, not copied. The BSD-licensed HiGuy Dif library's
  version-0 writer agrees.
- Checked against real map2dif output: `difdump.py` reads all 25 interiors of
  *Revenge Of The Cats: Ethernet* by Michael Goldener, (C) 2008-2014
  (https://github.com/fr1tz/rotc-ethernet-game; its game content is under
  CC BY 3.0, https://creativecommons.org/licenses/by/3.0/) to the last byte.
  Those files settled two points: a zone record ends with a 16-bit surface
  count and 16-bit flags, and surfaces wind so that Torque's
  `PlaneF(v0, v1, v2)` of a strip's first triangle is the stored plane. The
  files themselves are not in this repo; the lab takes them from a pack.
- The 5.12 version gate (44 / 0 / 0): our own read of `Graal3DEngine.dll`
  ([stock-tge-reference-mbg](../../torque/stock-tge-reference-mbg-2026-11-25.md)).
