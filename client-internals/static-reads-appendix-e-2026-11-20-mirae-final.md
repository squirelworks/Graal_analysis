# Static reads and labs for Appendix E, last Mirae batch (2026-11-20)

Date: 2026-11-20. Evidence: **[bin]** (disassembler reads of the real client executables on the
Mirae lab) and, where a section says so, **[lab]** (a loopback run). Only behaviour is given here. Covers App.
E#203, E#507 and E#304.

## Bare `#5` and `#6` on 2.17.1 (E#203)

Static read of the 2.17.1 `Graal_2171.exe`, with the same code pattern then matched in 2.22, 2.31
and 2.05 rev 2. No debugger trace was needed.

**How 2.17.1 expands a message.** The registry has one entry per code name; each holds an argument
spec (`(R)` or none), a getter and an optional setter. `#5` and `#6` are each registered twice,
once with `(R)` and once bare, and both forms share one getter. A compiled message is a list of
parts, literal text and codes, joined by one evaluator:

1. Clear the result string.
2. For each part, evaluate it into one scratch string, then append that scratch string to the
   result.

The scratch string is set to empty once, when the evaluator starts, and is **not cleared between
parts**. A literal part and a getter that finds its value both overwrite it.

**Why the label repeats.**
- The `#5` getter reads the selected character's horse-image object. When there is none, it
  returns without writing anything. The `#6` getter does the same with the carried-NPC association.
- The scratch string then still holds the previous part's text, and the evaluator appends it again,
  so `07:[A` + `#5` + `B]` gives `07:[A07:[AB]`, as the lab saw.
- When the getter finds its object (sword `#1`, shield `#2` and body `#8` always have defaults), it
  writes the scratch string and the output is correct.

**Why 2.05 rev 2 shows nothing.** 2.05 rev 2 has no such evaluator. Its single dispatch finds the
first `#`, builds a fresh replacement string for that code, expands the rest of the text
recursively, and joins prefix, replacement and suffix. A code with no object leaves its own fresh
replacement empty, so nothing stale repeats.

**By build.** The same join loop, with the scratch string not cleared, is in 2.17.1, 2.22 and 2.31.
It is not in the 2.05 rev 2 `Graal.exe`.

**Predictions, not run.** Any registered code whose getter can skip the write should repeat the
previous part's text: `#1#5` with no horse should show the sword image name twice. A bare `#5` at
the very start of a message should come out empty.

## What 3.04 uses for tile types when no `addtiledef` arrives (E#507)

Static read of the UPX-unpacked Linux 3.04 `graalexe`. No 3.04-era server capture was available.

**There is no per-level tile-type table to fill on the default sheet.**
- When the player enters a level, a picker walks the tile-definition entries. It starts from image
  `pics1.png` and sheet type 0, then takes the entry of type 0, 1, 2 or 5 with the longest matching
  level prefix.
- The sheet type is one global value, not a per-level table. The picker first resets it to 0, so
  when no `tiledefs` file line and no `addtiledef` matches, the type stays 0 and the image stays
  `pics1.png`.
- The level keeps only its board of tile ids. On type 0 the walk test and the type tests look each
  id up in the compiled-in id lists (the lists equal to `arrays.dat`'s). Nothing per level is built
  from them.

**`tiletype(x, y)`** confirms this: on a type-0 sheet it returns −1 at once for every position. A
per-tile number exists only when an entry has given the level a non-zero type.

**What type 5 changes.**
- When the picker selects a type-5 entry, the client also sets a flag on the drawing side.
- With type 5 the walk test and the type tests ignore the board's tile ids completely. Walls, water
  and the other types come only from the level's object shapes (the `setshape2` cell values).
- With type 5, `tiletype` returns 0 wherever no object shape covers the spot.
- So type 5 means "this sheet's tiles carry no rules; only placed shapes do".

**Not settled.** Whether a 3.04-era server sent `addtiledef` at login (no capture was available),
and what the drawing-side type-5 flag changes on screen (its readers were not separated from other
uses of that field).

## Wire rounding of a position off the half tile, 2.22 (E#304)

**Static read** of the 2.22 `Graal_222.exe`, with 2.05 rev 2 for comparison **[bin]**.
- The player-props writer's case for prop 15 takes the player's x (or the segment x on a gmap),
  multiplies it by 2.0 and calls a helper that adds 0.0001 and converts to an integer with the FPU
  forced to round-to-nearest. It then adds 32 and writes one byte. Prop 16 is the same code for y.
- So the byte is `nearest(2x + 0.0001) + 32`: in practice the nearest half tile, ties going up.
  30.25 sends 30.5 and 30.24 sends 30.0. It is not truncation or floor.
- 2.05 rev 2 writes the same byte as `floor(2x + 0.5 + 0.0001)`, the same rule written another
  way; the two differ only within 0.0001 of a tie.
- 2.22 has a second helper of the same shape that forces round-down. It is not used for props 15
  and 16.

**Lab check, 2.22** (`GNW03014`), online against the loopback lab gserver behind the probe proxy
**[lab]**. For each value pair an injected one-line GS1 NPC ran `playerx = X; playery = Y;` and
echoed `#v(playerx) #v(playery)` into the chat, so the client reports what it holds; the props
message that carries that chat also carries the prop 15 and 16 bytes.

| Set (x, y) | Client holds | Sent x | Sent y |
| --- | --- | --- | --- |
| 30.25, 30.75 | 30.25, 30.75 | 30.5 | 31.0 |
| 30.24, 30.26 | 30.23999, 30.25999 | 30.0 | 30.5 |
| 30.1, 30.4 | 30.09999, 30.39999 | not sent (still 30.0) | not sent (still 30.5) |
| 30.6, 30.9 | 30.59999, 30.89999 | 30.5 | 31.0 |
| 0.25, 30.25 | 0.25, 30.25 | 0.5 | 30.5 |
| 30.75, 31.25 | 30.75, 31.25 | 31.0 | 31.5 |
| 29.74, 29.76 | 29.73999, 29.75999 | 29.5 | 30.0 |
| 30.5, 30.0 | 30.5, 30.0 | 30.5 | not sent (still 30.0) |
| 30.3, 30.7 | 30.29999, 30.7 | not sent (still 30.5) | 30.5 |
| 30.2, 30.8 | 30.2, 30.79999 | 30.0 | 31.0 |

- Every value fits round to nearest, ties up. Truncation or floor would have sent 30.0 for y
  30.26, 30.5 for y 30.9, 0.0 for x 0.25 and 30.5 for x 30.75; none of those happened.
- A prop is sent only when its rounded byte changes; otherwise the client sends the chat alone.
- The client stores its own position in fixed point, so 30.24 reads back as 30.23999. That moves
  no value across a rounding edge here.
- In the same message the lab world's GS1 weapon set flags `gr.x` and `gr.y` (id 18) to the
  rounded values.

**What did not work.** The first two runs sent nothing: the injected script text held newline
bytes, and a newline ends a message on the 2.x wire. One-line scripts fixed it.

**Not done.** Negative x (it would leave the level), and the client's own 0.1 nudges at a corner
with a non-half-tile value; scripted positions stand in for them.

## Client-to-server ids of the six Graal 2002 builds (E#15, send sites)

Static read of the six Graal 2002 executables (ver7, ver8, ver9, ver10, ver13, v22), with 2.05 rev
2, 2.1 test 3, 2.17.1 and 1.41 rev 1 as controls **[bin]**.

**Method.** The connection object's send method is a virtual call with the id in one register and
the body in another (as the login builder shows). Every call through that slot whose id is a
constant set just before the call was listed. On 2.05 rev 2 this gives exactly 0–24, 26–30, 32–38,
80 and 81, the set already in the per-build table, so the method is sound for this compiler. Every
build also has the same number (9) of send calls whose id is in a register (forwarders such as the
UDP twins), so no build hides an extra constant sender behind one of them.

| Build | Token | Ids sent (constant send sites) | Count |
| --- | --- | --- | ---: |
| 2.05 rev 2 (control) | `GNW03081` | 0–24, 26–30, 32–38, 80, 81 | 39 |
| 2.1 test 3 (control) | `GNW03081` | 0–24, 26–30, 32–38, 80, 81 | 39 |
| ver7 | `GNW03081` | 0–6, 9, 10, 12–14, 18, 19, 21–24, 26–30, 32–38, 80, 81 | 32 |
| ver8 | `GNW03081` | as ver7 | 32 |
| ver9 | `GNW03081` | as ver7 | 32 |
| ver10 | `GNW31101` | ver7's set plus 39 | 33 |
| ver13 | `GNW31101` | as ver10 | 33 |
| v22 | `GNW31101` | 0–24, 26–30, 32–39, 80, 81 | 40 |
| 2.17.1 (control) | `GNW22122` | 0–24, 26–30, 32–39, 41, 43–45, 80, 81 | 44 |
| 1.41 rev 1 (control) | `GNW13110` | 0–24, 26–30, 32, 33, 80, 81 | 34 |

**What the sets show.**
- ver7 to ver13 have no send site for 7, 8, 11, 15, 16, 17 and 20: horse add and delete, throw
  carried, baddy props, baddy hurt, baddy add and open chest. This matches their receive side,
  which routes the baddy, chest and horse ids to the default branch: the early Graal 2002 world
  had no horses, baddies, chests or thrown objects, in either direction.
- v22 has all seven back; its set is 2.05 rev 2's plus 39.
- 39 (the tamper check) is first sent by ver10, with the token change. The v22 lab login already
  showed 39 (10 bytes) sent right after the language message.
- 41 and 43 to 45 come after v22: 2.17.1 has them, no Graal 2002 build does.

**The token does not predict the send set.** No 1.41 build shares a token with these builds (1.41
rev 1 has its own token and an older set without 34 to 38). ver7 to ver9 share `GNW03081` with
2.05 and 2.1 test 3 but lack seven of their ids; ver10 and ver13 share `GNW31101` with v22 but lack
the same seven. Only v22 equals a neighbour plus one id. This confirms the manual's rule not to
borrow rows by token.

**Not done.** No lab run checked these sends: a send site shows that the client can send an id,
not when it does. The default-route fixtures stay open.

## `format` and list lookups on 6.03r7 (E#210, partial)

Native Linux 6.03r7, online against the loopback lab world behind the probe proxy **[lab]**. A GS2
level NPC, compiled with the Seihai compiler and delivered as bytecode, wrote each result into the
player chat, which was read from the client's props messages.

| Expression | Result |
| --- | --- |
| `format("%d", 2.7)` | `2` |
| `format("%d", -2.7)` | `-3` |
| `format("%d", 2.5)` | `2` |
| `format("%d", -0.5)` | `-1` |
| `format("%i", -2.7)` | `-3` |
| `format("%d", 2.9999)` | `3` |
| `format("%u", -2.7)` | `4294967293` (−3 as unsigned 32-bit) |

- **`%d` and `%i` floor; they do not truncate.** −2.7 gives −3. 2.9999 giving 3 suggests the same
  small upward bias as the client's biased-floor helper (inferred from that one value). This
  agrees with the GwenTea2 floor result on 4.20r8 and 5.12.

| Expression | Result |
| --- | --- |
| `{"a","B","c"}.index("B")` | `1` |
| `{"a","B","c"}.index("b")` | `-1` |
| `"abc".index("B")`, `"abc".index("b")`, `"abc".index("abc")`, `"abc".index("ABC")` | all `-1`: a plain string is not searched as a list |
| `"abc".pos("B")` / `"abc".pos("b")` | `-1` / `1` |
| `.indexof(...)` on a string or a list | `0` every time: 6.03r7 has no method of that name, and an unknown method gives 0 |

- **Lookups are case-sensitive.** Opcode 82 is `.index()`.

**Particles: not finished.** Emitters ran in every scene: the client's own counters read 8 live and
8 emitted after 1.5 s, and `particletypes = 2` read back as 2. A local `once` modifier on `x` with a
−2 to 2 range spread the particles about ±2 tiles, so particle x and y are in tiles. The kind
screenshots were unusable: the lab session came up without its tile layer (all 4 retries) and the
client then never cleared the frame, so every scene showed stale pixels. A rerun with a background
image was stopped when research ended, so the particle kinds, `removemodifiers()` and the timing of
a global `once` were not observed.

## Items not run in this batch

- E#324: a denser 2.05 frame capture of sword against sword was mid-run when research ended and
  was stopped; no spark sprite was found.
- E#325: sample files were staged, but nothing was played.
