# 06 Handler behaviour changes, 2.00 -> 2.1

Basis: normalized-shape comparison of every handled id between consecutive builds (`handler_shape_changes.tsv`, similarity below 0.93 only), checked against the vendor changelog. A shape change means different statements, not necessarily different wire behaviour. Small handlers (4-12 statements) shift shape from compiler noise; only large drops are listed below.

## Revisions of the same version
- 2.00 rev1/rev2/rev3, 2.01 rev1, 2.02 rev1/rev2, 2.05 rev1/rev2: identical handler shapes for every id except one: 2.05 rev1 has one extra constant assignment in OTHERPLPROPS (id 8) that 2.05 and 2.05 rev2 do not have.
- The revisions differ in the VCL/RTL layer, not in game logic. 2.00 rev2, 2.02 rev2 and 2.05 rev1 each carry about 60 changed VCL/RTL functions (the multi-monitor wrapper set appears in rev2 builds; rev3 rolls part of it back). The only game-class changes are:
  - 2.00 rev1: one added options-form key handler.
  - 2.00 rev3: player creation and the tab-control handler.
  - 2.02 rev2: login (token + language) and the player-list history click.
  - 2.05 rev1/rev2: main-form creation and mouse-move handling; rev2 also a level-creation routine and server-list form creation.
- So for protocol work any rev of a version can stand in for the others, except 2.02 rev2 (different token, extra id 37).

## 2.00 -> 2.01
Biggest handler rewrites in the family (gs2lib names):
- LEVELBOARD (0) and PLAYERWARP (14), WARPFAILED (15): the client no longer does the "wait for level, then request level" steps inside the handler. This is the code side of "levels are preloaded when you walk on the map" in the changelog.
- LEVELNAME (6): shortened.
- BADDYHURT (27): a distance/direction-based calculation before the effect is removed.
- FREEZEPLAYER2 (154) / UNFREEZEPLAYER (155): go through a shared helper with a flag, instead of setting the field directly. 155 shrinks to one short step.
- HASNPCSERVER (44): stores a different constant than in 2.00 (value 11 instead of 1).
- New handlers: HITOBJECTS (46), SETACTIVELEVEL (156).

## 2.01 -> 2.02
- Only SAY2 (153) and PLAYERWARP (14) change shape. 47 STAFFGUILDS is new (list stored as comma text).
- The big 2.02 features (hats via gani attributes, signs with images, string parsing, free-server restrictions) are client-side script/UI and do not add any packet id other than 47.

## 2.02 -> 2.03
- NPCMOVED (24) grows (31 to 48 statements) and TOALL (13) changes slightly. That is the NPC `move` command and the pushed/pulled actions.
- SETACTIVELEVEL (156) shrinks to a single step.
- New: TRIGGERACTION (48), MOVE (165).

## 2.03 -> 2.04
- NPCMOVED grows again (48 to 55). MOVE (165) shrinks (17 to 9). SHOWIMGNPC (166) is new: matches "showimg works server-side, layer 4 works too".
- 26 NPCACTION is removed.
- Many other ids show only compiler-level churn.

## 2.04 -> 2.05 (all revs)
- SHOWIMGNPC (166) loses about 8 statements. UDP receive wrapper loses a bit-test step (purpose not resolved).
- New: id 168 (empty-ish body).
- Everything else is churn-level.

## 2.05 rev2 -> 2.1 test2
- Large churn in almost every handler. Treat as weak evidence: the 2.1 compiler output is lossy, and the new imaging engine (see `09`) touches many calls. Reliable facts are the id sets only (new 49, 169).
- PLAYERWARP2 (49): x2/y2 half-tile coordinates, an ignored z, two gmap cell bytes and the level name, same structure as the 2.17-2.31 layout in batch b. Tile positions are halved on receive.
- UPGRADEURL (169): raw text stored for the reconnect/upgrade button.

## 2.1 test2 -> test3
- LEVELBOARD (0), LEVELNAME (6) and PLAYERWARP (14) gain "is the incoming level the one already loaded" checks, so the client avoids reloading the same level. Same direction as in 2.31 (batch b noted that LEVELNAME compares with the current level).
- SAY2 (153) gains one extra call. The change to 31 is a constant-type difference only.
- No id added or removed.
