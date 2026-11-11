# NPCs, baddies, weapons and script in Linux 3.04

Date: 2026-11-07. Static read of the Linux `graalexe` 3.04 decompile. Nothing was run. Tags as in [README.md](README.md).

These units are `graal/npcs.cpp`, `graal/baddies.cpp`, `graal/weapons.cpp`, `graal/scriptfunctions.cpp` and the list helpers in `graal/convertedclasses.cpp`. The level file stores the bodies; this is what the client does with them. **[bin]**

## Triggers

Placing a copy of an NPC onto a level fires the trigger `playerenters` when the caller asks for it and the local player exists. The same name is fired from the local player on a level change ([304-adventure.md](304-adventure.md)). Other trigger names compiled in `npcs.cpp` are `created`, `timeout`, `waspelt`, `sparringzone`, `movementfinished` and `washitnpc`. **[bin]**

A body with no image name is filled from `sword1.png`, `sword2.png`, `sword3.png`, `sword4.png`, `shield1.png`, `shield2.png`, `shield3.png` or `head0.png`, and a head name is completed with `.png`. Player-like animations in this unit are `bomy_idle`, `bomy_walk` and `bomy_kick`, under the prefix `bomy_`. One compiled script signature is `(S;S;S)S`. **[bin]**

## Baddies and weapons

`baddies.cpp` gives baddy types 3 and 4 their own surface and loads `wbow1.png` into it. Other types drop that surface. The death sound named here is `compudead.wav`. **[bin]**

`weapons.cpp` cuts one rectangle out of a list of rectangles: any overlap is split into the pieces that remain, and the original rectangle is removed. Where a computed weapon name would be empty, the unit writes the name `Back`. **[bin]**

## Script helpers

`scriptfunctions.cpp` implements the verbs that touch the world from a script. The name `shapetiletypes` is the grid of tile values: the first two numbers are the width and height in tiles, and the values come from the script list or from an existing buffer. A show-image verb whose case is the polygon case creates the `polygon` object that `showimgs.cpp` also builds ([304-draw.md](304-draw.md)). Sounds played from this unit are `bomb.wav`, `thunder.wav`, `axe.wav` and `sword.wav`. **[bin]**

`convertedclasses.cpp` is the list and string layer the other Graal units call (index, append, compare). Turning a bare name into a file path uses the name's first two characters as the directory when those characters are accepted, and the directory `special` otherwise, then appends `.txt`. **[bin]**

## Retained local numeric and string helper branches

[bin] This addition is scoped to the archive-labelled Linux 3.04 fixed/obsolete identical x86 analysis ELF, SHA-256 `6e9e35a3ef1320e9705db382ea3184cec07cfce5cac9fb2a550d79fe41931e86`. The retained original packed input is separately identified as `7901897411ffcee7b72806d5d021d0b42f5670739ad2ed97467fc86bc75690d0`. Finding `V3-GRAAL-04` records selected local Graal value-helper branches; it is not a complete language conversion specification.

[bin] The reviewed numeric accessor returns zero for a null input. For a nonnull input, the reviewed type/slot-absent branch reads a stored double; the alternative dispatches through a type-specific function slot. This distinguishes a local fallback from type-specific conversion. It does not prove that every uninitialized script variable defaults to zero, identify every runtime type or establish what all type-specific implementations return.

[bin] The helper identified in the review as the string-result accessor dispatches through a type-specific function slot or invokes a fallback initializer. The retained statement establishes that branch distinction, not an empty-string default or an exact output format. The behavior and storage lifetime supplied by those implementations remain unresolved.

[bin] A separate reviewed assignment helper includes scalar and numeric-array paths, including element conversion and selected index-guarded writes. The retained summary does not specify a complete array/index contract. It supplies no general numeric rounding, exceptional-value policy, parsing grammar or guarantee for unreviewed index cases.

[inf] These local helper observations must remain separate from the [Torque code-word integer-to-string operation](linux-304-seven-operation-contract.md#operations-and-their-limits), which already has a signed-decimal static contract. Neither that operation nor these value helpers establishes a registered native callback's result adapter, calling convention, ownership or lifetime. This addition does not specify a generic Graal interpreter or transfer modern GS2 behavior into 3.04.

### Evidence and remaining conversion gaps

[doc] The existing note describes the broader script/list/string layer; the new precision is limited to the selected local branches above. `V3-GRAAL-04` in the actual retained `graal-findings.json` cites original carrier keys `V3-GRAAL-SRC-09`, `V3-GRAAL-SRC-10` and `V3-GRAAL-SRC-15`. Publication preparation reads and hashes the structured review and approved identity document; it does not reopen raw functions, assembly or executable bytes. The underlying static assertions and executable identities remain researcher-supplied.

The source IDs `LNX304-LOCAL-VALUES-FINDINGS-DOC` and `LNX304-LOCAL-VALUES-IDENTITIES-DOC` resolve through [the source index](../docs/evidence-index.tsv). Their digests identify owner-held documents rather than newly materialized native captures. No raw code, native addresses, original assets or private access information is included.

- [x] ~~Record the selected local numeric/string fallback and assignment branches without treating them as full coercion semantics.~~
- [ ] Establish type-specific implementations, exact formatting, rounding/exceptional values, parser behavior and storage lifetime separately.

This is a document-only review of retained static findings. No original client, debugger, provider or implementation build was run; server and server commit are none. No runtime conversion or rendered result is asserted.
