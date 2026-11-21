# Reference-fork tile-category options

Date: 2026-11-21

The Nov 11 [wiki cross-check](../client-internals/graal-wiki-crosscheck-2026-11-11.md#leads-not-yet-researched-here)
lists `newtilesets` and `newtilesetlevels` among options not read by GServer-v2.
The newer GPL reference fork consumes both, through the server's tile-category
lookup. This is a bounded source correction to G067, not a new reading of the
wiki's whole option list or evidence about the original server. **[srv][doc]**

All source links below pin the GPL-3.0 Seihai GServer-v2 fork at
`0cf8f83d0ac658299abb4a9c93dab99cca805f37`. The behavior is described in original
prose; no implementation or tile-category array is reproduced.

## Settings and selection

`newtilesets` is a tracked Boolean with a false default. `newtilesetlevels` is
a separate tracked list of strings, empty by default. These are effectful
settings, not two aliases for one value: one selects globally, the other
selects by the stored level name. Both caches are registered before settings
load. [Declarations](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/Server.h),
[registration and selection](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/Server.cpp).

The selection order is concrete: a missing level selects classic; an existing
level with terrain selects terrain before either option is considered. For a
non-terrain level, a matching list entry selects the new-format category map;
otherwise a true global Boolean does so. The remaining case selects classic.
The list check accepts either the string-mask helper or a literal prefix of
the stored level name. Both comparisons are case-sensitive as called here;
the selector calls the fork's own star/question-mark matcher, not a generic
glob API. In its pinned control flow, a pattern ending in a star does not
accept an empty suffix after an otherwise equal string; the literal-prefix
branch uses the unexpanded pattern. General glob compatibility is therefore
not implied. A literal prefix does not require a filename or directory boundary.
[Selector](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/Server.cpp),
[comparison helper](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/utilities/StringUtils.h).

The selector reads the cached values on each call. The cache machinery tracks
setting updates, but these functions do not establish a client notification,
image reload or successful live-toggle experiment.
[Cache implementation](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/utilities/Settings.h).

## Concrete consumers

The selected category map changes server-side tile lookup. The terrain branch
returns nonblocking before the tile-id range check. For other selections, ids
at or above 4096 return blocking; in-range classic and new-format selections
use their respective category arrays. Unrecognized selections fall back to
blocking. This traces the category selection, not the correctness of every
array member or its equivalence to an original client.
[Lookup](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/Server.cpp).

Level lookup checks coordinates at or above its upper dimensions and tile
availability first, returning blocking when those checks fail; terrain does
not bypass them. This read does not establish every negative-coordinate path. Once a tile is available it uses the selector
and category lookup. The level wall predicate returns true for the
throw-through, jump-stone and blocking categories; its rectangle form checks
the covered cells. The water predicate checks the water category.
[Level consumers](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp).

The NPC-server's tile-category helper delegates to the same selector; that
helper alone is not evidence of active script dispatch. The registered GS1
`tiletype` function directly returns the level category at the requested
position, or blocking when no current level exists. GS1 `onwall`
and `onwall2` call the level wall checks, but also have script-object/player
logic; these settings alone do not specify the whole GS1 collision result.
The `playerswimming` flag tests the player's tile category for water or lava
at its sampled position.
[NPC helper](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/npcserver/NPCServer.cpp),
[GS1 wall functions](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/scripting/gs1/GS1Functions.cpp),
[GS1 flag](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/scripting/gs1/GS1Flags.cpp).

## Remaining scope

- [ ] Original-server support and equivalence remain unverified.
- [ ] Client image selection, rendering and collision agreement are separate questions.
- [ ] Live setting changes and their observable effects need their own runtime evidence.
- [ ] The other options and historical 99-option inventory remain open; this audit supplies no replacement count.

This audit is a source read. It claims no new server test execution or lab
result and copies no GPL code or arrays into a permissive implementation.
