# Show-images, the particle emitter, and GS2 `indexof` and `format`

Date: 2026-11-12. These are static reads of two engines; nothing was executed. Evidence ID: `SHOWIMG-PARTICLES-FORMAT-20261112`.

The two engines are the Windows 4.20r8 GraalEngine.dll (version resource 4.2.0.8) and the Linux 6.03 x64 client. The 6.03 image is the clearer read, so most behaviour below is taken from it. Where this note says "4.2.0.8", that engine was checked as well. Names in quotes are the engines' own script-facing names and help strings. Tags: **[bin]** is read from the binary, **[help]** is the engine's own help text for that property, and **[inf]** is inferred.

The test cases are the 4.04r2 main menu's own calls: four `GuiShowImgCtrl` objects, one actor with body-part images, and one emitter with three modifiers. The GS2 core thread holds them as a disassembly extract. That extract is project-only and not in this repo.

## GuiShowImgCtrl and TShowImg

- A `GuiShowImgCtrl` owns a single `TShowImg`. The control has no picture code of its own: on every draw it moves its show-image and draws it. **[bin]**
- **Placement.** The show-image is placed at the control's screen position plus (`offsetx`, `offsety`), in screen pixels. The control repositions it only when that position has changed. If the show-image is a particle emitter, the emitter moves with it. **[bin]**
- **Order.** The control draws its show-image first and its child controls after it, so children are on top. **[bin]**
- **Hit test.** For one show-image kind, a mouse hit only counts where the picture itself is hit. **[bin]** That kind is probably the plain image, and the per-pixel alpha rule is probably what decides a hit. **[inf]**
- `clipchildren` and `clipmove` are ordinary control properties. The help text notes that turning clipping off can be useful for a `GuiShowImgCtrl`. **[help]**
- **The control's own properties.** The 6.03 property string for `GuiShowImgCtrl` adds `red`, `green`, `blue`, `alpha`, `mode`, `style` and `rotation` on top of the show-image. **[bin]**
- **Drawing an ani.** When a show-image draws an ani, the property `playerlook` decides where the body images come from. With `playerlook` true (the default), the ani takes head, body, sword, shield and `attr[]` from the owner. Set `playerlook` false to supply them through `showimg.actor.head`, `showimg.actor.body` and the like. **[help]**
- **The 4.04r2 menu.** That menu gives StartAni1 an `actor` with an `attr` array, so it is the `actor.*` case. **[inf]**
- **`mode`.** For a show-image and for each particle, `mode` picks the blend: 0 add, 1 transparent (normal alpha), 2 subtract, 3 day-night. **[help]**
- **Particle blend state.** A particle with default colour and mode 0 or 1 is drawn without changing the blend state. Any other colour, alpha or mode sets the blend first. **[bin]**

## The emitter: `TParticleEmitter`

### Properties

The 4.2.0.8 engine registers the same names that 6.03 uses. **[bin]**

`attachposition`, `autorotation`, `checkbelowterrain`, `clippingbox`, `cliptoscreen`, `continueafterdestroy`, `currentparticlecount`, `delaymin`, `delaymax`, `dropemitter`, `dropwateremitter`, `emissionoffset`, `emitatterrainheight`, `emitautomatically`, `emittedparticles`, `firstinfront`, `isfrozen`, `maxparticles`, `movementfactor`, `nrofparticles`, `particle`, `particletypes`, `wraptoclippingbox`

It has these methods: `addglobalmodifier`, `addlocalmodifier`, `addemitmodifier`, `advancetime`, `emitat`, `removemodifiers` and `removeparticles`.

The behaviours in the table below were read from the emitter's update, emit and draw code. Which stored field each script-facing name writes was matched by behaviour, not read from the property table. So every name-to-behaviour pairing here is **[inf]**, except `nrofparticles`, `maxparticles` and the counters, which the emit code makes unambiguous.

| Property | What it does | Tag |
| --- | --- | --- |
| `emitautomatically` | When true, the emitter fires bursts on its own. | [bin] |
| `delaymin`, `delaymax` | Seconds between bursts. After each burst, the next delay is drawn uniformly from [`delaymin`, `delaymax`]. The first tick only starts the timer, so the first burst comes one delay after the emitter starts. | [bin] |
| `nrofparticles` | Particles per burst. Each burst emits `min(nrofparticles, maxparticles − currentparticlecount)`. | [bin] |
| `maxparticles` | The cap on live particles. A particle that finds the live count over the cap is removed. | [bin] |
| `currentparticlecount`, `emittedparticles` | Live count, and the running total emitted. | [bin] |
| `particletypes`, `particle` | Each emitted particle copies one template from the type list, picked at random when there is more than one. `particle` is the template being edited. | [bin][inf] |
| `emissionoffset` | {x, y, z} added to the emitter's position for each new particle, multiplied by the emitter's movement scale (below). If the emitter has a turn angle, the x/y part of the offset is rotated by it. | [bin] |
| `attachposition` | When true, a particle's position is relative to the owner and is drawn at owner position plus particle position. | [bin] |
| `emitatterrainheight` | New particles start at the terrain height plus the offset z (3D). | [bin] |
| `movementfactor` | The scale described below. | [inf] |
| `clippingbox`, `wraptoclippingbox`, `cliptoscreen` | A particle that leaves the box (or the screen, when there is no box) is removed. With wrap on, it is moved by whole box widths back inside instead. The help text says one clipping flag disables all clipping to screen and box. | [bin][help] |
| `checkbelowterrain` | Particles under the terrain are lifted to it, or removed (3D). | [bin] |
| `firstinfront` | Draw order (see below). | [bin] |
| `isfrozen` | When true, nothing moves or emits. | [bin] |

The emitter keeps one scale factor. It multiplies the emission offset, each particle's per-second move (`movex`, `movey`, `movez`) and the add modifier on `x`, `y` and `z`. **[bin]** That scale is probably `movementfactor`. **[inf]**

### Particle fields

The modifier variable list gives the fields a modifier can change, in this order (index 0 to 17):

`x, y, z, movex, movey, movez, angle, zangle, speed, rotation, spin, stretchx, stretchy, red, green, blue, alpha, zoom` **[bin]**

| Field | Meaning | Tag |
| --- | --- | --- |
| `lifetime` | Seconds. A particle dies when its age reaches this. | [bin] |
| `angle`, `zangle`, `speed` | Direction and speed. Together they make the movement vector `movex`, `movey`, `movez` (help: "particle movement vector (angle + zangle + speed)"). Angles are in radians; the 4.04r2 menu uses `2*pi`. | [help][inf] |
| `movex`, `movey`, `movez` | Per-second movement. Each frame, position += dt × move × the emitter scale. | [bin] |
| `rotation`, `spin` | Drawing rotation in radians, and its change per second (rotation += spin × dt). With the emitter's `autorotation` on, rotation follows the movement angle instead. | [bin] |
| `stretchx`, `stretchy`, `zoom` | Drawing scale. | [bin] |
| `red`, `green`, `blue`, `alpha` | Drawing colour, from 0 to 1. | [bin][inf] |
| `image`, `mode` | The picture and the blend (see `mode` above). | [help] |
| `sound` | A sound played when the particle is emitted. If several are given, one is picked at random. | [bin][help] |

### Modifiers

All three methods take the signature `sffssff`. **[bin]**

`addXmodifier(type, time1, time2, field, operation, min, max)`

- `type` is one of `once`, `impulse` or `range`.
- `operation` is one of `replace`, `add` or `multiply`.
- `field` is a name from the list above.
- The engine refuses an unknown type, and it caps a list at 1000 modifiers. **[bin]**

Each time a modifier fires, the value it uses is drawn uniformly from [`min`, `max`]. `range` is the exception: it interpolates instead (see below). **[bin]**

| Operation | Effect on the field | Tag |
| --- | --- | --- |
| `replace` | field = value | [bin] |
| `add` | field = field + value. For `x`, `y` and `z` the value is first multiplied by the emitter scale. | [bin] |
| `multiply` | field = field × value | [bin] |

| Type | When it fires | Tag |
| --- | --- | --- |
| `once` | One time only. The fire time is drawn from [`time1`, `time2`] seconds after the modifier's clock starts. After firing it never fires again. | [bin] |
| `impulse` | First at a time drawn from [`time1`, `time2`] seconds, then again after each new delay drawn from the same range. | [bin] |
| `range` | Every frame while the particle's age is between `time1` and `time2`. `replace` sets the field to the linear interpolation of `min` to `max` over that span; after `time2` it is `max`. `add` adds the interpolated value × dt each frame, so it acts as a per-second rate. `multiply` does nothing in a `range` modifier. Only the first non-multiply field entry of a `range` modifier is applied each frame. | [bin] |

Which method you call decides whose clock the modifier runs on and what it changes. **[bin]**

| Method | Clock | Changes |
| --- | --- | --- |
| `addlocalmodifier` | Each particle gets its own clock, started when it is emitted. | That particle. |
| `addglobalmodifier` | One clock shared by the emitter. When it fires, the change is applied to every live particle in that frame, and the clock is then re-armed (`impulse`) or switched off (`once`). | Every live particle. |
| `addemitmodifier` | The emitter's clock. | The particle-type templates, so it changes particles emitted later. |

`removemodifiers()` clears the modifier lists. **[bin]** Whether it clears all three lists or only some of them was not separated. **[inf]**

**Worked examples** from the 4.04r2 menu's emitter (StartAni4):

- `addglobalmodifier("impulse", 0.2, 0.2, "spin", "multiply", 0.9, 0.9)`: every 0.2 s, every live particle's spin is multiplied by 0.9, so spinning slows by 10% five times a second.
- `addlocalmodifier("once", 0, 0, "angle", "add", -0.2, 0.2)`: at birth, each particle's direction is turned by a random amount between −0.2 and 0.2 radians.
- `addlocalmodifier("once", 0, 0, "rotation", "replace", 0, 2*pi)`: at birth, each particle gets a random drawing rotation.

All three readings are **[inf]**, worked from the rules above.

### Draw order

- New particles are put at the front of the emitter's list. **[bin]**
- With `firstinfront` false (the default), drawing starts at the oldest particle and ends at the newest, so newer particles are on top. With `firstinfront` true, drawing starts at the newest, so the oldest are on top. **[bin]**
- Sub-emitters attached to an emitter are drawn before its own particles. **[bin]**
- An emitter with exactly one particle type of the plain kind takes a batched path. It draws in the same list order. **[bin][inf]**

## GS2 opcode 82: `indexof`

Stack before: `…, list, value`. Stack after: `…, index`. **[bin]** (4.2.0.8)

- The `list` slot is used as an object directly; the opcode does not resolve it. The compiler converts it to an object first.
- When `list` has no members, or is not an object, the result is −1.
- Otherwise the opcode resolves `value` and searches by its type:
  - a number uses float equality;
  - a string uses string equality;
  - an object uses object identity.
- Any other value type gives −1.
- The result is a number: the 0-based index, or −1. It replaces the `list` slot.
- At least two stack slots are required; with fewer, the opcode faults like any other short-stack opcode.

The original read did not open the case-comparison helper; the later selected read and published lab reconciliation below supply the bounded answer. **[bin][lab]**

## GS2 opcode 84: `format`

Stack before: `…, marker, argN, …, arg1, fmt`. This is the compiler's usual reversed argument order with the type-0 marker below. Stack after: `…, result` (a string, in the marker's slot). **[bin]** (4.2.0.8, 6.03)

- The opcode looks down the stack for the nearest marker. If none is found, the stack is emptied.
- If the marker is on top (no format string), the result is the empty string.
- Otherwise the top slot is converted to text and used as the format string. The arguments are read downward from the slot under it.

The formatter is Graal's own, not the C library's. **[bin]** (6.03 conversion letters read directly; 4.2.0.8 has the same structure)

- **Flags:** `+` forces a sign, `-` left-justifies, and `#` sets an alternate form.
- **Width and precision:** a decimal width, then `.` and a precision. Each is capped at 120.
- **Positional arguments:** `n$` picks argument `n`. Arguments read after it continue from that point.
- **Length:** one `l` is accepted and ignored.

| Conversion | Output |
| --- | --- |
| `%%` | A literal `%`. |
| `%d`, `%i` | A signed integer. Precision pads with zeros; width pads with spaces. |
| `%u` | An unsigned integer. |
| `%x`, `%X` | Hexadecimal in lower or upper case. |
| `%c` | One character from the integer value. |
| `%f` | A decimal number. |
| `%s` | A string. Precision truncates it; width pads it with spaces. |
| Any other letter | Consumed, and prints nothing. |

**Missing arguments.**
- When the arguments run out, the argument reader returns nothing. `%s` then prints an empty string, still padded to the width. `%d`, `%i` and `%u` print `0`. **[bin]**
- `%f` with no argument behaves like a zero value. **[inf]** Its number reader was not opened.
- A positional `n$` past the last argument is also treated as missing. **[bin]**
- Extra arguments are ignored. **[bin]**

The original read did not open the integer path; the selected Linux read below supplies its epsilon-biased rule and domain limits. **[bin]**

## Selected Linux 6.03r7 mechanisms and published lab reconciliation

Date: 2026-11-22. Evidence ID: `LNX603-LIST-FORMAT-20261122`. This is a new selected static read of a separately identity-bound Linux 6.03r7-labelled x64 carrier, using instruction and exact data-record checks with independent review. It does not retrospectively identify the November 12 static inputs or the executables used by the published November 20 labs. No new original-client run was performed. **[bin]**

The selected opcode 82 string route passes a query string to a list helper. It visits element indices in ascending order, obtains each element's string representation through its virtual interface, and returns the first matching zero-based index or −1. The equality helper requires equal recorded lengths and, apart from identical-storage or empty-string shortcuts, compares the bytes exactly; it performs no case folding itself. This is a string-representation comparison, not proof that arbitrary original member values preserve their source spelling. Other value tags and normalization paths are outside this selected read. **[bin]**

The selected opcode 84 `%d` route uses the custom formatter's integer callbacks for both sequential and explicit-position arguments. For an already numeric value, each adds `0.0001` to the binary64 payload, truncates toward zero, then corrects a negative fractional result downward. Thus the bounded rule is `floor(y)`, where `y` is the evaluated binary64 sum `x + 0.0001`, provided `y` is finite and `floor(y)` fits signed 32-bit. This is neither nearest rounding nor unqualified truncation or floor of the original `x`. The selected static route does not establish exceptional conversions, nonnumeric coercion grammar, all integer-output limits or every conversion letter. **[bin]**

Published labs already answer the original observable questions at their named-build scope; they are cited as reports, not as new runs or byte-identical specimens:

- `removemodifiers()` stopped the emit-template zoom impulse, retained the template's last value and removed live particles while emission and the cumulative count continued, on 4.20r8, 5.12, 5.24r4 and 6.03r7. **[lab]** ([second batch](../protocol/lab-appe-hosta-2026-11-20b.md#particle-modifiers-e210)).
- Global `once` values of 2, 3 and 6 seconds took effect within one 0.5-second observation step after addition on 4.20r8, 5.12 and 6.03r7, including later additions. The report calls this first-frame behavior; it does not measure an internal clock origin or sub-step latency. A pre-particle addition had no visible effect, and `impulse` followed its interval. The report does not assign these timing results to 5.24r4. **[lab]** ([second batch](../protocol/lab-appe-hosta-2026-11-20b.md#particle-modifiers-e210)).
- Case-distinguishing list samples and signed `%d` samples are reported on 4.20r8/5.12 and Linux 6.03r7. The Linux report uses `.index()` for opcode 82, not a source method named `.indexof()`, and includes `2.9999` → `3`. Its negative `%i` sample distinguishes floor from truncation; the earlier positive `%i(3.7)` → `3` sample alone does not. These samples agree with the new selected mechanism without proving carrier identity or all exceptional domains. **[lab][bin]** ([first batch](../protocol/lab-appe-hosta-2026-11-20.md#format-and-indexof-e210); [Linux report](static-reads-appendix-e-2026-11-20-hostb-final.md#format-and-list-lookups-on-603r7-e210-partial)).

The particle-kind selector remains unresolved. The Linux report's unfinished particle scene does not negate the separate positive modifier batch. Overall Appendix E#210 remains partial. **[lab][inf]**

## Not settled

- [x] ~~Whether `removemodifiers()` clears the emit list as well as the local and global ones.~~ Answered for the four reported lab builds in the [reconciliation](#selected-linux-603r7-mechanisms-and-published-lab-reconciliation).
- [x] ~~The predicted first-frame global `once` behavior.~~ Answered at the published three-build, 0.5-second observation scope in the [reconciliation](#selected-linux-603r7-mechanisms-and-published-lab-reconciliation); exact internal clock origin is not measured.
- [ ] The exact particle kinds: image, ani and text. The help string "store its own data (good for text emitters)" shows a text kind exists.
- [x] ~~Case handling in `indexof` string search, and `%d` rounding.~~ Published named-build samples and the separately bound selected Linux mechanism are reconciled [above](#selected-linux-603r7-mechanisms-and-published-lab-reconciliation); exceptional domains and other routes remain outside that answer.
