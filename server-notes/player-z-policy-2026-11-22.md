# Reference-fork player Z updates and NPC touch policy

Date: 2026-11-22

The historical [server-option lead](../client-internals/graal-wiki-crosscheck-2026-11-11.md#leads-not-yet-researched-here)
combines a Z-range description with a locking option. The newer fork has
separate coordinate conversion, property-update and NPC-touch paths. This is
a bounded G067 source classification, not original-server equivalence or a
replacement for the wider option inventory. **[srv][doc]**

All source links pin the GPL-3.0 Seihai GServer-v2 fork at
`0cf8f83d0ac658299abb4a9c93dab99cca805f37`. This is original-prose source
analysis, with no copied implementation, new test execution or client run.

## Settings and Z property updates

The Boolean keys `lockplayerz` and `playertouchsmenoz` both default false.
They are tracked settings with actual consumers. The second spelling is the
configuration key, despite the different spelling of the C++ field.
[Definitions](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/Server.h#L196),
[tracking](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/Server.cpp#L128).

After their input checks, the coarse Z and pixel-precision Z2 property
setters return a revert result when `lockplayerz` is true. Z2 ignores an
already-equal coordinate before reaching its lock check. The opened lock
checks have no generation or server-origin exception. On the assignment
path, the setters store optional pixel Z, clear paused state, include
the counterpart coordinate property in their results and update movement
time for a client player. Neither Z-only update invokes the NPC-touch probe.
[Z setter](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/PlayerProps.cpp#L508),
[Z2 setter](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/PlayerProps.cpp#L1127).

These gates do not reset an existing Z to undefined. The account loader
assigns saved Z directly, and the script Z setter writes the coordinate
helper's result directly; neither path reads the lock. Saving a present Z
also does not apply it. The option is therefore not a universal invariant
over all stored state or direct server assignments.
[Account load](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/loader/flatfile/FlatFileAccountLoader.cpp#L209),
[script setter](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/Player.cpp#L1621),
[save](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/loader/flatfile/FlatFileAccountLoader.cpp#L667).

The coordinate helpers independently clear an optional coordinate when its
converted pixel value lies outside the range corresponding to −50..170 tiles.
Their conversions use 16 server pixels per tile. This is a check after
conversion, not validation of every arbitrary numeric input before narrowing.
The range rule does not read `lockplayerz`; it must not be attributed to the
option or treated as a new client-decoder result.
[Range definition](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/object/Character.h#L75),
[pixel helper](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/utilities/PropertySerializers.cpp#L469),
[coarse helper](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/utilities/PropertySerializers.cpp#L552).

## NPC-touch probe and event queues

The touch routine first requires an NPC-server. It tests signs and links
before the NPC-touch path, returning early when either handles the movement.
The remaining path constructs a facing-dependent XY probe from the player's
global pixel position, with a vertical span of 48 pixels. If
`playertouchsmenoz` is true, the probe's Z origin becomes the minimum signed
16-bit value and its length the maximum unsigned 16-bit value. Other probe
dimensions and stored player Z are unchanged.
[Touch routine](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/PlayerClient.cpp#L1859),
[pixel-position producer](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/object/Character.h#L57).

The resulting query intersects that probe with NPC collision boxes, through
the level's visibility and nearby-NPC selection. These are relative XYZ
overlap tests, not a universal condition that absolute player Z must be below
three tiles. NPC collision boxes have their own shape and Z. The separate
nearby search uses XY distance on map levels.
[Collision query](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp#L3541),
[NPC boxes](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/object/NPC.h#L596),
[overlap predicate](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/utilities/Extents.h#L399),
[nearby selection](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/level/Level.cpp#L3415).

Intersecting NPCs get a queued player-touches-me event. Only after at least
one touch, nearby nonintersecting NPCs may get a queued player-touches-other
event. Queueing is not proof that a script handler ran. XY and X2/Y2
property changes, and sprite direction changes, invoke this probe when a
client-player object is available. The option does not govern every trigger,
player-hurt path, collision, client rendering or Z packet encoding.
[Event queueing](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/PlayerClient.cpp#L1890),
[XY callers](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/PlayerProps.cpp#L470),
[direction caller](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/PlayerProps.cpp#L545),
[pixel-coordinate callers](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/PlayerProps.cpp#L1091).

## Validation and remaining evidence

The sample configuration's short lock/reset and touch-height descriptions
do not replace the consumer conditions above. The existing client Z layouts
and historical touch observations remain separately attributed.
[Configuration comments](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/bin/servers/default/config/serveroptions.txt#L120).

- [ ] Production-path tests should distinguish existing state, Z/Z2 property rejection, direct script assignment and account loading.
- [ ] Relative-height touch boundaries, NPC-server presence, sign/link early returns and queued events need targeted tests.
- [ ] Live setting changes, original-server equivalence and client-visible agreement remain unverified.
- [ ] G067's wider versioned option inventory remains open.

No dedicated option-matrix test was identified in the targeted test-tree
search. That is not a complete test census, and no tests were executed for
this source audit.
