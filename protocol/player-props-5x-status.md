# Player-prop parsers on 5.00r7 / 5.12 — status

Date: 2026-11-16. Research-list rank **#6** (focus 5.007, 5.120). Points at the completed case-set read; **no new jump-table pass or two-client prop lab** this pass.

Tags: **[bin]** case sets and the selected reader extent below; **[inf]** complete value-width and pyreborn leads still open.

## Settled (case sets)

Canonical note: [`v5-props.md`](v5-props.md) (2026-11-13 static).

| Stream | 5.00r7 / 5.12 (same as 5.30r3 / 5.31r4) | vs 4.x |
|---|---|---|
| self (PLO 9) | 0–32, 34–49, 52, 54–74, 78–**82**; skip-unknown as one byte | **+82** only |
| other (PLO 8) | 0, 2, 8–13, 15–21, 23, 24, 30–76, 78–**82**; unknown ends stream | **+82** only |
| NPC (PLO 3) | 0–47, 53–77 | unchanged from late 4.x set in that note |
| baddy (PLO 2) | 0–10 | unchanged |

- **82** on other players: one length byte (−32) then that many bytes → string on the player; self hands 82 to the other-player parser. Server name `COMMUNITYNAME` is **[srv]**; the string read is **[bin]**.
- **77** still not parsed in 5.x (ends other-player stream; one-byte skip in self).
- 6.x native parsers and the 6.1.1.3 `tclient_set*props` bridge are in the same note / [`v6-props.md`](v6-props.md) — out of #6’s focus but adjacent.

Identity reminder: a folder labelled “5.12 untouched” is **5.00r7** re-versioned ([`launchers-420r8-500r7-512.md`](../client-internals/launchers-420r8-500r7-512.md)). Genuine 5.12 engine is `Graal3DEngine.dll`. **[bin]**

## Selected appearance-reader extents (2026-11-22)

A retained archive-labelled 5.00r7 backup input gives a bounded sword/shield consumption result (evidence `W500-APPEARANCE-READERS-20261122`). The label is not authenticated stock/vendor provenance or runtime identity, and this input does not establish the genuine 5.12 reader. **[bin]**

For these two properties, the selected shared reader uses one value byte when its unsigned byte minus 32 is below 10. Otherwise its nominal value extent is two bytes plus the nonnegative declared image length: the first value byte, a length byte and the image bytes. The length is the unsigned length byte minus 32, clamped at zero for this cursor calculation. These extents exclude the property ID. The own-player parser independently calculates the same nominal extent before forwarding the selected property prefix to shared application; the top-level self and other parsers are not identical. **[bin]**

The image substring helper bounds the selected image slice by available text. This is distinct from the declared cursor advancement: the selected outer guards do not prove that the entire extended value is present, strict truncation rejection or safe arbitrary-byte consumption. Compact preset-image cases cover sword 1–4 and shield 1–3, but being below the reader discriminator alone does not establish semantic power. That discriminator is not interchangeable with a historical sender's bias. **[bin]**

This is a selected static extent, not the complete self/other width table, P6 semantic resolution, rendering/healing behavior or a runtime alignment result. Other properties, other specimens and genuine 5.12 remain open. **[bin][inf]**

## Additional selected reader extents (2026-11-22)

The same archive-labelled backup input supports the following additional nominal extents (evidence `W500-PLAYER-EXTENTS-20261122`). Every value extent below excludes the property ID; adding that ID gives the nominal record extent. Available-data slicing remains distinct from cursor advancement. These are selected reader branches, not a complete table or a result for genuine 5.12. **[bin]**

- **Head image (logical 11):** with `p` equal to the unsigned first value byte minus 32, the value extent is one byte for `p < 100`; otherwise it is `1 + (p - 100)`. The custom image length is encoded in that discriminator, without another length byte. **Body image (logical 35)** instead uses one length byte followed by the declared nonnegative image length. Actual image assignment and named property getters bind these identities. Own-player code calculates matching nominal extents before shared application. This does not establish asset existence or rendering. **[bin]**
- **Strings (logical 0 and 10):** both use one length byte plus `max(unsigned length byte - 32, 0)` string bytes. Logical 0 reaches a common string consumer; exact nickname naming is not independently established by this read. Logical 10 reaches an animation-loading attempt, not guaranteed loading or rendering. Own logical 0 calls the common consumer directly; logical 10 uses shared application after a separate cursor calculation. Delimiter/argument semantics remain outside this result. **[bin]**
- **Colors (logical 13):** both selected readers consume five value bytes. The update loop requires the full six-byte record including ID, but the declared cursor remains fixed even when that guard prevents updates. Named property/getter storage and the numeric collection setter bind the color identity. No five-versus-eight selector appears in these selected branches; their relationship to PLO 177 remains unestablished. This is not a whole-client absence claim or a palette/rendering result. **[bin]**
- **Paired scalar forms (logical 15/16 and 78/79):** the first pair consumes one value byte, the second two. Corresponding setter/reference-getter pairs establish that these are alternative forms for two components, but this read does not independently name the components X/Y or bind numerical units. Conversion to stored floating values is separate from wire extent. The own-player parser applies these cases directly; shared equality suppression preserves the two-byte nominal extent. **[bin]**
- **Optional image-string holder (logical 21):** both readers select one length byte plus `max(unsigned length byte - 32, 0)` string bytes. The stored string reaches a sprite-image selection path, but this read does not independently establish an exact native property name. Own and shared update gates differ; the own empty-string path also has additional state changes. Equal nominal extents do not imply identical application or successful image loading/rendering. **[bin]**
- **Conditional unnamed field (logical 23):** with `p` equal to the unsigned first value byte minus 32, the value extent is five bytes only when `p > 0`; otherwise it is one. Negative decoded values take the short path too. The selected shared branch chooses the cursor extent without establishing a color/effect consumer or the meaning of the remaining bytes. Own code delegates the long prefix, but that is not a semantic binding. **[bin]**

Substring clipping and selected update guards do not prove complete malformed-stream safety or successful alignment. Stock/vendor provenance, runtime identity, genuine 5.12, the full width census and the broader P4–P6 questions remain open. **[bin][inf]**

## Selected coordinate conversion and storage (2026-11-22)

A further read of the same archive-labelled backup binds the conversion constants and a selected concrete shared receiver (evidence `W500-COORDINATE-DISPATCH-20261122`). It does not authenticate a distribution, establish runtime identity or transfer the result to genuine 5.12. **[bin]**

For logical 15/16, the unsigned value byte minus 32 is multiplied by 0.5. For logical 78/79, the combined integer is 128 times the first unsigned value byte plus the second, minus 4128. The reader arithmetic-shifts this signed integer right once, multiplies by 1/16, then negates the result when the combined integer's low bit is set. Sign/magnitude shorthand therefore needs a nonnegative combined integer; it is not the exact rule for arbitrary raw bytes. The optional reference component is added in the selected branches. Assembly passes both words of the resulting 64-bit value to the setter, rather than only the low word suggested by recovered C. None of this changes the nominal one/two-value-byte wire extents or proves arbitrary malformed-input safety. **[bin]**

For the shared handler's newly constructed receiver, the allocation/constructor/vtable/application chain binds the first pair (15/78) to exported `getx` and the second (16/79) to exported `gety`. Their getters read double storage updated by the concrete setter chains. Those setters also maintain relative caches and propagate to a member list; their full effect is not merely storing the incoming value. This binds x/y for that selected new-object path, not the dynamic types of own-player, already-existing shared or optional reference objects. Tile/pixel units, reference/map conventions, dirty-state meaning and rendering remain unestablished. **[bin]**

This is static conversion/storage evidence, not a movement experiment, complete property table or resolution of P4–P6. **[bin][inf]**

## Selected logical 177 dispatcher binding (2026-11-22)

The same selected backup's constructed connection decodes the logical message ID from the first message byte. Its direct dispatch and queue-drain routes preserve that ID. For logical 177, the selected translation and jump-slot data bind the dispatch to its default return path, with no intervening selected handler call. This resolves the selected static mapping rather than relying on the absence of a recovered switch arm. **[bin]**

That route supplies no color-mode handler to connect with the separately examined five-value player-colors reader. It does not establish whole-client packet177 absence, another ID's equivalence, all connection subclasses or alternate paths, genuine 5.12, observed traffic, color rendering or runtime acceptance. P4–P6 remain open beyond this selected result. **[bin][inf]**

## Selected ordering and power-storage boundaries (2026-11-22)

Further static reads of the same archive-labelled backup qualify P5/P6 (evidence `W500-PROP-ORDER-POWER-20261122`). They do not authenticate a distribution or transfer the result to genuine 5.12. **[bin]**

The examined own/shared outer dispatch and common-advance paths reload the current ID and reset the extent for each iteration. Those regions and the direct player-property packet wrappers do not compare the current ID with a carried previous ID. The shared reader's unsupported-current-ID exit is a membership stop, not positive evidence of an ascending-order requirement. This does not prove order independence, descending-stream acceptance, a historical observation's cause or the absence of policy in handlers, callbacks, transport or other builds. P5 is not refuted by this bounded negative result. **[bin][inf]**

For shared logical 8/9, let a be the unsigned first value byte and p equal a minus 32. Both branches select compact representation when p is below 10 and pass p unchanged on that path. In extended representation, logical 8 subtracts an additional 30 from p, while logical 9 subtracts an additional 10. The representation threshold is therefore distinct from the numeric adjustment. This is receive-side arithmetic, not a sender encoder or a valid numeric range. Negative arithmetic results do not establish healing behavior. **[bin]**

For the already bound newly constructed shared receiver, concrete getter/setter slots agree with the named swordpower and shieldpower property-adapter paths. The selected setters store the full computed 32-bit word without a local clamp. Corresponding image holders agree with the named swordimg and shieldimg getter paths. These bindings do not establish active property registration or the same setter policy for every runtime object, nor damage, healing or rendering behavior. **[bin]**

The compact image routing selects four sword presets for decoded values 1–4 and three shield presets for 1–3; other compact values retain the initially empty image path. Extended image text uses its separate length and available-bounded slice. Image assignment and numeric storage converge, but neither successful asset loading nor gameplay follows from those stores. The nominal extents stay as recorded in the cursor census. Own-player concrete storage, existing/shared subclasses, sender behavior, genuine 5.12 and full P6 remain open. **[bin][inf]**

## Genuine 5.12 has the same widths (G173 / G098, 2026-11-25)

The genuine 5.12 engine and the unpatched 5.00r7 engine give every property the same value width, in all four streams: self
(PLO 9), other (PLO 8), NPC (PLO 3) and baddy (PLO 2). So the 5.00r7 numeric table in the
[cursor census](player-props-selected-backup-cursors-2026-11-22.md) also holds for 5.12. **[bin]**

Method: in both engines the four parsers were found by their switch (id byte minus 32 and its bound), and the case sets rebuilt
from the dispatch tables; they match `v5-props.md`. Each case handler was then compared instruction by instruction up to the
blocks shared by many cases, with addresses masked, called functions compared recursively, and offset-only differences (object
field and stack-frame offsets) kept apart from code changes. Each whole parser was also compared in straight-line order. **[bin]**

| Stream | Cases | Result |
|---|---|---|
| self | 76, plus 7 default ids | all identical; the two parsers differ only in call targets |
| other | 69, plus 14 default ids | 68 identical; id 11 differs in code but not in width |
| NPC | 73 | 34 identical; 36 differ only in object field and frame offsets (part of the NPC object moved 8 to 12 bytes); ids 1, 4 and 22 differ in code, all with the same width |
| baddy | 11 | whole parser and every callee equivalent |

The shared readers (character at cursor, substring, prefix removal that advances the cursor, and the string helpers) are
equivalent. There are no separate two- or three-byte reader functions: multi-byte values are decoded inline in the handlers,
which are part of the identical bodies. Callees that changed (the bomb setter used by self 7, image and gani loading, sound,
rendering, NPC image setters) act after the width is fixed. **[bin]**

The code differences:

- **Other 11 and NPC 22 (head image).** Same encoding in both: with `p` the first value byte minus 32, one byte naming
  `head<p>.png` when `p < 100`, otherwise `1 + (p - 100)` bytes holding the image name. 5.12 only builds the default
  `head0.png` name once and keeps it, where 5.00r7 uses a literal each time. **[bin]**
- **NPC 4.** Flagged only because a block it shares changed its field offsets; it reads one byte in both. **[bin]**
- **NPC 1 (script) — same width, different effect.** Both read a two-byte length `L = 128·a + b − 0x1020` (0 if negative) and
  then `L` bytes, so the record is `L + 3` bytes with the id. 5.00r7 stores the script when the NPC has none yet and goes on to
  its player-enters path. 5.12 never stores it: it only checks the text for the `sparringzone` marker (bare, or after
  `//#CLIENTSIDE`) and, on a match, sets a sparring-zone flag; any other script is dropped. This fits 5.1's removal of GS1
  ([gs1-commands-by-version](../npc-library/gs1-commands-by-version.md#512-no-gs1-command-table-2026-11-24)). Runtime effect not
  tested. **[bin][inf]**

Inputs: the unpatched 5.00r7 engine and a memory image of the genuine 5.12 engine (link date 2007-10-19). The census's 5.00r7
widths were spot-checked against the same 5.00r7 code (self 3 and 14, other 11, NPC 1) and agree. This pass proves equality; it
does not add an NPC or baddy width table. **[bin]**

## Sword and shield power on 4.20r8 to 6.03r7 (2026-11-25)

Sword (prop 8) and shield (prop 9) use the same wire form from 2.05 to 6.03r7, so P6 is settled for these builds. With `b` the value byte minus 32: below 10 is a bare preset, and from 10 up it is power + 30 (sword) or power + 10 (shield) followed by a length byte and the image. Healing swords −20..−1 go out as bytes 10..29. seihai-gserver-v2 PR #149 decodes and encodes this form. **[bin][lab]**

| Client | Receive | Send | Lab |
|---|---|---|---|
| 2.05 rev2 | threshold 10, −30 / −10 | sword byte clamped to 10..50 (power −20..20) | yes (PR #149) |
| 4.20r8 (engine 828e9311) | same | sword clamped to 10..50; byte 30 (power 0) goes as 0. Presets `sword1`–`sword4` and `shield1`–`shield3` go as bytes 1..4 and 1..3. Shield is capped at power 3 (byte 13); 10 or less goes as 0 | no |
| 5.00r7 (stock dde0fc85; 5.12 2D engine 1d100a7a is the same code) | same | same as 4.20r8 | no |
| 6.03r7 Linux x64 and Windows | same | as 4.20r8 but never uses the preset bytes: `sword1.png` power 1 goes as 31 + `sword1.png` | yes, two Linux clients |

- **Shield cap.** From 4.20r8 on, the client never sends a shield power above 3, whatever the script sets. The 6.03r7 lab sent 13 for powers 5 and 250. **[bin][lab]**
- **Clamped locally, not on the wire.** 6.03r7 keeps −25 or 25 as its own sword power and sends −20 or 20 (bytes 10 and 50). **[lab]**
- **Power 0 with an image** goes out as byte 0 on 4.x to 6.x, so the image is lost. **[bin]**
- **Receivers do not clamp**, so a server that sends a sword above 20 or a shield above 3 has it taken as is. **[bin]**
- **Lab:** two real Linux 6.03r7 clients on PR #149's server (`healswords=true`, `swordlimit=20`, `shieldlimit=255`). The client sent 27 + `heal.png` for −3, 10 for −20 and −25, 36 for 6 and 50 for 25. The server forwarded the same bytes to the second client, a client that joined later got the stored values, and the props after them were not shifted. **[lab]**
- **Writer addresses:** 4.20r8 0x1005ce71 / 0x1005d055; 5.00r7 0x100a2e5e / 0x100a3048; 6.03r7 Linux 0x507b90 / 0x507e8e, Windows 0x486465. **[bin]**
- **Open:** the send side of the genuine 5.12 3D engine (04f7a133) was not read; its receive side matches (above). 4.20r8 and 5.00r7 were not run in the lab.

## Still open for #6

A [complete selected own/shared cursor census](player-props-selected-backup-cursors-2026-11-22.md), with a numeric per-ID table, now records these two backup functions' dispatch membership, nominal extents, short guards and default behavior. It distinguishes own prefix-copy delegation from shared cursor advancement. This closes that selected static census only; the multi-build/genuine-5.12 checklist below and semantic/runtime questions remain open. **[bin][inf]**

| Question | Why | Next |
|---|---|---|
| ~~Per-id **value widths** beyond the ids named in `v5-props.md`~~ | Needed for safe encode / fuzz-free lab fixtures | Done for self and other: 5.00r7 census, and 5.12 identical ([above](#genuine-512-has-the-same-widths-g173--g098-2026-11-25)) |
| Two-client prop **diff** on the wire | Confirms other-player accept set live | **L** after #1 assets |
| Pyreborn leads **P4** COLORS 5↔8 via PLO 177; **P5** ascending-id stop; ~~**P6** sword/shield bias~~ | Leads only until our **S** | P6 done ([sword and shield](#sword-and-shield-power-on-420r8-to-603r7-2026-11-25)); P4, P5 open |

## Open checklist

- [x] ~~Publish a 5.00r7 / 5.12 per-id width table (self + other).~~ The 5.00r7 table is the [cursor census](player-props-selected-backup-cursors-2026-11-22.md); 5.12 has the same widths in all four streams ([above](#genuine-512-has-the-same-widths-g173--g098-2026-11-25)).
- [ ] Confirm or reject P4–P5 against that table / two-client capture. P6 is confirmed ([sword and shield](#sword-and-shield-power-on-420r8-to-603r7-2026-11-25)).
- [ ] Optional: unknown own-id long-value desync lab (called out in `v5-props.md`).
