# Per-version script packet guards (193/132/133 vs 197/140)

Date: 2026-11-16

Server → client compiled-script delivery uses two eras of message ids. A
server must gate by the **client profile's handled PLO set**, the same way
RC and the Seihai suite already gate other packets — not by a loose "v4" /
"v6" nickname alone.

Tags: **[bin]** · **[inf]** from those reads · **[srv]** open-server
behaviour as contrast only.

## Hard rules

| Rule | Why |
|---|---|
| **Never** send **132**, **133** or **193** to a build that dropped them | 5.24r4 and later (including 6.x) have no receive case; the client ignores the id **[bin]** |
| **Never** send **197** or **140** to a build that never had them | pure 4.x (through 4.20r8) has no receive case **[bin]** |

Era shorthand used in leads: "never 132/133/193 to **v6**", "never 197/140
to **v4**". The implementable form is the table below, keyed off each
profile's `plo` set (seihai-core rows mirror the binary reads).

## Which builds handle which ids

| Id | Name (gs2lib / core) | Handled by | Dropped from |
|---|---|---|---|
| 193 | `PLO_WEAPONHASH` | 4.04r2 through 5.12 (Win + Mac) | 5.24r4 |
| 132 | `PLO_UNKNOWN132` / weapon bytecode | 3.153 through 5.12 | 5.24r4 |
| 133 | `PLO_UNKNOWN133` / class bytecode | 3.153 through 5.12 | 5.24r4 |
| 140 | `PLO_NPCWEAPONSCRIPT` | 5.00r7 onward (incl. 5.12 and 6.x) | — (not on 4.x) |
| 197 | `PLO_LOADSCRIPT` | 5.00r7 onward | — (not on 4.x) |

Sources: `protocol/unknown-ids-2026-11-06.md` (132/133/193),
`protocol/v4x-clients.md`, `protocol/v5x-clients.md`,
`protocol/v5v6-windows-unpacked.md` (drop of 132/133/193 at 5.24; 140/197
present from 5.00r7), `protocol/v6x-clients.md`,
`protocol/class-bytecode-v4.md`.

## Two delivery paths

| Path | Proactive | Client ask | Body |
|---|---|---|---|
| **Classic** (3.153–5.12) | 193 (weapons only) | 158 weapons / 161 classes | 132 / 133 behind `PLO_RAWDATA` |
| **Modern** (5.24 onward; also available on 5.00r7/5.12) | 197 cache descriptor | 158 on miss | 140 body (`GRESCR01` when cached) |

A third-party lead that stock GServer-v2 was "version-gated the wrong way"
is the motivation for these asserts: a modern-only push to 4.20r8 is
useless, and a classic push to 6.03r7 is dropped. **[bin]** on the
handlers; **[srv]** on stock server habits.

## Transitional 5.00r7 / 5.12

Those builds **handle both** sets. Preferring classic while 193/132/133
are still present matches seihai-gserver's profile gate today. Which path
a stock 5.x client *needs* for a given world (CLASS prop vs empty line vs
158 ask) is a separate open question — do not treat it as closed by these
guards alone.

## What a server should do

1. Resolve the connection's client profile once (token → version row).
2. Send classic ids **only** when the profile's `plo` set contains them.
3. Send modern ids **only** when the profile's `plo` set contains them.
4. Prefer classic when both are present, until a lab says otherwise for
   that build.
5. Do not use 193 as a class announce; classes use 133 (or 197/140 on the
   modern path). See `class-bytecode-v4.md`.

## Classic weapon delivery on 4.20r8, step by step (2026-11-25)

Static read of the 4.20r8 engine, with 5.12 for contrast; nothing run. Follow-up to G324/G325. **[bin]** unless marked.

- **193** (`PLO_WEAPONHASH`: GINT5 CRC-32, then the weapon name) is ignored unless a weapon of that name already exists, and while ghost mode is on. The cache file is `weblevels/weapons/<server>/<weapon>.code`; the server name only selects the folder. The CRC-32 is computed over the decrypted compiled script. On a match the client installs the cached script and `onCreated` fires at once. On a miss it sends `PLI_UPDATESCRIPT` (158) with the name; in offline mode it calls a launcher hook instead.
- **132** answers 158: name length, name, then the compiled script. It has the same two gates (weapon must exist, ghost mode off). It writes the cache file, installs the script and fires `onCreated`. A compiled script normally contains newline bytes, so 132 has to travel inside `PLO_RAWDATA` (100). 133 and 196 are not this path, and neither 102 nor 33 can carry a compiled script.
- **Cache file format.** A 4-byte length, then 8-byte blocks, then an 8-byte check value that must equal the sum of the decrypted blocks. Each block is DES-encrypted with its own key from a small pseudo-random generator seeded by a hash of the lower-cased weapon name. The plaintext is the raw compiled script, with no `GRESCR01` header (that is the 5.x/6.x cache wrapper). Whether the DES key bits are reversed, as in the 2.05 gani cipher, needs a known cache file to confirm; the file-name escape rule is also open.
- **5.12** keeps 132 and 193 and adds 140/197, so both paths work there; 196 is unhandled in 5.12. Its cache file format was not re-read.

Recipe for a server delivering a compiled weapon script to 4.20r8:

1. Ghost mode (170) off.
2. 33 adds the weapon; it must exist before 193 or 132.
3. Optionally 193 with the CRC-32 and name. On a hit the client is done; on a miss it sends 158.
4. 132 with name and compiled script, inside 100.
5. The compiled script must avoid opcodes the 4.20r8 VM lacks (54, 121 and other 5.x/6.x-only ones) and must not carry the 6.x 140 header. **[bin]** for the missing handlers, from G324.
6. All of this before 190 if the weapon needs the login events ([G325](v4-login-account-contract.md#login-event-order-for-login-weapon-authors-g325-2026-11-25)).

## Evidence limits

- No new Wine/lab capture for this note; the id ranges are from the
  existing binary passes cited above.
- Offline / ghost skips on 132/193: on 4.20r8 ghost mode drops both, and offline mode routes a 193 miss to a launcher hook instead of 158 (section above). Other builds remain unread.
- CRC-of-source vs CRC-of-cached-bytes traps on stock servers are
  out of scope here (weapon-cache notes).

## Cross-links

- `protocol/class-bytecode-v4.md` — 161 → 133
- `protocol/unknown-ids-2026-11-06.md` — receive behaviour for 132/133/193
- `client-internals/v4-420r8-class-surface.md` — engine surface reminder
- `formats/gwebl001-cache.md` / `formats/linux-6x-class-cache.md` — 197 era
