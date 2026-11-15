# Class bytecode on the v4 path (PLO 133)

Date: 2026-11-16

How a classic GS2-capable client (3.153 through 5.12, including **4.20r8**)
gets a joined class script. This is the path `this.join("classname")` uses
when the client does not already hold that class. It is **not** the later
`PLO_LOADSCRIPT` (197) / `GRESCR01` path that starts at 5.24.

Tags: **[bin]** client binary · **[lab]** loopback lab · **[srv]** open
server source as behaviour only · **[inf]** inferred from those.

## Verdict

| Direction | Id | Layout | Role |
|---|---|---|---|
| C→S | 161 `PLI_UPDATECLASS` | `i5` CRC of the client's stored class body (0 when it has none), then the class name as the rest | ask for the class |
| S→C | 133 `PLO_UNKNOWN133` (beta4 name `PLO_CLASSBYTECODE`) | behind `PLO_RAWDATA`: `GCHAR` name length, name, then the compiled class bytecode (or name only for an empty stand-in) | deliver the class |

For **4.20r8** and the other 3.153–5.12 builds that still handle 133, the
server answers a 161 with **raw 133**, not with 197 and not with the weapon
cache pair 193/132. **[bin]**

## Client → server (161)

Layout in the packet tables is written as `i5 modtime` + name. On the class
path the five bytes are a **zlib CRC-32 of the client's stored body**, not a
file modification time. **[bin]**

- Windows 5.00r7: on a class cache miss the helper sends logical 161 with
  that checksum and the name
  (`client-internals/windows-404r2-500r7-static-2026-11-09.md`). **[bin]**
- Linux 6.x: the same 161 shape on a class cache miss
  (`formats/linux-6x-class-cache.md`). **[bin]**
- An authored vector with a non-zero stored-body CRC and name `fixture`
  packs the CRC as five GINT5 digits after the id byte, then the name and
  a newline (exact bytes in
  `client-internals/windows-404r2-500r7-static-2026-11-09.md`). **[inf]**
  from that reading.

When the client has **no** stored body for the name (cold join, first
`this.join`, or a cleared list after 194), the CRC field is **0**, so the
request is `i5 0` + name. **[inf]** from the checksum field's meaning; the
v4 receive path for 133 does not write a weapons-style `.code` cache file
(see below), so a 4.x join routinely asks with 0. **[bin]** on 133 vs 132.

A third-party lead that "161 always sends crc=0" is therefore **too strong
as a universal rule** (5.x/6.x send the stored-body CRC when they have one)
but **matches the practical v4 join case** that seihai must answer.

## Server → client (133)

Read in Windows 4.04r2 and 5.12 and compared with Mac 3.153
(`protocol/unknown-ids-2026-11-06.md`, 2026-11-12). **[bin]**

- Body: `str name` (`GCHAR` length + bytes), then the rest is the compiled
  class script. Shorter than name+1 is dropped.
- The client adds the name to its class list if new, creates or finds the
  class object, loads the bytecode, and marks `public.` functions as
  callable from outside. The object holds `joinedclasses`.
- A body that is only the name is an **empty** class (useful when the
  server has no such class, so `join` still completes).
- **Handled by:** 3.153 (Mac), 4.04r2, 4.20r6, 4.20r8, 5.00r7, 5.12.
- **Not** 5.24r4 or later: those drop 132, 133 and 193 together; compiled
  scripts move to 197 + `GRESCR01` (`formats/gwebl001-cache.md`).

Unlike 132 (weapon bytecode), the 133 reader traced for 4.04r2 does **not**
write a `weblevels/weapons/<name>.code`-style file before installing the
script. **[bin]** So v4 class delivery is one-shot over the wire; it is not
the weapon hash-and-ask loop.

## How this differs from weapons (193 / 158 / 132)

| | Weapons (v4) | Classes (v4) |
|---|---|---|
| Proactive hash | 193 with CRC of the bytecode file | none |
| Client ask | 158 `PLI_UPDATESCRIPT` (name only) | 161 with CRC + name |
| Body | 132 behind `PLO_RAWDATA` | 133 behind `PLO_RAWDATA` |
| Disk cache on 4.x | yes (`.code`, checked by 193) | not on the 133 path traced |

A server that answers a class ask with 197/140 on 4.20r8 is on the wrong
era path. A server that answers 161 with 132 is wrong too. **[bin][inf]**

## What a v4-capable server should do

1. Read 161: five-byte CRC, then the class name.
2. If the world has that class and the client's CRC equals the zlib CRC-32
   of the bytecode that would be sent, send nothing.
3. Otherwise, for a build that reads 133 (and `PLO_RAWDATA`), send 133 with
   the name and bytecode (whole compiled file, including the compiler's
   trailing newline, same rule as 132).
4. If the world has no such class, send 133 with the name only (empty
   class), still on the v4 path — not a 5.x empty-197 stand-in.
5. Do not send 133 to builds that dropped it (5.24 on).

World layout used by open GServer-v2 sample servers: class sources live as
`scripts/<name>.txt` (file stem = class name, file body = script text).
That is a folder name observed in sample trees, not a licence to copy
server code. **[file]**

## Evidence limits

- No new 4.20r8 Wine lab of 161→133 was run for this note; the receive
  layout and build range are from the 2026-11-12 binary pass, and the 161
  CRC field from the 5.00r7 / Linux 6.x static reads cited above.
- Whether Mac 3.153 also keeps any on-disk class body cache was not read.
- `UPDATEGANI` (157) is a sibling ask, not covered here.

## Cross-links

- `protocol/unknown-ids-2026-11-06.md` — 132/133 receive behaviour
- `protocol/packet-ids.md` — id table rows
- `client-internals/windows-404r2-500r7-static-2026-11-09.md` — 161 CRC field
- `formats/linux-6x-class-cache.md` — 161 on 6.x; 197 era
- seihai-gserver `docs/PARITY.md` — "Classes…" row (implementation target)
