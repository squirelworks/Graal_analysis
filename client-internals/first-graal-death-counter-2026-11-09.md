# Static death-counter increment in exact 1st Graal

## Input and provenance

The subject is the 654,336-byte Windows x86 1st Graal input, researcher-supplied SHA-256 `03d8121711f41ac7b5a6e3fe549145d8fdfd44d22040f6706329ae83c6a1a37b`, MD5 `07452f8941fdfcdce878b035156e701c`. Evidence record `GRAAL-FIRST-MOVEMENT-20261109-01` and its retained-record digest are registered in [the evidence index](../docs/evidence-index.tsv). The record also contains a separate movement investigation.

Input identity, instruction checks and retained-record digest are researcher-supplied. The editor reviewed the address-free original-prose handoff only, without inspecting the executable, raw instructions or private record. This documentation does not independently verify binary provenance.

## Counter transition

`[bin]` The heart-change path selects the dead life state and clears the shared counter when hearts are not above zero. In the player updater, the dead-state branch increments that counter only while it is below 30. Starting from the death path's zero value, it therefore rises to 30 and stops.

`[bin]` This supplies the previously unlocated increment and cap in the [earlier matrix note](../version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin). Its existing dead-sprite and restart-key predicates require the same shared counter to exceed 27. The new static path connects those predicates to the counter's progression; it does not change the earlier restart destination, hearts or drawing evidence.

## Verification and limits

`[bin]` The researcher rechecked the executable digest and reviewed the heart-change and player-updater x86 instructions independently of recovered pseudocode. The two paths link death-state selection, counter clearing, the increment and its upper bound. No client or server was executed for this read.

- [x] ~~Locate the exact 1st Graal dead-state counter increment and cap.~~
- [ ] Measure elapsed death timing and updater cadence separately.

The counter values are static state-transition evidence, not a newly measured duration in seconds. No result is generalized to 1.39 or another build merely because its counter also reaches 30.
