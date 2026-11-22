# Reference-fork script-engine defaults

Date: 2026-11-22

The historical [server-option lead](../client-internals/graal-wiki-crosscheck-2026-11-11.md#leads-not-yet-researched-here)
still needs a versioned inventory. This bounded G067 result classifies
`scriptstyle`, `default_scriptengine` and the two side-specific defaults in
the newer GPL-3.0 Seihai GServer-v2 fork. All source citations pin
`0cf8f83d0ac658299abb4a9c93dab99cca805f37`. This is attributed original
prose, with no copied implementation or option table. **[srv][doc]**

The fork's [own option note](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/bin/docs/server-options-gaps.md)
already calls this an implemented alias. The finding is its concrete
consumer chain, not a newly implemented feature or proof of stock-server
behavior. The November 11 counts are not a refreshed inventory.

## Initialization and precedence

The [server cache declaration](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/Server.h)
gives `scriptstyle` a `gs1` fallback, and
[settings registration](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/Server.cpp)
tracks it. The actual default-engine selection occurs when the NPC-server
initializes, through direct settings reads rather than that cache on each
compile. The server constructs and initializes the NPC-server only when
`serverside` resolves true.

[NPC-server initialization](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/npcserver/NPCServer.cpp)
prefers a present `default_scriptengine`, then a present `scriptstyle`, then
GS1. Individually present `default_scriptengine_client` and
`default_scriptengine_server` override that shared choice for their sides.
These presence checks do not validate engine names or make an empty value
absent. The selected strings are copied into the script system during
initialization. Both GS1 and GS2 engines are registered regardless of the
chosen defaults; choosing GS2 does not remove GS1. Hot reconfiguration is
not established by these reads.

## Compile consumers and separate generation routing

For nonempty source, the
[script system](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/scripting/ScriptSystem.cpp)
starts with the appropriate side's default. A leading `//#` engine marker
can select another registered engine; its name is lowercased. Compilation
uses the CLIENT or SERVER target, respectively. Rejection or failure of a
selected non-default engine returns no result. The remaining client path
can try GS2 as a final fallback; the server path has no corresponding final
GS2 attempt. Compiled-result caching exists, so this read does not establish
per-request cache isolation or settings reload behavior.

The [script object's compile route](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/scripting/Script.cpp)
requires an NPC-server and branches on ServerGeneration, not `scriptstyle`.
NEWMAIN and CLASSIC compile server pieces while retaining their existing
client-text routes. MODERN requests compiled client and server pieces, and
clears client source when client compilation fails. Source markers and
generation routing must therefore remain separate from default selection.

The [GS1 engine's CLIENT target](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/scripting/gs1/ScriptEngineGS1.cpp)
translates GS1 source into GS2 bytecode, rejecting a failed translation.
Selecting GS1 as the source engine does not imply raw GS1 wire bytes on
the modern route. These settings are not universal parser, save-format or
client-generation switches.

## Another default-client consumer

The [player's saysnumber property](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/Player.cpp)
also looks up the default client engine through the
[script-system getter](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/scripting/ScriptSystem.h).
When available, it evaluates chat text up to the first space, with an
additional question-mark cutoff for GS1. It falls back to numeric parsing
when no expression result is available. This is a concrete downstream
consumer, not a measured gameplay result.

## Validation and limits

The existing [script-style test definitions](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/Catch_tests/ServerOptions/ScriptStyle_tests.cpp)
were read, not executed. The first case checks cache registration, fallback
and updates without initializing the NPC-server. The precedence case tests
a helper defined in the test file, duplicating the selection logic rather
than invoking the production initializer. It does not establish production
precedence, per-side overrides, empty/unknown values or compilation end to
end.

The [November 14 named-login lab](../protocol/named-login-5x-6x.md#the-method)
records needing the client-side default override and a marker not being
honored in that run. That historical result is unchanged; this newer pinned
source read does not retroactively validate or replace it. Runtime compile
success, live changes, original option domains/defaults, original-server
equivalence, general GS1/GS2 parity and Mac build/run remain unverified.
G067's wider versioned inventory remains open.
