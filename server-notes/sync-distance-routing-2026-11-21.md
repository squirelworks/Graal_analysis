# Reference-fork synchronization distances and nearby routing

Date: 2026-11-21

The historical [server-option lead](../client-internals/graal-wiki-crosscheck-2026-11-11.md#leads-not-yet-researched-here)
names synchronization distances among unread options. The newer reference
fork has concrete consumers, but they do not define a universal visibility
or movement-update cutoff. This is a bounded G067 source classification,
not a new 99-option inventory or original-server equivalence claim. **[srv][doc]**

All source links pin the GPL-3.0 Seihai GServer-v2 fork at
`0cf8f83d0ac658299abb4a9c93dab99cca805f37`. The behavior is described in
original prose, with no copied implementation or table.

## Defaults and the numeric query

`syncdistancex` and `syncdistancey` are separate tracked unsigned settings,
both defaulting to 192 tiles. `syncbydistanceinside` defaults false, and
`sendtonearbybigmaplevels` defaults true. These caches are registered with
the other server settings.
[Declarations](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/Server.h),
[registration](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/Server.cpp).

The synchronization query handles bigmaps first by delegating to the separate
data-range query. The numeric pair does not control that branch. After that,
a non-gmap level returns all its members unless inside-distance selection is
enabled. Otherwise the query compares global tile coordinates, using
inclusive independent X/Y differences against the float-converted settings.
This is a rectangle, not a Euclidean radius. If both configured distances
cover the corresponding map/level dimensions, it returns all members before
the per-player comparison. Caller filters can still restrict actual sends.
[Query](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp),
[player coordinate getter](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/object/Player.h),
[global pixel/tile conversion](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/object/Character.h).

Identified numeric-query callers are reciprocal entry-property exchange,
a departure cleanup loop and nearby ghost-icon refresh. The fork's specialized older-client
entry path also uses this query. These are specific call sites, not proof
that all property changes use the numeric distances.
[Client callers](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/PlayerClient.cpp),
[older-client caller](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/PlayerClientOriginal.cpp).

## Ordinary data routing and send gates

The ordinary level-scoped property buffer follows a different server helper,
which uses the data-range query. Without a map position that query returns
the current level's members. With a map position it uses a bounded 3-by-3
cell area: bigmaps enumerate loaded neighboring levels, while gmaps filter
members by their map-cell coordinates. This path does not compare the
numeric synchronization settings.
[Property-buffer route](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/PlayerProps.cpp),
[data-range query](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp),
[server helpers](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/Server.cpp).

A second nearby-send method applies additional gates after finding those
recipients. For a different level name it skips clients older than 2.01 and
also skips the send when `sendtonearbybigmaplevels` is false. A permitted
cross-level send is wrapped with temporary active-level selection and a
restore to the recipient's level. The property-buffer helper described above
does not apply this setting gate. It therefore is not a master switch for
every nearby-send method.
[Send-method gates](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/Server.cpp).

## Advice, updates and remaining evidence

The sample configuration describes a radius, warns that implementation is
incomplete and advises against distances below 64. The inspected numeric
predicate does not enforce a 64-tile minimum. Configuration advice is not a
validated clamp, and this audit makes no promise that malformed input restores
192. Later query calls read the tracked cached values; that alone does not
prove complete reannouncement or removal after a live setting change.
[Configuration advice](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/bin/servers/default/config/serveroptions.txt),
[predicate](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp).

- [ ] Original-server policy and equivalence remain unverified.
- [ ] Boundary, inside-level, bigmap-bypass and entry-versus-update behavior need targeted runtime tests.
- [ ] Live setting-change effects and client-visible agreement remain open.
- [ ] The wider historical option inventory remains open, without a replacement count.

This is a source audit with no new server test execution or lab result. It
does not copy GPL implementation into a permissive consumer.
