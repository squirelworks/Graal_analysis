# Reference-fork ghost-mode options: from read keys to effects

Date: 2026-11-21. Evidence: **[srv]** for the pinned GPL reference-fork source;
**[doc]** for the earlier published documentation lead. No client, server or test was run.

## Scope of the G067 correction

The [Nov 11 wiki cross-check](../client-internals/graal-wiki-crosscheck-2026-11-11.md)
listed `ghostmodeenabled` among examples the reference server did not read at that time.
This audit reuses that published lead; it is not a fresh wiki fetch or a recount of all
99 options. It follows that key and its coupled `ghostmodefornotstaff` setting in
[seihai-gserver-v2 at `0cf8f83d`](https://github.com/squirelworks/seihai-gserver-v2/tree/0cf8f83d0ac658299abb4a9c93dab99cca805f37).
The fork's newer [option-gap note](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/bin/docs/server-options-gaps.md)
already identifies this pair as implemented. The source chain below checks what that means.

Both keys are Boolean settings, defaulting to false. They are registered with the setting
tracker, read by the player-appearance predicate and consumed by actual packet/property
builders. They are therefore more than accepted configuration with no effect in this
pinned source. The wider 99-option reference table remains open. No GPL code or source
table is reproduced, and no behavior is transferred to a permissive implementation. **[srv]**

## Selection policy

With ghost mode disabled, the appearance predicate selects nobody, regardless of the
second flag. When enabled with the non-staff flag set, it selects only non-staff players.
When enabled without that restriction, it selects everybody, including staff. **[srv]**

The staff predicate looks up the account in the server's staff list, case-insensitively;
an unavailable list yields false. This branch is not a test of an arbitrary rights bitmask.
The appearance method reads the current cached flag values before applying the policy.

References: [Server.h](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/Server.h),
[Server.cpp](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/Server.cpp),
[GhostMode.h](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/utilities/GhostMode.h),
[Player.cpp](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/Player.cpp).

## Concrete consumers

- During client login, the selected player receives an empty `PLO_GHOSTMODE` followed by
  `PLO_GHOSTTEXT` with the corner label "Ghost Mode". The routine returns for an unselected
  player or a non-client connection; it does not emit a disabling mode packet on that branch.
- The other-client property builder appends a trailing GANI override named `ghostani` for a
  selected player. The same helper is used for relevant other-player property broadcasts.
  This helper changes the serialized other-player view rather than assigning a new stored
  own-player gani value.
- The level-entry path sends `PLO_GHOSTICON`. Its presence value is set when the supplied
  level's player collection contains an eligible client; null entries and non-clients are
  skipped. The scan is gated by the enabled setting.
- Entry and departure paths refresh nearby clients' icons. Recipients of that refresh are
  selected through the existing synchronization-range path. **[srv]**

References: [PlayerProps.cpp](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/PlayerProps.cpp),
[PlayerClient.cpp](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/PlayerClient.cpp).

## Validation and limits

The existing [GhostMode test definitions](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/Catch_tests/ServerOptions/GhostMode_tests.cpp)
check the two declared keys, false defaults, tracked value changes, all eight Boolean
policy combinations and the extension-free ghost gani name. Their definitions were read;
this audit did not execute them. They do not by themselves prove client rendering or live
configuration-transition behavior.

- [x] Reconcile the named ghost-mode example with the current pinned reference source:
  defaults, registration, selection and concrete consumers are identified.
- [ ] Audit the remaining documented options with separate read/default/effect/stub status.
- [ ] Establish original-server equivalence, per-client rendering, collision and live-toggle
  behavior separately before extending this source contract.

G067 remains partially answered. A key being tracked is not a general proof of an implemented
feature; this pair has the additional consumer chain described above. The finding does not
reclassify other keys or replace a full versioned configuration reference.
