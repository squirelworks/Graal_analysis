# Height transport: packet 185 and the reference server's gmap gates

Date: 2026-11-21. Tags: **[srv]** for a source audit of the GPL reference fork;
**[doc]** for existing original-client findings, not a fresh binary read or lab run.
This partially reconciles G228. It does not establish height delivery on 5.12 or 6.03r7.

## Separate the evidence scopes

The statement that nothing in the lab server sends heights is too broad.
The audited [seihai-gserver-v2 source at `4d1fb2f9`](https://github.com/squirelworks/seihai-gserver-v2/tree/4d1fb2f9dfc0916c43f74e136695b678344c8218)
contains a conditional height sender. The absence of a heights message in the earlier standalone
level experiment is consistent with its gates; it is not proof that original servers lack a
height transport. No GPL implementation code is reproduced here. **[srv]**

Separately, the existing [2.17/2.22/2.31 receiver table](../version-profiles/plo-layouts-217-231.tsv)
identifies `PLO_BOARDHEIGHTS` (185). It describes a gmap-cell target, six one-byte GCHAR fields,
then two bytes per height sample. That is prior original-client evidence, not evidence that the
same path has been reached in the modern builds or in the GR-V1.05 experiment. **[doc]**

## Reference-fork storage to sender

The following are necessary gates in the traced source path, not a complete audit of every
login, version or map-configuration rule. **[srv]**

- The binary loader calls its height-section parser only for format version greater than 4:
  GR-V1.05 enters it, GR-V1.04 does not. The text-level loader has a separate HEIGHTS branch.
  Both retain an 81-value override vector and clear it when the parsed count is not 81.
- Runtime terrain is created for a gmap only when the map's terrain seed list is nonempty.
  The loader copies the static level's height vector into that terrain's overrides.
- The player entry path sends boards when the level has not been entered in the session or
  the supplied cache time is older than the level modification time. Its sublevel path calls
  the board, layer and height senders. The fallback static-data path sends boards and layers
  without a height call.
- The height sender itself returns unless there is a map position, runtime terrain and a
  nonempty override vector. A standalone HEIGHTS block therefore does not by itself enable
  this gmap-oriented sender.

Source references: [LevelLoader.cpp](https://github.com/squirelworks/seihai-gserver-v2/blob/4d1fb2f9dfc0916c43f74e136695b678344c8218/server/src/loader/LevelLoader.cpp),
[PlayerClient.cpp](https://github.com/squirelworks/seihai-gserver-v2/blob/4d1fb2f9dfc0916c43f74e136695b678344c8218/server/src/player/PlayerClient.cpp),
[Level.cpp](https://github.com/squirelworks/seihai-gserver-v2/blob/4d1fb2f9dfc0916c43f74e136695b678344c8218/server/src/level/Level.cpp).

## Reference-fork serialization

Once those gates pass, the sender emits packet 185, with a fixed nine-by-nine override grid.
Its six GCHAR fields are map x, map y, block start x and y (both zero), and width-minus-one
and height-minus-one (both 8). The 81 samples follow in row-major order, two one-byte fields
per sample: the floored whole part plus 50, then the fractional part multiplied by 128.
These fields use the GCHAR-writing helper; they are not a little-endian 16-bit tile array
like packet 107. The body is 168 bytes before the packet id and outer framing. **[srv]**

The fork pins [gs2lib at `efaabb30`](https://github.com/squirelworks/seihai-gs2lib/tree/efaabb30b3b2744db9a4d8fdbb72ff1fa8644c19).
Its [CString byte insertion](https://github.com/squirelworks/seihai-gs2lib/blob/efaabb30b3b2744db9a4d8fdbb72ff1fa8644c19/include/CString.h)
uses [writeGChar](https://github.com/squirelworks/seihai-gs2lib/blob/efaabb30b3b2744db9a4d8fdbb72ff1fa8644c19/src/CString.cpp),
which clamps its unsigned byte input at 223 and adds 32. The serializer performs its numeric
casts before that helper. This audit does not specify valid out-of-range or nonfinite heights.

## Original receivers and unresolved mapping

The prior 2.x receiver finding decodes a sample as the first received byte minus 32 and 50,
plus the second received byte minus 32 divided by 128. It checks the gmap cell and writes
into that level's nine-column height grid from the supplied block start. See
[packet layouts](../protocol/packet-layouts.md) and the dedicated receiver table above. **[doc]**

File-reader support is a different gate. [Component-level findings](gmap-heights-by-component-2026-11-19.md)
show that gmap height parsing depends on the engine component. The
[5.00r7 cache experiment](gr-v105-500r7-cache-lab.md) did not round-trip the authored height
block; it did not prove transport absence. Neither result supplies a modern packet-185
receive-dispatch trace or a successful height rendering run.

- [x] Identify the reference fork's conditional height sender and distinguish it from standalone
  GR-V1.05 loading. **[srv]**
- [ ] Trace packet-185 receive dispatch and height consumption in exact 5.12 and 6.03r7 builds.
- [ ] Establish original-server serialization and the accepted transport for standalone level
  heights separately from the reference fork's gmap override path.
- [ ] Observe delivery, stored values and rendering independently with a qualified positive control.

G228 remains open for those modern/original and runtime questions. No packet implementation,
new lab result, or original-client equivalence is inferred from the GPL source contract.
