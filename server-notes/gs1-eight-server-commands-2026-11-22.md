# Eight GS1 server commands in the pinned GPL reference fork

This is a source reference for eight names in the historical GS1 server-command lead, using Seihai GServer-v2 at [`0cf8f83d`](https://github.com/squirelworks/seihai-gserver-v2/tree/0cf8f83d0ac658299abb4a9c93dab99cca805f37). It distinguishes registration, argument handling and selected effects from successful execution. It does not confirm the commands in an original server build: that G069 requirement remains open. No original server, compiler, script or gameplay probe was run. **[srv]**

Date: 2026-11-22. Evidence identifier: GS1-EIGHT-COMMANDS-20261122.

## Registration and shared dispatch

All eight names occur in the actual [GS1 command map][commands-map]. The dispatcher looks up the command and invokes its registered function after collecting argument values. Registration is not implementation proof: `saveinfo` is registered but its body throws an unimplemented-command error. These are GS1 visitor handlers; a similarly named GS2 client registry member does not establish GS2 server syntax or equivalent behavior.

The shared [dispatch/error path][dispatch] treats argument errors derived from `logic_error` as script warnings, while other standard exceptions are logged and rethrown. Therefore a filesystem exception, a missing optional dependency, and an ordinary no-op are not interchangeable outcomes. The wrappers do not provide a script-visible Boolean success result for the delegate operations below.

## Complete eight-command reference

| Command | Argument contract | Selected effect and limits |
|---|---|---|
| `addguildmember` | Exactly three values: guild, account and nickname. Failed string extraction supplies an empty string. | If the guild manager exists, requests membership insertion; otherwise no operation. Delegate success is discarded. [Body][addguild] |
| `removeguildmember` | At least two values: guild and account; a third nickname is optional. This body does not reject extra arguments. Failed string extraction supplies an empty string. | Empty or omitted nickname requests removal of all memberships for that account in the selected guild. A nonempty nickname requests removal of the first matching account/nickname entry. Missing manager is a no-op; success is discarded. [Body][remove-member] |
| `removeguild` | Exactly one guild value; empty-string fallback. | Requests removal of the selected guild's backing file when the manager exists. The selected manager body does not itself erase the in-memory guild entry; later lifecycle effects are not established here. Success is discarded. [Body][remove-guild] [Delegate][guild-delete] |
| `copylevel` | Exactly two filename values; empty-string fallbacks. | If the world filesystem locates the source in its level category, copies to the source directory joined with the requested destination, with replacement enabled. This wrapper does not report success, explicitly refresh the level cache, or establish destination containment, atomicity or durability. Missing source is a no-op; filesystem exceptions follow the shared error path. [Body][copy-level] |
| `deletelevel` | Exactly one filename value; empty-string fallback. | Acts only when the no-hint lookup returns a loaded level. It attempts safe-place warps for that level's players, discards each warp result, then requests removal of the resolved level file. A failed warp does not gate that removal call. No explicit loaded-level cache removal or successful disk deletion is proved by this wrapper. [Body][delete-level] |
| `saveinfo` | No implemented argument-validation or database-write path. | Unconditionally throws an unimplemented-command error. The fork's historical comment is not original-server confirmation. [Body][save-info] |
| `copystrings` | Exactly two prefix values; empty-string fallbacks. | Selects and normalizes storage prefixes, then copies values for matching source keys into destination names made from the new prefix and original suffix. Missing stores are a no-op. The copied payload is a typed game value, not necessarily text. Destination replacement and the same-store limits are detailed below. [Body][copy-strings] |
| `updateboard2` | Exactly four numeric values: X, Y, width and height. Each extraction falls back to zero, is bounded below by zero and passed through the fork's integral-floor conversion. | With a current level, passes the rectangle to its board-update operation; no current level is a no-op. The subsequent temporary/permanent/file behavior depends on separate settings. This is not a proof of safe extreme/NaN dimensions, allocation limits or original gmap behavior. [Body][update-board] |

## Membership changes and persistence

The selected [guild manager][guild-members] stores memberships by account. Adding to an existing guild inserts a membership and marks it modified. Creating a missing guild follows a creation path and requests a save after adding the membership. Removing one nickname removes the first equal nickname in that account's range; removing the whole account erases its keyed entries. The void GS1 wrappers discard delegate status.

A separate [save pass][guild-save] exists, but this reference does not establish its external scheduling or guarantee synchronous persistence for edits to an existing guild. The selected delete operation requests filesystem removal while retaining the in-memory entry in that body. These are bounded source actions, not a reproduced failure, a guarantee of later cache lifetime, or a new implementation proposal.

## `copystrings`: storage and value semantics

The [storage selector][storage-prefix] recognizes the fork's `this`, `thiso`, player/client variants, server variants, level, local and temporary prefixes. Recognition uses its case-insensitive prefix predicate. Unrecognized or unqualified names default to client storage in this command. Normalization is a separate operation: `this`, `thiso` and level prefixes are stripped; object-client variants remove the `o` only when that character is literally lowercase. Consequently recognition and normalization must not be summarized as universal case canonicalization.

[Store selection][store-selection] is context-dependent. `this` variants seek NPC storage, then weapon storage; client variants seek a player source. Object-context variants request a one-source skip; the helper can fall back to the last matching source it encountered, rather than guaranteeing a distinct outer source. Server variants use the server store. Level storage derives from the original player/NPC source; local and temporary storage use the visitor's built-in store. These source accesses are not proof that every missing-object or unavailable-level state is safe.

The copy loop uses the remaining source prefix with a case-sensitive prefix test. It constructs the replacement name from the destination prefix and unchanged suffix, then passes a copy of the source `GameValue` to [store insertion][store-add]. In the selected base GameVariableStore insertion path, a static destination container declines the insertion. Otherwise that base path creates a new variable wrapper, gives it the destination's default lifetime and optional source association, and inserts or replaces that destination name. The wrapper's weak result is ignored. The add operation is virtual; binding every possible destination override is outside this selected base-path read. Thus this base-path replacement does not mean preserving the old destination variable object's identity, metadata or aliases.

The [value container][value-container] has ordinary copy construction and stores Boolean, numeric, text and vector/object-reference forms. This supports typed value copying, not deep cloning of referenced game objects or transferring their ownership. The command iterates the live source store and performs destination insertion during that iteration. It does not create a source snapshot. When both names select the same underlying store, this reference therefore does not promise snapshot behavior, iterator safety, an exactly-once visit set, termination for prefix expansion, or preservation of aliases. No such edge case was executed here.

## Board changes and existing study boundaries

The [level delegate][board-delegate] falls back to the ordinary board-update path when `savelevels` is false. When enabled, it applies the selected scripted tile changes through its non-respawn path. It additionally requests retained/file updates only when `levelsautosave` is true and the required static level data exists. The command name alone therefore does not guarantee a saved file.

The existing [level-persistence study](../server-notes/level-persistence-options-2026-11-22.md) owns the deeper option-policy explanation; the [folder-routing study](../server-notes/folder-configuration-routing-2026-11-22.md) owns its indexed filesystem qualifications. This command reference does not replace those studies or independently prove packet routing, disk-write success, original-server compatibility or resource safety.

## What remains open

The historical [GS1 server-only lead](../client-internals/graal-wiki-crosscheck-2026-11-11.md) asks for confirmation from a server build. This GPL reference supplies a concrete later-fork contract, including a registered-but-unimplemented command, and cannot satisfy that original-build requirement by substitution. Original server availability/semantics, native runtime acceptance, GS2 equivalence, complete malformed-value behavior, callback scheduling, file containment/durability, same-store mutation behavior and game-object ownership remain separate questions. No whole G069 closure or permissive implementation transfer follows.

[commands-map]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/scripting/gs1/GS1Commands.cpp#L233
[dispatch]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/scripting/gs1/GS1Commands.cpp#L492
[addguild]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/scripting/gs1/GS1Commands.cpp#L680
[remove-member]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/scripting/gs1/GS1Commands.cpp#L1984
[remove-guild]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/scripting/gs1/GS1Commands.cpp#L1972
[guild-delete]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/utilities/manager/GuildManager.cpp#L197
[copy-level]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/scripting/gs1/GS1Commands.cpp#L1071
[delete-level]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/scripting/gs1/GS1Commands.cpp#L1116
[save-info]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/scripting/gs1/GS1Commands.cpp#L2098
[copy-strings]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/scripting/gs1/GS1Commands.cpp#L1087
[update-board]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/scripting/gs1/GS1Commands.cpp#L3823
[guild-members]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/utilities/manager/GuildManager.cpp#L243
[guild-save]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/utilities/manager/GuildManager.cpp#L80
[storage-prefix]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/scripting/gs1/GS1Visitor.h#L231
[store-selection]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/scripting/gs1/GS1Visitor.cpp#L289
[store-add]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/scripting/ScriptContainers.cpp#L168
[value-container]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/scripting/ScriptContainers.h#L63
[board-delegate]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp#L1861
