# Level persistence and cache options in the pinned GServer-v2 fork

This note describes source behavior in the public reference fork
[squirelworks/seihai-gserver-v2 at commit
0cf8f83d0ac658299abb4a9c93dab99cca805f37](https://github.com/squirelworks/seihai-gserver-v2/tree/0cf8f83d0ac658299abb4a9c93dab99cca805f37).
It is a later open reimplementation, not an original Graal server. These findings
are a static source read; no server was run and no runtime result is claimed.

## Script-driven tile changes

The fork declares `savelevels` and `levelsautosave` false by default [srv]
([setting declarations](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/Server.h#L138-L145)).
The first option gates the script-driven `updateboard2` path. When it is off,
`updateboard2` follows the ordinary board-update route. When on, it applies the
script-staged tile change without the ordinary respawn behavior. The second
option acts inside that enabled path: it copies staged edits into per-sublevel
instanced tile state and attempts to rewrite the level file. This is triggered
by `updateboard2`; the source shows no autosave interval [srv]
([tile update and save route](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp#L1810-L1882)).

The writer emits a `GLEVNW01` level file. For an update rectangle spanning more
than one gmap sublevel, the staged tile update is applied across its covered
parts, but the save call names only the sublevel containing the rectangle's
origin [srv]
([level writer](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp#L1001-L1135)).
The save helper can report failure when level data or a managed directory is
missing. Otherwise it opens an output stream, writes the level, and returns
without checking stream state; `updateboard2` ignores that return value. The
source therefore establishes a save attempt, not that bytes reached durable
storage.

The older lab comparison records board-change retention for a different
GServer-v2 commit [srv]
([lab comparison](lab-servers-2026-10-30.md#2-gserver-v2-beta4-against-our-build)).
This static trace does not reproduce that run, identify its configuration, or
settle original-server behavior.

## Gmap sublevel sleep and NPC save requests

`unloadinactiveleveltime` defaults to 600 seconds. For eligible gmap sublevels,
a once-per-minute sweep checks eligible gmap sublevels; if the idle duration is strictly
greater than the configured seconds and no players are in range, it marks the
sublevel's NPCs as sleeping. A nearby player resets the idle timestamp. This
path sleeps NPCs; it does not unload the whole level [srv]
([sublevel activity check](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp#L734-L760),
[sleep and wake state](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp#L533-L585)).

Separately, `savenpcsonlevelcache` defaults true. When the last player leaves
a level, and an NPC server exists, the level asks it to save every NPC ID in
that level [srv]
([last-player path](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp#L1545-L1567)).
The NPC server ignores IDs that are not in its global NPC list. Its flat-file
loader rejects NPCs that are not database-backed; the level caller does not
check the save result. Thus the option enables save calls on player departure,
not proof that every level NPC was persisted [srv]
([NPC save dispatch](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/npcserver/NPCServer.cpp#L336-L344),
[flat-file save gate and writer](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/loader/flatfile/FlatFileNPCLoader.cpp#L679-L708)).

## Evidence and test limits

These claims describe this pinned fork only. The option defaults do not establish
historical server settings, and no original-server equivalence or runtime effect
was tested. The source audit found no targeted test evidence for the option
combinations, gmap cross-sublevel writes, failed level-file writes, the sleep
threshold, or NPC storage-type outcomes; no tests were run for this note.

A future test should distinguish the four `savelevels`/`levelsautosave`
combinations, in-memory updates, client broadcasts, and a parsed file after
reload. It should include a rectangle crossing a gmap sublevel boundary and a
deterministic unwritable destination. Separate cases should check the sleep
threshold and cadence, nearby-player reset, and last-player NPC save calls for
level-backed versus database-backed NPCs. A requested save must not be described
as durable unless the test verifies the resulting file.
