# Reference-fork level persistence options

Date: 2026-11-22

This bounded G067 audit follows four settings through the newer GPL reference fork. It supplements the historical [server-option lead](../client-internals/graal-wiki-crosscheck-2026-11-11.md#leads-not-yet-researched-here); it does not establish original-server equivalence or complete the versioned 99-option reference. All links pin GPL-3.0 source at `0cf8f83d0ac658299abb4a9c93dab99cca805f37`. Findings are original-prose static source descriptions, not executed save or inactivity tests. **[srv]**

## Defaults and tile update paths

`savelevels` and `levelsautosave` both default false. `unloadinactiveleveltime` defaults to 600 seconds, while `savenpcsonlevelcache` defaults true. The settings are registered with the server's tracked configuration. [Declarations](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/Server.h#L141-L145), [registration](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/Server.cpp#L111-L113). **[srv]**

With `savelevels` disabled, `updateboard2` delegates to the ordinary respawning update path. With it enabled, staged script tile changes are applied without respawn. `levelsautosave` additionally gates copying eligible edits into instanced tile state and attempting a level-file rewrite. This tile-save path responds to the update operation; it is not a periodic tile-save interval. Separate NPC save routines must not be ruled out by that observation. [Update paths](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp#L1856-L1882), [separate NPC saves](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/npcserver/NPCServer.cpp#L312-L334). **[srv]**

## Copy extent and rewrite attempt

The copy helper visits intersected sublevels. Missing staged data, missing layers or static data, and empty clipped areas can prevent copying. Eligible nonempty staged tiles populate per-sublevel instanced tile state. The subsequent rewrite call instead selects the sublevel containing the update area's origin and calls the writer once. A rectangle crossing map parts therefore does not establish a rewrite of every affected level file. This is a source boundary, not a demonstrated runtime loss defect. [Copy helper](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp#L1810-L1853), [rewrite selection](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp#L1873-L1882). **[srv]**

The writer selects that sublevel's static data and an existing path or configured level directory, then serializes `GLEVNW01`, including LEVEL-backed NPC definitions for the selected map position. Missing prerequisites can return false. Its final true return does not inspect stream-open, write or flush state, and the update caller ignores the result. These are rewrite attempts, not verified durable or crash-safe writes. [Level writer](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp#L1001-L1139). **[srv]**

## Inactivity means sublevel NPC sleep

Only gmaps without `keepAllLevelsLoaded` enter this minute-gated inactivity check. Already sleeping sublevels and those without a last-use timestamp are skipped. Elapsed time must be strictly greater than `unloadinactiveleveltime`; an empty nearby-player data query then permits NPC sleep, while nearby players refresh the timestamp. The threshold is not an exact wall-clock deadline. [Inactivity loop](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp#L734-L763). **[srv]**

The sleep operation marks the sublevel and its NPCs sleeping. It does not unload the whole Level or save a level file. Last-use updates and wake operations are separate paths. [Sleep and wake helpers](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp#L533-L585). **[srv]**

## Empty-level NPC save requests

After player removal, an empty resulting player set records the last-player-left time. If `savenpcsonlevelcache` is enabled and an NPC server is available, the code requests saves for the level's NPC IDs. The observed predicate is empty-after-removal, not a proven exactly-once transition when the last player leaves. It is separate from the minute-based sublevel sleep loop. [Removal callback](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp#L1545-L1567). **[srv]**

Each request first needs a registered NPC whose weak reference is still live. The wrapper then calls the loader without propagating success. The selected flat-file writer accepts DATABASE storage only and rejects failed output opening; its later close, timestamp and filesystem-registration work does not establish atomic or durable output. This is distinct from the level writer's LEVEL-backed NPC serialization. It does not mean every NPC ID in the callback produces a file. [Wrapper](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/npcserver/NPCServer.cpp#L336-L344), [loader gate](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/loader/flatfile/FlatFileNPCLoader.cpp#L679-L708), [writer completion](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/loader/flatfile/FlatFileNPCLoader.cpp#L821-L864). **[srv]**

## Validation and remaining boundaries

The audit read source; no save-failure, cross-sublevel, inactivity or NPC-cache tests were executed. Meaningful future GPL-only controls would distinguish staged tile state, broadcast updates, attempted file operations and independently read file contents; test the strict threshold separately from the minute gate; and separate empty-after-removal requests from registered/live/DATABASE eligibility. **[srv]**

Existing [board-respawn evidence](../client-internals/board-respawn.md), [save/load and account placement](../client-internals/feature-specs/05-save-load.md), historical 2.2 command documentation and documentary database-NPC persistence retain their own build and evidence scopes. This newer-fork trace does not confirm those historical implementations, client behavior, live configuration changes or original-server agreement. G067 remains partial.
