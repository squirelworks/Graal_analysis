# Reference-fork folder configuration and output routing

Date: 2026-11-22

This bounded G067 classification follows `nofoldersconfig` and `sharefolder`
through the newer GPL-3.0 Seihai GServer-v2 fork. All source links pin
`0cf8f83d0ac658299abb4a9c93dab99cca805f37`. It is attributed original prose,
not copied implementation or a versioned option table. The historical
[99-option lead](../client-internals/graal-wiki-crosscheck-2026-11-11.md#leads-not-yet-researched-here)
and original-server equivalence remain open. **[srv][doc]**

## Setup selection

The [world-filesystem setup](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/Server.cpp)
reads `nofoldersconfig` directly. False selects `loadFolderConfig()`;
true selects `loadAllFolders()`. The
[boolean parser](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/utilities/Settings.h)
recognizes case-insensitive true/false, and a missing or unparseable value
takes the false fallback at this call. These selected functions use
optional settings reads, rather than a cache read on each file operation.

The configured path reads `config/foldersconfig.txt`, adds category globs
under `world`, then requests binding `world`. The alternate path also
requests `world`; a present, nonempty `sharefolder` supplies additional
comma-separated binding requests. The selected
[split helper](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/utilities/StringUtils.h)
skips empty tokens but does not trim each nonempty token. `sharefolder`
is read in this alternate setup path, not the configured path.

This is setup selection, not a verified live toggle. The
[filesystem reset](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/filesystem/FileSystem.cpp)
clears indexed files and managed roots but retains folder-config patterns.
Re-running setup therefore does not itself establish a clean switch that
discards earlier filters. Duplicate setting-key precedence is outside this
classification.

## File membership is not output-root selection

The same [filesystem implementation](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/filesystem/FileSystem.cpp)
assigns each indexed file the ALL category and every matching configured
category. `findi()` performs case-insensitive filename lookup, checking a
file's category bit when folder patterns exist. Without patterns, that
category test is bypassed. Finding a file does not establish successful
opening, transfer or client use.

Directory binding recursively indexes regular files, but registers only
the explicitly bound root as a managed directory. The
[managed-root container](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/filesystem/FileSystem.h)
is unordered. Category-specific root selection uses a different rule from
per-file membership: the directory classifier returns the first category
in enum-index order whose configured glob parent matches that root.
Selection compares this single result with the requested category.
Without patterns, or for ALL, roots are exposed without that filtering;
no stable destination priority or unique enumeration is established here.

The category-taking `openForWriting()` and `openiForWriting()` first try an
existing direct path, then indexed lookup. Only when neither supplies a
result and creation is enabled do they append the requested path to the
first yielded managed root. Thus this fallback does not govern every
write. A recursively discovered file's parent is not automatically a new
output root, and category membership is not a writable-folder guarantee.
Constructing a fallback file object is not proof of successful or durable
output.

## Validation and limits

These are source reads, not option tests or an original-server run. The
fork's [existing manual](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/bin/docs/server.md)
already describes folder configuration. Parser recognition of a category,
including sound, does not by itself establish usable client behavior.

The separate [project path-binding correction](https://github.com/squirelworks/seihai-gserver-v2/pull/145)
does not make nested binding requests at this older pin proven successful.
This note does not claim runtime registration of configured roots,
reload correctness, duplicate-name priority, arbitrary-path validation,
durable saves or stock-server agreement. No implementation was changed by
this classification, and G067's wider versioned inventory remains open.
