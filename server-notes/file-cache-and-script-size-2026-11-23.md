# File checksums, cached resources and script sizes: a versioned comparison

The [historical 4.02 lead](../client-internals/graal-wiki-crosscheck-2026-11-11.md#leads-not-yet-researched-here) groups file-checksum updates, in-memory gmap/package caching and an RC editing-limit increase from roughly 28k to 100k, with an old-engine compatibility warning. Those remain documentary claims about that era. This note compares them with the later GPL reference fork at [`0cf8f83d`](https://github.com/squirelworks/seihai-gserver-v2/tree/0cf8f83d0ac658299abb4a9c93dab99cca805f37); it does not identify that fork with the original 4.02 server. **[doc][srv]**

Date: 2026-11-23. Evidence: FILE-CACHE-SCRIPT-SIZE-20261123. Source read only: no server, archived client, script or network test was run.

## A checksum request is not a universal package rule

In [the file-verification handler][verify], the server reads a five-character unsigned checksum followed by a filename. For files other than `.gupd`, it locates the file and loads its bytes into a local string. A nonempty file with matching CRC32 produces the up-to-date reply, after the separate package-key send. An empty file does not take that matching branch. A missing ordinary file returns without sending it, except for the selected 3D-client path, which continues to the file-send call. **[srv]**

The `.gupd` extension explicitly bypasses that checksum-comparison branch and reaches `sendFile`. This is a concrete exception in this handler, not proof that update packages never use checksums. In [the package-member request][members], the server finds the cached package resource and compares supplied checksums with its stored member entries. Reinstall mode clears the supplied checksum sequence, requesting every listed member. Missing/different checksums contribute the stored member size and a subsequent file-send request; the handler then emits its completion reply. **[srv]**

The latter loop consumes available checksums in the package's stored member iteration order. This source read does not establish the correctness of a particular client's ordering, the freshness of every stored entry, transfer success or a historical protocol change. **[srv]**

## What is retained in memory

[Package reload][package] clears the retained package checksum, aggregate size and member list, reads the manifest from disk and computes its CRC32. For each recognized `FILE` line it derives a basename, locates a file, reads its bytes and stores the member's length/checksum. The selected object retains this metadata; these local reads do not demonstrate retention of all member file bodies. The [resource manager][resources] retains shared resource objects by name, and also records an empty pointer for a failed load rather than automatically retrying on every lookup. **[srv]**

At world-filesystem setup, [the server enumerates `.gupd` files][world-files] and requests package reload. In [the file-category event callback][events], deletion removes a package resource and modification requests its reload when lookup succeeds. That callback's ordinary-file branch does not perform the same package-member rebuild: it has separate modern-generation update notifications and GANI handling. These are selected invalidation paths, not a guarantee that every dependency change refreshes all package metadata. **[srv]**

Gmaps have a different retained representation. [Map loading][load-maps] clears the server's map-object list and constructs maps named in configuration. The [gmap constructor][map] opens its indexed file and populates parsed map state, including level names and preload information. It does not follow that the raw gmap file is a universally cached transfer body. The [file index entry][file-data] holds a path, categories, size/time metadata and callback, and its `openFile()` constructs a file object. Its watcher [updates indexed state and invokes file/category callbacks][watch]. Those mechanisms must not be conflated with the package manager. **[srv]**

The selected [gmap warp path][warp] is also independent of a checksum request: it requests the gmap file for clients before version 3, or when the later client's session has not seen that file, then sends the warp message. This later-fork compatibility route cannot establish the original 4.02 cache rule or client disk-cache persistence. **[srv]**

## Editing, stored source and client output have different bounds

The selected [NC NPC-script setter][npc-set] reads the remaining tokenized script, converts its line representation, and calls the NPC script setter. The [NC weapon setter][weapon-set] reads name/image fields and the remaining code, restores line separators and updates or creates the weapon. Neither selected body contains an explicit roughly-100k script-length check. These are NC handlers in this fork, not evidence for the historical RC editor's limit; upstream framing and other paths remain separate. **[srv]**

The [NPC setters][npc-warn] and [weapon-file loader][weapon-warn] warn when client-side source exceeds 28,767 bytes without pre-existing client bytecode. A warning alone is not input rejection. The actual [NPC GS1 property serializer][serialize] has a separate effect: modern server generation emits zero text length; the classic branch converts source to its wire-text representation, then bounds both the declared length and emitted prefix to 28,767 bytes. The [NPC property binding][binding] supplies the assembled client-side script to this serializer. This output bound does not establish a stored-source or editing bound. **[srv]**

It is not a universal bound on every script send. In the selected [classic weapon-text branch][weapon-send], the fork writes the converted script length and complete script directly, subject to that branch's bytecode/profile selection. The NPC serializer's truncation must not be projected onto this independent path. Nor does either path prove how an old engine handles an oversized script. **[srv]**

## Remaining G070 scope

- [x] Classify the selected later fork's checksum exception, cached package metadata, explicit reload routes, parsed map state and distinct script-input/output paths.
- [ ] Confirm the original 4.02 server's file-checksum and memory-cache behavior, including invalidation and historical timing.
- [ ] Establish the historical RC editing-limit increase and its exact unit, framing and build boundaries.
- [ ] Confirm the stated old-engine failure with version-bound original evidence. Warnings, truncation and a wide stored string are not that evidence.

G070 remains partial. This is a source comparison with a newer, modified fork, not a historical refutation, native parity result, runtime acceptance test or implementation port.

[verify]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/packets/PlayerClientPackets.cpp#L1583
[members]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/packets/PlayerClientPackets.cpp#L1710
[package]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/UpdatePackage.cpp#L17
[resources]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/utilities/manager/ResourceManager.h#L33
[world-files]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/Server.cpp#L853
[events]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/Server.Init.cpp#L432
[load-maps]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/Server.cpp#L1009
[map]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Map.cpp#L88
[file-data]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/filesystem/FileSystem.h#L35
[watch]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/filesystem/FileSystem.cpp#L159
[warp]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/PlayerClient.cpp#L1278
[npc-set]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/packets/PlayerNCPackets.cpp#L216
[weapon-set]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/packets/PlayerNCPackets.cpp#L635
[npc-warn]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/object/NPC.cpp#L767
[weapon-warn]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/object/Weapon.cpp#L63
[serialize]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/utilities/PropertySerializers.cpp#L587
[binding]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/object/NPC.h#L661
[weapon-send]: https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/object/Weapon.cpp#L184
