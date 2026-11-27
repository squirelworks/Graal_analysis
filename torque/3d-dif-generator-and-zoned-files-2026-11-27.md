# v44 `.dif` interiors we can test with: our own generator and an open-licensed zoned file (2026-11-27)

Board rows T3D-030 / T3D-087 were blocked on "no enclosed, zoned v44 interior". They no longer are.

## What we have now

- **Our own files.** [`tools/dif/difgen.py`](../tools/dif/README.md) writes v44 / v0 interiors (the 5.12 gate,
  44/0/0) from box brushes: BSP, zones split by portal rectangles, portals, surfaces with texgens and a white
  lightmap (or none), one convex hull per brush with emit strings and poly lists, coordinate bins, map2dif's
  tail. Scenes: an enclosed two-room house (zones 0/1/2, two portals) and deliberately inconsistent variants
  (`noportal`, `window`) with their one-zone baselines, so a screenshot pair shows whether 5.12 culls by zone.
  **[gen]**
- **A reader/checker.** [`tools/dif/difdump.py`](../tools/dif/difdump.py) reads all 25 map2dif interiors of
  *Revenge Of The Cats: Ethernet* and the 12 held Marble Blast Gold demo interiors to the last byte with no
  problems (MBG: all 1 zone, no portals, clockwise windings). The ROTC files fixed the zone record (16-bit
  surface count + 16-bit flags, inside zones flags 1) and the vehicle-collision tail. **[file]**
- **Third-party zoned interiors, open licence.** *Revenge Of The Cats: Ethernet* by Michael Goldener,
  (C) 2008-2014, https://github.com/fr1tz/rotc-ethernet-game, game content under CC BY 3.0
  (https://creativecommons.org/licenses/by/3.0/): `share/interiors/eth3/base.dif` (2 zones, 1 portal,
  sha256 `d1a64380520c1d7a930987c1a94ecf0921a9af95e953a60a067e4c7c014587d9`) and
  `share/interiors/nort1/base.dif` (5 zones, 8 portals, sha256
  `d7217d203f261c50466f5d05963cdd2dd640712abb6e6e94e10afa4a8cb0ab1b`). Kept out of the repo; the lab takes
  them from a pack (`[packs] rotc`). Other zoned finds (TGE demo `orkbase`, TGE 1.4 cottages, MMOKit
  buildings, Marble Blast ports) are not openly licensed and are not used.

## Not yet run (exercise for the handover)

Conformance cases C049 to C056 ([cases](conformance/cases/)) play these on the real 5.12. A first run was
started on the Mirae VirtualBox lab host (seihai-gserver 833faba, VMs on reduced memory) but no results were
recorded before research was paused. To finish:

1. `python tools/conformance/run.py --lab <lab.toml> --build 5.12 --case C049,C050,C051,C052,C053,C054,C055,C056 --record`
   with `[packs] rotc` pointing at a rotc-ethernet-game checkout.
2. Read the pairs: C050 vs C051 (from outside, does room A show through a front wall with no surfaces?
   drawn = zones ignored outside), C052 vs C053 (from inside room A, does room B show without the portal?
   drawn = zones/portals ignored inside). C054 records `castray`, `getdropz` and `isInInterior` against the
   house (expected hits: y 12 beside the door, y 23.5 through both doors, roof z 4.5, floor z 0). C055: does
   a file with no lightmap load? C056: does the map2dif ROTC interior load?
3. Put the answers in the T3D-030 / T3D-087 board rows.
